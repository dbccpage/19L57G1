"""Tests of the adapter mirror, its negative controls, and custody.

AuthorityEffect: None.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess

import pytest

import adapters
import run
from derivation.primitive_passage import GENESIS_P, PS

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]


def test_receipt_matches_committed() -> None:
    assert run.main(["--check"]) == 0


def test_small_reports() -> None:
    assert adapters.counter_report(3) == {"squares": 3, "distinct_cores": 4}
    assert adapters.matrix_report()["distinct_cores"] == 1
    assert adapters.mechanics_report(1) == {"pairs": 81, "moved": 80}
    report = adapters.license_report([GENESIS_P, PS(licensed=False)])
    assert report["inert_proposals"] == 6 and report["gated_applies"] == 6


def test_grant_maps_to_a_license_write() -> None:
    assert adapters.pl_events("grant", True) == [("setLicense", True)]


# Negative controls.

def test_counter_catches_a_broken_square(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(adapters, "pstep", lambda s, e: s)
    with pytest.raises(AssertionError, match="counter square fails"):
        adapters.counter_report(2)


def test_counter_catches_a_collapsed_core(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(adapters, "core", lambda s: 0)
    with pytest.raises(AssertionError, match="not injective"):
        adapters.counter_report(2)


def test_matrix_catches_a_non_involution(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(adapters, "h_step", lambda v: (v[1], 1))
    with pytest.raises(AssertionError, match="not an involution"):
        adapters.matrix_report()


def test_matrix_catches_a_broken_budget_square(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(adapters, "preplay", lambda h, s: s)
    with pytest.raises(AssertionError, match="budget square fails"):
        adapters.matrix_report()


def test_mechanics_catches_a_wrong_period(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(adapters, "next_point", lambda c, a, b: (b[0] + 1, b[1]))
    with pytest.raises(AssertionError, match="period four"):
        adapters.mechanics_report(1)


def test_license_catches_an_acting_proposal(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(adapters, "pl_events", lambda kind, arg: [("halt",)])
    with pytest.raises(AssertionError, match="proposal changed"):
        adapters.license_report([GENESIS_P])


def test_license_catches_an_ungated_apply(monkeypatch: pytest.MonkeyPatch) -> None:
    real = adapters.pl_events
    monkeypatch.setattr(adapters, "pl_events",
                        lambda kind, arg: [("halt",)] if kind == "apply" else real(kind, arg))
    with pytest.raises(AssertionError, match="unlicensed or unfunded"):
        adapters.license_report([PS(licensed=False)])


@pytest.mark.parametrize("text", ['{"counter_bound": 1}', "[1]",
                                  '{"battery_depth": -1, "counter_bound": 1, "grid_radius": 1}',
                                  '{"battery_depth": true, "counter_bound": 1, "grid_radius": 1}'])
def test_bounds_reject_malformed_input(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                       text: str) -> None:
    (tmp_path / "input.json").write_text(text, encoding="utf-8")
    monkeypatch.setattr(adapters, "__file__", str(tmp_path / "adapters.py"))
    with pytest.raises(ValueError, match="input.json"):
        adapters.bounds()


def test_run_writes_and_detects_drift(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                      capsys: pytest.CaptureFixture[str]) -> None:
    target = tmp_path / "evidence" / "receipt.json"
    monkeypatch.setattr(run, "RECEIPT", target)
    monkeypatch.setattr(run, "HERE", tmp_path)
    monkeypatch.setattr(run, "receipt", lambda: {"small": True})
    assert run.main(["--check"]) == 1
    assert run.main([]) == 0
    assert run.main(["--check"]) == 0
    target.write_bytes(b"{}\n")
    assert run.main(["--check"]) == 1
    assert "differs" in capsys.readouterr().err


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
