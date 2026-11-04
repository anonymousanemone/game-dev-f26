# Evaluation — development results and first live trial; held-out comparison pending

## Final tuned prompt selection — November 4

The student selected the **combined combat prompt** as the final tuned default
in `players/model.py`, retaining Vertex Gemini 3.5 Flash-Lite, normal speed,
memory off and the standard observation boundary. `agent-config.json` records
the exact prompt hash and evidence. This supersedes earlier descriptions of the
default prompt leaving the heka rule to discovery: the selected prompt explicitly
teaches red/plain heka selection, target priority, facing, alignment and timing.
The historical control remains available as `BASE_PROMPT`; the combat experiment
runner preserves that control and does not append the combined instructions twice.

In the [four full development runs](reports/experiments/combat-speed-full.md), turn-backs
were 2/14 and 2/14 for the control at 1.0× and 0.75× speed, versus 7/14 and 6/14
for combined. All four lost. One stochastic trial per condition on seed 30
supports this selection only as development evidence; it is not a general ranking
or a successful held-out evaluation. No additional paid calls were made to adopt
the prompt. The student will commit manually; no gate or merge is approved here.


This evaluates a self-contained excerpt of the student’s original Totenbuch game. The design is original; the implementation starts from their own existing Godot codebase.

## Declared experiment

The 2026-10-26 suite in [suite.json](suite.json) was written before player tuning. Three starting situations: spell31 tutorial/waves; standard two-sided spell32; spell32 starting at the lowest allowed position. Development uses seed 30. Held-out seeds are 101/102, 201/202 and 301/302 respectively and have not been used during setup. Run each case/held-out seed for the baseline, model history=0, and model history=2 after freezing prompts and the heuristic. This gives six episodes per policy/history condition, two per situation.

The model and baseline receive the same accessible visible-state representation and control meanings. The final combined prompt teaches the heka rule explicitly, as the baseline already knows it. The baseline reacts only after a crocodile has been visible for 0.4 s, estimates velocity from successive visible positions, aligns, turns and chooses heka by color. It has no engine handle or hidden speed/spawn data.

The baseline retains up to ten previous observations. New summaries record `history: 10`; historical summaries reported 2 incorrectly. Model history=0 sends no explicit previous observations; history=2 sends up to two. Both receive `seconds_to_bearer`, derived from consecutive visible positions, and persistent read notes. This comparison measures the added value of explicit snapshots beyond those existing temporal features. It does not isolate motion access versus no motion access. Optional event memory is off in standard runs and is reported separately.

## Historical heka-discovery condition (2026-11-04)

Earlier development prompts left the red/plain heka rule unstated. In those trials agents could use `look` to read the same message a human sees by clicking the glowing word. The resulting notes persist through the episode. Looking normally costs 1.0 s of idle controls while crocodiles continue moving; the reading duration is an assumption, not a human measurement. The step-cap fix now truncates that duration to the remaining budget. The baseline did not look because it already knew the rule.

The selected combined prompt supersedes that discovery condition: it teaches the rule directly. Comparisons across these prompt versions must retain those knowledge differences. Human discovery and clarity still require peer playtesting.

## Current difficulty and recording revision

On November 4 the crocodile combat was synced with the tuned Totenbuch game (commit `0d5a340`). Spell 32 runs at 175 plate px/s. Each crocodile's arrival at the bearer must be at least max(half its body ÷ its speed, the wave's 0.9 s `min_gap`) from every other's, on both sides and at all heights, and crocodiles turned back wait for that before crawling again. This replaces the midterm's earlier launch-gap and distance-queue spacing. The midterm keeps only its seeded lane shuffle and agent input hooks ([patch](reports/provenance/inherited-crocodiles.patch)). Native **Record session** is beside Begin; it preserves original press semantics and records exact frame deltas. [Change, regression and replay evidence](reports/validation/difficulty-and-recording.md).

## Arena-width fix (2026-11-04)

