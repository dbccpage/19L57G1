"""Challenge 1: the supply of ``<a|>`` under readings U and O.

Everything computed here is metatheory about the kernel in ``model.py``
and the presentation layer in ``presentation.py``.  The caller supplies
and does not retain, so under each reading the receipt carries the
supplied-only history, whose replay is the current state and equals
genesis, and every one-step admission candidate as a separately certified
candidate history.  No candidate is designated current: the current state
is the replay of the caller's history and nothing the caller did not
supply.  The declared convention selects which candidate admission the
presented side licenses, if admission is later called for; it admits
nothing.  Under U the two candidates are one isomorphism class; under O
they are two, both retained, the second the reflection of the first by a
replay-level theorem.  Nothing is admitted silently: every state change in
the receipt is an event in a replayed candidate history, and the retention
probes are hypothetical, like the Challenge 0 census.

An earlier version designated the convention's admitted candidate as the
current state.  That turned a candidate from this module's own enumerator
into admitted state with no admission event from the caller, conflating
supply with admission, and is WITHDRAWN.
"""

from __future__ import annotations

import sys
from itertools import product
from typing import Any

from boundary import challenge0, model, presentation
from boundary.challenge0 import (
    EVENT_TYPES,
    judgment_json,
    observation_vocabulary,
    profile_json,
    state_event_generators,
)
from boundary.model import (
    READING_O,
    READING_U,
    SIDE_NAMES,
    AdmissionError,
    AdmitMark,
    Event,
    Observation,
    OnSide,
    Regime,
    SideNamed,
    Supply,
    canonical,
    certify,
    event_follows,
    genesis,
    is_isomorphic,
    isomorphism_witness,
    mark_profile,
    mentioned,
    name_observations,
    new_observations,
    observation_holds,
    observations,
    permitted_images,
    reflect,
    replay,
    side_profile,
    sides_collapsed,
    supplied,
)
from boundary.presentation import (
    CONVENTIONS,
    DECLARED_CONVENTION,
    OTHER_CONVENTION,
    Whole,
    admission_event,
    read_whole,
    supply_event,
)

SEED_SHA256 = challenge0.SEED_SHA256
C0_PREDICTIONS_SHA256 = challenge0.PREDICTIONS_SHA256
PREDICTIONS_SHA256 = "7cf17e56fffb4e45d4100750010265582fa921fabeed7fb1b84aa798f6e56dc7"
INSCRIPTION = "<a|>"
JUDGMENT_DOMAIN_MAX_MARKS = 2
REGIME_DOMAIN_MAX_MARKS = 1
HYPOTHETICAL_TOKEN = "b"
STATE_CHANGING_EVENT_KINDS: list[str] = ["AdmitMark"]

BOUNDARY_DEPENDENCE: dict[str, str] = {
    "supply is presentation only": "does not depend on the admitted boundary",
    "admission is a separate event; the mark is retained": (
        "does not depend on the admitted boundary for the event discipline; "
        "the side the mark is retained on requires it"
    ),
    "the current state is the replay of the caller's history": (
        "does not depend on the admitted boundary"
    ),
    "the initial datum and reading are unchanged by every event": (
        "does not depend on the admitted boundary"
    ),
    "the event-follows relation stays empty": "does not depend on the admitted boundary",
    "one new judgment, the mark's side; profiles; candidates; convention; classes": (
        "require the admitted boundary and are not formulated after removing it"
    ),
}

Json = dict[str, Any]


def event_json(e: Event) -> dict[str, object]:
    if isinstance(e, Supply):
        return {"kind": "Supply", "token": e.token}
    return {"kind": "AdmitMark", "token": e.token, "side": e.side}


def history_json(history: list[Event]) -> list[dict[str, object]]:
    return [event_json(e) for e in history]


def judgments_json(judgments: frozenset[Observation] | list[Observation]) -> list[dict[str, object]]:
    return [judgment_json(j) for j in sorted(judgments, key=repr)]


def key_json(key: tuple[object, ...]) -> list[object]:
    """A canonical key as it is rendered: tuples become lists."""
    return [list(part) if isinstance(part, tuple) else part for part in key]


