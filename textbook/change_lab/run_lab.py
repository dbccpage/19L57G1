"""Reproduce the passage lesson over three natural-number positions.

AuthorityEffect: None. Uses sealed sources read-only. Finite comparisons
do not establish a general Python-to-Lean refinement or model transport.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, replace
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "code"))
from derivation import primitive_passage as passage, represented  # noqa: E402

PAIRS = ((0, 1), (0, 2), (1, 2))
TARGET = (1, 2)
COLUMNS = tuple(c for size in range(4) for c in combinations(range(3), size))
HISTORY = tuple(("admitOcc", t) for t in (10, 20, 30)) + tuple(
    event for pair in PAIRS for event in (("assertWit", *pair), ("admitWit", *pair))
) + (("protect", 0, 1), ("protect", 1, 2), ("declareObs",),
     ("setBudget", 2), ("addCol", (0,)))


def plain(value):
    return json.loads(json.dumps(value))


def state_record(state):
    return plain(asdict(state))


def expect_natural_encoding(state):
    """Bound the teaching encoding; the raw Python API also accepts ints.

    This is a teaching-input guard, not a claim that the sealed Python
    mirror rejects all negative integers as Lean's Nat type does.
    """
    for token in state.occ:
        if type(token) is not int or token < 0:
            raise ValueError("The teaching carrier uses natural-number tokens")
    for pair in state.asserted + state.wit + state.prot + state.refusals:
        if len(pair) != 2 or any(type(p) is not int or not 0 <= p < len(state.occ) for p in pair):
            raise ValueError("Pair endpoints must be admitted natural-number positions")
    if state.obs is not None:
        for column in state.obs:
            if any(type(p) is not int or not 0 <= p < len(state.occ) for p in column):
                raise ValueError("Column entries must be admitted natural-number positions")
    if type(state.budget) is not int or state.budget < 0:
        raise ValueError("The teaching budget is a natural number")


def describe(state):
    expect_natural_encoding(state)
    declared = state.obs is not None
    if declared:
        assert len(state.occ) == 3, "The declared-observation lab uses exactly three occurrences"
    answers = None if not declared else [[i in c for c in state.obs] for i in range(3)]
    menu = passage.response_menu(state)
    repairs = passage.repair_family_p(state, *TARGET)
    # Independent direct calculation on the declared column/position menu.
    expected_repairs = []
    for column, point in menu:
        changed = tuple(((point,) + c) if c == column else c for c in state.obs)
        separates = lambda cols, pair: any((pair[0] in c) != (pair[1] in c) for c in cols)
        active = lambda pair: pair in state.wit and pair in state.prot and not separates(state.obs, pair)
        structural = (point not in column
                      and any(active(r) and ((r[0] in (point,) + column) != (r[1] in (point,) + column)) for r in state.prot)
                      and all(not separates(state.obs, r) or separates(changed, r) for r in state.prot))
        assert passage.refine_ok(state, column, point) == structural
        if structural and separates(changed, TARGET):
            expected_repairs.append((column, point))
    assert repairs == expected_repairs
    target_zero = None if not declared else not any(answers[TARGET[0]][q] != answers[TARGET[1]][q] for q in range(len(state.obs)))
    active = TARGET in state.wit and TARGET in state.prot and declared and target_zero
    assert passage.obst_p(state, *TARGET) == bool(active)
    return {"state": state_record(state), "answers": answers,
            "retained": TARGET in state.wit, "protected": TARGET in state.prot,
            "declared": declared, "zero_on_target": target_zero,
            "active": bool(active), "response_menu": plain(menu), "repairs": plain(repairs),
            "singleton_proposals": plain(passage.extension_proposals(state, *TARGET)),
            "next_blocks": plain(passage.next_family_p(state)),
            "reachable_store_invariant": set(state.prot) <= set(state.wit) <= set(state.asserted)}


def snapshot_timeline(history, start=passage.GENESIS_P):
    state = start
    rows = [{"event": None, **describe(state)}]
    for event in history:
        before = state
        state = passage.pstep(state, event)
        assert set(before.wit) <= set(state.wit)
        assert set(state.prot) <= set(state.wit) <= set(state.asserted)
        rows.append({"event": plain(event), "changed": state != before, **describe(state)})
    assert state == passage.preplay(history, start)
    return rows


def operation_case(state, event):
    before = describe(state)
    after = passage.pstep(state, event)
    after_record = describe(after)
    structural = passage.refine_ok(state, event[1], event[2]) if event[0] == "refineCol" else passage.col_ok(state, event[1])
    return {"event": plain(event), "changed": after != state,
            "gates": {"structural_ok": structural, "budget_positive": state.budget > 0,
                      "permission_required": event[0] == "addCol", "permission_on": state.licensed,
                      "not_halted": not state.halted},
            "resolved_target": before["active"] and not after_record["active"],
            "after": after_record}


def build_packet():
    source_pins = {}
    for module in (passage, represented):
        path = Path(module.__file__).resolve()
        assert path.is_relative_to(ROOT / "code")
        source_pins[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_text(encoding="utf-8").encode()).hexdigest()
    timeline = snapshot_timeline(HISTORY)
    base = passage.preplay(HISTORY, passage.GENESIS_P)
    strong = passage.pstep(base, ("protect", 0, 2))
    assert base.obs == ((0,),) and base.budget == 1 and base.prot == ((0, 1), (1, 2))
    assert passage.repair_family_p(base, *TARGET) == [((0,), 2)]
    assert passage.repair_family_p(strong, *TARGET) == []

    operations = {}
    for protection, initial in (("two_pairs", base), ("all_pairs", strong)):
        for budget, licensed, halted in product((0, 1, 2), (False, True), (False, True)):
            # All variations are obtained by legal events on the same carrier.
            history = (("setBudget", budget), ("setLicense", licensed)) + ((("halt",),) if halted else ())
            state = passage.preplay(history, initial)
            key = f"{protection}_{budget}_{int(licensed)}_{int(halted)}"
            row = {"before": describe(state), "variations": plain(history),
                   "refine_C": operation_case(state, ("refineCol", (0,), 2)),
                   "add_B": operation_case(state, ("addCol", (1,)))}
            assert row["refine_C"]["changed"] == (protection == "two_pairs" and budget > 0 and not halted)
            assert row["add_B"]["changed"] == (budget > 0 and licensed and not halted)
            operations[key] = row

    # Compare raw records separately from reachable event histories.
    gates = []
    for retained, protected, obs in product((False, True), (False, True), (None, (), ((0,),), ((0,), (1,)))):
        state = passage.PS(occ=(10, 20, 30), asserted=(TARGET,),
                           wit=(TARGET,) if retained else (), prot=(TARGET,) if protected else (), obs=obs)
        row = describe(state)
        row["zero_total_convention"] = True if obs is None else passage.zero_p(obs, *TARGET)
        assert row["active"] == (retained and protected and row["declared"] and row["zero_total_convention"])
        gates.append(row)
    assert len(gates) == 16 and sum(row["active"] for row in gates) == 2
    assert sum(not row["reachable_store_invariant"] for row in gates) == 4
    assert {(row["declared"], row["zero_total_convention"]) for row in gates} == {(False, True), (True, True), (True, False)}

    columns = []
    for column in COLUMNS:
        after = passage.pstep(strong, ("addCol", column))
        columns.append({"column": list(column), "structural_ok": passage.col_ok(strong, column),
                        "in_singleton_family": column in passage.extension_proposals(strong, *TARGET),
                        "accepted": after != strong, "resolves": not passage.obst_p(after, *TARGET),
                        "after": state_record(after)})
    assert sum(row["structural_ok"] for row in columns) == 4
    assert sum(row["in_singleton_family"] for row in columns) == 2
    column_counts = {"base": sum(passage.col_ok(base, c) for c in COLUMNS),
                     "strong": sum(passage.col_ok(strong, c) for c in COLUMNS)}
    assert column_counts == {"base": 4, "strong": 4}

    unfunded_unlicensed = passage.preplay((("setBudget", 0), ("setLicense", False)), strong)
    refusal_events = (("refuse", *TARGET), ("setLicense", True), ("setBudget", 1), ("addCol", (1,)))
    refusal = snapshot_timeline(refusal_events, unfunded_unlicensed)
    assert refusal[-1]["state"]["refusals"] == [[1, 2]] and not refusal[-1]["active"]
    terminal = snapshot_timeline((("halt",),) + refusal_events[1:], unfunded_unlicensed)
    assert terminal[-1]["active"] and terminal[-1]["state"]["halted"]
    assert all(not row["changed"] for row in terminal[2:])
    generated = []
    for block in passage.next_family_p(unfunded_unlicensed):
        result = passage.preplay(block, unfunded_unlicensed)
        generated.append({"events": plain(block), "after": describe(result), "changed": result != unfunded_unlicensed})
    assert len(generated) == 2 and all(row["changed"] and row["after"]["active"] for row in generated)

    # This is a comparison of two specific encodings, not a transport theorem.
    comparison = []
    for label, state in (("repair_available", base), ("existing_menu_exhausted", strong)):
        world = represented.World(data=state.occ, views=state.obs, reqs=state.prot, budget=state.budget)
        p_refusal = passage.pstep(state, ("refuse", *TARGET))
        w_refusal = represented.step(world, ("refuse", *TARGET))
        comparison.append({"case": label, "passage_active": passage.obst_p(state, *TARGET),
                           "world_exhausted_obstruction": represented.obstructed(world, TARGET),
                           "passage_refusal_recorded": p_refusal != state,
                           "world_refusal_recorded": w_refusal != world})
    assert comparison[0] == {"case": "repair_available", "passage_active": True,
                             "world_exhausted_obstruction": False, "passage_refusal_recorded": True,
                             "world_refusal_recorded": False}

    return plain({"schema": 1, "authority_effect": "None", "carrier": [10, 20, 30],
                  "source_text_sha256": source_pins, "digest_mode": "UTF-8 source text with LF normalization",
                  "history": HISTORY, "timeline": timeline, "base": describe(base), "strong": describe(strong),
                  "operations": operations, "gate_records": gates, "canonical_columns": columns,
                  "column_counts": column_counts,
                  "refusal_trace": refusal, "halt_trace": terminal,
                  "generated_unlicensed_blocks": generated, "model_comparison": comparison})


def check_recorded(directory=SOURCE):
    expected = build_packet()
    actual = json.loads((directory / "recorded_lab.json").read_text(encoding="utf-8"))
    if actual != expected:
        raise ValueError("Recorded passage lesson differs from the source-backed computations")
    text = (SOURCE / "SOURCE_MAP.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\| (A/B and B/C protected|All three pairs protected) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|$", text, re.MULTILINE)
    observed = {label: tuple(map(int, values)) for label, *values in rows}
    wanted = {}
    for label, key in (("A/B and B/C protected", "base"), ("All three pairs protected", "strong")):
        row = expected[key]
        wanted[label] = (len(row["response_menu"]), len(row["repairs"]), len(row["singleton_proposals"]), expected["column_counts"][key])
    if len(rows) != 2 or observed != wanted:
        raise ValueError("Passage lesson population table differs from the checked source cases")
    return {"gate_records": len(expected["gate_records"]), "operational_settings": len(expected["operations"]),
            "guarded_events": 2 * len(expected["operations"]), "canonical_columns": 8,
            "singleton_proposals": 2}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.write:
        SOURCE.mkdir(parents=True, exist_ok=True)
        (SOURCE / "recorded_lab.json").write_text(json.dumps(build_packet(), indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(check_recorded(), sort_keys=True))
