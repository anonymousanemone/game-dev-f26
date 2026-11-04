## Screen-space interface: a title bar and the scribe's strip under the scene, both deep papyrus
## and each set off from the scene by the scroll's own frame band. The strip holds the last line said (its speaker as a tag on the
## band). Built in code so the level scenes stay small. Each level passes its own titles and texts
## to setup(). Its look (palette, font, band, icons) is in ui.gd.
extends CanvasLayer

signal restart_pressed

const TOP_BAR := 46.0         ## the title bar, without its band
const STRIP := 130.0          ## the scribe's strip, its band included
const BOXED := false          ## the band also down the screen's sides and along its bottom, round the strip
const EDGE := 12.0            ## that band, which has ink only on the strip's side
const TAG_H := 32.0           ## the speaker's tag, centred on the band
const OVERLAY_W := 900.0      ## the intro and outro cards' text, at most this wide (at the dialogue size)

## Keys are written in brackets ("hold [shift]"); these are shown as written, not read as BBCode
## tags ("[s]" would otherwise start a strikethrough).
const KEY_NAMES := ["space", "shift", "esc", "←", "→", "↑", "↓", "w", "a", "s", "d"]

var _level: Node
var _cfg: Dictionary
var _root: Control
var _say: RichTextLabel
var _tag: PanelContainer
var _tag_label: Label
var _intro: Control
var _outro: Control
var _outro_text: RichTextLabel
var _text := ""
var _overlay_layouts: Array = []
var _title_label: Label
var _record_session_button: Button
var _stop_recording_button: Button
var _recording_preparing := false


## cfg keys: title, intro_title, intro_body, outro_title.
func setup(level: Node, cfg: Dictionary) -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_level = level
	_cfg = cfg
	_root = Control.new()
	_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	_root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_root.theme = UI.theme()
	add_child(_root)
	_build_top_bar()
	_build_strip()
	_intro = _build_overlay(cfg.intro_title, cfg.intro_body, "Begin", dismiss_intro)
	if not OS.has_feature("web") and level.has_method("start_session_recording"):
		_record_session_button = Button.new()
		_record_session_button.text = "Record session"
		_record_session_button.add_theme_font_size_override("font_size", UI.BIG)
		_record_session_button.focus_mode = Control.FOCUS_NONE
		_record_session_button.pressed.connect(func():
			_recording_preparing = true
			_record_session_button.disabled = true
			_overlay_layouts[0].button.disabled = true
			if _level.start_session_recording():
				# Keep the intro paused through archive I/O and its resulting long frame.
				await get_tree().process_frame
				await get_tree().process_frame
				_recording_preparing = false
				dismiss_intro()
			else:
				_recording_preparing = false
				_record_session_button.disabled = false
				_overlay_layouts[0].button.disabled = false)
		_overlay_layouts[0].actions.add_child(_record_session_button)
	_intro.visible = true
	_outro = _build_overlay(cfg.outro_title, "", "Play again", func(): Scroll.finish(level.scene_file_path.get_file().get_basename()))
	_outro_text = _outro.find_child("Body", true, false)
	var quit := Button.new()
	quit.text = "Quit game"
	quit.add_theme_font_size_override("font_size", UI.BIG)
	quit.focus_mode = Control.FOCUS_NONE
	quit.pressed.connect(func(): get_tree().quit())
	_overlay_layouts[1].actions.add_child(quit)
	get_viewport().size_changed.connect(_resize_hud)
	_resize_hud.call_deferred()
	_sync_pause()


# ---------------------------------------------------------------- API used by the level

func top_height() -> float:
	return TOP_BAR + UI.BAND


## How far the speaker's tag reaches up above the strip (it sits centred on the strip's band).
func tag_reach() -> float:
	return (TAG_H - UI.BAND) / 2.0


func bottom_height() -> float:
	return STRIP


func is_blocking() -> bool:
	return _intro.visible or _outro.visible


func dismiss_intro() -> void:
	_note_command("begin")
	_intro.visible = false
	_sync_pause()


func reset_view() -> void:
	_outro.visible = false
	_sync_pause()


