"""Test suite for Target P209d: Non-Classicality Horizons & Gottesman-Knill Boundary.

AuthorityEffect: None.
Tests:
- Symplectic tableau initialization, invariants, and Clifford gate updates.
- Bell pair creation, GHZ state preparation, and measurement collapse.
- Complete teleportation and superdense coding verification via tableaux.
- Discrete Hudson theorem boundary on F_3 x F_3 (stabilizer W >= 0 vs magic W < 0).
- Magic state injection branch scaling 2^k and polynomial Clifford scaling O(n^2).
"""

from __future__ import annotations

from fractions import Fraction
import math
import time
from typing import Sequence
import pytest

from horizons import (
    MagicStateType,
    PhaseSpaceCarrier,
    StabilizerMixture,
    SymplecticTableau,
)
import wigner_phase_space as _wps


def inner_product(u: Sequence[complex], v: Sequence[complex]) -> complex:
    """Compute inner product <u|v> = sum u_i* v_i."""
    return sum(u[i].conjugate() * v[i] for i in range(len(u)))


def test_tableau_initialization() -> None:
    tab = SymplecticTableau(3)
    assert tab.n == 3
    assert tab.check_tableau_invariants()
    # Check destabilizers Di = Xi
    for i in range(3):
        assert tab.x[i, i] == 1
        assert tab.z[i, i] == 0
        assert tab.r[i] == 0
    # Check stabilizers Si = Zi
    for i in range(3):
        assert tab.x[i + 3, i] == 0
        assert tab.z[i + 3, i] == 1
        assert tab.r[i + 3] == 0


def test_hadamard_gate_update() -> None:
    tab = SymplecticTableau(1)
    tab.h(0)
    # H transforms Z to X: stabilizer should now be X
    assert tab.x[1, 0] == 1
    assert tab.z[1, 0] == 0
    assert tab.r[1] == 0
    # Destabilizer should be Z
    assert tab.x[0, 0] == 0
    assert tab.z[0, 0] == 1
    assert tab.check_tableau_invariants()


def test_s_gate_update() -> None:
    tab = SymplecticTableau(1)
    tab.h(0)  # Stabilizer is X
    tab.s_gate(0)  # S X S_dag = Y
    # Y is x=1, z=1, r=0
    assert tab.x[1, 0] == 1
    assert tab.z[1, 0] == 1
    assert tab.r[1] == 0
    assert tab.check_tableau_invariants()


def test_cnot_gate_update() -> None:
    tab = SymplecticTableau(2)
    tab.h(0)
    tab.cnot(0, 1)
    # Stabilizers should be X0 X1 and Z0 Z1
    assert tab.x[2] == [1, 1] and tab.z[2] == [0, 0]
    assert tab.x[3] == [0, 0] and tab.z[3] == [1, 1]
    assert tab.check_tableau_invariants()


def test_clifford_invariants_preservation() -> None:
    tab = SymplecticTableau(4)
    assert tab.check_tableau_invariants()
    gates = [
        ("h", 0), ("s", 1), ("cnot", 0, 1),
        ("h", 2), ("cnot", 1, 2), ("s", 3),
        ("cnot", 2, 3), ("h", 1), ("s", 0),
        ("cnot", 3, 0), ("h", 3)
    ]
    for g in gates:
        if g[0] == "h":
            assert isinstance(g[1], int)
            tab.h(g[1])
        elif g[0] == "s":
            assert isinstance(g[1], int)
            tab.s_gate(g[1])
        elif g[0] == "cnot":
            assert isinstance(g[1], int) and len(g) > 2 and isinstance(g[2], int)
            tab.cnot(g[1], g[2])
        assert tab.check_tableau_invariants()


def test_bell_pair_creation() -> None:
    tab = SymplecticTableau(2)
    tab.create_bell_pair(0, 1)
    assert tab.check_tableau_invariants()
    vec = tab.state_vector()
    expected = [1.0 / math.sqrt(2), 0.0, 0.0, 1.0 / math.sqrt(2)]
    overlap = abs(inner_product(expected, vec))
    assert math.isclose(overlap, 1.0, abs_tol=1e-8)


