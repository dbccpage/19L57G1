"""Challenge 5: the caller supplies and retains `<<a|>|>`, a whole within a
side.

Everything computed here is metatheory about the kernel in ``model.py``, the
presentation layer in ``presentation.py``, and the readers of Challenges 1 and
4.  Nothing here is admitted beyond the caller's own history under a declared
policy: every policy is a candidate, no policy is taken, and every retained
state is the replay of an explicit history.

The rung has five parts, in this order:

1. **A third reader bound, the second widening of the run's reader.**  Both
   readers the run has refuse the inscription by name: neither reads an ITEM
   on a side that is itself a whole.  The bound is widened to a reader in
   which an item is a mark or a whole, down to a declared finite depth, and
   both narrower readers are left refusing so that what forced each widening
   stays visible.  The run has three reader bounds and has widened twice: the
   Challenge 1 bound was declared and not widened.  Reading a nested item is
   not admitting one.
2. **The declared policy space.**  What an admission does with an item that is
   a whole is not decided by the admitted boundary, so four policies are
   declared and priced: refuse it; admit the inner whole as one opaque mark on
   the outer side; discard the inner boundary and admit its items on the outer
   side; record the crossing, admitting the items with the sequence of sides
   crossed to reach them.  Three capabilities are declared for policies and a
   fourth for the naming coordinate of part 5.
3. **What each policy retains, and what it makes invisible.**  Under both
   one-step policies the caller's inscription retains one mark on one side and
   is isomorphic — under the discarding policy, EQUAL — to what the Challenge 1
   inscription `<a|>` retains.  So the object language cannot see a boundary
   within a side at any policy of capability count one.
4. **Depth, in two senses kept apart.**  Under the recording policy a mark's
   depth is invariant under every permitted renaming and determined by the
   key, so it is internally available in the sense Challenge 3 declared; no
   judgment form of the closed grammar reads it, so it is not expressible, and
   this rung adds no form.
5. **What "within" means at depth two.**  Whether the reading's naming of the
   two sides reaches the inner boundary is a further declaration the seed's one
   exception does not decide.  It collapses under U, which names nothing at any
   level, and does not collapse under O.

**One step is capability count one, and at this rung that is no longer the
coordinate count.**  Challenge 4 could report the two as the same number
because each of its coordinates named one capability.  Here the policy
coordinate has a value that uses two, so the two counts part, and the run keeps
the CAPABILITY reading: the seed requires a candidate called one step not to
bundle capabilities.  Challenge 4's identity of the two counts is therefore a
fact about that rung's space and not a general one.

The declared space is exhaustive over its two coordinates and over nothing
wider.  Every minimality statement below is scoped to it.
"""

from __future__ import annotations

import hashlib
import sys
from dataclasses import dataclass
from functools import cache
from itertools import combinations
from typing import Sequence

from boundary import challenge0, challenge1, challenge2, challenge3, challenge4
from boundary import model, presentation
from boundary.challenge0 import observation_vocabulary, state_event_generators
from boundary.challenge1 import Json, key_json
from boundary.challenge2 import DECLARED_POLICY, RELABELLED_TOKEN
from boundary.challenge3 import one_step_minima
from boundary.model import (
    READING_O,
    READING_U,
    Address,
    AdmissionError,
    AdmitAt,
    AdmitOccurrence,
    DeepEvent,
    DeepRegime,
    Event,
    Regime,
    Supply,
    certify,
    deep_automorphisms,
    deep_canonical,
    deep_certify,
    deep_event_follows,
    deep_genesis,
    deep_is_isomorphic,
    deep_mark_orbit,
    deep_replay,
    depth_of,
    event_follows,
    flatten_deep,
    genesis,
    is_isomorphic,
    replay,
)
from boundary.presentation import (
    DECLARED_CONVENTION,
    DECLARED_WITHIN_WHOLE_ORDER,
    NESTING_BOUND,
    OTHER_WITHIN_WHOLE_ORDER,
    WITHIN_WHOLE_ORDERS,
    Item,
    NestedWhole,
    PresentationError,
    admitted_side,
    read_nested_whole,
    read_pair_whole,
    read_whole,
    render_whole,
    whole_depth,
)

SEED_SHA256 = challenge0.SEED_SHA256
C0_PREDICTIONS_SHA256 = challenge0.PREDICTIONS_SHA256
C1_PREDICTIONS_SHA256 = challenge1.PREDICTIONS_SHA256
C2_PREDICTIONS_SHA256 = challenge2.PREDICTIONS_SHA256
C3_PREDICTIONS_SHA256 = challenge3.PREDICTIONS_SHA256
C4_PREDICTIONS_SHA256 = challenge4.PREDICTIONS_SHA256
PREDICTIONS_SHA256 = "b3aab18d8e5a0700e563862ef7a884248badefbc7c653df0e00097044e3d99de"

INSCRIPTION = "<<a|>|>"
FLAT_INSCRIPTION = "<a|>"
DEEPER_INSCRIPTION = "<<<a|>|>|>"
CALLER_TOKEN = "a"
WHOLE_TOKEN = "w"
"""The declared presentation token of a whole admitted as a mark (definition 71).

A whole admitted opaquely presents no visible mark of its own, so the run
declares ONE token for every such presentation.  That conflates all inner
wholes at the presentation level, which is what admitting one opaquely means,
and it changes no key: definition 14 forgets the labels.  It is a declaration
of this rung and is recorded rather than assumed.

It carries weight beyond the presentation: the collateral fact
``inner_whole_presentation_admitted`` is this token's membership in the
retained state's labels, and the enumeration reports it as the ONE declared
fact separating the opaque policy from the discarding one, so the second
measure's choice between the two tied minima rests on this declaration.
"""

LEVELS: tuple[int, ...] = tuple(range(NESTING_BOUND))
ALPHABET: tuple[str, str] = (CALLER_TOKEN, "b")
EVENT_TYPES: tuple[type, ...] = (Supply, model.AdmitMark, AdmitOccurrence, AdmitAt)
STATE_CHANGING_EVENT_KINDS: list[str] = ["AdmitMark", "AdmitOccurrence", "AdmitAt"]
NEW_EVENT_KINDS_AT_CHALLENGE_5: list[str] = ["AdmitAt"]
WITHDRAWN_RULES_AT_CHALLENGE_5: list[str] = []

READER_WIDENING = (
    "an item on a side is a mark OR a whole, down to a declared depth bound "
    "of two, where the Challenge 4 reader admitted at most one MARK on each "
    "side and read no item that is itself a whole"
)
NESTED_ORDER_DECLARATION = (
    "the declared within-whole admission order is applied at every level, and "
    "every supply of the retained whole precedes every admission of it; the "
    "inscription fixes neither, any more than it fixes the convention"
)
DECLARED_AT_CHALLENGE_5: tuple[str, ...] = (
    READER_WIDENING,
    NESTED_ORDER_DECLARATION,
    "one presentation token for every whole admitted as a mark",
)

# ---------------------------------------------------------------------------
# The declared policy space
# ---------------------------------------------------------------------------

POLICY_REFUSE = "refuse: an admission never names an item that is a whole"
POLICY_OPAQUE = (
    "opaque: the inner whole is admitted as ONE mark on the outer side and its "
    "interior is discarded"
)
POLICY_FLATTEN = (
    "discard: the inner boundary is discarded and the inner whole's own items "
    "are admitted on the outer side"
)
POLICY_ADDRESS = (
    "record: the inner whole's items are admitted, each carrying the finite "
    "sequence of sides crossed to reach it"
)
POLICY_SPACE: tuple[str, str, str, str] = (
    POLICY_REFUSE,
    POLICY_OPAQUE,
    POLICY_FLATTEN,
    POLICY_ADDRESS,
)
POLICY_NAMES: dict[str, str] = {
    POLICY_REFUSE: "refuse",
    POLICY_OPAQUE: "opaque",
    POLICY_FLATTEN: "discard",
    POLICY_ADDRESS: "record",
}
POLICY_SPACE_IS_EXHAUSTIVE_BECAUSE = (
    "an admission meeting an item that is a whole either does not act on it "
    "(refuse), acts on the whole without its interior (opaque), acts on the "
    "interior without the boundary between (discard), or acts on the interior "
    "keeping that boundary (record).  Those four exhaust the declared "
    "alternatives; what the space does NOT enumerate is a policy that admits "
    "the inner whole AND its items as separate marks, one that admits the "
    "inner boundary as a datum of its own, one that reads an item under a "
    "different convention at each level, or one that groups marks by anything "
    "but the crossing.  Every minimality statement of this rung is scoped to "
    "the declared four"
)

CAP_AS_MARK = "admit_a_whole_as_a_mark"
CAP_REACH = "reach_inside_a_nested_whole"
CAP_RECORD = "record_the_crossing"
CAP_NAME_INNER = "the_reading_names_the_inner_sides"

CAPABILITY_OF: dict[str, str] = {
    CAP_AS_MARK: (
        "an admission event may name an item that is not a visible mark, and "
        "admit it as one mark on a side"
    ),
    CAP_REACH: (
        "an admission event may name a mark lying inside a nested whole, so "
        "that the interior of an item is reachable at all"
    ),
    CAP_RECORD: (
        "the state records, for each admitted mark, the finite sequence of "
        "sides crossed to reach it rather than one side, and the event grammar "
        "gains the admission that names such a sequence"
    ),
    CAP_NAME_INNER: (
        "the reading's naming of the two sides reaches the inner boundary, so "
        "that the exchange of an inner boundary's two sides is not a renaming "
        "the object language can miss"
    ),
}
POLICY_CAPABILITIES: dict[str, tuple[str, ...]] = {
    POLICY_REFUSE: (),
    POLICY_OPAQUE: (CAP_AS_MARK,),
    POLICY_FLATTEN: (CAP_REACH,),
    POLICY_ADDRESS: (CAP_REACH, CAP_RECORD),
}

