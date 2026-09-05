"""The mirror: this tree's own re-declaration of a side-typed carrier.

Classification: COUNTERMODEL — specifically, a countermodel-DOMAIN object.

It exists for two jobs and no others.  It is the domain over which the
forgetful lemma and the two censuses are stated, and it is the second row of
the shared table so that the comparison is one enumerator over two carriers
rather than two runs compared by hand.

**It is never claimed to be the pinned carrier.**  It is a re-declaration
made from the pinned source, and if it diverged from that source the lemma
would be about a different object.  Gate ``G6`` therefore pins it against the
pinned receipt's whole published vector — every one of the 48 point rows per
reading — and a divergence VOIDS the run rather than adjusting it.  The
load-bearing tie between this tree and the pinned world remains ``G4``, which
uses no re-declaration at all: it replays this tree's own verdict function
against the pinned world's own recorded automorphism sets.

Nothing here is admitted.  Every regime is the replay of an explicit history
from genesis, and every augmentation is a declared candidate that applies
nothing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from itertools import permutations, product
from typing import Callable, Sequence

from sidefree.enumerate import Json, key_json
from sidefree.model import Regime as SideFreeRegime
from sidefree.model import automorphisms_under as side_free_automorphisms_under
from sidefree.model import marks_separable_under as side_free_marks_separable_under
from sidefree.requirement import RETAINED_MARKS, separates

READING_U = "U"
READING_O = "O"
READINGS: tuple[str, str] = (READING_U, READING_O)
SIDE_NAMES: tuple[str, str] = ("near", "far")

SUPPLIED_TOKEN = "a"
RELABELLED_TOKEN = "z"
INSCRIPTIONS: tuple[str, str] = ("<a|>", "<|a>")
PROPERTY_LABELS: tuple[str, str] = (SUPPLIED_TOKEN, RELABELLED_TOKEN)
PROPERTY_DOMAIN_MAX_MARKS = 3
LEMMA_CENSUS_MAX_MARKS = 3


class MirrorError(ValueError):
    """An event or a text is ill-formed relative to the mirror declaration."""


@dataclass(frozen=True)
class OpaqueDatum:
    internal_id: int


INITIAL_DATUM = OpaqueDatum(0)


@dataclass(frozen=True)
class Regime:
    """A side-typed regime: a reading, the marks' labels, and their placement."""

    reading: str
    marks: tuple[str, ...]
    placement: tuple[int, ...]
    initial_datum: OpaqueDatum = INITIAL_DATUM

    def __post_init__(self) -> None:
        if self.reading not in READINGS:
            raise MirrorError(f"unknown reading: {self.reading!r}")
        if self.initial_datum != INITIAL_DATUM:
            raise MirrorError("the supplied initial datum is fixed")
        if len(self.marks) != len(self.placement):
            raise MirrorError("marks and placement must have equal length")
        if any(s not in (0, 1) for s in self.placement):
            raise MirrorError("every admitted mark must lie on side 0 or 1")

    def n_marks(self) -> int:
        return len(self.marks)


def genesis(reading: str) -> Regime:
    return Regime(reading, (), ())


@dataclass(frozen=True)
class Supply:
    token: str


@dataclass(frozen=True)
class AdmitMark:
    token: str
    side: int


@dataclass(frozen=True)
class AdmitOccurrence:
    token: str
    side: int


Event = Supply | AdmitMark | AdmitOccurrence


def step(r: Regime, e: Event) -> Regime:
    if isinstance(e, Supply):
        return r
    if e.side not in (0, 1):
        raise MirrorError(f"side must be 0 or 1, got {e.side}")
    if isinstance(e, AdmitOccurrence):
        return Regime(r.reading, r.marks + (e.token,), r.placement + (e.side,))
    if r.marks.count(e.token) > 1:
        raise MirrorError(
            f"label {e.token!r} names more than one admitted mark; the "
            f"token-keyed admission cannot say which and is refused"
        )
    if e.token in r.marks:
        held = r.placement[r.marks.index(e.token)]
        if held != e.side:
            raise MirrorError(
                f"mark {e.token!r} is admitted on side {held}; an admission "
                f"naming side {e.side} would move it and is refused"
            )
        return r
    return Regime(r.reading, r.marks + (e.token,), r.placement + (e.side,))


