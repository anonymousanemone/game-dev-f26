# Full-episode combat prompt × speed comparison — 2026-11-04

## Plan before execution

Follow-up to the truncated combat-speed experiment: four fresh Spell32 episodes,
one per current/combined prompt × 1.0/0.75 crocodile speed, matched development
seed 30. Prediction: combined instructions and slower speed increase turn-backs
and completion success; equal/lower scores contradict directional improvement.
Primary measures: terminal outcome/reason and turn-backs out of 14. Alignment,
health, thrusts, provider errors and usage are diagnostics. One stochastic trial
per cell cannot establish general performance or isolate individual instructions.

User authorized $10 total for these four trials. Vertex gemini-3.5-flash-lite,
$2.50 conservative reservation per episode, 1200 calls, 30 seconds/call,
1800 wall seconds/episode. No paid retries or favorable-result selection. A run
that reaches a limit is incomplete, not a loss. Memory off, history 2, reach flag
off, 3 lives, normal crocodile count, 1024 output cap, six-frame actions. Existing
configured dated prices are saved per run. No held-out seeds or suite changes.

Exact current PROMPT is control, current PROMPT + COMBAT is intervention; texts
and hashes saved. Existing speed reset wrapper changes no observation fields or
rules and exposes no hidden state. Same authoritative Godot scene. Order:
current/1.0, combined/1.0, current/0.75, combined/0.75. Fixed order/provider
stochasticity are limitations. This is a fresh comparison, not continuation of
partial traces; historical results are context only. Source/build hashes,
configuration, raw traces and summaries saved uniquely. Preserve failures and
neutral fallbacks. Apply make-experiment and crocodile-evaluation skills.

Command: `python -B -m players.combat_experiment --run --full --total-budget 10`
Offline analysis: `python -B -m players.combat_analysis playtrace/RUN-DIRECTORY`.

## Results

Pending live execution.
