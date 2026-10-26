## Re-execute a native human session in the authoritative scene, checking every frame.
extends RefCounted
var tree: SceneTree
var game
var tape
var rows: Array
var index := 0
var frame_index := 0
var elapsed := 0.0
var paused := false
var stopped := false
var speed := 1.0
var verify_only := false

func _init(scene_tree: SceneTree) -> void:
	tree = scene_tree

func start(metadata: Dictionary, recorded: Array, verify: bool) -> void:
	rows = recorded
	verify_only = verify
	tree.root.size = Vector2i(int(metadata.window_size[0]), int(metadata.window_size[1]))
	game = load("res://scenes/dangers.tscn").instantiate()
	tree.root.add_child(game)
	tape = load("res://scripts/session_tape.gd").new(game)
	game.add_child(tape)
	tape.activate()
	game.set_process_unhandled_input(false)
	load("res://scripts/trace_build.gd").lock_hud(game.hud)
	game.rng.seed = int(metadata.rng_seed)
	game.rng.state = int(metadata.rng_state)
	seed(30)
	if normalized(tape.state()) != metadata.initial_state:
		fail("initial state")
		return
	if verify_only:
		while index < rows.size() and not stopped: advance()
		if not stopped:
			print("Verified all %d recorded native frames" % frame_index)
			tree.quit()

func normalized(value: Variant) -> Variant:
	return JSON.parse_string(JSON.stringify(value))

func difference(a: Variant, b: Variant, path := "state") -> String:
	if a is Dictionary and b is Dictionary:
		for key in a:
			if not b.has(key): return path + "." + key + " missing"
			var found := difference(a[key], b[key], path + "." + key)
			if not found.is_empty(): return found
	elif a is Array and b is Array:
		if a.size() != b.size(): return path + " array length"
		for i in a.size():
			var found := difference(a[i], b[i], path + "[%d]" % i)
			if not found.is_empty(): return found
	elif a != b: return path + ": recorded " + str(a) + ", replay " + str(b)
	return ""

func fail(where: String) -> void:
	stopped = true
	push_error("Session replay mismatch at " + where)
	if verify_only: tree.quit(1)
	else: game.hud._title_label.text = "Replay stopped: mismatch at " + where

func next_delta() -> float:
	for i in range(index, rows.size()):
		if rows[i].get("type") == "frame": return float(rows[i].delta_seconds)
	return 0.0

func advance() -> void:
	while index < rows.size():
		var row: Dictionary = rows[index]
		index += 1
		match row.get("type"):
			"command": tape.apply_command(row)
			"frame":
				var controls: Dictionary = row.controls
				game.set_meta("midterm_controls", {"move": controls.move, "face": controls.face, "heka": controls.heka})
				game.avatar.set_meta("session_walk_axis", controls.walk_axis)
				game._focused = controls.focused
				# JSON decimals can round native frame deltas. Preserve the exact binary value.
				var delta: float = str(row.delta_float64).hex_decode().to_float64_array()[0]
				tape.native_tick(delta, controls, row.paused)
				frame_index += 1
				var actual: Dictionary = normalized(tape.state())
				if actual != row.state:
					fail("frame %d (%s)" % [frame_index, difference(row.state, actual)])
					return
				# Preserve recorded dialogue and decorative shake as well as verified gameplay.
				if game.hud._text != row.view.message or game.hud._tag_label.text != row.view.speaker:
					game.hud.say(row.view.speaker, row.view.message)
				game.hud._intro.visible = row.view.intro
				game.hud._outro.visible = row.view.outro
				game.hud._journal_page.visible = row.view.journal
				game.hud._journal_scroll.scroll_vertical = int(row.view.journal_scroll)
				game.camera.offset = Vector2(row.view.camera_offset[0], row.view.camera_offset[1])
				game.hud._title_label.text = "Session replay · frame %d · Space: pause · Right: one frame" % frame_index
				return
	paused = true
	game.hud._title_label.text = "End of session · %d verified native frames" % frame_index

func tick(delta: float) -> void:
	if stopped or paused: return
	elapsed += minf(delta, 0.25) * speed
	while index < rows.size() and not stopped and elapsed >= next_delta():
		elapsed -= next_delta()
		advance()
	if index == rows.size():
		paused = true
		game.hud._title_label.text = "End of session · %d verified native frames" % frame_index

func input_event(event: InputEvent) -> void:
	if stopped or not event is InputEventKey or not event.pressed or event.echo: return
	match event.keycode:
		KEY_SPACE: paused = not paused
		KEY_RIGHT:
			paused = true
			if index < rows.size(): advance()
		KEY_1: speed = 0.25
		KEY_2: speed = 1.0
		KEY_3: speed = 2.0
		KEY_ESCAPE: tree.quit()
