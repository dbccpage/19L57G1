"""Challenge 4: the caller supplies and retains `<a|b>` and `<b|a>` and
requires their internal separability in the declared sense.

Everything computed here is metatheory about the kernel in ``model.py``, the
presentation layer in ``presentation.py``, and the Challenge 2 retention.
Nothing here is admitted beyond the caller's own history: the augmentations
are declared candidates, and every candidate's configuration is the replay of
an explicit history together with a grouping read off that history.

The rung has five parts, in this order:

1. **The reader bound.**  The Challenge 1 reader refuses both inscriptions by
   name, its declared bound being at most one mark in a whole.  The bound is
   widened deliberately to at most one mark on EACH side of the bar; the
   widening is a declared augmentation of the metatheory, paid by the run,
   and the narrower reader is left refusing so that what forced the widening
   stays visible.  In which order the two marks of one whole are admitted is
   a second declaration of the same kind as the convention.
2. **What the retention makes.**  Under the Challenge 2 reading of "retains"
   and the declared occurrence identity, the caller's history is a supply and
   an admission for each of the four marks, and the current state under each
   reading is its replay.
3. **The declared sense.**  The requirement is about the two retained WHOLES,
   and a whole is a set of marks, not a mark.  Two wholes meet it under a
   reading when no permitted automorphism of the configuration carries the
   mark-set of one onto the mark-set of the other.  The Challenge 3 sense
   taken pointwise — every pair of distinct admitted marks separable — is
   declared beside it and computed; the whole sense reduces to the Challenge
   3 sense at the Challenge 3 configuration, where each whole is one mark.
4. **What the boundary contributes here, and what it cannot.**  The boundary
   sorts the four marks by the side each lies on and no finer, and each side
   now carries one mark of each whole, so the exchange of the two wholes is a
   permitted automorphism under BOTH readings and the requirement fails under
   both — the first rung at which reading O does not already meet it.
5. **The declared candidate space and its minima.**  Seven coordinates, 192
   points, each a declared augmentation; a candidate is one step exactly when
   it moves one coordinate, and one whose capability count is two or more is
   refused as bundling.

A whole property witnesses the separation only if it is BOTH invariant under
the permitted renamings and determined by the key the candidate declares.
The second conjunct is Challenge 3's token-forgetting clause generalized, and
it is load-bearing here: the property that reads the group tag is invariant
under the renamings at every point and would otherwise be reported as a
witness at the very base where the requirement fails.

The declared space is exhaustive over its seven coordinates and over nothing
wider.  Every minimality statement below is scoped to it.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from itertools import combinations, product
from typing import Callable

from boundary import challenge0, challenge1, challenge2, challenge3, model, presentation
from boundary.challenge0 import observation_vocabulary, state_event_generators
from boundary.challenge1 import Json, judgments_json, key_json
from boundary.challenge2 import (
    DECLARED_POLICY,
    EVENT_TYPES,
    RELABELLED_TOKEN,
    history_json,
    refusal,
)
from boundary.challenge3 import minima, one_step_minima, probes
from boundary.model import (
    READING_O,
    READING_U,
    SIDE_NAMES,
    AdmitOccurrence,
    Configuration,
    Event,
    Regime,
    Renamings,
    Supply,
    Witness,
    certify,
    configuration_automorphisms,
    configuration_key,
    configurations_isomorphic,
    event_follows,
    genesis,
    marks_separable_in,
    mark_observations,
    mark_profile,
    permitted_configuration_images,
    replay,
    whole_orbit,
    wholes_separable_in,
)
from boundary.presentation import (
    DECLARED_CONVENTION,
    DECLARED_WITHIN_WHOLE_ORDER,
    OTHER_CONVENTION,
    OTHER_WITHIN_WHOLE_ORDER,
    PairWhole,
    PresentationError,
    pair_marks,
    read_pair_whole,
    read_whole,
)

SEED_SHA256 = challenge0.SEED_SHA256
C0_PREDICTIONS_SHA256 = challenge0.PREDICTIONS_SHA256
C1_PREDICTIONS_SHA256 = challenge1.PREDICTIONS_SHA256
C2_PREDICTIONS_SHA256 = challenge2.PREDICTIONS_SHA256
C3_PREDICTIONS_SHA256 = challenge3.PREDICTIONS_SHA256
PREDICTIONS_SHA256 = "42371f458e23ce89885a76c542863c112482c0ca6b4f1d9ff6a058b3c21f2041"

INSCRIPTIONS: tuple[str, str] = ("<a|b>", "<b|a>")
CALLER_TOKENS: tuple[str, str] = ("a", "b")
RETAINED_WHOLES: tuple[int, int] = (0, 1)
PROCESS_TAG = 2
FRESH_TOKEN = RELABELLED_TOKEN
PROPERTY_LABELS: tuple[str, str] = (CALLER_TOKENS[0], FRESH_TOKEN)
# The three ways four marks fall into two wholes of two; the domain carries
# all of them, because a property that reads the grouping must be tested
# against configurations whose grouping differs while their key does not.
DOMAIN_GROUPINGS: tuple[tuple[int, ...], ...] = (
    (0, 0, 1, 1),
    (0, 1, 0, 1),
    (0, 1, 1, 0),
)

READER_WIDENING = (
    "the reader admits at most one mark on EACH side of the bar, where the "
    "Challenge 1 reader admitted at most one mark in the whole"
)
WITHIN_WHOLE_ORDER_DECLARATION = (
    "the two marks of one whole are admitted in the declared within-whole "
    "order; the inscription does not fix that order any more than it fixes "
    "the convention"
)
DECLARED_AT_CHALLENGE_4: tuple[str, ...] = (
    READER_WIDENING,
    WITHIN_WHOLE_ORDER_DECLARATION,
)

REQUIREMENT = (
    "the two retained wholes are internally separable under a reading exactly "
    "when no permitted automorphism of the configuration carries the mark-set "
    "of one onto the mark-set of the other"
)
REQUIREMENT_SECOND_READING = (
    "some property of a mark-set that forgets whatever the candidate's "
    "declared key forgets, and that is invariant under every permitted "
    "renaming, holds of one retained whole's mark-set and not of the other's"
)
REQUIREMENT_POINTWISE_SENSE = (
    "the Challenge 3 sense taken pointwise: every pair of distinct admitted "
    "marks is separable, no permitted automorphism carrying one to the other"
)
REQUIREMENT_READINGS_AGREE_BECAUSE = (
    "membership in a whole's orbit under the permitted renamings is a "
    "property of a (configuration, mark-set) pair invariant under those "
    "renamings by construction, which rests on a premise stated here and "
    "checked by nothing, that a candidate's permitted renamings are closed "
    "under composition and inverse; it separates the two wholes exactly when "
    "no permitted automorphism carries one mark-set onto the other, so that "
    "half of the agreement is by unfolding and not a further fact.  What is "
    "computed at every point is the first reading against this declared "
    "witness, and not against the existential over every such property; the "
    "direction back from an arbitrary such property is the justifying "
    "sentence below, which is prose"
)
GROUPING_IS_METATHEORY = (
    "the grouping of marks into wholes is read off the caller's history and "
    "is no component of the regime.  The requirement is therefore a statement "
    "about the automorphisms of the state and about a grouping the state does "
    "not carry, and so is its declared witness, at every candidate that does "
    "not admit the grouping.  That is recorded as a narrowing of what "
    "internal separability can mean for a whole, and it is why the grouping "
    "is one of the declared coordinates"
)

COORDINATES: tuple[str, ...] = (
    "withdraw_reflection",
    "withdraw_mark_permutations",
    "admit_names",
    "keep_labels",
    "admit_grouping",
    "name_wholes",
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
    "admit_grouping": (
        "each admitted mark carries which presented whole admitted it: the "
        "grouping the caller's history holds becomes a component of the state "
        "and of the key"
    ),
    "name_wholes": (
        "the two caller whole tags are named, so their exchange is not a "
        "renaming the object language can miss"
    ),
    "extra_mark": (
        "the process extends the caller's history with an admission of its "
        "own, rather than replaying only what the caller supplied and admitted"
    ),
}
EXTRA_MARK_VALUES: tuple[int | None, int, int] = (None, 0, 1)

SPACE_IS_EXHAUSTIVE_OVER = (
    "the seven declared coordinates and their declared values, and nothing "
    "wider.  It does not enumerate an augmentation that changes the event "
    "grammar again, that admits more than one further mark in one step, that "
    "supplies a datum the caller never presented, that groups marks by "
    "anything but the presented whole, or that derives the permitted "
    "renamings from the judgment grammar instead of declaring them "
    "(definition 16).  Every minimality statement below is scoped to this "
    "space"
)

# The declared whole properties.  Each is a property of a configuration and a
# SET of internal identities, which is what a whole is here; definition 34's
# mark forms are the first two read of a set rather than of a mark.
WholeProperty = Callable[[Configuration, frozenset[int]], bool]


def set_has_a_mark_on_side_0(c: Configuration, marks: frozenset[int]) -> bool:
    """Some mark of the set lies on side 0.  Reads the placement only."""
    return any(c.regime.placement[i] == 0 for i in marks)


def set_has_a_mark_on_side_1(c: Configuration, marks: frozenset[int]) -> bool:
    """Some mark of the set lies on side 1.  Reads the placement only."""
    return any(c.regime.placement[i] == 1 for i in marks)


def set_contains_mark_0(c: Configuration, marks: frozenset[int]) -> bool:
    """The set contains the first admitted mark.  Reads the index only."""
    return 0 in marks


def set_carries_label_a_on_side_0(c: Configuration, marks: frozenset[int]) -> bool:
    """Some mark of the set carries the first caller token and lies on side 0."""
    return any(
        c.regime.marks[i] == CALLER_TOKENS[0] and c.regime.placement[i] == 0
        for i in marks
    )


def set_is_the_first_whole(c: Configuration, marks: frozenset[int]) -> bool:
    """The set is the mark-set the first caller tag groups.  Reads the tag."""
    return marks == c.members(RETAINED_WHOLES[0])


DECLARED_WHOLE_PROPERTIES: tuple[tuple[str, WholeProperty], ...] = (
    ("set_has_a_mark_on_side_0", set_has_a_mark_on_side_0),
    ("set_has_a_mark_on_side_1", set_has_a_mark_on_side_1),
    ("set_contains_mark_0", set_contains_mark_0),
    ("set_carries_label_a_on_side_0", set_carries_label_a_on_side_0),
    ("set_is_the_first_whole", set_is_the_first_whole),
)
SIDE_PROPERTIES: tuple[str, str] = (
    "set_has_a_mark_on_side_0",
    "set_has_a_mark_on_side_1",
)
WHOLE_PROPERTY_READS: dict[str, str] = {
    "set_has_a_mark_on_side_0": "the placement: which side a mark lies on",
    "set_has_a_mark_on_side_1": "the placement: which side a mark lies on",
    "set_contains_mark_0": "the admission index, a metatheoretic name",
    "set_carries_label_a_on_side_0": "a presentation label and a side",
    "set_is_the_first_whole": "the group tag, which the regime does not carry",
}

# The declared collateral facts about the retained configuration.  The second
# cost measure counts how many of them a candidate makes available that the
# same reading's base did not.
COLLATERAL_FACTS: tuple[str, ...] = (
    "sides_internally_separable",
    "marks_pairwise_separable",
    "retention_order_internally_available",
    "within_whole_order_internally_available",
    "labels_internally_available",
    "cross_boundary_matching_internally_available",
    "convention_internally_available",
    "side_names_hold",
)

MU1 = "capability count: the number of undeclared capabilities the candidate uses"
MU2 = (
    "collateral count: how many of the eight declared facts about the retained "
    "configuration the candidate makes internally available that the same "
    "reading's base did not.  The required separation of the two WHOLES is "
    "not one of the eight; two of them are near it — the same separation said "
    "of the two SIDES, and the Challenge 3 separation said pointwise of the "
    "four MARKS — and whether either takes the requirement's value at every "
    "point of the declared space is computed and reported rather than assumed"
)

SCORED_PREDICTIONS: tuple[str, ...] = (
    "C4-1", "C4-2", "C4-3", "C4-4", "C4-5", "C4-6", "C4-7", "C4-8",
)
# The scored predictions whose every hitting clause, read literally, is fixed
# by a declaration of this run: the reading of the caller's inscriptions under
# the widened reader and the declared convention, policy, and order; and the
# declared candidate space with its declared capability count.  A HIT on one
# of them is HIT by construction and is not counted as content; a miss on one
# is a miss like any other.  The criterion is the one Challenge 1 declared.
DEFINITION_LEVEL_PREDICTIONS: tuple[str, ...] = ("C4-1", "C4-4")
TALLY_CRITERION = challenge1.TALLY_CRITERION

CAPABILITIES: dict[str, dict[str, str]] = {
    "admitted boundary": {
        "declared_at": "the seed, as the one admitted primitive exception",
        "paid_by": "the seed",
        "buys_at_challenge_4": (
            "that a mark lies on a side at all, which sorts the four retained "
            "marks into two classes of two and no finer; every declared whole "
            "property but the index one and the tag one is formulable only "
            "under it, and so is the further-mark coordinate"
        ),
    },
    "side names under O": {
        "declared_at": "genesis, as the O reading of the one declaration",
        "paid_by": "the declared reading",
        "buys_at_challenge_4": (
            "nothing the requirement uses directly; what the O reading "
            "carries that reading U does not is the withdrawal of the side "
            "exchange, and at this rung that withdrawal is what makes the "
            "label-keeping candidate meet the requirement under O alone"
        ),
    },
    "the side exchange is not a permitted renaming": {
        "declared_at": (
            "genesis under O, as the other half of the O reading; at "
            "Challenge 3 and here under U, as one candidate augmentation"
        ),
        "paid_by": "the declared reading under O; the run under U",
        "buys_at_challenge_4": (
            "not the requirement: the exchange of the two wholes carries the "
            "retained configuration onto itself with no side exchange, so "
            "withdrawing the side exchange leaves the requirement unmet.  "
            "What it buys is that a property reading a label and a side is "
            "invariant, which is what the label-keeping minimum uses under O"
        ),
    },
    "occurrence identity": {
        "declared_at": "Challenge 2, as that rung's one new declaration",
        "paid_by": "the run",
        "buys_at_challenge_4": (
            "that the four presented marks are four admitted marks at all, "
            "the two wholes sharing both visible marks between them"
        ),
    },
    "presentation convention": {
        "declared_at": "Challenge 1, as metatheory",
        "paid_by": "the run",
        "buys_at_challenge_4": (
            "which presented side becomes which admitted side; not the "
            "separation, the other convention's configuration lying in the "
            "same class under both readings at the base"
        ),
    },
    "the widened reader bound": {
        "declared_at": "Challenge 4, as this rung's declaration",
        "paid_by": "the run",
        "buys_at_challenge_4": (
            "that the caller's two inscriptions can be read at all; the "
            "Challenge 1 reader refuses both by name"
        ),
    },
    "the within-whole admission order": {
        "declared_at": "Challenge 4, as this rung's second declaration",
        "paid_by": "the run",
        "buys_at_challenge_4": (
            "which mark of a whole is admitted first; not the separation, the "
            "other order giving an isomorphic configuration under both "
            "readings at the base"
        ),
    },
}

BOUNDARY_DEPENDENCE: dict[str, str] = {
    "the declared sense, its second reading, and the pointwise sense": (
        "does not depend on the admitted boundary; they are about renamings, "
        "orbits, and mark-sets, and would be stated the same way for any "
        "renaming set"
    ),
    "the identity of the candidate space, the capability counts, the one-step "
    "rule, and the refusal of bundles": "does not depend on the admitted boundary",
    "the grouping coordinates, the tag property, the index property, and the "
    "withdrawal of the mark permutations": (
        "does not depend on the admitted boundary; a group tag and an "
        "admission index are carried by the placement tuple's length and by "
        "the caller's history, not by the sides"
    ),
    "the side exchange, its withdrawal, the two side-reading whole "
    "properties, the label-and-side property, and every separation result of "
    "the rung": (
        "require the admitted boundary and are not formulated after removing it"
    ),
    "the further-mark coordinate": (
        "requires the admitted boundary: the further mark is admitted ON a "
        "side, and there is no other coordinate for it to move"
    ),
}


# ---------------------------------------------------------------------------
# The declared candidate space
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Augmentation:
    """One declared candidate augmentation: a value for each coordinate.

    A deterministic value object.  It applies nothing: a candidate becomes a
    configuration only through ``replay`` of an explicit history together with
    the grouping that history fixes, and it becomes a renaming set only by
    being handed to the kernel's declared enumerations.
    """

    withdraw_reflection: bool = False
    withdraw_mark_permutations: bool = False
    admit_names: bool = False
    keep_labels: bool = False
    admit_grouping: bool = False
    name_wholes: bool = False
    extra_mark: int | None = None

    def values(self) -> tuple[object, ...]:
        return (
            self.withdraw_reflection,
            self.withdraw_mark_permutations,
            self.admit_names,
            self.keep_labels,
            self.admit_grouping,
            self.name_wholes,
            self.extra_mark,
        )


NULL_AUGMENTATION = Augmentation()
GROUPING_BUNDLE = Augmentation(admit_grouping=True, name_wholes=True)
READING_O_BUNDLE = Augmentation(withdraw_reflection=True, admit_names=True)


def candidate_space() -> list[Augmentation]:
    """Every point of the declared space, in a deterministic order."""
    return [
        Augmentation(wr, wp, an, kl, ag, nw, em)
        for wr in (False, True)
        for wp in (False, True)
        for an in (False, True)
        for kl in (False, True)
        for ag in (False, True)
        for nw in (False, True)
        for em in EXTRA_MARK_VALUES
    ]


def changed_coordinates(aug: Augmentation) -> list[str]:
    """The coordinates the candidate moves off their inherited values.

    Each coordinate is tested against its own inherited value rather than
    against a shared falsehood, as Challenge 3 was repaired to do:
    ``extra_mark`` is inherited as ``None`` and its value ``0`` is a move,
    which a truth test would silently drop.
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
    if aug.admit_grouping:
        moved.append("admit_grouping")
    if aug.name_wholes:
        moved.append("name_wholes")
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
    return "+".join(
        f"extra_mark_{aug.extra_mark}" if name == "extra_mark" else name
        for name in moved
    )


