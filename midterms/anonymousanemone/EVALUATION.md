# Evaluation — development results, live trials pending

This evaluates a self-contained excerpt of the student’s original Totenbuch game. The design is original; the implementation starts from their own existing Godot codebase.

## Declared experiment

The 2026-10-26 suite in [suite.json](suite.json) was written before player tuning. Three starting situations: spell31 tutorial/waves; standard two-sided spell32; spell32 starting at the lowest allowed position. Development uses seed 30. Held-out seeds are 101/102, 201/202 and 301/302 respectively and have not been used during setup. Run each case/held-out seed for the baseline, model history=0, and model history=2 after freezing prompts and the heuristic. This gives six episodes per policy/history condition, two per situation.

The model and baseline receive the same accessible visible-state representation and control rules. The baseline is a real heuristic competitor: it estimates velocity from successive visible snout positions, aligns vertically, turns toward the closest threat and chooses ordinary or heka thrusts by visible color. It has no engine handle or hidden speed/spawn data. The model-history comparison is needed because one snapshot deliberately omits velocity; history can recover visible motion.

## Recorded development baseline

Latest October 26 checkpoint evidence is in [the first comparison table](reports/session7-comparison.md) and [readiness audit](reports/session7-readiness.md). The fresh run under [playtrace](playtrace/20261026T184527216889Z-baseline-h2-development/summary.json) reproduced the results below. Its action files include build metadata and local archives; replay verified all 249 spell31 actions against their recorded results.

Godot 4.7.2 on macOS; game content SHA-256 `07df2c5adc03eed03574cdd8f72588aaf4294086b14b4f4fecc0fa6e2817ac1b`. Configuration records the suite and prompt hashes and timestamps.

| Situation | Seed | Outcome | Score | Steps | Illegal actions | Calls |
|---|---:|---|---:|---:|---:|---:|
| spell31 | 30 | won: all_crocodiles_defeated | 9 | 249 | 0 | 0 |
| spell32 | 30 | lost: three_bites | 3 | 64 | 0 | 0 |
| spell32_low | 30 | lost: three_bites | 1 | 37 | 0 | 0 |

[Run configuration](reports/development/20261026T113707082914Z-baseline-h2-development/configuration.json), [full summary including latency](reports/development/20261026T113707082914Z-baseline-h2-development/summary.json). Raw traces:

- [spell31, seed 30](reports/development/20261026T113707082914Z-baseline-h2-development/spell31-30.jsonl)
- [spell32, seed 30](reports/development/20261026T113707082914Z-baseline-h2-development/spell32-30.jsonl)
- [spell32_low, seed 30](reports/development/20261026T113707082914Z-baseline-h2-development/spell32_low-30.jsonl)

Baseline: 1 win, 2 losses across these three development episodes. No model tokens or API charges. Repeated development runs are debugging/reproducibility evidence, not extra independent evaluation trials. Both failed spell32 episodes are retained. Runs under `reports/obsolete-replacement/` belong to discarded replacement layouts and are not evidence for this original-scene extraction.

## Live model and held-out comparison — not yet run

The user now authorizes a checkpoint run with the cheapest current model and a $10 ceiling. GPT-6 Luna is configured with prices dated October 26, 2026 ($0.10 input / $0.50 output per million tokens at standard rates); the private API key is still blank. No live provider outcome, model success rate, cost or latency is claimed. Mocked provider responses in tests verify the application only. After supplying the key, `python -m players.checkpoint` runs a matched development baseline/model pair and writes its actual comparison. Freeze tuning before the held-out comparison. Do not count baseline or replay as live model evidence.

| Condition | Episodes | Wins/losses | Illegal actions | Limit/timeout reasons | Calls/failures | Latency | Tokens | Dated cost |
|---|---|---|---|---|---|---|---|---|
| Baseline, held-out | Pending | Pending | Pending | Pending | 0 | Pending | 0 | No API cost |
| Live model, observation only | Pending | Pending | Pending | Pending | Pending | Pending | Pending | Pending |
| Live model, two-observation history | Pending | Pending | Pending | Pending | Pending | Pending | Pending | Pending |

Store every trace, including API failures and limits. The runner hashes game/suite/prompt and logs provider response IDs, actions, bounded input observations, reported usage and elapsed latency. Error calls count toward the budget; neutral fallback is labeled separately. Cost estimates cover reported token usage at entered prices; a failed request with unavailable usage may have unknown cost, so reconcile provider billing instead of claiming zero. Model IDs can be moving aliases; use a provider snapshot ID where available.

## Deterministic validation

**Actual GitHub CI:** [dedicated midterm run — success, 14 tests](https://github.com/anonymousanemone/game-dev-f26/actions/runs/40396786117), for commit `88c9a6d09d3b44512490e4238754b4088977a157` on the course fork's `anonymousanemone/midterm` branch. GitHub installed Godot 4.7.2, imported the packaged project and ran the complete deterministic suite under Python 3.12 on Ubuntu. [Machine-readable evidence](reports/ci-evidence.json). This is the game's own workflow, not only the starter tests. The upstream course PR remains unopened; the older instructor-owned minigame boundary workflow currently conflicts with the required `.github/workflows/midterm-anonymousanemone.yml` addition.

See [reports/deterministic-tests.txt](reports/deterministic-tests.txt). Fourteen local tests now cover archived human-action replay, tamper detection, cost reservations and the earlier checks: a complete baseline success, plain/red/heka rules, health/third-bite loss, original click/leave interaction, the two-encounter ending, opposite-side spacing, final-strike victory, seeded JSON replay, legal and illegal actions, terminal lock, the [observed JSON-number regression](reports/regression.md), observation leakage checks, step/call/time limits, failed calls/fallbacks, observation-only input and cost accounting. Direct-state GDScript fixtures test rules and are not counted as player victories.

Local Godot import, startup, scroll and opened-arena rendering checks passed. The game now uses a direct extraction of the original `dangers.tscn`. All 55 retained scene blocks and 27 copied artwork/font files match the source byte-for-byte; [direct extraction evidence](reports/direct-extraction.json) and [source patch](reports/extraction.patch) document that boundary. The original HUD, papyrus, captions, avatar, camera and arena animations are retained, while unused encounter nodes and movement/combat code are removed. The packaged course workflow has now run successfully on GitHub, linked above. Add the eventual upstream course PR and refresh evidence for the final submitted version.

## Limitations — student to revise after playtests

This is a setup comparison on one development seed per situation, not the required completed live experiment. A three-case small classroom sample cannot support statistical certainty. Structured positions simplify perception; inference is paused, and each decision advances 0.1 simulated seconds. Human play retains the original scroll and real-time controls. Agent evaluation wraps the same original scene, skips its opening presentation and advances the original simulation in fixed 1/60-second ticks. No replacement arena or HUD is used. No learning or improvement through repeated play is claimed. No independent review, second skill session, peer feedback, recording, or student-authored reflection has yet been supplied. The exact historical scan provenance/reuse terms remain to be recorded. The baseline has not been retuned for the restored original arena. Its two spell32 losses are reported honestly; they do not establish that held-out cases are balanced or that a model will perform better.

The student must write their own interpretation of model failures/history, design decisions and actual peer observations. If partner notes have not arrived by November 6, state that and link the notes you gave.
