"""Stage 4: finite saturation under the declared admission procedure.

The instruction calculation is represented; endogenous admission and obligation
meaning remain unproved. No change to native rules. AuthorityEffect: None.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import product
from typing import Iterator

from derivation.model import (
    AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, Event, Inst, Pair, Regime, replay,
)
from derivation.observe import derivable, separable
import emitter as e
from materialize import validate


def slots(r: Regime) -> frozenset[Inst]:
    """Coarse carrier, including binary tuples on forms of other arities."""
    return frozenset((f, (x, y)) for f in range(len(r.forms))
                     for x, y in product(range(r.n_data()), repeat=2))


def budget(r: Regime) -> int:
    return len(slots(r) - r.insts)


@dataclass(frozen=True)
class Run:
    states: tuple[Regime, ...]
    batches: tuple[tuple[Event, ...], ...]


def run(r: Regime) -> Run:
    """Store every batch until an empty one; enforce a finite initial bound."""
    validate(r)
    states = [r]
    batches: list[tuple[Event, ...]] = []
    for _ in range(budget(r) + 1):
        after, batch = e.emit(states[-1])
        if not batch:
            if after != states[-1]:
                raise ValueError("EMPTY_ROUND_CHANGED")
            return Run(tuple(states), tuple(batches))
        states.append(after)
        batches.append(batch)
    raise ValueError("ROUND_BOUND_EXCEEDED")


def reference_closure(r: Regime) -> frozenset[Inst]:
    """Serial carrier scan, independent of raw path enumeration and replay."""
    stored = set(r.insts)
    codes = tuple(a for f, a in sorted(r.insts) if f == 0 and len(a) == 3)
    while True:
        previous = len(stored)
        for k, l, o in codes:
            for x, z, y in product(range(r.n_data()), repeat=3):
                target = (3 + o, (x, y))
                if (x < y and (3 + k, (x, z)) in stored and (3 + l, (z, y)) in stored
                        and e.well_formed(r, target)):
                    stored.add(target)
        if len(stored) == previous:
            return frozenset(stored)


def audit(r: Regime, result: Run) -> None:
    validate(r)
    if (not result.states or result.states[0] != r or
            len(result.states) != len(result.batches) + 1):
        raise ValueError("ROUND_POPULATION")
    if len(result.batches) > budget(r):
        raise ValueError("ROUND_BOUND")
    for before, after, batch in zip(result.states, result.states[1:], result.batches):
        if not batch:
            raise ValueError("EMPTY_RECORDED_BATCH")
        e.audit(before, after, batch)
        if e.instructions(before.insts) != e.instructions(after.insts):
            raise ValueError("INSTRUCTIONS_CHANGED")
        if budget(after) >= budget(before):
            raise ValueError("NO_STRICT_DECREASE")
    last = result.states[-1]
    if any(e.well_formed(last, i) and i not in last.insts for i in e.reference_outputs(last)):
        raise ValueError("TERMINAL_NOT_CLOSED")
    if last.insts != reference_closure(r):
        raise ValueError("TERMINAL_NOT_LEAST")
    events = tuple(event for batch in result.batches for event in batch)
    if replay(events, base=r) != last:
        raise ValueError("DYNAMICS_REPLAY")


def history(n: int, relation: tuple[Pair, ...], program: bool, cover: bool) -> tuple[Event, ...]:
    return (tuple(AdmitDatum(str(i)) for i in range(n)) +
            tuple(AdmitForm(a) for a in (3, 1, 1, 2)) +
            ((AdmitInst(0, (0, 0, 0)),) if program else ()) +
            tuple(AdmitInst(3, edge) for edge in relation) +
            tuple(AdmitRuleAll(f) for f in range(4 if cover else 3)))


def configurations() -> Iterator[tuple[Event, ...]]:
    """Every relation on 0..3 active data, program/coverage toggled.

    One extra admitted datum keeps the all-zero instruction valid at size zero.
    The extra datum is not used as a graph endpoint. Four forms are admitted.
    """
    for n in range(4):
        for relation in e.all_relations(n):
            for program, cover in product((False, True), repeat=2):
                yield history(n + 1, relation, program, cover)


def sweep() -> dict[str, object]:
    population = rounds = admissions = stored = 0
    distribution: Counter[int] = Counter()
    for seed in configurations():
        initial = replay(seed)
        result = run(initial)
        audit(initial, result)
        events = tuple(event for batch in result.batches for event in batch)
        if replay(seed + events) != result.states[-1]:
            raise ValueError("DYNAMICS_WHOLE_HISTORY")
        population += 1
        rounds += len(result.batches)
        admissions += len(events)
        stored += len(result.states[-1].insts - initial.insts)
        distribution[len(result.batches)] += 1
    return {"configurations": population, "strict_rounds_total": rounds,
            "admission_events": admissions, "distinct_new_instances": stored,
            "round_count_distribution": {str(k): v for k, v in sorted(distribution.items())},
            "active_data_bound": 3, "additional_data_per_state": 1, "forms": 4}


def chain_sample(cover: bool) -> dict[str, object]:
    seed = history(4, ((0, 1), (1, 2), (2, 3)), True, cover)
    initial = replay(seed)
    result = run(initial)
    audit(initial, result)
    terminal = result.states[-1]
    events = tuple(event for batch in result.batches for event in batch)
    payload = (3, (0, 3))
    record: dict[str, object] = {
        "output_covered": cover, "data_count": 4, "forms": (3, 1, 1, 2),
        "instruction": (0, 0, 0), "initial_edges": ((0, 1), (1, 2), (2, 3)),
        "initial_budget": budget(initial), "strict_rounds": len(result.batches),
        "admissions_per_round": [len(batch) for batch in result.batches],
        "new_instances_per_round": [len(b.insts - a.insts) for a, b in zip(result.states, result.states[1:])],
        "terminal_edges": e.edges(terminal.insts, 3),
        "operand_functional_per_state": [e.functional(state.insts, 3) for state in result.states],
        "payload_initially_stored": payload in initial.insts,
        "payload_initially_derivable": derivable(initial, payload),
        "pair_initially_separable": separable(initial, 0, 3),
        "pair_terminal_separable": separable(terminal, 0, 3),
        "requirements_after": sorted(terminal.reqs),
        "whole_replay": replay(seed + events) == terminal,
    }
    if cover:
        response: tuple[Event, ...] = (AdmitForm(1), AdmitInst(4, (0,)))
        answered = replay(response, base=terminal)
        if (not separable(answered, 0, 3) or payload not in answered.insts or
                replay(seed + events + response) != answered):
            raise ValueError("CHAIN_RESPONSE")
        record["response"] = (("AdmitForm", 1), ("AdmitInst", 4, (0,)))
        record["whole_response_replay"] = True
        record["answered_payload_retained"] = True
    return record


def report() -> dict[str, object]:
    return {"stage": 4, "outcome": "OPEN", "authority_effect": "None",
            "dynamics": "Finite saturation of the declared host admission law on fixed data/forms",
            "bound": "Strict rounds at most initially absent binary slots; at most form_count * data_count^2",
            "terminal": "Least closed extension by instance membership on the same data/forms",
            "scope": "No interleaved carrier growth, response, or other event; no bound on duplicate path events",
            "sweep": sweep(), "chain_samples": [chain_sample(cover) for cover in (False, True)],
            "E1": "OPEN: computation and termination do not prove native admission or obligation meaning",
            "E2_literal": "NOT_SATISFIED: requirements unchanged at every round",
            "E2_owed_separation": "Conditional covered witnesses; obligation role remains declared",
            "E3": "Earlier unruled singleton fails; covered chain stays collapsed at every round",
            "E4": "Covered terminal chain and earlier reading samples have valid responses and whole replay",
            "next_stage": "Reconcile claims and current main, then local integration and publication"}
