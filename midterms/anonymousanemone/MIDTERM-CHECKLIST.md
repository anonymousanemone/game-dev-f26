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
- [x] In-game Record session beside Begin; native-input session replay, exact frame-delta preservation, local build archives and tamper checks.
- [x] Spell32 reduced speed and cross-side/all-height half-body movement spacing, including returning crocodiles; deterministic regression fixtures and current development baseline traces.
- [x] Identify the Lepsius digital edition, digital-version supplier, repository, DOI/URN, deposit date and actual linked reuse notice in CREDITS.md and reports/lepsius-provenance.json.

## Still needs actual evidence / student work

- [x] Record the public-domain basis for the Lepsius edition: published 1842, copyright expired, and faithful scans create no new copyright (§ 68 UrhG; *Bridgeman v. Corel*). Recorded in CREDITS.md.
- [ ] Optional: record the existing PNGs' precise source/crop chain from plate XVI. No assets have been silently replaced.
- [x] Record the OldFax.ttf source and reuse terms: "Old Fax" by George Blackwell, CC BY 4.0, credited in CREDITS.md.
- [ ] Link the implementation session from the course PR.
- [ ] Use the reusable skill by name in a second separate session; record that evidence.
- [ ] Obtain independent read-only review and respond to its actual findings.
- [ ] Write AGENT-TEAM.md and reflection in your own voice.
- [ ] Run at least one live model episode and first comparison for the October 26 checkpoint. Gemini 3.5 Flash-Lite on Vertex AI with a $10 default cap; the starter's Vertex check passes. Set `GOOGLE_CLOUD_PROJECT` in `.env`, then run `python -m players.checkpoint`.
- [ ] After freezing tuning, run baseline and model on the six held-out episodes; compare model history=0 and history=2, document failures and cost.
- [ ] Incorporate real peer playtest notes and limitations.
- [ ] Record 3–5 minutes and link it from README/PR.
- [ ] Package into the course repository, review only permitted paths and run its GitHub workflow. Local tests are not GitHub CI evidence.
- [ ] Open one course PR targeting main, complete links in submission/PR.md and submit its URL on CourseWorks by November 7, 11:59 p.m.
- [ ] Update the Week 3 scope thread if the chosen scope changed; complete later recording feedback before November 16.
