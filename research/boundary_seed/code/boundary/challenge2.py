"""Challenge 2: the caller supplies and retains ``<a|>`` and ``<|a>``.

Everything computed here is metatheory about the kernel in ``model.py`` and
the presentation layer in ``presentation.py``.

The caller retains, so unlike Challenge 1 this rung has admitted state: the
current regime under each reading is the replay of a caller history that
contains, for each whole, a supply and an admission.  Which admission event
that is, is the rung's first decision, and it is decided by a declared
finite space of two identity policies rather than by judgment:

* under the SHARED policy an admission names the mark its presentation token
  already names, which is the Challenge 1 event ``AdmitMark``;
* under the OCCURRENCE policy an admission admits a fresh mark and the token
  is only a label, which is the Challenge 2 event ``AdmitOccurrence``.

Every policy over the caller's two wholes is one of these two, because the
second admission's target either is or is not already admitted.  Under SHARED
the caller's history is refused by name, so exactly one policy of the
declared space lets the caller retain both wholes; the run declares that one
and prices it.

Nothing is admitted silently: every state change in the receipt is an event
of a replayed history, and the later-event probes are hypothetical, as at
Challenges 0 and 1.
"""

from __future__ import annotations

import sys
from itertools import product
from typing import Any

from boundary import challenge0, challenge1, model, presentation
from boundary.challenge0 import (
    judgment_json,
    observation_vocabulary,
    profile_json,
    state_event_generators,
)
from boundary.challenge1 import (
    Json,
    judgments_json,
    key_json,
    probes,
)
from boundary.model import (
    READING_O,
    READING_U,
    SIDE_NAMES,
    AdmissionError,
    AdmitMark,
    AdmitOccurrence,
    Event,
    OnSide,
    Regime,
    Supply,
    automorphisms,
    canonical,
    certify,
    event_follows,
    fixed_up_to_mark_renaming,
    genesis,
    is_isomorphic,
    isomorphism_witness,
    mark_automorphism_to,
    mark_profile,
    mark_side,
    marks_internally_separable,
    marks_on_different_sides,
    mentioned,
    name_observations,
    new_observations,
    observation_holds,
    observations,
    permitted_images,
    reflect,
    rename_marks,
    replay,
    serialize,
    side_exchanging_automorphism,
    side_profile,
    sides_collapsed,
    supplied,
)
from boundary.presentation import (
    CONVENTIONS,
    DECLARED_CONVENTION,
    OTHER_CONVENTION,
    Whole,
    admitted_side,
    read_whole,
    supply_event,
)

SEED_SHA256 = challenge0.SEED_SHA256
C0_PREDICTIONS_SHA256 = challenge0.PREDICTIONS_SHA256
C1_PREDICTIONS_SHA256 = challenge1.PREDICTIONS_SHA256
PREDICTIONS_SHA256 = "95f9371b030b8df64b4842a5df7be695d9e7f1b2311a300e78d915a701c16474"

INSCRIPTIONS: tuple[str, str] = ("<a|>", "<|a>")
EVENT_TYPES: tuple[type, ...] = (Supply, AdmitMark, AdmitOccurrence)
STATE_CHANGING_EVENT_KINDS: list[str] = ["AdmitMark", "AdmitOccurrence"]
NEW_EVENT_KINDS_AT_CHALLENGE_2: list[str] = ["AdmitOccurrence"]
WITHDRAWN_RULES_AT_CHALLENGE_2: list[str] = [
    "admitted presentation tokens must be unique (definition 3 of Challenges 0 and 1)"
]
RELABELLED_TOKEN = "z"
GROWTH_TOKEN = "b"
CENSUS_MAX_MARKS = 3
JUDGMENT_DOMAIN_MAX_MARKS = 2
REGIME_DOMAIN_MAX_MARKS = 2
MARK_FORMS: tuple[int, int] = (0, 1)

POLICY_SHARED = "shared identity: an admission names the mark its token already names"
POLICY_OCCURRENCE = "occurrence identity: an admission admits a fresh mark, the token being a label"
POLICY_SPACE: tuple[str, str] = (POLICY_SHARED, POLICY_OCCURRENCE)
DECLARED_POLICY = POLICY_OCCURRENCE
POLICY_SPACE_IS_EXHAUSTIVE_BECAUSE = (
    "a policy decides what the second admission of the caller's two wholes "
    "admits, and its target either is or is not a mark already admitted; the "
    "space has one policy for each answer and no third answer exists.  This "
    "is exhaustive over the declared space and claims nothing about policies "
    "that would change the event grammar further"
)

