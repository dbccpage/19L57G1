"""Test suite for Target P209a: Discrete Wigner Phase_Spaces.

AuthorityEffect: None.
Tests:
1. Cyclotomic arithmetic over Q(zeta_p) for odd_prime dimensions p in {3, 5}.
2. Parity reflection operator P: P |j> = |-j mod p>, P^2 = I, Tr(P) = 1.
3. Translation shift X and clock Z orders: X^p = I, Z^p = I.
4. Gross phase_space covariance: P X P = X^{-1} and P Z P = Z^{-1}.
5. Discrete Weyl displacement operator D(q, p) algebra and group law.
6. Gross phase_point operator A(q, p) hermiticity, involution, trace, completeness, orthogonality.
7. Stabilizer state non-negativity: W_{|0>}(q, p) >= 0 and W_{|+>}(q, p) >= 0 everywhere.
8. Magic state point negativity witness: W_{|M>}(0, 0) = -1/p < 0.
9. Discrete Wigner total probability normalization and exact state reconstruction.
10. Marginal distribution consistency on position and vertical coordinate slices.
"""

from __future__ import annotations

from fractions import Fraction
import pytest

from wigner_phase_space import (
    CyclotomicPrime,
    ExactMatrix,
    discrete_clock,
    discrete_shift,
    discrete_wigner_distribution,
    discrete_wigner_point,
    displacement_operator,
    ket_magic_density,
    ket_plus_density,
    ket_zero_density,
    matrix_power,
    parity_operator,
    phase_point_operator,
    reconstruct_state,
    trace_prod,
    verify_completeness,
    verify_gross_covariance,
    verify_orthogonality,
    verify_parity_involution,
)


# =============================================================================
# 1. Cyclotomic Field Invariants
# =============================================================================

def test_cyclotomic_field_invariants_dim3() -> None:
    """Cyclotomic arithmetic in dimension 3 over Q(w_3)."""
    p = 3
    z = CyclotomicPrime.root_unity(p, 1)
    # w^3 = 1
    assert (z * z * z) == CyclotomicPrime.from_rational(p, 1)
    # 1 + w + w^2 = 0
    s = CyclotomicPrime.from_rational(p, 1) + z + (z * z)
    assert s == CyclotomicPrime.from_rational(p, 0)
    # w * conj(w) = 1
    assert (z * z.conj()) == CyclotomicPrime.from_rational(p, 1)
    # Inversion
    elem = CyclotomicPrime(p, (Fraction(1), Fraction(2)))
    inv_elem = elem.inv()
    assert (elem * inv_elem) == CyclotomicPrime.from_rational(p, 1)


def test_cyclotomic_field_invariants_dim5() -> None:
    """Cyclotomic arithmetic in dimension 5 over Q(w_5)."""
    p = 5
    z = CyclotomicPrime.root_unity(p, 1)
    # w^5 = 1
    z5 = CyclotomicPrime.from_rational(p, 1)
    for _ in range(5):
        z5 = z5 * z
    assert z5 == CyclotomicPrime.from_rational(p, 1)
    # sum_{k=0}^4 w^k = 0
    s = CyclotomicPrime.from_rational(p, 0)
    for k in range(5):
        s = s + CyclotomicPrime.root_unity(p, k)
    assert s == CyclotomicPrime.from_rational(p, 0)
    # w * conj(w) = 1
    assert (z * z.conj()) == CyclotomicPrime.from_rational(p, 1)
    # Inversion
    elem = CyclotomicPrime(p, (Fraction(2), Fraction(0), Fraction(1), Fraction(0)))
    inv_elem = elem.inv()
    assert (elem * inv_elem) == CyclotomicPrime.from_rational(p, 1)


# =============================================================================
# 2. Parity Reflection Operator
# =============================================================================

@pytest.mark.parametrize("p", [3, 5])
def test_parity_involution_and_trace(p: int) -> None:
    """Parity reflection operator satisfies P^2 = I and Tr(P) = 1."""
    assert verify_parity_involution(p)
    P = parity_operator(p)
    # Test individual action: P |j> = |-j mod p>
    for j in range(p):
        v = [[1 if i == j else 0] for i in range(p)]
        # Multiply P by column vector
        Pv = [sum(P[i, k].to_rational() * v[k][0] for k in range(p)) for i in range(p)]
        target_idx = (-j) % p
        for i in range(p):
            expected = 1 if i == target_idx else 0
            assert Pv[i] == expected


