"""The side-free carrier: regimes, events, replay, observation, renaming.

This is the pinned carrier with the placement, the sides, and the reading
removed.  Nothing here is admitted; the tree admits no primitive at all.

Classification (assumption discipline):

* ``OpaqueDatum`` and the refusal that fixes it are the one SUPPLIED DATUM,
  inherited unchanged.  It is not a mark and its numeral lives in a different
  identity space from a mark's index.
* ``Regime`` is a DERIVED DEFINITION with one variable field.  A mark's
  internal identity is its index in ``marks``, which is the order in which it
  was admitted; the entry beside it is the presentation LABEL and may repeat.
  This is the pinned Challenge 2 declaration with the placement's index space
  replaced by the marks' own, which is legitimate because the pinned
  validator forced the two tuples to have equal length at every valid regime,
  so the two index spaces are the same set.
* ``Supply`` is an external presentation event and changes no state.
  ``AdmitMark`` and ``AdmitOccurrence`` are the only events that change
  state.  ``replay`` rebuilds a regime from an event list; every certified
  regime equals the replay of its history from genesis.
* The closed observation grammar has ONE positive judgment form,
  ``Admitted``.  The pinned grammar's side judgment is literally the
  conjunction of "the mark is admitted" and "its placement is that side", so
  ``Admitted`` is the side-free conjunct of a pinned judgment: not less than
  the pinned grammar leaves behind, and not more.  Its extension is empty at
  genesis, and a test proves it separates nothing at any census cell.
* A refusal is REMOVED AND RECORDED, not absorbed.  The pinned carrier
  refuses an admission that would move an already-admitted mark to the other
  side.  There is nowhere to move a mark to here, so the refusal has no
  side-free statement at all.  ``DELETED.md`` carries it as a removed
  refusal and the receipt reports its computed consequence.
* ``serialize`` forgets the labels and keeps the arity;
  ``serialize_keeping_labels`` is what a candidate that withdraws the
  forgetting would leave.  Which one is used is a declared FLAG of the
  candidate under examination and is never chosen by judgment.  The key
  choice itself — arity or nothing — is likewise a declared flag, and the
  receipt recomputes every verdict under both.
* Equality of regimes is structural; isomorphism is the implemented relation
  below; the two are never conflated.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from typing import Sequence, Union

from sidefree.requirement import separates

# The two declared key choices.  ``arity`` keeps the number of admitted marks;
# ``empty`` keeps nothing at all.  ``arity`` is declared because the pinned key
# keeps a tuple whose length is the arity, so both worlds get the arity free.
# Of these TWO, ``arity`` is the richer and ``empty`` the poorer, and a poorer
# key gives fewer distinctions and so more automorphisms: within this pair the
# declared choice is the more generous to this control, not the less.  What
# errs against the control is the scope the frozen design states -- the arity
# alone is the poorest DEFENSIBLE key, against richer keys that are outside
# this pair and are not declared here.  Neither declared choice is
# load-bearing, and that is DEFINITION-level rather than a computed finding:
# ``rename_marks`` permutes indices and never changes ``n_marks``, so
# ``serialize`` is constant across the images under either choice and both
# admit the same automorphisms.  The receipt still recomputes every verdict
# under both and reports the table.
KEY_CHOICES: tuple[str, str] = ("arity", "empty")
DECLARED_KEY_CHOICE = "arity"


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

    ``marks``:         for each admitted mark, in admission order, the
                       presentation token named when it was admitted.  This
                       is a LABEL and need not be unique; the mark's internal
                       identity is its index.
    ``initial_datum``: the one opaque supplied whole, implicit and unique in
                       every valid regime.  Its ``internal_id`` is not a mark
                       index.
    """

    marks: tuple[str, ...]
    initial_datum: OpaqueDatum = INITIAL_DATUM

    def __post_init__(self) -> None:
        if self.initial_datum != INITIAL_DATUM:
            raise AdmissionError("the supplied initial datum is fixed")

    def n_marks(self) -> int:
        return len(self.marks)


def genesis() -> Regime:
    """The regime before any admission.  One carrier, so no reading."""
    return Regime(())


@dataclass(frozen=True)
class Supply:
    """External presentation of a token.  Not an admission."""

    token: str


@dataclass(frozen=True)
class AdmitMark:
    """Label-keyed admission of a previously presented token.

    A no-op when the label already names exactly one mark; refused by name
    when it names more than one, because a label-keyed admission cannot say
    which mark it means there.
    """

    token: str


@dataclass(frozen=True)
class AdmitOccurrence:
    """Admission of one presented occurrence as a FRESH mark.

    The token becomes the new mark's label and is not consulted for identity:
    the mark's internal identity is its admission index.
    """

    token: str


Event = Union[Supply, AdmitMark, AdmitOccurrence]
EVENT_TYPES: tuple[type, ...] = (Supply, AdmitMark, AdmitOccurrence)
STATE_CHANGING_EVENT_KINDS: tuple[str, ...] = ("AdmitMark", "AdmitOccurrence")


