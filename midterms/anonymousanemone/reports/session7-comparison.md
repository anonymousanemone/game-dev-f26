# Session 7 comparison — live episode pending

No live model episode has run. These are actual baseline development results,
not a completed baseline/model comparison.

| Player | Case/seed | Outcome/reason | Score | Steps | Illegal | Calls/failed | Mean decision seconds | Input/output tokens | API cost USD |
|---|---|---|---:|---:|---:|---|---:|---|---:|
| Baseline | spell31/30 | won: all_crocodiles_defeated | 9 | 249 | 0 | 0/0 | 0.000002 | 0/0 | 0 |
| Baseline | spell32/30 | lost: three_bites | 3 | 64 | 0 | 0/0 | 0.000002 | 0/0 | 0 |
| Baseline | spell32_low/30 | lost: three_bites | 1 | 37 | 0 | 0/0 | 0.000003 | 0/0 | 0 |
| Live model | Pending funded key | Not run | — | — | — | — | — | — | — |

[Configuration](../playtrace/20261026T184527216889Z-baseline-h2-development/configuration.json)
and [full summary](../playtrace/20261026T184527216889Z-baseline-h2-development/summary.json).
Each case's JSONL action trace is alongside them in the same directory.

After configuring the private key, run `python -m players.checkpoint`. It will
replace this report with a matched baseline/live-model comparison, trace links,
configuration hashes and dated cost from actual runs. No held-out seeds are used.
