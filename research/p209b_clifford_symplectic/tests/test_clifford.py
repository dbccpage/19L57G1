"""Tests for Discrete Clifford Group & Symplectic Geometry (Target P209b).

Covers:
- Symplectic form antisymmetry and canonical pairing.
- Sp(2, F_2) =~ S_3: order 6, det = 1, symplectic preservation, element orders, Cayley table.
- Sp(2, F_3) =~ SL(2, F_3): order 24, det = 1, symplectic preservation, order spectrum.
- Isomorphism to S_3 via vector permutations.
- Eastin-Knill finite quotient obstruction bounds and dense covering obstruction.

AuthorityEffect: None.
"""

from __future__ import annotations

import pytest

from clifford_symplectic import (
    Matrix2,
    build_sp2_f2_elements,
    build_sp2_f3_elements,
    compute_order_spectrum,
    eastin_knill_obstruction_analysis,
    generate_group_from_generators,
    get_sp2_f2_generators,
    get_sp2_f2_multiplication_table,
    get_sp2_f3_generators,
    omega,
)


def test_symplectic_form_antisymmetry_f2() -> None:
    """In F_2, omega(u, u) = 0 and omega(u, v) = omega(v, u) since 1 = -1 mod 2."""
    vectors = [(x, z) for x in range(2) for z in range(2)]
    for u in vectors:
        assert omega(u, u, 2) == 0
        for v in vectors:
            assert omega(u, v, 2) == omega(v, u, 2)


def test_symplectic_form_antisymmetry_odd_prime() -> None:
    """For odd moduli, omega(u, v) = -omega(v, u) mod p."""
    for p in (3, 5):
        vectors = [(x, z) for x in range(p) for z in range(p)]
        for u in vectors:
            assert omega(u, u, p) == 0
            for v in vectors:
                val_uv = omega(u, v, p)
                val_vu = omega(v, u, p)
                assert (val_uv + val_vu) % p == 0


def test_canonical_basis_pairing() -> None:
    """Canonical basis vectors e_x = (1, 0) and e_z = (0, 1) satisfy omega(e_x, e_z) = 1."""
    ex = (1, 0)
    ez = (0, 1)
    for p in (2, 3, 5):
        assert omega(ex, ez, p) == 1
        assert omega(ez, ex, p) == (-1) % p


def test_sp2_f2_generators_properties() -> None:
    """H and S generators have determinant 1 and order 2 in Sp(2, F_2)."""
    h_mat, s_mat = get_sp2_f2_generators()
    assert h_mat.det == 1
    assert s_mat.det == 1
    assert h_mat.order() == 2
    assert s_mat.order() == 2


def test_sp2_f2_determinant_unity() -> None:
    """All 6 elements of Sp(2, F_2) have determinant 1 mod 2."""
    elements = build_sp2_f2_elements()
    assert len(elements) == 6
    for name, m in elements.items():
        assert m.det == 1, f"Determinant of {name} must be 1 mod 2"


def test_sp2_f2_mutual_distinctness() -> None:
    """The 6 matrices I, H, S, SH, HS, HSH are pairwise distinct."""
    elements = build_sp2_f2_elements()
    items = list(elements.items())
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            name_i, m_i = items[i]
            name_j, m_j = items[j]
            assert m_i != m_j, f"Distinct elements expected: {name_i} == {name_j}"


def test_sp2_f2_symplectic_invariance() -> None:
    """All 6 matrices in Sp(2, F_2) preserve the symplectic form."""
    elements = build_sp2_f2_elements()
    for name, m in elements.items():
        assert m.preserves_symplectic_form(), f"Element {name} must preserve symplectic form"


def test_sp2_f2_element_order_classification() -> None:
    """Classification: 1 identity, 3 reflections of order 2, 2 rotations of order 3."""
    elements = build_sp2_f2_elements()
    assert elements["I"].order() == 1
    assert elements["H"].order() == 2
    assert elements["S"].order() == 2
    assert elements["HSH"].order() == 2
    assert elements["SH"].order() == 3
    assert elements["HS"].order() == 3


