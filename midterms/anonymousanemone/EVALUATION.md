# Evaluation — development results and first live trial; held-out comparison pending

This evaluates a self-contained excerpt of the student’s original Totenbuch game. The design is original; the implementation starts from their own existing Godot codebase.

## Declared experiment

The 2026-10-26 suite in [suite.json](suite.json) was written before player tuning. Three starting situations: spell31 tutorial/waves; standard two-sided spell32; spell32 starting at the lowest allowed position. Development uses seed 30. Held-out seeds are 101/102, 201/202 and 301/302 respectively and have not been used during setup. Run each case/held-out seed for the baseline, model history=0, and model history=2 after freezing prompts and the heuristic. This gives six episodes per policy/history condition, two per situation.

The model and baseline receive the same accessible visible-state representation and control meanings. Since 2026-11-04 they differ in one piece of knowledge: the model is not told the heka rule and must discover it (see "Heka discovery" below), while the baseline keeps it built in as an informed reference. The baseline is a real heuristic competitor: it estimates velocity from successive visible snout positions, aligns vertically, turns toward the closest threat and chooses ordinary or heka thrusts by visible color. It has no engine handle or hidden speed/spawn data. The model-history comparison is needed because one snapshot deliberately omits velocity; history can recover visible motion.

## Heka discovery (2026-11-04)

A human player learns what [shift] does by clicking the glowing heka word; until then the first red crocodile to arrive is sent back with a hint ("The signs glowing above may say how"). Agents now face the same step. The model prompt no longer says which crocodiles need heka. The observation adds `heka_word_glowing` and `notes`, and the action set adds `look`. A look shows the same message as the human's click, through the same `read_heka` function. The rule text stays in `notes` for the rest of the episode, as a player would remember it. Looking costs 1.0 s with the controls idle while the crocodiles keep coming. The baseline does not look; it keeps the rule built in.

**Goal, not yet met:** the agent's discovery should be as close as possible to a human's. A human takes time to read, may not notice or may ignore the flashing, and may click at a bad moment. The fixed 1.0 s idle look is a first approximation; that number is an assumption, not a measurement. Better estimates would come from human session recordings (time from the word first glowing to the click, and how long the bearer stays idle afterwards).

All model trials before this change used the earlier prompt, which stated the heka rule, so they are not comparable with later trials. The baseline's results are unaffected: it ignores the new observation fields and never looks.

## Current difficulty and recording revision

On November 4 the crocodile combat was synced with the tuned Totenbuch game (commit `0d5a340`). Spell 32 runs at 175 plate px/s. Each crocodile's arrival at the bearer must be at least max(half its body ÷ its speed, the wave's 0.9 s `min_gap`) from every other's, on both sides and at all heights, and crocodiles turned back wait for that before crawling again. This replaces the midterm's earlier launch-gap and distance-queue spacing. The midterm keeps only its seeded lane shuffle and agent input hooks ([patch](reports/inherited-crocodiles.patch)). Native **Record session** is beside Begin; it preserves original press semantics and records exact frame deltas. [Change, regression and replay evidence](reports/difficulty-and-recording.md).

## Arena-width fix (2026-11-04)

Headless Godot has no window and reported a square 1280×1280 viewport to every agent run. The arena's width follows the viewport's aspect (`vis_w = vp.x / z`, with zoom `z` fitted to the height). So agents fought in an arena about half as wide as the game's 1280×720 window: 1,187 instead of 2,471 world px. Crocodiles started 30–300 px from the bearer instead of 344–866, and a spell 32 copy's snout could appear 29 px away. `episode.gd` now sets the root viewport to the project's 1280×720 base size in headless runs; windowed human play is unaffected. The regression check is in `spacing_checks.gd`. It failed before the fix and passes after. **Every agent result before this fix, baseline and model, was measured in the narrow arena** and is kept below only as history.

## Current development baseline (2026-11-04, Totenbuch sync and arena-width fix)

Game content SHA-256 `d33f017b8ed276aff1b69b5800afdef62d971ca44ee2b9655463b684ad096f80`; Godot 4.7.2 on macOS. [Configuration](playtrace/20261104T025623889524Z-baseline-h2-development/configuration.json) · [summary](playtrace/20261104T025623889524Z-baseline-h2-development/summary.json); traces are beside them.

| Situation | Seed | Outcome | Score | Steps | Illegal actions | Calls |
|---|---:|---|---:|---:|---:|---:|
| spell31 | 30 | won: all_crocodiles_defeated | 9 | 396 | 0 | 0 |
| spell32 | 30 | won: all_crocodiles_defeated | 14 | 189 | 0 | 0 |
| spell32_low | 30 | won: all_crocodiles_defeated | 14 | 179 | 0 | 0 |

