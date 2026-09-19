"""Four-pillar integration checks for Cohort 6."""
from __future__ import annotations

from fractions import Fraction
import math
from pathlib import Path
import random
import subprocess
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TARGET_DIRS = [
    REPO_ROOT / "research" / "p203_composite_systems",
    REPO_ROOT / "research" / "m108_internal_algebra",
    REPO_ROOT / "research" / "m109_obstruction_homology",
    REPO_ROOT / "research" / "x300_observer_information",
]
for p in reversed(TARGET_DIRS):
    p_str = str(p)
    if p_str in sys.path:
        sys.path.remove(p_str)
    sys.path.insert(0, p_str)

import composite_systems as p203
import algebra as m108
import homology as m109
import information as x300

def test_four_pillar_cross_integration() -> int:
    """End-to-end integration connecting:

    P203 multi-locus carrier networks
    -> M108 algebraic observables
    -> M109 boundary/cohomology circulation
    -> X300 channel transmission & Data Processing Inequality.
    """
    print(">>> Executing Multi-Target 4-Pillar Cross-Integration Pipeline...")
    checks = 0
    rng = random.Random(4444)

    for trial in range(15):
        # ----------------------------------------------------------------------
        # PILLAR 1: P203 Composite Carrier Network & Bipartite Cut
        # ----------------------------------------------------------------------
        loci_a = ["loc_0", "loc_1"]
        loci_b = ["loc_2", "loc_3"]
        cut = p203.BipartiteCut(part_a=frozenset(loci_a), part_b=frozenset(loci_b))

        # 64-state ensemble over {0, 1}^4
        raw_states = []
        for v0 in (0, 1):
            for v1 in (0, 1):
                for v2 in (0, 1):
                    for v3 in (0, 1):
                        raw_states.append(
                            p203.CarrierState({"loc_0": v0, "loc_1": v1, "loc_2": v2, "loc_3": v3})
                        )
        # Duplicate to form 128 states
        ensemble = raw_states * 2

        # Verify operational non-signaling: local A-transition does not affect B
        op_a = p203.Transition(
            name="flip_a0",
            reads=frozenset(["loc_0"]),
            writes=frozenset(["loc_0"]),
            transform=lambda s: {"loc_0": 1 - s["loc_0"]},
        )
        obs_b = p203.Observable(
            name="sum_b",
            footprint=frozenset(loci_b),
            measure=lambda s: s["loc_2"] + s["loc_3"],
        )
        ns_rep = p203.verify_operational_non_signaling(ensemble, cut, [op_a], obs_b)
        assert ns_rep["non_signaling_satisfied"] is True
        assert ns_rep["max_tvd"] == Fraction(0, 1)
        checks += 2

        # ----------------------------------------------------------------------
        # PILLAR 2: M108 Algebraic Observables via Free Module over Q
        # ----------------------------------------------------------------------
        fmod = m108.FreeModule(set(loci_a + loci_b), scalar_type=m108.InternalRat)

        # Construct linear algebraic observable on Part A: Phi_A = 1*loc_0 + 2*loc_1
        phi_a = fmod.eta("loc_0").smul(m108.InternalRat(1, 1)) + fmod.eta("loc_1").smul(m108.InternalRat(2, 1))

        # Evaluate Phi_A across the ensemble
        measured_values: List[int] = []
        for s in ensemble:
            # Map carrier locus values into InternalRat
            eval_map = {locus: m108.InternalRat(s[locus], 1) for locus in fmod.generators}
            # Evaluate linear combination
            res_val = m108.InternalRat.zero()
            for k, c in phi_a.terms:
                res_val = res_val + c * eval_map[k]
            # Valuation in {0, 1, 2, 3}
            measured_values.append(res_val.num)

        # Confirm exact 4-level valuation
        assert set(measured_values) == {0, 1, 2, 3}
        checks += 1

        # Form a quotient congruence mod 4 over (Z, +)
        base_z = m108.Algebra(
            name="Z",
            signature=m108.MONOID_SIGNATURE,
            interpretations={"e": lambda: m108.InternalInt(0), "mul": lambda a, b: a + b},
        )
        cong_mod4 = m108.CongruenceRelation(
            base_z, lambda a, b: (a.val - b.val) % 4 == 0, name="mod4"
        )
        q_mod4 = m108.QuotientAlgebra(
            base_z,
            cong_mod4,
            canonicalizer=lambda x: m108.InternalInt(x.val % 4),
            name="Z_4",
        )
        test_pairs_4 = [
            (
                (m108.InternalInt(1), m108.InternalInt(2)),
                (m108.InternalInt(5), m108.InternalInt(6)),
            ),
            (
                (m108.InternalInt(0), m108.InternalInt(3)),
                (m108.InternalInt(4), m108.InternalInt(7)),
            ),
        ]
        assert q_mod4.check_representative_independence("mul", test_pairs_4) is True
        checks += 1

        # ----------------------------------------------------------------------
        # PILLAR 3: M109 Boundary/Cohomology Circulation on Cycle Complex
        # ----------------------------------------------------------------------
        # The 4 measurement values {0, 1, 2, 3} form vertices of a 4-cycle complex
        c4 = m109.build_cycle_complex(4)

        # Construct a 1-chain corresponding to a complete cycle traversal
        chain_cycle = [Fraction(1, 1) for _ in range(4)]
        bnd = m109.matrix_vector_mul(c4.boundary(1), chain_cycle)
        # Boundary of a 1-cycle is 0 in C_0
        assert all(val == Fraction(0, 1) for val in bnd)
        checks += 1

        # Dual 1-cochain measuring circulation around the state cycle
        cochain_w = [Fraction(1, 1) for _ in range(4)]
        obstr_rep = m109.analyze_obstruction(c4, grade=1, cochain=cochain_w)
        assert obstr_rep.is_cocycle is True
        assert obstr_rep.is_coboundary is False
        assert obstr_rep.is_obstruction_class is True
        assert obstr_rep.circulation == Fraction(4, 1)
        checks += 4

        # Stokes duality on the complex
        dc4 = c4.dual_cochain_complex()
        assert dc4.verify_stokes_theorem(0, [Fraction(1, 1) for _ in range(4)], chain_cycle) is True
        checks += 1

        # ----------------------------------------------------------------------
        # PILLAR 4: X300 Channel Transmission, Data Processing Inequality & Landauer
        # ----------------------------------------------------------------------
        # Empirical distribution of measured algebraic observable X in {0, 1, 2, 3}
        p_x = x300.DiscreteDistribution.uniform([0, 1, 2, 3])
        assert p_x.exact_hartley_capacity() == 2
        assert p_x.exact_dyadic_shannon_entropy() == Fraction(2, 1)
        checks += 2

        # Operational channel cascade: X -> Y (noisy channel) -> Z (coarse graining)
        w_xy = x300.Channel({
            0: x300.DiscreteDistribution({0: Fraction(4, 5), 1: Fraction(1, 5)}),
            1: x300.DiscreteDistribution({1: Fraction(4, 5), 2: Fraction(1, 5)}),
            2: x300.DiscreteDistribution({2: Fraction(4, 5), 3: Fraction(1, 5)}),
            3: x300.DiscreteDistribution({3: Fraction(4, 5), 0: Fraction(1, 5)}),
        })
        # Coarse graining: parity Z = Y % 2
        w_yz = x300.Channel.coarse_graining(lambda y: y % 2, [0, 1, 2, 3])

        cert = x300.verify_data_processing_inequality(p_x, w_xy, w_yz)
        assert cert.passed is True
        assert cert.delta_i >= -1e-12
        assert cert.i_xy >= cert.i_xz
        checks += 3

        # Landauer operational erasure on observer register
        acct = x300.LandauerAccounting(p_x, reset_state=0, temperature_kelvin=300.0)
        receipt = acct.compute_erasure_cost()
        assert receipt.initial_entropy_bits == 2.0
        assert receipt.final_entropy_bits == 0.0
        assert receipt.exact_erased_entropy_q == Fraction(2, 1)
        assert receipt.operational_non_reversibility is True
        checks += 4

    print(f"  4-Pillar Cross-Integration passed {checks} checks.")
    return checks


# ==============================================================================
# 6. Repository Seal and Axiom Audit
# ==============================================================================