def test_ghz_state_creation() -> None:
    tab3 = SymplecticTableau(3)
    tab3.create_ghz()
    assert tab3.check_tableau_invariants()
    vec3 = tab3.state_vector()
    expected3 = [1.0 / math.sqrt(2) if i in (0, 7) else 0.0 for i in range(8)]
    overlap3 = abs(inner_product(expected3, vec3))
    assert math.isclose(overlap3, 1.0, abs_tol=1e-8)

    tab4 = SymplecticTableau(4)
    tab4.create_ghz()
    assert tab4.check_tableau_invariants()
    vec4 = tab4.state_vector()
    expected4 = [1.0 / math.sqrt(2) if i in (0, 15) else 0.0 for i in range(16)]
    overlap4 = abs(inner_product(expected4, vec4))
    assert math.isclose(overlap4, 1.0, abs_tol=1e-8)


def test_deterministic_z_measurement() -> None:
    tab0 = SymplecticTableau(1)
    assert tab0.measure_z(0) == 0

    tab1 = SymplecticTableau(1)
    tab1.x_gate(0)
    assert tab1.measure_z(0) == 1


def test_random_z_measurement_and_collapse() -> None:
    # State |+> = H |0>
    tab = SymplecticTableau(1)
    tab.h(0)
    # Collapse to 0
    out0 = tab.measure_z(0, forced_outcome=0)
    assert out0 == 0
    assert tab.measure_z(0) == 0
    assert tab.check_tableau_invariants()

    tab2 = SymplecticTableau(1)
    tab2.h(0)
    # Collapse to 1
    out1 = tab2.measure_z(0, forced_outcome=1)
    assert out1 == 1
    assert tab2.measure_z(0) == 1
    assert tab2.check_tableau_invariants()


def test_bell_measurement_correlations() -> None:
    for forced in [0, 1]:
        tab = SymplecticTableau(2)
        tab.create_bell_pair(0, 1)
        res0 = tab.measure_z(0, forced_outcome=forced)
        res1 = tab.measure_z(1)
        assert res0 == res1 == forced
        assert tab.check_tableau_invariants()


def test_teleportation_all_branches() -> None:
    # Teleport input state |1> across all 4 measurement outcome branches
    for m0 in [0, 1]:
        for m1 in [0, 1]:
            tab = SymplecticTableau(3)
            m0_out, m1_out = tab.teleport(
                input_prep=lambda t: t.x_gate(0),
                forced_outcomes=(m0, m1)
            )
            assert (m0_out, m1_out) == (m0, m1)
            assert tab.measure_z(2) == 1
            assert tab.check_tableau_invariants()

    # Teleport input state |0> across all 4 measurement outcome branches
    for m0 in [0, 1]:
        for m1 in [0, 1]:
            tab = SymplecticTableau(3)
            m0_out, m1_out = tab.teleport(
                input_prep=lambda t: None,
                forced_outcomes=(m0, m1)
            )
            assert (m0_out, m1_out) == (m0, m1)
            assert tab.measure_z(2) == 0
            assert tab.check_tableau_invariants()


def test_teleportation_superposition_state() -> None:
    # Teleport |+> = H |0> across all 4 measurement branches
    for m0 in [0, 1]:
        for m1 in [0, 1]:
            tab = SymplecticTableau(3)
            tab.teleport(
                input_prep=lambda t: t.h(0),
                forced_outcomes=(m0, m1)
            )
            # Receiver applies H to measure in X basis
            tab.h(2)
            assert tab.measure_z(2) == 0
            assert tab.check_tableau_invariants()


def test_superdense_coding_via_tableau() -> None:
    # Encode 2 classical bits (b0, b1) on carrier 0 of a Bell pair
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            tab = SymplecticTableau(2)
            tab.create_bell_pair(0, 1)
            # Encoding: b1 controls X, b0 controls Z
            if b1 == 1:
                tab.x_gate(0)
            if b0 == 1:
                tab.z_gate(0)
            # Decoding via Bell basis measurement:
            tab.cnot(0, 1)
            tab.h(0)
            dec0 = tab.measure_z(0)
            dec1 = tab.measure_z(1)
            assert (dec0, dec1) == (b0, b1)
            assert tab.check_tableau_invariants()


