"""Comprehensive tests for Target P208c: Finite Commutator Obstruction & Discrete MUB Tomography.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import pytest

from tomography import (
    Cyclotomic3,
    GaussianRational,
    commutator_obstruction_gap,
    commutator_trace,
    construct_mub_projectors_dim3,
    construct_mub_projectors_dim4,
    construct_mubs_dim3,
    construct_mubs_dim4,
    discrete_clock_operator_dim3,
    discrete_clock_operator_dim4,
    discrete_shift_operator,
    identity_matrix,
    kronecker_product,
    matrix_add,
    matrix_commutator,
    matrix_multiply,
    matrix_scale,
    matrix_sub,
    matrix_trace,
    measure_mub_probabilities,
    reconstruct_state_from_probabilities,
    reconstruct_state_linear_inversion,
    vector_dot,
    verify_canonical_commutation_obstruction,
    verify_microcausality_bipartite,
    verify_mub_pairwise_overlap,
    zero_matrix,
)


# =============================================================================
# 1. Exact Field Arithmetic Tests
# =============================================================================

def test_gaussian_rational_refuses_float() -> None:
    with pytest.raises(TypeError, match="float is not exact"):
        GaussianRational(0.5, 0)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="float is not exact"):
        GaussianRational(0, 0.5)  # type: ignore[arg-type]


def test_cyclotomic3_refuses_float() -> None:
    with pytest.raises(TypeError, match="float is not exact"):
        Cyclotomic3(0.5, 0)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="float is not exact"):
        Cyclotomic3(0, 0.5)  # type: ignore[arg-type]


def test_cyclotomic3_arithmetic() -> None:
    """Tests exact arithmetic in cyclotomic rationals Q(w)."""
    w0 = Cyclotomic3.root_power(0)
    w1 = Cyclotomic3.root_power(1)
    w2 = Cyclotomic3.root_power(2)
    w3 = Cyclotomic3.root_power(3)

    assert w0 == 1
    assert w3 == w0
    # w^2 + w + 1 = 0
    assert w2 + w1 + w0 == 0

    # Multiplication
    assert w1 * w1 == w2
    assert w1 * w2 == w0

    # Inverses and division
    inv_w1 = 1 / w1
    assert inv_w1 == w2
    assert (w1 + 2) / (w1 + 2) == 1

    # Norm squared
    z = Cyclotomic3(2, 3)
    # (2 + 3w)((2 - 3) - 3w) = (2 + 3w)(-1 - 3w)
    # Norm sq = 2^2 - 2*3 + 3^2 = 4 - 6 + 9 = 7
    assert z.norm_sq() == 7
    assert z * z.conj() == 7

    # Division by zero
    with pytest.raises(ZeroDivisionError):
        _ = z / 0
    with pytest.raises(ZeroDivisionError):
        _ = z / Cyclotomic3(0, 0)


def test_gaussian_rational_arithmetic() -> None:
    """Tests exact arithmetic in Gaussian rationals Q(i)."""
    one = GaussianRational(1, 0)
    i = GaussianRational(0, 1)

    assert one * one == one
    assert i * i == -1
    assert (one + i) * (one - i) == 2

    z = GaussianRational(3, 4)
    assert z.norm_sq() == 25
    assert z * z.conj() == 25

    inv_z = 1 / z
    assert inv_z * z == 1

    with pytest.raises(ZeroDivisionError):
        _ = z / 0
    with pytest.raises(ZeroDivisionError):
        _ = z / GaussianRational(0, 0)


# =============================================================================
# 2. Finite Commutator Trace Obstruction Tests
# =============================================================================

def test_commutator_trace_identically_zero() -> None:
    """Tests that Tr([A, B]) = 0 for arbitrary matrices across various dimensions."""
    for dim in [2, 3, 4, 5]:
        A = [[Fraction(i * 3 + j + 1) for j in range(dim)] for i in range(dim)]
        B = [[Fraction((i + 1) * (j + 2)) for j in range(dim)] for i in range(dim)]

        tr_comm = commutator_trace(A, B)
        assert tr_comm == Fraction(0)
        assert tr_comm == 0


def test_canonical_commutation_obstruction() -> None:
    """Tests the algebraic obstruction theorem for [Q, P] = c * I on finite carriers."""
    for dim in [1, 2, 3, 4, 10]:
        c = Fraction(1)
        assert verify_canonical_commutation_obstruction(dim, c) is True

        # For any putative Q, P, verify obstruction gap Tr([Q, P] - c * I) = -N * c != 0
        Q = identity_matrix(dim)
        P = identity_matrix(dim)
        gap = commutator_obstruction_gap(Q, P, c)
        assert gap == -Fraction(dim) * c
        assert gap != 0


# =============================================================================
# 3. Multi-Locus Microcausality Tests
# =============================================================================

def test_single_locus_conjugate_noncommutation() -> None:
    """Tests that conjugate observables on the same locus fail to commute."""
    # Dimension 3: discrete clock Z and shift X
    X3 = discrete_shift_operator(3, Cyclotomic3(0), Cyclotomic3(1))
    Z3 = discrete_clock_operator_dim3()
    comm3 = matrix_commutator(Z3, X3)
    zero3 = zero_matrix(3, 3, Cyclotomic3(0))
    assert comm3 != zero3

    # Dimension 4: discrete clock and shift
    X4 = discrete_shift_operator(4, GaussianRational(0), GaussianRational(1))
    Z4 = discrete_clock_operator_dim4()
    comm4 = matrix_commutator(Z4, X4)
    zero4 = zero_matrix(4, 4, GaussianRational(0))
    assert comm4 != zero4


def test_multi_locus_microcausality() -> None:
    """Tests that observables on disjoint loci strictly commute: [A (x) I_B, I_A (x) B] = 0."""
    # Composite carrier 2 x 3
    A = [[Fraction(1), Fraction(2)], [Fraction(3), Fraction(4)]]
    B = [
        [Fraction(2), Fraction(0), Fraction(1)],
        [Fraction(1), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(3), Fraction(2)],
    ]
    assert verify_microcausality_bipartite(A, B) is True

    # Composite carrier 3 x 3 with cyclotomic operators
    X3 = discrete_shift_operator(3, Cyclotomic3(0), Cyclotomic3(1))
    Z3 = discrete_clock_operator_dim3()
    assert verify_microcausality_bipartite(X3, Z3) is True


# =============================================================================
# 4. Discrete MUB Construction & Unbiasedness Tests
# =============================================================================

def test_mub_dim3_construction_and_unbiasedness() -> None:
    """Tests the d + 1 = 4 MUBs in dimension d = 3."""
    bases = construct_mubs_dim3()
    assert len(bases) == 4
    for b in bases:
        assert len(b) == 3

    # Within-basis orthonormality:
    # Standard basis: ||v||^2 = 1, inner product delta_{j, k}
    for j in range(3):
        for k in range(3):
            dot_val = vector_dot(bases[0][j], bases[0][k])
            expected = Cyclotomic3(1 if j == k else 0)
            assert dot_val == expected

    # Fourier bases 1, 2, 3: unscaled vectors have ||v||^2 = 3
    for r in range(1, 4):
        for j in range(3):
            for k in range(3):
                dot_val = vector_dot(bases[r][j], bases[r][k])
                expected = Cyclotomic3(3 if j == k else 0)
                assert dot_val == expected

    # Pairwise mutual unbiasedness across all bases: |<u | v>|^2 = 1/3
    # Standard vs Fourier: dot has |val|^2 = 1. Scaled: 1 / 3.
    # Fourier vs Fourier: dot has |val|^2 = 3. Scaled: 3 / 9 = 1/3.
    for r in range(1, 4):
        for j in range(3):
            for k in range(3):
                dot_val = vector_dot(bases[0][j], bases[r][k])
                assert dot_val.norm_sq() == 1

    for r1 in range(1, 4):
        for r2 in range(r1 + 1, 4):
            for j in range(3):
                for k in range(3):
                    dot_val = vector_dot(bases[r1][j], bases[r2][k])
                    assert dot_val.norm_sq() == 3

    # Projector resolution of identity: sum_k Pi_{b, k} = I_3
    projectors = construct_mub_projectors_dim3()
    I3 = identity_matrix(3, Cyclotomic3(0), Cyclotomic3(1))
    for b_idx, b_projs in enumerate(projectors):
        s = zero_matrix(3, 3, Cyclotomic3(0))
        for P in b_projs:
            s = matrix_add(s, P)
        assert s == I3, f"Basis {b_idx} does not resolve identity"


def test_mub_dim4_construction_and_unbiasedness() -> None:
    """Tests the d + 1 = 5 MUBs in dimension d = 4."""
    bases = construct_mubs_dim4()
    assert len(bases) == 5
    for b in bases:
        assert len(b) == 4

    # All unscaled vectors in all 5 bases have norm squared 4
    for b_idx, b in enumerate(bases):
        for k in range(4):
            nsq = vector_dot(b[k], b[k]).norm_sq()
            assert nsq == 16, f"Basis {b_idx} vector {k} norm_sq != 16"

    # Mutual unbiasedness: |<u | v>|^2 = 1/4
    # With physical vectors = v / 2, norm_factor_sq = 4 * 4 = 16
    assert verify_mub_pairwise_overlap(bases, 4, Fraction(16)) is True

    # Projector resolution of identity: sum_k Pi_{b, k} = I_4
    projectors = construct_mub_projectors_dim4()
    I4 = identity_matrix(4, GaussianRational(0), GaussianRational(1))
    for b_idx, b_projs in enumerate(projectors):
        s = zero_matrix(4, 4, GaussianRational(0))
        for P in b_projs:
            s = matrix_add(s, P)
        assert s == I4, f"Basis {b_idx} does not resolve identity"


# =============================================================================
# 5. Complete Operational State Tomography Tests
# =============================================================================

def test_operational_tomography_dim3() -> None:
    """Tests complete state reconstruction in dimension d = 3."""
    projectors = construct_mub_projectors_dim3()
    I3 = identity_matrix(3, Cyclotomic3(0), Cyclotomic3(1))

    # Test 1: Maximally mixed state I / 3
    rho_mixed = matrix_scale(Cyclotomic3(Fraction(1, 3)), I3)
    probs_mixed = measure_mub_probabilities(rho_mixed, projectors)
    rec_mixed = reconstruct_state_from_probabilities(
        probs_mixed, projectors, 3, Cyclotomic3(0), Cyclotomic3(1)
    )
    assert rec_mixed == rho_mixed

    # Test 2: Non-trivial carrier state with off-diagonal coherences
    X = discrete_shift_operator(3, Cyclotomic3(0), Cyclotomic3(1))
    X_dag = [[X[j][i].conj() for j in range(3)] for i in range(3)]
    # rho = (1/3) I + (1/12) (X + X_dag)
    term = matrix_scale(Cyclotomic3(Fraction(1, 12)), matrix_add(X, X_dag))
    rho_coh = matrix_add(rho_mixed, term)

    # Forward measurement
    probs_coh = measure_mub_probabilities(rho_coh, projectors)

    # Inverse reconstruction via Wootters dual frame formula
    rec_wootters = reconstruct_state_from_probabilities(
        probs_coh, projectors, 3, Cyclotomic3(0), Cyclotomic3(1)
    )
    assert rec_wootters == rho_coh

    # Linear system inversion
    rec_lin = reconstruct_state_linear_inversion(
        probs_coh, projectors, 3, Cyclotomic3(0), Cyclotomic3(1)
    )
    assert rec_lin == rho_coh


def test_operational_tomography_dim4() -> None:
    """Tests complete state reconstruction in dimension d = 4."""
    projectors = construct_mub_projectors_dim4()
    I4 = identity_matrix(4, GaussianRational(0), GaussianRational(1))

    # Maximally mixed state I / 4
    rho_mixed = matrix_scale(GaussianRational(Fraction(1, 4)), I4)
    probs_mixed = measure_mub_probabilities(rho_mixed, projectors)
    rec_mixed = reconstruct_state_from_probabilities(
        probs_mixed, projectors, 4, GaussianRational(0), GaussianRational(1)
    )
    assert rec_mixed == rho_mixed

    # Non-trivial state
    # Perturb with projection differences from basis 1
    diff = matrix_sub(projectors[1][0], projectors[1][1])
    term = matrix_scale(GaussianRational(Fraction(1, 8)), diff)
    rho_pert = matrix_add(rho_mixed, term)

    # Forward measurement
    probs_pert = measure_mub_probabilities(rho_pert, projectors)

    # Inverse reconstruction via Wootters dual frame formula
    rec_wootters = reconstruct_state_from_probabilities(
        probs_pert, projectors, 4, GaussianRational(0), GaussianRational(1)
    )
    assert rec_wootters == rho_pert

    # Linear system inversion
    rec_lin = reconstruct_state_linear_inversion(
        probs_pert, projectors, 4, GaussianRational(0), GaussianRational(1)
    )
    assert rec_lin == rho_pert


# =============================================================================
# 6. Negative Tests: the Hypotheses the Claims Name
# =============================================================================

def test_commutation_obstruction_refuses_an_empty_carrier() -> None:
    """CL-P208C-01 is stated for N >= 1; a carrier of dimension N < 1 is refused by name."""
    for dim in (0, -1):
        with pytest.raises(ValueError, match="Carrier dimension must be positive"):
            verify_canonical_commutation_obstruction(dim, Fraction(1))


def test_commutation_at_zero_is_not_obstructed() -> None:
    """At c = 0, Q = P = I_N solves [Q, P] = 0 * I_N, so nothing is obstructed.

    Until 2026-09-25 the function answered True ("obstructed") here.
    """
    for dim in (1, 2, 3, 4, 10):
        for zero in (0, Fraction(0)):
            assert verify_canonical_commutation_obstruction(dim, zero) is False
        witness = identity_matrix(dim)
        assert matrix_commutator(witness, witness) == matrix_scale(Fraction(0), identity_matrix(dim))


def test_overlap_check_refuses_a_biased_pair_of_bases() -> None:
    """CL-P208C-03 and 04 claim overlap exactly 1/d; a repeated basis is refused."""
    bases3 = construct_mubs_dim3()
    # The three Fourier bases share the unscaled norm 3, so their scale factor is 9.
    assert verify_mub_pairwise_overlap(bases3[1:], 3, Fraction(9)) is True
    assert verify_mub_pairwise_overlap([bases3[1], bases3[1]], 3, Fraction(9)) is False

    bases4 = construct_mubs_dim4()
    assert verify_mub_pairwise_overlap([bases4[1], bases4[1]], 4, Fraction(16)) is False
    swapped = [list(bases4[2]), list(bases4[3])]
    swapped[1][0] = bases4[2][0]
    assert verify_mub_pairwise_overlap(swapped, 4, Fraction(16)) is False


def test_dimension3_fixture_is_not_determined_by_d_bases() -> None:
    """The README asks for all d + 1 bases: with the shift eigenbasis dropped, the
    coherent dimension-3 fixture and the maximally mixed state give identical
    probabilities on the remaining d = 3 bases, so those bases cannot separate them."""
    projectors = construct_mub_projectors_dim3()
    I3 = identity_matrix(3, Cyclotomic3(0), Cyclotomic3(1))
    rho_mixed = matrix_scale(Cyclotomic3(Fraction(1, 3)), I3)
    X = discrete_shift_operator(3, Cyclotomic3(0), Cyclotomic3(1))
    X_dag = [[X[j][i].conj() for j in range(3)] for i in range(3)]
    rho_coh = matrix_add(rho_mixed, matrix_scale(Cyclotomic3(Fraction(1, 12)), matrix_add(X, X_dag)))
    assert rho_coh != rho_mixed

    probs_mixed = measure_mub_probabilities(rho_mixed, projectors)
    probs_coh = measure_mub_probabilities(rho_coh, projectors)
    assert [b for b in range(4) if probs_mixed[b] != probs_coh[b]] == [1]
    remaining = [0, 2, 3]
    assert [probs_mixed[b] for b in remaining] == [probs_coh[b] for b in remaining]
