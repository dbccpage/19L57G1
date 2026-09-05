"""Continuation stage 1: the branches, their challenge generators, and the
declared resource bounds.

The mandatory challenge sequence is closed at Challenge 5.  The seed's
autonomous continuation asks, for each surviving branch under each reading,
for the weakest deterministic finite procedure the run can justify for
generating the next challenge from that branch alone, with a proof that it
imports no undeclared object-language structure, and for the resource bounds
under which the rounds are then run.  **This stage declares those and runs no
round.**  Nothing here is admitted: no candidate is adopted, no event is
issued, and every configuration reported is the replay of an explicit recorded
history.

The stage has four parts, in this order:

1. **The declared branch set.**  A branch is a certified line of the run: the
   declarations in force on it, the caller history it replays, and the
   configuration that replay produces.  The base branch adopts nothing; every
   other declared branch adopts exactly one retained tied-minimum class of one
   closed rung.  The minima are recomputed from the closed rungs' own modules
   rather than restated here, and a test holds the recomputation to their
   committed receipts.
2. **The branch quotient.**  Two branches are the same branch exactly when
   their keys are equal, and the key carries the declarations in force — the
   Challenge 5 class key of an adopted policy among them — beside the least key
   of the configuration under the branch's own permitted renamings.  The
   configuration alone is not enough: the two Challenge 5 policy branches
   retain configurations with the same least key, so a key read at the
   configuration would report one branch where the declarations give two.
3. **The generator space.**  What the run may do to a branch from that branch
   alone is decided by nothing the run has declared, so this stage declares a
   finite space of generators over three coordinates and prices each in
   capabilities.  A generator is one step exactly when its capability count is
   one; two or more bundles and is refused, so a generator that both supplies
   and retains is refused.  Among the generators that emit a challenge at all
   the minimum is one, and where the minimum is attained twice the tie is
   computed and not declared.
4. **The bounds.**  The node ceiling is a declaration; the branching bound is
   read off the three closed rungs' own minima; the round bound is computed
   from them and comes in short of the seed's fifteen, so an exact frontier
   under a declared bound is owed and fifteen rounds are not attempted.

**One step is capability count one, and here as at Challenge 5 that is not the
coordinate count**: the state-reading source moves one coordinate and uses two
capabilities.  The run keeps the capability reading, because the seed requires
a candidate called one step not to bundle capabilities.

The declared spaces are exhaustive over their own coordinates and over nothing
wider.  Every minimality statement below is scoped to them.
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from functools import cache
from itertools import combinations
from typing import Sequence

from boundary import challenge0, challenge1, challenge2, challenge3, challenge4
from boundary import challenge5, model, presentation
from boundary.challenge0 import observation_vocabulary, state_event_generators
from boundary.challenge1 import Json, key_json
from boundary.challenge3 import one_step_minima
from boundary.challenge4 import Augmentation
from boundary.challenge5 import Point, Retention
from boundary.model import (
    READING_O,
    READING_U,
    READINGS,
    Configuration,
    Renamings,
    certify,
    configuration_automorphisms,
    configuration_key,
    deep_certify,
    deep_event_follows,
    deep_genesis,
    event_follows,
    genesis,
    permitted_configuration_images,
    wholes_separable_in,
)
from boundary.presentation import NestedWhole, read_nested_whole

SEED_SHA256 = challenge0.SEED_SHA256
C0_PREDICTIONS_SHA256 = challenge0.PREDICTIONS_SHA256
C1_PREDICTIONS_SHA256 = challenge1.PREDICTIONS_SHA256
C2_PREDICTIONS_SHA256 = challenge2.PREDICTIONS_SHA256
C3_PREDICTIONS_SHA256 = challenge3.PREDICTIONS_SHA256
C4_PREDICTIONS_SHA256 = challenge4.PREDICTIONS_SHA256
C5_PREDICTIONS_SHA256 = challenge5.PREDICTIONS_SHA256
PREDICTIONS_SHA256 = "ac401dafbfa5072f04b6ab532992eae41391f87b6fe4441592b86804c4bf8313"

STAGE = 1
EVENT_TYPES: tuple[type, ...] = challenge5.EVENT_TYPES

INITIAL_INSCRIPTION = "<|>"
"""The initial object-language inscription, presented by the seed at genesis.

It carries no supply event: definition 1 makes it the one supplied opaque
datum of the regime, present before any event.  It is nevertheless a text the
object language has been presented, so the presented record below carries it,
and the record is what the enumeration generator reads.  Leaving it out would
make the least unpresented member of the declared domain the initial
inscription itself, which is a declaration this stage declines to make.
"""

PRESENTED_TEXTS: tuple[str, ...] = (
    INITIAL_INSCRIPTION,
    challenge1.INSCRIPTION,
    challenge2.INSCRIPTIONS[1],
    challenge4.INSCRIPTIONS[0],
    challenge4.INSCRIPTIONS[1],
    challenge5.INSCRIPTION,
)
"""The record of the texts the caller has presented, in presentation order.

Read off the closed rungs' own declared inscriptions rather than restated:
Challenge 2 retains the Challenge 1 whole and one further whole, so only the
further one is new there.  Metatheory of the history, exactly as ``supplied``
is (definition 20), and no regime carries it.
"""

WITHIN_WHOLE_ORDER = presentation.DECLARED_WITHIN_WHOLE_ORDER
CONVENTION = presentation.DECLARED_CONVENTION


# ---------------------------------------------------------------------------
# The closed rungs' retained minima
# ---------------------------------------------------------------------------


CLOSED_RUNGS: tuple[int, int, int] = (3, 4, 5)
RUNG_PREDICATE: dict[int, str] = {3: "satisfies", 4: "satisfies", 5: "admits"}


def _challenge3_rows(reading: str) -> list[Json]:
    wholes = [presentation.read_whole(text) for text in challenge2.INSCRIPTIONS]
    base_facts = challenge3.collateral_facts(
        reading, challenge3.NULL_AUGMENTATION, wholes
    )
    return [
        challenge3.point_row(reading, aug, wholes, base_facts)
        for aug in challenge3.candidate_space()
        if challenge3.is_one_step(aug) or challenge3.mu1(aug) == 0
    ]


def _challenge4_rows(reading: str) -> list[Json]:
    wholes = challenge4.caller_wholes()
    base_facts = challenge4.analyse(
        reading, challenge4.NULL_AUGMENTATION, wholes
    ).facts
    return [
        challenge4.point_row(challenge4.analyse(reading, aug, wholes), base_facts)
        for aug in challenge4.candidate_space()
        if challenge4.is_one_step(aug) or challenge4.mu1(aug) == 0
    ]


def _challenge5_rows(reading: str) -> list[Json]:
    base_facts = challenge5.collateral_facts(
        reading,
        challenge5.BASE_POINT,
        challenge5.retain(
            reading,
            read_nested_whole(challenge5.INSCRIPTION),
            challenge5.POLICY_REFUSE,
            challenge5.INSCRIPTION,
        ),
    )
    return [
        challenge5.point_row(reading, point, base_facts)
        for point in challenge5.point_space()
    ]


@cache
def rung_minima(rung: int, reading: str) -> str:
    """The closed rung's retained tied-minimum classes, recomputed.

    Only the one-step points and the null point are computed, which is exactly
    what ``one_step_minima`` keeps, so the answer is the rung's own and the
    whole-space census it does not need is not paid for.  Returned as JSON text
    so that the cache holds an immutable value.
    """
    rows = {
        3: _challenge3_rows,
        4: _challenge4_rows,
        5: _challenge5_rows,
    }[rung](reading)
    return json.dumps(one_step_minima(rows, "mu1", RUNG_PREDICATE[rung]), sort_keys=True)


def rung_classes(rung: int, reading: str) -> list[list[str]]:
    """The member names of each retained minimum class, in the rung's order."""
    minima: Json = json.loads(rung_minima(rung, reading))
    return [[str(name) for name in entry["members"]] for entry in minima["classes"]]


