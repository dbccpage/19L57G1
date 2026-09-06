"""The declared candidate space of the side-free world, and its carrier view.

Classification (assumption discipline):

* ``COORDINATES``, ``CAPABILITY_OF``, ``Augmentation``, ``mu1``, ``mu2`` and
  the class key are DERIVED DEFINITIONS.  An augmentation applies nothing: a
  candidate becomes a regime only through ``replay`` of an explicit history,
  and it becomes a renaming set only by being handed to the kernel's flagged
  enumerations.
* ``INSCRIPTIONS`` are the SUPPLIED DATUM: the caller's two presented wholes,
  inherited unchanged.
* The deletion criterion is METATHEORY APPARATUS and is MECHANICAL: a pinned
  coordinate transfers exactly when its pinned capability sentence contains
  no whole word "side" or "sides".  ``transfers`` implements it; a test
  applies it to the five sentences of the vendored receipt and requires the
  partition it induces to equal ``COORDINATES``.
* The three surviving capability sentences are carried BYTE-IDENTICAL from
  the pinned receipt, and gate ``G3`` asserts that.  Their names are
  string-identical to the pinned names, so the cross-world join is by
  equality and a rename fails the join by name rather than dropping a route.
* ``extra_mark`` collapses from three pinned values to two.  This is the
  SINGLE value-set change of the whole deletion and is flagged as such,
  because it is the one place a second deletion could hide.  It is read from
  the pin, not asserted: the two pinned further-mark points carry one class
  key and stand as the two members of one retained class.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from itertools import product
from typing import Callable, Sequence

from sidefree.enumerate import Json, key_json
from sidefree.model import (
    DECLARED_KEY_CHOICE,
    KEY_CHOICES,
    Admitted,
    AdmitMark,
    AdmitOccurrence,
    AdmissionError,
    Event,
    Regime,
    Supply,
    automorphisms_under,
    canonical_under,
    certify,
    event_follows,
    genesis,
    is_isomorphic_under,
    key_of,
    mark_orbit_under,
    marks_separable_under,
    no_permitted_renaming_moves_an_index,
    observation_holds,
    permitted_images_under,
    replay,
)
from sidefree.presentation import Whole, read_whole
from sidefree.requirement import RETAINED_MARKS

SUPPLIED_TOKEN = "a"
RELABELLED_TOKEN = "z"
INSCRIPTIONS: tuple[str, str] = ("<a|>", "<|a>")
PROPERTY_LABELS: tuple[str, str] = (SUPPLIED_TOKEN, RELABELLED_TOKEN)
PROPERTY_DOMAIN_MAX_MARKS = 3

# The three pinned coordinates whose capability sentence names no side.  The
# order is the pinned order with the two deleted coordinates removed.
COORDINATES: tuple[str, ...] = (
    "withdraw_mark_permutations",
    "keep_labels",
    "extra_mark",
)

# Byte-identical to `candidate_space.capability_of` in the vendored receipt.
# Gate G3 asserts it.
CAPABILITY_OF: dict[str, str] = {
    "withdraw_mark_permutations": (
        "a mark's admission index is internally available: the metatheoretic "
        "name definition 3 assigns is declared to be an internal designation"
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

# The value each coordinate is inherited at.  Each coordinate is tested
# against its OWN inherited value and never against a shared falsehood; the
# pinned world repaired exactly that defect for its three-valued coordinate,
# and dropping a repaired guard because the repair happens not to bite is how
# the defect comes back.
INHERITED: dict[str, bool] = {
    "withdraw_mark_permutations": False,
    "keep_labels": False,
    "extra_mark": False,
}

# The single value-set change of the whole deletion.
EXTRA_MARK_VALUES: tuple[bool, bool] = (False, True)
PINNED_EXTRA_MARK_VALUES: tuple[str, str, str] = ("None", "0", "1")

DELETION_CRITERION = (
    "a pinned coordinate transfers exactly when its pinned capability "
    "sentence contains no whole word 'side' or 'sides'"
)

SPACE_IS_EXHAUSTIVE_OVER = (
    "the three declared coordinates and their declared values, and nothing "
    "wider.  It does not enumerate an augmentation that changes the event "
    "grammar again, that admits more than one further mark in one step, that "
    "supplies a datum the caller never presented, that derives the permitted "
    "renamings instead of declaring them, or that admits a new per-mark "
    "datum.  Every minimality statement is scoped to this space"
)

REJECTED_COORDINATE = {
    "name": "admit a per-mark two-valued datum",
    "rejected_because": [
        "it is an addition where the whole instrument is a deletion",
        "it lies outside the pinned space, so allowing it would price a route "
        "the pinned world was never charged for either",
        "it answers a different question: the PRICE of rebuilding the "
        "admitted primitive, not the WORTH of having it free",
    ],
    "carried_as": "open obstruction (b)",
}

_SIDE_WORD = re.compile(r"\b(?:side|sides)\b", re.IGNORECASE)


def transfers(capability_sentence: str) -> bool:
    """The mechanical deletion criterion, applied to one pinned sentence."""
    return _SIDE_WORD.search(capability_sentence) is None


# ---------------------------------------------------------------------------
# The declared space
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Augmentation:
    """One declared candidate augmentation: a value for each coordinate."""

    withdraw_mark_permutations: bool = False
    keep_labels: bool = False
    extra_mark: bool = False

    def value_of(self, name: str) -> bool:
        if name == "withdraw_mark_permutations":
            return self.withdraw_mark_permutations
        if name == "keep_labels":
            return self.keep_labels
        if name == "extra_mark":
            return self.extra_mark
        raise ValueError(f"unknown coordinate: {name!r}")

    def values(self) -> tuple[bool, ...]:
        return tuple(self.value_of(name) for name in COORDINATES)


NULL_AUGMENTATION = Augmentation()


def candidate_space() -> list[Augmentation]:
    """Every point of the declared space, in a deterministic order."""
    return [
        Augmentation(wp, kl, em)
        for wp in (False, True)
        for kl in (False, True)
        for em in EXTRA_MARK_VALUES
    ]


def changed_coordinates(aug: Augmentation) -> list[str]:
    """The coordinates the candidate moves off their own inherited values."""
    return [name for name in COORDINATES if aug.value_of(name) != INHERITED[name]]


def capabilities(aug: Augmentation) -> list[str]:
    """The undeclared capabilities used, one per moved coordinate."""
    return [CAPABILITY_OF[name] for name in changed_coordinates(aug)]


def point_name(aug: Augmentation) -> str:
    """A deterministic name for a point of the space."""
    moved = changed_coordinates(aug)
    return "+".join(moved) if moved else "base"


# ---------------------------------------------------------------------------
# What a candidate declares
# ---------------------------------------------------------------------------


def mark_permutations_permitted(aug: Augmentation) -> bool:
    return not aug.withdraw_mark_permutations


def flags(aug: Augmentation) -> tuple[bool, bool]:
    """The two flags the kernel's flagged enumerations take."""
    return (mark_permutations_permitted(aug), aug.keep_labels)


