"""Part 1 of the recording: watch the model play, as text, live.

    python -m players.watch --case spell32

Starts `players.run --policy model` (the same evaluator, the same live provider call, the same
budget checks) and follows the trace file it writes, printing every model reply as it arrives.
When the episode ends it prints the result and the command for part 2 (`players.show`), which
opens the game window and replays this exact trace.

`--policy baseline` runs the scripted baseline instead (no model call, no cost) to rehearse the
layout. Anything after `--` goes to players.run unchanged.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from .engine import ROOT

BOLD, DIM, RED, GREEN, YELLOW, RESET = '\033[1m', '\033[2m', '\033[31m', '\033[32m', '\033[33m', '\033[0m'
if not sys.stdout.isatty() or os.environ.get('NO_COLOR'):
    BOLD = DIM = RED = GREEN = YELLOW = RESET = ''


def describe(action):
    """The action in words: what the agent chose to do for the next 0.1 s."""
    if action is None:
        return 'no valid action (nothing is pressed)'
    if action.get('look'):
        return 'LOOK at the word of power (hands off the keys for 1.0 s)'
    parts = []
    parts.append({-1: 'move up', 1: 'move down'}.get(action.get('move'), 'stay put'))
    if action.get('face'):
        parts.append('face ' + ('left' if action['face'] < 0 else 'right'))
    if action.get('thrust'):
        parts.append('THRUST')
    if action.get('heka'):
        parts.append('hold heka key')
    return ', '.join(parts)


def nearest(observation):
    crocs = observation.get('crocodiles') or []
    if not crocs:
        return 'no crocodile in view'
    c = min(crocs, key=lambda c: abs(c['dx_from_tip']))
    seconds = c.get('seconds_to_bearer')
    arrive = f", reaches you in {seconds:.1f}s" if seconds is not None and seconds > 0 else ''
    return (f"{len(crocs)} in view; nearest is {'RED ' if c['red'] else ''}{c['side']}, "
            f"{c['dx_from_tip']:+.0f} px across, {c['dy_from_tip']:+.0f} px up/down from the spear tip{arrive}")


def show_step(row):
    seen, after = row['observation'], row['result'].get('observation', row['observation'])
    action, outcome = row['action'], row['result'].get('outcome', {})
    print(f"{BOLD}step {row['step']:>3}{RESET}  t={seen['time']:5.1f}s  health {seen['health']}  "
          f"turned back {seen['killed']}/{seen['total']}   {DIM}{nearest(seen)}{RESET}")
    reply = row.get('raw')
    source = row.get('source')
    label = 'model said' if source == 'model' else 'baseline chose'
    shown = ' '.join(str(reply).split()) if reply else json.dumps(action)
    print(f"        {label}: {shown}")
    if row.get('error'):
        print(f"        {RED}provider error: {row['error']} (no action sent){RESET}")
    elif row.get('fallback'):
        print(f"        {RED}reply was not valid JSON; sent nothing{RESET}")
    print(f"        => {describe(action)}   {DIM}({row.get('latency_seconds', 0):.2f}s, "
          f"{row.get('usage', {}).get('output_tokens', 0)} output tokens){RESET}")
    if not row['result'].get('valid', True):
        print(f"        {RED}the game rejected that action as invalid{RESET}")
    if after['killed'] > seen['killed']:
        print(f"        {GREEN}a crocodile was turned back ({after['killed']}/{after['total']}){RESET}")
    if after['health'] < seen['health']:
        print(f"        {RED}BITTEN: health {after['health']}{RESET}")
    if after['message'] and after['message'] != seen['message']:
        print(f"        {YELLOW}game says: {after['message']}{RESET}")
    if outcome.get('terminal'):
        print(f"        {BOLD}episode over: {outcome['status']} ({outcome['reason']}){RESET}")
    sys.stdout.flush()


def new_output_dir(out, before, process, patience=60):
    deadline = time.time() + patience
    while time.time() < deadline:
        fresh = sorted(set(out.glob('*-*')) - before)
        if fresh:
            return fresh[-1]
        if process.poll() is not None:
            return None
        time.sleep(0.2)
    return None


def follow(path, process):
    """Yield each complete JSON row of a growing .jsonl file until the run exits."""
    while not path.exists():
        if process.poll() is not None:
            return
        time.sleep(0.2)
    with path.open() as handle:
        buffer = ''
        while True:
            chunk = handle.readline()
            if chunk:
                buffer += chunk
                if buffer.endswith('\n'):
                    line, buffer = buffer, ''
                    if line.strip():
                        yield json.loads(line)
                continue
            if process.poll() is not None:
                return
            time.sleep(0.05)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--case', choices=['spell31', 'spell32', 'spell32_low'], default='spell32')
    parser.add_argument('--policy', choices=['model', 'baseline'], default='model')
    parser.add_argument('--split', choices=['development', 'held_out'], default='development')
    parser.add_argument('--no-prompt', action='store_true', help='Do not wait for Enter before opening part 2')
    parser.add_argument('--open-replay', action='store_true', help='Open part 2 automatically when the run ends')
    parser.add_argument('extra', nargs=argparse.REMAINDER, help='after --: extra arguments for players.run')
    args = parser.parse_args()
    extra = [a for a in args.extra if a != '--']

    out = ROOT / 'playtrace'
    out.mkdir(exist_ok=True)
    before = set(out.glob('*-*'))
    command = [sys.executable, '-u', '-m', 'players.run', '--policy', args.policy, '--split', args.split,
               '--case', args.case, *extra]
    print(f"{BOLD}Crocodiles: {args.policy} playing {args.case} ({args.split}){RESET}")
    if args.policy == 'model':
        print(f"{DIM}Live provider call each step; the game freezes while the model decides.{RESET}")
    process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    folder = new_output_dir(out, before, process)
    if folder is None:
        print(process.stdout.read())
        sys.exit(f'players.run stopped before it started an episode (exit code {process.wait()}).')
    trace = None
    summary = None
    try:
        while trace is None:
            traces = sorted(folder.glob('*.jsonl'))
            if traces:
                trace = traces[0]
            elif process.poll() is not None:
                break
            else:
                time.sleep(0.2)
        if trace is not None:
            print(f"{DIM}Trace: {trace}{RESET}\n")
            for row in follow(trace, process):
                if row.get('type') == 'reset':
                    first = row['observation']
                    print(f"{DIM}seed {row['seed']}: {first['total']} crocodiles to turn back, "
                          f"health {first['health']}{RESET}\n")
                elif row.get('type') == 'step':
                    show_step(row)
                elif row.get('type') == 'summary':
                    summary = row
    except KeyboardInterrupt:
        process.terminate()
        print('\nStopped. The partial trace is kept; nothing was replayed.')
        sys.exit(130)
    output = process.stdout.read()
    code = process.wait()
    if summary is None:
        print(f"{RED}The run ended without a summary (exit code {code}).{RESET}")
        print(output[-2000:])
        sys.exit(code or 1)

    outcome = summary['outcome']
    print('\n' + '=' * 72)
    print(f"{BOLD}Result: {outcome['status'].upper()} ({outcome['reason']}){RESET}  "
          f"{outcome['score']} turned back, {outcome['steps']} steps, {outcome['invalid_actions']} invalid")
    if summary['policy'] == 'model':
        cost = summary['estimated_cost_usd']
        print(f"model {summary['model']}: {summary['calls']} calls ({summary['failed_calls']} failed), "
              f"{summary['input_tokens']} in / {summary['output_tokens']} out tokens"
              + (f", about ${cost:.4f}" if cost is not None else '')
              + f", mean latency {summary['mean_latency_seconds']:.2f}s")
    print('=' * 72)
    shown = f"python -m players.show {trace.relative_to(ROOT)}"
    print(f"\n{BOLD}Part 2 - open the game window and replay this episode:{RESET}\n\n    {shown}\n")
    if args.open_replay or (not args.no_prompt and sys.stdin.isatty()):
        if not args.open_replay:
            try:
                input('Press Enter to open it now (Ctrl-C to skip) ')
            except (KeyboardInterrupt, EOFError):
                print()
                return
        subprocess.call([sys.executable, '-m', 'players.show', str(trace)], cwd=ROOT)


if __name__ == '__main__':
    main()
