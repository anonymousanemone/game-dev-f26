extends RefCounted
const ENCOUNTERS := [
	{"id": "e31", "tag": "Crocodiles", "boxes": ["e31"], "kind": "crocs", "spear": "spear31", "task": 0, "tutorial": true,
		"foes": ["c31a", "c31b", "c31c", "c31d"], "first_speed": 120.0, "break": 6.0,
		# `waves` instead of one count: the lesson, a break while the heka word starts to flash, then
		# a wave with red ones (`red_order`: which launches come red, in order); each crocodile of a
		# wave `ramp` faster than the one before. A lost fight starts again from the first wave.
		"waves": [
			{"count": 3, "speed": 180.0, "ramp": 0.01, "interval": 3.0, "at_once": 1},
			{"count": 6, "speed": 200.0, "ramp": 0.01, "interval": 2.2, "at_once": 2, "red_order": [false, true, false, true, true, false]},
		],
		"caption": [5189, 6667]},
	{"id": "e32", "tag": "Crocodiles", "boxes": ["e32"], "kind": "crocs", "spear": "spear32", "task": 0,
		"foes": ["c32a", "c32b", "c32c", "c32d"], "both_sides": true,
		# harder than 31 and losable, but always possible: each crocodile is `ramp` faster than the
		# one before (210 -> about 420), and none reaches him within `min_gap` s of the one before
		"waves": [{"count": 14, "speed": 180.0, "ramp": 0.01, "interval": 0.8, "at_once": 2, "red": 0.35, "min_gap": 0.9}],
		"caption": [3944, 5168]},
]