def effective_structure(aug: Augmentation) -> list[str]:
    """What the candidate actually declares: renamings and serialization."""
    return [str(part) for part in flags(aug)]


# ---------------------------------------------------------------------------
# Histories and regimes
# ---------------------------------------------------------------------------


def caller_history(wholes: Sequence[Whole]) -> list[Event]:
    """The caller's history: for each retained whole, a supply and an
    admission under the declared identity policy."""
    history: list[Event] = []
    for whole in wholes:
        if whole.token is None:
            raise AdmissionError("a whole with no mark cannot be retained")
        history.append(Supply(whole.token))
        history.append(AdmitOccurrence(whole.token))
    return history


def shared_policy_history(wholes: Sequence[Whole]) -> list[Event]:
    """The same history under the pinned SHARED identity policy.

    Reported, never declared.  Side-free the second admission names a label
    already admitted, so it is admit-then-no-op and yields ONE mark; the
    requirement then has no subject.
    """
    history: list[Event] = []
    for whole in wholes:
        if whole.token is None:
            raise AdmissionError("a whole with no mark cannot be retained")
        history.append(Supply(whole.token))
        history.append(AdmitMark(whole.token))
    return history


def process_admission(aug: Augmentation) -> list[Event]:
    """The event the process adds for a further-mark candidate; nothing else.

    The token is the one the caller already supplied, so no supply is needed
    and the candidate uses exactly the one pinned capability.
    """
    return [AdmitOccurrence(SUPPLIED_TOKEN)] if aug.extra_mark else []


