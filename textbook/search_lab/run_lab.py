"""Reproduce the search lesson using the sealed kernel read-only.

AuthorityEffect: None. The packet is teaching evidence over declared finite
populations, not a general refinement proof or an authorization protocol.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "code"))

from derivation import candidates, engine, export, iso, model, observe  # noqa: E402

BOUNDS = candidates.Bounds(2, 2)
WATCHED = (candidates, engine, export, iso, model, observe)


def jsonable(value):
    return json.loads(json.dumps(value))


def digest(value) -> str:
    return hashlib.sha256(export.dumps_deterministic(value)).hexdigest()


def delta_record(delta) -> list[dict]:
    return export.delta_json(delta)


def child(base, target, delta):
    return model.replay((model.Impose(*target),) + candidates.delta_events(base, delta), base)


def witness_record(regime, target):
    witness = observe.witness(regime, *target)
    if witness is None:
        return None
    return {"form": witness[0], "slots": list(witness[1]),
            "derivable": [observe.derivable(regime, observe.plug(witness, d)) for d in target]}


def group_responses(base, target, deltas) -> list[dict]:
    grouped = defaultdict(list)
    reference = defaultdict(list)
    for index, delta in enumerate(deltas):
        regime = child(base, target, delta)
        grouped[iso.canonical(regime)].append(index)
        reference[iso.canonical_bruteforce(regime)].append(index)
    # Refined and brute-force keys need not have the same values. Their
    # equivalence classes must agree, which is the property the lesson uses.
    assert sorted(sorted(v) for v in grouped.values()) == sorted(sorted(v) for v in reference.values())
    classes = []
    for members in sorted(grouped.values(), key=lambda xs: xs[0]):
        rep = child(base, target, deltas[members[0]])
        mappings = []
        for index in members:
            actual = child(base, target, deltas[index])
            mapping = iso.find_iso(actual, rep)
            assert mapping is not None
            dmap, fmap = mapping
            assert iso.serialize(actual, dmap, fmap) == iso.serialize(
                rep, tuple(range(rep.n_data())), tuple(range(len(rep.forms))))
            mappings.append({"member": index, "dmap": list(dmap), "fmap": list(fmap)})
        classes.append({"members": members, "representative": delta_record(deltas[members[0]]),
                        "witness": witness_record(rep, target), "mappings_to_representative": mappings})
    return classes


def search_case(base, target, bounds) -> dict:
    snapshot = export.regime_json(base)
    layers = []
    valid = []
    for count in range(bounds.max_items + 1):
        all_deltas = tuple(candidates.iter_full_deltas(base, count, bounds))
        accepted = tuple(d for d in all_deltas if candidates.response_valid_naive(base, target, d))
        layers.append({"items": count, "well_formed": len(all_deltas), "valid": len(accepted)})
        valid.extend(accepted)
    results = {}
    for measure, cost_fn in (("mu1", candidates.mu1), ("mu2", candidates.mu2)):
        actual = candidates.min_responses(base, target, measure, bounds)
        if not valid:
            assert actual is None
            results[measure] = None
            continue
        least = min(cost_fn(d) for d in valid)
        expected = {d for d in valid if cost_fn(d) == least}
        assert actual is not None and set(actual.deltas) == expected
        assert actual.complete_within == bounds
        assert actual.cost == ((least, -1) if measure == "mu1" else least)
        deltas = actual.deltas
        results[measure] = {"display_cost": jsonable(least), "api_cost": list(actual.cost),
                            "raw_minima": [delta_record(d) for d in deltas],
                            "classes": group_responses(base, target, deltas)}
    assert export.regime_json(base) == snapshot, "A search must not mutate its base"
    return {"base": snapshot, "target": list(target), "bounds": vars(bounds),
            "layers": layers, "results": results}


def preservation_cases() -> dict:
    history = engine.READING_L.genesis + (
        model.Impose(0, 1), model.AdmitForm(1), model.AdmitInst(0, (0,)), model.AdmitDatum("C"))
    base = model.replay(history)
    alternatives = {
        "mark_B_on_old_form": (candidates.NewInst(0, (1,)),),
        "mark_C_on_old_form": (candidates.NewInst(0, (2,)),),
        "new_unary_form_marking_B": (candidates.NewForm(1), candidates.NewInst(1, (1,))),
    }
    out = {}
    for protect_ac in (False, True):
        regime = model.step(base, model.Impose(0, 2)) if protect_ac else base
        rows = []
        for name, delta in alternatives.items():
            after = candidates.apply_delta(regime, delta)
            rows.append({"name": name, "delta": delta_record(delta), "items": len(delta),
                         "admission_well_formed": True,
                         "valid_response": candidates.response_valid_naive(regime, (1, 2), delta),
                         "separated_AB_AC_BC": [observe.separable(after, *p) for p in ((0, 1), (0, 2), (1, 2))]})
        out["AB_and_AC_protected" if protect_ac else "only_AB_protected"] = {
            "before": export.regime_json(regime), "alternatives": rows,
            "search_one_item": search_case(regime, (1, 2), candidates.Bounds(1, 2)),
            "search_two_items": search_case(regime, (1, 2), BOUNDS)}
    assert [row["valid_response"] for row in out["only_AB_protected"]["alternatives"]] == [False, True, True]
    assert [row["valid_response"] for row in out["AB_and_AC_protected"]["alternatives"]] == [False, False, True]
    return out


def build_packet() -> tuple[dict, dict]:
    pins = {}
    for module in WATCHED:
        path = Path(module.__file__).resolve()
        assert path.is_relative_to(ROOT / "code"), f"Unexpected kernel origin: {path}"
        # The digest is explicitly over decoded text with normalized LF
        # endings, so Windows checkout transport does not change the census.
        pins[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
    cases = {}
    for reading in engine.READINGS:
        base = model.replay(reading.genesis)
        for arity in (1, 2, 3):
            cases[f"{reading.name}_arity_{arity}"] = search_case(base, reading.target, candidates.Bounds(2, arity))
    # Record all 14 well-formed two-item plans in the main case, including
    # the eight failures. The smaller-cost layers are recorded above.
    base = model.replay(engine.READING_L.genesis)
    plans = []
    for delta in candidates.iter_full_deltas(base, 2, BOUNDS):
        after = child(base, (0, 1), delta)
        plans.append({"delta": delta_record(delta), "valid": observe.satisfies(after),
                      "witness": witness_record(after, (0, 1))})
    assert len(plans) == 14 and sum(row["valid"] for row in plans) == 6
    try:
        model.step(base, model.AdmitInst(0, (0,)))
    except model.AdmissionError as error:
        malformed = str(error)
    else:
        raise AssertionError("An instance on an absent form must be refused")

    stopping = {}
    settings = {
        "all_separated": dict(max_rounds=1, pre_expansion_node_guard=40, supply=False),
        "round_limit": dict(max_rounds=0, pre_expansion_node_guard=40, supply=True),
        "node_guard": dict(max_rounds=5, pre_expansion_node_guard=0, supply=True),
        "guard_40_is_not_a_hard_cap": dict(max_rounds=5, pre_expansion_node_guard=40, supply=True),
        "no_response_with_one_item": dict(max_rounds=1, pre_expansion_node_guard=40, supply=False),
    }
    for name, options in settings.items():
        bounds = candidates.Bounds(1, 2) if name == "no_response_with_one_item" else BOUNDS
        tree = engine.build_tree(engine.READING_L, "mu1", bounds, **options)
        stopping[name] = {"settings": {**options, "bounds": vars(bounds)}, "stats": tree.stats()}
    assert stopping["all_separated"]["stats"]["by_status"] == {"expanded": 1, "terminal_all_separated": 3}
    assert stopping["round_limit"]["stats"]["by_status"] == {"completed": 1}
    assert stopping["node_guard"]["stats"]["by_status"] == {"frontier_guard": 1}
    assert stopping["guard_40_is_not_a_hard_cap"]["stats"]["nodes"] == 41
    assert stopping["no_response_with_one_item"]["stats"]["by_status"] == {"terminal_no_response": 1}

    tree = engine.build_tree(engine.READING_L, "mu1", BOUNDS, max_rounds=5,
                             pre_expansion_node_guard=400, supply=True)
    full = export.tree_full_json(tree)
    assert (len(full["nodes"]), len(full["edges"]), sum(e.kind == "merge" for e in tree.edges)) == (128, 130, 3)
    assert tree.stats()["by_status"] == {"expanded": 36, "completed": 92}
    assert export.verify_full_export(full)
    corrupt_hash = deepcopy(full)
    corrupt_hash["nodes"][0]["regime_sha256"] = "0" * 64
    corrupt_map = deepcopy(full)
    merge = next(edge for edge in corrupt_map["edges"] if edge["kind"] == "merge")
    merge["merge_iso"]["dmap"] = []
    corrupt_cost = deepcopy(full)
    corrupt_cost["edges"][0]["cost"] = [999, 999]
    checks = {"ordinary_export": export.verify_full_export(full),
              "wrong_root_hash": export.verify_full_export(corrupt_hash),
              "missing_merge_map": export.verify_full_export(corrupt_map),
              "changed_cost_metadata": export.verify_full_export(corrupt_cost)}
    assert checks == {"ordinary_export": True, "wrong_root_hash": False,
                      "missing_merge_map": False, "changed_cost_metadata": True}
    packet = {"schema": 1, "authority_effect": "None",
              "source_digest_mode": "SHA-256 of UTF-8 decoded text with LF line endings",
              "source_text_sha256": pins,
              "main_reading": "L", "main_bounds": vars(BOUNDS),
              "root_history": [export.event_json(e) for e in engine.READING_L.genesis],
              "cases": cases, "all_main_two_item_plans": plans,
              "malformed_instance_error": malformed,
              "preservation": preservation_cases(), "stopping": stopping,
              "extended_export": {"file": "reading_L_mu1_rounds5.json", "sha256": digest(full),
                                  "stats": tree.stats(),
                                  "merge_edges": sum(e.kind == "merge" for e in tree.edges),
                                  "replay_checks": checks}}
    return jsonable(packet), jsonable(full)


def check_recorded(directory: Path = SOURCE) -> dict:
    expected, full = build_packet()
    recorded = json.loads((directory / "recorded_lab.json").read_text(encoding="utf-8"))
    actual_export = json.loads((directory / "reading_L_mu1_rounds5.json").read_text(encoding="utf-8"))
    if recorded != expected:
        raise ValueError("Recorded lesson data differs from the source-backed finite search; regenerate and review")
    if actual_export != full or not export.verify_full_export(actual_export):
        raise ValueError("Recorded export differs from the independently replayed graph")
    # Bind the published population table to the computed cases. Matching
    # names in prose would not establish that the numerical lesson is current.
    rows = re.findall(r"^\| ([LF]) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|$",
                      (SOURCE / "SOURCE_MAP.md").read_text(encoding="utf-8"), re.MULTILINE)
    observed_rows = {(reading, int(arity)): tuple(map(int, values)) for reading, arity, *values in rows}
    expected_rows = {}
    for name, case in expected["cases"].items():
        reading, _, arity = name.split("_")
        layer = case["layers"][2]
        expected_rows[(reading, int(arity))] = (layer["well_formed"], layer["valid"], len(case["results"]["mu1"]["classes"]))
    if observed_rows != expected_rows or len(rows) != 6:
        raise ValueError("The lesson population table differs from the computed cases")
    return {"search_cases": len(expected["cases"]) + 4, "main_plans": 14,
            "export_nodes": len(full["nodes"]), "export_edges": len(full["edges"]),
            "merge_edges": expected["extended_export"]["merge_edges"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="regenerate the two teaching records outside the seal")
    parser.add_argument("--directory", type=Path, default=SOURCE)
    args = parser.parse_args()
    if args.write:
        packet, full = build_packet()
        args.directory.mkdir(parents=True, exist_ok=True)
        export.write_json(args.directory / "recorded_lab.json", packet)
        export.write_json(args.directory / "reading_L_mu1_rounds5.json", full)
    print(json.dumps(check_recorded(args.directory), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