# ---------------------------------------------------------------------------
# What a candidate declares
# ---------------------------------------------------------------------------


def reflection_permitted(reading: str, aug: Augmentation) -> bool:
    """Under O the side exchange is not permitted whatever the candidate says;
    under U it is permitted unless the candidate withdraws it."""
    return reading == READING_U and not aug.withdraw_reflection


def names_admitted(reading: str, aug: Augmentation) -> bool:
    """Whether the side-name judgment form is in this candidate's grammar."""
    return reading == READING_O or aug.admit_names


def renamings(reading: str, aug: Augmentation) -> Renamings:
    """The five flags the kernel's declared enumerations take.

    The tag exchange is a permitted renaming exactly when the grouping is
    admitted and the two wholes are not named: naming wholes that no mark
    carries changes nothing, which is why that point collapses into the base.
    """
    return Renamings(
        reflection=reflection_permitted(reading, aug),
        mark_permutations=not aug.withdraw_mark_permutations,
        group_permutations=aug.admit_grouping and not aug.name_wholes,
        keep_labels=aug.keep_labels,
        keep_groups=aug.admit_grouping,
    )


def effective_structure(reading: str, aug: Augmentation) -> tuple[object, ...]:
    """What the candidate actually declares once the reading is applied.

    Two points that declare the same renamings and the same key are the same
    structure however their raw coordinates read: under O, withdrawing an
    already absent side exchange and admitting already admitted names change
    nothing, and under both readings naming the wholes without admitting the
    grouping changes nothing.
    """
    rn = renamings(reading, aug)
    return (
        rn.reflection,
        rn.mark_permutations,
        names_admitted(reading, aug),
        rn.keep_labels,
        rn.keep_groups,
        rn.group_permutations,
    )


