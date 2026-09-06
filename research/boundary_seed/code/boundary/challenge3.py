"""Challenge 3: the caller requires `<a|>` and `<|a>` to be internally
separable in a precisely declared sense.

Everything computed here is metatheory about the kernel in ``model.py``, the
presentation layer in ``presentation.py``, and the Challenge 2 retention in
``challenge2.py``.  Nothing here is admitted: the augmentations are declared
candidates, and each candidate's regime is the replay of an explicit history.

The rung has four parts, in this order:

1. **The declared sense.**  The requirement is the sense Challenge 2
   computed — no permitted automorphism of the regime carries one of the two
   retained marks to the other — together with a second reading, that some
   mark property invariant under every permitted renaming holds of one and
   not of the other.  The two agree by unfolding: the witness for the second
   is membership in the first mark's orbit, a property invariant by
   construction, so the second reading is a restatement and not a new fact.
   The receipt computes the agreement at every point of the declared space
   rather than asserting it.
2. **The current regime.**  Under O the requirement is already met and under
   U it is not.  What meets it under O is the withdrawal of the side
   exchange from the permitted renamings, which the O reading of the one
   admitted primitive carries; the two admitted names are not used.  The
   four-cell counterfactual over (names admitted) by (side exchange
   permitted) shows it: the value depends on the second coordinate only.
   That the names CANNOT enter is definition 16 — permission is declared,
   not derived from the judgment grammar — and it is recorded as a
   consequence of that declaration rather than as a discovery.
3. **The declared candidate space.**  Five coordinates, 48 points, each a
   declared augmentation; a candidate is one-step exactly when it changes
   one coordinate, and one whose capability count is two or more is refused
   as bundling.  Adopting reading O under U is such a bundle.
4. **The minima.**  Under U the minimum capability count over the satisfying
   one-step candidates is one, and three non-isomorphic classes attain it;
   all three are retained and uniqueness is refused.  Under O the minimum is
   zero, attained by the null augmentation alone.

The declared space is exhaustive over its five coordinates and over nothing
wider.  An augmentation outside it — one that changed the event grammar
again, or that derived permission from the judgment grammar — is not
enumerated here, and the minimality claim is scoped accordingly.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from itertools import product
from typing import Any, Callable

from boundary import challenge0, challenge1, challenge2, model, presentation
from boundary.challenge0 import observation_vocabulary, state_event_generators
from boundary.challenge1 import Json, judgments_json, key_json
from boundary.challenge2 import (
    DECLARED_POLICY,
    EVENT_TYPES,
    INSCRIPTIONS,
    RELABELLED_TOKEN,
    caller_history,
    history_json,
    refusal,
    witness_json,
)
from boundary.model import (
    READING_O,
    READING_U,
    SIDE_NAMES,
    AdmitMark,
    AdmitOccurrence,
    Event,
    OnSide,
    Regime,
    automorphisms,
    automorphisms_under,
    canonical_under,
    certify,
    event_follows,
    genesis,
    is_isomorphic_under,
    mark_automorphism_to_under,
    mark_observations,
    mark_orbit_under,
    mark_profile,
    marks_internally_separable,
    marks_separable_under,
    observation_holds,
    permitted_images,
    permitted_images_under,
    replay,
    serialize,
    serialize_keeping_labels,
    side_exchanging_automorphism_under,
)
from boundary.model import Supply  # noqa: E402  (grouped with the kernel above)
from boundary.presentation import (
    DECLARED_CONVENTION,
    OTHER_CONVENTION,
    Whole,
    admitted_side,
    read_whole,
)

SEED_SHA256 = challenge0.SEED_SHA256
C0_PREDICTIONS_SHA256 = challenge0.PREDICTIONS_SHA256
C1_PREDICTIONS_SHA256 = challenge1.PREDICTIONS_SHA256
C2_PREDICTIONS_SHA256 = challenge2.PREDICTIONS_SHA256
PREDICTIONS_SHA256 = "27057895c47e5bd718b0ea8e51689f3325cef78102c912c6feea8e913a7e7755"

SUPPLIED_TOKEN = "a"
RETAINED_MARKS: tuple[int, int] = (0, 1)
PROPERTY_DOMAIN_MAX_MARKS = 3
PROPERTY_LABELS: tuple[str, str] = (SUPPLIED_TOKEN, RELABELLED_TOKEN)

REQUIREMENT = (
    "the two retained marks are internally separable under a reading exactly "
    "when no permitted automorphism of the regime carries one of them to the "
    "other"
)
REQUIREMENT_SECOND_READING = (
    "some property of a mark that forgets whatever the candidate's declared "
    "serialization forgets, and that is invariant under every permitted "
    "renaming of the reading, holds of one retained mark and not of the other"
)
REQUIREMENT_READINGS_AGREE_BECAUSE = (
    "membership in a mark's orbit under the permitted renamings is a property "
    "of a (regime, mark) pair invariant under those renamings by "
    "construction, which rests on a premise stated here and checked by "
    "nothing, that a candidate's permitted renamings are closed under "
    "composition and inverse; it separates the two marks exactly when no "
    "permitted automorphism carries one to the other, so that half of the "
    "agreement is by unfolding and not a further fact.  What is "
    "computed at every point is the first reading against this declared "
    "witness, and not against the existential over every such property; the "
    "direction back from an arbitrary such property is the justifying "
    "sentence of the Challenge 2 separability definition, which is prose"
)

# The five declared coordinates of the candidate space, in the order the
# enumeration takes them.  Each is one declared augmentation; changing one is
# one step, and the capability it uses is named below.
COORDINATES: tuple[str, ...] = (
    "withdraw_reflection",
    "withdraw_mark_permutations",
    "admit_names",
    "keep_labels",
    "extra_mark",
)
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
EXTRA_MARK_VALUES: tuple[int | None, int, int] = (None, 0, 1)

SPACE_IS_EXHAUSTIVE_OVER = (
    "the five declared coordinates and their declared values, and nothing "
    "wider.  It does not enumerate an augmentation that changes the event "
    "grammar again, that admits more than one further mark in one step, that "
    "supplies a datum the caller never presented, or that derives the "
    "permitted renamings from the judgment grammar instead of declaring them "
    "(definition 16).  Every minimality statement below is scoped to this "
    "space"
)

# The declared mark properties.  Each is a property of a (regime, mark) pair.
# Invariance is a census over the declared bounded domain under the
# augmentation's permitted renamings; separation is read at the candidate's
# own regime.
MarkProperty = Callable[[Regime, int], bool]


def on_side_0(r: Regime, i: int) -> bool:
    """Mark ``i`` lies on side 0.  Mark form of definition 34."""
    return observation_holds(r, OnSide(i, 0))


def on_side_1(r: Regime, i: int) -> bool:
    """Mark ``i`` lies on side 1.  Mark form of definition 34."""
    return observation_holds(r, OnSide(i, 1))


def has_index_0(r: Regime, i: int) -> bool:
    """Mark ``i`` is the first admitted mark.  Reads the index, not the state."""
    return i == 0


def has_index_1(r: Regime, i: int) -> bool:
    """Mark ``i`` is the second admitted mark."""
    return i == 1


def carries_label_a(r: Regime, i: int) -> bool:
    """Mark ``i`` carries the presentation label the caller supplied."""
    return i < r.n_marks() and r.marks[i] == SUPPLIED_TOKEN


DECLARED_MARK_PROPERTIES: tuple[tuple[str, MarkProperty], ...] = (
    ("on_side_0", on_side_0),
    ("on_side_1", on_side_1),
    ("has_index_0", has_index_0),
    ("has_index_1", has_index_1),
    ("carries_label_a", carries_label_a),
)

# The declared collateral facts: things about the retained configuration that
# no permitted renaming of reading U left available at the close of Challenge
# 2.  The second cost measure counts how many of them a candidate makes
# available that the same reading's base did not.
COLLATERAL_FACTS: tuple[str, ...] = (
    "sides_internally_separable",
    "order_internally_available",
    "label_internally_available",
    "convention_internally_available",
    "side_names_hold",
)

MU1 = "capability count: the number of undeclared capabilities the candidate uses"
MU2 = (
    "collateral count: how many of the five declared facts about the retained "
    "configuration the candidate makes internally available that the same "
    "reading's base did not.  The required separation is not one of the five, "
    "but the first of them, that the two sides are internally separable, is "
    "computed to take the requirement's value at every point of the declared "
    "space, so where the base fails the requirement a satisfying candidate's "
    "count includes that one"
)

SCORED_PREDICTIONS: tuple[str, ...] = (
    "C3-1", "C3-2", "C3-3", "C3-4", "C3-5", "C3-6", "C3-7", "C3-8",
)
# The scored predictions whose every hitting clause, read literally, is fixed
# by a declaration of this run: the declared sense together with the
# by-unfolding agreement of its two readings, and the declared candidate
# space with its declared capability count.  A HIT on one of them is HIT by
# construction and is not counted as content; a miss on one is a miss like
# any other.  The criterion is the one Challenge 1 declared.
DEFINITION_LEVEL_PREDICTIONS: tuple[str, ...] = ("C3-1", "C3-4")
TALLY_CRITERION = challenge1.TALLY_CRITERION

CAPABILITIES: dict[str, dict[str, str]] = {
    "admitted boundary": {
        "declared_at": "the seed, as the one admitted primitive exception",
        "paid_by": "the seed",
        "buys_at_challenge_3": (
            "that a mark lies on a side at all, so that every candidate of "
            "the declared space and every mark property of the declared list "
            "except the two index ones is formulable"
        ),
    },
    "side names under O": {
        "declared_at": "genesis, as the O reading of the one declaration",
        "paid_by": "the declared reading",
        "buys_at_challenge_3": (
            "nothing the requirement uses: the four-cell counterfactual shows "
            "the names do not enter the automorphism computation, and what "
            "meets the requirement under O is the withdrawal of the side "
            "exchange that the same reading carries"
        ),
    },
    "the side exchange is not a permitted renaming": {
        "declared_at": (
            "genesis under O, as the other half of the O reading; at "
            "Challenge 3 under U, as one candidate augmentation"
        ),
        "paid_by": "the declared reading under O; the run under U",
        "buys_at_challenge_3": (
            "the required separation, under O without a new declaration and "
            "under U as one of three tied minima"
        ),
    },
    "occurrence identity": {
        "declared_at": "Challenge 2, as that rung's one new declaration",
        "paid_by": "the run",
        "buys_at_challenge_3": (
            "that there are two marks to separate at all; without it the "
            "caller's retention is refused and the requirement has no subject"
        ),
    },
    "presentation convention": {
        "declared_at": "Challenge 1, as metatheory",
        "paid_by": "the run",
        "buys_at_challenge_3": (
            "which retained whole is which mark; not the separation, the "
            "other convention's regime lying in the same class under both "
            "readings, as Challenge 2 computed"
        ),
    },
}

BOUNDARY_DEPENDENCE: dict[str, str] = {
    "the declared sense of the requirement and the agreement of its two readings": (
        "does not depend on the admitted boundary; it is about renamings and "
        "orbits, and it would be stated the same way for any renaming set"
    ),
    "the identity of the candidate space, the capability counts, and the "
    "refusal of bundles": "does not depend on the admitted boundary",
    "the two index mark properties and the withdrawal of the mark permutations": (
        "does not depend on the admitted boundary; the admission index is "
        "carried by the placement tuple's length and not by the sides"
    ),
    "the side exchange, its withdrawal, the two side mark properties, the "
    "counterfactual square, and every separation result of the rung": (
        "require the admitted boundary and are not formulated after removing it"
    ),
    "the further-mark candidate": (
        "requires the admitted boundary: the further mark is admitted ON a "
        "side, and what separates the two retained marks there is that the "
        "two sides then carry different numbers of marks"
    ),
}


# ---------------------------------------------------------------------------
# The declared candidate space
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Augmentation:
    """One declared candidate augmentation: a value for each coordinate.

    A deterministic value object.  It applies nothing: a candidate becomes a
    regime only through ``replay`` of an explicit history, and it becomes a
    renaming set only by being handed to the kernel's flagged enumerations.
    """

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
    """Every point of the declared space, in a deterministic order."""
    return [
        Augmentation(wr, wp, an, kl, em)
        for wr in (False, True)
        for wp in (False, True)
        for an in (False, True)
        for kl in (False, True)
        for em in EXTRA_MARK_VALUES
    ]


def changed_coordinates(aug: Augmentation) -> list[str]:
    """The coordinates the candidate moves off their inherited values.

    Each coordinate is tested against its own inherited value rather than
    against a shared falsehood: ``extra_mark`` is inherited as ``None`` and
    its value ``0`` is a move, which a truth test would silently drop,
    ``0 == False`` in this language.  That defect was live and is fixed by
    name here; ``test_side_zero_is_a_moved_coordinate`` holds it.
    """
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


def capabilities(aug: Augmentation) -> list[str]:
    """The undeclared capabilities the candidate uses, one per moved coordinate."""
    return [CAPABILITY_OF[name] for name in changed_coordinates(aug)]


def mu1(aug: Augmentation) -> int:
    """The first declared cost measure: the capability count."""
    return len(capabilities(aug))


def is_one_step(aug: Augmentation) -> bool:
    """Whether the candidate moves exactly one coordinate."""
    return len(changed_coordinates(aug)) == 1


def bundles(aug: Augmentation) -> bool:
    """Whether the candidate bundles capabilities and is refused as one step."""
    return mu1(aug) >= 2


def point_name(aug: Augmentation) -> str:
    """A deterministic name for a point of the space."""
    moved = changed_coordinates(aug)
    if not moved:
        return "base"
    parts = [
        f"extra_mark_{aug.extra_mark}" if name == "extra_mark" else name
        for name in moved
    ]
    return "+".join(parts)


# ---------------------------------------------------------------------------
# What a candidate declares: renamings, grammar, serialization
# ---------------------------------------------------------------------------


def reflection_permitted(reading: str, aug: Augmentation) -> bool:
    """Whether the side exchange is a permitted renaming for this candidate.

    Under O it is not permitted whatever the candidate says; under U it is
    permitted unless the candidate withdraws it.
    """
    return reading == READING_U and not aug.withdraw_reflection


def mark_permutations_permitted(aug: Augmentation) -> bool:
    return not aug.withdraw_mark_permutations


def names_admitted(reading: str, aug: Augmentation) -> bool:
    """Whether the side-name judgment form is in this candidate's grammar."""
    return reading == READING_O or aug.admit_names