def replay(history: Sequence[Event], base: Regime) -> Regime:
    r = base
    supplied: set[str] = set()
    for e in history:
        if isinstance(e, Supply):
            supplied.add(e.token)
        elif isinstance(e, AdmitOccurrence):
            if e.token not in supplied:
                raise MirrorError(
                    f"occurrence {e.token!r} was not supplied before admission"
                )
        elif e.token not in supplied and e.token not in r.marks:
            raise MirrorError(f"mark {e.token!r} was not supplied before admission")
        r = step(r, e)
    return r


def certify(history: Sequence[Event], base: Regime, claimed: Regime) -> bool:
    try:
        return replay(history, base) == claimed
    except MirrorError:
        return False


def event_follows(_r: Regime, _e: Event) -> bool:
    return False


# ---------------------------------------------------------------------------
# Presentation, with the convention this world still has
# ---------------------------------------------------------------------------

PRESENTED_SIDES: tuple[str, str] = ("left", "right")
CONVENTIONS: dict[str, dict[str, int]] = {
    "left is side 0": {"left": 0, "right": 1},
    "left is side 1": {"left": 1, "right": 0},
}
DECLARED_CONVENTION = "left is side 0"
OTHER_CONVENTION = "left is side 1"

_WHOLE = re.compile(r"^<([a-z]*)\|([a-z]*)>$")


@dataclass(frozen=True)
class Whole:
    token: str | None
    presented_side: str | None


def read_whole(text: str) -> Whole:
    m = _WHOLE.match(text)
    if m is None:
        raise MirrorError(f"not a whole with one bar and at most one mark: {text!r}")
    left, right = m.group(1), m.group(2)
    if len(left) + len(right) > 1:
        raise MirrorError(f"more than one mark is beyond the bound: {text!r}")
    if left:
        return Whole(left, "left")
    if right:
        return Whole(right, "right")
    return Whole(None, None)


def admitted_side(presented_side: str, convention: str) -> int:
    if convention not in CONVENTIONS:
        raise MirrorError(f"unknown convention: {convention!r}")
    if presented_side not in PRESENTED_SIDES:
        raise MirrorError(f"unknown presented side: {presented_side!r}")
    return CONVENTIONS[convention][presented_side]


def caller_wholes() -> list[Whole]:
    return [read_whole(text) for text in INSCRIPTIONS]


# ---------------------------------------------------------------------------
# Observation
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OnSide:
    mark: int
    side: int


@dataclass(frozen=True)
class SideNamed:
    side: int
    name: str


Observation = OnSide | SideNamed


def observation_holds(r: Regime, judgment: Observation) -> bool:
    if isinstance(judgment, OnSide):
        return judgment.mark < r.n_marks() and r.placement[judgment.mark] == judgment.side
    return r.reading == READING_O and SIDE_NAMES[judgment.side] == judgment.name


def mark_observations(r: Regime) -> frozenset[OnSide]:
    return frozenset(OnSide(i, s) for i, s in enumerate(r.placement))


# ---------------------------------------------------------------------------
# Renaming, keys, and the flagged family
# ---------------------------------------------------------------------------


def reflect(r: Regime) -> Regime:
    return Regime(
        r.reading, r.marks, tuple(1 - s for s in r.placement), r.initial_datum
    )


def rename_marks(r: Regime, pi: Sequence[int]) -> Regime:
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
    return (r.reading, r.placement)


def serialize_keeping_labels(r: Regime) -> tuple[object, ...]:
    return (r.reading, r.marks, r.placement)


def key_of(r: Regime, keep_labels: bool) -> tuple[object, ...]:
    return serialize_keeping_labels(r) if keep_labels else serialize(r)


