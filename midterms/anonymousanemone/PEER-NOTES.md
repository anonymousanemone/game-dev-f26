# Peer playtest notes

My roommate played the frozen build in the native Record session, saved as [human-session-2026-11-07T03-19-30](playtrace/human-session-2026-11-07T03-19-30-24929513.jsonl) (UTC). She is rather in patient and not very into it, and gave up quickly. The last three attempts on spell 32 in that file are the my own, not hers, just to finish the game. 

The controls were fairly intuitive, and she was able to get started with no problem. The first level was easy, as intended, and she immediately went to click the red heka sign when the hint was given, and had time to read it, test out shift a few times, before the crocodiles of the next wave reached her. However, spell 32 was significantly more challenging, and she failed enough times to want to quit. The feeback I got was that there should've been an intermediate level, because the difficulty jump betwen spell 31 and 32 was too drastic. 

This is sensical feedback, and I would implement it in the future by either decreasing the difficulty of 32 or increasing the difficulty of 31 (probably the former). Although an intermediate 3rd level might've been a happier solution, in order to adhere to the logic that each minigame maps to a spell within the source book, there can only be 2 crocodile levels. 

I'm still conflicted, because I did want the game to be challenging, but had measured it off of my own playtest experience. What I would've preferred is for spell 32 to take 2-3 attempts to win, which is true for my attempts. However, it was too hard for my playtester, and rather discouraging. Nevertheless, one playtester, who gave up after about six attempts, is not a measure of how a motivated new player would do. I would ask at least two more people to try it before settling on a definitive decision. 


## Playtester data from the recording

Computed by Claude Code Sonnet 5.5 from the playtrace. The session ran 278 s of recorded game time; about 186 s of it was before the developer's three attempts.

**Per attempt** (encounter time is the in-fight clock; a thrust is a spear strike started; "moving" is the share of fight time a walk/move key was held):

| # | Player | Spell | Result | Encounter time | Kills | Thrusts | Bites | Moving | Heka held | Turns |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Playtester | 31 | Won | 49.4 s | 9 | 25 | 1 | 13% | 10% | 0 |
| 2 | Playtester | 32 | Backed out at 2 health | 17.8 s | 1 | 7 | 1 | 25% | 8% | 10 |
| 3 | Playtester | 32 | Lost | 13.2 s | 1 | 11 | 3 | 19% | 20% | 4 |
| 4 | Playtester | 32 | Lost | 13.5 s | 2 | 4 | 3 | 20% | 7% | 2 |
| 5 | Playtester | 32 | Lost | 14.5 s | 3 | 7 | 3 | 25% | 18% | 0 |
| 6 | Playtester | 32 | Lost | 10.0 s | 0 | 7 | 3 | 12% | 2% | 6 |
| 7 | Playtester | 32 | Lost | 10.8 s | 1 | 5 | 3 | 26% | 15% | 2 |
| 8 | Developer | 32 | Lost | 24.3 s | 12 | 16 | 3 | 29% | 8% | 8 |
| 9 | Developer | 32 | Lost | 18.3 s | 9 | 12 | 3 | 31% | 15% | 4 |
| 10 | Developer | 32 | Won | 27.7 s | 14 | 18 | 2 | 41% | 7% | 8 |

**Spell 32 only, same build, same game:**

| | Attempts | Wins | Mean encounter time | Kills (total) | Thrusts per kill | Bites per attempt | Moving | Turns per attempt |
|---|---|---|---|---|---|---|---|---|
| Playtester | 6 | 0 | 13.3 s | 8 | 5.1 | 2.7 | 22% | 4.0 |
| Developer | 3 | 1 | 23.4 s | 35 | 1.3 | 2.7 | 34% | 6.7 |

What the numbers show:
- **Both of us lost the same way.** Every losing spell 32 attempt ended with all three health lost (rows 3–9); the one exception is her first attempt, which she left at 2 health. Bites per attempt are equal (2.7), but she was bitten after about 13 s and 1.3 kills on average, while the developer lasted about 23 s with about 12 kills per attempt.
- **Accuracy is the largest gap.** She needed about 5 thrusts per kill; the developer needed about 1.3 (the same as in the developer's earlier recordings). This is one person's first attempts against one person's practised play, so it shows the effect of practice, not a general rate for new players.
- **The developer moved more.** The developer held a move key 34% of the time against her 22%, and turned a little more often per attempt.
- **Heka use was similar** (about 10–12% of fight time for both), so the difference is not that she skipped the magic.
- **The developer's win was close.** It ended with 2 bites, so even after practice (this was the developer's third attempt in the file; the developer had also played many times before) spell 32 is not comfortably winnable. That supports her feedback about the jump from spell 31.

