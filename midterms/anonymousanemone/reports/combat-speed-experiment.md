# Combined combat prompt × speed — 2026-11-04

## Plan recorded before live execution

Question: does combined combat guidance improve performance, and does slowing
crocodiles help independently or in combination? Prediction: the combined prompt
increases turn-backs at each speed, and 0.75× increases turn-backs within each
prompt. Equal or lower scores contradict each directional prediction. Primary
measure: turn-backs, paired by seed. Wins, health, alignment, thrust alignment,
invalid actions and failures are secondary. This is not a learning experiment.

Four conditions: exact current players.model.PROMPT versus that prompt plus
players.combat_experiment.COMBAT, each at speed_scale 1.0 and 0.75. The combined
package gives target priority, consistent facing, explicit y alignment,
color-dependent heka, predictive timing at five frames, and attack availability.
This tests the whole instruction/knowledge package, not individual components.
Only current observations and bounded history inform actions; no hidden state,
collision queries, future schedules, or controller aid. A trusted wrapper forwards
the existing speed_scale reset setting; authoritative Godot rules, observation
schema and six-frame action cadence stay unchanged.

Spell32, seeds 30, 31, 32, one episode per condition per seed: 12 episodes.
30 is the suite development seed; 31 and 32 are separately declared exploratory
development seeds, excluded from every held-out set. Suite unchanged. Rotate
condition order by seed. Provider sampling is stochastic, without paired RNG.
Vertex / gemini-3.5-flash-lite, history=2, memory off, reach flag off, 3 lives,
14 crocodiles, output cap 1024. All conditions are exploratory, not final evaluation.

User explicitly approved Vertex Gemini Flash-Lite and $3 total reservation.
Fixed $0.25 reservation per episode, 1200 calls, 30 seconds/call, 300 wall seconds.
No paid retries or redistribution of unused budget. Conservative reservations
can truncate slower or successful episodes; report limits as incomplete rather
than losses. Failed calls reserve cost and retain neutral fallbacks. Dated prices
and their configured source are saved; estimates are not verified billing.

Command from midterm: python -B -m players.combat_experiment --run --total-budget 3