# =============================================================================
# 3. Translation and Clock Operators
# =============================================================================

@pytest.mark.parametrize("p", [3, 5])
def test_shift_and_clock_orders(p: int) -> None:
    """Translation shift and clock operators satisfy X^p = I and Z^p = I."""
    X = discrete_shift(p)
    Z = discrete_clock(p)
    eye = ExactMatrix.eye(p, p)
    assert matrix_power(X, p) == eye
    assert matrix_power(Z, p) == eye


@pytest.mark.parametrize("p", [3, 5])
def test_gross_covariance_translation(p: int) -> None:
    """Gross phase_space covariance for translation: P X P = X^{-1}."""
    P = parity_operator(p)
    X = discrete_shift(p)
    X_inv = matrix_power(X, p - 1)
    assert (P @ X @ P) == X_inv


@pytest.mark.parametrize("p", [3, 5])
def test_gross_covariance_clock(p: int) -> None:
    """Gross phase_space covariance for clock: P Z P = Z^{-1}."""
    P = parity_operator(p)
    Z = discrete_clock(p)
    Z_inv = matrix_power(Z, p - 1)
    assert (P @ Z @ P) == Z_inv


@pytest.mark.parametrize("p", [3, 5])
def test_gross_covariance_full_harness(p: int) -> None:
    """High-level harness verification for Gross covariance."""
    assert verify_gross_covariance(p)


# =============================================================================
# 4. Discrete Weyl Displacements
# =============================================================================

@pytest.mark.parametrize("p", [3, 5])
def test_weyl_displacement_origin_and_dagger(p: int) -> None:
    """D(0, 0) = I and D(q, p)^dagger = D(-q, -p)."""
    eye = ExactMatrix.eye(p, p)
    assert displacement_operator(p, 0, 0) == eye

    for q in range(p):
        for p_coord in range(p):
            D = displacement_operator(p, q, p_coord)
            D_dag = D.dag()
            D_neg = displacement_operator(p, (-q) % p, (-p_coord) % p)
            assert D_dag == D_neg


@pytest.mark.parametrize("p", [3, 5])
def test_weyl_displacement_order_p(p: int) -> None:
    """Each displacement operator has order dividing p: D(q, p)^p = I."""
    eye = ExactMatrix.eye(p, p)
    for q in range(p):
        for p_coord in range(p):
            D = displacement_operator(p, q, p_coord)
            assert matrix_power(D, p) == eye


@pytest.mark.parametrize("p", [3, 5])
def test_weyl_group_law(p: int) -> None:
    """Weyl group composition law: D(u) D(v) = w_p^{2^{-1}(u_p v_q - u_q v_p)} D(u + v)."""
    inv2 = (p + 1) // 2
    for q1 in range(p):
        for p1 in range(p):
            D1 = displacement_operator(p, q1, p1)
            for q2 in range(p):
                for p2 in range(p):
                    D2 = displacement_operator(p, q2, p2)
                    phase_exp = (inv2 * (p1 * q2 - q1 * p2)) % p
                    phase_factor = CyclotomicPrime.root_unity(p, phase_exp)
                    target = phase_factor * displacement_operator(p, (q1 + q2) % p, (p1 + p2) % p)
                    assert (D1 @ D2) == target


# =============================================================================
# 5. Gross Phase_Point Operators
# =============================================================================

@pytest.mark.parametrize("p", [3, 5])
def test_phase_point_hermiticity_and_involution(p: int) -> None:
    """Gross phase_point operators are Hermitian involutions: A^dagger = A and A^2 = I."""
    eye = ExactMatrix.eye(p, p)
    for q in range(p):
        for p_coord in range(p):
            A = phase_point_operator(p, q, p_coord)
            assert A.dag() == A
            assert (A @ A) == eye


@pytest.mark.parametrize("p", [3, 5])
def test_phase_point_unit_trace(p: int) -> None:
    """Tr(A(q, p)) = 1 for all phase_space points."""
    one = CyclotomicPrime.from_rational(p, 1)
    for q in range(p):
        for p_coord in range(p):
            A = phase_point_operator(p, q, p_coord)
            assert A.trace() == one