def step(r: Regime, e: Event) -> Regime:
    """Apply one event to admitted state, assuming a well-formed history."""
    if isinstance(e, Supply):
        return r
    if isinstance(e, AdmitOccurrence):
        return Regime(r.marks + (e.token,), r.initial_datum)
    if r.marks.count(e.token) > 1:
        raise AdmissionError(
            f"label {e.token!r} names more than one admitted mark; the "
            f"token-keyed admission cannot say which and is refused"
        )
    if e.token in r.marks:
        return r
    return Regime(r.marks + (e.token,), r.initial_datum)


def replay(history: Sequence[Event], base: Regime) -> Regime:
    """Replay a well-formed history, refusing an admission not supplied first."""
    r = base
    supplied_tokens: set[str] = set()
    for e in history:
        if isinstance(e, Supply):
            supplied_tokens.add(e.token)
        elif isinstance(e, AdmitOccurrence):
            if e.token not in supplied_tokens:
                raise AdmissionError(
                    f"occurrence {e.token!r} was not supplied before admission"
                )
        elif e.token not in supplied_tokens and e.token not in r.marks:
            raise AdmissionError(f"mark {e.token!r} was not supplied before admission")
        r = step(r, e)
    return r


def certify(history: Sequence[Event], base: Regime, claimed: Regime) -> bool:
    """Whether the claimed regime is the replay of the history from ``base``."""
    try:
        return replay(history, base) == claimed
    except AdmissionError:
        return False


