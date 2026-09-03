"""The reach measure: how much observable content a response creates.

The sealed measures are base-free.  ``mu1`` is the item count; ``mu2`` is
the item count refined by new-form arity sum.  Neither reads the state the
response is applied to, and neither can therefore distinguish a response
that changes one thing from a response that changes everything: a single
instance and a single uniform rule are both one item of zero new-form
arity, so both are ``mu1 = 1`` and ``mu2 = (1, 0)``.

This tree declares a third measure that does read the state.

    REACH(base, delta) = the number of pluggings that become derivable.

Nothing is weighted by hand.  A plugging is the estate's own unit of
observable content -- a context filled by a datum, derivable or not -- and
a datum's profile is exactly the set of contexts derivable for it.  The
reach of a response is the growth of the total profile size.  So a single
instance has reach one, and a uniform rule has the reach of every plugging
of its form that was not already derivable.

Two consequences, both recorded rather than assumed:

* reach is BASE-RELATIVE.  The same delta has different reach on different
  states, which is what the sealed measures cannot express.
* reach is NOT a refinement of the item count.  It can prefer a response
  with strictly more items, and `sealed_side.py` exhibits a pair where it
  does.

AuthorityEffect: None.  Nothing here amends the sealed derivation; the
sealed measures keep their meaning and this measure sits beside them.
"""

from __future__ import annotations

import pathlib
import sys
from collections.abc import Callable
from dataclasses import dataclass

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
_CODE = str(REPO / "code")
if _CODE not in sys.path:
    sys.path.insert(0, _CODE)

from derivation.candidates import (  # noqa: E402
    Delta,
    NewDatum,
    NewForm,
    NewInst,
    NewRuleAll,
    apply_delta,
    mu1,
    mu2,
)
from derivation.model import Regime  # noqa: E402
from derivation.observe import profiles  # noqa: E402

# The two sealed measures are re-exported deliberately: this module is the
# one place all three orders are named together, and a consumer that
# imported `mu1` from here and `mu3` from there could drift.
__all__ = [
    "Priced",
    "delta_kind",
    "item_kind",
    "measure_key",
    "minima_under",
    "mu1",
    "mu2",
    "mu3",
    "price",
    "profile_size",
    "reach",
    "separates_kinds",
]


def profile_size(r: Regime) -> int:
    """The total observable content of a state: how many context-and-datum
    pluggings are derivable, summed over the data.

    This is the estate's own `profiles`, counted.  Nothing is weighted."""

    return sum(len(p) for p in profiles(r))


def reach(base: Regime, delta: Delta) -> int:
    """REACH: the number of pluggings the response makes newly derivable.

    Base-relative by construction.  Raises through `apply_delta` when the
    delta is ill-formed for the base, which is the sealed module's own
    behaviour and is not caught here."""

    return profile_size(apply_delta(base, delta)) - profile_size(base)


def mu3(base: Regime, delta: Delta) -> tuple[int, int]:
    """The reach measure, lexicographic: reach first, item count second.

    Reach leads because the question this measure exists to answer is how
    much of the state a response disturbs, not how many keystrokes it
    takes.  The item count is retained as the second coordinate so that
    two responses of equal reach are still ordered, and so that the
    measure is total."""

    return (reach(base, delta), mu1(delta))


def item_kind(it: object) -> str:
    if isinstance(it, NewDatum):
        return "datum"
    if isinstance(it, NewForm):
        return "form"
    if isinstance(it, NewInst):
        return "inst"
    if isinstance(it, NewRuleAll):
        return "rule"
    raise TypeError(type(it))


def delta_kind(delta: Delta) -> str:
    """The item-kind signature of a response, in the sealed canonical
    order, as the dual tree's census reports it."""

    return "+".join(sorted(item_kind(it) for it in delta))


@dataclass(frozen=True)
class Priced:
    """One response, priced under all three measures."""

    kind: str
    items: int
    mu1: int
    mu2: tuple[int, int]
    reach: int
    mu3: tuple[int, int]


def price(base: Regime, delta: Delta) -> Priced:
    return Priced(
        kind=delta_kind(delta),
        items=len(delta),
        mu1=mu1(delta),
        mu2=mu2(delta),
        reach=reach(base, delta),
        mu3=mu3(base, delta),
    )


def measure_key(base: Regime, measure: str) -> Callable[[Delta], tuple[int, ...]]:
    """One measure as a comparison key, named so the three orders are
    declared in a single place and cannot drift apart between callers."""

    if measure == "mu1":
        return lambda d: (mu1(d),)
    if measure == "mu2":
        return lambda d: mu2(d)
    if measure == "mu3":
        return lambda d: mu3(base, d)
    raise ValueError(f"unknown measure: {measure}")


def minima_under(base: Regime, deltas: list[Delta], measure: str) -> list[Delta]:
    """The minimum responses among a supplied list, under one measure.

    Takes the candidate list rather than enumerating: the sealed and dual
    enumerators are the authorities on what is valid, and this tree
    re-prices their output rather than second-guessing it."""

    if not deltas:
        return []
    key = measure_key(base, measure)
    best = min(key(d) for d in deltas)
    return [d for d in deltas if key(d) == best]


def separates_kinds(base: Regime, deltas: list[Delta]) -> dict[str, object]:
    """Whether a measure distinguishes the item kinds present.

    Records, for each measure, how many distinct cost values it assigns
    across the supplied responses, and how many distinct item-kind
    signatures those responses have.  A measure that assigns one cost to
    several kinds cannot select among them."""

    kinds = sorted({delta_kind(d) for d in deltas})
    out: dict[str, object] = {"kinds": kinds, "responses": len(deltas)}
    for name in ("mu1", "mu2", "mu3"):
        key = measure_key(base, name)
        costs = {key(d) for d in deltas}
        by_kind: dict[str, set[tuple[int, ...]]] = {}
        for d in deltas:
            by_kind.setdefault(delta_kind(d), set()).add(key(d))
        collided = sorted(
            k for k in kinds
            if any(
                key(d) in by_kind.get(other, set())
                for other in kinds if other != k
                for d in deltas if delta_kind(d) == k
            )
        )
        out[name] = {
            "distinct_costs": len(costs),
            "kinds_sharing_a_cost_with_another_kind": collided,
        }
    return out
