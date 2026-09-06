"""The item alphabet, the canonical delta order, the two cost measures, and
the stated state.

Classification: admitted primitive of this rung (the two reader item kinds and
the widened item bound); metatheory apparatus (everything else).

Six item kinds: the four sealed, plus ``NewReader`` and ``AddContext``.

``NewReader`` admits a reader with an **empty** selection, and every context
costs its own ``AddContext``.  A reader's width is therefore exactly the items
spent on it.  This is the load-bearing anti-smuggle: were ``NewReader`` to
carry its selection, a candidate would buy unbounded observational capacity at
unit price and every number on both sides of the comparison would be wrong by
an unbounded amount.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from .grammar import Context, contexts
from .readers import (
    Aggregation, Reader, Reading, lawful_aggregations, reading_class,
)
from .regime import (
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    AdmissionRefused,
    Args,
    Event,
    Regime,
    replay,
)


@dataclass(frozen=True)
class NewDatum:
    pass


@dataclass(frozen=True)
class NewForm:
    arity: int


@dataclass(frozen=True)
class NewInst:
    form: int
    args: Args


@dataclass(frozen=True)
class NewRuleAll:
    form: int


@dataclass(frozen=True)
class NewReader:
    """Admits a reader with an empty selection.  Such a reader is blind and
    separates nothing until contexts are bought one at a time."""

    reading: Reading
    aggregation: Aggregation


@dataclass(frozen=True)
class AddContext:
    """Adds one context to an admitted reader's selection.  One item, one
    context, no exceptions."""

    reader: int
    context: Context


SealedItem = Union[NewDatum, NewForm, NewInst, NewRuleAll]
Item = Union[NewDatum, NewForm, NewInst, NewRuleAll, NewReader, AddContext]
Delta = tuple[Item, ...]


def item_key(it: Item) -> tuple[int, int, tuple[object, ...]]:
    """The canonical item order: data, forms, rules, instances, readers,
    context additions.  Total and deterministic, extending the sealed key."""
    if isinstance(it, NewDatum):
        return (0, 0, ())
    if isinstance(it, NewForm):
        return (1, it.arity, ())
    if isinstance(it, NewRuleAll):
        return (2, it.form, ())
    if isinstance(it, NewInst):
        return (3, it.form, tuple(it.args))
    if isinstance(it, NewReader):
        return (4, 0, (tuple(it.reading), tuple(it.aggregation)))
    return (5, it.reader, (it.context[0], tuple(
        -1 if s is None else s for s in it.context[1]
    )))


def canonical_delta(items: tuple[Item, ...]) -> Delta:
    return tuple(sorted(items, key=item_key))


def is_sealed_item(it: Item) -> bool:
    return isinstance(it, (NewDatum, NewForm, NewInst, NewRuleAll))


ITEM_FIELDS: dict[type[object], set[str]] = {
    NewDatum: set(), NewForm: {"arity"}, NewInst: {"form", "args"},
    NewRuleAll: {"form"}, NewReader: {"reading", "aggregation"},
    AddContext: {"reader", "context"},
}


def item_shape_valid(it: object) -> bool:
    """The complete six-kind field census, with unknown subclasses refused."""
    return type(it) in ITEM_FIELDS and set(vars(it)) == ITEM_FIELDS[type(it)]


def mu1(delta: Delta) -> int:
    """The sealed item count, re-implemented.  Reader items are items."""
    return len(delta)


def mu2(delta: Delta) -> tuple[int, int]:
    """The sealed ``(item count, new-form arity sum)``, re-implemented.

    Reader items contribute nothing to the second component **by the
    formula**, not by amendment.  The resulting blindness of ``mu2`` along the
    reader axis is reported as a finding and never repaired: amending it would
    stop it being the sealed function and would silently change what every
    sealed answer means."""
    return (
        len(delta),
        sum(it.arity for it in delta if isinstance(it, NewForm)),
    )


@dataclass(frozen=True)
class StatedState:
    """A sealed regime together with a finite tuple of admitted readers.

    Genesis has ``readers = ()``.  The projection to the regime is asserted by
    test to commute with every sealed event, so the reader-free slice of this
    tree is exactly the sealed derivation."""

    regime: Regime
    readers: tuple[Reader, ...]


def project(s: StatedState) -> Regime:
    return s.regime


def sealed_events(base: Regime, delta: Delta) -> tuple[Event, ...]:
    """Translate the sealed items of a canonical delta into admission events.

    Fresh data receive tokens ``w<index>`` at their admission position, as in
    the pinned sealed source."""
    events: list[Event] = []
    n = base.n_data()
    for it in delta:
        if isinstance(it, NewDatum):
            events.append(AdmitDatum(f"w{n}"))
            n += 1
        elif isinstance(it, NewForm):
            events.append(AdmitForm(it.arity))
        elif isinstance(it, NewRuleAll):
            events.append(AdmitRuleAll(it.form))
        elif isinstance(it, NewInst):
            events.append(AdmitInst(it.form, it.args))
    return tuple(events)


def apply_delta(
    state: StatedState, delta: Delta, w_max: int, max_readers: int
) -> StatedState:
    """Apply a canonical delta by naive replay.  Refuses ill-formed items.

    Validity is decided here and never by the sealed fast path, which is
    forced rather than cautious: the fast path refuses a rule-bearing base and
    every minimum rival prefix contains ``NewRuleAll``."""
    if not all(item_shape_valid(it) for it in delta):
        raise AdmissionRefused("item kind or fields are outside the declared alphabet")
    delta = canonical_delta(delta)
    regime = replay(sealed_events(state.regime, delta), state.regime)
    readers = list(state.readers)
    available = contexts(regime)
    for it in delta:
        if isinstance(it, NewReader):
            if len(readers) >= max_readers:
                raise AdmissionRefused(
                    f"at most {max_readers} readers per stated state"
                )
            if len(it.reading) != 4 or any(type(v) is not bool for v in it.reading):
                raise AdmissionRefused("reader reading must be four Boolean values")
            if (len(it.aggregation) != w_max + 1
                    or any(type(v) is not bool for v in it.aggregation)
                    or it.aggregation not in lawful_aggregations(w_max)):
                raise AdmissionRefused("reader aggregation is not lawful at the declared width")
            readers.append(Reader((), it.reading, it.aggregation))
        elif isinstance(it, AddContext):
            if not 0 <= it.reader < len(readers):
                raise AdmissionRefused(f"unknown reader {it.reader}")
            if it.context not in available:
                raise AdmissionRefused(
                    f"context {it.context} is not a context of the regime"
                )
            rho = readers[it.reader]
            if it.context in rho.selection:
                raise AdmissionRefused("context already in the selection")
            if rho.width() >= w_max:
                raise AdmissionRefused(f"selection exceeds width {w_max}")
            readers[it.reader] = Reader(
                tuple(sorted(rho.selection + (it.context,), key=str)),
                rho.reading,
                rho.aggregation,
            )
    return StatedState(regime, tuple(readers))


def capabilities(delta: Delta) -> dict[str, object]:
    """The capability vector of a candidate.

    The sealed five keys unchanged, plus the reader keys.  Reported as a
    vector and **never** totalled into a scalar: totalling would invent a
    third measure."""
    return {
        "new_data": sum(1 for it in delta if isinstance(it, NewDatum)),
        "new_forms": sum(1 for it in delta if isinstance(it, NewForm)),
        "new_form_arity_sum": sum(
            it.arity for it in delta if isinstance(it, NewForm)
        ),
        "new_instances": sum(1 for it in delta if isinstance(it, NewInst)),
        "new_rules": sum(1 for it in delta if isinstance(it, NewRuleAll)),
        "new_readers": sum(1 for it in delta if isinstance(it, NewReader)),
        "new_reader_contexts": sum(
            1 for it in delta if isinstance(it, AddContext)
        ),
        "reading_class": [
            list(reading_class(it.reading)) for it in delta
            if isinstance(it, NewReader)
        ],
        "aggregation_lawful": [
            it.aggregation in lawful_aggregations(len(it.aggregation) - 1)
            for it in delta if isinstance(it, NewReader)
        ],
    }


def item_json(it: Item) -> dict[str, object]:
    """A deterministic JSON rendering of one item."""
    if isinstance(it, NewDatum):
        return {"kind": "datum"}
    if isinstance(it, NewForm):
        return {"arity": it.arity, "kind": "form"}
    if isinstance(it, NewRuleAll):
        return {"form": it.form, "kind": "rule"}
    if isinstance(it, NewInst):
        return {"args": list(it.args), "form": it.form, "kind": "inst"}
    if isinstance(it, NewReader):
        return {
            "aggregation": [bool(v) for v in it.aggregation],
            "kind": "reader",
            "reading": [bool(v) for v in it.reading],
        }
    return {
        "context": [it.context[0], [-1 if s is None else s
                                    for s in it.context[1]]],
        "kind": "add_context",
        "reader": it.reader,
    }


def delta_json(delta: Delta) -> list[dict[str, object]]:
    return [item_json(it) for it in canonical_delta(delta)]
