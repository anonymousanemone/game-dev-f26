## Direct engine fixtures, not human or agent playtest evidence.
extends SceneTree
var failures := 0
func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)
func put(game, c: Dictionary, distance: float, dir: int, y: float) -> void:
	c.dir = dir
	c.node.position = Vector2(game.fight.pos.x - dir * distance, y) - game.crocodiles._croc_head(c.node, dir)
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var game = load("res://scenes/dangers.tscn").instantiate()
	root.add_child(game)
	var episode = load("res://scripts/episode.gd").new(game)
	episode.reset(30, "spell32")
	# Regression: headless runs once used a square 1280x1280 viewport, halving the arena.
	expect(game.get_viewport().get_visible_rect().size == Vector2(1280, 720), "agent runs use the project's 1280x720 viewport")
	expect(game.fight.full.size.x > 2400.0, "spell32 arena has its full 16:9 width")
	for c in game.fight.crocs: c.s = "gone"
	var lead: Dictionary = game.fight.crocs[0]
	var next: Dictionary = game.fight.crocs[1]
	lead.s = "crawl"
	lead.speed = 120.0
	# Tuned Totenbuch rule: arrivals at the bearer differ by at least max(the later one's half
	# body / its speed, the wave's min_gap) seconds, whatever the height or side.
	var v: float = 120.0 * game.unit
	var gap: float = maxf(next.node.get_meta("size").x / 2.0 / v, game.fight.waves[0].min_gap) * v
	for lead_dir in [-1, 1]:
		for next_dir in [-1, 1]:
			put(game, lead, 900.0, lead_dir, 500.0)
			put(game, next, 900.0 + gap * 0.5, next_dir, 1000.0)
			expect(not game.crocodiles._croc_clear(next, 120.0), "all heights/sides need the arrival gap")
			put(game, next, 900.0 + gap + 1.0, next_dir, 1000.0)
			expect(game.crocodiles._croc_clear(next, 120.0), "the full arrival gap permits movement")
			put(game, next, 1800.0, next_dir, 1000.0)
			expect(not game.crocodiles._croc_clear(next, 240.0), "a faster follower arriving at the same time is not clear")
			put(game, next, 900.0 + gap * 0.5, next_dir, 1000.0)
			next.s = "back"
			next.speed = 120.0
			game.crocodiles._croc_return(next)
			expect(next.s == "back", "returning crocodiles also wait for the arrival gap")
			put(game, next, 900.0 + gap + 1.0, next_dir, 1000.0)
			game.crocodiles._croc_return(next)
			expect(next.s == "crawl", "returning crocodile crawls again once clear")
			next.s = "wait"
	# Real movement still applies the artwork scale exactly once.
	next.s = "gone"
	put(game, lead, 900.0, 1, 1000.0)
	game.fight.tut = "first"
	var x: float = lead.node.position.x
	game.crocodiles._crocs(1.0 / 60.0)
	expect(is_equal_approx(lead.node.position.x - x, 120.0 * game.unit / 60.0), "speed applies scale once per fixed tick")
	expect(game.ENCOUNTERS[1].waves[0].speed == 175.0, "spell32 base speed matches the tuned original")
	# Walking to the far end, the camera stops just past spell32's left double line (x 3924-3943).
	game.reset()
	game.avatar.position.x = game.avatar.min_x
	game._update_camera(1.0)
	var left: float = game._visible_rect().position.x
	expect(left <= 3924.0 and left >= 3900.0, "camera stops just past the second double line (left edge %.1f)" % left)
	for b in game.hud.find_children("*", "BaseButton", true, false):
		expect(not b.tooltip_text in ["Menu", "Hint", "Journal  [j]"], "no %s button" % b.tooltip_text)
	# The screen keeps 16:9 at any window shape.
	expect(ProjectSettings.get_setting("display/window/stretch/aspect") == "keep", "aspect ratio is locked")
	var intro: String = game.hud._intro.find_child("Body", true, false).get_parsed_text()
	expect(intro.begins_with("Repel the crocodiles. Look and click around for helpful hints"), "intro says what to do: " + intro)
	# A human-started fight waits for [space] and says so; agent episodes skip that wait.
	episode.reset(30, "spell32")
	expect(game.fight.tut == "", "agent episodes start without the [space] wait")
	game.reset()
	game.start_fight(game.ENCOUNTERS[1])
	game._croc_open(1.0)
	expect(game.fight.tut == "start", "a clicked fight waits for [space]")
	expect(game.hud._text.ends_with("Press [space] to start."), "fight text ends with the start prompt: " + game.hud._text)
	expect("[↑] [↓]" in game.hud._text, "fight text includes the play instructions")
	expect(game.hud._text.begins_with("Crocodiles come from both sides now. Turn and spear each one."), "spell32 uses the short story line")
	for i in 300: game.crocodiles._crocs(1.0 / 60.0)
	expect(game.fight.wave_launched == 0, "no crocodile comes in 5 s before [space] (%d)" % game.fight.wave_launched)
	game._croc_thrust()
	expect(game.fight.tut == "" and game.fight.thrust >= 0.0, "[space] starts the fight and strikes, as in spell 31's lesson")
	# The ending offers another go or quitting.
	game.leave_fight()
	game.finish()
	var outro_buttons: Array = game.hud._outro.find_children("*", "Button", true, false).map(func(b): return b.text)
	expect(outro_buttons == ["Play again", "Quit game"], "ending buttons: %s" % [outro_buttons])
	var titles: Array = game.hud._outro.find_children("*", "Label", true, false).map(func(l): return l.text)
	expect("You've fended off the crocodiles." in titles, "ending title: %s" % [titles])
	print("Spacing fixtures: ", failures, " failures")
	quit(1 if failures else 0)
