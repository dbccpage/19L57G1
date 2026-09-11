"""Composite Systems & Pre-Spatial Locality (Target P203).

Establishes:
1. Multi-locus carrier networks with associative composition:
   (A ⊗ B) ⊗ C ≅ A ⊗ (B ⊗ C)
2. Pre-spatial interaction graphs derived from represented read/write footprints.
3. Strict operational non-signaling across bipartite network cuts (TVD = 0.0)
   prior to mediating transitions.
4. Negative controls: leaky footprint intervention and mediated coupling both
   yield TVD > 0.
5. Duplicate observer agreement on symmetric preparations and symmetry invariance
   under graph automorphisms without external spatial coordinates.

AuthorityEffect: None.
Axiom Scope: Constructive finite-state discrete probability distributions and exact rational arithmetic.
"""

from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable, Dict, FrozenSet, Iterable, List, Mapping, Optional, Sequence, Set, Tuple


@dataclass(frozen=True)
class CarrierState:
    """Discrete valuation of a multi-locus carrier network."""

    values: Mapping[str, int]

    def __post_init__(self) -> None:
        # Normalize to immutable dictionary with sorted keys
        object.__setattr__(
            self,
            "values",
            dict(sorted((str(k), int(v)) for k, v in self.values.items())),
        )

    @property
    def loci(self) -> FrozenSet[str]:
        return frozenset(self.values.keys())

    def get(self, locus: str, default: int = 0) -> int:
        return self.values.get(locus, default)

    def __getitem__(self, locus: str) -> int:
        if locus not in self.values:
            raise KeyError(f"Locus '{locus}' not present in carrier state loci {sorted(self.loci)}")
        return self.values[locus]

    def set(self, locus: str, value: int) -> CarrierState:
        new_values = dict(self.values)
        new_values[locus] = int(value)
        return CarrierState(new_values)

    def update(self, mapping: Mapping[str, int]) -> CarrierState:
        new_values = dict(self.values)
        for k, v in mapping.items():
            new_values[k] = int(v)
        return CarrierState(new_values)

    def project(self, subset: Iterable[str]) -> CarrierState:
        target = set(subset)
        return CarrierState({k: v for k, v in self.values.items() if k in target})

    def tensor(self, other: CarrierState) -> CarrierState:
        """Tensor composition of two carrier subsystems over disjoint locus sets."""
        overlap = self.loci & other.loci
        if overlap:
            raise ValueError(f"Cannot compose subsystems with overlapping loci: {sorted(overlap)}")
        merged = dict(self.values)
        merged.update(other.values)
        return CarrierState(merged)


def verify_associativity_isomorphism(
    state_a: CarrierState, state_b: CarrierState, state_c: CarrierState
) -> Dict[str, bool]:
    """Demonstrate the canonical associator isomorphism:

    (A ⊗ B) ⊗ C ≅ A ⊗ (B ⊗ C).
    Verifies that the composite carrier states evaluate to identical locus valuations
    and preserve projection onto each component subsystem.
    """
    left_grouped = (state_a.tensor(state_b)).tensor(state_c)
    right_grouped = state_a.tensor(state_b.tensor(state_c))

    identical_valuations = (left_grouped.values == right_grouped.values)
    proj_a_match = (
        left_grouped.project(state_a.loci).values
        == right_grouped.project(state_a.loci).values
        == state_a.values
    )
    proj_b_match = (
        left_grouped.project(state_b.loci).values
        == right_grouped.project(state_b.loci).values
        == state_b.values
    )
    proj_c_match = (
        left_grouped.project(state_c.loci).values
        == right_grouped.project(state_c.loci).values
        == state_c.values
    )

    return {
        "identical_valuations": identical_valuations,
        "proj_a_preserved": proj_a_match,
        "proj_b_preserved": proj_b_match,
        "proj_c_preserved": proj_c_match,
        "associativity_satisfied": (
            identical_valuations and proj_a_match and proj_b_match and proj_c_match
        ),
    }


