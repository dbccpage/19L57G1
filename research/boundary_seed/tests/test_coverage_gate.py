"""Adversarial tests for the tree-local coverage arithmetic."""

from __future__ import annotations

import unittest
from typing import Any

from check_coverage import percentages


class CoverageArithmeticTests(unittest.TestCase):
    def test_combined_percent_cannot_rescue_low_line_coverage(self) -> None:
        totals: dict[str, Any] = {
            "covered_lines": 94,
            "num_statements": 100,
            "covered_branches": 100,
            "num_branches": 100,
            "percent_covered": 97.0,
        }
        self.assertEqual(percentages(totals), (94.0, 100.0))

    def test_impossible_counters_are_refused(self) -> None:
        totals: dict[str, Any] = {
            "covered_lines": 101,
            "num_statements": 100,
            "covered_branches": 10,
            "num_branches": 10,
        }
        with self.assertRaisesRegex(ValueError, "impossible line counters"):
            percentages(totals)


if __name__ == "__main__":
    unittest.main()