def judgment_domain(max_marks: int) -> list[Observation]:
    """Every judgment of the closed grammar naming a mark below ``max_marks``."""
    out: list[Observation] = [OnSide(i, s) for i in range(max_marks) for s in (0, 1)]
    out.extend(SideNamed(s, n) for s in (0, 1) for n in SIDE_NAMES)
    return out


def regime_domain(reading: str, max_marks: int) -> list[Regime]:
    """Every hypothetical placement of up to ``max_marks`` marks; none admitted."""
    out: list[Regime] = []
    for n in range(max_marks + 1):
        marks = tuple(f"m{i}" for i in range(n))
        for placement in product((0, 1), repeat=n):
            out.append(Regime(reading, marks, placement))
    return out


def invariant_under_permitted_renamings(j: Observation, domain: list[Regime]) -> bool:
    """Whether ``j`` holds equally at every regime of the domain and at every
    image of it under a permitted renaming of its reading."""
    return all(
        observation_holds(image, j) == observation_holds(r, j)
        for r in domain
        for _reflected, _pi, image in permitted_images(r)
    )


def separating_judgments(a: Regime, b: Regime, judgments: list[Observation]) -> list[Observation]:
    return [j for j in judgments if observation_holds(a, j) != observation_holds(b, j)]


def probes(token: str) -> list[Event]:
    """Events offered to the empty event-follows relation; none applied."""
    return [Supply(token), AdmitMark(token, 0), AdmitMark(token, 1)]


def refusal(history: list[Event], base: Regime) -> str | None:
    """The message certifying replay refuses a history with, or ``None``."""
    try:
        replay(history, base)
    except AdmissionError as exc:
        return str(exc)
    return None


def one_step_admissions(r: Regime, presented: frozenset[str]) -> list[AdmitMark]:
    """The declared finite candidate space of admissions after a history.

    One candidate per presented, not yet admitted token and per side, in a
    deterministic order.  Deterministic computation over metatheory: it
    enumerates and applies nothing; a candidate becomes state only through
    ``replay`` of a history that contains it, and no history the caller
    supplied at Challenge 1 contains one.  It lives here and not in the
    kernel because the Challenge 0 generator census fired on it there.
    """
    return [
        AdmitMark(token, side)
        for token in sorted(presented - set(r.marks))
        for side in (0, 1)
    ]


def event_returning_functions_by_module() -> dict[str, list[str]]:
    """The Challenge 0 census, run over the kernel and the metatheory modules.

    The kernel must report none.  The metatheory modules name their event
    constructors and the bounded enumerator; each takes a read whole, a
    token, or a declared candidate space, and none is applied to state by
    anything but ``replay`` of an explicit history.
    """
    return {
        "model": state_event_generators(model),
        "presentation": state_event_generators(presentation),
        "challenge1": state_event_generators(sys.modules[__name__]),
    }


def supply_facts(reading: str, g: Regime, history: list[Event]) -> Json:
    after = replay(history, g)
    return {
        "history": history_json(history),
        "regime_equals_genesis": after == g,
        "certifies_genesis": certify(history, g, g),
        "observations_unchanged": observations(after) == observations(g),
        "holding_judgments_before": len(observations(g)),
        "holding_judgments_after": len(observations(after)),
        "mentioned": sorted(mentioned(history)),
        "supplied": sorted(supplied(history)),
        "admitted": list(after.marks),
        "sides_collapsed": sides_collapsed(after),
    }


def current_state_facts(g: Regime, history: list[Event], candidate_regimes: list[Regime]) -> Json:
    """The current state after the challenge: the replay of the caller's
    history, which is the supply alone.  No candidate is designated.

    ``admitted_candidate_is_current`` is membership: whether the current
    regime equals one of the candidate regimes, each the replay of the
    supplied-only history extended by one candidate admission.  An earlier
    version computed it as "the current regime has at least one mark",
    which a caller history admitting any other token would have made true
    with no Challenge 1 candidate current; that proxy is WITHDRAWN.
    """
    current = replay(history, g)
    return {
        "rule": "the replay of the caller's history, which supplied and did not retain",
        "history": history_json(history),
        "placement": list(current.placement),
        "marks": current.n_marks(),
        "regime_equals_genesis": current == g,
        "certified": certify(history, g, current),
        "admitted_candidate_is_current": current in candidate_regimes,
    }


