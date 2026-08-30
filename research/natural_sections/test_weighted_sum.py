"""Tests for the weighted layer: the pre-registered predictions on the chain,
the square and the star; the orbit counterexample; every value; the receipt."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import tempfile
import unittest
from pathlib import Path

import holonomy_fixture as two
import run_weighted_sum as runner
import weighted_sum as ws

TREE = Path(__file__).resolve().parent


class LayerTests(unittest.TestCase):
    def test_closed_walks_are_closed_and_carry_their_holonomy(self) -> None:
        adj = ws.arrows(4, two.grid(2, 2), 2)
        base = sorted(adj)[0]
        walks = ws.closed_walks(adj, base, 4)
        self.assertIn(((), (0, 1)), walks)  # the empty walk, identity
        for walk, perm in walks:
            if walk:
                self.assertEqual(walk[0][0], base)
                self.assertEqual(walk[-1][1], base)
            self.assertIn(perm, [(0, 1), (1, 0)])
        exchange = ((base, (0, 3)), ((0, 3), (0, 2)), ((0, 2), (1, 2)), ((1, 2), base))
        self.assertIn((exchange, (1, 0)), walks)

    def test_weight_is_the_product_and_sign_weight_is_parity(self) -> None:
        edges = two.grid(2, 2)
        sign = ws.sign_amp(edges)
        exchange = (((0, 1), (0, 3)), ((0, 3), (0, 2)), ((0, 2), (1, 2)), ((1, 2), (0, 1)))
        self.assertEqual(ws.weight(exchange, ws.unit_amp), 1)
        self.assertEqual(ws.weight(exchange, sign), -1)
        self.assertEqual(ws.weight((), sign), 1)


class PredictionTests(unittest.TestCase):
    """Written into STATUS.md before the run."""

    def test_chain_twisted_equals_total_at_every_pair(self) -> None:
        r = ws.analyse("chain_P4_k2", 4, two.chain(4), 2, 6)
        for pair, v in r.pairs.items():
            self.assertEqual(v["twisted_unit"], r.total_unit, pair)
            self.assertEqual(v["twisted_sign"], r.total_sign, pair)
            self.assertEqual(v["movers"], 0)

    def test_square_twisted_below_total_and_sign_twisted_counts_even_walks(self) -> None:
        r = ws.analyse("square_2x2_k2", 4, two.grid(2, 2), 2, 6)
        for pair, v in r.pairs.items():
            self.assertLess(v["twisted_unit"], r.total_unit, pair)
            self.assertGreater(v["movers"], 0)
            # every mover on the square is an exchange (odd), so under sign
            # weights the twisted sum is the count of even walks and the
            # plain sum is even minus odd
            self.assertEqual(v["twisted_sign"], v["twisted_unit"])
            self.assertEqual(r.total_sign, v["twisted_unit"] - v["movers"])

    def test_star_twisted_below_total(self) -> None:
        r = ws.analyse("star_K13_k2", 4, two.star(3), 2, 6)
        for pair, v in r.pairs.items():
            self.assertLess(v["twisted_unit"], r.total_unit, pair)

    def test_orbit_counterexample(self) -> None:
        c = ws.orbit_counterexample()
        self.assertEqual(c["twisted_at_fixed"], 1)
        self.assertEqual(c["twisted_at_moved"], 0)

    def test_every_value_on_both_families(self) -> None:
        values = [-3, -1, 0, 2, 7]
        got = ws.every_value(values)
        self.assertEqual(got["square_2x2"], values)
        self.assertEqual(got["chain_P4"], values)


class ReceiptTests(unittest.TestCase):
    def test_receipt_replays_byte_identically_and_matches_the_committed_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=TREE) as scratch:
            a = Path(scratch) / "a"
            b = Path(scratch) / "b"
            self.assertEqual(runner.main(["--out", str(a)]), 0)
            self.assertEqual(runner.main(["--out", str(b)]), 0)
            one = (a / "weighted_sum.json").read_bytes()
            self.assertEqual(one, (b / "weighted_sum.json").read_bytes())
            self.assertEqual(one, (TREE / "receipts" / "weighted_sum.json").read_bytes())

    def test_runner_refuses_an_output_directory_outside_the_tree(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            self.assertEqual(runner.main(["--out", outside]), 1)


if __name__ == "__main__":
    unittest.main()
