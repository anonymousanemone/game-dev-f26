## Standalone excerpt: both original HUD destinations return to this excerpt's intro.
extends Node
func next_built(_key: String) -> Dictionary:
	return {}
func finish(_key: String) -> void:
	get_tree().paused = false
	get_tree().reload_current_scene()
