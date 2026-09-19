"""Master Empirical Adversarial Stress Suite for Genesis Cohort 7.

Lead Architect & Adversarial Critic Review Gate.
Targets:
- P204: Operational Valuations & Convex State Spaces
- P208a: path_interference & Vanishing Sorkin I_3
- P208b: Nonlocality & Contextuality Obstructions
- P208c: Commutator Obstruction & Discrete MUB State Tomography

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

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Prepend research directories for Cohort 7
TARGET_DIRS = [
    REPO_ROOT / "research" / "p204_operational_valuations",
    REPO_ROOT / "research" / "p208a_path_interference",
    REPO_ROOT / "research" / "p208b_contextuality_nonlocality",
    REPO_ROOT / "research" / "p208c_commutator_tomography",
]
for p in reversed(TARGET_DIRS):
    p_str = str(p)
    if p_str in sys.path:
        sys.path.remove(p_str)
    sys.path.insert(0, p_str)

import valuations as p204
import path_interference as p208a
import correlations as p208b
import tomography as p208c


# ==============================================================================
# 1. Target P204: Operational Valuations & Convex State Spaces Fuzzing
# ==============================================================================

def test_p204_adversarial_operational_valuations() -> int:
    """Fuzz P204 operational states, effects, valuations, simplices, and non-signaling."""
    print(">>> Fuzzing Target P204: Operational Valuations & Convex State Spaces...")
    checks = 0
    rng = random.Random(204204)

    # 1. Outcome space structural invariants and boundary rejections
    for n_outcomes in range(2, 11):
        labels = tuple(f"w_{i}" for i in range(n_outcomes))
        space = p204.OutcomeSpace(labels)
        assert space.dim == n_outcomes
        assert len(space) == n_outcomes
        assert space.outcomes == labels
        for idx, lbl in enumerate(labels):
            assert space.index(lbl) == idx
            assert space.contains(lbl) is True
        assert space.contains("non_existent_label") is False
        checks += 5

        # Rejection: empty outcome space
        try:
            p204.OutcomeSpace(())
            raise AssertionError("Expected ValueError on empty outcome space")
        except ValueError:
            checks += 1

        # Rejection: duplicate outcome labels
        try:
            p204.OutcomeSpace(("dup", "dup", f"unique_{n_outcomes}"))
            raise AssertionError("Expected ValueError on duplicate outcome labels")
        except ValueError:
            checks += 1

    # 2. Operational state normalization and probability bounds fuzzing
    for trial in range(35):
        dim = rng.randint(2, 7)
        space = p204.OutcomeSpace(tuple(f"out_{k}" for k in range(dim)))
        raw_weights = [rng.randint(1, 50) for _ in range(dim)]
        total_w = sum(raw_weights)
        dist = {f"out_{k}": Fraction(w, total_w) for k, w in enumerate(raw_weights)}

        state = p204.OperationalState(space, dist)
        assert len(state.vector) == dim
        total_p = sum(state.probability(out) for out in space.outcomes)
        assert total_p == Fraction(1, 1)
        for out in space.outcomes:
            p_val = state.probability(out)
            assert Fraction(0, 1) <= p_val <= Fraction(1, 1)
        checks += 4

        # Boundary rejection: negative probability
        bad_dist = dict(dist)
        bad_dist[space.outcomes[0]] = Fraction(-1, 10)
        bad_dist[space.outcomes[1]] = bad_dist[space.outcomes[1]] + Fraction(1, 10)
        try:
            p204.OperationalState(space, bad_dist)
            raise AssertionError("Expected ValueError on negative probability")
        except ValueError:
            checks += 1

        # Boundary rejection: unnormalized sum != 1
        bad_sum_dist = {f"out_{k}": Fraction(1, dim + 1) for k in range(dim)}
        try:
            p204.OperationalState(space, bad_sum_dist)
            raise AssertionError("Expected ValueError on unnormalized distribution")
        except ValueError:
            checks += 1

    # 3. Operational effects, unit effect, zero effect, and complement pairing
    for trial in range(35):
        dim = rng.randint(2, 6)
        space = p204.OutcomeSpace(tuple(f"e_out_{k}" for k in range(dim)))
        effect_weights = {
            f"e_out_{k}": Fraction(rng.randint(0, 20), 20) for k in range(dim)
        }
        eff = p204.OperationalEffect(space, effect_weights)
        u_eff = p204.OperationalEffect.unit_effect(space)
        z_eff = p204.OperationalEffect.zero_effect(space)
        comp_eff = eff.complement()

        # Random normalized test state
        raw_w = [rng.randint(1, 30) for _ in range(dim)]
        tot = sum(raw_w)
        s_dist = {f"e_out_{k}": Fraction(w, tot) for k, w in enumerate(raw_w)}
        state = p204.OperationalState(space, s_dist)

        # Invariant 1: unit effect evaluates to exactly 1 on any operational state
        assert p204.evaluate(u_eff, state) == Fraction(1, 1)
        # Invariant 2: zero effect evaluates to exactly 0
        assert p204.evaluate(z_eff, state) == Fraction(0, 1)
        # Invariant 3: complement pairing <u - e, s> = 1 - <e, s>
        val_eff = p204.evaluate(eff, state)
        val_comp = p204.evaluate(comp_eff, state)
        assert val_eff + val_comp == Fraction(1, 1)
        assert Fraction(0, 1) <= val_eff <= Fraction(1, 1)
        checks += 4

    # 4. Convex mixtures and operational bilinearity sweeps
    for trial in range(35):
        dim = rng.randint(2, 5)
        space = p204.OutcomeSpace(tuple(f"b_out_{k}" for k in range(dim)))
        n_states = rng.randint(2, 5)
        n_effects = rng.randint(2, 5)

        # Generate states
        states: List[p204.OperationalState] = []
        for _ in range(n_states):
            rw = [rng.randint(1, 20) for _ in range(dim)]
            tot = sum(rw)
            st = p204.OperationalState(
                space, {f"b_out_{k}": Fraction(w, tot) for k, w in enumerate(rw)}
            )
            states.append(st)

        # Generate state weights
        sw = [rng.randint(1, 15) for _ in range(n_states)]
        tot_sw = sum(sw)
        state_weights = [Fraction(w, tot_sw) for w in sw]

        # Generate effects
        effects: List[p204.OperationalEffect] = []
        for _ in range(n_effects):
            ew = {f"b_out_{k}": Fraction(rng.randint(0, 10), 10) for k in range(dim)}
            effects.append(p204.OperationalEffect(space, ew))

        # Generate effect weights
        ew_weights = [rng.randint(1, 15) for _ in range(n_effects)]
        tot_ew = sum(ew_weights)
        effect_weights = [Fraction(w, tot_ew) for w in ew_weights]

        bilinear_ok = p204.verify_bilinearity(state_weights, states, effect_weights, effects)
        assert bilinear_ok is True
        checks += 2

    # 5. Classical simplex uniqueness vs square state space non-uniqueness
    for trial in range(25):
        dim = rng.randint(2, 6)
        space = p204.OutcomeSpace(tuple(f"s_out_{k}" for k in range(dim)))
        simplex = p204.ClassicalSimplex(space)
        assert len(simplex.extreme_states) == dim

        raw_w = [rng.randint(1, 30) for _ in range(dim)]
        tot = sum(raw_w)
        s_dist = {f"s_out_{k}": Fraction(w, tot) for k, w in enumerate(raw_w)}
        state = p204.OperationalState(space, s_dist)

        # Decompose in classical simplex: must equal the probability coordinates
        decomp = simplex.decompose(state)
        assert len(decomp) == dim
        canonical_weights = [s_dist[out] for out in space.outcomes]
        assert simplex.is_unique_decomposition(state, canonical_weights) is True

        # Defective candidate weights must be rejected
        defective_weights = list(canonical_weights)
        if dim >= 2:
            defective_weights[0] = defective_weights[0] + Fraction(1, 100)
            defective_weights[1] = defective_weights[1] - Fraction(1, 100)
            assert simplex.is_unique_decomposition(state, defective_weights) is False
        checks += 4

    # Square state space non-unique extreme decompositions
    sq_space = p204.SquareStateSpace()
    assert len(sq_space.extreme_states) == 4
    w1, s1 = sq_space.decomposition_diagonal_1()
    w2, s2 = sq_space.decomposition_diagonal_2()
    assert w1 != w2
    assert s1 == s2 == sq_space.center_state
    assert sq_space.demonstrates_non_unique_decomposition() is True
    checks += 4

    # 6. Tensor product composition & Bipartite operational non-signaling sweeps
    for cut_trial in range(30):
        da = rng.randint(2, 4)
        db = rng.randint(2, 4)
        space_a = p204.OutcomeSpace(tuple(f"A_{i}" for i in range(da)))
        space_b = p204.OutcomeSpace(tuple(f"B_{j}" for j in range(db)))
        comp_space = p204.tensor_outcome_space(space_a, space_b)
        assert comp_space.dim == da * db

        # Generate correlated bipartite operational state
        raw_joint = [rng.randint(1, 40) for _ in range(da * db)]
        tot_j = sum(raw_joint)
        joint_dist: Dict[Tuple[Any, Any], Fraction] = {}
        idx = 0
        for a in space_a.outcomes:
            for b in space_b.outcomes:
                joint_dist[(a, b)] = Fraction(raw_joint[idx], tot_j)
                idx += 1
        state_ab = p204.OperationalState(comp_space, joint_dist)

        # Construct random partition of unity on subsystem A: sum_i e_{A, i} = u_A
        m_partitions = rng.randint(2, 4)
        partition_weights: List[Dict[Any, Fraction]] = [
            {a: Fraction(0, 1) for a in space_a.outcomes} for _ in range(m_partitions)
        ]
        for a in space_a.outcomes:
            cuts = sorted([0] + [rng.randint(1, 99) for _ in range(m_partitions - 1)] + [100])
            for p_idx in range(m_partitions):
                share = Fraction(cuts[p_idx + 1] - cuts[p_idx], 100)
                partition_weights[p_idx][a] = share

        meas_effects_a = [
            p204.OperationalEffect(space_a, pw) for pw in partition_weights
        ]

        # Test arbitrary response effect on subsystem B
        b_weights = {b: Fraction(rng.randint(0, 10), 10) for b in space_b.outcomes}
        test_effect_b = p204.OperationalEffect(space_b, b_weights)

        ns_receipt = p204.verify_non_signaling_across_cut(
            state_ab, space_a, space_b, meas_effects_a, test_effect_b
        )
        assert ns_receipt["non_signaling"] is True
        assert ns_receipt["summed_eval"] == ns_receipt["unit_eval"] == ns_receipt["marginal_eval"]

        # TVD between marginal distribution on B and operational readout
        s_b = p204.marginal_state_b(state_ab, space_a, space_b)
        assert s_b.space == space_b
        tvd_val = abs(ns_receipt["summed_eval"] - ns_receipt["marginal_eval"])
        assert tvd_val == Fraction(0, 1)
        checks += 5

    print(f"  Target P204 passed {checks} checks.")
    return checks


# ==============================================================================
# 2. Target P208a: path_interference & Vanishing Sorkin I_3 Fuzzing
# ==============================================================================

def test_p208a_adversarial_path_interference() -> int:
    """Fuzz P208a Gaussian rational path_amplitudes, I_2 != 0, and vanishing Sorkin I_3."""
    print(">>> Fuzzing Target P208a: path_interference & Vanishing Sorkin I_3...")
    checks = 0
    rng = random.Random(208208)

    # 1. Exact Gaussian rational arithmetic and Pythagorean unit rotations
    for _ in range(50):
        m = rng.randint(-25, 25)
        n = rng.randint(-25, 25)
        if m == 0 and n == 0:
            m = 1
        u = p208a.GaussianRational.unit_pythagorean(m, n)
        assert u.norm_sq() == Fraction(1, 1)
        assert u.valuation() == Fraction(1, 1)
        conj_u = u.conjugate()
        prod = u * conj_u
        assert prod.re == Fraction(1, 1)
        assert prod.im == Fraction(0, 1)
        checks += 4

    # 2. Constructive second-order path_interference witnesses (I_2 != 0)
    # Aligned: I_2 = 2
    d_aligned = p208a.Diamond2Complex(
        ["A", "B"],
        {"A": p208a.GaussianRational.one(), "B": p208a.GaussianRational.one()},
    )
    assert d_aligned.second_order_interference("A", "B") == Fraction(2, 1)
    # Destructive: I_2 = -2
    d_destr = p208a.Diamond2Complex(
        ["A", "B"],
        {"A": p208a.GaussianRational.one(), "B": -p208a.GaussianRational.one()},
    )
    assert d_destr.second_order_interference("A", "B") == Fraction(-2, 1)
    # Orthogonal delay: I_2 = 0
    d_orth = p208a.Diamond2Complex(
        ["A", "B"],
        {"A": p208a.GaussianRational.one(), "B": p208a.GaussianRational.i()},
    )
    assert d_orth.second_order_interference("A", "B") == Fraction(0, 1)
    # Pythagorean shift: a_A = 1, a_B = 3/5 + 4/5 i => I_2 = 6/5 != 0
    d_pyth = p208a.Diamond2Complex(
        ["A", "B"],
        {
            "A": p208a.GaussianRational.one(),
            "B": p208a.GaussianRational(Fraction(3, 5), Fraction(4, 5)),
        },
    )
    i2_pyth = d_pyth.second_order_interference("A", "B")
    assert i2_pyth == Fraction(6, 5)
    assert i2_pyth != Fraction(0, 1)
    checks += 6

    # 3. Second-order path_interference under random shifts: I_2(A, B) = 2 * Re(a_A * a_B^*)
    for _ in range(50):
        re_a = Fraction(rng.randint(-20, 20), rng.randint(1, 10))
        im_a = Fraction(rng.randint(-20, 20), rng.randint(1, 10))
        re_b = Fraction(rng.randint(-20, 20), rng.randint(1, 10))
        im_b = Fraction(rng.randint(-20, 20), rng.randint(1, 10))
        amp_a = p208a.GaussianRational(re_a, im_a)
        amp_b = p208a.GaussianRational(re_b, im_b)

        diamond = p208a.Diamond2Complex(["A", "B"], {"A": amp_a, "B": amp_b})
        i2_val = diamond.second_order_interference("A", "B")
        expected = Fraction(2, 1) * (re_a * re_b + im_a * im_b)
        assert i2_val == expected
        checks += 2

    # 4. Exhaustive Vanishing Sorkin I_3 = 0 sweeps over random 3-path configurations
    for trial in range(150):
        amp_dict: Dict[str, p208a.GaussianRational] = {}
        for p in ["A", "B", "C"]:
            re_p = Fraction(rng.randint(-30, 30), rng.randint(1, 15))
            im_p = Fraction(rng.randint(-30, 30), rng.randint(1, 15))
            amp_dict[p] = p208a.GaussianRational(re_p, im_p)

        diamond3 = p208a.Diamond2Complex(["A", "B", "C"], amp_dict)
        i3_val = diamond3.third_order_sorkin("A", "B", "C")
        assert i3_val == Fraction(0, 1)
        assert diamond3.is_sorkin_zero(["A", "B", "C"]) is True
        checks += 2

    # 5. Invariance across cyclotomic field orders n in {3, 4, 6, 8, 12}
    for cyc_n in [3, 4, 6, 8, 12]:
        for _ in range(15):
            deg = len(p208a.CyclotomicRational._PHI[cyc_n]) - 1
            amp_c: Dict[str, p208a.CyclotomicRational] = {}
            for p in ["A", "B", "C"]:
                coeffs = [Fraction(rng.randint(-10, 10), rng.randint(1, 5)) for _ in range(deg)]
                amp_c[p] = p208a.CyclotomicRational(cyc_n, coeffs)

            d_cyc = p208a.Diamond2Complex(["A", "B", "C"], amp_c)
            i3_cyc = d_cyc.third_order_sorkin("A", "B", "C")
            assert isinstance(i3_cyc, p208a.CyclotomicRational)
            assert i3_cyc.is_zero() is True
            assert d_cyc.is_sorkin_zero(["A", "B", "C"]) is True
            checks += 3

    # 6. Higher-order path_interference vanishing I_k = 0 for k in {4, 5, 6}
    for k in [4, 5, 6]:
        for _ in range(20):
            names = [f"P_{idx}" for idx in range(k)]
            amp_k: Dict[str, p208a.GaussianRational] = {}
            for name in names:
                re_k = Fraction(rng.randint(-15, 15), rng.randint(1, 10))
                im_k = Fraction(rng.randint(-15, 15), rng.randint(1, 10))
                amp_k[name] = p208a.GaussianRational(re_k, im_k)

            diamond_k = p208a.Diamond2Complex(names, amp_k)
            ik_val = diamond_k.higher_order_sorkin(names)
            assert ik_val == Fraction(0, 1)
            assert diamond_k.is_sorkin_zero(names) is True

            # Discrete difference equality
            diff_val = p208a.higher_order_discrete_difference(diamond_k, names)
            assert diff_val == Fraction(0, 1)
            checks += 3

    print(f"  Target P208a passed {checks} checks.")
    return checks


# ==============================================================================
# 3. Target P208b: Contextuality & Nonlocality Obstructions Fuzzing
# ==============================================================================

def test_p208b_adversarial_contextuality_nonlocality() -> int:
    """Fuzz P208b Bell-CHSH LHV bounds, Pythagorean S=2.8 nonlocality, and Cabello 18-ray parity."""
    print(">>> Fuzzing Target P208b: Contextuality & Nonlocality Obstructions...")
    checks = 0
    rng = random.Random(208209)

    # 1. Exhaustive deterministic LHV strategies and |S| <= 2 verification
    strategies = p208b.generate_all_deterministic_strategies()
    assert len(strategies) == 16
    census = p208b.verify_deterministic_lhv_bounds()
    assert census["plus_2"] == 8
    assert census["minus_2"] == 8
    assert census["other"] == 0
    for strat in strategies:
        s_val = strat.correlator()
        assert abs(s_val) <= 2
        assert s_val in (2, -2)
        checks += 2

    # 2. Random convex combinations of LHV strategies: always |S| <= 2
    for _ in range(50):
        k_strats = rng.randint(2, 16)
        chosen = rng.sample(strategies, k_strats)
        raw_weights = [rng.randint(1, 50) for _ in range(k_strats)]
        tot_w = sum(raw_weights)
        frac_weights = tuple(Fraction(w, tot_w) for w in raw_weights)

        model = p208b.ConvexLHVModel(tuple(chosen), frac_weights)
        s_convex = model.chsh_correlator()
        assert abs(s_convex) <= Fraction(2, 1)
        checks += 2

    # 3. Rational Pythagorean non-local correlator S = 14/5 = 2.8 > 2
    table, s_pyth = p208b.pythagorean_model()
    assert s_pyth == Fraction(14, 5)
    assert s_pyth > Fraction(2, 1)
    assert table.is_valid_distribution() is True
    assert table.is_no_signaling() is True
    checks += 4

    # Verify individual expectation values match exact dot products
    assert table.expectation(0, 0) == Fraction(4, 5)
    assert table.expectation(0, 1) == Fraction(4, 5)
    assert table.expectation(1, 0) == Fraction(3, 5)
    assert table.expectation(1, 1) == Fraction(-3, 5)
    checks += 4

    # PR-box maximal non-signaling box: S = 4
    pr_table, s_pr = p208b.pr_box_model()
    assert s_pr == Fraction(4, 1)
    assert pr_table.is_valid_distribution() is True
    assert pr_table.is_no_signaling() is True
    checks += 3

    # 4. Cabello 18-ray configuration in Q^4: geometry and 2-incidence regularity
    assert len(p208b.CABELLO_RAYS) == 18
    assert len(p208b.CABELLO_CONTEXTS) == 9

    # Verify all coordinates lie in {-1, 0, 1}
    for r in p208b.CABELLO_RAYS:
        for c in r:
            assert c in (-1, 0, 1)
        checks += 1

    # Verify mutual orthogonality in every context (9 contexts * 6 pairs = 54 checks)
    assert p208b.verify_cabello_orthogonality() is True
    for ctx in p208b.CABELLO_CONTEXTS:
        for i in range(4):
            for j in range(i + 1, 4):
                dp = p208b.dot_product_4d(p208b.CABELLO_RAYS[ctx[i]], p208b.CABELLO_RAYS[ctx[j]])
                assert dp == 0
                checks += 1

    # Verify exact degree-2 incidence regularity: every ray belongs to exactly 2 contexts
    inc_counts = p208b.verify_cabello_incidence()
    assert len(inc_counts) == 18
    for ray_idx, deg in inc_counts.items():
        assert deg == 2
        checks += 1

    # Verify 9x18 incidence matrix properties
    inc_matrix = p208b.build_cabello_incidence_matrix()
    assert len(inc_matrix) == 9
    for row in inc_matrix:
        assert sum(row) == 4  # 4 rays per context
        checks += 1
    for col_idx in range(18):
        assert sum(inc_matrix[row_idx][col_idx] for row_idx in range(9)) == 2  # degree 2
        checks += 1

    # 5. Non-contextual valuation parity obstruction and Cech 1-cochain obstruction
    obstruction_report = p208b.evaluate_noncontextual_valuation_obstruction()
    assert obstruction_report["num_contexts"] == 9
    assert obstruction_report["num_rays"] == 18
    assert obstruction_report["each_ray_degree"] == 2
    assert obstruction_report["exhaustive_valid_valuations"] == 0
    checks += 4

    cech_report = p208b.cech_cochain_parity_obstruction()
    assert cech_report["context_cycle_mod2"] == 1
    assert cech_report["incidence_degree_mod2"] == 0
    assert cech_report["coboundary_obstruction_mod2"] == 1
    checks += 3

    # Sampled randomized valuation attempts: none must satisfy all 9 contexts
    for _ in range(500):
        rand_val = tuple(rng.choice((0, 1)) for _ in range(18))
        context_sums = [sum(rand_val[r] for r in ctx) for ctx in p208b.CABELLO_CONTEXTS]
        assert not all(s == 1 for s in context_sums)
        checks += 1

    print(f"  Target P208b passed {checks} checks.")
    return checks


# ==============================================================================
# 4. Target P208c: Commutator Obstruction & Discrete MUB Tomography Fuzzing
# ==============================================================================

def test_p208c_adversarial_commutator_tomography() -> int:
    """Fuzz P208c commutator trace obstruction, microcausality, MUBs, and state tomography."""
    print(">>> Fuzzing Target P208c: Commutator Obstruction & Discrete MUB Tomography...")
    checks = 0
    rng = random.Random(208210)

    # 1. Finite-dimensional commutator trace obstruction: Tr([A, B]) = 0
    for dim in range(2, 7):
        for _ in range(15):
            A = [
                [Fraction(rng.randint(-20, 20), rng.randint(1, 10)) for _ in range(dim)]
                for _ in range(dim)
            ]
            B = [
                [Fraction(rng.randint(-20, 20), rng.randint(1, 10)) for _ in range(dim)]
                for _ in range(dim)
            ]
            tr_comm = p208c.commutator_trace(A, B)
            assert tr_comm == Fraction(0, 1)

            # Canonical commutation obstruction gap: Tr([Q, P] - c * I) = -N * c != 0
            c_val = Fraction(rng.randint(1, 20), rng.randint(1, 5))
            gap = p208c.commutator_obstruction_gap(A, B, c_val)
            expected_gap = -Fraction(dim, 1) * c_val
            assert gap == expected_gap
            assert gap != Fraction(0, 1)
            assert p208c.verify_canonical_commutation_obstruction(dim, c_val) is True
            checks += 4

    # 2. Multi-locus microcausality on composite bipartite carriers
    for dim_a in [2, 3]:
        for dim_b in [2, 3]:
            for _ in range(10):
                A = [
                    [Fraction(rng.randint(-15, 15), rng.randint(1, 8)) for _ in range(dim_a)]
                    for _ in range(dim_a)
                ]
                B = [
                    [Fraction(rng.randint(-15, 15), rng.randint(1, 8)) for _ in range(dim_b)]
                    for _ in range(dim_b)
                ]
                comm_ok = p208c.verify_microcausality_bipartite(A, B)
                assert comm_ok is True
                checks += 1

    # Conjugate observables on same locus do NOT commute: [X, Z] != 0
    X3 = p208c.discrete_shift_operator(3, p208c.Cyclotomic3(0), p208c.Cyclotomic3(1))
    Z3 = p208c.discrete_clock_operator_dim3()
    comm_XZ3 = p208c.matrix_commutator(X3, Z3)
    assert any(comm_XZ3[i][j] != p208c.Cyclotomic3(0) for i in range(3) for j in range(3))
    checks += 1

    # 3. Discrete MUBs in dimension d = 3: orthonormality and mutual unbiasedness
    mubs3 = p208c.construct_mubs_dim3()
    assert len(mubs3) == 4  # d + 1 = 4 bases
    # Basis 0 (standard computational basis): norm squared is 1
    for i in range(3):
        for j in range(3):
            dot_val = p208c.vector_dot(mubs3[0][i], mubs3[0][j])
            if i == j:
                assert dot_val == p208c.Cyclotomic3(1)
                assert dot_val.norm_sq() == Fraction(1, 1)
            else:
                assert dot_val == p208c.Cyclotomic3(0)
            checks += 1

    # Bases 1, 2, 3 (Fourier bases): unscaled vectors have norm squared 3
    for r in range(1, 4):
        for i in range(3):
            for j in range(3):
                dot_val = p208c.vector_dot(mubs3[r][i], mubs3[r][j])
                if i == j:
                    assert dot_val == p208c.Cyclotomic3(3)
                    assert dot_val.norm_sq() == Fraction(9, 1)
                else:
                    assert dot_val == p208c.Cyclotomic3(0)
                checks += 1

    # Pairwise mutual unbiasedness across all bases in d = 3: |<u | v>|^2 = 1/3
    # Standard vs Fourier: dot has |val|^2 = 1 (1 / 3 physical)
    for r in range(1, 4):
        for j in range(3):
            for k in range(3):
                dot_val = p208c.vector_dot(mubs3[0][j], mubs3[r][k])
                assert dot_val.norm_sq() == Fraction(1, 1)
                checks += 1

    # Fourier vs Fourier: dot has |val|^2 = 3 (3 / 9 = 1/3 physical)
    for r1 in range(1, 4):
        for r2 in range(r1 + 1, 4):
            for j in range(3):
                for k in range(3):
                    dot_val = p208c.vector_dot(mubs3[r1][j], mubs3[r2][k])
                    assert dot_val.norm_sq() == Fraction(3, 1)
                    checks += 1

    # Projector resolution of identity for d = 3
    projs3 = p208c.construct_mub_projectors_dim3()
    I3 = p208c.identity_matrix(3, p208c.Cyclotomic3(0), p208c.Cyclotomic3(1))
    for b_idx, b_projs in enumerate(projs3):
        s = p208c.zero_matrix(3, 3, p208c.Cyclotomic3(0))
        for P in b_projs:
            s = p208c.matrix_add(s, P)
        assert s == I3
        checks += 1

    # 4. Discrete MUBs in dimension d = 4: orthonormality and mutual unbiasedness
    mubs4 = p208c.construct_mubs_dim4()
    assert len(mubs4) == 5  # d + 1 = 5 bases
    for b in mubs4:
        assert len(b) == 4
        # Orthonormality within basis
        for i in range(4):
            for j in range(4):
                dot_val = p208c.vector_dot(b[i], b[j])
                if i == j:
                    assert dot_val.norm_sq() == Fraction(16, 1)  # Unnormalized length 2
                else:
                    assert dot_val == p208c.GaussianRational(0, 0)
                checks += 1

    # Pairwise mutual unbiasedness: |<u | v>|^2 / (4 * 4) = 1/4
    overlap_ok4 = p208c.verify_mub_pairwise_overlap(mubs4, 4, Fraction(16, 1))
    assert overlap_ok4 is True
    checks += 2

    # Projector resolution of identity for d = 4
    projs4 = p208c.construct_mub_projectors_dim4()
    I4 = p208c.identity_matrix(4, p208c.GaussianRational(0, 0), p208c.GaussianRational(1, 0))
    for b_idx, b_projs in enumerate(projs4):
        s = p208c.zero_matrix(4, 4, p208c.GaussianRational(0, 0))
        for P in b_projs:
            s = p208c.matrix_add(s, P)
        assert s == I4
        checks += 1

    # 5. Complete operational state tomography reconstruction in d = 3
    projs3 = p208c.construct_mub_projectors_dim3()
    for _ in range(20):
        # Create random density operator in d = 3: rho = sum p_i |v_i><v_i|
        w_raw = [rng.randint(1, 20) for _ in range(3)]
        w_tot = sum(w_raw)
        p_weights = [Fraction(w, w_tot) for w in w_raw]

        rho = p208c.zero_matrix(3, 3, p208c.Cyclotomic3(0))
        for k in range(3):
            # Pure projector from Basis 1
            P_k = projs3[1][k]
            scaled = p208c.matrix_scale(p208c.Cyclotomic3(p_weights[k]), P_k)
            rho = p208c.matrix_add(rho, scaled)

        # Operational measurement along all 4 MUBs
        probs = p208c.measure_mub_probabilities(rho, projs3)
        assert len(probs) == 4

        # Dual frame Wootters inversion
        rho_rec = p208c.reconstruct_state_from_probabilities(
            probs, projs3, 3, p208c.Cyclotomic3(0), p208c.Cyclotomic3(1)
        )
        for i in range(3):
            for j in range(3):
                assert rho_rec[i][j] == rho[i][j]
        checks += 3

    # 6. Complete operational state tomography reconstruction in d = 4
    projs4 = p208c.construct_mub_projectors_dim4()
    for _ in range(20):
        w_raw = [rng.randint(1, 20) for _ in range(4)]
        w_tot = sum(w_raw)
        p_weights = [Fraction(w, w_tot) for w in w_raw]

        rho4 = p208c.zero_matrix(4, 4, p208c.GaussianRational(0, 0))
        for k in range(4):
            P_k = projs4[1][k]
            scaled = p208c.matrix_scale(p208c.GaussianRational(p_weights[k], 0), P_k)
            rho4 = p208c.matrix_add(rho4, scaled)

        probs4 = p208c.measure_mub_probabilities(rho4, projs4)
        assert len(probs4) == 5

        rho4_rec = p208c.reconstruct_state_from_probabilities(
            probs4, projs4, 4, p208c.GaussianRational(0, 0), p208c.GaussianRational(1, 0)
        )
        for i in range(4):
            for j in range(4):
                assert rho4_rec[i][j] == rho4[i][j]
        checks += 3

    print(f"  Target P208c passed {checks} checks.")
    return checks


# ==============================================================================
# 5. Multi-Target 4-Pillar Cross-Integration Pipeline Fuzzing
# ==============================================================================

def test_four_pillar_cross_integration() -> int:
    """Chains P204 -> P208a -> P208b -> P208c in an end-to-end operational pipeline."""
    print(">>> Executing Multi-Target 4-Pillar Cross-Integration Pipeline...")
    checks = 0
    rng = random.Random(700700)

    # 20 randomized integration trials
    for trial in range(20):
        # ---------------------------------------------------------------------
        # Pillar 1 (P204): Composite State Preparation & Operational Non-Signaling
        # ---------------------------------------------------------------------
        space_a = p204.OutcomeSpace(("alice_0", "alice_1"))
        space_b = p204.OutcomeSpace(("bob_0", "bob_1"))
        comp_space = p204.tensor_outcome_space(space_a, space_b)

        # Rational bipartite preparation
        raw_joint = [rng.randint(5, 50) for _ in range(4)]
        tot_j = sum(raw_joint)
        joint_map = {
            ("alice_0", "bob_0"): Fraction(raw_joint[0], tot_j),
            ("alice_0", "bob_1"): Fraction(raw_joint[1], tot_j),
            ("alice_1", "bob_0"): Fraction(raw_joint[2], tot_j),
            ("alice_1", "bob_1"): Fraction(raw_joint[3], tot_j),
        }
        state_ab = p204.OperationalState(comp_space, joint_map)

        # Operational partition of unity on Alice
        cut_w = Fraction(rng.randint(1, 9), 10)
        eff_a0 = p204.OperationalEffect(space_a, {"alice_0": cut_w, "alice_1": Fraction(1, 1) - cut_w})
        eff_a1 = eff_a0.complement()
        test_eff_b = p204.OperationalEffect(space_b, {"bob_0": Fraction(3, 5), "bob_1": Fraction(4, 5)})

        ns_receipt = p204.verify_non_signaling_across_cut(
            state_ab, space_a, space_b, [eff_a0, eff_a1], test_eff_b
        )
        assert ns_receipt["non_signaling"] is True
        checks += 2

        # Extract marginal preparation for Alice
        s_a = p204.marginal_state_a(state_ab, space_a, space_b)
        p_a0 = s_a.probability("alice_0")
        p_a1 = s_a.probability("alice_1")

        # ---------------------------------------------------------------------
        # Pillar 2 (P208a): path_interference & Sorkin Vanishing
        # ---------------------------------------------------------------------
        # Encode Alice marginal probabilities into path_amplitudes in a 3-branch diamond
        amp_a = p208a.GaussianRational(p_a0, 0)
        # Shift path B by a Pythagorean rotation
        u_pyth = p208a.GaussianRational.unit_pythagorean(3, 4)  # ( -7/25, 24/25 )
        amp_b = p208a.GaussianRational(p_a1, 0) * u_pyth
        amp_c = p208a.GaussianRational(Fraction(1, 10), Fraction(1, 10))

        diamond = p208a.Diamond2Complex(["A", "B", "C"], {"A": amp_a, "B": amp_b, "C": amp_c})
        # Second-order path_interference is non-zero
        i2_val = diamond.second_order_interference("A", "B")
        assert i2_val != Fraction(0, 1)
        # Third-order Sorkin quantity vanishes identically
        i3_val = diamond.third_order_sorkin("A", "B", "C")
        assert i3_val == Fraction(0, 1)
        checks += 3

        # ---------------------------------------------------------------------
        # Pillar 3 (P208b): Non-Local Correlator & Cabello Parity Obstruction
        # ---------------------------------------------------------------------
        # Evaluate Pythagorean non-local model: S = 14/5 = 2.8 > 2
        tab, s_val = p208b.pythagorean_model()
        assert s_val == Fraction(14, 5)
        assert tab.is_no_signaling() is True

        # Verify Cabello 18-ray contextuality parity obstruction
        cech_obs = p208b.cech_cochain_parity_obstruction()
        assert cech_obs["coboundary_obstruction_mod2"] == 1
        checks += 3

        # ---------------------------------------------------------------------
        # Pillar 4 (P208c): Commutator Trace Obstruction & State Tomography
        # ---------------------------------------------------------------------
        # Microcausality check on 2-carrier register
        M_a = [
            [p_a0, p_a1],
            [p_a1, p_a0],
        ]
        M_b = [
            [Fraction(1, 2), Fraction(1, 2)],
            [Fraction(1, 2), Fraction(-1, 2)],
        ]
        assert p208c.verify_microcausality_bipartite(M_a, M_b) is True
        assert p208c.commutator_trace(M_a, M_b) == Fraction(0, 1)

        # Complete operational state tomography reconstruction in d = 3
        projs3 = p208c.construct_mub_projectors_dim3()
        # Build test density operator from Alice marginal probabilities
        rho_in = p208c.zero_matrix(3, 3, p208c.Cyclotomic3(0))
        rho_in[0][0] = p208c.Cyclotomic3(p_a0)
        rho_in[1][1] = p208c.Cyclotomic3(p_a1)
        rho_in[2][2] = p208c.Cyclotomic3(Fraction(0, 1))

        probs_meas = p208c.measure_mub_probabilities(rho_in, projs3)
        rho_out = p208c.reconstruct_state_from_probabilities(
            probs_meas, projs3, 3, p208c.Cyclotomic3(0), p208c.Cyclotomic3(1)
        )
        for i in range(3):
            for j in range(3):
                assert rho_out[i][j] == rho_in[i][j]
        checks += 4

    print(f"  4-Pillar Cross-Integration passed {checks} checks.")
    return checks


# ==============================================================================
# 6. Repository Seal and Axiom Audit
# ==============================================================================

def audit_repository_seal_and_axioms() -> int:
    """Audit repository blind seal integrity and Lean 4 axiom censuses across Cohort 7."""
    print(">>> Auditing Repository Seal & Lean 4 Axioms...")
    checks = 0

    SEALED_PATHS = [
        "prompt",
        "paper",
        "code",
        "lean4/Derivation",
        "artifacts",
        "CLAUDE.md",
    ]

    # 1. Seal audit: git status
    git_proc = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert git_proc.returncode == 0
    violations = []
    for line in git_proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(maxsplit=1)
        status = parts[0]
        path = parts[1].replace("\\", "/")

        for sp in SEALED_PATHS:
            if path == sp or path.startswith(sp + "/"):
                violations.append(path)

        # Tracked modifications outside research/ and .agents/
        if status in ("M", "D", "A", "R") and not (
            path.startswith("research/") or path.startswith(".agents/")
        ):
            violations.append(path)

    assert len(violations) == 0, f"Repository seal violation detected: {violations}"
    checks += 1

    # 2. Lean packages build and axiom audit across all 4 targets
    lean_packages = [
        REPO_ROOT / "research" / "p204_operational_valuations" / "lean",
        REPO_ROOT / "research" / "p208a_path_interference" / "lean",
        REPO_ROOT / "research" / "p208b_contextuality_nonlocality" / "lean",
        REPO_ROOT / "research" / "p208c_commutator_tomography" / "lean",
    ]
    ALLOWED_AXIOMS = {"propext", "Quot.sound"}
    total_theorems = 0

    for pkg in lean_packages:
        # lake build
        proc = subprocess.run(["lake", "build"], cwd=pkg, capture_output=True, text=True, check=False)
        assert proc.returncode == 0, f"lake build failed for {pkg.parent.name}:\n{proc.stderr}"
        checks += 1

        # Inventory.lean census and axiom audit
        inv_proc = subprocess.run(
            ["lake", "env", "lean", "Inventory.lean"], cwd=pkg, capture_output=True, text=True, check=False
        )
        assert inv_proc.returncode == 0, f"Inventory.lean failed for {pkg.parent.name}:\n{inv_proc.stderr}"
        output = inv_proc.stdout + inv_proc.stderr

        # Check forbidden dependencies
        for forbidden in ["Classical.choice", "mathlib"]:
            assert forbidden not in output, f"Disallowed dependency '{forbidden}' found in {pkg.parent.name}"

        # Parse axioms
        pkg_theorems = 0
        for line in output.splitlines():
            if "depends on axioms: [" in line:
                pkg_theorems += 1
                ax_part = line.split("depends on axioms: [")[1].split("]")[0]
                axioms = [a.strip() for a in ax_part.split(",") if a.strip()]
                for a in axioms:
                    assert a in ALLOWED_AXIOMS, (
                        f"Disallowed axiom '{a}' in {pkg.parent.name}: not in {ALLOWED_AXIOMS}"
                    )
            elif "does not depend on any axioms" in line:
                pkg_theorems += 1
        total_theorems += pkg_theorems
        checks += 1

    assert total_theorems >= 200, f"Expected >= 200 formal Lean 4 theorems, got {total_theorems}"
    print(f"  Seal and axiom audits passed {checks} checks (verified {total_theorems} Lean 4 theorems).")
    return checks


# ==============================================================================
# Main Runner & Receipt Generation
# ==============================================================================

def main() -> None:
    print("=" * 80)
    print("Genesis Cohort 7 Master Empirical Adversarial Stress Suite")
    print("Lead Architect & Adversarial Critic Review Gate")
    print("=" * 80)

    start_time = time.time()
    total_checks = 0

    total_checks += test_p204_adversarial_operational_valuations()
    total_checks += test_p208a_adversarial_path_interference()
    total_checks += test_p208b_adversarial_contextuality_nonlocality()
    total_checks += test_p208c_adversarial_commutator_tomography()
    total_checks += test_four_pillar_cross_integration()
    total_checks += audit_repository_seal_and_axioms()

    elapsed = time.time() - start_time
    print("=" * 80)
    print(f"ALL ADVERSARIAL CHECKS PASSED in {elapsed:.4f}s")
    print(f"Total Verified Checks for Cohort 7: {total_checks}")
    print("Axioms verified strictly within {propext, Quot.sound}; zero Classical.choice.")
    print("=" * 80)

    receipt = {
        "suite": "Cohort 7 Master Empirical Adversarial Stress Suite",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_checks": total_checks,
        "elapsed_seconds": elapsed,
        "targets_covered": ["P204", "P208a", "P208b", "P208c"],
        "cross_integration": "PASS",
        "seal_audit": "PASS",
        "axiom_audit": "PASS",
        "status": "PASS",
    }
    receipt_path = REPO_ROOT / "research" / "e2e_tests" / "evidence_cohort7_adversarial.json"
    receipt_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"Receipt written to {receipt_path}")


if __name__ == "__main__":
    main()