def rung_minimum(rung: int, reading: str) -> int | None:
    """The rung's own minimum capability count, or nothing where none exists."""
    minima: Json = json.loads(rung_minima(rung, reading))
    value = minima["minimum"]
    return None if value is None else int(value)


# ---------------------------------------------------------------------------
# Branches
# ---------------------------------------------------------------------------


BASE_NAME = "base"
ONE_ADOPTION_RULE = (
    "the base branch adopts nothing and every other declared branch adopts "
    "exactly one retained tied-minimum class of one closed rung.  A branch "
    "adopting two or more is NOT enumerated: each rung's minimum answers that "
    "rung's own requirement and no requirement of the run justifies a second "
    "adoption, so the product of the rungs' classes is a wider space about "
    "which this stage claims nothing"
)


@dataclass(frozen=True)
class Branch:
    """One declared branch: what it adopts, and the declarations in force.

    A deterministic value object.  It applies nothing: a branch becomes a
    configuration only through replay of an explicit recorded history, and a
    renaming set only by being handed to the kernel's declared enumerations.
    """

    name: str
    rung: int | None
    aug: Augmentation
    policy: str | None

    def adopts_nothing(self) -> bool:
        return self.rung is None

    def label(self) -> str:
        return self.name if self.rung is None else f"{self.name}@{self.rung}"


BASE_BRANCH = Branch(BASE_NAME, None, Augmentation(), None)


def augmentation_named(rung: int, name: str) -> Augmentation:
    """The Challenge 4 shaped augmentation a closed rung's point name denotes.

    Challenge 3's space is Challenge 4's without the two grouping coordinates,
    so a Challenge 3 point is carried across by its five shared coordinates.
    An unknown name is refused by name rather than resolved to the base.
    """
    if rung == 3:
        for aug in challenge3.candidate_space():
            if challenge3.point_name(aug) == name:
                return Augmentation(
                    withdraw_reflection=aug.withdraw_reflection,
                    withdraw_mark_permutations=aug.withdraw_mark_permutations,
                    admit_names=aug.admit_names,
                    keep_labels=aug.keep_labels,
                    extra_mark=aug.extra_mark,
                )
        raise KeyError(f"no Challenge 3 point is named {name!r}")
    for candidate in challenge4.candidate_space():
        if challenge4.point_name(candidate) == name:
            return candidate
    raise KeyError(f"no Challenge 4 point is named {name!r}")


def policy_named(name: str) -> str:
    """The Challenge 5 policy a point name denotes; an unknown one is refused."""
    for point in challenge5.point_space():
        if challenge5.point_name(point) == name:
            return point.policy
    raise KeyError(f"no Challenge 5 point is named {name!r}")


def branch_candidates(reading: str) -> list[Branch]:
    """The base branch and one candidate branch per retained minimum class.

    Before the quotient: two rungs may name the same declaration, and one class
    may carry two points.  A class is represented by its first member in the
    rung's own order.
    """
    out = [BASE_BRANCH]
    for rung in CLOSED_RUNGS:
        for members in rung_classes(rung, reading):
            name = members[0]
            if rung == 5:
                out.append(Branch(name, rung, Augmentation(), policy_named(name)))
            else:
                out.append(Branch(name, rung, augmentation_named(rung, name), None))
    return out


def branch_renamings(reading: str, branch: Branch) -> Renamings:
    """The five flags the kernel's declared enumerations take on this branch.

    A branch that adopts a Challenge 5 policy adopts no Challenge 3 or
    Challenge 4 coordinate, so its renamings are the reading's own.
    """
    return challenge4.renamings(reading, branch.aug)


def branch_retention(reading: str, branch: Branch) -> Retention:
    """What the Challenge 5 caller history retains under the branch's policy."""
    if branch.policy is None:
        raise ValueError(f"branch {branch.name!r} adopts no policy")
    return challenge5.retain(
        reading,
        read_nested_whole(challenge5.INSCRIPTION),
        branch.policy,
        challenge5.INSCRIPTION,
    )


def inherited_history(branch: Branch) -> list[model.Event]:
    """The Challenge 4 caller history, extended where a branch adopts the
    process's own further admission."""
    return challenge4.candidate_history(
        challenge4.caller_wholes(), branch.aug, CONVENTION, WITHIN_WHOLE_ORDER
    )


def branch_history(reading: str, branch: Branch) -> Json:
    """The recorded history the branch replays, rendered.

    A branch that adopts a policy replays the Challenge 5 caller history under
    it, in the deep grammar; every other branch replays the Challenge 4 caller
    history.  Which of the two is current is definition 25 read per challenge,
    as the closed rungs read it: nothing was retained at Challenge 5 unless a
    policy is taken, so the Challenge 4 retention stands where none is.
    """
    if branch.policy is None:
        events = inherited_history(branch)
        return {
            "grammar": "inherited",
            "events": challenge2.history_json(events),
            "length": len(events),
        }
    deep_events = branch_retention(reading, branch).history or []
    return {
        "grammar": "deep",
        "events": challenge5.deep_history_json(deep_events),
        "length": len(deep_events),
    }


def configuration_of_retention(reading: str, retention: Retention) -> Configuration:
    """The configuration a Challenge 5 retention flattens to.

    Every address a one-step policy holds has length one, so the flattened
    regime is the state type Challenges 0 to 4 use; the grouping is the one
    whole the caller presented at that rung.  A retention that admits nothing
    gives the genesis configuration, which is what a refusing policy would
    leave and is reported rather than treated as an error.
    """
    if retention.regime is None:
        return Configuration(genesis(reading), ())
    return Configuration(
        retention.regime, tuple(0 for _ in range(retention.regime.n_marks()))
    )


def branch_configuration(reading: str, branch: Branch) -> Configuration:
    """The configuration the branch's recorded history produces."""
    if branch.policy is None:
        return challenge4.configuration_of(
            reading,
            challenge4.caller_wholes(),
            branch.aug,
            CONVENTION,
            WITHIN_WHOLE_ORDER,
        )
    return configuration_of_retention(reading, branch_retention(reading, branch))


def retention_certified(reading: str, retention: Retention) -> bool:
    """Whether a retention's deep state is the replay of its own history."""
    if retention.deep is None:
        return False
    return deep_certify(retention.history or [], deep_genesis(reading), retention.deep)


def branch_certified(reading: str, branch: Branch) -> bool:
    """Whether the branch's configuration is the replay of its own history."""
    if branch.policy is None:
        return certify(
            inherited_history(branch),
            genesis(reading),
            branch_configuration(reading, branch).regime,
        )
    return retention_certified(reading, branch_retention(reading, branch))


def branch_policy_key(reading: str, branch: Branch) -> list[object]:
    """The Challenge 5 class key of an adopted policy, or the declared sentinel.

    A policy's identity is settled by Challenge 5's own quotient over its
    144-member domain, not by what it retains from one inscription.  That is
    what keeps the two policy branches apart below.
    """
    if branch.policy is None:
        return ["no policy taken"]
    point = Point(branch.policy)
    digest = challenge5.behaviour_digest(challenge5.domain_behaviour(reading, point))
    return challenge5.class_key(reading, point, digest)


def branch_least_key(reading: str, branch: Branch) -> list[object]:
    """The least key of the branch's configuration under its own renamings."""
    configuration = branch_configuration(reading, branch)
    rn = branch_renamings(reading, branch)
    return min(
        key_json(configuration_key(image, rn))
        for _reflected, _pi, _sigma, image in permitted_configuration_images(
            configuration, rn
        )
    )


def branch_key(reading: str, branch: Branch) -> list[object]:
    """The implemented quotient of branches: the declarations in force, the
    adopted policy's own class key, and the least configuration key.

    This is the only sanctioned quotient of branches.
    """
    structure = challenge4.effective_structure(reading, branch.aug)
    return [
        *[str(part) for part in structure],
        [str(part) for part in branch_policy_key(reading, branch)],
        branch_least_key(reading, branch),
    ]


