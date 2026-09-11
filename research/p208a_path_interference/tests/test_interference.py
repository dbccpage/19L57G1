"""Unit and property test suite for Target P208a: path_interference and Vanishing Sorkin I_3.

AuthorityEffect: None.
Axiom Scope: Exact rational arithmetic; constructive verification.
"""

from __future__ import annotations

from fractions import Fraction
import importlib
from itertools import combinations
import pytest

import path_interference as _mod
CyclotomicRational = _mod.CyclotomicRational
Diamond2Complex = _mod.Diamond2Complex
GaussianRational = _mod.GaussianRational
discrete_derivative = _mod.discrete_derivative
higher_order_discrete_difference = _mod.higher_order_discrete_difference
run_cyclotomic_parameter_sweep = _mod.run_cyclotomic_parameter_sweep
run_pythagorean_parameter_sweep = _mod.run_pythagorean_parameter_sweep
verify_constructive_nonzero_i2 = _mod.verify_constructive_nonzero_i2


# =============================================================================
# 1. GaussianRational Arithmetic Tests
# =============================================================================

def test_gaussian_rational_basics() -> None:
    z0 = GaussianRational.zero()
    assert z0.re == 0 and z0.im == 0
    assert z0.norm_sq() == 0

    z1 = GaussianRational.one()
    assert z1.re == 1 and z1.im == 0
    assert z1.norm_sq() == 1

    zi = GaussianRational.i()
    assert zi.re == 0 and zi.im == 1
    assert zi.norm_sq() == 1

    # i * i = -1
    prod_ii = zi * zi
    assert prod_ii == GaussianRational(-1, 0)
    assert prod_ii == -1


def test_gaussian_rational_operations() -> None:
    a = GaussianRational(3, 4)
    b = GaussianRational(1, -2)

    # Addition and Subtraction
    assert a + b == GaussianRational(4, 2)
    assert a - b == GaussianRational(2, 6)

    # Commutativity of addition and multiplication
    assert a + b == b + a
    assert a * b == b * a

    # Multiplication: (3+4i)(1-2i) = 3 - 6i + 4i - 8i^2 = 11 - 2i
    assert a * b == GaussianRational(11, -2)

    # Division: (11 - 2i) / (1 - 2i) = 3 + 4i
    assert (a * b) / b == a

    # Conjugate
    assert a.conjugate() == GaussianRational(3, -4)
    assert a * a.conjugate() == a.norm_sq()
    assert a.norm_sq() == Fraction(25, 1)

    # Negation
    assert -a == GaussianRational(-3, -4)
    assert a + (-a) == GaussianRational.zero()


def test_gaussian_rational_pythagorean_rotations() -> None:
    # m=2, n=1 -> (3/5, 4/5)
    u1 = GaussianRational.unit_pythagorean(2, 1)
    assert u1.re == Fraction(3, 5)
    assert u1.im == Fraction(4, 5)
    assert u1.norm_sq() == Fraction(1, 1)

    # m=3, n=2 -> (5/13, 12/13)
    u2 = GaussianRational.unit_pythagorean(3, 2)
    assert u2.re == Fraction(5, 13)
    assert u2.im == Fraction(12, 13)
    assert u2.norm_sq() == Fraction(1, 1)

    # Product of unit rotations remains exact unit rotation
    u_prod = u1 * u2
    assert u_prod.norm_sq() == Fraction(1, 1)

    with pytest.raises(ValueError):
        GaussianRational.unit_pythagorean(0, 0)


def test_gaussian_rational_division_by_zero() -> None:
    a = GaussianRational(1, 1)
    with pytest.raises(ZeroDivisionError):
        _ = a / GaussianRational.zero()
    with pytest.raises(ZeroDivisionError):
        _ = a / 0


# =============================================================================
# 2. CyclotomicRational Arithmetic Tests
# =============================================================================

def test_cyclotomic_rational_basics() -> None:
    # n=4 corresponds to Q(i) with Phi_4(x) = x^2 + 1
    gen4 = CyclotomicRational.root_gen(4)
    gen4_sq = gen4 * gen4
    # x^2 mod (x^2 + 1) = -1
    assert gen4_sq.coeffs == (Fraction(-1, 1), Fraction(0, 1))

    # n=3: Phi_3(x) = x^2 + x + 1
    gen3 = CyclotomicRational.root_gen(3)
    gen3_sq = gen3 * gen3
    # x^2 mod (x^2 + x + 1) = -x - 1
    assert gen3_sq.coeffs == (Fraction(-1, 1), Fraction(-1, 1))

    # x^3 = x * (-x - 1) = -x^2 - x = -(-x - 1) - x = 1
    gen3_cube = gen3_sq * gen3
    assert gen3_cube.coeffs == (Fraction(1, 1), Fraction(0, 1))
    assert gen3_cube == 1


def test_cyclotomic_rational_conjugation() -> None:
    # For n=8, Phi_8(x) = x^4 + 1
    gen8 = CyclotomicRational.root_gen(8)
    gen8_conj = gen8.conjugate()
    # gen * gen_conj = 1
    prod = gen8 * gen8_conj
    assert prod == 1
    assert prod.valuation() == 1


# =============================================================================
# 3. Diamond 2-Complex Topology and Valuation Tests
# =============================================================================

def test_diamond_2_complex_structure() -> None:
    c = Diamond2Complex(["A", "B", "C"])
    assert c.path_names == ("A", "B", "C")
    assert len(c.path_amplitudes) == 3

    # Total path_amplitude of empty subset is zero
    empty_amp = c.total_amplitude([])
    assert empty_amp == GaussianRational.zero()
    assert c.intensity([]) == Fraction(0, 1)

    # Singleton path valuations
    assert c.intensity(["A"]) == Fraction(1, 1)
    assert c.intensity(["B"]) == Fraction(1, 1)
    assert c.intensity(["C"]) == Fraction(1, 1)