def candidate_history(
    wholes: Sequence[Whole], aug: Augmentation, order_reversed: bool = False
) -> list[Event]:
    """The caller's history, optionally in the other order, extended by the
    process's own admission when the candidate declares one."""
    presented = list(reversed(list(wholes))) if order_reversed else list(wholes)
    return caller_history(presented) + process_admission(aug)


def relabelled(r: Regime) -> Regime:
    """The same arity under a different visible mark."""
    return Regime(tuple(RELABELLED_TOKEN for _ in r.marks), r.initial_datum)


def caller_wholes() -> list[Whole]:
    return [read_whole(text) for text in INSCRIPTIONS]


def comparison_regimes(
    wholes: Sequence[Whole], aug: Augmentation
) -> tuple[Regime, Regime, Regime]:
    """The candidate's regime and the two the collateral facts compare it to."""
    g = genesis()
    main = replay(candidate_history(wholes, aug, False), g)
    other_order = replay(candidate_history(wholes, aug, True), g)
    return (main, other_order, relabelled(main))


# ---------------------------------------------------------------------------
# The declared mark properties
# ---------------------------------------------------------------------------

MarkProperty = Callable[[Regime, int], bool]


def admitted(r: Regime, i: int) -> bool:
    """Mark ``i`` is admitted.  The one positive judgment form, as a property."""
    return observation_holds(r, Admitted(i))


def has_index_0(_r: Regime, i: int) -> bool:
    """Mark ``i`` is the first admitted mark.  Reads the index, not the state."""
    return i == 0


def has_index_1(_r: Regime, i: int) -> bool:
    """Mark ``i`` is the second admitted mark."""
    return i == 1


def carries_label_a(r: Regime, i: int) -> bool:
    """Mark ``i`` carries the presentation label the caller supplied."""
    return i < r.n_marks() and r.marks[i] == SUPPLIED_TOKEN


# The pinned list with its two side properties deleted and the residue
# judgment added as a property, so the residue's inertness is COMPUTED.
DECLARED_MARK_PROPERTIES: tuple[tuple[str, MarkProperty], ...] = (
    ("admitted", admitted),
    ("has_index_0", has_index_0),
    ("has_index_1", has_index_1),
    ("carries_label_a", carries_label_a),
)

DomainImages = list[tuple[Regime, list[tuple[tuple[int, ...], Regime]]]]


def property_domain(max_marks: int) -> list[Regime]:
    """Every hypothetical regime of at most ``max_marks`` marks over the two
    declared labels; none of them is admitted."""
    return [
        Regime(labels)
        for n in range(max_marks + 1)
        for labels in product(PROPERTY_LABELS, repeat=n)
    ]


def domain_images(domain: Sequence[Regime], mark_permutations: bool) -> DomainImages:
    return [(r, permitted_images_under(r, mark_permutations)) for r in domain]


def property_invariant(prop: MarkProperty, images: DomainImages) -> bool:
    """Whether a property holds of a mark exactly when it holds of that mark's
    image, at every regime of the domain and every permitted image."""
    return all(
        prop(image, pi[i]) == prop(r, i)
        for r, entries in images
        for pi, image in entries
        for i in range(r.n_marks())
    )


