"""Operational Valuations and Convex State Spaces (Target P204).

Exact rational implementation of:
1. Discrete outcome spaces and operational state distributions.
2. Operational effects and state-effect valuation pairing.
3. Unit effect and normalization invariance.
4. Convex combinations of preparations and bilinearity.
5. Characterization of extreme states vs mixed states.
6. Classical simplex state spaces (unique extreme decomposition) vs
   general convex state spaces (non-unique extreme decompositions).
7. Tensor product composition and operational non-signaling across bipartite cuts.

AuthorityEffect: None.
Axiom Scope: Exact rational arithmetic with fractions.Fraction.
Vocabulary Firewall: No watched terms; strict claim hygiene.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from fractions import Fraction
from typing import Any, TypeVar

T = TypeVar("T")


def _exact_q(val: object) -> Fraction:
    """Convert int/Fraction to Q. Refuse float stand-ins for claimed exact rationals."""
    if isinstance(val, float):
        raise TypeError("float is not exact Q; pass Fraction or int")
    if isinstance(val, Fraction):
        return val
    if isinstance(val, int):
        return Fraction(val, 1)
    raise TypeError(f"Unsupported exact-Q conversion: {type(val)}")


class OutcomeSpace:
    """Finite discrete outcome space Omega."""

    def __init__(self, outcomes: Iterable[Any]) -> None:
        raw = tuple(outcomes)
        if not raw:
            raise ValueError("Outcome space must be non-empty.")
        if len(set(raw)) != len(raw):
            raise ValueError("Outcomes must be distinct.")
        self._outcomes = raw
        self._index_map = {item: i for i, item in enumerate(raw)}

    @property
    def outcomes(self) -> tuple[Any, ...]:
        return self._outcomes

    @property
    def dim(self) -> int:
        return len(self._outcomes)

    def index(self, outcome: Any) -> int:
        if outcome not in self._index_map:
            raise KeyError(f"Outcome {outcome!r} not in space.")
        return self._index_map[outcome]

    def contains(self, outcome: Any) -> bool:
        return outcome in self._index_map

    def __len__(self) -> int:
        return len(self._outcomes)

    def __iter__(self):
        return iter(self._outcomes)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OutcomeSpace):
            return False
        return self._outcomes == other._outcomes

    def __hash__(self) -> int:
        return hash(self._outcomes)

    def __repr__(self) -> str:
        return f"OutcomeSpace({list(self._outcomes)!r})"


class OperationalState:
    """Operational preparation represented as an exact rational distribution on Omega."""

    def __init__(
        self,
        space: OutcomeSpace,
        distribution: Mapping[Any, Fraction | int],
    ) -> None:
        self._space = space
        dist: dict[Any, Fraction] = {}
        total = Fraction(0, 1)

        for out in space.outcomes:
            val = distribution.get(out, 0)
            frac = _exact_q(val)
            if frac < Fraction(0, 1):
                raise ValueError(f"Negative probability {frac} on outcome {out!r}.")
            if frac > Fraction(1, 1):
                raise ValueError(f"Probability {frac} exceeds 1 on outcome {out!r}.")
            dist[out] = frac
            total += frac

        if total != Fraction(1, 1):
            raise ValueError(f"State probabilities sum to {total}, expected 1.")

        self._dist = dist
        self._vector = tuple(dist[out] for out in space.outcomes)

    @property
    def space(self) -> OutcomeSpace:
        return self._space

    @property
    def vector(self) -> tuple[Fraction, ...]:
        return self._vector

    def probability(self, outcome: Any) -> Fraction:
        if not self._space.contains(outcome):
            raise KeyError(f"Outcome {outcome!r} not in space.")
        return self._dist[outcome]

    def evaluate(self, effect: OperationalEffect) -> Fraction:
        return evaluate(effect, self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OperationalState):
            return False
        return self._space == other._space and self._vector == other._vector

    def __hash__(self) -> int:
        return hash((self._space, self._vector))

    def __repr__(self) -> str:
        items = ", ".join(f"{k!r}: {v}" for k, v in self._dist.items())
        return f"OperationalState({{{items}}})"


class OperationalEffect:
    """Operational effect assigning response probabilities in [0, 1] to outcomes."""

    def __init__(
        self,
        space: OutcomeSpace,
        weights: Mapping[Any, Fraction | int],
    ) -> None:
        self._space = space
        w_dict: dict[Any, Fraction] = {}

        for out in space.outcomes:
            val = weights.get(out, 0)
            frac = _exact_q(val)
            if frac < Fraction(0, 1) or frac > Fraction(1, 1):
                raise ValueError(
                    f"Effect weight {frac} on outcome {out!r} outside [0, 1]."
                )
            w_dict[out] = frac

        self._weights = w_dict
        self._vector = tuple(w_dict[out] for out in space.outcomes)

    @property
    def space(self) -> OutcomeSpace:
        return self._space

    @property
    def vector(self) -> tuple[Fraction, ...]:
        return self._vector

    def weight(self, outcome: Any) -> Fraction:
        if not self._space.contains(outcome):
            raise KeyError(f"Outcome {outcome!r} not in space.")
        return self._weights[outcome]

    def evaluate(self, state: OperationalState) -> Fraction:
        return evaluate(self, state)

    def complement(self) -> OperationalEffect:
        """Return the complement effect u - e."""
        comp_weights = {out: Fraction(1, 1) - w for out, w in self._weights.items()}
        return OperationalEffect(self._space, comp_weights)

    @classmethod
    def unit_effect(cls, space: OutcomeSpace) -> OperationalEffect:
        """Unit effect u assigning weight 1 to every outcome."""
        return cls(space, {out: Fraction(1, 1) for out in space.outcomes})

    @classmethod
    def zero_effect(cls, space: OutcomeSpace) -> OperationalEffect:
        """Zero effect assigning weight 0 to every outcome."""
        return cls(space, {out: Fraction(0, 1) for out in space.outcomes})

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OperationalEffect):
            return False
        return self._space == other._space and self._vector == other._vector

    def __hash__(self) -> int:
        return hash((self._space, self._vector))

    def __repr__(self) -> str:
        items = ", ".join(f"{k!r}: {v}" for k, v in self._weights.items())
        return f"OperationalEffect({{{items}}})"


def evaluate(effect: OperationalEffect, state: OperationalState) -> Fraction:
    """Operational valuation pairing <e, s> = sum_omega e(omega) * s(omega)."""
    if effect.space != state.space:
        raise ValueError("Cannot evaluate effect and state over distinct spaces.")
    val = sum(
        (effect.weight(out) * state.probability(out) for out in state.space.outcomes),
        Fraction(0, 1),
    )
    return val


def deterministic_state(space: OutcomeSpace, outcome: Any) -> OperationalState:
    """Deterministic indicator state concentrated on a single outcome."""
    dist = {out: Fraction(1, 1) if out == outcome else Fraction(0, 1) for out in space.outcomes}
    return OperationalState(space, dist)


def convex_combination_states(
    weights: Sequence[Fraction | int],
    states: Sequence[OperationalState],
) -> OperationalState:
    """Convex mixture of preparation states sum_i p_i * s_i with sum_i p_i = 1, p_i >= 0."""
    if len(weights) != len(states):
        raise ValueError("Lengths of weights and states must match.")
    if not states:
        raise ValueError("Cannot form empty mixture.")

    space = states[0].space
    frac_weights = [_exact_q(w) for w in weights]

    total_w = Fraction(0, 1)
    for w in frac_weights:
        if w < Fraction(0, 1):
            raise ValueError(f"Negative convex weight {w}.")
        total_w += w
    if total_w != Fraction(1, 1):
        raise ValueError(f"Weights sum to {total_w}, expected 1.")

    for s in states:
        if s.space != space:
            raise ValueError("All states in mixture must share identical space.")

    mixed_dist: dict[Any, Fraction] = {out: Fraction(0, 1) for out in space.outcomes}
    for w, s in zip(frac_weights, states):
        for out in space.outcomes:
            mixed_dist[out] += w * s.probability(out)

    return OperationalState(space, mixed_dist)


def convex_combination_effects(
    weights: Sequence[Fraction | int],
    effects: Sequence[OperationalEffect],
) -> OperationalEffect:
    """Convex mixture of effects sum_j q_j * e_j with sum_j q_j = 1, q_j >= 0."""
    if len(weights) != len(effects):
        raise ValueError("Lengths of weights and effects must match.")
    if not effects:
        raise ValueError("Cannot form empty effect mixture.")

    space = effects[0].space
    frac_weights = [_exact_q(w) for w in weights]

    total_w = Fraction(0, 1)
    for w in frac_weights:
        if w < Fraction(0, 1):
            raise ValueError(f"Negative convex weight {w}.")
        total_w += w
    if total_w != Fraction(1, 1):
        raise ValueError(f"Weights sum to {total_w}, expected 1.")

    for e in effects:
        if e.space != space:
            raise ValueError("All effects in mixture must share identical space.")

    mixed_weights: dict[Any, Fraction] = {out: Fraction(0, 1) for out in space.outcomes}
    for w, e in zip(frac_weights, effects):
        for out in space.outcomes:
            mixed_weights[out] += w * e.weight(out)

    return OperationalEffect(space, mixed_weights)


def verify_bilinearity(
    state_weights: Sequence[Fraction | int],
    states: Sequence[OperationalState],
    effect_weights: Sequence[Fraction | int],
    effects: Sequence[OperationalEffect],
) -> bool:
    """Verify operational bilinearity:

    <sum_j q_j e_j, sum_i p_i s_i> = sum_{j, i} q_j * p_i * <e_j, s_i>.
    """
    mixed_state = convex_combination_states(state_weights, states)
    mixed_effect = convex_combination_effects(effect_weights, effects)

    left_eval = evaluate(mixed_effect, mixed_state)

    right_eval = Fraction(0, 1)
    for q, e in zip(effect_weights, effects):
        fq = _exact_q(q)
        for p, s in zip(state_weights, states):
            fp = _exact_q(p)
            right_eval += fq * fp * evaluate(e, s)

    return left_eval == right_eval


class ClassicalSimplex:
    """Classical discrete simplex over a finite outcome space Omega.

    Every normalized state has a unique decomposition into extreme states.
    """

    def __init__(self, space: OutcomeSpace) -> None:
        self._space = space
        self._extreme_states = tuple(
            deterministic_state(space, out) for out in space.outcomes
        )

    @property
    def space(self) -> OutcomeSpace:
        return self._space

    @property
    def extreme_states(self) -> tuple[OperationalState, ...]:
        return self._extreme_states

    def decompose(
        self, state: OperationalState
    ) -> dict[OperationalState, Fraction]:
        """Return the canonical decomposition into extreme indicator states."""
        if state.space != self._space:
            raise ValueError("State space mismatch.")
        result: dict[OperationalState, Fraction] = {}
        for ext in self._extreme_states:
            # The extreme state is concentrated at exactly one outcome
            # Identify which outcome has probability 1
            out = next(o for o in self._space.outcomes if ext.probability(o) == Fraction(1, 1))
            weight = state.probability(out)
            result[ext] = weight
        return result

    def is_unique_decomposition(
        self,
        state: OperationalState,
        candidate_weights: Sequence[Fraction | int],
    ) -> bool:
        """Check if candidate convex weights over extreme states match canonical decomposition."""
        if len(candidate_weights) != len(self._extreme_states):
            return False
        candidate = [_exact_q(w) for w in candidate_weights]
        if sum(candidate) != Fraction(1, 1) or any(w < Fraction(0, 1) for w in candidate):
            return False
        canonical = [state.probability(out) for out in self._space.outcomes]
        return candidate == canonical


class SquareStateSpace:
    """General convex state space (discrete square) with non-unique extreme decompositions.

    Subspace of states on Omega = (0, 1, 2, 3) spanned by 4 extreme states:
      v1 = (1/2, 0, 1/2, 0)
      v2 = (0, 1/2, 1/2, 0)
      v3 = (0, 1/2, 0, 1/2)
      v4 = (1/2, 0, 0, 1/2)

    The center state s_c = (1/4, 1/4, 1/4, 1/4) admits two distinct decompositions:
      s_c = 1/2 * v1 + 1/2 * v3
      s_c = 1/2 * v2 + 1/2 * v4
    """

    def __init__(self) -> None:
        self._space = OutcomeSpace((0, 1, 2, 3))
        self._v1 = OperationalState(
            self._space,
            {0: Fraction(1, 2), 1: Fraction(0, 1), 2: Fraction(1, 2), 3: Fraction(0, 1)},
        )
        self._v2 = OperationalState(
            self._space,
            {0: Fraction(0, 1), 1: Fraction(1, 2), 2: Fraction(1, 2), 3: Fraction(0, 1)},
        )
        self._v3 = OperationalState(
            self._space,
            {0: Fraction(0, 1), 1: Fraction(1, 2), 2: Fraction(0, 1), 3: Fraction(1, 2)},
        )
        self._v4 = OperationalState(
            self._space,
            {0: Fraction(1, 2), 1: Fraction(0, 1), 2: Fraction(0, 1), 3: Fraction(1, 2)},
        )
        self._extreme_states = (self._v1, self._v2, self._v3, self._v4)
        self._center_state = OperationalState(
            self._space,
            {0: Fraction(1, 4), 1: Fraction(1, 4), 2: Fraction(1, 4), 3: Fraction(1, 4)},
        )

    @property
    def space(self) -> OutcomeSpace:
        return self._space

    @property
    def extreme_states(self) -> tuple[OperationalState, ...]:
        return self._extreme_states

    @property
    def center_state(self) -> OperationalState:
        return self._center_state

    def decomposition_diagonal_1(self) -> tuple[tuple[Fraction, ...], OperationalState]:
        """Decomposition: 1/2 * v1 + 1/2 * v3."""
        weights = (Fraction(1, 2), Fraction(0, 1), Fraction(1, 2), Fraction(0, 1))
        mixed = convex_combination_states(weights, self._extreme_states)
        return weights, mixed

    def decomposition_diagonal_2(self) -> tuple[tuple[Fraction, ...], OperationalState]:
        """Decomposition: 1/2 * v2 + 1/2 * v4."""
        weights = (Fraction(0, 1), Fraction(1, 2), Fraction(0, 1), Fraction(1, 2))
        mixed = convex_combination_states(weights, self._extreme_states)
        return weights, mixed

    def demonstrates_non_unique_decomposition(self) -> bool:
        """Check that two distinct weight distributions produce identical center state."""
        w1, s1 = self.decomposition_diagonal_1()
        w2, s2 = self.decomposition_diagonal_2()
        weights_distinct = w1 != w2
        states_equal = s1 == s2 == self._center_state
        return weights_distinct and states_equal


def tensor_outcome_space(
    space_a: OutcomeSpace, space_b: OutcomeSpace
) -> OutcomeSpace:
    """Composite outcome space Omega_A x Omega_B with pair outcomes (a, b)."""
    product_outcomes = tuple((a, b) for a in space_a.outcomes for b in space_b.outcomes)
    return OutcomeSpace(product_outcomes)


def tensor_product_states(
    state_a: OperationalState, state_b: OperationalState
) -> OperationalState:
    """Tensor product state s_A (x) s_B with s_AB(a, b) = s_A(a) * s_B(b)."""
    comp_space = tensor_outcome_space(state_a.space, state_b.space)
    dist = {
        (a, b): state_a.probability(a) * state_b.probability(b)
        for a in state_a.space.outcomes
        for b in state_b.space.outcomes
    }
    return OperationalState(comp_space, dist)


def tensor_product_effects(
    effect_a: OperationalEffect, effect_b: OperationalEffect
) -> OperationalEffect:
    """Tensor product effect e_A (x) e_B with e_AB(a, b) = e_A(a) * e_B(b)."""
    comp_space = tensor_outcome_space(effect_a.space, effect_b.space)
    weights = {
        (a, b): effect_a.weight(a) * effect_b.weight(b)
        for a in effect_a.space.outcomes
        for b in effect_b.space.outcomes
    }
    return OperationalEffect(comp_space, weights)


def marginal_state_a(
    state_ab: OperationalState, space_a: OutcomeSpace, space_b: OutcomeSpace
) -> OperationalState:
    """Partial trace / marginal reduction to Subsystem A: s_A(a) = sum_b s_AB(a, b)."""
    dist: dict[Any, Fraction] = {a: Fraction(0, 1) for a in space_a.outcomes}
    for a in space_a.outcomes:
        for b in space_b.outcomes:
            dist[a] += state_ab.probability((a, b))
    return OperationalState(space_a, dist)


def marginal_state_b(
    state_ab: OperationalState, space_a: OutcomeSpace, space_b: OutcomeSpace
) -> OperationalState:
    """Partial trace / marginal reduction to Subsystem B: s_B(b) = sum_a s_AB(a, b)."""
    dist: dict[Any, Fraction] = {b: Fraction(0, 1) for b in space_b.outcomes}
    for b in space_b.outcomes:
        for a in space_a.outcomes:
            dist[b] += state_ab.probability((a, b))
    return OperationalState(space_b, dist)


def verify_non_signaling_across_cut(
    state_ab: OperationalState,
    space_a: OutcomeSpace,
    space_b: OutcomeSpace,
    measurement_effects_a: Sequence[OperationalEffect],
    test_effect_b: OperationalEffect,
) -> dict[str, Any]:
    """Verify operational non-signaling across bipartite cut A | B.

    When measurement_effects_a forms an operational partition of unity on A:
      sum_i e_{A, i} = u_A
    then for any effect e_B on B:
      sum_i <e_{A, i} (x) e_B, s_AB> = <u_A (x) e_B, s_AB> = <e_B, s_B>.
    """
    unit_a = OperationalEffect.unit_effect(space_a)

    # Verify partition of unity on A
    summed_weights_a = {out: Fraction(0, 1) for out in space_a.outcomes}
    for eff_a in measurement_effects_a:
        if eff_a.space != space_a:
            raise ValueError("Measurement effect not on space A.")
        for out in space_a.outcomes:
            summed_weights_a[out] += eff_a.weight(out)

    is_partition = all(summed_weights_a[out] == Fraction(1, 1) for out in space_a.outcomes)
    if not is_partition:
        raise ValueError("Measurement effects on A do not sum to unit effect.")

    # 1. Evaluate sum_i <e_{A, i} (x) e_B, s_AB>
    summed_eval = Fraction(0, 1)
    for eff_a in measurement_effects_a:
        joint_eff = tensor_product_effects(eff_a, test_effect_b)
        summed_eval += evaluate(joint_eff, state_ab)

    # 2. Evaluate <u_A (x) e_B, s_AB>
    unit_joint = tensor_product_effects(unit_a, test_effect_b)
    unit_eval = evaluate(unit_joint, state_ab)

    # 3. Evaluate <e_B, s_B> on marginal state
    s_b = marginal_state_b(state_ab, space_a, space_b)
    marginal_eval = evaluate(test_effect_b, s_b)

    non_signaling = (summed_eval == unit_eval == marginal_eval)
    return {
        "non_signaling": non_signaling,
        "summed_eval": summed_eval,
        "unit_eval": unit_eval,
        "marginal_eval": marginal_eval,
    }
