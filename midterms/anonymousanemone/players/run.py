"""Bounded evaluator. python -m players.run --help"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import time

from . import baseline, model
from .engine import Engine, ROOT
from .config import load_env
from .traces import archive


def write_trace(trace, row):
    trace.write(json.dumps(row) + '\n')
    trace.flush()


def version():
    digest = hashlib.sha256()
    for p in sorted((ROOT / 'godot').rglob('*')):
        # Finder's .DS_Store files are not game content and are absent from a fresh clone.
        if p.is_file() and '.godot' not in p.parts and p.suffix not in ('.import', '.uid') and p.name != '.DS_Store':
            digest.update(str(p.relative_to(ROOT)).encode())
            digest.update(p.read_bytes())
    return digest.hexdigest()


MEMORY_EVENTS = 60   # the event log keeps the most recent entries


def memory_events(before, action, after):
    """What one step added to the model's event log: its own action and what it was then shown."""
    t0, t1 = f"t={before['time']:.1f}s", f"t={after['time']:.1f}s"
    events = []
    if action and action.get('look'):
        events.append(f'{t0}: looked at the word of power')
    elif action and action.get('thrust'):
        heka = 'on' if action.get('heka') else 'off'
        if before['crocodiles']:
            c = min(before['crocodiles'], key=lambda c: abs(c['dx_from_tip']))
            events.append(f"{t0}: thrust, heka {heka}; nearest crocodile {'red' if c['red'] else 'plain'}, "
                          f"{c['side']}, dx_from_tip {round(c['dx_from_tip'])}, dy_from_tip {round(c['dy_from_tip'])}")
        else:
            events.append(f'{t0}: thrust, heka {heka}; no crocodile visible')
    if after['killed'] > before['killed']:
        n = after['killed'] - before['killed']
        events.append(f"{t1}: {n} crocodile{'s' if n > 1 else ''} turned back (total {after['killed']})")
    if after['health'] < before['health']:
        events.append(f"{t1}: bitten, health now {after['health']}")
    if after['message'] != before['message'] and after['message']:
        events.append(f"{t1}: game said: {after['message']}")
    return events


def episode(engine, case, seed, policy, args, suite, trace, budget=None):
    if budget is None:
        budget = {'reserved_usd': 0.0}
    initial_reservation = budget['reserved_usd']
    reset_settings = dict(speed_scale=getattr(args, 'speed_scale', 1.0),
                          lives=getattr(args, 'lives', 3),
                          crocodiles=getattr(args, 'crocodiles', 0),
                          reach_flag=getattr(args, 'reach_flag', False))
    observation = engine.call('reset', seed=seed, case=case, **reset_settings)
    memory = [] if getattr(args, 'memory', False) else None
    history = []
    calls = failed_calls = input_tokens = output_tokens = 0
    started = time.monotonic()
    latencies = []
    outcome = engine.call('outcome')
    write_trace(trace, {'type': 'reset', 'case': case, 'seed': seed,
                        'settings': reset_settings, 'observation': observation})
    while not outcome['terminal']:
        if time.monotonic() - started >= args.episode_timeout:
            outcome.update(status='limit', terminal=True, reason='episode_timeout')
            break
        if policy == 'model' and calls >= args.max_calls:
            outcome.update(status='limit', terminal=True, reason='model_call_limit')
            break
        usage, raw, response_id, error = {}, None, None, None
        before = time.monotonic()
        if policy == 'baseline':
            action = baseline.choose(observation, history)
        else:
            model_history = history[-args.history:] if args.history else []
            reserve = model.cost_reservation(observation, model_history, args.model,
                                            args.input_price, args.output_price, memory)
            max_cost = getattr(args, 'max_cost_usd', None)
            if max_cost is not None and budget['reserved_usd'] + reserve > max_cost:
                outcome.update(status='limit', terminal=True, reason='cost_limit')
                break
            budget['reserved_usd'] += reserve
            calls += 1  # Includes provider errors and timeouts.
            try:
                action, usage, raw, response_id = model.choose(observation, model_history, args.model,
                    min(args.call_timeout, max(.01, args.episode_timeout - (before - started))), memory)
            except Exception as exc:
                # Store the error type, never provider bodies which might contain credentials.
                error = type(exc).__name__
                action = None
                failed_calls += 1
        elapsed = time.monotonic() - before
        latencies.append(elapsed)
        input_tokens += usage.get('input_tokens', 0)
        output_tokens += usage.get('output_tokens', 0)
        if time.monotonic() - started >= args.episode_timeout:
            write_trace(trace, {'type': 'call', 'action': action, 'usage': usage, 'error': error,
                                    'latency_seconds': elapsed, 'submitted': False})
            outcome.update(status='limit', terminal=True, reason='episode_timeout')
            break
        result = engine.call('step', action=action)
        write_trace(trace, {'type': 'step', 'observation': observation, 'action': action,
            'step': result['outcome']['steps'],
            # Terminal actions can stop before all six ticks have elapsed.
            'simulation_frame': round(result['observation']['time'] * 60),
            'nominal_simulation_frame': result['outcome']['steps'] * 6,
            'wall_elapsed_seconds': time.monotonic() - started,
            'source': policy, 'fallback': action is None, 'error': error, 'raw': raw,
            'response_id': response_id, 'usage': usage, 'latency_seconds': elapsed, 'result': result,
            **({'memory_sent': memory} if memory is not None and policy == 'model' else {})})
        if memory is not None and 'observation' in result:
            memory = (memory + memory_events(observation, action, result['observation']))[-MEMORY_EVENTS:]
        history.append(observation)
        history = history[-10:]  # the model sees at most the last 2; the baseline's reaction delay looks back 0.6 s
        observation = result['observation']
        outcome = result['outcome']
    cost = None
    if args.input_price is not None and args.output_price is not None:
        cost = (input_tokens * args.input_price + output_tokens * args.output_price) / 1_000_000
    summary = dict(case=case, seed=seed, policy=policy, model=args.model if policy == 'model' else None,
        history=args.history if policy == 'model' else 10,
        derived_motion_in_observation=True,
        memory_events_capacity=MEMORY_EVENTS if memory is not None and policy == 'model' else 0,
        calls=calls, failed_calls=failed_calls,
        input_tokens=input_tokens, output_tokens=output_tokens, estimated_cost_usd=cost,
        max_cost_usd=getattr(args, 'max_cost_usd', None),
        reserved_cost_usd=budget['reserved_usd'] - initial_reservation,
        run_reserved_cost_usd=budget['reserved_usd'],
        price_date=args.price_date, price_source=args.price_source,
        input_price_per_million=args.input_price, output_price_per_million=args.output_price,
        elapsed_seconds=time.monotonic()-started, mean_latency_seconds=sum(latencies)/max(1, len(latencies)),
        outcome=outcome)
    write_trace(trace, {'type': 'summary', **summary})
    return summary


