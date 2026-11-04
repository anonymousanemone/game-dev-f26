import io
import json
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from players import run
from players.engine import Engine


class RunnerTests(unittest.TestCase):
    def test_baseline_summary_reports_actual_history_capacity(self):
        with Engine() as engine:
            summary = run.episode(engine, 'spell31', 30, 'baseline', self.args(), {}, io.StringIO())
        self.assertEqual(summary['history'], 10)
        self.assertTrue(summary['derived_motion_in_observation'])
        self.assertEqual(summary['memory_events_capacity'], 0)

    def args(self, **changes):
        values = dict(history=2, model='test-model', episode_timeout=30, max_calls=2,
                      call_timeout=1, input_price=1, output_price=2,
                      price_date='2026-10-26', price_source='test fixture')
        values.update(changes)
        return SimpleNamespace(**values)

    def test_failed_calls_consume_budget_and_are_fallbacks(self):
        with Engine() as engine, patch.object(run.model, 'choose', side_effect=TimeoutError):
            trace = io.StringIO()
            summary = run.episode(engine, 'spell31', 30, 'model', self.args(), {}, trace)
        self.assertEqual(summary['calls'], 2)
        self.assertEqual(summary['failed_calls'], 2)
        self.assertEqual(summary['outcome']['reason'], 'model_call_limit')
        self.assertEqual(summary['outcome']['invalid_actions'], 2)
        steps = [r for r in map(__import__('json').loads, trace.getvalue().splitlines()) if r['type'] == 'step']
        self.assertTrue(all(r['fallback'] and r['error'] == 'TimeoutError' for r in steps))

    def test_observation_only_and_cost_accounting(self):
        replies = (dict(move=0, face=0, thrust=False, heka=False),
                   dict(input_tokens=100, output_tokens=10), '{}', 'mock-id')
        with Engine() as engine, patch.object(run.model, 'choose', return_value=replies) as choose:
            summary = run.episode(engine, 'spell31', 30, 'model', self.args(history=0), {}, io.StringIO())
        self.assertTrue(all(call.args[1] == [] for call in choose.call_args_list))
        self.assertEqual(summary['input_tokens'], 200)
        self.assertAlmostEqual(summary['estimated_cost_usd'], .00024)
        self.assertEqual(summary['failed_calls'], 0)
        self.assertEqual(summary['history'], 0)
        self.assertTrue(summary['derived_motion_in_observation'])
        self.assertEqual(summary['outcome']['reason'], 'model_call_limit')

    def test_episode_timeout_before_first_call(self):
        with Engine() as engine, patch.object(run.model, 'choose') as choose:
            summary = run.episode(engine, 'spell31', 30, 'model', self.args(episode_timeout=0), {}, io.StringIO())
        choose.assert_not_called()
        self.assertEqual(summary['outcome']['reason'], 'episode_timeout')

    def test_cost_reservation_stops_before_an_unfunded_call(self):
        with Engine() as engine, patch.object(run.model, 'choose') as choose:
            summary = run.episode(engine, 'spell31', 30, 'model',
                self.args(max_cost_usd=0.0000001), {}, io.StringIO())
        choose.assert_not_called()
        self.assertEqual(summary['outcome']['reason'], 'cost_limit')

    def test_failed_calls_keep_their_full_cost_reservation(self):
        with Engine() as engine, patch.object(run.model, 'choose', side_effect=TimeoutError):
            budget = {'reserved_usd': 0.0}
            summary = run.episode(engine, 'spell31', 30, 'model',
                self.args(max_cost_usd=10), {}, io.StringIO(), budget=budget)
        self.assertEqual(summary['failed_calls'], 2)
        self.assertGreater(budget['reserved_usd'], 0)
        self.assertEqual(summary['reserved_cost_usd'], budget['reserved_usd'])