def retention_facts(g: Regime, history: list[Event], r: Regime, ev: AdmitMark) -> Json:
    """Hypothetical later events of the Challenge 1 grammar; nothing admitted.

    A supply and a re-admission of the admitted token on its own side leave
    the regime unchanged; an admission naming the other side is refused by
    certifying replay rather than absorbed; a hypothetical second admission
    of a never-supplied-by-the-caller token leaves the first mark's judgment
    holding.

    ``moving_admission_accepted_and_inert`` is the fact the frozen C1-2
    parenthetical needs for its other-side half: the re-admission naming
    the other side is accepted by certifying replay and leaves the regime
    unchanged.  It is false whenever the admission is refused, because a
    refused event has no after-state; the two facts are reported separately
    so that the scorer can read the clause literally.
    """
    readmission: list[Event] = [
        Supply(HYPOTHETICAL_TOKEN),
        Supply(ev.token),
        AdmitMark(ev.token, ev.side),
    ]
    moving: list[Event] = [AdmitMark(ev.token, 1 - ev.side)]
    growth: list[Event] = [Supply(HYPOTHETICAL_TOKEN), AdmitMark(HYPOTHETICAL_TOKEN, 1 - ev.side)]
    after_readmission = replay(history + readmission, g)
    after_growth = replay(history + growth, g)
    judgment = OnSide(0, ev.side)
    moving_refusal = refusal(history + moving, g)
    moving_inert = moving_refusal is None and replay(history + moving, g) == r
    return {
        "readmission_probe": history_json(readmission),
        "regime_unchanged_by_supply_and_readmission": after_readmission == r,
        "mark_judgment_retained_after_readmission": observation_holds(after_readmission, judgment),
        "moving_admission_probe": history_json(moving),
        "moving_admission_refused": moving_refusal is not None,
        "moving_admission_refusal": moving_refusal,
        "moving_admission_accepted_and_inert": moving_inert,
        "growth_probe": history_json(growth),
        "mark_judgment_retained_after_growth": observation_holds(after_growth, judgment),
        "growth_regime_has_two_marks": after_growth.n_marks() == 2,
    }


def candidate_facts(reading: str, g: Regime, supplied_history: list[Event], ev: AdmitMark) -> Json:
    history = supplied_history + [ev]
    r = replay(history, g)
    after_supply = replay(supplied_history, g)
    other = 1 - ev.side
    return {
        "event": event_json(ev),
        "history": history_json(history),
        "certified": certify(history, g, r),
        "unsupplied_admission_refused": not certify([ev], g, r),
        "marks": r.n_marks(),
        "placement": list(r.placement),
        "canonical_key": key_json(canonical(r)),
        "side_profiles": [profile_json(side_profile(r, 0)), profile_json(side_profile(r, 1))],
        "sides_collapsed": sides_collapsed(r),
        "new_observations": judgments_json(new_observations(after_supply, r)),
        "mark_profile": judgments_json(mark_profile(r, 0)),
        "other_side_judgment_holds": observation_holds(r, OnSide(0, other)),
        "name_observations_unchanged": name_observations(r) == name_observations(g),
        "holding_judgments": len(observations(r)),
        "event_follows_relation_empty": all(
            not event_follows(r, e) for e in probes(ev.token) + probes(HYPOTHETICAL_TOKEN)
        ),
        "initial_datum_unchanged": r.initial_datum == g.initial_datum,
        "reading_unchanged": r.reading == reading,
        "mentioned": sorted(mentioned(history)),
        "supplied": sorted(supplied(history)),
        "admitted": list(r.marks),
        "retention": retention_facts(g, history, r, ev),
    }


