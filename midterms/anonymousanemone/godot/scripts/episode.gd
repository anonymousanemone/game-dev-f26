## Evaluation adapter around the actual Dangers scene. It does not create a replacement level.
extends RefCounted
const DT := 1.0 / 60.0
const FRAMES_PER_ACTION := 6
const STEP_LIMIT := 1200
const CASES := ["spell31", "spell32", "spell32_low"]
## A look at the heka word (the human's click on it) leaves the controls idle this many actions
## (1.0 s) while the note is read. Assumed, not measured: a stand-in for human reading time.
const LOOK_STEPS := 10
const LOOK := {"move": 0, "face": 0, "thrust": false, "heka": false, "look": true}
var game
var status := "ongoing"
var reason := ""
var steps := 0
var invalid_actions := 0
var case_id := "spell31"
var notes := []          ## what the player has read and would remember (the heka rule, once looked at)
var reach_flag := false  ## experiment setting: add `in_reach` to each crocodile
var _seen := {}          ## visible snouts at the previous observation: crocodile id -> [x, clock]

func _init(scene) -> void:
	game = scene
	game.set_meta("fixed_step", true)
	game.set_process(false)
	game.set_process_unhandled_input(false)
	# Headless Godot has no window and reports a square viewport, which narrows the arena
	# (its width follows the viewport's aspect). Use the project's own base size instead.
	if DisplayServer.get_name() == "headless":
		game.get_tree().root.size = Vector2i(ProjectSettings.get_setting("display/window/size/viewport_width"),
			ProjectSettings.get_setting("display/window/size/viewport_height"))

## `speed_scale` multiplies every wave's crocodile speed (difficulty sweeps; 1.0 = as tuned). It is an
## evaluation setting chosen by the caller of reset, not something a player controls. Spell 31's
## single slow lesson crocodile (`first_speed`) is not scaled. `lives` (bites the bearer can take)
## and `crocodiles` (how many to turn back; one-wave encounters only, 0 = as tuned) are likewise
## evaluation settings for longer experiments. `reach_flag` adds `in_reach` to each crocodile.
func reset(seed: int, situation := "spell31", speed_scale := 1.0, lives := 3, crocodiles := 0, reach_flag := false) -> Dictionary:
	if situation not in CASES: return {"error": "unknown_case"}
	if crocodiles > 0 and situation == "spell31": return {"error": "crocodiles_needs_one_wave"}
	game.reset()
	game.hud.dismiss_intro()
	game.rng.seed = seed
	game.set_meta("episode_won", false)
	game.set_meta("midterm_controls", {"move": 0, "face": 0, "thrust": false, "heka": false})
	status = "ongoing"
	reason = ""
	steps = 0
	invalid_actions = 0
	notes = []
	_seen = {}
	self.reach_flag = reach_flag
	case_id = situation
	var e: Dictionary = game.ENCOUNTERS[0 if situation == "spell31" else 1]
	game.avatar.position.x = game.rects[e.spear].get_center().x
	game._update_camera(1.0)
	game.start_fight(e)
	if speed_scale != 1.0 or crocodiles > 0:
		game.fight.waves = game.fight.waves.map(func(w):
			var scaled: Dictionary = w.duplicate()
			scaled.speed = w.speed * speed_scale
			if crocodiles > 0: scaled.count = crocodiles
			return scaled)
	game.fight.health = lives
	# The human "Press [space] to start" wait is presentation; agents start in the fight as before.
	if game.fight.tut == "start": game.fight.tut = ""
	game.say("Scribe", game._hints.text("dangers." + e.id, "instructions"))
	# Skip only presentation time, preserving the original spawn-spacing checks (_instant stays false).
	game._kill_fight_tweens()
	game._croc_open(1.0)
	game.avatar.set_process(false)
	if situation == "spell32_low": game.fight.pos.y = game.fight.y_range.y
	game._place_bearer()
	game._update_camera(1.0)
	game._place_frame()
	return observe()

func legal_actions(player_id := 0) -> Array:
	if status != "ongoing" or player_id != 0: return []
	var actions := []
	for move in [-1, 0, 1]:
		for face in ([-1, 0, 1] if game.fight.both else [0]):
			for thrust in [false, true]:
				for heka in [false, true]:
					actions.append({"move": move, "face": face, "thrust": thrust, "heka": heka})
	actions.append(LOOK.duplicate())
	return actions

