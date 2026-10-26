"""Recording evidence must survive replay and detect a changed result."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile

from players.engine import ROOT, godot_binary


class HumanTraceTests(unittest.TestCase):
    def test_archive_replay_and_tamper_detection(self):
        with tempfile.TemporaryDirectory(prefix='crocodiles-trace-') as folder:
            trace = Path(folder) / 'attempt.jsonl'

            def run(script, arguments, before=()):
                return subprocess.run(
                    [godot_binary(), '--headless', '--path', str(ROOT/'godot'),
                     '--script', 'res://scripts/' + script, *before, '--', *arguments],
                    capture_output=True, text=True, timeout=30)

            recorded = run('human_trace.gd', ['--case=spell32', f'--trace={trace}'],
                           ['--quit-after', '120', '--max-fps', '60'])
            self.assertEqual(recorded.returncode, 0, recorded.stdout + recorded.stderr)
            self.assertNotIn('SCRIPT ERROR', recorded.stderr)
            rows = [json.loads(line) for line in trace.read_text().splitlines()]
            self.assertEqual(rows[0]['type'], 'metadata')
            self.assertEqual(rows[-1]['outcome']['status'], 'interrupted')
            self.assertTrue(any(row['type'] == 'step' for row in rows))
            archive = Path(str(trace) + '.build.zip')
            self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), rows[0]['archive_sha256'])
            with zipfile.ZipFile(archive) as build:
                for source, digest in rows[0]['files_sha256'].items():
                    content = build.read('godot/' + source.removeprefix('res://'))
                    self.assertEqual(hashlib.sha256(content).hexdigest(), digest)
                self.assertFalse(any('/.godot/' in name for name in build.namelist()))
            replayed = run('replay.gd', [f'--replay={trace}', '--verify-only'])
            self.assertEqual(replayed.returncode, 0, replayed.stdout + replayed.stderr)
            self.assertNotIn('SCRIPT ERROR', replayed.stderr)
            self.assertIn('Verified all', replayed.stdout)
            next(row for row in rows if row['type'] == 'step')['result']['observation']['health'] = 99
            tampered = Path(folder) / 'tampered.jsonl'
            tampered.write_text(''.join(json.dumps(row) + '\n' for row in rows))
            rejected = run('replay.gd', [f'--replay={tampered}', '--verify-only'])
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn('Replay mismatch at step 1', rejected.stderr)