def convention_facts(reading: str, g: Regime, whole: Whole, supplied_history: list[Event]) -> Json:
    """The declared convention selects a candidate admission; it admits nothing."""
    candidate_event = admission_event(whole, DECLARED_CONVENTION)
    other_event = admission_event(whole, OTHER_CONVENTION)
    candidate = replay(supplied_history + [candidate_event], g)
    other = replay(supplied_history + [other_event], g)
    witness = isomorphism_witness(candidate, other)
    judgments = judgment_domain(JUDGMENT_DOMAIN_MAX_MARKS)
    domain = regime_domain(reading, REGIME_DOMAIN_MAX_MARKS)
    separating = separating_judgments(candidate, other, judgments)
    invariant_separating = [
        j for j in separating if invariant_under_permitted_renamings(j, domain)
    ]
    return {
        "declared": DECLARED_CONVENTION,
        "conventions": {name: dict(sides) for name, sides in CONVENTIONS.items()},
        "presented_side": whole.presented_side,
        "candidate_event": event_json(candidate_event),
        "other_event": event_json(other_event),
        "candidate_placement": list(candidate.placement),
        "other_placement": list(other.placement),
        "candidates_equal": candidate == other,
        "other_is_reflection_of_candidate": reflect(candidate) == other,
        "isomorphic_under_reading": is_isomorphic(candidate, other),
        "isomorphism_witness": (
            None if witness is None else {"reflected": witness[0], "permutation": list(witness[1])}
        ),
        "judgment_domain_max_marks": JUDGMENT_DOMAIN_MAX_MARKS,
        "regime_domain_max_marks": REGIME_DOMAIN_MAX_MARKS,
        "separating_judgments": judgments_json(separating),
        "permitted_renaming_invariant_separating_judgments": judgments_json(invariant_separating),
        "selection_is_by": "declared convention, not proof; the convention admits nothing",
    }


def candidate_classes(g: Regime, supplied_history: list[Event], candidates: list[AdmitMark]) -> list[Json]:
    """The candidates grouped by canonical key; every class is retained."""
    classes: dict[tuple[object, ...], list[dict[str, object]]] = {}
    for ev in candidates:
        key = canonical(replay(supplied_history + [ev], g))
        classes.setdefault(key, []).append(event_json(ev))
    return [
        {"canonical_key": key_json(key), "members": members}
        for key, members in sorted(classes.items(), key=lambda item: repr(item[0]))
    ]


def reading_facts(reading: str) -> Json:
    g = genesis(reading)
    whole = read_whole(INSCRIPTION)
    supplied_history: list[Event] = [supply_event(whole)]
    candidates = one_step_admissions(replay(supplied_history, g), supplied(supplied_history))
    candidate_rows = [candidate_facts(reading, g, supplied_history, ev) for ev in candidates]
    candidate_regimes = [replay(supplied_history + [ev], g) for ev in candidates]
    classes = candidate_classes(g, supplied_history, candidates)
    return {
        "reading": reading,
        "whole": {"token": whole.token, "presented_side": whole.presented_side},
        "genesis_sides_collapsed": sides_collapsed(g),
        "genesis_holding_judgments": len(observations(g)),
        "supply": supply_facts(reading, g, supplied_history),
        "current_state": current_state_facts(g, supplied_history, candidate_regimes),
        "candidate_space": {
            "declared": "each supplied, not yet admitted token on each side",
            "count": len(candidates),
            "classes_under_isomorphism": len(classes),
        },
        "candidates": candidate_rows,
        "candidate_classes": classes,
        "convention": convention_facts(reading, g, whole, supplied_history),
    }