def branch_key_without_the_policy(reading: str, branch: Branch) -> list[object]:
    """The same key with the policy part dropped.

    Not a quotient the stage uses: it is computed only to report how many
    branches a key read at the configuration alone would lose.
    """
    structure = challenge4.effective_structure(reading, branch.aug)
    return [*[str(part) for part in structure], branch_least_key(reading, branch)]


def _classes(keyed: Sequence[tuple[Branch, list[object]]]) -> list[list[str]]:
    grouped: dict[str, list[str]] = {}
    for branch, key in keyed:
        grouped.setdefault(repr(key), []).append(branch.label())
    return [members for _key, members in sorted(grouped.items())]


def branch_classes(reading: str) -> list[list[str]]:
    """The branch candidates grouped by the implemented branch key."""
    return _classes(
        [(branch, branch_key(reading, branch)) for branch in branch_candidates(reading)]
    )


def branch_classes_without_the_policy(reading: str) -> list[list[str]]:
    """The same grouping with the policy part of the key dropped."""
    return _classes(
        [
            (branch, branch_key_without_the_policy(reading, branch))
            for branch in branch_candidates(reading)
        ]
    )


def declared_branches(reading: str) -> list[Branch]:
    """One branch per class, represented by its first candidate."""
    seen: dict[str, Branch] = {}
    for branch in branch_candidates(reading):
        seen.setdefault(repr(branch_key(reading, branch)), branch)
    return list(seen.values())


# ---------------------------------------------------------------------------
# The requirements a branch carries
# ---------------------------------------------------------------------------


IMPOSED_DEMANDS: tuple[tuple[int, int], ...] = ((0, 1),)
"""The demands the caller has already imposed, as pairs of group tags.

Challenge 3 required the two retained wholes of its configuration to be
internally separable, and Challenge 4 required the same of the two wholes of
the configuration current there.  Both name the pair ``(0, 1)`` of the
configuration current at their rung, and the Challenge 3 configuration is not
the current one: its wholes left the configuration when the Challenge 4
retention replaced it, which is one of the fates the seed lists for an
unresolved requirement.
"""

REQUIREMENT_SENSE = (
    "two retained wholes of a branch meet the requirement under a reading when "
    "no permitted automorphism of the configuration carries the mark-set of "
    "one onto the mark-set of the other (definition 52), read at the branch's "
    "own renamings"
)


def branch_tags(reading: str, branch: Branch) -> list[int]:
    """The group tags the branch's configuration carries, in order."""
    return sorted(set(branch_configuration(reading, branch).groups))


def branch_pairs(reading: str, branch: Branch) -> list[tuple[int, int]]:
    """Every unordered pair of distinct retained wholes of the branch."""
    return list(combinations(branch_tags(reading, branch), 2))


def remaining_demands(reading: str, branch: Branch) -> list[tuple[int, int]]:
    """The pairs the run has not already been required to separate."""
    return [
        pair for pair in branch_pairs(reading, branch) if pair not in IMPOSED_DEMANDS
    ]


def demand_met(reading: str, branch: Branch, pair: tuple[int, int]) -> bool:
    """Whether the branch already meets a demand at its own renamings."""
    return wholes_separable_in(
        branch_configuration(reading, branch),
        pair[0],
        pair[1],
        branch_renamings(reading, branch),
    )


def live_requirement(reading: str, branch: Branch) -> Json:
    """The Challenge 4 requirement at the branch, or its disappearance.

    A requirement about two retained wholes cannot be carried by a
    configuration that holds fewer than two, so on a policy branch it does not
    persist, split, or create a new one: it disappears with the configuration
    the caller's retention replaced.
    """
    if IMPOSED_DEMANDS[0] not in branch_pairs(reading, branch):
        return {
            "carried": False,
            "met": None,
            "because": (
                "the branch's configuration holds fewer than two retained "
                "wholes, so the pair the caller demanded is not a pair of it "
                "and the requirement disappears with the configuration"
            ),
        }
    met = demand_met(reading, branch, IMPOSED_DEMANDS[0])
    return {
        "carried": True,
        "met": met,
        "because": (
            "no permitted automorphism of the configuration carries the first "
            "whole's mark-set onto the second's"
            if met
            else "a permitted automorphism of the configuration carries the "
            "first whole's mark-set onto the second's, so the requirement is "
            "unresolved on this branch"
        ),
    }


# ---------------------------------------------------------------------------
# The presented record, and the declared domain
# ---------------------------------------------------------------------------


def domain_texts() -> list[str]:
    """The Challenge 5 declared domain, in that rung's own order."""
    return challenge5.domain_texts()


def presented_indices() -> list[int]:
    """Where each presented text lies in the declared domain's order."""
    texts = domain_texts()
    return [texts.index(presented) for presented in PRESENTED_TEXTS]


def first_missing(presented: Sequence[int], bound: int) -> int | None:
    """The least index below the bound the record does not carry.

    Separated from its callers so that the direction returning nothing is
    exercised by a test: the record carries six of 144 members, so a search
    written inline could only ever read one way.
    """
    seen = set(presented)
    for index in range(bound):
        if index not in seen:
            return index
    return None


def least_unpresented_index() -> int | None:
    return first_missing(presented_indices(), len(domain_texts()))


def text_at(index: int | None) -> str | None:
    """The declared domain's member at an index, or nothing for no index."""
    return None if index is None else domain_texts()[index]


def least_unpresented() -> str | None:
    return text_at(least_unpresented_index())


def marks_in(whole: NestedWhole) -> int:
    """How many marks a read whole carries, counting at every level."""
    total = 0
    for item in (whole.left, whole.right):
        if isinstance(item, NestedWhole):
            total += marks_in(item)
        elif item is not None:
            total += 1
    return total


def domain_member_with_marks(count: int) -> str | None:
    """The least member of the declared domain carrying exactly that many marks."""
    for text in domain_texts():
        if marks_in(read_nested_whole(text)) == count:
            return text
    return None


# ---------------------------------------------------------------------------
# The declared generator space
# ---------------------------------------------------------------------------


SOURCE_NONE = "none: the generator names no inscription"
SOURCE_ENUMERATION = (
    "enumeration: the least member of the declared domain, in that domain's "
    "own order, that the presented record does not carry"
)
SOURCE_STATE = (
    "state: the least member of the declared domain carrying as many marks as "
    "the branch's configuration admits"
)
SOURCE_SPACE: tuple[str, str, str] = (SOURCE_NONE, SOURCE_ENUMERATION, SOURCE_STATE)
SOURCE_NAMES: dict[str, str] = {
    SOURCE_NONE: "none",
    SOURCE_ENUMERATION: "enumeration",
    SOURCE_STATE: "state",
}
SOURCE_SPACE_IS_EXHAUSTIVE_BECAUSE = (
    "a generator either names no inscription, or names one without reading the "
    "branch's admitted state, or names one by reading it.  Those three exhaust "
    "the declared alternatives.  The stage enumerates ONE source of each of the "
    "last two kinds — the declared domain enumeration, and the least domain "
    "member carrying as many marks as the configuration admits — and not every "
    "source of either kind; what a state-reading source costs is the same for "
    "all of them, because every one of them reads the state, and that is the "
    "only thing this space asks of the third value"
)

CAP_SUPPLY = "the_process_supplies"
CAP_ADMIT = "the_process_admits"
CAP_READ_STATE = "the_process_reads_the_state_into_the_presentation"
CAP_DEMAND = "the_process_imposes_a_requirement"