COORDINATES: tuple[str, str] = ("nesting_policy", "naming_reaches_inward")

MU1 = "capability count: the number of undeclared capabilities the candidate uses"
MU2 = (
    "collateral count: how many of the eight declared facts the candidate makes "
    "internally available that the same reading's base did not.  They are not "
    "eight facts about one retained configuration: FOUR are about the caller's "
    "retained whole and are reported FALSE where there is no retained "
    "configuration rather than vacuously true, the base being the refusing "
    "policy, which retains nothing; TWO are censuses of the policy's behaviour "
    "over the declared domain; ONE is about the closed observation grammar; and "
    "ONE is about the reading.  The eight are facts and not independent facts: "
    "the receipt computes which pairs of them take the same value at every "
    "point of this rung's space and names them, so that a reader knows where "
    "this measure counts one thing twice"
)

ONE_STEP_RULE = (
    "a candidate is one step exactly when the number of undeclared "
    "capabilities it uses is one.  At Challenge 4 that number was also the "
    "number of coordinates moved; here it is not, the policy coordinate having "
    "a value that uses two capabilities, and the run keeps the capability "
    "reading because the seed requires a candidate called one step not to "
    "bundle capabilities"
)

# The eight declared collateral facts, in the declared order of definition 70:
# four about the caller's retained whole (the first, the fourth, the fifth, and
# the seventh), two censuses of the policy's behaviour over the declared domain
# (the second and the third), one about the closed observation grammar (the
# sixth), and one about the reading (the eighth).  The second measure counts
# how many of them a candidate makes available that its reading's base did not.
COLLATERAL_FACTS: tuple[str, ...] = (
    "nesting_internally_visible",
    "depth_determined_by_the_key",
    "depth_takes_more_than_one_value_over_the_domain",
    "inner_side_internally_available",
    "outer_side_internally_available",
    "depth_expressible_in_the_closed_grammar",
    "inner_whole_presentation_admitted",
    "side_names_hold",
)

SCORED_PREDICTIONS: tuple[str, ...] = (
    "C5-1", "C5-2", "C5-3", "C5-4", "C5-5", "C5-6", "C5-7", "C5-8",
)
# The scored predictions whose every hitting clause, read literally, is fixed
# by a declaration of this run: the two readers' declared bounds replayed on
# the caller's text, and the declared policy space with its declared
# capability names and counts.  A HIT on one of them is HIT by construction
# and is not counted as content; a miss on one is a miss like any other.  The
# criterion is the one Challenge 1 declared.
DEFINITION_LEVEL_PREDICTIONS: tuple[str, ...] = ("C5-1", "C5-2")
TALLY_CRITERION = challenge1.TALLY_CRITERION

CAPABILITIES: dict[str, dict[str, str]] = {
    "admitted boundary": {
        "declared_at": "the seed, as the one admitted primitive exception",
        "paid_by": "the seed",
        "buys_at_challenge_5": (
            "that an item lies on a side at all, and therefore that a nested "
            "item lies on a side of a side; every policy but the refusing one "
            "is formulable only under it, and so is the whole notion of a "
            "crossing"
        ),
    },
    "side names under O": {
        "declared_at": "genesis, as the O reading of the one declaration",
        "paid_by": "the declared reading",
        "buys_at_challenge_5": (
            "which side of the OUTER boundary the retained mark lies on, at "
            "every policy that admits it.  It buys nothing about the inner "
            "boundary: whether the naming reaches inward is a further "
            "declaration, and without it the inner side is not internally "
            "available under O either"
        ),
    },
    "occurrence identity": {
        "declared_at": "Challenge 2, as that rung's one new declaration",
        "paid_by": "the run",
        "buys_at_challenge_5": (
            "that a presented item becomes a fresh admitted mark whatever "
            "labels are already present, which every admitting policy uses"
        ),
    },
    "presentation convention": {
        "declared_at": "Challenge 1, as metatheory",
        "paid_by": "the run",
        "buys_at_challenge_5": (
            "which presented side becomes which admitted side, now applied at "
            "every level; the run declares one convention for all levels and "
            "does not enumerate a policy that reads a different one inside"
        ),
    },
    "the widened reader bound": {
        "declared_at": "Challenge 4, as that rung's declaration",
        "paid_by": "the run",
        "buys_at_challenge_5": (
            "nothing here: the Challenge 4 reader refuses the caller's "
            "inscription by name, exactly as the Challenge 1 reader does"
        ),
    },
    "the nested reader bound": {
        "declared_at": "Challenge 5, as this rung's declaration",
        "paid_by": "the run",
        "buys_at_challenge_5": (
            "that the caller's inscription can be read at all, and a finite "
            "domain of inscriptions to enumerate; it decides nothing about "
            "what an admission does with what it reads"
        ),
    },
}

BOUNDARY_DEPENDENCE: dict[str, str] = {
    "the identity of the policy space, the capability counts, the one-step "
    "rule, and the refusal of bundles": (
        "does not depend on the admitted boundary"
    ),
    "the notion of depth, the address, the crossing, and every level exchange": (
        "require the admitted boundary: a crossing is a crossing OF a boundary, "
        "and an address is a sequence of its sides.  Nothing in this rung's "
        "state is formulated after removing it"
    ),
    "the invisibility of the nesting at every one-step policy": (
        "requires the admitted boundary, being a statement about which side a "
        "mark lies on after the inner boundary is discarded or absorbed"
    ),
    "the reader's depth bound and the domain of inscriptions": (
        "require the admitted boundary in the weak sense that a whole is "
        "delimited by one bar with a side on each hand; how many items a side "
        "may carry and how deep the reader goes are declarations the boundary "
        "does not decide"
    ),
    "the two senses of an available depth, and their parting": (
        "does not depend on the admitted boundary: one is a statement about "
        "renamings and a key, the other about the forms of the closed "
        "observation grammar, and both would be stated the same way for any "
        "state carrying a sequence"
    ),
    "the outside of the outermost boundary": (
        "requires the admitted boundary to be formulated at all, and the run "
        "formulates no address value for it; that is recorded OPEN"
    ),
}


# ---------------------------------------------------------------------------
# Points of the declared space
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Point:
    """One declared candidate: a nesting policy and the naming coordinate.

    A deterministic value object.  It applies nothing: a candidate becomes a
    retained state only through replay of an explicit history, and a renaming
    set only by being handed to the kernel's declared enumerations.
    """

    policy: str = POLICY_REFUSE
    naming_reaches_inward: bool = False

    def values(self) -> tuple[object, ...]:
        return (POLICY_NAMES[self.policy], self.naming_reaches_inward)


BASE_POINT = Point()


def point_space() -> list[Point]:
    """Every point of the declared space, in a deterministic order."""
    return [
        Point(policy, naming)
        for policy in POLICY_SPACE
        for naming in (False, True)
    ]


def changed_coordinates(point: Point) -> list[str]:
    """The coordinates the candidate moves off their inherited values."""
    moved: list[str] = []
    if point.policy != POLICY_REFUSE:
        moved.append("nesting_policy")
    if point.naming_reaches_inward:
        moved.append("naming_reaches_inward")
    return moved


def capabilities(point: Point) -> list[str]:
    """The undeclared capabilities the candidate uses."""
    used = list(POLICY_CAPABILITIES[point.policy])
    if point.naming_reaches_inward:
        used.append(CAP_NAME_INNER)
    return used


def mu1(point: Point) -> int:
    """The first declared cost measure: the capability count."""
    return len(capabilities(point))


def is_one_step(point: Point) -> bool:
    """Whether the candidate uses exactly one undeclared capability."""
    return mu1(point) == 1


def bundles(point: Point) -> bool:
    """Whether the candidate bundles capabilities and is refused as one step."""
    return mu1(point) >= 2


def point_name(point: Point) -> str:
    """A deterministic name for a point of the space."""
    parts = [POLICY_NAMES[point.policy]]
    if point.naming_reaches_inward:
        parts.append("naming_reaches_inward")
    return "+".join(parts)


def policy_count(policy: str) -> int:
    """The capability count of a policy alone, with the naming coordinate off."""
    return len(POLICY_CAPABILITIES[policy])


def policy_is_one_step(policy: str) -> bool:
    return policy_count(policy) == 1


# ---------------------------------------------------------------------------
# What a candidate declares: the levels, and the reachable ones
# ---------------------------------------------------------------------------


def named_levels(reading: str, point: Point) -> tuple[int, ...]:
    """The boundary levels whose two sides carry admitted names.

    Reading U names no side at any level, so the naming coordinate has nothing
    to reach inward with and names nothing however it is set; reading O names
    the outermost, and the coordinate decides whether that naming reaches the
    inner boundaries.  This is a declaration of the candidate, never a
    discovery.
    """
    if reading == READING_U:
        return ()
    return LEVELS if point.naming_reaches_inward else (0,)


def unnamed_levels(reading: str, point: Point) -> tuple[int, ...]:
    """The levels whose exchange is a renaming the object language cannot see."""
    named = set(named_levels(reading, point))
    return tuple(level for level in LEVELS if level not in named)


