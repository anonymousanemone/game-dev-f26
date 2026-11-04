"""Two bounded prompt variants; no changes to the default player or game rules."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import statistics
import subprocess
from types import SimpleNamespace

from . import model
from .config import load_env
from .engine import Engine, ROOT, godot_binary
from .run import episode, version, write_trace
from .traces import archive

INSTRUCTION = (
    "Line up with approaching crocodiles by matching the spear tip's y level to "
    "the crocodile's snout y level (dy_from_tip near zero). Positive dy_from_tip "
    "means the crocodile is below your spear: move=1 moves down toward it. "
    "Negative dy_from_tip means it is above: move=-1 moves up toward it. "
    "Use move=0 once lined up; a movement action shifts you about 39 world pixels."
)


def metrics(path):
    rows = [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
    steps = [r for r in rows if r.get('type') == 'step']
    visible = moved = far = toward = useful = toward_any = aligned = thrusts = aligned_thrusts = 0
    errors = []
    for row in steps:
        o, a = row['observation'], row.get('action')
        if not isinstance(a, dict) or not row['result'].get('valid') or a.get('look'):
            continue
        crocs = o.get('crocodiles', [])
        if not crocs:
            continue
        incoming = [c for c in crocs if c.get('seconds_to_bearer') is not None
                    and c['seconds_to_bearer'] >= 0]
        target = (min(incoming, key=lambda c: c['seconds_to_bearer']) if incoming else
                  min(crocs, key=lambda c: abs(c['dx_from_tip'])))
        dy = target['dy_from_tip']
        move = a.get('move', 0)
        visible += 1
        moved += move != 0
        errors.append(abs(dy))
        aligned += abs(dy) <= 20
        if abs(dy) > 20:
            far += 1
            toward += move * dy > 0
        useful += move != 0 and abs(dy - move * 39) < abs(dy)
        toward_any += move != 0 and any(move * c['dy_from_tip'] > 0 for c in crocs)
        if a.get('thrust'):
            thrusts += 1
            aligned_thrusts += abs(dy) <= 20
    summary = next((r for r in reversed(rows) if r.get('type') == 'summary'), None)
    return dict(trace=str(path), decisions=len(steps), visible_control_decisions=visible,
                moving_decisions=moved, moving_toward_any_visible=toward_any,
                nearest_threat_far_decisions=far, moving_toward_nearest_when_far=toward,
                moves_predicted_to_reduce_nearest_error=useful, aligned_decisions=aligned,
                median_abs_dy=statistics.median(errors) if errors else None,
                thrust_decisions_with_visible=thrusts, aligned_thrusts=aligned_thrusts,
                summary=summary)


def run(total_budget=1.0):
    if not 0 < total_budget <= 1.0:
        raise ValueError('Total reservation must be positive and at most the authorized $1')
    load_env(ROOT / '.env')
    if os.environ.get('CROC_MODEL') != 'gemini-3.5-flash-lite':
        raise ValueError('This experiment was authorized for gemini-3.5-flash-lite only')
    required = ['GOOGLE_CLOUD_PROJECT', 'CROC_INPUT_PRICE', 'CROC_OUTPUT_PRICE',
                'CROC_PRICE_DATE', 'CROC_PRICE_SOURCE']
    if any(not os.environ.get(key) for key in required):
        raise ValueError('Missing configured provider or dated prices; no calls made')
    suite = json.loads((ROOT / 'suite.json').read_text())
    case = next(c for c in suite['cases'] if c['id'] == 'spell32')
    assert 30 in case['development_seeds']
    assert all(30 not in c['held_out_seeds'] for c in suite['cases'])
    args = SimpleNamespace(model=os.environ['CROC_MODEL'], history=2, memory=False,
        lives=3, crocodiles=0, reach_flag=False, max_calls=1200, call_timeout=30,
        episode_timeout=300, max_cost_usd=total_budget / 2, input_price=float(os.environ['CROC_INPUT_PRICE']),
        output_price=float(os.environ['CROC_OUTPUT_PRICE']), price_date=os.environ['CROC_PRICE_DATE'],
        price_source=os.environ['CROC_PRICE_SOURCE'])
    if min(args.input_price, args.output_price) < 0:
        raise ValueError('Negative prices')
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output = ROOT / 'playtrace' / f'{stamp}-y-alignment-experiment'
    output.mkdir(exist_ok=False)
    original = model.PROMPT
    game_hash = version()
    godot_version = subprocess.check_output([godot_binary(), '--version'], text=True).strip()
    results = []
    try:
        for label, prompt in [('control', original), ('explicit-y', original + '\n' + INSTRUCTION)]:
            if version() != game_hash:
                raise RuntimeError('Game changed during experiment; stopping')
            model.PROMPT = prompt  # In-process override, fully saved; no source mutation.
            folder = output / label
            folder.mkdir()
            configuration = dict(date_utc=stamp, variant=label, provider='vertex',
                location=os.environ.get('GOOGLE_CLOUD_LOCATION') or 'global', case='spell32', seed=30,
                split='development', arguments=vars(args), game_version=game_hash,
                suite_sha256=hashlib.sha256((ROOT/'suite.json').read_bytes()).hexdigest(),
                prompt=prompt, prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),
                max_output_tokens=model.MAX_OUTPUT_TOKENS, godot_version=godot_version,
                player_source_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                      for p in sorted((ROOT/'players').glob('*.py'))})
            (folder/'configuration.json').write_text(json.dumps(configuration, indent=2)+'\n')
            trace_path = folder/'spell32-30.jsonl'
            metadata = archive(trace_path)
            metadata['policy'] = 'model'
            with Engine() as engine, trace_path.open('x') as trace:
                write_trace(trace, metadata)
                summary = episode(engine, 'spell32', 30, 'model', args, suite, trace,
                                  budget={'reserved_usd': 0.0})
            (folder/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
            measured = metrics(trace_path)
            results.append(dict(variant=label, **measured))
            (output/'results.json').write_text(json.dumps(results, indent=2)+'\n')
            print(json.dumps(results[-1]), flush=True)
        assert sum(r['summary']['reserved_cost_usd'] for r in results) <= total_budget
    finally:
        model.PROMPT = original
    print('Results:', output, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--run', action='store_true', help='Two paid episodes, at most $1 reserved total')
    group.add_argument('--analyze', nargs='+', type=Path, help='Analyze existing traces without API calls')
    parser.add_argument('--total-budget', type=float, default=1.0,
                        help='Reservation cap across both episodes, at most the authorized $1')
    args = parser.parse_args()
    if args.run:
        run(args.total_budget)
    else:
        print(json.dumps([metrics(p) for p in args.analyze], indent=2))


if __name__ == '__main__':
    main()
