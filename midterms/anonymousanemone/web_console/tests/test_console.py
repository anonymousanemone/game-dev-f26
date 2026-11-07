"""Transport tests: no provider calls or cloud credentials required."""
import http.client
import json
import threading
import unittest
from unittest.mock import patch

from web_console.server import Server
from web_console.runner import run_spells
from pathlib import Path
import tempfile


class ConsoleTests(unittest.TestCase):
    def setUp(self):
        self.server = Server(('127.0.0.1', 0))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def request(self, method, path, data=None, headers=None):
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_port)
        connection.request(method, path, json.dumps(data) if data else None, headers or {})
        response = connection.getresponse()
        result = response.status, response.read()
        connection.close()
        return result

    def test_page_and_no_arbitrary_file_access(self):
        self.assertEqual(self.request('GET', '/')[0], 200)
        self.assertEqual(self.request('GET', '/../server.py')[0], 404)
        self.assertEqual(self.request('GET', '/replay/../server.py')[0], 404)
        self.assertEqual(self.request('GET', '/api/config', headers={'Host': 'untrusted.example'})[0], 403)

    def test_saved_examples_are_listed_and_need_no_run_or_spending(self):
        status, body = self.request('GET', '/api/examples')
        self.assertEqual(status, 200)
        examples = json.loads(body)
        self.assertEqual(len(examples), 3)
        for item in examples:
            self.assertTrue(item['run'].startswith('example-'))
            self.assertTrue(item['episode'].startswith('spell32'))
            # Trace is served only when the matching browser build exists (409 otherwise).
            url = f"/api/runs/{item['run']}/trace?episode={item['episode']}"
            self.assertIn(self.request('GET', url)[0], (200, 409))
            self.assertIn(self.request('GET', f"/api/runs/{item['run']}/trace?episode=unknown")[0], (404, 409))
            self.assertEqual(self.request('GET', f"/api/runs/{item['run']}/events")[0], 404)

    def test_examples_outside_playtrace_are_refused(self):
        listing = {'examples': [{'id': 'x', 'title': 't', 'summary': 's', 'trace': 'godot/project.godot'},
                                {'id': 'y', 'title': 't', 'summary': 's', 'trace': '../../../etc/hosts'}]}
        with patch('web_console.server.json.loads', return_value=listing):
            from web_console.server import load_examples
            self.assertEqual(load_examples(), {})

    def test_run_requires_token_and_explicit_live_authorization(self):
        settings = dict(case='both', policy='model', history=2)
        self.assertEqual(self.request('POST', '/api/runs', settings)[0], 403)
        headers = {'X-Console-Token': self.server.token}
        self.assertEqual(self.request('POST', '/api/runs', settings, headers)[0], 400)
        settings['case'] = '--arbitrary-command'
        self.assertEqual(self.request('POST', '/api/runs', settings, headers)[0], 400)

    def test_stream_keeps_run_identity_and_resumes(self):
        class FakeRun:
            id = 'test-run'
            done = False
            ready = False
            condition = threading.Condition()
            events = [{'kind': 'log', 'text': 'first'}, {'kind': 'complete', 'replay': True}]
            def __init__(self, *args): pass
            def execute(self): self.done = True
        with patch('web_console.server.Run', FakeRun):
            status, body = self.request('POST', '/api/runs', dict(case='both', policy='baseline', history=2), {'X-Console-Token': self.server.token})
            self.assertEqual(status, 200)
            self.assertEqual(json.loads(body)['id'], 'test-run')
            status, body = self.request('GET', '/api/runs/test-run/events', headers={'Last-Event-ID': '0'})
            self.assertEqual(status, 200)
            self.assertNotIn(b'first', body)
            self.assertIn(b'complete', body)


class SharedBudgetTests(unittest.TestCase):
    def test_second_spell_receives_only_unused_reservations(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            commands = []
            def run(command, cwd):
                commands.append(command)
                case = command[command.index('--case') + 1]
                output = folder / case
                output.mkdir()
                (output / 'summary.json').write_text(json.dumps([
                    {'case': case, 'reserved_cost_usd': 2.25 if case == 'spell31' else .5}]))
                return type('Result', (), {'returncode': 0})()
            with patch('web_console.runner.subprocess.run', side_effect=run):
                run_spells(folder, 'model', 2)
            self.assertEqual([c[c.index('--case')+1] for c in commands], ['spell31', 'spell32'])
            self.assertEqual([float(c[c.index('--max-cost-usd')+1]) for c in commands], [5., 2.75])
            self.assertEqual(json.loads((folder/'budget.json').read_text())['reserved_usd'], 2.75)

    def test_accounting_failure_stops_before_another_paid_episode(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch('web_console.runner.subprocess.run') as run:
                run.return_value.returncode = 1
                with self.assertRaises(RuntimeError):
                    run_spells(Path(temp), 'model', 2)
                self.assertEqual(run.call_count, 1)


if __name__ == '__main__':
    unittest.main()