def reachable_levels(point: Point) -> tuple[int, ...]:
    """The levels a policy's admitted addresses can reach.

    A policy that does not record the crossing places every mark at an address
    of length one, so only the outermost boundary is ever crossed by anything
    the state carries; the refusing policy reaches none, admitting nothing.
    """
    if point.policy == POLICY_REFUSE:
        return ()
    if point.policy == POLICY_ADDRESS:
        return LEVELS
    return (0,)


def effective_unnamed_levels(reading: str, point: Point) -> tuple[int, ...]:
    """The exchanges that actually act on what this candidate can hold.

    Two points that declare the same acting exchanges and the same key are the
    same structure however their raw coordinates read, which is why the naming
    coordinate collapses under U and at every policy that reaches only the
    outermost boundary.
    """
    reach = set(reachable_levels(point))
    return tuple(level for level in unnamed_levels(reading, point) if level in reach)


def effective_structure(reading: str, point: Point) -> tuple[object, ...]:
    """What the candidate actually declares once the reading is applied."""
    return (
        "records the crossing" if point.policy == POLICY_ADDRESS else "one side per mark",
        point.policy != POLICY_REFUSE,
        effective_unnamed_levels(reading, point),
    )


# ---------------------------------------------------------------------------
# The caller's history under a policy
# ---------------------------------------------------------------------------


class PolicyRefusal(ValueError):
    """The declared policy refuses to admit an item that is a whole."""


def side_items(whole: NestedWhole, order: str) -> list[tuple[Item | None, str]]:
    """The two sides' items in the declared within-whole order, with the side."""
    if order not in WITHIN_WHOLE_ORDERS:
        raise PresentationError(f"unknown within-whole order: {order!r}")
    return [
        (whole.left if presented == "left" else whole.right, presented)
        for presented in WITHIN_WHOLE_ORDERS[order]
    ]


def placements(
    whole: NestedWhole,
    policy: str,
    convention: str = DECLARED_CONVENTION,
    order: str = DECLARED_WITHIN_WHOLE_ORDER,
    prefix: Address = (),
) -> list[tuple[str, Address]]:
    """The ``(token, address)`` pairs a policy admits from a read whole.

    Under every policy but the recording one the returned addresses have length
    one, so the admitted state is a ``Regime``; under the recording policy the
    address is the sequence of sides crossed.  The refusing policy raises where
    an item is a whole, which is the refusal itself and not an error of the
    reader.
    """
    if policy not in POLICY_SPACE:
        raise PolicyRefusal(f"unknown nesting policy: {policy!r}")
    out: list[tuple[str, Address]] = []
    for item, presented in side_items(whole, order):
        if item is None:
            continue
        address = (*prefix, admitted_side(presented, convention))
        if isinstance(item, str):
            out.append((item, address))
            continue
        if policy == POLICY_REFUSE:
            raise PolicyRefusal(
                f"the declared policy refuses an item that is a whole: "
                f"{render_whole(item)!r}"
            )
        if policy == POLICY_OPAQUE:
            out.append((WHOLE_TOKEN, address))
            continue
        inner = placements(item, policy, convention, order, address)
        if policy == POLICY_ADDRESS:
            out.extend(inner)
        else:
            out.extend((token, address) for token, _deeper in inner)
    return out


def policy_history(
    whole: NestedWhole,
    policy: str,
    convention: str = DECLARED_CONVENTION,
    order: str = DECLARED_WITHIN_WHOLE_ORDER,
) -> list[DeepEvent]:
    """The caller's history under a policy: every supply first, in the declared
    order, then every admission in that order.

    The events are rendered in the deep grammar throughout, so that one replay
    serves every policy; a policy that does not record the crossing yields
    addresses of length one, and ``flat_history`` renders the same history in
    the inherited grammar for the cross-check.
    """
    pairs = placements(whole, policy, convention, order)
    history: list[DeepEvent] = [Supply(token) for token, _address in pairs]
    history.extend(AdmitAt(token, address) for token, address in pairs)
    return history


def flat_history(
    whole: NestedWhole,
    policy: str,
    convention: str = DECLARED_CONVENTION,
    order: str = DECLARED_WITHIN_WHOLE_ORDER,
) -> list[Event]:
    """The same history in the INHERITED grammar, available only where every
    address has length one.

    A policy that records the crossing has no such rendering, and asking for
    one is refused by name rather than silently truncated.
    """
    pairs = placements(whole, policy, convention, order)
    if any(len(address) != 1 for _token, address in pairs):
        raise PolicyRefusal(
            "a policy that records the crossing has no history in the "
            "inherited grammar; the crossing would be discarded silently"
        )
    history: list[Event] = [Supply(token) for token, _address in pairs]
    history.extend(AdmitOccurrence(token, address[0]) for token, address in pairs)
    return history


@dataclass(frozen=True)
class Retention:
    """What one policy retains from one inscription, or the refusal."""

    inscription: str
    policy: str
    history: list[DeepEvent] | None
    deep: DeepRegime | None
    regime: Regime | None
    refusal: str | None


def retain(reading: str, whole: NestedWhole, policy: str, text: str) -> Retention:
    """Replay the caller's history under a policy, or record the refusal."""
    try:
        history = policy_history(whole, policy)
    except PolicyRefusal as exc:
        return Retention(text, policy, None, None, None, str(exc))
    deep = deep_replay(history, deep_genesis(reading))
    regime = flatten_deep(deep)
    return Retention(text, policy, history, deep, regime, None)


# ---------------------------------------------------------------------------
# The declared domain of inscriptions
# ---------------------------------------------------------------------------


@cache
def domain_items(depth_left: int) -> list[Item]:
    """Every item within the declared depth allowance, deterministically."""
    out: list[Item] = list(ALPHABET)
    if depth_left >= 1:
        out.extend(domain_wholes(depth_left))
    return out


@cache
def domain_wholes(depth_left: int) -> list[NestedWhole]:
    """Every whole whose items lie within the declared depth allowance."""
    inner: list[Item | None] = [None, *domain_items(depth_left - 1)]
    return [NestedWhole(left, right) for left in inner for right in inner]


@cache
def domain() -> list[NestedWhole]:
    """The declared finite domain: every whole the reader accepts at the bound.

    Two policies are the same policy exactly when they retain isomorphic states
    at every member of this domain.  The domain is a declaration; a wider
    alphabet or a deeper bound is available and is not enumerated.
    """
    return domain_wholes(NESTING_BOUND)


@cache
def domain_texts() -> list[str]:
    return [render_whole(whole) for whole in domain()]


# ---------------------------------------------------------------------------
# The class key: a policy's behaviour over the whole domain
# ---------------------------------------------------------------------------


@cache
def retained_key(reading: str, point: Point, whole: NestedWhole) -> object:
    """The canonical key of what a point retains from one inscription.

    ``"refused"`` where the policy refuses, so that a refusal is a value of the
    key and not a gap in it.
    """
    try:
        history = policy_history(whole, point.policy)
    except PolicyRefusal:
        return "refused"
    deep = deep_replay(history, deep_genesis(reading))
    return repr(deep_canonical(deep, effective_unnamed_levels(reading, point)))


@cache
def domain_behaviour(reading: str, point: Point) -> list[object]:
    """The point's canonical key at every inscription of the declared domain."""
    return [retained_key(reading, point, whole) for whole in domain()]


def behaviour_digest(behaviour: Sequence[object]) -> str:
    """A deterministic digest of a point's behaviour over the whole domain.

    The digest is a naming device for the class key and is never evidence:
    every inscription at which two points differ is enumerated and named
    beside it.
    """
    payload = "\n".join(repr(entry) for entry in behaviour)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def class_key(reading: str, point: Point, digest: str) -> list[object]:
    """The implemented quotient: the structure the candidate declares, with the
    digest of its behaviour over the whole declared domain.

    Over the domain and not at the caller's one inscription: the two one-step
    policies retain isomorphic states there, so a key read at that inscription
    alone would report ONE class where the enumeration finds two, and the tie
    the seed requires to be retained would be understated.
    """
    return [*[str(part) for part in effective_structure(reading, point)], digest]


def differing_inscriptions(
    reading: str, a: Point, b: Point, limit: int = 4
) -> list[str]:
    """The first inscriptions of the domain at which two points differ."""
    left = domain_behaviour(reading, a)
    right = domain_behaviour(reading, b)
    out = [
        text
        for text, x, y in zip(domain_texts(), left, right)
        if x != y
    ]
    return out[:limit]


# ---------------------------------------------------------------------------
# Depth, the closed grammar, and the collateral facts
# ---------------------------------------------------------------------------


@cache
def depths_over_the_domain(reading: str, point: Point) -> list[int]:
    """Every depth any mark of any retained state of the domain carries."""
    seen: set[int] = set()
    for whole in domain():
        try:
            history = policy_history(whole, point.policy)
        except PolicyRefusal:
            continue
        deep = deep_replay(history, deep_genesis(reading))
        seen.update(depth_of(deep, i) for i in range(deep.n_marks()))
    return sorted(seen)


def signatures_agree(pairs: Sequence[tuple[object, tuple[int, ...]]]) -> bool:
    """Whether every two entries with the same key carry the same signature.

    Separated from its caller so that the direction that returns FALSE is
    exercised by a test: over the real policies no two inscriptions with equal
    keys carry different depths, so a check written inline could only ever read
    one way.  An empty list reports FALSE: there is nothing of which the fact
    could hold, and absence of a test is not the fact holding.
    """
    seen: dict[object, tuple[int, ...]] = {}
    for key, signature in pairs:
        if key in seen:
            if seen[key] != signature:
                return False
        else:
            seen[key] = signature
    return bool(pairs)


