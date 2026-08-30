"""Tests for the re-presentation, deletion and cover computations, against the
predictions written into STATUS.md before the run."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import tempfile
import unittest
from pathlib import Path

import holonomy_fixture as two
import representation as rp
import run_representation as runner

TREE = Path(__file__).resolve().parent


class PredictionTests(unittest.TestCase):
    def test_pointwise_re_presentation_never_changes_the_class(self) -> None:
        for name, sites, edges in two.fixtures():
            if sites > 4:
                continue  # 2^15 re-presentations on the ladder is not the question
            r = rp.repres_all(sites, edges)
            self.assertTrue(r["class_invariant"], name)
            expected = r["re_presentations"] if r["original_has_section"] else 0
            self.assertEqual(r["with_section"], expected, name)
        square = rp.repres_all(4, two.grid(2, 2))
        self.assertEqual((square["re_presentations"], square["with_section"]), (64, 0))
        chain = rp.repres_all(4, two.chain(4))
        self.assertEqual((chain["re_presentations"], chain["with_section"]), (64, 64))

    def test_square_minimum_cut_is_two(self) -> None:
        d = rp.deletions(4, two.grid(2, 2))
        self.assertEqual(d["subsets"], 256)
        self.assertEqual(d["minimum_deletion"], 2)
        self.assertFalse(d["single_deletion_suffices"])
        minimal = d["minimal_deletion_sets"]
        assert isinstance(minimal, list)
        self.assertEqual(len(minimal), 8)
        # the two flipping hops form one of the minimal cuts
        hops = d["hops"]
        assert isinstance(hops, list)
        flips = [h for h in hops if h["flip"]]
        self.assertEqual(len(flips), 2)

    def test_chain_every_deletion_keeps_the_section(self) -> None:
        d = rp.deletions(4, two.chain(4))
        self.assertEqual(d["subsets_with_section"], d["subsets"])

    def test_star_single_deletion_suffices(self) -> None:
        """Not predicted; recorded as computed: the star's configuration graph
        carries one odd cycle, so cutting any one of its hops suffices."""
        d = rp.deletions(4, two.star(3))
        self.assertEqual(d["minimum_deletion"], 1)

    def test_cover_has_a_section_everywhere(self) -> None:
        for name, sites, edges in two.fixtures():
            if sites > 4:
                continue
            self.assertTrue(rp.cover(sites, edges)["section_exists"], name)

    def test_components_even_on_a_hand_made_odd_cycle(self) -> None:
        objs = [(0, 1), (0, 2), (1, 2)]
        hops = [(((0, 1), (0, 2)), False), (((0, 2), (1, 2)), False), (((0, 1), (1, 2)), True)]
        self.assertEqual(rp.components_even(objs, hops), (False, 1, 1))
        hops[2] = (((0, 1), (1, 2)), False)
        self.assertEqual(rp.components_even(objs, hops), (True, 1, 0))


class ReceiptTests(unittest.TestCase):
    def test_receipt_replays_byte_identically_and_matches_the_committed_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=TREE) as scratch:
            a = Path(scratch) / "a"
            b = Path(scratch) / "b"
            self.assertEqual(runner.main(["--out", str(a)]), 0)
            self.assertEqual(runner.main(["--out", str(b)]), 0)
            one = (a / "representation.json").read_bytes()
            self.assertEqual(one, (b / "representation.json").read_bytes())
            self.assertEqual(one, (TREE / "receipts" / "representation.json").read_bytes())

    def test_runner_refuses_an_output_directory_outside_the_tree(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            self.assertEqual(runner.main(["--out", outside]), 1)


if __name__ == "__main__":
    unittest.main()