SCORED_PREDICTIONS: tuple[str, ...] = (
    "C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7", "C2-8",
)
# The scored predictions whose every hitting clause, read literally, is fixed
# by a declaration of the run: the reading of "retains", the Challenge 1
# refusal replayed on a declared history, and the declared two-policy space
# with its declared price.  A HIT on one of them is HIT by construction and
# is not counted as content, by the rule of PLAN.md; a miss on one is a miss
# like any other.  The criterion is the one Challenge 1 declared.
DEFINITION_LEVEL_PREDICTIONS: tuple[str, ...] = ("C2-1", "C2-2", "C2-3")
TALLY_CRITERION = challenge1.TALLY_CRITERION

CAPABILITIES: dict[str, dict[str, str]] = {
    "admitted boundary": {
        "declared_at": "the seed, as the one admitted primitive exception",
        "paid_by": "the seed",
        "buys_at_challenge_2": (
            "that each retained whole lies on a side, and that the two "
            "retained marks do not share one"
        ),
    },
    "side names under O": {
        "declared_at": "genesis, as the O reading of the one declaration",
        "paid_by": "the declared reading",
        "buys_at_challenge_2": (
            "under O only: that the two retained marks are separated, one on "
            "near and one on far"
        ),
    },
    "presentation convention": {
        "declared_at": "Challenge 1, as metatheory",
        "paid_by": "the run",
        "buys_at_challenge_2": (
            "which presented whole becomes which mark; not that the two "
            "marks are separated, the other convention's regime lying in the "
            "same isomorphism class under both readings"
        ),
    },
    "occurrence identity": {
        "declared_at": "Challenge 2, as this rung's one new declaration",
        "paid_by": "the run",
        "buys_at_challenge_2": (
            "that the two wholes are two marks at all, despite the shared "
            "visible mark; without it the caller's retention is refused"
        ),
    },
}
BOUNDARY_DEPENDENCE: dict[str, str] = {
    "the identity policy space and the refusal of the shared policy": (
        "does not depend on the admitted boundary; it is about presentation "
        "tokens and internal identity"
    ),
    "supply is presentation only, and the current state is the replay of the "
    "caller's history": "does not depend on the admitted boundary",
    "the initial datum and reading are unchanged by every event": (
        "does not depend on the admitted boundary"
    ),
    "the event-follows relation stays empty": "does not depend on the admitted boundary",
    "the two new judgments, the sides the marks are retained on, the "
    "automorphisms, the separation, and the different-sides fact": (
        "require the admitted boundary and are not formulated after removing it"
    ),
}


def event_json(e: Event) -> dict[str, object]:
    """Render any event of the Challenge 2 grammar."""
    if isinstance(e, Supply):
        return {"kind": "Supply", "token": e.token}
    if isinstance(e, AdmitMark):
        return {"kind": "AdmitMark", "token": e.token, "side": e.side}
    return {"kind": "AdmitOccurrence", "token": e.token, "side": e.side}


def history_json(history: list[Event]) -> list[dict[str, object]]:
    return [event_json(e) for e in history]


def policy_event(policy: str, token: str, side: int) -> Event:
    """The admission event a declared identity policy forms.

    Deterministic computation over metatheory: it applies nothing.  A
    candidate becomes state only through ``replay`` of a history containing
    it.
    """
    if policy == POLICY_SHARED:
        return AdmitMark(token, side)
    if policy == POLICY_OCCURRENCE:
        return AdmitOccurrence(token, side)
    raise ValueError(f"unknown identity policy: {policy!r}")


def caller_history(wholes: list[Whole], convention: str, policy: str) -> list[Event]:
    """The caller's Challenge 2 history: for each retained whole, a supply
    and an admission under the given convention and identity policy."""
    history: list[Event] = []
    for whole in wholes:
        assert whole.token is not None and whole.presented_side is not None
        history.append(supply_event(whole))
        history.append(
            policy_event(policy, whole.token, admitted_side(whole.presented_side, convention))
        )
    return history


def refusal(history: list[Event], base: Regime) -> str | None:
    """The message certifying replay refuses a history with, or ``None``."""
    try:
        replay(history, base)
    except AdmissionError as exc:
        return str(exc)
    return None


def policy_facts(g: Regime, wholes: list[Whole], convention: str, policy: str) -> Json:
    """What one identity policy does with the caller's Challenge 2 history."""
    history = caller_history(wholes, convention, policy)
    message = refusal(history, g)
    if message is not None:
        return {
            "policy": policy,
            "convention": convention,
            "history": history_json(history),
            "refused": True,
            "refusal": message,
            "certified": False,
            "marks": 0,
            "placement": [],
            "labels": [],
        }
    r = replay(history, g)
    return {
        "policy": policy,
        "convention": convention,
        "history": history_json(history),
        "refused": False,
        "refusal": None,
        "certified": certify(history, g, r),
        "marks": r.n_marks(),
        "placement": list(r.placement),
        "labels": list(r.marks),
    }


