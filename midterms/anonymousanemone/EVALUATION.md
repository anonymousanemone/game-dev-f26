# Evaluation

## Declared suite and conditions

[suite.json](suite.json) was declared October 26, 2026 before player tuning. Development uses seed 30. The three situations and reserved final seeds were:

| Situation | Starting state | Held-out seeds |
|---|---|---|
| spell31 | One-sided tutorial and mixed-color waves | 101, 102 |
| spell32 | Two-sided fight, default vertical position | 201, 202 |
| spell32_low | Same fight, lowest allowed vertical position | 301, 302 |

After freezing the game, suite, heuristic and prompt, each case/seed ran once for baseline, model history=0 and model history=2: 18 episodes, including 12 live model trials. These seeds are consumed; no tuning or paid retries on them are claimed.

The model was Vertex **gemini-3.5-flash-lite**, using the student-selected combined combat prompt recorded in [agent-config.json](agent-config.json). Standard settings: speed=1, three lives, tuned crocodile counts, event memory off and privileged reach flag off. Godot owns state, validates controls and determines outcomes.

Both players receive structured visible observations and know the red/plain heka rule. The baseline estimates motion, aligns and predicts strikes after a 0.4-second visibility delay, retaining up to ten observations. Model history=0/2 supplies zero or two explicit prior snapshots. Both model settings retain motion-derived `seconds_to_bearer` and persistent read notes; this measures additional snapshots, not temporal information versus none. Historical baseline summaries mislabeled history capacity as two; new summaries record ten.

## Frozen comparison — November 4, 2026

| Condition | Episodes | Wins / losses | Turn-backs | Invalid / failed calls | Model calls | Returned-usage USD | Reserved USD |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline | 6 | 6 / 0 | 74/74 | 0 / 0 | 0 | 0 | 0 |
| Model, no explicit history | 6 | 0 / 6 | 7/74 | 11 / 11 | 875 | 0.423916 | 3.581124 |
| Model, two-observation history | 6 | 2 / 4 | 30/74 | 3 / 3 | 1324 | 0.975958 | 6.042026 |

All episodes reached game wins/losses; none hit step, call, cost or wall-time limits. Both model wins were spell31; all model spell32/low-start episodes lost. Fourteen provider failures produced explicitly labeled neutral fallbacks, counted as invalid actions and failed calls rather than successful model moves.

Estimated returned-usage cost totaled **$1.3998745**; conservative reservations totaled **$9.6231501** under the authorized **$20** shared cap. Saved Vertex prices, dated November 3, were $0.30/M input and $2.50/M output tokens, including reasoning output. Failed requests may have unavailable usage; reconcile actual charges with provider billing.

The [full final report](reports/held-out-final.md) links every episode's outcome, steps, calls, latency, token usage, prices, runtime model and trace. Its [frozen configuration](playtrace/20261104T082332827621Z-held-out-final/configuration.json) records game, suite, prompt and player-source identifiers. The exact evaluated runner is recoverable from commit `aee02a6`.

## Development and checkpoint evidence

The [first matched live comparison](reports/session7-comparison.md) was completed November 4, after the October 26 checkpoint date. It establishes live model-controlled play separately from deterministic fixtures.

The [full combat experiment](reports/experiments/combat-speed-full.md) supports the selected prompt: on development seed 30, control turned back 2/14 at each speed, while combined turned back 7/14 at normal speed and 6/14 at 0.75×. All four lost; one trial per condition supports a development choice, not a general ranking. Other prompt, alignment, memory, reach-assistance and difficulty studies remain in the [report index](reports/README.md), with their failures and raw evidence. They are not pooled with the frozen suite.

Earlier narrow-headless-arena results used different geometry and cannot validate the corrected game. [Observed regression evidence](reports/validation/regression.md) documents that correction and JSON-number action validation. The [historical difficulty/recording report](reports/validation/difficulty-and-recording.md) distinguishes superseded tuning from the later game.

## Deterministic verification

[Dedicated course CI](https://github.com/columbia-university-ai-games/game-dev-f26/actions/runs/41857753499) passed **29 tests** on commit `ae74a5d699b877f11098c3d09c3d610c6d5c0771`, Godot 4.7.2 / Python 3.12 / Ubuntu. [Machine-readable evidence](reports/validation/ci-evidence.json) records the run and scope. This covers that commit, not subsequent local edits; no paid calls were part of CI.

Run `python -m unittest discover -s tests -v` from `midterms/anonymousanemone/`. Checks cover rule invariants, successful baseline play, legal/illegal actions, terminal locks, seeded determinism, observation boundaries, observed regressions, step/call/time limits, failed calls, budget reservations and replay/tamper detection. Mocked Vertex responses check transport, not live model performance. Direct-state rule fixtures are not player victories. [Independent review findings and responses](review.md) are separate evidence.

The later logging correction records actual simulation frames from encounter time and charged-step frames separately as `nominal_simulation_frame`. Historical traces retain their original hashes and nominal frame values; recover actual frames as `round(observation.time * 60)`. Step-cap and reset/replay fixes are documented in review.md. No paid reruns were made for these corrections.

## Limitations and remaining evidence

Three related situations with one stochastic trial per seed/condition cannot establish statistical certainty. History=2 won more episodes here, but unequal provider failures and shared derived-motion/read-note features limit causal claims. The baseline is a strong hand-written predictor; its history capacity differs from the model's. Structured coordinates simplify perception, and inference pauses simulation. Human play uses real-time controls while automated actions normally advance 0.1 seconds; `look` assumes one second of reading, capped by the remaining step budget. Neither policy learns across episodes, and repeated play alone is not evidence of improvement.

Actual anonymous [peer notes](PEER-NOTES.md), the [viewable demonstration](README.md#recording-and-replay), and the student-authored [team log](AGENT-TEAM.md) remain pending. Source inspection and automated tests cannot establish first-time-player clarity or fun. The student must provide their own interpretation and incorporate actual playtest observations. If partner notes have not arrived by November 6, say so here and link the notes given.
