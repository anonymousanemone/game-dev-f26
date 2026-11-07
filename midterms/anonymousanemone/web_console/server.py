"""Local run console. Start from the midterm folder: python -m web_console.server."""
import argparse
import contextlib
import io
import json
import mimetypes
import secrets
import os
import signal
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from players.config import load_env
from players.engine import ROOT
from players.watch import show_step
from .runner import TOTAL_BUDGET_USD

HERE = Path(__file__).resolve().parent


class Run:
    def __init__(self, case, policy, history):
        self.id = secrets.token_hex(12)
        self.folder = HERE / 'runs' / self.id
        self.folder.mkdir(parents=True)
        self.events = []
        self.condition = threading.Condition()
        self.done = False
        self.trace = None
        self.traces = {}
        self.ready = False
        self.process = None
        self.replay_identity = None
        self.command = [sys.executable, '-u', '-m', 'web_console.runner',
                        '--policy', policy, '--history', str(history), '--out', str(self.folder)]

    def emit(self, kind, **data):
        with self.condition:
            self.events.append(dict(kind=kind, **data))
            self.condition.notify_all()

    def execute(self):
        try:
            self.emit('log', text='Starting existing players.run evaluator.\n')
            process = subprocess.Popen(self.command, cwd=ROOT, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, text=True, start_new_session=True)
            self.process = process
            def output():
                for line in process.stdout:
                    self.emit('log', text=line)
                process.stdout.close()
            reader = threading.Thread(target=output, daemon=True)
            reader.start()
            positions = {}
            def drain():
                for trace in sorted(self.folder.glob('*/*.jsonl')):
                    self.traces[trace.stem] = trace
                    offset, pending = positions.get(trace, (0, b''))
                    with trace.open('rb') as handle:
                        handle.seek(offset)
                        chunk = handle.read()
                        offset = handle.tell()
                    lines = (pending + chunk).split(b'\n')
                    pending = lines.pop()
                    positions[trace] = (offset, pending)
                    for line in lines:
                        if not line.strip():
                            continue
                        row = json.loads(line)
                        self.emit('row', episode=trace.stem, row=row)
                        if row.get('type') == 'reset':
                            self.emit('log', text=f'\n=== {trace.stem} ===\n')
                        if row.get('type') == 'step':
                            stream = io.StringIO()
                            with contextlib.redirect_stdout(stream):
                                show_step(row)
                            self.emit('log', text=stream.getvalue())
            while process.poll() is None:
                drain()
                time.sleep(.1)
            reader.join()
            drain()
            if process.returncode != 0 or not list(self.folder.glob('*/summary.json')):
                raise RuntimeError('Runner failed or produced no complete summary; exit %s' % process.returncode)
            for name, trace in self.traces.items():
                self.emit('log', text=f'Checking {name} with the native replay verifier…\n')
                check = subprocess.run([sys.executable, '-m', 'players.replay', str(trace), '--verify'],
                                       cwd=ROOT, capture_output=True, text=True, timeout=120)
                self.emit('log', text=check.stdout + check.stderr)
                if check.returncode:
                    raise RuntimeError(f'Native replay verification failed: {name}')
            manifest = HERE / 'build' / 'source.json'
            if not manifest.exists() or json.loads(manifest.read_text()) != source_identity():
                raise RuntimeError('Run completed and verified. Build the matching browser replay: python -m web_console.build')
            self.replay_identity = json.loads(manifest.read_text())
            self.ready = True
            self.emit('complete', replay=True, episodes=list(self.traces),
                      budget=json.loads((self.folder / 'budget.json').read_text()))
        except Exception as exc:
            self.emit('error', text=str(exc))
        finally:
            self.cancel()
            with self.condition:
                self.done = True
                self.condition.notify_all()

    def cancel(self):
        if self.process is not None and self.process.poll() is None:
            os.killpg(self.process.pid, signal.SIGTERM)
            self.process.wait(timeout=10)


class Example:
    """A saved, already-recorded episode served through the same replay route as a run."""
    done = True
    ready = True

    def __init__(self, trace):
        self.traces = {trace.stem: trace}
        self.replay_identity = None


def load_examples():
    """Saved episodes listed in examples.json; only files under playtrace/ are served."""
    listing = json.loads((HERE / 'examples.json').read_text())['examples']
    playtrace = (ROOT / 'playtrace').resolve()
    examples = {}
    for item in listing:
        trace = (ROOT / item['trace']).resolve()
        if trace.is_relative_to(playtrace) and trace.suffix == '.jsonl' and trace.is_file():
            examples[item['id']] = (item, Example(trace))
    return examples


def source_identity():
    import hashlib
    from players.engine import godot_binary
    return {'godot': subprocess.check_output([godot_binary(), '--version'], text=True).strip(),
            'files': {str(p.relative_to(ROOT / 'godot')): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in sorted((ROOT / 'godot').rglob('*')) if p.is_file()
                      and '.godot' not in p.parts and p.suffix not in ('.uid', '.import')
                      and p.name != '.DS_Store'}}


