# Frozen held-out evaluation — 2026-11-04

## Plan recorded before execution

Run the declared suite once per configuration: baseline, frozen combined-prompt
Vertex gemini-3.5-flash-lite with history=0, and the same model with history=2.
Spell31 seeds 101/102; spell32 seeds 201/202; spell32_low seeds 301/302.
18 held-out episodes total (6 baseline, 12 paid model). No tuning, selection or
paid retries using held-out results. Primary measures: wins and turn-backs;
retain reasons, steps, illegal actions, failures, usage/cost and raw evidence.

User authorized $20 total and requested a decision before increasing it. One
shared conservative reservation ledger across all paid episodes, cap $20, pause
before any call that reaches $16. The approval file gate preserves the active
engine and excludes approval waiting from episode wall time. Only an explicit
user decision can authorize creating that file. No automatic budget increases.
1200 calls and 1800 active wall seconds per episode; 30 seconds/call. Limit
outcomes are incomplete, not defeats. Dated configured token prices saved.

Normal speed, six-frame actions, 3 lives, standard crocodile counts, memory off,
reach flag off. Same visible observation schema. Baseline retains up to ten
observations for its 0.4-second reaction delay;
model receives exactly 0 or 2 prior observations. Both know red/plain heka rules:
the final tuned combined prompt now supplies that knowledge explicitly. Neither
receives RNG, schedules, hidden velocities or engine handles. Godot is authoritative.

Freeze exact prompt, player sources, suite and game hashes before execution;
verify before every episode/model call. Save configuration, Godot version,
per-action traces, errors, fallbacks, response IDs, usage and summaries. Tests
and baseline development evidence are separate checks, not held-out model results.
Independent review remains independently tracked; this run does not approve a gate.

Command: `python -B -m players.held_out_evaluation` from the midterm folder.
Model/default settings and suite are unchanged by the evaluation runner.

## Results

Executed November 4, 2026 UTC. All 18 planned held-out episodes ran once and reached a game win/loss. No retries, tuning, cap increases, limits or approval pauses occurred.

| Configuration | Wins | Turn-backs / total | Calls / failed | Estimated usage USD | Reserved USD |
|---|---:|---:|---:|---:|---:|
| baseline | 6/6 | 74/74 | 0/0 | 0.000000 | 0.000000 |
| model-h0 | 0/6 | 7/74 | 875/11 | 0.423916 | 3.581124 |
| model-h2 | 2/6 | 30/74 | 1324/3 | 0.975958 | 6.042026 |

### Individual episodes