def flags(reading: str, aug: Augmentation) -> tuple[bool, bool, bool]:
    """The three flags the kernel's flagged enumerations take."""
    return (
        reflection_permitted(reading, aug),
        mark_permutations_permitted(aug),
        aug.keep_labels,
    )


def key_of(r: Regime, keep_labels: bool) -> tuple[object, ...]:
    """The serialization the candidate declares."""
    return serialize_keeping_labels(r) if keep_labels else serialize(r)


def effective_structure(reading: str, aug: Augmentation) -> tuple[object, ...]:
    """What the candidate actually declares, after the reading is applied.

    Two points of the space that declare the same renamings, the same grammar,
    and the same serialization are the same structure however their raw
    coordinates read: under O, withdrawing an already absent side exchange and
    admitting already admitted names both change nothing.
    """
    return (
        reflection_permitted(reading, aug),
        mark_permutations_permitted(aug),
        names_admitted(reading, aug),
        aug.keep_labels,
    )


# ---------------------------------------------------------------------------
# The candidate's regime, and its comparison regimes
# ---------------------------------------------------------------------------


def probes(token: str) -> list[Event]:
    """Events offered to the empty event-follows relation; none applied.

    The Challenge 1 probe set offered a supply and the two token-keyed
    admissions only, so the occurrence admission Challenge 2 declared was
    never offered to the relation at all.  Review found that; this set offers
    every kind of the current grammar, and ``test_the_probe_set_offers_every
    _event_kind`` holds it to that.
    """
    return [
        Supply(token),
        AdmitMark(token, 0),
        AdmitMark(token, 1),
        AdmitOccurrence(token, 0),
        AdmitOccurrence(token, 1),
    ]