Apply make-experiment and crocodile-evaluation skills. Save exact prompts,
configuration, game/suite/player/prompt hashes, Godot version, per-action traces
and summaries under a unique playtrace/*-combat-speed-experiment directory.
Use existing alignment analysis: nearest nonnegative arrival-time proxy,
otherwise nearest horizontal tip distance. Proxy measures do not prove intent.
Turn-back totals with different survival/exposure and budget truncation are
limited evidence. Three development seeds cannot establish a general ranking.

## Results

Executed November 4, 2026 UTC with the make-experiment and crocodile-evaluation
skills. All 12 planned paid trials were run exactly once; every one stopped at
its conservative cost reservation cap. None reached a game win or loss.

| Prompt | Speed | Seed | Outcome / reason | Turn-backs | Health | Steps | Calls / failed | Usage USD | Reserved USD | Evidence |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| combined | 1.0 | 30 | limit / cost_limit | 1/14 | 2 | 55 | 55/0 | 0.040232 | 0.248436 | [trace](../playtrace/20261104T072415073512Z-combat-speed-experiment/combined-speed1.0-seed30/spell32-30.jsonl), [config](../playtrace/20261104T072415073512Z-combat-speed-experiment/combined-speed1.0-seed30/configuration.json), [summary](../playtrace/20261104T072415073512Z-combat-speed-experiment/combined-speed1.0-seed30/summary.json) |
| current | 1.0 | 30 | limit / cost_limit | 1/14 | 1 | 70 | 61/0 | 0.038081 | 0.247441 | [trace](../playtrace/20261104T072415073512Z-combat-speed-experiment/current-speed1.0-seed30/spell32-30.jsonl), [config](../playtrace/20261104T072415073512Z-combat-speed-experiment/current-speed1.0-seed30/configuration.json), [summary](../playtrace/20261104T072415073512Z-combat-speed-experiment/current-speed1.0-seed30/summary.json) |
| combined | 0.75 | 30 | limit / cost_limit | 1/14 | 2 | 55 | 55/0 | 0.040468 | 0.248771 | [trace](../playtrace/20261104T072415073512Z-combat-speed-experiment/combined-speed0.75-seed30/spell32-30.jsonl), [config](../playtrace/20261104T072415073512Z-combat-speed-experiment/combined-speed0.75-seed30/configuration.json), [summary](../playtrace/20261104T072415073512Z-combat-speed-experiment/combined-speed0.75-seed30/summary.json) |
| current | 0.75 | 30 | limit / cost_limit | 2/14 | 3 | 61 | 61/0 | 0.039581 | 0.247751 | [trace](../playtrace/20261104T072415073512Z-combat-speed-experiment/current-speed0.75-seed30/spell32-30.jsonl), [config](../playtrace/20261104T072415073512Z-combat-speed-experiment/current-speed0.75-seed30/configuration.json), [summary](../playtrace/20261104T072415073512Z-combat-speed-experiment/current-speed0.75-seed30/summary.json) |
| combined | 1.0 | 31 | limit / cost_limit | 2/14 | 3 | 55 | 55/0 | 0.039325 | 0.247427 | [trace](../playtrace/20261104T072415073512Z-combat-speed-experiment/combined-speed1.0-seed31/spell32-31.jsonl), [config](../playtrace/20261104T072415073512Z-combat-speed-experiment/combined-speed1.0-seed31/configuration.json), [summary](../playtrace/20261104T072415073512Z-combat-speed-experiment/combined-speed1.0-seed31/summary.json) |
| current | 1.0 | 31 | limit / cost_limit | 1/14 | 1 | 71 | 62/0 | 0.037707 | 0.249863 | [trace](../playtrace/20261104T072415073512Z-combat-speed-experiment/current-speed1.0-seed31/spell32-31.jsonl), [config](../playtrace/20261104T072415073512Z-combat-speed-experiment/current-speed1.0-seed31/configuration.json), [summary](../playtrace/20261104T072415073512Z-combat-speed-experiment/current-speed1.0-seed31/summary.json) |
| combined | 0.75 | 31 | limit / cost_limit | 1/14 | 3 | 55 | 55/1 | 0.039053 | 0.248384 | [trace](../playtrace/20261104T072415073512Z-combat-speed-experiment/combined-speed0.75-seed31/spell32-31.jsonl), [config](../playtrace/20261104T072415073512Z-combat-speed-experiment/combined-speed0.75-seed31/configuration.json), [summary](../playtrace/20261104T072415073512Z-combat-speed-experiment/combined-speed0.75-seed31/summary.json) |
| current | 0.75 | 31 | limit / cost_limit | 0/14 | 1 | 70 | 61/0 | 0.037613 | 0.246284 | [trace](../playtrace/20261104T072415073512Z-combat-speed-experiment/current-speed0.75-seed31/spell32-31.jsonl), [config](../playtrace/20261104T072415073512Z-combat-speed-experiment/current-speed0.75-seed31/configuration.json), [summary](../playtrace/20261104T072415073512Z-combat-speed-experiment/current-speed0.75-seed31/summary.json) |
| combined | 1.0 | 32 | limit / cost_limit | 0/14 | 1 | 55 | 55/0 | 0.040433 | 0.248918 | [trace](../playtrace/20261104T072415073512Z-combat-speed-experiment/combined-speed1.0-seed32/spell32-32.jsonl), [config](../playtrace/20261104T072415073512Z-combat-speed-experiment/combined-speed1.0-seed32/configuration.json), [summary](../playtrace/20261104T072415073512Z-combat-speed-experiment/combined-speed1.0-seed32/summary.json) |
| current | 1.0 | 32 | limit / cost_limit | 2/14 | 3 | 62 | 62/2 | 0.037325 | 0.249625 | [trace](../playtrace/20261104T072415073512Z-combat-speed-experiment/current-speed1.0-seed32/spell32-32.jsonl), [config](../playtrace/20261104T072415073512Z-combat-speed-experiment/current-speed1.0-seed32/configuration.json), [summary](../playtrace/20261104T072415073512Z-combat-speed-experiment/current-speed1.0-seed32/summary.json) |
| combined | 0.75 | 32 | limit / cost_limit | 0/14 | 2 | 55 | 55/0 | 0.040760 | 0.249568 | [trace](../playtrace/20261104T072415073512Z-combat-speed-experiment/combined-speed0.75-seed32/spell32-32.jsonl), [config](../playtrace/20261104T072415073512Z-combat-speed-experiment/combined-speed0.75-seed32/configuration.json), [summary](../playtrace/20261104T072415073512Z-combat-speed-experiment/combined-speed0.75-seed32/summary.json) |
| current | 0.75 | 32 | limit / cost_limit | 1/14 | 3 | 61 | 61/0 | 0.039157 | 0.247549 | [trace](../playtrace/20261104T072415073512Z-combat-speed-experiment/current-speed0.75-seed32/spell32-32.jsonl), [config](../playtrace/20261104T072415073512Z-combat-speed-experiment/current-speed0.75-seed32/configuration.json), [summary](../playtrace/20261104T072415073512Z-combat-speed-experiment/current-speed0.75-seed32/summary.json) |

### Aggregate observations

Scores below are turn-backs at each episode's budget cutoff, in seed order
30, 31, 32. They are not completed-episode scores or comparable win rates.

| Prompt | Speed | Turn-backs by seed | Mean turn-backs | Health by seed | Within 20 px / visible decisions | Thrust requests with visible threats |
|---|---:|---|---:|---|---:|---:|
| Current | 1.0 | 1, 1, 2 | 1.33 | 1, 1, 3 | 60/145 (41%) | 14 |
| Current | 0.75 | 2, 0, 1 | 1.00 | 3, 1, 3 | 51/145 (35%) | 15 |
| Combined | 1.0 | 1, 2, 0 | 1.00 | 2, 3, 1 | 72/128 (56%) | 3 |
| Combined | 0.75 | 1, 1, 0 | 0.67 | 2, 3, 2 | 69/127 (54%) | 2 |

Combined-minus-current score differences: [0, +1, -2] at 1.0×, and
[-1, +1, -1] at 0.75×. Slow-minus-normal differences: [+1, -1, -1]
for current, and [0, -1, 0] for combined. The predicted score advantages were
not observed consistently. These small partial samples do not establish harm.

Against the analysis target proxy, current had 3/14 color-mismatched thrust
requests at normal speed and 3/15 at slower speed; combined had 0/3 and 0/2.
Current requested a thrust while already thrusting three times at each speed;
combined did so zero times. Wrong-facing thrusts were 0, 2, 0, 0 respectively.
These are decision-boundary requests, not counts of distinct attacks or proof
of the model's chosen target. More alignment and fewer mistakes did not produce
higher scores. Reduced attack frequency is a candidate mechanism, not a proved
cause; the prompt package also changes target selection and rule knowledge.

### Post-hoc common-time check

Added during execution after budget truncation became apparent: compare the latest
recorded step boundary shared by every trace, step 37 (3.7 simulation seconds).
Reading actions skip observation boundaries, so the exact common boundary is
earlier than the minimum cutoff. Current scores were [1, 0, 0] at both speeds;
combined scores were [0, 1, 0] at 1.0× and [0, 0, 0] at 0.75×. All had health 3
except combined/1.0×/seed30, which had health 2. This early-game descriptive check
also shows no consistent benefit. It is not the preregistered primary measure,
a matched full episode, or an opportunity-normalized attack comparison.

### Calls, costs, reproducibility and deviations

698 calls, 3 failures (two HTTPError and one TimeoutError), 3 invalid neutral
fallbacks. Failures: combined/0.75×/seed31: 1; current/1.0×/seed32: 2.
All other submitted actions were accepted. Input tokens: 1,346,919; billed-output
usage tokens: 26,264. Estimated returned-usage cost: $0.469736. Total conservative
reservation: $2.9800184, below the approved $3. Missing usage for failed calls is
not evidence of zero billing. Prices configured for 2026-11-03 were $0.30/million
input tokens and $2.50/million output tokens; exact source is in each summary.
No paid retries, held-out trials, fixtures or budget expansion.

The $0.25 per-run reservation stopped current after 61–62 calls and combined
after 55 calls. The longer intervention reserves more per decision. Simulation
exposure also differs because look advances one second. This is a major confound:
fixed-spend performance was observed, but final survival and win probability
remain unknown. Low estimated usage does not release conservative reservations.

The initial invocation stopped after saving the first episode because its
progress print passed seed twice. Corrected only logging/resume behavior and
resumed the remaining planned trials with:
`python -B -m players.combat_experiment --run --total-budget 3 --resume 20261104T072415073512Z-combat-speed-experiment`.
The completed first episode was skipped. Recorded source hashes expose the
runner revision; model adapter, default prompt and game were unchanged by it.

After episode 11, the build guard detected a workspace change: removal of
window/stretch/aspect="keep" from project.godot. The saved original manifest
showed only that file differed. Preserved the workspace edit and copied Godot
into a temporary folder, restoring only project.godot from the original build
archive. The first isolated attempt lacked imported assets and timed out at
reset before any provider call; retained under
[preflight evidence](../playtrace/20261104T072415073512Z-combat-speed-experiment/preflight-failed-combined-speed1.0-seed32/configuration.json).
Including the existing imported asset cache allowed the final planned episode
to run. [Isolated resume script](combat-speed-resume.py) records the exact setup;
it ran as `PYTHONPATH=. python -B /tmp/resume-croc-combat.py` from the midterm.
Its SHA-256 assertion verified the original build before calls. No workspace
engine setting was overwritten. Temporary copies/caches are not report artifacts.

All twelve configurations record game hash
`4691db9ee9c68dfeccd945014cf166b33a10e6c2886a2d78a2a9d80e42effa31`.
Per-run configs contain exact prompt/suite/player hashes, model identifier,
Godot version and overrides. The first trace's archive manifest and final trace's
manifest have identical source-file hashes. Traces/build archives are trusted
evaluator evidence, never player inputs. Do not stage local build ZIPs or caches.

Verification: all 26 deterministic tests passed in 24.702 seconds after an initial
sandbox failure accessing Godot logs/system certificates; reset-only speed wrapper
and action passthrough check passed. Offline analysis verified common-time boundaries.
No game rules, normal player prompt, maintained agent configuration or suite were
changed for this experiment. New runner/analyzer are opt-in.

Recompute offline:
`python -B -m players.combat_analysis playtrace/20261104T072415073512Z-combat-speed-experiment`.
[Raw combined results](../playtrace/20261104T072415073512Z-combat-speed-experiment/results.json)
and [diagnostic analysis](../playtrace/20261104T072415073512Z-combat-speed-experiment/analysis.json)
retain individual measurements and common-time scores.

## Interpretation and next decision

This experiment does not support adopting either the full combined prompt or
0.75× speed as a demonstrated performance improvement. The alignment and
color-selection signals are promising; combined instructions appear more
conservative about attacking. A focused next hypothesis is that its prediction
and attack-availability guidance suppress useful thrusts. Test that component
separately before adding more instructions or memory; do not claim it as the
identified cause.

A future completed-episode comparison needs enough conservative reservation per
run and a matched exposure plan. This experiment's $3 authorization is consumed
for reservation purposes; no further live trials are authorized by this report.
Three exploratory seeds, one stochastic trial per cell, package knowledge
differences, provider failures and budget truncation limit inference. No final
evaluation, independent review, gate approval, personal reflection or human
playtest evidence is claimed. Student design decisions remain with the student.