# ---------------------------------------------------------------------------
# The caller's history, the grouping, and the comparison configurations
# ---------------------------------------------------------------------------


def caller_wholes() -> list[PairWhole]:
    """The two inscriptions, read under the widened bound."""
    return [read_pair_whole(text) for text in INSCRIPTIONS]


def retention_history(
    wholes: list[PairWhole],
    convention: str = DECLARED_CONVENTION,
    order: str = DECLARED_WITHIN_WHOLE_ORDER,
) -> list[Event]:
    """The caller's Challenge 4 history: for each retained whole, a supply for
    each of its marks and then an occurrence admission for each, in the
    declared within-whole order.

    The supplies come in presented order, left then right, because a whole is
    presented once and presents both its marks; the admissions come in the
    declared order.  Supply, admission, and retention are three things and are
    kept apart here as at every earlier rung.
    """
    history: list[Event] = []
    for whole in wholes:
        for token in (whole.left, whole.right):
            if token is not None:
                history.append(Supply(token))
        for token, side in pair_marks(whole, convention, order):
            history.append(AdmitOccurrence(token, side))
    return history


def retention_groups(
    wholes: list[PairWhole], aug: Augmentation = NULL_AUGMENTATION
) -> tuple[int, ...]:
    """The grouping the caller's history fixes: for each admitted mark, in
    admission order, the tag of the whole whose admission introduced it.

    The process's own further mark, when a candidate declares one, carries a
    tag of its own: it is no whole the caller presented.
    """
    tags: list[int] = []
    for tag, whole in enumerate(wholes):
        tags.extend(tag for _token in (whole.left, whole.right) if _token is not None)
    if aug.extra_mark is not None:
        tags.append(PROCESS_TAG)
    return tuple(tags)


def process_admission(aug: Augmentation) -> list[Event]:
    """The event the process adds for a further-mark candidate; nothing else.

    The token is one the caller already supplied, so no supply is needed and
    the candidate uses exactly one new capability: that the process, not the
    caller, issues the event.
    """
    if aug.extra_mark is None:
        return []
    return [AdmitOccurrence(CALLER_TOKENS[0], aug.extra_mark)]


def candidate_history(
    wholes: list[PairWhole],
    aug: Augmentation,
    convention: str = DECLARED_CONVENTION,
    order: str = DECLARED_WITHIN_WHOLE_ORDER,
) -> list[Event]:
    """The caller's history under a convention and a within-whole order,
    extended by the process's own admission when the candidate declares one."""
    return retention_history(wholes, convention, order) + process_admission(aug)


def configuration_of(
    reading: str,
    wholes: list[PairWhole],
    aug: Augmentation,
    convention: str = DECLARED_CONVENTION,
    order: str = DECLARED_WITHIN_WHOLE_ORDER,
) -> Configuration:
    """The candidate's configuration: the replay of its explicit history, with
    the grouping that history fixes."""
    history = candidate_history(wholes, aug, convention, order)
    return Configuration(
        replay(history, genesis(reading)), retention_groups(wholes, aug)
    )


def relabelled(c: Configuration) -> Configuration:
    """The same placement and grouping under one visible mark throughout."""
    return Configuration(
        Regime(
            c.regime.reading,
            tuple(FRESH_TOKEN for _ in c.regime.marks),
            c.regime.placement,
        ),
        c.groups,
    )


def matching_broken(c: Configuration) -> Configuration:
    """The same configuration with the second whole's copy of the first
    caller token replaced by a token the caller never presented.

    This is the operational form of "the matching of a visible mark across the
    boundary": if the object language cannot tell this configuration from the
    retained one, it cannot tell that the two wholes share a visible mark.
    """
    second = sorted(c.members(RETAINED_WHOLES[1]))
    marks = list(c.regime.marks)
    for i in second:
        if marks[i] == CALLER_TOKENS[0]:
            marks[i] = FRESH_TOKEN
            break
    return Configuration(
        Regime(c.regime.reading, tuple(marks), c.regime.placement), c.groups
    )


def comparison_configurations(
    reading: str, wholes: list[PairWhole], aug: Augmentation
) -> dict[str, Configuration]:
    """The candidate's configuration and the four it is compared with."""
    main = configuration_of(reading, wholes, aug)
    return {
        "main": main,
        "other_retention_order": configuration_of(
            reading, list(reversed(wholes)), aug
        ),
        "other_within_whole_order": configuration_of(
            reading, wholes, aug, DECLARED_CONVENTION, OTHER_WITHIN_WHOLE_ORDER
        ),
        "relabelled": relabelled(main),
        "matching_broken": matching_broken(main),
        "other_convention": configuration_of(
            reading, wholes, aug, OTHER_CONVENTION, DECLARED_WITHIN_WHOLE_ORDER
        ),
    }


# ---------------------------------------------------------------------------
# The requirement, in its declared readings
# ---------------------------------------------------------------------------


def requirement_met(c: Configuration, rn: Renamings) -> bool:
    """The declared requirement: no permitted automorphism carries the mark-set
    of one retained whole onto the mark-set of the other."""
    a, b = RETAINED_WHOLES
    return wholes_separable_in(c, a, b, rn)


def orbit_witness_separates(c: Configuration, rn: Renamings) -> bool:
    """The second reading of the requirement, at its declared orbit witness."""
    a, b = RETAINED_WHOLES
    return (configuration_key(c, rn), c.members(b)) not in whole_orbit(c, a, rn)


def mark_pairs(c: Configuration) -> list[tuple[int, int]]:
    return list(combinations(range(c.regime.n_marks()), 2))


def separable_mark_pairs(c: Configuration, rn: Renamings) -> list[tuple[int, int]]:
    """The pairs of distinct admitted marks no permitted automorphism joins."""
    return [(i, j) for i, j in mark_pairs(c) if marks_separable_in(c, i, j, rn)]


def marks_pairwise_separable(c: Configuration, rn: Renamings) -> bool:
    """The Challenge 3 sense taken pointwise over every pair."""
    return len(separable_mark_pairs(c, rn)) == len(mark_pairs(c))


# ---------------------------------------------------------------------------
# The declared whole-property census
# ---------------------------------------------------------------------------


def property_domain(reading: str) -> list[Configuration]:
    """Every configuration of two two-mark wholes over the two declared labels
    and the three declared groupings; none of them is admitted.

    The grouping varies because a property that reads the tag must be tested
    against configurations whose grouping differs while their key does not;
    with one grouping throughout, such a property would be reported as
    determined by a key that does not carry it.  That was live: the tag
    property was reported as a witness at the very base where the requirement
    fails, and the two-set family below is the other half of the repair.
    """
    return [
        Configuration(Regime(reading, labels, placement), groups)
        for groups in DOMAIN_GROUPINGS
        for labels in product(PROPERTY_LABELS, repeat=4)
        for placement in product((0, 1), repeat=4)
    ]