def permitted_images_under(
    r: Regime, reflection: bool, mark_permutations: bool
) -> list[tuple[bool, tuple[int, ...], Regime]]:
    n = r.n_marks()
    perms = list(permutations(range(n))) if mark_permutations else [tuple(range(n))]
    bases = [(False, r)] + ([(True, reflect(r))] if reflection else [])
    return [
        (reflected, tuple(pi), rename_marks(base, pi))
        for reflected, base in bases
        for pi in perms
    ]


def automorphisms_under(
    r: Regime, reflection: bool, mark_permutations: bool, keep_labels: bool
) -> list[tuple[bool, tuple[int, ...]]]:
    target = key_of(r, keep_labels)
    return [
        (reflected, pi)
        for reflected, pi, image in permitted_images_under(
            r, reflection, mark_permutations
        )
        if key_of(image, keep_labels) == target
    ]


def marks_separable_under(
    r: Regime,
    i: int,
    j: int,
    reflection: bool,
    mark_permutations: bool,
    keep_labels: bool,
) -> bool:
    """The requirement at this regime, by the ONE shared verdict function."""
    return separates(
        [pi for _reflected, pi in automorphisms_under(r, reflection, mark_permutations, keep_labels)],
        i,
        j,
    )


def side_exchanging_automorphism_under(
    r: Regime, reflection: bool, mark_permutations: bool, keep_labels: bool
) -> tuple[bool, tuple[int, ...]] | None:
    for reflected, pi in automorphisms_under(r, reflection, mark_permutations, keep_labels):
        if reflected:
            return (reflected, pi)
    return None


def is_isomorphic_under(
    a: Regime, b: Regime, reflection: bool, mark_permutations: bool, keep_labels: bool
) -> bool:
    if a.reading != b.reading:
        return False
    target = key_of(b, keep_labels)
    return any(
        key_of(image, keep_labels) == target
        for _reflected, _pi, image in permitted_images_under(
            a, reflection, mark_permutations
        )
    )


def canonical_under(
    r: Regime, reflection: bool, mark_permutations: bool, keep_labels: bool
) -> tuple[object, ...]:
    keys = [
        key_of(image, keep_labels)
        for _reflected, _pi, image in permitted_images_under(r, reflection, mark_permutations)
    ]
    return min(keys, key=repr)


def mark_orbit_under(
    r: Regime, mark: int, reflection: bool, mark_permutations: bool, keep_labels: bool
) -> frozenset[tuple[str, int]]:
    return frozenset(
        (repr(key_of(image, keep_labels)), pi[mark])
        for _reflected, pi, image in permitted_images_under(
            r, reflection, mark_permutations
        )
    )


def no_permitted_renaming_moves_an_index(
    r: Regime, reflection: bool, mark_permutations: bool
) -> bool:
    identity = tuple(range(r.n_marks()))
    return all(
        pi == identity
        for _reflected, pi, _image in permitted_images_under(
            r, reflection, mark_permutations
        )
    )


# ---------------------------------------------------------------------------
# The pinned five-coordinate candidate space
# ---------------------------------------------------------------------------

COORDINATES: tuple[str, ...] = (
    "withdraw_reflection",
    "withdraw_mark_permutations",
    "admit_names",
    "keep_labels",
    "extra_mark",
)
EXTRA_MARK_VALUES: tuple[int | None, int, int] = (None, 0, 1)

CAPABILITY_OF: dict[str, str] = {
    "withdraw_reflection": (
        "the side exchange is not a permitted renaming: the two sides are "
        "declared distinguishable, which is the part of the O reading that "
        "reading U does not carry"
    ),
    "withdraw_mark_permutations": (
        "a mark's admission index is internally available: the metatheoretic "
        "name definition 3 assigns is declared to be an internal designation"
    ),
    "admit_names": (
        "the two sides carry admitted names, so the judgment grammar of the "
        "reading gains the side-name form"
    ),
    "keep_labels": (
        "a mark's presentation label is internally available: the token "
        "forgetting of definition 14 is withdrawn"
    ),
    "extra_mark": (
        "the process extends the caller's history with an admission of its "
        "own, rather than replaying only what the caller supplied and admitted"
    ),
}

