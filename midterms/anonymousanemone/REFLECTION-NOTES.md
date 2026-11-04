# Reflection notes: evidence for the student's reflection

**These are agent-gathered notes, not the reflection.** The assignment requires the reflection in the student's own voice; this file only collects findings from the saved traces so they can be checked, interpreted and written up. Figures were computed on 2026-11-04 from the files linked below.

## Sources

| What | File |
|---|---|
| Gemini 3.5 Flash-Lite, spell32, development seed 30, first trial with the heka-discovery rules | [trace](playtrace/20261104T054256539690Z-model-h2-development/spell32-30.jsonl) |
| Baseline, same case and seed | [trace](playtrace/20261104T054253858015Z-baseline-h2-development/spell32-30.jsonl) |
| Baseline, spell31, seed 30 | [trace](playtrace/20261104T025623889524Z-baseline-h2-development/spell31-30.jsonl) |
| Student's own play (Record session) | [04:13](playtrace/human-session-2026-11-04T04-13-22-6323711.jsonl), [04:35](playtrace/human-session-2026-11-04T04-35-41-3622553.jsonl), [04:59](playtrace/human-session-2026-11-04T04-59-53-4476653.jsonl), [05:31](playtrace/human-session-2026-11-04T05-31-40-3102374.jsonl) (UTC) |

## Why Gemini lost (spell32, seed 30)

Gemini lost by three bites after 65 steps (6.5 s of game time), turning back no crocodiles. All 56 calls returned valid actions with no fallbacks; it cost about $0.029. The baseline won the same episode 14/14 with no bites.

