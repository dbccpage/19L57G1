"""Declared SearchPolicy: a subset of retained iso-class keys.

AuthorityEffect: None.

Input is the sealed retained iso-class key set.  Output is a subset.
Every retained class is recorded explored, pruned, or open, and
explored + pruned + open equals the tie-set size.  A key absent from
the sealed quotient is refused.  A silent drop of a retained class
fails the census.  Selection is a declared subset, not a necessity
claim.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from fractions import Fraction
from typing import Any


def _exact_q(val: object) -> Fraction:
    """Convert int/Fraction/rational-str to Q. Refuse float stand-ins."""
    if isinstance(val, float):
        raise TypeError("float is not exact Q; pass Fraction, int, or rational str")
    if isinstance(val, Fraction):
        return val
    if isinstance(val, int):
        return Fraction(val, 1)
    if isinstance(val, str):
        return Fraction(val)
    raise TypeError(f"Unsupported exact-Q conversion: {type(val)}")

from derivation.iso import CanonKey

from harness import HarnessError


class FabricatedClassError(HarnessError):
    """A class key absent from the sealed retained set is refused."""


class CensusError(HarnessError):
    """explored + pruned + open must partition the retained set."""


@dataclass(frozen=True)
class PolicyCensus:
    """Partition of one retained tie set."""

    explored: tuple[CanonKey, ...]
    pruned: tuple[CanonKey, ...]
    open_keys: tuple[CanonKey, ...]
    tie_set_size: int

    def __post_init__(self) -> None:
        total = len(self.explored) + len(self.pruned) + len(self.open_keys)
        if total != self.tie_set_size:
            raise CensusError(
                "explored+pruned+open must equal the tie-set size"
            )


@dataclass(frozen=True)
class SearchPolicy:
    """Declared authorizer.  Output keys are a subset of ``retained``."""

    policy_id: str
    justification: str
    retained: tuple[CanonKey, ...]
    explored: tuple[CanonKey, ...]
    pruned: tuple[CanonKey, ...]
    open_keys: tuple[CanonKey, ...]

    def subset(self) -> tuple[CanonKey, ...]:
        """Authorized keys: the explored bucket, checked as a subset."""
        return record_census(
            self.retained, self.explored, self.pruned, self.open_keys
        ).explored

    def census(self) -> PolicyCensus:
        return record_census(
            self.retained, self.explored, self.pruned, self.open_keys
        )


def record_census(
    retained: tuple[CanonKey, ...],
    explored: tuple[CanonKey, ...],
    pruned: tuple[CanonKey, ...],
    open_keys: tuple[CanonKey, ...],
) -> PolicyCensus:
    """Require a disjoint cover of ``retained``.  Name extras and drops."""
    retained_set = frozenset(retained)
    if len(retained_set) != len(retained):
        raise CensusError("retained keys must be distinct")
    buckets = {
        "explored": explored,
        "pruned": pruned,
        "open": open_keys,
    }
    seen: set[CanonKey] = set()
    extras: list[CanonKey] = []
    for name, keys in buckets.items():
        del name
        if len(set(keys)) != len(keys):
            raise CensusError("census buckets cannot duplicate a key")
        for key in keys:
            if key not in retained_set:
                extras.append(key)
            if key in seen:
                raise CensusError("census buckets must be disjoint")
            seen.add(key)
    if extras:
        raise FabricatedClassError(
            "class key absent from the sealed quotient"
        )
    missing = retained_set - seen
    if missing:
        raise CensusError("silent drop of a retained class")
    return PolicyCensus(
        explored=tuple(sorted(explored)),
        pruned=tuple(sorted(pruned)),
        open_keys=tuple(sorted(open_keys)),
        tie_set_size=len(retained),
    )


class _PriorityScoreKey:
    """Deterministic comparator for score ranking with canonical tie-breaking."""

    __slots__ = ("score", "key")

    def __init__(self, score: Any, key: CanonKey) -> None:
        self.score: Any = score
        self.key: CanonKey = key

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, _PriorityScoreKey):
            return NotImplemented
        if self.score != other.score:
            return bool(self.score > other.score)
        return bool(self.key < other.key)


def declared_explore_first(retained: tuple[CanonKey, ...]) -> SearchPolicy:
    """Declared subset: first key in sealed-key order; remainder open."""
    ordered = tuple(sorted(retained))
    explored = ordered[:1]
    open_keys = ordered[1:]
    pruned: tuple[CanonKey, ...] = ()
    census = record_census(ordered, explored, pruned, open_keys)
    return SearchPolicy(
        policy_id="declared-first-key-explored",
        justification=(
            "declared subset: explore the first retained key in "
            "sealed-key order; leave the rest open; prune none"
        ),
        retained=ordered,
        explored=census.explored,
        pruned=census.pruned,
        open_keys=census.open_keys,
    )


def declared_bounded_priority(
    retained: tuple[CanonKey, ...],
    bound: int = 1,
    *,
    priority_fn: Callable[[CanonKey], Any] | None = None,
    score_fn: Callable[[CanonKey], Any] | None = None,
    policy_id: str = "declared-bounded-priority",
    justification: str | None = None,
) -> SearchPolicy:
    """Declared subset: top-bound keys in priority order; remainder open.

    Keys are ordered by priority_fn or score_fn descending if provided, with
    ties broken in sealed canonical key order. When bound <= 0, no keys are
    explored. Census invariance is verified via record_census.
    """
    if bound < 0:
        raise ValueError("bound cannot be negative")
    ordered = tuple(sorted(retained))
    fn = priority_fn if priority_fn is not None else score_fn
    if fn is not None:
        ranked = tuple(
            sorted(ordered, key=lambda k: _PriorityScoreKey(fn(k), k))
        )
    else:
        ranked = ordered

    limit = min(bound, len(ranked))
    explored = ranked[:limit]
    explored_set = set(explored)
    open_keys = tuple(k for k in ordered if k not in explored_set)
    pruned: tuple[CanonKey, ...] = ()

    census = record_census(ordered, explored, pruned, open_keys)
    desc = justification or (
        f"declared bounded priority: explore up to {bound} retained keys "
        "in declared priority order; leave remainder open; prune none"
    )
    return SearchPolicy(
        policy_id=policy_id,
        justification=desc,
        retained=ordered,
        explored=census.explored,
        pruned=census.pruned,
        open_keys=census.open_keys,
    )


def declared_constraint_pruned(
    retained: tuple[CanonKey, ...],
    *,
    predicate: Callable[[CanonKey], bool] | None = None,
    pruned_keys: Iterable[CanonKey] | None = None,
    bound: int | None = None,
    prune_if: bool = True,
    policy_id: str = "declared-constraint-pruned",
    justification: str | None = None,
) -> SearchPolicy:
    """Declared subset: prune keys via constraint predicate; explore up to bound viable keys.

    If pruned_keys is given directly, those keys are designated pruned.
    Otherwise, if predicate is provided, a key k is pruned when
    bool(predicate(k)) == prune_if.
    Viable keys (non-pruned) are explored up to bound (all viable if bound is None),
    with any remaining viable keys left open.
    Census invariance is verified via record_census.
    """
    if bound is not None and bound < 0:
        raise ValueError("bound cannot be negative")
    ordered = tuple(sorted(retained))

    if pruned_keys is not None:
        pruned_tuple = tuple(pruned_keys)
        pruned_set = set(pruned_tuple)
        viable = tuple(k for k in ordered if k not in pruned_set)
    elif predicate is not None:
        pruned_list: list[CanonKey] = []
        viable_list: list[CanonKey] = []
        for k in ordered:
            if bool(predicate(k)) == prune_if:
                pruned_list.append(k)
            else:
                viable_list.append(k)
        pruned_tuple = tuple(pruned_list)
        viable = tuple(viable_list)
    else:
        pruned_tuple = ()
        viable = ordered

    if bound is not None:
        limit = min(bound, len(viable))
        explored = viable[:limit]
        open_keys = viable[limit:]
    else:
        explored = viable
        open_keys = ()

    census = record_census(ordered, explored, pruned_tuple, open_keys)
    desc = justification or (
        f"declared constraint pruned: {len(census.pruned)} keys pruned, "
        f"{len(census.explored)} keys explored, {len(census.open_keys)} keys open"
    )
    return SearchPolicy(
        policy_id=policy_id,
        justification=desc,
        retained=ordered,
        explored=census.explored,
        pruned=census.pruned,
        open_keys=census.open_keys,
    )


def declared_cost_budgeted(
    retained: tuple[CanonKey, ...],
    cost_fn: Callable[[CanonKey], Fraction | int | str] | Mapping[CanonKey, Fraction | int | str],
    budget: Fraction | int | str,
    *,
    policy_id: str = "declared-cost-budgeted",
    justification: str | None = None,
) -> SearchPolicy:
    """Declared subset: explore keys within exact rational budget in Q; remainder open.

    Costs and budget are computed in exact rational arithmetic (fractions.Fraction).
    Keys are considered in ascending cost order, with ties broken in canonical key order.
    Funded keys are recorded as explored; unfunded keys are recorded as open; none pruned.
    Census invariance is verified via record_census.
    """
    exact_budget = _exact_q(budget)
    if exact_budget < 0:
        raise ValueError("budget cannot be negative")
    ordered = tuple(sorted(retained))

    def _get_cost(k: CanonKey) -> Fraction:
        raw = cost_fn[k] if isinstance(cost_fn, Mapping) else cost_fn(k)
        c = _exact_q(raw)
        if c < 0:
            raise ValueError("cost cannot be negative")
        return c

    # Sort keys by ascending exact cost, breaking ties by canonical key order
    cost_map = {k: _get_cost(k) for k in ordered}
    cost_ranked = tuple(sorted(ordered, key=lambda k: (cost_map[k], k)))

    spent = Fraction(0)
    explored_list: list[CanonKey] = []
    open_list: list[CanonKey] = []

    for k in cost_ranked:
        c = cost_map[k]
        if spent + c <= exact_budget:
            explored_list.append(k)
            spent += c
        else:
            open_list.append(k)

    explored = tuple(explored_list)
    open_keys = tuple(open_list)
    pruned: tuple[CanonKey, ...] = ()

    census = record_census(ordered, explored, pruned, open_keys)
    desc = justification or (
        f"declared cost budgeted: budget={exact_budget}, spent={spent}, "
        f"explored={len(census.explored)}, open={len(census.open_keys)}"
    )
    return SearchPolicy(
        policy_id=policy_id,
        justification=desc,
        retained=ordered,
        explored=census.explored,
        pruned=census.pruned,
        open_keys=census.open_keys,
    )