COLLATERAL_FACTS: tuple[str, ...] = (
    "sides_internally_separable",
    "order_internally_available",
    "label_internally_available",
    "convention_internally_available",
    "side_names_hold",
)
RESTRICTED_FACTS: tuple[str, ...] = (
    "order_internally_available",
    "label_internally_available",
)


@dataclass(frozen=True)
class Augmentation:
    withdraw_reflection: bool = False
    withdraw_mark_permutations: bool = False
    admit_names: bool = False
    keep_labels: bool = False
    extra_mark: int | None = None

    def values(self) -> tuple[object, ...]:
        return (
            self.withdraw_reflection,
            self.withdraw_mark_permutations,
            self.admit_names,
            self.keep_labels,
            self.extra_mark,
        )


NULL_AUGMENTATION = Augmentation()
READING_O_BUNDLE = Augmentation(withdraw_reflection=True, admit_names=True)


def candidate_space() -> list[Augmentation]:
    return [
        Augmentation(wr, wp, an, kl, em)
        for wr in (False, True)
        for wp in (False, True)
        for an in (False, True)
        for kl in (False, True)
        for em in EXTRA_MARK_VALUES
    ]


def changed_coordinates(aug: Augmentation) -> list[str]:
    moved: list[str] = []
    if aug.withdraw_reflection:
        moved.append("withdraw_reflection")
    if aug.withdraw_mark_permutations:
        moved.append("withdraw_mark_permutations")
    if aug.admit_names:
        moved.append("admit_names")
    if aug.keep_labels:
        moved.append("keep_labels")
    if aug.extra_mark is not None:
        moved.append("extra_mark")
    return moved


def point_name(aug: Augmentation) -> str:
    moved = changed_coordinates(aug)
    if not moved:
        return "base"
    parts = [
        f"extra_mark_{aug.extra_mark}" if name == "extra_mark" else name
        for name in moved
    ]
    return "+".join(parts)


def reflection_permitted(reading: str, aug: Augmentation) -> bool:
    return reading == READING_U and not aug.withdraw_reflection


def mark_permutations_permitted(aug: Augmentation) -> bool:
    return not aug.withdraw_mark_permutations


def names_admitted(reading: str, aug: Augmentation) -> bool:
    return reading == READING_O or aug.admit_names


def flags(reading: str, aug: Augmentation) -> tuple[bool, bool, bool]:
    return (
        reflection_permitted(reading, aug),
        mark_permutations_permitted(aug),
        aug.keep_labels,
    )


def effective_structure(reading: str, aug: Augmentation) -> list[str]:
    return [
        str(part)
        for part in (
            reflection_permitted(reading, aug),
            mark_permutations_permitted(aug),
            names_admitted(reading, aug),
            aug.keep_labels,
        )
    ]


def caller_history(wholes: Sequence[Whole], convention: str) -> list[Event]:
    history: list[Event] = []
    for whole in wholes:
        if whole.token is None or whole.presented_side is None:
            raise MirrorError("a whole with no mark cannot be retained")
        history.append(Supply(whole.token))
        history.append(
            AdmitOccurrence(whole.token, admitted_side(whole.presented_side, convention))
        )
    return history


def process_admission(aug: Augmentation) -> list[Event]:
    if aug.extra_mark is None:
        return []
    return [AdmitOccurrence(SUPPLIED_TOKEN, aug.extra_mark)]


def candidate_history(
    wholes: Sequence[Whole], aug: Augmentation, convention: str, order_reversed: bool
) -> list[Event]:
    presented = list(reversed(list(wholes))) if order_reversed else list(wholes)
    return caller_history(presented, convention) + process_admission(aug)


def relabelled(r: Regime) -> Regime:
    return Regime(r.reading, tuple(RELABELLED_TOKEN for _ in r.marks), r.placement)