def process_admission(aug: Augmentation) -> list[Event]:
    """The event the process adds for a further-mark candidate; nothing else.

    The token is the one the caller already supplied, so no supply is needed
    and the candidate uses exactly one new capability: that the process, not
    the caller, issues the event.
    """
    if aug.extra_mark is None:
        return []
    return [AdmitOccurrence(SUPPLIED_TOKEN, aug.extra_mark)]


def candidate_history(
    wholes: list[Whole], aug: Augmentation, convention: str, order_reversed: bool
) -> list[Event]:
    """The caller's Challenge 2 history under a convention and order, extended
    by the process's own admission when the candidate declares one."""
    presented = list(reversed(wholes)) if order_reversed else list(wholes)
    return caller_history(presented, convention, DECLARED_POLICY) + process_admission(aug)


def relabelled(r: Regime) -> Regime:
    """The same placement under a different visible mark."""
    return Regime(r.reading, tuple(RELABELLED_TOKEN for _ in r.marks), r.placement)


def comparison_regimes(
    reading: str, wholes: list[Whole], aug: Augmentation
) -> tuple[Regime, Regime, Regime, Regime]:
    """The candidate's regime, and the three the collateral facts compare it to."""
    g = genesis(reading)
    main = replay(candidate_history(wholes, aug, DECLARED_CONVENTION, False), g)
    other_order = replay(candidate_history(wholes, aug, DECLARED_CONVENTION, True), g)
    other_convention = replay(candidate_history(wholes, aug, OTHER_CONVENTION, False), g)
    return (main, other_order, relabelled(main), other_convention)


# ---------------------------------------------------------------------------
# The requirement, in both of its declared readings
# ---------------------------------------------------------------------------


def requirement_met(r: Regime, reading: str, aug: Augmentation) -> bool:
    """The declared requirement: no permitted automorphism carries one of the
    two retained marks to the other."""
    i, j = RETAINED_MARKS
    return marks_separable_under(r, i, j, *flags(reading, aug))


def orbit_property_separates(r: Regime, reading: str, aug: Augmentation) -> bool:
    """The second reading of the requirement, with its orbit witness.

    The property "this (regime, mark) pair lies in the orbit of the first
    retained mark" is invariant under the permitted renamings by
    construction; it separates the two marks exactly when the pair of the
    second mark is outside that orbit.
    """
    i, j = RETAINED_MARKS
    _reflection, _perms, keep_labels = flags(reading, aug)
    orbit = mark_orbit_under(r, i, *flags(reading, aug))
    return (key_of(r, keep_labels), j) not in orbit


def property_domain(reading: str, max_marks: int) -> list[Regime]:
    """Every hypothetical regime of at most ``max_marks`` marks over the two
    declared labels; none of them is admitted."""
    out: list[Regime] = []
    for n in range(max_marks + 1):
        for labels in product(PROPERTY_LABELS, repeat=n):
            for placement in product((0, 1), repeat=n):
                out.append(Regime(reading, labels, placement))
    return out


DomainImages = list[tuple[Regime, list[tuple[bool, tuple[int, ...], Regime]]]]


def domain_images(
    domain: list[Regime], reflection: bool, mark_permutations: bool
) -> DomainImages:
    """Every regime of the domain with the images the two flags permit."""
    return [
        (r, permitted_images_under(r, reflection, mark_permutations)) for r in domain
    ]


def property_invariant(prop: MarkProperty, images: DomainImages) -> bool:
    """Whether a mark property holds of a mark exactly when it holds of that
    mark's image, at every regime of the domain and every permitted image."""
    return all(
        prop(image, pi[i]) == prop(r, i)
        for r, entries in images
        for _reflected, pi, image in entries
        for i in range(r.n_marks())
    )


def property_separates(prop: MarkProperty, r: Regime) -> bool:
    i, j = RETAINED_MARKS
    return prop(r, i) != prop(r, j)


def mark_property_facts(
    r: Regime, images: DomainImages
) -> dict[str, list[str]]:
    """Which declared mark properties are invariant, which separate the two
    retained marks, and which do both."""
    invariant = [
        name for name, prop in DECLARED_MARK_PROPERTIES if property_invariant(prop, images)
    ]
    separating = [
        name for name, prop in DECLARED_MARK_PROPERTIES if property_separates(prop, r)
    ]
    return {
        "invariant": invariant,
        "separating": separating,
        "invariant_separating": [n for n in separating if n in invariant],
    }


# ---------------------------------------------------------------------------
# The collateral facts and the second measure
# ---------------------------------------------------------------------------


def collateral_facts(
    reading: str, aug: Augmentation, wholes: list[Whole]
) -> dict[str, bool]:
    """The five declared facts, computed under the candidate's own renamings."""
    main, other_order, relabel, other_convention = comparison_regimes(reading, wholes, aug)
    fl = flags(reading, aug)
    return {
        "sides_internally_separable": side_exchanging_automorphism_under(main, *fl) is None,
        "order_internally_available": not is_isomorphic_under(main, other_order, *fl),
        "label_internally_available": not is_isomorphic_under(main, relabel, *fl),
        "convention_internally_available": not is_isomorphic_under(
            main, other_convention, *fl
        ),
        "side_names_hold": names_admitted(reading, aug),
    }


def mu2(facts: dict[str, bool], base_facts: dict[str, bool]) -> int:
    """The second declared cost measure: newly available collateral facts."""
    return sum(1 for name in COLLATERAL_FACTS if facts[name] and not base_facts[name])


