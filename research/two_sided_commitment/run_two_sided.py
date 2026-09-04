"""Write the deterministic receipts for the two-sided commitment rung.

Usage: python research/two_sided_commitment/run_two_sided.py [--out PATH] [--full PATH]

No timestamp, no environment value.  The frozen texts are hashed at run
time so an edit after the freeze shows in the receipt.  Prediction
scoring is mechanical: every verdict is a function of the computed
tables.  The summary keeps per-tree statistics, refusals, growth epochs,
and the scoring; the full export keeps every node and edge and records
its content hash in the summary.
"""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys
from typing import Sequence

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from two_sided import (  # noqa: E402
    COMMITMENTS,
    REPO,
    TEdge,
    TTree,
    build_ts_tree,
    demands,
    edge_json,
    growth_epochs,
    node_json,
    pre_growth_nodes,
    sealed_closed_counts,
    sealed_readings,
)

if str(REPO / "code") not in sys.path:
    sys.path.insert(0, str(REPO / "code"))
from derivation.candidates import Bounds  # noqa: E402
from derivation.export import Json, dumps_deterministic, write_json, write_json_gz  # noqa: E402

BOUNDS = Bounds(max_items=2, max_arity=2)
MAX_ROUNDS = 15
GUARD = 250
MAX_DATA = 5
MEASURES = ("mu1", "mu2")