class MemoryTests(unittest.TestCase):
    """The model's optional event log, built only from its own actions and what it was shown."""

    def test_events_from_one_step(self):
        from players.run import memory_events
        croc = {'snout': [300.0, 500.0], 'direction': 1, 'red': False, 'dx_from_tip': -67.0,
                'dy_from_tip': 9.0, 'side': 'left', 'seconds_to_bearer': 0.7}
        before = {'time': 2.0, 'health': 3, 'killed': 0, 'message': 'Go.', 'notes': [], 'crocodiles': [croc]}
        after = dict(before, time=2.1, health=2, killed=1, message='A crocodile earns a snack.')
        events = memory_events(before, dict(move=0, face=0, thrust=True, heka=False), after)
        self.assertEqual(events, [
            't=2.0s: thrust, heka off; nearest crocodile plain, left, dx_from_tip -67, dy_from_tip 9',
            't=2.1s: 1 crocodile turned back (total 1)',
            't=2.1s: bitten, health now 2',
            't=2.1s: game said: A crocodile earns a snack.'])
        self.assertEqual(memory_events(before, dict(move=1, face=0, thrust=False, heka=False), before), [])

    def test_memory_reaches_the_request_only_when_given(self):
        from players import model
        o = {'both_sides': True}
        self.assertNotIn('memory', json.loads(model.request_payload(o, [])['contents'][0]['parts'][0]['text']))
        sent = json.loads(model.request_payload(o, [], ['t=1.0s: bitten'])['contents'][0]['parts'][0]['text'])
        self.assertEqual(sent['memory'], ['t=1.0s: bitten'])


class VertexAdapterTests(unittest.TestCase):
    """Mocked transport: checks the request boundary and usage parsing, not a live model."""

    def test_vertex_request_and_reasoning_tokens_billed_as_output(self):
        import json
        from players import model
        observation = {'both_sides': False, 'health': 3}
        reply = {'responseId': 'r-1', 'modelVersion': 'gemini-3.5-flash-lite',
                 'candidates': [{'finishReason': 'STOP', 'content': {'parts': [
                     {'text': 'thinking', 'thought': True},
                     {'text': '{"move": 1, "face": 0, "thrust": true, "heka": false}'}]}}],
                 'usageMetadata': {'promptTokenCount': 300, 'candidatesTokenCount': 20,
                                   'thoughtsTokenCount': 80, 'totalTokenCount': 400}}
        sent = []

        class Response(io.BytesIO):
            def __enter__(self): return self
            def __exit__(self, *exc): return False

        def fake_urlopen(request, timeout):
            sent.append(request)
            return Response(json.dumps(reply).encode())

        with patch.dict('os.environ', {'GOOGLE_CLOUD_PROJECT': 'demo-project',
                                       'GOOGLE_CLOUD_LOCATION': 'global'}), \
             patch.object(model, 'access_token', return_value='token'), \
             patch.object(model.urllib.request, 'urlopen', side_effect=fake_urlopen):
            action, usage, raw, response_id = model.choose(observation, [], 'gemini-3.5-flash-lite', 5)
        self.assertEqual(action, {'move': 1, 'face': 0, 'thrust': True, 'heka': False})
        self.assertEqual(response_id, 'r-1')
        self.assertEqual(usage['input_tokens'], 300)
        self.assertEqual(usage['output_tokens'], 100)
        self.assertNotIn('thinking', raw)
        self.assertEqual(sent[0].full_url, 'https://aiplatform.googleapis.com/v1/projects/demo-project/'
                         'locations/global/publishers/google/models/gemini-3.5-flash-lite:generateContent')
        body = json.loads(sent[0].data)
        self.assertNotIn('tools', body)
        self.assertEqual(json.loads(body['contents'][0]['parts'][0]['text']),
                         {'history': [], 'observation': observation})
        self.assertEqual(body['generationConfig']['responseSchema']['properties']['face']['maximum'], 0)
        schema = body['generationConfig']['responseSchema']
        self.assertEqual(schema['properties']['look'], {'type': 'BOOLEAN'})
        self.assertIn('look', schema['required'])

    def test_control_prompt_leaves_the_heka_rule_to_discovery(self):
        # The historical control leaves discovery to look; the tuned default teaches the rule.
        from players import model
        prompt = model.BASE_PROMPT.lower()
        for told in ['red crocodile', 'only for red', 'ordinary crocodile', 'shift']:
            self.assertNotIn(told, prompt)
        self.assertIn('look', prompt)


if __name__ == '__main__': unittest.main()
