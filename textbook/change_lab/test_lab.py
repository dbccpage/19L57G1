"""Check teaching artifacts and input boundaries; AuthorityEffect: None."""
from dataclasses import replace
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from run_lab import SOURCE, HISTORY, check_recorded, expect_natural_encoding, passage
from build_results import render


class PassageLessonTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("recorded_lab.json", "SOURCE_MAP.md"):
            shutil.copyfile(SOURCE / name, self.root / name)

    def change(self, mutate):
        path = self.root / "recorded_lab.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        mutate(data)
        path.write_text(json.dumps(data), encoding="utf-8")

    def test_refinement_is_not_silently_given_a_license_gate(self):
        self.change(lambda d: d["operations"]["two_pairs_1_0_0"]["refine_C"].update(changed=False))
        with self.assertRaisesRegex(ValueError, "Recorded passage lesson differs"):
            check_recorded(self.root)

    def test_dropped_singleton_proposal_is_refused(self):
        self.change(lambda d: d["strong"]["singleton_proposals"].pop())
        with self.assertRaisesRegex(ValueError, "Recorded passage lesson differs"):
            check_recorded(self.root)

    def test_source_map_numbers_are_checked(self):
        path = self.root / "SOURCE_MAP.md"
        path.write_text(path.read_text(encoding="utf-8").replace("| All three pairs protected | 3 | 0 | 2 | 4 |", "| All three pairs protected | 3 | 99 | 2 | 4 |"), encoding="utf-8")
        with patch("run_lab.SOURCE", self.root):
            with self.assertRaisesRegex(ValueError, "population table differs"):
                check_recorded(self.root)

    def test_bundle_contains_current_recorded_cases(self):
        self.assertEqual((SOURCE / "results.html").read_text(encoding="utf-8"), render(SOURCE))

    def test_natural_encoding_boundary_refuses_negative_values(self):
        base = passage.preplay(HISTORY, passage.GENESIS_P)
        for bad in (replace(base, budget=-1), replace(base, obs=((-1,),)), replace(base, wit=((-1, 2),)), replace(base, occ=(-1, 20, 30))):
            with self.assertRaises(ValueError):
                expect_natural_encoding(bad)


if __name__ == "__main__":
    unittest.main()
