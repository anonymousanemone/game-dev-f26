## Local JSON-lines protocol. Only this process owns Godot state.
extends SceneTree
var game
func _initialize() -> void:
	call_deferred("serve")
func serve() -> void:
	game = load("res://scenes/dangers.tscn").instantiate()
	root.add_child(game)
	var episode = load("res://scripts/episode.gd").new(game)
	while true:
		var line := OS.read_string_from_stdin()
		if line.is_empty(): break
		var request = JSON.parse_string(line)
		var result: Variant
		if not request is Dictionary:
			result = {"error": "invalid_request"}
		else:
			match request.get("op", ""):
				"reset": result = episode.reset(int(request.get("seed", 30)), request.get("case", "spell31"))
				"observe": result = episode.observe(int(request.get("player_id", 0)))
				"legal_actions": result = episode.legal_actions(int(request.get("player_id", 0)))
				"step": result = episode.step(int(request.get("player_id", 0)), request.get("action"))
				"outcome": result = episode.outcome()
				"quit": break
				_: result = {"error": "unknown_operation"}
		print("CROC_JSON:" + JSON.stringify(result))
	quit()