def identity_policy_facts(g: Regime, wholes: list[Whole]) -> Json:
    """The declared two-policy space, run under both conventions."""
    rows = [
        policy_facts(g, wholes, convention, policy)
        for policy in POLICY_SPACE
        for convention in CONVENTIONS
    ]
    admitting_both = sorted(
        {
            str(row["policy"])
            for row in rows
            if row["marks"] == 2 and row["certified"]
        }
    )
    refused_under_every_convention = sorted(
        {
            str(row["policy"])
            for row in rows
            if all(
                other["refused"]
                for other in rows
                if other["policy"] == row["policy"]
            )
        }
    )
    return {
        "space": list(POLICY_SPACE),
        "space_size": len(POLICY_SPACE),
        "exhaustive_because": POLICY_SPACE_IS_EXHAUSTIVE_BECAUSE,
        "declared": DECLARED_POLICY,
        "rows": rows,
        "policies_admitting_both_wholes": admitting_both,
        "policies_refused_under_every_convention": refused_under_every_convention,
        "declared_is_the_only_one_admitting_both": admitting_both == [DECLARED_POLICY],
    }


def later_event_facts(g: Regime, history: list[Event], r: Regime) -> Json:
    """Hypothetical later events on the retained regime; nothing admitted.

    A further supply and a further occurrence admission leave both retained
    marks' judgments holding.  The Challenge 1 token-keyed admission can no
    longer act on this regime at all: the label names two marks and it is
    refused by name, which is the withdrawn identification of presentation
    identity with internal identity made visible.
    """
    growth: list[Event] = [Supply(GROWTH_TOKEN), AdmitOccurrence(GROWTH_TOKEN, 0)]
    after_growth = replay(history + growth, g)
    token_keyed: list[Event] = [AdmitMark(r.marks[0], mark_side(r, 0))]
    return {
        "growth_probe": history_json(growth),
        "judgments_retained_after_growth": [
            observation_holds(after_growth, OnSide(i, mark_side(r, i))) for i in range(r.n_marks())
        ],
        "growth_regime_marks": after_growth.n_marks(),
        "token_keyed_probe": history_json(token_keyed),
        "token_keyed_refused": refusal(history + token_keyed, g) is not None,
        "token_keyed_refusal": refusal(history + token_keyed, g),
    }


def regime_domain(reading: str, max_marks: int) -> list[Regime]:
    """Every hypothetical placement of up to ``max_marks`` marks; none admitted."""
    out: list[Regime] = []
    for n in range(max_marks + 1):
        marks = tuple(f"m{i}" for i in range(n))
        for placement in product((0, 1), repeat=n):
            out.append(Regime(reading, marks, placement))
    return out


def mark_form_invariant(side: int, domain: list[Regime]) -> bool:
    """Whether the mark property "this mark lies on ``side``" is invariant.

    Invariance is at every regime of the domain, every permitted image of it,
    and every mark: the property must hold of a mark exactly when it holds of
    that mark's image under the renaming.
    """
    return all(
        observation_holds(image, OnSide(pi[i], side)) == observation_holds(r, OnSide(i, side))
        for r in domain
        for _reflected, pi, image in permitted_images(r)
        for i in range(r.n_marks())
    )


def separating_mark_forms(r: Regime, i: int, j: int) -> list[int]:
    """The mark forms whose holding differs at the two marks."""
    return [
        side
        for side in MARK_FORMS
        if observation_holds(r, OnSide(i, side)) != observation_holds(r, OnSide(j, side))
    ]


def different_sides_census(max_marks: int) -> Json:
    """Whether "no two admitted marks share a side" survives every permitted
    renaming, over every hypothetical placement of up to ``max_marks`` marks."""
    images = 0
    invariant = True
    for reading in (READING_U, READING_O):
        for n in range(max_marks + 1):
            marks = tuple(f"m{i}" for i in range(n))
            for placement in product((0, 1), repeat=n):
                r = Regime(reading, marks, placement)
                want = marks_on_different_sides(r)
                for _reflected, _pi, image in permitted_images(r):
                    images += 1
                    if marks_on_different_sides(image) != want:
                        invariant = False
    return {
        "max_marks": max_marks,
        "images_checked": images,
        "invariant_under_every_permitted_renaming": invariant,
        "note": (
            "hypothetical placements under both readings; nothing here is "
            "admitted.  The property reads the placement tuple only and is "
            "not an object-language value."
        ),
    }


def witness_json(witness: tuple[bool, tuple[int, ...]] | None) -> Json | None:
    if witness is None:
        return None
    return {"reflected": witness[0], "permutation": list(witness[1])}


