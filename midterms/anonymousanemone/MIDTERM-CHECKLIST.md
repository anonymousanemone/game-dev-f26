# Midterm completion checklist

## Implemented locally

- [x] Two complete crocodile games and required exported artwork; no MDPs.
- [x] Godot 4.7.2 imports, starts and renders.
- [x] The original dangers.tscn is used directly, retaining original node data and presentation and removing unused encounters.
- [x] Authoritative five-operation interface and fixed-step simulation.
- [x] Valid/invalid actions, observation boundary, terminal reasons and episode limits.
- [x] Observation-only heuristic and separate live API adapter.
- [x] Three-case suite declared before tuning; held-out seeds reserved.
- [x] Development baseline trials and action traces, including failure.
- [x] Deterministic rule, terminal, regression and budget checks.
- [x] Reusable skill and independent-review task prepared.
- [x] Source map, extraction hashes, patch and submission packager.
- [x] October 26 checkpoint branch pushed to the course fork; dedicated GitHub CI passed all 14 deterministic tests.
- [x] Human action tracing under `playtrace/`, exact-result replay checks and local matching-build archives.

## Still needs actual evidence / student work

- [ ] Record exact historical scan provenance and applicable reuse terms in CREDITS.md. - https://archiv.ub.uni-heidelberg.de/propylaeumdok/467/
- [ ] Link the implementation session from the course PR.
- [ ] Use the reusable skill by name in a second separate session; record that evidence.
- [ ] Obtain independent read-only review and respond to its actual findings.
- [ ] Write AGENT-TEAM.md and reflection in your own voice.
- [ ] Run at least one live model episode and first comparison for the October 26 checkpoint. GPT-6 Luna and a $10 cap are authorized; the funded API key is not yet configured. Run `python -m players.checkpoint` after filling `.env`.
- [ ] After freezing tuning, run baseline and model on the six held-out episodes; compare model history=0 and history=2, document failures and cost.
- [ ] Incorporate real peer playtest notes and limitations.
- [ ] Record 3–5 minutes and link it from README/PR.
- [ ] Package into the course repository, review only permitted paths and run its GitHub workflow. Local tests are not GitHub CI evidence.
- [ ] Open one course PR targeting main, complete links in submission/PR.md and submit its URL on CourseWorks by November 7, 11:59 p.m.
- [ ] Update the Week 3 scope thread if the chosen scope changed; complete later recording feedback before November 16.
