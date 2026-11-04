"""Trusted offline build archive; never passed to a player policy."""
import json
import subprocess
from .engine import ROOT, godot_binary


def archive(trace_path):
    result = subprocess.run([godot_binary(), '--headless', '--path', str(ROOT/'godot'),
        '--script', 'res://scripts/archive_trace.gd', '--', f'--trace={trace_path.resolve()}'],
        capture_output=True, text=True, timeout=30)
    for line in result.stdout.splitlines():
        if result.returncode == 0 and line.startswith('CROC_METADATA:'):
            return json.loads(line.removeprefix('CROC_METADATA:'))
    raise RuntimeError('Godot could not archive the recording build: ' + result.stderr[-2000:])