func say(who: String, text: String, category := "default") -> void:
	var color: Color = UI.TAG_MINIGAME if category == "minigame" else UI.TAG
	_tag.add_theme_stylebox_override("panel", UI.box(color, UI.INK, 4, 12, 0))
	_tag_label.add_theme_color_override("font_color", UI.CREAM)
	_text = UI.plain(text)
	_tag_label.text = who
	_tag.visible = who != ""
	_say.text = _keys(_text)   # always at the dialogue size (two font pixels to a screen pixel), never paged


func _sync_pause() -> void:
	var blocked := is_blocking()
	if get_tree().paused and not blocked:
		# A key used while reading must not become a movement/exit on resume.
		for action in ["ui_left", "ui_right", "ui_up", "ui_down", "ui_accept"]:
			Input.action_release(action)
	get_tree().paused = blocked


func show_outro(body: String) -> void:
	_outro_text.text = _keys(body)
	_outro_text.get_parent().visible = body != ""
	_outro.visible = true
	_resize_hud.call_deferred()
	_sync_pause()


func _input(event: InputEvent) -> void:
	if _recording_preparing: return
	if not (event is InputEventKey and event.pressed and not event.echo):
		return
	if _intro.visible or _outro.visible:
		if event.keycode in [KEY_ENTER, KEY_KP_ENTER, KEY_SPACE]:
			if _intro.visible:
				dismiss_intro()
			else:
				Scroll.finish(_level.scene_file_path.get_file().get_basename())
			get_viewport().set_input_as_handled()
		return


# ---------------------------------------------------------------- building

func _build_top_bar() -> void:
	var bar := ColorRect.new()
	bar.color = UI.DEEP
	bar.set_anchors_preset(Control.PRESET_TOP_WIDE)
	bar.offset_bottom = TOP_BAR
	_root.add_child(bar)
	UI.band(bar, "band_top", Control.PRESET_BOTTOM_WIDE, Rect2(0, 0, 0, UI.BAND))
	var row := HBoxContainer.new()
	row.set_anchors_preset(Control.PRESET_FULL_RECT)
	row.offset_left = 16
	row.offset_right = -16
	row.add_theme_constant_override("separation", 22)
	bar.add_child(row)
	var title := Label.new()
	_title_label = title
	title.text = _cfg.title
	title.add_theme_font_size_override("font_size", UI.BIG)
	title.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	title.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(title)
	row.add_child(spacer)
	_stop_recording_button = Button.new()
	_stop_recording_button.text = "Recording · Stop"
	_stop_recording_button.focus_mode = Control.FOCUS_NONE
	_stop_recording_button.visible = false
	_stop_recording_button.pressed.connect(func(): _level.stop_session_recording())
	row.add_child(_stop_recording_button)
	row.add_child(UI.icon_button("restart", "Restart", func():
		_note_command("restart")
		restart_pressed.emit()))


## The strip: deep papyrus under the band (and, if BOXED, inside it along the screen's edges), the
## line said with its speaker's tag on the band.
func _build_strip() -> void:
	var strip := ColorRect.new()
	strip.color = UI.DEEP
	strip.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	strip.offset_top = -STRIP
	_root.add_child(strip)
	UI.band(strip, "band_top", Control.PRESET_TOP_WIDE, Rect2(0, 0, 0, UI.BAND))
	var edge := EDGE if BOXED else 0.0
	if BOXED:
		UI.band(strip, "band_bottom", Control.PRESET_BOTTOM_WIDE, Rect2(0, -EDGE, 0, 0))
		UI.band(strip, "band_left", Control.PRESET_LEFT_WIDE, Rect2(0, UI.BAND, EDGE, -EDGE))
		UI.band(strip, "band_right", Control.PRESET_RIGHT_WIDE, Rect2(-EDGE, UI.BAND, 0, -EDGE))

	var row := HBoxContainer.new()
	row.set_anchors_preset(Control.PRESET_FULL_RECT)
	row.offset_left = edge + 28
	row.offset_right = -edge - 16
	row.offset_top = UI.BAND + 8
	row.offset_bottom = -edge - 8
	row.add_theme_constant_override("separation", 24)
	strip.add_child(row)

	# what is said, centred in the strip
	_say = _rich(UI.DIALOGUE)
	_say.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_say.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_say.add_theme_constant_override("line_separation", 0)
	_say.add_theme_constant_override("paragraph_separation", 0)
	row.add_child(_say)

	# the speaker's tag sits on the band
	_tag = PanelContainer.new()
	_tag.add_theme_stylebox_override("panel", UI.box(UI.TAG, UI.INK, 4, 12, 0))
	_tag.custom_minimum_size.y = TAG_H
	_tag.position = Vector2(edge + 24, (UI.BAND - TAG_H) / 2.0)
	_tag.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_tag.visible = false
	_tag_label = Label.new()
	_tag_label.add_theme_color_override("font_color", UI.CREAM)
	_tag_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_tag.add_child(_tag_label)
	strip.add_child(_tag)


