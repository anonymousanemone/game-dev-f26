"""Run both development spells, carrying unused reservation allowance forward."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

from players.engine import ROOT

TOTAL_BUDGET_USD = 5.0
CASES = ('spell31', 'spell32')


def run_spells(folder, policy, history):
    reserved = 0.0
    episodes = []
    folder.mkdir(parents=True, exist_ok=True)
    for case in CASES:
        remaining = max(0.0, TOTAL_BUDGET_USD - reserved)
        if policy == 'model' and remaining <= 0:
            print(f'{case} skipped: shared ${TOTAL_BUDGET_USD:g} reservation budget exhausted.', flush=True)
            break
        before = set(folder.glob('*/summary.json'))
        command = [sys.executable, '-u', '-m', 'players.run', '--case', case,
                   '--policy', policy, '--history', str(history), '--split', 'development',
                   '--max-cost-usd', str(remaining or TOTAL_BUDGET_USD), '--out', str(folder)]
        print(f'\n{case} · shared reservation ${reserved:.4f}/${TOTAL_BUDGET_USD:g} · remaining ${remaining:.4f}', flush=True)
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode:
            raise RuntimeError(f'{case} runner failed; stopping without resetting the budget.')
        summaries = set(folder.glob('*/summary.json')) - before
        if len(summaries) != 1:
            raise RuntimeError('Cannot identify episode accounting; stopping.')
        rows = json.loads(summaries.pop().read_text())
        reserved += sum(r['reserved_cost_usd'] for r in rows)
        episodes.extend(rows)
        (folder / 'budget.json').write_text(json.dumps(dict(cap_usd=TOTAL_BUDGET_USD,
            reserved_usd=reserved, remaining_usd=max(0.0, TOTAL_BUDGET_USD-reserved),
            episodes=episodes), indent=2))
        if reserved > TOTAL_BUDGET_USD + 1e-9:
            raise RuntimeError('Reservation accounting exceeded the shared cap.')
    print(f'Both-spell attempt finished · reserved ${reserved:.4f}/${TOTAL_BUDGET_USD:g}. No retries.', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--policy', choices=['model', 'baseline'], required=True)
    parser.add_argument('--history', type=int, choices=[0, 2], default=2)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    run_spells(args.out, args.policy, args.history)


if __name__ == '__main__':
    main()
