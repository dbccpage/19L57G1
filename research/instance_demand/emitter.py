"""Stage 3: stored instructions compose stored edges, retaining every path.

The interpreter and its output-admission operation are declared host apparatus.
The computation bridge does not establish endogenous admission or obligation.
AuthorityEffect: None.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
from typing import Iterator

from derivation.model import (
    AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, Event, Impose, Inst, Pair, Regime, replay,
)
from derivation.observe import derivable, profiles, separable, witness
from materialize import validate


def instructions(insts: frozenset[Inst]) -> tuple[tuple[int, int, int], ...]:
    return tuple((a[0], a[1], a[2]) for f, a in sorted(insts) if f == 0 and len(a) == 3)


def edges(insts: frozenset[Inst], form: int) -> tuple[Pair, ...]:
    return tuple((a[0], a[1]) for f, a in sorted(insts) if f == form and len(a) == 2)


def raw_outputs(insts: frozenset[Inst]) -> tuple[Inst, ...]:
    """Form 0 holds (k,l,o); operation indices refer to binary forms 3+index.

    Repeated output tuples retain distinct path witnesses. No first match is
    selected. The ordering serializes all stored instructions and edges.
    """
    return tuple((3 + o, (x, y)) for k, l, o in instructions(insts)
                 for x, z in edges(insts, 3 + k) for middle, y in edges(insts, 3 + l)
                 if z == middle and x < y)


def well_formed(r: Regime, item: Inst) -> bool:
    f, args = item
    return (0 <= f < len(r.forms) and len(args) == r.forms[f]
            and all(0 <= x < r.n_data() for x in args))


def pending(r: Regime) -> tuple[Inst, ...]:
    validate(r)
    return tuple(i for i in raw_outputs(r.insts) if well_formed(r, i) and i not in r.insts)


def emit(r: Regime) -> tuple[Regime, tuple[Event, ...]]:
    events: tuple[Event, ...] = tuple(AdmitInst(f, args) for f, args in pending(r))
    return replay(events, base=r), events


def functional(insts: frozenset[Inst], form: int) -> bool:
    pairs = edges(insts, form)
    return len({x for x, _ in pairs}) == len(pairs)


def lookup_unique(insts: frozenset[Inst], form: int, x: int) -> int | None:
    values = tuple(y for a, y in edges(insts, form) if a == x)
    return values[0] if len(values) == 1 else None


def eval_word(insts: frozenset[Inst], word: tuple[int, ...], start: int) -> int | None:
    """Graph reader; only the functional case is identified with Execution."""
    active = start
    for k in word:
        value = lookup_unique(insts, 3 + k, active)
        if value is None:
            return None
        active = value
    return active


def reference_outputs(r: Regime) -> tuple[Inst, ...]:
    """Independent carrier enumeration, testing instance membership directly."""
    return tuple((3 + a[2], (x, y))
                 for f, a in sorted(r.insts) if f == 0 and len(a) == 3
                 for x, z, y in product(range(r.n_data()), repeat=3)
                 if x < y and (3 + a[0], (x, z)) in r.insts and (3 + a[1], (z, y)) in r.insts)


def audit(r: Regime, after: Regime, events: tuple[Event, ...]) -> int:
    expected_raw = reference_outputs(r)
    if Counter(raw_outputs(r.insts)) != Counter(expected_raw):
        raise ValueError("PATH_POPULATION")
    expected = tuple(i for i in expected_raw if well_formed(r, i) and i not in r.insts)
    if ((r.data, r.forms, r.rules, r.reqs) != (after.data, after.forms, after.rules, after.reqs)
            or after.insts != r.insts | frozenset(expected)):
        raise ValueError("EMISSION_ENDPOINT")
    if (any(not isinstance(e, AdmitInst) for e in events) or
            Counter((e.form, e.args) for e in events if isinstance(e, AdmitInst)) != Counter(expected)):
        raise ValueError("EMISSION_TRACE")
    if replay(events, base=r) != after:
        raise ValueError("EMISSION_REPLAY")
    bridged = 0
    for k, l, o in instructions(r.insts):
        if functional(r.insts, 3 + k) and functional(r.insts, 3 + l):
            for x in range(r.n_data()):
                y = eval_word(r.insts, (k, l), x)
                if y is not None and x < y:
                    if (3 + o, (x, y)) not in expected_raw:
                        raise ValueError("EXECUTION_BRIDGE")
                    bridged += 1
    return bridged


def history(n: int, left: tuple[Pair, ...], right: tuple[Pair, ...],
            program: bool, cover: bool) -> tuple[Event, ...]:
    return (tuple(AdmitDatum(str(i)) for i in range(n)) +
            tuple(AdmitForm(a) for a in (3, 1, 1, 2, 2, 2)) +
            ((AdmitInst(0, (0, 1, 2)),) if program else ()) +
            tuple(AdmitInst(3, p) for p in left) + tuple(AdmitInst(4, p) for p in right) +
            tuple(AdmitRuleAll(f) for f in range(6 if cover else 5)))


def all_relations(n: int) -> Iterator[tuple[Pair, ...]]:
    pairs = tuple((x, y) for x in range(n) for y in range(n))
    for mask in range(1 << len(pairs)):
        yield tuple(p for j, p in enumerate(pairs) if mask & (1 << j))


def all_functional_relations(n: int) -> Iterator[tuple[Pair, ...]]:
    for values in product(range(-1, n), repeat=n):
        yield tuple((x, y) for x, y in enumerate(values) if y >= 0)


def configurations() -> Iterator[tuple[Event, ...]]:
    """All two-relation subsets on 0..2 active data, and all functional pairs on 3.

    There are three additional admitted data in each state so the instruction
    codes are valid. Those data do not occur in the enumerated graph edges.
    """
    for n in range(3):
        for left, right in product(tuple(all_relations(n)), repeat=2):
            for program, cover in product((False, True), repeat=2):
                yield history(n + 3, left, right, program, cover)
    for left, right in product(tuple(all_functional_relations(3)), repeat=2):
        yield history(6, left, right, True, True)


def sweep() -> dict[str, int]:
    states = admissions = stored = bridge_paths = no_program = 0
    for seed in configurations():
        r = replay(seed)
        after, events = emit(r)
        bridge_paths += audit(r, after, events)
        if replay(seed + events) != after:
            raise ValueError("WHOLE_HISTORY")
        states += 1
        admissions += len(events)
        stored += len(after.insts - r.insts)
        if not instructions(r.insts):
            no_program += 1
            if events:
                raise ValueError("MISSING_INSTRUCTION")
    return {"states": states, "admission_events": admissions, "distinct_new_instances": stored,
            "functional_execution_paths": bridge_paths, "states_without_instruction": no_program}


def sample(reading: str, cover: bool) -> dict[str, object]:
    if reading not in {"L", "F"}:
        raise ValueError("READING")
    n, x, z, y = (3, 0, 2, 1) if reading == "L" else (4, 1, 3, 2)
    seed = history(n, ((x, z),), ((z, y),), True, cover)
    before = replay(seed)
    after, events = emit(before)
    audit(before, after, events)
    payload = (5, (x, y))
    if (pending(before) != (payload,) or separable(before, x, y) or
            separable(after, x, y) == cover or any(isinstance(e, Impose) for e in seed + events)):
        raise ValueError("SAMPLE_BOUNDARY")
    record: dict[str, object] = {
        "reading": reading, "data_count": n, "pair": (x, y), "intermediate": z,
        "instruction": (0, 1, 2), "output_covered": cover,
        "payload_previously_stored": payload in before.insts,
        "payload_previously_derivable": derivable(before, payload),
        "pair_already_separated_by_emission": separable(after, x, y),
        "requirements_after": sorted(after.reqs), "contains_impose": False,
        "computed_endpoint": eval_word(before.insts, (0, 1), x),
        "whole_emission_replay": replay(seed + events) == after,
    }
    without_program = replay(history(n, ((x, z),), ((z, y),), False, cover))
    record["outputs_without_instruction"] = raw_outputs(without_program.insts)
    record["same_profiles_without_instruction"] = profiles(before) == profiles(without_program)
    if cover:
        response: tuple[Event, ...] = (AdmitForm(1), AdmitInst(6, (x,)))
        answered = replay(response, base=after)
        if not separable(answered, x, y) or replay(seed + events + response) != answered:
            raise ValueError("SAMPLE_RESPONSE")
        record["response_context"] = witness(answered, x, y)
        record["whole_response_replay"] = True
    return record


def report() -> dict[str, object]:
    return {"stage": 3, "outcome": "OPEN", "authority_effect": "None",
            "candidate_class": "One-pass stored ternary instructions composing two stored binary edges",
            "sweep": sweep(),
            "samples": [sample(reading, cover) for reading in ("L", "F") for cover in (False, True)],
            "bridge": "Computed outputs agree with represented execution on functional operand graphs",
            "E1": "OPEN: output admission and obligation meaning remain additional host operations",
            "E2_literal": "NOT_SATISFIED: requirements unchanged",
            "native_inference": "REFUTED for this join schema by a reachable unruled-output counterexample",
            "E3": "Unruled singleton output separates its pair; covered output remains unmet conditionally",
            "E4": "Covered two-reading samples have existing responses and whole replay",
            "next_stage": "Assess the scoped outcome and dynamics without claiming E1"}
