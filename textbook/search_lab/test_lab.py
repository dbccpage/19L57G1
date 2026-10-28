"""Refuse dropped ties and false annotations in the teaching records.

AuthorityEffect: None. The source-backed checks are finite evidence.
"""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from run_lab import SOURCE, check_recorded
from build_results import build, render


class LessonRecords(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        for name in ("recorded_lab.json", "reading_L_mu1_rounds5.json", "results.template.html", "SOURCE_MAP.md"):
            shutil.copyfile(SOURCE / name, self.directory / name)

    def edit_packet(self, mutate):
        path = self.directory / "recorded_lab.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        mutate(data)
        path.write_text(json.dumps(data), encoding="utf-8")

    def test_dropped_tie_fails_even_when_the_export_still_replays(self):
        self.edit_packet(lambda data: data["cases"]["L_arity_2"]["results"]["mu1"]["raw_minima"].pop())
        with self.assertRaisesRegex(ValueError, "Recorded lesson data differs"):
            check_recorded(self.directory)

    def test_changed_price_fails_the_full_record_check(self):
        path = self.directory / "reading_L_mu1_rounds5.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["edges"][0]["cost"] = [999, 999]
        path.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Recorded export differs"):
            check_recorded(self.directory)

    def test_bundle_is_self_contained_and_preserves_download_links(self):
        output = self.directory / "result.html"
        build(self.directory, output, {"reading_L_mu1_rounds5.json": "https://example.invalid/graph"})
        text = output.read_text(encoding="utf-8")
        self.assertNotIn("__LAB_PACKET__", text)
        self.assertNotIn("fetch(", text)
        self.assertIn('href="https://example.invalid/graph"', text)
        self.assertIn('"changed_cost_metadata":true', text)

    def test_committed_results_desk_is_current(self):
        self.assertEqual((SOURCE / "results.html").read_text(encoding="utf-8"), render(SOURCE))

    def test_stale_numbers_in_the_lesson_table_are_refused(self):
        path = self.directory / "SOURCE_MAP.md"
        text = path.read_text(encoding="utf-8").replace("| L | 2 | 14 | 6 | 3 |", "| L | 2 | 14 | 6 | 99 |")
        path.write_text(text, encoding="utf-8")
        with patch("run_lab.SOURCE", self.directory):
            with self.assertRaisesRegex(ValueError, "lesson population table differs"):
                check_recorded(self.directory)


if __name__ == "__main__":
    unittest.main()
