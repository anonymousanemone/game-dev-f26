"""Part 2 of the recording: the game window, replaying the episode that part 1 just played.

    python -m players.show                 # the trace part 1 finished last
    python -m players.show path/to/trace.jsonl [--resolution 1600x900] [--speed 2]

Nothing here chooses a move. The replayer feeds the recorded actions back through the real
Dangers scene one 0.1 s step at a time and stops with a mismatch message if any observation or
result differs from what was recorded. In the window: Space pauses, Right steps once while
paused, 1/2/3 set speed 0.25x/1x/2x, Esc quits. The title bar shows the step, the time, the
health and the action that was sent.
"""
import argparse
from pathlib import Path
import subprocess
import sys

from .engine import ROOT, godot_binary


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('trace', nargs='?', type=Path)
    parser.add_argument('--resolution', default='1600x900', help='window size, e.g. 1920x1080 for a recording')
    parser.add_argument('--verify', action='store_true', help='check every step headlessly and exit; no window')
    args = parser.parse_args()
    path = args.trace
    if path is None:
        # The newest episode a player (not a human) finished: its folder has a summary.json.
        finished = sorted((ROOT / 'playtrace').glob('*/summary.json'), key=lambda p: p.stat().st_mtime_ns)
        traces = [t for f in finished for t in sorted(f.parent.glob('*.jsonl'))]
        if not traces:
            parser.error('No trace given and none finished yet (run python -m players.watch first).')
        path = traces[-1]
    if not path.is_file():
        parser.error(f'No such trace: {path}')
    command = [godot_binary()]
    command.append('--headless') if args.verify else command.extend(['--resolution', args.resolution])
    command += ['--path', str(ROOT / 'godot'), '--script', 'res://scripts/replay.gd', '--', f'--replay={path.resolve()}']
    if args.verify:
        command.append('--verify-only')
    print('Replaying the recorded episode (no new decisions):', path.resolve(), flush=True)
    raise SystemExit(subprocess.call(command))


if __name__ == '__main__':
    main()