def comparison_regimes(
    reading: str, wholes: Sequence[Whole], aug: Augmentation
) -> tuple[Regime, Regime, Regime, Regime]:
    g = genesis(reading)
    main = replay(candidate_history(wholes, aug, DECLARED_CONVENTION, False), g)
    other_order = replay(candidate_history(wholes, aug, DECLARED_CONVENTION, True), g)
    other_convention = replay(candidate_history(wholes, aug, OTHER_CONVENTION, False), g)
    return (main, other_order, relabelled(main), other_convention)


def collateral_facts(
    reading: str, aug: Augmentation, wholes: Sequence[Whole]
) -> dict[str, bool]:
    main, other_order, relabel, other_convention = comparison_regimes(
        reading, wholes, aug
    )
    fl = flags(reading, aug)
    return {
        "sides_internally_separable": side_exchanging_automorphism_under(main, *fl)
        is None,
        "order_internally_available": not is_isomorphic_under(main, other_order, *fl),
        "label_internally_available": not is_isomorphic_under(main, relabel, *fl),
        "convention_internally_available": not is_isomorphic_under(
            main, other_convention, *fl
        ),
        "side_names_hold": names_admitted(reading, aug),
    }


# ---------------------------------------------------------------------------
# Mark properties
# ---------------------------------------------------------------------------

MarkProperty = Callable[[Regime, int], bool]


def on_side_0(r: Regime, i: int) -> bool:
    return observation_holds(r, OnSide(i, 0))


def on_side_1(r: Regime, i: int) -> bool:
    return observation_holds(r, OnSide(i, 1))


def has_index_0(_r: Regime, i: int) -> bool:
    return i == 0


def has_index_1(_r: Regime, i: int) -> bool:
    return i == 1


def carries_label_a(r: Regime, i: int) -> bool:
    return i < r.n_marks() and r.marks[i] == SUPPLIED_TOKEN


DECLARED_MARK_PROPERTIES: tuple[tuple[str, MarkProperty], ...] = (
    ("on_side_0", on_side_0),
    ("on_side_1", on_side_1),
    ("has_index_0", has_index_0),
    ("has_index_1", has_index_1),
    ("carries_label_a", carries_label_a),
)

DomainImages = list[tuple[Regime, list[tuple[bool, tuple[int, ...], Regime]]]]


def property_domain(reading: str, max_marks: int) -> list[Regime]:
    return [
        Regime(reading, labels, placement)
        for n in range(max_marks + 1)
        for labels in product(PROPERTY_LABELS, repeat=n)
        for placement in product((0, 1), repeat=n)
    ]


def domain_images(
    domain: Sequence[Regime], reflection: bool, mark_permutations: bool
) -> DomainImages:
    return [
        (r, permitted_images_under(r, reflection, mark_permutations)) for r in domain
    ]


def property_invariant(prop: MarkProperty, images: DomainImages) -> bool:
    return all(
        prop(image, pi[i]) == prop(r, i)
        for r, entries in images
        for _reflected, pi, image in entries
        for i in range(r.n_marks())
    )


def property_separates(prop: MarkProperty, r: Regime) -> bool:
    i, j = RETAINED_MARKS
    return prop(r, i) != prop(r, j)


# ---------------------------------------------------------------------------
# The forgetting map and the forgetful lemma
# ---------------------------------------------------------------------------


def forget(r: Regime) -> SideFreeRegime:
    """Forget the reading and the placement; keep the marks in their order.

    This is the map the lemma is about.  It is total, and it is the only
    bridge between the two carriers.
    """
    return SideFreeRegime(r.marks)


def side_free_permutations(
    r: Regime, mark_permutations: bool, keep_labels: bool, inject_side: bool
) -> list[tuple[int, ...]]:
    """The permutations the side-free world admits as automorphisms.

    ``inject_side`` is the INJECTION and is false in every live run: it
    re-admits the placement into the side-free key as a per-mark two-valued
    attribute, which is exactly the substitute the lemma exists to catch.
    """
    if inject_side:
        return [
            pi
            for _reflected, pi in automorphisms_under(
                r, False, mark_permutations, keep_labels
            )
        ]
    return side_free_automorphisms_under(forget(r), mark_permutations, keep_labels)


