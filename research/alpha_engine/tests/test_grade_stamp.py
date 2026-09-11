"""A partial-Decide grade stamp is not a License."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness import GradeIsNotLicenseError, license_from_grade  # noqa: E402


class GradeStamp(unittest.TestCase):
    def test_unique_delta_stamp_is_not_a_license(self) -> None:
        with self.assertRaises(GradeIsNotLicenseError):
            license_from_grade({"grade": "UniqueDelta"})

    def test_tie_stamp_is_not_a_license(self) -> None:
        with self.assertRaises(GradeIsNotLicenseError):
            license_from_grade({"grade": "Tie"})

    def test_unique_class_stamp_is_not_a_license(self) -> None:
        with self.assertRaises(GradeIsNotLicenseError):
            license_from_grade({"grade": "UniqueClass"})

    def test_none_stamp_is_not_a_license(self) -> None:
        with self.assertRaises(GradeIsNotLicenseError):
            license_from_grade(None)

    def test_harness_does_not_import_partial_decide(self) -> None:
        text = (
            Path(__file__).resolve().parents[1] / "harness.py"
        ).read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                self.assertNotIn("partial_decide", stripped)


if __name__ == "__main__":
    unittest.main()
