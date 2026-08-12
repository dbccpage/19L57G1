"""Tests for JSON export (normalized DAG records) and the artifact
entry point."""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

from derivation.candidates import Bounds, NewForm, NewInst
from derivation.engine import READING_L, build_tree
from derivation.export import (
    delta_json,
    dumps_deterministic,
    edge_events,
    event_from_json,
    event_json,
    read_json_gz,
    regime_json,
    regime_sha256,
    tree_full_json,
    tree_summary_json,
    verify_full_export,
    write_json,
    write_json_gz,
)
from derivation.model import (
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Impose,
    Supply,
    replay,
)

import run_derivation


def test_event_json_roundtrip_all_kinds() -> None:
    events = [
        Supply("<>"),
        AdmitDatum("<a>"),
        AdmitForm(2),
        AdmitInst(0, (1, 0)),
        AdmitRuleAll(0),
        Impose(0, 1),
    ]
    for e in events:
        assert event_from_json(event_json(e)) == e
    assert event_json(Supply("<>")) == {"event": "supply", "token": "<>"}
    try:
        event_from_json({"event": "bogus"})
    except ValueError:
        pass
    else:  # pragma: no cover - defensive
        raise AssertionError("expected ValueError")


def test_regime_and_delta_json() -> None:
    r = replay(
        [
            AdmitDatum("x"),
            AdmitDatum("y"),
            Impose(0, 1),
            AdmitForm(1),
            AdmitInst(0, (1,)),
            AdmitRuleAll(0),
        ]
    )
    assert regime_json(r) == {
        "data": ["x", "y"],
        "forms": [1],
        "insts": [[0, [1]]],
        "rules": [0],
        "reqs": [[0, 1]],
    }
    assert len(regime_sha256(r)) == 64
    assert delta_json((NewForm(1), NewInst(0, (0,)))) == [
        {"kind": "form", "arity": 1},
        {"kind": "inst", "form": 0, "args": [0]},
    ]


def test_full_export_replays_and_verifies(tmp_path: Path) -> None:
    t = build_tree(READING_L, "mu2", Bounds(), max_rounds=4, node_budget=40)
    payload = tree_full_json(t)
    # Nodes carry hashes, not histories (deduplicated records).
    nodes = payload["nodes"]
    assert isinstance(nodes, list) and "history" not in nodes[0]
    assert verify_full_export(payload)
    # Edge deltas agree with the recorded creation histories.
    seen: set[int] = {0}
    for edge, tnode in ((e, t.nodes[e.child]) for e in t.edges):
        if tnode.node_id in seen:
            continue
        seen.add(tnode.node_id)
        parent = t.nodes[edge.parent]
        assert (
            parent.history + edge_events(parent.regime, edge)
            == tnode.history
        )
    # Round-trips through reproducible compression.
    sha = write_json_gz(tmp_path / "t.json.gz", payload)
    assert read_json_gz(tmp_path / "t.json.gz") == json.loads(
        dumps_deterministic(payload)
    )
    assert sha == hashlib.sha256(dumps_deterministic(payload)).hexdigest()


def test_verify_full_export_detects_tampering() -> None:
    t = build_tree(READING_L, "mu2", Bounds(), max_rounds=2, node_budget=10)
    payload = json.loads(dumps_deterministic(tree_full_json(t)))
    payload["nodes"][1]["regime_sha256"] = "0" * 64
    assert not verify_full_export(payload)
    payload2 = json.loads(dumps_deterministic(tree_full_json(t)))
    payload2["nodes"][0]["regime_sha256"] = "0" * 64
    assert not verify_full_export(payload2)


def test_summary_carries_stats_and_hash() -> None:
    t = build_tree(READING_L, "mu2", Bounds(), max_rounds=2, node_budget=10)
    summary = tree_summary_json(t, "abc")
    assert summary["full_export_sha256"] == "abc"
    stats = summary["stats"]
    assert isinstance(stats, dict) and stats["all_certified"] is True


