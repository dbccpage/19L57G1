"""Unit tests for cost cohomology and cellular homology computations.

Pins the algebraic topology invariants of the depth-3 move graph.
AuthorityEffect: None.
"""

from __future__ import annotations

import pathlib
import sys
import unittest

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
_CODE = str(REPO / "code")
_PDC = str(REPO / "research" / "path_dependent_cost")
for _p in (str(HERE), _CODE, _PDC):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from cohomology import compute_cohomology, native_candidate_matrix  # noqa: E402
import costs as ct  # noqa: E402
import exactness as ex  # noqa: E402
import movegraph as mg  # noqa: E402


class TestCostCohomology(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph = mg.build()
        cls.report = compute_cohomology(cls.graph)

    def test_move_graph_dimensions(self) -> None:
        rep = self.report
        self.assertEqual(rep.n_vertices, 262)
        self.assertEqual(rep.n_edges, 638)
        self.assertEqual(rep.n_components, 2)
        self.assertEqual(rep.dim_c1, 638)
        self.assertEqual(rep.dim_b1, 260)
        self.assertEqual(rep.dim_z1, 378)
        self.assertEqual(rep.dim_h1_quotient, 378)

    def test_cohomology_quotient_decomposition(self) -> None:
        rep = self.report
        self.assertEqual(rep.dim_waste_subspace, 232)
        self.assertEqual(rep.dim_order_subspace, 146)
        self.assertEqual(
            rep.dim_waste_subspace + rep.dim_order_subspace, rep.dim_h1_quotient
        )

    def test_pure_commuting_squares_span_order_subspace(self) -> None:
        rep = self.report
        self.assertEqual(rep.n_all_squares, 770)
        self.assertEqual(rep.n_pure_squares, 146)
        self.assertEqual(rep.rank_pure_squares, 146)
        self.assertTrue(rep.pure_squares_span_order_space)

    def test_cellular_2complex_homology(self) -> None:
        rep = self.report
        self.assertEqual(rep.rank_d2_all_squares, 324)
        self.assertEqual(rep.dim_h1_2complex, 54)
        # All 146 order directions are eliminated by the 2-cells;
        # remaining 54 degrees of freedom are uncancelled self-loops (waste).
        self.assertEqual(
            rep.dim_h1_2complex, rep.dim_waste_subspace - (rep.rank_d2_all_squares - rep.rank_pure_squares)
        )

    def test_rule_span_detects_commitment_growth(self) -> None:
        rep = self.report
        discs = rep.candidate_pure_discrepancies
        self.assertEqual(discs["rule_span"], 4)

        witness = rep.rule_span_witness
        self.assertIsNotNone(witness)
        r1 = witness["route_one"]
        r2 = witness["route_two"]
        assert isinstance(r1, list) and isinstance(r2, list)
        kinds = {
            tuple(str(k) for k, _ in r1),
            tuple(str(k) for k, _ in r2),
        }
        self.assertEqual(kinds, {("datum", "rule"), ("rule", "datum")})
        # The circulation difference is non-zero
        self.assertNotEqual(witness["route_one_total"], witness["route_two_total"])

    def test_native_order_cocycles_rank_4(self) -> None:
        rep = self.report
        self.assertEqual(rep.rank_native_order_cocycles, 4)

        discs = rep.candidate_pure_discrepancies
        self.assertEqual(discs["width_at_admission"], 16)
        self.assertEqual(discs["rule_span"], 4)
        self.assertEqual(discs["empty_admission"], 22)
        self.assertEqual(discs["mention_deficit"], 18)

    def test_exact_costs_vanish_on_all_pure_squares(self) -> None:
        rep = self.report
        discs = rep.candidate_pure_discrepancies
        self.assertEqual(discs["arity_debt"], 0)
        self.assertEqual(discs["context_opening"], 0)
        self.assertEqual(discs["reach"], 0)

    def test_item_count_vanishes_on_pure_squares(self) -> None:
        rep = self.report
        discs = rep.candidate_pure_discrepancies
        self.assertEqual(discs["item_count"], 0)


if __name__ == "__main__":
    unittest.main()