CAPABILITY_OF: dict[str, str] = {
    CAP_SUPPLY: (
        "the process, and not only the caller, issues a presentation event: "
        "definition 25 makes the current state the replay of the CALLER's "
        "history, and a challenge the process generates is the first "
        "presentation that history does not contain"
    ),
    CAP_ADMIT: (
        "the process, and not only the caller, issues an admission event.  "
        "This is the capability the further-mark candidate of Challenge 3 was "
        "priced at (definition 45), read as its admission half: the event it "
        "names is an admission, and supply and admission are never conflated"
    ),
    CAP_READ_STATE: (
        "the next presentation is computed from the branch's admitted state, "
        "so that what the object language holds decides what it is next shown"
    ),
    CAP_DEMAND: (
        "the process, and not the caller, requires two retained wholes to be "
        "internally separable: at Challenges 3 and 4 the caller imposed the "
        "requirement and the run answered it"
    ),
}

COORDINATES: tuple[str, str, str] = ("source", "retains", "demands")

MU1 = "capability count: the number of undeclared capabilities the generator uses"
NO_SECOND_MEASURE_BECAUSE = (
    "the run's second measure has been the number of declared collateral facts "
    "a candidate makes internally available that its reading's base did not.  A "
    "generator makes no fact available: it changes no admitted state, and this "
    "stage runs no round.  So no second measure is declared here, and the tie "
    "the first measure leaves on one branch is left standing rather than broken "
    "by a measure invented to break it"
)

ONE_STEP_RULE = (
    "a generator is one step exactly when the number of undeclared "
    "capabilities it uses is one, and one of two or more bundles capabilities "
    "and is refused as a one-step augmentation.  As at Challenge 5 that number "
    "is not the number of coordinates moved: the state-reading source moves one "
    "coordinate and uses two capabilities"
)


@dataclass(frozen=True)
class Generator:
    """One declared candidate generator: a value for each coordinate.

    A deterministic value object.  It applies nothing and issues nothing: what
    it emits is reported as a text and a pair of tags, and no event of any
    grammar is built from it anywhere in this module.
    """

    source: str = SOURCE_NONE
    retains: bool = False
    demands: bool = False

    def values(self) -> tuple[object, ...]:
        return (SOURCE_NAMES[self.source], self.retains, self.demands)


NULL_GENERATOR = Generator()
ENUMERATION_GENERATOR = Generator(SOURCE_ENUMERATION)
DEMAND_GENERATOR = Generator(demands=True)
STATE_GENERATOR = Generator(SOURCE_STATE)


def generator_space() -> list[Generator]:
    """Every point of the declared space, in a deterministic order."""
    return [
        Generator(source, retains, demands)
        for source in SOURCE_SPACE
        for retains in (False, True)
        for demands in (False, True)
    ]


def changed_coordinates(g: Generator) -> list[str]:
    """The coordinates the generator moves off their inherited values."""
    moved: list[str] = []
    if g.source != SOURCE_NONE:
        moved.append("source")
    if g.retains:
        moved.append("retains")
    if g.demands:
        moved.append("demands")
    return moved


def capabilities(g: Generator) -> list[str]:
    """The undeclared capabilities the generator uses.

    A coordinate that changes nothing still costs its capability, as the naming
    coordinate did at Challenge 5: retaining what no source named retains
    nothing, and it collapses under the quotient rather than under the price.
    """
    used: list[str] = []
    if g.source != SOURCE_NONE:
        used.append(CAP_SUPPLY)
    if g.source == SOURCE_STATE:
        used.append(CAP_READ_STATE)
    if g.retains:
        used.append(CAP_ADMIT)
    if g.demands:
        used.append(CAP_DEMAND)
    return used


def mu1(g: Generator) -> int:
    """The one declared cost measure: the capability count."""
    return len(capabilities(g))


def is_one_step(g: Generator) -> bool:
    return mu1(g) == 1


def bundles(g: Generator) -> bool:
    return mu1(g) >= 2


def generator_name(g: Generator) -> str:
    parts = [SOURCE_NAMES[g.source]]
    if g.retains:
        parts.append("retains")
    if g.demands:
        parts.append("demands")
    return "+".join(parts)


def effective_structure(g: Generator) -> tuple[object, ...]:
    """What the generator actually does once the source is applied.

    Retaining an inscription no source names retains nothing, so that value
    collapses, exactly as the Challenge 5 naming coordinate collapses where the
    reading names nothing at any level.
    """
    return (
        SOURCE_NAMES[g.source],
        g.retains and g.source != SOURCE_NONE,
        g.demands,
    )


# ---------------------------------------------------------------------------
# What a generator emits
# ---------------------------------------------------------------------------


def emitted_inscription(reading: str, branch: Branch, g: Generator) -> str | None:
    """The inscription the generator's source names, if any."""
    if g.source == SOURCE_NONE:
        return None
    if g.source == SOURCE_ENUMERATION:
        return least_unpresented()
    return domain_member_with_marks(
        branch_configuration(reading, branch).regime.n_marks()
    )


def emitted_demand(reading: str, branch: Branch, g: Generator) -> list[int] | None:
    """The demand the generator imposes, if any."""
    if not g.demands:
        return None
    remaining = remaining_demands(reading, branch)
    if not remaining:
        return None
    return list(remaining[0])


def emitted(reading: str, branch: Branch, g: Generator) -> Json:
    """The challenge one generator emits at one branch, or its silence."""
    inscription = emitted_inscription(reading, branch, g)
    demand = emitted_demand(reading, branch, g)
    return {
        "inscription": inscription,
        "retained": inscription is not None and g.retains,
        "demand": demand,
        "demand_already_met": (
            None
            if demand is None
            else demand_met(reading, branch, (demand[0], demand[1]))
        ),
        "emits": inscription is not None or demand is not None,
    }


def emitted_key(reading: str, branch: Branch, g: Generator) -> object:
    """A comparable value for what a generator emits at one branch."""
    row = emitted(reading, branch, g)
    return (row["inscription"], row["retained"], row["demand"])


def generator_behaviour(reading: str, g: Generator) -> list[object]:
    """What the generator emits at every declared branch of the reading."""
    return [emitted_key(reading, branch, g) for branch in declared_branches(reading)]


def behaviour_digest(behaviour: Sequence[object]) -> str:
    """A deterministic digest of a generator's behaviour over the branch set.

    A naming device for the class key and never evidence: every branch at which
    two generators differ is enumerated and named beside it.
    """
    payload = "\n".join(repr(entry) for entry in behaviour)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def generator_class_key(reading: str, g: Generator, digest: str) -> list[object]:
    """The implemented quotient of generators: the structure it declares, with
    the digest of what it emits at every declared branch.

    Over the branch set and not at one branch, for the reason Challenge 5 read
    its policy key over the whole declared domain: two generators can agree at
    one branch and part at another.
    """
    return [*[str(part) for part in effective_structure(g)], digest]


def differing_branches(reading: str, a: Generator, b: Generator) -> list[str]:
    """The declared branches at which two generators emit different challenges."""
    return [
        branch.name
        for branch in declared_branches(reading)
        if emitted_key(reading, branch, a) != emitted_key(reading, branch, b)
    ]


# ---------------------------------------------------------------------------
# That the weakest emitting generator reads nothing of the branch
# ---------------------------------------------------------------------------


def branch_substitution_census(reading: str, g: Generator) -> Json:
    """Whether replacing one branch by another moves what the generator emits.

    This substitutes the WHOLE branch, declarations and configuration together,
    which is stronger than substituting the configuration alone: a generator
    whose emitted challenge is constant over the branch set reads no component
    of any branch, state included.  It is not vacuous — the branch set holds
    several distinct configuration keys, which the row reports beside the
    answer — and the state-reading source moves under it, which is what makes
    the census a test rather than a tautology.
    """
    branches = declared_branches(reading)
    moved = [
        [source.name, other.name]
        for source in branches
        for other in branches
        if emitted_key(reading, other, g) != emitted_key(reading, source, g)
    ]
    return {
        "generator": generator_name(g),
        "substitutions": len(branches) * len(branches),
        "substitutions_that_move_the_challenge": len(moved),
        "first_moving_substitutions": moved[:4],
        "distinct_configuration_keys": len(
            {repr(branch_least_key(reading, branch)) for branch in branches}
        ),
        "reads_nothing_of_the_branch": not moved,
    }


