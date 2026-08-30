"""Tests for the refinement fixtures: verdicts invariant across subdivision
rounds, growth as expected, and the receipt."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import tempfile
import unittest
from pathlib import Path

import holonomy_fixture as two
import refinement as rf
import representation as rp
import run_refinement as runner

TREE = Path(__file__).resolve().parent


class PredictionTests(unittest.TestCase):
    def test_verdicts_never_move_across_rounds(self) -> None:
        for name, sites, edges, expected in (
            ("square", 4, two.grid(2, 2), False),
            ("chain", 4, two.chain(4), True),
            ("star", 4, two.star(3), False),
        ):
            rows = rf.rounds(sites, edges, 2)
            for row in rows:
                self.assertEqual(row["section_exists"], expected, (name, row["round"]))

    def test_growth_and_odd_generators(self) -> None:
        rows = rf.rounds(4, two.grid(2, 2), 2)
        self.assertEqual([r["objects"] for r in rows], [6, 14, 30])
        self.assertEqual([r["hops"] for r in rows], [8, 16, 32])
        self.assertEqual([r["odd_generators"] for r in rows], [2, 2, 2])

    def test_subdivide_preserves_cycle_parity_by_construction(self) -> None:
        objs: list[object] = [0, 1, 2]
        hops: list[rf.HopEdge] = [((0, 1), True), ((1, 2), False), ((0, 2), False)]
        even_before = rp.components_even(objs, hops)[0]  # type: ignore[arg-type]
        new_objs, new_hops = rf.subdivide(objs, hops)
        self.assertEqual(len(new_objs), 6)
        self.assertEqual(len(new_hops), 6)
        even_after = rp.components_even(new_objs, new_hops)[0]  # type: ignore[arg-type]
        self.assertEqual(even_before, even_after)
        self.assertFalse(even_before)

    def test_report_invariance_flags(self) -> None:
        r = rf.report()
        self.assertEqual(
            r["verdict_invariant_across_rounds"],
            {"square_2x2": True, "chain_P4": True, "star_K13": True},
        )


class ReceiptTests(unittest.TestCase):
    def test_receipt_replays_byte_identically_and_matches_the_committed_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=TREE) as scratch:
            a = Path(scratch) / "a"
            b = Path(scratch) / "b"
            self.assertEqual(runner.main(["--out", str(a)]), 0)
            self.assertEqual(runner.main(["--out", str(b)]), 0)
            one = (a / "refinement.json").read_bytes()
            self.assertEqual(one, (b / "refinement.json").read_bytes())
            self.assertEqual(one, (TREE / "receipts" / "refinement.json").read_bytes())

    def test_runner_refuses_an_output_directory_outside_the_tree(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            self.assertEqual(runner.main(["--out", outside]), 1)


if __name__ == "__main__":
    unittest.main()