@cache
def depth_signatures(reading: str, point: Point) -> list[tuple[object, tuple[int, ...]]]:
    """Each retained state of the domain, as its key with its sorted depths."""
    out: list[tuple[object, tuple[int, ...]]] = []
    for whole in domain():
        try:
            history = policy_history(whole, point.policy)
        except PolicyRefusal:
            continue
        deep = deep_replay(history, deep_genesis(reading))
        out.append(
            (
                retained_key(reading, point, whole),
                tuple(sorted(depth_of(deep, i) for i in range(deep.n_marks()))),
            )
        )
    return out


def depth_determined_by_the_key(reading: str, point: Point) -> bool:
    """Whether two inscriptions with equal keys give equal depth signatures.

    The generalization to depth of definition 29's token-forgetting clause: a
    fact the key does not carry is not internally available, whatever else is
    true of it.  A point that retains nothing over the whole domain reports
    FALSE, because there is no retained configuration of which the fact could
    hold.
    """
    return signatures_agree(depth_signatures(reading, point))


def closed_grammar_forms_reading_depth() -> list[str]:
    """The judgment forms of the closed observation grammar whose value can
    depend on a mark's depth.

    The grammar is ``OnSide`` and ``SideNamed`` and neither carries a sequence
    or a count: ``OnSide`` names one mark and one side, ``SideNamed`` names one
    side and one name.  The census is over the vocabulary the Challenge 0
    receipt derives from the sum type, so a form added later would appear here
    rather than being asserted absent.
    """
    return [name for name in observation_vocabulary() if name not in ("OnSide", "SideNamed")]


def collateral_facts(
    reading: str, point: Point, retention: Retention
) -> dict[str, bool]:
    """The eight declared facts, computed under the candidate's own renamings.

    A fact about a retained configuration is FALSE where the policy retains
    nothing: the absence of a test is not turned into the fact holding.
    """
    admits = retention.deep is not None
    levels = effective_unnamed_levels(reading, point)
    orbit: frozenset[Address] = frozenset()
    if retention.deep is not None and retention.deep.n_marks() > 0:
        orbit = deep_mark_orbit(retention.deep, 0, levels)
    flat = retain(reading, read_nested_whole(FLAT_INSCRIPTION), point.policy, FLAT_INSCRIPTION)
    visible = (
        admits
        and flat.deep is not None
        and retention.deep is not None
        and not deep_is_isomorphic(retention.deep, flat.deep, levels)
    )
    return {
        "nesting_internally_visible": visible,
        "depth_determined_by_the_key": depth_determined_by_the_key(reading, point),
        "depth_takes_more_than_one_value_over_the_domain": (
            len(depths_over_the_domain(reading, point)) > 1
        ),
        "inner_side_internally_available": bool(orbit)
        and all(len(address) > 1 for address in orbit)
        and len({address[1] for address in orbit}) == 1,
        "outer_side_internally_available": bool(orbit)
        and len({address[0] for address in orbit}) == 1,
        "depth_expressible_in_the_closed_grammar": admits
        and bool(closed_grammar_forms_reading_depth()),
        "inner_whole_presentation_admitted": admits
        and retention.deep is not None
        and WHOLE_TOKEN in retention.deep.marks,
        "side_names_hold": reading == READING_O,
    }


def mu2(facts: dict[str, bool], base_facts: dict[str, bool]) -> int:
    """The second declared cost measure: newly available collateral facts."""
    return sum(1 for name in COLLATERAL_FACTS if facts[name] and not base_facts[name])


def holding(facts: dict[str, bool]) -> list[str]:
    """The declared collateral facts that hold, in the declared order."""
    return [name for name in COLLATERAL_FACTS if facts[name]]


def facts_agreeing_everywhere(rows: list[Json]) -> list[list[str]]:
    """Pairs of declared facts taking the same value at every point.

    The second measure counts facts and not independent facts.  Challenge 4's
    review found two clause statuses equal by construction and counted twice;
    rather than repeat that silently, this rung computes which pairs agree
    everywhere in its own space and names them.
    """
    values = {
        name: [name in row["collateral_facts_holding"] for row in rows]
        for name in COLLATERAL_FACTS
    }
    return [
        [a, b]
        for a, b in combinations(COLLATERAL_FACTS, 2)
        if values[a] == values[b]
    ]


# ---------------------------------------------------------------------------
# Treating the inner whole as the outer whole was treated
# ---------------------------------------------------------------------------


def deepest_place_a_policy_names(reading: str, point: Point) -> int:
    """The deepest place the policy's own admissions name over the domain.

    A census and not a declaration: every member of the declared domain is
    replayed under the policy and the longest address its admissions produce is
    read off.  It is one at the refusing policy, which admits every member
    carrying no nested item, and zero only where the policy admits no member at
    all.  The probe below reads this number rather than the policy's name, so
    that what refuses a deeper admission is what the policy's own admissions
    do.
    """
    depths = depths_over_the_domain(reading, point)
    return max(depths) if depths else 0


def a_place_of_that_depth_is_nameable(requested: int, deepest_named: int) -> bool:
    """Whether a policy naming places to ``deepest_named`` names one at
    ``requested``.

    Separated from its caller so that both directions are exercised by a test:
    over the real policies the deepest place a one-step policy names is one, so
    a comparison written inline could only ever read one way at those points.
    A request at depth zero is no request and reads FALSE.
    """
    return 1 <= requested <= deepest_named


def further_mark_within_the_inner_whole(
    reading: str, point: Point, retention: Retention
) -> Json:
    """Whether a further mark may be admitted INSIDE the caller's inner whole.

    That is the mechanical reading of "treating the inner whole as the outer
    whole was treated": the outer whole's two sides are places at which a mark
    may be admitted, and this asks whether the inner whole's are.  The probe
    extends the caller's own history with one admission at the inner boundary's
    other side and reads two things: that the replay records the mark at the
    requested address, which holds at every admitting point and is reported so
    that it can be read, and that the address is no deeper than the deepest
    place this policy's OWN admissions name over the declared domain.  The
    second is what decides it, and it is a census — the deep grammar is
    policy-agnostic and accepts the event under every policy, so the address it
    records is not by itself evidence that the policy could have produced it.
    It is a probe and is admitted by no history the receipt reports as current.
    """
    if retention.history is None or retention.deep is None:
        return {
            "possible": False,
            "because": (
                "the policy refuses the caller's inscription and retains "
                "nothing, so there is no inner whole to enter"
            ),
            "probe": None,
            "address": None,
            "recorded_at_the_requested_place": False,
            "deepest_place_the_policy_names": deepest_place_a_policy_names(reading, point),
        }
    requested: Address = (0, 1)
    probe: list[DeepEvent] = [*retention.history, Supply("b"), AdmitAt("b", requested)]
    try:
        after = deep_replay(probe, deep_genesis(reading))
    except AdmissionError as exc:  # pragma: no cover - the grammar accepts it
        return {
            "possible": False,
            "because": str(exc),
            "probe": deep_history_json(probe),
            "address": None,
            "recorded_at_the_requested_place": False,
            "deepest_place_the_policy_names": deepest_place_a_policy_names(reading, point),
        }
    recorded = after.addresses[-1]
    kept = tuple(recorded) == requested
    deepest = deepest_place_a_policy_names(reading, point)
    nameable = a_place_of_that_depth_is_nameable(len(requested), deepest)
    return {
        "possible": kept and nameable,
        "because": (
            f"the policy's own admissions name places to depth {deepest} over "
            "the declared domain, so the admission names a place inside the "
            "inner whole and the replay keeps the mark there"
            if nameable
            else "the policy's own admissions name no place deeper than "
            f"{deepest} over the declared domain, so the length-{len(requested)} "
            "address the policy-agnostic deep grammar records here is not one "
            "this policy produces: a place inside the inner whole is not "
            "nameable under it"
        ),
        "probe": deep_history_json(probe),
        "address": list(recorded),
        "recorded_at_the_requested_place": kept,
        "deepest_place_the_policy_names": deepest,
    }


WHAT_THE_INNER_WHOLE_IS: dict[str, str] = {
    POLICY_REFUSE: "not admissible: no admission names it",
    POLICY_OPAQUE: "a MARK: it is admitted as one mark on the outer side",
    POLICY_FLATTEN: (
        "NOTHING: it is not admitted at all, and only the items it carries are"
    ),
    POLICY_ADDRESS: (
        "a second BOUNDARY: a new definition, whose two sides are places at "
        "which a mark may be admitted"
    ),
}


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def deep_event_json(e: DeepEvent) -> dict[str, object]:
    """Render any event of the Challenge 5 grammar."""
    if isinstance(e, Supply):
        return {"kind": "Supply", "token": e.token}
    return {"kind": "AdmitAt", "token": e.token, "address": list(e.address)}


def deep_history_json(history: Sequence[DeepEvent]) -> list[dict[str, object]]:
    return [deep_event_json(e) for e in history]


def deep_regime_json(r: DeepRegime | None) -> Json | None:
    if r is None:
        return None
    return {
        "reading": r.reading,
        "marks": list(r.marks),
        "addresses": [list(address) for address in r.addresses],
        "depths": [depth_of(r, i) for i in range(r.n_marks())],
    }