| Configuration | Case / seed | Outcome / reason | Turn-backs | Steps | Invalid / failed | Calls | Usage USD | Reserved USD | Evidence |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| baseline | spell31 / 101 | won / all_crocodiles_defeated | 9/9 | 403 | 0/0 | 0 | 0.000000 | 0.000000 | [trace](../playtrace/20261104T082332827621Z-held-out-final/baseline/spell31-101.jsonl), [summary](../playtrace/20261104T082332827621Z-held-out-final/baseline/spell31-101.summary.json) |
| baseline | spell31 / 102 | won / all_crocodiles_defeated | 9/9 | 406 | 0/0 | 0 | 0.000000 | 0.000000 | [trace](../playtrace/20261104T082332827621Z-held-out-final/baseline/spell31-102.jsonl), [summary](../playtrace/20261104T082332827621Z-held-out-final/baseline/spell31-102.summary.json) |
| baseline | spell32 / 201 | won / all_crocodiles_defeated | 14/14 | 233 | 0/0 | 0 | 0.000000 | 0.000000 | [trace](../playtrace/20261104T082332827621Z-held-out-final/baseline/spell32-201.jsonl), [summary](../playtrace/20261104T082332827621Z-held-out-final/baseline/spell32-201.summary.json) |
| baseline | spell32 / 202 | won / all_crocodiles_defeated | 14/14 | 181 | 0/0 | 0 | 0.000000 | 0.000000 | [trace](../playtrace/20261104T082332827621Z-held-out-final/baseline/spell32-202.jsonl), [summary](../playtrace/20261104T082332827621Z-held-out-final/baseline/spell32-202.summary.json) |
| baseline | spell32_low / 301 | won / all_crocodiles_defeated | 14/14 | 182 | 0/0 | 0 | 0.000000 | 0.000000 | [trace](../playtrace/20261104T082332827621Z-held-out-final/baseline/spell32_low-301.jsonl), [summary](../playtrace/20261104T082332827621Z-held-out-final/baseline/spell32_low-301.summary.json) |
| baseline | spell32_low / 302 | won / all_crocodiles_defeated | 14/14 | 233 | 0/0 | 0 | 0.000000 | 0.000000 | [trace](../playtrace/20261104T082332827621Z-held-out-final/baseline/spell32_low-302.jsonl), [summary](../playtrace/20261104T082332827621Z-held-out-final/baseline/spell32_low-302.summary.json) |
| model-h0 | spell31 / 101 | lost / three_bites | 1/9 | 260 | 5/5 | 260 | 0.121865 | 1.059264 | [trace](../playtrace/20261104T082332827621Z-held-out-final/model-h0/spell31-101.jsonl), [summary](../playtrace/20261104T082332827621Z-held-out-final/model-h0/spell31-101.summary.json) |
| model-h0 | spell31 / 102 | lost / three_bites | 1/9 | 248 | 5/5 | 248 | 0.115955 | 1.010321 | [trace](../playtrace/20261104T082332827621Z-held-out-final/model-h0/spell31-102.jsonl), [summary](../playtrace/20261104T082332827621Z-held-out-final/model-h0/spell31-102.summary.json) |
| model-h0 | spell32 / 201 | lost / three_bites | 1/14 | 87 | 0/0 | 87 | 0.044038 | 0.358096 | [trace](../playtrace/20261104T082332827621Z-held-out-final/model-h0/spell32-201.jsonl), [summary](../playtrace/20261104T082332827621Z-held-out-final/model-h0/spell32-201.summary.json) |
| model-h0 | spell32 / 202 | lost / three_bites | 1/14 | 80 | 0/0 | 80 | 0.040493 | 0.329206 | [trace](../playtrace/20261104T082332827621Z-held-out-final/model-h0/spell32-202.jsonl), [summary](../playtrace/20261104T082332827621Z-held-out-final/model-h0/spell32-202.summary.json) |
| model-h0 | spell32_low / 301 | lost / three_bites | 1/14 | 90 | 1/1 | 90 | 0.045190 | 0.370627 | [trace](../playtrace/20261104T082332827621Z-held-out-final/model-h0/spell32_low-301.jsonl), [summary](../playtrace/20261104T082332827621Z-held-out-final/model-h0/spell32_low-301.summary.json) |
| model-h0 | spell32_low / 302 | lost / word_stolen | 2/14 | 110 | 0/0 | 110 | 0.056375 | 0.453609 | [trace](../playtrace/20261104T082332827621Z-held-out-final/model-h0/spell32_low-302.jsonl), [summary](../playtrace/20261104T082332827621Z-held-out-final/model-h0/spell32_low-302.summary.json) |
| model-h2 | spell31 / 101 | won / all_crocodiles_defeated | 9/9 | 411 | 0/0 | 402 | 0.291918 | 1.836522 | [trace](../playtrace/20261104T082332827621Z-held-out-final/model-h2/spell31-101.jsonl), [summary](../playtrace/20261104T082332827621Z-held-out-final/model-h2/spell31-101.summary.json) |
| model-h2 | spell31 / 102 | won / all_crocodiles_defeated | 9/9 | 513 | 2/2 | 504 | 0.364370 | 2.294713 | [trace](../playtrace/20261104T082332827621Z-held-out-final/model-h2/spell31-102.jsonl), [summary](../playtrace/20261104T082332827621Z-held-out-final/model-h2/spell31-102.summary.json) |
| model-h2 | spell32 / 201 | lost / three_bites | 0/14 | 78 | 1/1 | 78 | 0.058823 | 0.356375 | [trace](../playtrace/20261104T082332827621Z-held-out-final/model-h2/spell32-201.jsonl), [summary](../playtrace/20261104T082332827621Z-held-out-final/model-h2/spell32-201.summary.json) |
| model-h2 | spell32 / 202 | lost / three_bites | 1/14 | 80 | 0/0 | 80 | 0.060635 | 0.364900 | [trace](../playtrace/20261104T082332827621Z-held-out-final/model-h2/spell32-202.jsonl), [summary](../playtrace/20261104T082332827621Z-held-out-final/model-h2/spell32-202.summary.json) |
| model-h2 | spell32_low / 301 | lost / three_bites | 7/14 | 148 | 0/0 | 148 | 0.115384 | 0.678875 | [trace](../playtrace/20261104T082332827621Z-held-out-final/model-h2/spell32_low-301.jsonl), [summary](../playtrace/20261104T082332827621Z-held-out-final/model-h2/spell32_low-301.summary.json) |
| model-h2 | spell32_low / 302 | lost / three_bites | 4/14 | 121 | 0/0 | 112 | 0.084829 | 0.510642 | [trace](../playtrace/20261104T082332827621Z-held-out-final/model-h2/spell32_low-302.jsonl), [summary](../playtrace/20261104T082332827621Z-held-out-final/model-h2/spell32_low-302.summary.json) |

## Interpretation