Earlier versions, all measured in the narrow headless arena, kept as history:
- **After the sync, before the arena fix** ([run](playtrace/20261104T023058631783Z-baseline-h2-development/summary.json)): 251 / 35 (1 turned back) / 32 (1) steps.
- **Before the sync, also November 4** ([run](playtrace/20261104T022216325694Z-baseline-h2-development/summary.json)): 251 / 70 (3 turned back) / 43 (2) steps.
- **October 26** ([run](playtrace/20261026T234254422011Z-baseline-h2-development/summary.json)): 249 / 122 (8) / 43 (2) steps. This run predates the final October 26 edits to `crocodiles.gd` and `danger_encounters.gd`, made about ten minutes later.

Local validation covers **17 tests**, including native record-button play through defeat/return-to-scroll, exact replay, altered-frame rejection, all-height/all-side spacing, the headless arena-width regression and a mocked Vertex request/response check. The previously linked 14-test GitHub CI run is historical until refreshed for this revision.

## Earlier development baselines (older game versions)

These runs belong to earlier versions and are kept as development history, not current results. The run under [playtrace](playtrace/20261026T184527216889Z-baseline-h2-development/summary.json) reproduced the results below. Its action files include build metadata and local archives; replay verified all 249 spell31 actions against their recorded results.

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

## Live model checkpoint (development, 2026-11-04)

The model player uses Gemini 3.5 Flash-Lite (`gemini-3.5-flash-lite`; the response reported model version `gemini-3.5-flash-lite`) on Vertex AI's global endpoint, paid from the course Google Cloud credit. Prices are from the [Vertex AI pricing page](https://cloud.google.com/model-garden/pricing), dated November 3, 2026: $0.30 input and $2.50 output per million tokens, with reasoning tokens billed as output. The default cost cap is $10 per runner invocation, and the bounded history holds two earlier observations.

`python -m players.checkpoint` runs the baseline and the live model on the same development episode (spell32, seed 30) and the same game version. The runner checks that before writing [the comparison](reports/session7-comparison.md). Three live trials have been run so far, all reported below. Only the first is on the current game.

**Current game: Totenbuch sync and arena-width fix** (game SHA-256 `d33f017b…`):

| Player | Outcome | Score | Steps | Illegal | Calls / failed | Fallbacks | Mean decision s | Tokens in / out | Estimated cost |
|---|---|---:|---:|---:|---|---:|---:|---|---:|
| Baseline (heuristic) | won: all_crocodiles_defeated | 14 | 189 | 0 | 0 / 0 | 0 | 0.000005 | 0 / 0 | $0 |
| Gemini 3.5 Flash-Lite, history 2 | lost: three_bites | 1 | 80 | 0 | 80 / 0 | 0 | 0.88 | 101,561 / 2,160 | $0.0359 |

Traces: [baseline](playtrace/20261104T025633917875Z-baseline-h2-development/spell32-30.jsonl), [model](playtrace/20261104T025635197909Z-model-h2-development/spell32-30.jsonl); each folder also holds its configuration and summary.

- All 80 actions came from model responses: no fallbacks, no invalid actions, every response finished with `STOP`, and no reasoning tokens were reported.
- Latency was 0.70–1.29 s (median 0.87). The episode took 71 seconds of wall time, and the pre-call reservation was $0.29.
- The baseline turned back all 14 crocodiles without losing health. Gemini was bitten at steps 32, 47 and 80, and turned one back at step 62.
- The model stood still in 33 of 80 steps. It thrust 19 times, held heka on 14 steps (4 of them while thrusting), turned left 23 times and right 6 times.
- On this episode the two players clearly differ. It is still a single development episode.

**Before the arena fix, after the Totenbuch sync** (narrow arena, game SHA-256 `ece4185b…`): both players lost in 35 steps with 1 turned back, on an identical timeline. That was the symptom that exposed the arena bug. Gemini made 35 valid model actions, at $0.0132. Traces: [baseline](playtrace/20261104T023109674461Z-baseline-h2-development/spell32-30.jsonl), [model](playtrace/20261104T023110940288Z-model-h2-development/spell32-30.jsonl).

**Earlier, before the sync** (narrow arena, game SHA-256 `4fa1f22d…`):

| Player | Outcome | Score | Steps | Illegal | Calls / failed | Fallbacks | Mean decision s | Tokens in / out | Estimated cost |
|---|---|---:|---:|---:|---|---:|---:|---|---:|
| Baseline (heuristic) | lost: three_bites | 3 | 70 | 0 | 0 / 0 | 0 | 0.000004 | 0 / 0 | $0 |
| Gemini 3.5 Flash-Lite, history 2 | lost: three_bites | 2 | 58 | 0 | 58 / 0 | 0 | 0.98 | 61,382 / 1,534 | $0.0222 |

Traces: [baseline](playtrace/20261104T021950645037Z-baseline-h2-development/spell32-30.jsonl), [model](playtrace/20261104T021952386012Z-model-h2-development/spell32-30.jsonl). All 58 model actions were valid model responses with no fallbacks. Latency was 0.64–4.22 s (median 0.87). The model never used heka.

