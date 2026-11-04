# Independent reviews and implementation responses

The original read-only review task is retained below. Actual separate-review findings and implementation responses follow; these do not approve a course gate or merge.

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

## Follow-up review — November 4, after evaluation and report cleanup

Reviewer: separate read-only Codex task `/root/rules_fix_review`. Reviewed the
working tree based on commit `aee02a6`, including the uncommitted reporting fix.
Game hash remains `f08e6aea82a27010f29b03c9073c5ca26e539fd5ac16813d374ef23d8f036bd5`.

Initial follow-up finding:

> [should fix] README.md:9/160/197, MIDTERM-CHECKLIST.md:30 and EVALUATION.md:1/155/175 still mark completed held-out work pending and suggest rerunning consumed seeds.

Response: replaced pending status with completed results, marked the held-out
seeds consumed, and removed instructions to repeat them as fresh validation.
All 41 final evidence files were already committed by the student at `aee02a6`.
A frame-reporting regression failed before the fix (2,376 versus 2,375 frames).
New logs use actual simulated time and separately record nominal frames;
historical evaluation artifacts and their original hashes remain unchanged.
The evaluated runner source can be recovered from `aee02a6`.

Reviewer’s final follow-up findings:

> No findings in the current uncommitted fixes.
>
> All 41 final evidence files are present byte-for-byte at aee02a6. Every evaluated player-source hash matches that commit. The sole current source-hash difference is the documented run.py logging correction. Actual frame reporting uses the encounter clock, which advances per simulation tick without resetting between waves. Completed held-out status is consistent across the changed readiness docs. git diff --check passes.
>
> Read-only review; no edits, commits, gameplay, paid calls, or independent test runs.

The implementation session owns the automated test result; the separate reviewer
owns the read-only findings above. Human acceptance, source permissions, student
authorship, peer experience, current CI and submission remain separate evidence.

Validation after the frame-reporting fix: all 29 deterministic tests passed in
35.751 seconds outside the sandbox. No paid or held-out episodes were run for
these fixes, and no commit was made by the assistant.