def automorphism_facts(r: Regime) -> Json:
    """The permitted renamings carrying the retained regime to itself."""
    found = automorphisms(r)
    exchange = mark_automorphism_to(r, 0, 1)
    side_exchange = side_exchanging_automorphism(r)
    return {
        "count": len(found),
        "entries": [witness_json(entry) for entry in found],
        "mark_exchange_witness": witness_json(exchange),
        "marks_internally_separable": marks_internally_separable(r, 0, 1),
        "side_exchange_witness": witness_json(side_exchange),
        "sides_internally_separable": side_exchange is None,
        "reflection_alone_fixes": reflect(r) == r,
        "mark_exchange_alone_fixes": serialize(rename_marks(r, (1, 0))) == serialize(r),
        "fixed_by_reflection_up_to_mark_renaming": fixed_up_to_mark_renaming(r),
    }


def separation_facts(reading: str, r: Regime) -> Json:
    """Which mark forms separate the two retained marks, and which of those
    are invariant under the permitted renamings of the reading."""
    domain = regime_domain(reading, REGIME_DOMAIN_MAX_MARKS)
    separating = separating_mark_forms(r, 0, 1)
    invariant = [side for side in MARK_FORMS if mark_form_invariant(side, domain)]
    return {
        "regime_domain_max_marks": REGIME_DOMAIN_MAX_MARKS,
        "regime_domain_size": len(domain),
        "mark_forms": list(MARK_FORMS),
        "separating_mark_forms": separating,
        "invariant_mark_forms": invariant,
        "invariant_separating_mark_forms": [s for s in separating if s in invariant],
        "mark_profiles": [judgments_json(mark_profile(r, i)) for i in range(r.n_marks())],
        "mark_sides": [mark_side(r, i) for i in range(r.n_marks())],
        "mark_side_names": (
            [SIDE_NAMES[mark_side(r, i)] for i in range(r.n_marks())]
            if reading == READING_O
            else []
        ),
    }


def order_facts(g: Regime, wholes: list[Whole], r: Regime) -> Json:
    """The same two retentions in the other order."""
    other_history = caller_history(list(reversed(wholes)), DECLARED_CONVENTION, DECLARED_POLICY)
    other = replay(other_history, g)
    witness = isomorphism_witness(r, other)
    return {
        "other_order_history": history_json(other_history),
        "other_order_placement": list(other.placement),
        "regimes_equal": other == r,
        "isomorphic": is_isomorphic(r, other),
        "witness": witness_json(witness),
        "canonical_keys_equal": canonical(other) == canonical(r),
        "order_internally_available": not is_isomorphic(r, other),
    }


def label_facts(r: Regime) -> Json:
    """The same placement under a different visible mark.

    Python regime equality compares the presentation tokens; the isomorphism
    relation and the canonical key forget them, and the Lean regime has no
    token to compare.  At Challenge 2 that difference is live, so it is
    reported rather than left implicit.
    """
    relabelled = Regime(r.reading, tuple(RELABELLED_TOKEN for _ in r.marks), r.placement)
    return {
        "relabelled_labels": list(relabelled.marks),
        "regimes_equal": relabelled == r,
        "isomorphic": is_isomorphic(r, relabelled),
        "canonical_keys_equal": canonical(relabelled) == canonical(r),
        "serializations_equal": serialize(relabelled) == serialize(r),
        "label_internally_available": not is_isomorphic(r, relabelled),
    }


def convention_facts(g: Regime, wholes: list[Whole], r: Regime) -> Json:
    """The declared convention against the other one, at two retained marks."""
    other_history = caller_history(wholes, OTHER_CONVENTION, DECLARED_POLICY)
    other = replay(other_history, g)
    witness = isomorphism_witness(r, other)
    classes = {canonical(r), canonical(other)}
    return {
        "declared": DECLARED_CONVENTION,
        "conventions": {name: dict(sides) for name, sides in CONVENTIONS.items()},
        "presented_sides": [whole.presented_side for whole in wholes],
        "declared_placement": list(r.placement),
        "other_placement": list(other.placement),
        "regimes_equal": other == r,
        "isomorphic_under_reading": is_isomorphic(r, other),
        "witness": witness_json(witness),
        "classes_under_isomorphism": len(classes),
        "selection_is_by": (
            "declared convention, not proof; it fixes which presented whole "
            "becomes which mark and not that the two marks are separated"
        ),
    }


