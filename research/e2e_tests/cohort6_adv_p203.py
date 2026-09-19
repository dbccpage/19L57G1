"""P203 adversarial checks for Cohort 6."""
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

