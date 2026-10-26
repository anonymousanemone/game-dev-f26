# Sources and reuse

## Historical artwork

Karl Richard Lepsius (editor), *Das Todtenbuch der Ägypter nach dem hieroglyphischen Papyrus in Turin*, Leipzig: Georg Wigand, 1842, plate XVI, spells 31 and 32. Bibliographic reference: [Heidelberg digitized volume](https://archiv.ub.uni-heidelberg.de/propylaeumdok/467/1/lepsius_todtenbuch.pdf). This is a reference to the historical volume, not a claim that the working sprites were downloaded directly from that URL during extraction.

The copied PNGs come from the existing Totenbuch project's exported artwork. They include the original full strip, avatar, crocodiles, heka signs, flesh health sign and spear animation sheet, plus the original HUD artwork. No MDP is included. The original `OldFax.ttf` font is copied to preserve the HUD. Its original source/reuse terms also need to be recorded before public submission. The old 1842 publication is historical artwork; a modern scan provider's terms and the exact original scan provenance still need to be recorded by the student before public submission. The available repository did not establish that chain conclusively. Do not treat this document as a verified license grant for a scan provider's material.

## Your original game and existing implementation

Source: [anonymousanemone/totenbuch-game](https://github.com/anonymousanemone/totenbuch-game), local working tree on 2026-10-26. The base Git commit was `228809a656ca0d20ba009c125bfcb533ee7d919c`; the working tree had uncommitted edits, so that commit alone does not identify everything copied. `reports/source-manifest.json` records actual original and destination hashes. `reports/inherited-crocodiles.patch` identifies the adaptations to the original combat file.

Extracted from your original game: `crocodiles.gd` combat, e31/e32 encounter dictionaries, the original scene transforms/metadata and exported spear animation metadata, PNG artwork, and shared spear timing/pose geometry from `dangers.gd`. Added for this submission: standalone completion flow, fixed-step JSON interface, deterministic shuffle, observation boundary, baseline, API player, evaluator, tests, replay, packaging and documentation.

The student identifies Totenbuch as their original game and authorized extracting these encounters for this midterm. Its combat rules are original design choices, not reconstructed rules from a third-party game. Existing implementation is credited to that original project; the source manifest and patch make the midterm extraction inspectable. No new blanket license has been assigned by the assistant. Historical plate/scanning provenance is recorded separately above.

## Runtime and provider

[Godot Engine](https://godotengine.org/license/) is a separately installed dependency; [Godot's third-party notices](https://godotengine.org/license/#thirdparty) apply if shipping an engine binary. This project ships source and assets, not a Godot binary. Python is also separately installed. The API adapter follows [OpenAI's text generation documentation](https://developers.openai.com/api/docs/guides/text), consulted 2026-10-26; no SDK code or provider credentials are copied.

The artwork source/reuse check remains incomplete until the exact scan provenance and applicable reuse terms are recorded. It is explicitly listed in the hand-in checklist.

## Direct scene extraction

The active game uses the original `godot/scenes/dangers.tscn`, with only unused
node/resource blocks removed. Every retained scene block and every copied PNG/font
is byte-for-byte original; `reports/direct-extraction.json` records the comparison.
The original camera, papyrus, HUD, avatar, captions and arena animation remain in
use. The earlier substitute scenes/resources were discarded. `episode.gd` is a
separate evaluation adapter around this original scene. `reports/extraction.patch`
records scene and controller changes against the source project.
