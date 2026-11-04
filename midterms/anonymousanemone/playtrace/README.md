# Saved action traces

Human, baseline and live-model attempts are saved here. JSONL files are inputs to
the Godot replay script: the engine executes the recorded actions automatically
and checks the resulting observations and outcomes against the saved attempt.
See the project README for record, replay and verification commands.

Keep each local `.jsonl.build.zip` next to its trace to restore the exact Godot
source and artwork later. These generated build archives are Git-ignored; they
are not part of the course PR. Committed JSONL/configuration/summary files remain
inspectable evidence. Do not put API keys or personal playtester details here.