def score_c0x(u: Json, o: Json, observation_kinds: list[str], event_kinds: list[str]) -> Json:
    """Score the Challenge 0 extrapolation against the Challenge 1 facts.

    C0-X is conditional on the mark being admitted on a side, so it is
    scored against every certified candidate, not against a current state.
    """
    no_augmentation = (
        observation_kinds == ["OnSide", "SideNamed"]
        and event_kinds == ["Supply", "AdmitMark"]
        and all(
            [e["kind"] for e in c["history"]] == ["Supply", "AdmitMark"] for c in u["candidates"]
        )
    )
    u_half = (
        bool(u["genesis_sides_collapsed"])
        and all(not c["sides_collapsed"] for c in u["candidates"])
        and no_augmentation
    )
    o_half = not o["genesis_sides_collapsed"] and all(
        not c["sides_collapsed"]
        and c["new_observations"] == [{"kind": "OnSide", "mark": 0, "side": c["event"]["side"]}]
        and c["name_observations_unchanged"]
        for c in o["candidates"]
    )

    def verdict(hit: bool) -> str:
        return "HIT" if hit else "MISSED"

    return {
        "status": verdict(u_half and o_half),
        "label": "NOT FORCED",
        "U_half_status": verdict(u_half),
        "O_half_status": verdict(o_half),
        "evidence": (
            "U: genesis collapsed, every certified one-mark candidate not, with a "
            "history of one supply and one admission and no new event kind or "
            "judgment form; O: the sides were distinct and remain so, and the only "
            "new holding judgment of every candidate is the mark's own side"
        ),
    }