func step(player_id: int, action: Variant) -> Dictionary:
	if player_id != 0: return {"error": "unknown_player"}
	if status != "ongoing": return {"error": "episode_terminal", "outcome": outcome()}
	steps += 1
	_seen = _visible_snouts()
	# `look` is optional; when true the other controls are ignored (the hands are off the keys).
	var valid: bool = action is Dictionary and action.size() == (5 if action.has("look") else 4) and action.has_all(["move", "face", "thrust", "heka"])
	if valid and action.has("look"):
		valid = typeof(action.look) == TYPE_BOOL
	if valid:
		valid = typeof(action.thrust) == TYPE_BOOL and typeof(action.heka) == TYPE_BOOL and typeof(action.move) in [TYPE_INT, TYPE_FLOAT] and typeof(action.face) in [TYPE_INT, TYPE_FLOAT]
	if valid:
		valid = (action.move == -1 or action.move == 0 or action.move == 1) and (action.face == 0 or (game.fight.both and (action.face == -1 or action.face == 1)))
	var looking: bool = valid and action.get("look", false)
	var controls := {"move": 0, "face": 0, "thrust": false, "heka": false}
	if valid and not looking:
		controls = action.duplicate()
		controls.erase("look")
	elif not valid: invalid_actions += 1
	game.set_meta("midterm_controls", controls)
	if looking:
		game.read_heka()
		if not game.hud._text in notes: notes.append(game.hud._text)
		steps += LOOK_STEPS - 1
		_advance(LOOK_STEPS * FRAMES_PER_ACTION)
	else:
		if controls.thrust: game._croc_thrust()
		_advance(FRAMES_PER_ACTION)
	game.overlay.queue_redraw()
	if steps >= STEP_LIMIT and status == "ongoing":
		status = "limit"
		reason = "step_limit"
	return {"valid": valid, "observation": observe(), "outcome": outcome()}

func _advance(frames: int) -> void:
	for frame in frames:
		if status != "ongoing": break
		game._time += DT
		game._update_fight(DT)
		for tween in game._fight_tweens.duplicate():
			if tween.is_valid(): tween.custom_step(DT)
		game._update_camera(DT)
		game._place_frame()
		if game.get_meta("episode_won", false):
			status = "won"
			reason = "all_crocodiles_defeated"
		elif game.fight.lost:
			status = "lost"
			reason = "three_bites" if game.fight.health <= 0 else "word_stolen"

## Would the spear's stroke, from where it rests to full extension, touch this crocodile where it
## is now? The game's own strike test (`_croc_strike`) at the current position, without predicting
## where the crocodile will be when a thrust lands.
func _in_reach(c: Dictionary) -> bool:
	var tip0: Vector2 = game.fight.pos + game._tip_offset()
	var tip: Vector2 = tip0 + game._spear_dir() * game.CROC_THRUST * game.unit
	var h: Vector2 = game.crocodiles._snout(c)
	if Geometry2D.get_closest_point_to_segment(h, tip0, tip).distance_to(h) < game.crocodiles.CROC_REACH * game.unit:
		return true
	for i in 5:
		if game.crocodiles._on_croc(c, tip0.lerp(tip, i / 4.0)): return true
	return false

func _visible_snouts() -> Dictionary:
	var at := {}
	for c in game.fight.get("crocs", []):
		if c.s == "crawl" and c.node.modulate.a >= 0.1:
			at[c.node.get_instance_id()] = [game.crocodiles._snout(c).x, game.fight.clock]
	return at

func observe(player_id := 0) -> Dictionary:
	if player_id != 0: return {"error": "unknown_player"}
	var visible := []
	for c in game.fight.crocs:
		if c.s != "crawl" or c.node.modulate.a < 0.1: continue
		var snout: Vector2 = game.crocodiles._snout(c)
		var size: Vector2 = c.node.get_meta("size")
		visible.append({"snout": [snout.x, snout.y], "direction": c.dir, "red": c.red, "width": size.x, "height": size.y,
			"id": c.node.get_instance_id()})
		if reach_flag: visible[-1].in_reach = _in_reach(c)
	var tip: Vector2 = game.fight.pos + game._tip_offset()
	# Derived only from what is on screen: offsets from the spear tip, the side, and time to reach
	# the bearer at the motion seen since the previous observation (null until it has been seen moving).
	for v in visible:
		var x: float = v.snout[0]
		v.dx_from_tip = x - tip.x
		v.dy_from_tip = v.snout[1] - tip.y
		v.side = "left" if x < game.fight.pos.x else "right"
		v.seconds_to_bearer = null
		var was = _seen.get(v.id)
		if was != null and game.fight.clock > was[1] and absf(x - was[0]) > 0.0:
			v.seconds_to_bearer = (game.fight.pos.x - x) * v.direction / (absf(x - was[0]) / (game.fight.clock - was[1]))
		v.erase("id")
	var direction: Vector2 = game._spear_dir()
	return {"case": case_id, "time": game.fight.clock, "step_seconds": FRAMES_PER_ACTION * DT,
		"health": game.fight.health, "killed": game.fight.killed, "total": game.crocodiles._croc_total(),
		"both_sides": game.fight.both, "player_y": game.fight.pos.y, "player_x": game.fight.pos.x,
		"y_range": [game.fight.y_range.x, game.fight.y_range.y], "facing": game.fight.facing,
		"tip": [tip.x, tip.y], "spear_direction": [direction.x, direction.y],
		"thrusting": game.fight.thrust >= 0, "tutorial": game.fight.tut,
		"heka_word_glowing": game.fight.get("heka_on", false), "notes": notes.duplicate(),
		"message": game.hud._text, "crocodiles": visible}

func outcome() -> Dictionary:
	return {"status": status, "terminal": status != "ongoing", "reason": reason,
		"score": game.fight.get("killed", 0), "steps": steps, "invalid_actions": invalid_actions}
