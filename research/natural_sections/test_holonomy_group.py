"""Tests for the k-particle holonomy group: the permutation helpers, the hop
rule, agreement with the two-label flip bit, the pre-registered k = 3
predictions, and the separation of parity from the fixed pair."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import tempfile
import unittest
from pathlib import Path

import holonomy_fixture as two
import holonomy_group as hg
import run_holonomy_group as runner

TREE = Path(__file__).resolve().parent


class PermutationTests(unittest.TestCase):
    def test_compose_inverse_and_parity(self) -> None:
        c3 = (1, 2, 0)
        t01 = (1, 0, 2)
        t12 = (0, 2, 1)
        self.assertEqual(hg.compose(c3, hg.inverse(c3)), hg.identity(3))
        self.assertEqual(hg.compose(hg.compose(c3, c3), c3), hg.identity(3))
        self.assertTrue(hg.is_even(hg.identity(3)))
        self.assertTrue(hg.is_even(c3))
        self.assertFalse(hg.is_even(t01))
        self.assertEqual(hg.compose(t01, t12), c3)  # t12 first, then t01

    def test_closure_is_a_group(self) -> None:
        group = hg.closure([(1, 0, 2)], 3)
        self.assertEqual(group, [(0, 1, 2), (1, 0, 2)])
        full = hg.closure([(1, 0, 2), (0, 2, 1)], 3)
        self.assertEqual(len(full), 6)
        for g in full:
            self.assertIn(hg.inverse(g), full)
            for h in full:
                self.assertIn(hg.compose(g, h), full)


class HopRuleTests(unittest.TestCase):
    def test_k2_hop_perm_is_the_flip_bit_on_every_hop(self) -> None:
        for name, sites, edges in two.fixtures():
            objs = [(x, y) for x, y in two.configurations(sites)]
            for a in objs:
                for b in objs:
                    is_hop, flip = two.hop(edges, a, b)
                    perm = hg.hop_perm(edges, a, b)
                    self.assertEqual(perm is not None, is_hop, (name, a, b))
                    if perm is not None:
                        self.assertEqual(perm == (1, 0), flip, (name, a, b))

    def test_square_hole_circulation_is_a_3_cycle(self) -> None:
        edges = two.grid(2, 2)
        walk = [(0, 1, 2), (0, 2, 3), (1, 2, 3), (0, 1, 3), (0, 1, 2)]
        total = hg.identity(3)
        for a, b in zip(walk, walk[1:]):
            perm = hg.hop_perm(edges, a, b)
            self.assertIsNotNone(perm, (a, b))
            assert perm is not None
            total = hg.compose(perm, total)
        self.assertEqual(total, (1, 2, 0))
        self.assertTrue(hg.is_even(total))

    def test_hops_and_non_hops(self) -> None:
        edges = two.grid(2, 2)
        self.assertIsNone(hg.hop_perm(edges, (0, 1, 2), (0, 1, 2)))  # nothing moved
        self.assertIsNone(hg.hop_perm(two.chain(5), (0, 1, 2), (0, 3, 4)))  # two moved
        self.assertIsNone(hg.hop_perm(two.chain(5), (0, 1, 2), (0, 1, 4)))  # 2 !~ 4
        # 1 -> 3 on the square: the mover keeps index 2's neighbour order? No:
        # {0,1,2} -> {0,2,3}: particle at 1 (index 1) lands at 3 (index 2),
        # the particle at 2 (index 2) becomes index 1.
        self.assertEqual(hg.hop_perm(edges, (0, 1, 2), (0, 2, 3)), (0, 2, 1))
        # 2 -> 3 on the chain: order preserved, identity.
        self.assertEqual(hg.hop_perm(two.chain(4), (0, 1, 2), (0, 1, 3)), (0, 1, 2))


class AgreementTests(unittest.TestCase):
    def test_k2_verdicts_agree_with_the_flip_bit_receipt(self) -> None:
        for name, sites, edges in two.fixtures():
            self.assertEqual(
                hg.analyse_k(name, sites, edges, 2).section_exists,
                two.analyse(name, sites, edges).section_exists,
                name,
            )

    def test_at_k2_parity_and_fixed_pair_never_come_apart(self) -> None:
        for name, sites, edges in two.fixtures():
            v = hg.analyse_k(name, sites, edges, 2)
            self.assertEqual(v.section_exists, v.parity_says_clean, name)


class PredictionK3Tests(unittest.TestCase):
    """The k = 3 predictions written into STATUS.md before the run."""

    def verdict(self, name: str) -> hg.VerdictK:
        for n, sites, edges in two.fixtures():
            if n == name:
                return hg.analyse_k(name, sites, edges, 3)
        raise AssertionError(name)

    def test_chain_P2_is_vacuous(self) -> None:
        v = self.verdict("chain_P2")
        self.assertEqual(v.objects, 0)
        self.assertTrue(v.section_exists)

    def test_frozen_fixtures_have_one_object_and_a_section(self) -> None:
        for name in ("chain_P3", "triangle_C3"):
            v = self.verdict(name)
            self.assertEqual(v.objects, 1)
            self.assertEqual(v.arrows, 0)
            self.assertTrue(v.section_exists, name)

    def test_chains_have_trivial_holonomy(self) -> None:
        for name in ("chain_P4", "chain_P5", "chain_P6"):
            v = self.verdict(name)
            self.assertEqual(len(v.components), 1, name)
            self.assertTrue(v.components[0].trivial, name)
            self.assertEqual(v.components[0].common_fixed, (0, 1, 2))
            self.assertTrue(v.section_exists, name)

    def test_square_separates_parity_from_the_fixed_pair(self) -> None:
        v = self.verdict("square_2x2")
        self.assertEqual(len(v.components), 1)
        c = v.components[0]
        self.assertEqual(c.group_order, 3)
        self.assertTrue(c.all_even)
        self.assertEqual(c.common_fixed, ())
        self.assertFalse(c.fixed_pair_exists)
        self.assertTrue(v.parity_says_clean)
        self.assertFalse(v.section_exists)
        self.assertEqual(c.witness_perm, (1, 2, 0))

    def test_ladder_is_the_full_symmetric_group(self) -> None:
        v = self.verdict("ladder_2x3")
        self.assertEqual(len(v.components), 1)
        self.assertEqual(v.components[0].group_order, 6)
        self.assertFalse(v.parity_says_clean)
        self.assertFalse(v.section_exists)

    def test_star_reverses_its_k2_verdict(self) -> None:
        v = self.verdict("star_K13")
        self.assertEqual(len(v.components), 1)
        self.assertTrue(v.components[0].trivial)
        self.assertTrue(v.section_exists)
        self.assertFalse(two.analyse("star_K13", 4, two.star(3)).section_exists)

    def test_witness_walks_compose_to_the_witness_permutation(self) -> None:
        for name, sites, edges in two.fixtures():
            v = hg.analyse_k(name, sites, edges, 3)
            for c in v.components:
                if c.witness is None:
                    continue
                self.assertEqual(c.witness[0], c.base)
                self.assertEqual(c.witness[-1], c.base)
                total = hg.identity(3)
                for a, b in zip(c.witness, c.witness[1:]):
                    perm = hg.hop_perm(v.edges, a, b)
                    self.assertIsNotNone(perm, (name, a, b))
                    assert perm is not None
                    total = hg.compose(perm, total)
                self.assertEqual(total, c.witness_perm, name)
                self.assertNotEqual(total, hg.identity(3), name)


class ReceiptTests(unittest.TestCase):
    def test_receipt_replays_byte_identically_and_matches_the_committed_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=TREE) as scratch:
            a = Path(scratch) / "a"
            b = Path(scratch) / "b"
            self.assertEqual(runner.main(["--out", str(a)]), 0)
            self.assertEqual(runner.main(["--out", str(b)]), 0)
            one = (a / "holonomy_group.json").read_bytes()
            self.assertEqual(one, (b / "holonomy_group.json").read_bytes())
            self.assertEqual(one, (TREE / "receipts" / "holonomy_group.json").read_bytes())

    def test_runner_refuses_an_output_directory_outside_the_tree(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            self.assertEqual(runner.main(["--out", outside]), 1)

    def test_summary_matches_the_predictions(self) -> None:
        report = hg.report()
        self.assertTrue(all(hg.k2_agreement().values()))
        self.assertEqual(report["k2_agrees_with_flip_bit_receipt"], hg.k2_agreement())
        self.assertEqual(report["summary_k3"], hg.summary_k3())
        self.assertEqual(
            hg.summary_k3(),
            {
                "chain_P2": {"section_exists": True, "parity_says_clean": True},
                "chain_P3": {"section_exists": True, "parity_says_clean": True},
                "chain_P4": {"section_exists": True, "parity_says_clean": True},
                "chain_P5": {"section_exists": True, "parity_says_clean": True},
                "chain_P6": {"section_exists": True, "parity_says_clean": True},
                "square_2x2": {"section_exists": False, "parity_says_clean": True},
                "ladder_2x3": {"section_exists": False, "parity_says_clean": False},
                "star_K13": {"section_exists": True, "parity_says_clean": True},
                "triangle_C3": {"section_exists": True, "parity_says_clean": True},
            },
        )


if __name__ == "__main__":
    unittest.main()