def two_element_sets(n: int) -> list[frozenset[int]]:
    """Every two-element mark-set of an ``n``-mark configuration.

    A whole of this rung is such a set, and the key-determination census runs
    over all of them: a property evaluated only at a configuration's OWN two
    wholes is constant by construction if it reads the tag, which is what made
    the first census report the tag property as a witness.
    """
    return [frozenset(pair) for pair in combinations(range(n), 2)]


# One domain configuration, its two whole mark-sets, and for each permitted
# image the image with the two sets carried along.  Computed once per flag
# triple so that the property census enumerates no image twice.
DomainEntry = tuple[
    Configuration,
    tuple[frozenset[int], frozenset[int]],
    list[tuple[Configuration, frozenset[int], frozenset[int]]],
]
DomainImages = list[DomainEntry]


def domain_images(domain: list[Configuration], rn: Renamings) -> DomainImages:
    """Every configuration of the domain with the images the candidate permits
    and the image of each of its two wholes under each."""
    out: DomainImages = []
    for c in domain:
        sets = (c.members(RETAINED_WHOLES[0]), c.members(RETAINED_WHOLES[1]))
        carried = [
            (
                image,
                frozenset(pi[i] for i in sets[0]),
                frozenset(pi[i] for i in sets[1]),
            )
            for _reflected, pi, _sigma, image in permitted_configuration_images(c, rn)
        ]
        out.append((c, sets, carried))
    return out


def property_invariant(prop: WholeProperty, images: DomainImages) -> bool:
    """Whether a whole property holds of a whole exactly when it holds of that
    whole's image, at every configuration of the domain, every permitted image,
    and each of the two declared whole tags.

    The image of the whole tagged ``w`` is the whole whose marks are the images
    of that whole's marks; where the tag map is not the identity it carries a
    different tag, which is exactly what makes the tag property fail this test
    when the two wholes are unnamed.
    """
    return all(
        prop(image, first) == prop(c, sets[0]) and prop(image, second) == prop(c, sets[1])
        for c, sets, carried in images
        for image, first, second in carried
    )


def property_key_determined(
    prop: WholeProperty, domain: list[Configuration], rn: Renamings
) -> bool:
    """Whether the property forgets whatever the candidate's key forgets.

    Two configurations of the domain with equal keys must give the property
    equal values at every two-element mark-set.  This is Challenge 3's
    token-forgetting clause generalized, and it is what stops a property that
    reads the group tag — which no key carries unless the grouping is admitted
    — from being reported as a witness at a point where the requirement fails.
    """
    sets = two_element_sets(4)
    seen: dict[tuple[object, ...], tuple[bool, ...]] = {}
    for c in domain:
        key = configuration_key(c, rn)
        values = tuple(prop(c, marks) for marks in sets)
        if key in seen:
            if seen[key] != values:
                return False
        else:
            seen[key] = values
    return True


def property_separates(prop: WholeProperty, c: Configuration) -> bool:
    a, b = RETAINED_WHOLES
    return prop(c, c.members(a)) != prop(c, c.members(b))


def whole_property_facts(
    c: Configuration, domain: list[Configuration], images: DomainImages, rn: Renamings
) -> dict[str, list[str]]:
    """Which declared whole properties are invariant, which are determined by
    the candidate's key, which separate the two retained wholes, and which do
    all three.  Only the last is a witness."""
    invariant = [
        name for name, prop in DECLARED_WHOLE_PROPERTIES if property_invariant(prop, images)
    ]
    determined = [
        name
        for name, prop in DECLARED_WHOLE_PROPERTIES
        if property_key_determined(prop, domain, rn)
    ]
    separating = [
        name for name, prop in DECLARED_WHOLE_PROPERTIES if property_separates(prop, c)
    ]
    return {
        "invariant": invariant,
        "key_determined": determined,
        "separating": separating,
        "witnesses": [
            name for name in separating if name in invariant and name in determined
        ],
    }


# ---------------------------------------------------------------------------
# The collateral facts and the second measure
# ---------------------------------------------------------------------------


COMPARISONS: tuple[tuple[str, str], ...] = (
    ("other_retention_order", "retention_order_internally_available"),
    ("other_within_whole_order", "within_whole_order_internally_available"),
    ("relabelled", "labels_internally_available"),
    ("matching_broken", "cross_boundary_matching_internally_available"),
    ("other_convention", "convention_internally_available"),
)


@dataclass
class Analysis:
    """One candidate, computed from ONE unpruned enumeration of its images.

    Every value below is the kernel's own definition read off that single
    enumeration rather than recomputed per question; the kernel functions stay
    the declared ones and a test cross-checks the two at every one-step point
    and at a sample of bundles.  Metatheory apparatus: nothing is admitted.
    """

    reading: str
    aug: Augmentation
    main: Configuration
    rn: Renamings
    images: list[tuple[bool, tuple[int, ...], tuple[int, ...], Configuration]]
    automorphisms: list[Witness]
    facts: dict[str, bool]
    satisfies: bool
    second_reading: bool
    whole_exchange: Witness | None
    side_exchange: Witness | None
    separable_pairs: list[tuple[int, int]]
    least_key: list[object]


def analyse(reading: str, aug: Augmentation, wholes: list[PairWhole]) -> Analysis:
    """Compute one candidate's facts from a single enumeration of its images."""
    parts = comparison_configurations(reading, wholes, aug)
    main = parts["main"]
    rn = renamings(reading, aug)
    images = permitted_configuration_images(main, rn)
    target = configuration_key(main, rn)
    reached = {configuration_key(image, rn) for _r, _p, _s, image in images}
    autos: list[Witness] = [
        (reflected, pi, sigma)
        for reflected, pi, sigma, image in images
        if configuration_key(image, rn) == target
    ]
    a, b = RETAINED_WHOLES
    first, second = main.members(a), main.members(b)
    whole_exchange = next(
        ((r, p, s) for r, p, s in autos if frozenset(p[i] for i in first) == second), None
    )
    side_exchange = next(((r, p, s) for r, p, s in autos if r), None)
    n = main.regime.n_marks()
    separable = [
        (i, j)
        for i, j in combinations(range(n), 2)
        if all(pi[i] != j for _r, pi, _s in autos)
    ]
    orbit = {
        (configuration_key(image, rn), frozenset(pi[i] for i in first))
        for _r, pi, _s, image in images
    }
    facts = {
        "sides_internally_separable": side_exchange is None,
        "marks_pairwise_separable": len(separable) == len(list(combinations(range(n), 2))),
        **{
            fact: configuration_key(parts[name], rn) not in reached
            for name, fact in COMPARISONS
        },
        "side_names_hold": names_admitted(reading, aug),
    }
    return Analysis(
        reading=reading,
        aug=aug,
        main=main,
        rn=rn,
        images=images,
        automorphisms=autos,
        facts=facts,
        satisfies=whole_exchange is None,
        second_reading=(target, second) not in orbit,
        whole_exchange=whole_exchange,
        side_exchange=side_exchange,
        separable_pairs=separable,
        least_key=min(
            key_json(configuration_key(image, rn)) for _r, _p, _s, image in images
        ),
    )


def collateral_facts(
    reading: str, aug: Augmentation, parts: dict[str, Configuration]
) -> dict[str, bool]:
    """The eight declared facts, computed under the candidate's own renamings
    by the kernel's own functions.

    ``analyse`` derives the same eight from one enumeration; this is the
    declared form, and the two are checked to agree.
    """
    rn = renamings(reading, aug)
    main = parts["main"]
    return {
        "sides_internally_separable": not any(
            reflected for reflected, _pi, _sigma in configuration_automorphisms(main, rn)
        ),
        "marks_pairwise_separable": marks_pairwise_separable(main, rn),
        **{
            fact: not configurations_isomorphic(main, parts[name], rn)
            for name, fact in COMPARISONS
        },
        "side_names_hold": names_admitted(reading, aug),
    }


def mu2(facts: dict[str, bool], base_facts: dict[str, bool]) -> int:
    """The second declared cost measure: newly available collateral facts."""
    return sum(1 for name in COLLATERAL_FACTS if facts[name] and not base_facts[name])


def holding(facts: dict[str, bool]) -> list[str]:
    """The declared collateral facts that hold, in the declared order."""
    return [name for name in COLLATERAL_FACTS if facts[name]]


def fact_agrees_with_the_requirement(rows: list[Json], fact: str) -> bool:
    """Whether one declared collateral fact takes the requirement's value at
    every enumerated point.

    Challenge 3 found that its first declared fact did, so that its second
    measure re-counted the requirement rather than reading what a candidate
    costs beside it.  This rung computes the same thing for the two facts that
    are near the requirement and reports the answers as they come.
    """
    return all(
        (fact in row["collateral_facts_holding"]) == row["satisfies"] for row in rows
    )


# ---------------------------------------------------------------------------
# Rows of the enumeration
# ---------------------------------------------------------------------------


def witness_json(witness: Witness | None) -> Json | None:
    if witness is None:
        return None
    return {
        "reflected": witness[0],
        "permutation": list(witness[1]),
        "tag_map": list(witness[2]),
    }


