"""Replay a saved trace in Godot; default to the latest completed agent trace.

Use --latest-human for the newest native recording. No policy makes new decisions.
"""
import argparse
from pathlib import Path
import subprocess
from .engine import ROOT, godot_binary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('trace', nargs='?', type=Path)
    parser.add_argument('--latest-human', action='store_true', help='Use newest playtrace/human-*.jsonl')
    parser.add_argument('--resolution', help='Window size, e.g. 1600x900 for a recording')
    parser.add_argument('--verify', action='store_true', help='Check every result headlessly and exit')
    args = parser.parse_args()
    path = args.trace
    if args.latest_human:
        if path is not None:
            parser.error('Choose a trace path or --latest-human, not both.')
        paths = sorted((ROOT/'playtrace').glob('human-*.jsonl'), key=lambda p: p.stat().st_mtime_ns)
        if not paths:
            parser.error('No recorded human attempt in playtrace yet.')
        path = paths[-1]
    elif path is None:
        finished = sorted((ROOT/'playtrace').glob('*/summary.json'), key=lambda p: p.stat().st_mtime_ns)
        paths = [trace for summary in finished for trace in sorted(summary.parent.glob('*.jsonl'))]
        if not paths:
            parser.error('No completed agent trace found; supply a path or use --latest-human.')
        path = paths[-1]
    if path is None or not path.is_file():
        parser.error('Supply an existing .jsonl action trace or --latest-human.')
    command = [godot_binary()]
    if args.verify:
        command.append('--headless')
    elif args.resolution:
        command.extend(['--resolution', args.resolution])
    command += ['--path', str(ROOT/'godot'), '--script', 'res://scripts/replay.gd',
                '--', f'--replay={path.resolve()}']
    if args.verify:
        command.append('--verify-only')
    print('Replaying recorded actions:', path.resolve(), flush=True)
    raise SystemExit(subprocess.call(command))


if __name__ == '__main__':
    main()
