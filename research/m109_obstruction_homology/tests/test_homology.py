"""Comprehensive test suite for Target M109: Higher Chain Complexes & Obstruction Homology."""

from __future__ import annotations

from fractions import Fraction
import pathlib
import sys
import unittest

HERE = pathlib.Path(__file__).resolve().parent
TARGET_DIR = HERE.parent
if str(TARGET_DIR) not in sys.path:
    sys.path.insert(0, str(TARGET_DIR))

import homology as hom  # noqa: E402


class TestExactRationalLinearAlgebra(unittest.TestCase):
    """Test exact rational linear algebra primitives over Q."""

    def test_to_fraction_refuses_float(self) -> None:
        with self.assertRaises(TypeError):
            hom.to_fraction(0.5)  # type: ignore[arg-type]
        self.assertEqual(hom.to_fraction(1), Fraction(1, 1))
        self.assertEqual(hom.to_fraction(Fraction(2, 3)), Fraction(2, 3))

    def test_rref_and_rank(self) -> None:
        # A 3x3 matrix of rank 2
        m = hom.to_fraction_matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ])
        r_mat, pivots, rank = hom.rref(m)
        self.assertEqual(rank, 2)
        self.assertEqual(pivots, [0, 1])
        # Verify rref properties
        self.assertEqual(r_mat[0][0], Fraction(1))
        self.assertEqual(r_mat[0][1], Fraction(0))
        self.assertEqual(r_mat[0][2], Fraction(-1))
        self.assertEqual(r_mat[1][0], Fraction(0))
        self.assertEqual(r_mat[1][1], Fraction(1))
        self.assertEqual(r_mat[1][2], Fraction(2))
        self.assertEqual(r_mat[2], [Fraction(0), Fraction(0), Fraction(0)])

    def test_kernel_basis_rank_nullity(self) -> None:
        # 2x4 matrix of rank 2, nullity must be 2
        m = hom.to_fraction_matrix([
            [1, 0, 2, -1],
            [0, 1, 1, 3],
        ])
        k_basis = hom.kernel_basis(m)
        self.assertEqual(len(k_basis), 2)
        for v in k_basis:
            prod = hom.matrix_vector_mul(m, v)
            self.assertTrue(all(x == 0 for x in prod))

    def test_column_space_basis(self) -> None:
        m = hom.to_fraction_matrix([
            [1, 2, 1],
            [2, 4, 2],
            [3, 6, 4],
        ])
        c_basis = hom.column_space_basis(m)
        self.assertEqual(len(c_basis), 2)
        self.assertEqual(hom.matrix_rank(m), 2)

    def test_quotient_basis(self) -> None:
        # Subspace Z of dimension 3, B of dimension 1 inside Z
        # Z = span(e1, e2, e3), B = span(e1 + e2)
        z_basis = [
            [Fraction(1), Fraction(0), Fraction(0)],
            [Fraction(0), Fraction(1), Fraction(0)],
            [Fraction(0), Fraction(0), Fraction(1)],
        ]
        b_basis = [
            [Fraction(1), Fraction(1), Fraction(0)],
        ]
        q_basis = hom.quotient_basis(z_basis, b_basis, 3)
        self.assertEqual(len(q_basis), 2)
        # B + Q must span full R^3
        full_mat = b_basis + q_basis
        self.assertEqual(hom.matrix_rank(full_mat), 3)