def class_key(reading: str, aug: Augmentation, least_key: list[object]) -> list[object]:
    """The implemented quotient: the structure the candidate declares, with the
    least key of its configuration under that structure's own renamings."""
    return [*[str(part) for part in effective_structure(reading, aug)], least_key]


def point_row(analysis: Analysis, base_facts: dict[str, bool]) -> Json:
    """One point of the declared space: its cost under each measure, whether it
    is one step, whether it bundles, and whether it meets the requirement in
    each of the declared readings of it.

    The row carries the facts that HOLD rather than eight booleans, the
    declared list in the receipt's ``collateral_facts`` being what the names
    are read against; the one-step rows carry the full map beside it.
    """
    aug = analysis.aug
    return {
        "name": point_name(aug),
        "coordinates": dict(zip(COORDINATES, aug.values())),
        "capability_coordinates": changed_coordinates(aug),
        "mu1": mu1(aug),
        "mu2": mu2(analysis.facts, base_facts),
        "one_step": is_one_step(aug),
        "bundles": bundles(aug),
        "satisfies": analysis.satisfies,
        "satisfies_second_reading": analysis.second_reading,
        "marks_pairwise_separable": analysis.facts["marks_pairwise_separable"],
        "class_key": class_key(analysis.reading, aug, analysis.least_key),
        "collateral_facts_holding": holding(analysis.facts),
    }


def expected_placement(
    wholes: list[PairWhole], aug: Augmentation
) -> list[int]:
    """The placement the declared convention and within-whole order predict.

    Computed from the presented sides and the declarations alone, so that the
    receipt carries one statement about the candidate configuration that is not
    a comparison of a replay with itself.
    """
    out = [
        side
        for whole in wholes
        for _token, side in pair_marks(whole, DECLARED_CONVENTION, DECLARED_WITHIN_WHOLE_ORDER)
    ]
    if aug.extra_mark is not None:
        out.append(aug.extra_mark)
    return out


def one_step_detail(
    analysis: Analysis,
    wholes: list[PairWhole],
    domain: list[Configuration],
    images_cache: dict[tuple[bool, bool, bool], DomainImages],
    base_facts: dict[str, bool],
) -> Json:
    """The full report for one candidate: its history, its configuration, its
    automorphisms, the requirement in both of its readings, the pairwise sense
    beside it, and which declared whole property witnesses the separation."""
    reading, aug, main, rn = analysis.reading, analysis.aug, analysis.main, analysis.rn
    g = genesis(reading)
    history = candidate_history(wholes, aug)
    images = images_cache[(rn.reflection, rn.mark_permutations, rn.group_permutations)]
    props = whole_property_facts(main, domain, images, rn)
    row = point_row(analysis, base_facts)
    row.update(
        {
            "capabilities": capabilities(aug),
            "effective_structure": [
                str(part) for part in effective_structure(reading, aug)
            ],
            "history": history_json(history),
            "certified": certify(history, g, main.regime),
            "replays_from_genesis": replay(history, g) == main.regime,
            "marks": main.regime.n_marks(),
            "placement": list(main.regime.placement),
            "placement_matches_the_declarations": list(main.regime.placement)
            == expected_placement(wholes, aug),
            "labels": list(main.regime.marks),
            "groups": list(main.groups),
            "whole_members": [sorted(main.members(w)) for w in RETAINED_WHOLES],
            "permitted_renamings": {
                "side_exchange": rn.reflection,
                "mark_permutations": rn.mark_permutations,
                "tag_exchange": rn.group_permutations,
                "labels_kept": rn.keep_labels,
                "groups_kept": rn.keep_groups,
                "names_admitted": names_admitted(reading, aug),
                "images": len(analysis.images),
            },
            "collateral_facts": analysis.facts,
            "automorphism_count": len(analysis.automorphisms),
            "automorphism_entries": [
                witness_json(entry) for entry in analysis.automorphisms
            ],
            "whole_exchange_witness": witness_json(analysis.whole_exchange),
            "side_exchange_witness": witness_json(analysis.side_exchange),
            "separable_mark_pairs": [list(pair) for pair in analysis.separable_pairs],
            "mark_pair_count": len(mark_pairs(main)),
            "no_permitted_renaming_moves_an_index": all(
                pi == tuple(range(main.regime.n_marks()))
                for _reflected, pi, _sigma, _image in analysis.images
            ),
            "invariant_whole_properties": props["invariant"],
            "key_determined_whole_properties": props["key_determined"],
            "separating_whole_properties": props["separating"],
            "witness_whole_properties": props["witnesses"],
            "orbit_size": len(whole_orbit(main, RETAINED_WHOLES[0], rn)),
            "mark_profiles": [
                judgments_json(mark_profile(main.regime, k))
                for k in range(main.regime.n_marks())
            ],
            "marks_on_each_side": [
                sum(1 for s in main.regime.placement if s == side) for side in (0, 1)
            ],
            "mark_side_names": (
                [SIDE_NAMES[side] for side in main.regime.placement]
                if names_admitted(reading, aug)
                else []
            ),
            "holding_mark_judgments": len(mark_observations(main.regime)),
            "holding_judgments_with_names": len(mark_observations(main.regime))
            + (2 if names_admitted(reading, aug) else 0),
            "event_follows_relation_empty": all(
                not event_follows(main.regime, e) for e in probes(CALLER_TOKENS[0])
            ),
            "initial_datum_unchanged": main.regime.initial_datum == g.initial_datum,
            "reading_unchanged": main.regime.reading == reading,
        }
    )
    return row


# ---------------------------------------------------------------------------
# The grouping square, the reader, and the price
# ---------------------------------------------------------------------------


def grouping_square(reading: str, wholes: list[PairWhole]) -> list[Json]:
    """The requirement at the retained configuration over (the grouping
    admitted) by (the two wholes named), four cells under each reading.

    It isolates what the caller's own demand costs: the grouping alone leaves
    the tag exchange a renaming the object language cannot see, the names
    alone name tags no mark carries, and only the two together meet the
    requirement — at a capability count of two.
    """
    out: list[Json] = []
    for grouping in (False, True):
        for named in (False, True):
            aug = Augmentation(admit_grouping=grouping, name_wholes=named)
            main = configuration_of(reading, wholes, aug)
            out.append(
                {
                    "grouping_admitted": grouping,
                    "wholes_named": named,
                    "requirement_met": requirement_met(main, renamings(reading, aug)),
                    "capability_count": mu1(aug),
                    "is_the_inherited_cell": not grouping and not named,
                }
            )
    return out


def reader_facts() -> Json:
    """What the Challenge 1 reader does with the caller's inscriptions, and
    what the widened reader reads."""
    refusals: list[Json] = []
    for text in INSCRIPTIONS:
        try:
            read_whole(text)
        except PresentationError as exc:
            refusals.append({"inscription": text, "refused": True, "refusal": str(exc)})
        else:  # pragma: no cover - the narrow reader refuses by construction
            refusals.append({"inscription": text, "refused": False, "refusal": None})
    wholes = caller_wholes()
    return {
        "challenge_1_reader": refusals,
        "challenge_1_reader_refuses_both": all(row["refused"] for row in refusals),
        "widened_bound": READER_WIDENING,
        "widened_reader_reads": [
            {"left": whole.left, "right": whole.right} for whole in wholes
        ],
        "declared_within_whole_order": DECLARED_WITHIN_WHOLE_ORDER,
        "other_within_whole_order": OTHER_WITHIN_WHOLE_ORDER,
        "within_whole_order_declaration": WITHIN_WHOLE_ORDER_DECLARATION,
        "declared_at_challenge_4": list(DECLARED_AT_CHALLENGE_4),
        "paid_by": "the run",
        "nested_whole_probe": "<<a|>|>",
        "nested_whole_refused": nested_whole_refusal() is not None,
        "nested_whole_refusal": nested_whole_refusal(),
    }


def nested_whole_refusal() -> str | None:
    """The message the widened reader refuses a nested whole with, or ``None``.

    Recorded here and not acted on: what a whole within a side is belongs to
    the next rung, and this rung records only that its own reader refuses it.
    """
    try:
        read_pair_whole("<<a|>|>")
    except PresentationError as exc:
        return str(exc)
    return None  # pragma: no cover - the reader refuses by construction


PRICE_FIELDS_DECLARED: tuple[str, ...] = (
    "capabilities_the_satisfaction_would_use",
    "capabilities_not_used",
    "declared_at",
    "paid_by",
)


