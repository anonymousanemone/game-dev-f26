"""Recording evidence must survive replay and detect a changed result."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

from players.engine import ROOT, godot_binary


class HumanTraceTests(unittest.TestCase):
    def test_intro_button_records_native_controls_and_replays_session(self):
        with tempfile.TemporaryDirectory(prefix='crocodiles-native-session-') as folder:
            trace = Path(folder)/'session.jsonl'
            command = [godot_binary(), '--headless', '--path', str(ROOT/'godot')]
            recorded = subprocess.run(command + ['--script', 'res://scripts/session_checks.gd',
                '--max-fps', '60', '--', f'--trace={trace}'], capture_output=True, text=True, timeout=60)
            self.assertEqual(recorded.returncode, 0, recorded.stdout + recorded.stderr)
            self.assertNotIn('SCRIPT ERROR', recorded.stderr)
            self.assertIn('Native session fixture completed', recorded.stdout)
            rows = [json.loads(line) for line in trace.read_text().splitlines()]
            self.assertEqual(rows[0]['format'], 'native_session_v1')
            self.assertEqual(rows[-1]['reason'], 'stopped')
            self.assertTrue(any(row.get('state', {}).get('fight') for row in rows))
            self.assertTrue(any(row.get('state', {}).get('fight', {}).get('lost') for row in rows))
            replayed = subprocess.run(command + ['--script', 'res://scripts/replay.gd', '--',
                f'--replay={trace}', '--verify-only'], capture_output=True, text=True, timeout=30)
            self.assertEqual(replayed.returncode, 0, replayed.stdout + replayed.stderr)
            self.assertNotIn('SCRIPT ERROR', replayed.stderr)
            self.assertIn('recorded native frames', replayed.stdout)
            next(row for row in rows if row['type'] == 'frame')['state']['bites'] = 99
            altered = Path(folder)/'altered.jsonl'
            altered.write_text(''.join(json.dumps(row) + '\n' for row in rows))
            rejected = subprocess.run(command + ['--script', 'res://scripts/replay.gd', '--',
                f'--replay={altered}', '--verify-only'], capture_output=True, text=True, timeout=30)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn('Session replay mismatch', rejected.stderr)

    def test_archive_replay_and_tamper_detection(self):
        with tempfile.TemporaryDirectory(prefix='crocodiles-trace-') as folder:

            def run(script, arguments):
                return subprocess.run(
                    [godot_binary(), '--headless', '--path', str(ROOT/'godot'),
                     '--script', 'res://scripts/' + script, '--', *arguments],
                    capture_output=True, text=True, timeout=30)

            # An archived step trace from the deterministic baseline (no model call).
            recorded = subprocess.run([sys.executable, '-m', 'players.run', '--policy', 'baseline',
                '--case', 'spell32', '--out', folder], cwd=ROOT, capture_output=True, text=True, timeout=120)
            self.assertEqual(recorded.returncode, 0, recorded.stdout + recorded.stderr)
            trace = next(Path(folder).glob('*/spell32-30.jsonl'))
            rows = [json.loads(line) for line in trace.read_text().splitlines()]
            self.assertTrue(any(row.get('type') == 'step' for row in rows))
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
            next(row for row in rows if row.get('type') == 'step')['result']['observation']['health'] = 99
            tampered = trace.parent / 'tampered.jsonl'
            tampered.write_text(''.join(json.dumps(row) + '\n' for row in rows))
            rejected = run('replay.gd', [f'--replay={tampered}', '--verify-only'])
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn('Replay mismatch at step 1', rejected.stderr)
