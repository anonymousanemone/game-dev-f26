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
