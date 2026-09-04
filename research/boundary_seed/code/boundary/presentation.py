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
"""

from __future__ import annotations

import re
from dataclasses import dataclass

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
