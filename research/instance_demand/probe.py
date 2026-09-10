"""Stage 1 finite controls; event occurrence is not event authorship.

AuthorityEffect: None. All state transitions call the sealed Python model.
"""

from __future__ import annotations

from itertools import combinations, product
from typing import Iterator

from derivation.model import (
    AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, Event, Impose, Inst,
    Regime, Supply, replay, step,
)
from derivation.observe import derivable, separable, witness


def instance_events(history: tuple[Event, ...]) -> frozenset[Inst]:
    """The explicit instance-event population, without a claim about its source."""
    return frozenset((e.form, e.args) for e in history if isinstance(e, AdmitInst))


def check_step(before: Regime, event: Event, after: Regime) -> None:
    expected = before.insts
    if isinstance(event, AdmitInst):
        expected = expected | {(event.form, event.args)}
    if after.insts != expected:
        raise ValueError(f"INSTANCE_WRITER: {type(event).__name__}")


def configurations() -> Iterator[tuple[tuple[Event, ...], Regime]]:
    """Every instance subset and rule subset on one binary form, sizes 0..3.

    Requirements are empty. Every state is built by a recorded admission history.
    """
    for n in range(4):
        pairs = tuple(product(range(n), repeat=2))
        prefix: tuple[Event, ...] = tuple(AdmitDatum(str(i)) for i in range(n)) + (AdmitForm(2),)
        for mask in range(1 << len(pairs)):
            admissions = tuple(AdmitInst(0, p) for k, p in enumerate(pairs) if mask & (1 << k))
            for has_rule in (False, True):
                tail: tuple[Event, ...] = (AdmitRuleAll(0),) if has_rule else ()
                history = prefix + admissions + tail
                yield history, replay(history)


def sweep() -> dict[str, int]:
    states = transitions = uniform_conclusions = 0
    for history, before in configurations():
        states += 1
        n = before.n_data()
        pairs = tuple(product(range(n), repeat=2))
        events: tuple[Event, ...] = (
            Supply("unused"), AdmitDatum("fresh"), AdmitForm(1), AdmitForm(2), AdmitRuleAll(0),
            *(AdmitInst(0, p) for p in pairs), *(Impose(x, y) for x, y in combinations(range(n), 2)),
        )
        for event in events:
            after = step(before, event)
            check_step(before, event, after)
            if replay(history + (event,)) != after:
                raise ValueError("REPLAY_MISMATCH")
            if instance_events(history + (event,)) != after.insts:
                raise ValueError("INSTANCE_ORIGIN")
            transitions += 1
        for pair in pairs:
            item = (0, pair)
            if derivable(before, item) and item not in before.insts:
                if not all(derivable(before, (0, other)) for other in pairs):
                    raise ValueError("UNIFORM_CONCLUSION")
                uniform_conclusions += 1
    return {"states": states, "successful_transitions": transitions,
            "fresh_derivable_instances": uniform_conclusions}


def sample(reading: str, cover: bool) -> dict[str, object]:
    if reading not in {"L", "F"}:
        raise ValueError("READING: expected L or F")
    tokens = ("a", "b") if reading == "L" else ("seed", "a", "b")
    x, y = len(tokens) - 2, len(tokens) - 1
    history: tuple[Event, ...] = tuple(AdmitDatum(t) for t in tokens) + (
        AdmitForm(2), AdmitInst(0, (x, y)),
    )
    if cover:
        history += (AdmitRuleAll(0),)
    regime = replay(history)
    return {"reading": reading, "pair": [x, y], "data_count": len(tokens),
            "instance_stored": (0, (x, y)) in regime.insts,
            "rule_covered": cover, "already_separable": separable(regime, x, y),
            "separating_context": witness(regime, x, y),
            "requirements": sorted(regime.reqs),
            "contains_impose": any(isinstance(e, Impose) for e in history),
            "instance_event_present": (0, (x, y)) in instance_events(history),
            "history_event_types": [type(e).__name__ for e in history]}


def report() -> dict[str, object]:
    return {"stage": 1, "outcome": "OPEN", "authority_effect": "None",
            "scope": "Native instance provenance and finite controls, not event authorship",
            "sweep": sweep(),
            "samples": [sample(reading, cover) for reading in ("L", "F") for cover in (False, True)],
            "next_stage": "Attempt uniform closure materialization with its admission law explicit"}
