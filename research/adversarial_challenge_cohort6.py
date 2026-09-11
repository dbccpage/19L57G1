"""Master Empirical Adversarial Stress Suite for Genesis Cohort 6.

Lead Architect & Adversarial Critic Review Gate.
Targets:
- P203: Composite Systems & Pre-Spatial Locality
- M108: General Internal Algebra
- M109: Higher Chain Complexes & Obstruction Homology
- X300: Observer-Relative Information, Channels & Loss

Axiom Scope: Constructive discrete carrier operations with exact rational arithmetic.
Allowed Axioms: strictly within {'propext', 'Quot.sound'} (zero Classical.choice, zero mathlib).
AuthorityEffect: None.
Claim Hygiene: All properties bounded to finite discrete models; exact rational arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import time
from typing import Any, Callable, Dict, List, Mapping, Sequence, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent

# Prepend research directories for Cohort 6
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


# ==============================================================================
# 1. Target P203: Composite Systems & Pre-Spatial Locality Fuzzing
# ==============================================================================

def test_p203_adversarial_composite_systems() -> int:
    """Fuzz P203 multi-locus carrier networks, non-signaling cuts, and observer pairs."""
    print(">>> Fuzzing Target P203: Composite Systems & Pre-Spatial Locality...")
    checks = 0
    rng = random.Random(203203)

    # 1. Random multi-locus network configurations & associativity isomorphism sweeps
    for n_loci in range(3, 12):
        locus_names = [f"loc_{i}" for i in range(n_loci)]
        split1 = n_loci // 3
        split2 = (2 * n_loci) // 3
        if split1 == 0:
            split1 = 1
        if split2 <= split1:
            split2 = split1 + 1

        part_a_keys = locus_names[:split1]
        part_b_keys = locus_names[split1:split2]
        part_c_keys = locus_names[split2:]

        state_a = p203.CarrierState({k: rng.randint(-100, 100) for k in part_a_keys})
        state_b = p203.CarrierState({k: rng.randint(-100, 100) for k in part_b_keys})
        state_c = p203.CarrierState({k: rng.randint(-100, 100) for k in part_c_keys})

        # Test canonical associator isomorphism: (A ⊗ B) ⊗ C ≅ A ⊗ (B ⊗ C)
        assoc_rep = p203.verify_associativity_isomorphism(state_a, state_b, state_c)
        assert assoc_rep["associativity_satisfied"] is True
        assert assoc_rep["identical_valuations"] is True
        assert assoc_rep["proj_a_preserved"] is True
        assert assoc_rep["proj_b_preserved"] is True
        assert assoc_rep["proj_c_preserved"] is True
        checks += 5

        # Overlap refusal: tensor composition of non-disjoint subsystems must raise ValueError
        overlapping_state = p203.CarrierState({part_a_keys[0]: 42, "other": 99})
        try:
            state_a.tensor(overlapping_state)
            raise AssertionError("Expected ValueError on overlapping tensor composition")
        except ValueError:
            checks += 1

    # 2. Bipartite cut operational non-signaling sweeps (TVD = 0.0)
    for cut_trial in range(30):
        n_a = rng.randint(2, 5)
        n_b = rng.randint(2, 5)
        loci_a = [f"a_{i}" for i in range(n_a)]
        loci_b = [f"b_{j}" for j in range(n_b)]
        cut = p203.BipartiteCut(part_a=frozenset(loci_a), part_b=frozenset(loci_b))

        # Generate ensemble of 80 random carrier states
        ensemble = [
            p203.CarrierState({
                **{k: rng.randint(0, 10) for k in loci_a},
                **{k: rng.randint(0, 10) for k in loci_b},
            })
            for _ in range(80)
        ]

        # Interventions localized strictly to Part A
        interventions = [
            p203.Transition(
                name="inc_a0",
                reads=frozenset([loci_a[0]]),
                writes=frozenset([loci_a[0]]),
                transform=lambda s, target=loci_a[0]: {target: s[target] + 1},
            ),
            p203.Transition(
                name="permute_a",
                reads=frozenset(loci_a),
                writes=frozenset(loci_a),
                transform=lambda s, la=loci_a: {la[i]: s[la[(i + 1) % len(la)]] for i in range(len(la))},
            ),
            p203.Transition(
                name="reset_a",
                reads=frozenset(),
                writes=frozenset([loci_a[-1]]),
                transform=lambda _: {loci_a[-1]: 0},
            ),
        ]

        # Observable localized strictly to Part B
        obs_target = loci_b[0]
        observable_b = p203.Observable(
            name="read_b0_parity",
            footprint=frozenset([obs_target]),
            measure=lambda s, t=obs_target: s[t] % 2,
        )

        ns_rep = p203.verify_operational_non_signaling(ensemble, cut, interventions, observable_b)
        assert ns_rep["non_signaling_satisfied"] is True
        assert ns_rep["max_tvd"] == Fraction(0, 1)
        checks += 2

        # 3. Leaky intervention attack: writing to Part B from Part A yields TVD > 0
        leaky_op = p203.Transition(
            name="leak_to_b",
            reads=frozenset([loci_a[0]]),
            writes=frozenset([loci_a[0], obs_target]),
            transform=lambda s, t=obs_target, src=loci_a[0]: {src: s[src], t: 999},
        )
        tvd_leak = p203.verify_leaky_intervention_divergence(ensemble, cut, leaky_op, observable_b)
        assert tvd_leak > Fraction(0, 1)
        checks += 1

        # 4. Mediated coupling attack: mediated transition across cut enables signaling (TVD > 0)
        intervention_a = p203.Transition(
            name="override_a0",
            reads=frozenset(),
            writes=frozenset([loci_a[0]]),
            transform=lambda _: {loci_a[0]: 777},
        )
        mediating_op = p203.Transition(
            name="copy_a0_to_b0",
            reads=frozenset([loci_a[0]]),
            writes=frozenset([obs_target]),
            transform=lambda s, src=loci_a[0], dst=obs_target: {dst: s[src]},
        )
        tvd_mediated = p203.verify_mediated_coupling_divergence(
            ensemble, cut, intervention_a, mediating_op, observable_b
        )
        assert tvd_mediated > Fraction(0, 1)
        checks += 1

    # 5. Duplicate observer agreement and graph automorphism invariance sweeps
    for g_trial in range(25):
        # Construct symmetric 4-locus diamond graph: u <-> w1 <-> v, u <-> w2 <-> v
        loci = ["u", "v", "w1", "w2"]
        # Reflection automorphism swaps u <-> v and w1 <-> w2
        refl = {"u": "v", "v": "u", "w1": "w2", "w2": "w1"}
        non_aut = {"u": "w1", "w1": "u", "v": "v", "w2": "w2"}

        transitions = [
            p203.Transition("e_u_w1", frozenset(["u"]), frozenset(["w1"]), lambda s: {"w1": s["u"]}),
            p203.Transition("e_u_w2", frozenset(["u"]), frozenset(["w2"]), lambda s: {"w2": s["u"]}),
            p203.Transition("e_w1_v", frozenset(["w1"]), frozenset(["v"]), lambda s: {"v": s["w1"]}),
            p203.Transition("e_w2_v", frozenset(["w2"]), frozenset(["v"]), lambda s: {"v": s["w2"]}),
        ]
        graph = p203.InteractionGraph.derive_from_operations(loci, transitions)
        assert graph.is_automorphism(refl) is True
        assert graph.is_automorphism(non_aut) is False
        checks += 2

        # Duplicate observers at symmetric loci u and v
        pair = p203.DuplicateObserverPair("u", "v", readout_probe=lambda x: x % 3)

        # Mixed ensemble of symmetric and asymmetric states
        sym_states = [
            p203.CarrierState({"u": val, "v": val, "w1": w, "w2": w})
            for val in range(5)
            for w in range(2)
        ]
        asym_states = [
            p203.CarrierState({"u": 0, "v": 1, "w1": 0, "w2": 2}),
            p203.CarrierState({"u": 1, "v": 2, "w1": 1, "w2": 0}),
            p203.CarrierState({"u": 2, "v": 0, "w1": 0, "w2": 1}),
        ]
        mixed_ensemble = sym_states + asym_states

        agr_rep = p203.verify_duplicate_observer_agreement(mixed_ensemble, pair, refl)
        assert agr_rep["duplicate_agreement_satisfied"] is True
        assert agr_rep["symmetric_agreement_rate"] == Fraction(1, 1)
        assert agr_rep["asymmetric_divergence_rate"] == Fraction(1, 1)
        checks += 3

    print(f"  P203 passed {checks} adversarial checks.")
    return checks


# ==============================================================================
# 2. Target M108: General Internal Algebra Fuzzing
# ==============================================================================

def test_m108_adversarial_internal_algebra() -> int:
    """Fuzz M108 free monoids, free modules over Q, free rings, and quotient factorizations."""
    print(">>> Fuzzing Target M108: General Internal Algebra...")
    checks = 0
    rng = random.Random(108108)

    # 1. Free monoid universal mapping property & arrow uniqueness
    for trial in range(30):
        alphabet = [f"g_{i}" for i in range(rng.randint(2, 6))]
        fm = m108.FreeMonoid(set(alphabet))

        # Target monoid: additive InternalInt
        val_map = {g: m108.InternalInt(rng.randint(-50, 50)) for g in alphabet}

        # Generate sample words
        sample_words = [m108.Word.unit()]
        for g in alphabet:
            sample_words.append(fm.eta(g))
        for _ in range(5):
            w = m108.Word.unit()
            for _ in range(rng.randint(2, 5)):
                w = w + fm.eta(rng.choice(alphabet))
            sample_words.append(w)

        ump_res = fm.verify_universal_mapping_property(
            f=lambda g, vm=val_map: vm[g],
            target_unit=m108.InternalInt(0),
            target_mul=lambda x, y: x + y,
            sample_words=sample_words,
        )
        assert ump_res["holds"] is True
        checks += 1

        # Verify arrow uniqueness
        def valid_candidate(w: m108.Word, vm=val_map) -> m108.InternalInt:
            tot = m108.InternalInt(0)
            for ch in w.letters:
                tot = tot + vm[ch]
            return tot

        assert fm.verify_arrow_uniqueness(
            f=lambda g, vm=val_map: vm[g],
            candidate_hom=valid_candidate,
            target_unit=m108.InternalInt(0),
            target_mul=lambda x, y: x + y,
            test_words=sample_words,
        ) is True
        checks += 1

        # Negative test: defective candidate map rejected
        def defective_candidate(w: m108.Word, vm=val_map) -> m108.InternalInt:
            base = valid_candidate(w, vm)
            return base + m108.InternalInt(1) if len(w) > 1 else base

        assert fm.verify_arrow_uniqueness(
            f=lambda g, vm=val_map: vm[g],
            candidate_hom=defective_candidate,
            target_unit=m108.InternalInt(0),
            target_mul=lambda x, y: x + y,
            test_words=sample_words,
        ) is False
        checks += 1

    # 2. Free module / vector space over Q & linear UMP sweeps
    for trial in range(30):
        basis = [f"e_{i}" for i in range(rng.randint(2, 5))]
        fmod = m108.FreeModule(set(basis), scalar_type=m108.InternalRat)

        # Target vector space: 1D rational field InternalRat
        eval_weights = {
            b: m108.InternalRat(rng.randint(-20, 20), rng.randint(1, 10)) for b in basis
        }

        # Linear combination operations
        lc1 = m108.LinearCombination.zero()
        lc2 = m108.LinearCombination.zero()
        for b in basis:
            lc1 = lc1 + fmod.eta(b).smul(m108.InternalRat(rng.randint(-5, 5), rng.randint(1, 5)))
            lc2 = lc2 + fmod.eta(b).smul(m108.InternalRat(rng.randint(-5, 5), rng.randint(1, 5)))

        # Additive inverse cancellation
        zero_test = lc1 + (-lc1)
        assert zero_test.is_zero()
        checks += 1

        # Scalar distributivity
        sc_a = m108.InternalRat(rng.randint(-5, 5), rng.randint(1, 5))
        sc_b = m108.InternalRat(rng.randint(-5, 5), rng.randint(1, 5))
        dist_lhs = (lc1 + lc2).smul(sc_a)
        dist_rhs = lc1.smul(sc_a) + lc2.smul(sc_a)
        assert dist_lhs == dist_rhs
        checks += 1

        # Free module UMP over Q
        sample_elems = [m108.LinearCombination.zero(), lc1, lc2, lc1 + lc2]
        ump_mod = fmod.verify_universal_mapping_property(
            f=lambda g, ew=eval_weights: ew[g],
            target_zero=m108.InternalRat.zero(),
            target_add=lambda x, y: x + y,
            target_smul=lambda sc, x: sc * x,
            sample_elements=sample_elems,
        )
        assert ump_mod["holds"] is True
        checks += 1

        # Arrow uniqueness
        def valid_linear(elem: m108.LinearCombination, ew=eval_weights) -> m108.InternalRat:
            acc = m108.InternalRat.zero()
            for k, c in elem.terms:
                acc = acc + c * ew[k]
            return acc

        assert fmod.verify_arrow_uniqueness(
            f=lambda g, ew=eval_weights: ew[g],
            candidate_linear=valid_linear,
            target_zero=m108.InternalRat.zero(),
            target_add=lambda x, y: x + y,
            target_smul=lambda sc, x: sc * x,
            test_elements=sample_elems,
        ) is True
        checks += 1

    # 3. Free ring Cauchy multiplication, non-commutativity & UMP
    for trial in range(25):
        gens = {"x", "y"}
        fring = m108.FreeRing(gens, scalar_type=m108.InternalRat)
        x = fring.eta("x")
        y = fring.eta("y")
        one = m108.FreeRingElement.one(m108.InternalRat)
        zero = m108.FreeRingElement.zero()

        # Cauchy multiplication associativity & distributivity
        lhs = x * (y + one)
        rhs = (x * y) + x
        assert lhs == rhs
        checks += 1

        # Non-commutativity of free ring generators: x*y != y*x
        assert x * y != y * x
        checks += 1

        # Zero annihilation
        assert (x * zero).is_zero()
        assert (zero * y).is_zero()
        checks += 2

    # 4. Congruence relation, representative independence, and quotient factorization
    for trial in range(25):
        modulus = rng.randint(3, 9)
        base_alg = m108.Algebra(
            name=f"Z_mod_{modulus}",
            signature=m108.MONOID_SIGNATURE,
            interpretations={
                "e": lambda: m108.InternalInt(0),
                "mul": lambda a, b: a + b,
            },
        )

        def mod_rel(a: m108.InternalInt, b: m108.InternalInt, m=modulus) -> bool:
            return (a.val - b.val) % m == 0

        congruence = m108.CongruenceRelation(base_alg, mod_rel, name=f"mod_{modulus}")
        sample_ints = [m108.InternalInt(i) for i in range(-15, 15)]
        op_tuples = {
            "mul": [(m108.InternalInt(i), m108.InternalInt(j)) for i in range(-3, 4) for j in range(-3, 4)]
        }

        axiom_res = congruence.verify_congruence_axioms(sample_ints, op_tuples)
        assert axiom_res["valid"] is True
        # Explicitly verify individual equivalence properties
        assert all(congruence.rel(x, x) for x in sample_ints)  # Reflexive
        assert all(congruence.rel(x, y) == congruence.rel(y, x) for x in sample_ints[:8] for y in sample_ints[:8])  # Symmetric
        assert all(
            not (congruence.rel(x, y) and congruence.rel(y, z)) or congruence.rel(x, z)
            for x in sample_ints[:6] for y in sample_ints[:6] for z in sample_ints[:6]
        )  # Transitive
        checks += 4

        # Build quotient algebra
        q_alg = m108.QuotientAlgebra(
            base_alg,
            congruence,
            canonicalizer=lambda x, m=modulus: m108.InternalInt(x.val % m),
            name=f"Z_{modulus}",
        )
        test_pairs = [
            (
                (m108.InternalInt(1), m108.InternalInt(2)),
                (m108.InternalInt(1 + modulus), m108.InternalInt(2 + modulus)),
            ),
            (
                (m108.InternalInt(0), m108.InternalInt(modulus - 1)),
                (m108.InternalInt(modulus), m108.InternalInt(2 * modulus - 1)),
            ),
        ]
        assert q_alg.check_representative_independence("mul", test_pairs) is True
        checks += 1

        # Target algebra: Z_m under addition
        target_alg = m108.Algebra(
            name=f"Z{modulus}",
            signature=m108.MONOID_SIGNATURE,
            interpretations={
                "e": lambda: m108.InternalInt(0),
                "mul": lambda a, b, m=modulus: m108.InternalInt((a.val + b.val) % m),
            },
        )
        h = m108.Homomorphism(
            source=base_alg,
            target=target_alg,
            mapping=lambda x, m=modulus: m108.InternalInt(x.val % m),
            name="mod_proj",
        )

        tilde_h = m108.quotient_factorization(h, q_alg)
        assert m108.verify_quotient_factorization_uniqueness(
            h=h,
            quotient=q_alg,
            candidate_h_bar=lambda q, m=modulus: m108.InternalInt(q.val % m),
            sample_elements=sample_ints[:10],
        ) is True
        checks += 1

        # Defective candidate is rejected
        bad_cand = lambda q, m=modulus: m108.InternalInt((q.val + 1) % m)
        assert m108.verify_quotient_factorization_uniqueness(
            h=h,
            quotient=q_alg,
            candidate_h_bar=bad_cand,
            sample_elements=sample_ints[:10],
        ) is False
        checks += 1

    print(f"  M108 passed {checks} adversarial checks.")
    return checks


# ==============================================================================
# 3. Target M109: Higher Chain Complexes & Obstruction Homology Fuzzing
# ==============================================================================

def test_m109_adversarial_obstruction_homology() -> int:
    """Fuzz M109 chain complexes, boundary nilpotency, Stokes theorem, and Target 7 obstruction."""
    print(">>> Fuzzing Target M109: Higher Chain Complexes & Obstruction Homology...")
    checks = 0
    rng = random.Random(109109)

    # 1. Graded chain complexes: cycle complexes C_n sweeps
    for n in (3, 4, 5, 6, 8, 10):
        cn = m109.build_cycle_complex(n)
        assert cn.max_grade == 1
        assert cn.dimensions[0] == n
        assert cn.dimensions[1] == n

        # Nilpotency at all grades
        nil = cn.verify_nilpotency()
        assert nil == {}  # No intermediate 2-cells, boundary is trivially nilpotent
        checks += 1

        # Homology: 1 connected component, 1 1-cycle
        h = cn.compute_all_homology()
        assert h[0].betti_number == 1
        assert h[1].betti_number == 1
        assert cn.euler_characteristic() == 0
        checks += 3

        # Dual cochain complex & coboundary nilpotency
        dcn = cn.dual_cochain_complex()
        ch = dcn.compute_all_cohomology()
        assert ch[0].betti_number == 1
        assert ch[1].betti_number == 1
        checks += 2

    # 2. Torus complex T_{m,n} sweeps: \partial_1 \circ \partial_2 = 0 & Betti (1, 2, 1)
    for m, n in [(2, 2), (2, 3), (3, 3)]:
        torus = m109.build_torus_complex(m, n)
        nil = torus.verify_nilpotency()
        assert nil[1] is True  # \partial_1 \circ \partial_2 = 0
        checks += 1

        dtorus = torus.dual_cochain_complex()
        cobound_nil = dtorus.verify_coboundary_nilpotency()
        assert cobound_nil[0] is True  # \delta^1 \circ \delta^0 = 0
        checks += 1

        # Homology betti numbers: \beta_0 = 1, \beta_1 = 2, \beta_2 = 1
        h_torus = torus.compute_all_homology()
        assert h_torus[0].betti_number == 1
        assert h_torus[1].betti_number == 2
        assert h_torus[2].betti_number == 1
        assert torus.euler_characteristic() == 0
        checks += 4

        # Duality isomorphism over Q: dim H_k = dim H^k
        ch_torus = dtorus.compute_all_cohomology()
        for k in range(3):
            assert h_torus[k].betti_number == ch_torus[k].betti_number
        checks += 3

        # Discrete Stokes-Cartan theorem verification: <\delta \omega, c> = <\omega, \partial c>
        for _ in range(5):
            omega_1 = [Fraction(rng.randint(-10, 10), rng.randint(1, 5)) for _ in range(torus.dimensions[1])]
            c_2 = [Fraction(rng.randint(-10, 10), rng.randint(1, 5)) for _ in range(torus.dimensions[2])]
            assert dtorus.verify_stokes_theorem(1, omega_1, c_2) is True
            checks += 1

    # 3. Cubical cavity S^2 vs solid cube D^3
    s2 = m109.build_cubical_cavity_complex(include_3cell=False)
    assert s2.euler_characteristic() == 2  # \chi(S^2) = 2
    h_s2 = s2.compute_all_homology()
    assert h_s2[0].betti_number == 1
    assert h_s2[1].betti_number == 0
    assert h_s2[2].betti_number == 1  # 2-cavity cycle
    checks += 4

    cube = m109.build_cubical_cavity_complex(include_3cell=True)
    assert cube.euler_characteristic() == 1  # \chi(D^3) = 1
    h_cube = cube.compute_all_homology()
    assert h_cube[0].betti_number == 1
    assert h_cube[1].betti_number == 0
    assert h_cube[2].betti_number == 0  # 2-cavity cycle filled by 3-cell
    assert h_cube[3].betti_number == 0
    checks += 5

    # 4. Target 7 Relational Move Complex audit
    c7 = m109.build_target7_complex(pure_only=True)
    assert c7.dimensions[0] == 262
    assert c7.dimensions[1] == 638
    assert c7.dimensions[2] == 146
    checks += 3

    nil_c7 = c7.verify_nilpotency()
    assert nil_c7[1] is True  # \partial_1 \circ \partial_2 = 0
    checks += 1

    h0_c7 = c7.compute_homology(0)
    h1_c7 = c7.compute_homology(1)
    h2_c7 = c7.compute_homology(2)
    assert h0_c7.betti_number == 2
    assert h1_c7.betti_number == 232  # 378 cycles - 146 square boundaries = 232
    assert h2_c7.betti_number == 0
    checks += 3

    # Native candidate cost functions on Target 7 pure complex
    reports = m109.evaluate_target7_native_candidates(c7)
    assert len(reports) == 4
    for name in ("rule_span", "width_at_admission", "empty_admission", "mention_deficit"):
        assert name in reports
        # In 2-complex, these cost functions have non-zero coboundary on pure squares
        assert reports[name].is_cocycle is False
        checks += 2

    print(f"  M109 passed {checks} adversarial checks.")
    return checks


# ==============================================================================
# 4. Target X300: Observer-Relative Information, Channels & Loss Fuzzing
# ==============================================================================

def test_x300_adversarial_observer_information() -> int:
    """Fuzz X300 operational channels, Data Processing Inequality, dyadic uncertainty, and Landauer erasure."""
    print(">>> Fuzzing Target X300: Observer-Relative Information, Channels & Loss...")
    checks = 0
    rng = random.Random(300300)

    # 1. Operational channel composition associativity sweeps: (W3 o W2) o W1 = W3 o (W2 o W1)
    for trial in range(30):
        p_err1 = Fraction(rng.randint(1, 4), 10)
        p_err2 = Fraction(rng.randint(1, 4), 10)
        w1 = x300.Channel.binary_symmetric(p_err1)
        w2 = x300.Channel.binary_symmetric(p_err2)
        w3 = x300.Channel({
            0: x300.DiscreteDistribution({0: Fraction(3, 4), 1: Fraction(1, 4)}),
            1: x300.DiscreteDistribution({0: Fraction(1, 3), 1: Fraction(2, 3)}),
        })

        c_left = w1.compose(w2).compose(w3)
        c_right = w1.compose(w2.compose(w3))

        for x_sym in (0, 1):
            d_left = c_left.transition(x_sym)
            d_right = c_right.transition(x_sym)
            for z_sym in (0, 1):
                assert d_left.prob(z_sym) == d_right.prob(z_sym)
        checks += 2

    # 2. Data Processing Inequality (DPI) sweeps across noisy cascades
    for trial in range(30):
        # Cascaded BSC channels: X -> Y -> Z
        p_x = x300.DiscreteDistribution.uniform([0, 1])
        w_xy = x300.Channel.binary_symmetric(Fraction(rng.randint(1, 3), 10))
        w_yz = x300.Channel.binary_symmetric(Fraction(rng.randint(1, 3), 10))

        cert = x300.verify_data_processing_inequality(p_x, w_xy, w_yz)
        assert cert.passed is True
        assert cert.delta_i >= -1e-12  # Non-negative mutual information loss
        assert cert.i_xy >= cert.i_xz
        checks += 3

        # Deterministic lossy coarse-graining: X uniform on {0, 1, 2, 3} -> Y = X -> Z = Y // 2
        p_quad = x300.DiscreteDistribution.uniform([0, 1, 2, 3])
        w_id = x300.Channel.identity([0, 1, 2, 3])
        w_cg = x300.Channel.coarse_graining(lambda y: y // 2, [0, 1, 2, 3])

        cert_cg = x300.verify_data_processing_inequality(p_quad, w_id, w_cg)
        assert cert_cg.passed is True
        assert math.isclose(cert_cg.i_xy, 2.0)
        assert math.isclose(cert_cg.i_xz, 1.0)
        assert cert_cg.delta_i >= 0.999
        checks += 4

        # Invertible processing (sufficient statistic): Z = 1 - Y
        w_inv = x300.Channel.deterministic({0: 1, 1: 0})
        cert_inv = x300.verify_data_processing_inequality(p_x, w_xy, w_inv)
        assert cert_inv.passed is True
        assert cert_inv.is_sufficient_statistic is True
        assert math.isclose(cert_inv.delta_i, 0.0, abs_tol=1e-12)
        checks += 3

    # 3. Exact dyadic rational uncertainty & relative divergence non-negativity in Q
    for trial in range(30):
        # Lengths summing to Kraft equality sum 2^-l = 1
        lengths_p = {"a": 1, "b": 2, "c": 3, "d": 3}  # 1/2 + 1/4 + 1/8 + 1/8 = 1
        dist_p = x300.DiscreteDistribution.pure_dyadic(lengths_p)
        assert dist_p.is_pure_dyadic() is True
        # H(P) = 1/2*1 + 1/4*2 + 1/8*3 + 1/8*3 = 1/2 + 2/4 + 6/8 = 7/4 in Q
        assert dist_p.exact_dyadic_shannon_entropy() == Fraction(7, 4)
        checks += 2

        # Relative divergence identity: D(P || P) = 0 in Q
        assert x300.exact_dyadic_divergence(dist_p, dist_p) == Fraction(0, 1)
        checks += 1

        # Relative divergence non-negativity: D(P || Q) > 0 for Q != P
        lengths_q = {"a": 2, "b": 2, "c": 2, "d": 2}  # Uniform 1/4 each
        dist_q = x300.DiscreteDistribution.pure_dyadic(lengths_q)
        div_pq = x300.exact_dyadic_divergence(dist_p, dist_q)
        assert div_pq == Fraction(1, 4)
        assert div_pq > Fraction(0, 1)
        # Cross-divergence formula: H(P, Q) = H(P) + D(P || Q)
        assert x300.exact_dyadic_cross_entropy(dist_p, dist_q) == dist_p.exact_dyadic_shannon_entropy() + div_pq
        checks += 3

    # 4. Hartley capacity metric additivity sweeps
    for trial in range(25):
        p1 = x300.DiscreteDistribution.uniform(list(range(4)))  # 2^2 -> cap 2
        p2 = x300.DiscreteDistribution.uniform(list(range(8)))  # 2^3 -> cap 3
        c1 = p1.exact_hartley_capacity()
        c2 = p2.exact_hartley_capacity()
        assert c1 == 2
        assert c2 == 3

        prod = x300.product_distribution(p1, p2)
        assert prod.exact_hartley_capacity() == c1 + c2
        checks += 3

    # 5. Landauer erasure accounting sweeps
    for trial in range(25):
        p_init = x300.DiscreteDistribution.uniform([0, 1])
        acct = x300.LandauerAccounting(p_init, reset_state=0, temperature_kelvin=300.0)
        receipt = acct.compute_erasure_cost()
        assert receipt.initial_entropy_bits == 1.0
        assert receipt.final_entropy_bits == 0.0
        assert receipt.erased_entropy_bits == 1.0
        assert receipt.exact_erased_entropy_q == Fraction(1, 1)
        assert receipt.operational_non_reversibility is True
        checks += 5

        # Already erased state requires 0 dissipation
        p_zero = x300.DiscreteDistribution.point_mass(0)
        acct_zero = x300.LandauerAccounting(p_zero, reset_state=0)
        rec_zero = acct_zero.compute_erasure_cost()
        assert rec_zero.erased_entropy_bits == 0.0
        assert rec_zero.operational_non_reversibility is False
        assert rec_zero.minimal_heat_dissipated_joules == 0.0
        checks += 3

    print(f"  X300 passed {checks} adversarial checks.")
    return checks


# ==============================================================================
# 5. Multi-Target 4-Pillar Cross-Integration Pipeline Test
# ==============================================================================

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

def audit_repository_seal_and_axioms() -> int:
    """Audit repository blind seal integrity and Lean 4 axiom censuses across Cohort 6."""
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
        if status in ("M", "D", "A", "R") and not (path.startswith("research/") or path.startswith(".agents/")):
            violations.append(path)

    assert len(violations) == 0, f"Repository seal violation detected: {violations}"
    checks += 1

    # 2. Lean packages build and axiom audit across all 4 targets
    lean_packages = [
        REPO_ROOT / "research" / "p203_composite_systems" / "lean",
        REPO_ROOT / "research" / "m108_internal_algebra" / "lean",
        REPO_ROOT / "research" / "m109_obstruction_homology" / "lean",
        REPO_ROOT / "research" / "x300_observer_information" / "lean",
    ]
    ALLOWED_AXIOMS = {"propext", "Quot.sound"}

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
        for line in output.splitlines():
            if "depends on axioms: [" in line:
                ax_part = line.split("depends on axioms: [")[1].split("]")[0]
                axioms = [a.strip() for a in ax_part.split(",") if a.strip()]
                for a in axioms:
                    assert a in ALLOWED_AXIOMS, (
                        f"Disallowed axiom '{a}' in {pkg.parent.name}: not in {ALLOWED_AXIOMS}"
                    )
        checks += 1

    print(f"  Seal and axiom audits passed {checks} checks.")
    return checks


# ==============================================================================
# Main Runner & Receipt Generation
# ==============================================================================

def main() -> None:
    print("=" * 80)
    print("Genesis Cohort 6 Master Empirical Adversarial Stress Suite")
    print("Lead Architect & Adversarial Critic Review Gate")
    print("=" * 80)

    start_time = time.time()
    total_checks = 0

    total_checks += test_p203_adversarial_composite_systems()
    total_checks += test_m108_adversarial_internal_algebra()
    total_checks += test_m109_adversarial_obstruction_homology()
    total_checks += test_x300_adversarial_observer_information()
    total_checks += test_four_pillar_cross_integration()
    total_checks += audit_repository_seal_and_axioms()

    elapsed = time.time() - start_time
    print("=" * 80)
    print(f"ALL ADVERSARIAL CHECKS PASSED in {elapsed:.4f}s")
    print(f"Total Verified Checks for Cohort 6: {total_checks}")
    print("Axioms verified strictly within {propext, Quot.sound}; zero Classical.choice.")
    print("=" * 80)

    receipt = {
        "suite": "Cohort 6 Master Empirical Adversarial Stress Suite",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_checks": total_checks,
        "elapsed_seconds": elapsed,
        "targets_covered": ["P203", "M108", "M109", "X300"],
        "cross_integration": "PASS",
        "seal_audit": "PASS",
        "axiom_audit": "PASS",
        "status": "PASS",
    }
    receipt_path = REPO_ROOT / "research" / "evidence_cohort6_adversarial.json"
    receipt_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"Receipt written to {receipt_path}")


if __name__ == "__main__":
    main()
