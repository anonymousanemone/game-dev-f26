## Shared puzzle instructions, success and feedback text.
extends RefCounted

static var _catalog: Dictionary = _load_catalog()
var data: Dictionary = _catalog


static func _load_catalog() -> Dictionary:
	var catalog := {"messages": {}, "puzzles": {}}
	for level in ["dangers"]:
		var content: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://assets/%s/puzzles.json" % level))
		catalog.messages.merge(content.messages)
		catalog.puzzles.merge(content.puzzles)
	return catalog


static func message(id: String) -> String:
	return _catalog.messages[id]


## Instructions/success are plain strings; feedback is selected by event name.
static func text(puzzle: String, field: String, variant := "default") -> String:
	var entry = _catalog.puzzles[puzzle][field]
	if entry is String:
		return entry
	return entry[variant]
