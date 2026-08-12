"""Tests for JSON export and the artifact-producing entry point."""

from __future__ import annotations

import json
from pathlib import Path

from derivation.candidates import Bounds, NewForm, NewInst
from derivation.engine import READING_L, build_tree
from derivation.export import (
    delta_json,
    event_json,
    regime_json,
    tree_json,
    write_json,
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


def test_event_json_all_kinds() -> None:
    assert event_json(Supply("<>")) == {"event": "supply", "token": "<>"}
    assert event_json(AdmitDatum("<a>"))["event"] == "admit_datum"
    assert event_json(AdmitForm(2)) == {"event": "admit_form", "arity": 2}
    assert event_json(AdmitInst(0, (1, 0))) == {
        "event": "admit_inst",
        "form": 0,
        "args": [1, 0],
    }
    assert event_json(AdmitRuleAll(0)) == {
        "event": "admit_rule_all",
        "form": 0,
    }
    assert event_json(Impose(0, 1)) == {
        "event": "impose_separation",
        "i": 0,
        "j": 1,
    }


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
    assert delta_json((NewForm(1), NewInst(0, (0,)))) == [
        {"kind": "form", "arity": 1},
        {"kind": "inst", "form": 0, "args": [0]},
    ]


def test_tree_json_roundtrips_to_json(tmp_path: Path) -> None:
    t = build_tree(READING_L, "mu2", Bounds(), max_rounds=2, node_budget=10)
    payload = tree_json(t)
    path = tmp_path / "tree.json"
    write_json(path, payload)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["reading"] == "L"
    assert loaded["stats"]["all_certified"] is True
    assert len(loaded["nodes"]) == len(t.nodes)
    # Every exported node carries its full replayable history.
    for node in loaded["nodes"]:
        assert node["history"][0] == {"event": "supply", "token": "<>"}


def test_write_json_is_deterministic(tmp_path: Path) -> None:
    p1, p2 = tmp_path / "a.json", tmp_path / "b.json"
    write_json(p1, {"b": 1, "a": [1, 2]})
    write_json(p2, {"a": [1, 2], "b": 1})
    assert p1.read_bytes() == p2.read_bytes()


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
    names = {p.name for p in out.iterdir()}
    assert names == {
        "bounds.json",
        "challenges.json",
        "claims.json",
        "nosupply_L.json",
        "nosupply_F.json",
        "tree_L_mu1.json",
        "tree_L_mu2.json",
        "tree_F_mu1.json",
        "tree_F_mu2.json",
    }
    claims = json.loads((out / "claims.json").read_text(encoding="utf-8"))
    assert claims["CL-3-FAIL-CURRENT"] == {"L": False, "F": False}
    assert claims["CL-3-NONUNIQUE-MU1"] == {"L": 3, "F": 5}
    assert claims["CL-3-UNIQUE-MU2"] == {"L": 1, "F": 1}
    term = claims["CL-ENDOGENOUS-TERMINATION"]
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
    assert all(claims["CL-REPLAY-CERTIFIED"].values())


def test_run_main_is_deterministic(tmp_path: Path) -> None:
    out1, out2 = tmp_path / "a1", tmp_path / "a2"
    args = ["--rounds", "2", "--budget-mu1", "8", "--budget-mu2", "8"]
    run_derivation.main(["--artifacts", str(out1), *args])
    run_derivation.main(["--artifacts", str(out2), *args])
    for p in sorted(out1.iterdir()):
        assert p.read_bytes() == (out2 / p.name).read_bytes()
