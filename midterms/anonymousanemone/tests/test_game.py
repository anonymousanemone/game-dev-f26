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
        self.assertEqual(len(actions), 13)  # 12 control combinations plus one look
        for action in [dict(WAIT, face=1), dict(WAIT, move=.5), dict(WAIT, thrust=1),
                       dict(WAIT, move=True), dict(WAIT, extra=1), {}, None]:
            result = self.engine.call('step', action=action)
            self.assertFalse(result['valid'])
        self.assertEqual(result['outcome']['invalid_actions'], 7)
        self.assertEqual(result['outcome']['steps'], 7)
        self.assertAlmostEqual(result['observation']['time'], .7)
        self.assertEqual(self.engine.call('observe', player_id=1), {'error': 'unknown_player'})

    def test_heka_discovery_by_looking(self):
        # Like a human clicking the glowing word: the rule is learned in the game, not given.
        o = self.engine.call('reset', seed=30, case='spell32')
        self.assertTrue(o['heka_word_glowing'])
        self.assertEqual(o['notes'], [])
        look = dict(WAIT, look=True)
        self.assertIn(look, self.engine.call('legal_actions'))
        y = o['player_y']
        # Reading takes the hands off the keys: other controls are ignored for the whole look.
        r = self.engine.call('step', action=dict(look, move=1, thrust=True))
        self.assertTrue(r['valid'])
        self.assertEqual(r['outcome']['steps'], 10)
        self.assertEqual(r['observation']['player_y'], y)
        self.assertFalse(r['observation']['thrusting'])
        notes = r['observation']['notes']
        self.assertEqual(len(notes), 1)
        self.assertIn('[shift]', notes[0])
        # The note is remembered after later messages; looking again adds nothing.
        r = self.engine.call('step', action=look)
        self.assertEqual(r['observation']['notes'], notes)
        self.assertFalse(self.engine.call('step', action=dict(WAIT, look=1))['valid'])
        # Without a look the rule is never noted.
        o = self.engine.call('reset', seed=30, case='spell32')
        for _ in range(20):
            o = self.engine.call('step', action=WAIT)['observation']
        self.assertEqual(o['notes'], [])

    def test_speed_scale_for_difficulty_sweeps(self):
        # An evaluation setting chosen by whoever calls reset; the default leaves the game as tuned.
        def per_step(scale):
            o = self.engine.call('reset', seed=30, case='spell32', speed_scale=scale)
            seen = []
            while len(seen) < 2:
                o = self.engine.call('step', action=WAIT)['observation']
                if o['crocodiles']: seen.append(o['crocodiles'][0]['snout'][0])
            return abs(seen[1] - seen[0])
        normal = per_step(1.0)
        self.assertAlmostEqual(per_step(1.5), 1.5 * normal, delta=1.0)
        self.engine.call('reset', seed=30, case='spell32')
        self.assertAlmostEqual(per_step(1.0), normal)

    def test_crocodile_distances_derived_from_the_screen(self):
        # Precomputed from visible positions so the model need not do coordinate arithmetic.
        o = self.engine.call('reset', seed=30, case='spell32')
        while not o['crocodiles']:
            o = self.engine.call('step', action=WAIT)['observation']
        first = o['crocodiles'][0]
        self.assertIsNone(first['seconds_to_bearer'])  # motion not yet seen
        o = self.engine.call('step', action=WAIT)['observation']
        c = o['crocodiles'][0]
        self.assertAlmostEqual(c['dx_from_tip'], c['snout'][0] - o['tip'][0])
        self.assertAlmostEqual(c['dy_from_tip'], c['snout'][1] - o['tip'][1])
        self.assertEqual(c['side'], 'left' if c['snout'][0] < o['player_x'] else 'right')
        moved = abs(c['snout'][0] - first['snout'][0]) / o['step_seconds']
        expected = (o['player_x'] - c['snout'][0]) * c['direction'] / moved
        self.assertAlmostEqual(c['seconds_to_bearer'], expected, places=2)

    def test_lives_and_crocodile_count_settings(self):
        # Evaluation settings for longer learning experiments; defaults are the tuned game.
        o = self.engine.call('reset', seed=30, case='spell32')
        self.assertEqual((o['health'], o['total']), (3, 14))
        o = self.engine.call('reset', seed=30, case='spell32', lives=5, crocodiles=20)
        self.assertEqual((o['health'], o['total']), (5, 20))
        self.assertEqual(self.engine.call('reset', seed=30, case='spell31', crocodiles=20),
                         {'error': 'crocodiles_needs_one_wave'})

    def test_optional_in_reach_flag(self):
        # Geometry only: the spear's stroke touches the crocodile where it is now (no prediction).
        o = self.engine.call('reset', seed=30, case='spell32')
        while not o['crocodiles']:
            o = self.engine.call('step', action=WAIT)['observation']
        self.assertNotIn('in_reach', o['crocodiles'][0])  # off unless an experiment asks for it
        o = self.engine.call('reset', seed=30, case='spell32', reach_flag=True)
        history, flagged = [], []
        for _ in range(150):
            r = self.engine.call('step', action=choose(o, history))
            history, o = (history + [o])[-10:], r['observation']
            for c in o['crocodiles']:
                self.assertIsInstance(c['in_reach'], bool)
                if c['in_reach']: flagged.append(c)
            if r['outcome']['terminal']: break
        self.assertTrue(flagged)
        for c in flagged:
            self.assertLess(abs(c['dy_from_tip']), c['height'])
            self.assertLess(abs(c['dx_from_tip']), c['width'])

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
        self.assertEqual(len(self.engine.call('legal_actions')), 37)  # 36 control combinations plus one look

    def test_step_limit_and_terminal_lock(self):
        self.engine.call('reset', seed=30, case='spell31')
        for _ in range(1200):
            result = self.engine.call('step', action=WAIT)
        self.assertEqual(result['outcome']['reason'], 'step_limit')
        self.assertEqual(self.engine.call('legal_actions'), [])
        self.assertEqual(self.engine.call('step', action=WAIT)['error'], 'episode_terminal')

    def test_look_stops_at_remaining_step_budget(self):
        for action in (dict(WAIT, look=True), dict(WAIT, look='invalid')):
            self.engine.call('reset', seed=30, case='spell31')
            for _ in range(1195):
                self.engine.call('step', action=WAIT)
            result = self.engine.call('step', action=action)
            expected = 1200 if action['look'] is True else 1196
            self.assertEqual(result['outcome']['steps'], expected)
            self.assertAlmostEqual(result['observation']['time'], expected / 10)
            self.assertEqual(result['valid'], action['look'] is True)
            if result['valid']:
                self.assertEqual(result['outcome']['reason'], 'step_limit')

    def test_baseline_complete_successful_path(self):
        observation = self.engine.call('reset', seed=30, case='spell31')
        history = []
        for _ in range(1200):
            result = self.engine.call('step', action=choose(observation, history))
            self.assertTrue(result['valid'])
            history, observation = (history + [observation])[-10:], result['observation']
            if result['outcome']['terminal']: break
        self.assertEqual(result['outcome']['status'], 'won')
        self.assertEqual(result['outcome']['score'], 9)

    def test_baseline_reacts_only_after_human_reaction_time(self):
        from players import baseline
        self.assertEqual(baseline.REACTION_SECONDS, 0.4)
        # Student recordings: a new crocodile is acted on 0.4-1.2 s after it appears; the baseline uses 0.4 s.
        def seen(time, x):
            return {'tutorial': '', 'time': time, 'both_sides': False, 'player_x': 500.0,
                    'tip': [400.0, 300.0], 'facing': -1, 'thrusting': False,
                    'crocodiles': [{'snout': [x, 300.0], 'direction': 1, 'red': False,
                                    'width': 200.0, 'height': 80.0}]}
        empty = dict(seen(0.0, 0.0), crocodiles=[])
        now = seen(1.0, 395.0)  # aligned and in reach of the tip
        just_appeared = [dict(empty, time=t / 10) for t in range(7)] + [seen(.7 + t / 10, 317.0 + 26 * t) for t in range(3)]  # visible 0.3 s
        self.assertEqual(choose(now, just_appeared), dict(move=0, face=0, thrust=False, heka=False))
        visible_long_enough = [seen(.1 * t, 135.0 + 26 * t) for t in range(10)]
        self.assertTrue(choose(now, visible_long_enough)['thrust'])

    def test_original_scene_and_artwork_preserved(self):
        import hashlib
        import re
        manifest = json.loads((ROOT/'reports/provenance/direct-extraction.json').read_text())
        text = (ROOT/'godot/scenes/dangers.tscn').read_text()
        blocks = re.split(r'(?=^\[(?:ext_resource|sub_resource|node)\b)', text, flags=re.M)
        # Trailing whitespace is ignored: Godot adds or drops blank lines between blocks on save.
        actual = {block.splitlines()[0]: hashlib.sha256(block.rstrip().encode()).hexdigest()
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
        # Godot's headless renderer cannot compile the success-glow shader's sampler and says so;
        # windowed runs do not (the original Totenbuch autotest prints the same line).
        headless_shader = 'ERROR: Condition "!actions.custom_samplers.has(function->arguments[j].tex_builtin)" is true.'
        stderr = '\n'.join(line for line in result.stderr.splitlines() if not line.startswith(headless_shader))
        self.assertNotIn('ERROR:', stderr)

    def test_both_side_half_body_movement_spacing(self):
        result = subprocess.run([godot_binary(), '--headless', '--path', str(ROOT/'godot'),
            '--script', 'res://scripts/spacing_checks.gd', '--', '--machine'],
            capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn('SCRIPT ERROR', result.stderr)


if __name__ == '__main__': unittest.main()
