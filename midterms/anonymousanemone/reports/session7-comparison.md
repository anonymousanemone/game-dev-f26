# Session 7 comparison — live episode pending

Current difficulty revision: spell32 base speed reduced and global half-body movement spacing enforced. These are actual development baseline results, not a completed baseline/model comparison.

| Player | Case/seed | Outcome/reason | Score | Steps | Illegal | Calls/failed | Mean decision seconds | Input/output tokens | API cost USD |
|---|---|---|---:|---:|---:|---|---:|---|---:|
| Baseline | spell31/30 | won: all_crocodiles_defeated | 9 | 249 | 0 | 0/0 | 0.000003 | 0/0 | 0 |
| Baseline | spell32/30 | lost: three_bites | 8 | 122 | 0 | 0/0 | 0.000003 | 0/0 | 0 |
| Baseline | spell32_low/30 | lost: three_bites | 2 | 43 | 0 | 0/0 | 0.000005 | 0/0 | 0 |
| Live model | Pending funded key | Not run | — | — | — | — | — | — | — |

[Configuration](../playtrace/20261026T234254422011Z-baseline-h2-development/configuration.json) · [Summary](../playtrace/20261026T234254422011Z-baseline-h2-development/summary.json). Individual JSONL traces are beside them.

The prior faster-difficulty runs remain available as historical evidence, not results for this revision. Repeated development runs are reproducibility/debugging checks, not independent held-out trials. After configuring the key, `python -m players.checkpoint` replaces this report with a matched baseline/live-model comparison. No held-out seeds have been used.
