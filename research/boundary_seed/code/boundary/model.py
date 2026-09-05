"""Admitted regimes, events, replay, observation, and renaming for the
boundary world, as far as Challenges 0 and 1 require.

Classification (assumption discipline):

* The initial inscription is one supplied opaque datum.  The BOUNDARY and
  its two SIDES are the one admitted primitive exception carried by that
  datum.  A regime records, for each later admitted mark, the side it lies
  on.  The boundary is not a second datum.
* A READING is metatheory: ``U`` leaves the two sides unnamed, so the
  exchange of sides is a renaming the object language cannot see; ``O``
  names them ``near`` and ``far``, so the exchange is not a renaming.
* ``Supply`` is an external presentation event and changes no state.
  ``AdmitMark`` is the only event that changes state: it admits a supplied
  mark on a side.  An admission naming a token already admitted on that
  side is a no-op: the token is already admitted and nothing is
  duplicated.  An admission naming the other side would move the mark and
  is refused by name.  Both are Python-only declarations, because the Lean
  model carries no tokens.  The word "designation" is reserved for
  current-state designation (the current state is the replay of the
  caller's history) and is not used for this no-op; an earlier version
  called the no-op a designation and absorbed the moving admission
  silently, which is WITHDRAWN.
* The closed observation grammar has two positive judgment forms:
  ``OnSide`` and, under ``O``, ``SideNamed``.  ``contents`` and
  ``side_profile`` are metatheoretic extensions of those judgments used to
  compare observable behaviour; the returned Python collections are not
  object-language data.  There is no ``Empty`` or counting judgment.
* ``replay`` rebuilds a regime from an event list; every certified regime
  must equal the replay of its history.

Challenge 1 additions, each a DERIVED DEFINITION over the above unless
marked otherwise:

* ``mentioned`` and ``supplied`` are metatheoretic readings of a history:
  the tokens any event names, and the tokens a ``Supply`` presents.  A
  mention is not an event; it is the metatheory naming a token.
* ``mark_profile`` is the metatheoretic extension of the holding judgments
  that name one admitted mark; ``new_observations`` is the set difference
  of two extensions.
* The declared finite candidate space of admissions after a history lives
  in ``challenge1.py``, not here: the kernel carries no public function
  whose return annotation contains an event type, and the Challenge 0
  generator census keeps it that way.
* ``permitted_images`` lists the regimes a permitted renaming reaches
  (mark permutations under both readings, the reflection under ``U``);
  ``isomorphism_witness`` searches it without pruning, and
  ``is_isomorphic`` is its truth value.  Equality of regimes is
  structural; isomorphism is this relation; the two are never conflated.
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
class OpaqueDatum:
    """Internal identity of the supplied whole; its presentation is opaque."""

    internal_id: int


INITIAL_DATUM = OpaqueDatum(0)


@dataclass(frozen=True)
class Regime:
    """Admitted state.

    ``reading``:       the declared reading of the boundary, ``U`` or ``O``.
    ``marks``:         admitted marks in admission order (presentation tokens;
                       internal identity is the index).
    ``placement``:     for each admitted mark, the side it lies on, ``0`` or
                       ``1``.
    ``initial_datum``: the one opaque supplied whole.  It and its boundary
                       frame are implicit and unique in every valid regime.
    """

    reading: str
    marks: tuple[str, ...]
    placement: tuple[int, ...]
    initial_datum: OpaqueDatum = INITIAL_DATUM

    def __post_init__(self) -> None:
        if self.reading not in READINGS:
            raise AdmissionError(f"unknown reading: {self.reading!r}")
        if self.initial_datum != INITIAL_DATUM:
            raise AdmissionError("the Challenge 0 initial datum is fixed")
        if len(self.marks) != len(self.placement):
            raise AdmissionError("marks and placement must have equal length")
        if len(set(self.marks)) != len(self.marks):
            raise AdmissionError("admitted mark tokens must be unique")
        if any(side not in (0, 1) for side in self.placement):
            raise AdmissionError("every admitted mark must lie on side 0 or 1")

    def n_marks(self) -> int:
        return len(self.marks)


def genesis(reading: str) -> Regime:
    return Regime(reading, (), ())


@dataclass(frozen=True)
class Supply:
    """External presentation of a token.  Not an admission."""

    token: str


@dataclass(frozen=True)
class AdmitMark:
    """Admission of a previously presented token as a mark on a side.

    ``step`` is the low-level state action.  ``replay`` is the certifying
    interface and enforces the prior-presentation precondition.
    """

    token: str
    side: int


Event = Union[Supply, AdmitMark]


def step(r: Regime, e: Event) -> Regime:
    """Apply one event to admitted state, assuming a well-formed history."""
    if isinstance(e, Supply):
        return r
    if e.side not in (0, 1):
        raise AdmissionError(f"side must be 0 or 1, got {e.side}")
    if e.token in r.marks:
        held = r.placement[r.marks.index(e.token)]
        if held != e.side:
            raise AdmissionError(
                f"mark {e.token!r} is admitted on side {held}; an admission "
                f"naming side {e.side} would move it and is refused"
            )
        return r
    return Regime(r.reading, r.marks + (e.token,), r.placement + (e.side,))


def replay(history: Sequence[Event], base: Regime) -> Regime:
    """Replay a well-formed history, refusing a new mark not supplied first."""
    r = base
    supplied: set[str] = set()
    for e in history:
        if isinstance(e, Supply):
            supplied.add(e.token)
        elif e.token not in supplied and e.token not in r.marks:
            raise AdmissionError(f"mark {e.token!r} was not supplied before admission")
        r = step(r, e)
    return r


def certify(history: Sequence[Event], base: Regime, claimed: Regime) -> bool:
    try:
        return replay(history, base) == claimed
    except AdmissionError:
        return False


def event_follows(_r: Regime, _e: Event) -> bool:
    """The Challenge 0 object-language transition relation is empty.

    Events may be supplied externally to ``replay``; no event is entailed by
    admitted state.  This is the declared Challenge 0 grammar, not a discovery
    made by inspecting Python callables.
    """
    return False


def mentioned(history: Sequence[Event]) -> frozenset[str]:
    """Tokens named by any event of a history.  A mention is not an event."""
    return frozenset(e.token for e in history)


def supplied(history: Sequence[Event]) -> frozenset[str]:
    """Tokens presented by a ``Supply`` event of a history."""
    return frozenset(e.token for e in history if isinstance(e, Supply))


# ---------------------------------------------------------------------------
# Observation judgments and metatheoretic profiles
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OnSide:
    """Positive judgment that an admitted mark lies on a side."""

    mark: int
    side: int

    def __post_init__(self) -> None:
        if self.mark < 0:
            raise ValueError("mark identity must be nonnegative")
        if self.side not in (0, 1):
            raise ValueError("side must be 0 or 1")


@dataclass(frozen=True)
class SideNamed:
    """Positive judgment that an O-reading side carries its admitted name."""

    side: int
    name: str

    def __post_init__(self) -> None:
        if self.side not in (0, 1):
            raise ValueError("side must be 0 or 1")


Observation = Union[OnSide, SideNamed]
OBSERVATION_TYPES: tuple[type, ...] = (OnSide, SideNamed)


def observation_holds(r: Regime, judgment: Observation) -> bool:
    """Whether one judgment in the closed Challenge 0 grammar holds."""
    if isinstance(judgment, OnSide):
        return (
            judgment.mark < r.n_marks()
            and r.placement[judgment.mark] == judgment.side
        )
    return r.reading == READING_O and SIDE_NAMES[judgment.side] == judgment.name


def contents(r: Regime, side: int) -> frozenset[int]:
    """Metatheoretic extension of all positive ``OnSide`` judgments."""
    if side not in (0, 1):
        raise ValueError(f"side must be 0 or 1, got {side}")
    return frozenset(i for i, s in enumerate(r.placement) if s == side)


def side_profile(r: Regime, side: int) -> tuple[object, ...]:
    """Metatheoretic extensional profile used for behavioural comparison.

    The collection is not itself an object-language value.  Its entries are
    exactly the positive judgments available for this side.
    """
    if side not in (0, 1):
        raise ValueError(f"side must be 0 or 1, got {side}")
    if r.reading == READING_O:
        return (SIDE_NAMES[side], contents(r, side))
    return (contents(r, side),)


def sides_collapsed(r: Regime) -> bool:
    """Whether the two sides have equal metatheoretic profiles."""
    return side_profile(r, 0) == side_profile(r, 1)


def mark_observations(r: Regime) -> frozenset[OnSide]:
    """All positive mark-on-side judgments, enumerated metatheoretically."""
    return frozenset(OnSide(i, s) for i, s in enumerate(r.placement))


def name_observations(r: Regime) -> frozenset[SideNamed]:
    """The two admitted name judgments under O, and none under U."""
    if r.reading == READING_U:
        return frozenset()
    return frozenset(SideNamed(side, name) for side, name in enumerate(SIDE_NAMES))


def observations(r: Regime) -> frozenset[Observation]:
    """All judgments in the closed Challenge 0 observation grammar that hold."""
    return frozenset((*mark_observations(r), *name_observations(r)))


def mark_profile(r: Regime, mark: int) -> frozenset[Observation]:
    """Metatheoretic extension of the holding judgments naming one mark.

    At Challenge 1 this is the mark's side and nothing else; the collection
    is not an object-language value.
    """
    if not 0 <= mark < r.n_marks():
        raise ValueError(f"mark {mark} is not admitted")
    return frozenset(j for j in observations(r) if isinstance(j, OnSide) and j.mark == mark)


def new_observations(before: Regime, after: Regime) -> frozenset[Observation]:
    """Judgments holding in ``after`` that did not hold in ``before``."""
    return observations(after) - observations(before)


# ---------------------------------------------------------------------------
# Renaming and the reflection
# ---------------------------------------------------------------------------


def reflect(r: Regime) -> Regime:
    """Exchange the two sides.  Under ``U`` this is a renaming the object
    language cannot see; under ``O`` it is not a renaming, because the
    names are admitted, and the result is a different regime whenever any
    mark is placed."""
    return Regime(
        r.reading,
        r.marks,
        tuple(1 - s for s in r.placement),
        r.initial_datum,
    )


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
    return Regime(r.reading, tuple(marks), tuple(placement), r.initial_datum)


def serialize(r: Regime) -> tuple[object, ...]:
    """Tokens forgotten; reading and placement kept.

    The one initial datum is omitted because validation fixes it identically
    in every Challenge 0 regime.
    """
    return (r.reading, r.placement)


def canonical(r: Regime) -> tuple[object, ...]:
    """The minimum serialization over every mark permutation, and under
    ``U`` also over the side exchange.

    Invariance and class separation are checked only at the finite census
    bounds reported by Challenge 0; no unbounded completeness theorem for
    this key is claimed.
    """
    candidates = [r] + ([reflect(r)] if r.reading == READING_U else [])
    best: tuple[object, ...] | None = None
    for base in candidates:
        for pi in permutations(range(base.n_marks())):
            key = serialize(rename_marks(base, pi))
            if best is None or key < best:
                best = key
    assert best is not None
    return best


def permitted_images(r: Regime) -> list[tuple[bool, tuple[int, ...], Regime]]:
    """Every regime a permitted renaming reaches from ``r``, with the renaming.

    Each entry is ``(reflected, permutation, image)``.  Mark permutations are
    permitted under both readings; the side exchange only under ``U``.  This
    is the unpruned enumeration that ``canonical`` minimizes over.
    """
    bases = [(False, r)] + ([(True, reflect(r))] if r.reading == READING_U else [])
    return [
        (reflected, tuple(pi), rename_marks(base, pi))
        for reflected, base in bases
        for pi in permutations(range(r.n_marks()))
    ]


def isomorphism_witness(
    a: Regime, b: Regime
) -> tuple[bool, tuple[int, ...]] | None:
    """A permitted renaming carrying ``a`` onto ``b`` with tokens forgotten,
    found by unpruned search, or ``None``.  Regimes of different readings are
    never isomorphic."""
    if a.reading != b.reading:
        return None
    target = serialize(b)
    for reflected, pi, image in permitted_images(a):
        if serialize(image) == target:
            return (reflected, pi)
    return None


def is_isomorphic(a: Regime, b: Regime) -> bool:
    """The implemented isomorphism relation: a permitted renaming exists."""
    return isomorphism_witness(a, b) is not None


def fixed_up_to_mark_renaming(r: Regime) -> bool:
    """Whether reflection stabilizes this placement after a mark renaming.

    This is stricter than asking whether ``r`` and ``reflect(r)`` have the
    same canonical orbit key: under U the canonical quotient identifies every
    reflected pair, including one-mark placements that reflection does not
    stabilize.
    """

    target = serialize(r)
    reflected = reflect(r)
    return any(
        serialize(rename_marks(reflected, pi)) == target
        for pi in permutations(range(r.n_marks()))
    )


def is_automorphism_reflection(r: Regime) -> bool:
    """Whether reflection is permitted and stabilizes this regime.

    Under ``O`` reflection is not permitted, even at the raw fixed point of
    genesis.  Under U, orbit equivalence alone is insufficient: reflection
    must fix the placement up to a mark renaming.  ``reflect(r) == r`` and
    canonical orbit equivalence are reported separately.
    """
    if r.reading == READING_O:
        return False
    return fixed_up_to_mark_renaming(r)