Headless Godot has no window and reported a square 1280×1280 viewport to every agent run. The arena's width follows the viewport's aspect (`vis_w = vp.x / z`, with zoom `z` fitted to the height). So agents fought in an arena about half as wide as the game's 1280×720 window: 1,187 instead of 2,471 world px. Crocodiles started 30–300 px from the bearer instead of 344–866, and a spell 32 copy's snout could appear 29 px away. `episode.gd` now sets the root viewport to the project's 1280×720 base size in headless runs; windowed human play is unaffected. The regression check is in `spacing_checks.gd`. It failed before the fix and passes after. **Every agent result before this fix, baseline and model, was measured in the narrow arena** and is kept below only as history.

## Baseline reaction delay (2026-11-04)

The baseline's job is to be a fair, simple competitor: a hand-written policy that uses only what the player can see, so the comparison shows whether the model adds anything. Because this is a reaction game, an instant, exact policy wins almost by construction. To make it a closer stand-in for a human player, the baseline now ignores a crocodile until it has been visible for **0.4 s** (`REACTION_SECONDS` in [baseline.py](players/baseline.py)). In the student's four session recordings a new crocodile was first acted on 0.40–1.17 s after it appeared (middle half of 44 cases, median 0.59 s); the student chose the fast end, 0.4 s. The student took longer to turn toward a crocodile behind them (median 1.52 s, 9 cases), but that sample is small and partly reflects choice, so no separate turning delay was added. Once it reacts, the baseline still estimates speed and predicts the strike point exactly. See [REFLECTION-NOTES.md](REFLECTION-NOTES.md) for the recordings analysis.

## Current development baseline (2026-11-04, with 0.4 s reaction delay)

Game content SHA-256 `5e81f385505bc61cfa794cdb369b78337377c38d7d489cb8b648e4e8e09824cf`; Godot 4.7.2 on macOS. [Configuration](playtrace/20261104T060838473822Z-baseline-h2-development/configuration.json) · [summary](playtrace/20261104T060838473822Z-baseline-h2-development/summary.json); traces are beside them.

| Situation | Seed | Outcome | Score | Steps | Bites | Illegal actions | Calls |
|---|---:|---|---:|---:|---:|---:|---:|
| spell31 | 30 | won: all_crocodiles_defeated | 9 | 396 | 0 | 0 | 0 |
| spell32 | 30 | won: all_crocodiles_defeated | 14 | 215 | 1 | 0 | 0 |
| spell32_low | 30 | won: all_crocodiles_defeated | 14 | 205 | 1 | 0 | 0 |

Without the delay, earlier the same day ([run](playtrace/20261104T025623889524Z-baseline-h2-development/summary.json)), it won in 396 / 189 / 179 steps with no bites. With 0.6 s ([run](playtrace/20261104T060429310913Z-baseline-h2-development/summary.json)) it won in 396 / 217 / 207 steps with one bite in each spell32 case. The live checkpoint below was run against the baseline before any delay.

## Crocodile speed sweep (2026-11-04)

[Full report](reports/experiments/speed-sweep.md). Raising every wave's speed (five non-held-out seeds per setting, baseline only), the 0.4 s baseline wins every spell32 seed up to 1.4× the tuned speed, then 1 in 5 at 1.6×–2.0× and none from 2.2×. An instant-reaction baseline also fails from about 2.2×, so beyond that the game is too fast for this strategy whatever the reaction time; between 1.6× and 2.0× the 0.4 s delay decides it. Spell31 has no breaking point up to 3×; its few losses at 1.6× and 2.0× look like a timing quirk in the baseline's fixed-lead strike prediction (likely, not verified). At the tuned speed the baseline has about 1.4× of headroom, while the student lost several first spell32 attempts at 1.0×.

Earlier versions, all measured in the narrow headless arena, kept as history:
- **After the sync, before the arena fix** ([run](playtrace/20261104T023058631783Z-baseline-h2-development/summary.json)): 251 / 35 (1 turned back) / 32 (1) steps.
- **Before the sync, also November 4** ([run](playtrace/20261104T022216325694Z-baseline-h2-development/summary.json)): 251 / 70 (3 turned back) / 43 (2) steps.
- **October 26** ([run](playtrace/20261026T234254422011Z-baseline-h2-development/summary.json)): 249 / 122 (8) / 43 (2) steps. This run predates the final October 26 edits to `crocodiles.gd` and `danger_encounters.gd`, made about ten minutes later.

