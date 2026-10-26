"""Stage a reviewable course hand-in; never pushes, commits or opens a PR."""
import argparse
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
ROOT_ENTRIES = {'godot', 'players', 'tests', 'skills', 'reports', 'submission',
                'playtrace', 'suite.json', 'agent-config.json', '.gitignore', '.env.example'}


def ignore_private_files(folder, names):
    ignored = []
    for name in names:
        if Path(folder) == ROOT and name not in ROOT_ENTRIES and not name.endswith('.md'):
            ignored.append(name)
        elif (name in {'.git', '.godot', '__pycache__', '.DS_Store', '.env', '.venv',
                       'node_modules', 'build', 'obsolete-replacement'}
              or (name.startswith('.env.') and name != '.env.example')
              or name.endswith(('.pyc', '.mdp', '.build.zip', '.html'))):
            ignored.append(name)
    return ignored


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--login', required=True)
    parser.add_argument('--course-repo', required=True, type=Path)
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,37}[a-z0-9])?', args.login):
        parser.error('Use your lowercase GitHub login.')
    repo = args.course_repo.resolve()
    destination = repo/'midterms'/args.login
    if destination.exists():
        parser.error(f'{destination} already exists; refusing to overwrite a submission.')
    workflow = repo/'.github'/'workflows'/f'midterm-{args.login}.yml'
    if workflow.exists():
        parser.error(f'{workflow} already exists; refusing to overwrite it.')
    shutil.copytree(ROOT, destination, ignore=ignore_private_files)
    workflow.parent.mkdir(parents=True, exist_ok=True)
    # This workflow touches only this login's folder; it needs no secrets.
    workflow.write_text(f'''name: Midterm {args.login}
on:
  push:
    branches: ['{args.login}/midterm']
    paths:
      - 'midterms/{args.login}/**'
      - '.github/workflows/midterm-{args.login}.yml'
  pull_request:
    paths:
      - 'midterms/{args.login}/**'
      - '.github/workflows/midterm-{args.login}.yml'
permissions:
  contents: read
jobs:
  deterministic:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: midterms/{args.login}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install Godot
        env:
          GODOT_VERSION: '4.7.2'
        run: |
          curl --fail --location --retry 3 "https://github.com/godotengine/godot-builds/releases/download/${{GODOT_VERSION}}-stable/Godot_v${{GODOT_VERSION}}-stable_linux.x86_64.zip" -o "$RUNNER_TEMP/godot.zip"
          unzip "$RUNNER_TEMP/godot.zip" -d "$RUNNER_TEMP/godot-bin"
          echo "GODOT=$RUNNER_TEMP/godot-bin/Godot_v${{GODOT_VERSION}}-stable_linux.x86_64" >> "$GITHUB_ENV"
      - name: Import project
        run: '"$GODOT" --headless --path godot --editor --import --quit'
      - name: Deterministic checks
        run: python -m unittest discover -s tests -v
''')
    print(destination)
    print(workflow)
    print('Review these files, create your midterm branch, and open the course PR when ready.')


if __name__ == '__main__': main()
