"""Comprehensive Test Suite for Target P209c: Stabilizer Codes on Affine Grids.

AuthorityEffect: None.

Tests:
1. Exact integer and Pauli string arithmetic (I, X, Y, Z).
2. Symplectic binary vector coordinates and commutation duality.
3. 3-carrier bit-flip code [[3, 1, 1]]:
   - Stabilizers commutativity.
   - Logical operators commutativity with stabilizers and mutual anticommutation.
   - 4 distinct syndrome patterns and deterministic correction.
   - Codespace projection operator idempotence Pi_S^2 = Pi_S and dimension 2.
4. 4-carrier CSS code [[4, 2, 2]] on discrete 2-torus:
   - S_Z and S_X commutativity.
   - 2 independent logical carrier algebras.
   - Distance-2 detection across all 12 single-carrier Pauli errors.
   - Codespace projection operator idempotence Pi_S^2 = Pi_S and dimension 4.
5. Steane [[7, 1, 3]] CSS code on the Fano plane PG(2, 2):
   - Fano dual lines weight 4 and even pairwise intersections |h_i cap h_j| = 2.
   - All 15 pairwise stabilizer commutations.
   - Logical operators X_L and Z_L commutations and mutual anticommutation.
   - Transversal Hadamard gate preserving stabilizer group and interchanging X_L <-> Z_L.
   - Deterministic diagnosis and correction of all 21 single-carrier Pauli errors.
   - Codespace projection operator idempotence Pi_S^2 = Pi_S and dimension 2.
"""

from __future__ import annotations

import pytest

from stabilizer_codes import (
    BitFlipCode3,
    GaussianRational,
    Pauli,
    PauliString,
    SteaneCode7,
    TorusCode4,
    check_projection_idempotence,
    generate_stabilizer_group,
    int_matrix_multiply,
    matrix_commutator,
    stabilizer_codespace_dimension,
    stabilizer_sum_int_matrix,
)


# =============================================================================
# 1. Single Pauli & String Arithmetic Tests
# =============================================================================


def test_single_pauli_products_and_powers() -> None:
    """Verifies single-carrier Pauli multiplication table and self-inverse property."""
    p_i = PauliString("I")
    p_x = PauliString("X")
    p_y = PauliString("Y")
    p_z = PauliString("Z")

    # Squares evaluate to identity (+I)
    assert p_x * p_x == p_i
    assert p_y * p_y == p_i
    assert p_z * p_z == p_i

    # Products with unit-i factors
    assert p_x * p_y == PauliString("Z", phase_power=1)   # +i Z
    assert p_y * p_x == PauliString("Z", phase_power=3)   # -i Z
    assert p_y * p_z == PauliString("X", phase_power=1)   # +i X
    assert p_z * p_y == PauliString("X", phase_power=3)   # -i X
    assert p_z * p_x == PauliString("Y", phase_power=1)   # +i Y
    assert p_x * p_z == PauliString("Y", phase_power=3)   # -i Y


def test_pauli_string_multiplication_powers() -> None:
    """Verifies multi-carrier string multiplication and exponent accumulation."""
    s1 = PauliString("XYZ", phase_power=1)
    s2 = PauliString("ZYX", phase_power=2)
    # X*Z = -iY (p=3), Y*Y = I (p=0), Z*X = iY (p=1) -> symbol YIY, power = 1 + 2 + 3 + 0 + 1 = 7 = 3 mod 4
    prod = s1 * s2
    assert prod.symbols == ("Y", "I", "Y")
    assert prod.phase_power == 3


def test_pauli_string_tensor_product() -> None:
    """Verifies Kronecker tensor product concatenation and weight computation."""
    p1 = PauliString("ZZ", phase_power=0)
    p2 = PauliString("IX", phase_power=1)
    t = p1.tensor(p2)
    assert t.symbols == ("Z", "Z", "I", "X")
    assert t.phase_power == 1
    assert t.n_carriers == 4
    assert t.weight == 3


def test_symplectic_inner_product_and_commutation() -> None:
    """Verifies equivalence between symplectic inner product and commutation relations."""
    pairs = [
        (PauliString("ZZI"), PauliString("IZZ"), True),   # commute
        (PauliString("XII"), PauliString("ZZI"), False),  # anticommute
        (PauliString("IXI"), PauliString("ZZI"), False),  # anticommute
        (PauliString("IIX"), PauliString("ZZI"), True),   # commute
        (PauliString("ZZZZ"), PauliString("XXXX"), True), # 4 anticommuting loci -> even -> commute
        (PauliString("ZZII"), PauliString("XIXI"), False),# 1 anticommuting locus -> odd -> anticommute
    ]
    for p, q, expected_commute in pairs:
        assert p.commutes_with(q) == expected_commute
        assert p.anticommutes_with(q) == (not expected_commute)
        inner = p.symplectic_inner_product(q)
        assert (inner == 0) == expected_commute


