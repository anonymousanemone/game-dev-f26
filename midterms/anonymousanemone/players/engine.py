"""Trusted runner's Godot transport. Never exposed as a model tool."""
import json
import os
from pathlib import Path
import selectors
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def godot_binary():
    return os.environ.get('GODOT') or shutil.which('godot') or '/Applications/Godot.app/Contents/MacOS/Godot'


class Engine:
    def __init__(self):
        self.process = subprocess.Popen(
            [godot_binary(), '--headless', '--path', str(ROOT / 'godot'),
             '--script', 'res://scripts/server.gd', '--', '--machine'],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1)
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.process.stdout, selectors.EVENT_READ)

    def call(self, op, **kwargs):
        self.process.stdin.write(json.dumps({'op': op, **kwargs}) + '\n')
        self.process.stdin.flush()
        while self.selector.select(timeout=15):
            line = self.process.stdout.readline()
            if not line:
                raise RuntimeError('Godot exited: ' + self.process.stderr.read()[-2000:])
            if line.startswith('CROC_JSON:'):
                return json.loads(line[len('CROC_JSON:'):])
        self.process.kill()
        raise TimeoutError('Godot operation timed out')

    def close(self):
        if self.process.poll() is None:
            self.process.stdin.write('{"op":"quit"}\n')
            self.process.stdin.flush()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
        self.selector.close()
        for stream in (self.process.stdin, self.process.stdout, self.process.stderr):
            stream.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