def probes(token: str) -> list[DeepEvent]:
    """Events offered to the empty deep event-follows relation; none applied."""
    return [Supply(token), AdmitAt(token, (0,)), AdmitAt(token, (0, 1))]


# ---------------------------------------------------------------------------
# One point, computed
# ---------------------------------------------------------------------------


def point_row(reading: str, point: Point, base_facts: dict[str, bool]) -> Json:
    """One point of the declared space: its cost under each measure, whether it
    is one step, whether it bundles, and whether it admits the caller's whole."""
    whole = read_nested_whole(INSCRIPTION)
    retention = retain(reading, whole, point.policy, INSCRIPTION)
    facts = collateral_facts(reading, point, retention)
    behaviour = domain_behaviour(reading, point)
    return {
        "name": point_name(point),
        "coordinates": dict(zip(COORDINATES, point.values())),
        "capability_coordinates": changed_coordinates(point),
        "capabilities": capabilities(point),
        "mu1": mu1(point),
        "mu2": mu2(facts, base_facts),
        "one_step": is_one_step(point),
        "bundles": bundles(point),
        "admits": retention.deep is not None,
        "refusal": retention.refusal,
        "effective_unnamed_levels": list(effective_unnamed_levels(reading, point)),
        "class_key": class_key(reading, point, behaviour_digest(behaviour)),
        "collateral_facts_holding": holding(facts),
    }


def point_detail(reading: str, point: Point, base_facts: dict[str, bool]) -> Json:
    """The full report for one point: its history, its retained state, its
    automorphisms, the mark's address orbit, and the declared facts."""
    whole = read_nested_whole(INSCRIPTION)
    retention = retain(reading, whole, point.policy, INSCRIPTION)
    flat = retain(reading, read_nested_whole(FLAT_INSCRIPTION), point.policy, FLAT_INSCRIPTION)
    levels = effective_unnamed_levels(reading, point)
    g = deep_genesis(reading)
    row = point_row(reading, point, base_facts)
    autos = (
        deep_automorphisms(retention.deep, levels) if retention.deep is not None else []
    )
    orbit = (
        sorted(deep_mark_orbit(retention.deep, 0, levels))
        if retention.deep is not None and retention.deep.n_marks() > 0
        else []
    )
    inherited: Json = {
        "available": False,
        "because": (
            "the policy admits nothing"
            if retention.deep is None
            else "the policy records the crossing, which the inherited grammar "
            "cannot carry"
        ),
    }
    if retention.deep is not None and point.policy != POLICY_ADDRESS:
        history = flat_history(whole, point.policy)
        regime = replay(history, genesis(reading))
        flat_regime = (
            replay(flat_history(read_nested_whole(FLAT_INSCRIPTION), point.policy), genesis(reading))
        )
        inherited = {
            "available": True,
            "history": challenge2.history_json(history),
            "certified": certify(history, genesis(reading), regime),
            "marks": list(regime.marks),
            "placement": list(regime.placement),
            "flat_inscription_regime_equal": regime == flat_regime,
            "flat_inscription_regime_isomorphic": is_isomorphic(regime, flat_regime),
            "agrees_with_the_deep_replay": regime == retention.regime,
        }
    row.update(
        {
            "what_the_inner_whole_is": WHAT_THE_INNER_WHOLE_IS[point.policy],
            "named_levels": list(named_levels(reading, point)),
            "unnamed_levels": list(unnamed_levels(reading, point)),
            "reachable_levels": list(reachable_levels(point)),
            "effective_structure": [str(part) for part in effective_structure(reading, point)],
            "history": deep_history_json(retention.history or []),
            "retained": deep_regime_json(retention.deep),
            "certified": retention.deep is not None
            and deep_certify(retention.history or [], g, retention.deep),
            "replays_from_genesis": retention.deep is not None
            and deep_replay(retention.history or [], g) == retention.deep,
            "marks": retention.deep.n_marks() if retention.deep is not None else 0,
            "automorphism_count": len(autos),
            "permitted_images": (
                len(model.deep_permitted_images(retention.deep, levels))
                if retention.deep is not None
                else 0
            ),
            "mark_address_orbit": [list(address) for address in orbit],
            "mark_address_orbit_size": len(orbit),
            "flat_inscription_retained": deep_regime_json(flat.deep),
            "flat_inscription_isomorphic": (
                retention.deep is not None
                and flat.deep is not None
                and deep_is_isomorphic(retention.deep, flat.deep, levels)
            ),
            "flat_inscription_equal": retention.deep is not None
            and flat.deep is not None
            and retention.deep == flat.deep,
            "inherited_grammar": inherited,
            "collateral_facts": collateral_facts(reading, point, retention),
            "further_mark_within_the_inner_whole": further_mark_within_the_inner_whole(
                reading, point, retention
            ),
            "domain_behaviour_digest": behaviour_digest(domain_behaviour(reading, point)),
            "depths_over_the_domain": depths_over_the_domain(reading, point),
            "least_key": key_json(
                tuple(deep_canonical(retention.deep, levels))
                if retention.deep is not None
                else ("refused",)
            ),
            "event_follows_relation_empty": all(
                not deep_event_follows(retention.deep or g, e) for e in probes(CALLER_TOKEN)
            ),
            "inherited_event_follows_relation_empty": all(
                not event_follows(genesis(reading), e)
                for e in challenge1.probes(CALLER_TOKEN)
            ),
            "initial_datum_unchanged": (retention.deep or g).initial_datum == g.initial_datum,
            "reading_unchanged": (retention.deep or g).reading == reading,
        }
    )
    return row


# ---------------------------------------------------------------------------
# The reader, the order, and the price
# ---------------------------------------------------------------------------


def reader_facts() -> Json:
    """What the two inherited readers do with the caller's inscription, and
    what the widened reader reads."""
    refusals: list[Json] = []
    for name, reader in (("challenge_1_reader", read_whole), ("challenge_4_reader", read_pair_whole)):
        try:
            reader(INSCRIPTION)
        except PresentationError as exc:
            refusals.append({"reader": name, "refused": True, "refusal": str(exc)})
        else:  # pragma: no cover - both readers refuse by construction
            refusals.append({"reader": name, "refused": False, "refusal": None})
    whole = read_nested_whole(INSCRIPTION)
    deeper: str | None = None
    try:
        read_nested_whole(DEEPER_INSCRIPTION)
    except PresentationError as exc:
        deeper = str(exc)
    return {
        "inherited_readers": refusals,
        "inherited_readers_refuse_both": all(bool(row["refused"]) for row in refusals),
        # The census of the run's reader bounds, read off the inherited list
        # plus this rung's own.  The first bound was DECLARED and not widened,
        # so the number of widenings is one fewer than the number of bounds.
        # DEFINITION-level; it is here because two frozen prediction files
        # assert an ordinal for the same event and the scorer reads this.
        "reader_bounds_declared": len(refusals) + 1,
        "widenings_of_the_reader_bound": len(refusals),
        "widened_bound": READER_WIDENING,
        "declared_depth_bound": NESTING_BOUND,
        "read": {
            "spelling_rebuilt": render_whole(whole),
            "depth": whole_depth(whole),
            "left_is_a_whole": isinstance(whole.left, NestedWhole),
            "right_is_empty": whole.right is None,
        },
        "beyond_the_bound_probe": DEEPER_INSCRIPTION,
        "beyond_the_bound_refused": deeper is not None,
        "beyond_the_bound_refusal": deeper,
        "declared_at_challenge_5": list(DECLARED_AT_CHALLENGE_5),
        "paid_by": "the run",
        "whole_token": WHOLE_TOKEN,
        "order_declaration": NESTED_ORDER_DECLARATION,
    }


def order_facts(reading: str) -> Json:
    """Whether the other within-whole order is internally available.

    At the caller's inscription it cannot be: one mark is admitted and there is
    no order to see.  Over the declared domain the run counts the inscriptions
    at which the other order gives a state the permitted renamings do not
    reach, under the recording policy, and reports the number rather than
    asserting the order invisible.
    """
    point = Point(POLICY_ADDRESS)
    levels = effective_unnamed_levels(reading, point)
    differing: list[str] = []
    unequal: list[str] = []
    for whole in domain():
        declared = deep_replay(
            policy_history(whole, POLICY_ADDRESS), deep_genesis(reading)
        )
        other = deep_replay(
            policy_history(whole, POLICY_ADDRESS, DECLARED_CONVENTION, OTHER_WITHIN_WHOLE_ORDER),
            deep_genesis(reading),
        )
        if declared != other:
            unequal.append(render_whole(whole))
        if not deep_is_isomorphic(declared, other, levels):  # pragma: no cover
            differing.append(render_whole(whole))
    caller = read_nested_whole(INSCRIPTION)
    caller_declared = deep_replay(policy_history(caller, POLICY_ADDRESS), deep_genesis(reading))
    caller_other = deep_replay(
        policy_history(caller, POLICY_ADDRESS, DECLARED_CONVENTION, OTHER_WITHIN_WHOLE_ORDER),
        deep_genesis(reading),
    )
    return {
        "declared_order": DECLARED_WITHIN_WHOLE_ORDER,
        "other_order": OTHER_WITHIN_WHOLE_ORDER,
        "at_the_caller_inscription_isomorphic": deep_is_isomorphic(
            caller_declared, caller_other, levels
        ),
        "domain_size": len(domain()),
        "domain_inscriptions_where_the_states_differ": len(unequal),
        "first_such_inscriptions": unequal[:4],
        "domain_inscriptions_where_the_orders_part_up_to_renaming": len(differing),
        "part_up_to_renaming_is_definition_level_because": (
            "the two orders admit the same marks at the same addresses and "
            "differ only in the order of admission, which is a permutation of "
            "the internal identities; the mark permutations are permitted at "
            "every point of this rung's space, so the two states are always "
            "carried onto each other.  The census computes the number and is "
            "not evidence for it: the count is zero by unfolding definition 13, "
            "and only the STRUCTURAL difference above is a measurement"
        ),
        "note": (
            "the order is a declaration extended to every level at this rung; "
            "it is invisible at the caller's inscription, which admits one "
            "mark, and the two counts say how many members of the declared "
            "domain it moves structurally and how many up to renaming"
        ),
    }


