"""Proof and simulation of spacelike-separated non-signaling.

Demonstrates:
1. Spacelike separation:
   Local interventions at Locus 1 and embedded readouts at Locus 2 have
   disjoint access footprints prior to relational step propagation.
2. Marginal distribution invariance:
   Arbitrary interventions at Locus 1 do not perturb the marginal readout
   distribution at Locus 2:
       P(R2 = r | I1 = a) = P(R2 = r | I1 = b)
   Total variation distance between marginal distributions is exactly 0.0.
3. Inter-observer correlation on symmetric/correlated preparations:
   Coincidence evaluators record agreement, while marginal readouts remain
   strictly independent of distant intervention choices.
4. Causal propagation contrast:
   Signaling occurs only after relational step propagation through mediating
   coupling channel M.

AuthorityEffect: None.
Axiom Scope: Constructive finite state probability distributions and exact counting.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Sequence, Tuple

from embedded_observer import EmbeddedObserver, create_duplicate_observers
from protocol import (
    CarrierState,
    Locus,
    coincidence_evaluator,
    intervene_l1,
    prepare_product,
    prepare_symmetric,
)


def compute_marginal_r2_distribution(
    states: Sequence[CarrierState],
    intervention_1: Callable[[int], int],
    observer_2: EmbeddedObserver,
) -> Dict[int, float]:
    """Compute empirical marginal distribution of Observer 2's record R2

    after applying an intervention at Locus 1.
    """
    counts: Counter[int] = Counter()
    total = len(states)
    if total == 0:
        return {}

    for s in states:
        # Apply intervention at Locus 1
        s_perturbed = intervene_l1(s, intervention_1)
        # Observer 2 executes readout
        s_measured = observer_2.readout(s_perturbed)
        r2_val = observer_2.get_record(s_measured)
        counts[r2_val] += 1

    return {k: v / total for k, v in counts.items()}


def total_variation_distance(
    p: Dict[int, float], q: Dict[int, float]
) -> float:
    """Compute total variation distance between two discrete distributions:

    TVD = 0.5 * sum_x |p(x) - q(x)|.
    """
    all_keys = set(p.keys()) | set(q.keys())
    diff = sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in all_keys)
    return 0.5 * diff


@dataclass(frozen=True)
class NonSignalingReport:
    """Rigorous verification report for spacelike non-signaling."""

    total_states_tested: int
    interventions_tested: List[str]
    max_total_variation_distance: float
    non_signaling_satisfied: bool
    marginal_distributions: Dict[str, Dict[int, float]]


def verify_spacelike_non_signaling(
    states: Sequence[CarrierState],
    interventions: Dict[str, Callable[[int], int]],
    observer_2: EmbeddedObserver,
    tolerance: float = 1e-12,
) -> NonSignalingReport:
    """Test multiple candidate interventions at Locus 1 and verify that

    the marginal distribution at Observer 2 remains invariant within tolerance.
    """
    distributions: Dict[str, Dict[int, float]] = {}
    for name, fn in interventions.items():
        distributions[name] = compute_marginal_r2_distribution(states, fn, observer_2)

    names = list(interventions.keys())
    max_tvd = 0.0
    if len(names) >= 2:
        base_name = names[0]
        base_dist = distributions[base_name]
        for other_name in names[1:]:
            tvd = total_variation_distance(base_dist, distributions[other_name])
            if tvd > max_tvd:
                max_tvd = tvd

    satisfied = max_tvd <= tolerance

    return NonSignalingReport(
        total_states_tested=len(states),
        interventions_tested=names,
        max_total_variation_distance=max_tvd,
        non_signaling_satisfied=satisfied,
        marginal_distributions=distributions,
    )


def simulate_correlated_pair_protocol(
    n_trials: int,
    modulus: int = 4,
    intervention_1: Callable[[int], int] = lambda x: (x + 1) % 4,
) -> Dict[str, Any]:
    """Demonstrate inter-observer correlation without signaling:

    1. Prepare ensemble of correlated states: l1 == l2.
    2. Without intervention, coincidence evaluator records 100% agreement.
    3. Observer 1 applies local intervention; Observer 2 marginal distribution
       remains identical to the unperturbed marginal distribution.
    """
    obs1, obs2 = create_duplicate_observers()

    # Initial unperturbed ensemble
    states = [prepare_symmetric(CarrierState(), v=i % modulus) for i in range(n_trials)]

    # 1. Unperturbed joint readout
    unperturbed_agreements = 0
    for s in states:
        s1 = obs1.readout(s)
        s2 = obs2.readout(s1)
        if coincidence_evaluator(s2):
            unperturbed_agreements += 1

    # 2. Compare marginal distributions with vs without intervention at L1
    identity_intervention = lambda x: x
    dist_unperturbed = compute_marginal_r2_distribution(states, identity_intervention, obs2)
    dist_perturbed = compute_marginal_r2_distribution(states, intervention_1, obs2)
    tvd = total_variation_distance(dist_unperturbed, dist_perturbed)

    return {
        "n_trials": n_trials,
        "unperturbed_coincidence_rate": unperturbed_agreements / n_trials,
        "marginal_tvd": tvd,
        "is_non_signaling": tvd < 1e-12,
    }


def simulate_causal_propagation_contrast(
    s: CarrierState,
    intervention_val: int,
) -> Dict[str, Any]:
    """Contrast demonstration: signaling occurs ONLY after relational propagation

    through mediating channel M.
    Step 0: Spacelike separation -> R2 marginal unaffected.
    Step 1: Observer 1 writes to M.
    Step 2: Observer 2 reads from M into L2, then reads into R2 -> R2 diverges!
    """
    obs1, obs2 = create_duplicate_observers()

    # Base state
    s0 = CarrierState(l1=0, l2=0, m=0, r1=0, r2=0)
    # Perturbed state at L1
    s_pert = CarrierState(l1=intervention_val, l2=0, m=0, r1=0, r2=0)

    # Step 0: Immediate readout at Locus 2 prior to propagation
    r2_base_0 = obs2.get_record(obs2.readout(s0))
    r2_pert_0 = obs2.get_record(obs2.readout(s_pert))
    spacelike_shift = (r2_base_0 != r2_pert_0)

    # Step 1: Relational propagation step 1: Locus 1 writes to M
    s0_m = CarrierState(l1=s0.l1, l2=s0.l2, m=s0.l1, r1=0, r2=0)
    s_pert_m = CarrierState(l1=s_pert.l1, l2=s_pert.l2, m=s_pert.l1, r1=0, r2=0)

    # Step 2: Relational propagation step 2: Locus 2 reads M
    s0_coupled = CarrierState(l1=s0_m.l1, l2=s0_m.m, m=s0_m.m, r1=0, r2=0)
    s_pert_coupled = CarrierState(l1=s_pert_m.l1, l2=s_pert_m.m, m=s_pert_m.m, r1=0, r2=0)

    # Observer 2 reads post-propagation
    r2_base_post = obs2.get_record(obs2.readout(s0_coupled))
    r2_pert_post = obs2.get_record(obs2.readout(s_pert_coupled))
    causal_shift = (r2_base_post != r2_pert_post)

    return {
        "spacelike_shift_detected": spacelike_shift,
        "causal_shift_detected": causal_shift,
        "information_transferred_post_coupling": causal_shift and (not spacelike_shift),
    }
