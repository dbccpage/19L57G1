"""The presentation layer: reading a supplied whole, and the convention
that maps a presented side to an admitted side.

Classification (assumption discipline):

* Everything here is METATHEORY APPARATUS.  A supplied whole such as
  ``<a|>`` is opaque to the object language except for the one admitted
  exception: its boundary has two sides and the mark lies on one of them.
  ``read_whole`` is the metatheoretic reader that extracts exactly that
  and nothing more: at most one mark, and which side of the bar it was
  presented on.  It refuses anything beyond the declared Challenge 1
  bound (two marks, a mark on each side, a nested whole) rather than
  guessing.
* The presented side (``left`` or ``right``) is a fact of the
  presentation.  Which admitted side it becomes is a CONVENTION declared
  here and not derived from the inscription.  Two conventions exist; the
  declared one maps ``left`` to side ``0``, which reading ``O`` names
  ``near``.  Under ``U`` the choice is invisible up to the permitted
  reflection; under ``O`` it is not, and Challenge 1 reports both
  candidates.
* ``supply_event`` turns a read whole into the external presentation
  event; ``admission_event`` turns it, under a convention, into the
  admission event.  Neither applies anything to a regime.

Challenge 4 addition.  The caller supplies wholes with a mark on each side
of the bar, which ``read_whole`` refuses by name.  ``read_pair_whole`` is
the WIDENED reader: at most one mark on each side, and nothing further.
The widening is a declared augmentation of the metatheory, priced in the
rung's ledger and paid by the run; the narrower reader is left as it was,
so the refusal that forced the widening stays visible.  In which order the
two marks of one whole are admitted is a second declaration of the same
kind as the convention, and both orders are reported.

Challenge 5 addition.  The caller supplies a whole within a side, which both
earlier readers refuse by name: neither reads an ITEM that is itself a whole.
``read_nested_whole`` is this run's third reader bound, and the second
widening of the reader — the Challenge 1 bound was declared and not widened: an
item on a side is a mark or a whole, down to a declared finite depth beyond
which the reader refuses by name.  The two narrower readers are left refusing,
so what forced each widening stays visible, and the widening is a declaration
of the run priced in the rung's ledger.  Reading a nested item is not
admitting one: what an admission does with an item that is a whole is the
declared policy space of ``challenge5.py`` and is decided there, not here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Union

from boundary.model import AdmitMark, Supply

PRESENTED_SIDES: tuple[str, str] = ("left", "right")
CONVENTIONS: dict[str, dict[str, int]] = {
    "left is side 0": {"left": 0, "right": 1},
    "left is side 1": {"left": 1, "right": 0},
}
DECLARED_CONVENTION = "left is side 0"
OTHER_CONVENTION = "left is side 1"

_WHOLE = re.compile(r"^<([a-z]*)\|([a-z]*)>$")


class PresentationError(ValueError):
    """The text is not a whole within the declared Challenge 1 bound."""


@dataclass(frozen=True)
class Whole:
    """A read whole: at most one mark and the side of the bar it lies on.

    ``token`` and ``presented_side`` are both ``None`` for the initial
    inscription ``<|>``.  The spelling of the whole is not stored.
    """

    token: str | None
    presented_side: str | None

    def __post_init__(self) -> None:
        if (self.token is None) != (self.presented_side is None):
            raise PresentationError("a mark and its presented side come together")
        if self.presented_side is not None and self.presented_side not in PRESENTED_SIDES:
            raise PresentationError(f"unknown presented side: {self.presented_side!r}")


def read_whole(text: str) -> Whole:
    """Read one whole of the form ``<|>``, ``<x|>``, or ``<|x>``.

    Declared bound: one bar, at most one mark in total.  Anything else is
    refused by name so that no structure beyond the admitted exception is
    read silently.
    """
    m = _WHOLE.match(text)
    if m is None:
        raise PresentationError(f"not a whole with one bar and at most one mark: {text!r}")
    left, right = m.group(1), m.group(2)
    if len(left) + len(right) > 1:
        raise PresentationError(f"more than one mark is beyond the Challenge 1 bound: {text!r}")
    if left:
        return Whole(left, "left")
    if right:
        return Whole(right, "right")
    return Whole(None, None)


def supply_event(whole: Whole) -> Supply:
    """The external presentation event for a read whole with a mark."""
    if whole.token is None:
        raise PresentationError("the initial whole carries no mark to supply")
    return Supply(whole.token)


def admitted_side(presented_side: str, convention: str) -> int:
    """The admitted side a presented side maps to under a convention."""
    if convention not in CONVENTIONS:
        raise PresentationError(f"unknown convention: {convention!r}")
    if presented_side not in PRESENTED_SIDES:
        raise PresentationError(f"unknown presented side: {presented_side!r}")
    return CONVENTIONS[convention][presented_side]


def admission_event(whole: Whole, convention: str) -> AdmitMark:
    """The admission event for a read whole under a convention."""
    if whole.token is None or whole.presented_side is None:
        raise PresentationError("the initial whole carries no mark to admit")
    return AdmitMark(whole.token, admitted_side(whole.presented_side, convention))


# ---------------------------------------------------------------------------
# Challenge 4: the widened reader bound, and the within-whole order
# ---------------------------------------------------------------------------

WITHIN_WHOLE_ORDERS: dict[str, tuple[str, str]] = {
    "left first": ("left", "right"),
    "right first": ("right", "left"),
}
DECLARED_WITHIN_WHOLE_ORDER = "left first"
OTHER_WITHIN_WHOLE_ORDER = "right first"


@dataclass(frozen=True)
class PairWhole:
    """A whole read under the WIDENED Challenge 4 bound: at most one mark on
    each side of the bar.

    ``read_whole`` keeps the narrower Challenge 1 bound and still refuses
    ``<a|b>`` by name; this type and its reader are a declared widening of the
    metatheory, priced in the rung's ledger and paid by the run.  The spelling
    of the whole is not stored, and nothing beyond a mark per side is read.
    """

    left: str | None
    right: str | None


def read_pair_whole(text: str) -> PairWhole:
    """Read one whole of the form ``<|>``, ``<x|>``, ``<|y>``, or ``<x|y>``.

    Declared bound: one bar, at most one mark on each side.  Two marks on one
    side, and a nested whole, are refused by name, so that no structure beyond
    the admitted exception and this rung's declared widening is read silently.
    """
    m = _WHOLE.match(text)
    if m is None:
        raise PresentationError(
            f"not a whole with one bar and at most one mark on each side: {text!r}"
        )
    left, right = m.group(1), m.group(2)
    if len(left) > 1 or len(right) > 1:
        raise PresentationError(
            f"more than one mark on a side is beyond the Challenge 4 bound: {text!r}"
        )
    return PairWhole(left or None, right or None)


def pair_marks(whole: PairWhole, convention: str, order: str) -> list[tuple[str, int]]:
    """The ``(token, admitted side)`` pairs of a read whole, in the declared
    within-whole admission order.

    The presented side of each mark is a fact of the presentation; the
    admitted side it maps to is the declared convention (definition 18).  In
    which order the marks of one whole are admitted is a second declaration of
    the same kind, and the other order is reported beside it.
    """
    if order not in WITHIN_WHOLE_ORDERS:
        raise PresentationError(f"unknown within-whole order: {order!r}")
    out: list[tuple[str, int]] = []
    for presented in WITHIN_WHOLE_ORDERS[order]:
        token = whole.left if presented == "left" else whole.right
        if token is not None:
            out.append((token, admitted_side(presented, convention)))
    return out


# ---------------------------------------------------------------------------
# Challenge 5: the nested reader bound
# ---------------------------------------------------------------------------

NESTING_BOUND = 2
"""The declared finite depth the Challenge 5 reader accepts.

