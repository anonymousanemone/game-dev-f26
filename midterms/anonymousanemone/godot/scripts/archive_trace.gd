## Offline runner helper; preserves the same archive format as human recording.
extends SceneTree
func _initialize() -> void:
	var path := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--trace="): path = arg.trim_prefix("--trace=")
	if path.is_empty() or FileAccess.file_exists(path + ".build.zip"):
		push_error("Supply a new --trace path for its build archive")
		quit(1)
		return
	var build = load("res://scripts/trace_build.gd")
	var metadata: Dictionary = build.manifest()
	if build.archive(path + ".build.zip", metadata.files_sha256) != OK:
		push_error("Cannot archive build")
		quit(1)
		return
	metadata.type = "metadata"
	metadata.started_utc = Time.get_datetime_string_from_system(true)
	metadata.build_archive = path.get_file() + ".build.zip"
	metadata.archive_sha256 = FileAccess.get_sha256(path + ".build.zip")
	print("CROC_METADATA:" + JSON.stringify(metadata))
	quit()
