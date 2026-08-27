"""A partial metatheoretic grade for a declared separation request.

This module records what the existing bounded candidate computation returns.
It does not choose a request, reading, measure, bound, response, or
representative, and it performs no object-language event beyond those already
used by the candidate computation when constructing comparison children.

``decide`` classifies a valid request when the bounded minimum and quotient
computations complete. Invalid targets, unsupported bounds, rule-bearing
bases, and exhausted isomorphism budgets are errors. ``None`` is reserved for
one fact: no valid response was found inside the supplied candidate bounds.

AuthorityEffect: None
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias

from derivation.candidates import (
    Bounds,
    Delta,
    MinResponses,
    NewDatum,
    NewForm,
    NewInst,
    NewRuleAll,
    delta_events,
    item_key,
    min_responses,
)
from derivation.iso import CanonKey, canonical
from derivation.model import Impose, Pair, Regime, replay

Measure: TypeAlias = Literal["mu1", "mu2"]


class DecisionInputError(ValueError):
    """The request lies outside the declared domain of ``decide``."""


class DecisionInvariantError(RuntimeError):
    """The bounded minimum computation returned an inconsistent payload."""


@dataclass(frozen=True)
class Minimum:
    """The raw bounded minima before the implemented isomorphism quotient."""

    target: Pair
    measure: Measure
    cost: tuple[int, int]
    bounds: Bounds
    raw_minima: tuple[Delta, ...]

    def __post_init__(self) -> None:
        if self.measure not in ("mu1", "mu2"):
            raise ValueError(f"unknown minimum measure: {self.measure}")
        if not self.raw_minima:
            raise ValueError("a minimum must retain at least one raw delta")
        if len(set(self.raw_minima)) != len(self.raw_minima):
            raise ValueError("a minimum cannot contain duplicate raw deltas")
        if tuple(sorted(self.raw_minima, key=_delta_key)) != self.raw_minima:
            raise ValueError("raw minima must be in deterministic order")


@dataclass(frozen=True)
class ResponseClass:
    """One class of minima under the existing regime isomorphism relation."""

    key: CanonKey
    members: tuple[Delta, ...]

    def __post_init__(self) -> None:
        if not self.members:
            raise ValueError("a response class must be inhabited")
        if len(set(self.members)) != len(self.members):
            raise ValueError("a response class cannot duplicate a member")
        if tuple(sorted(self.members, key=_delta_key)) != self.members:
            raise ValueError("response-class members must be deterministic")


@dataclass(frozen=True)
class Quotient:
    """The complete quotient of one bounded raw-minimum population."""

    minimum: Minimum
    classes: tuple[ResponseClass, ...]
    perm_budget: int

    def __post_init__(self) -> None:
        if self.perm_budget <= 0:
            raise ValueError("quotient permutation budget must be positive")
        if not self.classes:
            raise ValueError("a quotient must retain at least one class")
        if tuple(sorted(self.classes, key=lambda item: item.key)) != self.classes:
            raise ValueError("quotient classes must be sorted by canonical key")
        if len({item.key for item in self.classes}) != len(self.classes):
            raise ValueError("quotient classes must have distinct canonical keys")
        members = tuple(
            delta for response_class in self.classes for delta in response_class.members
        )
        if set(members) != set(self.minimum.raw_minima) or len(members) != len(
            self.minimum.raw_minima
        ):
            raise ValueError("quotient classes must partition the raw minima")


@dataclass(frozen=True)
class Tie:
    """At least two live isomorphism classes remain."""

    quotient: Quotient

    def __post_init__(self) -> None:
        if len(self.quotient.classes) < 2:
            raise ValueError("Tie requires at least two quotient classes")


@dataclass(frozen=True)
class UniqueClass:
    """Several raw minima remain, but they form one isomorphism class."""

    quotient: Quotient

    def __post_init__(self) -> None:
        if len(self.quotient.classes) != 1:
            raise ValueError("UniqueClass requires exactly one quotient class")
        if len(self.quotient.minimum.raw_minima) < 2:
            raise ValueError("UniqueClass requires multiple literal raw minima")


@dataclass(frozen=True)
class UniqueDelta:
    """Exactly one literal raw minimum remains."""

    minimum: Minimum
    delta: Delta

    def __post_init__(self) -> None:
        if self.minimum.raw_minima != (self.delta,):
            raise ValueError("UniqueDelta must be the sole raw minimum")


Grade: TypeAlias = Tie | UniqueClass | UniqueDelta


def _delta_key(delta: Delta) -> tuple[tuple[int, int, tuple[int, ...]], ...]:
    return tuple(item_key(item) for item in delta)


def _validate_request(
    regime: Regime,
    i: int,
    j: int,
    measure: str,
    bounds: Bounds,
    perm_budget: int,
) -> Measure:
    if measure not in ("mu1", "mu2"):
        raise DecisionInputError(f"unknown measure: {measure}")
    if isinstance(i, bool) or not isinstance(i, int):
        raise DecisionInputError("target i must be an integer")
    if isinstance(j, bool) or not isinstance(j, int):
        raise DecisionInputError("target j must be an integer")
    if isinstance(bounds.max_items, bool) or not isinstance(bounds.max_items, int):
        raise DecisionInputError("bounds.max_items must be an integer")
    if not 0 <= bounds.max_items <= 2:
        raise DecisionInputError(
            "bounds.max_items must lie in the implemented interval 0..2"
        )
    if isinstance(bounds.max_arity, bool) or not isinstance(bounds.max_arity, int):
        raise DecisionInputError("bounds.max_arity must be an integer")
    if bounds.max_arity < 0:
        raise DecisionInputError("bounds.max_arity must be nonnegative")
    if isinstance(perm_budget, bool) or not isinstance(perm_budget, int):
        raise DecisionInputError("perm_budget must be an integer")
    if perm_budget <= 0:
        raise DecisionInputError("perm_budget must be positive")
    if not (0 <= i < j < regime.n_data()):
        raise DecisionInputError(
            f"target must satisfy 0 <= i < j < {regime.n_data()}: ({i}, {j})"
        )
    if regime.rules:
        raise DecisionInputError(
            "rule-bearing bases are outside the declared fast candidate domain"
        )
    return "mu1" if measure == "mu1" else "mu2"


def _minimum(
    result: MinResponses,
    target: Pair,
    measure: Measure,
    bounds: Bounds,
) -> Minimum:
    if result.measure != measure or result.complete_within != bounds:
        raise DecisionInvariantError("minimum-response metadata does not match request")
    if not result.deltas:
        raise DecisionInvariantError("a present minimum response has no deltas")
    if len(set(result.deltas)) != len(result.deltas):
        raise DecisionInvariantError("minimum-response population contains duplicates")
    if any(delta != tuple(sorted(delta, key=item_key)) for delta in result.deltas):
        raise DecisionInvariantError("minimum-response delta is not canonical")
    ordered = tuple(sorted(result.deltas, key=_delta_key))
    if ordered != result.deltas:
        raise DecisionInvariantError("minimum-response population is not deterministic")
    return Minimum(target, measure, result.cost, bounds, result.deltas)


def _quotient(
    regime: Regime,
    minimum: Minimum,
    perm_budget: int,
) -> Quotient:
    grouped: dict[CanonKey, list[Delta]] = {}
    for delta in minimum.raw_minima:
        child = replay(
            (Impose(minimum.target[0], minimum.target[1]),)
            + delta_events(regime, delta),
            regime,
        )
        key = canonical(child, perm_budget)
        grouped.setdefault(key, []).append(delta)
    classes = tuple(
        ResponseClass(key, tuple(sorted(members, key=_delta_key)))
        for key, members in sorted(grouped.items())
    )
    if not classes:
        raise DecisionInvariantError("nonempty minima produced an empty quotient")
    if sum(len(response_class.members) for response_class in classes) != len(
        minimum.raw_minima
    ):
        raise DecisionInvariantError("quotient lost or duplicated a raw minimum")
    return Quotient(minimum, classes, perm_budget)


def decide(
    regime: Regime,
    i: int,
    j: int,
    measure: Measure,
    bounds: Bounds,
    *,
    perm_budget: int = 100_000,
) -> Grade | None:
    """Return the bounded grade for an already-declared request.

    ``None`` means only that the finite candidate search found no response
    inside ``bounds``.  It does not mean that no response exists globally.
    The function never chooses any of its arguments and never applies a
    returned delta.
    """

    checked_measure = _validate_request(
        regime, i, j, measure, bounds, perm_budget
    )
    result = min_responses(regime, (i, j), checked_measure, bounds)
    if result is None:
        return None
    minimum = _minimum(result, (i, j), checked_measure, bounds)
    if len(minimum.raw_minima) == 1:
        return UniqueDelta(minimum, minimum.raw_minima[0])
    quotient = _quotient(regime, minimum, perm_budget)
    if len(quotient.classes) == 1:
        return UniqueClass(quotient)
    return Tie(quotient)


def grade_kind(grade: Grade | None) -> str:
    """Stable lower-case tag for receipts and tests."""

    if grade is None:
        return "none"
    if isinstance(grade, Tie):
        return "tie"
    if isinstance(grade, UniqueClass):
        return "unique_class"
    return "unique_delta"


def delta_payload(delta: Delta) -> list[dict[str, object]]:
    """Deterministic neutral serialization of a raw delta."""

    out: list[dict[str, object]] = []
    for item in delta:
        if isinstance(item, NewDatum):
            out.append({"kind": "datum"})
        elif isinstance(item, NewForm):
            out.append({"arity": item.arity, "kind": "form"})
        elif isinstance(item, NewRuleAll):
            out.append({"form": item.form, "kind": "rule_all"})
        elif isinstance(item, NewInst):
            out.append(
                {"args": list(item.args), "form": item.form, "kind": "inst"}
            )
        else:  # pragma: no cover - Delta's closed union makes this unreachable
            raise DecisionInvariantError(f"unknown delta item: {item!r}")
    return out


def _minimum_payload(minimum: Minimum) -> dict[str, object]:
    return {
        "bounds": {
            "max_arity": minimum.bounds.max_arity,
            "max_items": minimum.bounds.max_items,
        },
        "measure": minimum.measure,
        "minimum_cost": {
            "items": minimum.cost[0],
            "new_form_arity_sum": (
                None if minimum.measure == "mu1" else minimum.cost[1]
            ),
        },
        "raw_minima": [delta_payload(delta) for delta in minimum.raw_minima],
        "raw_minimum_count": len(minimum.raw_minima),
        "target": list(minimum.target),
    }


def grade_payload(grade: Grade | None) -> dict[str, object]:
    """Serialize the grade without turning a representative into a choice."""

    if grade is None:
        return {
            "kind": "none",
            "meaning": "no valid response inside the declared finite bounds",
        }
    if isinstance(grade, UniqueDelta):
        payload = _minimum_payload(grade.minimum)
        payload.update(
            {
                "delta": delta_payload(grade.delta),
                "kind": "unique_delta",
            }
        )
        return payload
    quotient = grade.quotient
    payload = _minimum_payload(quotient.minimum)
    payload.update(
        {
            "classes": [
                {
                    "canonical_key": response_class.key,
                    "members": [
                        delta_payload(delta) for delta in response_class.members
                    ],
                    "size": len(response_class.members),
                }
                for response_class in quotient.classes
            ],
            "iso_class_count": len(quotient.classes),
            "iso_perm_budget": quotient.perm_budget,
            "kind": grade_kind(grade),
        }
    )
    return payload


__all__ = [
    "DecisionInputError",
    "DecisionInvariantError",
    "Grade",
    "Measure",
    "Minimum",
    "Quotient",
    "ResponseClass",
    "Tie",
    "UniqueClass",
    "UniqueDelta",
    "decide",
    "delta_payload",
    "grade_kind",
    "grade_payload",
]