@dataclass(frozen=True)
class Transition:
    """An operational transition or intervention with explicit read/write footprints."""

    name: str
    reads: FrozenSet[str]
    writes: FrozenSet[str]
    transform: Callable[[CarrierState], Mapping[str, int]]

    @property
    def active_loci(self) -> FrozenSet[str]:
        return self.reads | self.writes

    def is_localized_to(self, subset: FrozenSet[str]) -> bool:
        return self.active_loci.issubset(subset)

    def apply(self, state: CarrierState) -> CarrierState:
        # Transform takes state and returns dict of updates for write loci
        updates = self.transform(state)
        # Ensure only declared write loci are modified
        invalid_writes = set(updates.keys()) - self.writes
        if invalid_writes:
            raise ValueError(
                f"Transition '{self.name}' attempted to write outside declared writes footprint: {invalid_writes}"
            )
        return state.update(updates)


@dataclass(frozen=True)
class InteractionGraph:
    """Pre-spatial interaction graph derived relationally from operation footprints."""

    vertices: FrozenSet[str]
    edges: FrozenSet[FrozenSet[str]]

    @classmethod
    def derive_from_operations(
        cls, loci: Iterable[str], transitions: Iterable[Transition]
    ) -> InteractionGraph:
        v_set = frozenset(loci)
        edges: Set[FrozenSet[str]] = set()

        for t in transitions:
            # Coupling between read loci and write loci
            for r in t.reads:
                for w in t.writes:
                    if r != w and r in v_set and w in v_set:
                        edges.add(frozenset({r, w}))
            # Direct coupling between multi-write loci in an elementary transition
            writes_list = sorted(t.writes & v_set)
            for i in range(len(writes_list)):
                for j in range(i + 1, len(writes_list)):
                    edges.add(frozenset({writes_list[i], writes_list[j]}))

        return cls(vertices=v_set, edges=frozenset(edges))

    def neighbors(self, locus: str) -> FrozenSet[str]:
        nbrs: Set[str] = set()
        for e in self.edges:
            if locus in e:
                nbrs.update(e - {locus})
        return frozenset(nbrs)

    def shortest_path_distance(self, u: str, v: str) -> Optional[int]:
        """Compute relational shortest path distance (edge step count) in the interaction graph.

        Returns None if unreachable (disconnected).
        """
        if u not in self.vertices or v not in self.vertices:
            return None
        if u == v:
            return 0

        visited: Set[str] = {u}
        queue: deque[Tuple[str, int]] = deque([(u, 0)])

        while queue:
            curr, dist = queue.popleft()
            for nbr in self.neighbors(curr):
                if nbr == v:
                    return dist + 1
                if nbr not in visited:
                    visited.add(nbr)
                    queue.append((nbr, dist + 1))
        return None

    def are_connected(self, u: str, v: str) -> bool:
        return self.shortest_path_distance(u, v) is not None

    def connected_components(self) -> List[FrozenSet[str]]:
        unvisited = set(self.vertices)
        comps: List[FrozenSet[str]] = []
        while unvisited:
            start = next(iter(unvisited))
            comp: Set[str] = {start}
            queue = deque([start])
            unvisited.remove(start)
            while queue:
                curr = queue.popleft()
                for nbr in self.neighbors(curr):
                    if nbr in unvisited:
                        unvisited.remove(nbr)
                        comp.add(nbr)
                        queue.append(nbr)
            comps.append(frozenset(comp))
        return sorted(comps, key=lambda c: sorted(c))

    def is_automorphism(self, perm: Mapping[str, str]) -> bool:
        """Check whether permutation is an automorphism of the interaction graph."""
        if set(perm.keys()) != self.vertices or set(perm.values()) != self.vertices:
            return False
        # Permutation must be injective/bijective
        if len(set(perm.values())) != len(self.vertices):
            return False
        # Edge preservation
        mapped_edges = {
            frozenset({perm[u], perm[v]}) for e in self.edges for u, v in [tuple(e)]
        }
        return mapped_edges == set(self.edges)