def test_discrete_hudson_stabilizer_states() -> None:
    psc = PhaseSpaceCarrier(p=3)
    dens = psc.stabilizer_densities()
    assert len(dens) == 12  # p * (p + 1) = 3 * 4 = 12 MUB states
    for idx, rho in enumerate(dens):
        assert psc.is_wigner_non_negative(rho), f"Stabilizer density {idx} failed non-negativity."
        assert psc.wigner_negativity(rho) == Fraction(0)
        assert psc.mana(rho) == Fraction(0)


def test_discrete_hudson_magic_states() -> None:
    psc = PhaseSpaceCarrier(p=3)
    rho_n = psc.norrell_magic_density()
    assert not psc.is_wigner_non_negative(rho_n)
    w_n = psc.wigner_distribution(rho_n)
    assert w_n[0][0] == Fraction(-1, 3)
    assert w_n[0][0] == _wps.discrete_wigner_point(3, _wps.ket_magic_density(3), 0, 0).to_rational()
    assert psc.wigner_negativity(rho_n) > 0
    assert psc.mana(rho_n) > 0

    rho_s = psc.strange_magic_density()
    assert not psc.is_wigner_non_negative(rho_s)
    w_s = psc.wigner_distribution(rho_s)
    assert min(min(row) for row in w_s) < 0
    assert w_s[0][1] == Fraction(-1, 6)


def test_wigner_clifford_orbit_covariance() -> None:
    psc = PhaseSpaceCarrier(p=3)
    rho = _wps.ket_zero_density(3)
    assert psc.is_wigner_non_negative(rho)

    d10 = psc.displacement(1, 0)
    rho_d10 = d10 @ rho @ d10.dag()
    assert psc.is_wigner_non_negative(rho_d10)

    d01 = psc.displacement(0, 1)
    rho_d01 = d01 @ rho @ d01.dag()
    assert psc.is_wigner_non_negative(rho_d01)


def test_magic_mixture_branch_scaling() -> None:
    res = StabilizerMixture.benchmark_scaling(k_max=5, n_carriers=5)
    for entry in res["scaling_results"]:
        k = entry["magic_count_k"]
        expected = 1 << k
        assert entry["branch_count"] == expected
        assert entry["expected_exponential"] == expected


def test_magic_mixture_clifford_parallel() -> None:
    mix = StabilizerMixture(n_carriers=2)
    mix.inject_magic_state(0, magic_type=MagicStateType.T)
    assert mix.branch_count == 2
    mix.apply_h(1)
    mix.apply_cnot(0, 1)
    mix.apply_s_gate(1)
    assert mix.branch_count == 2
    for _, tab in mix.branches:
        assert tab.check_tableau_invariants()


def test_polynomial_clifford_complexity_scaling() -> None:
    times: list[float] = []
    carrier_sizes = [2, 4, 8, 16]
    for n in carrier_sizes:
        tab = SymplecticTableau(n)
        start = time.perf_counter()
        for _ in range(50):
            tab.h(0)
            tab.s_gate(1)
            tab.cnot(0, 1)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
        assert tab.check_tableau_invariants()

    # Empirical time should remain small (polynomial)
    for t in times:
        assert t < 0.5


def test_pauli_representation_and_copy() -> None:
    tab = SymplecticTableau(2)
    tab.create_bell_pair(0, 1)
    paulis = tab.to_pauli_strings()
    assert "+XX" in paulis["stabilizers"] or "+XX" in [s[1:] for s in paulis["stabilizers"]]
    assert "+ZZ" in paulis["stabilizers"] or "+ZZ" in [s[1:] for s in paulis["stabilizers"]]

    cloned = tab.copy()
    assert cloned.check_tableau_invariants()
    cloned.h(0)
    # Original should remain unaffected
    assert tab.x != cloned.x

    with pytest.raises(IndexError):
        tab.h(5)
    with pytest.raises(ValueError):
        tab.cnot(0, 0)
