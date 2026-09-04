"""Admitted regimes, events, replay, observation, and renaming for the
boundary world, as far as Challenge 0 requires.

Classification (assumption discipline):

* The BOUNDARY and its two SIDES are the one admitted primitive.  A regime
  records, for each admitted mark, the side it lies on.  The boundary is
  not a datum: it is the frame every datum is placed against.
* A READING is metatheory: ``U`` leaves the two sides unnamed, so the
  exchange of sides is a renaming the object language cannot see; ``O``
  names them ``near`` and ``far``, so the exchange is not a renaming.
* ``Supply`` is an external presentation event and changes no state.
  ``AdmitMark`` is the only event that changes state: it admits a supplied
  mark on a side.  Re-admission of an admitted mark is a designation, not
  a duplication (declared convention, as presentation identity is
  metatheoretic).
* Observation of a side is its CONTENTS: the internal identities (indices)
  of the marks on it.  Under ``O`` a side's name is also observable.
  Nothing else about a side is observable; in particular there is no
  admitted judgment that a side is empty.  The absence of an observation
  is never converted into a judgment.
* ``replay`` rebuilds a regime from an event list; every certified regime
  must equal the replay of its history.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from typing import Sequence, Union

READING_U = "U"
READING_O = "O"
READINGS: tuple[str, ...] = (READING_U, READING_O)
SIDE_NAMES: tuple[str, str] = ("near", "far")  # reading O only


class AdmissionError(ValueError):
    """An event is ill-formed relative to the current regime."""


@dataclass(frozen=True)
class Regime:
    """Admitted state.

    ``reading``:   the declared reading of the boundary, ``U`` or ``O``.
    ``marks``:     admitted marks in admission order (presentation tokens;
                   internal identity is the index).
    ``placement``: for each admitted mark, the side it lies on, ``0`` or
                   ``1``.  The boundary is implicit and unique.
    """

    reading: str
    marks: tuple[str, ...]
    placement: tuple[int, ...]

    def n_marks(self) -> int:
        return len(self.marks)


def genesis(reading: str) -> Regime:
    if reading not in READINGS:
        raise AdmissionError(f"unknown reading: {reading!r}")
    return Regime(reading, (), ())


@dataclass(frozen=True)
class Supply:
    """External presentation of a token.  Not an admission."""

    token: str


@dataclass(frozen=True)
class AdmitMark:
    """Admission of a presented token as a mark on a side."""

    token: str
    side: int


Event = Union[Supply, AdmitMark]


def step(r: Regime, e: Event) -> Regime:
    """Apply one event.  Deterministic; raises on ill-formed admissions."""
    if isinstance(e, Supply):
        return r
    if e.side not in (0, 1):
        raise AdmissionError(f"side must be 0 or 1, got {e.side}")
    if e.token in r.marks:
        return r
    return Regime(r.reading, r.marks + (e.token,), r.placement + (e.side,))


def replay(history: Sequence[Event], base: Regime) -> Regime:
    r = base
    for e in history:
        r = step(r, e)
    return r


def certify(history: Sequence[Event], base: Regime, claimed: Regime) -> bool:
    return replay(history, base) == claimed


# ---------------------------------------------------------------------------
# Observation
# ---------------------------------------------------------------------------


def contents(r: Regime, side: int) -> frozenset[int]:
    """The marks on a side, by internal identity."""
    if side not in (0, 1):
        raise ValueError(f"side must be 0 or 1, got {side}")
    return frozenset(i for i, s in enumerate(r.placement) if s == side)


def side_profile(r: Regime, side: int) -> tuple[object, ...]:
    """Everything the object language can observe of a side: its contents,
    and under reading ``O`` its admitted name."""
    if r.reading == READING_O:
        return (SIDE_NAMES[side], contents(r, side))
    return (contents(r, side),)


def sides_collapsed(r: Regime) -> bool:
    """The two sides are observationally indistinguishable."""
    return side_profile(r, 0) == side_profile(r, 1)


def observations(r: Regime) -> frozenset[tuple[int, int]]:
    """The admitted observation relation: (mark, side) for every admitted
    mark.  At genesis it is empty; nothing else about a side is observable."""
    return frozenset((i, s) for i, s in enumerate(r.placement))


# ---------------------------------------------------------------------------
# Renaming and the reflection
# ---------------------------------------------------------------------------


def reflect(r: Regime) -> Regime:
    """Exchange the two sides.  Under ``U`` this is a renaming the object
    language cannot see; under ``O`` it is not a renaming, because the
    names are admitted, and the result is a different regime whenever any
    mark is placed."""
    return Regime(r.reading, r.marks, tuple(1 - s for s in r.placement))


def rename_marks(r: Regime, pi: Sequence[int]) -> Regime:
    """Apply a permutation of internal identities.  Presentation tokens
    travel with their marks and are forgotten by ``canonical``."""
    n = r.n_marks()
    if sorted(pi) != list(range(n)):
        raise ValueError("not a permutation of the admitted marks")
    marks = [""] * n
    placement = [0] * n
    for i in range(n):
        marks[pi[i]] = r.marks[i]
        placement[pi[i]] = r.placement[i]
    return Regime(r.reading, tuple(marks), tuple(placement))


def serialize(r: Regime) -> tuple[object, ...]:
    """Tokens forgotten; the reading kept; the placement kept."""
    return (r.reading, r.placement)


def canonical(r: Regime) -> tuple[object, ...]:
    """The minimum serialization over every mark permutation, and under
    ``U`` also over the side exchange.  Two regimes have equal keys exactly
    when they differ by a renaming the object language cannot see."""
    candidates = [r] + ([reflect(r)] if r.reading == READING_U else [])
    best: tuple[object, ...] | None = None
    for base in candidates:
        for pi in permutations(range(base.n_marks())):
            key = serialize(rename_marks(base, pi))
            if best is None or key < best:
                best = key
    assert best is not None
    return best


def is_automorphism_reflection(r: Regime) -> bool:
    """Whether the side exchange fixes the regime up to a renaming the
    reading permits.  Under ``O`` the exchange is not a permitted renaming,
    so this is ``False`` by definition whenever it would move a mark, and
    ``True`` only in the degenerate case of no marks, where it moves
    nothing; the receipt reports both facts separately."""
    if r.reading == READING_O:
        return reflect(r) == r
    return canonical(reflect(r)) == canonical(r)
