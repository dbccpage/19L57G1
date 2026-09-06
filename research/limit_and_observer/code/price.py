"""The one pricing routine, and the tie-retention harness.

Classification: metatheory apparatus.

Every demand is priced by this routine and no other.  It enumerates the space
at item count 0, 1, ... in order, keeps the satisfying candidates, returns at
the first count with a non-empty set, refines by the measure's later
coordinates, quotients by the canonical key of the **resulting** stated state,
retains every tied class with its capability vector, and decides
``cost_below_minimum_all_fail`` by exhaustion rather than by assertion — the
flag is computed from the item counts the walk actually exhausted, so
reordering the walk falsifies it instead of leaving it silently true.

The harness reproduces ``research/partial_decide``'s invariants, including the
one that matters: the classes must **partition** the raw minima.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .demands import Demand, Situation
from .enumerate_space import Bounds, CandidateBudgetRefused, iter_candidates
from .items import Delta, StatedState, capabilities, mu1, mu2
from .quotient import CanonKey, canonical_state, designated_pair
from .readers import induced_relation
from .regime import Pair, Regime


class GradeRefused(ValueError):
    """A grade was constructed violating one of its own invariants."""


@dataclass
class PricingTrace:
    """Actual completed levels and a replayable interrupted frontier, if any."""

    completed_levels: dict[int, int] = field(default_factory=dict)
    refused_level: int | None = None
    yielded_at_refusal: int = 0
    last_yielded: Delta | None = None
    first_refused: Delta | None = None
    reason: str | None = None
    observed_hits_at_refusal: dict[str, int] = field(default_factory=dict)
    first_witnesses_at_refusal: dict[str, Delta] = field(default_factory=dict)


@dataclass(frozen=True)
class ResponseClass:
    """One isomorphism class of minimum candidates."""

    key: CanonKey
    representative: Delta
    members: tuple[Delta, ...]
    capability_vector: dict[str, object]

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
    search_refused: bool = False
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
        return "Refused" if m.search_refused else "Empty"
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


def below_minimum_exhausted(
    empty_counts: int, found_at: Optional[int], max_items: int
) -> bool:
    """Whether every item count strictly below the reported minimum was
    enumerated **in full** and produced no satisfying candidate.

    This is the field ``cost_below_minimum_all_fail``, and it is decided from
    what the search actually did rather than asserted.  ``empty_counts`` is
    how many whole item counts the demand survived before it was answered;
    ``found_at`` is the count that answered it, or ``None`` when nothing did.

    It was a hard-coded ``True`` in both branches of the assembly, correct only
    by the accident that the walk happens to ascend, with no test able to catch
    a regression: reordering the enumeration left the receipt saying ``true``
    for every row.  Computing it from the walk is what makes a reordering
    falsify it."""
    if found_at is None:
        return empty_counts == max_items + 1
    return empty_counts == found_at


def price_many(
    base: Regime,
    reading: str,
    demands: "tuple[Demand, ...]",
    measures: tuple[str, ...],
    bounds: Bounds,
    prune: bool = True,
    trace: PricingTrace | None = None,
    retain_completed_on_refusal: bool = False,
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
    #: Whole item counts each demand survived with nothing satisfying it, and
    #: the count that answered it.  These two are what decide
    #: ``cost_below_minimum_all_fail``; nothing about the loop's direction is
    #: assumed by the decision.
    empty_counts: dict[str, int] = {d.name: 0 for d in demands}
    found_at: dict[str, Optional[int]] = {d.name: None for d in demands}
    refused = False
    for total in range(0, bounds.max_items + 1):
        if not pending:
            break
        hits: dict[str, list[tuple[Delta, StatedState]]] = {
            name: [] for name in pending
        }
        yielded = 0
        last_delta = None
        try:
            for delta, state in iter_candidates(base, total, bounds, prune):
                yielded += 1
                last_delta = delta
                sit = Situation(base, delta, state, designated, bounds.w_max)
                for name, d in pending.items():
                    if d.predicate(sit):
                        hits[name].append((delta, state))
        except CandidateBudgetRefused as error:
            if trace is not None:
                trace.refused_level = total
                trace.yielded_at_refusal = yielded
                trace.last_yielded = last_delta
                trace.first_refused = error.candidate
                trace.reason = str(error)
                trace.observed_hits_at_refusal = {name: len(v) for name, v in hits.items()}
                trace.first_witnesses_at_refusal = {
                    name: v[0][0] for name, v in hits.items() if v
                }
            if not retain_completed_on_refusal:
                raise
            refused = True
            # Nothing from the interrupted level is a complete minimum/tie
            # certificate. Only earlier, fully completed levels survive.
            break
        if trace is not None:
            trace.completed_levels[total] = yielded
        for name in list(pending):
            if hits[name]:
                found[name] = hits[name]
                found_at[name] = total
                del pending[name]
            else:
                empty_counts[name] += 1

    out: dict[tuple[str, str], Minimum] = {}
    for d in demands:
        for measure in measures:
            out[(d.name, measure)] = _assemble(
                d, reading, measure, bounds, designated,
                found.get(d.name, []),
                below_minimum_exhausted(
                    empty_counts[d.name], found_at[d.name], bounds.max_items
                ),
                search_refused=refused and found_at[d.name] is None,
            )
    return out


def _assemble(
    demand: Demand,
    reading: str,
    measure: str,
    bounds: Bounds,
    designated: Optional[Pair],
    hits: list[tuple[Delta, StatedState]],
    exhausted: bool,
    search_refused: bool = False,
) -> "Minimum":
    """Turn the satisfying candidates at the first successful item count into
    a graded, quotiented ``Minimum``.

    ``exhausted`` is computed by the caller from the walk and is not decided
    here; see ``below_minimum_exhausted``."""
    if not hits:
        return Minimum(
            demand=demand.name,
            evidence_arity=demand.evidence_arity,
            base_reading=reading,
            measure=measure,
            cost=(-1, -1),
            raw_minima=(),
            classes=(),
            cost_below_minimum_all_fail=exhausted,
            complete_within=bounds,
            designated=designated,
            search_refused=search_refused,
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
        cost_below_minimum_all_fail=exhausted,
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