def lemma_cells() -> list[tuple[Regime, bool, bool, bool]]:
    """The declared lemma census, in the declared iteration order.

    Reading, then mark count ascending, then labels in the order the two
    declared labels are taken, then placement in ascending tuple order, then
    ``withdraw_reflection``, then ``mark_permutations``, then ``keep_labels``,
    each false before true.  The order is declared so that "the first
    violating cell" is determined.
    """
    return [
        (Regime(reading, labels, placement), wr, mp, kl)
        for reading in READINGS
        for n in range(1, LEMMA_CENSUS_MAX_MARKS + 1)
        for labels in product(PROPERTY_LABELS, repeat=n)
        for placement in product((0, 1), repeat=n)
        for wr in (False, True)
        for mp in (False, True)
        for kl in (False, True)
    ]


def forgetful_lemma(inject_side: bool = False) -> Json:
    """The lemma, its corollary, and two counts over the full census.

    Every side-typed automorphism of a mirror regime must have its
    permutation admitted as an automorphism of the forgotten regime under the
    transferred flags.  A violation names the cell and the offending
    renaming.  The corollary then says side-free separation implies
    side-typed separation at every cell of two or more marks.

    The two counts measure different things and neither substitutes for the
    other.  ``corollary_antecedent_cells`` counts the cells where the
    side-free world separates -- where the corollary's antecedent HOLDS, so
    it is the count that says the implication is not empty.
    ``converse_failure_cells`` counts the cells where the side-typed world
    separates and the forgotten one does not: there the antecedent FAILS and
    the corollary asserts nothing, so it measures the converse's failure --
    that forgetting really does lose separations -- and not the corollary's
    non-vacuity.  An earlier version of this function reported the second
    count alone, under the first count's name.
    """
    checked = 0
    violations: list[Json] = []
    corollary_violations: list[Json] = []
    antecedent_cells = 0
    converse_failures = 0
    cells = lemma_cells()
    i, j = RETAINED_MARKS
    for r, wr, mp, kl in cells:
        reflection = reflection_permitted(r.reading, Augmentation(withdraw_reflection=wr))
        free = set(side_free_permutations(r, mp, kl, inject_side))
        for reflected, pi in automorphisms_under(r, reflection, mp, kl):
            checked += 1
            if pi not in free:
                violations.append(
                    {
                        "reading": r.reading,
                        "labels": list(r.marks),
                        "placement": list(r.placement),
                        "withdraw_reflection": wr,
                        "mark_permutations": mp,
                        "keep_labels": kl,
                        "automorphism": {"reflected": reflected, "permutation": list(pi)},
                    }
                )
        if r.n_marks() >= 2:
            sided = marks_separable_under(r, i, j, reflection, mp, kl)
            free_sep = separates(side_free_permutations(r, mp, kl, inject_side), i, j)
            if free_sep and not sided:
                corollary_violations.append(
                    {
                        "reading": r.reading,
                        "labels": list(r.marks),
                        "placement": list(r.placement),
                        "withdraw_reflection": wr,
                        "mark_permutations": mp,
                        "keep_labels": kl,
                    }
                )
            if free_sep:
                antecedent_cells += 1
            if sided and not free_sep:
                converse_failures += 1
    return {
        "cells": len(cells),
        "automorphisms_checked": checked,
        "violations": len(violations),
        "first_violation": violations[0] if violations else None,
        "corollary_violations": len(corollary_violations),
        "first_corollary_violation": (
            corollary_violations[0] if corollary_violations else None
        ),
        "corollary_antecedent_cells": antecedent_cells,
        "converse_failure_cells": converse_failures,
        "holds": not violations,
        "corollary_holds": not corollary_violations,
        "corollary_non_vacuous": antecedent_cells > 0,
        "forgetting_loses_separation": converse_failures > 0,
        "injection_live": inject_side,
    }


