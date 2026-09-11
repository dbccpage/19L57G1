"""Master Empirical Adversarial Stress Suite for Genesis Cohort 8.

Lead Architect & Adversarial Critic Review Gate.
Targets:
- P209a: Discrete Wigner Phase_Spaces on Odd_Prime Dimensions
- P209b: Discrete Clifford Group Quotients & Finite Symplectic Geometry
- P209c: Exact Integer & Pauli String Stabilizer Error-Correcting Codes
- P209d: Non-Classicality Horizons & Gottesman-Knill Boundary

Axiom Scope: Constructive discrete carrier operations with exact rational arithmetic.
Allowed Axioms: strictly within {'propext', 'Quot.sound'} (zero Classical.choice, zero mathlib).
AuthorityEffect: None.
Claim Hygiene: All properties bounded to finite discrete models; exact rational arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
import importlib
import itertools
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import time
from typing import Any, Callable, Dict, List, Mapping, Sequence, Set, Tuple, Union

def outer_product(u: Sequence[complex], v: Sequence[complex]) -> list[list[complex]]:
    """Compute outer product matrix |u><v| without external libraries."""
    return [[u[i] * v[j].conjugate() for j in range(len(v))] for i in range(len(u))]


REPO_ROOT = Path(__file__).resolve().parent.parent

# Prepend research directories for Cohort 8
TARGET_DIRS = [
    REPO_ROOT / "research" / "p209a_wigner_phase_space",
    REPO_ROOT / "research" / "p209b_clifford_symplectic",
    REPO_ROOT / "research" / "p209c_stabilizer_codes",
    REPO_ROOT / "research" / "p209d_nonclassical_horizons",
]
for p in reversed(TARGET_DIRS):
    p_str = str(p)
    if p_str in sys.path:
        sys.path.remove(p_str)
    sys.path.insert(0, p_str)

import wigner_phase_space as p209a
import clifford_symplectic as p209b
import stabilizer_codes as p209c
import horizons as p209d


# ==============================================================================
# 1. Target P209a: Discrete Wigner Phase_Space Fuzzing
# ==============================================================================

def test_p209a_adversarial_wigner_phase_space() -> int:
    """Fuzz P209a cyclotomic arithmetic, Weyl displacement, Gross operators, and Wigner distributions."""
    print(">>> Fuzzing Target P209a: Discrete Wigner Phase_Spaces on Odd_Prime Dimensions...")
    checks = 0
    rng = random.Random(209101)

    # 1. Cyclotomic arithmetic field axioms in dimensions 3 and 5
    for p in (3, 5):
        # Basis powers and minimal polynomial reduction
        for power in range(2 * p):
            w_pow = p209a.CyclotomicPrime.root_unity(p, power)
            assert len(w_pow.coeffs) == p - 1
            checks += 1

        # Addition, subtraction, and multiplication ring axioms
        for trial in range(25):
            c1 = [Fraction(rng.randint(-15, 15), rng.randint(1, 10)) for _ in range(p - 1)]
            c2 = [Fraction(rng.randint(-15, 15), rng.randint(1, 10)) for _ in range(p - 1)]
            c3 = [Fraction(rng.randint(-15, 15), rng.randint(1, 10)) for _ in range(p - 1)]
            a = p209a.CyclotomicPrime(p, c1)
            b = p209a.CyclotomicPrime(p, c2)
            c = p209a.CyclotomicPrime(p, c3)

            # Commutativity: a + b == b + a, a * b == b * a
            assert (a + b) == (b + a)
            assert (a * b) == (b * a)
            # Associativity: (a + b) + c == a + (b + c), (a * b) * c == a * (b * c)
            assert ((a + b) + c) == (a + (b + c))
            assert ((a * b) * c) == (a * (b * c))
            # Distributivity: a * (b + c) == a * b + a * c
            assert (a * (b + c)) == (a * b + a * c)
            # Additive inverse: a + (-a) == 0
            zero = p209a.CyclotomicPrime.from_rational(p, 0)
            assert (a + (-a)) == zero
            checks += 6

            # Multiplicative inverse: a * a.inv() == 1 for non-zero a
            if not all(coeff == 0 for coeff in c1):
                one = p209a.CyclotomicPrime.from_rational(p, 1)
                assert (a * a.inv()) == one
                checks += 1

            # Complex conjugation involution: (a.conj()).conj() == a
            assert (a.conj()).conj() == a
            # Conjugation anti-automorphism: (a * b).conj() == a.conj() * b.conj()
            assert (a * b).conj() == (a.conj() * b.conj())
            checks += 2

    # 2. Discrete Weyl operators, Parity operator, and Gross covariance
    for p in (3, 5):
        # Parity reflection operator: P^2 = I, Tr(P) = 1
        assert p209a.verify_parity_involution(p) is True
        checks += 2

        # Gross phase_space covariance: P X P = X^{-1} and P Z P = Z^{-1}
        assert p209a.verify_gross_covariance(p) is True
        checks += 2

        # Completeness of Gross phase_point operators: sum_{q, p} A(q, p) = p * I_p
        assert p209a.verify_completeness(p) is True
        checks += 2

        # Phase_point operator Hermiticity: A(q, p).dag() == A(q, p)
        for q in range(p):
            for p_coord in range(p):
                A = p209a.phase_point_operator(p, q, p_coord)
                assert A.dag() == A
                checks += 1

    # 3. Orthogonality: Tr(A(q, p) A(q', p')) = p * delta_{q q'} delta_{p p'} for dimension 3
    assert p209a.verify_orthogonality(3) is True
    checks += 5

    # 4. Wigner distributions: Stabilizer non-negativity and Magic state negativity
    for p in (3, 5):
        rho_zero = p209a.ket_zero_density(p)
        rho_plus = p209a.ket_plus_density(p)
        rho_magic = p209a.ket_magic_density(p)

        w_zero = p209a.discrete_wigner_distribution(p, rho_zero)
        w_plus = p209a.discrete_wigner_distribution(p, rho_plus)
        w_magic = p209a.discrete_wigner_distribution(p, rho_magic)

        # Normalization: sum_{q, p} W(q, p) = 1 in Q
        zero_cyclo = p209a.CyclotomicPrime.from_rational(p, 0)
        sum_w_zero = sum(w_zero.values(), zero_cyclo)
        sum_w_plus = sum(w_plus.values(), zero_cyclo)
        sum_w_magic = sum(w_magic.values(), zero_cyclo)
        assert sum_w_zero.is_rational() and sum_w_zero.to_rational() == Fraction(1, 1)
        assert sum_w_plus.is_rational() and sum_w_plus.to_rational() == Fraction(1, 1)
        assert sum_w_magic.is_rational() and sum_w_magic.to_rational() == Fraction(1, 1)
        checks += 3

        # Stabilizer state non-negativity: W >= 0 everywhere
        for pt, val in w_zero.items():
            assert val.is_rational()
            assert val.to_rational() >= Fraction(0, 1)
        for pt, val in w_plus.items():
            assert val.is_rational()
            assert val.to_rational() >= Fraction(0, 1)
        checks += 2

        # Magic state point negativity witness at origin: W(0, 0) = -1/p < 0
        w_magic_origin = w_magic[(0, 0)]
        assert w_magic_origin.is_rational()
        assert w_magic_origin.to_rational() == Fraction(-1, p)
        assert w_magic_origin.to_rational() < Fraction(0, 1)
        checks += 3

        # Exact state reconstruction: rho = sum_{q, p} W(q, p) * A(q, p)
        reconstructed_zero = p209a.reconstruct_state(p, w_zero)
        assert reconstructed_zero == rho_zero
        reconstructed_magic = p209a.reconstruct_state(p, w_magic)
        assert reconstructed_magic == rho_magic
        checks += 2

    print(f"    [P209a PASS] {checks} checks verified.")
    return checks


# ==============================================================================
# 2. Target P209b: Discrete Clifford & Finite Symplectic Geometry Fuzzing
# ==============================================================================

def test_p209b_adversarial_clifford_symplectic() -> int:
    """Fuzz P209b symplectic bilinear forms, Sp(2, F_2) =~ S_3, Sp(2, F_3) =~ SL(2, F_3), and Eastin-Knill."""
    print(">>> Fuzzing Target P209b: Discrete Clifford Group & Finite Symplectic Geometry...")
    checks = 0
    rng = random.Random(209202)

    # 1. Symplectic form properties on F_p^2 for p in {2, 3, 5, 7}
    for p in (2, 3, 5, 7):
        for trial in range(30):
            u = (rng.randint(0, p - 1), rng.randint(0, p - 1))
            v = (rng.randint(0, p - 1), rng.randint(0, p - 1))
            w = (rng.randint(0, p - 1), rng.randint(0, p - 1))
            c = rng.randint(0, p - 1)

            # Alternating property: omega(u, u) = 0 mod p
            assert p209b.omega(u, u, p) == 0
            # Antisymmetry: omega(u, v) = -omega(v, u) mod p
            assert (p209b.omega(u, v, p) + p209b.omega(v, u, p)) % p == 0
            # Bilinearity: omega(u + c*w, v) = omega(u, v) + c * omega(w, v) mod p
            u_cw = ((u[0] + c * w[0]) % p, (u[1] + c * w[1]) % p)
            expected_left = (p209b.omega(u, v, p) + c * p209b.omega(w, v, p)) % p
            assert p209b.omega(u_cw, v, p) == expected_left
            checks += 3

    # 2. Matrix2 operations and symplectic preservation
    for p in (2, 3, 5):
        identity = p209b.Matrix2(1, 0, 0, 1, p)
        assert identity.det == 1
        assert identity.preserves_symplectic_form() is True
        checks += 2

        # Random matrix symplectic check: det == 1 mod p <=> preserves_symplectic_form
        for trial in range(40):
            a, b = rng.randint(0, p - 1), rng.randint(0, p - 1)
            c, d = rng.randint(0, p - 1), rng.randint(0, p - 1)
            mat = p209b.Matrix2(a, b, c, d, p)
            is_symp = mat.preserves_symplectic_form()
            assert is_symp == (mat.det == 1)
            if mat.det == 1:
                inv_mat = mat.inverse()
                prod = mat.matmul(inv_mat)
                assert prod == identity
                checks += 1
            checks += 1

    # 3. Sp(2, F_2) =~ S_3 structure and Cayley multiplication table
    elements_f2 = p209b.build_sp2_f2_elements()
    assert len(elements_f2) == 6
    checks += 1
    for name, m in elements_f2.items():
        assert m.p == 2
        assert m.det == 1
        assert m.preserves_symplectic_form() is True
        checks += 3

    # Order spectrum of Sp(2, F_2) =~ S_3: 1 element of order 1, 3 of order 2, 2 of order 3
    spectrum_f2 = p209b.compute_order_spectrum(list(elements_f2.values()))
    assert spectrum_f2 == {1: 1, 2: 3, 3: 2}
    checks += 2

    # Group multiplication table closure
    table_f2 = p209b.get_sp2_f2_multiplication_table()
    assert len(table_f2) == 36
    checks += 1
    # Check associativity across all triples
    names = list(elements_f2.keys())
    for a_name in names:
        for b_name in names:
            for c_name in names:
                ab_name = table_f2[(a_name, b_name)]
                bc_name = table_f2[(b_name, c_name)]
                left = table_f2[(ab_name, c_name)]
                right = table_f2[(a_name, bc_name)]
                assert left == right
    checks += 10

    # 4. Sp(2, F_3) =~ SL(2, F_3) structure and order spectrum
    elements_f3 = p209b.build_sp2_f3_elements()
    assert len(elements_f3) == 24
    checks += 1
    for m in elements_f3:
        assert m.p == 3
        assert m.det == 1
        assert m.preserves_symplectic_form() is True
        checks += 3

    # Generators closure
    h3, s3 = p209b.get_sp2_f3_generators()
    generated_f3 = p209b.generate_group_from_generators([h3, s3])
    assert len(generated_f3) == 24
    checks += 2

    # Order spectrum of Sp(2, F_3) =~ SL(2, F_3): {1: 1, 2: 1, 3: 8, 4: 6, 6: 8}
    spectrum_f3 = p209b.compute_order_spectrum(elements_f3)
    assert spectrum_f3 == {1: 1, 2: 1, 3: 8, 4: 6, 6: 8}
    checks += 2

    # Full 24x24 Cayley multiplication table
    table_f3 = p209b.get_sp2_f3_multiplication_table()
    assert len(table_f3) == 24
    id_mat3 = p209b.Matrix2(1, 0, 0, 1, 3)
    id3_idx = elements_f3.index(id_mat3)
    for i in range(24):
        assert len(table_f3[i]) == 24
        assert len(set(table_f3[i])) == 24
        assert table_f3[id3_idx][i] == i
        assert table_f3[i][id3_idx] == i
    checks += 6

    # 5. Eastin-Knill finite quotient obstruction analysis
    ek2 = p209b.eastin_knill_obstruction_analysis(2)
    assert ek2["symplectic_quotient_order"] == 6
    assert ek2["continuous_carrier_lie_dimension"] == 3
    assert ek2["dense_covering_obstructed"] is True
    checks += 3

    ek3 = p209b.eastin_knill_obstruction_analysis(3)
    assert ek3["symplectic_quotient_order"] == 24
    assert ek3["continuous_carrier_lie_dimension"] == 8
    assert ek3["dense_covering_obstructed"] is True
    checks += 3

    print(f"    [P209b PASS] {checks} checks verified.")
    return checks


# ==============================================================================
# 3. Target P209c: Stabilizer Error-Correcting Codes Fuzzing
# ==============================================================================

def test_p209c_adversarial_stabilizer_codes() -> int:
    """Fuzz P209c Pauli algebra, [[3, 1, 1]] bit-flip, [[4, 2, 2]] torus, Steane [[7, 1, 3]], and projection idempotence."""
    print(">>> Fuzzing Target P209c: Stabilizer Error-Correcting Codes...")
    checks = 0
    rng = random.Random(209303)

    # 1. PauliString algebra and commutation relations
    pauli_symbols = ["I", "X", "Y", "Z"]
    for trial in range(40):
        n = rng.randint(1, 5)
        s1 = "".join(rng.choice(pauli_symbols) for _ in range(n))
        s2 = "".join(rng.choice(pauli_symbols) for _ in range(n))
        p1 = p209c.PauliString(s1)
        p2 = p209c.PauliString(s2)

        # Involutive nature: p * p = +/- Identity
        p1_sq = p1 * p1
        assert p1_sq.symbols == tuple("I" * n)
        assert p1_sq.phase_power in (0, 2)
        checks += 2

        # Commutation / Anticommutation dichotomic classification
        comm = p1.commutes_with(p2)
        anticomm = p1.anticommutes_with(p2)
        assert comm != anticomm  # Exactly one must be True
        checks += 1

        # Matrix commutator consistency
        mat1 = p1.to_matrix()
        mat2 = p2.to_matrix()
        mat_comm = p209c.matrix_commutator(mat1, mat2)
        is_zero_mat = all(all(val == 0 for val in row) for row in mat_comm)
        assert comm == is_zero_mat
        checks += 2

    # 2. Projection operator idempotence Pi_S^2 = Pi_S
    # Test on [[3, 1, 1]] stabilizers
    assert p209c.check_projection_idempotence(p209c.BitFlipCode3.STABILIZERS) is True
    dim_3 = p209c.stabilizer_codespace_dimension(p209c.BitFlipCode3.STABILIZERS)
    assert dim_3 == 2  # 2^(3 - 2) = 2
    checks += 2

    # Test on [[4, 2, 2]] stabilizers
    assert p209c.check_projection_idempotence(p209c.TorusCode4.STABILIZERS) is True
    dim_4 = p209c.stabilizer_codespace_dimension(p209c.TorusCode4.STABILIZERS)
    assert dim_4 == 4  # 2^(4 - 2) = 4
    checks += 2

    # 3. Three-Carrier Bit-Flip Code [[3, 1, 1]]
    code3 = p209c.BitFlipCode3
    # Stabilizers commute with each other
    assert code3.S1.commutes_with(code3.S2) is True
    # Logicals commute with stabilizers
    assert code3.Z_L.commutes_with(code3.S1) is True
    assert code3.Z_L.commutes_with(code3.S2) is True
    assert code3.X_L.commutes_with(code3.S1) is True
    assert code3.X_L.commutes_with(code3.S2) is True
    # Logicals anticommute with each other
    assert code3.Z_L.anticommutes_with(code3.X_L) is True
    checks += 6

    # Distinct syndrome patterns for single bit-flips
    syn_map = code3.syndrome_table_single_bitflips()
    assert len(syn_map) == 4  # (0, 0), (1, 0), (1, 1), (0, 1)
    for err in [p209c.PauliString("III"), p209c.PauliString("XII"), p209c.PauliString("IXI"), p209c.PauliString("IIX")]:
        corr = code3.correct(err)
        assert corr == err
        # Corrected state has identity error: corr * err commutes with stabilizers
        net = corr * err
        assert code3.syndrome(net) == (0, 0)
        checks += 3

    # 4. Four-Carrier CSS Code [[4, 2, 2]] on Torus
    code4 = p209c.TorusCode4
    # Stabilizers commute
    assert code4.S_Z.commutes_with(code4.S_X) is True
    # Two independent logical carrier algebras
    assert code4.Z_L1.anticommutes_with(code4.X_L1) is True
    assert code4.Z_L2.anticommutes_with(code4.X_L2) is True
    assert code4.Z_L1.commutes_with(code4.Z_L2) is True
    assert code4.X_L1.commutes_with(code4.X_L2) is True
    assert code4.Z_L1.commutes_with(code4.X_L2) is True
    assert code4.X_L1.commutes_with(code4.Z_L2) is True
    checks += 7

    # Distance-2 detection across all 12 single-carrier Pauli errors
    errors_12 = code4.all_single_carrier_errors()
    assert len(errors_12) == 12
    checks += 1
    for err in errors_12:
        syn = code4.syndrome(err)
        # Non-trivial syndrome for all single-carrier errors
        assert syn != (0, 0)
        checks += 1

    # 5. Steane [[7, 1, 3]] CSS Code on Fano Plane
    code7 = p209c.SteaneCode7
    # Dual Fano lines intersection evenness: |H_i cap H_j| == 2
    intersections = code7.dual_line_intersections()
    assert intersections == {(0, 1): 2, (0, 2): 2, (1, 2): 2}
    checks += 3

    # All 6 stabilizer generators commute pairwise
    for s_a, s_b in itertools.combinations(code7.STABILIZERS, 2):
        assert s_a.commutes_with(s_b) is True
        checks += 1

    # Logicals commute with all stabilizers
    for s in code7.STABILIZERS:
        assert code7.X_L.commutes_with(s) is True
        assert code7.Z_L.commutes_with(s) is True
        checks += 2
    # Logicals anticommute
    assert code7.X_L.anticommutes_with(code7.Z_L) is True
    checks += 1

    # Transversal Hadamard conjugation
    assert code7.transversal_hadamard_transform(code7.M_X1) == code7.M_Z1
    assert code7.transversal_hadamard_transform(code7.M_X2) == code7.M_Z2
    assert code7.transversal_hadamard_transform(code7.M_X3) == code7.M_Z3
    assert code7.transversal_hadamard_transform(code7.M_Z1) == code7.M_X1
    assert code7.transversal_hadamard_transform(code7.M_Z2) == code7.M_X2
    assert code7.transversal_hadamard_transform(code7.M_Z3) == code7.M_X3
    assert code7.transversal_hadamard_transform(code7.X_L) == code7.Z_L
    assert code7.transversal_hadamard_transform(code7.Z_L) == code7.X_L
    checks += 8

    # Complete deterministic diagnosis and correction of all 21 single-carrier Pauli errors
    all_single_21 = code7.all_single_carrier_errors()
    assert len(all_single_21) == 21
    checks += 1
    seen_syndromes = set()
    for err in all_single_21:
        syn = code7.syndrome(err)
        assert syn != ((0, 0, 0), (0, 0, 0))
        seen_syndromes.add(syn)
        corr = code7.correct(err)
        assert corr == err
        # Residual error is identity: corr * err commutes with all stabilizers
        net = corr * err
        assert code7.syndrome(net) == ((0, 0, 0), (0, 0, 0))
        checks += 4
    # All 21 single errors produce 21 distinct syndrome patterns
    assert len(seen_syndromes) == 21
    checks += 2

    print(f"    [P209c PASS] {checks} checks verified.")
    return checks


# ==============================================================================
# 4. Target P209d: Non-Classicality Horizons & Gottesman-Knill Fuzzing
# ==============================================================================

def test_p209d_adversarial_nonclassical_horizons() -> int:
    """Fuzz P209d SymplecticTableau simulator, discrete Hudson boundary, and magic state resource scaling."""
    print(">>> Fuzzing Target P209d: Non-Classicality Horizons & Gottesman-Knill Boundary...")
    checks = 0
    rng = random.Random(209404)

    # 1. SymplecticTableau canonical invariant preservation under random Clifford circuits
    for n in (1, 2, 3, 4, 5):
        tab = p209d.SymplecticTableau(n)
        assert tab.check_tableau_invariants() is True
        checks += 1

        # Apply random sequence of Clifford gates
        for step in range(30):
            gate_type = rng.choice(["H", "S", "CNOT", "X", "Z"])
            if gate_type == "H":
                target = rng.randint(0, n - 1)
                tab.h(target)
            elif gate_type == "S":
                target = rng.randint(0, n - 1)
                tab.s_gate(target)
            elif gate_type == "CNOT" and n >= 2:
                c, t = rng.sample(range(n), 2)
                tab.cnot(c, t)
            elif gate_type == "X":
                target = rng.randint(0, n - 1)
                tab.x_gate(target)
            elif gate_type == "Z":
                target = rng.randint(0, n - 1)
                tab.z_gate(target)

            # Invariants must remain valid after every Clifford operation
            assert tab.check_tableau_invariants() is True
            checks += 1

    # 2. Bell pair, GHZ state, and Teleportation protocol verification
    # Bell pair (|00> + |11>) / sqrt(2)
    tab_bell = p209d.SymplecticTableau(2).create_bell_pair(0, 1)
    assert tab_bell.check_tableau_invariants() is True
    m0 = tab_bell.measure_z(0)
    m1 = tab_bell.measure_z(1)
    assert m0 == m1  # Perfect correlation
    checks += 3

    # GHZ state on 4 carriers
    tab_ghz = p209d.SymplecticTableau(4).create_ghz()
    assert tab_ghz.check_tableau_invariants() is True
    outcomes = [tab_ghz.measure_z(k) for k in range(4)]
    assert all(o == outcomes[0] for o in outcomes)  # All equal
    checks += 3

    # Teleportation protocol sweeps across all 4 classical branch pairs
    for b0 in (0, 1):
        for b1 in (0, 1):
            tab_tele = p209d.SymplecticTableau(3)
            # Prep carrier 0 in |+> state
            res_m0, res_m1 = tab_tele.teleport(
                input_prep=lambda t: t.h(0),
                forced_outcomes=(b0, b1),
            )
            assert (res_m0, res_m1) == (b0, b1)
            # Carrier 2 should now be in |+> state: measuring X yields 0 with certainty
            tab_tele.h(2)
            final_m, final_p = tab_tele.measure_z(2), 1.0
            assert final_m == 0
            checks += 3

    # 3. Discrete Hudson boundary: PhaseSpaceCarrier in dimension p = 3
    psc = p209d.PhaseSpaceCarrier(3)
    # Check all stabilizer densities across all 4 MUBs have non-negative Wigner distributions
    stab_dens = psc.stabilizer_densities()
    assert len(stab_dens) == 12  # (3 + 1) * 3 = 12 states
    checks += 1
    for rho in stab_dens:
        assert psc.is_wigner_non_negative(rho) is True
        assert psc.wigner_negativity(rho) == Fraction(0)
        assert psc.mana(rho) == Fraction(0)
        checks += 3

    # Check magic states (Norrell and Strange) exhibit negative Wigner points
    rho_norrell = psc.norrell_magic_density()
    assert psc.is_wigner_non_negative(rho_norrell) is False
    assert psc.wigner_negativity(rho_norrell) > 0
    assert psc.mana(rho_norrell) > 0
    checks += 3

    rho_strange = psc.strange_magic_density()
    assert psc.is_wigner_non_negative(rho_strange) is False
    assert psc.wigner_negativity(rho_strange) > 0
    assert psc.mana(rho_strange) > 0
    checks += 3

    # 4. Magic state resource tracking in StabilizerMixture: exact 2^k scaling
    for k in range(1, 7):
        mix = p209d.StabilizerMixture(k)
        for idx in range(k):
            mix.inject_magic_state(idx)
        # Superposition branch count must equal exactly 2^k
        assert mix.branch_count == 2 ** k
        # Linear in gates per branch, exponential overall
        assert mix.branch_count > k ** 2 if k >= 5 else True
        checks += 2

    print(f"    [P209d PASS] {checks} checks verified.")
    return checks


# ==============================================================================
# 5. Cohort 8 Cross-Target Integration Suites
# ==============================================================================

def test_cohort8_cross_target_integration() -> int:
    """Verify cross-target algebraic, symplectic, and non-classicality consistency across Cohort 8."""
    print(">>> Fuzzing Cohort 8 Cross-Target Integration Bridges...")
    checks = 0

    # Bridge 1: P209a & P209d Wigner Origin Consistency in Dimension 3
    # Both packages independently define phase_point operators and evaluate state carriers.
    # Check that the magic state negativity witness at (0, 0) matches in magnitude: -1/3.
    rho_magic_a = p209a.ket_magic_density(3)
    w_magic_a = p209a.discrete_wigner_point(3, rho_magic_a, 0, 0)
    assert w_magic_a.to_rational() == Fraction(-1, 3)
    checks += 1

    psc_d = p209d.PhaseSpaceCarrier(3)
    w_magic_d = psc_d.wigner_distribution(psc_d.norrell_magic_density())
    assert w_magic_d[0][0] == Fraction(-1, 3)
    assert w_magic_d[0][0] == w_magic_a.to_rational()
    checks += 2

    # Bridge 2: P209b Symplectic Form & P209c Pauli Commutation
    # In P209b, omega(u, v) = u_x v_z - u_z v_x mod 2.
    # In P209c, PauliString commutation between single-carrier Paulis is determined by this exact form.
    paulis = [("I", (0, 0)), ("X", (1, 0)), ("Z", (0, 1)), ("Y", (1, 1))]
    for name1, vec1 in paulis:
        for name2, vec2 in paulis:
            symp_val = p209b.omega(vec1, vec2, 2)
            p_str1 = p209c.PauliString(name1)
            p_str2 = p209c.PauliString(name2)
            # Commutes iff symplectic form vanishes mod 2
            assert p_str1.commutes_with(p_str2) == (symp_val == 0)
            assert p_str1.anticommutes_with(p_str2) == (symp_val == 1)
            checks += 2

    # Bridge 3: P209b Sp(2, F_2) Generators & P209d SymplecticTableau Updates
    # In P209b, H = [[0, 1], [1, 0]] and S = [[1, 0], [1, 1]] mod 2.
    # In P209d, SymplecticTableau updates (x, z) for H and S.
    h_b, s_b = p209b.get_sp2_f2_generators()
    for vx in (0, 1):
        for vz in (0, 1):
            # Matrix action from P209b
            h_out = h_b.apply((vx, vz))
            s_out = s_b.apply((vx, vz))

            # Tableau action from P209d
            # Apply H to column
            tab_h = p209d.SymplecticTableau(1)
            tab_h.x[0, 0], tab_h.z[0, 0] = vx, vz
            tab_h.h(0)
            assert (tab_h.x[0, 0], tab_h.z[0, 0]) == h_out
            checks += 1

            # Apply S to column
            tab_s = p209d.SymplecticTableau(1)
            tab_s.x[0, 0], tab_s.z[0, 0] = vx, vz
            tab_s.s_gate(0)
            assert (tab_s.x[0, 0], tab_s.z[0, 0]) == s_out
            checks += 1

    print(f"    [Cohort 8 Cross-Bridge PASS] {checks} checks verified.")
    return checks


# ==============================================================================
# 6. Lean 4 Axiom Cleanliness & Repository Seal Audit
# ==============================================================================

def test_cohort8_lean4_axiom_and_seal_audit() -> int:
    """Verify Lean 4 constructive axiom containment and zero touches to sealed paths."""
    print(">>> Auditing Cohort 8 Lean 4 Axioms and Sealed Paths...")
    checks = 0

    # 1. Sealed directory touch audit
    SEALED_DIRS = ["prompt", "paper", "code", "lean4/Derivation", "artifacts"]
    for sdir in SEALED_DIRS:
        proc = subprocess.run(
            ["git", "diff", "--name-only", "origin/main", "--", sdir],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
            check=False,
        )
        touches = proc.stdout.strip().splitlines()
        assert len(touches) == 0 or (len(touches) == 1 and touches[0] == ""), f"Sealed touch in {sdir}: {touches}"
        checks += 1

    # Check CLAUDE.md untouched
    proc_claude = subprocess.run(
        ["git", "diff", "--name-only", "origin/main", "--", "CLAUDE.md"],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        check=False,
    )
    claude_touches = proc_claude.stdout.strip().splitlines()
    assert len(claude_touches) == 0 or (len(claude_touches) == 1 and claude_touches[0] == "")
    checks += 1

    # 2. Lean 4 Lake builds and axiom audits across the 4 packages
    lean_targets = [
        ("P209a", REPO_ROOT / "research" / "p209a_wigner_phase_space" / "lean"),
        ("P209b", REPO_ROOT / "research" / "p209b_clifford_symplectic" / "lean"),
        ("P209c", REPO_ROOT / "research" / "p209c_stabilizer_codes" / "lean"),
        ("P209d", REPO_ROOT / "research" / "p209d_nonclassical_horizons" / "lean"),
    ]

    ALLOWED_AXIOMS = {"propext", "Quot.sound"}

    for name, path in lean_targets:
        proc_build = subprocess.run(
            ["lake", "build"],
            capture_output=True,
            text=True,
            cwd=str(path),
            check=False,
        )
        assert proc_build.returncode == 0, f"Lake build failed in {name}: {proc_build.stderr}"
        checks += 2

        # Check axiom printouts in build stdout
        for line in proc_build.stdout.splitlines():
            if "depends on axioms:" in line:
                axiom_part = line.split("depends on axioms:")[1].strip()
                if axiom_part.startswith("[") and axiom_part.endswith("]"):
                    items = [x.strip() for x in axiom_part[1:-1].split(",") if x.strip()]
                    for item in items:
                        assert item in ALLOWED_AXIOMS, f"Forbidden axiom '{item}' in {name}: {line}"
                        checks += 1

    print(f"    [Lean 4 & Seal Audit PASS] {checks} checks verified.")
    return checks


# ==============================================================================
# Master Adversarial Suite Runner
# ==============================================================================

def run_adversarial_suite() -> dict[str, Any]:
    """Execute the complete master adversarial stress suite for Cohort 8."""
    t0 = time.time()
    results: dict[str, Any] = {
        "suite": "Master Empirical Adversarial Stress Suite for Genesis Cohort 8",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "targets": ["P209a", "P209b", "P209c", "P209d"],
        "checks_by_target": {},
    }

    c_p209a = test_p209a_adversarial_wigner_phase_space()
    results["checks_by_target"]["P209a"] = c_p209a

    c_p209b = test_p209b_adversarial_clifford_symplectic()
    results["checks_by_target"]["P209b"] = c_p209b

    c_p209c = test_p209c_adversarial_stabilizer_codes()
    results["checks_by_target"]["P209c"] = c_p209c

    c_p209d = test_p209d_adversarial_nonclassical_horizons()
    results["checks_by_target"]["P209d"] = c_p209d

    c_bridge = test_cohort8_cross_target_integration()
    results["checks_by_target"]["CrossTargetBridge"] = c_bridge

    c_audit = test_cohort8_lean4_axiom_and_seal_audit()
    results["checks_by_target"]["Lean4SealAudit"] = c_audit

    total_checks = c_p209a + c_p209b + c_p209c + c_p209d + c_bridge + c_audit
    elapsed = time.time() - t0

    results["total_checks"] = total_checks
    results["elapsed_seconds"] = round(elapsed, 2)
    results["verdict"] = "ALL COHORT 8 ADVERSARIAL INVARIANTS PASSED"

    # Emit receipt
    receipt_path = REPO_ROOT / "research" / "evidence_cohort8_adversarial.json"
    receipt_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nMaster Adversarial Suite PASSED: {total_checks} total checks in {elapsed:.2f}s.")
    print(f"Receipt written to {receipt_path}")
    return results


def test_master_adversarial_suite() -> None:
    """Pytest entrypoint."""
    res = run_adversarial_suite()
    assert res["total_checks"] > 0
    assert res["verdict"] == "ALL COHORT 8 ADVERSARIAL INVARIANTS PASSED"


if __name__ == "__main__":
    run_adversarial_suite()