def price_facts(reading: str, base_met: bool, by_mu1: Json, rows: list[Json]) -> Json:
    """What the requirement costs under this reading, and who pays it.

    Four of the eight fields move with the run: ``minimum_capability_count``,
    ``nothing_new_paid_at_challenge_4``, ``new_at_challenge_4`` (the capability
    coordinates of the retained minima), and
    ``requirement_met_without_augmentation``.  The other four are declarations
    this function writes and no run can move, and the receipt names them under
    ``fields_declared_not_computed`` so that a reader is not invited to take a
    declaration for a measurement — the repair Challenge 3 made to the same
    shape, carried forward rather than repeated as a defect.
    """
    minimum = by_mu1["minimum"]
    paid = sorted(
        {
            capability
            for entry in by_mu1["classes"]
            for member in entry["members"]
            for capability in named(rows, str(member))["capability_coordinates"]
        }
    )
    return {
        "requirement_met_without_augmentation": base_met,
        "capabilities_the_satisfaction_would_use": [
            "admitted boundary",
            "occurrence identity",
            "the widened reader bound",
        ],
        "capabilities_not_used": (
            ["side names under O"] if reading == READING_O else []
        ),
        "declared_at": "Challenge 4, by whichever retained minimum is taken",
        "paid_by": "the run",
        "new_at_challenge_4": paid,
        "nothing_new_paid_at_challenge_4": minimum == 0,
        "minimum_capability_count": minimum,
        "declared_regardless_at_challenge_4": list(DECLARED_AT_CHALLENGE_4),
        "fields_declared_not_computed": list(PRICE_FIELDS_DECLARED),
    }


def named(rows: list[Json], name: str) -> Json:
    return next(row for row in rows if row["name"] == name)


# ---------------------------------------------------------------------------
# The reduction to Challenge 3, and the process's own admission
# ---------------------------------------------------------------------------


def reduction_to_challenge_3(reading: str) -> Json:
    """At the Challenge 3 configuration each whole is one mark, and the whole
    sense is then the Challenge 3 sense.

    The Challenge 2 retention replayed with one tag per whole: two marks,
    placement `(0, 1)`, labels `("a", "a")`.  The comparison is computed and
    not asserted.
    """
    g = genesis(reading)
    history: list[Event] = [
        Supply(CALLER_TOKENS[0]),
        AdmitOccurrence(CALLER_TOKENS[0], 0),
        Supply(CALLER_TOKENS[0]),
        AdmitOccurrence(CALLER_TOKENS[0], 1),
    ]
    c = Configuration(replay(history, g), (0, 1))
    rn = renamings(reading, NULL_AUGMENTATION)
    a, b = RETAINED_WHOLES
    whole = wholes_separable_in(c, a, b, rn)
    mark = marks_separable_in(c, 0, 1, rn)
    return {
        "history": history_json(history),
        "placement": list(c.regime.placement),
        "labels": list(c.regime.marks),
        "groups": list(c.groups),
        "whole_sense": whole,
        "pointwise_sense": mark,
        "senses_agree": whole == mark,
    }


def process_admission_facts(reading: str, wholes: list[PairWhole]) -> Json:
    """What the further-mark candidate needs, and what it does not."""
    g = genesis(reading)
    history = retention_history(wholes)
    own = process_admission(Augmentation(extra_mark=0))
    fresh: list[Event] = [AdmitOccurrence("c", 0)]
    return {
        "event": history_json(own),
        "token_already_supplied": CALLER_TOKENS[0]
        in {e.token for e in history if isinstance(e, Supply)},
        "accepted_without_a_new_supply": refusal(history + own, g) is None,
        "fresh_token_probe": history_json(fresh),
        "fresh_token_refused": refusal(history + fresh, g) is not None,
        "fresh_token_refusal": refusal(history + fresh, g),
        "carries_a_tag_of_its_own": PROCESS_TAG,
        "capabilities_used": [CAPABILITY_OF["extra_mark"]],
        "note": (
            "the further mark belongs to no whole the caller presented, so it "
            "carries a tag of its own; it needs no supply, the caller having "
            "presented its token, and a token never presented is refused by "
            "name"
        ),
    }


# ---------------------------------------------------------------------------
# The reading facts
# ---------------------------------------------------------------------------


def reading_facts(reading: str) -> Json:
    wholes = caller_wholes()
    domain = property_domain(reading)
    space = candidate_space()
    one_step = [aug for aug in space if is_one_step(aug)]
    analyses = {point_name(aug): analyse(reading, aug, wholes) for aug in space}
    base_facts = analyses["base"].facts
    images_cache: dict[tuple[bool, bool, bool], DomainImages] = {}
    for aug in [NULL_AUGMENTATION, *one_step]:
        rn = renamings(reading, aug)
        flags = (rn.reflection, rn.mark_permutations, rn.group_permutations)
        if flags not in images_cache:
            images_cache[flags] = domain_images(domain, rn)
    rows = [point_row(analyses[point_name(aug)], base_facts) for aug in space]
    base = one_step_detail(
        analyses["base"], wholes, domain, images_cache, base_facts
    )
    steps = [
        one_step_detail(
            analyses[point_name(aug)], wholes, domain, images_cache, base_facts
        )
        for aug in one_step
    ]
    by_mu1 = one_step_minima(rows, "mu1")
    by_mu2 = one_step_minima(rows, "mu2")
    parted = [
        str(row["name"])
        for row in rows
        if row["satisfies"] != row["marks_pairwise_separable"]
    ]
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
        "minima_by_mu1": by_mu1,
        "minima_by_mu2": by_mu2,
        "measures_agree_on_minima": by_mu1["points"] == by_mu2["points"],
        "measures_differ_somewhere": any(row["mu1"] != row["mu2"] for row in rows),
        "one_step_iff_capability_count_one": all(
            row["one_step"] == (row["mu1"] == 1) for row in rows
        ),
        "bundles_refused": [str(row["name"]) for row in rows if row["bundles"]],
        "bundles_refused_count": sum(1 for row in rows if row["bundles"]),
        "grouping_bundle": {
            "name": point_name(GROUPING_BUNDLE),
            "mu1": named(rows, point_name(GROUPING_BUNDLE))["mu1"],
            "one_step": named(rows, point_name(GROUPING_BUNDLE))["one_step"],
            "bundles": named(rows, point_name(GROUPING_BUNDLE))["bundles"],
            "satisfies": named(rows, point_name(GROUPING_BUNDLE))["satisfies"],
            "refused_because": (
                "it moves two coordinates and uses two capabilities, so it is "
                "not one step; and neither half alone is a minimum, the "
                "grouping alone leaving the tag exchange a renaming the object "
                "language cannot see and the names alone naming tags no mark "
                "carries"
            ),
        },
        "reading_O_bundle": {
            "name": point_name(READING_O_BUNDLE),
            "mu1": named(rows, point_name(READING_O_BUNDLE))["mu1"],
            "satisfies": named(rows, point_name(READING_O_BUNDLE))["satisfies"],
        },
        "name_wholes_collapses_into_the_base": named(
            rows, "name_wholes"
        )["class_key"] == named(rows, "base")["class_key"],
        "grouping_square": grouping_square(reading, wholes),
        "requirement_readings_agree_at_every_point": all(
            row["satisfies"] == row["satisfies_second_reading"] for row in rows
        ),
        "pointwise_implies_whole_at_every_point": all(
            row["satisfies"] for row in rows if row["marks_pairwise_separable"]
        ),
        "points_where_the_two_senses_part": parted,
        "at_every_parting_point_the_wholes_separate_and_the_marks_do_not": all(
            named(rows, name)["satisfies"]
            and not named(rows, name)["marks_pairwise_separable"]
            for name in parted
        ),
        "sides_fact_agrees_with_the_requirement_at_every_point": (
            fact_agrees_with_the_requirement(rows, "sides_internally_separable")
        ),
        "pairwise_fact_agrees_with_the_requirement_at_every_point": (
            fact_agrees_with_the_requirement(rows, "marks_pairwise_separable")
        ),
        "price": price_facts(reading, bool(base["satisfies"]), by_mu1, rows),
        "process_admission": process_admission_facts(reading, wholes),
        "reduction_to_challenge_3": reduction_to_challenge_3(reading),
    }


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def score_c3x(u: Json, o: Json, reader: Json) -> Json:
    """Score the Challenge 3 extrapolation against the Challenge 4 facts."""
    u_base = u["base"]
    o_base = o["base"]

    def verdict(hit: bool) -> str:
        return "HIT" if hit else "MISSED"

    reader_clause = bool(reader["challenge_1_reader_refuses_both"]) and reader[
        "paid_by"
    ] == "the run"
    placement_clause = (
        u_base["placement"] == [0, 1, 0, 1] and o_base["placement"] == [0, 1, 0, 1]
    )
    counts_clause = (
        u_base["marks_on_each_side"] == [2, 2]
        and o_base["marks_on_each_side"] == [2, 2]
        and u_base["side_exchange_witness"] is not None
    )
    u_clause = (not u_base["satisfies"]) and u["minima_by_mu1"]["minimum"] == 1
    o_clause = bool(o_base["satisfies"])
    # The frozen clause names what the boundary contributes — "the side each
    # mark lies on" — so it is scored on the two side-reading whole properties
    # and on the mark profiles, and not on the whole declared property list:
    # the index, label, and tag properties are outside the clause and are
    # reported separately.  Scored the other way this clause would report a
    # miss the frozen text does not make.
    side_clause = all(
        SIDE_PROPERTIES[0] not in rd["base"]["separating_whole_properties"]
        and SIDE_PROPERTIES[1] not in rd["base"]["separating_whole_properties"]
        and all(len(profile) == 1 for profile in rd["base"]["mark_profiles"])
        for rd in (u, o)
    )
    same_as_before_clause = o_clause
    matching_clause = not (
        u_base["collateral_facts"]["cross_boundary_matching_internally_available"]
        or o_base["collateral_facts"]["cross_boundary_matching_internally_available"]
    )
    core = reader_clause and placement_clause and counts_clause and u_clause
    status = (
        "HIT"
        if (core and o_clause and side_clause and same_as_before_clause and matching_clause)
        else "PARTIAL"
        if core
        else "MISSED"
    )
    return {
        "status": status,
        "label": "NOT FORCED",
        "reader_widening_clause_status": verdict(reader_clause),
        "placement_clause_status": verdict(placement_clause),
        "equal_counts_and_side_exchange_clause_status": verdict(counts_clause),
        "U_fails_at_minimum_one_clause_status": verdict(u_clause),
        "O_holds_with_no_new_declaration_clause_status": verdict(o_clause),
        "boundary_contributes_the_side_clause_status": verdict(side_clause),
        "boundary_contributes_exactly_what_it_did_clause_status": verdict(
            same_as_before_clause
        ),
        "matching_stays_unavailable_clause_status": verdict(matching_clause),
        "O_clause_fact": (
            "the frozen clause reads 'the requirement will therefore fail again "
            "under U, with the same minimum count of one, and hold again under "
            "O with no new declaration', and its falsifier names 'the O "
            "requirement needing a new declaration'.  Under O the requirement "
            "FAILS: the exchange of the two wholes is a permitted automorphism "
            "of the retained configuration that uses no side exchange, so the "
            "withdrawal reading O carries does not touch it.  The falsifier "
            "fired, and with it the clause that the boundary contributes here "
            "exactly what it contributed at Challenge 3, where that "
            "contribution met the requirement under O"
        ),
        "evidence": (
            "the Challenge 1 reader refuses both inscriptions and the widening "
            "is paid by the run; the retained placement is (0, 1, 0, 1) with "
            "two marks on each side and a side-exchanging automorphism under "
            "U; the requirement fails under U at a minimum capability count of "
            "one; it fails under O as well; neither side-reading whole "
            "property separates the two wholes; and the cross-boundary "
            "matching is internally unavailable at the retained configuration "
            "under both readings"
        ),
    }