func _build_overlay(title: String, body: String, button: String, on_press: Callable) -> Control:
	var dim := ColorRect.new()
	dim.color = Color(UI.DIM, 0.72)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	dim.mouse_filter = Control.MOUSE_FILTER_STOP
	dim.visible = false
	_root.add_child(dim)
	var center := CenterContainer.new()
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	dim.add_child(center)
	var panel := PanelContainer.new()
	panel.add_theme_stylebox_override("panel", UI.box(UI.PAPYRUS, UI.INK, 4, 36, 30))
	center.add_child(panel)
	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 18)
	panel.add_child(v)
	var t := Label.new()
	t.text = title
	t.add_theme_font_size_override("font_size", UI.BIG)
	t.add_theme_color_override("font_color", UI.TAG)
	t.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	v.add_child(t)
	var scroll := ScrollContainer.new()
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	v.add_child(scroll)
	var b := _rich(UI.DIALOGUE)
	b.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	b.name = "Body"
	b.custom_minimum_size.x = OVERLAY_W
	b.text = _keys(body)
	scroll.add_child(b)
	_overlay_layouts.append({"scroll": scroll, "body": b, "title": t})
	var btn := Button.new()
	btn.text = button
	btn.size_flags_horizontal = Control.SIZE_SHRINK_BEGIN
	btn.add_theme_font_size_override("font_size", UI.BIG)
	btn.focus_mode = Control.FOCUS_NONE
	btn.pressed.connect(on_press)
	var button_margin := MarginContainer.new()
	button_margin.add_theme_constant_override("margin_top", 6)
	var actions := HBoxContainer.new()
	actions.add_theme_constant_override("separation", 18)
	actions.add_child(btn)
	button_margin.add_child(actions)
	v.add_child(button_margin)
	_overlay_layouts[-1]["button"] = btn
	_overlay_layouts[-1]["actions"] = actions
	return dim


func _note_command(op: String, data := {}) -> void:
	if _level.has_method("record_session_command"):
		_level.record_session_command(op, data)


## `text` with its bracketed key names escaped for BBCode.
static func _keys(text: String) -> String:
	text = text.replace("\n\n", "\n")
	text = text.replace("[b]", "[color=#%s]" % UI.TAG.to_html(false)).replace("[/b]", "[/color]")
	text = text.replace("[i]", "[color=#%s]" % UI.OCHRE.to_html(false)).replace("[/i]", "[/color]")
	for k in KEY_NAMES:
		text = text.replace("[%s]" % k, "[lb]%s[rb]" % k)
	return text


func _rich(size: int) -> RichTextLabel:
	var r := RichTextLabel.new()
	r.bbcode_enabled = true
	r.fit_content = true
	r.scroll_active = false
	r.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	r.add_theme_font_size_override("normal_font_size", size)
	r.add_theme_font_size_override("bold_font_size", size)
	r.add_theme_font_size_override("italics_font_size", size)
	r.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return r


func _resize_hud() -> void:
	var viewport := get_viewport().get_visible_rect().size
	_title_label.add_theme_font_size_override("font_size", UI.SMALL if viewport.x < 900.0 else UI.BIG)
	for layout in _overlay_layouts:
		var width := clampf(viewport.x - 120.0, 200.0, OVERLAY_W)
		layout.body.custom_minimum_size.x = width
		layout.title.custom_minimum_size.x = width
		var available: float = viewport.y - 142.0 - layout.title.get_combined_minimum_size().y - layout.button.get_combined_minimum_size().y
		var height: float = minf(maxf(40.0, available), layout.body.get_content_height() + 8.0)
		layout.scroll.custom_minimum_size = Vector2(width, maxf(40.0, height))


func _exit_tree() -> void:
	get_tree().paused = false
