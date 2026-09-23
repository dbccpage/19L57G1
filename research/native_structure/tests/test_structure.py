"""Tests of the finite structure mirror, its negative controls, and custody.

AuthorityEffect: None.
"""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import subprocess

import pytest

from bridge import core
import run
import structure
from derivation.primitive_passage import GENESIS_P, PS, PEvent, pstep
from derivation.trace_algebra import named_states, refine_state

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]


def test_receipt_matches_committed() -> None:
    assert run.main(["--check"]) == 0


def test_receipt_records_both_funded_violations() -> None:
    descent = structure.receipt()["descent"]
    assert isinstance(descent, dict)
    assert set(descent["funded_violations"]) == {"refineCol", "addCol"}
    assert all(v > 0 for v in descent["funded_violations"].values())


def test_square_boundaries() -> None:
    u = GENESIS_P
    assert structure.commutes(u, ("setBudget", 1), ("setLicense", False))
    assert not structure.commutes(u, ("halt",), ("setLicense", False))
    assert structure.d_square(structure.budget_delta, u, ("setBudget", 1),
                              ("setLicense", False)) == 0


def test_writes_loop_costs_two() -> None:
    loop: list[PEvent] = [("setBudget", 1), ("setBudget", 0)]
    assert structure.path_cost(structure.writes, GENESIS_P, loop) == 2
    assert structure.path_cost(structure.budget_delta, GENESIS_P, loop) == 0


def test_telescoping_without_loops() -> None:
    report = structure.telescoping_report(GENESIS_P, [("admitOcc", 0)], 2)
    assert report == {"histories": 3, "writes_nonzero_loops": 0, "shortest_loop": []}


def test_descent_on_refine_state() -> None:
    s = refine_state()
    t = replace(s, budget=0)
    assert core(s) == core(t)
    assert core(pstep(s, ("refineCol", (), 0))) != \
        core(pstep(t, ("refineCol", (), 0)))


def test_equivariance_needs_injectivity() -> None:
    states = [pstep(GENESIS_P, ("admitOcc", 0))]
    events: list[PEvent] = [("admitOcc", 1)]
    assert structure.equivariance_failures(lambda t: t + 1, states, events) == 0
    assert structure.equivariance_failures(lambda t: 0, states, events) == 1
    assert structure.act_event(lambda t: t + 1, ("halt",)) == ("halt",)


def test_frame_report_counts() -> None:
    report = structure.frame_report([GENESIS_P], [("admitOcc", 0), ("halt",)])
    assert report == {"license_frame_squares": 2}


# Negative controls.

def test_square_report_catches_an_open_budget_cost(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(structure, "budget_delta",
                        lambda s, e: 1 if e[0] == "setBudget" and s.halted else 0)
    with pytest.raises(AssertionError, match="exact budget cost is open"):
        structure.square_report([GENESIS_P], [("halt",), ("setBudget", 0)])


def test_telescoping_catches_a_broken_cost(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(structure, "budget_delta", lambda s, e: 2)
    with pytest.raises(AssertionError, match="does not telescope"):
        structure.telescoping_report(GENESIS_P, [("setBudget", 1)], 1)


def test_descent_catches_an_unfunded_violation(monkeypatch: pytest.MonkeyPatch) -> None:
    def leaky(s: PS, e: PEvent) -> PS:
        t = pstep(s, e)
        return replace(t, occ=t.occ + (9,)) if e[0] == "declareObs" and s.budget else t
    monkeypatch.setattr(structure, "pstep", leaky)
    states = [GENESIS_P, replace(GENESIS_P, budget=1)]
    with pytest.raises(AssertionError, match="unfunded event fails descent"):
        structure.descent_report(states, [("declareObs",)])


def test_frame_catches_a_broken_frame(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(structure, "commutes", lambda u, a, b: False)
    with pytest.raises(AssertionError, match="license frame fails"):
        structure.frame_report([GENESIS_P], [("admitOcc", 0)])


@pytest.mark.parametrize("text", ['{"square_depth": 1}', "[1]",
                                  '{"descent_depth": -1, "history_length": 1, "square_depth": 1}',
                                  '{"descent_depth": false, "history_length": 1, "square_depth": 1}'])
def test_bounds_reject_malformed_input(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                       text: str) -> None:
    (tmp_path / "input.json").write_text(text, encoding="utf-8")
    monkeypatch.setattr(structure, "__file__", str(tmp_path / "structure.py"))
    with pytest.raises(ValueError, match="input.json"):
        structure.bounds()


def test_run_writes_and_detects_drift(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                      capsys: pytest.CaptureFixture[str]) -> None:
    target = tmp_path / "evidence" / "receipt.json"
    monkeypatch.setattr(run, "RECEIPT", target)
    monkeypatch.setattr(run, "HERE", tmp_path)
    assert run.main(["--check"]) == 1
    assert run.main([]) == 0
    assert run.main(["--check"]) == 0
    target.write_bytes(b"{}\n")
    assert run.main(["--check"]) == 1
    assert "differs" in capsys.readouterr().err


def test_named_battery_is_the_sealed_one() -> None:
    assert len(named_states()) == 12


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True,
                          check=False)


def test_consumed_sources_match_their_snapshot() -> None:
    pins = json.loads((HERE / "SEALED_PINS.json").read_text(encoding="utf-8"))
    snapshot = pins["snapshot"]
    if _git("cat-file", "-e", f"{snapshot}^{{commit}}").returncode != 0:
        pytest.skip(f"snapshot {snapshot} is not in this checkout's history")
    drift = []
    for path, blob in pins["pins"].items():
        assert _git("rev-parse", f"{snapshot}:{path}").stdout.strip() == blob, path
        if _git("rev-parse", f"HEAD:{path}").stdout.strip() != blob:
            drift.append(path)
    if drift:
        print(f"drift at HEAD (reported, not failed): {drift}")
