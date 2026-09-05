"""The one pricing routine, and the tie-retention harness.

Classification: metatheory apparatus.

Every demand is priced by this routine and no other.  It enumerates the space
at item count 0, 1, ... in order, keeps the satisfying candidates, returns at
the first count with a non-empty set, refines by the measure's later
coordinates, quotients by the canonical key of the **resulting** stated state,
retains every tied class with its capability vector, and decides
``cost_below_minimum_all_fail`` by exhaustion rather than by assertion.

The harness reproduces ``research/partial_decide``'s invariants, including the
one that matters: the classes must **partition** the raw minima.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .demands import Demand, Situation
from .enumerate_space import Bounds, iter_candidates
from .items import Delta, StatedState, capabilities, mu1, mu2
from .quotient import CanonKey, canonical_state, designated_pair
from .readers import induced_relation
from .regime import Pair, Regime


class GradeRefused(ValueError):
    """A grade was constructed violating one of its own invariants."""


@dataclass(frozen=True)
class ResponseClass:
    """One isomorphism class of minimum candidates."""

    key: CanonKey
    representative: Delta
    members: tuple[Delta, ...]
    capability_vector: dict[str, int]

    def __post_init__(self) -> None:
        if not self.members:
            raise GradeRefused("a response class is never empty")
        if len(set(self.members)) != len(self.members):
            raise GradeRefused("a response class holds no duplicate")
        if self.representative not in self.members:
            raise GradeRefused("the representative is a member")
        if tuple(sorted(self.members, key=str)) != self.members:
            raise GradeRefused("members are in deterministic sorted order")


@dataclass(frozen=True)
class Minimum:
    """The output of the pricing routine for one demand at one base."""

    demand: str
    evidence_arity: str
    base_reading: str
    measure: str
    cost: tuple[int, int]
    raw_minima: tuple[Delta, ...]
    classes: tuple[ResponseClass, ...]
    cost_below_minimum_all_fail: bool
    complete_within: Bounds
    designated: Optional[Pair]
    #: How many *genuinely different* readers the minima buy, counted by the
    #: induced separation relation rather than by syntax.  The class count
    #: above is the canonical-key count and is deliberately finer: two readers
    #: agreeing at this state may differ at another, so they are not one
    #: admitted object.  Both are reported; neither is presented as the other.
    distinct_induced_relations: int = 0
    grade: str = field(default="")

    def __post_init__(self) -> None:
        if len(set(self.raw_minima)) != len(self.raw_minima):
            raise GradeRefused("raw minima hold no duplicate")
        if tuple(sorted(self.raw_minima, key=str)) != self.raw_minima:
            raise GradeRefused("raw minima are in deterministic sorted order")
        keys = [c.key for c in self.classes]
        if len(set(keys)) != len(keys):
            raise GradeRefused("response classes have distinct keys")
        covered: list[Delta] = []
        for c in self.classes:
            covered.extend(c.members)
        if tuple(sorted(covered, key=str)) != self.raw_minima:
            raise GradeRefused(
                "the response classes must partition the raw minima"
            )
        object.__setattr__(self, "grade", _grade(self))


def _grade(m: Minimum) -> str:
    if not m.raw_minima:
        return "Empty"
    if len(m.raw_minima) == 1:
        return "UniqueDelta"
    if len(m.classes) == 1:
        return "UniqueClass"
    return "Tie"


def _with_imposed(s: StatedState, demand: Demand) -> StatedState:
    """Apply the demand's imposed requirement before the quotient is taken.

    A requirement is part of the child's structure, so it constrains which
    bijections preserve it.  Omitting it makes the quotient strictly coarser
    than the sealed one, which the calibration catches."""
    if demand.impose is None:
        return s
    from .regime import Impose, step

    return StatedState(
        step(s.regime, Impose(demand.impose[0], demand.impose[1])), s.readers
    )


def _measure_value(measure: str, delta: Delta) -> tuple[int, int]:
    if measure == "mu1":
        return (mu1(delta), -1)
    if measure == "mu2":
        return mu2(delta)
    raise ValueError(f"unknown measure: {measure}")


def price_many(
    base: Regime,
    reading: str,
    demands: "tuple[Demand, ...]",
    measures: tuple[str, ...],
    bounds: Bounds,
    prune: bool = True,
) -> dict[tuple[str, str], "Minimum"]:
    """Price several demands at one base, enumerating the space once.

    This is the one pricing routine.  The demands are parameters and never
    branches: every one of them sees the same enumeration, the same bounds and
    the same measures, so no demand can acquire an enumerator, a bound or a
    measure of its own.  Enumerating once rather than once per demand changes
    nothing about what is searched; ``tests/test_price.py`` asserts that the
    single-demand wrapper and this routine agree.
    """
    from .grammar import collapsed_pairs

    designated = designated_pair(base, collapsed_pairs(base))
    pending = {d.name: d for d in demands}
    found: dict[str, list[tuple[Delta, StatedState]]] = {}
    for total in range(0, bounds.max_items + 1):
        if not pending:
            break
        hits: dict[str, list[tuple[Delta, StatedState]]] = {
            name: [] for name in pending
        }
        for delta, state in iter_candidates(base, total, bounds, prune):
            sit = Situation(base, delta, state, designated, bounds.w_max)
            for name, d in pending.items():
                if d.predicate(sit):
                    hits[name].append((delta, state))
        for name in list(pending):
            if hits[name]:
                found[name] = hits[name]
                del pending[name]

    out: dict[tuple[str, str], Minimum] = {}
    for d in demands:
        for measure in measures:
            out[(d.name, measure)] = _assemble(
                d, reading, measure, bounds, designated, found.get(d.name, [])
            )
    return out


def _assemble(
    demand: Demand,
    reading: str,
    measure: str,
    bounds: Bounds,
    designated: Optional[Pair],
    hits: list[tuple[Delta, StatedState]],
) -> "Minimum":
    """Turn the satisfying candidates at the first successful item count into
    a graded, quotiented ``Minimum``."""
    if not hits:
        return Minimum(
            demand=demand.name,
            evidence_arity=demand.evidence_arity,
            base_reading=reading,
            measure=measure,
            cost=(-1, -1),
            raw_minima=(),
            classes=(),
            cost_below_minimum_all_fail=True,
            complete_within=bounds,
            designated=designated,
        )
    best = min(_measure_value(measure, d) for d, _ in hits)
    chosen = [(d, s) for (d, s) in hits if _measure_value(measure, d) == best]
    raw = tuple(sorted({d for d, _ in chosen}, key=str))
    groups: dict[CanonKey, list[Delta]] = {}
    for d, s in chosen:
        groups.setdefault(
            canonical_state(_with_imposed(s, demand), bounds.bijection_budget),
            [],
        ).append(d)
    classes = tuple(
        ResponseClass(
            key=k,
            representative=min(set(v), key=str),
            members=tuple(sorted(set(v), key=str)),
            capability_vector=capabilities(min(set(v), key=str)),
        )
        for k, v in sorted(groups.items(), key=lambda kv: str(kv[0]))
    )
    relations = {
        frozenset(
            induced_relation(_with_imposed(s, demand).regime, rho)
            for rho in s.readers
        )
        for _, s in chosen
    }
    return Minimum(
        demand=demand.name,
        evidence_arity=demand.evidence_arity,
        base_reading=reading,
        measure=measure,
        cost=best,
        raw_minima=raw,
        classes=classes,
        cost_below_minimum_all_fail=True,
        complete_within=bounds,
        designated=designated,
        distinct_induced_relations=len(relations),
    )


def price(
    base: Regime,
    reading: str,
    demand: Demand,
    measure: str,
    bounds: Bounds,
    prune: bool = True,
) -> "Minimum":
    """Price one demand at one base under one measure.

    A thin wrapper over ``price_many``.  ``raw_minima`` is empty exactly when
    no candidate within the declared bound satisfies the demand.  An empty set
    is **not** an obstruction by itself; it is reported OPEN unless a proof and
    a positive control accompany it."""
    return price_many(base, reading, (demand,), (measure,), bounds, prune)[
        (demand.name, measure)
    ]


def satisfies_at(
    base: Regime, delta: Delta, demand: Demand, bounds: Bounds
) -> bool:
    """Whether one candidate satisfies one demand at one base.

    Used by the purchase test, so that "does either buy the other" is decided
    by running each demand's predicate on the other's retained minima rather
    than inferred from equal cost — which is exactly the inference a shared
    measure invites."""
    from .grammar import collapsed_pairs
    from .items import apply_delta
    from .regime import AdmissionRefused

    try:
        state = apply_delta(
            StatedState(base, ()), delta, bounds.w_max, bounds.max_readers
        )
    except AdmissionRefused:
        return False
    designated = designated_pair(base, collapsed_pairs(base))
    return demand.predicate(
        Situation(base, delta, state, designated, bounds.w_max)
    )