def price_facts(reading: str, separable: bool) -> Json:
    """What the separation of the two retained wholes costs, and who paid."""
    used = ["admitted boundary", "occurrence identity"]
    if reading == READING_O:
        used = ["admitted boundary", "side names under O", "occurrence identity"]
    return {
        "capabilities": CAPABILITIES,
        "new_at_challenge_2": ["occurrence identity"],
        "new_event_kinds": list(NEW_EVENT_KINDS_AT_CHALLENGE_2),
        "withdrawn_rules": list(WITHDRAWN_RULES_AT_CHALLENGE_2),
        "paid_by_at_challenge_2": "the run",
        "nothing_new_paid_at_challenge_2": False,
        "separation_available": separable,
        "capabilities_the_separation_uses": used if separable else [],
        "boundary_alone_buys": (
            "that the two retained marks do not share a side, under both readings"
        ),
    }


def retained_facts(reading: str, g: Regime, wholes: list[Whole]) -> Json:
    history = caller_history(wholes, DECLARED_CONVENTION, DECLARED_POLICY)
    r = replay(history, g)
    after_supplies = replay([e for e in history if isinstance(e, Supply)], g)
    supplies = [e for e in history if isinstance(e, Supply)]
    return {
        "history": history_json(history),
        "certified": certify(history, g, r),
        "replays_from_genesis": replay(history, g) == r,
        "marks": r.n_marks(),
        "placement": list(r.placement),
        "labels": list(r.marks),
        "labels_repeat": len(set(r.marks)) < r.n_marks(),
        "supplies_are_equal_values": len(supplies) == 2 and supplies[0] == supplies[1],
        "supply_only_regime_equals_genesis": after_supplies == g,
        "marks_on_different_sides": marks_on_different_sides(r),
        "canonical_key": key_json(canonical(r)),
        "holding_judgments_before": len(observations(g)),
        "holding_judgments_after": len(observations(r)),
        "new_observations": judgments_json(new_observations(g, r)),
        "name_observations_unchanged": name_observations(r) == name_observations(g),
        "side_profiles": [profile_json(side_profile(r, 0)), profile_json(side_profile(r, 1))],
        "sides_collapsed": sides_collapsed(r),
        "initial_datum_unchanged": r.initial_datum == g.initial_datum,
        "reading_unchanged": r.reading == reading,
        "event_follows_relation_empty": all(
            not event_follows(r, e) for e in probes("a") + probes(GROWTH_TOKEN)
        ),
        "mentioned": sorted(mentioned(history)),
        "supplied": sorted(supplied(history)),
        "later_events": later_event_facts(g, history, r),
    }


def reading_facts(reading: str) -> Json:
    g = genesis(reading)
    wholes = [read_whole(text) for text in INSCRIPTIONS]
    policies = identity_policy_facts(g, wholes)
    retained = retained_facts(reading, g, wholes)
    history = caller_history(wholes, DECLARED_CONVENTION, DECLARED_POLICY)
    r = replay(history, g)
    separation = separation_facts(reading, r)
    return {
        "reading": reading,
        "wholes": [
            {"token": whole.token, "presented_side": whole.presented_side} for whole in wholes
        ],
        "identity_policies": policies,
        "retained": retained,
        "automorphisms": automorphism_facts(r),
        "separation": separation,
        "order": order_facts(g, wholes, r),
        "label": label_facts(r),
        "convention": convention_facts(g, wholes, r),
        "price": price_facts(reading, marks_internally_separable(r, 0, 1)),
    }


def score_c1x(u: Json, o: Json) -> Json:
    """Score the Challenge 1 extrapolation against the Challenge 2 facts.

    C1-X has a U half and an O half, and the O half has two clauses: that
    the side names separate the two marks, and that "the price is the O
    declaration paid at genesis, and nothing new is paid at Challenge 2".
    Each is scored on the frozen words.
    """
    ua = u["automorphisms"]
    us = u["separation"]
    oa = o["automorphisms"]
    os_ = o["separation"]
    u_half = (
        bool(ua["fixed_by_reflection_up_to_mark_renaming"])
        and ua["mark_exchange_witness"] is not None
        and not ua["marks_internally_separable"]
        and us["invariant_separating_mark_forms"] == []
    )
    o_names = (
        bool(oa["marks_internally_separable"])
        and os_["mark_side_names"] == [SIDE_NAMES[0], SIDE_NAMES[1]]
        and os_["invariant_separating_mark_forms"] == list(MARK_FORMS)
    )
    o_price = bool(o["price"]["nothing_new_paid_at_challenge_2"])

    def verdict(hit: bool) -> str:
        return "HIT" if hit else "MISSED"

    o_half = "HIT" if (o_names and o_price) else "PARTIAL" if o_names else "MISSED"
    status = "HIT" if (u_half and o_names and o_price) else "PARTIAL" if (u_half and o_names) else "MISSED"
    return {
        "status": status,
        "label": "NOT FORCED",
        "U_half_status": verdict(u_half),
        "O_half_status": o_half,
        "O_names_clause_status": verdict(o_names),
        "O_nothing_new_paid_clause_status": verdict(o_price),
        "condition_status": verdict(
            bool(u["retained"]["labels_repeat"])
            and u["retained"]["marks"] == 2
            and o["retained"]["marks"] == 2
        ),
        "O_nothing_new_paid_clause_fact": (
            "the frozen clause reads 'the price is the O declaration paid at "
            "genesis, and nothing new is paid at Challenge 2', and its "
            "falsifier names 'under O a price beyond the names'.  The rung "
            "paid one new declaration, the occurrence identity of "
            "price.new_at_challenge_2, without which the caller's retention "
            "is refused under both readings, so the clause is false as "
            "written and the falsifier fired.  The names clause is scored "
            "separately and hits"
        ),
        "evidence": (
            "U: the retained regime is fixed by the reflection up to mark "
            "renaming, a permitted automorphism exchanges the two marks, and "
            "no invariant mark form separates them; O: the marks are "
            "separated, one on near and one on far, by two invariant mark "
            "forms, but a new declaration was paid at this rung"
        ),
    }


