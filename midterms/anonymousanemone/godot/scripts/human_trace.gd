## Record human controls through the same fixed-step episode used by agents and replay.
extends SceneTree
var episode
var trace: FileAccess
var elapsed := 0.0
var observation: Dictionary
var last_outcome: Dictionary
var finished := false
var started_usec := 0
var step_index := 0
const Build = preload("res://scripts/trace_build.gd")

func _initialize() -> void:
	call_deferred("start")

func start() -> void:
	var situation := "spell31"
	var path := ProjectSettings.globalize_path("res://../playtrace/human-%s-%s.jsonl" % [Time.get_datetime_string_from_system(true).replace(":", "-"), Time.get_ticks_usec()])
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--case="): situation = arg.trim_prefix("--case=")
		if arg.begins_with("--trace="): path = arg.trim_prefix("--trace=")
	DirAccess.make_dir_recursive_absolute(path.get_base_dir())
	if situation not in ["spell31", "spell32", "spell32_low"] or path.is_empty():
		push_error("Supply --case=spell31|spell32|spell32_low and --trace=/absolute/path/to/new.jsonl")
		quit(1)
		return
	if FileAccess.file_exists(path) or FileAccess.file_exists(path + ".build.zip"):
		push_error("Trace already exists; choose a new filename: " + path)
		quit(1)
		return
	var metadata := Build.manifest()
	if Build.archive(path + ".build.zip", metadata.files_sha256) != OK:
		push_error("Cannot archive build beside trace")
		quit(1)
		return
	trace = FileAccess.open(path, FileAccess.WRITE)
	if trace == null:
		push_error("Cannot create trace; check the parent directory: " + path)
		quit(1)
		return
	var game = load("res://scenes/dangers.tscn").instantiate()
	root.add_child(game)
	episode = load("res://scripts/episode.gd").new(game)
	observation = episode.reset(30, situation)
	last_outcome = episode.outcome()
	Build.lock_hud(game.hud)
	started_usec = Time.get_ticks_usec()
	metadata.type = "metadata"
	metadata.started_utc = Time.get_datetime_string_from_system(true)
	metadata.build_archive = path.get_file() + ".build.zip"
	metadata.archive_sha256 = FileAccess.get_sha256(path + ".build.zip")
	metadata.input_mode = "held keys sampled at 0.1 simulated seconds; no HUD navigation"
	write_row(metadata)
	game.hud._title_label.text += " · Human trace · Esc to finish"
	write_row({"type": "reset", "source": "human", "case": situation, "seed": 30, "observation": observation})
	print("Human trace: " + path)

func write_row(row: Dictionary) -> void:
	row.wall_elapsed_usec = Time.get_ticks_usec() - started_usec
	trace.store_line(JSON.stringify(row))
	trace.flush()

func _input(event: InputEvent) -> void:
	if episode == null or finished: return
	if event is InputEventKey and not event.echo:
		write_row({"type": "input", "keycode": event.keycode, "physical_keycode": event.physical_keycode,
			"pressed": event.pressed, "step": step_index})

func _notification(what: int) -> void:
	if episode == null or finished: return
	if what == NOTIFICATION_APPLICATION_FOCUS_IN or what == NOTIFICATION_APPLICATION_FOCUS_OUT:
		write_row({"type": "focus", "focused": what == NOTIFICATION_APPLICATION_FOCUS_IN, "step": step_index})

func _process(delta: float) -> bool:
	if episode == null or finished: return false
	if Input.is_key_pressed(KEY_ESCAPE):
		finish("human_stopped")
		quit()
		return false
	elapsed += minf(delta, 0.25)
	while elapsed >= 0.1 and not finished:
		elapsed -= 0.1
		var move := int(Input.is_key_pressed(KEY_DOWN) or Input.is_key_pressed(KEY_S)) - int(Input.is_key_pressed(KEY_UP) or Input.is_key_pressed(KEY_W))
		var face := 0
		if observation.both_sides:
			face = int(Input.is_key_pressed(KEY_RIGHT) or Input.is_key_pressed(KEY_D)) - int(Input.is_key_pressed(KEY_LEFT) or Input.is_key_pressed(KEY_A))
		var action := {"move": move, "face": face, "thrust": Input.is_key_pressed(KEY_SPACE), "heka": Input.is_key_pressed(KEY_SHIFT)}
		var result: Dictionary = episode.step(0, action)
		step_index += 1
		last_outcome = result.outcome
		write_row({"type": "step", "step": step_index, "simulation_frame": step_index * 6,
			"source": "human", "observation": observation, "action": action, "result": result})
		observation = result.observation
		if result.outcome.terminal:
			finish()
			episode.game.say("Human trace", result.outcome.reason.replace("_", " ") + ". Trace saved; close this window.")
	return false

func finish(stop_reason := "") -> void:
	if finished or episode == null: return
	finished = true
	var result: Dictionary = last_outcome.duplicate()
	if not result.terminal:
		result = result.duplicate()
		result.status = "interrupted"
		result.reason = stop_reason
	write_row({"type": "summary", "policy": "human", "outcome": result})
	trace.close()

func _finalize() -> void:
	finish("window_closed")
