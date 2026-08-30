"""Tests for the hop fixture: the pre-registered predictions, the hop rule,
the witnesses, the receipt, and the negative control that shows the flip
bit is what carries the obstruction."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import holonomy_fixture as hf
import run_holonomy_fixture as runner

TREE = Path(__file__).resolve().parent
SQUARE = [(0, 1), (0, 2), (1, 3), (2, 3)]


class HopRuleTests(unittest.TestCase):
    def test_the_four_hop_cases_and_their_flips(self) -> None:
        # stayer 0 keeps index false: y = 1 -> 3 (1~3), no flip
        self.assertEqual(hf.hop(SQUARE, (0, 1), (0, 3)), (True, False))
        # stayer 2 keeps index true: x = 0 -> 1 (0~1), no flip
        self.assertEqual(hf.hop(SQUARE, (0, 2), (1, 2)), (True, False))
        # y = 2 moves below the stayer 1 (2~0): flip
        self.assertEqual(hf.hop(SQUARE, (1, 2), (0, 1)), (True, True))
        # x = 0 moves above the stayer 1 (0~2): flip
        self.assertEqual(hf.hop(SQUARE, (0, 1), (1, 2)), (True, True))

    def test_non_hops(self) -> None:
        self.assertEqual(hf.hop(SQUARE, (0, 1), (0, 1)), (False, False))
        self.assertEqual(hf.hop(SQUARE, (0, 1), (2, 3)), (False, False))  # both moved
        self.assertEqual(hf.hop(SQUARE, (0, 1), (0, 2)), (False, False))  # 1 !~ 2
        self.assertEqual(hf.hop(hf.chain(4), (0, 1), (1, 2)), (False, False))  # 0 !~ 2


class PredictionTests(unittest.TestCase):
    """The predictions written into STATUS.md before the computation ran."""

    def test_every_open_chain_has_a_section(self) -> None:
        for n in range(2, 8):
            verdict = hf.analyse(f"chain_P{n}", n, hf.chain(n))
            self.assertTrue(verdict.section_exists, n)
            self.assertEqual(verdict.odd_generators, 0)
            self.assertIsNone(verdict.witness)
            self.assertEqual(verdict.reachable, verdict.objects)

    def test_square_ladder_star_triangle_have_none(self) -> None:
        for name, sites, edges in [
            ("square", 4, hf.grid(2, 2)),
            ("ladder", 6, hf.grid(2, 3)),
            ("star", 4, hf.star(3)),
            ("triangle", 3, [(0, 1), (1, 2), (0, 2)]),
        ]:
            verdict = hf.analyse(name, sites, edges)
            self.assertFalse(verdict.section_exists, name)
            self.assertIsNotNone(verdict.witness, name)

    def test_witnesses_are_closed_hop_walks_with_odd_parity(self) -> None:
        for name, sites, edges in hf.fixtures():
            verdict = hf.analyse(name, sites, edges)
            if verdict.witness is None:
                continue
            walk = verdict.witness
            self.assertEqual(walk[0], verdict.base)
            self.assertEqual(walk[-1], verdict.base)
            parity = 0
            for a, b in zip(walk, walk[1:]):
                is_hop, flip = hf.hop(verdict.edges, a, b)
                self.assertTrue(is_hop, (name, a, b))
                parity ^= int(flip)
            self.assertEqual(parity, 1, name)

    def test_the_lean_witnesses_are_the_receipt_witnesses(self) -> None:
        square = hf.analyse("square", 4, hf.grid(2, 2)).witness
        self.assertEqual(square, ((0, 1), (0, 3), (0, 2), (1, 2), (0, 1)))
        star = hf.analyse("star", 4, hf.star(3)).witness
        self.assertEqual(star, ((0, 1), (1, 3), (0, 3), (2, 3), (0, 2), (1, 2), (0, 1)))

    def test_negative_control_without_the_flip_bit_the_square_is_clean(self) -> None:
        """The cover: if no hop ever flips, every closed walk is the identity
        and the square comes out with a section.  This is the failure mode
        "a pass counted as no flip", exhibited on purpose."""
        real = hf.hop

        def never_flips(edges: object, a: hf.Config, b: hf.Config) -> tuple[bool, bool]:
            is_hop, _ = real(edges, a, b)  # type: ignore[arg-type]
            return (is_hop, False)

        with mock.patch.object(hf, "hop", never_flips):
            verdict = hf.analyse("square_cover", 4, hf.grid(2, 2))
        self.assertTrue(verdict.section_exists)

    def test_negative_control_one_spurious_flip_obstructs_the_chain(self) -> None:
        """The other failure mode, "a flip where nothing passed": a flip on
        ONE hop that lies on a cycle of the configuration graph.  On the
        chain 0-1-2-3 the objects {0,2},{0,3},{1,3},{1,2} form a 4-cycle;
        flipping the hop {0,2} <-> {0,3} makes that cycle odd."""
        real = hf.hop
        spurious = {((0, 2), (0, 3)), ((0, 3), (0, 2))}

        def one_flip(edges: object, a: hf.Config, b: hf.Config) -> tuple[bool, bool]:
            is_hop, flip = real(edges, a, b)  # type: ignore[arg-type]
            return (is_hop, flip or (a, b) in spurious)

        with mock.patch.object(hf, "hop", one_flip):
            verdict = hf.analyse("chain_spurious", 4, hf.chain(4))
        self.assertFalse(verdict.section_exists)
        self.assertIsNotNone(verdict.witness)

    def test_a_uniform_spurious_flip_is_a_gauge_not_an_obstruction(self) -> None:
        """Found by a failed first version of the control above, recorded
        rather than hidden: flipping EVERY hop leaves the chain clean.  A hop
        changes x + y by one, so the configuration graph is bipartite, every
        closed walk has even length, and a flip on every hop contributes an
        even parity.  A uniform relabelling of the fibre is absorbed by a
        section; only a flip that breaks the parity of some cycle obstructs."""
        real = hf.hop

        def always_flips(edges: object, a: hf.Config, b: hf.Config) -> tuple[bool, bool]:
            is_hop, _ = real(edges, a, b)  # type: ignore[arg-type]
            return (is_hop, is_hop)

        for n in range(3, 7):
            with mock.patch.object(hf, "hop", always_flips):
                verdict = hf.analyse(f"chain_all_flips_P{n}", n, hf.chain(n))
            self.assertTrue(verdict.section_exists, n)
        # With the real flips discarded and every hop flipped uniformly, even
        # the square is clean: the uniform flip is a gauge on every bipartite
        # configuration graph, and the square's obstruction lives entirely in
        # the non-uniform, position-computed flip bit.
        with mock.patch.object(hf, "hop", always_flips):
            square = hf.analyse("square_all_flips", 4, hf.grid(2, 2))
        self.assertTrue(square.section_exists)


class ReceiptTests(unittest.TestCase):
    def test_receipt_replays_byte_identically_and_matches_the_committed_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=TREE) as scratch:
            a = Path(scratch) / "a"
            b = Path(scratch) / "b"
            self.assertEqual(runner.main(["--out", str(a)]), 0)
            self.assertEqual(runner.main(["--out", str(b)]), 0)
            one = (a / "holonomy_fixture.json").read_bytes()
            self.assertEqual(one, (b / "holonomy_fixture.json").read_bytes())
            self.assertEqual(one, (TREE / "receipts" / "holonomy_fixture.json").read_bytes())
            self.assertNotIn(b"\r", one)

    def test_runner_refuses_an_output_directory_outside_the_tree(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            self.assertEqual(runner.main(["--out", outside]), 1)
            self.assertFalse((Path(outside) / "holonomy_fixture.json").exists())

    def test_summary_matches_the_predictions(self) -> None:
        self.assertEqual(hf.report()["summary"], hf.summary())
        self.assertEqual(
            hf.summary(),
            {
                "chain_P2": True,
                "chain_P3": True,
                "chain_P4": True,
                "chain_P5": True,
                "chain_P6": True,
                "square_2x2": False,
                "ladder_2x3": False,
                "star_K13": False,
                "triangle_C3": False,
            },
        )


if __name__ == "__main__":
    unittest.main()