def score(u: Json, o: Json, census: Json, observation_kinds: list[str], event_kinds: list[str]) -> Json:
    """Mechanical scoring of the frozen Challenge 2 predictions and of C1-X."""
    both = (u, o)

    def verdict(hit: bool) -> str:
        return "HIT" if hit else "MISSED"

    c2_1 = all(
        [e["kind"] for e in rd["retained"]["history"]]
        == ["Supply", "AdmitOccurrence", "Supply", "AdmitOccurrence"]
        and rd["retained"]["certified"]
        and rd["retained"]["replays_from_genesis"]
        and rd["retained"]["marks"] == 2
        and rd["retained"]["marks_on_different_sides"]
        and rd["retained"]["placement"] == [0, 1]
        and rd["retained"]["supplies_are_equal_values"]
        for rd in both
    ) and all(
        e["kind"] == "Supply" or e["kind"] in STATE_CHANGING_EVENT_KINDS
        for rd in both
        for e in rd["retained"]["history"]
    )
    shared_rows = [
        row
        for rd in both
        for row in rd["identity_policies"]["rows"]
        if row["policy"] == POLICY_SHARED
    ]
    c2_2 = len(shared_rows) == 4 and all(
        row["refused"] and "would move it and is refused" in str(row["refusal"])
        for row in shared_rows
    )
    c2_3 = all(
        rd["identity_policies"]["space_size"] == 2
        and rd["identity_policies"]["declared_is_the_only_one_admitting_both"]
        and rd["identity_policies"]["declared"] == DECLARED_POLICY
        and rd["price"]["new_at_challenge_2"] == ["occurrence identity"]
        and rd["price"]["new_event_kinds"] == NEW_EVENT_KINDS_AT_CHALLENGE_2
        and rd["price"]["withdrawn_rules"] == WITHDRAWN_RULES_AT_CHALLENGE_2
        and rd["price"]["paid_by_at_challenge_2"] == "the run"
        for rd in both
    ) and u["price"]["new_at_challenge_2"] == o["price"]["new_at_challenge_2"] and (
        u["price"]["withdrawn_rules"] == o["price"]["withdrawn_rules"]
    ) and u["price"]["paid_by_at_challenge_2"] == o["price"]["paid_by_at_challenge_2"]
    c2_4 = (
        all(
            rd["retained"]["new_observations"]
            == [
                {"kind": "OnSide", "mark": 0, "side": 0},
                {"kind": "OnSide", "mark": 1, "side": 1},
            ]
            and rd["retained"]["name_observations_unchanged"]
            and rd["retained"]["initial_datum_unchanged"]
            and rd["retained"]["reading_unchanged"]
            and rd["separation"]["mark_profiles"]
            == [
                [{"kind": "OnSide", "mark": 0, "side": 0}],
                [{"kind": "OnSide", "mark": 1, "side": 1}],
            ]
            and rd["retained"]["later_events"]["judgments_retained_after_growth"] == [True, True]
            for rd in both
        )
        and u["retained"]["holding_judgments_before"] == 0
        and u["retained"]["holding_judgments_after"] == 2
        and o["retained"]["holding_judgments_before"] == 2
        and o["retained"]["holding_judgments_after"] == 4
        and observation_kinds == ["OnSide", "SideNamed"]
    )
    c2_5 = (
        u["automorphisms"]["count"] == 2
        and o["automorphisms"]["count"] == 1
        and u["automorphisms"]["mark_exchange_witness"] == {"reflected": True, "permutation": [1, 0]}
        and not u["automorphisms"]["marks_internally_separable"]
        and u["separation"]["invariant_mark_forms"] == []
        and u["separation"]["invariant_separating_mark_forms"] == []
    )
    c2_6 = (
        o["automorphisms"]["count"] == 1
        and o["automorphisms"]["mark_exchange_witness"] is None
        and o["automorphisms"]["marks_internally_separable"]
        and o["retained"]["name_observations_unchanged"]
        and o["separation"]["invariant_mark_forms"] == list(MARK_FORMS)
        and o["separation"]["invariant_separating_mark_forms"] == list(MARK_FORMS)
        and o["separation"]["mark_side_names"] == [SIDE_NAMES[0], SIDE_NAMES[1]]
        and o["price"]["capabilities_the_separation_uses"]
        == ["admitted boundary", "side names under O", "occurrence identity"]
        and all(
            rd["convention"]["isomorphic_under_reading"]
            and rd["convention"]["classes_under_isomorphism"] == 1
            for rd in both
        )
    )
    c2_7 = (
        bool(census["invariant_under_every_permitted_renaming"])
        and census["max_marks"] == CENSUS_MAX_MARKS
        and all(rd["retained"]["marks_on_different_sides"] for rd in both)
        and u["separation"]["invariant_separating_mark_forms"] == []
        and o["separation"]["invariant_separating_mark_forms"] == list(MARK_FORMS)
    )
    c2_8 = (
        u["automorphisms"]["side_exchange_witness"] is not None
        and not u["automorphisms"]["sides_internally_separable"]
        and o["automorphisms"]["side_exchange_witness"] is None
        and o["automorphisms"]["sides_internally_separable"]
        and all(not rd["retained"]["sides_collapsed"] for rd in both)
        and all(not rd["order"]["order_internally_available"] for rd in both)
        and all(not rd["label"]["label_internally_available"] for rd in both)
    )
    return {
        "C1-X": score_c1x(u, o),
        "C2-1": {
            "status": verdict(c2_1),
            "label": "NOT FORCED",
            "result_basis": (
                "DEFINITION-level: the reading of the caller's 'retains' is the "
                "run's decision, and the two marks on opposite sides follow from "
                "the declared convention and the declared identity policy; a hit "
                "is by construction and is not counted as content"
            ),
            "evidence": (
                "the caller history is a supply and an occurrence admission for "
                "each whole, certified and replayed from genesis, and its regime "
                "holds two marks on opposite sides; the two supplies are the same "
                "event value"
            ),
        },
        "C2-2": {
            "status": verdict(c2_2),
            "label": "FORCED",
            "result_basis": (
                "DEFINITION-level: the refusal is the Challenge 1 moving-admission "
                "declaration replayed on a declared history, under both readings "
                "and both conventions; a hit is by construction and is not counted "
                "as content, although the declaration was made before this "
                "question arose"
            ),
            "evidence": (
                "all four shared-policy histories are refused, each by the "
                "moving-admission refusal naming the side the mark is admitted on"
            ),
        },
        "C2-3": {
            "status": verdict(c2_3),
            "label": "NOT FORCED",
            "result_basis": (
                "DEFINITION-level: the space, its exhaustiveness, the declared "
                "policy, and the price are declarations of this rung, and the "
                "clause that only one policy admits both rests on the C2-2 "
                "refusal; a hit is by construction and is not counted as content"
            ),
            "evidence": (
                "the declared space has two policies, exactly one of which lets "
                "the caller retain both wholes; the price is one new admission "
                "event and the withdrawal of the token-uniqueness rule, paid by "
                "the run and equal under both readings"
            ),
        },
        "C2-4": {
            "status": verdict(c2_4),
            "label": "FORCED",
            "result_basis": (
                "content: the two new judgments and their evaluation rest on "
                "retained_onSide_true_iff with retained_onSide_zero, "
                "retained_onSide_one, and retained_onSide_beyond, none of them by "
                "unfolding, and retention on retained_judgments_survive"
            ),
            "evidence": (
                "exactly two new holding judgments, one per mark and per side; no "
                "name judgment, datum, or reading changes; 0 to 2 under U and 2 to "
                "4 under O; each mark's profile is its own side; both judgments "
                "survive the growth probe"
            ),
        },
        "C2-5": {
            "status": verdict(c2_5),
            "label": "FORCED",
            "result_basis": (
                "content: the automorphism counts and the exchanging witness are "
                "computed over the unpruned permitted-image enumeration, and the "
                "invariance of each mark form is a census over the bounded regime "
                "domain; the concrete transport is the Lean "
                "retained_exchange_transports"
            ),
            "evidence": (
                "two permitted automorphisms under U and one under O; the "
                "reflection with the mark exchange carries mark 0 to mark 1; "
                "neither mark form is invariant under U, so none separates them"
            ),
        },
        "C2-6": {
            "status": verdict(c2_6),
            "label": "FORCED",
            "result_basis": (
                "content: the single O automorphism and the absence of an "
                "exchanging one are computed over the unpruned search, the "
                "invariance of both mark forms is a census, and the convention "
                "class count is an isomorphism-witness computation; the raw "
                "separation is the Lean retained_marks_separated_by_a_side"
            ),
            "evidence": (
                "under O the only permitted automorphism is the identity, both "
                "mark forms are invariant and both separate the marks, one lying "
                "on near and one on far; the other convention's regime lies in "
                "the same class under both readings"
            ),
        },
        "C2-7": {
            "status": verdict(c2_7),
            "label": "FORCED",
            "result_basis": (
                "content: the invariance of the different-sides property is a "
                "census over every regime of at most three marks under both "
                "readings and every permitted image of each"
            ),
            "evidence": (
                "the property survives every permitted renaming in the census and "
                "holds of the retained regime; under U no invariant mark form "
                "separates the two wholes, under O both do"
            ),
        },
        "C2-8": {
            "status": verdict(c2_8),
            "label": "NOT FORCED",
            "result_basis": (
                "content: the side-exchanging automorphism, the order "
                "isomorphism, and the label isomorphism are witness searches over "
                "the unpruned enumeration, and none is fixed by a declaration"
            ),
            "evidence": (
                "under U a permitted automorphism exchanges the two sides and "
                "under O none does; the profile comparison is false at the "
                "retained regime under both readings; the other admission order "
                "and a different visible mark both give isomorphic regimes"
            ),
        },
        "C2-X": {
            "status": "PENDING",
            "label": "NOT FORCED",
            "evidence": "scored by Challenge 3",
        },
    }


