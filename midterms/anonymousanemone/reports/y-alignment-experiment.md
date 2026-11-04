# Vertical alignment prompt experiment — 2026-11-04

## Plan (recorded before live runs)

Question: does Gemini move to line up vertically with approaching crocodiles,
and does an explicit instruction to match their height help?

The control prompt already says “Align vertically with an approaching crocodile.”
The intervention appends: “Line up with approaching crocodiles by matching the
spear tip's y level to the crocodile's snout y level (dy_from_tip near zero).
Positive dy_from_tip means the crocodile is below your spear: move=1 moves down
toward it. Negative dy_from_tip means it is above: move=-1 moves up toward it.
Use move=0 once lined up; a movement action shifts you about 39 world pixels.”
This gives control/coordinate interpretation, not a target oracle or hidden state.
It does not prescribe a heka rule, target priority, or attack distance.

Hypothesis: the explicit instruction increases the proportion of visible-threat
decisions with vertical movement, increases movement toward a threat, and lowers
vertical error. It is not supported if these measures do not improve. Kills and
outcome are secondary; more movement alone does not establish better alignment.

Two fresh live episodes: control followed by intervention. Both use Vertex
`gemini-3.5-flash-lite`, spell32 development seed 30, history=2, no event memory,
no reach flag, normal speed, 3 lives and 14 crocodiles. Same current engine and
player sources, fixed six-frame actions, 1024 output-token cap. Limits per
episode: 1200 calls, 30 seconds/call, 300 wall seconds, $0.50 conservative
reservation; $1 maximum across this two-episode experiment. No retries or extra
trials to obtain a favorable result. No held-out episodes.

Measures use only saved visible observations and submitted actions. Since the
model does not declare its target, analysis selects the nearest approaching
crocodile by nonnegative `seconds_to_bearer`, falling back to horizontal distance.
This is an analysis proxy, not proof of intent. Record movement frequency on
visible-threat decisions, movement direction toward that proxy when |dy|>20 px,
fraction of decisions within 20 px, median |dy|, and thrust alignment. Also count
movement toward any visible crocodile, to avoid treating every other choice as
aimless. A movement shifts roughly 39 px; count predicted error reduction to
distinguish useful direction from overshooting. Outcomes, failures, fallbacks,
calls, tokens, and costs remain visible.

Existing runs are descriptive context only. The causal comparison uses the two
new episodes with matched settings and hashes except the appended prompt.
One stochastic episode per prompt on one seed cannot establish general benefit
or reveal the model's internal intent. Instruction wording also adds explicit
coordinate/control explanation, so this tests that package, not the bare phrase
“match y levels” alone.

Execution: from the submission folder,
`python -B -m players.alignment_experiment --run`.
Analysis only: `python -B -m players.alignment_experiment --analyze TRACE ...`.
The runner saves prompts, configuration/hashes, raw traces, summaries, and metrics
under a unique `playtrace/...-y-alignment-experiment/` directory. The normal prompt,
engine, suite, and agent configuration are not modified.

## Results

Executed November 4, 2026 (UTC). Skills applied: `make-experiment` for the plan,
controlled variants and report; `crocodile-evaluation` for evaluation boundaries
and deterministic verification. This is actual experiment evidence, not an
independent review or student-authored reflection.

**Answer:** Gemini sometimes moves toward crocodile height already, but the
explicit instruction improved alignment in this pair. It did not produce a kill
or avoid defeat. The improvement was in where it moved, not how often it moved.

### Two fresh live episodes

Both used the same Godot version, game hash, suite hash, player-source hashes,
arguments and output-token cap; only the prompt differed. Configurations below
contain full hashes, exact prompts, dated prices and settings. No normal prompt,
engine, observation schema, suite or maintained agent configuration was changed.

| Measure | Current prompt | Explicit y instruction |
|---|---:|---:|
| Total calls / failed calls | 56 / 1 | 56 / 2 |
| Valid, non-look decisions with visible crocodiles | 42 | 42 |
| Vertical movement on those decisions | 18/42 (43%) | 16/42 (38%) |
| Movement toward any visible crocodile | 12/18 moves | 15/16 moves |
| Movement toward nearest approaching threat when >20 px off | 10/26 opportunities (38%) | 11/11 opportunities (100%) |
| Moves predicted to reduce that threat's vertical error | 10/18 moves | 11/16 moves |
| Within 20 px of that threat's snout height | 16/42 (38%) | 31/42 (74%) |
| Median absolute vertical error | 42.47 px | 8.95 px |
| Thrust decisions aligned within 20 px | 2/4 | 9/9 |
| Crocodiles turned back | 0/14 | 0/14 |
| Outcome | Lost: three bites | Lost: three bites |
| Simulation steps | 65 | 65 |
| Input / output tokens | 95,332 / 2,080 | 102,721 / 1,992 |
| Estimated usage cost | $0.033800 | $0.035796 |
| Reserved cost, including failed calls | $0.225059 | $0.233428 |

