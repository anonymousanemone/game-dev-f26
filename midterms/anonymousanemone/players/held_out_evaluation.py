"""Frozen 18-episode evaluation with one shared budget and a live approval gate."""
import datetime
import hashlib
import json
import os
import subprocess
import time
from types import SimpleNamespace

from . import model, run
from .config import load_env
from .engine import ROOT, Engine, godot_binary
from .traces import archive


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


class EvaluationClock:
    def __init__(self):
        self.paused = 0.0

    def monotonic(self):
        return time.monotonic() - self.paused


def main():
    load_env(ROOT/'.env')
    suite = json.loads((ROOT/'suite.json').read_text())
    maintained = json.loads((ROOT/'agent-config.json').read_text())
    prompt_hash = hashlib.sha256(model.PROMPT.encode()).hexdigest()
    assert prompt_hash == maintained['player']['tuned_prompt']['sha256']
    required = ['GOOGLE_CLOUD_PROJECT', 'CROC_INPUT_PRICE', 'CROC_OUTPUT_PRICE',
                'CROC_PRICE_DATE', 'CROC_PRICE_SOURCE']
    if any(not os.environ.get(k) for k in required):
        raise ValueError('Missing provider configuration or dated prices')
    args = SimpleNamespace(model='gemini-3.5-flash-lite', history=2, memory=False,
        lives=3, crocodiles=0, reach_flag=False, max_calls=suite['model_call_limit'],
        call_timeout=suite['call_timeout_seconds'], episode_timeout=suite['episode_timeout_seconds'],
        max_cost_usd=20.0, input_price=float(os.environ['CROC_INPUT_PRICE']),
        output_price=float(os.environ['CROC_OUTPUT_PRICE']),
        price_date=os.environ['CROC_PRICE_DATE'], price_source=os.environ['CROC_PRICE_SOURCE'])
    if min(args.input_price, args.output_price) < 0:
        raise ValueError('Negative prices')
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output = ROOT/'playtrace'/f'{stamp}-held-out-final'
    output.mkdir(exist_ok=False)
    print('Evaluation:', output, flush=True)
    game_hash = run.version()
    source_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in sorted((ROOT/'players').glob('*.py'))}
    suite_hash = hashlib.sha256((ROOT/'suite.json').read_bytes()).hexdigest()
    config = dict(date_utc=stamp, split='held_out', provider='vertex',
        runtime_model=args.model, location=os.environ.get('GOOGLE_CLOUD_LOCATION') or 'global',
        prompt=model.PROMPT, prompt_sha256=prompt_hash, game_version=game_hash,
        suite_sha256=suite_hash, player_source_sha256=source_hashes,
        godot_version=subprocess.check_output([godot_binary(), '--version'], text=True).strip(),
        arguments=vars(args).copy(), max_output_tokens=model.MAX_OUTPUT_TOKENS,
        total_authorized_usd=20, pause_at_reserved_usd=16,
        baseline_history='up to ten retained observations for reaction delay; velocity uses previous observation',
        model_history=[0, 2], memory=False, reach_flag=False, speed_scale=1,
        prior_knowledge='Both policies know the red/plain heka rule; model uses frozen combined instructions',
        order=['baseline', 'model-h0', 'model-h2'],
        episodes=[dict(case=c['id'], seed=s) for c in suite['cases'] for s in c['held_out_seeds']])
    save(output/'configuration.json', config)
    budget = {'reserved_usd': 0.0}
    gate = {'threshold': 16.0, 'stopped': False}
    clock = EvaluationClock()
    original_clock, original_reservation = run.time, model.cost_reservation
    run.time = clock  # Only approval waiting is excluded from active episode time.

    def frozen():
        if run.version() != game_hash or hashlib.sha256((ROOT/'suite.json').read_bytes()).hexdigest() != suite_hash:
            raise RuntimeError('Frozen game/suite changed; stopping without rerunning episodes')
        for name, expected in source_hashes.items():
            if hashlib.sha256((ROOT/'players'/name).read_bytes()).hexdigest() != expected:
                raise RuntimeError('Frozen player source changed; stopping')

    def reserve(*a, **kw):
        frozen()
        amount = original_reservation(*a, **kw)
        if not gate['stopped'] and budget['reserved_usd'] + amount >= gate['threshold']:
            save(output/'budget-paused.json', dict(reserved_usd=budget['reserved_usd'],
                next_call_reservation=amount, cap_usd=args.max_cost_usd,
                message='Paused before next call; awaiting explicit user budget decision'))
            print('BUDGET PAUSED:', budget['reserved_usd'], flush=True)
            started = time.monotonic()
            decision = output/'budget-decision.json'
            while not decision.exists():
                time.sleep(1)
            approved = json.loads(decision.read_text())
            decision.rename(output/f'budget-decision-{time.time_ns()}.json')
            clock.paused += time.monotonic()-started
            if approved.get('stop'):
                args.max_cost_usd = budget['reserved_usd']
                gate['stopped'] = True
            else:
                cap = float(approved['max_cost_usd'])
                threshold = float(approved['pause_at_usd'])
                if not budget['reserved_usd'] + amount < threshold <= cap:
                    raise ValueError('Invalid approved cap/threshold')
                args.max_cost_usd, gate['threshold'] = cap, threshold
            frozen()
        return amount

    model.cost_reservation = reserve
    results = []
    try:
        for policy, history in [('baseline', 2), ('model', 0), ('model', 2)]:
            args.history = history
            label = 'baseline' if policy == 'baseline' else f'model-h{history}'
            folder = output/label
            folder.mkdir()
            for case in suite['cases']:
                for seed in case['held_out_seeds']:
                    if gate['stopped']:
                        break
                    frozen()
                    path = folder/f"{case['id']}-{seed}.jsonl"
                    metadata = archive(path)
                    metadata.update(policy=policy, configuration='../configuration.json')
                    with Engine() as engine, path.open('x') as trace:
                        run.write_trace(trace, metadata)
                        summary = run.episode(engine, case['id'], seed, policy, args, suite, trace, budget)
                    result = dict(condition=label, trace=str(path.relative_to(ROOT)), **summary)
                    results.append(result)
                    save(folder/f"{case['id']}-{seed}.summary.json", result)
                    save(output/'results.json', results)
                    save(output/'budget.json', dict(**budget, cap_usd=args.max_cost_usd,
                        pause_at_usd=gate['threshold'], approval_pause_seconds=clock.paused))
                    print(json.dumps(result), flush=True)
            if gate['stopped']:
                break
        frozen()
        save(output/'completion.json', dict(completed_episodes=len(results), expected_episodes=18,
            stopped_by_budget_decision=gate['stopped'], reserved_usd=budget['reserved_usd']))
    finally:
        model.cost_reservation, run.time = original_reservation, original_clock
    print('Results:', output, flush=True)


if __name__ == '__main__':
    main()