def withdrawal_census(mark_permutations: bool) -> list[bool]:
    """The declared withdrawal census of this world: 64 cells.

    The two declared labels in each of the two retained positions, each
    reading, each ``keep_labels`` value, and each placement.  The parameter is
    the coordinate under measurement; the side exchange follows the reading.
    """
    i, j = RETAINED_MARKS
    return [
        marks_separable_under(
            Regime(reading, tuple(labels), tuple(placement)),
            i,
            j,
            reading == READING_U,
            mark_permutations,
            kl,
        )
        for labels in product(PROPERTY_LABELS, repeat=2)
        for reading in READINGS
        for kl in (False, True)
        for placement in product((0, 1), repeat=2)
    ]


def route_census_regimes(reading: str, aug: Augmentation) -> list[Regime]:
    """This world's own two-mark configuration domain for one candidate."""
    extra_labels = (SUPPLIED_TOKEN,) if aug.extra_mark is not None else ()
    extra_placement = (aug.extra_mark,) if aug.extra_mark is not None else ()
    return [
        Regime(
            reading,
            tuple(labels) + extra_labels,
            tuple(placement) + tuple(int(s) for s in extra_placement),
        )
        for labels in product(PROPERTY_LABELS, repeat=2)
        for placement in product((0, 1), repeat=2)
    ]


# ---------------------------------------------------------------------------
# The mirror's view for the generic enumerator
# ---------------------------------------------------------------------------


def event_json(e: Event) -> Json:
    if isinstance(e, Supply):
        return {"kind": "Supply", "token": e.token}
    return {"kind": type(e).__name__, "side": e.side, "token": e.token}


def probes(token: str) -> list[Event]:
    return [
        Supply(token),
        AdmitMark(token, 0),
        AdmitMark(token, 1),
        AdmitOccurrence(token, 0),
        AdmitOccurrence(token, 1),
    ]