Evidence: [combined metrics](../playtrace/20261104T071342178167Z-y-alignment-experiment/results.json),
[control configuration](../playtrace/20261104T071342178167Z-y-alignment-experiment/control/configuration.json),
[control trace](../playtrace/20261104T071342178167Z-y-alignment-experiment/control/spell32-30.jsonl),
[control summary](../playtrace/20261104T071342178167Z-y-alignment-experiment/control/summary.json),
[explicit-y configuration](../playtrace/20261104T071342178167Z-y-alignment-experiment/explicit-y/configuration.json),
[explicit-y trace](../playtrace/20261104T071342178167Z-y-alignment-experiment/explicit-y/spell32-30.jsonl),
[explicit-y summary](../playtrace/20261104T071342178167Z-y-alignment-experiment/explicit-y/summary.json).

### What the traces show

The control did sometimes line up: 10 movement decisions were predicted to reduce
the nearest approaching threat's vertical error. The model's intended target is
not exposed, so this establishes behavior consistent with alignment, not its
internal reasoning. Some other movements could target a different visible foe.

The explicit instruction reduced movement away from all visible foes: 15 of
16 moves pointed toward at least one visible crocodile, compared with 12 of 18
in the control. It brought the nearest threat within 20 px on substantially
more decisions, despite moving slightly less often. The stated hypothesis is
supported on the error and directional measures, but **not** its prediction of
increased movement frequency.

Alignment alone did not solve combat. In the explicit-y run, the first thrust
(step 24) was aligned within 9 px but the snout was still 118 px horizontally
from the tip. A later thrust (step 42) was vertically aligned and about 40 px
from a red crocodile, but used no heka. All nine visible-threat thrust decisions
used plain attacks. At step 61 it faced right while the nearest threat approached
from the left, 241 px from the tip. These are concrete remaining timing, color,
and facing problems; vertical alignment is not sufficient for a hit. Some thrust
requests also occurred during cooldown, so nine decisions do not mean nine
distinct attacks. These examples do not establish a single cause for every miss.

For descriptive context, the earlier [standard-game run without memory](../playtrace/20261104T061923835525Z-model-h2-development/spell32-30.jsonl)
made 22 vertical moves on 43 valid non-look visible-threat decisions. Fourteen
were predicted to reduce the nearest threat's error, but median error was
108.05 px and only 14/43 decisions were within 20 px. Thus the earlier agent did
move in alignment-compatible directions at times. This historical prompt/build
is not the matched control and is not pooled with the new comparison.

### Execution deviations, costs and verification

The first invocation, `python -B -m players.alignment_experiment --run`, was
network-sandboxed. Each variant made 56 failed calls (`URLError`) and advanced
neutral fallbacks; neither contains any valid Gemini-selected action. Their
losses are transport-failure episodes, **not evidence about either prompt**.
They remain preserved in the [failed-attempt results](../playtrace/20261104T071243034359Z-y-alignment-experiment/results.json)
and corresponding configuration/trace/summary subfolders.

After requesting network access, the command was
`python -B -m players.alignment_experiment --run --total-budget 0.54`.
This split the remaining allowance equally ($0.27 per episode), rather than
resetting the initial $1 allowance. Reservations across **all four attempts**
totaled $0.917625, below the approved $1. The two network-enabled episodes had
estimated usage cost $0.069596 combined. Failed requests have no returned token
usage; that absence is not proof that provider billing was zero. Billing is not
verified by this report. No favorable-result retries or held-out runs were made.

The control's one HTTP error at step 25 and the explicit-y run's timeouts at
steps 8 and 21 were retained as invalid neutral fallbacks. Their differing
locations are a confound; neither run was transport-perfect.

Offline analysis checks passed for toward/away/neutral movement and exclusion
of look and invalid actions. The 26 deterministic tests initially had one
sandbox-related failure: Godot could not write its log or access system
certificates. The permitted rerun of
`python -B -m unittest discover -s tests -v` passed all 26 tests in 25.209 seconds.
No game-rule implementation was changed for this experiment.

### Limits and next decision

One episode per prompt on one seed is evidence of a possible benefit, not a
reliable estimate of effect. The model is stochastic, there were provider
failures, and the proxy target may differ from its actual target. Alignment is
measured at decision boundaries, excluding looks, invalid actions and moments
without visible crocodiles; it is not time-weighted across the whole episode.
The 20 px threshold is an analysis convention, not the engine collision rule.
Predicted improvement assumes a 39 px move and does not correct for clamping or
measure the next frame's actual collision geometry.

If the student chooses to adopt the instruction, repeat matched development
trials before final prompt freeze and held-out evaluation. Do not treat improved
alignment as improved survival or learning: both runs still lost with zero kills.
