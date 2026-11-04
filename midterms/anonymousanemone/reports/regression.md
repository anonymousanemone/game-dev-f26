# Observed JSON-control regression

During setup on 2026-10-26, the first development baseline episode ended with
1200 invalid actions, score 0 and step_limit, although it submitted the documented
control objects. Godot JSON.parse_string represents JSON numbers as floats;
Dictionary/Array membership against the integer-built legal-action dictionaries
rejected those otherwise valid controls.

The fix validates exact keys, numeric control domains and real boolean types
explicitly in episode.gd::step. Fractional movement and boolean numeric controls
remain invalid. test_json_numeric_regression submits the actual JSON transport
shape and verifies acceptance and tutorial progression. The full development
baseline subsequently completed spell31 with zero invalid actions.

This is actual observed development behavior, not a hypothetical regression.
The final baseline artifacts are linked from EVALUATION.md; the failed early
run was a local diagnostic, not a model trial.

# Observed headless arena-width regression

On 2026-11-04 the baseline and the live model lost spell32 seed 30 on an
identical timeline: one crocodile turned back at step 16 and bites at steps 23,
31 and 35, despite different actions. A per-step dump of every crocodile showed
that they started only 30–300 world px from the bearer, and a copy's snout
appeared 29 px away.

Cause: headless Godot has no window and reported a square 1280×1280 viewport.
The arena width is `vis_w = vp.x / z`, with the zoom `z` fitted to the
viewport height. So every agent run had an arena of 1,187 instead of 2,471
world px, about half the width of the project's 1280×720 window.

The fix sets the root viewport to the project's base size in `episode.gd`
`_init` when the display server is headless. Windowed human play is unchanged.
`spacing_checks.gd` asserts the 1280×720 viewport and an arena wider than 2,400
px; both checks failed before the fix and pass after. With the fix, the
baseline wins all three development cases. Earlier agent results are kept
in EVALUATION.md as narrow-arena history.