PRICE_FIELDS_DECLARED: tuple[str, ...] = (
    "capabilities_the_retention_would_use",
    "capabilities_not_used",
    "declared_at",
    "paid_by",
    # Both are read off the DECLARED capability count of the recording policy
    # and move with no enumeration.  WHICH policy the caller's demand names is
    # computed, by the probe of `further_mark_within_the_inner_whole`; what
    # that policy costs is a declaration of definition 62.
    "what_the_caller_asked_for_costs",
    "what_the_caller_asked_for_is_one_step",
)


def price_facts(reading: str, by_mu1: Json, rows: list[Json]) -> Json:
    """What the caller's retention costs under this reading, and who pays it."""
    minimum = by_mu1["minimum"]
    paid = sorted(
        {
            capability
            for entry in by_mu1["classes"]
            for member in entry["members"]
            for capability in named(rows, str(member))["capabilities"]
        }
    )
    return {
        "retained_without_a_new_capability": bool(named(rows, "refuse")["admits"]),
        "capabilities_the_retention_would_use": [
            "admitted boundary",
            "occurrence identity",
            "the nested reader bound",
        ],
        "capabilities_not_used": (
            ["side names under O"] if reading == READING_O else []
        ),
        "declared_at": "Challenge 5, by whichever retained minimum is taken",
        "paid_by": "the run",
        "new_at_challenge_5": paid,
        "minimum_capability_count": minimum,
        "what_the_caller_asked_for_costs": policy_count(POLICY_ADDRESS),
        "what_the_caller_asked_for_is_one_step": policy_is_one_step(POLICY_ADDRESS),
        "declared_regardless_at_challenge_5": list(DECLARED_AT_CHALLENGE_5),
        "fields_declared_not_computed": list(PRICE_FIELDS_DECLARED),
    }


def named(rows: list[Json], name: str) -> Json:
    return next(row for row in rows if row["name"] == name)


# ---------------------------------------------------------------------------
# The reading facts
# ---------------------------------------------------------------------------


def policy_rows(reading: str) -> list[Json]:
    """One row per declared policy, with the naming coordinate off."""
    return [
        {
            "policy": POLICY_NAMES[policy],
            "declared": policy,
            "capabilities": list(POLICY_CAPABILITIES[policy]),
            "capability_count": policy_count(policy),
            "one_step": policy_is_one_step(policy),
            "bundles": policy_count(policy) >= 2,
            "what_the_inner_whole_is": WHAT_THE_INNER_WHOLE_IS[policy],
            "admits_the_caller_inscription": retain(
                reading, read_nested_whole(INSCRIPTION), policy, INSCRIPTION
            ).deep
            is not None,
        }
        for policy in POLICY_SPACE
    ]


def policy_separation(reading: str) -> Json:
    """Whether the two one-step policies are the same policy on the domain."""
    opaque = Point(POLICY_OPAQUE)
    flatten = Point(POLICY_FLATTEN)
    differing = differing_inscriptions(reading, opaque, flatten, limit=len(domain()))
    caller = INSCRIPTION in differing
    return {
        "domain_size": len(domain()),
        "same_policy_on_the_domain": not differing,
        "inscriptions_where_they_part": len(differing),
        "first_inscriptions_where_they_part": differing[:4],
        "part_at_the_caller_inscription": caller,
        "note": (
            "the two one-step policies agree up to isomorphism at the caller's "
            "own inscription and are two policies nonetheless; the class key is "
            "read over the whole declared domain for exactly that reason"
        ),
    }


def reading_facts(reading: str) -> Json:
    points = point_space()
    base_facts = collateral_facts(
        reading,
        BASE_POINT,
        retain(reading, read_nested_whole(INSCRIPTION), POLICY_REFUSE, INSCRIPTION),
    )
    rows = [point_row(reading, point, base_facts) for point in points]
    detail = [point_detail(reading, point, base_facts) for point in points]
    by_mu1 = one_step_minima(rows, "mu1", "admits")
    by_mu2 = one_step_minima(rows, "mu2", "admits")
    collapses = [
        [point_name(Point(policy)), point_name(Point(policy, True))]
        for policy in POLICY_SPACE
        if named(rows, point_name(Point(policy)))["class_key"]
        == named(rows, point_name(Point(policy, True)))["class_key"]
    ]
    return {
        "reading": reading,
        "levels": list(LEVELS),
        "policies": policy_rows(reading),
        "points": rows,
        "point_detail": detail,
        "space_size": len(rows),
        "one_step_points": [str(row["name"]) for row in rows if row["one_step"]],
        "admitting_points": [str(row["name"]) for row in rows if row["admits"]],
        "admitting_one_step_points": [
            str(row["name"]) for row in rows if row["admits"] and row["one_step"]
        ],
        "bundles_refused": [str(row["name"]) for row in rows if row["bundles"]],
        "bundles_refused_count": sum(1 for row in rows if row["bundles"]),
        "minima_by_mu1": by_mu1,
        "minima_by_mu2": by_mu2,
        "measures_agree_on_minima": by_mu1["points"] == by_mu2["points"],
        "measures_differ_somewhere": any(row["mu1"] != row["mu2"] for row in rows),
        "one_step_iff_capability_count_one": all(
            row["one_step"] == (row["mu1"] == 1) for row in rows
        ),
        "one_step_iff_one_coordinate_moved": all(
            row["one_step"] == (len(row["capability_coordinates"]) == 1) for row in rows
        ),
        "naming_coordinate_collapses_at": collapses,
        "naming_coordinate_collapses_everywhere": len(collapses) == len(POLICY_SPACE),
        "policy_separation": policy_separation(reading),
        "collateral_facts_agreeing_everywhere": facts_agreeing_everywhere(rows),
        "order": order_facts(reading),
        "price": price_facts(reading, by_mu1, rows),
    }


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def score_c4x(u: Json, o: Json, reader: Json) -> Json:
    """Score the Challenge 4 extrapolation against the Challenge 5 facts."""

    def verdict(hit: bool) -> str:
        return "HIT" if hit else "MISSED"

    reader_clause = bool(reader["inherited_readers_refuse_both"]) and reader[
        "paid_by"
    ] == "the run"
    # The frozen clause reads "the widened reader of this rung will refuse it
    # by name as well, its declared bound reading marks and not wholes", which
    # is the Challenge 4 reader; the Challenge 1 reader refusing it too is
    # reported beside it and is not what the clause names.
    challenge_4_reader = next(
        row for row in reader["inherited_readers"] if row["reader"] == "challenge_4_reader"
    )
    named_reader_clause = bool(challenge_4_reader["refused"])
    depth_clause = all(
        not named(rd["points"], "refuse")["admits"]
        and "depth_takes_more_than_one_value_over_the_domain"
        not in named(rd["points"], "opaque")["collateral_facts_holding"]
        and "depth_takes_more_than_one_value_over_the_domain"
        not in named(rd["points"], "discard")["collateral_facts_holding"]
        for rd in (u, o)
    )
    datum_clause = all(
        all(bool(row["initial_datum_unchanged"]) for row in rd["point_detail"])
        and all(
            row["retained"] is None or WHOLE_TOKEN not in row["retained"]["marks"]
            or row["what_the_inner_whole_is"] == WHAT_THE_INNER_WHOLE_IS[POLICY_OPAQUE]
            for row in rd["point_detail"]
        )
        for rd in (u, o)
    )
    space_clause = all(len(rd["policies"]) == len(POLICY_SPACE) for rd in (u, o))
    # "the bound will have to be widened a second time": the run has three
    # reader bounds and has widened twice, the first bound having been declared
    # and not widened.  The frozen ordinal is read against the reader census
    # rather than left unscored, because the same event is given a different
    # ordinal by the frozen C5-1.
    ordinal_clause = reader["widenings_of_the_reader_bound"] == 2
    # "exactly one member letting the caller retain the inscription": three of
    # the four policies admit it, and exactly one retains it so that the state
    # tells it from the flat inscription.  Both counts are reported.
    admitting = [
        row["policy"] for row in u["policies"] if row["admits_the_caller_inscription"]
    ]
    faithful = [
        str(row["name"])
        for row in u["points"]
        if "nesting_internally_visible" in row["collateral_facts_holding"]
    ]
    exactly_one_clause = len(admitting) == 1
    core = named_reader_clause and depth_clause and datum_clause and space_clause
    status = (
        "HIT"
        if (core and exactly_one_clause and reader_clause and ordinal_clause)
        else "PARTIAL"
        if core
        else "MISSED"
    )
    return {
        "status": status,
        "label": "NOT FORCED",
        "reader_refuses_clause_status": verdict(named_reader_clause),
        "widening_priced_clause_status": verdict(reader_clause),
        "widening_ordinal_clause_status": verdict(ordinal_clause),
        "reader_bounds_declared": reader["reader_bounds_declared"],
        "widenings_of_the_reader_bound": reader["widenings_of_the_reader_bound"],
        "depth_not_available_without_a_declaration_clause_status": verdict(depth_clause),
        "inner_whole_not_a_datum_clause_status": verdict(datum_clause),
        "declared_finite_policy_space_clause_status": verdict(space_clause),
        "exactly_one_member_retains_clause_status": verdict(exactly_one_clause),
        "policies_admitting_the_inscription": admitting,
        "points_where_the_nesting_is_internally_visible": faithful,
        "exactly_one_clause_fact": (
            "the frozen clause reads 'a declared finite space of policies with "
            "exactly one member letting the caller retain the inscription'.  "
            "THREE of the four declared policies admit the caller's "
            "inscription; exactly one retains it so that the retained state "
            "tells it from the flat inscription.  The clause is scored on the "
            "first count, which is what 'letting the caller retain the "
            "inscription' says, and the second is reported beside it"
        ),
        "evidence": (
            "both inherited readers refuse the caller's inscription by name and "
            "the new bound — the run's THIRD reader bound and its SECOND "
            "widening, which is the ordinal this clause asserts — is paid by "
            "the run; the decision takes the form of a declared finite policy "
            "space of four members; depth is available at no policy of "
            "capability count one; and the inner whole is a second initial "
            "datum under no policy"
        ),
    }


