"""Run a matched development comparison after a funded key is configured."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

from .config import load_env
from .engine import ROOT


def run_policy(policy, case):
    command = [sys.executable, '-m', 'players.run', '--policy', policy,
               '--split', 'development', '--case', case]
    result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE)
    print(result.stdout, end='', flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
    paths = [line.removeprefix('Results: ') for line in result.stdout.splitlines()
             if line.startswith('Results: ')]
    if not paths:
        raise RuntimeError('Runner did not report a results directory.')
    return Path(paths[-1])


def compare(baseline, live):
    directories = [baseline, live]
    configs = [json.loads((path/'configuration.json').read_text()) for path in directories]
    for key in ['game_version', 'suite_sha256']:
        if configs[0][key] != configs[1][key]:
            raise RuntimeError('Comparison requires the same game and suite: ' + key)
    summaries = [json.loads((path/'summary.json').read_text()) for path in directories]
    if {(r['case'], r['seed']) for r in summaries[0]} != {(r['case'], r['seed']) for r in summaries[1]}:
        raise RuntimeError('Comparison requires matching case/seed pairs.')
    lines = ['# Session 7 development comparison', '',
             'Automatically assembled from actual run summaries; this is not held-out evaluation.', '',
             '| Player/model | Case/seed | Outcome/reason | Score | Steps | Illegal | Calls/failed | Mean decision seconds | Input/output tokens | Estimated USD |',
             '|---|---|---|---:|---:|---:|---|---:|---|---:|']
    ready = True
    evidence = []
    for path, rows in zip(directories, summaries):
        for row in rows:
            outcome = row['outcome']
            cost = row['estimated_cost_usd']
            cost_text = f'{cost:.6f}' if cost is not None else 'unknown'
            lines.append(f"| {row['policy']} / {row['model'] or 'heuristic'} | {row['case']}/{row['seed']} | "
                         f"{outcome['status']}: {outcome['reason']} | {outcome['score']} | {outcome['steps']} | "
                         f"{outcome['invalid_actions']} | {row['calls']}/{row['failed_calls']} | "
                         f"{row['mean_latency_seconds']:.6f} | {row['input_tokens']}/{row['output_tokens']} | "
                         f"{cost_text} |")
            trace = path/f"{row['case']}-{row['seed']}.jsonl"
            if row['policy'] == 'model':
                steps = [json.loads(line) for line in trace.read_text().splitlines()]
                model_moves = sum(r.get('type') == 'step' and r.get('source') == 'model'
                                  and not r.get('fallback') and r['result']['valid'] for r in steps)
                ready &= model_moves > 0 and outcome['status'] in {'won', 'lost'}
            evidence += ['', f"[Trace](../{trace.relative_to(ROOT).as_posix()}) · "
                      f"[Configuration](../{(path/'configuration.json').relative_to(ROOT).as_posix()}) · "
                      f"[Summary](../{(path/'summary.json').relative_to(ROOT).as_posix()})", '']
    lines += evidence
    lines += [f"Game SHA-256: `{configs[0]['game_version']}`.", '',
              f"Dated prices: {summaries[1][0]['price_date']}; "
              f"[provider price source]({summaries[1][0]['price_source']}). "
              'Uncached input prices are used for the estimate; reconcile failed-call billing with the provider.', '',
              'Live checkpoint episode: ' + ('a model submitted valid actions and reached a game win/loss.' if ready
                  else 'not yet established: inspect failures, limits and trace; do not claim completion.'), '',
              'Limitations: one development seed, one trial per player, no statistical inference. '
              'CI evidence is tracked separately in EVALUATION.md. Peer observations and student interpretation remain separate evidence.', '']
    report = ROOT/'reports/session7-comparison.md'
    report.write_text('\n'.join(lines))
    return ready, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', choices=['spell31', 'spell32', 'spell32_low'], default='spell32')
    args = parser.parse_args()
    load_env(ROOT/'.env')
    if not os.environ.get('OPENAI_API_KEY'):
        parser.error('Paste your funded API key into the private .env first; no live run was attempted.')
    baseline = run_policy('baseline', args.case)
    live = run_policy('model', args.case)
    ready, report = compare(baseline, live)
    print('Comparison:', report)
    if not ready:
        raise SystemExit('Live episode did not establish a valid model-controlled game ending; see report.')


if __name__ == '__main__':
    main()