The caller's inscription has depth two — one boundary within one side of
another — and the reader refuses depth three by name rather than reading
arbitrarily deep, so that every enumeration below stays finite by
declaration.  The bound is a declaration of the run, not a fact about the
inscription.
"""


@dataclass(frozen=True)
class NestedWhole:
    """A whole read under the Challenge 5 bound: at most one ITEM on each side
    of the bar, where an item is a mark or a whole.

    ``read_whole`` and ``read_pair_whole`` keep their own narrower bounds and
    still refuse a nested whole by name; this type and its reader are the run's
    third declared reader bound and its second widening of the reader, paid by
    the run.  The spelling of the whole is not stored: ``render`` rebuilds a
    spelling from the read structure and is used to name a domain member, never
    as a token.
    """

    left: Item | None
    right: Item | None


Item = Union[str, NestedWhole]

_MARK = re.compile(r"^[a-z]$")


def whole_depth(whole: NestedWhole) -> int:
    """The number of boundaries crossed to reach the deepest mark, at least one.

    A whole with no item has depth one: its own boundary is the one crossed.
    """
    inner = [
        whole_depth(item)
        for item in (whole.left, whole.right)
        if isinstance(item, NestedWhole)
    ]
    return 1 + max(inner, default=0)


def render_item(item: Item | None) -> str:
    """The spelling of a read item; ``""`` for an empty side."""
    if item is None:
        return ""
    if isinstance(item, NestedWhole):
        return render_whole(item)
    return item


def render_whole(whole: NestedWhole) -> str:
    """A spelling rebuilt from the read structure, for naming a domain member."""
    return f"<{render_item(whole.left)}|{render_item(whole.right)}>"


def _split_sides(text: str) -> tuple[str, str]:
    """Split a whole's body at ITS bar: the one at nesting level zero.

    A body may itself contain bars, so the split cannot be a regular
    expression over the whole text; the level is counted here.
    """
    if len(text) < 2 or text[0] != "<" or text[-1] != ">":
        raise PresentationError(f"not a whole delimited by one pair of marks: {text!r}")
    body = text[1:-1]
    level = 0
    bar: int | None = None
    for index, char in enumerate(body):
        if char == "<":
            level += 1
        elif char == ">":
            level -= 1
            if level < 0:
                raise PresentationError(f"a whole closes before it opens: {text!r}")
        elif char == "|" and level == 0:
            if bar is not None:
                raise PresentationError(f"more than one bar at this level: {text!r}")
            bar = index
    if level != 0:
        raise PresentationError(f"a whole opens and does not close: {text!r}")
    if bar is None:
        raise PresentationError(f"no bar at this level: {text!r}")
    return body[:bar], body[bar + 1 :]


def _read_item(text: str, depth_left: int) -> Item | None:
    """Read one side's item: nothing, a mark, or a whole within the bound."""
    if text == "":
        return None
    if _MARK.match(text):
        return text
    if not text.startswith("<"):
        raise PresentationError(
            f"an item on a side is one mark or one whole, not {text!r}"
        )
    if depth_left <= 0:
        raise PresentationError(
            f"an item lying deeper than the declared bound of {NESTING_BOUND} "
            f"is refused: {text!r}"
        )
    return _read_nested(text, depth_left - 1)


def _read_nested(text: str, depth_left: int) -> NestedWhole:
    left_text, right_text = _split_sides(text)
    return NestedWhole(
        _read_item(left_text, depth_left),
        _read_item(right_text, depth_left),
    )


def read_nested_whole(text: str, bound: int = NESTING_BOUND) -> NestedWhole:
    """Read one whole in which an item on a side may itself be a whole.

    Declared bound: one bar per whole, at most one item on each side, and
    depth at most ``bound``.  Anything else is refused by name so that no
    structure beyond the admitted exception and this rung's declared widening
    is read silently.  Reading is not admitting: what an admission does with
    an item that is a whole is the policy space of ``challenge5.py``.
    """
    if bound < 1:
        raise PresentationError(f"the declared depth bound must be at least one: {bound}")
    return _read_nested(text, bound - 1)
