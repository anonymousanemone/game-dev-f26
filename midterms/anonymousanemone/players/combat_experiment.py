"""Bounded 2x2 prompt/speed experiment; normal player and engine stay unchanged."""
import argparse
import datetime
import hashlib
import json
import os
import subprocess
from types import SimpleNamespace

from . import model
from .alignment_experiment import metrics
from .config import load_env
from .engine import Engine, ROOT, godot_binary
from .run import episode, version, write_trace
from .traces import archive

COMBAT = model.COMBAT_INSTRUCTION


class SpeedEngine:
    """Trusted reset override only; observations/actions pass through unmodified."""
    def __init__(self, engine, speed):
        self.engine, self.speed = engine, speed

    def call(self, op, **kwargs):
        if op == 'reset':
            kwargs['speed_scale'] = self.speed
        return self.engine.call(op, **kwargs)


def run(total_budget, resume=None, full=False):
    ceiling = 10 if full else 3
    if not 0 < total_budget <= ceiling:
        raise ValueError(f'Authorized total is at most ${ceiling}')
    load_env(ROOT / '.env')
    required = ['GOOGLE_CLOUD_PROJECT', 'CROC_INPUT_PRICE', 'CROC_OUTPUT_PRICE',
                'CROC_PRICE_DATE', 'CROC_PRICE_SOURCE']
    if any(not os.environ.get(k) for k in required):
        raise ValueError('Missing provider configuration or dated prices')
    suite = json.loads((ROOT / 'suite.json').read_text())
    seeds = [30] if full else [30, 31, 32]
    assert not set(seeds).intersection(s for c in suite['cases'] for s in c['held_out_seeds'])
    args = SimpleNamespace(model='gemini-3.5-flash-lite', history=2, memory=False,
        lives=3, crocodiles=0, reach_flag=False, max_calls=1200, call_timeout=30,
        episode_timeout=1800 if full else 300, max_cost_usd=total_budget/(4*len(seeds)),
        input_price=float(os.environ['CROC_INPUT_PRICE']),
        output_price=float(os.environ['CROC_OUTPUT_PRICE']),
        price_date=os.environ['CROC_PRICE_DATE'], price_source=os.environ['CROC_PRICE_SOURCE'])
    if min(args.input_price, args.output_price) < 0:
        raise ValueError('Negative price')
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    suffix = 'full' if full else 'experiment'
    output = ROOT / 'playtrace' / f'{stamp}-combat-speed-{suffix}'
    if resume:
        output = ROOT / 'playtrace' / resume
    else:
        output.mkdir(exist_ok=False)
    original = model.PROMPT
    control = model.BASE_PROMPT
    game_hash = version()
    common = dict(date_utc=stamp, provider='vertex', case='spell32', split='exploratory-development',
        declared_seeds=seeds, total_budget_usd=total_budget, arguments=vars(args),
        game_version=game_hash, suite_sha256=hashlib.sha256((ROOT/'suite.json').read_bytes()).hexdigest(),
        godot_version=subprocess.check_output([godot_binary(), '--version'], text=True).strip(),
        max_output_tokens=model.MAX_OUTPUT_TOKENS,
        player_source_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in sorted((ROOT/'players').glob('*.py'))})
    conditions = [('current', 1.0), ('combined', 1.0), ('current', .75), ('combined', .75)]
    results = json.loads((output/'results.json').read_text()) if resume else []
    if sum(r['summary']['reserved_cost_usd'] for r in results) > total_budget:
        raise ValueError('Prior reservations exceed budget')
    try:
        for index, seed in enumerate(seeds):
            # Rotate condition order to reduce a fixed provider/time ordering confound.
            for label, speed in conditions[index:] + conditions[:index]:
                if any(r['seed'] == seed and r['variant'] == label and r['speed_scale'] == speed for r in results):
                    continue
                if version() != game_hash:
                    raise RuntimeError('Game changed; stopping')
                model.PROMPT = control if label == 'current' else control + '\n' + COMBAT
                folder = output / f'{label}-speed{speed}-seed{seed}'
                folder.mkdir()
                config = dict(common, variant=label, speed_scale=speed, seed=seed,
                    prompt=model.PROMPT, prompt_sha256=hashlib.sha256(model.PROMPT.encode()).hexdigest())
                (folder/'configuration.json').write_text(json.dumps(config, indent=2)+'\n')
                path = folder / f'spell32-{seed}.jsonl'
                metadata = archive(path)
                metadata.update(policy='model', speed_scale=speed)
                with Engine() as engine, path.open('x') as trace:
                    write_trace(trace, metadata)
                    summary = episode(SpeedEngine(engine, speed), 'spell32', seed, 'model', args,
                                      suite, trace, budget={'reserved_usd': 0.0})
                (folder/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
                results.append(dict(variant=label, speed_scale=speed, seed=seed, **metrics(path)))
                (output/'results.json').write_text(json.dumps(results, indent=2)+'\n')
                print(json.dumps(dict(variant=label, speed=speed, **summary)), flush=True)
        assert sum(r['summary']['reserved_cost_usd'] for r in results) <= total_budget
    finally:
        model.PROMPT = original
    print('Results:', output, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true', required=True)
    parser.add_argument('--total-budget', type=float, required=True)
    parser.add_argument('--resume', help='Existing experiment directory name; completed trials are skipped')
    parser.add_argument('--full', action='store_true', help='Four fresh seed-30 episodes, up to $10 total')
    options = parser.parse_args()
    run(options.total_budget, options.resume, options.full)
