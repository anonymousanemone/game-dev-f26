"""Observation-only heuristic. No engine imports or hidden-state access."""
import math

# Human reaction time: in the student's recordings a new crocodile is first acted on
# 0.40-1.17 s after it appears (middle half of 44 cases, median 0.59 s). The student set
# the faster end, 0.4 s. The baseline ignores a crocodile until it has been visible this long.
REACTION_SECONDS = 0.4


def _same(a, b):
    """The same crocodile seen at two times: same side, color and lane, and no further along."""
    return (a['direction'] == b['direction'] and a['red'] == b['red']
            and abs(a['snout'][1] - b['snout'][1]) < 1
            and (b['snout'][0] - a['snout'][0]) * b['direction'] >= 0)


def noticed(observation, history):
    """Crocodiles already visible REACTION_SECONDS ago (history: earlier observations, newest last)."""
    then = [h for h in history if h['time'] <= observation['time'] - REACTION_SECONDS + 1e-9]
    if not then:
        return []
    return [c for c in observation['crocodiles'] if any(_same(p, c) for p in then[-1]['crocodiles'])]


def choose(observation, history=()):
    o = observation
    previous = history[-1] if history else None
    a = dict(move=0, face=0, thrust=False, heka=False)
    if o['tutorial'] == 'thrust':
        a['thrust'] = True
        return a
    crocodiles = noticed(o, history)
    if not crocodiles:
        return a
    # Estimated velocity comes from successive visible positions, never spawn state.
    def velocity(c):
        if previous:
            elapsed = o['time'] - previous['time']
            matches = [p for p in previous['crocodiles']
                       if p['direction'] == c['direction'] and p['red'] == c['red']
                       and abs(p['snout'][1] - c['snout'][1]) < 1]
            if matches and elapsed > 0:
                p = min(matches, key=lambda p: abs(p['snout'][0] - c['snout'][0]))
                return min(650, max(100, abs(c['snout'][0] - p['snout'][0]) / elapsed))
        return 300
    target = min(crocodiles, key=lambda c: abs(o['player_x'] - c['snout'][0]) / velocity(c))
    desired_face = -target['direction']
    if o['both_sides']:
        a['face'] = desired_face
    dy = target['snout'][1] - o['tip'][1]
    a['move'] = (1 if dy > 0 else -1) if abs(dy) > 12 else 0
    # Predict the snout at the strike frame (5 fixed ticks after a thrust).
    speed = velocity(target)
    snout_x = target['snout'][0] + target['direction'] * speed * (5 / 60)
    tip_x = o['tip'][0]
    if desired_face != o['facing']:
        tip_x = 2 * o['player_x'] - tip_x
    distance = (tip_x - snout_x) * target['direction']
    # The inherited strike accepts the silhouette behind the snout as well as its tip.
    if not o['thrusting'] and abs(dy) < 32 and -target['width'] * .70 < distance < 32:
        a.update(thrust=True, heka=target['red'], move=0)
    return a
