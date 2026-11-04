"""Offline report for saved combat/speed trials, including partial runs."""
import argparse
import json
from pathlib import Path
import statistics

from .alignment_experiment import metrics


def analyze(folder):
    results = []
    for config_path in sorted(folder.glob('*/configuration.json')):
        c = json.loads(config_path.read_text())
        path = config_path.parent / f"spell32-{c['seed']}.jsonl"
        if not path.exists():
            continue
        rows = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
        measured = metrics(path)
        if measured['summary'] is None:
            continue
        thrusts = wrong_color = wrong_face = busy = 0
        # Same proxy target as alignment analysis; never a claim about model intent.
        for r in rows:
            if r.get('type') != 'step' or not r['result'].get('valid'):
                continue
            o, a = r['observation'], r['action']
            crocs = o['crocodiles']
            if not crocs or a.get('look') or not a.get('thrust'):
                continue
            incoming = [x for x in crocs if x.get('seconds_to_bearer') is not None
                        and x['seconds_to_bearer'] >= 0]
            target = (min(incoming, key=lambda x: x['seconds_to_bearer']) if incoming else
                      min(crocs, key=lambda x: abs(x['dx_from_tip'])))
            thrusts += 1
            wrong_color += bool(a.get('heka')) != target['red']
            face = a.get('face') or o['facing']
            wrong_face += face != (-1 if target['side'] == 'left' else 1)
            busy += o['thrusting']
        steps = [r for r in rows if r.get('type') == 'step']
        last = steps[-1]['result']['observation'] if steps else rows[1]['observation']
        results.append(dict(variant=c['variant'], speed=c['speed_scale'], seed=c['seed'],
            **measured, proxy_thrusts=thrusts, proxy_wrong_color_thrusts=wrong_color,
            proxy_wrong_face_thrusts=wrong_face, thrust_requests_while_busy=busy,
            final_health=last['health'], provider_errors=sum(bool(r.get('error')) for r in steps),
            neutral_fallbacks=sum(bool(r.get('fallback')) for r in steps)))
    # Post-hoc descriptive comparison at the latest step boundary shared by all.
    if results:
        boundaries = []
        for r in results:
            rows = [json.loads(l) for l in Path(r['trace']).read_text().splitlines() if l.strip()]
            boundaries.append({x['step'] for x in rows if x.get('type') == 'step'})
        horizon = max(set.intersection(*boundaries))
        for r in results:
            rows = [json.loads(l) for l in Path(r['trace']).read_text().splitlines() if l.strip()]
            prefix = [x for x in rows if x.get('type') == 'step' and x['step'] <= horizon]
            if prefix:
                boundary = prefix[-1]
                r['common_horizon'] = dict(requested_step=horizon, actual_step=boundary['step'],
                    score=boundary['result']['outcome']['score'],
                    health=boundary['result']['observation']['health'])
    return results


def table(results, root):
    lines = ['| Prompt | Speed | Seed | Outcome / reason | Turn-backs | Health | Steps | Calls / failed | Usage USD | Reserved USD | Evidence |',
             '|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---|']
    for r in sorted(results, key=lambda x: (x['seed'], -x['speed'], x['variant'])):
        s = r['summary']; o = s['outcome']
        path = Path(r['trace']).relative_to(root)
        base = path.parent
        lines.append(f"| {r['variant']} | {r['speed']} | {r['seed']} | {o['status']} / {o['reason']} | {o['score']}/14 | {r['final_health']} | {o['steps']} | {s['calls']}/{s['failed_calls']} | {s['estimated_cost_usd']:.6f} | {s['reserved_cost_usd']:.6f} | [trace](../{path}), [config](../{base}/configuration.json), [summary](../{base}/summary.json) |")
    return '\n'.join(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    options = parser.parse_args()
    results = analyze(options.folder.resolve())
    (options.folder/'analysis.json').write_text(json.dumps(results, indent=2)+'\n')
    print(table(results, options.folder.resolve().parents[1]))
    for variant in ['current', 'combined']:
        for speed in [1., .75]:
            group = [r for r in results if r['variant'] == variant and r['speed'] == speed]
            if group:
                print(variant, speed, 'scores', [r['summary']['outcome']['score'] for r in group],
                      'median dy', statistics.median(r['median_abs_dy'] for r in group if r['median_abs_dy'] is not None))