def main():
    load_env(ROOT/'.env')
    parser = argparse.ArgumentParser()
    parser.add_argument('--policy', choices=['baseline', 'model'], default='baseline')
    parser.add_argument('--model', default=os.environ.get('CROC_MODEL'))
    parser.add_argument('--split', choices=['development', 'held_out'], default='development')
    parser.add_argument('--case', choices=['spell31', 'spell32', 'spell32_low'])
    parser.add_argument('--history', type=int, choices=[0, 2], default=2)
    parser.add_argument('--memory', action='store_true', help='Give the model an event log of this episode')
    parser.add_argument('--reach-flag', action='store_true', help='Experiment: add in_reach to each crocodile')
    parser.add_argument('--lives', type=int, default=3, help='Evaluation setting: bites the bearer can take')
    parser.add_argument('--crocodiles', type=int, default=0, help='Evaluation setting: crocodiles to turn back (spell32 cases; 0 = as tuned)')
    parser.add_argument('--max-calls', type=int, default=1200)
    parser.add_argument('--call-timeout', type=float, default=30)
    parser.add_argument('--episode-timeout', type=float, default=1800)
    parser.add_argument('--out', type=Path, default=ROOT/'playtrace')
    parser.add_argument('--max-cost-usd', type=float, default=float(os.environ.get('CROC_MAX_COST_USD', '10')),
                        help='Conservative total reservation cap across this entire invocation')
    parser.add_argument('--input-price', type=float, default=os.environ.get('CROC_INPUT_PRICE'), help='USD per million input tokens')
    parser.add_argument('--output-price', type=float, default=os.environ.get('CROC_OUTPUT_PRICE'), help='USD per million output tokens')
    parser.add_argument('--price-date', default=os.environ.get('CROC_PRICE_DATE'))
    parser.add_argument('--price-source', default=os.environ.get('CROC_PRICE_SOURCE'))
    args = parser.parse_args()
    if args.policy == 'model' and (not args.model or not os.environ.get('GOOGLE_CLOUD_PROJECT')):
        parser.error('Live play requires --model and GOOGLE_CLOUD_PROJECT (in .env or the environment).')
    if args.policy == 'model' and not all(v is not None for v in [args.input_price, args.output_price, args.price_date, args.price_source]):
        parser.error('Live evaluation requires dated input/output prices and --price-source.')
    if args.max_calls < 1 or args.call_timeout <= 0 or args.episode_timeout <= 0 or args.max_cost_usd <= 0:
        parser.error('Budgets must be positive.')
    if args.policy == 'model' and (args.input_price < 0 or args.output_price < 0):
        parser.error('Prices must not be negative.')
    suite = json.loads((ROOT/'suite.json').read_text())
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output = args.out / f'{stamp}-{args.policy}-h{args.history}-{args.split}'
    output.mkdir(parents=True, exist_ok=False)
    configuration = vars(args).copy()
    configuration['out'] = str(args.out)
    (output/'configuration.json').write_text(json.dumps({'date': stamp, 'game_version': version(),
        'suite_sha256': hashlib.sha256((ROOT/'suite.json').read_bytes()).hexdigest(),
        'prompt_sha256': hashlib.sha256(model.PROMPT.encode()).hexdigest(),
        'prompt': model.PROMPT, 'max_output_tokens': model.MAX_OUTPUT_TOKENS,
        'player_source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in sorted((ROOT/'players').glob('*.py'))},
        'arguments': configuration}, indent=2)+'\n')
    summaries = []
    budget = {'reserved_usd': 0.0}
    with Engine() as engine:
        for case in suite['cases']:
            if args.case and case['id'] != args.case:
                continue
            for seed in case[f'{args.split}_seeds']:
                trace_path = output/f"{case['id']}-{seed}.jsonl"
                metadata = archive(trace_path)
                metadata['policy'] = args.policy
                with trace_path.open('x') as trace:
                    write_trace(trace, metadata)
                    row = episode(engine, case['id'], seed, args.policy, args, suite, trace, budget=budget)
                summaries.append(row)
                print(json.dumps(row), flush=True)
    (output/'summary.json').write_text(json.dumps(summaries, indent=2)+'\n')
    print('Results:', output)


if __name__ == '__main__':
    main()