@dataclass(frozen=True)
class BipartiteCut:
    """Bipartite network cut partitioning loci into disjoint subsets L_A and L_B."""

    part_a: FrozenSet[str]
    part_b: FrozenSet[str]

    def __post_init__(self) -> None:
        overlap = self.part_a & self.part_b
        if overlap:
            raise ValueError(f"Bipartite cut parts must be disjoint; found overlap {sorted(overlap)}")

    @property
    def total_loci(self) -> FrozenSet[str]:
        return self.part_a | self.part_b

    def is_strictly_in_a(self, transition: Transition) -> bool:
        return transition.active_loci.issubset(self.part_a)

    def is_strictly_in_b(self, transition: Transition) -> bool:
        return transition.active_loci.issubset(self.part_b)

    def is_cut_crossing(self, transition: Transition) -> bool:
        touches_a = bool(transition.active_loci & self.part_a)
        touches_b = bool(transition.active_loci & self.part_b)
        return touches_a and touches_b


@dataclass(frozen=True)
class Observable:
    """An operational observable with explicit measurement footprint."""

    name: str
    footprint: FrozenSet[str]
    measure: Callable[[CarrierState], Any]

    def is_localized_to(self, subset: FrozenSet[str]) -> bool:
        return self.footprint.issubset(subset)


def compute_marginal_distribution(
    ensemble: Sequence[CarrierState], observable: Observable
) -> Dict[Any, Fraction]:
    """Compute exact rational empirical distribution of an observable over an ensemble."""
    total = len(ensemble)
    if total == 0:
        return {}
    counts: Counter[Any] = Counter()
    for s in ensemble:
        res = observable.measure(s)
        counts[res] += 1
    return {k: Fraction(v, total) for k, v in counts.items()}


def total_variation_distance(
    dist_p: Mapping[Any, Fraction | float], dist_q: Mapping[Any, Fraction | float]
) -> Fraction:
    """Compute exact rational Total Variation Distance (TVD) between two discrete distributions:

    TVD = 1/2 * sum_x |P(x) - Q(x)| in Q.
    """
    all_keys = set(dist_p.keys()) | set(dist_q.keys())
    diff = sum(abs(Fraction(dist_p.get(k, 0)) - Fraction(dist_q.get(k, 0))) for k in all_keys)
    return Fraction(1, 2) * diff


def verify_operational_non_signaling(
    ensemble: Sequence[CarrierState],
    cut: BipartiteCut,
    interventions_a: Sequence[Transition],
    observable_b: Observable,
) -> Dict[str, Any]:
    """Verify strict operational non-signaling across a bipartite network cut.

    Ensures that for any intervention localized to Part A, the marginal readout
    distribution on Part B has exact TVD = 0.0 relative to the unperturbed baseline.
    """
    # 1. Footprint checks
    for t in interventions_a:
        if not cut.is_strictly_in_a(t):
            raise ValueError(
                f"Intervention '{t.name}' footprint {sorted(t.active_loci)} leaks outside Part A {sorted(cut.part_a)}"
            )
    if not cut.is_strictly_in_b(
        Transition(
            name="check_obs",
            reads=observable_b.footprint,
            writes=frozenset(),
            transform=lambda _: {},
        )
    ):
        raise ValueError(
            f"Observable '{observable_b.name}' footprint {sorted(observable_b.footprint)} leaks outside Part B {sorted(cut.part_b)}"
        )

    # 2. Baseline unperturbed distribution
    baseline_dist = compute_marginal_distribution(ensemble, observable_b)

    # 3. Test each intervention
    tvd_reports: Dict[str, Fraction] = {}
    distributions: Dict[str, Dict[Any, Fraction]] = {"baseline": baseline_dist}

    for t in interventions_a:
        perturbed_ensemble = [t.apply(s) for s in ensemble]
        dist_t = compute_marginal_distribution(perturbed_ensemble, observable_b)
        distributions[t.name] = dist_t
        tvd_reports[t.name] = total_variation_distance(baseline_dist, dist_t)

    max_tvd = max(tvd_reports.values()) if tvd_reports else Fraction(0, 1)
    non_signaling_satisfied = (max_tvd == Fraction(0, 1))

    return {
        "ensemble_size": len(ensemble),
        "cut_part_a": sorted(cut.part_a),
        "cut_part_b": sorted(cut.part_b),
        "observable_tested": observable_b.name,
        "interventions_tested": [t.name for t in interventions_a],
        "tvd_by_intervention": tvd_reports,
        "max_tvd": max_tvd,
        "non_signaling_satisfied": non_signaling_satisfied,
    }


