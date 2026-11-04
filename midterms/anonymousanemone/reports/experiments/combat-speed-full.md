# Full-episode combat prompt × speed comparison — 2026-11-04

## Plan before execution

Follow-up to the truncated combat-speed experiment: four fresh Spell32 episodes,
one per current/combined prompt × 1.0/0.75 crocodile speed, matched development
seed 30. Prediction: combined instructions and slower speed increase turn-backs
and completion success; equal/lower scores contradict directional improvement.
Primary measures: terminal outcome/reason and turn-backs out of 14. Alignment,
health, thrusts, provider errors and usage are diagnostics. One stochastic trial
per cell cannot establish general performance or isolate individual instructions.

User authorized $10 total for these four trials. Vertex gemini-3.5-flash-lite,
$2.50 conservative reservation per episode, 1200 calls, 30 seconds/call,
1800 wall seconds/episode. No paid retries or favorable-result selection. A run
that reaches a limit is incomplete, not a loss. Memory off, history 2, reach flag
off, 3 lives, normal crocodile count, 1024 output cap, six-frame actions. Existing
configured dated prices are saved per run. No held-out seeds or suite changes.

Exact current PROMPT is control, current PROMPT + COMBAT is intervention; texts
and hashes saved. Existing speed reset wrapper changes no observation fields or
rules and exposes no hidden state. Same authoritative Godot scene. Order:
current/1.0, combined/1.0, current/0.75, combined/0.75. Fixed order/provider
stochasticity are limitations. This is a fresh comparison, not continuation of
partial traces; historical results are context only. Source/build hashes,
configuration, raw traces and summaries saved uniquely. Preserve failures and
neutral fallbacks. Apply make-experiment and crocodile-evaluation skills.

Command: `python -B -m players.combat_experiment --run --full --total-budget 10`
Offline analysis: `python -B -m players.combat_analysis playtrace/RUN-DIRECTORY`.

## Results

Executed November 4, 2026 UTC. All four fresh episodes reached real terminal
losses, with no cost, call or time truncation and no retries.

| Prompt | Speed | Seed | Outcome / reason | Turn-backs | Health | Steps | Calls / failed | Usage USD | Reserved USD | Evidence |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| combined | 1.0 | 30 | lost / three_bites | 7/14 | 0 | 159 | 159/0 | 0.123176 | 0.727785 | [trace](../../playtrace/20261104T075055997841Z-combat-speed-full/combined-speed1.0-seed30/spell32-30.jsonl), [config](../../playtrace/20261104T075055997841Z-combat-speed-full/combined-speed1.0-seed30/configuration.json), [summary](../../playtrace/20261104T075055997841Z-combat-speed-full/combined-speed1.0-seed30/summary.json) |
| current | 1.0 | 30 | lost / three_bites | 2/14 | 0 | 90 | 90/1 | 0.057100 | 0.364700 | [trace](../../playtrace/20261104T075055997841Z-combat-speed-full/current-speed1.0-seed30/spell32-30.jsonl), [config](../../playtrace/20261104T075055997841Z-combat-speed-full/current-speed1.0-seed30/configuration.json), [summary](../../playtrace/20261104T075055997841Z-combat-speed-full/current-speed1.0-seed30/summary.json) |
| combined | 0.75 | 30 | lost / three_bites | 6/14 | 0 | 182 | 182/1 | 0.142574 | 0.836370 | [trace](../../playtrace/20261104T075055997841Z-combat-speed-full/combined-speed0.75-seed30/spell32-30.jsonl), [config](../../playtrace/20261104T075055997841Z-combat-speed-full/combined-speed0.75-seed30/configuration.json), [summary](../../playtrace/20261104T075055997841Z-combat-speed-full/combined-speed0.75-seed30/summary.json) |
| current | 0.75 | 30 | lost / word_stolen | 2/14 | 2 | 99 | 90/1 | 0.059281 | 0.368480 | [trace](../../playtrace/20261104T075055997841Z-combat-speed-full/current-speed0.75-seed30/spell32-30.jsonl), [config](../../playtrace/20261104T075055997841Z-combat-speed-full/current-speed0.75-seed30/configuration.json), [summary](../../playtrace/20261104T075055997841Z-combat-speed-full/current-speed0.75-seed30/summary.json) |

## Analysis

Combined instructions improved score in both matched speed comparisons: 7 versus
2 at normal speed, and 6 versus 2 at 0.75×. All still lost. Slower crocodiles
changed current score from 2 to 2 and combined score from 7 to 6. These trials
support the combined prompt as the more promising candidate; they do not show
a score benefit from slowing down or establish a general effect from one trial.
The current slow run lost to word_stolen; the other three lost to three_bites.

Median absolute vertical error was 52.89 px (current/1.0), 78.00 px
(current/0.75), 25.11 px (combined/1.0), and 6.95 px (combined/0.75).
Within-20-px decisions: 30/77, 20/76, 67/147, 99/169 respectively.
Visible-threat thrust requests: 6, 5, 8, 10. Proxy color-mismatched thrusts:
1, 0, 0, 0. These measurements describe behavior against the nearest-threat
analysis proxy, not proof of target intent. The slower combined run aligned
better yet scored one fewer turn-back, so alignment alone does not explain
success. More opportunities, stochastic actions and transport errors remain
possible influences. The earlier hypothesis that combined instructions suppress
attacks was based on truncated prefixes; completed episodes now show useful
attacks and larger scores. This does not isolate which instruction helped.

## Cost, failures and verification

521 calls, 3 timeouts, 3 invalid neutral fallbacks. One timeout in each condition
except combined/1.0, which had none. Retained all failures; their differing
locations confound attribution. Returned usage: 1,106,103 input tokens and
20,120 output tokens (including any billed reasoning usage). Estimated usage
cost $0.382131; total reservation $2.2973348 of the authorized $10. Prices saved
per run: 2026-11-03, $0.30/million input and $2.50/million output, with configured
source. Failed-call usage is missing; billing is not independently reconciled.

The user requested notice and a decision before increasing limits. Monitored
reservations during execution; no episode approached its $2.50 cap (largest
$0.836370), and total stayed far below $10. No increase was needed or made.

All 26 deterministic tests passed in 25.410 seconds. Four source-file manifests
match; all four configurations share the game hash below. No engine/interface,
observation schema, standard player prompt, suite, or maintained model settings
were changed. Added an opt-in --full runner mode with seed 30, four episodes,
$10 maximum and 1800-second wall limit. Normal experiment mode remains capped
at $3 across twelve trials. Exact prompts, source hashes, Godot version, suite
hashes, settings and runtime model are saved in every configuration.

Game SHA-256: `15cefaf63adce9a684d0a5e266745f86498aa02e6687e987a6172cad7a771905`.

[Raw results](../../playtrace/20261104T075055997841Z-combat-speed-full/results.json)
and [offline diagnostics](../../playtrace/20261104T075055997841Z-combat-speed-full/analysis.json).
Command actually run: `python -B -m players.combat_experiment --run --full --total-budget 10`.
No execution retries, held-out seeds or isolated build recovery were needed.
Earlier truncated experiments are separate evidence and are not pooled here.

## Limits and decision

Use combined instructions at normal speed as the leading candidate for a future
matched development comparison across additional seeds. This run does not
justify slowing gameplay for the agent or claim it can win. One stochastic
trial per cell on one development seed, unequal survival/exposure, fixed order,
provider timeouts, and multiple bundled instructions limit causal inference.
No independent review, human playtest, gate approval or student reflection is
claimed. No further paid trials are included in this completed four-run request.

