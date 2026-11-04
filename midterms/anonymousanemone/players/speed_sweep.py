"""Baseline difficulty sweep: raise crocodile speed until the baseline starts to lose.

Uses only the deterministic baseline (no model calls) and never the held-out seeds.
"""
import argparse
import json
from pathlib import Path
from . import baseline
from .engine import Engine, ROOT

SEEDS = [30, 31, 32, 33, 34]   # development seed 30 plus unreserved seeds; held-out seeds stay unused
CASES = ['spell31', 'spell32', 'spell32_low']


def play(engine, case, seed, scale):
    observation = engine.call('reset', seed=seed, case=case, speed_scale=scale)
    history = []
    while True:
        result = engine.call('step', action=baseline.choose(observation, history))
        history, observation = (history + [observation])[-10:], result['observation']
        if result['outcome']['terminal']:
            return result['outcome'], observation


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scales', default='1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0')
    parser.add_argument('--reactions', default='0.4,0.0', help='baseline reaction delays in seconds')
    parser.add_argument('--out', type=Path, default=ROOT/'reports'/'speed-sweep.json')
    args = parser.parse_args()
    engine = Engine()
    rows = []
    try:
        for reaction in [float(r) for r in args.reactions.split(',')]:
            baseline.REACTION_SECONDS = reaction
            for case in CASES:
                for scale in [float(s) for s in args.scales.split(',')]:
                    for seed in SEEDS:
                        outcome, last = play(engine, case, seed, scale)
                        rows.append(dict(reaction=reaction, case=case, scale=scale, seed=seed,
                                         status=outcome['status'], reason=outcome['reason'],
                                         steps=outcome['steps'], score=outcome['score'],
                                         bites=3 - last['health']))
                    won = sum(r['status'] == 'won' for r in rows[-len(SEEDS):])
                    print(f'reaction {reaction:.1f}s  {case:11}  speed x{scale:.1f}: won {won}/{len(SEEDS)}', flush=True)
    finally:
        engine.close()
    args.out.write_text(json.dumps({'seeds': SEEDS, 'rows': rows}, indent=1) + '\n')
    print('Results:', args.out)


if __name__ == '__main__':
    main()
