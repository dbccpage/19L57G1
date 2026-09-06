"""The presentation layer: reading a supplied whole.

Classification (assumption discipline):

* Everything here is METATHEORY APPARATUS.  A supplied whole is opaque to the
  object language; ``read_whole`` is the metatheoretic reader that extracts
  at most one mark and the position it was presented at, and refuses anything
  beyond the declared bound rather than guessing.
* The presented position is a fact of the PRESENTATION.  It is metatheory in
  the pinned world too, by that world's own words, so keeping it costs this
  control nothing and gives it nothing — while preserving the caller's two
  inscriptions as two distinct facts of presentation.
* What is deleted is the CONVENTION, not the reader.  The pinned world maps a
  presented position to an admitted side by a convention declared in its
  metatheory; the codomain of that map is gone, so the map goes.  There is no
  successor to it here, and no function of this module reaches admitted
  state.  Deleting the reader as well would have collapsed the caller's two
  inscriptions into one identical history, which is a loss with nothing
  bought by it; the deletion belongs at the convention.
* ``supply_event`` turns a read whole into the external presentation event;
  ``admission_event`` turns it into the admission event of the declared
  identity policy.  Neither applies anything to a regime.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from sidefree.model import AdmitOccurrence, Supply

# The two positions a mark can be presented at, relative to the one bar of the
# inscription.  Nothing in the carrier reads these; they are recorded so that
# the caller's two inscriptions stay two facts and not one.
PRESENTED_POSITIONS: tuple[str, str] = ("before", "after")

_WHOLE = re.compile(r"^<([a-z]*)\|([a-z]*)>$")


class PresentationError(ValueError):
    """The text is not a whole within the declared bound."""


@dataclass(frozen=True)
class Whole:
    """A read whole: at most one mark, and the position it was presented at.

    ``token`` and ``presented_position`` are both ``None`` for a whole with no
    mark.  The spelling of the whole is not stored.
    """

    token: str | None
    presented_position: str | None

    def __post_init__(self) -> None:
        if (self.token is None) != (self.presented_position is None):
            raise PresentationError("a mark and its presented position come together")
        if (
            self.presented_position is not None
            and self.presented_position not in PRESENTED_POSITIONS
        ):
            raise PresentationError(
                f"unknown presented position: {self.presented_position!r}"
            )


def read_whole(text: str) -> Whole:
    """Read one whole of the form ``<|>``, ``<x|>``, or ``<|x>``.

    Declared bound: one bar, at most one mark in total.  Anything else is
    refused by name so that no structure is read silently.
    """
    m = _WHOLE.match(text)
    if m is None:
        raise PresentationError(
            f"not a whole with one bar and at most one mark: {text!r}"
        )
    before, after = m.group(1), m.group(2)
    if len(before) + len(after) > 1:
        raise PresentationError(f"more than one mark is beyond the bound: {text!r}")
    if before:
        return Whole(before, "before")
    if after:
        return Whole(after, "after")
    return Whole(None, None)


def supply_event(whole: Whole) -> Supply:
    """The external presentation event for a read whole with a mark."""
    if whole.token is None:
        raise PresentationError("a whole with no mark carries nothing to supply")
    return Supply(whole.token)


def admission_event(whole: Whole) -> AdmitOccurrence:
    """The admission event of the declared identity policy for a read whole.

    The presented position reaches nothing: it is not an argument of the
    event, and there is no convention here that would make it one.
    """
    if whole.token is None:
        raise PresentationError("a whole with no mark carries nothing to admit")
    return AdmitOccurrence(whole.token)