# =============================================================================
# 2. Three-Carrier Bit-Flip Code [[3, 1, 1]] Tests
# =============================================================================


def test_bitflip_code_stabilizers_commute() -> None:
    """Verifies S1 = ZZI and S2 = IZZ commute."""
    assert BitFlipCode3.S1.commutes_with(BitFlipCode3.S2)
    m1 = BitFlipCode3.S1.to_int_matrix()
    m2 = BitFlipCode3.S2.to_int_matrix()
    diff = [[m1[i][j] - m2[i][j] for j in range(8)] for i in range(8)]
    # Commutator [m1, m2] = 0
    comm = int_matrix_multiply(m1, m2)
    comm_rev = int_matrix_multiply(m2, m1)
    for i in range(8):
        for j in range(8):
            assert comm[i][j] == comm_rev[i][j]


def test_bitflip_code_logicals_commute_with_stabilizers() -> None:
    """Verifies Z_L = ZZZ and X_L = XXX commute with both stabilizers S1 and S2."""
    assert BitFlipCode3.Z_L.commutes_with(BitFlipCode3.S1)
    assert BitFlipCode3.Z_L.commutes_with(BitFlipCode3.S2)
    assert BitFlipCode3.X_L.commutes_with(BitFlipCode3.S1)
    assert BitFlipCode3.X_L.commutes_with(BitFlipCode3.S2)


def test_bitflip_code_logicals_anticommute() -> None:
    """Verifies logical operators X_L and Z_L anticommute on the encoded carrier."""
    assert BitFlipCode3.X_L.anticommutes_with(BitFlipCode3.Z_L)


def test_bitflip_code_syndromes_distinct() -> None:
    """Verifies that all 4 single-carrier bit-flip errors produce distinct syndrome pairs."""
    table = BitFlipCode3.syndrome_table_single_bitflips()
    assert len(table) == 4
    expected_syndromes = {
        (0, 0): PauliString("III"),
        (1, 0): PauliString("XII"),
        (1, 1): PauliString("IXI"),
        (0, 1): PauliString("IIX"),
    }
    assert table == expected_syndromes


def test_bitflip_code_deterministic_correction() -> None:
    """Verifies that applying the diagnosed correction recovers the error to identity."""
    errors = [
        PauliString("III"),
        PauliString("XII"),
        PauliString("IXI"),
        PauliString("IIX"),
    ]
    for err in errors:
        correction = BitFlipCode3.correct(err)
        recovered = correction * err
        assert recovered.symbols == ("I", "I", "I")
        assert recovered.phase_power == 0


def test_bitflip_code_projection_idempotence() -> None:
    """Verifies Pi_S^2 = Pi_S exactly and dimension of codespace is 2 (1 logical carrier)."""
    assert check_projection_idempotence(BitFlipCode3.STABILIZERS)
    dim = stabilizer_codespace_dimension(BitFlipCode3.STABILIZERS)
    assert dim == 2


# =============================================================================
# 3. Four-Carrier CSS Torus Code [[4, 2, 2]] Tests
# =============================================================================


def test_torus_code_stabilizers_commute() -> None:
    """Verifies S_Z = ZZZZ and S_X = XXXX commute."""
    assert TorusCode4.S_Z.commutes_with(TorusCode4.S_X)


def test_torus_code_logicals_commute_with_stabilizers() -> None:
    """Verifies both logical pairs commute with S_Z and S_X."""
    logicals = [TorusCode4.Z_L1, TorusCode4.X_L1, TorusCode4.Z_L2, TorusCode4.X_L2]
    for log_op in logicals:
        assert log_op.commutes_with(TorusCode4.S_Z)
        assert log_op.commutes_with(TorusCode4.S_X)


def test_torus_code_independent_logical_algebras() -> None:
    """Verifies the two independent logical Pauli algebras:

    {X_L1, Z_L1} = 0, {X_L2, Z_L2} = 0, and all cross-pair operators commute.
    """
    # Intra-carrier anticommutation
    assert TorusCode4.X_L1.anticommutes_with(TorusCode4.Z_L1)
    assert TorusCode4.X_L2.anticommutes_with(TorusCode4.Z_L2)

    # Cross-carrier commutations
    assert TorusCode4.X_L1.commutes_with(TorusCode4.X_L2)
    assert TorusCode4.Z_L1.commutes_with(TorusCode4.Z_L2)
    assert TorusCode4.X_L1.commutes_with(TorusCode4.Z_L2)
    assert TorusCode4.X_L2.commutes_with(TorusCode4.Z_L1)