def score(
    u: Json,
    o: Json,
    observation_kinds: list[str],
    event_kinds: list[str],
    state_changing: list[str],
) -> Json:
    """Mechanical scoring of the frozen Challenge 1 predictions and of C0-X."""
    both = (u, o)
    cands = [c for rd in both for c in rd["candidates"]]

    def verdict(hit: bool) -> str:
        return "HIT" if hit else "MISSED"

    c1_1 = all(
        rd["supply"]["regime_equals_genesis"]
        and rd["supply"]["certifies_genesis"]
        and rd["supply"]["observations_unchanged"]
        for rd in both
    )
    # C1-2's facts: the mark enters the admitted state only through the
    # admission event, refused without the prior supply; and no ACCEPTED
    # later event of the grammar removes or moves the mark.  The moving
    # admission satisfies that either by being refused (no after-state) or
    # by being accepted and leaving the regime unchanged; accepted and not
    # inert is the falsifier "an event that moves the admitted mark".
    c1_2_facts = all(rd["supply"]["admitted"] == [] for rd in both) and all(
        c["certified"]
        and c["unsupplied_admission_refused"]
        and c["retention"]["regime_unchanged_by_supply_and_readmission"]
        and c["retention"]["mark_judgment_retained_after_readmission"]
        and (
            c["retention"]["moving_admission_refused"]
            or c["retention"]["moving_admission_accepted_and_inert"]
        )
        and c["retention"]["mark_judgment_retained_after_growth"]
        for c in cands
    )
    # The frozen parenthetical reads "a re-admission of the same token on
    # either side, which is designation and not duplication": an accepted
    # later event on either side that leaves the mark's judgment unchanged.
    # Its same-side half is the no-op above; its other-side half is scored
    # literally and hits only if the moving admission is accepted and
    # inert.  The kernel refuses it, so the clause is a literal miss with
    # the facts hitting: PARTIAL, by the rule that scored C1-4.  An earlier
    # version labelled the clause SHARPENED from the overall boolean with no
    # clause fact; that label is WITHDRAWN.
    c1_2_either_side = all(
        c["retention"]["regime_unchanged_by_supply_and_readmission"]
        and c["retention"]["moving_admission_accepted_and_inert"]
        for c in cands
    )
    c1_3 = all(
        rd["supply"]["holding_judgments_after"] == rd["supply"]["holding_judgments_before"]
        for rd in both
    ) and all(
        c["new_observations"] == [{"kind": "OnSide", "mark": 0, "side": c["event"]["side"]}]
        and c["mark_profile"] == c["new_observations"]
        and not c["other_side_judgment_holds"]
        and c["name_observations_unchanged"]
        for c in cands
    ) and all(
        c["holding_judgments"] == rd["supply"]["holding_judgments_after"] + 1
        for rd in both
        for c in rd["candidates"]
    )
    uc = u["convention"]
    c1_4_facts = (
        all(not c["sides_collapsed"] for c in u["candidates"])
        and not uc["candidates_equal"]
        and uc["other_is_reflection_of_candidate"]
        and u["candidate_space"]["classes_under_isomorphism"] == 1
        and uc["isomorphic_under_reading"]
        and uc["permitted_renaming_invariant_separating_judgments"] == []
    )
    # The frozen clause reads "the admission is the only event in the
    # history".  A supply is an event by definition 5, so the clause is
    # scored literally and, separately, on the weaker reading "the only
    # state-changing event"; a literal miss with a weaker hit is PARTIAL.
    c1_4_only_event = all(len(c["history"]) == 1 for c in u["candidates"])
    c1_4_only_state_changing = all(
        [e["kind"] for e in c["history"] if e["kind"] in state_changing] == ["AdmitMark"]
        for c in u["candidates"]
    )
    oc = o["convention"]
    c1_5_facts = (
        oc["declared"] in oc["conventions"]
        and o["candidate_space"]["count"] == 2
        and all(c["certified"] for c in o["candidates"])
        and not oc["candidates_equal"]
        and o["candidate_space"]["classes_under_isomorphism"] == 2
        and not oc["isomorphic_under_reading"]
        and oc["other_is_reflection_of_candidate"]
        and len(o["candidate_classes"]) == 2
        and oc["candidate_event"] in [c["event"] for c in o["candidates"]]
    )
    # The frozen clause "the designation is by convention and not by proof"
    # was first scored as current-state designation of the convention's
    # admitted candidate.  The caller supplied and did not retain, so no
    # admitted candidate is current; that reading is scored here as it was
    # read, and fails.  The convention's selection of a candidate survives.
    c1_5_designated_current = bool(o["current_state"]["admitted_candidate_is_current"])
    c1_6 = (
        all(
            c["event_follows_relation_empty"] and c["initial_datum_unchanged"] and c["reading_unchanged"]
            for c in cands
        )
        and observation_kinds == ["OnSide", "SideNamed"]
        and event_kinds == ["Supply", "AdmitMark"]
    )
    c1_7 = all(c["initial_datum_unchanged"] and c["marks"] == 1 for c in cands) and all(
        rd["genesis_holding_judgments"] == rd["supply"]["holding_judgments_before"] for rd in both
    ) and c1_6

    return {
        "C0-X": score_c0x(u, o, observation_kinds, event_kinds),
        "C1-1": {
            "status": verdict(c1_1),
            "label": "FORCED",
            "evidence": "supply.regime_equals_genesis, certifies_genesis, observations_unchanged",
        },
        "C1-2": {
            "status": (
                "MISSED"
                if not c1_2_facts
                else "HIT"
                if c1_2_either_side
                else "PARTIAL"
            ),
            "label": "FORCED",
            "facts_status": verdict(c1_2_facts),
            "either_side_readmission_clause_status": verdict(c1_2_either_side),
            "either_side_readmission_clause_fact": (
                "the frozen parenthetical reads a re-admission of the same token on "
                "either side as an accepted later event that leaves the mark's "
                "judgment unchanged; a re-admission on the mark's own side is such "
                "an event, and one naming the other side is refused by certifying "
                "replay, so the clause is false as written and is scored as "
                "written; the word designation is reserved for current-state "
                "designation"
            ),
            "evidence": (
                "no mark after supply alone; every candidate certified only with the "
                "prior supply; a supply and a same-side re-admission leave the regime "
                "unchanged; no accepted event moves or duplicates the mark, the "
                "moving admission being refused; the hypothetical growth probe "
                "leaves the mark's judgment holding; the other-side half of the "
                "parenthetical is a literal miss"
            ),
        },
        "C1-3": {
            "status": verdict(c1_3),
            "label": "FORCED",
            "evidence": (
                "supply adds no holding judgment; each candidate adds exactly its "
                "OnSide judgment, the other side's does not hold, names unchanged"
            ),
        },
        "C1-4": {
            "status": (
                "MISSED"
                if not c1_4_facts
                else "HIT"
                if c1_4_only_event
                else "PARTIAL"
                if c1_4_only_state_changing
                else "MISSED"
            ),
            "label": "FORCED",
            "facts_status": verdict(c1_4_facts),
            "only_event_clause_status": verdict(c1_4_only_event),
            "only_state_changing_event_status": verdict(c1_4_only_state_changing),
            "evidence": (
                "U profiles differ after one admission; the candidates are unequal, "
                "each the other's reflection, one isomorphism class, and no "
                "permitted-renaming-invariant judgment of the bounded domain separates "
                "them; the clause 'the admission is the only event in the history' is "
                "false as written, the history being one supply and one admission, and "
                "is scored on the reading 'the only state-changing event'"
            ),
        },
        "C1-5": {
            "status": (
                "MISSED"
                if not c1_5_facts
                else "HIT"
                if c1_5_designated_current
                else "PARTIAL"
            ),
            "label": "NOT FORCED",
            "facts_status": verdict(c1_5_facts),
            "current_state_designation_status": verdict(c1_5_designated_current),
            "evidence": (
                "a declared convention; two certified O candidates in two classes, "
                "not isomorphic, the other the reflection of the convention's "
                "candidate; both classes retained; the convention selects a candidate "
                "admission; the clause 'the designation is by convention' was first "
                "scored as current-state designation of the admitted candidate, which "
                "conflated supply with admission and is withdrawn: the caller "
                "supplied and did not retain, so no admitted candidate is current"
            ),
        },
        "C1-6": {
            "status": verdict(c1_6),
            "label": "FORCED",
            "evidence": (
                "the event-follows relation is empty on every candidate; the initial "
                "datum and reading are unchanged; no new event kind or judgment form"
            ),
        },
        "C1-7": {
            "status": verdict(c1_7),
            "label": "NOT FORCED",
            "result_basis": (
                "DEFINITION-level: the regime type represents neither a second "
                "datum nor a second boundary, so the mechanical part holds by "
                "construction and is not counted as content; the modelling clause "
                "is a decision only a later challenge can falsify"
            ),
            "mechanical_part": (
                "initial_datum_unchanged, which the regime type fixes and which no "
                "receipt can report false; and marks == 1, a proxy reading 'the mark "
                "placed on a side' as exactly one placed mark, which the frozen text "
                "does not name"
            ),
            "evidence": (
                "every certified regime keeps the one initial datum and places one "
                "mark; no second datum or boundary appears in any regime because "
                "none is representable; the whole-as-datum question is left OPEN "
                "for Challenge 5"
            ),
        },
        "C1-X": {
            "status": "PENDING",
            "label": "NOT FORCED",
            "evidence": "scored by Challenge 2",
        },
    }


