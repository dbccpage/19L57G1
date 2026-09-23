"""Tests of the finite ladder mirror, its negative controls, and custody.

AuthorityEffect: None.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess

import pytest

import ladder
import run

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]
SMALL = ladder.grid(1)


def test_receipt_matches_committed() -> None:
    assert run.main(["--check"]) == 0


def test_dual_arithmetic() -> None:
    a, b = ladder.Dual(2, 3), ladder.Dual(5, 7)
    assert a * b == ladder.Dual(10, 2 * 7 + 3 * 5)
    assert a + b == ladder.Dual(7, 10)
    assert -a == ladder.Dual(-2, -3)


def test_charge_formula_and_nonconstancy() -> None:
    e = ladder.central(3)
    assert ladder.charge(e, ladder.rot, (0, 0), (1, 1)) == 0
    assert ladder.charge(e, ladder.rot, (1, 0), (0, 1)) == 2


def test_small_reports() -> None:
    assert ladder.exactness_report(SMALL, [0, 1])["checked"] == 2 * 81 * 3
    inv = ladder.invariance_report(SMALL, [0, 1])
    assert inv["central_rot_failures"] == 0 and inv["central0_shift_failures"] == 0
    assert inv["aniso_rot_failures"] > 0 and inv["central1_shift_failures"] > 0
    cons = ladder.conservation_report(SMALL, [1], 5)
    assert cons["central_histories"] == 81
    assert cons["aniso_histories_with_moving_charge"] > 0
    assert ladder.nonstationary_report(SMALL)["moving"] > 0


def test_variation_of_a_nonstationary_history() -> None:
    q = [(0, 0), (1, 0), (1, 1)]
    assert ladder.varied_action_du(ladder.central(0), q, 1, (1, 0)) != 0


def test_expression_constructors() -> None:
    assert ladder.evaluate(lambda i: 3, ladder.sub(ladder.const(5), ladder.var(0))) == 2


# Negative controls: each injected defect is caught by name.

def test_exactness_catches_a_wrong_derivative(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ladder, "ddir", lambda rho, tau, e: 0)
    with pytest.raises(AssertionError, match="not exact"):
        ladder.exactness_report([(1, 1), (0, 0)], [0])


def test_exactness_catches_a_wrong_closed_form(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ladder, "d1", lambda e, a, b, v: 99)
    with pytest.raises(AssertionError, match="closed-form"):
        ladder.exactness_report([(1, 1)], [0])


def test_invariance_catches_a_broken_symmetry(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ladder, "rot", lambda p: (p[1], p[0]))
    with pytest.raises(AssertionError, match="not rotation invariant"):
        ladder.invariance_report(SMALL, [0])


def test_conservation_catches_a_wrong_recurrence(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ladder, "next_point", lambda c, a, b: (b[0] + 1, b[1]))
    with pytest.raises(AssertionError, match="charge moved"):
        ladder.conservation_report(SMALL, [0], 4)


def test_conservation_catches_a_nonzero_variation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ladder, "varied_action_du", lambda e, q, k, v: 1)
    with pytest.raises(AssertionError, match="nonzero variation"):
        ladder.conservation_report([(0, 0)], [0], 4)


@pytest.mark.parametrize("text", ['{"grid_radius": 1}', "[1]",
                                  '{"coefficient_radius": -1, "grid_radius": 1, "history_length": 3}',
                                  '{"coefficient_radius": true, "grid_radius": 1, "history_length": 3}'])
def test_bounds_reject_malformed_input(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                       text: str) -> None:
    (tmp_path / "input.json").write_text(text, encoding="utf-8")
    monkeypatch.setattr(ladder, "__file__", str(tmp_path / "ladder.py"))
    with pytest.raises(ValueError, match="input.json"):
        ladder.bounds()


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
