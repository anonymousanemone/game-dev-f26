## Native human-session recording. No policy is given this trusted recorder or its state.
## Inputs retain their original press semantics; simulation uses each recorded render delta.
extends Node
const Build = preload("res://scripts/trace_build.gd")
var game
var recording := false
var trace: FileAccess
var path := ""
var frame_index := 0
var started := 0
var last_state := {}
var window_size := Vector2i.ZERO

func _init(scene = null) -> void:
	game = scene
	process_mode = Node.PROCESS_MODE_ALWAYS
	process_priority = 100

func begin(output_path := "") -> bool:
	var folder := ProjectSettings.globalize_path("res://../playtrace")
	if not output_path.is_empty(): folder = output_path.get_base_dir()
	if DirAccess.make_dir_recursive_absolute(folder) != OK: return false
	path = output_path if not output_path.is_empty() else folder.path_join("human-session-%s-%s.jsonl" % [Time.get_datetime_string_from_system(true).replace(":", "-"), Time.get_ticks_usec()])
	if FileAccess.file_exists(path) or FileAccess.file_exists(path + ".build.zip"): return false
	var metadata := Build.manifest()
	if Build.archive(path + ".build.zip", metadata.files_sha256) != OK: return false
	trace = FileAccess.open(path, FileAccess.WRITE)
	if trace == null: return false
	recording = true
	started = Time.get_ticks_usec()
	window_size = game.get_window().size
	activate()
	# Only decorative damage shake uses the global RNG; gameplay owns its separate seeded RNG.
	seed(30)
	metadata.type = "metadata"
	metadata.format = "native_session_v1"
	metadata.erase("fixed_step_seconds")
	metadata.erase("frames_per_action")
	metadata.simulation_mode = "native frame deltas and immediate key-press events"
	metadata.started_utc = Time.get_datetime_string_from_system(true)
	metadata.build_archive = path.get_file() + ".build.zip"
	metadata.archive_sha256 = FileAccess.get_sha256(path + ".build.zip")
	metadata.window_size = [game.get_window().size.x, game.get_window().size.y]
	metadata.rng_seed = str(game.rng.seed)
	metadata.rng_state = str(game.rng.state)
	metadata.initial_state = state()
	write_row(metadata)
	print("Recording session: " + path)
	return true

func activate() -> void:
	game.set_meta("session_driven", true)
	game.avatar.set_meta("session_driven", true)
	for tween in game._fight_tweens:
		if tween.is_valid(): tween.pause()

func write_row(row: Dictionary) -> void:
	row.wall_elapsed_usec = Time.get_ticks_usec() - started
	trace.store_line(JSON.stringify(row))
	trace.flush()

func command(op: String, data := {}) -> void:
	if recording: write_row({"type": "command", "op": op, "data": data, "after_frame": frame_index})

func input_event(event: InputEvent, mouse: Vector2) -> void:
	if not recording: return
	var data := {"mouse": [mouse.x, mouse.y]}
	if event is InputEventKey:
		data.kind = "key"
		data.keycode = event.keycode
		data.physical_keycode = event.physical_keycode
		data.pressed = event.pressed
		data.echo = event.echo
	elif event is InputEventMouseButton:
		data.kind = "mouse_button"
		data.button = event.button_index
		data.pressed = event.pressed
	elif event is InputEventMouseMotion:
		data.kind = "mouse_motion"
	else: return
	command("input", data)

func _process(delta: float) -> void:
	if not recording: return
	if game.get_window().size != window_size:
		window_size = game.get_window().size
		command("resize", {"width": window_size.x, "height": window_size.y})
	var move := Vector2.ZERO
	if not game.fight.is_empty(): move = game.crocodiles._keys()
	var controls := {"move": move.y, "face": move.x, "heka": Input.is_key_pressed(KEY_SHIFT),
		"walk_axis": Input.get_axis("ui_left", "ui_right"), "focused": game._focused}
	var blocked: bool = game.get_tree().paused
	native_tick(delta, controls, blocked)
	frame_index += 1
	last_state = state()
	write_row({"type": "frame", "frame": frame_index, "delta_seconds": delta,
		"delta_float64": PackedFloat64Array([delta]).to_byte_array().hex_encode(),
		"paused": blocked, "controls": controls, "state": last_state, "view": view()})