def build() -> Json:
    u = reading_facts(READING_U)
    o = reading_facts(READING_O)
    observation_kinds = observation_vocabulary()
    event_kinds = [t.__name__ for t in EVENT_TYPES]
    return {
        "challenge": 1,
        "inscription": INSCRIPTION,
        "seed_sha256": SEED_SHA256,
        "predictions_sha256": PREDICTIONS_SHA256,
        "challenge0_predictions_sha256": C0_PREDICTIONS_SHA256,
        "readings": {READING_U: u, READING_O: o},
        "event_kinds": event_kinds,
        "state_changing_event_kinds": list(STATE_CHANGING_EVENT_KINDS),
        "state_event_generators": state_event_generators(),
        "event_returning_functions_by_module": event_returning_functions_by_module(),
        "observation_vocabulary": observation_kinds,
        "what_the_challenge_exercises": {
            "supply": "yes: the Supply event of the read whole's mark",
            "mention": "yes: the token is named by the supply and by every candidate admission",
            "admission": (
                "examined: applied only in the certified candidate histories, "
                "never by the supply, and never by the caller at this challenge"
            ),
            "current-state designation": (
                "yes: the current state is the replay of the caller's history, the "
                "supply alone, and equals genesis; no admission candidate is current"
            ),
            "retention": (
                "probed: a supply and a same-side re-admission leave the admitted "
                "mark's judgment holding; a moving admission is refused"
            ),
            "observation": "yes: one new OnSide judgment holds after a candidate admission",
            "side": "yes: the presented side, mapped to an admitted side by convention",
            "equality": (
                "yes: structural regime equality, distinct from the isomorphism relation"
            ),
        },
        "boundary_dependence": BOUNDARY_DEPENDENCE,
        "scores": score(u, o, observation_kinds, event_kinds, STATE_CHANGING_EVENT_KINDS),
        "authority_effect": "None",
    }