def sides_fact_agrees_with_the_requirement(rows: list[Json]) -> bool:
    """Whether the first declared collateral fact takes the requirement's value
    at every enumerated point.

    The second measure was declared to read what a candidate costs BESIDE what
    it was asked for.  Review found that it does not, and this computes the
    reason: ``sides_internally_separable`` is the requirement said of the two
    SIDES, and over this space it agrees with the requirement said of the two
    MARKS at every point, so a satisfying candidate whose base fails always
    carries that one fact in its count.  Reported, not repaired: changing the
    declared fact list after the enumeration would fit the declaration to the
    answer.
    """
    return all(
        row["collateral_facts"]["sides_internally_separable"] == row["satisfies"]
        for row in rows
    )


# ---------------------------------------------------------------------------
# Rows of the enumeration
# ---------------------------------------------------------------------------


def point_row(
    reading: str,
    aug: Augmentation,
    wholes: list[Whole],
    base_facts: dict[str, bool],
) -> Json:
    """One point of the declared space: its cost under each measure, whether it
    is one step, whether it bundles, and whether it satisfies the requirement
    in each of the two readings of it."""
    main, _order, _label, _convention = comparison_regimes(reading, wholes, aug)
    facts = collateral_facts(reading, aug, wholes)
    met = requirement_met(main, reading, aug)
    return {
        "name": point_name(aug),
        "coordinates": dict(zip(COORDINATES, aug.values())),
        # by coordinate, one capability each; the text of every capability is
        # in `candidate_space.capability_of`, and the one-step rows carry it
        # in full.  The point rows name the coordinates so that the receipt of
        # 48 points twice over stays readable.
        "capability_coordinates": changed_coordinates(aug),
        "mu1": mu1(aug),
        "mu2": mu2(facts, base_facts),
        "one_step": is_one_step(aug),
        "bundles": bundles(aug),
        "satisfies": met,
        "satisfies_second_reading": orbit_property_separates(main, reading, aug),
        "effective_structure": [str(part) for part in effective_structure(reading, aug)],
        "class_key": class_key(reading, aug, main),
        "collateral_facts": facts,
    }


def class_key(reading: str, aug: Augmentation, main: Regime) -> list[object]:
    """The implemented quotient: the structure the candidate declares, with the
    canonical key of its regime under that structure's own renamings."""
    return [
        *[str(part) for part in effective_structure(reading, aug)],
        key_json(canonical_under(main, *flags(reading, aug))),
    ]


def expected_placement(wholes: list[Whole], aug: Augmentation) -> list[int]:
    """The placement the declared convention and the candidate predict.

    Computed from the presented sides and the convention alone, so that the
    receipt carries one statement about the candidate regime that is not a
    comparison of a replay with itself.
    """
    out = [
        admitted_side(str(whole.presented_side), DECLARED_CONVENTION) for whole in wholes
    ]
    if aug.extra_mark is not None:
        out.append(aug.extra_mark)
    return out


def one_step_detail(
    reading: str,
    aug: Augmentation,
    wholes: list[Whole],
    images_cache: dict[tuple[bool, bool], DomainImages],
    base_facts: dict[str, bool],
) -> Json:
    """The full report for one candidate: its history, its regime, its
    automorphisms, the requirement in both readings, and its mechanism."""
    g = genesis(reading)
    history = candidate_history(wholes, aug, DECLARED_CONVENTION, False)
    main, _order, _label, _convention = comparison_regimes(reading, wholes, aug)
    reflection, perms, keep_labels = flags(reading, aug)
    found = automorphisms_under(main, reflection, perms, keep_labels)
    i, j = RETAINED_MARKS
    exchange = mark_automorphism_to_under(main, i, j, reflection, perms, keep_labels)
    images = images_cache[(reflection, perms)]
    props = mark_property_facts(main, images)
    row = point_row(reading, aug, wholes, base_facts)
    row.update(
        {
            "capabilities": capabilities(aug),
            "history": history_json(history),
            "certified": certify(history, g, main),
            "replays_from_genesis": replay(history, g) == main,
            "marks": main.n_marks(),
            "placement": list(main.placement),
            # derived from the declared convention and the candidate's own
            # side, NOT from the replay the row reports: `certified` and
            # `replays_from_genesis` beside it compare the replay with itself
            # and cannot be false, which review named at the previous rung.
            # This one can.
            "placement_matches_the_declared_convention": list(main.placement)
            == expected_placement(wholes, aug),
            "labels": list(main.marks),
            "permitted_renamings": {
                "side_exchange": reflection,
                "mark_permutations": perms,
                "labels_kept": keep_labels,
                "names_admitted": names_admitted(reading, aug),
                "images": len(permitted_images_under(main, reflection, perms)),
            },
            "automorphism_count": len(found),
            "automorphism_entries": [witness_json(entry) for entry in found],
            "mark_exchange_witness": witness_json(exchange),
            "side_exchange_witness": witness_json(
                side_exchanging_automorphism_under(main, reflection, perms, keep_labels)
            ),
            "no_permitted_renaming_moves_an_index": all(
                pi == tuple(range(main.n_marks()))
                for _reflected, pi, _image in permitted_images_under(main, reflection, perms)
            ),
            "invariant_mark_properties": props["invariant"],
            "separating_mark_properties": props["separating"],
            "invariant_separating_mark_properties": props["invariant_separating"],
            "orbit_size": len(mark_orbit_under(main, i, reflection, perms, keep_labels)),
            "mark_profiles": [
                judgments_json(mark_profile(main, k)) for k in range(main.n_marks())
            ],
            "mark_side_names": (
                [SIDE_NAMES[main.placement[k]] for k in range(main.n_marks())]
                if names_admitted(reading, aug)
                else []
            ),
            "holding_mark_judgments": len(mark_observations(main)),
            "holding_judgments_with_names": len(mark_observations(main))
            + (2 if names_admitted(reading, aug) else 0),
            "event_follows_relation_empty": all(
                not event_follows(main, e) for e in probes(SUPPLIED_TOKEN)
            ),
            "initial_datum_unchanged": main.initial_datum == g.initial_datum,
            "reading_unchanged": main.reading == reading,
        }
    )
    return row


# ---------------------------------------------------------------------------
# The counterfactual square, and the price
# ---------------------------------------------------------------------------


def counterfactual_square(reading: str, wholes: list[Whole]) -> list[Json]:
    """The requirement at the retained regime over (names admitted) by (the
    side exchange permitted).

    The value depends on the second coordinate only.  That is a consequence of
    definition 16 — permission is declared and is not derived from the
    judgment grammar — and it is reported as such: under a model in which
    permission were derived, admitting the names would withdraw the exchange
    and the two coordinates would not be independent.
    """
    main, _order, _label, _convention = comparison_regimes(
        reading, wholes, NULL_AUGMENTATION
    )
    i, j = RETAINED_MARKS
    return [
        {
            "names_admitted": names,
            "side_exchange_permitted": exchange,
            "requirement_met": marks_separable_under(main, i, j, exchange, True, False),
            "is_the_real_cell_for_this_reading": (
                names == names_admitted(reading, NULL_AUGMENTATION)
                and exchange == reflection_permitted(reading, NULL_AUGMENTATION)
            ),
        }
        for names in (False, True)
        for exchange in (False, True)
    ]


