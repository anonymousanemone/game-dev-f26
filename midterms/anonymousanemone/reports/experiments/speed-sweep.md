# Crocodile speed sweep (baseline only), 2026-11-04

**Question:** how much faster can the crocodiles get before the baseline starts to lose, and how much does the human-like reaction delay matter?

**Method:** `python -m players.speed_sweep`. It runs the baseline through the normal engine interface with `reset(..., speed_scale=k)`, which multiplies every wave's crocodile speed by `k` (spell31's single slow lesson crocodile is not scaled). Five seeds per setting: development seed 30 plus 31–34; the held-out seeds were not used. Speed scales are 1.0× to 3.0× in steps of 0.2. Two baselines: the current one, which ignores a crocodile until it has been visible 0.4 s, and an instant-reaction version (0.0 s) for comparison. No model calls. Raw results: [speed-sweep.json](../speed-sweep.json).

For scale, spell32's tuned speed is 262.5 world px/s, so 1.4× is about 367 px/s, 1.6× about 420 px/s and 2.2× about 578 px/s. The bearer moves vertically at 390 px/s.

## Wins out of 5

| Speed | spell31 (0.4 s) | spell32 (0.4 s) | spell32_low (0.4 s) | spell31 (instant) | spell32 (instant) | spell32_low (instant) |
|---|---|---|---|---|---|---|
| 1.0× | 5 | 5 | 5 | 5 | 5 | 5 |
| 1.2× | 5 | 5 | 5 | 5 | 5 | 5 |
| 1.4× | 5 | 5 | 5 | 5 | 5 | 5 |
| 1.6× | 3 | **1** | 4 | 3 | 4 | 4 |
| 1.8× | 5 | 1 | **0** | 5 | 2 | 3 |
| 2.0× | 3 | 1 | 1 | 3 | 3 | 3 |
| 2.2× | 5 | 0 | 0 | 5 | **0** | **0** |
| 2.4× | 5 | 0 | 0 | 5 | 1 | 1 |
| 2.6× | 5 | 0 | 0 | 5 | 1 | 0 |
| 2.8× | 5 | 0 | 0 | 5 | 0 | 0 |
| 3.0× | 5 | 0 | 0 | 5 | 0 | 0 |

Every loss was by three bites; no word was stolen.

## Findings

1. **Spell32 breaks at about 1.6× the tuned speed.** With the 0.4 s delay the baseline wins every seed up to 1.4×, then 1 in 5 at 1.6×–2.0×, and none from 2.2×. Spell32_low holds slightly longer (4 in 5 at 1.6×) and then collapses at 1.8×.
2. **The reaction delay moves the breaking point earlier, but only a little.** The instant baseline also starts losing at 1.6× and wins nothing at 2.2×. Between 1.6× and 2.0× it wins clearly more often (2–4 in 5 against 0–1 in 5). So beyond about 2× the game itself is too fast for this strategy, whatever the reaction time; between 1.6× and 2.0× the 0.4 s delay is what decides it.
3. **Bites appear before losses.** At 1.0×–1.4× the delayed baseline already averages 0.4–0.8 bites in spell32, against 0.2–0.6 for the instant one. At 1.6× the average jumps to 2–3 bites.
4. **Spell31 has no breaking point up to 3×.** Losses appear only at 1.6× and 2.0× (2 of 5 seeds each). They are identical with and without the delay and disappear again at higher speeds. That pattern points to a timing quirk in the baseline itself: it predicts the strike point a fixed 5 ticks ahead and checks only every 0.1 s step, so at some speeds the crocodile can skip past its strike window. This is a likely cause, not a verified one. Spell31's one-sided waves never press the bearer the way spell32's two-sided waves do.
5. **The tuned game sits well inside the baseline's range.** At 1.0× the delayed baseline wins every case and seed, so there is headroom of about 1.4× before it fails. The student's own spell32 losses (three of the first attempts in four sessions) happened at 1.0×, so the game is hard for a human at a speed the baseline finds easy.

## Limits

- Five seeds per setting, so each win count is coarse (one seed moves it by 20 percentage points).
- Only the baseline was swept; Gemini was not run at higher speeds.
- Spell31's lesson crocodile keeps its normal speed.
