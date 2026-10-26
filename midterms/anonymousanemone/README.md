# Crocodiles: spells 31 and 32

A self-contained midterm excerpt of your original game, [Totenbuch](https://github.com/anonymousanemone/totenbuch-game): survive the crocodiles, align the spear, and reserve heka for red opponents. Design choice: **original game**. Implementation starting point: **your own existing codebase**. This midterm extracts two complete encounters from that original game and uses historical artwork as its visual source.

## Scope

[Game rules, core loop and interfaces](GAME.md) provides a short submission-ready description based on the implemented source. Interface screenshots are pending.

For the October 26 checkpoint, see [current readiness and remaining blockers](reports/session7-readiness.md). A live model episode still needs the funded API key; passing local tests is reported separately from GitHub CI.

Two complete encounters: spell 31's one-sided tutorial and mixed-color waves, and spell 32's two-sided fight. Each can be won or lost independently. Three declared evaluation situations use these two games; the third starts spell 32 at the lowest permitted vertical position. Included: existing crocodile combat, cropped artwork, human play, authoritative five-operation interface, baseline, live model adapter, deterministic tests and trace playback.

The game is a direct extraction of `godot/scenes/dangers.tscn`. The retained nodes,
positions, textures, offsets, camera and papyrus are copied verbatim. Original
walking/click-to-enter interaction, HUD, Journal, Hint, spear animation, arena
opening/closing, health signs and defeat presentation are retained. The other
encounter groups, carried breath/life objects and their movement/combat code are
removed. Walking is bounded to the two crocodile vignettes. Completing both ends
this excerpt; the original HUD's menu/continuation returns to this excerpt's intro.
The original full strip bitmap is retained so source coordinates and caption art
remain unchanged; the other encounters have no active actors or code.

The earlier replacement scenes and resources have been removed. Historical runs
from those discarded implementations are not validation of this extraction.

The suite was declared on 2026-10-26 before player tuning. Keep `suite.json` and update the Week 3 scope thread if this changes your prior commitment. No held-out cases have been run during setup.

## Setup and play

All commands below start in **this folder**, `midterms/<github-login>/` after packaging, or `Documents/School/gameAI/midterm-crocodiles/` in the standalone copy. Requires Python 3.10+ (standard library only) and [Godot 4.7.2](https://godotengine.org/download/archive/4.7.2-stable/). No Python packages or API key are needed for local play, baseline, or tests.

On macOS:

```bash
export GODOT=/Applications/Godot.app/Contents/MacOS/Godot
"$GODOT" --headless --path godot --editor --import --quit
"$GODOT" --path godot
```

On Linux/Windows, set `GODOT` to the executable or put `godot` on PATH. Open
`godot/project.godot`, then **`scenes/dangers.tscn`** in the editor.

Play exactly as in Dangers: click Begin, walk right to left with arrows or by
clicking the papyrus, and click crocodiles to enter their encounter. In combat,
up/down (or W/S) moves the spear-bearer; left/right (or A/D) turns him in spell 32.
Space thrusts; hold Shift for red crocodiles only. Escape leaves an encounter.
The original HUD provides restart, Journal and Hint. Three bites lose; using heka
against an ordinary crocodile loses, and an escaping crocodile can steal the word.
Turn back every crocodile to win an encounter; complete both to finish the excerpt.

## Classmate play: record a human trace

**Current evidence:** the saved development runs are scripted baseline runs. No live model run or model-player trace has been recorded. A human trace records a real person's inputs; it is separate from baseline and model evidence.

Use this mode for a classmate's recorded combat attempt. First complete the import command under **Setup and play**. From this project's root folder, run:

```bash
export GODOT=/Applications/Godot.app/Contents/MacOS/Godot
"$GODOT" --path godot --script res://scripts/human_trace.gd -- --case=spell31
```

On Linux/Windows, substitute your Godot executable. Each attempt automatically gets a unique filename in **./playtrace/**, printed in the terminal. No API key, Python package or model service is needed. An optional `--trace=/absolute/path/to/new.jsonl` overrides the destination; existing traces are never overwritten.

The window opens directly in spell 31 combat. Click the game window to give it keyboard focus. Use **Up/Down or W/S** to align the spear, **Space** to thrust, and **Shift + Space** against red crocodiles. Ordinary crocodiles require Space without Shift. Three bites lose, with introductory tutorial protection; using heka on an ordinary crocodile or letting a crocodile steal the active heka word also loses. Turn back all crocodiles to win.

For the next encounter, rerun the command with `--case=spell32` to record a new attempt. **Left/Right or A/D** turns the bearer in spell 32. `--case=spell32_low` selects its low starting position. All human recordings use development seed 30; do not use held-out seeds for classmate practice.

Recording samples held keys every 0.1 seconds and advances the actual Godot scene six fixed frames per action, matching the automated interface. Hold a key through a sampling interval; holding Space requests repeated thrusts as cooldown permits. This mode skips the intro, scroll navigation and arena opening. Use the regular launch above to audit those interfaces. During a recorded attempt, use the combat keys; close and relaunch to restart rather than using HUD navigation.

At victory, defeat or the 1200-action limit, recording stops and the window displays the reason. Close it afterward. **Escape** ends an unfinished attempt and closes the window. Closing the window also ends an attempt. Interrupted attempts are labeled as interrupted, not as wins or losses. Each row is flushed to disk; a crash can leave a partial trace without a summary.

The terminal prints the trace path. Keep **both** the `.jsonl` action file and the automatically created `.jsonl.build.zip` beside it in **./playtrace/**. This folder is permanent project storage; no copying out of `/tmp` is needed. The action files can be committed as evidence. Generated build archives are Git-ignored and stay local; back them up if needed.

The JSONL saves:

- Build file hashes, exact Godot version, UTC start time, fixed-step settings and the build archive's SHA-256.
- Starting case, development seed and initial observation.
- Every submitted action, sequential step/frame number, wall-clock elapsed microseconds, before/after observations, action validity and outcome. Observations include visible crocodile geometry/color/direction, bearer and spear geometry, thrust state, tutorial feedback, health and score.
- Keyboard press/release events received by the recorder, with timestamps and step numbers, plus application focus changes. These help distinguish the sampled actions from brief presses between samples.
- The final outcome or interruption reason. Rows are flushed after writing; a crash may leave an incomplete final row or no summary.

The ZIP preserves the Godot source and artwork used in the attempt, excluding import caches. It contains no API keys or installed dependencies. Keep the matching Godot release too: the archive does not contain the engine executable. HUD navigation is disabled during recording and replay so unrecorded restart, hint or Journal interactions cannot alter the attempt.

This is a deterministic **combat action trace**, not a video of the screen or a record of scroll navigation. It does not capture spoken questions, mouse movement, operating-system overlays or every rendered frame. For exact visual appearance and original wall-clock pacing, also make a screen recording outside this project. Write classmate questions separately in [PEER-NOTES.md](PEER-NOTES.md).

Replay the saved attempt with the same build:

```bash
python -m players.replay --latest-human
```

To replay a particular actions file instead, use `python -m players.replay playtrace/YOUR_FILENAME.jsonl`. The replay executor is a bot that follows that file exactly: it makes no new tactical choices. It reconstructs the combat by submitting those actions to the original Godot engine and verifying the results.

Replay checks the build hashes and Godot version before starting, then compares every replayed result with the recorded result. It stops on a mismatch rather than presenting an inaccurate continuation. Older traces without build metadata can only verify their recorded observations/results. An interrupted trace replays only the actions that were saved; a malformed row is rejected.

Replay controls: **Space** pauses/resumes; **Right arrow** advances one action and pauses; **1/2/3** selects 0.25×/1×/2× speed; **Escape** exits. The title shows the current step, simulation time, health, score and submitted action. Replay uses simulation timing; wall-clock timestamps remain in the JSONL for analysis of original timing.

To check the entire trace without watching:

```bash
python -m players.replay --latest-human --verify
```

Success prints `Verified all N recorded steps`; a mismatch exits unsuccessfully. This verifies exact recorded observations and outcomes at action boundaries on the matching engine/build. It is not a claim of pixel-identical rendering across computers.

If this project's files have changed, restore the archived build into a new folder outside the project, using the matching Godot version identified in the trace's first row. For example, with an unused destination folder:

```bash
unzip playtrace/REPLACE_WITH_PRINTED_FILENAME.jsonl.build.zip -d /tmp/crocodiles-restored-attempt1
"$GODOT" --headless --path /tmp/crocodiles-restored-attempt1/godot --editor --import --quit
"$GODOT" --path /tmp/crocodiles-restored-attempt1/godot --script res://scripts/replay.gd -- --replay="$PWD/playtrace/REPLACE_WITH_PRINTED_FILENAME.jsonl"
```

Label playback **human trace replay**, not a fresh playtest or model run.

For a README-only audit, give the classmate this README and let them follow setup and these commands without coaching. Note every question they need to ask; those questions identify instructions to clarify. For silent play, observe without directing their choices. No classmate playtest is claimed merely because recording mode exists.

## Editor/source layout

Use the original scene tree:

- `actors/spell31_crocs` and `actors/spell32_crocs`: the original selectable sprites,
  spear-bearers, overlays and heka signs, with unchanged transforms and metadata.
- `Papyrus`, `Strip`, `Avatar`, `Camera`, `Overlay`, `HUD` and `CaptionRegions`:
  retained original nodes. The original HUD and opening arena are built by the
  original shared scripts, as they are in Totenbuch; no replacement UI is used.
- `scripts/dangers/dangers.gd`: the original scene controller with unused
  encounter/inventory/movement paths removed.
- `scripts/dangers/crocodiles.gd`: the original combat, with seeded lane shuffling
  and a small input hook for the separate evaluation wrapper.
- `scripts/dangers/danger_encounters.gd`: only the original e31/e32 dictionaries.
- `assets/dangers/level.json`, `registry.json`, `puzzles.json` and
  `animation/spearers.json`: original source data limited to the retained encounters.

Runtime actor placement is read from the original scene transforms/metadata.
The original combat still animates and spawns copies as before. The independent
`episode.gd` adapter wraps this actual scene; it does not substitute another layout.
[Extraction evidence](reports/direct-extraction.json) records the original hashes
of all retained scene blocks and copied artwork/font files.

## Test and evaluate

```bash
python -m unittest discover -s tests -v
python -m players.run --policy baseline --split development
```

The second command writes configuration, JSONL action traces, local build archives and summaries under `playtrace/`. The preserved setup comparison is linked from [EVALUATION.md](EVALUATION.md).

Live trials are prepared but **have not been run**: the private API key is not yet configured. The current choice is `gpt-6-luna`, the lowest-priced current flagship text model on the [OpenAI pricing page](https://developers.openai.com/api/docs/pricing), checked October 26, 2026: $0.10 input and $0.50 output per million tokens at standard processing rates. The user authorized at most $10 for the checkpoint run. The adapter follows the [Responses API text generation documentation](https://developers.openai.com/api/docs/guides/text). It sends no tools, repository contents or hidden state. All model actions come from the model response.

### Set up the live player privately

1. Sign in to the [OpenAI API platform](https://platform.openai.com/), choose your project, and configure [API billing](https://platform.openai.com/settings/organization/billing/overview). ChatGPT subscription access does not fund this player's API calls.
2. Create a secret key on the [API keys page](https://platform.openai.com/api-keys); see the [official quickstart](https://developers.openai.com/api/docs/quickstart).
3. Open this project's `.env` locally and paste the key after `OPENAI_API_KEY=`. Do not paste it into chat, a recording, a report or a commit. A private `.env` has been created in the local working copy; on a fresh clone, run `cp .env.example .env` first. `.env` is Git-ignored and excluded from packaging.
4. From this project folder, run:

```bash
python -m players.checkpoint
```

The runner reads `.env` directly; no `source` command or Python dependency is required. This command runs the baseline and the live model on the same spell32/development-seed-30 episode, saves both under `./playtrace/`, and writes [the comparison report](reports/session7-comparison.md). Spell32 provides a short game episode that can end in a real win or loss; either outcome is valid evidence. The report states whether the model submitted valid actions and reached such an ending. Limits and provider failures remain visible and are never relabeled as successful gameplay. Use `--case spell31` to choose the tutorial encounter instead.

The `.env.example` records the model, dated prices and $10 maximum. A conservative reservation before each call covers the input byte bound plus message overhead and the full output-token cap. Reservations, including failed calls, count across every episode in one runner invocation; it stops before a call would exceed `--max-cost-usd`. This is intentionally more conservative than the reported usage-cost estimate. The cap resets for a new invocation: do not rerun paid experiments repeatedly without accounting for earlier spend. No automatic retries are made. Provider billing remains the source for actual charges.

Example command shape; replace the capitalized values before running:

```bash
python -m players.run --policy model --model MODEL_ID --split development --case spell31 --max-calls 50 --input-price INPUT_USD_PER_MILLION --output-price OUTPUT_USD_PER_MILLION --price-date YYYY-MM-DD --price-source PROVIDER_PRICING_URL
```

A 50-call pilot will usually hit its call limit before completing spell 31. Use it to inspect transport and cost, not to claim a win. Full episodes can require hundreds of calls. Choose a total spend budget before live execution. Defaults are declared in `suite.json`: 1200 steps/calls, 30 seconds per call and 1800 wall seconds per episode. A failed call counts and submits an explicitly labeled neutral fallback. Invalid actions consume one step and advance neutral simulation. No retries are silently substituted.

After freezing the prompt and heuristic, run the same six held-out case/seed episodes for the baseline and the model with both history settings. Use identical model/budget/price flags for the two model variants:

```bash
python -m players.run --policy baseline --split held_out
python -m players.run --policy model --model MODEL_ID --split held_out --history 0 --input-price INPUT_USD_PER_MILLION --output-price OUTPUT_USD_PER_MILLION --price-date YYYY-MM-DD --price-source PROVIDER_PRICING_URL
python -m players.run --policy model --model MODEL_ID --split held_out --history 2 --input-price INPUT_USD_PER_MILLION --output-price OUTPUT_USD_PER_MILLION --price-date YYYY-MM-DD --price-source PROVIDER_PRICING_URL
```

For visual playback, use the path to an actual episode trace:

```bash
"$GODOT" --path godot --script res://scripts/replay.gd -- --replay=/ABSOLUTE/PATH/TO/spell31-30.jsonl
```

This replays recorded actions with the same engine. Label it as replay in a recording; it is not a fresh live trial. No manual move selection is needed. See [RECORDING.md](RECORDING.md) for the recording plan; recording link is pending.

## Machine interface and information boundary

`players.engine.Engine` connects to `godot/scripts/server.gd`, which loads the extracted `scenes/dangers.tscn` and wraps it with `scripts/episode.gd`. The actual original scene owns state and enforces combat. There is no second simulator. Use `Engine.call` with these operations:

| Operation | Arguments | Result |
|---|---|---|
| `reset` | `seed`, `case` | Initial observation |
| `observe` | `player_id=0` | Player-visible observation |
| `legal_actions` | `player_id=0` | All permitted control combinations, including mistakes |
| `step` | `player_id=0`, `action` | Validation, visible observation, outcome |
| `outcome` | none | Ongoing/terminal, reason, score, counts |

Only player 0 exists. Reset before other stateful operations. Action: `{"move": -1|0|1, "face": -1|0|1, "thrust": boolean, "heka": boolean}`. Face must be 0 in spell 31. Thrust during cooldown is permitted but has no effect. The list never filters out a tactically wrong heka choice or chooses a target. The game runs six 1/60-second ticks per action, then freezes during inference. Human play retains the original real-time controls. The evaluation wrapper selects those controls at the declared fixed cadence and skips only the arena opening animation; it preserves original spawning/collision rules. Drawing frames and wall-clock model latency do not advance combat.

Observations include active visible snout positions/directions/colors/dimensions, player position/facing, spear geometry, health, progress, tutorial feedback and simulation time. They exclude RNG, future waves/colors, launch timers, internal velocities and collision-mask queries. Coordinates are a deliberate accessible representation of the visible screen, rather than raw pixels. Velocity is inferred by the baseline from two observations; the model can receive the same two. The baseline has no engine reference. The model receives serialized observation/history, instructions, and no executable tools. The evaluator, not the model, determines victory. Rules and static control meanings are disclosed equally.

## Rule/source map

`design` labels identify your original gameplay rules and midterm-specific choices. `code` labels provide implementation evidence for rules extracted from your existing game. A combined label means an original design choice with a code locator; it does not imply that the mechanic was reconstructed from another game. Historical plates establish visual subject matter, not combat rules. No unverified historical game mechanics are asserted.

| Rule or state | Label | Evidence / specification |
|---|---|---|
| Crocodiles, bearer, heka glyphs and captions of spells 31/32 | manual (visual reference) | Lepsius, *Das Todtenbuch der Ägypter* (1842), plate XVI; [digitized volume](https://archiv.ub.uni-heidelberg.de/propylaeumdok/467/1/lepsius_todtenbuch.pdf); see [CREDITS.md](CREDITS.md) |
| Spell 31 tutorial, waves, red-order choices; spell 32 two-sided mixed waves; counts, speeds, ramp, spacing | design + code | `godot/scripts/dangers/danger_encounters.gd`, original e31/e32 dictionaries |
| Movement speed, lane spacing, snout geometry, silhouette strike and grace distance | design + code | `godot/scripts/dangers/crocodiles.gd`, constants, `_move_bearer`, `_croc_head`, `_solid_of`, `_croc_strike` |
| Plain/heka color match; heka on ordinary foe loses; red foe resists plain strike | design + code | Same file, `_croc_strike`, `_croc_takes_word` |
| Three health; bites, escape/word theft; tutorial bite grace | design + code | Same file, `_croc_bites`, `_crocs`, `_croc_dies` |
| Last drawn crocodile waits until others are gone; waves complete only when all are turned | design + code | Same file, `_croc_launch`, `_croc_break`, `_croc_next_wave` |
| Thrust timing 0.07+0.18 seconds, health 3, scale 1.5 | design + code | Original shared Dangers constants in `godot/scripts/dangers/dangers.gd` |
| Original scroll/arena presentation and editor placement; removal of unused encounters; standalone completion | design | `godot/scenes/dangers.tscn`; original `_arena_setup`, `_croc_open`, `_place_frame`; excerpt scope above |
| Episode seed owns every lane shuffle | design | `scripts/dangers/crocodiles.gd`, `_crocs_start`; fixes the original unseeded `Array.shuffle` |
| Initial health, pose, tutorial state and low-start situation | design + code | `scripts/episode.gd`, `reset`; `suite.json`; low-start changes only initial y |
| Control vocabulary, validation, neutral invalid action, cooldown behavior | design | `scripts/episode.gd`, `legal_actions`, `step`; original `_croc_thrust` |
| Fixed ticks, steps/calls/timeouts, terminal lock, no automatic retry | design | `scripts/episode.gd`, `step`, `outcome`; `players/run.py`, `episode`; `suite.json` |
| Score is number of crocodiles turned back; victory is whole encounter completed | design + code | Original `_won_if`; `scripts/episode.gd`, `outcome`; inherited wave completion |
| Observation fields, conservative visibility and no hidden schedules | design | `scripts/episode.gd`, `observe`; tests in `tests/test_game.py` |
| Heuristic baseline and bounded-history/observation-only comparison | design | `players/baseline.py`, `players/model.py`, `suite.json` |
| JSON numeric controls were incorrectly rejected before the fix | observed | `reports/regression.md`; `test_json_numeric_regression` |

### State, actions and outcomes at a glance

| Required element | Implemented meaning | Source evidence |
|---|---|---|
| Key state | Bearer position/facing, health, spear thrust, visible crocodile position/color/direction, tutorial and encounter progress | [Observation fields](godot/scripts/episode.gd), `observe`; [combat updates](godot/scripts/dangers/crocodiles.gd), `_crocs` |
| Legal actions | Up/neutral/down, left/unchanged/right facing in spell 32, thrust on/off, heka on/off; spell 31 requires unchanged facing. Legal choices include tactical mistakes. | [Action enumeration and validation](godot/scripts/episode.gd), `legal_actions` and `step` |
| Outcomes | Win after all crocodiles are turned back; lose through health depletion or word theft; stop at the action limit | [Terminal checks and outcome fields](godot/scripts/episode.gd), `step` and `outcome`; [bite and theft rules](godot/scripts/dangers/crocodiles.gd), `_croc_bites` and `_croc_takes_word` |

Unresolved usability question: can a new player distinguish the red heka cue and understand that using heka on an ordinary crocodile is fatal without coaching? This needs a real silent playtest; source inspection cannot answer it.

### Acceptance trace: opening the spell 31 lesson

This is a short worked example of **expected** behavior for later checks, not a recorded human/model trial. Use development seed 30 and the fixed-step interface. Its outcome is an ongoing lesson with the first crocodile approaching; it does not claim an encounter victory.

| Step | Operation / legal action | Expected state change and outcome |
|---|---|---|
| 0 | `reset(seed=30, case="spell31")` | Health is 3, score is 0, tutorial is `thrust`, and outcome is `ongoing`. |
| 1 | `{"move":0,"face":0,"thrust":true,"heka":false}` | Action is valid. The practice thrust begins and advances the lesson to `first`, launching the first ordinary crocodile. Six frames pass; health remains 3, score remains 0, and the episode is ongoing. |
| 2 | `{"move":0,"face":0,"thrust":false,"heka":false}` | Action is valid. Another six frames pass. The initial thrust is still completing; the crocodile approaches. No hit or health loss is expected this early. |
| 3 | `{"move":0,"face":0,"thrust":false,"heka":false}` | Action is valid. Total simulated time is about 0.3 seconds; the 0.25-second thrust cycle has finished. Health is 3, score is 0, tutorial remains `first`, and outcome remains `ongoing`. |

Evidence: [reset, fixed ticks and observations](godot/scripts/episode.gd); [practice-thrust transition](godot/scripts/dangers/dangers.gd), `_croc_thrust`; [first launch and thrust completion](godot/scripts/dangers/crocodiles.gd), `_crocs`. A later acceptance example can cover a full win or loss using an actual saved trace.

## Evidence and hand-in

- [Evaluation and current results](EVALUATION.md)
- [Credits, reuse terms and extraction provenance](CREDITS.md), [source manifest](reports/source-manifest.json)
- [Agent-team log prompts; student authorship still required](AGENT-TEAM.md)
- [Reusable evaluation skill](skills/crocodile-evaluation/SKILL.md), [session evidence](reports/skill-sessions.md)
- [Independent review task](review.md), [peer playtest notes](PEER-NOTES.md)
- [Recording plan and link field](RECORDING.md), [remaining checklist](MIDTERM-CHECKLIST.md)

Stage the course-repository files from this folder (login inferred from the source repository owner; change it if your course login differs):

```bash
python submission/package.py --login anonymousanemone --course-repo /PATH/TO/game-dev-f26
```

This creates only `midterms/anonymousanemone/` and `.github/workflows/midterm-anonymousanemone.yml`. It refuses to overwrite an existing submission or workflow, excludes caches, and never commits/pushes. Run setup/tests from the copied folder. The workflow imports Godot and runs deterministic checks without API secrets; its GitHub execution remains pending until the course PR exists. Then create a branch such as `anonymousanemone/midterm`, review the changes, push and open one PR targeting the course repository's `main`. Use [submission/PR.md](submission/PR.md) for the description. Submit that PR URL on CourseWorks by November 7, 11:59 p.m. The complete source belongs in the PR, not only a link to this standalone repository.