def event_follows(_r: Regime, _e: Event) -> bool:
    """The object-language transition relation is empty.

    Events may be supplied externally to ``replay``; no event is entailed by
    admitted state.  This is the declared grammar, inherited, not a discovery
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
# The observation grammar
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Admitted:
    """Positive judgment that a mark is admitted.

    The pinned side judgment is the conjunction of this and a placement test.
    This is its side-free conjunct: the honest residue of the pinned grammar,
    neither emptied nor enriched.
    """

    mark: int

    def __post_init__(self) -> None:
        if self.mark < 0:
            raise ValueError("mark identity must be nonnegative")


Observation = Admitted
OBSERVATION_TYPES: tuple[type, ...] = (Admitted,)
JUDGMENT_FORMS: tuple[str, ...] = ("Admitted",)


def observation_holds(r: Regime, judgment: Observation) -> bool:
    """Whether one judgment in the closed grammar holds."""
    return judgment.mark < r.n_marks()


def mark_observations(r: Regime) -> frozenset[Admitted]:
    """All positive mark judgments, enumerated metatheoretically."""
    return frozenset(Admitted(i) for i in range(r.n_marks()))


def observations(r: Regime) -> frozenset[Observation]:
    """All judgments in the closed grammar that hold."""
    return mark_observations(r)


def _check_mark(r: Regime, mark: int) -> None:
    if not 0 <= mark < r.n_marks():
        raise ValueError(f"mark {mark} is not admitted")


def mark_profile(r: Regime, mark: int) -> frozenset[Observation]:
    """Metatheoretic extension of the holding judgments naming one mark."""
    _check_mark(r, mark)
    return frozenset(j for j in observations(r) if j.mark == mark)


def new_observations(before: Regime, after: Regime) -> frozenset[Observation]:
    """Judgments holding in ``after`` that did not hold in ``before``."""
    return observations(after) - observations(before)


# ---------------------------------------------------------------------------
# Renaming, keys, and the flagged family
# ---------------------------------------------------------------------------


def rename_marks(r: Regime, pi: Sequence[int]) -> Regime:
    """Apply a permutation of internal identities.

    Presentation tokens travel with their marks and are forgotten by
    ``serialize``.  This is the pinned function with its placement line
    removed.
    """
    n = r.n_marks()
    if sorted(pi) != list(range(n)):
        raise ValueError("not a permutation of the admitted marks")
    marks = [""] * n
    for i in range(n):
        marks[pi[i]] = r.marks[i]
    return Regime(tuple(marks), r.initial_datum)


def serialize(r: Regime, key_choice: str = DECLARED_KEY_CHOICE) -> tuple[object, ...]:
    """Tokens forgotten.  Under the declared choice the arity is kept."""
    if key_choice == "arity":
        return (r.n_marks(),)
    if key_choice == "empty":
        return ()
    raise ValueError(f"unknown key choice: {key_choice!r}")


def serialize_keeping_labels(r: Regime) -> tuple[object, ...]:
    """The presentation labels, in admission order.

    ``serialize`` forgets them.  A declared candidate may withdraw that
    forgetting; this is what it would leave.
    """
    return (r.marks,)


def _key(
    r: Regime, keep_labels: bool, key_choice: str = DECLARED_KEY_CHOICE
) -> tuple[object, ...]:
    if keep_labels:
        return serialize_keeping_labels(r)
    return serialize(r, key_choice)


def key_of(
    r: Regime, keep_labels: bool, key_choice: str = DECLARED_KEY_CHOICE
) -> tuple[object, ...]:
    """The serialization a candidate declares.  Public face of ``_key``."""
    return _key(r, keep_labels, key_choice)


def permitted_images_under(
    r: Regime, mark_permutations: bool
) -> list[tuple[tuple[int, ...], Regime]]:
    """Every regime reached by the renamings the flag permits.  Unpruned.

    The identity permutation is always offered; the others only when
    ``mark_permutations`` is set.  There is no second generator: the pinned
    carrier's side exchange has no side-free statement.
    """
    n = r.n_marks()
    perms = list(permutations(range(n))) if mark_permutations else [tuple(range(n))]
    return [(tuple(pi), rename_marks(r, pi)) for pi in perms]


def automorphisms_under(
    r: Regime,
    mark_permutations: bool,
    keep_labels: bool,
    key_choice: str = DECLARED_KEY_CHOICE,
) -> list[tuple[int, ...]]:
    """Every renaming the flags permit that carries ``r`` onto itself."""
    target = _key(r, keep_labels, key_choice)
    return [
        pi
        for pi, image in permitted_images_under(r, mark_permutations)
        if _key(image, keep_labels, key_choice) == target
    ]


def mark_automorphism_to_under(
    r: Regime,
    i: int,
    j: int,
    mark_permutations: bool,
    keep_labels: bool,
    key_choice: str = DECLARED_KEY_CHOICE,
) -> tuple[int, ...] | None:
    """A permitted automorphism carrying mark ``i`` to mark ``j``, or ``None``."""
    _check_mark(r, i)
    _check_mark(r, j)
    for pi in automorphisms_under(r, mark_permutations, keep_labels, key_choice):
        if pi[i] == j:
            return pi
    return None


def marks_separable_under(
    r: Regime,
    i: int,
    j: int,
    mark_permutations: bool,
    keep_labels: bool,
    key_choice: str = DECLARED_KEY_CHOICE,
) -> bool:
    """The declared requirement at this regime, by the one shared verdict.

    This is ``separates`` applied to this carrier's own automorphism set.  It
    is never a second implementation of the verdict, and a test pins that.
    """
    _check_mark(r, i)
    _check_mark(r, j)
    return separates(
        automorphisms_under(r, mark_permutations, keep_labels, key_choice), i, j
    )


def is_isomorphic_under(
    a: Regime,
    b: Regime,
    mark_permutations: bool,
    keep_labels: bool,
    key_choice: str = DECLARED_KEY_CHOICE,
) -> bool:
    """Whether a renaming the flags permit carries ``a`` onto ``b``."""
    target = _key(b, keep_labels, key_choice)
    return any(
        _key(image, keep_labels, key_choice) == target
        for _pi, image in permitted_images_under(a, mark_permutations)
    )


def canonical_under(
    r: Regime,
    mark_permutations: bool,
    keep_labels: bool,
    key_choice: str = DECLARED_KEY_CHOICE,
) -> tuple[object, ...]:
    """The minimum key over every image the flags permit.

    Bounded: no unbounded completeness is claimed for this key.  The order is
    taken on ``repr`` rather than on the tuples themselves, because a tuple of
    ``object`` has no total order the type checker will accept.  Within one
    call every candidate key has the same shape and its atoms are small
    non-negative integers or single-letter labels, so the two orders agree
    there; ``G6`` checks the result against the pinned class keys rather than
    trusting that argument.
    """
    keys = [
        _key(image, keep_labels, key_choice)
        for _pi, image in permitted_images_under(r, mark_permutations)
    ]
    return min(keys, key=repr)


def mark_orbit_under(
    r: Regime,
    mark: int,
    mark_permutations: bool,
    keep_labels: bool,
    key_choice: str = DECLARED_KEY_CHOICE,
) -> frozenset[tuple[str, int]]:
    """The images of one mark under every renaming the flags permit.

    Each element pairs the key of an image regime with the index the mark is
    carried to.  Membership is a property of a ``(regime, mark)`` pair
    invariant under those renamings by construction, so it is the witness the
    second reading of the requirement asks for.
    """
    _check_mark(r, mark)
    return frozenset(
        (repr(_key(image, keep_labels, key_choice)), pi[mark])
        for pi, image in permitted_images_under(r, mark_permutations)
    )


def no_permitted_renaming_moves_an_index(r: Regime, mark_permutations: bool) -> bool:
    """Whether every permitted renaming is the identity permutation.

    COMPUTED, never asserted.  When it holds, the requirement is met by
    unfolding the declaration rather than by a fact about the regime, and the
    receipt says so beside the verdict.
    """
    identity = tuple(range(r.n_marks()))
    return all(pi == identity for pi, _image in permitted_images_under(r, mark_permutations))