- **Every thrust was far out of reach.** The spear reaches 15 px past its tip, and a thrust lands 0.083 s after it starts, so it has to start when the snout is roughly 25–40 px away (the baseline's median is 39 px). Gemini's nine thrusts started a median 223 px away, between 130 and 290 px.
- **It faced the far crocodile instead of the near one.** At step 25 it turned right toward a red crocodile about 700 px away while a plain crocodile was 92 px away on its left. That one bit from behind at step 32. The same thing happened at step 65 for the final bite.
- **It looked at a bad moment.** At step 38 it used `look` with the red crocodile about 170 px away. Looking leaves the controls idle for 1.0 s (about 260 px of crocodile travel), and the crocodile bit during the read. The look did work: the shift rule went into its `notes`.
- **It never paired heka with a thrust.** It held heka twice, once with no thrust and once during the look, when controls are ignored.
- **It rarely lined up.** Its first thrusts toward the red crocodile came while it was 76 px off vertically. It only lined up from step 51, at one health.
- **It hardly moved.** It stood still on 29 of 56 decisions, moved on 8% of steps and turned once.

A possible reading for the student to test: the model gets raw coordinates and has to subtract snout from tip itself, and its choices look driven by colour (red first) more than by distance. This is one development episode and does not rank the players.

## Student play compared with the baseline and Gemini

Four recordings: three cover both fights, and the fourth covers spell31 only. All four are the developer playing their own game, so they show one experienced player, not new players.

Spell32:

| | Result | Time | Thrusts per kill | Bites | Time moving | Turns |
|---|---|---|---|---|---|---|
| Student, winning attempts | 14/14 | 24–26 s | 1.1–1.2 | 1–2 | 22–35% | 4–10 |
| Student, losing attempts | 6–11 kills, then three bites | 19–33 s | 1.2–1.6 | 3 | 13–26% | 8–12 |
| Baseline (before the reaction delay) | 14/14 | 18.9 s | 1.2 | 0 | 53% | 8 |
| Baseline with 0.4 s reaction delay | 14/14 | 21.5 s | 1.2 | 1 | — | — |
| Gemini | 0 kills, three bites | 6.5 s | 9 thrusts, no kills | 3 | 8% | 1 |

1. **Accuracy.** On wins the student needed about 1.1 thrusts per kill, the same as the baseline. Gemini never connected.
2. **Learning within a session.** In 3 of 4 sessions the student's first spell32 attempt ended in three bites, and the next attempt won. Neither agent carries anything from one episode to the next.
3. **Bites.** The student's wins still cost 1–2 bites; the baseline took none, because it predicts exactly where each snout will be when the thrust lands.
4. **Movement.** The student moved 22–35% of the time and turned 4–12 times in spell32. The baseline moved 53% of the time, lining up with each next threat. Gemini moved on only 8% of its decisions and turned once, toward the wrong crocodile.
5. **Speed.** Student wins took 24–26 s; the baseline took 18.9 s. Part of the difference is reaction time and part is waiting before the first thrust (1–11 s after the fight opened; the baseline's first thrust came 2.7 s in).
6. **Discovering heka.** In two sessions the student clicked the heka word 2–3 s after "signs begin to glow red" appeared. In one they clicked before that message, and in another on the scroll before any fight. After clicking, they waited 1.1–3.1 s (about 2.6 s typical) before their next control input. The agent's 1.0 s look cost is at the low end of that, and about 2.5 s would match these recordings better. The student also clicked during a wave break, when looking is cheap; Gemini looked with a crocodile approaching.
7. **Spell31.** Every spell31 win took 10 thrusts for 9 kills, for the student and the baseline alike. The student's very first attempt was lost with no bites, meaning a word was stolen (a heka mistake or a crocodile that slipped past).

## Does Gemini learn within an episode?

From [the learning experiment](reports/learning-experiment.md) (one episode per setting, development seed 30):

- With 5 lives and 20 crocodiles, no Gemini run did clearly better in its second half than its first. Without memory it turned back none of 20; with an event-log memory it turned back 3, then lost when a crocodile slipped past and stole the word.
- With memory in the standard game (3 lives, 14 crocodiles) it turned back 1. After reading the shift rule it thrust with heka on 35 steps in a row at a red crocodile 150–290 px away, and its memory filled up with those repeated thrusts.
- The baseline won 20 of 20 with no bites. Like the agents, it cannot learn across episodes; unlike them, it does not need to.
- Compare with your own play: you lost your first spell32 attempts and then won, which is the kind of improvement neither agent shows.

## Does a reach flag help?

From [the reach flag experiment](reports/reach-flag-experiment.md): with an `in_reach` flag on each crocodile, Gemini thrust every time the flag was on, but the flag was on for only 2 of its 56 decisions, and it still turned back nothing. A test player that aims like the baseline and thrusts only on the flag won 14 of 14. Gemini's weakness is getting into position (height and facing), not knowing when to press.

## Limits of these findings

- The recordings store crocodile body positions, not snout positions, so distances in them are not in the same units as the agent traces. Thrusts per kill, timing and bite counts are comparable.
- Student fight times include any wait before the first thrust, including the "Press [space] to start" wait in the later recordings.
- The four recordings span several builds from 2026-11-04; the crocodile tuning was the same in all of them.
- The agent figures come from one episode each on the development seed. They are not held-out results.

## Questions for the reflection

- What do you make of Gemini's failure: is it about timing, perception (raw coordinates), priorities (colour over distance), or the prompt? What would you try, and would changing it be fair before the held-out runs?
- Does the baseline's strength (no bites, wins everything on development cases) help or hurt the comparison you want to make?
- The baseline now waits 0.4 s (the fast end of your reaction times) before reacting to a crocodile. In the [speed sweep](reports/speed-sweep.md) it stays reliable up to 1.4× the tuned speed, yet you lost first attempts at 1.0×. Does that make it a fairer stand-in for a human, and what does it still do that you don't (exact prediction, no hesitation)?
- How close is the agent's heka discovery to yours? You kept the look cost at 1.0 s although your recordings show about 2.5 s; why is 1.0 s the right choice?
- What did you learn from losing your first spell32 attempts? What does it mean that the agents do not improve within an episode even with more lives and a memory?
- How might a first-time player differ from you, and what will the partner playtest add?
