# Crocodiles midterm

Scope is spells 31 and 32 only. Reuse `godot/scripts/dangers/crocodiles.gd`; the Godot
engine is authoritative for humans, baseline, model and replay. No parallel MDP or
Python reimplementation. Never copy source MDPs or unrelated Totenbuch assets.

Players receive observations only. Keep RNG, spawn schedules and engine objects
out of player inputs. Fixed step is 1/60 s; each action advances six frames.
Read `suite.json` before changes and leave held-out seeds out of tuning.
Run `python -m unittest discover -s tests -v` after engine/interface changes.
Use `$crocodile-evaluation` at `skills/crocodile-evaluation/SKILL.md` for evaluation.
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
are recorded in `reports/direct-extraction.json`.