def score(u: Json, o: Json, reader: Json) -> Json:
    """Mechanical scoring of the frozen Challenge 5 predictions and of C4-X."""
    both = (u, o)

    def verdict(hit: bool) -> str:
        return "HIT" if hit else "MISSED"

    c5_1 = (
        bool(reader["inherited_readers_refuse_both"])
        and reader["paid_by"] == "the run"
        and bool(reader["beyond_the_bound_refused"])
        and reader["declared_depth_bound"] == NESTING_BOUND
        and bool(reader["read"]["left_is_a_whole"])
        and bool(reader["read"]["right_is_empty"])
        and reader["read"]["depth"] == 2
    )
    # The frozen C5-1 also says "the bound must be widened a third time", and
    # the frozen C4-X says "a second time" of the same event.  Both are scored
    # against the one reader census rather than one of them being left unread:
    # the run has three reader bounds and has widened twice, so C4-X's ordinal
    # holds and C5-1's does not.
    c5_1_ordinal = reader["widenings_of_the_reader_bound"] == 3
    c5_2 = (
        all(
            [row["capability_count"] for row in rd["policies"]] == [0, 1, 1, 2]
            and [row["one_step"] for row in rd["policies"]] == [False, True, True, False]
            and rd["one_step_iff_capability_count_one"]
            for rd in both
        )
        and len(POLICY_SPACE) == 4
        and len(POLICY_CAPABILITIES[POLICY_ADDRESS]) == 2
        and sorted({cap for caps in POLICY_CAPABILITIES.values() for cap in caps})
        == sorted([CAP_AS_MARK, CAP_REACH, CAP_RECORD])
    )
    c5_3 = all(
        all(
            named(rd["point_detail"], name)["marks"] == 1
            and named(rd["point_detail"], name)["retained"]["addresses"] == [[0]]
            and named(rd["point_detail"], name)["flat_inscription_isomorphic"]
            and named(rd["point_detail"], name)["inherited_grammar"][
                "flat_inscription_regime_isomorphic"
            ]
            and "nesting_internally_visible"
            not in named(rd["points"], name)["collateral_facts_holding"]
            for name in ("opaque", "discard")
        )
        for rd in both
    )
    c5_4 = all(
        not rd["policy_separation"]["same_policy_on_the_domain"]
        and rd["policy_separation"]["inscriptions_where_they_part"] > 0
        and not rd["policy_separation"]["part_at_the_caller_inscription"]
        and rd["minima_by_mu1"]["minimum"] == 1
        and rd["minima_by_mu1"]["class_count"] == 2
        and not rd["minima_by_mu1"]["unique"]
        and sorted(rd["minima_by_mu1"]["points"]) == ["discard", "opaque"]
        for rd in both
    )
    c5_5 = all(
        all(bool(row["initial_datum_unchanged"]) for row in rd["point_detail"])
        and named(rd["point_detail"], "opaque")["what_the_inner_whole_is"]
        == WHAT_THE_INNER_WHOLE_IS[POLICY_OPAQUE]
        and named(rd["point_detail"], "discard")["what_the_inner_whole_is"]
        == WHAT_THE_INNER_WHOLE_IS[POLICY_FLATTEN]
        and named(rd["point_detail"], "record")["what_the_inner_whole_is"]
        == WHAT_THE_INNER_WHOLE_IS[POLICY_ADDRESS]
        and [
            str(row["name"])
            for row in rd["point_detail"]
            if row["further_mark_within_the_inner_whole"]["possible"]
        ]
        == ["record", "record+naming_reaches_inward"]
        and all(
            not row["further_mark_within_the_inner_whole"]["possible"]
            for row in rd["point_detail"]
            if row["one_step"]
        )
        for rd in both
    )
    c5_6 = all(
        all(
            row["depths_over_the_domain"] == [1]
            for row in rd["point_detail"]
            if row["one_step"] and row["admits"]
        )
        and named(rd["point_detail"], "record")["depths_over_the_domain"] == [1, 2]
        and "depth_determined_by_the_key"
        in named(rd["points"], "record")["collateral_facts_holding"]
        and all(
            "depth_expressible_in_the_closed_grammar"
            not in row["collateral_facts_holding"]
            for row in rd["points"]
        )
        for rd in both
    ) and closed_grammar_forms_reading_depth() == []
    c5_7 = (
        u["naming_coordinate_collapses_everywhere"]
        and not o["naming_coordinate_collapses_everywhere"]
        and [pair[0] for pair in o["naming_coordinate_collapses_at"]]
        == ["refuse", "opaque", "discard"]
        and named(u["point_detail"], "record")["mark_address_orbit_size"] == 4
        and named(o["point_detail"], "record+naming_reaches_inward")[
            "mark_address_orbit_size"
        ] == 1
        and named(o["point_detail"], "record")["mark_address_orbit_size"] == 2
        and "inner_side_internally_available"
        not in named(o["points"], "record")["collateral_facts_holding"]
        and "inner_side_internally_available"
        in named(o["points"], "record+naming_reaches_inward")["collateral_facts_holding"]
    )
    c5_8 = all(
        all(
            bool(row["event_follows_relation_empty"])
            and bool(row["inherited_event_follows_relation_empty"])
            and bool(row["initial_datum_unchanged"])
            and bool(row["reading_unchanged"])
            and (bool(row["certified"]) and bool(row["replays_from_genesis"]))
            == bool(row["admits"])
            for row in rd["point_detail"]
        )
        for rd in both
    ) and WITHDRAWN_RULES_AT_CHALLENGE_5 == []
    return {
        "C4-X": score_c4x(u, o, reader),
        "C5-1": {
            "status": "HIT" if (c5_1 and c5_1_ordinal) else "PARTIAL" if c5_1 else "MISSED",
            "label": "FORCED",
            "readers_clause_status": verdict(c5_1),
            "widening_ordinal_clause_status": verdict(c5_1_ordinal),
            "reader_bounds_declared": reader["reader_bounds_declared"],
            "widenings_of_the_reader_bound": reader["widenings_of_the_reader_bound"],
            "widening_ordinal_clause_fact": (
                "the frozen clause gives this widening the ordinal THIRD; the "
                "frozen C4-X gives the same event the ordinal SECOND.  Both are "
                "scored against the one census beside this key — the reader "
                "bounds the run has declared, and the widenings, which are one "
                "fewer because the Challenge 1 bound was declared and not "
                "widened.  Each clause is scored on the ordinal its own words "
                "carry, and the frozen files are untouched"
            ),
            "result_basis": (
                "DEFINITION-level: the two refusals are the Challenge 1 and "
                "Challenge 4 bounds replayed on the caller's text, the widened "
                "reader's own bound is this rung's declaration, and the ordinal "
                "is a census of the run's own reader bounds; a hit is by "
                "construction and is not counted as content"
            ),
            "evidence": (
                "both inherited readers refuse the caller's inscription by "
                "name; the widened reader reads it as a whole whose left item "
                "is a whole and whose right side is empty, at depth two; and it "
                "refuses a whole deeper than its declared bound by name.  The "
                f"ordinal clause {verdict(c5_1_ordinal)}: the run has "
                f"{reader['reader_bounds_declared']} reader bounds and "
                f"{reader['widenings_of_the_reader_bound']} widenings"
            ),
        },
        "C5-2": {
            "status": verdict(c5_2),
            "label": "NOT FORCED",
            "result_basis": (
                "DEFINITION-level: the four policies, the three capabilities "
                "named for them, and therefore the counts and the identity of "
                "one step with capability count one are declarations of this "
                "rung; a hit is by construction and is not counted as content"
            ),
            "evidence": (
                "four declared policies at capability counts 0, 1, 1, and 2 "
                "over three declared capabilities; a policy is one step exactly "
                "when its capability count is one; and the recording policy, "
                "which is what the caller's demand needs, is refused as a "
                "bundle"
            ),
        },
        "C5-3": {
            "status": verdict(c5_3),
            "label": "FORCED",
            "result_basis": (
                "content: the comparison with what `<a|>` retains is an "
                "isomorphism-witness search over the unpruned enumeration at "
                "each candidate's own renamings, and both values are attained "
                "elsewhere in the space"
            ),
            "evidence": (
                "under both one-step policies and both readings the caller's "
                "inscription retains exactly one mark, and what it retains is "
                "isomorphic to what the Challenge 1 inscription retains, so the "
                "nesting is internally invisible there"
            ),
        },
        "C5-4": {
            "status": verdict(c5_4),
            "label": "FORCED",
            "result_basis": (
                "content: the separation of the two one-step policies is a "
                "census over the declared domain with the parting inscriptions "
                "named, and the class count is the implemented quotient"
            ),
            "evidence": (
                "the two one-step policies part on the declared domain and "
                "agree at the caller's own inscription; the minimum capability "
                "count among admitting points is one, two classes attain it, "
                "both are retained, and uniqueness is refuted under both "
                "readings"
            ),
        },
        "C5-5": {
            "status": verdict(c5_5),
            "label": "NOT FORCED",
            "result_basis": (
                "content: that no policy makes a second initial datum is a "
                "replay of every point's history with the datum read off, and "
                "that a further mark may be admitted within the inner whole is "
                "a probe whose deciding fact is a census — the deepest place "
                "each policy's own admissions name over the declared domain — "
                "with both values attained.  The "
                "classification of what the inner whole IS under each policy is "
                "the run's and is declared, not computed"
            ),
            "evidence": (
                "no retained state under any policy carries a second initial "
                "datum; the inner whole is a mark under the opaque policy, "
                "nothing under the discarding policy, and a second boundary "
                "under the recording policy; and a further mark may be admitted "
                "inside it under the recording policy alone, which is not one "
                "step"
            ),
        },
        "C5-6": {
            "status": verdict(c5_6),
            "label": "FORCED",
            "result_basis": (
                "content: the key-determination of depth is a census over the "
                "declared domain, and the depths a policy can hold are read off "
                "the same census.  That no form of the closed grammar reads "
                "depth is DEFINITION-level, the grammar being the declared sum "
                "of two forms, and it is reported separately"
            ),
            "evidence": (
                "under every one-step policy every retained mark has depth one, "
                "so depth separates nothing; under the recording policy the "
                "domain holds depths one and two and equal keys give equal "
                "depths; and no form of the closed observation grammar reads "
                "depth at any point"
            ),
        },
        "C5-7": {
            "status": verdict(c5_7),
            "label": "FORCED",
            "result_basis": (
                "content: the collapse is the implemented quotient over the "
                "whole declared domain, and the orbit sizes are read off the "
                "unpruned enumeration of each candidate's permitted renamings"
            ),
            "evidence": (
                "the naming coordinate collapses at every policy under U and at "
                "three of four under O; the retained mark's address orbit has "
                "four members under U, one under O with the naming reaching "
                "inward, and two under O without it, so which side of the inner "
                "boundary the mark lies on is not internally available under O "
                "either without that further declaration"
            ),
        },
        "C5-8": {
            "status": verdict(c5_8),
            "label": "FORCED",
            "result_basis": (
                "content: the certification and the replay are computed at "
                "every point of the space, and both values of the admission "
                "predicate are attained.  That the event-follows relation is "
                "empty is the declared grammar and is DEFINITION-level"
            ),
            "evidence": (
                "at every point the initial datum and the reading are "
                "unchanged and the event-follows relation is empty on every "
                "probe of both grammars; every admitting point's history is "
                "certified and replays from genesis; and no rule of an earlier "
                "rung is withdrawn"
            ),
        },
        "C5-X": {
            "status": "PENDING",
            "label": "NOT FORCED",
            "evidence": "scored by the autonomous continuation",
        },
    }


