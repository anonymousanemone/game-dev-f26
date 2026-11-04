import json
from pathlib import Path
import subprocess
import unittest
from players.engine import Engine, ROOT, godot_binary
from players.baseline import choose

WAIT = dict(move=0, face=0, thrust=False, heka=False)


class GameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = Engine()

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()

    def test_json_numeric_regression(self):
        # Observed during the first baseline run: Dictionary.has rejected float
        # controls produced by JSON.parse_string, making all 1200 actions invalid.
        self.engine.call('reset', seed=30)
        action = json.loads('{"move":0,"face":0,"thrust":true,"heka":false}')
        result = self.engine.call('step', action=action)
        self.assertTrue(result['valid'])
        self.assertEqual(result['outcome']['invalid_actions'], 0)
        self.assertNotEqual(result['observation']['tutorial'], 'thrust')

    def test_legal_actions_and_invalid_handling(self):
        self.engine.call('reset', seed=30)
        actions = self.engine.call('legal_actions')
        self.assertEqual(len(actions), 12)
        for action in [dict(WAIT, face=1), dict(WAIT, move=.5), dict(WAIT, thrust=1),
                       dict(WAIT, move=True), dict(WAIT, extra=1), {}, None]:
            result = self.engine.call('step', action=action)
            self.assertFalse(result['valid'])
        self.assertEqual(result['outcome']['invalid_actions'], 7)
        self.assertEqual(result['outcome']['steps'], 7)
        self.assertAlmostEqual(result['observation']['time'], .7)
        self.assertEqual(self.engine.call('observe', player_id=1), {'error': 'unknown_player'})

    def test_deterministic_seeded_replay(self):
        def play():
            self.engine.call('reset', seed=30, case='spell32')
            return [self.engine.call('step', action=WAIT) for _ in range(20)]
        self.assertEqual(play(), play())

    def test_observation_boundary(self):
        o = self.engine.call('reset', seed=30, case='spell32')
        self.assertEqual(o['crocodiles'], [])  # Waiting figures aren't attack-state hints.
        for _ in range(15):
            o = self.engine.call('step', action=WAIT)['observation']
        forbidden = {'rng', 'seed', 'speed', 'timer', 'red_order', 'wave_launched', 'answer', 'force_heka'}
        def inspect(value):
            if isinstance(value, dict):
                self.assertFalse(forbidden.intersection(value))
                for v in value.values(): inspect(v)
            elif isinstance(value, list):
                for v in value: inspect(v)
        inspect(o)
        self.assertEqual(len(self.engine.call('legal_actions')), 36)

    def test_step_limit_and_terminal_lock(self):
        self.engine.call('reset', seed=30, case='spell31')
        for _ in range(1200):
            result = self.engine.call('step', action=WAIT)
        self.assertEqual(result['outcome']['reason'], 'step_limit')
        self.assertEqual(self.engine.call('legal_actions'), [])
        self.assertEqual(self.engine.call('step', action=WAIT)['error'], 'episode_terminal')

    def test_baseline_complete_successful_path(self):
        observation = self.engine.call('reset', seed=30, case='spell31')
        previous = None
        for _ in range(1200):
            result = self.engine.call('step', action=choose(observation, previous))
            self.assertTrue(result['valid'])
            previous, observation = observation, result['observation']
            if result['outcome']['terminal']: break
        self.assertEqual(result['outcome']['status'], 'won')
        self.assertEqual(result['outcome']['score'], 9)

    def test_original_scene_and_artwork_preserved(self):
        import hashlib
        import re
        manifest = json.loads((ROOT/'reports/direct-extraction.json').read_text())
        text = (ROOT/'godot/scenes/dangers.tscn').read_text()
        blocks = re.split(r'(?=^\[(?:ext_resource|sub_resource|node)\b)', text, flags=re.M)
        actual = {block.splitlines()[0]: hashlib.sha256(block.encode()).hexdigest()
                  for block in blocks if block.strip()}
        self.assertEqual(actual, manifest['retained_scene_blocks'])
        for name, expected in manifest['original_asset_sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(), expected, name)
        self.assertNotIn('spell33_lunging_snake', text)
        self.assertNotIn('spell41_sheaf', text)
        self.assertIn('actors/spell31_crocs', text)
        self.assertIn('actors/spell32_crocs', text)

    def test_godot_rule_invariants(self):
        result = subprocess.run([godot_binary(), '--headless', '--path', str(ROOT/'godot'),
             '--script', 'res://scripts/checks.gd', '--', '--machine'], capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn('SCRIPT ERROR', result.stderr)
        self.assertNotIn('ERROR:', result.stderr)

    def test_both_side_half_body_movement_spacing(self):
        result = subprocess.run([godot_binary(), '--headless', '--path', str(ROOT/'godot'),
            '--script', 'res://scripts/spacing_checks.gd', '--', '--machine'],
            capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn('SCRIPT ERROR', result.stderr)


if __name__ == '__main__': unittest.main()
