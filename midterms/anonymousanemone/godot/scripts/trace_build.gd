## Trusted recording metadata, never supplied to a player policy.
extends RefCounted

static func files_in(path: String) -> Array:
	var result := []
	for name in DirAccess.get_files_at(path):
		if not name.ends_with(".import") and not name.ends_with(".uid"):
			result.append(path.path_join(name))
	for name in DirAccess.get_directories_at(path):
		if not name.begins_with("."):
			result.append_array(files_in(path.path_join(name)))
	result.sort()
	return result

static func manifest() -> Dictionary:
	var hashes := {}
	for path in files_in("res://"):
		hashes[path] = FileAccess.get_sha256(path)
	return {"schema": 2, "godot": Engine.get_version_info(), "files_sha256": hashes,
		"fixed_step_seconds": 1.0 / 60.0, "frames_per_action": 6}

static func archive(path: String, files: Dictionary) -> Error:
	var zip := ZIPPacker.new()
	var error := zip.open(path)
	if error != OK: return error
	for source in files:
		error = zip.start_file("godot/" + source.trim_prefix("res://"))
		if error == OK: error = zip.write_file(FileAccess.get_file_as_bytes(source))
		if error == OK: error = zip.close_file()
		if error != OK:
			zip.close()
			return error
	return zip.close()

static func lock_hud(node: Node) -> void:
	node.set_process_input(false)
	node.set_process_unhandled_input(false)
	if node is Control: node.mouse_filter = Control.MOUSE_FILTER_IGNORE
	for child in node.get_children(): lock_hud(child)