# The four price fields this function writes as declarations of the run.  No
# run can move them, and the receipt names them under
# `fields_declared_not_computed` so that a reader does not take a declaration
# for a measurement; the rest of the price is read off the enumeration.
PRICE_FIELDS_DECLARED: tuple[str, ...] = (
    "capabilities_the_satisfaction_uses",
    "capabilities_not_used",
    "declared_at",
    "paid_by",
)


def price_facts(reading: str, base_met: bool, by_mu1: Json, rows: list[Json]) -> Json:
    """What the requirement costs under this reading, and who pays it.

    Four of the eight fields move with the run: ``minimum_capability_count``,
    ``nothing_new_paid_at_challenge_3`` (that minimum being zero), and
    ``new_at_challenge_3`` (the capability list of the retained minima) are
    read off the enumeration, and ``requirement_met_without_augmentation`` is
    the base value the caller computed.
    ``test_the_price_is_read_off_the_enumeration`` fixes the direction of the
    first three.  The other four are declarations this function writes and no
    run can move; they are named in the receipt under
    ``fields_declared_not_computed`` so that a reader is not invited to take a
    declaration for a measurement, and
    ``test_the_declared_price_fields_do_not_move_with_the_enumeration`` fixes
    that direction.  An earlier version of this docstring said every field was
    read off the enumeration, which was false of those four; review found it,
    as it found the same defect one rung earlier in the corresponding
    Challenge 2 field.
    """
    minimum = int(by_mu1["minimum"])
    paid = sorted(
        {
            capability
            for entry in by_mu1["classes"]
            for member in entry["members"]
            for capability in named(rows, str(member))["capability_coordinates"]
        }
    )
    if base_met:
        used = [
            "admitted boundary",
            "the side exchange is not a permitted renaming",
            "occurrence identity",
        ]
        return {
            "requirement_met_without_augmentation": True,
            "capabilities_the_satisfaction_uses": used,
            "capabilities_not_used": ["side names under O", "presentation convention"],
            "declared_at": (
                "genesis, as the O reading of the one admitted primitive; the "
                "occurrence identity at Challenge 2"
            ),
            "paid_by": "the declared reading, and the run at Challenge 2",
            "new_at_challenge_3": paid,
            "nothing_new_paid_at_challenge_3": minimum == 0,
            "minimum_capability_count": minimum,
            "fields_declared_not_computed": list(PRICE_FIELDS_DECLARED),
        }
    return {
        "requirement_met_without_augmentation": False,
        "capabilities_the_satisfaction_uses": [],
        "capabilities_not_used": [],
        "declared_at": "Challenge 3, by whichever retained minimum is taken",
        "paid_by": "the run",
        "new_at_challenge_3": paid,
        "nothing_new_paid_at_challenge_3": minimum == 0,
        "minimum_capability_count": minimum,
        "fields_declared_not_computed": list(PRICE_FIELDS_DECLARED),
    }


# ---------------------------------------------------------------------------
# Minima, quotient, and uniqueness
# ---------------------------------------------------------------------------


def minima(rows: list[Json], measure: str, predicate: str = "satisfies") -> Json:
    """The satisfying candidates of least cost under one measure, quotiented by
    the implemented class key, with every tied class retained.

    ``predicate`` names the row key that says whether a candidate answers the
    rung's demand.  It defaults to ``satisfies``, which is what Challenges 3
    and 4 mean and is the only value either of them passes; Challenge 5's
    demand is the caller's retention and not a separability requirement, so
    that rung passes its own key rather than reusing this word for a second
    predicate.  Adding the parameter moves no computed value of any earlier
    rung, and their receipts regenerate byte-identically.
    """
    satisfying = [row for row in rows if row[predicate]]
    if not satisfying:
        return {
            "measure": measure,
            "minimum": None,
            "points": [],
            "classes": [],
            "class_count": 0,
            "unique": False,
        }
    least = min(int(row[measure]) for row in satisfying)
    attaining = [row for row in satisfying if int(row[measure]) == least]
    classes: dict[str, list[str]] = {}
    for row in attaining:
        classes.setdefault(repr(row["class_key"]), []).append(str(row["name"]))
    ordered = sorted(classes.items())
    return {
        "measure": measure,
        "minimum": least,
        "points": [str(row["name"]) for row in attaining],
        "classes": [
            {"class_key": next(r["class_key"] for r in attaining if str(r["name"]) == members[0]),
             "members": members}
            for _key, members in ordered
        ],
        "class_count": len(ordered),
        "unique": len(ordered) == 1,
    }


def one_step_minima(
    rows: list[Json], measure: str, predicate: str = "satisfies"
) -> Json:
    """The same, over the one-step candidates AND the null point.  A bundle is
    refused as a one-step augmentation, so it is not eligible to be a minimum
    of the enumeration the seed asks for; the null point is not a one-step
    augmentation either, and it is admitted because a reading whose base
    already meets the requirement pays nothing, which is what the reading-O
    minimum of zero reports.  An earlier version of this docstring said
    one-step candidates only, which the filter beside it contradicts; review
    found that, and the correction changes no computed value."""
    return minima(
        [row for row in rows if row["one_step"] or row["mu1"] == 0], measure, predicate
    )


def reading_facts(reading: str) -> Json:
    g = genesis(reading)
    wholes = [read_whole(text) for text in INSCRIPTIONS]
    base_facts = collateral_facts(reading, NULL_AUGMENTATION, wholes)
    images_cache: dict[tuple[bool, bool], DomainImages] = {}
    domain = property_domain(reading, PROPERTY_DOMAIN_MAX_MARKS)
    for reflection in (False, True):
        for perms in (False, True):
            images_cache[(reflection, perms)] = domain_images(domain, reflection, perms)
    rows = [point_row(reading, aug, wholes, base_facts) for aug in candidate_space()]
    base = one_step_detail(reading, NULL_AUGMENTATION, wholes, images_cache, base_facts)
    steps = [
        one_step_detail(reading, aug, wholes, images_cache, base_facts)
        for aug in candidate_space()
        if is_one_step(aug)
    ]
    by_mu1 = one_step_minima(rows, "mu1")
    by_mu2 = one_step_minima(rows, "mu2")
    bundle_row = next(
        row for row in rows if row["name"] == point_name(READING_O_BUNDLE)
    )
    return {
        "reading": reading,
        "base": base,
        "points": rows,
        "space_size": len(rows),
        "one_step_points": [str(row["name"]) for row in rows if row["one_step"]],
        "one_step_detail": steps,
        "satisfying_points": [str(row["name"]) for row in rows if row["satisfies"]],
        "satisfying_one_step_points": [
            str(row["name"]) for row in rows if row["satisfies"] and row["one_step"]
        ],
        "points_satisfying_with_grammar_change_only": [
            str(row["name"])
            for row in rows
            if row["satisfies"]
            and not row["coordinates"]["withdraw_reflection"]
            and not row["coordinates"]["withdraw_mark_permutations"]
            and row["coordinates"]["extra_mark"] is None
            and reading == READING_U
        ],
        "minima_by_mu1": by_mu1,
        "minima_by_mu2": by_mu2,
        "measures_agree_on_minima": by_mu1["points"] == by_mu2["points"],
        "measures_differ_somewhere": any(row["mu1"] != row["mu2"] for row in rows),
        "sides_fact_agrees_with_the_requirement_at_every_point": (
            sides_fact_agrees_with_the_requirement(rows)
        ),
        "one_step_iff_capability_count_one": all(
            row["one_step"] == (row["mu1"] == 1) for row in rows
        ),
        "bundles_refused": [str(row["name"]) for row in rows if row["bundles"]],
        "bundles_refused_count": sum(1 for row in rows if row["bundles"]),
        "reading_O_bundle": {
            "name": bundle_row["name"],
            "mu1": bundle_row["mu1"],
            "one_step": bundle_row["one_step"],
            "bundles": bundle_row["bundles"],
            "satisfies": bundle_row["satisfies"],
            "refused_because": (
                "it moves two coordinates and uses two capabilities, so it is "
                "not one step; its withdrawal half alone is a retained minimum "
                "and its name half alone satisfies nothing"
            ),
        },
        "requirement_readings_agree_at_every_point": all(
            row["satisfies"] == row["satisfies_second_reading"] for row in rows
        ),
        "requirement_matches_the_challenge_2_notion": base["satisfies"]
        == marks_internally_separable(
            replay(candidate_history(wholes, NULL_AUGMENTATION, DECLARED_CONVENTION, False), g),
            *RETAINED_MARKS,
        ),
        "counterfactual_square": counterfactual_square(reading, wholes),
        "price": price_facts(reading, bool(base["satisfies"]), by_mu1, rows),
        "process_admission": process_admission_facts(reading, wholes),
    }


