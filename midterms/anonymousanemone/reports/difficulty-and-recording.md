# Difficulty correction and native session recording — October 26, 2026

## Actual feedback and source comparison

The student reported that spell32 felt too fast, and clarified that movement
starts must be separated by at least half a crocodile body when measuring
absolute distance from the bearer across **both** sides and **all** crocodiles.
This is student feedback in the implementation conversation, not a claimed
classmate or independent playtest.

Comparison with the original Totenbuch working tree found identical e31/e32 wave
numbers, shared combat constants, scale 1.5 and the `speed * unit * dt` movement
formula before these changes. The inspected moving-objects refactor `0b8b463`
and its parent also use the same base spell32 speed and multiplication. No
additional speed multiplier was found in those inspected versions; this does
not identify every older version the student might remember.

The actual spacing flaw was reproducible: `_croc_clear` checked near-height
arrival times and intersecting front-half rectangles. Distant vertical lanes
could pass even at almost identical distances from the bearer, including across
opposite sides. Returning crocodiles could also resume movement without that
clearance check.

## Implemented design changes

- Spell32 base speed: **180 → 120 plate px/s**, or **270 → 180 world px/s** at
  scale 1.5. The 1% per-launch ramp remains: the 14th launch is now 203.4 world
  px/s. This is a deliberate one-third reduction, not a claim to restore an
  unverified earlier speed. Spell31 tuning is unchanged.
- In spell32, a new mover's snout must be farther from the bearer than every
  currently approaching snout by at least half the larger body's width. This
  gate ignores vertical lane and side. An analytical closing-speed check also
  rejects a faster follower that would consume that gap before first arrival.
- After a bite, the crocodile can reappear stationary but waits for the same
  clearance before moving again. Existing health, heka matching and win/loss
  rules remain intact.
- **Record session** is added beside the original Begin button. Normal native
  input semantics, walking, Journal, hints, restarts and subsequent attempts are
  recorded. Stop is in the existing top bar; Escape still leaves combat.
- Native recording uses the actual scene's original frame updates and manually
  advances its paused fight tweens with those same deltas. This lets replay
  reproduce animation callbacks as well as combat. Exact binary frame deltas
  avoid decimal serialization drift. The API/evaluation adapter still uses six
  fixed 1/60-second frames per action and is not replaced by another simulator.

## Verification and limitations

New spacing fixtures were written and run before the fix: **9 failures** exposed
the all-height/all-side gap, faster-following behavior, and old base speed. After
the fix, both left/right direction combinations, different heights, half-body
clearance, closing speed, return-to-movement clearance and single scale
multiplication pass. See `godot/scripts/spacing_checks.gd`.

The native-session fixture presses the intro button, walks, clicks an original
crocodile, holds Space without auto-repeat, opens/closes Journal, requests a hint,
restarts and stops. Replay checks each recorded gameplay state with no numerical
tolerance; an altered frame is rejected. These are automated fixtures, not human
trial evidence. The actual intro was rendered and inspected; preview remains
outside the project.

All **16** tests passed with `python -m unittest discover -s tests -v` after these
changes. The original scene/resource preservation check passes. No held-out seeds
were used. A fresh baseline run is linked below; prior game-version results must
not be presented as results for this revised difficulty.

[Development configuration](../playtrace/20261026T234254422011Z-baseline-h2-development/configuration.json)
and [summary](../playtrace/20261026T234254422011Z-baseline-h2-development/summary.json):
spell31 won (9/9, 249 actions), spell32 lost (8/14, 122 actions), spell32_low lost
(2/14, 43 actions); no invalid actions or API calls. These three development
episodes are not evidence of statistical balance or a live model comparison.

The player observation/action boundary is unchanged. Native audit state and RNG
are offline recording metadata, never model inputs. Actual independent review
and a human check of the revised feel remain pending; this implementation report
does not certify either.
