"""OV3 fixture, OV5 decision, OV6 pricing, OV7 gap, OV8 dual."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import inspect
import json
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

import decide
import diagram as dg
import dual
import gap
import pricing
import run_decide
import run_pricing

TREE = Path(__file__).resolve().parent


class Ov1PassivityTests(unittest.TestCase):
    def test_j_le_i_and_i_zero_forces_every_j(self) -> None:
        s = dg.patch3_section()
        i_all = dg.mass(s, dg.PATCH3_EDGES)
        j_all = dg.j_coord(s, dg.PATCH3_EDGES)
        self.assertLessEqual(j_all, i_all)
        j_partial = dg.j_coord(s, dg.PATCH3_EDGES[:4])
        self.assertLessEqual(j_partial, i_all)
        self.assertLessEqual(dg.j_coord(s, ()), i_all)
        visible: dg.Section = {0: (0, 0), 1: (1, 0)}
        vis_edges: tuple[dg.Edge, ...] = ((0, 1),)
        self.assertEqual(dg.mass(visible, vis_edges), 1)
        self.assertEqual(dg.j_coord(visible, vis_edges), 1)
        z: dg.Section = {i: (0, 0) for i in range(6)}
        self.assertEqual(dg.mass(z, dg.PATCH3_EDGES), 0)
        observers_j = [
            dg.j_coord(z, dg.PATCH3_EDGES),
            dg.j_coord(z, dg.PATCH3_EDGES[:3]),
            dg.j_coord(z, ()),
        ]
        self.assertTrue(all(j == 0 for j in observers_j))


class Patch3Tests(unittest.TestCase):
    def test_lean_section_has_mass_six_and_is_all_green(self) -> None:
        s = dg.patch3_section()
        self.assertEqual(dg.mass(s, dg.PATCH3_EDGES), 6)
        self.assertTrue(dg.all_green(s, dg.PATCH3_EDGES))
        self.assertEqual(len(dg.PATCH3_EDGES), 6)

    def test_scaled_sections_match_preregistered_masses(self) -> None:
        masses = [dg.mass(dg.patch3_scale_section(k), dg.PATCH3_EDGES) for k in range(1, 6)]
        self.assertEqual(masses, [6, 12, 18, 24, 30])
        for k in range(1, 6):
            self.assertTrue(dg.all_green(dg.patch3_scale_section(k), dg.PATCH3_EDGES))
            self.assertEqual(dg.j_coord(dg.patch3_scale_section(k), dg.PATCH3_EDGES), 0)
        self.assertEqual(dg.patch3_scale_section(1), dg.patch3_section())
        r = run_decide.report()
        self.assertEqual(r["patch3_scale_masses"], [6, 12, 18, 24, 30])
        self.assertTrue(r["patch3_scale_all_green"])

    def test_decision_returns_unsound_not_larger_than_lean_section(self) -> None:
        d = decide.decide(6, dg.PATCH3_EDGES, decide.patch3_watch(), bound=1)
        self.assertEqual(d["verdict"], "UNSOUND")
        assert isinstance(d["mass"], int)
        self.assertGreater(d["mass"], 0)
        self.assertLessEqual(d["mass"], 6)

    def test_trivial_kernels_are_sound_on_the_box(self) -> None:
        d = decide.decide_trivial_kernels(6, dg.PATCH3_EDGES, bound=1)
        self.assertEqual(d["verdict"], "SOUND")

    def test_identity_watch_all_green_forces_mass_zero(self) -> None:
        constant: dg.Section = {0: (1, 1), 1: (1, 1)}
        edges: tuple[dg.Edge, ...] = ((0, 1),)
        self.assertTrue(all(dg.cob(constant, e) == (0, 0) for e in edges))
        self.assertEqual(dg.mass(constant, edges), 0)
        self.assertTrue(dg.all_green(constant, edges, ((True, True),)))
        shifted: dg.Section = {0: (0, 0), 1: (0, 1)}
        self.assertFalse(dg.all_green(shifted, edges, ((True, True),)))
        self.assertGreater(dg.mass(shifted, edges), 0)

    def test_self_loop_is_sound_with_nontrivial_kernel(self) -> None:
        edges: tuple[dg.Edge, ...] = ((0, 0),)
        unwatched: decide.Watch = {(0, 0): (False, False)}
        d = decide.decide(1, edges, unwatched, bound=1)
        self.assertEqual(d["verdict"], "SOUND")
        self.assertEqual(dg.cob({0: (3, 4)}, (0, 0)), (0, 0))
        self.assertTrue(dg.kills((0, 1), True, False))
        self.assertNotEqual((0, 1), (0, 0))

    def test_patch3_generator_matches_box_minimum(self) -> None:
        watch = decide.patch3_watch()
        gen = decide.decide(6, dg.PATCH3_EDGES, watch, bound=1)
        box = decide.min_unsound_on_box(6, dg.PATCH3_EDGES, watch, bound=1)
        self.assertEqual(gen["verdict"], "UNSOUND")
        self.assertEqual(box["verdict"], "UNSOUND")
        self.assertEqual(gen["support"], box["support"])
        self.assertEqual(gen["mass"], box["mass"])
        self.assertEqual(gen["support"], 1)
        self.assertEqual(gen["mass"], 2)
        src = inspect.getsource(decide.decide)
        self.assertNotIn("min_unsound_on_box", src)
        self.assertNotIn("product(", src)


class DecisionIndependenceTests(unittest.TestCase):
    def test_decide_is_not_brute(self) -> None:
        src = inspect.getsource(decide.decide)
        self.assertNotIn("product(", src)
        self.assertIn("nullspace", src)
        self.assertIn("Fraction", inspect.getsource(decide))
        brute_src = inspect.getsource(decide.brute)
        self.assertIn("product(", brute_src)
        self.assertIn("all_green", brute_src)
        self.assertIn("mass", brute_src)
        self.assertNotEqual(decide.extra_watch_kills_kernel(), decide.patch3_watch())

    def test_nullspace_of_a_difference_contains_constants(self) -> None:
        matrix = decide.watch_matrix(2, ((0, 1),), {(0, 1): (True, False)})
        kernel = decide.nullspace(matrix, 4)
        flats = [tuple(vector) for vector in kernel]
        constant_x = (Fraction(1), Fraction(0), Fraction(1), Fraction(0))
        self.assertIn(constant_x, flats)

    def test_brute_agrees_on_twenty_seeded_diagrams(self) -> None:
        r = run_decide.report()
        self.assertEqual(r["seed"], 20260830)
        self.assertTrue(r["seeded_agree"])
        seeded = r["seeded"]
        assert isinstance(seeded, list)
        self.assertEqual(len(seeded), 20)
        for row in seeded:
            assert isinstance(row, dict)
            self.assertEqual(row["decide"], row["brute"])

    def test_receipt_replays(self) -> None:
        with tempfile.TemporaryDirectory(dir=TREE) as scratch:
            a = Path(scratch) / "a"
            self.assertEqual(run_decide.main(["--out", str(a)]), 0)
            self.assertEqual((a / "decide.json").read_bytes(), run_decide.render())
            self.assertEqual(
                (a / "decide.json").read_bytes(),
                (TREE / "receipts" / "decide.json").read_bytes(),
            )


class PricingGapDualTests(unittest.TestCase):
    def test_phi_zero_iff_both_fluxes_zero(self) -> None:
        src = inspect.getsource(pricing.table)
        self.assertIn("repeat=len(Edges)", src)
        r = pricing.report()
        expected = {2: 2**5, 3: 3**5, 4: 4**5}
        for key, n in (("Z2", 2), ("Z3", 3), ("Z4", 4)):
            block = r[key]
            assert isinstance(block, dict)
            self.assertEqual(block["n_cochains"], expected[n], key)
            self.assertTrue(block["phi_zero_iff_fluxes_zero"], key)
            self.assertEqual(block["zero_count"], block["flux_zero_count"], key)
            rows = block["rows"]
            assert isinstance(rows, list)
            self.assertEqual(len(rows), expected[n], key)
            for row in rows:
                assert isinstance(row, dict)
                self.assertEqual(
                    row["phi"] == 0,
                    row["flux1"] == 0 and row["flux2"] == 0,
                    key,
                )

    def test_gap_splits_and_sums_to_i_minus_maxj(self) -> None:
        s = dg.patch3_section()
        g = gap.gap(s, dg.PATCH3_EDGES, max_j=0)
        self.assertEqual(g["sum"], g["I"] - g["maxJ"])
        self.assertGreaterEqual(g["edge_loss"], 0)
        self.assertGreaterEqual(g["fragment"], 0)
        self.assertEqual(g["I"], 6)
        self.assertEqual(g["edge_loss"], 6)
        self.assertEqual(g["fragment"], 0)

    def test_split_observers_make_fragment_the_whole_gap(self) -> None:
        section: dg.Section = {0: (0, 0), 1: (1, 0), 2: (1, 0)}
        edges: tuple[dg.Edge, ...] = ((0, 1), (0, 2))
        observers = ((True, False), (False, True))
        g = gap.gap_from_observers(section, edges, observers)
        self.assertEqual(g["I"], 2)
        self.assertEqual(g["maxJ"], 1)
        self.assertEqual(g["edge_loss"], 0)
        self.assertEqual(g["fragment"], 1)
        self.assertEqual(g["sum"], g["I"] - g["maxJ"])
        self.assertEqual(gap.observer_j(section, edges, observers[0]), 1)
        self.assertEqual(gap.observer_j(section, edges, observers[1]), 1)

    def test_dual_certifies_patch3_section(self) -> None:
        s = dg.patch3_section()
        ys = [-1] * 6
        self.assertTrue(dual.certifies(ys, s, dg.PATCH3_EDGES))
        self.assertEqual(abs(dual.pairing(ys, s, dg.PATCH3_EDGES)), 6)

    def test_pricing_receipt_replays(self) -> None:
        with tempfile.TemporaryDirectory(dir=TREE) as scratch:
            a = Path(scratch) / "a"
            self.assertEqual(run_pricing.main(["--out", str(a)]), 0)
            self.assertEqual((a / "pricing.json").read_bytes(), run_pricing.render())
            self.assertEqual(
                (a / "pricing.json").read_bytes(),
                (TREE / "receipts" / "pricing.json").read_bytes(),
            )


if __name__ == "__main__":
    unittest.main()