def test_diamond_2_complex_missing_path_error() -> None:
    with pytest.raises(KeyError):
        _ = Diamond2Complex(["A", "B"], {"A": GaussianRational.one()})

    c = Diamond2Complex(["A", "B"])
    with pytest.raises(KeyError):
        c.set_path_amplitude("Z", GaussianRational.one())


# =============================================================================
# 4. Second-Order path_interference Tests (I_2 != 0)
# =============================================================================

def test_second_order_path_interference_constructive_witness() -> None:
    i2, a1, a2 = verify_constructive_nonzero_i2()
    assert i2 == Fraction(6, 5)
    assert i2 != Fraction(0, 1)
    assert a1 == GaussianRational.one()
    assert a2 == GaussianRational(Fraction(3, 5), Fraction(4, 5))


def test_second_order_path_interference_shifts() -> None:
    c = Diamond2Complex(["A", "B"])

    # 1. Zero shift: both real unit path_amplitudes
    # A=1, B=1 -> P(A+B)=4, P(A)=1, P(B)=1 -> I_2 = 2
    c.set_path_amplitude("A", GaussianRational(1, 0))
    c.set_path_amplitude("B", GaussianRational(1, 0))
    assert c.second_order_interference("A", "B") == Fraction(2, 1)

    # 2. Orthogonal delay: A=1, B=i
    # A+B = 1+i -> P(A+B) = 2, P(A)=1, P(B)=1 -> I_2 = 0
    c.set_path_amplitude("B", GaussianRational(0, 1))
    assert c.second_order_interference("A", "B") == Fraction(0, 1)

    # 3. Destructive shift: A=1, B=-1
    # A+B = 0 -> P(A+B) = 0, P(A)=1, P(B)=1 -> I_2 = -2
    c.set_path_amplitude("B", GaussianRational(-1, 0))
    assert c.second_order_interference("A", "B") == Fraction(-2, 1)

    # 4. Pythagorean shift: A=1, B=3/5 + 4/5*i -> I_2 = 2*Re(3/5) = 6/5
    c.set_path_amplitude("B", GaussianRational.unit_pythagorean(2, 1))
    assert c.second_order_interference("A", "B") == Fraction(6, 5)


# =============================================================================
# 5. Third-Order Sorkin Vanishing Tests (I_3 == 0)
# =============================================================================

def test_third_order_sorkin_identically_zero() -> None:
    # 3-path network with arbitrary non-trivial Gaussian rationals
    amps = {
        "A": GaussianRational(Fraction(3, 7), Fraction(-2, 5)),
        "B": GaussianRational(Fraction(-1, 3), Fraction(4, 9)),
        "C": GaussianRational(Fraction(5, 2), Fraction(7, 11)),
    }
    c = Diamond2Complex(["A", "B", "C"], amps)

    i3 = c.third_order_sorkin("A", "B", "C")
    assert i3 == Fraction(0, 1)
    assert c.is_sorkin_zero(["A", "B", "C"])


def test_pythagorean_parameter_sweep() -> None:
    res = run_pythagorean_parameter_sweep(max_param=4)
    assert res["all_i3_identically_zero"] is True
    assert res["i3_zero_count"] == res["configurations_tested"]
    assert res["i2_nonzero_count"] > 0
    assert res["higher_order_zero_count"] > 0


def test_cyclotomic_parameter_sweep() -> None:
    res = run_cyclotomic_parameter_sweep()
    assert res["all_i3_identically_zero"] is True
    assert res["configurations_tested"] > 0


# =============================================================================
# 6. Ruling Out Higher-Order path_interference (I_k == 0 for k >= 3)
# =============================================================================

def test_higher_order_path_interference_discrete_difference() -> None:
    # 5-path network
    paths = ["A", "B", "C", "D", "E"]
    c = Diamond2Complex(
        paths,
        {
            "A": GaussianRational(1, 2),
            "B": GaussianRational(-3, 1),
            "C": GaussianRational(0, 4),
            "D": GaussianRational.unit_pythagorean(2, 1),
            "E": GaussianRational.unit_pythagorean(3, 2),
        },
    )

    # Verify that discrete derivative matches discrete difference definition
    diff1 = discrete_derivative(c, ["A"], "B")
    expected_diff1 = c.intensity(["A", "B"]) - c.intensity(["A"])
    assert diff1 == expected_diff1

    # Verify all 3-path, 4-path, 5-path combinations have vanishing I_k
    for k in (3, 4, 5):
        for sub in combinations(paths, k):
            ik = higher_order_discrete_difference(c, sub)
            assert ik == Fraction(0, 1)
            assert c.is_sorkin_zero(sub)


def test_bilinear_structure_algebraic_proof() -> None:
    """Verify that any bilinear valuation sum_{j,k in sigma} a_j a_k^*

    yields vanishing finite differences of degree >= 3.
    """
    coeffs = [
        GaussianRational(i + 1, (i + 2) % 3) for i in range(6)
    ]
    path_names = [f"P{i}" for i in range(6)]
    c = Diamond2Complex(path_names, dict(zip(path_names, coeffs)))

    # Every order 3, 4, 5, 6 subset must have I_k == 0
    for k in (3, 4, 5, 6):
        for sub in combinations(path_names, k):
            assert c.is_sorkin_zero(sub)