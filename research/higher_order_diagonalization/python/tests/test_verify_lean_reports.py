"""Primed theorem names in this tree's Lean axiom reports.

A Lean name may end in one or more apostrophes, and `#print axioms` quotes
the name in apostrophes, so the report of `n''` reads `'n'''`.  The
quote-blind capture `'([^']+)'` cannot read such a report; the non-greedy
capture anchored on the report phrase can.  This case covers names ending in
zero, one and two apostrophes.  Added 2026-09-18.

AuthorityEffect: None.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock

TREE = Path(__file__).resolve().parents[2]
if str(TREE) not in sys.path:
    sys.path.insert(0, str(TREE))

import verify_lean  # noqa: E402

NAMES = ("Probe.step", "Probe.step'", "Probe.step''")
REPORT = (
    "info: Inventory.lean:1:0: 'Probe.step' does not depend on any axioms\n"
    "info: Inventory.lean:2:0: 'Probe.step'' depends on axioms: [propext]\n"
    "info: Inventory.lean:3:0: 'Probe.step''' depends on axioms: "
    "[propext, Quot.sound]\n"
)


class PrimedReportNames(unittest.TestCase):
    def test_each_report_pattern_reads_primed_names(self) -> None:
        self.assertEqual(verify_lean.NO_AXIOMS.findall(REPORT), ["Probe.step"])
        self.assertEqual(
            verify_lean.HAS_AXIOMS.findall(REPORT),
            [("Probe.step'", "propext"), ("Probe.step''", "propext, Quot.sound")],
        )

    def test_population_check_accepts_primed_names(self) -> None:
        with mock.patch.object(verify_lean, "THEOREMS", NAMES):
            parsed = verify_lean.parse_axioms(REPORT)
        self.assertEqual(
            parsed,
            {
                "Probe.step": [],
                "Probe.step'": ["propext"],
                "Probe.step''": ["Quot.sound", "propext"],
            },
        )


if __name__ == "__main__":
    unittest.main()