DECLARED_GENERATOR_INPUTS: tuple[str, ...] = (
    "the declared 144-member domain of inscriptions and its order",
    "the record of the texts the caller has presented",
)
DECLARED_GENERATOR_INPUTS_ARE_METATHEORY_BECAUSE = (
    "the domain is the Challenge 5 reader's own enumeration and the presented "
    "record is a reading of the history (definition 20 at the level of texts); "
    "no regime, deep regime, judgment, or profile is among them, which the "
    "substitution census computes rather than asserts"
)


# ---------------------------------------------------------------------------
# The declared resource bounds
# ---------------------------------------------------------------------------


NODE_CEILING = 1000
"""The largest number of branch nodes the continuation may hold.

A DECLARATION of this stage, derived from nothing: it is not read off the run,
and a different ceiling gives a different round bound, which the receipt
reports at five ceilings so that the dependence is visible.  What is computed
from it is the round bound.
"""

SEED_ROUND_BOUND = 15
CEILING_SENSITIVITY: tuple[int, ...] = (10, 100, 1000, 10000, 100000)


def nodes(branches: int, branching: int, rounds: int) -> int:
    """The largest number of nodes a tree of this branching can hold.

    ``nodes(b, k, 0) = b`` and ``nodes(b, k, r + 1) = nodes(b, k, r) + b * k **
    (r + 1)``: every branch may split into at most ``k`` at each round and
    nothing is pruned, so this is an upper bound and never a count.
    """
    if rounds < 0:
        raise ValueError(f"a round count is nonnegative, got {rounds}")
    total = branches
    for level in range(1, rounds + 1):
        total += branches * branching**level
    return total


def round_bound(branches: int, branching: int, ceiling: int) -> int:
    """The largest round count whose worst-case node count fits the ceiling.

    Computed and not declared.  ``nodes`` does not decrease as the round count
    grows, so the search stops at the first round that does not fit; it is
    bounded by the seed's own fifteen, and a branch set that does not fit at
    one round reports zero.
    """
    best = 0
    for rounds in range(1, SEED_ROUND_BOUND + 1):
        if nodes(branches, branching, rounds) > ceiling:
            return best
        best = rounds
    return best


def branching_bound() -> int:
    """The largest number of tied minimum classes any closed rung produced.

    Read off the closed rungs' own recomputed minima under both readings rather
    than declared: it is what this run's enumerations have actually done.
    """
    return max(
        len(rung_classes(rung, reading))
        for rung in CLOSED_RUNGS
        for reading in READINGS
    )


def bounds_facts(reading: str) -> Json:
    branches = len(declared_branches(reading))
    branching = branching_bound()
    bound = round_bound(branches, branching, NODE_CEILING)
    return {
        "node_ceiling": NODE_CEILING,
        "node_ceiling_is_declared": True,
        "branching_bound": branching,
        "branching_bound_read_off": {
            f"challenge{rung}": {
                name: len(rung_classes(rung, name)) for name in READINGS
            }
            for rung in CLOSED_RUNGS
        },
        "branches": branches,
        "round_bound": bound,
        "round_bound_is_computed": True,
        "nodes_at_the_round_bound": nodes(branches, branching, bound),
        "nodes_one_round_further": nodes(branches, branching, bound + 1),
        "seed_round_bound": SEED_ROUND_BOUND,
        "short_of_the_seed_bound": bound < SEED_ROUND_BOUND,
        "frontier_export_is_owed": bound < SEED_ROUND_BOUND,
        "ceiling_sensitivity": [
            [ceiling, round_bound(branches, branching, ceiling)]
            for ceiling in CEILING_SENSITIVITY
        ],
        "rounds_accepted_at_this_stage": 0,
    }


# ---------------------------------------------------------------------------
# Rows
# ---------------------------------------------------------------------------


def generator_row(reading: str, branch: Branch, g: Generator) -> Json:
    """One generator at one branch: its cost, whether it is one step, whether
    it bundles, and what it emits there."""
    row: Json = {
        "name": generator_name(g),
        "coordinates": dict(zip(COORDINATES, g.values())),
        "capability_coordinates": changed_coordinates(g),
        "capabilities": capabilities(g),
        "mu1": mu1(g),
        "one_step": is_one_step(g),
        "bundles": bundles(g),
        "effective_structure": [str(part) for part in effective_structure(g)],
        "class_key": generator_class_key(
            reading, g, behaviour_digest(generator_behaviour(reading, g))
        ),
    }
    row.update(emitted(reading, branch, g))
    return row


def branch_detail(reading: str, branch: Branch) -> Json:
    """The full report for one branch: what it adopts, what it declares, what it
    replays, what it holds, what it still owes, and its generators."""
    configuration = branch_configuration(reading, branch)
    rn = branch_renamings(reading, branch)
    rows = [generator_row(reading, branch, g) for g in generator_space()]
    minima = one_step_minima(rows, "mu1", "emits")
    certified = branch_certified(reading, branch)
    return {
        "name": branch.name,
        "adopts": None if branch.rung is None else f"challenge{branch.rung}",
        "adopted_class": (
            []
            if branch.rung is None
            else next(
                members
                for members in rung_classes(branch.rung, reading)
                if members[0] == branch.name
            )
        ),
        "declarations": {
            "coordinates": dict(zip(challenge4.COORDINATES, branch.aug.values())),
            "policy": (
                None
                if branch.policy is None
                else challenge5.POLICY_NAMES[branch.policy]
            ),
            "effective_structure": [
                str(part)
                for part in challenge4.effective_structure(reading, branch.aug)
            ],
            "renamings": {
                "reflection": rn.reflection,
                "mark_permutations": rn.mark_permutations,
                "group_permutations": rn.group_permutations,
                "keep_labels": rn.keep_labels,
                "keep_groups": rn.keep_groups,
            },
        },
        "history": branch_history(reading, branch),
        "configuration": {
            "marks": list(configuration.regime.marks),
            "placement": list(configuration.regime.placement),
            "groups": list(configuration.groups),
            "n_marks": configuration.regime.n_marks(),
            "retained_wholes": branch_tags(reading, branch),
        },
        "certified": certified,
        "replays_from_genesis": certified,
        "automorphism_count": len(configuration_automorphisms(configuration, rn)),
        "least_key": branch_least_key(reading, branch),
        "branch_key": branch_key(reading, branch),
        "live_requirement": live_requirement(reading, branch),
        "demand_pairs": [list(pair) for pair in branch_pairs(reading, branch)],
        "remaining_demands": [list(pair) for pair in remaining_demands(reading, branch)],
        "generators": rows,
        "emitting_generators": [str(row["name"]) for row in rows if row["emits"]],
        "minima_by_mu1": minima,
        "weakest_emitting_generators": list(minima["points"]),
        "initial_datum_unchanged": configuration.regime.initial_datum
        == genesis(reading).initial_datum,
        "reading_unchanged": configuration.regime.reading == reading,
        "event_follows_relation_empty": all(
            not event_follows(configuration.regime, e)
            for e in challenge1.probes(challenge5.CALLER_TOKEN)
        ),
        "deep_event_follows_relation_empty": all(
            not deep_event_follows(deep_genesis(reading), e)
            for e in challenge5.probes(challenge5.CALLER_TOKEN)
        ),
    }