def tally(scores: Json) -> Json:
    """Count the scored Challenge 5 predictions by status and by basis."""
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
    """The Challenge 0 census, run over the Challenge 5 modules."""
    return {
        "model": state_event_generators(model, EVENT_TYPES),
        "presentation": state_event_generators(presentation, EVENT_TYPES),
        "challenge4": state_event_generators(
            sys.modules["boundary.challenge4"], EVENT_TYPES
        ),
        "challenge5": state_event_generators(sys.modules[__name__], EVENT_TYPES),
    }


def outside_facts() -> Json:
    """Whether the outside of the outermost boundary is formulable here."""
    return {
        "address_alphabet": [0, 1],
        "address_values_denoting_the_outside": [],
        "formulable": False,
        "status": "OPEN",
        "note": (
            "an address is a sequence of sides crossed INWARD from the "
            "outermost boundary, and the declared alphabet has two values, both "
            "of them sides of a boundary already crossed.  There is no value "
            "for a place beyond the outermost boundary, and the run declares "
            "none: the question is named and left OPEN rather than answered by "
            "a declaration made to answer it"
        ),
    }


def build() -> Json:
    u = reading_facts(READING_U)
    o = reading_facts(READING_O)
    reader = reader_facts()
    scores = score(u, o, reader)
    return {
        "challenge": 5,
        "inscription": INSCRIPTION,
        "seed_sha256": SEED_SHA256,
        "predictions_sha256": PREDICTIONS_SHA256,
        "challenge0_predictions_sha256": C0_PREDICTIONS_SHA256,
        "challenge1_predictions_sha256": C1_PREDICTIONS_SHA256,
        "challenge2_predictions_sha256": C2_PREDICTIONS_SHA256,
        "challenge3_predictions_sha256": C3_PREDICTIONS_SHA256,
        "challenge4_predictions_sha256": C4_PREDICTIONS_SHA256,
        "reader": reader,
        "identity_policy_inherited": DECLARED_POLICY,
        "relabelled_token_inherited": RELABELLED_TOKEN,
        "policy_space": {
            "members": list(POLICY_SPACE),
            "names": [POLICY_NAMES[policy] for policy in POLICY_SPACE],
            "capability_of": CAPABILITY_OF,
            "capabilities_of_policy": {
                POLICY_NAMES[policy]: list(caps)
                for policy, caps in POLICY_CAPABILITIES.items()
            },
            "exhaustive_because": POLICY_SPACE_IS_EXHAUSTIVE_BECAUSE,
            "coordinates": list(COORDINATES),
            "size": len(point_space()),
            "one_step_rule": ONE_STEP_RULE,
        },
        "measures": {"mu1": MU1, "mu2": MU2},
        "capabilities": CAPABILITIES,
        "collateral_facts": list(COLLATERAL_FACTS),
        "what_the_inner_whole_is": {
            POLICY_NAMES[policy]: text
            for policy, text in WHAT_THE_INNER_WHOLE_IS.items()
        },
        "domain": {
            "alphabet": list(ALPHABET),
            "depth_bound": NESTING_BOUND,
            "size": len(domain()),
            "first_members": domain_texts()[:8],
            "caller_inscription_in_the_domain": INSCRIPTION in domain_texts(),
            "declared_because": (
                "two policies are the same policy exactly when they retain "
                "isomorphic states at every member of this domain; the domain "
                "is a declaration, and a wider alphabet or a deeper bound is "
                "available and is not enumerated"
            ),
        },
        "readings": {READING_U: u, READING_O: o},
        "event_kinds": [t.__name__ for t in EVENT_TYPES],
        "new_event_kinds_at_challenge_5": list(NEW_EVENT_KINDS_AT_CHALLENGE_5),
        "withdrawn_rules_at_challenge_5": list(WITHDRAWN_RULES_AT_CHALLENGE_5),
        "state_event_generators": state_event_generators(model, EVENT_TYPES),
        "event_returning_functions_by_module": event_returning_functions_by_module(),
        "observation_vocabulary": observation_vocabulary(),
        "closed_grammar_forms_reading_depth": closed_grammar_forms_reading_depth(),
        "outside_of_the_outermost_boundary": outside_facts(),
        "what_the_challenge_exercises": {
            "supply": (
                "yes: one Supply per admitted mark, before every admission of "
                "the retained whole; a policy that admits nothing supplies "
                "nothing"
            ),
            "mention": (
                "yes: the inner whole is named by the reader and by the "
                "refusal, and naming it is not admitting it"
            ),
            "admission": (
                "yes, and it is the rung's subject: what an admission does with "
                "an item that is a whole is the declared policy space, and no "
                "policy is taken"
            ),
            "current-state designation": (
                "yes: every retained state is the replay of an explicit "
                "history, and the current configuration is the Challenge 4 "
                "retention, no policy of this rung having been taken"
            ),
            "retention": (
                "yes: what the caller's retention amounts to is exactly what "
                "the policy space decides, and three of the four policies "
                "retain something"
            ),
            "observation": (
                "yes: the closed grammar is unchanged and no form is added; "
                "the rung computes that no form of it reads depth"
            ),
            "side": (
                "yes, and it is the rung's subject: a side of a side is what "
                "the caller's inscription presents, and only the recording "
                "policy keeps the difference between the two levels"
            ),
            "equality": (
                "yes: structural equality of a deep regime, the isomorphism "
                "relation at a candidate's permitted renamings, and the "
                "sameness of two POLICIES over the declared domain are three "
                "different relations, and the rung uses all three"
            ),
        },
        "boundary_dependence": BOUNDARY_DEPENDENCE,
        "scores": scores,
        "tally": tally(scores),
        "authority_effect": "None",
    }
