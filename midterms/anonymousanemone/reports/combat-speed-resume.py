import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile
from players import combat_experiment, engine, run, traces
original = engine.ROOT
folder = original/'playtrace/20261104T072415073512Z-combat-speed-experiment'
root = Path(tempfile.mkdtemp(prefix='croc-combat-original-'))
shutil.copytree(original/'godot', root/'godot')
archive = folder/'current-speed1.0-seed30/spell32-30.jsonl.build.zip'
with zipfile.ZipFile(archive) as z:
    (root/'godot/project.godot').write_bytes(z.read('godot/project.godot'))
engine.ROOT = run.ROOT = traces.ROOT = root
expected = json.loads((folder/'current-speed1.0-seed30/configuration.json').read_text())['game_version']
assert run.version() == expected, 'Isolated build does not match original'
print('Isolated original build verified:', expected, flush=True)
pending = folder/'combined-speed1.0-seed32'
if pending.exists() and not (pending/'summary.json').exists():
    assert not (pending/'spell32-32.jsonl').exists() or len((pending/'spell32-32.jsonl').read_text().splitlines()) <= 1
    pending.rename(folder/'preflight-failed-combined-speed1.0-seed32')
combat_experiment.run(3, folder.name)