class TestGradedChainComplex(unittest.TestCase):
    """Test GradedChainComplex, boundary nilpotency, and homology."""

    def test_cycle_complex_nilpotency_and_betti(self) -> None:
        c4 = hom.build_cycle_complex(4)
        self.assertEqual(c4.max_grade, 1)
        self.assertEqual(c4.dimensions[0], 4)
        self.assertEqual(c4.dimensions[1], 4)
        nil = c4.verify_nilpotency()
        self.assertEqual(nil, {})

        h = c4.compute_all_homology()
        self.assertEqual(h[0].betti_number, 1)  # 1 connected component
        self.assertEqual(h[1].betti_number, 1)  # 1 cycle direction
        self.assertEqual(c4.euler_characteristic(), 0)

    def test_torus_square_complex(self) -> None:
        # Discretized 3x3 flat 2-torus T^2
        t = hom.build_torus_complex(3, 3)
        self.assertEqual(t.max_grade, 2)
        self.assertEqual(t.dimensions[0], 9)
        self.assertEqual(t.dimensions[1], 18)
        self.assertEqual(t.dimensions[2], 9)

        # Nilpotency \partial_1 \circ \partial_2 = 0
        nil = t.verify_nilpotency()
        self.assertTrue(nil[1])

        # Homology betti numbers: \beta_0 = 1, \beta_1 = 2, \beta_2 = 1
        h = t.compute_all_homology()
        self.assertEqual(h[0].betti_number, 1)
        self.assertEqual(h[1].betti_number, 2)
        self.assertEqual(h[2].betti_number, 1)
        self.assertEqual(t.euler_characteristic(), 0)

    def test_cubical_cavity_2sphere_and_3cube(self) -> None:
        # S^2 cavity (boundary of 3-cube, 6 square faces)
        s2 = hom.build_cubical_cavity_complex(include_3cell=False)
        self.assertEqual(s2.max_grade, 2)
        nil_s2 = s2.verify_nilpotency()
        self.assertTrue(nil_s2[1])

        h_s2 = s2.compute_all_homology()
        self.assertEqual(h_s2[0].betti_number, 1)
        self.assertEqual(h_s2[1].betti_number, 0)
        self.assertEqual(h_s2[2].betti_number, 1)  # cavity 2-cycle!
        self.assertEqual(s2.euler_characteristic(), 2)  # \chi(S^2) = 2

        # 3-cube with interior 3-cell
        cube = hom.build_cubical_cavity_complex(include_3cell=True)
        self.assertEqual(cube.max_grade, 3)
        nil_cube = cube.verify_nilpotency()
        self.assertTrue(nil_cube[1])
        self.assertTrue(nil_cube[2])  # \partial_2 \circ \partial_3 = 0

        h_cube = cube.compute_all_homology()
        self.assertEqual(h_cube[0].betti_number, 1)
        self.assertEqual(h_cube[1].betti_number, 0)
        self.assertEqual(h_cube[2].betti_number, 0)  # killed by 3-cell!
        self.assertEqual(h_cube[3].betti_number, 0)
        self.assertEqual(cube.euler_characteristic(), 1)  # \chi(D^3) = 1


class TestDualCochainComplexAndStokes(unittest.TestCase):
    """Test dual cochain complex, coboundary nilpotency, and discrete Stokes theorem."""

    def test_coboundary_nilpotency(self) -> None:
        t = hom.build_torus_complex(3, 3)
        dt = t.dual_cochain_complex()
        cobound_nil = dt.verify_coboundary_nilpotency()
        self.assertTrue(cobound_nil[0])

        cube = hom.build_cubical_cavity_complex(include_3cell=True)
        dcube = cube.dual_cochain_complex()
        cobound_nil_cube = dcube.verify_coboundary_nilpotency()
        self.assertTrue(cobound_nil_cube[0])
        self.assertTrue(cobound_nil_cube[1])

    def test_cohomology_homology_isomorphism(self) -> None:
        t = hom.build_torus_complex(3, 3)
        dt = t.dual_cochain_complex()
        h = t.compute_all_homology()
        ch = dt.compute_all_cohomology()
        for k in range(3):
            self.assertEqual(h[k].betti_number, ch[k].betti_number)

    def test_discrete_stokes_theorem(self) -> None:
        t = hom.build_torus_complex(3, 3)
        dt = t.dual_cochain_complex()
        # Test Stokes on arbitrary cochain and chain
        omega = [Fraction(i * 3 - 7, 2) for i in range(t.dimensions[1])]
        c2 = [Fraction(i * 5 + 1, 3) for i in range(t.dimensions[2])]
        self.assertTrue(dt.verify_stokes_theorem(1, omega, c2))


