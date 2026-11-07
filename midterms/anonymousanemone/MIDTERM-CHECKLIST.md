# Midterm completion checklist

## Implemented locally

- [x] Two complete crocodile games and required exported artwork; no MDPs.
- [x] Godot 4.7.2 imports, starts and renders.
- [x] The original dangers.tscn is used directly, retaining original node data and presentation and removing unused encounters.
- [x] Authoritative five-operation interface and fixed-step simulation.
- [x] Valid/invalid actions, observation boundary, terminal reasons and episode limits.
- [x] Observation-only heuristic and separate live API adapter.
- [x] Three-case suite declared before tuning; held-out seeds were reserved and have now been evaluated once per condition.
- [x] Development baseline trials and action traces, including failure.
- [x] Deterministic rule, terminal, regression and budget checks.
- [x] Reusable skill and independent-review task prepared.
- [x] Source map, extraction hashes and patch.
- [x] October 26 checkpoint branch pushed to the course fork; dedicated GitHub CI passed all 14 deterministic tests.
- [x] In-game Record session beside Begin; native-input session replay, exact frame-delta preservation, local build archives and tamper checks.
- [x] Crocodile speeds and arrival spacing synced with the tuned Totenbuch (commit 0d5a340), including returning crocodiles; deterministic spacing fixtures and current development baseline traces.
- [x] Credit the artwork and font, link their sources and state reuse terms in README.md (Credits and reuse).

## Evidence and remaining student work

- [x] Record the public-domain basis for the Lepsius edition: published 1842, copyright expired, and faithful scans create no new copyright (§ 68 UrhG; *Bridgeman v. Corel*). Recorded in README.md (Credits and reuse).
- [x] Record the OldFax.ttf source and reuse terms: "Old Fax" by George Blackwell, CC BY 4.0, credited in README.md (Credits and reuse).
- [ ] Link exported implementation sessions from the actual course PR; local evidence is in reports/sessions/codex-implementation-sessions.md and PR.md.
- [x] Use crocodile-evaluation and make-experiment by name in two separate sessions each; see reports/sessions/skill-sessions.md and linked exports, including the combat-tuning session.
- [x] Obtain independent read-only review of the November 4 fixes; findings, responses and follow-up are committed in review.md (ae74a5d).
- [ ] Optional: independent review of the later web console, replay consolidation, documentation cleanup (07a348d) and saved-example changes. The linked reviewer session (`01a1a5a8-…`) covers only the November 4 work and says so; the Nov 4 review is the course's independent-review evidence.
- [ ] Write AGENT-TEAM.md in your own voice.
- [x] Run at least one live model episode and first comparison (due for the October 26 checkpoint; done November 4). Gemini 3.5 Flash-Lite on Vertex AI, spell32 seed 30, with `python -m players.checkpoint`; results in EVALUATION.md and reports/session7-comparison.md.
- [x] Completed all 18 frozen held-out episodes (six per condition), including model history=0/2, failures and cost; report: reports/held-out-final.md. Evidence committed at aee02a6.
- [x] Incorporate real peer playtest notes and limitations. Playtest done; feedback (add an intermediate level or ease spell 32) was noted but not implemented. See PEER-NOTES.md.
- [x] Record 3–5 minutes and link it from README/PR: https://youtu.be/vOJ406Mh6Yk
- [x] Project is in the course repository; dedicated CI passed 29 tests on 74df51e. See reports/validation/ci-evidence.json.
- [x] Refresh CI evidence for later changes: 74df51e passed 29 tests (run 42418064311).
- [x] Course PR #66 exists, as recorded in EVALUATION.md and CI evidence.
- [ ] Complete/update links in the actual course PR (PR.md is the local draft) and submit its URL on CourseWorks by November 7, 11:59 p.m.
- [x] Update the Week 3 scope thread if the chosen scope changed (done by the student).
- [ ] Complete the later recording feedback on three classmates' recordings before November 16.