def _sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _j(value: object) -> Json:
    if isinstance(value, dict):
        return {str(k): _j(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_j(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError(f"not JSON: {value!r}")


def _kinds(e: TEdge) -> list[str]:
    raw = e.info.get("kinds")
    return [str(k) for k in raw] if isinstance(raw, list) else []


def _int(v: object) -> int:
    assert isinstance(v, int)
    return v


def _status_count(t: TTree, name: str) -> int:
    by = t.stats()["by_status"]
    assert isinstance(by, dict)
    v = by.get(name, 0)
    return v if isinstance(v, int) else 0


def _honoured_count(e: TEdge) -> int:
    raw = e.info.get("honoured_at_once")
    return len(raw) if isinstance(raw, list) else 0


def _responses(t: TTree) -> list[TEdge]:
    return [e for e in t.edges if e.challenge != "grow"]


def tree_id(t: TTree) -> str:
    return f"{t.reading}/{t.commitment}/{t.measure}"


def epoch_summary(t: TTree) -> dict[str, Json]:
    epochs = growth_epochs(t)
    by_data: dict[int, dict[str, int]] = {}
    for ep in epochs:
        d = _int(ep["data_before"])
        slot = by_data.setdefault(d, {"epochs": 0, "min_demands": 10**9, "max_demands": 0, "max_rounds": 0, "unclosed": 0})
        slot["epochs"] += 1
        dem = _int(ep["demands_after_growth"])
        slot["min_demands"] = min(slot["min_demands"], dem)
        slot["max_demands"] = max(slot["max_demands"], dem)
        if ep["reached_demand_free"]:
            slot["max_rounds"] = max(slot["max_rounds"], _int(ep["rounds_to_next_demand_free"]))
        else:
            slot["unclosed"] += 1
    return {str(k): _j(v) for k, v in sorted(by_data.items())}


def tree_json(t: TTree) -> dict[str, Json]:
    responses = _responses(t)
    kinds_by_demand: dict[str, dict[str, int]] = {}
    for e in responses:
        kind = str(e.info.get("kind"))
        k = "+".join(_kinds(e))
        kinds_by_demand.setdefault(kind, {})
        kinds_by_demand[kind][k] = kinds_by_demand[kind].get(k, 0) + 1
    pre = pre_growth_nodes(t)
    return {
        "id": tree_id(t),
        "reading": t.reading,
        "commitment": t.commitment,
        "measure": t.measure,
        "stats": _j(t.stats()),
        "kinds_answered": sorted({str(e.info.get("kind")) for e in responses}),
        "kinds_by_demand": _j(kinds_by_demand),
        "edges_honouring_several": sum(1 for e in responses if _honoured_count(e) >= 2),
        "edges_with_fresh_datum": sum(1 for e in responses if e.info.get("fresh_datum")),
        "edges_with_third_party_change": sum(1 for e in responses if e.info.get("third_party_changed")),
        "refusals": [_j(r) for r in t.refusals],
        "growth": epoch_summary(t),
        "pre_growth_nodes": len(pre),
        "pre_growth_demand_free_nodes": sum(1 for nid in pre if not demands(t.nodes[nid].state)),
        "nodes": [_j(node_json(n)) for n in t.nodes],
        "edges": [_j(edge_json(e)) for e in t.edges],
    }


def build_all() -> dict[str, Json]:
    trees: list[TTree] = []
    for reading in sealed_readings():
        for c in COMMITMENTS:
            for measure in MEASURES:
                trees.append(build_ts_tree(reading, c, measure, BOUNDS, MAX_ROUNDS, GUARD, MAX_DATA))
    sealed = {
        f"{rd.name}/{m}": sealed_closed_counts(rd, m, BOUNDS)
        for rd in sealed_readings() for m in MEASURES
    }
    tj = [tree_json(t) for t in trees]
    summary = _summary(trees, tj, sealed)
    scored, detail = _score(trees, tj, sealed)
    return {
        "authority_effect": "None",
        "bounds": {"max_items": BOUNDS.max_items, "max_arity": BOUNDS.max_arity,
                   "max_rounds": MAX_ROUNDS, "pre_expansion_node_guard": GUARD, "max_data": MAX_DATA},
        "commitments": [c.name for c in COMMITMENTS],
        "prompt_sha256": _sha(HERE / "PROMPT.md"),
        "predictions_sha256": _sha(HERE / "PREDICTIONS.md"),
        "sealed_closed_baselines": {k: {"nodes": v[0], "terminal": v[1]} for k, v in sealed.items()},
        "trees": tj,
        "summary": summary,
        "predictions_scored": scored,
        "prediction_detail": detail,
    }


def _summary(trees: Sequence[TTree], tj: Sequence[dict[str, Json]], sealed: dict[str, tuple[int, int]]) -> dict[str, Json]:
    by_commitment: dict[str, dict[str, Json]] = {}
    for t, j in zip(trees, tj):
        slot = by_commitment.setdefault(t.commitment, {
            "trees": 0, "nodes": 0, "responses": 0, "growth_edges": 0,
            "kinds_answered": [], "edges_honouring_several": 0, "edges_with_fresh_datum": 0,
            "edges_with_third_party_change": 0, "refusals": 0, "refusal_data_counts": [],
            "max_data_reached": 0,
        })
        slot["trees"] = _int(slot["trees"]) + 1
        slot["nodes"] = _int(slot["nodes"]) + _int(t.stats()["nodes"])
        slot["responses"] = _int(slot["responses"]) + len(_responses(t))
        slot["growth_edges"] = _int(slot["growth_edges"]) + _int(t.stats()["growth_edges"])
        ks = slot["kinds_answered"]
        assert isinstance(ks, list)
        for k in j["kinds_answered"] if isinstance(j["kinds_answered"], list) else []:
            if k not in ks:
                ks.append(k)
        slot["edges_honouring_several"] = _int(slot["edges_honouring_several"]) + _int(j["edges_honouring_several"])
        slot["edges_with_fresh_datum"] = _int(slot["edges_with_fresh_datum"]) + _int(j["edges_with_fresh_datum"])
        slot["edges_with_third_party_change"] = _int(slot["edges_with_third_party_change"]) + _int(j["edges_with_third_party_change"])
        slot["refusals"] = _int(slot["refusals"]) + len(t.refusals)
        rd = slot["refusal_data_counts"]
        assert isinstance(rd, list)
        for r in t.refusals:
            d = r.get("data")
            if isinstance(d, int) and d not in rd:
                rd.append(d)
        slot["max_data_reached"] = max(_int(slot["max_data_reached"]), _int(t.stats()["max_data"]))
    for slot in by_commitment.values():
        ks = slot["kinds_answered"]
        rd = slot["refusal_data_counts"]
        assert isinstance(ks, list) and isinstance(rd, list)
        ks.sort()
        rd.sort()
    return {
        "trees_built": len(trees),
        "by_commitment": by_commitment,
        "all_certified": all(bool(t.stats()["all_certified"]) for t in trees),
        "flip_events_in_grammar": 0,
    }


def _score(trees: Sequence[TTree], tj: Sequence[dict[str, Json]], sealed: dict[str, tuple[int, int]]) -> tuple[dict[str, Json], dict[str, Json]]:
    def trees_of(c: str) -> list[tuple[TTree, dict[str, Json]]]:
        return [(t, j) for t, j in zip(trees, tj) if t.commitment == c]

    # Q1: both kinds answered in some run under parity and under residue_three.
    q1_runs = {
        c: [tree_id(t) for t, j in trees_of(c) if set(j["kinds_answered"] if isinstance(j["kinds_answered"], list) else []) >= {"same", "apart"}]
        for c in ("parity", "residue_three")
    }
    q1 = all(bool(v) for v in q1_runs.values())
    # Q2: one response honours several demands.
    q2_count = sum(_int(j["edges_honouring_several"]) for j in tj)
    q2 = q2_count > 0
    # Q3: growth generates under total_apart, parity, residue_three; never under total_same (chain-shaped tree).
    def growth_always_generates(c: str) -> bool:
        ok = True
        for t, _ in trees_of(c):
            for e in t.edges:
                if e.challenge == "grow" and _int(e.info.get("demands_after_growth")) == 0:
                    ok = False
        return ok
    generating = {c: growth_always_generates(c) for c in ("total_apart", "parity", "residue_three")}
    total_same_silent = all(
        all(not demands(n.state) for n in t.nodes) and all(e.challenge == "grow" for e in t.edges)
        for t, _ in trees_of("total_same")
    )
    q3 = all(generating.values()) and total_same_silent
    # Q4: no accepted minimum admits a fresh datum.
    q4_count = sum(_int(j["edges_with_fresh_datum"]) for j in tj)
    q4 = q4_count == 0
    # Q5: a refusal at four or more data under parity or residue_three.
    q5_hits = [
        {"tree": tree_id(t), "data": r.get("data"), "kind": r.get("kind"), "target": r.get("target")}
        for c in ("parity", "residue_three") for t, _ in trees_of(c) for r in t.refusals
        if isinstance(r.get("data"), int) and _int(r.get("data")) >= 4
    ]
    q5 = bool(q5_hits)
    # Q6: total_apart before growth equals the sealed closed baseline.
    q6_rows = []
    for t, j in trees_of("total_apart"):
        nodes_sealed, term_sealed = sealed[f"{t.reading}/{t.measure}"]
        row = {
            "tree": tree_id(t), "pre_growth_nodes": j["pre_growth_nodes"], "sealed_nodes": nodes_sealed,
            "pre_growth_demand_free": j["pre_growth_demand_free_nodes"], "sealed_terminal": term_sealed,
        }
        row["match"] = (j["pre_growth_nodes"] == nodes_sealed and j["pre_growth_demand_free_nodes"] == term_sealed)
        q6_rows.append(row)
    q6 = bool(q6_rows) and all(bool(r["match"]) for r in q6_rows)
    # Q7: total_apart: growth on n data yields exactly n demands, honoured within n rounds when closed.
    q7_ok = True
    q7_examples: list[dict[str, Json]] = []
    for t, _ in trees_of("total_apart"):
        for ep in growth_epochs(t):
            d = _int(ep["data_before"])
            dem = _int(ep["demands_after_growth"])
            rounds = _int(ep["rounds_to_next_demand_free"])
            closed = bool(ep["reached_demand_free"])
            bad = dem != d or (closed and rounds > d)
            if bad:
                q7_ok = False
                if len(q7_examples) < 6:
                    q7_examples.append({"tree": tree_id(t), "data_before": d, "demands": dem, "rounds": rounds, "closed": closed})
    q7 = q7_ok
    # Q8: total_apart mu1 != mu2 node counts per reading; total_same equal.
    def counts(c: str, reading: str) -> tuple[int, int]:
        m = {t.measure: _int(t.stats()["nodes"]) for t, _ in trees_of(c) if t.reading == reading}
        return (m["mu1"], m["mu2"])
    readings = sorted({t.reading for t in trees})
    q8_rows = {f"{c}/{rd}": list(counts(c, rd)) for c in ("total_apart", "total_same") for rd in readings}
    q8 = all(counts("total_apart", rd)[0] != counts("total_apart", rd)[1] for rd in readings) and all(
        counts("total_same", rd)[0] == counts("total_same", rd)[1] for rd in readings
    )
    verdicts = {"Q1": q1, "Q2": q2, "Q3": q3, "Q4": q4, "Q5": q5, "Q6": q6, "Q7": q7, "Q8": q8}
    scored: dict[str, Json] = {k: {"hit": v, "verdict": "HIT" if v else "MISS"} for k, v in verdicts.items()}
    detail: dict[str, Json] = {
        "Q1_runs_with_both_kinds": _j(q1_runs),
        "Q2_edges_honouring_several": q2_count,
        "Q3_growth_always_generates": _j(generating),
        "Q3_total_same_silent_chain": total_same_silent,
        "Q4_edges_with_fresh_datum": q4_count,
        "Q5_refusals_at_four_or_more_data": _j(q5_hits),
        "Q6_rows": _j(q6_rows),
        "Q7_counterexamples": _j(q7_examples),
        "Q8_node_counts": _j(q8_rows),
    }
    return scored, detail


def split(payload: dict[str, Json]) -> tuple[dict[str, Json], dict[str, Json]]:
    trees = payload["trees"]
    assert isinstance(trees, list)
    full: dict[str, Json] = {"authority_effect": "None", "trees": trees}
    full_sha = hashlib.sha256(dumps_deterministic(full)).hexdigest()
    summary: dict[str, Json] = {k: v for k, v in payload.items() if k != "trees"}
    summary["trees"] = [
        {k: v for k, v in t.items() if k not in ("nodes", "edges")} for t in trees if isinstance(t, dict)
    ]
    summary["full_export"] = {
        "path": "receipts/full/two_sided_commitment_full.json.gz",
        "sha256_uncompressed": full_sha,
        "contents": ["trees[].nodes", "trees[].edges"],
    }
    return summary, full


def main() -> int:
    parser = argparse.ArgumentParser(description="Write the two-sided commitment receipts.")
    parser.add_argument("--out", type=pathlib.Path, default=HERE / "receipts" / "two_sided_commitment.json")
    parser.add_argument("--full", type=pathlib.Path, default=HERE / "receipts" / "full" / "two_sided_commitment_full.json.gz")
    args = parser.parse_args()
    summary, full = split(build_all())
    write_json(args.out, summary)
    sha = write_json_gz(args.full, full)
    recorded = summary["full_export"]
    assert isinstance(recorded, dict) and recorded["sha256_uncompressed"] == sha
    scored = summary["predictions_scored"]
    assert isinstance(scored, dict)
    for k in sorted(scored, key=lambda s: int(s[1:])):
        v = scored[k]
        assert isinstance(v, dict)
        print(f"{k}: {v['verdict']}")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