class TestObstructionClasses(unittest.TestCase):
    """Test obstruction class analysis and circulation witness detection."""

    def test_cycle_obstruction_detection(self) -> None:
        # In a directed cycle, a uniform cochain w = (1, 1, 1, 1) has non-zero circulation
        c4 = hom.build_cycle_complex(4)
        w_circ = [Fraction(1) for _ in range(4)]
        rep = hom.analyze_obstruction(c4, grade=1, cochain=w_circ)
        self.assertTrue(rep.is_cocycle)
        self.assertFalse(rep.is_coboundary)
        self.assertTrue(rep.is_obstruction_class)
        self.assertEqual(rep.circulation, Fraction(4))
        self.assertIsNotNone(rep.witness_cycle)

        # An exact cochain (coboundary of P = [0, 1, 3, 2])
        d0_p = [
            Fraction(1 - 0),
            Fraction(3 - 1),
            Fraction(2 - 3),
            Fraction(0 - 2),
        ]
        rep_exact = hom.analyze_obstruction(c4, grade=1, cochain=d0_p)
        self.assertTrue(rep_exact.is_cocycle)
        self.assertTrue(rep_exact.is_coboundary)
        self.assertFalse(rep_exact.is_obstruction_class)
        self.assertEqual(rep_exact.circulation, Fraction(0))

    def test_cavity_2cochain_obstruction(self) -> None:
        # S^2 cavity has H^2 of dimension 1
        s2 = hom.build_cubical_cavity_complex(include_3cell=False)
        ch_s2 = s2.dual_cochain_complex().compute_cohomology(2)
        self.assertEqual(ch_s2.betti_number, 1)
        gen2 = ch_s2.basis_cocycles[0]

        rep = hom.analyze_obstruction(s2, grade=2, cochain=gen2)
        self.assertTrue(rep.is_obstruction_class)
        self.assertNotEqual(rep.circulation, Fraction(0))

        # In filled 3-cube, the 3-cell boundary has \delta^2(gen2) != 0, so gen2 ceases to be closed
        cube = hom.build_cubical_cavity_complex(include_3cell=True)
        rep_cube = hom.analyze_obstruction(cube, grade=2, cochain=gen2)
        self.assertFalse(rep_cube.is_obstruction_class)
        self.assertFalse(rep_cube.is_cocycle)


class TestTarget7RelationalMoveComplex(unittest.TestCase):
    """Test relational move complex constructed from Target 7 movegraph."""

    def test_target7_pure_complex(self) -> None:
        c7 = hom.build_target7_complex(pure_only=True)
        self.assertEqual(c7.dimensions[0], 262)
        self.assertEqual(c7.dimensions[1], 638)
        self.assertEqual(c7.dimensions[2], 146)

        # Verify nilpotency \partial_1 \circ \partial_2 = 0
        nil = c7.verify_nilpotency()
        self.assertTrue(nil[1])

        # Compute homology
        h0 = c7.compute_homology(0)
        h1 = c7.compute_homology(1)
        h2 = c7.compute_homology(2)

        self.assertEqual(h0.betti_number, 2)  # 2 connected components
        self.assertEqual(h1.betti_number, 232)  # 378 - 146 pure squares = 232
        self.assertEqual(h2.betti_number, 0)

    def test_target7_native_candidates(self) -> None:
        c7 = hom.build_target7_complex(pure_only=True)
        reports = hom.evaluate_target7_native_candidates(c7)
        self.assertEqual(len(reports), 4)
        for name in ("rule_span", "width_at_admission", "empty_admission", "mention_deficit"):
            self.assertIn(name, reports)
            # In the 2-complex, these cost functions have non-zero coboundary on pure squares
            # (they are order-sensitive, detecting the commitment-growth obstruction!)
            self.assertFalse(reports[name].is_cocycle)


if __name__ == "__main__":
    unittest.main()
