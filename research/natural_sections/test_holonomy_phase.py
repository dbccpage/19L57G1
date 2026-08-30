"""Tests for the phase fibre: the wreath-product arithmetic, the hop rule, the
refusal of a continuous phase, the pre-registered predictions at the
component level, gauge invariance, periodicity, and compatibility with
refinement of the modulus."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import tempfile
import unittest
from pathlib import Path

import holonomy_fixture as two
import holonomy_group as hg
import holonomy_phase as hp
import run_holonomy_phase as runner

TREE = Path(__file__).resolve().parent


class ArithmeticTests(unittest.TestCase):
    def test_refuses_a_continuous_phase_by_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "REFUSED: a continuous phase"):
            hp.refuse_continuous_phase()

    def test_compose_and_inverse_in_the_wreath_product(self) -> None:
        g = ((1, 0), (1, 0))  # swap, register 0 gains 1
        e = hp.identity(2)
        self.assertEqual(hp.compose(g, hp.inverse(g, 4), 4), e)
        self.assertEqual(hp.compose(hp.inverse(g, 4), g, 4), e)
        gg = hp.compose(g, g, 4)
        self.assertEqual(gg, ((0, 1), (1, 1)))  # the pure phase (1, 1)
        g4 = hp.compose(gg, gg, 4)
        self.assertEqual(g4, ((0, 1), (2, 2)))
        self.assertEqual(hp.compose(g4, g4, 4), e)

    def test_connection_is_antisymmetric_and_gauge_keeps_flux(self) -> None:
        conn = hp.square_conn(1)
        self.assertEqual(conn[(0, 1)], 1)
        self.assertEqual(conn[(1, 0)], 3)
        cycle = [0, 1, 3, 2, 0]
        self.assertEqual(hp.flux(conn, cycle, 4), 1)
        conn2 = hp.gauge_transform(conn, (0, 1, 2, 3), 4)
        self.assertNotEqual(conn2, conn)
        self.assertEqual(hp.flux(conn2, cycle, 4), 1)
        self.assertEqual(hp.flux(hp.tree_conn(two.chain(4)), [0, 1, 2, 1, 0], 4), 0)

    def test_hop_shifts_only_the_mover(self) -> None:
        conn = hp.square_conn(1)
        elem = hp.hop(two.grid(2, 2), conn, 4, (0, 2), (1, 2))  # 0 -> 1 with 2 still
        self.assertEqual(elem, ((0, 1), (1, 0)))
        elem = hp.hop(two.grid(2, 2), conn, 4, (1, 2), (0, 1))  # 2 -> 0: flips, phase 0
        self.assertEqual(elem, ((1, 0), (0, 0)))
        self.assertIsNone(hp.hop(two.grid(2, 2), conn, 4, (0, 1), (2, 3)))


class PredictionTests(unittest.TestCase):
    """The predictions written into STATUS.md before the run, at the component level."""

    def test_trees_with_nonzero_edge_phases_are_trivial(self) -> None:
        for name, sites, edges, conn, k, modulus in hp.fixtures():
            if not name.endswith("tree_phases"):
                continue
            v = hp.analyse_phase(name, sites, edges, conn, k, modulus)
            self.assertTrue(v.section_exists, name)
            for c in v.components:
                self.assertEqual(c.group_order, 1, name)

    def test_square_two_particles_obstructed_for_every_flux(self) -> None:
        for phi in range(4):
            v = hp.analyse_phase("s", 4, two.grid(2, 2), hp.square_conn(phi), 2, 4)
            self.assertFalse(v.section_exists, phi)
            c = v.components[0]
            self.assertFalse(c.permutation_part_trivial)
            self.assertEqual(c.phase_part_trivial, phi == 0)
        # flux 1: the generator squared is the pure phase (1, 1)
        c = hp.analyse_phase("s", 4, two.grid(2, 2), hp.square_conn(1), 2, 4).components[0]
        self.assertEqual(c.group_order, 8)

    def test_one_on_each_is_the_pure_phase_obstruction(self) -> None:
        for phi in range(5):
            c = hp.one_on_each(phi, 4)
            self.assertEqual(c.size, 8)
            self.assertTrue(c.permutation_part_trivial, phi)
            self.assertEqual(c.fixed_pair_exists, phi % 4 == 0, phi)
            self.assertEqual(c.phase_part_trivial, phi % 4 == 0, phi)
        self.assertEqual(hp.one_on_each(1, 4).group_order, 4)
        self.assertEqual(hp.one_on_each(2, 4).group_order, 2)
        # The witness generator is a pure phase on the square particle's register,
        # +1 or -1 (= 3) depending on which way the breadth-first tree crosses
        # the flux edge; the edge particle's register is untouched.
        witness = hp.one_on_each(1, 4).witness_elem
        assert witness is not None
        self.assertEqual(witness[0], (0, 1))
        self.assertIn(witness[1], [(1, 0), (3, 0)])

    def test_frozen_pair_is_immune_to_flux(self) -> None:
        for phi in range(4):
            v = hp.analyse_phase(
                "e", 6, hg.square_plus_edge(), hp.square_edge_conn(phi), 4, 4
            )
            by_base = {c.base: c for c in v.components}
            frozen_pair = by_base[(0, 1, 4, 5)]
            self.assertTrue(frozen_pair.fixed_pair_exists, phi)
            self.assertEqual(frozen_pair.common_fixed_with_zero_shift, (2, 3))
            self.assertFalse(by_base[(0, 1, 2, 4)].fixed_pair_exists, phi)

    def test_gauge_invariance_periodicity_and_refinement(self) -> None:
        self.assertTrue(all(hp.gauge_check().values()))
        self.assertTrue(all(hp.periodicity_check().values()))
        self.assertTrue(all(hp.refinement_check().values()))

    def test_fixture_level_verdict_is_the_conjunction_over_components(self) -> None:
        """Recorded slip: the whole square-plus-edge fixture at k = 2 is always
        obstructed because of its both-on-square component; the question was
        about the one-on-each component and must be read there."""
        v = hp.analyse_phase("e", 6, hg.square_plus_edge(), hp.square_edge_conn(0), 2, 4)
        self.assertFalse(v.section_exists)
        by_base = {c.base: c for c in v.components}
        self.assertFalse(by_base[(0, 1)].fixed_pair_exists)
        self.assertTrue(by_base[(0, 4)].fixed_pair_exists)
        self.assertTrue(by_base[(4, 5)].fixed_pair_exists)


class ReceiptTests(unittest.TestCase):
    def test_receipt_replays_byte_identically_and_matches_the_committed_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=TREE) as scratch:
            a = Path(scratch) / "a"
            b = Path(scratch) / "b"
            self.assertEqual(runner.main(["--out", str(a)]), 0)
            self.assertEqual(runner.main(["--out", str(b)]), 0)
            one = (a / "holonomy_phase.json").read_bytes()
            self.assertEqual(one, (b / "holonomy_phase.json").read_bytes())
            self.assertEqual(one, (TREE / "receipts" / "holonomy_phase.json").read_bytes())

    def test_runner_refuses_an_output_directory_outside_the_tree(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            self.assertEqual(runner.main(["--out", outside]), 1)


if __name__ == "__main__":
    unittest.main()
