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
	print("Spacing fixtures: ", failures, " failures")
	quit(1 if failures else 0)
