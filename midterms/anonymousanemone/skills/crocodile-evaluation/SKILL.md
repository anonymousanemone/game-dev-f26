---
name: crocodile-evaluation
description: Validate and report this project's Godot crocodile episodes and observation boundaries without contaminating held-out evaluation cases.
---

Use the Godot engine through `players.engine.Engine`; do not implement a second simulator.
Read `suite.json` before selecting cases. Development uses its development seeds only;
held-out seeds are for final evaluation after tuning is frozen.

Check JSON transport as well as direct GDScript: Godot JSON numbers arrive as floats.
A legal action must remain accepted across that boundary, while booleans cannot stand
in for numeric movement. Invalid actions consume a step and advance neutral simulation.

Run `python -m unittest discover -s tests -v`. For baseline evidence run
`python -m players.run --policy baseline --split development` and retain losses.
For a live run use the model, budget, history variant and dated prices chosen by the user.
Count failed calls, identify neutral fallbacks, and report live and mocked evidence separately.

Before interpreting scores, inspect the observations and legal-action vocabulary for
spawn timers, future color schedules, RNG state, correct-target hints and hidden velocities.
Baseline and model must receive the same observations. Never report direct-state rule
fixtures as agent victories. Record game and suite hashes and link raw episode traces.

Report what was actually run. Independent review, two separate skill sessions, live
trials, peer observations and student-authored reflection need their own evidence.
