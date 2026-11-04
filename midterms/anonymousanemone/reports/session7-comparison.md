# Session 7 development comparison

Automatically assembled from actual run summaries; this is not held-out evaluation.

| Player/model | Case/seed | Outcome/reason | Score | Steps | Illegal | Calls/failed | Mean decision seconds | Input/output tokens | Estimated USD |
|---|---|---|---:|---:|---:|---|---:|---|---:|
| baseline / heuristic | spell32/30 | won: all_crocodiles_defeated | 14 | 215 | 0 | 0/0 | 0.000006 | 0/0 | 0.000000 |
| model / gemini-3.5-flash-lite | spell32/30 | lost: three_bites | 0 | 65 | 0 | 56/0 | 1.465467 | 102736/2144 | 0.036181 |

[Trace](../playtrace/20261104T062200879251Z-baseline-h2-development/spell32-30.jsonl) · [Configuration](../playtrace/20261104T062200879251Z-baseline-h2-development/configuration.json) · [Summary](../playtrace/20261104T062200879251Z-baseline-h2-development/summary.json)


[Trace](../playtrace/20261104T062201832076Z-model-h2-development/spell32-30.jsonl) · [Configuration](../playtrace/20261104T062201832076Z-model-h2-development/configuration.json) · [Summary](../playtrace/20261104T062201832076Z-model-h2-development/summary.json)

Game SHA-256: `703288e2055d3cfab2aa29f8e4c5c0fc7dc5204d48e62001d0d7cce9b5b4cddb`.

Dated prices: 2026-11-03; [provider price source](https://cloud.google.com/model-garden/pricing). Uncached input prices are used for the estimate; reconcile failed-call billing with the provider.

Live checkpoint episode: a model submitted valid actions and reached a game win/loss.

Limitations: one development seed, one trial per player, no statistical inference. CI evidence is tracked separately in EVALUATION.md. Peer observations and student interpretation remain separate evidence.