class MirrorCarrier:
    """One reading of the side-typed world, as the generic enumerator sees it."""

    coordinates = COORDINATES
    collateral_fact_names = COLLATERAL_FACTS
    restricted_fact_names = RESTRICTED_FACTS

    def __init__(self, reading: str) -> None:
        if reading not in READINGS:
            raise MirrorError(f"unknown reading: {reading!r}")
        self.reading = reading
        self.world = "unnamed" if reading == READING_U else "named"
        self._wholes = caller_wholes()
        domain = property_domain(reading, PROPERTY_DOMAIN_MAX_MARKS)
        self._images: dict[tuple[bool, bool], DomainImages] = {
            (refl, mp): domain_images(domain, refl, mp)
            for refl in (False, True)
            for mp in (False, True)
        }

    def _aug(self, aug: object) -> Augmentation:
        if not isinstance(aug, Augmentation):
            raise TypeError(f"not a candidate of this world: {aug!r}")
        return aug

    def _main(self, aug: object) -> Regime:
        main, _o, _l, _c = comparison_regimes(self.reading, self._wholes, self._aug(aug))
        return main

    def _events(self, aug: object) -> list[Event]:
        return candidate_history(
            self._wholes, self._aug(aug), DECLARED_CONVENTION, False
        )

    def points(self) -> list[object]:
        return list(candidate_space())

    def base_point(self) -> object:
        return NULL_AUGMENTATION

    def point_name(self, aug: object) -> str:
        return point_name(self._aug(aug))

    def coordinate_values(self, aug: object) -> Json:
        return dict(zip(COORDINATES, self._aug(aug).values()))

    def changed_coordinates(self, aug: object) -> list[str]:
        return changed_coordinates(self._aug(aug))

    def capability_of(self, name: str) -> str:
        return CAPABILITY_OF[name]

    def history(self, aug: object) -> list[Json]:
        return [event_json(e) for e in self._events(aug)]

    def certified(self, aug: object) -> bool:
        return certify(self._events(aug), genesis(self.reading), self._main(aug))

    def replays_from_genesis(self, aug: object) -> bool:
        return replay(self._events(aug), genesis(self.reading)) == self._main(aug)

    def initial_datum_unchanged(self, aug: object) -> bool:
        return self._main(aug).initial_datum == genesis(self.reading).initial_datum

    def event_follows_relation_empty(self, aug: object) -> bool:
        main = self._main(aug)
        return all(not event_follows(main, e) for e in probes(SUPPLIED_TOKEN))

    def n_marks(self, aug: object) -> int:
        return self._main(aug).n_marks()

    def labels(self, aug: object) -> list[str]:
        return list(self._main(aug).marks)

    def permitted_renamings(self, aug: object) -> Json:
        a = self._aug(aug)
        refl, mp, kl = flags(self.reading, a)
        return {
            "side_exchange": refl,
            "mark_permutations": mp,
            "labels_kept": kl,
            "names_admitted": names_admitted(self.reading, a),
            "images": len(permitted_images_under(self._main(aug), refl, mp)),
        }

    def automorphism_entries(self, aug: object) -> list[Json]:
        refl, mp, kl = flags(self.reading, self._aug(aug))
        return [
            {"reflected": reflected, "permutation": list(pi)}
            for reflected, pi in automorphisms_under(self._main(aug), refl, mp, kl)
        ]

    def carrier_separability(self, aug: object) -> bool:
        refl, mp, kl = flags(self.reading, self._aug(aug))
        i, j = RETAINED_MARKS
        return marks_separable_under(self._main(aug), i, j, refl, mp, kl)

    def satisfies_second_reading(self, aug: object) -> bool:
        refl, mp, kl = flags(self.reading, self._aug(aug))
        main = self._main(aug)
        i, j = RETAINED_MARKS
        return (repr(key_of(main, kl)), j) not in mark_orbit_under(main, i, refl, mp, kl)

    def orbit_size(self, aug: object) -> int:
        refl, mp, kl = flags(self.reading, self._aug(aug))
        i, _j = RETAINED_MARKS
        return len(mark_orbit_under(self._main(aug), i, refl, mp, kl))

    def no_permitted_renaming_moves_an_index(self, aug: object) -> bool:
        refl, mp, _kl = flags(self.reading, self._aug(aug))
        return no_permitted_renaming_moves_an_index(self._main(aug), refl, mp)

    def effective_structure(self, aug: object) -> list[str]:
        return effective_structure(self.reading, self._aug(aug))

    def canonical_key(self, aug: object) -> object:
        refl, mp, kl = flags(self.reading, self._aug(aug))
        return key_json(canonical_under(self._main(aug), refl, mp, kl))

    def collateral_facts(self, aug: object) -> dict[str, bool]:
        return collateral_facts(self.reading, self._aug(aug), self._wholes)

    def mark_property_facts(self, aug: object) -> dict[str, list[str]]:
        a = self._aug(aug)
        refl, mp, _kl = flags(self.reading, a)
        main = self._main(aug)
        images = self._images[(refl, mp)]
        invariant = [
            name
            for name, prop in DECLARED_MARK_PROPERTIES
            if property_invariant(prop, images)
        ]
        separating = [
            name
            for name, prop in DECLARED_MARK_PROPERTIES
            if property_separates(prop, main)
        ]
        return {
            "invariant_mark_properties": invariant,
            "separating_mark_properties": separating,
            "invariant_separating_mark_properties": [
                name for name in separating if name in invariant
            ],
        }

    def census_verdicts(self, aug: object) -> list[bool]:
        a = self._aug(aug)
        refl, mp, kl = flags(self.reading, a)
        i, j = RETAINED_MARKS
        return [
            marks_separable_under(r, i, j, refl, mp, kl)
            for r in route_census_regimes(self.reading, a)
        ]

    def satisfies_under_key_choice(self, aug: object) -> dict[str, bool]:
        """This world declares one key.  The key-choice question is the
        control's, and is answered there."""
        return {"pinned": self.carrier_separability(aug)}