def reading_facts(reading: str) -> Json:
    branches = declared_branches(reading)
    detail = [branch_detail(reading, branch) for branch in branches]
    weakest = sorted({name for row in detail for name in row["weakest_emitting_generators"]})
    ties = [str(row["name"]) for row in detail if len(row["minima_by_mu1"]["classes"]) > 1]
    return {
        "reading": reading,
        "branch_candidates": [branch.label() for branch in branch_candidates(reading)],
        "branch_classes": branch_classes(reading),
        "branch_count": len(branches),
        "branches": [branch.name for branch in branches],
        "branch_classes_without_the_policy_key": branch_classes_without_the_policy(
            reading
        ),
        "branch_count_without_the_policy_key": len(
            branch_classes_without_the_policy(reading)
        ),
        "branch_detail": detail,
        "generator_space_size": len(generator_space()),
        "one_step_generators": [
            generator_name(g) for g in generator_space() if is_one_step(g)
        ],
        "bundles_refused": [generator_name(g) for g in generator_space() if bundles(g)],
        "one_step_iff_capability_count_one": all(
            is_one_step(g) == (mu1(g) == 1) for g in generator_space()
        ),
        "one_step_iff_one_coordinate_moved": all(
            is_one_step(g) == (len(changed_coordinates(g)) == 1)
            for g in generator_space()
        ),
        "minimum_capability_count_among_emitting": sorted(
            {row["minima_by_mu1"]["minimum"] for row in detail}
        ),
        "weakest_emitting_generators": weakest,
        "branches_with_a_tie": ties,
        "the_minimum_is_unique_on_every_branch": not ties,
        "the_same_challenge_on_every_branch": len(
            {repr(emitted_key(reading, branch, ENUMERATION_GENERATOR)) for branch in branches}
        )
        == 1,
        "first_challenge": emitted(reading, branches[0], ENUMERATION_GENERATOR),
        "demand_generator_emits_at": [
            branch.name
            for branch in branches
            if emitted(reading, branch, DEMAND_GENERATOR)["emits"]
        ],
        "branches_parting_the_two_one_step_emitting_generators": differing_branches(
            reading, ENUMERATION_GENERATOR, DEMAND_GENERATOR
        ),
        "substitution_census": [
            branch_substitution_census(reading, g)
            for g in (ENUMERATION_GENERATOR, DEMAND_GENERATOR, STATE_GENERATOR)
        ],
        "bounds": bounds_facts(reading),
    }


# ---------------------------------------------------------------------------
# The presented record and the first challenge, reported once
# ---------------------------------------------------------------------------


def record_facts() -> Json:
    text = least_unpresented()
    whole = None if text is None else read_nested_whole(text)
    return {
        "presented": list(PRESENTED_TEXTS),
        "presented_indices": presented_indices(),
        "every_presented_text_is_in_the_domain": all(
            presented in domain_texts() for presented in PRESENTED_TEXTS
        ),
        "domain_size": len(domain_texts()),
        "least_unpresented_index": least_unpresented_index(),
        "least_unpresented": text,
        "least_unpresented_marks": None if whole is None else marks_in(whole),
        "least_unpresented_depth": (
            None if whole is None else presentation.whole_depth(whole)
        ),
        "least_unpresented_is_a_further_mark": (
            whole is not None
            and marks_in(whole) == 1
            and presentation.whole_depth(whole) == 1
        ),
        "initial_inscription_in_the_record": INITIAL_INSCRIPTION in PRESENTED_TEXTS,
        "note": (
            "the record is metatheory of the history and no regime carries it; "
            "the initial inscription is in it because definition 1 makes it a "
            "supplied whole, and leaving it out would make the least "
            "unpresented member the initial inscription itself"
        ),
    }


CAPABILITIES: dict[str, dict[str, str]] = {
    "admitted boundary": {
        "declared_at": "the seed, as the one admitted primitive exception",
        "paid_by": "the seed",
        "buys_at_stage_1": (
            "every configuration a branch holds, each mark of it lying on a "
            "side; the branch set and the generator space are stated without "
            "it, and what they range over is not"
        ),
    },
    "side names under O": {
        "declared_at": "genesis, as the O reading of the one declaration",
        "paid_by": "the declared reading",
        "buys_at_stage_1": (
            "one branch fewer and one tie fewer: under O the Challenge 3 "
            "minimum is the null point, which adopts nothing, so the branch "
            "that carries a third retained whole is a branch of reading U alone"
        ),
    },
    "the process supplies": {
        "declared_at": "stage 1, as this stage's own declaration",
        "paid_by": "whichever generator is taken, and none is taken here",
        "buys_at_stage_1": (
            "that a next challenge exists at all: without it the only generator "
            "of capability count zero emits nothing and every branch stops for "
            "want of a next challenge"
        ),
    },
    "the process admits": {
        "declared_at": (
            "Challenge 3, as the further-mark candidate's one capability "
            "(definition 45)"
        ),
        "paid_by": "whichever candidate is taken, and none is taken here",
        "buys_at_stage_1": (
            "nothing on its own: a generator that retains what no source named "
            "retains nothing, and one that supplies and retains costs two and "
            "is refused as a bundle"
        ),
    },
}

BOUNDARY_DEPENDENCE: dict[str, str] = {
    "the branch set, the one-adoption rule, and the branch quotient": (
        "does not depend on the admitted boundary as a rule, but every "
        "configuration it quotients does: the least key it compares is a key of "
        "a placement, and a placement is a side per mark"
    ),
    "the generator space, its capabilities, the one-step rule, and the refusal "
    "of bundles": "does not depend on the admitted boundary",
    "the enumeration generator and what it emits": (
        "requires the admitted boundary through the declared domain, whose "
        "members are wholes delimited by one bar with a side on each hand; the "
        "enumeration of that domain and the order on it are declarations the "
        "boundary does not decide"
    ),
    "the demand generator, and the requirement it imposes": (
        "requires the admitted boundary: a permitted automorphism of a "
        "configuration is a renaming of marks and, under U, of the two sides"
    ),
    "the node ceiling, the branching bound, and the computed round bound": (
        "does not depend on the admitted boundary: they count branches and "
        "rounds and would be stated the same way for any finite branching"
    ),
}


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


SCORED_PREDICTIONS: tuple[str, ...] = (
    "S1-1", "S1-2", "S1-3", "S1-4", "S1-5", "S1-6", "S1-7", "S1-8", "S1-9",
)
# The scored prediction whose every hitting clause, read literally, is fixed by
# a declaration of this stage: the generator space with its declared coordinate
# values, capability names and counts.  A HIT on it is HIT by construction and
# is not counted as content; a miss on it is a miss like any other.  The
# criterion is the one Challenge 1 declared.
DEFINITION_LEVEL_PREDICTIONS: tuple[str, ...] = ("S1-3",)
TALLY_CRITERION = challenge1.TALLY_CRITERION


def verdict(hit: bool) -> str:
    return "HIT" if hit else "MISSED"


def combine(*statuses: str) -> str:
    """HIT when every clause hits, MISSED when none does, PARTIAL between."""
    hits = [status == "HIT" for status in statuses]
    if all(hits):
        return "HIT"
    if not any(hits):
        return "MISSED"
    return "PARTIAL"


def _enumeration_reads_nothing(u: Json, o: Json) -> bool:
    return all(
        row["reads_nothing_of_the_branch"]
        for facts in (u, o)
        for row in facts["substitution_census"]
        if row["generator"] == "enumeration"
    )


def event_returning_functions() -> list[str]:
    """The Challenge 0 census, run over this stage's own module."""
    return state_event_generators(sys.modules[__name__], EVENT_TYPES)


