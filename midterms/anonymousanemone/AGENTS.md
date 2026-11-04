# Crocodiles midterm

## Remote changes

Scope is spells 31 and 32 only. Reuse `godot/scripts/dangers/crocodiles.gd`; the Godot
engine is authoritative for humans, baseline, model and replay. No parallel MDP or
Python reimplementation. Never copy source MDPs or unrelated Totenbuch assets.

Players receive observations only. Keep RNG, spawn schedules, hidden velocities,
collision-mask queries and engine objects out of standard player inputs.
The existing opt-in `--reach-flag` uses the exact engine strike/silhouette test:
it is privileged assistance, not an ordinary visible-state observation. Keep it
off in standard suite runs; label its historical results separately. Do not
silently promote privileged inputs into the standard interface.

Automated episodes use 1/60 s fixed ticks: ordinary and invalid actions advance
up to six frames; `look` idles for up to 60 frames and counts as up to ten steps, capped by the remaining episode budget.
Simulation stops early on an encounter ending. Native human sessions retain
actual frame timing and original input semantics, not the fixed action cadence.

Read `suite.json` before changes and leave held-out seeds out of tuning. Standard
runs use speed scale 1, three lives, tuned crocodile counts, no extra event memory
and no reach flag; compare the declared model history settings 0 and 2. Label
speed/lives/count/memory overrides and prompt pilots as development experiments;
do not mix their results into standard suite scores. Freeze the prompt, policy
and settings before final held-out evaluation.

Paths here are relative to `midterms/anonymousanemone/`; run commands from that
folder. The midterm interface is `godot/scripts/episode.gd`, reached through
`players/engine.py`; the rule/source map is in `README.md`. For rule, action,
observation or outcome changes, follow the repository-root
`.claude/skills/rule-change/SKILL.md` using those midterm paths: map the change,
demonstrate a failing test first, implement it, and hand the summary to an
independent reviewer using `review.md`. Do not modify the starter engine/map for
a midterm change or approve your own work.
Run `python -m unittest discover -s tests -v` after engine/interface changes.
Use `$crocodile-evaluation` at `skills/crocodile-evaluation/SKILL.md` for evaluation.
Use `$make-experiment` at `skills/make-experiment/SKILL.md` for experiment plans,
matched comparisons and reports. Live experiments require the user's provider,
model, dated prices and spending authorization plus configured credentials;
carry remaining allowance across invocations, including failed-call reservations.
Creating a skill is not evidence of using it; record actual sessions/artifacts in
`reports/sessions/skill-sessions.md` and references in `agent-config.json`.
Do not fabricate live trials, independent review, peer notes, skill sessions or a
student-authored log. Reports must identify remaining work honestly.
Keep screenshots and preview artifacts outside the project. Do not commit keys,
Godot caches, Python caches, installed dependencies or build outputs.

## Original scene extraction

Use `godot/scenes/dangers.tscn` directly. Retain its existing nodes, positions,
textures, metadata, camera, papyrus, HUD and arena animations. Remove only unused
encounter sprites and their code/movement. Do not create substitute arenas,
layout resources or a replacement HUD. The episode adapter wraps the actual
scene and must preserve its gameplay rules. The original node/resource hashes
are recorded in `reports/provenance/direct-extraction.json`.
