# Historical difficulty correction and native recording — October 26, 2026

This report describes an **earlier build**, not current tuning. On November 4,
combat was synced with Totenbuch commit `0d5a340`: spell32 base speed is 175 plate
px/s, with arrival-time spacing and a 0.9-second minimum gap. See the
[README rule/source map](../../README.md#rulesource-map) for current rules.

The student reported spell32 felt too fast and requested half-body clearance
across both sides and all heights. This was developer feedback, not a classmate
playtest. Inspection found no extra speed multiplier in the compared source;
the reproducible flaw was that distant vertical lanes could start almost equally
close to the bearer, and returning crocodiles could bypass clearance checks.

The October 26 revision reduced spell32 base speed from 180 to 120 plate px/s
and added all-height/all-side distance clearance, closing-speed checks and
return-to-movement gating. These speed and spacing choices were subsequently
superseded by the November 4 sync. Nine failing spacing checks preceded the
October fix; the historical full suite then passed 16 tests.

Native **Record session** was added beside Begin, with Stop in the top bar.
It records original input semantics and exact frame deltas, including walking,
restarts and encounter changes. Replay compares recorded gameplay states and
rejects altered frames. Automated native-session fixtures exercise these paths;
they are not human playtest evidence. Audit state and RNG remain recording
metadata, outside model inputs. Web exports now disable human recording.

The historical [configuration](../../playtrace/20261026T234254422011Z-baseline-h2-development/configuration.json)
and [summary](../../playtrace/20261026T234254422011Z-baseline-h2-development/summary.json)
record baseline results: spell31 9/9 (win, 249 actions), spell32 8/14 (loss, 122),
spell32_low 2/14 (loss, 43), with no invalid actions or API calls. That run also
predates the later arena-width correction. It is neither current balance evidence
nor a live model comparison. Current results and CI are in
[EVALUATION.md](../../EVALUATION.md); independent findings are in
[review.md](../../review.md).
