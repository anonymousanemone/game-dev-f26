---
name: make-experiment
description: Plan, implement, run, and report controlled development experiments for the Crocodiles midterm, including prompt, observation, memory, policy, and difficulty comparisons. Use for a new experiment or experiment report; creating a plan alone does not authorize paid trials.
---

# Make a Crocodiles experiment

Work within `midterms/anonymousanemone/`. Resolve project-relative paths below
from that folder. Read `AGENTS.md`, `suite.json`, and the relevant runner and
configuration before choosing settings. Use the existing authoritative Godot
scene through `players.engine.Engine`; do not build another simulator.

## Define the comparison before running

Write a dated plan in `reports/<experiment-name>.md`. State the question,
hypothesis, intervention, control, primary measure, cases/seeds, run count,
limits, and what result would contradict the hypothesis. Label predictions and
planned runs explicitly; leave results pending until raw evidence exists.

Prefer one changed factor per comparison. Match engine build, seed, starting
state, prompt, model, history, memory, observation fields, policy, and budgets
except for the declared intervention. If multiple factors must change, identify
the confound and limit the conclusion accordingly. A historical run can be a
control only after comparing its saved configuration and hashes; disclose any
mismatch instead of calling it matched.

Use development seeds from `suite.json`. Additional development seeds need a
separately declared experiment list that excludes every held-out seed. Do not
change the frozen suite to accommodate an exploratory experiment. Held-out
episodes belong to final evaluation after tuning is frozen, not experiment
pilots or selection of a preferred variant. Label changed lives, counts,
speeds, extra memory, and other variants as exploratory settings rather than
standard suite results.

## Preserve the information boundary

For every added input, explain its source and what information it conveys.
Positions or motion derived from visible observations differ from a flag using
the engine's exact strike/collision test. Do not silently give either player
RNG, spawn schedules, hidden velocities, collision-mask queries, correct-target
hints, or engine objects. A privileged diagnostic may be computed by the trusted
evaluator for analysis, but must stay out of policy inputs. If a requested input
conflicts with `AGENTS.md`, explain the conflict and propose a boundary-compliant
alternative before implementing it.

Build memory from the player's past observations and actions only. State its
capacity, reset behavior, and whether it replaces or supplements bounded history.
Document asymmetries such as the baseline knowing the heka rule while the model
must discover it. Identical observation schemas do not imply identical knowledge
or history access.

## Implement and verify only what the experiment needs

Reuse existing runner options where possible. Keep new variants opt-in and
record their actual values; preserve standard gameplay defaults. Do not rewrite
old traces or reports to make them match a new implementation.

If changing a rule, action, observation, or outcome, follow the repository's
`.claude/skills/rule-change/SKILL.md`: map the rule, demonstrate a failing test
first, then change the engine/interface and hand a summary to an independent
reviewer. The midterm's current rule/source map is in `README.md`; do not edit
the starter's map or engine for a midterm experiment. Preserve Godot's authority
and the fixed simulation cadence.

Use `skills/crocodile-evaluation/SKILL.md` for evaluation checks. After
engine/interface changes run, from the project folder:

```bash
python -m unittest discover -s tests -v
```

Check JSON action validation, boundary effects, and default behavior relevant to
the change. Test fixtures and mocked provider responses are verification, not
live policy episodes or evidence of human experience.

## Execute with bounded cost and reproducible evidence

Honor the user's existing authorization: a plan-only or offline request stays
that way. A live experiment needs an explicitly chosen provider/model,
configured credentials, dated token prices, and an authorized total spend.
Reuse choices already established in the session; ask only for missing required
choices. Check remaining authorization across invocations: the runner's cost
reservation resets each invocation. Define a finite run matrix and stop at its
run/call/time/cost limits; do not retry or expand paid trials to obtain a win.

Record exact commands, UTC dates, game and suite hashes, player-source and prompt
hashes, runtime model identifier, Godot version, actual history/memory settings,
and every experimental override. Keep model settings and artifact references in
`agent-config.json` when they become maintained project configuration; retain
per-run settings and runtime model identifiers in evaluation artifacts.

Use unique run directories under `playtrace/`. Link each reported result to its
saved configuration, raw action trace and summary (or raw sweep data when the
existing sweep runner produces aggregates). Do not claim replayability or
per-action evidence for runs that did not save it. Retain losses, invalid
actions, fallbacks, provider failures, interrupted runs, and limits. Count failed
calls and report token usage, estimated cost, reservations, and missing usage
separately. Never replace failed live trials with fixtures. Keep credentials,
caches and local build archives out of committed evidence; screenshots and
preview artifacts belong outside the project.

## Report observations separately from interpretation

Use this compact report outline, adapting measures to the question:

- **Question and prediction:** hypothesis and planned success/falsification measure.
- **Method:** control/intervention, settings, seeds, repetitions, commands,
  versions/hashes, budgets, and any deviation from the plan.
- **Results:** one row per run or clearly defined aggregate; outcome/reason,
  score/denominator, steps, calls, invalid actions/fallbacks, cost, and raw links.
- **Analysis:** measured behavior that bears on the question; label suspected
  mechanisms as hypotheses unless directly checked.
- **Limits and decision:** confounds, sample size, missing evidence, and what the
  experiment supports or leaves unresolved. Leave the student's design decision
  and personal reflection to the student.

Do not infer learning from higher totals in a longer/easier episode alone. Define
the learning measure and account for changing speed, opportunity counts, and
episode survival. A single matched seed gives a case study, not a general player
ranking; correlation in a trace does not establish causation. Report null and
negative findings without tuning the conclusion to the desired result.

For report examples, consult only those relevant to the experiment:
`reports/experiments/learning-experiment.md` (memory/lives/counts), `reports/experiments/speed-sweep.md`
(difficulty and reaction delay), and `reports/experiments/reach-flag-experiment.md`
(observation assistance). They are historical evidence, not templates to copy
uncritically: flag confounds, boundary problems, and unsupported causal claims.

Creating this skill is not proof it has been applied. Record actual invocation
and resulting artifacts when used; do not mark independent review, separate skill
sessions, student authorship, or course gates complete on the experiment's behalf.
