# Crocodiles: spells 31 and 32

A complete two-encounter excerpt of [Totenbuch](https://github.com/anonymousanemone/totenbuch-game), my original Godot game. **Design: original game. Starting point: my own existing codebase.** Align the spear, face approaching crocodiles, and reserve heka for red opponents.

## Scope

Spell 31 is a one-sided tutorial followed by mixed-color waves; spell 32 is a two-sided fight. Turn back every crocodile to win an encounter; complete both to finish the excerpt. Three bites, heka used against an ordinary crocodile, or an escaping crocodile stealing the heka word can end an encounter. The tutorial protects the initial lesson from bites.

The original `godot/scenes/dangers.tscn`, papyrus, HUD, camera, artwork and arena animations are retained. Other encounters and their actors/code are removed; walking is bounded to these two vignettes. The original full strip bitmap remains to preserve coordinates and captions. The menu/continuation returns to this excerpt's intro. [Extraction hashes and patches](reports/provenance/) make inherited work inspectable.

Humans, baseline, model and replay use the same authoritative Godot combat. Automated episodes skip the arena-opening presentation and pause during inference. The suite was declared October 26 before tuning; its held-out seeds have now been evaluated and are consumed. See [EVALUATION.md](EVALUATION.md) for results and limitations. Update the Week 3 scope thread if this differs from the original commitment.

## Setup and play

All commands in this README run from **`midterms/anonymousanemone/`**. Requires Python 3.10+ (standard library only) and Godot **4.7.2**. Local play, baseline and tests need no API credentials.

On macOS:

```bash
export GODOT=/Applications/Godot.app/Contents/MacOS/Godot
"$GODOT" --headless --path godot --editor --import --quit
"$GODOT" --path godot
```

On other platforms, set `GODOT` to the executable or put `godot` on PATH. In the editor, open `godot/project.godot` and `scenes/dangers.tscn`.

Click **Begin**, walk with arrows or by clicking the papyrus, then click crocodiles to enter an encounter. In combat:

| Control | Action |
|---|---|
| Up/Down or W/S | Align vertically |
| Left/Right or A/D | Turn in spell 32 |
| Space | Thrust |
| Shift with thrust | Heka: required for red crocodiles, fatal against ordinary ones |
| Escape | Leave the encounter |

The HUD provides restart. Click the glowing heka word to read its rule. The core loop is to identify the next threat, align and face it, choose the matching attack, then time the thrust at its snout.

## Tests and evaluation

```bash
python -m unittest discover -s tests -v
python -m players.run --policy baseline --split development
```

The runner saves configurations, summaries and JSONL traces under `playtrace/`. [The frozen comparison](reports/held-out-final.md) completed 18 episodes: baseline 6/6 wins, model history=0 0/6, history=2 2/6. [Recorded GitHub CI](https://github.com/columbia-university-ai-games/game-dev-f26/actions/runs/41857753499) passed 29 tests on `ae74a5d`; it does not cover newer local edits.

### Live model setup

The adapter uses Vertex AI with Gemini 3.5 Flash-Lite. Authenticate with `gcloud auth application-default login` and configure a private, Git-ignored `.env`:

```text
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GOOGLE_CLOUD_LOCATION=global
CROC_MODEL=gemini-3.5-flash-lite
CROC_MAX_COST_USD=10
CROC_INPUT_PRICE=0.30
CROC_OUTPUT_PRICE=2.50
CROC_PRICE_DATE=2026-11-03
CROC_PRICE_SOURCE=https://cloud.google.com/model-garden/pricing
```

These are the saved evaluation prices, not a fresh price check. Exported environment values override `.env`. Credentials come from Google Application Default Credentials or `GOOGLE_APPLICATION_CREDENTIALS`; never commit them.

With provider/model and spending authorized, run a matched development comparison:

```bash
python -m players.checkpoint
```

This runs baseline and model on spell32 seed 30 and writes [the checkpoint comparison](reports/session7-comparison.md). `--case spell31` selects the tutorial. For a short transport pilot:

```bash
python -m players.run --policy model --split development --case spell31 --max-calls 50
```

A 50-call pilot may stop before a game outcome. Defaults in `suite.json` are 1,200 steps/calls, 30 seconds per call and 1,800 active wall seconds per episode. Failed calls count; neutral fallbacks are labeled and no automatic retries occur. Conservative reservations include failed calls and the full output cap. Budgets reset between invocations, so account for prior spending. Provider billing determines actual charges. Do not rerun consumed held-out seeds as fresh validation or use them for tuning.

## Machine interface and information boundary

`players.engine.Engine` calls `godot/scripts/server.gd`, wrapping the original scene through `episode.gd`. Game code validates actions and computes outcomes; the player has no repository or evaluator tools.

| Operation | Arguments | Result |
|---|---|---|
| `reset` | `seed`, `case` | Initial observation |
| `observe` | `player_id=0` | Visible observation |
| `legal_actions` | `player_id=0` | Permitted controls, including tactical mistakes |
| `step` | `player_id=0`, `action` | Validation, observation, outcome |
| `outcome` | none | Ongoing/terminal, reason, score, counts |

Only player 0 exists; reset first. Actions have `move` and `face` in -1/0/1, boolean `thrust` and `heka`, and optional boolean `look`. Spell31 requires `face: 0`. Ordinary and invalid actions advance up to six 1/60-second ticks (0.1 seconds); invalid controls are neutral. `look` reads the heka word, retains its message in `notes`, and idles for up to 60 ticks/ten steps, capped by the remaining episode budget. The one-second reading time is an assumption. Cooldown thrusts are legal but ineffective. Simulation stops at an encounter ending. Headless and human views use the same 16:9 arena.

Observations expose visible snout positions, directions, colors and dimensions; offsets from the spear tip; side; motion-derived `seconds_to_bearer`; player pose, spear geometry, health, progress, feedback, time and read notes. They exclude RNG, spawn schedules, hidden velocities and collision queries. Coordinates simplify screen perception.

The baseline retains up to ten observations and waits 0.4 seconds before reacting to a newly visible crocodile. Model history=0/2 controls explicit prior snapshots; both settings still receive derived motion and persistent notes. Both policies know the heka rule; the final tuned prompt teaches it. Optional event memory, speed/lives/count overrides and `--reach-flag` are development variants, excluded from standard evaluation. The reach flag uses the exact engine strike test and is privileged assistance. Reset defaults are speed=1, lives=3 and tuned counts.

## Rule/source map

`design` labels identify your original gameplay rules and midterm-specific choices. `code` labels provide implementation evidence for rules extracted from your existing game. A combined label means an original design choice with a code locator; it does not imply that the mechanic was reconstructed from another game. Historical plates establish visual subject matter, not combat rules. No unverified historical game mechanics are asserted.

| Rule or state | Label | Evidence / specification |
|---|---|---|
| Crocodiles, bearer, heka glyphs and captions of spells 31/32 | manual (visual reference) | Lepsius, *Das Todtenbuch der Ägypter* (1842), plate XVI; [digitized volume](https://archiv.ub.uni-heidelberg.de/propylaeumdok/467/1/lepsius_todtenbuch.pdf); see [credits below](#credits-and-reuse) |
| Spell 31 tutorial, waves, red-order choices; spell 32 two-sided mixed waves; counts, speeds, ramp, spacing | design + code | `godot/scripts/dangers/danger_encounters.gd`, original e31/e32 dictionaries |
| Movement speed, lane spacing, snout geometry, silhouette strike and grace distance | design + code | `godot/scripts/dangers/crocodiles.gd`, constants, `_move_bearer`, `_croc_head`, `_solid_of`, `_croc_strike` |
| A crocodile may start (or, once turned back, crawl again) only if its arrival at the bearer is at least max(half its body ÷ its speed, the wave's `min_gap`) seconds from every other crawling crocodile's, whatever the height or side; returning crocodiles wait until clear. Spell 32 base speed is 175 plate px/s (262.5 world px/s at scale 1.5), with a 1% ramp and `min_gap` 0.9 s; spell 31's waves run at 190 and 210 plate px/s. | design + code | Tuned in Totenbuch at commit `0d5a340`; `crocodiles.gd`, `_croc_clear` and `_croc_return`; `danger_encounters.gd`, e31/e32. Deterministic fixtures in `spacing_checks.gd`. |
| Plain/heka color match; heka on ordinary foe loses; red foe resists plain strike | design + code | Same file, `_croc_strike`, `_croc_takes_word` |
| Three health; bites, escape/word theft; tutorial bite grace | design + code | Same file, `_croc_bites`, `_crocs`, `_croc_dies` |
| Last drawn crocodile waits until others are gone; waves complete only when all are turned | design + code | Same file, `_croc_launch`, `_croc_break`, `_croc_next_wave` |
| Thrust timing 0.07+0.18 seconds, health 3, scale 1.5 | design + code | Original shared Dangers constants in `godot/scripts/dangers/dangers.gd` |
| Original scroll/arena presentation and editor placement; removal of unused encounters; standalone completion | design | `godot/scenes/dangers.tscn`; original `_arena_setup`, `_croc_open`, `_place_frame`; excerpt scope above |
| Episode seed owns every lane shuffle | design | `scripts/dangers/crocodiles.gd`, `_crocs_start`; fixes the original unseeded `Array.shuffle` |
| Initial health, pose, tutorial state and low-start situation | design + code | `scripts/episode.gd`, `reset`; `suite.json`; low-start changes only initial y |
| Control vocabulary, validation, neutral invalid action, cooldown behavior | design | `scripts/episode.gd`, `legal_actions`, `step`; original `_croc_thrust` |
| Fixed ticks, steps/calls/timeouts, terminal lock, no automatic retry; look advances only the remaining step budget | design | `scripts/episode.gd`, `step`, `outcome`; `players/run.py`, `episode`; `suite.json` |
| Score is number of crocodiles turned back; victory is whole encounter completed | design + code | Original `_won_if`; `scripts/episode.gd`, `outcome`; inherited wave completion |
| Observation fields, conservative visibility and no hidden schedules | design | `scripts/episode.gd`, `observe`; tests in `tests/test_game.py` |
| Heuristic baseline (up to ten observations) and model history=0/2 comparison; both model conditions include derived visible motion and persistent read notes | design | `players/baseline.py`, `players/model.py`, `suite.json` |
| JSON numeric controls were incorrectly rejected before the fix | observed | `reports/validation/regression.md`; `test_json_numeric_regression` |

## Recording and replay

**Required 3–5 minute demonstration URL: pending.** It must show agent play without manual move selection and be linked from the PR too.

Native **Record session**, beside Begin, saves a human JSONL and matching local build archive under `playtrace/`. Stop in the top bar or close the game to finish; Escape only leaves combat. Web exports disable human recording.

```bash
python -m players.replay --latest-human
python -m players.replay --latest-human --verify
python -m players.replay playtrace/PATH/TO/EPISODE.jsonl
```

With no path, replay selects the latest completed agent trace. `--resolution 1600x900` sets the window size; `--verify` checks headlessly. Space pauses, Right steps, 1/2/3 change speed, Escape exits. Replay checks saved gameplay results; it is not a screen recording. Keep local build archives to replay changed game versions.

For the optional local browser console, install matching Godot Web export templates, then run:

```bash
python -m web_console.build
python -m web_console.server
```

Open `http://127.0.0.1:8765`. The console runs both development spells with a shared $5 reservation cap after confirmation, or rehearses with the baseline, then offers verified replay. Its Python backend stays local; it is not a static web upload. Rebuild after game-source changes. Browser playback remains unverified in the recorded implementation checks.

## Credits and reuse

Code and scenes come from [Totenbuch](https://github.com/anonymousanemone/totenbuch-game), my original game. This midterm project extracts spells 31–32 from the dangers scene and adds agent play, evaluation and replay tooling.

Historical artwork: Carl Richard Lepsius, *Das Todtenbuch der Ägypter* (1842), plate XVI, spells 31–32. Public-domain edition, cropped and adapted in Totenbuch. [Digital edition](https://doi.org/10.11588/propylaeumdok.00000467) supplied by Dr. Marcus Müller, Totenbuch-Projekt, University of Bonn; hosted by Universitätsbibliothek Heidelberg / Propylaeum-DOK.

Font: [Old Fax](https://georgeblackwell.itch.io/old-fax) by George Blackwell, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), unmodified.

HUD borders and pixel icons were created using Claude Code. All other artwork derives from the papyrus scan cited above, including the spear-bearers, which were animated using Claude Code. [Extraction patches](reports/provenance/) show the changes from the original game.

## Submission evidence

- [Evaluation](EVALUATION.md), [final comparison](reports/held-out-final.md), [report index](reports/README.md)
- [Agent-team log](AGENT-TEAM.md), [independent review](review.md), [peer notes](PEER-NOTES.md)
- [Agent configuration](agent-config.json), [evaluation skill](skills/crocodile-evaluation/SKILL.md), [experiment skill](skills/make-experiment/SKILL.md)
- [Skill invocation index](reports/sessions/skill-sessions.md), [implementation exports](reports/sessions/codex-implementation-sessions.md), [review/experiment export](reports/sessions/codex-review-and-experiment-session.md), [combat-tuning export](reports/sessions/codex-combat-tuning-session.md)

Peer observations, the student-authored team narrative and the recording remain pending. Submit the course PR URL on CourseWorks by November 7, 11:59 p.m. Complete source and evidence belong in this folder, with the dedicated workflow at `.github/workflows/midterm-anonymousanemone.yml` in the repository root.