def verify_leaky_intervention_divergence(
    ensemble: Sequence[CarrierState],
    cut: BipartiteCut,
    leaky_intervention: Transition,
    observable_b: Observable,
) -> Fraction:
    """Negative control: verify that when an intervention leaks across the cut,

    the marginal distribution shifts, yielding TVD > 0.
    """
    if not cut.is_cut_crossing(leaky_intervention):
        raise ValueError("Expected leaky_intervention to have a cut-crossing footprint")

    baseline_dist = compute_marginal_distribution(ensemble, observable_b)
    perturbed_ensemble = [leaky_intervention.apply(s) for s in ensemble]
    perturbed_dist = compute_marginal_distribution(perturbed_ensemble, observable_b)

    return total_variation_distance(baseline_dist, perturbed_dist)


def verify_mediated_coupling_divergence(
    ensemble: Sequence[CarrierState],
    cut: BipartiteCut,
    intervention_a: Transition,
    mediating_transition: Transition,
    observable_b: Observable,
) -> Fraction:
    """Negative control: verify that after a mediating coupling runs across the cut,

    an intervention in Part A becomes detectable in Part B, yielding TVD > 0.
    """
    if not cut.is_strictly_in_a(intervention_a):
        raise ValueError("intervention_a must be strictly in Part A")
    if not cut.is_cut_crossing(mediating_transition):
        raise ValueError("mediating_transition must cross the cut")

    # Baseline: mediating transition applied without intervention
    baseline_ensemble = [mediating_transition.apply(s) for s in ensemble]
    baseline_dist = compute_marginal_distribution(baseline_ensemble, observable_b)

    # Perturbed: intervention in A followed by mediating transition
    perturbed_ensemble = [
        mediating_transition.apply(intervention_a.apply(s)) for s in ensemble
    ]
    perturbed_dist = compute_marginal_distribution(perturbed_ensemble, observable_b)

    return total_variation_distance(baseline_dist, perturbed_dist)


@dataclass(frozen=True)
class DuplicateObserverPair:
    """Two identical embedded measurement instruments stationed at distinct carrier loci."""

    locus_u: str
    locus_v: str
    readout_probe: Callable[[int], int]

    def measure_u(self, state: CarrierState) -> int:
        return self.readout_probe(state[self.locus_u])

    def measure_v(self, state: CarrierState) -> int:
        return self.readout_probe(state[self.locus_v])

    def coincidence(self, state: CarrierState) -> bool:
        return self.measure_u(state) == self.measure_v(state)


def is_symmetric_state(state: CarrierState, automorphism: Mapping[str, str]) -> bool:
    """Check whether a carrier state is invariant under locus permutation."""
    for locus, val in state.values.items():
        mapped = automorphism.get(locus, locus)
        if state.get(mapped) != val:
            return False
    return True


def verify_duplicate_observer_agreement(
    ensemble: Sequence[CarrierState],
    observer_pair: DuplicateObserverPair,
    automorphism: Mapping[str, str],
) -> Dict[str, Any]:
    """Verify that duplicate observers at automorphism-related loci record 100% agreement

    on symmetric preparations, and that asymmetric preparations produce divergent readouts.
    """
    symmetric_agreements = 0
    symmetric_count = 0
    asymmetric_divergences = 0
    asymmetric_count = 0

    for s in ensemble:
        sym = is_symmetric_state(s, automorphism)
        agree = observer_pair.coincidence(s)
        if sym:
            symmetric_count += 1
            if agree:
                symmetric_agreements += 1
        else:
            asymmetric_count += 1
            if not agree:
                asymmetric_divergences += 1

    return {
        "total_states": len(ensemble),
        "symmetric_count": symmetric_count,
        "symmetric_agreement_rate": (
            Fraction(symmetric_agreements, symmetric_count)
            if symmetric_count > 0
            else Fraction(1, 1)
        ),
        "asymmetric_count": asymmetric_count,
        "asymmetric_divergence_rate": (
            Fraction(asymmetric_divergences, asymmetric_count)
            if asymmetric_count > 0
            else Fraction(0, 1)
        ),
        "duplicate_agreement_satisfied": (
            symmetric_agreements == symmetric_count and symmetric_count > 0
        ),
    }
