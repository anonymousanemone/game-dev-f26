# Sources and reuse

## Historical artwork

Carl Richard Lepsius, *Das Todtenbuch der Ägypter (nach dem hieroglyphischen Papyrus in Turin)*. Leipzig: Wigand, 1842. The midterm's crocodile-art locator is plate XVI, spells 31 and 32. Cite the digital edition using [DOI: 10.11588/propylaeumdok.00000467](https://doi.org/10.11588/propylaeumdok.00000467) or [URN: urn:nbn:de:bsz:16-propylaeumdok-4678](https://nbn-resolving.org/urn:nbn:de:bsz:16-propylaeumdok-4678), as requested by the repository.

### Public-domain status

The plates were first published in **1842** (Leipzig: Wigand). Lepsius died in 1884, so the edition's copyright term (the author's life plus 70 years under German and EU law, § 64 UrhG) ended at the close of 1954. In the United States, works published before 1931 are in the public domain. The underlying papyrus is ancient and was never under copyright.

A faithful scan or photograph of a public-domain two-dimensional work does not create a new copyright. German law says this explicitly in [§ 68 UrhG](https://www.gesetze-im-internet.de/urhg/__68.html): reproductions of public-domain visual works get no related-rights protection. That section implements Article 14 of the EU Directive 2019/790. In the United States, the same principle comes from *Bridgeman Art Library v. Corel Corp.*, 36 F. Supp. 2d 191 (S.D.N.Y. 1999). The Heidelberg digitization below therefore adds no new rights to the plate images, and the cropped plate artwork can be published in this repository.

### Heidelberg copy: verified digital-source provenance

The source URL supplied in the checklist is [Heidelberg's Propylaeum-DOK record 467](https://archiv.ub.uni-heidelberg.de/propylaeumdok/467/). Its catalog page and public OAI metadata were retrieved on October 26, 2026.

| Stage | Credit / evidence |
|---|---|
| Ancient source | Papyrus Turin 1791, dated by the catalog to the Ptolemaic period. |
| Printed edition | Carl Richard Lepsius; Leipzig: Wigand, 1842. This is the edition on which the modern numbering of spells 1–165 is based, according to the catalog. |
| Digital-version supplier | **Dr. Marcus Müller, Totenbuch-Projekt, University of Bonn.** The catalog credits him with supplying the digital version; it does not identify who operated the scanner or establish a digitization date. |
| Repository / host | **Universitätsbibliothek Heidelberg, Propylaeum-DOK**, collection Propylaeum-DOK-Retro / Ägyptologie. Deposited January 15, 2010; that is the repository deposit date, not a claimed scan date. |
| Download | [lepsius_todtenbuch.pdf](https://archiv.ub.uni-heidelberg.de/propylaeumdok/467/1/lepsius_todtenbuch.pdf), linked by that record. |
| Game adaptation | The midterm copies exported PNGs from the student's existing **Totenbuch** project. [Source hashes](reports/provenance/source-manifest.json) and [direct-extraction evidence](reports/provenance/direct-extraction.json) identify those actual files. No original MDP or replacement source scan was copied into this project. |

Suggested image credit: **Carl Richard Lepsius, *Das Todtenbuch der Ägypter*, 1842, plate XVI (spells 31–32); digital version supplied by Dr. Marcus Müller, Totenbuch-Projekt, University of Bonn; hosted by Universitätsbibliothek Heidelberg / Propylaeum-DOK, DOI 10.11588/propylaeumdok.00000467. Cropped and adapted in Totenbuch.** This includes the library/title/page elements requested in Heidelberg's [picture-credit guidance](https://www.ub.uni-heidelberg.de/Englisch/helios/digi/nutzung/).

The original source URL is now identified and its catalog provenance is verified. The PDF download returned a bot-check page during this audit, so no PDF checksum, scan-page inspection, or pixel match between this hosted PDF and the working PNGs is claimed. The plate locator above is retained from the game's existing source documentation. The verified local file chain begins with the existing Totenbuch exports, not a newly reconstructed cropping history. [Recorded metadata and retrieval hashes](reports/provenance/lepsius-provenance.json).

### Citation for the underlying papyrus

The Totenbuch archive identifies P. Turin 1791 as **TM 57201**, Museo Egizio, Turin, and lists spells 31 and 32 with vignettes. Its [object page](https://totenbuch.awk.nrw.de/objekt/tm57201) supplies this citation: **Totenbuchprojekt Bonn, TM 57201, https://totenbuch.awk.nrw.de/objekt/tm57201** (accessed October 26, 2026). Use this for the object description; retain the Lepsius DOI above for the printed/digitized edition used as the visual reference. The object page separately flags restricted image material.

The archive's [documentation](https://totenbuch.awk.nrw.de/projekt/dokumentation#OAIPMH) recommends stable `/objekt/tm…` addresses for citations. OAI-PMH supplies object metadata; unAPI supplies bibliographic exports, including BibTeX. Those interfaces document retrieval and citation, not permission to republish images. The documentation's persistent-citation section is the relevant guidance for this object.

### Other copied artwork

The copied files also include the original full strip, avatar, flesh health sign, spear animation sheet and HUD artwork. This Lepsius lookup does not establish independent provenance for every UI element.

## Font

**"Old Fax" by George Blackwell**, [georgeblackwell.itch.io/old-fax](https://georgeblackwell.itch.io/old-fax), licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). The license is the asset license listed on the itch.io page (checked November 3, 2026). The author's description allows personal and commercial use and asks for credit. The HUD uses it unmodified, as `godot/assets/fonts/OldFax.ttf`.

## Your original game and existing implementation

Source: [anonymousanemone/totenbuch-game](https://github.com/anonymousanemone/totenbuch-game), local working tree on 2026-10-26. The base Git commit was `228809a656ca0d20ba009c125bfcb533ee7d919c`; the working tree had uncommitted edits, so that commit alone does not identify everything copied. `reports/provenance/source-manifest.json` records actual original and destination hashes. `reports/provenance/inherited-crocodiles.patch` identifies the adaptations to the original combat file.

Extracted from your original game: `crocodiles.gd` combat, e31/e32 encounter dictionaries, the original scene transforms/metadata and exported spear animation metadata, PNG artwork, and shared spear timing/pose geometry from `dangers.gd`. Added for this submission: standalone completion flow, fixed-step JSON interface, deterministic shuffle, observation boundary, baseline, API player, evaluator, tests, replay, packaging and documentation.

The student identifies Totenbuch as their original game and authorized extracting these encounters for this midterm. Its combat rules are original design choices, not reconstructed rules from a third-party game. Existing implementation is credited to that original project; the source manifest and patch make the midterm extraction inspectable. No new blanket license has been assigned by the assistant. Historical plate/scanning provenance is recorded separately above.

## Runtime and provider

[Godot Engine](https://godotengine.org/license/) is a separately installed dependency; [Godot's third-party notices](https://godotengine.org/license/#thirdparty) apply if shipping an engine binary. This project ships source and assets, not a Godot binary. Python is also separately installed. The model adapter calls Google's [Vertex AI `generateContent` REST API](https://cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1/projects.locations.endpoints/generateContent) with Gemini 3.5 Flash-Lite, consulted 2026-11-03. It uses Python's standard library; no SDK code or provider credentials are copied.

## Direct scene extraction

The active game uses the original `godot/scenes/dangers.tscn`, with only unused
node/resource blocks removed. Every retained scene block and every copied PNG/font
is byte-for-byte original; `reports/provenance/direct-extraction.json` records the comparison.
The original camera, papyrus, HUD, avatar, captions and arena animation remain in
use. The earlier substitute scenes/resources were discarded. `episode.gd` is a
separate evaluation adapter around this original scene. `reports/provenance/extraction.patch`
records scene and controller changes against the source project.