def test_torus_code_distance2_error_detection() -> None:
    """Verifies that all 12 single-carrier Pauli errors produce non-trivial syndromes."""
    errs = TorusCode4.all_single_carrier_errors()
    assert len(errs) == 12
    for err in errs:
        syn = TorusCode4.syndrome(err)
        assert syn != (0, 0), f"Error {err} produced trivial syndrome"


def test_torus_code_projection_idempotence() -> None:
    """Verifies Pi_S^2 = Pi_S exactly and dimension of codespace is 4 (2 logical carriers)."""
    assert check_projection_idempotence(TorusCode4.STABILIZERS)
    dim = stabilizer_codespace_dimension(TorusCode4.STABILIZERS)
    assert dim == 4


# =============================================================================
# 4. Steane [[7, 1, 3]] CSS Fano Code Tests
# =============================================================================


def test_fano_dual_lines_intersections() -> None:
    """Verifies Fano dual lines have weight 4 and pairwise even intersection cardinality 2."""
    for line in SteaneCode7.DUAL_LINES:
        assert len(line) == 4
    intersections = SteaneCode7.dual_line_intersections()
    assert len(intersections) == 3
    for (i, j), count in intersections.items():
        assert count == 2
        assert count % 2 == 0


def test_steane_code_all_stabilizers_commute() -> None:
    """Verifies all 6 stabilizer generators commute pairwise (15 distinct pairs)."""
    gens = SteaneCode7.STABILIZERS
    assert len(gens) == 6
    for i in range(6):
        for j in range(i + 1, 6):
            assert gens[i].commutes_with(gens[j]), f"Generators {i} and {j} do not commute"


def test_steane_code_logicals_commute_with_stabilizers() -> None:
    """Verifies logical operators X_L and Z_L commute with all 6 stabilizer generators."""
    for gen in SteaneCode7.STABILIZERS:
        assert SteaneCode7.X_L.commutes_with(gen)
        assert SteaneCode7.Z_L.commutes_with(gen)


def test_steane_code_logicals_anticommute() -> None:
    """Verifies logical operators X_L and Z_L anticommute on the 7-carrier codespace."""
    assert SteaneCode7.X_L.anticommutes_with(SteaneCode7.Z_L)


def test_steane_code_transversal_hadamard_preservation() -> None:
    """Verifies transversal Hadamard H^{tensor 7} maps X-stabilizers to Z-stabilizers."""
    h_x1 = SteaneCode7.transversal_hadamard_transform(SteaneCode7.M_X1)
    h_x2 = SteaneCode7.transversal_hadamard_transform(SteaneCode7.M_X2)
    h_x3 = SteaneCode7.transversal_hadamard_transform(SteaneCode7.M_X3)
    assert h_x1 == SteaneCode7.M_Z1
    assert h_x2 == SteaneCode7.M_Z2
    assert h_x3 == SteaneCode7.M_Z3

    h_z1 = SteaneCode7.transversal_hadamard_transform(SteaneCode7.M_Z1)
    h_z2 = SteaneCode7.transversal_hadamard_transform(SteaneCode7.M_Z2)
    h_z3 = SteaneCode7.transversal_hadamard_transform(SteaneCode7.M_Z3)
    assert h_z1 == SteaneCode7.M_X1
    assert h_z2 == SteaneCode7.M_X2
    assert h_z3 == SteaneCode7.M_X3


def test_steane_code_transversal_hadamard_logical() -> None:
    """Verifies transversal Hadamard exchanges logical X_L and Z_L."""
    h_xl = SteaneCode7.transversal_hadamard_transform(SteaneCode7.X_L)
    h_zl = SteaneCode7.transversal_hadamard_transform(SteaneCode7.Z_L)
    assert h_xl == SteaneCode7.Z_L
    assert h_zl == SteaneCode7.X_L


def test_steane_code_deterministic_error_correction_all_21() -> None:
    """Verifies deterministic diagnosis and recovery of all 21 single-carrier Pauli errors."""
    errs = SteaneCode7.all_single_carrier_errors()
    assert len(errs) == 21

    # Trivial error recovery
    id_err = PauliString("IIIIIII")
    assert SteaneCode7.correct(id_err) == id_err

    # All 21 errors recovery
    for err in errs:
        correction = SteaneCode7.correct(err)
        # correction matches the error up to scalar factor
        assert correction.symbols == err.symbols
        prod = correction * err
        # Corrected state has identity carrier operators
        assert prod.symbols == ("I", "I", "I", "I", "I", "I", "I")


def test_steane_code_projection_idempotence() -> None:
    """Verifies Pi_S^2 = Pi_S exactly and dimension of codespace is 2 (1 logical carrier)."""
    assert check_projection_idempotence(SteaneCode7.STABILIZERS)
    dim = stabilizer_codespace_dimension(SteaneCode7.STABILIZERS)
    assert dim == 2
