"""Stage 2: finite uniform closure through existing instance admissions.

The procedure and the demand reading are declared host operations. Neither is
claimed to be a represented endogenous emitter. AuthorityEffect: None.
"""

from __future__ import annotations

from itertools import combinations, product

from derivation.model import (
    AdmissionError, AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll,
    Event, Inst, Pair, Regime, replay, step,
)
from derivation.observe import derivable, profiles, separable, witness
from probe import configurations


def validate(r: Regime) -> None:
    """Reject malformed direct constructions before enumerating consequences."""
    if any(a < 1 for a in r.forms):
        raise AdmissionError("FORM_ARITY")
    if any(not 0 <= f < len(r.forms) for f in r.rules):
        raise AdmissionError("RULE_FORM")
    for f, args in r.insts:
        if not (0 <= f < len(r.forms) and len(args) == r.forms[f]
                and all(0 <= x < r.n_data() for x in args)):
            raise AdmissionError("INSTANCE_SHAPE")
    if any(not 0 <= x < y < r.n_data() for x, y in r.reqs):
        raise AdmissionError("REQUIREMENT_SHAPE")


def uniform_instances(r: Regime) -> tuple[Inst, ...]:
    validate(r)
    return tuple((f, args) for f in sorted(r.rules)
                 for args in product(range(r.n_data()), repeat=r.forms[f]))


def pending(r: Regime) -> tuple[Inst, ...]:
    return tuple(i for i in uniform_instances(r) if i not in r.insts)


def materialize(r: Regime) -> tuple[Regime, tuple[Event, ...]]:
    """Keep every fresh well-formed uniform conclusion; choose no target pair."""
    events: tuple[Event, ...] = tuple(AdmitInst(f, args) for f, args in pending(r))
    after = r
    for event in events:
        after = step(after, event)
    return after, events


def read_pairs(r: Regime) -> tuple[Pair, ...]:
    """Declared meaning for stored binary form 0; retains all strict pairs.

    This reading does not consult requirements or observational profiles.
    Giving these instances the role of obligations is still a convention.
    """
    return tuple(sorted((args[0], args[1]) for f, args in r.insts
                        if f == 0 and len(args) == 2 and args[0] < args[1]))


def audit(before: Regime, after: Regime, events: tuple[Event, ...]) -> None:
    # Independently enumerate all well-formed derivable instances, including
    # non-rule forms, rather than use the candidate's uniform enumerator.
    expected = before.insts | frozenset(
        (f, args) for f, a in enumerate(before.forms)
        for args in product(range(before.n_data()), repeat=a)
        if derivable(before, (f, args)))
    if (before.data, before.forms, before.rules, before.reqs) != (
            after.data, after.forms, after.rules, after.reqs):
        raise ValueError("FIELDS_CHANGED")
    if after.insts != expected:
        raise ValueError("CLOSURE_INCOMPLETE_OR_UNSOUND")
    fresh = expected - before.insts
    if (len(events) != len(fresh) or
            any(not isinstance(e, AdmitInst) for e in events) or
            frozenset((e.form, e.args) for e in events if isinstance(e, AdmitInst)) != fresh):
        raise ValueError("ADMISSION_TRACE")
    if replay(events, base=before) != after:
        raise ValueError("REPLAY_MISMATCH")
    if profiles(before) != profiles(after):
        raise ValueError("OBSERVATIONS_CHANGED")


def sweep() -> dict[str, int]:
    states = admissions = fixed_points = 0
    for _, before in configurations():
        after, events = materialize(before)
        audit(before, after, events)
        again, second = materialize(after)
        audit(after, again, second)
        if again != after or second:
            raise ValueError("NOT_A_FIXED_POINT")
        states += 1
        admissions += len(events)
        fixed_points += 1
    return {"states": states, "new_admissions": admissions,
            "verified_fixed_points": fixed_points,
            "data_bound": 3, "binary_forms": 1, "requirements_per_state": 0}


def sample(reading: str) -> dict[str, object]:
    if reading not in {"L", "F"}:
        raise ValueError("READING: expected L or F")
    tokens = ("a", "b") if reading == "L" else ("seed", "a", "b")
    seed: tuple[Event, ...] = tuple(AdmitDatum(t) for t in tokens) + (
        AdmitForm(2), AdmitRuleAll(0))
    before = replay(seed)
    after, events = materialize(before)
    audit(before, after, events)
    pairs = read_pairs(after)
    expected_pairs = tuple(combinations(range(len(tokens)), 2))
    if read_pairs(before) or pairs != expected_pairs or any(separable(after, x, y) for x, y in pairs):
        raise ValueError("UNMET_PAIR_WITNESS")
    # A shared response separates every pair by n-1 fresh unary forms.
    # This is an explicit witness, with no optimality or uniqueness claim.
    response: tuple[Event, ...] = tuple(e for x in range(len(tokens) - 1)
                                       for e in (AdmitForm(1), AdmitInst(1 + x, (x,))))
    answered = replay(response, base=after)
    if replay(seed + events + response) != answered or not all(
            separable(answered, x, y) for x, y in pairs):
        raise ValueError("ANSWER_WITNESS")
    return {"reading": reading, "data_count": len(tokens),
            "fresh_instances": len(events), "read_pairs": pairs,
            "all_read_pairs_were_unmet": True, "requirements_after": sorted(after.reqs),
            "response_events": [(type(e).__name__, e.arity) if isinstance(e, AdmitForm)
                                else (type(e).__name__, e.form, e.args)
                                for e in response if isinstance(e, (AdmitForm, AdmitInst))],
            "separating_contexts": [witness(answered, x, y) for x, y in pairs],
            "read_pairs_after_answer": read_pairs(answered),
            "whole_history_replayed": True}


def report() -> dict[str, object]:
    return {"stage": 2, "outcome": "OPEN", "authority_effect": "None",
            "result": "Uniform materialization is conservative, finite, and idempotent",
            "sweep": sweep(), "samples": [sample("L"), sample("F")],
            "E1": "OPEN: admission procedure and obligation reading remain host operations",
            "E2_literal": "NOT_SATISFIED: requirements are unchanged",
            "E2_owed_separation": "Conditional witness under the declared instance reading",
            "E3": "Fresh stored pairs remain unseparated in the two reachable samples",
            "E4": "Existing admissions separate all pairs in both replayed samples",
            "next_stage": "Represent the emitter and prove its semantic bridge"}
