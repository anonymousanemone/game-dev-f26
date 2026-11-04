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

Pending. No live observations claimed yet.