def score(u: Json, o: Json, reader: Json, observation_kinds: list[str]) -> Json:
    """Mechanical scoring of the frozen Challenge 4 predictions and of C3-X."""
    both = (u, o)
    u_base = u["base"]
    o_base = o["base"]
    u_steps = u["one_step_detail"]
    o_steps = o["one_step_detail"]

    def verdict(hit: bool) -> str:
        return "HIT" if hit else "MISSED"

    c4_1 = (
        bool(reader["challenge_1_reader_refuses_both"])
        and all("beyond the Challenge 1 bound" in str(row["refusal"]) for row in reader["challenge_1_reader"])
        and reader["paid_by"] == "the run"
        and all(
            [e["kind"] for e in rd["base"]["history"]]
            == ["Supply", "Supply", "AdmitOccurrence", "AdmitOccurrence"] * 2
            and rd["base"]["placement"] == [0, 1, 0, 1]
            and rd["base"]["labels"] == ["a", "b", "b", "a"]
            and rd["base"]["marks"] == 4
            and rd["base"]["certified"]
            and rd["base"]["replays_from_genesis"]
            and rd["base"]["placement_matches_the_declarations"]
            and not rd["base"]["collateral_facts"][
                "within_whole_order_internally_available"
            ]
            for rd in both
        )
    )
    c4_2 = (
        not u_base["satisfies"]
        and not o_base["satisfies"]
        and o_base["whole_exchange_witness"] is not None
        and not o_base["whole_exchange_witness"]["reflected"]
        and u_base["whole_exchange_witness"] is not None
        and len(o_base["separable_mark_pairs"]) == 4
        and all(
            o_base["placement"][i] != o_base["placement"][j]
            for i, j in o_base["separable_mark_pairs"]
        )
        and u_base["separable_mark_pairs"] == []
        and o_base["mark_pair_count"] == 6
    )
    keep_labels_u = named(u_steps, "keep_labels")
    keep_labels_o = named(o_steps, "keep_labels")
    # The frozen C4-3 clause names "both declared side-reading whole
    # properties", which are the two of definition 34 read of a set, and not
    # the whole declared list; it is scored on those two.
    c4_3_sides_separate_nothing = all(
        SIDE_PROPERTIES[0] not in rd["base"]["separating_whole_properties"]
        and SIDE_PROPERTIES[1] not in rd["base"]["separating_whole_properties"]
        for rd in both
    )
    c4_3_sides_invariant = all(
        SIDE_PROPERTIES[0] in rd["base"]["invariant_whole_properties"]
        and SIDE_PROPERTIES[1] in rd["base"]["invariant_whole_properties"]
        for rd in both
    )
    c4_3_matching = not (
        u_base["collateral_facts"]["cross_boundary_matching_internally_available"]
        or o_base["collateral_facts"]["cross_boundary_matching_internally_available"]
    )
    c4_3_labels = keep_labels_o["satisfies"] and not keep_labels_u["satisfies"]
    c4_3 = (
        c4_3_sides_separate_nothing
        and c4_3_sides_invariant
        and c4_3_matching
        and c4_3_labels
    )
    c4_4 = all(
        rd["space_size"] == 192
        and rd["one_step_iff_capability_count_one"]
        and rd["name_wholes_collapses_into_the_base"]
        and all(row["bundles"] == (row["mu1"] >= 2) for row in rd["points"])
        for rd in both
    ) and list(COORDINATES) == [
        "withdraw_reflection",
        "withdraw_mark_permutations",
        "admit_names",
        "keep_labels",
        "admit_grouping",
        "name_wholes",
        "extra_mark",
    ]
    c4_5 = (
        u["satisfying_one_step_points"] == ["withdraw_mark_permutations"]
        and u["minima_by_mu1"]["minimum"] == 1
        and u["minima_by_mu1"]["class_count"] == 1
        and u["minima_by_mu1"]["unique"]
        and named(u_steps, "withdraw_mark_permutations")[
            "no_permitted_renaming_moves_an_index"
        ]
        and not named(u_steps, "withdraw_reflection")["satisfies"]
        and not named(u_steps, "extra_mark_0")["satisfies"]
        and not named(u_steps, "extra_mark_1")["satisfies"]
    )
    c4_6 = (
        sorted(o["satisfying_one_step_points"])
        == ["keep_labels", "withdraw_mark_permutations"]
        and o["minima_by_mu1"]["minimum"] == 1
        and o["minima_by_mu1"]["class_count"] == 2
        and not o["minima_by_mu1"]["unique"]
    )
    c4_7 = all(
        not named(rd["one_step_detail"], "admit_grouping")["satisfies"]
        and not named(rd["one_step_detail"], "name_wholes")["satisfies"]
        and rd["name_wholes_collapses_into_the_base"]
        and rd["grouping_bundle"]["mu1"] == 2
        and rd["grouping_bundle"]["bundles"]
        and not rd["grouping_bundle"]["one_step"]
        and rd["grouping_bundle"]["satisfies"]
        and [cell["requirement_met"] for cell in rd["grouping_square"]]
        == [False, False, False, True]
        for rd in both
    )
    c4_8 = all(
        rd["pointwise_implies_whole_at_every_point"]
        and rd["reduction_to_challenge_3"]["senses_agree"]
        and rd["at_every_parting_point_the_wholes_separate_and_the_marks_do_not"]
        for rd in both
    ) and u["points_where_the_two_senses_part"] != [] and point_name(
        GROUPING_BUNDLE
    ) in u["points_where_the_two_senses_part"]
    return {
        "C3-X": score_c3x(u, o, reader),
        "C4-1": {
            "status": verdict(c4_1),
            "label": "FORCED",
            "result_basis": (
                "DEFINITION-level: the Challenge 1 refusal is that rung's "
                "declared bound replayed on the caller's text, and the "
                "retained configuration follows from the widened reader, the "
                "declared convention, the declared within-whole order, and the "
                "Challenge 2 identity policy, all of them declarations; a hit "
                "is by construction and is not counted as content.  The one "
                "clause that is not a declaration, that the other within-whole "
                "order gives an isomorphic configuration, is an "
                "isomorphism-witness search and is reported separately"
            ),
            "evidence": (
                "the Challenge 1 reader refuses both inscriptions by name; the "
                "caller's history is a supply and an occurrence admission for "
                "each of four marks; the current configuration under each "
                "reading is placement (0, 1, 0, 1) with labels a, b, b, a, "
                "certified, replayed from genesis, and matching the placement "
                "the declarations predict; and the other within-whole order "
                "gives an isomorphic configuration"
            ),
        },
        "C4-2": {
            "status": verdict(c4_2),
            "label": "FORCED",
            "result_basis": (
                "content: whether an automorphism carries one whole's mark-set "
                "onto the other's is a search over the unpruned enumeration at "
                "the reading's own renamings, and both values are attained "
                "elsewhere in the space; the pair census is a search per pair"
            ),
            "evidence": (
                "the requirement fails under BOTH readings; the witness under O "
                "uses no side exchange, so the withdrawal reading O carries "
                "does not touch it; of the six pairs of marks exactly the four "
                "lying on different sides are separable under O and none is "
                "separable under U"
            ),
        },
        "C4-3": {
            "status": (
                "HIT"
                if c4_3
                else "PARTIAL"
                if (c4_3_sides_separate_nothing and c4_3_matching and c4_3_labels)
                else "MISSED"
            ),
            "label": "NOT FORCED",
            "side_properties_separate_neither_whole_status": verdict(
                c4_3_sides_separate_nothing
            ),
            "side_properties_invariant_under_both_readings_status": verdict(
                c4_3_sides_invariant
            ),
            "cross_boundary_matching_unavailable_status": verdict(c4_3_matching),
            "label_keeping_parts_the_readings_status": verdict(c4_3_labels),
            "side_properties_invariant_by_reading": {
                "U": SIDE_PROPERTIES[0] in u_base["invariant_whole_properties"],
                "O": SIDE_PROPERTIES[0] in o_base["invariant_whole_properties"],
            },
            "result_basis": (
                "content: the invariance of each declared whole property is a "
                "census over the declared domain under the candidate's own "
                "renamings, and the cross-boundary matching is an "
                "isomorphism-witness search"
            ),
            "evidence": (
                "neither side-reading whole property separates the two wholes "
                "under either reading; the configuration in which the second "
                "whole's copy of the first token is a token the caller never "
                "presented is isomorphic to the retained one under both "
                "readings; and keeping the presentation labels meets the "
                "requirement under O and does not meet it under U"
            ),
        },
        "C4-4": {
            "status": verdict(c4_4),
            "label": "NOT FORCED",
            "result_basis": (
                "DEFINITION-level: the coordinates, their values, the "
                "capability named for each, and therefore the point count and "
                "the identity of one-step with capability count one are "
                "declarations of this rung; a hit is by construction and is "
                "not counted as content"
            ),
            "evidence": (
                "seven coordinates and 192 points under each reading; a point "
                "is one step exactly when its capability count is one; every "
                "point of count two or more is refused as bundling; and naming "
                "the wholes without admitting the grouping collapses into the "
                "base under the implemented quotient"
            ),
        },
        "C4-5": {
            "status": verdict(c4_5),
            "label": "FORCED",
            "result_basis": (
                "content: which one-step points meet the requirement is a "
                "search at each candidate's own renamings, and the class count "
                "is the implemented quotient.  That the one minimum meets the "
                "requirement by unfolding is DEFINITION-level and the receipt "
                "reports it separately"
            ),
            "evidence": (
                "under U exactly one one-step point meets the requirement, the "
                "withdrawal of the mark permutations, at a minimum capability "
                "count of one and in one class, so uniqueness is not refuted "
                "inside the declared space; the withdrawal of the side "
                "exchange and both further-mark points do not meet it"
            ),
        },
        "C4-6": {
            "status": verdict(c4_6),
            "label": "FORCED",
            "result_basis": (
                "content: the same search and the same quotient, under the "
                "other reading"
            ),
            "evidence": (
                "under O exactly two one-step points meet the requirement, the "
                "withdrawal of the mark permutations and the keeping of the "
                "presentation labels, in two classes tied at capability count "
                "one, so uniqueness is refuted under O"
            ),
        },
        "C4-7": {
            "status": verdict(c4_7),
            "label": "FORCED",
            "result_basis": (
                "content: each cell of the grouping square is an automorphism "
                "search with both values attained, and the collapse of the "
                "name-wholes point is the implemented quotient"
            ),
            "evidence": (
                "the grouping alone does not meet the requirement, the names "
                "alone are a no-op that collapses into the base, and the two "
                "together meet it under both readings at a capability count of "
                "two, so the augmentation that gives the caller internal "
                "wholes is refused as a bundle"
            ),
        },
        "C4-8": {
            "status": verdict(c4_8),
            "label": "FORCED",
            "result_basis": (
                "content: the pointwise sense is a search per pair, the whole "
                "sense a search per whole, and their comparison a census over "
                "the 192 points; the reduction is computed at the Challenge 3 "
                "configuration and not asserted"
            ),
            "evidence": (
                "the pointwise sense implies the whole sense at every point of "
                "the space under both readings; the converse fails at the "
                "points under U where the grouping is admitted and the wholes "
                "are named; and at the Challenge 3 configuration, where each "
                "whole is one mark, the two senses agree under both readings"
            ),
        },
        "C4-X": {
            "status": "PENDING",
            "label": "NOT FORCED",
            "evidence": "scored by Challenge 5",
        },
    }


