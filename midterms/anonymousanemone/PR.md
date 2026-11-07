GitHub login: **anonymousanemone**

This midterm extracts two complete crocodile encounters (spells 31–32) from my original Godot game, Totenbuch. Humans, the heuristic baseline and the model player use the same authoritative engine; the model selects validated actions through an observation-only interface.

The declared held-out suite contains three starting situations and two seeds each. Across all 18 completed episodes, the baseline won 6/6, Gemini 3.5 Flash-Lite with no explicit history won 0/6, and the same model with two prior observations won 2/6. Both conditions retain motion-derived observation fields. Fourteen provider failures were retained as neutral fallbacks. Estimated returned-usage cost was $1.3998745; conservative reservations totaled $9.6231501 of the authorized $20. No held-out tuning or paid retries are claimed.

Validation: **29 tests passed** in [dedicated Godot deterministic CI](https://github.com/columbia-university-ai-games/game-dev-f26/actions/runs/42418064311) on commit `74df51ec755e7f989e4f6fbc73981197bbd54ac7`. The local course boundary screen passed: only `midterms/anonymousanemone/` and `.github/workflows/midterm-anonymousanemone.yml` are included. Course PR checks passed: dedicated midterm tests, submission boundaries, minigame tests/gallery, and Python 3.11/3.12 starter checks. The optional paid live setup workflow was skipped.

Artifacts:

- [README](https://github.com/anonymousanemone/game-dev-f26/blob/74df51ec755e7f989e4f6fbc73981197bbd54ac7/midterms/anonymousanemone/README.md)
- [Evaluation](https://github.com/anonymousanemone/game-dev-f26/blob/74df51ec755e7f989e4f6fbc73981197bbd54ac7/midterms/anonymousanemone/EVALUATION.md)
- [Final evaluation](https://github.com/anonymousanemone/game-dev-f26/blob/74df51ec755e7f989e4f6fbc73981197bbd54ac7/midterms/anonymousanemone/reports/held-out-final.md)
- [Agent team](https://github.com/anonymousanemone/game-dev-f26/blob/74df51ec755e7f989e4f6fbc73981197bbd54ac7/midterms/anonymousanemone/AGENT-TEAM.md)
- [Peer notes](https://github.com/anonymousanemone/game-dev-f26/blob/74df51ec755e7f989e4f6fbc73981197bbd54ac7/midterms/anonymousanemone/PEER-NOTES.md)
- [Demonstration video (YouTube)](https://youtu.be/vOJ406Mh6Yk)
- [Independent review](https://github.com/anonymousanemone/game-dev-f26/blob/74df51ec755e7f989e4f6fbc73981197bbd54ac7/midterms/anonymousanemone/review.md)
- [Implementation sessions](https://github.com/anonymousanemone/game-dev-f26/blob/74df51ec755e7f989e4f6fbc73981197bbd54ac7/midterms/anonymousanemone/reports/sessions/codex-implementation-sessions.md)
- [Review/experiment session](https://github.com/anonymousanemone/game-dev-f26/blob/74df51ec755e7f989e4f6fbc73981197bbd54ac7/midterms/anonymousanemone/reports/sessions/codex-review-and-experiment-session.md)
- [Combat-tuning session — second make-experiment invocation](https://github.com/anonymousanemone/game-dev-f26/blob/74df51ec755e7f989e4f6fbc73981197bbd54ac7/midterms/anonymousanemone/reports/sessions/codex-combat-tuning-session.md)
- [Skill evidence](https://github.com/anonymousanemone/game-dev-f26/blob/74df51ec755e7f989e4f6fbc73981197bbd54ac7/midterms/anonymousanemone/reports/sessions/skill-sessions.md)

Remaining before ready for review:

- [ ] Complete the student-authored one-page agent-team narrative and personal interpretation/limitations.
- [x] Peer playtest done; anonymous notes and playtrace data are in PEER-NOTES.md. The feedback was noted but not implemented.
- [x] Recorded and linked a viewable demonstration showing the game and agent play without manual move selection.
- [x] Course PR checks passed on 74df51e (29 tests); CI evidence refreshed.
- [x] Week 3 scope thread updated by the student.
- [ ] Submit this PR URL on CourseWorks by November 7, 11:59 p.m.

This is a draft, not a completed submission or gate approval. Historical traces retain their original hashes; the subsequent frame-reporting correction is documented in the evaluation report.