@pytest.mark.parametrize("p", [3, 5])
def test_phase_point_completeness(p: int) -> None:
    """Completeness relation: sum_{q, p} A(q, p) = p * I_p."""
    assert verify_completeness(p)


@pytest.mark.parametrize("p", [3, 5])
def test_phase_point_orthogonality_sweep(p: int) -> None:
    """Orthogonality relation: Tr(A(q, p) A(q', p')) = p * delta_{q q'} delta_{p p'}."""
    assert verify_orthogonality(p)


# =============================================================================
# 6. Stabilizer State Non-Negativity & Magic State Negativity Witnesses
# =============================================================================

@pytest.mark.parametrize("p", [3, 5])
def test_stabilizer_ket0_non_negativity(p: int) -> None:
    """Discrete Wigner function of stabilizer state |0> is non-negative everywhere."""
    rho0 = ket_zero_density(p)
    wigner = discrete_wigner_distribution(p, rho0)

    # |0> has support only on q = 0 slice with value 1/p
    for (q, p_coord), val in wigner.items():
        assert val.is_rational()
        r_val = val.to_rational()
        if q == 0:
            assert r_val == Fraction(1, p)
        else:
            assert r_val == Fraction(0)
        assert r_val >= 0


@pytest.mark.parametrize("p", [3, 5])
def test_stabilizer_ket_plus_non_negativity(p: int) -> None:
    """Discrete Wigner function of stabilizer state |+> is non-negative everywhere."""
    rhoplus = ket_plus_density(p)
    wigner = discrete_wigner_distribution(p, rhoplus)

    # |+> has support only on p = 0 slice with value 1/p
    for (q, p_coord), val in wigner.items():
        assert val.is_rational()
        r_val = val.to_rational()
        if p_coord == 0:
            assert r_val == Fraction(1, p)
        else:
            assert r_val == Fraction(0)
        assert r_val >= 0


@pytest.mark.parametrize("p", [3, 5])
def test_magic_state_negativity_witness(p: int) -> None:
    """Magic state |M> witnesses strict point negativity: W_{|M>}(0, 0) = -1/p < 0."""
    rhoM = ket_magic_density(p)
    w_origin = discrete_wigner_point(p, rhoM, 0, 0)
    assert w_origin.is_rational()
    val = w_origin.to_rational()
    assert val == -Fraction(1, p)
    assert val < 0


# =============================================================================
# 7. Total Normalization, Reconstruction & Marginals
# =============================================================================

@pytest.mark.parametrize("p", [3, 5])
def test_wigner_total_probability_normalization(p: int) -> None:
    """Sum over all p^2 phase_space points equals 1 for normalized states."""
    for rho in [ket_zero_density(p), ket_plus_density(p), ket_magic_density(p)]:
        wigner = discrete_wigner_distribution(p, rho)
        total = CyclotomicPrime.from_rational(p, 0)
        for val in wigner.values():
            total = total + val
        assert total.is_rational()
        assert total.to_rational() == Fraction(1, 1)


@pytest.mark.parametrize("p", [3, 5])
def test_exact_state_reconstruction(p: int) -> None:
    """Exact reconstruction of state from its discrete Wigner distribution."""
    for rho in [ket_zero_density(p), ket_plus_density(p), ket_magic_density(p)]:
        wigner = discrete_wigner_distribution(p, rho)
        reconstructed = reconstruct_state(p, wigner)
        assert reconstructed == rho


@pytest.mark.parametrize("p", [3, 5])
def test_position_marginal_slices(p: int) -> None:
    """Sum of W_rho(q, p) over vertical coordinate p yields position diagonal element <q|rho|q>."""
    for rho in [ket_zero_density(p), ket_plus_density(p), ket_magic_density(p)]:
        wigner = discrete_wigner_distribution(p, rho)
        for q in range(p):
            sum_p = CyclotomicPrime.from_rational(p, 0)
            for p_coord in range(p):
                sum_p = sum_p + wigner[(q, p_coord)]
            expected = rho[q, q]
            assert sum_p == expected
