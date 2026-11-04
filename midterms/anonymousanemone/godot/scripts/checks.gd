## Run the original crocodile acceptance checks against the extracted original scene.
extends SceneTree
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var game = load("res://scenes/dangers.tscn").instantiate()
	root.add_child(game)
	game._autotest()