def test_sp2_f2_group_closure_cayley_table() -> None:
    """Group multiplication is closed and matches the S_3 presentation."""
    table = get_sp2_f2_multiplication_table()
    assert len(table) == 36
    elements = build_sp2_f2_elements()
    # Check H * S * H == S * H * S
    hsh = elements["H"].matmul(elements["S"]).matmul(elements["H"])
    shs = elements["S"].matmul(elements["H"]).matmul(elements["S"])
    assert hsh == shs
    assert hsh == elements["HSH"]


def test_sp2_f2_inverses() -> None:
    """Every element in Sp(2, F_2) has a valid inverse within the group."""
    elements = build_sp2_f2_elements()
    identity = elements["I"]
    for name, m in elements.items():
        inv_m = m.inverse()
        assert m.matmul(inv_m) == identity
        assert inv_m.matmul(m) == identity
        assert inv_m in elements.values()
    # Reflections are self-inverse
    assert elements["H"].inverse() == elements["H"]
    assert elements["S"].inverse() == elements["S"]
    assert elements["HSH"].inverse() == elements["HSH"]
    # Rotations invert each other
    assert elements["SH"].inverse() == elements["HS"]
    assert elements["HS"].inverse() == elements["SH"]


def test_sp2_f2_isomorphism_s3() -> None:
    """Sp(2, F_2) acts faithfully on the 3 non-zero vectors in F_2^2 as S_3."""
    elements = build_sp2_f2_elements()
    non_zero_vectors = [(1, 0), (0, 1), (1, 1)]
    permutations = set()

    for name, m in elements.items():
        perm = tuple(m.apply(v) for v in non_zero_vectors)
        # Verify it permutes non_zero_vectors
        assert set(perm) == set(non_zero_vectors)
        permutations.add(perm)

    # 6 distinct permutations of 3 points indicates full S_3
    assert len(permutations) == 6


def test_sp2_f3_order_and_determinant() -> None:
    """Sp(2, F_3) =~ SL(2, F_3) has exactly 24 elements of determinant 1 mod 3."""
    elements = build_sp2_f3_elements()
    assert len(elements) == 24
    for m in elements:
        assert m.det == 1


def test_sp2_f3_symplectic_invariance() -> None:
    """All 24 elements of Sp(2, F_3) preserve the symplectic form on F_3^2."""
    elements = build_sp2_f3_elements()
    for m in elements:
        assert m.preserves_symplectic_form()


def test_sp2_f3_generation() -> None:
    """H_3 and S_3 generate the complete Sp(2, F_3) group of order 24."""
    h3, s3 = get_sp2_f3_generators()
    generated = generate_group_from_generators([h3, s3])
    assert len(generated) == 24
    enumerated = sorted(build_sp2_f3_elements(), key=lambda m: (m.a, m.b, m.c, m.d))
    assert generated == enumerated


def test_sp2_f3_order_spectrum() -> None:
    """Order spectrum of SL(2, F_3): 1 (order 1), 1 (order 2), 8 (order 3), 6 (order 4), 8 (order 6)."""
    elements = build_sp2_f3_elements()
    spectrum = compute_order_spectrum(elements)
    expected = {1: 1, 2: 1, 3: 8, 4: 6, 6: 8}
    assert spectrum == expected


def test_eastin_knill_finite_quotient_bounds() -> None:
    """Eastin-Knill analysis confirms finite quotient and obstruction of dense covering."""
    res_f2 = eastin_knill_obstruction_analysis(2)
    assert res_f2["symplectic_quotient_order"] == 6
    assert res_f2["continuous_carrier_lie_dimension"] == 3
    assert res_f2["is_finite_group"] is True
    assert res_f2["dense_covering_obstructed"] is True

    res_f3 = eastin_knill_obstruction_analysis(3)
    assert res_f3["symplectic_quotient_order"] == 24
    assert res_f3["continuous_carrier_lie_dimension"] == 8
    assert res_f3["is_finite_group"] is True
    assert res_f3["dense_covering_obstructed"] is True


def test_matrix_non_symplectic_detection() -> None:
    """Negative control: matrix with determinant != 1 fails symplectic preservation."""
    # Determinant = 0
    m_det0 = Matrix2(1, 1, 1, 1, 2)
    assert m_det0.det == 0
    assert not m_det0.preserves_symplectic_form()

    # In F_3: determinant = 2 != 1
    m_det2 = Matrix2(2, 0, 0, 1, 3)
    assert m_det2.det == 2
    assert not m_det2.preserves_symplectic_form()
