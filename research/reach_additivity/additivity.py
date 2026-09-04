"""Composition of responses, and what a difference cost does along it.

The sealed candidate grammar declares no composition on responses.  This
module declares one -- concatenation of item sequences -- and asks the
prior question the cost question depends on: does applying a composite
equal applying the parts in order?

It then studies not one cost but a CLASS.  A *difference cost* is any cost
of the form

    diff_P(base, delta) = P(apply(base, delta)) - P(base)

for a state functional `P`.  The preceding rung's cost is the instance at
`P = total profile size`; that instance is restated here in two lines
rather than imported, because that rung is unmerged and so not pinnable.
Nothing below is special to it.

Two things this module is careful about, both of which turned out to
matter:

* composition is a PARTIAL operation.  A response valid on its own may be
  ill-formed after another, and one ill-formed on its own may be
  well-formed after another.  Every check below records which side is
  defined rather than assuming both are;
* a repeat is absorbed at the EVENT level -- admitting a standing instance
  returns the same state -- but that does not by itself make a self-loop at
  the ITEM level, because the item-to-event translation chooses the token
  for a fresh datum.  The two levels are kept apart here.

AuthorityEffect: None.
"""

from __future__ import annotations

import pathlib
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
_CODE = str(REPO / "code")
if _CODE not in sys.path:
    sys.path.insert(0, _CODE)

from derivation.candidates import (  # noqa: E402
    Bounds,
    Delta,
    Item,
    NewDatum,
    NewForm,
    NewInst,
    NewRuleAll,
    apply_delta,
    delta_events,
    iter_full_deltas,
    mu1,
)
from derivation.model import AdmissionError, Regime  # noqa: E402
from derivation.observe import profiles  # noqa: E402

Functional = Callable[[Regime], int]

# The sealed item count is re-exported deliberately: this module is the one
# place the declared composition and the costs compared against it are
# named together.
__all__ = [
    "FUNCTIONALS",
    "Functional",
    "SequentialCheck",
    "act",
    "additivity_check",
    "compose",
    "constructed_self_loops",
    "datum_count",
    "diff_cost",
    "form_count",
    "item_kind",
    "mu1",
    "path_end",
    "path_total_diff",
    "path_total_items",
    "profile_size",
    "self_loops",
    "sequential_check",
]


def profile_size(r: Regime) -> int:
    """Total observable content: how many context-and-datum pluggings are
    derivable, summed over the data.  The estate's own `profiles`, counted.

    Restated, not imported: the sibling tree that first declared it is
    unmerged.  `SOURCE_MANIFEST.json` says so."""

    return sum(len(p) for p in profiles(r))


def form_count(r: Regime) -> int:
    """A second state functional, so that no result below can be an
    accident of the first one."""

    return len(r.forms)


def datum_count(r: Regime) -> int:
    """A third."""

    return r.n_data()


FUNCTIONALS: dict[str, Functional] = {
    "profile_size": profile_size,
    "form_count": form_count,
    "datum_count": datum_count,
}


def compose(d: Delta, e: Delta) -> Delta:
    """The declared composition: concatenation of item sequences.

    Declared, not discovered.  A different declaration -- one that renumbers
    the second response's indices against the intermediate state, say --
    is a different operation and would need its own run."""

    return tuple(d) + tuple(e)


def act(base: Regime, delta: Delta) -> Regime | None:
    """Apply a response, or `None` when it is ill-formed for this base.

    The sealed `apply_delta` raises; this wrapper turns the raise into a
    value so that partiality can be COUNTED rather than avoided."""

    try:
        return apply_delta(base, delta)
    except AdmissionError:
        return None


def diff_cost(functional: Functional, base: Regime, delta: Delta) -> int | None:
    """A difference cost: the change the response makes in the functional.

    Signed.  Nothing here assumes the functional grows."""

    after = act(base, delta)
    if after is None:
        return None
    return functional(after) - functional(base)


@dataclass(frozen=True)
class SequentialCheck:
    """One (base, d, e) triple, with every side's definedness recorded."""

    composite_defined: bool
    stepwise_defined: bool
    states_agree: bool | None
    e_alone_defined: bool
    events_agree: bool | None