class Server(ThreadingHTTPServer):
    daemon_threads = True
    def __init__(self, address):
        super().__init__(address, Handler)
        self.runs = {}
        self.lock = threading.Lock()
        self.token = secrets.token_urlsafe(32)
        load_env(ROOT / '.env')
        self.examples = load_examples()
        manifest = HERE / 'build' / 'source.json'
        identity = json.loads(manifest.read_text()) if manifest.exists() else None
        for key, (_, example) in self.examples.items():
            example.replay_identity = identity
            self.runs['example-' + key] = example


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def send_bytes(self, data, content_type='application/json', status=200):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        self.end_headers()
        self.wfile.write(data)

    def valid_host(self):
        return self.headers.get('Host') in (f'127.0.0.1:{self.server.server_port}',
                                           f'localhost:{self.server.server_port}')

    def do_POST(self):
        if not self.valid_host():
            return self.send_bytes(b'Forbidden host', 'text/plain', 403)
        if self.path != '/api/runs' or self.headers.get('X-Console-Token') != self.server.token:
            return self.send_bytes(b'{"error":"Forbidden"}', status=403)
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length < 4096:
                raise ValueError('Invalid request length')
            data = json.loads(self.rfile.read(length))
            case, policy, history = data['case'], data['policy'], data['history']
            if case != 'both' or policy not in ('baseline', 'model') or history not in (0, 2):
                raise ValueError('Invalid run settings')
            if policy == 'model' and data.get('authorize_live') is not True:
                raise ValueError('Live play requires explicit spending authorization')
            with self.server.lock:
                if any(not r.done for r in self.server.runs.values()):
                    return self.send_bytes(b'{"error":"A run is already active"}', status=409)
                run = Run(case, policy, history)
                self.server.runs[run.id] = run
                threading.Thread(target=run.execute, daemon=True).start()
            self.send_bytes(json.dumps({'id': run.id}).encode())
        except (ValueError, KeyError, TypeError):
            self.send_bytes(b'{"error":"Invalid run request"}', status=400)

    def do_GET(self):
        if not self.valid_host():
            return self.send_bytes(b'Forbidden host', 'text/plain', 403)
        path = urlsplit(self.path).path
        if path == '/api/config':
            return self.send_bytes(json.dumps({'token': self.server.token,
                'web_ready': (HERE / 'build/replay.html').exists(),
                'model': os.environ.get('CROC_MODEL'),
                'max_cost_usd': TOTAL_BUDGET_USD,
                'provider': 'Vertex', 'cases': ['spell31', 'spell32'], 'seed': 30,
                'input_price': os.environ.get('CROC_INPUT_PRICE'),
                'output_price': os.environ.get('CROC_OUTPUT_PRICE'),
                'price_date': os.environ.get('CROC_PRICE_DATE')}).encode())
        if path == '/api/examples':
            return self.send_bytes(json.dumps([
                {'id': key, 'title': item['title'], 'summary': item['summary'],
                 'run': 'example-' + key, 'episode': next(iter(example.traces))}
                for key, (item, example) in self.server.examples.items()]).encode())
        parts = path.strip('/').split('/')
        if len(parts) == 4 and parts[:2] == ['api', 'runs']:
            run = self.server.runs.get(parts[2])
            if not run:
                return self.send_bytes(b'Not found', 'text/plain', 404)
            if parts[3] == 'trace' and run.ready:
                manifest = HERE / 'build/source.json'
                if not manifest.exists() or json.loads(manifest.read_text()) != run.replay_identity:
                    return self.send_bytes(b'Browser build changed; start a new run.', 'text/plain', 409)
                episode = parse_qs(urlsplit(self.path).query).get('episode', [''])[0]
                trace = run.traces.get(episode)
                if trace is None:
                    return self.send_bytes(b'Unknown episode', 'text/plain', 404)
                return self.send_bytes(trace.read_bytes(), 'application/x-ndjson')
            if parts[3] == 'events' and isinstance(run, Run):
                self.send_response(200)
                self.send_header('Content-Type', 'text/event-stream')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                try:
                    index = int(self.headers.get('Last-Event-ID', '-1')) + 1
                    while True:
                        with run.condition:
                            if index >= len(run.events) and not run.done:
                                run.condition.wait(10)
                            batch = run.events[index:]
                            done = run.done
                        for event in batch:
                            self.wfile.write(f'id: {index}\ndata: {json.dumps(event)}\n\n'.encode())
                            index += 1
                        self.wfile.write(b': heartbeat\n\n')
                        self.wfile.flush()
                        if done and index == len(run.events):
                            return
                except (BrokenPipeError, ConnectionResetError):
                    return
        base = HERE / ('build' if path.startswith('/replay/') else 'static')
        relative = path.removeprefix('/replay/') if base.name == 'build' else path.lstrip('/') or 'index.html'
        file = (base / relative).resolve()
        if not file.is_relative_to(base.resolve()) or not file.is_file():
            return self.send_bytes(b'Not found', 'text/plain', 404)
        self.send_bytes(file.read_bytes(), mimetypes.guess_type(file)[0] or 'application/octet-stream')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    with Server(('127.0.0.1', args.port)) as server:
        print(f'Console: http://127.0.0.1:{server.server_port}', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            for run in server.runs.values():
                run.cancel()


if __name__ == '__main__':
    main()
