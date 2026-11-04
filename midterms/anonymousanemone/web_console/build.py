"""Export a disposable copy of the real game as an embedded browser replayer."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from players.engine import ROOT, godot_binary
from .server import HERE, source_identity


def prepare(target):
    shutil.copytree(ROOT / 'godot', target,
                    ignore=shutil.ignore_patterns('.godot', '*.uid', '*.import', '.DS_Store'))
    replay = (target / 'scripts/replay.gd').read_text()
    replay = replay.replace('extends SceneTree', 'extends Node\nvar root: Window:\n\tget: return get_tree().root\nfunc quit(code: int = 0) -> void:\n\tget_tree().quit(code)')
    begin = replay.index('func _initialize()')
    end = replay.index('\tvar file := FileAccess.open', begin)
    replay = replay[:begin] + '''func _ready() -> void:
	var url = JavaScriptBridge.eval("new URLSearchParams(window.location.search).get('trace')")
	if url == null or not str(url).begins_with("/api/runs/"):
		push_error("Missing console trace URL")
		return
	var request := HTTPRequest.new()
	add_child(request)
	var origin = JavaScriptBridge.eval("window.location.origin")
	if request.request(str(origin) + str(url)) != OK:
		push_error("Could not request trace")
		return
	var response = await request.request_completed
	request.queue_free()
	if response[1] != 200:
		push_error("Trace request failed")
		return
	var output := FileAccess.open("user://console-trace.jsonl", FileAccess.WRITE)
	output.store_buffer(response[3])
	output.close()
	start()
func start() -> void:
	var path := "user://console-trace.jsonl"
''' + replay[end:]
    begin = replay.index('\tif not metadata.is_empty():')
    end = replay.index('\tif metadata.get("format")', begin)
    replay = replay[:begin] + '''	# The local server verifies the original build/version natively before serving
	# this trace. Web export remaps resources and has a different platform identity.
	# Retain all initial-observation and per-step comparisons below.
''' + replay[end:]
    replay = replay.replace('func _process(delta: float) -> bool:', 'func _process(delta: float) -> void:').replace('return false', 'return')
    (target / 'scripts/console_replay.gd').write_text(replay)
    (target / 'scenes/console_replay.tscn').write_text('''[gd_scene load_steps=2 format=3]
[ext_resource type="Script" path="res://scripts/console_replay.gd" id="1"]
[node name="ConsoleReplay" type="Node"]
script = ExtResource("1")
''')
    project = target / 'project.godot'
    text = project.read_text().replace('run/main_scene="res://scenes/dangers.tscn"', 'run/main_scene="res://scenes/console_replay.tscn"')
    text += '\nrenderer/rendering_method="gl_compatibility"\nrenderer/rendering_method.mobile="gl_compatibility"\n'
    project.write_text(text)
    (target / 'export_presets.cfg').write_text('''[preset.0]
name="Console Web"
platform="Web"
runnable=true
export_filter="all_resources"
include_filter="*.json,*.gd"
exclude_filter=""
export_path=""
script_export_mode=0
[preset.0.options]
variant/extensions_support=false
variant/thread_support=false
html/export_icon=false
html/resize_canvas_on_start=true
html/focus_canvas_on_start=true
progressive_web_app/enabled=false
''')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--template', type=Path, help='Optional matching web_nothreads_release.zip')
    parser.add_argument('--prepare-only', type=Path, help='Prepare a temporary project without exporting')
    args = parser.parse_args()
    if args.prepare_only:
        prepare(args.prepare_only)
        return
    build = HERE / 'build'
    build.mkdir(exist_ok=True)
    # A failed rebuild must never leave a stale successful identity.
    (build / 'source.json').unlink(missing_ok=True)
    identity = source_identity()
    with tempfile.TemporaryDirectory(prefix='crocodiles-web-') as temp:
        project = Path(temp) / 'godot'
        prepare(project)
        if args.template:
            with (project / 'export_presets.cfg').open('a') as handle:
                handle.write('custom_template/release=' + json.dumps(str(args.template.resolve())) + '\n')
        subprocess.run([godot_binary(), '--headless', '--path', str(project), '--editor', '--import', '--quit'], check=True)
        subprocess.run([godot_binary(), '--headless', '--path', str(project), '--export-release',
                        'Console Web', str(build / 'replay.html')], check=True)
    if source_identity() != identity:
        raise RuntimeError('Game source changed during export; rebuild before replaying.')
    (build / 'source.json').write_text(json.dumps(identity))
    print('Browser replay built. Start: python -m web_console.server')


if __name__ == '__main__':
    main()