def property_separates(prop: MarkProperty, r: Regime) -> bool:
    i, j = RETAINED_MARKS
    return prop(r, i) != prop(r, j)


# ---------------------------------------------------------------------------
# The two transferring collateral facts, and the second measure
# ---------------------------------------------------------------------------

# Of the pinned five, exactly these two have a side-free subject.  The other
# three name sides, a convention whose codomain is gone, or admitted names.
COLLATERAL_FACTS: tuple[str, ...] = (
    "order_internally_available",
    "label_internally_available",
)
PINNED_COLLATERAL_FACTS_WITHOUT_A_SIDE_FREE_SUBJECT: tuple[str, ...] = (
    "sides_internally_separable",
    "convention_internally_available",
    "side_names_hold",
)


def collateral_facts(
    wholes: Sequence[Whole], aug: Augmentation, key_choice: str = DECLARED_KEY_CHOICE
) -> dict[str, bool]:
    """The two declared facts, computed under the candidate's own renamings."""
    main, other_order, relabel = comparison_regimes(wholes, aug)
    mp, kl = flags(aug)
    return {
        "order_internally_available": not is_isomorphic_under(
            main, other_order, mp, kl, key_choice
        ),
        "label_internally_available": not is_isomorphic_under(
            main, relabel, mp, kl, key_choice
        ),
    }


ORDER_FACT_REASON = (
    "the caller's two supplies carry the same token, so reversing them is not "
    "a change to notice.  This is NOT 'the admission order is unavailable': "
    "the admission order still exists, it is the mark's internal identity, "
    "and it is exactly what the result turns on"
)


# ---------------------------------------------------------------------------
# The side-free carrier's view for the generic enumerator
# ---------------------------------------------------------------------------


def event_json(e: Event) -> Json:
    return {"kind": type(e).__name__, "token": e.token}


def probes(token: str) -> list[Event]:
    """Events offered to the empty transition relation; none applied.

    Every kind of the current grammar is offered, so a kind cannot escape the
    relation by never having been asked about.
    """
    return [Supply(token), AdmitMark(token), AdmitOccurrence(token)]


def route_census_regimes(aug: Augmentation) -> list[Regime]:
    """The candidate's own two-mark configuration domain.

    The two declared labels in each of the two retained positions, with the
    candidate's further mark appended when it declares one.
    """
    extra = (SUPPLIED_TOKEN,) if aug.extra_mark else ()
    return [
        Regime(tuple(labels) + extra)
        for labels in product(PROPERTY_LABELS, repeat=2)
    ]


def withdrawal_census(mark_permutations: bool) -> list[bool]:
    """The declared withdrawal census of this world: 8 cells.

    The two declared labels in each of the two positions, and each value of
    ``keep_labels``.  The parameter is the coordinate under measurement.
    """
    i, j = RETAINED_MARKS
    return [
        marks_separable_under(Regime(tuple(labels)), i, j, mark_permutations, kl)
        for labels in product(PROPERTY_LABELS, repeat=2)
        for kl in (False, True)
    ]