def process_admission_facts(reading: str, wholes: list[Whole]) -> Json:
    """What the further-mark candidate needs, and what it does not.

    The caller already supplied the token, so the process needs no supply of
    its own; a token the caller never presented is refused by name.  The one
    capability is that the process issues the event at all.
    """
    g = genesis(reading)
    history = caller_history(wholes, DECLARED_CONVENTION, DECLARED_POLICY)
    own = process_admission(Augmentation(extra_mark=0))
    fresh: list[Event] = [AdmitOccurrence("c", 0)]
    return {
        "event": history_json(own),
        "token_already_supplied": SUPPLIED_TOKEN
        in {e.token for e in history if isinstance(e, model.Supply)},
        "accepted_without_a_new_supply": refusal(history + own, g) is None,
        "fresh_token_probe": history_json(fresh),
        "fresh_token_refused": refusal(history + fresh, g) is not None,
        "fresh_token_refusal": refusal(history + fresh, g),
        "capabilities_used": [CAPABILITY_OF["extra_mark"]],
        "note": (
            "a further mark carrying a token the caller never presented would "
            "need a supply as well, and would cost two capabilities rather "
            "than one; the enumerated candidate uses the supplied token"
        ),
    }


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def named(rows: list[Json], name: str) -> Json:
    return next(row for row in rows if row["name"] == name)


def score_c2x(u: Json, o: Json) -> Json:
    """Score the Challenge 2 extrapolation against the Challenge 3 facts."""
    minima_names = [
        member
        for entry in u["minima_by_mu1"]["classes"]
        for member in entry["members"]
    ]
    steps = u["one_step_detail"]
    sense = bool(
        u["requirement_matches_the_challenge_2_notion"]
        and o["requirement_matches_the_challenge_2_notion"]
    )
    o_already = bool(o["base"]["satisfies"]) and o["minima_by_mu1"]["minimum"] == 0
    u_unsatisfied = not u["base"]["satisfies"]
    judgment_only = u["points_satisfying_with_grammar_change_only"] == []
    literal = all(
        named(steps, name)["coordinates"]["admit_names"]
        or named(steps, name)["coordinates"]["extra_mark"] is not None
        for name in minima_names
    )
    weaker = all(
        named(steps, name)["coordinates"]["admit_names"]
        or named(steps, name)["coordinates"]["extra_mark"] is not None
        or named(steps, name)["coordinates"]["withdraw_reflection"]
        for name in minima_names
    )
    tied = int(u["minima_by_mu1"]["class_count"]) >= 2 and not u["minima_by_mu1"]["unique"]

    def verdict(hit: bool) -> str:
        return "HIT" if hit else "MISSED"

    core = sense and o_already and u_unsatisfied and judgment_only and tied
    status = "HIT" if (core and literal) else "PARTIAL" if core else "MISSED"
    return {
        "status": status,
        "label": "NOT FORCED",
        "sense_clause_status": verdict(sense),
        "O_already_satisfied_clause_status": verdict(o_already),
        "U_unsatisfied_clause_status": verdict(u_unsatisfied),
        "no_judgment_only_augmentation_clause_status": verdict(judgment_only),
        "every_minimum_names_a_side_or_admits_a_datum_clause_status": verdict(literal),
        "same_clause_on_the_weaker_reading_status": verdict(weaker),
        "tied_minima_clause_status": verdict(tied),
        "minima": minima_names,
        "every_minimum_clause_fact": (
            "the frozen clause reads 'every minimum one-step augmentation will "
            "either name a side, paying under U what reading O paid at "
            "genesis, or admit a further datum that the automorphism cannot "
            "carry', and its falsifier names 'a minimum that pays neither a "
            "side name nor a further datum'.  Two retained minima pay neither: "
            "withdrawing the side exchange admits no name, and withdrawing the "
            "mark permutations is neither.  The falsifier fired.  On the "
            "weaker reading that counts the withdrawal of the side exchange as "
            "paying what reading O paid, the clause still misses, on the "
            "second of those two"
        ),
        "evidence": (
            "the declared sense is the Challenge 2 notion; under O the "
            "requirement holds with no augmentation and the minimum count is "
            "zero; under U it fails; no candidate that only changes the "
            "judgment grammar satisfies it; and three non-isomorphic minima "
            "are retained, so uniqueness is refused"
        ),
    }


