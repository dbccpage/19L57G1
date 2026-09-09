"""Enumerated candidates on the reqs channel, each with a named failing clause.

Classification: deterministic computation plus declared records.  The class
``C_reqs`` is non-empty: every row below is a candidate a reader would try.
None satisfies E1 ∧ E2 ∧ E3 on that channel.  I1 is the instance-channel
remainder, outside ``C_reqs``, recorded OPEN.

The word *endogenous* is never applied to a row.  A row that claims it
is a guard failure (G1, G5).

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Callable

from derivation.engine import closure_challenge_orbits
from derivation.model import (
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Event,
    Impose,
    Pair,
    Regime,
    Supply,
    replay,
)
from derivation.observe import collapsed_pairs, separable

from grammar import e2_violation, imposes_in, is_impose, last_event_extends_reqs
from reader import read_pairs_of_regime

CLAUSES: tuple[str, ...] = ("E1", "E2", "E3", "E4")
REQUIRED_IDS: tuple[str, ...] = (
    "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "I1",
)
OUTCOME = "B"
CLASS_NAME = "C_reqs"


def host_next_demand(regime: Regime) -> Pair | None:
    """The core sin: a host function that inspects the regime and picks a pair."""
    pairs = collapsed_pairs(regime)
    if not pairs:
        return None
    return pairs[0]


def host_holds(i: int, j: int) -> bool:
    """Standing-commitment analogue: a host predicate, not an admitted instance."""
    return i != j


def _two_data() -> tuple[Event, ...]:
    return (Supply("a"), AdmitDatum("a"), Supply("b"), AdmitDatum("b"))


def _marked_two_data() -> tuple[Event, ...]:
    return _two_data() + (AdmitForm(1), AdmitInst(0, (0,)))


def witness_c1() -> dict[str, object]:
    regime = replay(_two_data())
    picked = host_next_demand(regime)
    return {
        "picked": list(picked) if picked is not None else None,
        "reqs": [list(p) for p in sorted(regime.reqs)],
        "host_function": "host_next_demand",
        "e2_violation": None,
    }


def witness_c2() -> dict[str, object]:
    base = replay(_two_data())
    orbits = closure_challenge_orbits(base)
    history = _two_data() + tuple(Impose(i, j) for i, j in orbits)
    regime = replay(history)
    return {
        "orbits": [list(p) for p in orbits],
        "impose_events": [list(p) for p in imposes_in(history)],
        "reqs": [list(p) for p in sorted(regime.reqs)],
        "last_is_impose": is_impose(history[-1]) if history else False,
        "e2_violation": e2_violation(history),
    }


def witness_c3() -> dict[str, object]:
    supplied = _two_data() + (Impose(0, 1),)
    laundered = supplied + (AdmitForm(2), AdmitInst(0, (0, 1)))
    regime = replay(laundered)
    copied = (0, 1)
    return {
        "supplied_pair": [0, 1],
        "copied_pair": list(copied),
        "identical_to_supplied": copied in replay(supplied).reqs,
        "instance": [0, [0, 1]],
        "reqs": [list(p) for p in sorted(regime.reqs)],
    }


def witness_c4() -> dict[str, object]:
    history = _two_data() + (AdmitForm(2), AdmitRuleAll(0))
    regime = replay(history)
    return {
        "reqs": [list(p) for p in sorted(regime.reqs)],
        "rules": sorted(regime.rules),
        "changed_reqs": last_event_extends_reqs(history),
        "e2_violation": e2_violation(history),
    }


def witness_c5() -> dict[str, object]:
    grown = replay(_two_data() + (Supply("c"), AdmitDatum("c")))
    demanded = [
        [i, j]
        for i in range(grown.n_data())
        for j in range(i + 1, grown.n_data())
        if host_holds(i, j)
    ]
    return {
        "host_predicate": "host_holds",
        "host_demanded": demanded,
        "reqs": [list(p) for p in sorted(grown.reqs)],
        "growth_event": "AdmitDatum",
        "e2_violation": e2_violation(_two_data() + (Supply("c"), AdmitDatum("c"))),
    }


def witness_c6() -> dict[str, object]:
    history = _two_data() + (Supply("c"), AdmitDatum("c"), Impose(0, 2))
    regime = replay(history)
    return {
        "impose_events": [list(p) for p in imposes_in(history)],
        "reqs": [list(p) for p in sorted(regime.reqs)],
        "last_is_impose": is_impose(history[-1]),
        "e2_violation": e2_violation(history),
    }


def witness_c9() -> dict[str, object]:
    history = _marked_two_data()
    regime = replay(history)
    pair = (0, 1)
    return {
        "pair": list(pair),
        "already_separable": separable(regime, pair[0], pair[1]),
        "reqs": [list(p) for p in sorted(regime.reqs)],
    }


def witness_i1() -> dict[str, object]:
    history = _two_data() + (AdmitForm(2), AdmitInst(0, (0, 1)))
    regime = replay(history)
    read = read_pairs_of_regime(regime, 0)
    return {
        "read_pairs": [list(p) for p in read],
        "reqs": [list(p) for p in sorted(regime.reqs)],
        "in_reqs": all(p in regime.reqs for p in read),
        "e2_violation": e2_violation(history),
        "channel": "instance",
        "status": "OPEN",
    }


WITNESSES: dict[str, Callable[[], dict[str, object]]] = {
    "C1": witness_c1,
    "C2": witness_c2,
    "C3": witness_c3,
    "C4": witness_c4,
    "C5": witness_c5,
    "C6": witness_c6,
    "C9": witness_c9,
    "I1": witness_i1,
}

# Frozen census.  ``endogenous`` is always False.  A test flips it to
# prove the G1 guard.  I1 is outside C_reqs.
CENSUS: tuple[dict[str, object], ...] = (
    {
        "id": "C1",
        "class": CLASS_NAME,
        "fails": ("E1",),
        "reason": "host next_demand inspects collapsed pairs and picks",
        "endogenous": False,
        "status": "defeated",
    },
    {
        "id": "C2",
        "class": CLASS_NAME,
        "fails": ("E1", "E2"),
        "reason": "declared closure policy; Impose is in the history",
        "endogenous": False,
        "status": "defeated",
        "cites": "CL-CLOSURE-POLICY",
    },
    {
        "id": "C3",
        "class": CLASS_NAME,
        "fails": ("E3",),
        "reason": "launders a previously supplied Impose through an instance",
        "endogenous": False,
        "status": "defeated",
    },
    {
        "id": "C4",
        "class": CLASS_NAME,
        "fails": ("E2",),
        "reason": "AdmitRuleAll changes derivability, not reqs",
        "endogenous": False,
        "status": "defeated",
    },
    {
        "id": "C5",
        "class": CLASS_NAME,
        "fails": ("E1", "E2"),
        "reason": "host holds plus external AdmitDatum; demand is not in reqs",
        "endogenous": False,
        "status": "defeated",
        "cites": "SC-8 SC-18 CL-IG-02",
    },
    {
        "id": "C6",
        "class": CLASS_NAME,
        "fails": ("E2",),
        "reason": "growth then Impose: the supplying event is in the history",
        "endogenous": False,
        "status": "defeated",
        "cites": "CL-IG-02",
    },
    {
        "id": "C7",
        "class": CLASS_NAME,
        "fails": ("E1",),
        "reason": "declared reflective rule; object-language generator not in scope",
        "endogenous": False,
        "status": "defeated",
        "cites": "GC-11 generation_never_dries",
    },
    {
        "id": "C8",
        "class": CLASS_NAME,
        "fails": ("E1",),
        "reason": "host Labeler; invariance leftover stays in second_stake",
        "endogenous": False,
        "status": "defeated",
        "cites": "ST-14 ST-24 ST-28",
    },
    {
        "id": "C9",
        "class": CLASS_NAME,
        "fails": ("E3",),
        "reason": "the pair is already internally separable",
        "endogenous": False,
        "status": "defeated",
    },
    {
        "id": "C10",
        "class": "outside",
        "fails": (),
        "reason": "new Event constructor would be a sealed-path amendment",
        "endogenous": False,
        "status": "outside_class",
    },
    {
        "id": "I1",
        "class": "instance_channel",
        "fails": ("E2",),
        "reason": "never-selects instance read never enters reqs; E2 as written fails; remainder OPEN",
        "endogenous": False,
        "status": "OPEN",
    },
)


def census_errors(rows: tuple[dict[str, object], ...] | None = None) -> tuple[str, ...]:
    """Named failures of the class-nonvacuity and endogenous-label guards."""
    table = CENSUS if rows is None else rows
    errors: list[str] = []
    ids = [str(row["id"]) for row in table]
    missing = [cid for cid in REQUIRED_IDS if cid not in ids]
    extra = [cid for cid in ids if cid not in REQUIRED_IDS]
    if missing:
        errors.append(f"CLASS_NONVACUITY: missing {missing}")
    if extra:
        errors.append(f"CLASS_NONVACUITY: extra {extra}")
    if len(ids) != len(set(ids)):
        errors.append("CLASS_NONVACUITY: duplicate ids")
    creqs = [row for row in table if row["class"] == CLASS_NAME]
    if len(creqs) < 9:
        errors.append(f"CLASS_NARROW: C_reqs has {len(creqs)} rows, need the obvious candidates")
    for row in table:
        cid = str(row["id"])
        if row.get("endogenous") is True:
            errors.append(f"E1_GUARD: {cid} labelled endogenous")
        fails = row["fails"]
        if not isinstance(fails, tuple):
            errors.append(f"CLAUSE_SHAPE: {cid} fails is not a tuple")
            continue
        for clause in fails:
            if clause not in CLAUSES:
                errors.append(f"CLAUSE_UNKNOWN: {cid} {clause}")
        if row["status"] == "defeated" and not fails:
            errors.append(f"CLAUSE_MISSING: {cid} defeated with no failing clause")
        if cid == "I1" and row["status"] != "OPEN":
            errors.append("OPEN_BOUNDARY: I1 is not recorded OPEN")
        if cid == "C10" and row["class"] != "outside":
            errors.append("OUTSIDE_CLASS: C10 must remain outside C_reqs")
    return tuple(errors)


def _census_row(row: dict[str, object]) -> dict[str, object]:
    fails = row["fails"]
    if not isinstance(fails, tuple):
        raise TypeError(f"{row['id']} fails is not a tuple")
    clauses = [str(item) for item in fails]
    out: dict[str, object] = {
        "id": row["id"],
        "class": row["class"],
        "fails": clauses,
        "reason": row["reason"],
        "endogenous": row["endogenous"],
        "status": row["status"],
    }
    if "cites" in row:
        out["cites"] = row["cites"]
    return out


def candidate_record() -> dict[str, object]:
    witnesses = {cid: WITNESSES[cid]() for cid in WITNESSES}
    return {
        "schema": "endogenous-demand-candidates-v1",
        "authority_effect": "None",
        "outcome": OUTCOME,
        "class": CLASS_NAME,
        "required_ids": list(REQUIRED_IDS),
        "census": [_census_row(row) for row in CENSUS],
        "witnesses": witnesses,
        "guard_errors": list(census_errors()),
        "dynamics": "not applicable inside C_reqs: there is no generator",
    }


def mutated_endogenous(rows: tuple[dict[str, object], ...], candidate_id: str) -> tuple[dict[str, object], ...]:
    """G1 injection: label one row endogenous."""
    out: list[dict[str, object]] = []
    for row in rows:
        if row["id"] == candidate_id:
            copy = dict(row)
            copy["endogenous"] = True
            out.append(copy)
        else:
            out.append(row)
    return tuple(out)


def mutated_narrow(rows: tuple[dict[str, object], ...]) -> tuple[dict[str, object], ...]:
    """G5 injection: drop every C_reqs row except C4."""
    return tuple(row for row in rows if row["id"] in {"C4", "C10", "I1"})