def score(u: Json, o: Json, record: Json) -> Json:
    """Score this stage's frozen predictions against the enumeration."""
    counts_clause = verdict(u["branch_count"] == 6 and o["branch_count"] == 5)
    quotient_clause = verdict(
        any(len(members) > 1 for members in u["branch_classes"])
        and any(len(members) > 1 for members in o["branch_classes"])
    )
    policy_key_clause = verdict(
        u["branch_count_without_the_policy_key"] == 5
        and o["branch_count_without_the_policy_key"] == 4
    )
    space_clause = verdict(
        u["generator_space_size"] == 12 and o["generator_space_size"] == 12
    )
    counts_part_clause = verdict(
        bool(u["one_step_iff_capability_count_one"])
        and not u["one_step_iff_one_coordinate_moved"]
    )
    minimum_clause = verdict(
        u["minimum_capability_count_among_emitting"] == [1]
        and o["minimum_capability_count_among_emitting"] == [1]
    )
    tie_clause = verdict(
        u["branches_with_a_tie"] == ["extra_mark_0"]
        and o["branches_with_a_tie"] == []
    )
    demand_clause = verdict(
        u["demand_generator_emits_at"] == ["extra_mark_0"]
        and o["demand_generator_emits_at"] == []
    )
    same_clause = verdict(
        bool(u["the_same_challenge_on_every_branch"])
        and bool(o["the_same_challenge_on_every_branch"])
    )
    first_clause = verdict(
        record["least_unpresented"] == "<|b>"
        and bool(record["least_unpresented_is_a_further_mark"])
    )
    substitution_clause = verdict(_enumeration_reads_nothing(u, o))
    no_event_clause = verdict(not event_returning_functions())
    bounds_clause = verdict(
        u["bounds"]["branching_bound"] == 3
        and u["bounds"]["round_bound"] == 4
        and o["bounds"]["round_bound"] == 4
        and bool(u["bounds"]["short_of_the_seed_bound"])
    )
    inertia_clause = verdict(
        all(
            row["certified"]
            and row["replays_from_genesis"]
            and row["initial_datum_unchanged"]
            and row["reading_unchanged"]
            and row["event_follows_relation_empty"]
            and row["deep_event_follows_relation_empty"]
            for facts in (u, o)
            for row in facts["branch_detail"]
        )
    )
    rounds_clause = verdict(
        u["bounds"]["rounds_accepted_at_this_stage"] == 0
        and o["bounds"]["rounds_accepted_at_this_stage"] == 0
    )
    return {
        "S1-1": {
            "label": "NOT FORCED",
            "status": combine(counts_clause, quotient_clause),
            "counts_clause_status": counts_clause,
            "quotient_identifies_a_class_clause_status": quotient_clause,
            "evidence": (
                f"branch counts {u['branch_count']} under U and "
                f"{o['branch_count']} under O, from the closed rungs' "
                "recomputed minima and the implemented branch key"
            ),
            "result_basis": "content: a recomputation and an implemented quotient",
        },
        "S1-2": {
            "label": "FORCED",
            "status": policy_key_clause,
            "evidence": (
                "with the policy part dropped the branch counts fall to "
                f"{u['branch_count_without_the_policy_key']} under U and "
                f"{o['branch_count_without_the_policy_key']} under O"
            ),
            "result_basis": "content: the two keys computed and compared",
        },
        "S1-3": {
            "label": "NOT FORCED",
            "status": combine(space_clause, counts_part_clause),
            "space_size_clause_status": space_clause,
            "counts_part_clause_status": counts_part_clause,
            "evidence": (
                f"{u['generator_space_size']} points over {len(COORDINATES)} "
                f"coordinates and {len(CAPABILITY_OF)} declared capabilities"
            ),
            "result_basis": (
                "DEFINITION-level: the coordinates, the capability names, and "
                "the counts are declarations of this stage"
            ),
        },
        "S1-4": {
            "label": "FORCED",
            "status": combine(minimum_clause, tie_clause, demand_clause),
            "minimum_clause_status": minimum_clause,
            "tie_clause_status": tie_clause,
            "demand_generator_clause_status": demand_clause,
            "evidence": (
                "the minimum among emitting generators is "
                f"{u['minimum_capability_count_among_emitting']} under U and "
                f"{o['minimum_capability_count_among_emitting']} under O; the "
                f"demand generator emits at {u['demand_generator_emits_at']} "
                f"under U and {o['demand_generator_emits_at']} under O"
            ),
            "result_basis": (
                "content: an eligibility filter computed per branch, with both "
                "values attained under U"
            ),
        },
        "S1-5": {
            "label": "FORCED",
            "status": combine(same_clause, first_clause),
            "same_challenge_clause_status": same_clause,
            "first_challenge_clause_status": first_clause,
            "evidence": (
                f"the first challenge is {record['least_unpresented']!r}, index "
                f"{record['least_unpresented_index']} of the declared domain, "
                f"with {record['least_unpresented_marks']} mark at depth "
                f"{record['least_unpresented_depth']}"
            ),
            "result_basis": "content: an enumeration over the declared domain",
        },
        "S1-6": {
            "label": "FORCED",
            "status": combine(substitution_clause, no_event_clause),
            "substitution_clause_status": substitution_clause,
            "no_event_returning_function_clause_status": no_event_clause,
            "evidence": (
                "every substitution of one declared branch for another leaves "
                "the emitted challenge where it was, over a branch set holding "
                "several distinct configuration keys, so the substitution "
                "clause HITS.  The second clause MISSED, recorded next to its "
                f"value: the census names {event_returning_functions()} in this "
                "stage's module, the function that reads the recorded caller "
                "history each branch replays.  What the clause asserted is "
                "false; what holds instead is in `events_named_by_this_stage`"
            ),
            "result_basis": "content: a census over every ordered pair of branches",
        },
        "S1-7": {
            "label": "FORCED",
            "status": verdict(
                record["least_unpresented"] not in record["presented"]
                and bool(record["every_presented_text_is_in_the_domain"])
            ),
            "evidence": (
                "the emitted challenge is not in the presented record; "
                "non-repetition and the exhaustion condition are the Lean "
                "theorems firstMissing_never_repeats and "
                "firstMissingFrom_none_means_every_index_present"
            ),
            "result_basis": (
                "content in the enumeration for the record; PROVED in Lean for the "
                "non-repetition and the exhaustion condition"
            ),
        },
        "S1-8": {
            "label": "NOT FORCED",
            "status": bounds_clause,
            "evidence": (
                f"branching bound {u['bounds']['branching_bound']} off the "
                f"closed rungs; round bound {u['bounds']['round_bound']} under U "
                f"and {o['bounds']['round_bound']} under O at a declared ceiling "
                f"of {NODE_CEILING}, against the seed's {SEED_ROUND_BOUND}"
            ),
            "result_basis": (
                "content: the branching bound is read off the closed rungs' own "
                "minima and the round bound is computed from it; the ceiling is "
                "a declaration and is listed as one"
            ),
        },
        "S1-9": {
            "label": "FORCED",
            "status": combine(inertia_clause, rounds_clause),
            "inertia_clause_status": inertia_clause,
            "no_round_accepted_clause_status": rounds_clause,
            "evidence": (
                "every branch replays from genesis and is certified; the "
                "initial datum and the reading are unchanged; both "
                "event-follows relations are empty on every probe; no round is "
                "accepted"
            ),
            "result_basis": (
                "content for the replay and certification at every branch; "
                "DEFINITION-level for the empty relations, which are declared "
                "empty, and reported apart"
            ),
        },
        "S1-X": {
            "label": "NOT FORCED",
            "status": "PENDING",
            "evidence": "scored by the stage that runs the accepted rounds",
        },
    }


def score_c5x(u: Json, o: Json, record: Json) -> Json:
    """Score the Challenge 5 extrapolation against this stage's facts.

    The frozen clause is about the GENERATOR importing object-language
    structure the run has not declared, so it is scored on the substitution
    census and not on this stage's own function census.  The function census is
    a clause of the frozen S1-6, which it MISSES, and the two are kept apart
    rather than one verdict being carried into the other.
    """
    further_mark = verdict(bool(record["least_unpresented_is_a_further_mark"]))
    no_undeclared = verdict(_enumeration_reads_nothing(u, o))
    not_fifteen = verdict(
        u["bounds"]["rounds_accepted_at_this_stage"] < SEED_ROUND_BOUND
        and o["bounds"]["rounds_accepted_at_this_stage"] < SEED_ROUND_BOUND
    )
    smaller_bound = verdict(
        bool(u["bounds"]["short_of_the_seed_bound"])
        and bool(o["bounds"]["short_of_the_seed_bound"])
    )
    return {
        "label": "NOT FORCED",
        "status": "PENDING",
        "first_challenge_is_a_further_mark_clause_status": further_mark,
        "imports_no_undeclared_structure_clause_status": no_undeclared,
        "fifteen_rounds_not_reached_clause_status": not_fifteen,
        "smaller_bound_declared_clause_status": smaller_bound,
        "frontier_exported_clause_status": "PENDING",
        "evidence": (
            "four of the five clauses are decided here and hit: the first "
            f"challenge is {record['least_unpresented']!r}, one mark at depth "
            f"{record['least_unpresented_depth']}; the generator reads nothing "
            "of the branch, which is what this clause asks and what the "
            "substitution census computes; no round is accepted, so fifteen "
            "are not reached; and the "
            f"round bound is {u['bounds']['round_bound']}, short of "
            f"{SEED_ROUND_BOUND}.  The frontier export is the work of the stage "
            "that runs the rounds, so the prediction stays PENDING and is not "
            "counted in this stage's tally"
        ),
    }


