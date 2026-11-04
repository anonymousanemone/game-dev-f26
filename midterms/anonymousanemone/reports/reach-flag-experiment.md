# Reach flag experiment (2026-11-04)

**Boundary classification:** this historical run supplied the model with the engine’s exact strike/silhouette result. It is privileged assistance, not a standard observation-only evaluation. Its results remain exploratory and must not be pooled into standard suite comparisons. The flag remains off by default; this classification does not resolve the boundary conflict or change implementation.

**Question:** does Gemini do better if each crocodile is marked when it is within the spear's reach?

**Setup.** Spell32, development seed 30, standard game (3 lives, 14 crocodiles), history 2, no memory. The observation keeps the option 1 distance fields and adds `in_reach` to each crocodile (`python -m players.run --reach-flag`; `reset(..., reach_flag=true)`). `in_reach` is the game's own strike test (`_croc_strike`) applied to where the crocodile is now: the snout is within 20 plate px of the spear's stroke, or the stroke lands on its outline. It does not predict where the crocodile will be when a thrust lands, 0.07 s later. The flag is an experiment setting and is off in normal runs. The prompt gained one sentence describing it (prompt SHA-256 recorded in the run's configuration).

## Result

| Player | Outcome | Turned back | Steps | Calls | Cost | Trace |
|---|---|---:|---:|---:|---:|---|
| Gemini 3.5 Flash-Lite with `in_reach` | lost, health 0 | 0 | 65 | 56 | $0.035 | [trace](../playtrace/20261104T064832630941Z-model-h2-development/spell32-30.jsonl) |
| Gemini without it (attempt B) | lost, health 0 | 0 | 65 | 56 | $0.034 | [trace](../playtrace/20261104T061923835525Z-model-h2-development/spell32-30.jsonl) |

All 56 calls returned valid actions with no fallbacks.

## Findings

1. **Gemini followed the flag.** `in_reach` was true on only 2 of its 56 decisions (steps 28 and 32), and it thrust on both. It made one other thrust (step 46), at a red crocodile 155 px away.
2. **Neither flagged thrust connected.** At step 28 the crocodile was 48 px off vertically; at step 32 its snout had already passed the tip and it bit on that step.
3. **The flag is useful when the aiming is right.** Checked with the deterministic baseline on the same episode (no model calls):
   - Every baseline thrust started while the flag was true hit (7 of 7). The baseline's other 7 hits came from thrusts it started just before the flag turned on, because it predicts where the snout will be.
   - A test player that moves and turns like the baseline but thrusts only when `in_reach` is true won 14 / 14 with one bite.
4. **So Gemini's problem is positioning, not the moment of the thrust.** It rarely put a crocodile within the spear's reach in the first place: wrong height, or facing the other way. A flag about reach cannot help with that.

## Limits

- One episode on one development seed.
- The flag-follower test reuses the baseline's own aiming; it shows what the flag allows, not what Gemini could learn.