def sequential_check(base: Regime, d: Delta, e: Delta) -> SequentialCheck:
    """Does applying `d ; e` equal applying `d` then `e`?

    Also records whether the two sides produce the same EVENT tuple, which
    is the stronger statement and the one that explains agreement on
    ill-formedness."""

    composite = act(base, compose(d, e))
    middle = act(base, d)
    stepwise = None if middle is None else act(middle, e)
    events_agree: bool | None = None
    if middle is not None:
        events_agree = delta_events(base, compose(d, e)) == (
            delta_events(base, d) + delta_events(middle, e)
        )
    return SequentialCheck(
        composite_defined=composite is not None,
        stepwise_defined=stepwise is not None,
        states_agree=(
            None
            if composite is None or stepwise is None
            else composite == stepwise
        ),
        e_alone_defined=act(base, e) is not None,
        events_agree=events_agree,
    )


def additivity_check(
    functional: Functional, base: Regime, d: Delta, e: Delta
) -> bool | None:
    """Whether the difference cost of the composite equals the sum of the
    parts, or `None` when either side is undefined."""

    middle = act(base, d)
    if middle is None:
        return None
    whole = diff_cost(functional, base, compose(d, e))
    first = diff_cost(functional, base, d)
    second = diff_cost(functional, middle, e)
    if whole is None or first is None or second is None:
        return None
    return whole == first + second


def item_kind(it: Item) -> str:
    if isinstance(it, NewDatum):
        return "datum"
    if isinstance(it, NewForm):
        return "form"
    if isinstance(it, NewInst):
        return "inst"
    if isinstance(it, NewRuleAll):
        return "rule"
    raise TypeError(type(it))


def self_loops(base: Regime, bounds: Bounds) -> list[tuple[str, Delta]]:
    """Every one-item response that returns the base unchanged.

    A self-loop is a closed walk of length one, and it is what makes the
    circulation question non-vacuous.  Enumerated over the sealed
    enumerator's own one-item deltas, so a self-loop found here is a
    response the estate itself offers."""

    found: list[tuple[str, Delta]] = []
    for delta in iter_full_deltas(base, 1, bounds):
        after = act(base, delta)
        if after is not None and after == base:
            found.append((item_kind(delta[0]), delta))
    return found


def constructed_self_loops(base: Regime) -> list[tuple[str, Delta]]:
    """Self-loops built by hand rather than enumerated.

    The sealed one-item enumerator never offers a rule already standing,
    and never offers an existing datum token, so a kind can be absorbing at
    the event level and absent from the enumeration.  This function asks
    the absorption question directly, of every kind."""

    probes: list[tuple[str, Delta]] = []
    for f in sorted(base.rules):
        probes.append(("rule", (NewRuleAll(f),)))
    for f, args in sorted(base.insts):
        probes.append(("inst", (NewInst(f, args),)))
    probes.append(("datum", (NewDatum(),)))
    if base.forms:
        probes.append(("form", (NewForm(base.forms[0]),)))
    out: list[tuple[str, Delta]] = []
    for kind, delta in probes:
        after = act(base, delta)
        if after is not None and after == base:
            out.append((kind, delta))
    return out


def path_end(base: Regime, path: Sequence[Delta]) -> Regime | None:
    """Where a sequence of moves lands, or `None` if any step is
    ill-formed."""

    here: Regime | None = base
    for move in path:
        if here is None:
            return None
        here = act(here, move)
    return here


def path_total_diff(
    functional: Functional, base: Regime, path: Sequence[Delta]
) -> int | None:
    """The total difference cost along a sequence of moves, summed step by
    step -- deliberately NOT computed from the endpoints, so that the
    telescoping is a finding rather than a definition."""

    total = 0
    here: Regime = base
    for move in path:
        step_cost = diff_cost(functional, here, move)
        if step_cost is None:
            return None
        total += step_cost
        nxt = act(here, move)
        assert nxt is not None
        here = nxt
    return total


def path_total_items(path: Sequence[Delta]) -> int:
    """The total item count along a sequence of moves."""

    return sum(mu1(move) for move in path)