def test_write_json_and_gz_are_deterministic(tmp_path: Path) -> None:
    p1, p2 = tmp_path / "a.json", tmp_path / "b.json"
    write_json(p1, {"b": 1, "a": [1, 2]})
    write_json(p2, {"a": [1, 2], "b": 1})
    assert p1.read_bytes() == p2.read_bytes()
    g1, g2 = tmp_path / "a.json.gz", tmp_path / "b.json.gz"
    write_json_gz(g1, {"b": 1, "a": [1, 2]})
    write_json_gz(g2, {"a": [1, 2], "b": 1})
    assert g1.read_bytes() == g2.read_bytes()


EXPECTED_SUMMARIES = {
    "tree_L_mu1_summary.json",
    "tree_L_mu2_summary.json",
    "tree_F_mu1_summary.json",
    "tree_F_mu2_summary.json",
    "closed_L_summary.json",
    "closed_F_summary.json",
}


def test_run_main_produces_all_artifacts(tmp_path: Path) -> None:
    out = tmp_path / "artifacts"
    code = run_derivation.main(
        [
            "--artifacts",
            str(out),
            "--rounds",
            "3",
            "--budget-mu1",
            "40",
            "--budget-mu2",
            "12",
        ]
    )
    assert code == 0
    names = {p.name for p in out.iterdir() if p.is_file()}
    assert names == EXPECTED_SUMMARIES | {
        "bounds.json",
        "challenges.json",
        "claims.json",
    }
    fulls = {p.name for p in (out / "full").iterdir()}
    assert fulls == {
        s.replace("_summary.json", ".json.gz") for s in EXPECTED_SUMMARIES
    }
    # Summary hashes pin the full exports; full exports replay-verify.
    for summary_name in EXPECTED_SUMMARIES:
        summary = json.loads(
            (out / summary_name).read_text(encoding="utf-8")
        )
        full_path = out / "full" / summary_name.replace(
            "_summary.json", ".json.gz"
        )
        raw = gzip.decompress(full_path.read_bytes())
        assert (
            hashlib.sha256(raw).hexdigest()
            == summary["full_export_sha256"]
        )
        assert verify_full_export(json.loads(raw))
    claims = json.loads((out / "claims.json").read_text(encoding="utf-8"))
    assert claims["CL-3-FAIL-CURRENT"] == {"L": False, "F": False}
    assert claims["CL-3-NONUNIQUE-MU1"] == {"L": 3, "F": 5}
    assert claims["CL-3-UNIQUE-MU2"] == {"L": 1, "F": 1}
    term = claims["CL-CLOSURE-TERMINATION"]
    for name in ("L", "F"):
        report = term[name]["branch_report"]
        assert report["every_maximal_branch_terminates"] is True
        assert report["budget_cutoff_branches"] == 0
        assert report["round_cutoff_branches"] == 0
        assert report["open_branches"] == 0
        assert term[name]["within_bound"] is True
    depth = claims["CL-REACHES-REQUESTED-DEPTH-WITH-EXTERNAL-SUPPLY"]
    for key in ("L_mu1", "L_mu2", "F_mu1", "F_mu2"):
        assert depth[key]["max_depth"] <= depth[key]["requested_rounds"]
    branch = claims["CL-BRANCH-REPORTS"]
    for key in ("L_mu1", "L_mu2", "F_mu1", "F_mu2"):
        assert set(branch[key]) == {
            "terminal_branches",
            "budget_cutoff_branches",
            "round_cutoff_branches",
            "open_branches",
            "every_maximal_branch_terminates",
        }
    equi = claims["CL-TRANSITION-EQUIVARIANCE"]
    assert "automorphism orbit" in equi["policy"]
    assert set(equi["expansions_with_multiple_orbits"]) == {
        "L_mu1", "L_mu2", "F_mu1", "F_mu2", "closed_L", "closed_F",
    }
    assert all(claims["CL-REPLAY-CERTIFIED"].values())


def test_run_main_is_deterministic(tmp_path: Path) -> None:
    out1, out2 = tmp_path / "a1", tmp_path / "a2"
    args = ["--rounds", "2", "--budget-mu1", "8", "--budget-mu2", "8"]
    run_derivation.main(["--artifacts", str(out1), *args])
    run_derivation.main(["--artifacts", str(out2), *args])
    for p in sorted(out1.rglob("*")):
        if p.is_file():
            rel = p.relative_to(out1)
            assert p.read_bytes() == (out2 / rel).read_bytes(), rel
