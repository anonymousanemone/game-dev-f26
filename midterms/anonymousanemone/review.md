# Independent review — pending

This implementation session cannot independently review its own code. Use a fresh read-only Codex session (or another assistant), with no instruction to approve. Paste the following task and commit its actual findings here or link the PR review.

> Review the Crocodiles midterm in read-only mode. Do not edit files. You did not implement this code. Read AGENTS.md, README.md, suite.json and skills/crocodile-evaluation/SKILL.md; invoke the crocodile-evaluation skill by name. Assess the rule/source map against inherited combat, the five operations, hidden-state boundaries, action validation, seeded determinism, victory/loss, all budget/timeout paths, fallback reporting, baseline fairness and the generated course workflow's boundaries. Run the deterministic tests if permitted; use development cases only. Do not spend API funds or run held-out cases. Report concrete findings with severity and file/line evidence, tests run, what was checked, and remaining uncertainty. Finding no issues is acceptable when supported. Do not certify live trials, source permissions, human feedback or student authorship that you cannot inspect.

After review: identify reviewer/session and reviewed game hash, record findings verbatim or link them, document your response, and rerun checks after any fixes. Keep this separate from the implementation agent's self-checks.

## November 4 fix handoff — findings 1, 2, 4 and 5

Implementation response for a separate read-only reviewer; not self-approval.

- Rule (design): fixed-step episodes stop at 1,200 steps; a look consumes at most
  the remaining budget. Evidence: suite.json and README rule/source map, fixed
  ticks/limits row. `test_look_stops_at_remaining_step_budget` failed before the
  fix (1,205 instead of 1,200). It also checks invalid look near the boundary.
- Replay: new reset rows store speed/lives/count/reach settings; replay restores
  them. Legacy traces read metadata and adjacent configuration. A mocked-player
  development regression with .75 speed, five lives, twenty crocodiles and reach
  assistance failed before the fix at the initial observation. No live calls.
- Boundary: no new player observations or actions. Motion-derived
  seconds_to_bearer remains in both history conditions; explicit snapshots are
  the intervention. New baseline summaries report history capacity ten, and
  summaries identify derived motion and optional event-memory capacity.
- Documentation now distinguishes the final combat prompt from historical heka
  discovery trials and historical trial/cost subtotals from cumulative totals.
- Assumption retained: a full look represents one second of reading; only its
  remaining-budget behavior changes. Existing live artifacts are not rewritten.
  The frozen model source/prompt and suite remain unchanged; game hashes change
  with these adapter fixes. No paid or held-out runs were made.

Review engine/interface, replay, runner, experiment reset forwarding, tests,
README rule/source map, EVALUATION and agent-config diff. Record actual findings
and implementation response separately before merging.

### Independent fix review — `/root/rules_fix_review`, November 4

Separate read-only reviewer findings:

> [note] `midterms/anonymousanemone/README.md:225` and `AGENTS.md:17`: still state that every look counts ten steps. Qualify this as “up to ten steps, capped by the remaining episode budget” to agree with the engine and updated rule/source map.
>
> No functional findings in the requested fixes. Read-only review checked `episode.gd`, `replay.gd`, `players/run.py`, `players/combat_experiment.py`, all three changed test files, README rule/source map, EVALUATION, agent-config, evaluation skill, and review handoff.
>
> Confirmed `players/model.py` and `suite.json` have no working-tree changes. `git diff --check` passes. No paid calls, held-out runs, edits, or independent test executions performed; the parent owns the full test run.

Implementation response: corrected both prose locations to match the capped
look behavior. Full deterministic suite: 29 tests passed in 29.262 seconds.
The step-cap, reset-replay and metadata regressions failed before implementation
and passed afterward. Frozen prompt hash still matches agent-config.json.
This focused fix review does not replace the broader submission review or a
student/instructor gate decision. Concurrent held-out evaluation files from
another session were excluded from this fix task and left untouched.
