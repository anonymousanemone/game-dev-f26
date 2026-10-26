# Session 7 readiness — October 26, 2026

Audited against the locally supplied **Midterm: build a game and an agent that
plays it** assignment HTML. The downloaded CourseWorks HTML is private reference
material and is excluded from packaging; it is not submitted as project source.

| Today's requirement | Evidence / status |
|---|---|
| Engine behind five operations | Implemented: `players.engine.Engine` calls the original Godot scene through reset, observe, legal_actions, step and outcome. Deterministic tests exercise these operations. |
| Baseline completes an episode | Verified on development seed 30: spell31 won in 249 actions; spell32 lost in 64; spell32_low lost in 37. [Current run](../playtrace/20261026T184527216889Z-baseline-h2-development/summary.json). |
| Live model completes an episode with a trace | **Pending funded API key.** No live calls have been made. The student chose the cheapest model and a $10 ceiling. The private `.env` has a blank key field and GPT-6 Luna settings. |
| First baseline/model comparison | Baseline rows are available; [live comparison remains pending](session7-comparison.md). `python -m players.checkpoint` runs a matched development pair and replaces that report with actual results. |
| GitHub CI green on deterministic checks | **Passed: 14 tests** in the dedicated [midterm workflow](https://github.com/anonymousanemone/game-dev-f26/actions/runs/40396786117), commit `88c9a6d09d3b44512490e4238754b4088977a157`, on the course fork's `anonymousanemone/midterm` branch. The workflow changes only the permitted project folder and one workflow file. |
| Demo / peer critique | Game launch, human trace recording and action-file replay are documented. Actual classmate observations have not been supplied. |

## In-class commands

From `midterm-crocodiles/` locally, or `midterms/anonymousanemone/` in the course
checkout, import and launch using README.md. For a human combat attempt with
automatic recording into `./playtrace/`:

```bash
"$GODOT" --path godot --script res://scripts/human_trace.gd -- --case=spell31
python -m players.replay --latest-human
python -m players.replay --latest-human --verify
```

After adding the funded key privately to `.env`:

```bash
python -m players.checkpoint
```

That command defaults to spell32/seed30 for a short real combat ending. Baseline
and model use the same case, seed, engine, observations and legal actions. It
retains API failures, invalid choices, limits, tokens and dated estimated cost.
An episode without valid model-selected actions and a game win/loss is explicitly
marked insufficient by the generated comparison report.

## Later requirements remain separate

The checkpoint branch is [published on the course fork](https://github.com/anonymousanemone/game-dev-f26/tree/anonymousanemone/midterm/midterms/anonymousanemone).
The sibling checkout's existing Get Out branch was left untouched. A clean
temporary checkout was used to package, import, test and push the midterm branch.
The upstream course PR is not open yet. Its existing minigame boundary checker
protects every `.github/` path, conflicting with the midterm's explicitly required
workflow file. Instructor-owned tooling has not been changed; that upstream
boundary needs resolution before claiming that the eventual course PR is green.

The HTML schedules the partner playtest during the week of November 2, notes by
November 6, the completed course PR URL on CourseWorks by **November 7 at 11:59
p.m.**, and three assigned recording critiques before class November 16.
Held-out comparisons, the viewable 3–5 minute recording, independent read-only
review, two separately evidenced skill sessions, the implementation session link,
source/font reuse verification, and the student's own team log and reflection
remain required before final hand-in. They are not fabricated as completed.

The assignment identifies a changed scope as requiring a Week 3 thread update.
The student must check whether their current two-encounter scope differs from
their original post. No external course discussion has been posted by this agent.
