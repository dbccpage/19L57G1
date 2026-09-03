"""Write the deterministic receipt for the identification dual.

Usage: python research/identification_dual/run_dual.py [--out PATH]

The receipt carries no timestamp and no environment value.  It records
the sha256 of the frozen challenge and prediction texts as read at run
time, so an edit to either after the freeze is visible in the receipt.
Prediction scoring is mechanical: each verdict is a function of the
computed tables, never of prose.
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

from dual import (  # noqa: E402
    IDENTIFY,
    REPO,
    DEdge,
    DTree,
    Genesis,
    admitted_fresh_data,
    branch_report,
    build_dual_tree,
    dual_replay,
    edge_json,
    events_json,
    genesis_history,
    node_json,
    pair_probe,
    regime_json,
    reversal_probe,
    sealed_fixpoints,
    separated_pairs,
)

if str(REPO / "code") not in sys.path:
    sys.path.insert(0, str(REPO / "code"))
from derivation.candidates import Bounds  # noqa: E402
from derivation.export import Json, write_json  # noqa: E402

BOUNDS = Bounds(max_items=2, max_arity=2)
MAX_ROUNDS = 15
GUARD = 250
READINGS = ("P", "R")
MEASURES = ("mu1", "mu2")


def _sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _j(value: object) -> Json:
    """Coerce plain Python containers to the sealed Json type."""
    if isinstance(value, dict):
        return {str(k): _j(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_j(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError(f"not JSON: {value!r}")


def _kinds(e: DEdge) -> list[str]:
    raw = e.info.get("kinds")
    return [str(k) for k in raw] if isinstance(raw, list) else []


def _flag(e: DEdge, name: str) -> bool:
    return bool(e.info.get(name))


def _status_count(t: DTree, name: str) -> int:
    by = t.stats()["by_status"]
    assert isinstance(by, dict)
    value = by.get(name, 0)
    return value if isinstance(value, int) else 0


def _int_of(t: DTree, name: str) -> int:
    value = t.stats()[name]
    assert isinstance(value, int)
    return value


def _identify_edges(t: DTree) -> list[DEdge]:
    return [e for e in t.edges if e.challenge.startswith(IDENTIFY)]


def branch_summary(t: DTree) -> dict[str, Json]:
    """Aggregates over every root-to-leaf path; the paths themselves go to
    the full export.  A merged DAG has many paths, so the summary keeps
    counts, sets, and extremes only."""
    reports = branch_report(t)
    statuses: dict[str, int] = {}
    rounds: set[int] = set()
    sequences: set[tuple[int, ...]] = set()
    max_forms = 0
    max_ruled = 0
    for b in reports:
        status = str(b["leaf_status"])
        statuses[status] = statuses.get(status, 0) + 1
        r = b["identify_rounds_in_final_segment"]
        assert isinstance(r, int)
        rounds.add(r)
        seq = b["identify_fixpoint_ruled_forms"]
        assert isinstance(seq, list)
        sequences.add(tuple(int(str(v)) for v in seq))
        forms = b["forms_at_leaf"]
        ruled = b["ruled_forms_at_leaf"]
        assert isinstance(forms, int) and isinstance(ruled, int)
        max_forms = max(max_forms, forms)
        max_ruled = max(max_ruled, ruled)
    return {
        "paths": len(reports),
        "leaf_statuses": _j(statuses),
        "identify_rounds_in_final_segment": sorted(rounds),
        "distinct_identify_fixpoint_ruled_sequences": len(sequences),
        "every_sequence_rises": all(
            all(later > earlier for earlier, later in zip(s, s[1:])) for s in sequences
        ),
        "max_forms_at_leaf": max_forms,
        "max_ruled_forms_at_leaf": max_ruled,
    }


def tree_json(t: DTree) -> dict[str, Json]:
    return {
        "genesis": t.genesis_id,
        "reading": t.reading,
        "measure": t.measure,
        "alternate": t.alternate,
        "stats": _j(t.stats()),
        "nodes": [_j(node_json(n)) for n in t.nodes],
        "edges": [_j(edge_json(e)) for e in t.edges],
        "refusals": [_j(r) for r in t.refusals],
        "branches": [_j(b) for b in branch_report(t)],
        "branch_summary": branch_summary(t),
        "fresh_data_admitted": admitted_fresh_data(t),
    }


def _genesis_json(g: Genesis) -> dict[str, Json]:
    free = [list(p) for p in separated_pairs(g.regime) if p not in g.regime.reqs]
    return {
        "id": g.genesis_id,
        "reading": g.reading,
        "sealed_measures": list(g.sealed_measures),
        "sealed_depth": g.depth,
        "regime": _j(regime_json(g.regime)),
        "history": _j(events_json(tuple(g.history))),
        "replay_certified": dual_replay(tuple(g.history)).regime == g.regime,
        "never_required_separations": _j(free),
    }


class Probe:
    """One single-pair probe entry, typed."""

    def __init__(self, genesis: str, reading: str, measure: str, entry: dict[str, object]) -> None:
        self.genesis = genesis
        self.reading = reading
        self.measure = measure
        self.required = bool(entry.get("required_separation"))
        self.answerable = bool(entry.get("identifiable_within_bounds"))
        cost = entry.get("min_cost")
        self.cost = int(str(cost[0])) if isinstance(cost, list) and cost else None


class Reversal:
    """One re-separation orbit, typed."""

    def __init__(self, entry: dict[str, object]) -> None:
        self.answerable = bool(entry.get("answerable"))
        cost = entry.get("min_cost")
        self.cost = int(str(cost[0])) if isinstance(cost, list) and cost else None
        diags = entry.get("class_diagnostics")
        self.fresh_form_all = True
        self.ruled_any = False
        if isinstance(diags, list):
            for d in diags:
                if isinstance(d, dict):
                    if not d.get("fresh_form"):
                        self.fresh_form_all = False
                    if d.get("instantiates_ruled_form"):
                        self.ruled_any = True


def _run_probes(
    genesis: Sequence[Genesis], trees: Sequence[DTree]
) -> tuple[list[Probe], list[Reversal], dict[str, Json]]:
    probes: list[Probe] = []
    pair_blocks: list[Json] = []
    for g in genesis:
        for reading in READINGS:
            state = dual_replay(genesis_history(g, reading))
            for measure in MEASURES:
                entries = pair_probe(state, measure, BOUNDS)
                probes.extend(Probe(g.genesis_id, reading, measure, e) for e in entries)
                pair_blocks.append({
                    "genesis": g.genesis_id, "reading": reading, "measure": measure,
                    "pairs": _j(entries),
                })
    reversals: list[Reversal] = []
    rev_blocks: list[Json] = []
    for t in trees:
        if t.reading != "R" or t.alternate:
            continue
        for n in t.nodes:
            if n.status != "terminal_all_collapsed":
                continue
            orbits = reversal_probe(n.state, t.measure, BOUNDS)
            reversals.extend(Reversal(o) for o in orbits)
            rev_blocks.append({
                "genesis": t.genesis_id, "measure": t.measure, "node": n.node_id,
                "orbits": _j(orbits),
            })
    return probes, reversals, {"pairs": pair_blocks, "reversal": rev_blocks}


def _branches(r_plain: Sequence[DTree], n_of: dict[str, int]) -> list[tuple[str, str, str, int, int]]:
    out: list[tuple[str, str, str, int, int]] = []
    for t in r_plain:
        for b in branch_report(t):
            status = str(b["leaf_status"])
            rounds = b["identify_rounds_in_final_segment"]
            assert isinstance(rounds, int)
            out.append((t.genesis_id, t.measure, status, rounds, n_of[t.genesis_id]))
    return out


def _alternating(alt: Sequence[DTree]) -> list[tuple[str, str, bool, bool, int, int]]:
    out: list[tuple[str, str, bool, bool, int, int]] = []
    for t in alt:
        monotone = all(
            len(t.nodes[e.child].state.regime.rules) >= len(t.nodes[e.parent].state.regime.rules)
            for e in t.edges
        )
        rise = True
        for b in branch_report(t):
            seq = b["identify_fixpoint_ruled_forms"]
            assert isinstance(seq, list)
            values = [int(str(v)) for v in seq]
            if any(not later > earlier for earlier, later in zip(values, values[1:])):
                rise = False
        switches = sum(1 for e in t.edges if e.challenge == "switch")
        out.append((t.genesis_id, t.measure, monotone, rise, admitted_fresh_data(t), switches))
    return out


def build_all() -> dict[str, Json]:
    genesis = sealed_fixpoints(BOUNDS)
    trees: list[DTree] = []
    for g in genesis:
        for reading in READINGS:
            for measure in MEASURES:
                trees.append(build_dual_tree(g, reading, measure, BOUNDS, False, MAX_ROUNDS, GUARD))
        for measure in MEASURES:
            trees.append(build_dual_tree(g, "R", measure, BOUNDS, True, MAX_ROUNDS, GUARD))
    probes, reversals, probe_json = _run_probes(genesis, trees)
    n_of = {g.genesis_id: g.regime.n_data() for g in genesis}
    r_plain = [t for t in trees if t.reading == "R" and not t.alternate]
    p_plain = [t for t in trees if t.reading == "P" and not t.alternate]
    alt = [t for t in trees if t.alternate]

    identify_edges = [e for t in r_plain for e in _identify_edges(t)]
    kinds_census: dict[str, int] = {}
    for e in identify_edges:
        k = "+".join(_kinds(e))
        kinds_census[k] = kinds_census.get(k, 0) + 1
    branches = _branches(r_plain, n_of)
    max_pair = max(((b[3], b[4]) for b in branches), default=(0, 0))
    mu_rows: list[tuple[str, bool, int, int, int, int]] = []
    for g in genesis:
        t1 = next(t for t in r_plain if t.genesis_id == g.genesis_id and t.measure == "mu1")
        t2 = next(t for t in r_plain if t.genesis_id == g.genesis_id and t.measure == "mu2")
        counts = (_int_of(t1, "nodes"), _int_of(t1, "edges"), _int_of(t2, "nodes"), _int_of(t2, "edges"))
        mu_rows.append((g.genesis_id, counts[:2] == counts[2:], *counts))
    rev_costs = sorted({r.cost for r in reversals if r.answerable and r.cost is not None})
    alt_rows = _alternating(alt)

    summary: dict[str, Json] = {
        "genesis_count": len(genesis),
        "reading_R": {
            "accepted_identification_edges": len(identify_edges),
            "costs_attained": sorted({e.cost[0] for e in identify_edges}),
            "kinds_census": _j(kinds_census),
            "edges_with_third_party_change": sum(1 for e in identify_edges if e.info.get("third_party_changed")),
            "edges_in_ties": sum(1 for e in identify_edges if e.tie_classes > 1),
            "no_response_nodes": sum(_status_count(t, "terminal_no_response") for t in r_plain),
            "round_bound_or_guard_nodes": sum(
                _status_count(t, "completed") + _status_count(t, "frontier_guard") for t in r_plain
            ),
            "max_identify_rounds_and_n": [max_pair[0], max_pair[1]],
            "branches": [
                {"genesis": b[0], "measure": b[1], "leaf_status": b[2], "identify_rounds": b[3], "n_data": b[4]}
                for b in branches
            ],
            "mu1_vs_mu2": [
                {"genesis": m[0], "equal_counts": m[1], "mu1": [m[2], m[3]], "mu2": [m[4], m[5]]}
                for m in mu_rows
            ],
        },
        "reading_P": {
            "by_status": {f"{t.genesis_id}/{t.measure}": _j(t.stats()["by_status"]) for t in p_plain},
        },
        "reversal": {
            "costs": rev_costs,
            "all_minima_use_fresh_form": all(r.fresh_form_all for r in reversals if r.answerable),
            "any_minimum_instantiates_ruled_form": any(r.ruled_any for r in reversals if r.answerable),
            "orbits_priced": sum(1 for r in reversals if r.answerable),
        },
        "alternating": [
            {
                "genesis": a[0], "measure": a[1],
                "stats": _j(next(t for t in alt if t.genesis_id == a[0] and t.measure == a[1]).stats()),
                "ruled_forms_monotone": a[2], "identify_fixpoints_rise": a[3],
                "fresh_data_admitted": a[4], "switches": a[5],
            }
            for a in alt_rows
        ],
    }

    # Mechanical scoring of the frozen predictions.
    r_costs_by_genesis: dict[tuple[str, str], list[int]] = {}
    for p in probes:
        if p.reading == "R" and p.answerable and p.cost is not None:
            r_costs_by_genesis.setdefault((p.genesis, p.measure), []).append(p.cost)
    p1 = (
        len(r_costs_by_genesis) == len(genesis) * len(MEASURES)
        and all(costs and min(costs) == 1 for costs in r_costs_by_genesis.values())
    )
    mu1_cost1 = [e for t in r_plain if t.measure == "mu1" for e in _identify_edges(t) if e.cost[0] == 1]
    p2 = bool(mu1_cost1) and all(_kinds(e) in (["inst"], ["rule"]) for e in mu1_cost1) and any(
        _kinds(e) == ["rule"] for e in mu1_cost1
    )
    p3 = any(
        bool(e.info.get("third_party_changed")) and n_of[t.genesis_id] == 3
        for t in r_plain for e in _identify_edges(t)
    )
    p4 = all(_status_count(t, "terminal_no_response") == 0 for t in r_plain)
    p5 = bool(branches) and all(b[2] == "terminal_all_collapsed" and b[3] <= b[4] - 1 for b in branches) and all(
        _status_count(t, "completed") + _status_count(t, "frontier_guard") == 0 for t in r_plain
    )
    p_never_fixpoint = all(
        _status_count(t, "terminal_all_collapsed") == 0 and _status_count(t, "terminal_no_response") >= 1
        for t in p_plain
    )
    p_required_refuse = all(not p.answerable for p in probes if p.reading == "P" and p.required)
    p_free_answer = all(p.answerable for p in probes if p.reading == "P" and not p.required)
    p6 = p_never_fixpoint and p_required_refuse and p_free_answer
    p7 = rev_costs == [2] and all(r.fresh_form_all for r in reversals if r.answerable) and not any(
        r.ruled_any for r in reversals if r.answerable
    )
    p8 = bool(alt_rows) and all(a[2] and a[3] and a[4] == 0 for a in alt_rows)
    groups: dict[tuple[str, int, str], list[list[str]]] = {}
    for t in r_plain:
        if t.measure != "mu1":
            continue
        for e in _identify_edges(t):
            if e.tie_classes > 1:
                groups.setdefault((t.genesis_id, e.parent, e.challenge), []).append(_kinds(e))
    p9 = bool(groups) and any(["inst"] in ks and ["rule"] in ks for ks in groups.values())
    p10 = all(m[1] for m in mu_rows) and not any(_flag(e, "fresh_form") for e in identify_edges)
    verdicts = {"P1": p1, "P2": p2, "P3": p3, "P4": p4, "P5": p5, "P6": p6, "P7": p7, "P8": p8, "P9": p9, "P10": p10}
    scored: dict[str, Json] = {
        k: {"hit": v, "verdict": "HIT" if v else "MISS"} for k, v in verdicts.items()
    }
    detail: dict[str, Json] = {
        "P6_clauses": {
            "no_reading_P_tree_reaches_the_fixpoint": p_never_fixpoint,
            "required_pairs_refuse": p_required_refuse,
            "free_pairs_answer": p_free_answer,
            "free_pairs_without_answer": [
                {"genesis": p.genesis, "measure": p.measure}
                for p in probes if p.reading == "P" and not p.required and not p.answerable
            ],
        },
        "P8_clauses": {
            "ruled_forms_monotone_everywhere": all(a[2] for a in alt_rows),
            "identify_fixpoints_rise_everywhere": all(a[3] for a in alt_rows),
            "no_fresh_datum_anywhere": all(a[4] == 0 for a in alt_rows),
            "runs_where_rise_fails": [
                {"genesis": a[0], "measure": a[1]} for a in alt_rows if not a[3]
            ],
        },
    }

    return {
        "authority_effect": "None",
        "bounds": {"max_items": BOUNDS.max_items, "max_arity": BOUNDS.max_arity,
                   "max_rounds": MAX_ROUNDS, "pre_expansion_node_guard": GUARD},
        "readings": {"P": "sealed separation requirements stand at genesis",
                     "R": "a declared retraction discards them at genesis"},
        "prompt_sha256": _sha(HERE / "PROMPT.md"),
        "predictions_sha256": _sha(HERE / "PREDICTIONS.md"),
        "genesis": [_genesis_json(g) for g in genesis],
        "trees": [tree_json(t) for t in trees],
        "probes": probe_json,
        "summary": summary,
        "predictions_scored": scored,
        "prediction_detail": detail,
    }


def tree_digest(t: dict[str, Json]) -> dict[str, Json]:
    """The per-tree part that stays in the committed summary: everything
    except the node and edge lists, which go to the full export."""
    return {k: v for k, v in t.items() if k not in ("nodes", "edges", "branches")}


def split(payload: dict[str, Json]) -> tuple[dict[str, Json], dict[str, Json]]:
    """(summary, full).  The summary keeps genesis, per-tree statistics,
    branches, refusals, the scoring, and the sha256 of the full export's
    uncompressed bytes; the full export keeps every node, edge, and probe
    entry.  Same split as the sealed ``tree_*_summary.json`` /
    ``artifacts/full`` pair, for the same reason: the full trees are large
    and repetitive, and the summary must stay readable in a diff."""
    from derivation.export import dumps_deterministic

    trees = payload["trees"]
    assert isinstance(trees, list)
    full: dict[str, Json] = {
        "authority_effect": "None",
        "trees": trees,
        "probes": payload["probes"],
    }
    full_sha = hashlib.sha256(dumps_deterministic(full)).hexdigest()
    summary: dict[str, Json] = {k: v for k, v in payload.items() if k not in ("trees", "probes")}
    summary["trees"] = [tree_digest(t) for t in trees if isinstance(t, dict)]
    summary["full_export"] = {
        "path": "receipts/full/identification_dual_full.json.gz",
        "sha256_uncompressed": full_sha,
        "contents": ["trees[].nodes", "trees[].edges", "trees[].branches", "probes"],
    }
    return summary, full


def main() -> int:
    parser = argparse.ArgumentParser(description="Write the identification-dual receipts.")
    parser.add_argument("--out", type=pathlib.Path, default=HERE / "receipts" / "identification_dual.json")
    parser.add_argument(
        "--full", type=pathlib.Path,
        default=HERE / "receipts" / "full" / "identification_dual_full.json.gz",
    )
    args = parser.parse_args()
    from derivation.export import write_json_gz

    summary, full = split(build_all())
    write_json(args.out, summary)
    sha = write_json_gz(args.full, full)
    recorded = summary["full_export"]
    assert isinstance(recorded, dict) and recorded["sha256_uncompressed"] == sha
    payload = summary
    scored = payload["predictions_scored"]
    assert isinstance(scored, dict)
    for k in sorted(scored, key=lambda s: int(s[1:])):
        v = scored[k]
        assert isinstance(v, dict)
        print(f"{k}: {v['verdict']}")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