The pre-review local validation covered **26 tests**, including native record-button play through defeat/return-to-scroll, exact replay, altered-frame rejection, all-height/all-side spacing, the headless arena-width regression and a mocked Vertex request/response check. The previously linked 14-test GitHub CI run is historical until refreshed for this revision.

## Earlier development baselines (older game versions)

Duplicate October 26 baseline traces and discarded-layout runs have been removed from the working tree. They remain recoverable from Git history; see [historical material](reports/README.md#historical-material). These are not current evaluation evidence.

## Live model checkpoint (development, 2026-11-04)

The model player uses Gemini 3.5 Flash-Lite (`gemini-3.5-flash-lite`; the response reported model version `gemini-3.5-flash-lite`) on Vertex AI's global endpoint, paid from the course Google Cloud credit. Prices are from the [Vertex AI pricing page](https://cloud.google.com/model-garden/pricing), dated November 3, 2026: $0.30 input and $2.50 output per million tokens, with reasoning tokens billed as output. The default cost cap is $10 per runner invocation, and the bounded history holds two earlier observations.

`python -m players.checkpoint` runs the baseline and the live model on the same development episode (spell32, seed 30) and the same game version. The runner checks that before writing [the comparison](reports/session7-comparison.md). The ten trials summarized in this historical checkpoint section precede the later alignment and combat experiments linked above; this is not a current cumulative trial count. Prompts and game hashes must be checked per run.

**Prompt and observation tuning on the development case** (spell32, seed 30; history 2; each a single episode). Three attempts under the heka-discovery rules:

| Attempt | Prompt SHA-256 | Gemini outcome | Kills | Thrusts (median distance from tip) | Moving | Calls | Cost | Baseline on the same run |
|---|---|---|---:|---|---:|---:|---:|---|
| A. Discovery rules only | `c706d99c…` | lost: three_bites | 0 | 9 (223 px) | 8% | 56 | $0.0286 | won 14/14, no delay ([trace](playtrace/20261104T054253858015Z-baseline-h2-development/spell32-30.jsonl)) |
| B. + distances in the observation (option 1) | `9daf00e0…` | lost: three_bites | 0 | 5 (67 px) | 39% | 56 | $0.0340 | won 14/14, 1 bite, 0.4 s delay ([trace](playtrace/20261104T061922863367Z-baseline-h2-development/spell32-30.jsonl)) |
| C. + targeting and timing facts in the prompt (option 2) | `5f41808f…` | lost: three_bites | 0 | 1 (92 px) | 37% | 56 | $0.0362 | won 14/14, 1 bite, 0.4 s delay ([trace](playtrace/20261104T062200879251Z-baseline-h2-development/spell32-30.jsonl)) |

Model traces: [A](playtrace/20261104T054256539690Z-model-h2-development/spell32-30.jsonl), [B](playtrace/20261104T061923835525Z-model-h2-development/spell32-30.jsonl), [C](playtrace/20261104T062201832076Z-model-h2-development/spell32-30.jsonl). All 168 calls returned valid actions with no fallbacks.

- **B (option 1)** adds, for each visible crocodile, `dx_from_tip` and `dy_from_tip` (snout minus spear tip), `side`, and `seconds_to_bearer` (time until the snout reaches the bearer at the motion seen since the previous observation; null until seen moving). These are derived only from what is on screen; there is no "in reach" flag. Gemini moved far more (39% of decisions against 8%) and thrust much closer (67 px against 223 px), but still turned nothing back.
- **C (option 2)** adds facts the model had got wrong: deal first with the crocodile that will reach you soonest; start a thrust when it is on the side you face within about 40 px horizontally and 20 px vertically; heka counts only when held with the thrust; look only when nothing will reach you within about 2 s. The prompt still does not say which crocodiles need heka. Gemini thrust only once. Two causes are visible in the trace. First, one movement step is 39 px (390 px/s for 0.1 s), wider than the ±20 px window, so it bounced past the right height while the first crocodile closed in. Second, from step 40 to 47 a red crocodile was level with the spear (vertical offset 0) and passed 40 px and then 13 px from the tip, yet it never thrust; it had not read the heka word yet. It then looked with a crocodile 1.7 s away, against its own 2 s instruction, and was facing the wrong way for the last bite.
- In all three attempts the bites came at steps 32, 47 and 65. Because Gemini never stopped a crocodile, they arrived on the seeded schedule regardless of what it did.
- The prompt and observation changes were made on the development seed only; no held-out seed has been used.

**Learning experiment: 5 lives, 20 crocodiles, and an event-log memory** ([full report](reports/experiments/learning-experiment.md)). Option 2 was dropped and the prompt is back to option 1 plus one sentence describing `memory`. The runner's optional `--memory` sends the model a log of its own thrusts and looks, crocodiles turned back, bites and game messages. Results:

| Gemini run | Turned back | Outcome |
|---|---|---|
| Memory, 3 lives / 14 crocodiles | 1 | lost: health 0 |
| No memory, 5 lives / 20 crocodiles | 0 | lost: health 0 |
| Memory, 5 lives / 20 crocodiles | 3 | lost: word stolen |

The baseline won 5 / 20 with no bites. No Gemini run did clearly better in its second half than its first, so there is no sign of learning within an episode. Memory produced the only crocodiles Gemini has turned back. After reading the shift rule, though, the 3 / 14 memory run thrust with heka on 35 steps in a row at a distant red crocodile. Extra lives alone only made the episode longer. Cost $0.193 for the three runs.

**Reach flag experiment** ([full report](reports/experiments/reach-flag-experiment.md)). With an optional `in_reach` flag on each crocodile (the game's strike test at its current position; no memory, standard game), Gemini again lost with 0 turned back ($0.035). The flag was true on only 2 of its 56 decisions; it thrust on both, but missed. The deterministic baseline shows the flag works when aiming is right: every baseline thrust started while it was true hit (7 of 7), and a test player with the baseline's aiming that thrusts only on the flag won 14 / 14. Gemini's problem is getting a crocodile within reach at all (height and facing), not the moment of the thrust.

**Before heka discovery: Totenbuch sync and arena-width fix** (game SHA-256 `d33f017b…`):

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

The historical ten-trial subtotal was about $0.398 in estimated token cost; later experiments report their own usage and reservations, so this is not a cumulative spend total; provider billing remains the authority for actual charges. These are single development episodes. They show that the model player works end to end. They are not held-out evidence and support no general claim about which player is stronger. Freeze the prompt and heuristic before the held-out comparison. Do not count baseline or replay as live model evidence.

## Held-out comparison — not yet run

| Condition | Episodes | Wins/losses | Illegal actions | Limit/timeout reasons | Calls/failures | Latency | Tokens | Dated cost |
|---|---|---|---|---|---|---|---|---|
| Baseline, held-out | Pending | Pending | Pending | Pending | 0 | Pending | 0 | No API cost |
| Live model, no explicit history (derived motion retained) | Pending | Pending | Pending | Pending | Pending | Pending | Pending | Pending |
| Live model, two-observation history | Pending | Pending | Pending | Pending | Pending | Pending | Pending | Pending |

Store every trace, including API failures and limits. The runner hashes game/suite/prompt and logs provider response IDs, actions, bounded input observations, reported usage and elapsed latency. Error calls count toward the budget; neutral fallback is labeled separately. Cost estimates cover reported token usage at entered prices; a failed request with unavailable usage may have unknown cost, so reconcile provider billing instead of claiming zero. Model IDs can be moving aliases; use a provider snapshot ID where available.

## Deterministic validation

**Actual GitHub CI:** [dedicated midterm run — success, 14 tests](https://github.com/anonymousanemone/game-dev-f26/actions/runs/40396786117), for commit `88c9a6d09d3b44512490e4238754b4088977a157` on the course fork's `anonymousanemone/midterm` branch. GitHub installed Godot 4.7.2, imported the packaged project and ran the complete deterministic suite under Python 3.12 on Ubuntu. [Machine-readable evidence](reports/validation/ci-evidence.json). This is the game's own workflow, not only the starter tests. The upstream course PR remains unopened. The same workflow is now in the course repository branch as `.github/workflows/midterm-anonymousanemone.yml`. The course's boundary and workflow screen (`scripts/minigames.py`) passes locally for this folder plus that file. A GitHub run for this version is pending until the branch is pushed.

The latest local result is recorded in the review-fixes section below; the obsolete test log is retained in Git history. The deterministic tests cover the optional reach flag, the lives and crocodile-count settings, the model's optional event-log memory, the per-crocodile distance fields, the crocodile speed setting, the baseline's 0.4 s reaction delay, reading through look and the historical control prompt leaving the rule unstated, archived trace replay and tamper detection, native human-session replay, cost reservations and the earlier checks: a complete baseline success, plain/red/heka rules, health/third-bite loss, original click/leave interaction, the two-encounter ending, opposite-side spacing, final-strike victory, seeded JSON replay, legal and illegal actions, terminal lock, the [observed JSON-number regression](reports/validation/regression.md), observation leakage checks, step/call/time limits, failed calls/fallbacks, observation-only input, cost accounting and the Vertex request/response format (mocked). Direct-state GDScript fixtures test rules and are not counted as player victories.

Local Godot import, startup, scroll and opened-arena rendering checks passed. The game now uses a direct extraction of the original `dangers.tscn`. All 55 retained scene blocks match the source exactly apart from trailing blank lines between blocks (which Godot rewrites on save), and the 27 copied artwork/font files match byte-for-byte; [direct extraction evidence](reports/provenance/direct-extraction.json) and [source patch](reports/provenance/extraction.patch) document that boundary. The original HUD, papyrus, captions, avatar, camera and arena animations are retained, while unused encounter nodes and movement/combat code are removed. The packaged course workflow has now run successfully on GitHub, linked above. Add the eventual upstream course PR and refresh evidence for the final submitted version.

## Limitations — student to revise after playtests

The selected prompt has one full normal-speed spell32 development trial on seed 30 (7/14, loss), plus the other conditions in the linked combat report. These are development evidence, not a ranking across situations. Older narrow-arena trials are historical and not directly comparable. The step-cap and replay fixes change the build hash; no live trials on that revised build are claimed. The required held-out experiment (six episodes each for the baseline and the model at history 0 and 2) has not been run. A three-case small classroom sample cannot support statistical certainty. Structured positions simplify perception; inference is paused, and each decision advances 0.1 simulated seconds. Human play retains the original scroll and real-time controls. Agent evaluation wraps the same original scene, skips its opening presentation and advances the original simulation in fixed 1/60-second ticks. It uses the project's 1280×720 viewport, and human play keeps the same 16:9 view at any window shape (the aspect ratio is locked), so humans and agents see the same arena. No replacement arena or HUD is used. No learning or improvement through repeated play is claimed. Full independent review, peer feedback and the required viewable recording remain pending. Two separate uses of crocodile-evaluation are now documented in [skill-session evidence](reports/sessions/skill-sessions.md); the linked exports also preserve implementation and partial scope-review evidence. The later alignment experiment is recorded separately in [its report](reports/experiments/y-alignment-experiment.md). CREDITS.md and reports/provenance/lepsius-provenance.json document the Lepsius digital edition and its supplier. The edition was published in 1842 and is in the public domain; faithful scans create no new copyright. The HUD font is "Old Fax" by George Blackwell, under CC BY 4.0. The existing PNGs' precise PDF-to-export crop history is not recorded. The baseline has not been retuned since the arena fix; it now wins all three development cases. A baseline that strong may leave little room for the model to do better on held-out cases. The selected prompt’s spell32 loss and the baseline’s development wins do not establish general performance across held-out cases.

The student must write their own interpretation of model failures/history, design decisions and actual peer observations. If partner notes have not arrived by November 6, state that and link the notes you gave.

## Review fixes — November 4

The step budget now caps long look actions, and replay restores complete reset settings. These adapter fixes do not change the selected prompt or observation schema. Historical live traces retain their original hashes and results; no paid reruns or held-out evaluations were performed for these fixes. New summaries report actual policy history capacity, derived-motion availability and optional event-memory capacity. After these fixes, `python -m unittest discover -s tests -v` passed all 29 tests in 29.262 seconds outside the sandbox; the added regressions cover the capped look, experimental/legacy reset replay, and baseline history metadata.
