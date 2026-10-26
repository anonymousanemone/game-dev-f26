## Replay an episode through the original Dangers scene, without manual move selection.
extends SceneTree
var episode
var actions: Array = []
var index := 0
var elapsed := 0.0
var rows: Array = []
var replay_paused := false
var speed := 1.0
var stopped := false
var verify_only := false
var trace_summary: Dictionary = {}
const Build = preload("res://scripts/trace_build.gd")
func _initialize() -> void:
	call_deferred("start")
func start() -> void:
	var path := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--replay="): path = arg.trim_prefix("--replay=")
		if arg == "--verify-only": verify_only = true
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("Supply --replay=/absolute/path/to/episode.jsonl")
		quit(1)
		return
	var seed_value := 30
	var situation := "spell31"
	var initial: Dictionary = {}
	var metadata: Dictionary = {}
	while not file.eof_reached():
		var line := file.get_line()
		if line.is_empty(): continue
		var row = JSON.parse_string(line)
		if not row is Dictionary:
			push_error("Malformed trace row; refusing an incomplete replay")
			quit(1)
			return
		if row.get("type") == "metadata": metadata = row
		if row.get("type") == "summary": trace_summary = row
		if row.get("type") == "reset":
			seed_value = int(row.seed)
			situation = row.case
			initial = row.observation
		elif row.get("type") == "step":
			actions.append(row.action)
			rows.append(row)
	if initial.is_empty():
		push_error("Trace has no initial observation")
		quit(1)
		return
	if not metadata.is_empty():
		var current: Dictionary = JSON.parse_string(JSON.stringify(Build.manifest()))
		if current.files_sha256 != metadata.files_sha256 or current.godot != metadata.godot:
			push_error("Build or Godot version differs from recording; restore the archived build and original Godot version")
			quit(1)
			return
	else:
		print("Legacy trace: build identity unavailable; checking recorded observations/results only")
	var game = load("res://scenes/dangers.tscn").instantiate()
	root.add_child(game)
	episode = load("res://scripts/episode.gd").new(game)
	var observed: Dictionary = episode.reset(seed_value, situation)
	Build.lock_hud(game.hud)
	if JSON.parse_string(JSON.stringify(observed)) != initial:
		fail("initial observation")
		return
	game.hud._title_label.text += " · Trace replay"
	if verify_only:
		while index < actions.size() and not stopped: advance()
		if not stopped:
			print("Verified all %d recorded steps" % index)
			quit()

func fail(where: String) -> void:
	stopped = true
	push_error("Replay mismatch at " + where)
	if episode != null: episode.game.say("Replay", "Mismatch at " + where + "; replay stopped.")
	if verify_only: quit(1)

func advance() -> void:
	var result: Dictionary = episode.step(0, actions[index])
	if JSON.parse_string(JSON.stringify(result)) != rows[index].result:
		fail("step %d" % (index + 1))
		return
	index += 1
	episode.game.hud._title_label.text = "Replay · step %d/%d · t=%.1f · health %d · turned %d · %s" % [index, actions.size(), result.observation.time, result.observation.health, result.observation.killed, JSON.stringify(actions[index - 1])]
	if index == actions.size():
		replay_paused = true
		var recorded: Dictionary = trace_summary.get("outcome", episode.outcome())
		episode.game.say("Replay", "End of trace · %d verified steps · %s: %s" % [index, recorded.status, recorded.reason])

func _input(event: InputEvent) -> void:
	if episode == null or stopped or not event is InputEventKey or not event.pressed or event.echo: return
	match event.keycode:
		KEY_SPACE: replay_paused = not replay_paused
		KEY_RIGHT:
			replay_paused = true
			if index < actions.size(): advance()
		KEY_1: speed = 0.25
		KEY_2: speed = 1.0
		KEY_3: speed = 2.0
		KEY_ESCAPE: quit()
func _process(delta: float) -> bool:
	if episode == null or replay_paused or stopped: return false
	elapsed += minf(delta, 0.25) * speed
	while elapsed >= 0.1 and index < actions.size() and not stopped:
		elapsed -= 0.1
		advance()
	return false