def score(u: Json, o: Json, observation_kinds: list[str]) -> Json:
    """Mechanical scoring of the frozen Challenge 3 predictions and of C2-X."""
    both = (u, o)
    u_steps = u["one_step_detail"]

    def verdict(hit: bool) -> str:
        return "HIT" if hit else "MISSED"

    c3_1 = all(
        rd["requirement_readings_agree_at_every_point"]
        and rd["requirement_matches_the_challenge_2_notion"]
        for rd in both
    ) and any(
        row["satisfies"] and row["invariant_separating_mark_properties"] == []
        for row in u_steps
    )
    square_u = u["counterfactual_square"]
    c3_2 = (
        o["base"]["satisfies"]
        and not u["base"]["satisfies"]
        and all(
            cell["requirement_met"] == (not cell["side_exchange_permitted"])
            for rd in both
            for cell in rd["counterfactual_square"]
        )
        and len(square_u) == 4
        and o["price"]["nothing_new_paid_at_challenge_3"]
        and o["price"]["capabilities_the_satisfaction_uses"]
        == [
            "admitted boundary",
            "the side exchange is not a permitted renaming",
            "occurrence identity",
        ]
        and "side names under O" in o["price"]["capabilities_not_used"]
    )
    # The frozen C3-3 clause names "the two mark forms of Challenge 2", which
    # are `on_side_0` and `on_side_1` (definition 34), and not the whole
    # declared property list: `carries_label_a` is invariant under every
    # candidate's renamings and separates nothing, both retained marks
    # carrying the same label, so it is outside the clause and is reported
    # separately.  The clause is scored on the two forms it names.
    c3_3 = (
        not named(u_steps, "admit_names")["satisfies"]
        and u["points_satisfying_with_grammar_change_only"] == []
        and "on_side_0" not in u["base"]["invariant_mark_properties"]
        and "on_side_1" not in u["base"]["invariant_mark_properties"]
        and u["base"]["invariant_separating_mark_properties"] == []
        and observation_kinds == ["OnSide", "SideNamed"]
    )
    c3_4 = all(
        rd["space_size"] == 48
        and rd["one_step_iff_capability_count_one"]
        and rd["reading_O_bundle"]["mu1"] == 2
        and rd["reading_O_bundle"]["bundles"]
        and not rd["reading_O_bundle"]["one_step"]
        and all(row["bundles"] == (row["mu1"] >= 2) for row in rd["points"])
        for rd in both
    ) and list(COORDINATES) == [
        "withdraw_reflection",
        "withdraw_mark_permutations",
        "admit_names",
        "keep_labels",
        "extra_mark",
    ]
    # The frozen C3-5 clause names four points and not an order, so the
    # comparison is by set; the enumeration's own order is the receipt's.
    c3_5 = (
        sorted(u["satisfying_one_step_points"])
        == sorted(
            [
                "withdraw_reflection",
                "withdraw_mark_permutations",
                "extra_mark_0",
                "extra_mark_1",
            ]
        )
        and u["minima_by_mu1"]["minimum"] == 1
        and u["minima_by_mu1"]["class_count"] == 3
        and not u["minima_by_mu1"]["unique"]
        and any(
            len(entry["members"]) == 2 for entry in u["minima_by_mu1"]["classes"]
        )
    )
    c3_6 = (
        all(
            named(u["points"], name)["mu2"] == 1
            for entry in u["minima_by_mu1"]["classes"]
            for name in entry["members"]
        )
        and u["measures_agree_on_minima"]
        and u["minima_by_mu2"]["minimum"] == 1
        and u["minima_by_mu2"]["class_count"] == 3
        and u["measures_differ_somewhere"]
    )
    withdraw_reflection = named(u_steps, "withdraw_reflection")
    withdraw_permutations = named(u_steps, "withdraw_mark_permutations")
    extra0 = named(u_steps, "extra_mark_0")
    extra1 = named(u_steps, "extra_mark_1")
    c3_7 = (
        withdraw_reflection["invariant_separating_mark_properties"]
        == ["on_side_0", "on_side_1"]
        and "has_index_0" not in withdraw_reflection["invariant_mark_properties"]
        and withdraw_permutations["invariant_separating_mark_properties"]
        == ["has_index_0", "has_index_1"]
        and "on_side_0" not in withdraw_permutations["invariant_mark_properties"]
        and extra0["invariant_separating_mark_properties"] == []
        and extra1["invariant_separating_mark_properties"] == []
        and withdraw_permutations["no_permitted_renaming_moves_an_index"]
        and not withdraw_reflection["no_permitted_renaming_moves_an_index"]
        and not extra0["no_permitted_renaming_moves_an_index"]
    )
    c3_8 = (
        o["minima_by_mu1"]["minimum"] == 0
        and o["minima_by_mu1"]["class_count"] == 1
        and o["minima_by_mu1"]["unique"]
        and u["minima_by_mu1"]["minimum"] == 1
        and u["minima_by_mu1"]["class_count"] == 3
        and o["price"]["requirement_met_without_augmentation"]
        and not u["price"]["requirement_met_without_augmentation"]
        and u["price"]["paid_by"] == "the run"
    )
    return {
        "C2-X": score_c2x(u, o),
        "C3-1": {
            "status": verdict(c3_1),
            "label": "NOT FORCED",
            "result_basis": (
                "DEFINITION-level: the sense is the run's declaration, and the "
                "agreement of its two readings is by unfolding, the orbit "
                "witness being invariant by construction; a hit is by "
                "construction and is not counted as content"
            ),
            "evidence": (
                "the declared sense agrees with the Challenge 2 notion at the "
                "base regime under both readings; the two readings of the "
                "requirement agree at all 48 points under each reading; and a "
                "satisfying candidate exists whose witness is the orbit "
                "property alone, no declared mark property being both "
                "invariant and separating there"
            ),
        },
        "C3-2": {
            "status": verdict(c3_2),
            "label": "FORCED",
            "result_basis": (
                "content on the side-exchange coordinate: whether an "
                "automorphism carries one retained mark to the other is a "
                "search over the unpruned enumeration, and both values are "
                "attained.  DEFINITION-level on the names coordinate: under "
                "definition 16 permission is declared and not derived from the "
                "judgment grammar, so the names cannot enter the computation, "
                "and the square exhibits that declaration's consequence rather "
                "than discovering it"
            ),
            "evidence": (
                "the O regime meets the requirement and the U regime does not; "
                "in all four cells under each reading the requirement is met "
                "exactly when the side exchange is not permitted, whether or "
                "not the names are admitted; and the O satisfaction is priced "
                "to the boundary, the withdrawal of the side exchange, and the "
                "occurrence identity, with the names recorded as not used"
            ),
        },
        "C3-3": {
            "status": verdict(c3_3),
            "label": "FORCED",
            "result_basis": (
                "content: that no property invariant under the composite "
                "separates the two retained marks is the Lean "
                "no_invariant_mark_property_separates_retained, quantified "
                "over an arbitrary property and not by unfolding, and that "
                "neither mark form is invariant under it is the Lean "
                "countermodel mark_form_is_not_invariant_under_the_composite; "
                "the census of the declared space is a computation"
            ),
            "evidence": (
                "admitting the two names into the U tower leaves the "
                "requirement unmet; no point of the declared space that "
                "changes only the judgment grammar satisfies it; and neither "
                "mark form is invariant under the permitted renamings of the U "
                "base, which is why both separate the marks as raw data and "
                "neither does so internally"
            ),
        },
        "C3-4": {
            "status": verdict(c3_4),
            "label": "NOT FORCED",
            "result_basis": (
                "DEFINITION-level: the coordinates, their values, the "
                "capability named for each, and therefore the point count and "
                "the identity of one-step with capability count one are "
                "declarations of this rung; a hit is by construction and is "
                "not counted as content"
            ),
            "evidence": (
                "five coordinates and 48 points under each reading; a point is "
                "one step exactly when its capability count is one; every "
                "point of count two or more is refused as bundling; and the "
                "reading-O candidate has count two and is refused"
            ),
        },
        "C3-5": {
            "status": verdict(c3_5),
            "label": "FORCED",
            "result_basis": (
                "content: which one-step points satisfy the requirement is a "
                "search over the unpruned enumeration at each candidate's own "
                "renamings, and the class count is the implemented quotient; "
                "the two further-mark points fall together because the side "
                "exchange carries one regime to the other, which is a witness "
                "search and not a declaration"
            ),
            "evidence": (
                "exactly four one-step points satisfy the requirement under U, "
                "in three classes, the two further-mark points being one "
                "class; the minimum capability count is one; all three classes "
                "are retained and uniqueness is refused"
            ),
        },
        "C3-6": {
            "status": verdict(c3_6),
            "label": "FORCED",
            "result_basis": (
                "content: each collateral fact is an isomorphism-witness or "
                "automorphism search at the candidate's own renamings, and "
                "that the two measures differ somewhere is a census over the "
                "48 points"
            ),
            "evidence": (
                "the collateral count is one at each of the three minima, so "
                "both measures select the same three classes at a minimum of "
                "one; and some point of the space has different values under "
                "the two measures, so neither measure is the other"
            ),
        },
        "C3-7": {
            "status": verdict(c3_7),
            "label": "FORCED",
            "result_basis": (
                "content on the first and third mechanisms: the invariance of "
                "each declared mark property is a census over the bounded "
                "domain under the candidate's renamings, and the third "
                "minimum's empty row is what makes the orbit witness "
                "necessary.  DEFINITION-level on the second: with the mark "
                "permutations withdrawn no permitted renaming moves an index "
                "at all, so that candidate satisfies the requirement by "
                "unfolding, and the receipt reports that separately"
            ),
            "evidence": (
                "withdrawing the side exchange makes both side properties "
                "invariant and separating and leaves the index properties "
                "non-invariant; withdrawing the mark permutations does the "
                "reverse, and satisfies the requirement by unfolding; "
                "admitting a further mark leaves none of the five both "
                "invariant and separating"
            ),
        },
        "C3-8": {
            "status": verdict(c3_8),
            "label": "NOT FORCED",
            "result_basis": (
                "content: the two minimum counts and the two class counts are "
                "the enumeration's results under each reading.  The "
                "boundary-dependence map beside them is the run's "
                "classification and is not computed"
            ),
            "evidence": (
                "under O the minimum capability count is zero, attained by the "
                "null augmentation alone; under U it is one, attained by three "
                "classes; nothing new is paid under O at this rung and one "
                "capability is paid by the run under U"
            ),
        },
        "C3-X": {
            "status": "PENDING",
            "label": "NOT FORCED",
            "evidence": "scored by Challenge 4",
        },
    }


