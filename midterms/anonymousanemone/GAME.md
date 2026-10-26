# Crocodiles: rules, core loop and interfaces

This is a playable excerpt of **Totenbuch**, an original game built around an illustrated Egyptian funerary scroll. The midterm includes only spells 31 and 32: two encounters in which a spear-bearer must turn back approaching crocodiles. This description is based on the implemented scene and source; it does not report playtesting results.

## Rules/manual/source excerpt

Click **Begin**, then use the arrow keys or click the papyrus to walk between the two crocodile vignettes. Click a crocodile to enter its encounter.

| Control | Effect during combat |
|---|---|
| Up/Down or W/S | Move the spear-bearer vertically to align with a crocodile |
| Left/Right or A/D | Face left or right in spell 32 |
| Space | Thrust the spear |
| Hold Shift while thrusting | Use heka; the spear turns red |
| Escape | Leave the encounter |

An ordinary crocodile requires a plain thrust. A red crocodile requires heka. A plain thrust does not turn back a red crocodile; using heka on an ordinary crocodile loses the encounter. Position the spear tip at the approaching snout and time the thrust to connect.

The bearer starts with three health signs. Bites reduce health, and losing all three ends the encounter, with an introductory tutorial exception that protects the first lesson. Once the heka word is active, a crocodile that slips past can steal it and end the encounter. Turn back every crocodile in every wave to win. Complete both encounters to finish the excerpt.

Spell 31 teaches the thrust against crocodiles approaching from one side, then introduces a mixed wave of ordinary and red crocodiles. Spell 32 combines ordinary and red crocodiles approaching from both sides, requiring the player to choose a facing as well as a vertical position and attack type.

The original Godot scene, [dangers.tscn](godot/scenes/dangers.tscn), is the game authority. Its combat implementation is [crocodiles.gd](godot/scripts/dangers/crocodiles.gd). This source excerpt describes the color-matching rule:

```gdscript
var heka := _holding_heka()
if best.red and not heka:
    return
if heka and not best.red:
    _croc_steals(best)
    return
```

The encounter definitions are in [danger_encounters.gd](godot/scripts/dangers/danger_encounters.gd). These are original gameplay rules; the historical artwork supplies the visual setting rather than a historical combat ruleset.

## Core loop

1. Observe the approaching crocodiles: their side, height, distance and color.
2. Move vertically to line up the spear; in spell 32, turn toward the threat.
3. Choose a plain or heka thrust according to the crocodile's color.
4. Time the strike as its snout reaches the spear tip.
5. Read the feedback: the crocodile turns back, the bearer takes a bite, or a mistake ends the encounter.
6. Repeat through the remaining waves, then enter the other encounter. After a defeat, restart and try again.

The repeated decision is which threat to meet next and when to commit to a thrust. Movement, facing, color matching and attack timing share the same combat space.

## Interfaces

### Human interface

The game retains the original papyrus scene, artwork, camera, arena animations and HUD. The scroll serves as the encounter-selection interface: walking brings the player to a vignette, and clicking its crocodiles opens combat. The combat view shows the spear-bearer, moving crocodiles, red heka cues and health signs. The spear animation and crocodile reactions provide action feedback. The HUD supplies restart, **Journal** and **Hint** controls; the Journal opens over the scene.

Screenshots are pending. Useful captures would show the scroll with the HUD, spell 31 with its health and heka cues, and spell 32 with threats on both sides. Captures should come from the running game and be stored outside the project, as required by AGENTS.md. Source artwork alone is not a screenshot of the interface.

### Agent interface

Human, baseline, model and replay all use the same Godot scene and combat rules. The automated interface wraps the scene through [episode.gd](godot/scripts/episode.gd) and exposes five operations: `reset`, `observe`, `legal_actions`, `step` and `outcome`.

An agent submits a control combination such as:

```json
{"move": -1, "face": 0, "thrust": true, "heka": false}
```

`move` selects up, neutral or down; `face` selects left, unchanged or right. Spell 31 requires `face: 0`. Each action advances six frames at a fixed 1/60-second step, or 0.1 seconds of simulation. Combat pauses while the model selects its next action.

Agents receive structured observations of visible crocodiles, player position and facing, spear geometry, health, progress and feedback. They do not receive RNG state, future spawn schedules or engine objects. The engine validates actions and determines the outcome. See the [README interface specification](README.md#machine-interface-and-information-boundary) for details.
