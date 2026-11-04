## Automated UI/record/replay fixture. This is not a human playtest.
extends SceneTree
var game
func _initialize() -> void:
	call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		push_error(message)
		quit(1)
func key(pressed: bool) -> void:
	var event := InputEventKey.new()
	event.keycode = KEY_SPACE
	event.pressed = pressed
	Input.parse_input_event(event)
func run() -> void:
	var path := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--trace="): path = arg.trim_prefix("--trace=")
	game = load("res://scenes/dangers.tscn").instantiate()
	root.add_child(game)
	await process_frame
	await process_frame
	check(game.hud._record_session_button.text == "Record session", "intro has a recording button")
	game.set_meta("session_trace_path", path)
	game.hud._record_session_button.pressed.emit()
	check(game.session_recorder.recording, "record button starts saving before Begin")
	for i in 3: await process_frame
	check(not game.hud._intro.visible, "record button starts normal play")
	# Walk using real Godot action state until inside the original spell31 vignette.
	var target: float = game.span(game.ENCOUNTERS[0]).y - 100.0 * game.unit
	Input.action_press("ui_left")
	for i in 900:
		if game.avatar.position.x <= target: break
		await process_frame
	Input.action_release("ui_left")
	await process_frame
	var event := InputEventMouseButton.new()
	event.button_index = MOUSE_BUTTON_LEFT
	event.pressed = true
	game.set_meta("session_mouse", game.actor_rect("c31a").get_center())
	game._unhandled_input(event)
	game.remove_meta("session_mouse")
	for i in 180:
		if not game.fight.is_empty() and game.fight.open >= 1.0: break
		await process_frame
	check(not game.fight.is_empty(), "click original crocodile to start fight")
	key(true)
	for i in 40: await process_frame
	check(game.fight.thrust < 0.0, "holding Space does not auto-repeat thrusts")
	check(game.fight.tut == "first", "native press starts original tutorial")
	key(false)
	game.hud.toggle_journal(true)
	for i in 3: await process_frame
	game.hud.toggle_journal(false)
	game.hud.request_hint()
	for i in 3: await process_frame
	game.hud._note_command("restart")
	game.hud.restart_pressed.emit()
	for i in 3: await process_frame
	# A second encounter exercises real bites, return-to-movement and defeat callbacks.
	target = game.span(game.ENCOUNTERS[1]).y - 100.0 * game.unit
	Input.action_press("ui_left")
	for i in 900:
		if game.avatar.position.x <= target: break
		await process_frame
	Input.action_release("ui_left")
	await process_frame
	game.set_meta("session_mouse", game.actor_rect("c32a").get_center())
	game._unhandled_input(event)
	game.remove_meta("session_mouse")
	var saw_loss := false
	for i in 1500:
		await process_frame
		if not game.fight.is_empty() and game.fight.lost:
			saw_loss = true
		if saw_loss and game.fight.is_empty(): break
	check(saw_loss and game.fight.is_empty(), "native session records a game loss and return to scroll")
	game.hud._stop_recording_button.pressed.emit()
	check(not game.session_recorder.recording and not game.has_meta("session_driven"), "stop saves and returns to unrecorded normal play")
	print("Native session fixture completed")
	quit()
