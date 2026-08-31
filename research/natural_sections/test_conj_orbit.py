"""Tests for the holonomy-orbit layer: the pre-registered P1 values on the
square at ``k = 2``, the conjugation machinery, and the receipt."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import tempfile
import unittest
from pathlib import Path

import conj_orbit as co
import holonomy_group as hg
import holonomy_fixture as two
import run_conj_orbit as runner
import weighted_sum as ws

TREE = Path(__file__).resolve().parent


class MachineryTests(unittest.TestCase):
    def test_conjugate_holonomy_is_the_conjugated_holonomy(self) -> None:
        """The holonomy of ``u ++ w ++ reverse(u)`` is ``pu^-1 . pw . pu``,
        for every ordered pair of closed walks up to length 4."""

        edges = two.grid(2, 2)
        adj = ws.arrows(4, edges, 2)
        base = sorted(adj)[0]
        walks = ws.closed_walks(adj, base, 4)
        for u, pu in walks:
            for w, pw in walks:
                got = co.walk_perm(edges, co.conjugate(u, w))
                want = hg.compose(hg.inverse(pu), hg.compose(pw, pu))
                self.assertEqual(got, want)

    def test_reverse_walk_reverses_and_walk_perm_matches_enumeration(self) -> None:
        edges = two.grid(2, 2)
        adj = ws.arrows(4, edges, 2)
        base = sorted(adj)[0]
        for w, perm in ws.closed_walks(adj, base, 4):
            self.assertEqual(co.walk_perm(edges, w), perm)
            self.assertEqual(co.reverse_walk(co.reverse_walk(w)), w)

    def test_holonomy_closure_generates_the_group(self) -> None:
        swap = (1, 0)
        self.assertEqual(co.holonomy_closure({swap}), {(0, 1), swap})
        self.assertEqual(co.holonomy_closure({(0, 1)}), {(0, 1)})


class PredictionTests(unittest.TestCase):
    """P1, written into STATUS.md before the run."""

    def setUp(self) -> None:
        self.report = co.report()

    def test_holonomy_group_is_identity_and_swap(self) -> None:
        square = self.report["square_k2"]
        assert isinstance(square, dict)
        self.assertEqual(square["closed_walks"], 147)
        self.assertEqual(square["group_order"], 2)
        self.assertEqual(square["holonomy_group"], [[0, 1], [1, 0]])

    def test_one_orbit_with_twisted_unit_95_at_both_members(self) -> None:
        square = self.report["square_k2"]
        assert isinstance(square, dict)
        orbits = square["orbits"]
        assert isinstance(orbits, list)
        self.assertEqual(len(orbits), 1)
        self.assertEqual(orbits[0]["orbit"], [[0, 1], [1, 0]])
        self.assertEqual(orbits[0]["twisted_unit"], [95, 95])
        self.assertTrue(orbits[0]["agree"])
        self.assertTrue(square["all_orbits_agree"])

    def test_mini_list_twisted_one_at_both_orbit_members_total_two(self) -> None:
        mini = self.report["mini_list"]
        assert isinstance(mini, dict)
        self.assertEqual(mini["twisted_unit"], {"0,1": 1, "1,0": 1})
        self.assertEqual(mini["total_unit"], 2)

    def test_unit_weighting_conjugation_closure_is_exhaustive_and_clean(self) -> None:
        closure = self.report["unit_conjugation_closure"]
        assert isinstance(closure, dict)
        self.assertEqual(closure["walks"], 19)
        self.assertEqual(closure["pairs"], 361)
        self.assertEqual(closure["violations"], 0)

    def test_cited_counterexample_names_the_kept_receipt_key(self) -> None:
        cited = self.report["cited_counterexample"]
        assert isinstance(cited, str)
        self.assertIn("orbit_counterexample", cited)
        # the cited countermodel is still in the weighted_sum receipt
        committed = (TREE / "receipts" / "weighted_sum.json").read_text(encoding="ascii")
        self.assertIn('"orbit_counterexample"', committed)


class ReceiptTests(unittest.TestCase):
    def test_receipt_replays_byte_identically_and_matches_the_committed_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=TREE) as scratch:
            a = Path(scratch) / "a"
            b = Path(scratch) / "b"
            self.assertEqual(runner.main(["--out", str(a)]), 0)
            self.assertEqual(runner.main(["--out", str(b)]), 0)
            one = (a / "conj_orbit.json").read_bytes()
            self.assertEqual(one, (b / "conj_orbit.json").read_bytes())
            self.assertEqual(one, (TREE / "receipts" / "conj_orbit.json").read_bytes())

    def test_runner_refuses_an_output_directory_outside_the_tree(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            self.assertEqual(runner.main(["--out", outside]), 1)


if __name__ == "__main__":
    unittest.main()
