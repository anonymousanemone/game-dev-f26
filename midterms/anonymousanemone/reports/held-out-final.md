# Frozen held-out evaluation — 2026-11-04

## Plan recorded before execution

Run the declared suite once per configuration: baseline, frozen combined-prompt
Vertex gemini-3.5-flash-lite with history=0, and the same model with history=2.
Spell31 seeds 101/102; spell32 seeds 201/202; spell32_low seeds 301/302.
18 held-out episodes total (6 baseline, 12 paid model). No tuning, selection or
paid retries using held-out results. Primary measures: wins and turn-backs;
retain reasons, steps, illegal actions, failures, usage/cost and raw evidence.

User authorized $20 total and requested a decision before increasing it. One
shared conservative reservation ledger across all paid episodes, cap $20, pause
before any call that reaches $16. The approval file gate preserves the active
engine and excludes approval waiting from episode wall time. Only an explicit
user decision can authorize creating that file. No automatic budget increases.
1200 calls and 1800 active wall seconds per episode; 30 seconds/call. Limit
outcomes are incomplete, not defeats. Dated configured token prices saved.

Normal speed, six-frame actions, 3 lives, standard crocodile counts, memory off,
reach flag off. Same visible observation schema. Baseline retains up to ten
observations for its 0.4-second reaction delay;
model receives exactly 0 or 2 prior observations. Both know red/plain heka rules:
the final tuned combined prompt now supplies that knowledge explicitly. Neither
receives RNG, schedules, hidden velocities or engine handles. Godot is authoritative.

Freeze exact prompt, player sources, suite and game hashes before execution;
verify before every episode/model call. Save configuration, Godot version,
per-action traces, errors, fallbacks, response IDs, usage and summaries. Tests
and baseline development evidence are separate checks, not held-out model results.
Independent review remains independently tracked; this run does not approve a gate.

Command: `python -B -m players.held_out_evaluation` from the midterm folder.
Model/default settings and suite are unchanged by the evaluation runner.

## Results

Pending execution. No held-out performance claimed yet.