def tally(scores: Json) -> Json:
    """Count the scored Challenge 4 predictions by status and by basis."""
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
    """The Challenge 0 census, run over the Challenge 4 modules."""
    return {
        "model": state_event_generators(model, EVENT_TYPES),
        "presentation": state_event_generators(presentation, EVENT_TYPES),
        "challenge3": state_event_generators(sys.modules["boundary.challenge3"], EVENT_TYPES),
        "challenge4": state_event_generators(sys.modules[__name__], EVENT_TYPES),
    }


def build() -> Json:
    u = reading_facts(READING_U)
    o = reading_facts(READING_O)
    reader = reader_facts()
    observation_kinds = observation_vocabulary()
    scores = score(u, o, reader, observation_kinds)
    return {
        "challenge": 4,
        "inscriptions": list(INSCRIPTIONS),
        "seed_sha256": SEED_SHA256,
        "predictions_sha256": PREDICTIONS_SHA256,
        "challenge0_predictions_sha256": C0_PREDICTIONS_SHA256,
        "challenge1_predictions_sha256": C1_PREDICTIONS_SHA256,
        "challenge2_predictions_sha256": C2_PREDICTIONS_SHA256,
        "challenge3_predictions_sha256": C3_PREDICTIONS_SHA256,
        "reader": reader,
        "identity_policy_inherited": DECLARED_POLICY,
        "requirement": {
            "declared": REQUIREMENT,
            "second_reading": REQUIREMENT_SECOND_READING,
            "pointwise_sense": REQUIREMENT_POINTWISE_SENSE,
            "readings_agree_because": REQUIREMENT_READINGS_AGREE_BECAUSE,
            "grouping_is_metatheory": GROUPING_IS_METATHEORY,
            "retained_wholes": list(RETAINED_WHOLES),
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
        "whole_properties": [
            {"name": name, "reads": WHOLE_PROPERTY_READS[name]}
            for name, _prop in DECLARED_WHOLE_PROPERTIES
        ],
        "collateral_facts": list(COLLATERAL_FACTS),
        "property_domain_groupings": [list(g) for g in DOMAIN_GROUPINGS],
        "property_domain_size": len(property_domain(READING_U)),
        "readings": {READING_U: u, READING_O: o},
        "event_kinds": [t.__name__ for t in EVENT_TYPES],
        "new_event_kinds_at_challenge_4": [],
        "state_event_generators": state_event_generators(model, EVENT_TYPES),
        "event_returning_functions_by_module": event_returning_functions_by_module(),
        "observation_vocabulary": observation_kinds,
        "what_the_challenge_exercises": {
            "supply": (
                "yes: one Supply per mark of each presented whole, four in "
                "all, in presented order; the further-mark candidate needs no "
                "new one"
            ),
            "mention": (
                "yes: each visible mark is named by two events of the caller's "
                "history, once in each whole, and is not an identity"
            ),
            "admission": (
                "yes: the caller retains, so the caller's history contains one "
                "occurrence admission per mark; the further-mark candidate "
                "would be the first event the process rather than the caller "
                "issues, and it is a candidate and is admitted by no history "
                "the receipt reports as current"
            ),
            "current-state designation": (
                "yes: the current state under each reading is the replay of "
                "the caller's Challenge 4 history; every candidate "
                "configuration is the replay of an explicit history and only "
                "the base is current"
            ),
            "retention": (
                "yes: the placement tuple carries all four marks, and the "
                "grouping the caller's history fixes is metatheory beside it"
            ),
            "observation": (
                "yes: four mark-on-side judgments, and under a candidate the "
                "side-name form; no new form is needed and none is added to "
                "the closed grammar"
            ),
            "side": (
                "yes, and it is the rung's subject: each side now carries one "
                "mark of each whole, which is why the boundary alone no longer "
                "meets the requirement under either reading"
            ),
            "equality": (
                "yes: structural regime equality, the isomorphism relation at "
                "the reading's renamings, and the isomorphism relation at a "
                "candidate's renamings over configurations rather than "
                "regimes are three different relations, and the rung uses all "
                "three"
            ),
        },
        "boundary_dependence": BOUNDARY_DEPENDENCE,
        "scores": scores,
        "tally": tally(scores),
        "authority_effect": "None",
    }
