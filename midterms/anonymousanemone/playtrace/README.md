# Saved action traces

Human, baseline and live-model attempts are saved here. JSONL files are inputs to
the Godot replay script: the engine executes the recorded actions automatically
and checks the resulting observations and outcomes against the saved attempt.
See the project README for record, replay and verification commands.

Keep each local `.jsonl.build.zip` next to its trace to restore the exact Godot
source and artwork later. These generated build archives are Git-ignored; they
are not part of the course PR. Committed JSONL/configuration/summary files remain
inspectable evidence. Do not put API keys or personal playtester details here.

## Who played which human recording

Most `human-session-*.jsonl` files are the developer playing their own game.
The exception is `human-session-2026-11-07T03-19-30-24929513.jsonl` (UTC), which
starts with a peer playtest by the developer's roommate (not a classmate). She
gave up quickly. The last three attempts on spell 32 in that file are the
developer's own. The file is therefore mixed, so it is not a clean first-time-player
record. (Attribution is the developer's account; the trace itself does not record who played.)