def tally(scores: Json) -> Json:
    """Count the scored predictions by status and by basis."""
    by_status: dict[str, list[str]] = {"HIT": [], "PARTIAL": [], "MISSED": []}
    for cid in SCORED_PREDICTIONS:
        status = str(scores[cid]["status"])
        if status not in by_status:
            raise ValueError(f"unexpected status {status!r} for {cid}")
        by_status[status].append(cid)
    return {
        "scored": list(SCORED_PREDICTIONS),
        "definition_level_declared": list(DEFINITION_LEVEL_PREDICTIONS),
        "criterion": TALLY_CRITERION,
        "hit_as_content": [
            c for c in by_status["HIT"] if c not in DEFINITION_LEVEL_PREDICTIONS
        ],
        "hit_definition_level": [
            c for c in by_status["HIT"] if c in DEFINITION_LEVEL_PREDICTIONS
        ],
        "partial": by_status["PARTIAL"],
        "missed": by_status["MISSED"],
    }


def event_returning_functions_by_module() -> dict[str, list[str]]:
    """The Challenge 0 census, run over this stage's modules."""
    return {
        "model": state_event_generators(model, EVENT_TYPES),
        "presentation": state_event_generators(presentation, EVENT_TYPES),
        "continuation1": event_returning_functions(),
    }


def events_named_facts() -> Json:
    """What this stage's event-returning functions actually return.

    The frozen S1-6 asserted this census would be empty for this module and it
    is not: replaying a recorded history means naming its events, and the
    census cannot tell naming a recorded event from issuing a new one.  The
    miss is recorded with its value, and what the census cannot see is stated
    beside it and computed: every branch's configuration is the replay of its
    own recorded history, and this stage declares no event kind.
    """
    return {
        "functions": event_returning_functions(),
        "what_they_return": (
            "the recorded caller history each branch replays: the Challenge 4 "
            "retention history, extended on the further-mark branch by that "
            "class's own declared admission (definition 45)"
        ),
        "event_kinds_declared_at_this_stage": [],
        "every_branch_configuration_is_certified": all(
            branch_certified(reading, branch)
            for reading in READINGS
            for branch in declared_branches(reading)
        ),
        "what_the_census_cannot_see": (
            "the census reads a return annotation; it cannot tell a function "
            "that names the events of a recorded history from one that issues a "
            "new event, so a clean census would not have been evidence either"
        ),
    }


def build() -> Json:
    u = reading_facts(READING_U)
    o = reading_facts(READING_O)
    record = record_facts()
    scores = score(u, o, record)
    scores["C5-X"] = score_c5x(u, o, record)
    return {
        "stage": STAGE,
        "of": "the autonomous continuation",
        "closes": (
            "the declaration of the branches, their challenge generators, and "
            "the resource bounds; no round is run"
        ),
        "seed_sha256": SEED_SHA256,
        "predictions_sha256": PREDICTIONS_SHA256,
        "challenge0_predictions_sha256": C0_PREDICTIONS_SHA256,
        "challenge1_predictions_sha256": C1_PREDICTIONS_SHA256,
        "challenge2_predictions_sha256": C2_PREDICTIONS_SHA256,
        "challenge3_predictions_sha256": C3_PREDICTIONS_SHA256,
        "challenge4_predictions_sha256": C4_PREDICTIONS_SHA256,
        "challenge5_predictions_sha256": C5_PREDICTIONS_SHA256,
        "branch_space": {
            "one_adoption_rule": ONE_ADOPTION_RULE,
            "closed_rungs": list(CLOSED_RUNGS),
            "rung_predicate": {f"challenge{k}": v for k, v in RUNG_PREDICATE.items()},
            "rung_minima": {
                f"challenge{rung}": {
                    reading: {
                        "minimum": rung_minimum(rung, reading),
                        "classes": rung_classes(rung, reading),
                    }
                    for reading in READINGS
                }
                for rung in CLOSED_RUNGS
            },
            "quotient": (
                "two branches are the same branch exactly when their branch "
                "keys are equal; the key is the declarations in force, the "
                "adopted policy's own Challenge 5 class key, and the least key "
                "of the configuration under the branch's own permitted "
                "renamings"
            ),
        },
        "generator_space": {
            "sources": list(SOURCE_SPACE),
            "source_names": [SOURCE_NAMES[s] for s in SOURCE_SPACE],
            "exhaustive_because": SOURCE_SPACE_IS_EXHAUSTIVE_BECAUSE,
            "coordinates": list(COORDINATES),
            "capability_of": CAPABILITY_OF,
            "size": len(generator_space()),
            "one_step_rule": ONE_STEP_RULE,
            "declared_inputs": list(DECLARED_GENERATOR_INPUTS),
            "declared_inputs_are_metatheory_because": (
                DECLARED_GENERATOR_INPUTS_ARE_METATHEORY_BECAUSE
            ),
            "what_a_generated_challenge_is": (
                "at most one inscription of the declared domain, supplied; "
                "whether that inscription is also retained; and at most one "
                "demand that two named retained wholes of the branch be "
                "internally separable in the declared sense.  A generator emits "
                "a challenge exactly when it produces an inscription or a demand"
            ),
        },
        "measures": {
            "mu1": MU1,
            "no_second_measure_because": NO_SECOND_MEASURE_BECAUSE,
        },
        "requirement_sense": REQUIREMENT_SENSE,
        "imposed_demands": [list(pair) for pair in IMPOSED_DEMANDS],
        "record": record,
        "capabilities": CAPABILITIES,
        "boundary_dependence": BOUNDARY_DEPENDENCE,
        "readings": {READING_U: u, READING_O: o},
        "event_kinds": [t.__name__ for t in EVENT_TYPES],
        "new_event_kinds_at_stage_1": [],
        "withdrawn_rules_at_stage_1": [],
        "event_returning_functions_by_module": event_returning_functions_by_module(),
        "events_named_by_this_stage": events_named_facts(),
        "observation_vocabulary": observation_vocabulary(),
        "what_the_stage_exercises": {
            "supply": (
                "yes, as the thing the weakest emitting generator would do and "
                "does not: no generator is taken and no presentation event is "
                "issued anywhere in this stage"
            ),
            "mention": (
                "yes: a generated challenge is reported as a text, and naming a "
                "text is not presenting it"
            ),
            "admission": (
                "no: nothing is admitted, and the capability that would let the "
                "process admit is priced and refused as the second half of a "
                "bundle"
            ),
            "current-state designation": (
                "yes: each branch's configuration is the replay of its own "
                "recorded history and of no event that history does not contain"
            ),
            "retention": (
                "yes, per branch: what the caller's Challenge 5 retention "
                "amounts to depends on the policy a branch adopts, and the two "
                "policy branches are the two that adopt one"
            ),
            "observation": (
                "yes: the closed grammar is unchanged and no form is added"
            ),
            "side": (
                "yes: every configuration a branch holds is a side per mark, "
                "and the branch quotient compares those keys"
            ),
            "equality": (
                "yes: structural equality of a configuration, the branch key, "
                "and the generator class key over the branch set are three "
                "different relations, and the stage uses all three"
            ),
        },
        "scores": scores,
        "tally": tally(scores),
        "authority_effect": "None",
    }