The baseline won all six cases. The frozen combined-prompt model with two prior observations won both spell31 seeds, but lost all four two-sided spell32 cases. Without prior observations it won none. History-two scored 30 turn-backs across the six episodes versus 7 without history, with the largest difference in spell31 (9/9 on both seeds versus 1/9 on both). Standard spell32 scores were 0 and 1 with history-two versus 1 and 1 without; low-start spell32 scores were 7 and 4 versus 1 and 2. This is a case-specific result, not universal improvement from history.

The baseline and model receive the same standard observation representation, but the baseline retains up to ten observations and uses an explicit reaction-delay heuristic. Both have the red/plain heka rule in advance. Even history=0 retains observations with motion-derived seconds_to_bearer, computed from past visible positions by the interface; it is not a condition without all temporal information. The model is not trained during these episodes.

One stochastic episode per case/seed/configuration and differing provider failures limit causal inference and generalization. The held-out suite is now consumed for this evaluation. Do not use these outcomes for further tuning and continue calling the same seeds unseen. No policy or prompt was changed after any held-out result.

## Failures, cost and budget decision

2,199 model calls: 14 provider failures (11 TimeoutError, 3 HTTPError), all retained as invalid neutral fallbacks. No other illegal actions occurred. Failures by condition: model-h0 11; model-h2 3; baseline 0. Per-episode error types, fallback counts, final health and observed runtime model identifiers are in verification.json. All 2,185 successful calls reported gemini-3.5-flash-lite. No fixture or baseline episode substitutes for a live trial.

Returned token usage: 3,984,315 input and 81,832 output tokens (including any billed reasoning). Estimated returned-usage cost: $1.3998745. Conservative total reservation: $9.6231501 of the approved $20. The shared ledger includes failed calls; missing usage does not imply zero provider billing. Configured prices dated 2026-11-03: $0.30/million input, $2.50/million output; the exact source is saved in configuration and summaries. Provider billing was not reconciled.

The user requested a decision if spending approached the limit. The runner would pause before a call reaching $16 in reservations, preserving the engine and awaiting explicit approval. No threshold was reached and no budget decision or increase was needed. Approval wait time was zero.

## Frozen configuration and checks

Command: `python -B -m players.held_out_evaluation` from the midterm folder. No execution deviations or paid retries. Separate read-only review findings and implementation responses are recorded in [review.md](../review.md); execution does not certify review or approve a course gate.

Game SHA-256: `f08e6aea82a27010f29b03c9073c5ca26e539fd5ac16813d374ef23d8f036bd5`.
Prompt SHA-256: `266b037a82f744197692ef37585dcac34e5695fc2729a7c55a8ddb2630ccebf9`.
Suite SHA-256: `ec3c1399d77b9bbfdacef14246234a20421a1e6540ec55d618cbbe35a756c752`.
Godot: `4.7.2.stable.official.ed1daf0bf`.

Before execution, all 28 deterministic tests passed in 26.935 seconds. Separately, the baseline won all three development cases in playtrace/20261104T082253432948Z-baseline-h2-development; these checks are not counted in the 18 held-out results. The new trusted runner adds a shared budget and approval gate only; it does not change policy decisions, observations or game rules.

Every episode and model-call reservation checked frozen game, suite and player-source hashes. Post-run artifact checks verified 18 unique condition/case/seed combinations, all terminal summaries, matching per-trace source manifests, every build-archive SHA-256, the reservation ledger, no event memory, no reach flags and no top-level RNG/schedule/engine fields. This artifact inspection supports the boundary audit; it is not independent review. Raw build archives remain local artifacts and should not be committed. No settings or prompt tuning was performed.

## Evidence

- [Frozen configuration, exact prompt and source hashes](../playtrace/20261104T082332827621Z-held-out-final/configuration.json)
- [All episode summaries](../playtrace/20261104T082332827621Z-held-out-final/results.json)
- [Final shared budget](../playtrace/20261104T082332827621Z-held-out-final/budget.json)
- [Completion record](../playtrace/20261104T082332827621Z-held-out-final/completion.json)
- [Artifact checks and per-episode diagnostics](../playtrace/20261104T082332827621Z-held-out-final/verification.json)

## Subsequent reporting correction (no new trials)

After evaluation, players/run.py was changed only to report actual elapsed simulation frames and retain the nominal count separately. Existing traces remain unchanged: their simulation_frame field is nominal (charged steps × 6); actual terminal frames can be recovered as round(result.observation.time × 60). The frozen runner source is preserved in commit aee02a6 and matches the configuration hash. Current runner-source hashes therefore differ for this documented logging change; game, prompt, suite and gameplay policy are unchanged. All 41 final trace/summary/configuration/completion/budget/verification files are committed in aee02a6. No paid reruns were performed.
