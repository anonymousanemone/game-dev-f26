# Does Gemini learn within an episode? (2026-11-04)

**Question:** given more time (5 lives, 20 crocodiles) and a memory of what happened, does Gemini 3.5 Flash-Lite get better as an episode goes on?

**Setup.** Spell32, development seed 30, history 2, prompt with the option 1 distance fields (prompt SHA-256 `3d7be3d0…`; it adds one sentence describing `memory` and says "You lose when health reaches 0" instead of "Three bites lose"). Two evaluation settings were added to `reset` for this: `lives` (bites the bearer can take; tuned game 3) and `crocodiles` (how many to turn back; tuned spell32 is 14). The wave's speed ramp still applies, so the 20th crocodile is about 19% faster than the first, against 13% for the 14th.

**Memory** (`python -m players.run --memory`) is an event log the runner builds from the model's own actions and the observations it was shown, then sends with each call (most recent 60 entries). Each entry is one of:
- a thrust, with heka on or off and the nearest crocodile's colour, side and distance from the tip
- a look
- a crocodile turned back
- a bite
- a new game message

Every trace row records the memory that was sent. Without `--memory` the model sees only its last two observations and `notes`, as before.

## Results

| Run | Memory | Lives / crocodiles | Outcome | Turned back | Steps | Calls | Cost | Trace |
|---|---|---|---|---:|---:|---:|---:|---|
| Baseline (0.4 s reaction) | — | 5 / 20 | won | 20 | 250 | 0 | $0 | [trace](../playtrace/20261104T063040763204Z-baseline-h2-development/spell32-30.jsonl) |
| Gemini | no | 3 / 14 | lost, health 0 | 0 | 65 | 56 | $0.034 | [trace](../playtrace/20261104T061923835525Z-model-h2-development/spell32-30.jsonl) (attempt B, earlier prompt) |
| Gemini | yes | 3 / 14 | lost, health 0 | 1 | 80 | 71 | $0.055 | [trace](../playtrace/20261104T063053132337Z-model-h2-development/spell32-30.jsonl) |
| Gemini | no | 5 / 20 | lost, health 0 | 0 | 98 | 89 | $0.058 | [trace](../playtrace/20261104T063344100046Z-model-h2-development/spell32-30.jsonl) |
| Gemini | yes | 5 / 20 | lost, word stolen | 3 | 113 | 104 | $0.080 | [trace](../playtrace/20261104T063158472703Z-model-h2-development/spell32-30.jsonl) |

All 264 calls in the three new runs returned valid actions with no fallbacks. The game reports a health loss as `three_bites` whatever the number of lives.

First half against second half of each episode (by game time):

| Run | First half: turned back / bites / thrusts | Second half: turned back / bites / thrusts |
|---|---|---|
| Memory, 3 / 14 | 1 / 0 / 1 | 0 / 3 / 35, all with heka on |
| No memory, 5 / 20 | 0 / 2 / 5 | 0 / 3 / 7 |
| Memory, 5 / 20 | 1 / 1 / 5 | 2 / 0 / 9 |
| Baseline, 5 / 20 | 8 / 0 / 10 | 12 / 0 / 14 |

## Findings

1. **No sign of learning within an episode.** No Gemini run did clearly better in its second half than its first. The best case (memory, 5 / 20) went from 1 crocodile turned back to 2, while the share of its thrusts that connected fell.
2. **Memory helped a little in absolute terms.** The only crocodiles Gemini has ever turned back came in the two memory runs (1 and 3). In the 5 / 20 memory run its thrusts started a median 40 px from the tip, about the distance the baseline uses; the 3 / 14 memory run's one successful thrust started 39 px away.
3. **Extra lives alone changed nothing.** Without memory, 5 lives only made the episode longer (98 steps against 65); it turned back none of 20.
4. **Reading the rule made the 3 / 14 memory run worse.** After the shift rule appeared (t = 4.1 s), it thrust with heka on 35 steps in a row at a red crocodile 150–290 px away. The memory then filled with those thrusts, so it kept repeating them. It was bitten three times in that stretch.
5. **The 5 / 20 memory run lost a different way.** Its look at t = 2.5 s overlapped a bite, so the rule went into its `notes` but never appeared as a message. It turned back three crocodiles. At t = 11.3 s one slipped past it; once the heka word is active, that steals the word and ends the fight.
6. **The baseline is unchanged by length.** With its 0.4 s reaction delay it won 20 / 20 without a bite, with the same accuracy in both halves.

## Limits

- One episode per setting, on one development seed; no statistics are possible.
- The memory runs use a slightly different prompt from attempt B (the memory sentence and the health wording), so the 3 / 14 comparison is not exact.
- The event log is one design among many. It records the nearest crocodile at each thrust but does not say whether that thrust caused the next turn-back.
- No held-out seed was used.