def tally(scores: Json) -> Json:
    """Count the scored Challenge 3 predictions by status and by basis."""
    by_status: dict[str, list[str]] = {"HIT": [], "PARTIAL": [], "MISSED": []}
    for cid in SCORED_PREDICTIONS:
        status = scores[cid]["status"]
        if status not in by_status:
            raise ValueError(f"unexpected status {status!r} for {cid}")
        by_status[status].append(cid)
    return {
        "scored": list(SCORED_PREDICTIONS),
        "definition_level_declared": list(DEFINITION_LEVEL_PREDICTIONS),
        "criterion": TALLY_CRITERION,
        "hit_as_content": [c for c in by_status["HIT"] if c not in DEFINITION_LEVEL_PREDICTIONS],
        "hit_definition_level": [c for c in by_status["HIT"] if c in DEFINITION_LEVEL_PREDICTIONS],
        "partial": by_status["PARTIAL"],
        "missed": by_status["MISSED"],
    }


def event_returning_functions_by_module() -> dict[str, list[str]]:
    """The Challenge 0 census, run over the Challenge 3 modules."""
    return {
        "model": state_event_generators(model, EVENT_TYPES),
        "presentation": state_event_generators(presentation, EVENT_TYPES),
        "challenge2": state_event_generators(sys.modules["boundary.challenge2"], EVENT_TYPES),
        "challenge3": state_event_generators(sys.modules[__name__], EVENT_TYPES),
    }


def build() -> Json:
    u = reading_facts(READING_U)
    o = reading_facts(READING_O)
    observation_kinds = observation_vocabulary()
    scores = score(u, o, observation_kinds)
    return {
        "challenge": 3,
        "inscriptions": list(INSCRIPTIONS),
        "seed_sha256": SEED_SHA256,
        "predictions_sha256": PREDICTIONS_SHA256,
        "challenge0_predictions_sha256": C0_PREDICTIONS_SHA256,
        "challenge1_predictions_sha256": C1_PREDICTIONS_SHA256,
        "challenge2_predictions_sha256": C2_PREDICTIONS_SHA256,
        "requirement": {
            "declared": REQUIREMENT,
            "second_reading": REQUIREMENT_SECOND_READING,
            "readings_agree_because": REQUIREMENT_READINGS_AGREE_BECAUSE,
            "retained_marks": list(RETAINED_MARKS),
        },
        "candidate_space": {
            "coordinates": list(COORDINATES),
            "capability_of": CAPABILITY_OF,
            "extra_mark_values": [str(v) for v in EXTRA_MARK_VALUES],
            "size": len(candidate_space()),
            "exhaustive_over": SPACE_IS_EXHAUSTIVE_OVER,
        },
        "measures": {"mu1": MU1, "mu2": MU2},
        "capabilities": CAPABILITIES,
        "mark_properties": [name for name, _prop in DECLARED_MARK_PROPERTIES],
        "collateral_facts": list(COLLATERAL_FACTS),
        "property_domain_max_marks": PROPERTY_DOMAIN_MAX_MARKS,
        "property_domain_size": len(property_domain(READING_U, PROPERTY_DOMAIN_MAX_MARKS)),
        "readings": {READING_U: u, READING_O: o},
        "event_kinds": [t.__name__ for t in EVENT_TYPES],
        "new_event_kinds_at_challenge_3": [],
        "state_event_generators": state_event_generators(model, EVENT_TYPES),
        "event_returning_functions_by_module": event_returning_functions_by_module(),
        "observation_vocabulary": observation_kinds,
        "what_the_challenge_exercises": {
            "supply": (
                "no new one: the further-mark candidate admits the token the "
                "caller already presented, and a token never presented is "
                "refused by name"
            ),
            "mention": (
                "yes: the shared visible mark is named by every event of every "
                "candidate history and is not an identity"
            ),
            "admission": (
                "examined: the further-mark candidate is the first event in "
                "the run that the process rather than the caller would issue, "
                "and it is priced as one capability and admitted by no history "
                "the receipt certifies as current"
            ),
            "current-state designation": (
                "unchanged: the current state is still the replay of the "
                "caller's Challenge 2 history; every candidate regime is the "
                "replay of an explicit candidate history and none is current"
            ),
            "retention": (
                "unchanged: the two retained marks and their judgments are "
                "those of Challenge 2, and they survive the further admission"
            ),
            "observation": (
                "yes: the two mark forms, and under a candidate the side-name "
                "form; no new form is needed and none is added to the closed "
                "grammar"
            ),
            "side": (
                "yes: the side each retained mark lies on is what two of the "
                "three minima make internal, one by withdrawing the side "
                "exchange and one by making the two sides carry different "
                "numbers of marks"
            ),
            "equality": (
                "yes: structural regime equality, the isomorphism relation at "
                "the reading's declared renamings, and the isomorphism "
                "relation at a candidate's declared renamings are three "
                "different relations, and the rung uses all three"
            ),
        },
        "boundary_dependence": BOUNDARY_DEPENDENCE,
        "scores": scores,
        "tally": tally(scores),
        "authority_effect": "None",
    }