func native_tick(delta: float, _controls: Dictionary, blocked: bool) -> void:
	if blocked: return
	game.set_meta("session_tick", true)
	game._process(delta)
	game.remove_meta("session_tick")
	if game.avatar.is_processing():
		game.avatar.set_meta("session_tick", true)
		game.avatar._process(delta)
		game.avatar.remove_meta("session_tick")
	for tween in game._fight_tweens.duplicate():
		if tween.is_valid(): tween.custom_step(delta)
	if not game.fight.is_empty(): game._place_frame()
	game.overlay.queue_redraw()

func state() -> Dictionary:
	var active := {}
	if not game.fight.is_empty():
		for key in ["health", "killed", "wave", "wave_launched", "wave_killed", "phase", "clock", "t", "thrust", "open", "lost", "facing", "tut"]:
			active[key] = game.fight.get(key)
		active.id = game.fight.e.id
		active.pos = [game.fight.pos.x, game.fight.pos.y]
		active.crocs = []
		for c in game.fight.crocs:
			active.crocs.append({"state": c.s, "position": [c.node.position.x, c.node.position.y],
				"direction": c.dir, "red": c.red, "speed": c.speed})
	var solved: Array = game.solved.keys()
	solved.sort()
	return {"fight": active, "avatar": [game.avatar.position.x, game.avatar.position.y],
		"facing": game.avatar.facing, "solved": solved, "finished": game.finished,
		"bites": game.bites, "heka_known": game.heka_known, "rng_state": str(game.rng.state)}

func view() -> Dictionary:
	return {"message": game.hud._text, "speaker": game.hud._tag_label.text,
		"intro": game.hud._intro.visible, "outro": game.hud._outro.visible,
		"journal": game.hud._journal_page.visible,
		"journal_scroll": game.hud._journal_scroll.scroll_vertical,
		"camera_offset": [game.camera.offset.x, game.camera.offset.y]}

func apply_command(row: Dictionary) -> void:
	var data: Dictionary = row.data
	match row.op:
		"begin": game.hud.dismiss_intro()
		"restart": game.reset()
		"resize": game.get_window().size = Vector2i(int(data.width), int(data.height))
		"hint": game.hint()
		"journal": game.hud.toggle_journal(data.open)
		"journal_entry":
			var entry: Dictionary = game.hud._journal_entries[data.id]
			game.hud.say(entry.speaker, entry.text)
		"input":
			var event: InputEvent
			match data.kind:
				"key":
					event = InputEventKey.new()
					event.keycode = int(data.keycode)
					event.physical_keycode = int(data.physical_keycode)
					event.pressed = data.pressed
					event.echo = data.echo
				"mouse_button":
					event = InputEventMouseButton.new()
					event.button_index = int(data.button)
					event.pressed = data.pressed
				"mouse_motion": event = InputEventMouseMotion.new()
			game.set_meta("session_mouse", Vector2(data.mouse[0], data.mouse[1]))
			game._unhandled_input(event)
			game.remove_meta("session_mouse")

func finish(reason := "window_closed") -> void:
	if not recording: return
	recording = false
	write_row({"type": "summary", "policy": "human", "format": "native_session_v1",
		"frames": frame_index, "reason": reason, "last_state": last_state})
	trace.close()
	if is_instance_valid(game):
		game.remove_meta("session_driven")
		if is_instance_valid(game.avatar): game.avatar.remove_meta("session_driven")
		for tween in game._fight_tweens:
			if tween.is_valid(): tween.play()
	print("Session saved: " + path)

func _exit_tree() -> void:
	finish()
