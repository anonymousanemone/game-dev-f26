## Standalone excerpt: both original HUD destinations return to this excerpt's intro.
extends Node
func finish(_key: String) -> void:
	get_tree().paused = false
	get_tree().reload_current_scene()