Live spend so far is about $0.071 in estimated token cost across the three trials; provider billing remains the authority for actual charges. These are single development episodes. They show that the model player works end to end. They are not held-out evidence and support no general claim about which player is stronger. Freeze the prompt and heuristic before the held-out comparison. Do not count baseline or replay as live model evidence.

## Held-out comparison — not yet run

| Condition | Episodes | Wins/losses | Illegal actions | Limit/timeout reasons | Calls/failures | Latency | Tokens | Dated cost |
|---|---|---|---|---|---|---|---|---|
| Baseline, held-out | Pending | Pending | Pending | Pending | 0 | Pending | 0 | No API cost |
| Live model, observation only | Pending | Pending | Pending | Pending | Pending | Pending | Pending | Pending |
| Live model, two-observation history | Pending | Pending | Pending | Pending | Pending | Pending | Pending | Pending |

Store every trace, including API failures and limits. The runner hashes game/suite/prompt and logs provider response IDs, actions, bounded input observations, reported usage and elapsed latency. Error calls count toward the budget; neutral fallback is labeled separately. Cost estimates cover reported token usage at entered prices; a failed request with unavailable usage may have unknown cost, so reconcile provider billing instead of claiming zero. Model IDs can be moving aliases; use a provider snapshot ID where available.

## Deterministic validation

**Actual GitHub CI:** [dedicated midterm run — success, 14 tests](https://github.com/anonymousanemone/game-dev-f26/actions/runs/40396786117), for commit `88c9a6d09d3b44512490e4238754b4088977a157` on the course fork's `anonymousanemone/midterm` branch. GitHub installed Godot 4.7.2, imported the packaged project and ran the complete deterministic suite under Python 3.12 on Ubuntu. [Machine-readable evidence](reports/ci-evidence.json). This is the game's own workflow, not only the starter tests. The upstream course PR remains unopened. The same workflow is now in the course repository branch as `.github/workflows/midterm-anonymousanemone.yml`. The course's boundary and workflow screen (`scripts/minigames.py`) passes locally for this folder plus that file. A GitHub run for this version is pending until the branch is pushed.

See [reports/deterministic-tests.txt](reports/deterministic-tests.txt). Nineteen local tests now cover heka discovery by looking (and that the prompt no longer states the rule), archived trace replay and tamper detection, native human-session replay, cost reservations and the earlier checks: a complete baseline success, plain/red/heka rules, health/third-bite loss, original click/leave interaction, the two-encounter ending, opposite-side spacing, final-strike victory, seeded JSON replay, legal and illegal actions, terminal lock, the [observed JSON-number regression](reports/regression.md), observation leakage checks, step/call/time limits, failed calls/fallbacks, observation-only input, cost accounting and the Vertex request/response format (mocked). Direct-state GDScript fixtures test rules and are not counted as player victories.

Local Godot import, startup, scroll and opened-arena rendering checks passed. The game now uses a direct extraction of the original `dangers.tscn`. All 55 retained scene blocks match the source exactly apart from trailing blank lines between blocks (which Godot rewrites on save), and the 27 copied artwork/font files match byte-for-byte; [direct extraction evidence](reports/direct-extraction.json) and [source patch](reports/extraction.patch) document that boundary. The original HUD, papyrus, captions, avatar, camera and arena animations are retained, while unused encounter nodes and movement/combat code are removed. The packaged course workflow has now run successfully on GitHub, linked above. Add the eventual upstream course PR and refresh evidence for the final submitted version.

## Limitations — student to revise after playtests

On the current game there is one live model episode and one baseline episode on a single development seed. Earlier live trials ran in the narrow headless arena and are not comparable. The required held-out experiment (six episodes each for the baseline and the model at history 0 and 2) has not been run. A three-case small classroom sample cannot support statistical certainty. Structured positions simplify perception; inference is paused, and each decision advances 0.1 simulated seconds. Human play retains the original scroll and real-time controls. Agent evaluation wraps the same original scene, skips its opening presentation and advances the original simulation in fixed 1/60-second ticks. It uses the project's 1280×720 viewport, and human play keeps the same 16:9 view at any window shape (the aspect ratio is locked), so humans and agents see the same arena. No replacement arena or HUD is used. No learning or improvement through repeated play is claimed. No independent review, second skill session, peer feedback, recording, or student-authored reflection has yet been supplied. CREDITS.md and reports/lepsius-provenance.json document the Lepsius digital edition and its supplier. The edition was published in 1842 and is in the public domain; faithful scans create no new copyright. The HUD font is "Old Fax" by George Blackwell, under CC BY 4.0. The existing PNGs' precise PDF-to-export crop history is not recorded. The baseline has not been retuned since the arena fix; it now wins all three development cases. A baseline that strong may leave little room for the model to do better on held-out cases. The model's single spell32 loss against the baseline's win is one episode and does not rank the players in general.

The student must write their own interpretation of model failures/history, design decisions and actual peer observations. If partner notes have not arrived by November 6, state that and link the notes you gave.