def tally(scores: Json) -> Json:
    """Count the scored Challenge 2 predictions by status and by basis."""
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
    """The Challenge 0 census, run over the Challenge 2 event grammar."""
    return {
        "model": state_event_generators(model, EVENT_TYPES),
        "presentation": state_event_generators(presentation, EVENT_TYPES),
        "challenge1": state_event_generators(sys.modules["boundary.challenge1"], EVENT_TYPES),
        "challenge2": state_event_generators(sys.modules[__name__], EVENT_TYPES),
    }


def build() -> Json:
    u = reading_facts(READING_U)
    o = reading_facts(READING_O)
    census = different_sides_census(CENSUS_MAX_MARKS)
    observation_kinds = observation_vocabulary()
    event_kinds = [t.__name__ for t in EVENT_TYPES]
    scores = score(u, o, census, observation_kinds, event_kinds)
    return {
        "challenge": 2,
        "inscriptions": list(INSCRIPTIONS),
        "seed_sha256": SEED_SHA256,
        "predictions_sha256": PREDICTIONS_SHA256,
        "challenge0_predictions_sha256": C0_PREDICTIONS_SHA256,
        "challenge1_predictions_sha256": C1_PREDICTIONS_SHA256,
        "readings": {READING_U: u, READING_O: o},
        "event_kinds": event_kinds,
        "state_changing_event_kinds": list(STATE_CHANGING_EVENT_KINDS),
        "new_event_kinds_at_challenge_2": list(NEW_EVENT_KINDS_AT_CHALLENGE_2),
        "withdrawn_rules_at_challenge_2": list(WITHDRAWN_RULES_AT_CHALLENGE_2),
        "state_event_generators": state_event_generators(model, EVENT_TYPES),
        "event_returning_functions_by_module": event_returning_functions_by_module(),
        "observation_vocabulary": observation_kinds,
        "different_sides_census": census,
        "what_the_challenge_exercises": {
            "supply": "yes: one Supply event per retained whole, the two equal as values",
            "mention": (
                "yes: the shared visible mark is named by every event of the "
                "caller's history and is not an identity"
            ),
            "admission": (
                "yes: the caller retains, so the caller's history contains one "
                "admission per whole; which admission event that is, is the "
                "declared identity policy"
            ),
            "current-state designation": (
                "yes: the current state is the replay of the caller's history and "
                "holds two marks on opposite sides"
            ),
            "retention": (
                "yes: the placement tuple carries both marks, and both judgments "
                "survive the hypothetical growth probe"
            ),
            "observation": "yes: two new OnSide judgments, one per mark",
            "side": (
                "yes: the presented side of each whole, mapped to an admitted side "
                "by the declared convention"
            ),
            "equality": (
                "yes: structural regime equality compares the labels, the "
                "isomorphism relation and the canonical key forget them, and the "
                "difference is live at this rung because the two wholes share a "
                "visible mark"
            ),
        },
        "boundary_dependence": BOUNDARY_DEPENDENCE,
        "scores": scores,
        "tally": tally(scores),
        "authority_effect": "None",
    }