class SideFreeCarrier:
    """The control world, as the generic enumerator sees it."""

    world = "control"
    coordinates = COORDINATES
    collateral_fact_names = COLLATERAL_FACTS
    restricted_fact_names = COLLATERAL_FACTS

    def __init__(self) -> None:
        self._wholes = caller_wholes()
        self._images: dict[bool, DomainImages] = {
            mp: domain_images(property_domain(PROPERTY_DOMAIN_MAX_MARKS), mp)
            for mp in (False, True)
        }

    # -- the candidate's own objects ---------------------------------------

    def _aug(self, aug: object) -> Augmentation:
        if not isinstance(aug, Augmentation):
            raise TypeError(f"not a candidate of this world: {aug!r}")
        return aug

    def _main(self, aug: object) -> Regime:
        main, _order, _label = comparison_regimes(self._wholes, self._aug(aug))
        return main

    def _events(self, aug: object) -> list[Event]:
        return candidate_history(self._wholes, self._aug(aug), False)

    # -- the protocol -------------------------------------------------------

    def points(self) -> list[object]:
        return list(candidate_space())

    def base_point(self) -> object:
        return NULL_AUGMENTATION

    def point_name(self, aug: object) -> str:
        return point_name(self._aug(aug))

    def coordinate_values(self, aug: object) -> Json:
        return {name: self._aug(aug).value_of(name) for name in COORDINATES}

    def changed_coordinates(self, aug: object) -> list[str]:
        return changed_coordinates(self._aug(aug))

    def capability_of(self, name: str) -> str:
        return CAPABILITY_OF[name]

    def history(self, aug: object) -> list[Json]:
        return [event_json(e) for e in self._events(aug)]

    def certified(self, aug: object) -> bool:
        return certify(self._events(aug), genesis(), self._main(aug))

    def replays_from_genesis(self, aug: object) -> bool:
        return replay(self._events(aug), genesis()) == self._main(aug)

    def initial_datum_unchanged(self, aug: object) -> bool:
        return self._main(aug).initial_datum == genesis().initial_datum

    def event_follows_relation_empty(self, aug: object) -> bool:
        main = self._main(aug)
        return all(not event_follows(main, e) for e in probes(SUPPLIED_TOKEN))

    def n_marks(self, aug: object) -> int:
        return self._main(aug).n_marks()

    def labels(self, aug: object) -> list[str]:
        return list(self._main(aug).marks)

    def permitted_renamings(self, aug: object) -> Json:
        mp, kl = flags(self._aug(aug))
        return {
            "mark_permutations": mp,
            "labels_kept": kl,
            "images": len(permitted_images_under(self._main(aug), mp)),
        }

    def automorphism_entries(self, aug: object) -> list[Json]:
        mp, kl = flags(self._aug(aug))
        return [
            {"permutation": list(pi)}
            for pi in automorphisms_under(self._main(aug), mp, kl)
        ]

    def carrier_separability(self, aug: object) -> bool:
        mp, kl = flags(self._aug(aug))
        i, j = RETAINED_MARKS
        return marks_separable_under(self._main(aug), i, j, mp, kl)

    def satisfies_second_reading(self, aug: object) -> bool:
        mp, kl = flags(self._aug(aug))
        main = self._main(aug)
        i, j = RETAINED_MARKS
        orbit = mark_orbit_under(main, i, mp, kl)
        return (repr(key_of(main, kl)), j) not in orbit

    def orbit_size(self, aug: object) -> int:
        mp, kl = flags(self._aug(aug))
        i, _j = RETAINED_MARKS
        return len(mark_orbit_under(self._main(aug), i, mp, kl))

    def no_permitted_renaming_moves_an_index(self, aug: object) -> bool:
        mp, _kl = flags(self._aug(aug))
        return no_permitted_renaming_moves_an_index(self._main(aug), mp)

    def effective_structure(self, aug: object) -> list[str]:
        return effective_structure(self._aug(aug))

    def canonical_key(self, aug: object) -> object:
        mp, kl = flags(self._aug(aug))
        return key_json(canonical_under(self._main(aug), mp, kl))

    def collateral_facts(self, aug: object) -> dict[str, bool]:
        return collateral_facts(self._wholes, self._aug(aug))

    def mark_property_facts(self, aug: object) -> dict[str, list[str]]:
        mp, _kl = flags(self._aug(aug))
        main = self._main(aug)
        images = self._images[mp]
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
        mp, kl = flags(self._aug(aug))
        i, j = RETAINED_MARKS
        return [
            marks_separable_under(r, i, j, mp, kl)
            for r in route_census_regimes(self._aug(aug))
        ]

    def satisfies_under_key_choice(self, aug: object) -> dict[str, bool]:
        mp, kl = flags(self._aug(aug))
        main = self._main(aug)
        i, j = RETAINED_MARKS
        return {
            choice: marks_separable_under(main, i, j, mp, kl, choice)
            for choice in KEY_CHOICES
        }
