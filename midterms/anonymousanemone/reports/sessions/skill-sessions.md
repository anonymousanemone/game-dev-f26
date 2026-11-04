# Reusable skill invocation evidence

## crocodile-evaluation

Instructions: [SKILL.md](../../skills/crocodile-evaluation/SKILL.md).

1. **October 26, 2026 — Codex `01a17976-2642-76b1-a706-135d79c974bc`.**
   The [implementation export, session 2](codex-implementation-sessions.md)
   explicitly states: “I’m using the project’s `crocodile-evaluation` skill to
   validate the interface change.” It records recording/replay work and
   development checks. Historical results apply to their recorded builds. The
   initial extraction session is also exported as session 1; creation of the
   skill alone is not used as proof of invocation.
2. **November 4, 2026 — Codex `01a1a54d-a53b-7ed1-8278-9086ef65ed8a`.**
   The [review/experiment export](codex-review-and-experiment-session.md)
   explicitly applies the skill during the initial scope/boundary inspection:
   static reads and scene/asset hashes, without runtime tests at that stage.
   Later in the same session, the [alignment experiment](../experiments/y-alignment-experiment.md)
   records live development trials, failures/costs, and 26 passing deterministic
   tests after a permitted rerun. Those later activities are not a third session.

These are two separate evidenced sessions, not certification of full independent
review, peer feedback or student authorship. The November 4 export is a snapshot
that predates these documentation updates; it does not include later messages.

## make-experiment

Instructions: [SKILL.md](../../skills/make-experiment/SKILL.md).

1. **November 4, 2026 — Codex `01a1a54d-a53b-7ed1-8278-9086ef65ed8a`.**
   Created the skill, then explicitly invoked `$make-experiment` for the
   vertical-alignment question. The [transcript](codex-review-and-experiment-session.md),
   [plan/results](../experiments/y-alignment-experiment.md), and linked raw
   configurations/traces provide evidence of actual use.
2. **November 4, 2026 — Codex `01a1a56c-5747-78a0-8c4f-be245174e43c`.**
   The [combat-tuning export](codex-combat-tuning-session.md) records the user's
   explicit `$make-experiment` invocation and the assistant's acknowledgment for
   the current/combined prompt comparison at 1.0× and 0.75× speed. See the
   [initial comparison](../experiments/combat-speed-experiment.md) and
   [full combat report](../experiments/combat-speed-full.md) for results and
   trial artifacts. This export preserves user and assistant messages; tool
   calls/results are omitted, as stated in its header.

These are two separate evidenced sessions using `make-experiment` by name.

Link the committed exports and this evidence index from the actual course PR.
