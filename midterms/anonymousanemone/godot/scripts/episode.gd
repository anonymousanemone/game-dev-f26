## Evaluation adapter around the actual Dangers scene. It does not create a replacement level.
extends RefCounted
const DT := 1.0 / 60.0
const FRAMES_PER_ACTION := 6
const STEP_LIMIT := 1200
const CASES := ["spell31", "spell32", "spell32_low"]
var game
var status := "ongoing"
var reason := ""
var steps := 0
var invalid_actions := 0
var case_id := "spell31"

func _init(scene) -> void:
	game = scene
	game.set_meta("fixed_step", true)
	game.set_process(false)
	game.set_process_unhandled_input(false)

func reset(seed: int, situation := "spell31") -> Dictionary:
	if situation not in CASES: return {"error": "unknown_case"}
	game.reset()
	game.hud.dismiss_intro()
	game.rng.seed = seed
	game.set_meta("episode_won", false)
	game.set_meta("midterm_controls", {"move": 0, "face": 0, "thrust": false, "heka": false})
	status = "ongoing"
	reason = ""
	steps = 0
	invalid_actions = 0
	case_id = situation
	var e: Dictionary = game.ENCOUNTERS[0 if situation == "spell31" else 1]
	game.avatar.position.x = game.rects[e.spear].get_center().x
	game._update_camera(1.0)
	game.start_fight(e)
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
	return actions

func step(player_id: int, action: Variant) -> Dictionary:
	if player_id != 0: return {"error": "unknown_player"}
	if status != "ongoing": return {"error": "episode_terminal", "outcome": outcome()}
	steps += 1
	var valid: bool = action is Dictionary and action.size() == 4 and action.has_all(["move", "face", "thrust", "heka"])
	if valid:
		valid = typeof(action.thrust) == TYPE_BOOL and typeof(action.heka) == TYPE_BOOL and typeof(action.move) in [TYPE_INT, TYPE_FLOAT] and typeof(action.face) in [TYPE_INT, TYPE_FLOAT]
	if valid:
		valid = (action.move == -1 or action.move == 0 or action.move == 1) and (action.face == 0 or (game.fight.both and (action.face == -1 or action.face == 1)))
	var controls := {"move": 0, "face": 0, "thrust": false, "heka": false}
	if valid: controls = action.duplicate()
	else: invalid_actions += 1
	game.set_meta("midterm_controls", controls)
	if controls.thrust: game._croc_thrust()
	for frame in FRAMES_PER_ACTION:
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
	game.overlay.queue_redraw()
	if steps >= STEP_LIMIT and status == "ongoing":
		status = "limit"
		reason = "step_limit"
	return {"valid": valid, "observation": observe(), "outcome": outcome()}

func observe(player_id := 0) -> Dictionary:
	if player_id != 0: return {"error": "unknown_player"}
	var visible := []
	for c in game.fight.crocs:
		if c.s != "crawl" or c.node.modulate.a < 0.1: continue
		var snout: Vector2 = game.crocodiles._snout(c)
		var size: Vector2 = c.node.get_meta("size")
		visible.append({"snout": [snout.x, snout.y], "direction": c.dir, "red": c.red, "width": size.x, "height": size.y})
	var tip: Vector2 = game.fight.pos + game._tip_offset()
	var direction: Vector2 = game._spear_dir()
	return {"case": case_id, "time": game.fight.clock, "step_seconds": FRAMES_PER_ACTION * DT,
		"health": game.fight.health, "killed": game.fight.killed, "total": game.crocodiles._croc_total(),
		"both_sides": game.fight.both, "player_y": game.fight.pos.y, "player_x": game.fight.pos.x,
		"y_range": [game.fight.y_range.x, game.fight.y_range.y], "facing": game.fight.facing,
		"tip": [tip.x, tip.y], "spear_direction": [direction.x, direction.y],
		"thrusting": game.fight.thrust >= 0, "tutorial": game.fight.tut,
		"message": game.hud._text, "crocodiles": visible}

func outcome() -> Dictionary:
	return {"status": status, "terminal": status != "ongoing", "reason": reason,
		"score": game.fight.get("killed", 0), "steps": steps, "invalid_actions": invalid_actions}
