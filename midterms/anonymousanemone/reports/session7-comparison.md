# Session 7 development comparison

Automatically assembled from actual run summaries; this is not held-out evaluation.

| Player/model | Case/seed | Outcome/reason | Score | Steps | Illegal | Calls/failed | Mean decision seconds | Input/output tokens | Estimated USD |
|---|---|---|---:|---:|---:|---|---:|---|---:|
| baseline / heuristic | spell32/30 | won: all_crocodiles_defeated | 14 | 189 | 0 | 0/0 | 0.000005 | 0/0 | 0.000000 |
| model / gemini-3.5-flash-lite | spell32/30 | lost: three_bites | 1 | 80 | 0 | 80/0 | 0.880433 | 101561/2160 | 0.035868 |

[Trace](../playtrace/20261104T025633917875Z-baseline-h2-development/spell32-30.jsonl) · [Configuration](../playtrace/20261104T025633917875Z-baseline-h2-development/configuration.json) · [Summary](../playtrace/20261104T025633917875Z-baseline-h2-development/summary.json)


[Trace](../playtrace/20261104T025635197909Z-model-h2-development/spell32-30.jsonl) · [Configuration](../playtrace/20261104T025635197909Z-model-h2-development/configuration.json) · [Summary](../playtrace/20261104T025635197909Z-model-h2-development/summary.json)

Game SHA-256: `d33f017b8ed276aff1b69b5800afdef62d971ca44ee2b9655463b684ad096f80`.

Dated prices: 2026-11-03; [provider price source](https://cloud.google.com/model-garden/pricing). Uncached input prices are used for the estimate; reconcile failed-call billing with the provider.

Live checkpoint episode: a model submitted valid actions and reached a game win/loss.

Limitations: one development seed, one trial per player, no statistical inference. CI evidence is tracked separately in EVALUATION.md. Peer observations and student interpretation remain separate evidence.
