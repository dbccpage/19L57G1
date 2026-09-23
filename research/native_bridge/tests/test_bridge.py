"""Tests of the finite mirror, its negative controls, and its custody.

AuthorityEffect: None.
"""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import subprocess

import pytest

import bridge
import run
from derivation.model import Event, Regime, Supply, step
from derivation.primitive_passage import GENESIS_P, PS, PEvent, pstep
from derivation.trace_algebra import TRecord, make_record, named_states

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]


def test_alphabet_has_every_event_kind() -> None:
    kinds = {e[0] for e in bridge.alphabet()}
    assert kinds == {"admitOcc", "assertWit", "admitWit", "protect", "declareObs",
                     "refineCol", "addCol", "refuse", "setBudget", "setLicense",
                     "halt"}
    assert len(bridge.alphabet()) == len(set(bridge.alphabet()))


def test_receipt_matches_committed() -> None:
    assert run.main(["--check"]) == 0


def test_receipt_growth_covers_every_growing_kind() -> None:
    grow = bridge.receipt()["dichotomy"]
    assert isinstance(grow, dict)
    kinds = grow["grow_by_kind"]
    assert isinstance(kinds, dict)
    assert set(kinds) == {"admitOcc", "assertWit", "admitWit", "protect",
                          "declareObs", "refineCol", "addCol", "refuse", "halt"}
    assert all(isinstance(v, int) and v > 0 for v in kinds.values())


def test_cycles_move_only_budget_and_license() -> None:
    states = bridge.reachable(4, bridge.alphabet(), named_states())
    report = bridge.cycle_report(states, bridge.alphabet())
    assert report["varying_fields"] == ["budget", "licensed"]
    assert report["nontrivial"] != 0


def test_license_only_cycle() -> None:
    events: list[PEvent] = [("setLicense", False), ("setLicense", True)]
    states = bridge.reachable(2, events)
    assert bridge.cycle_report(states, events)["varying_fields"] == ["licensed"]


def test_components_partition_the_states() -> None:
    states = bridge.reachable(3, bridge.alphabet())
    comps = bridge.components(states, bridge.alphabet())
    flat = [s for c in comps for s in c]
    assert sorted(map(repr, flat)) == sorted(map(repr, states))


def test_budget_cycle_is_real() -> None:
    up = pstep(GENESIS_P, ("setBudget", 1))
    assert up != GENESIS_P
    assert pstep(up, ("setBudget", 0)) == GENESIS_P
    assert bridge.core(up) == bridge.core(GENESIS_P)


def test_size_counts_each_store() -> None:
    s = PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),), prot=((0, 1),),
           obs=((0,), ()), refusals=((0, 1),), halted=True)
    assert bridge.size(s) == 2 + 1 + 1 + 1 + (1 + 2 + 1) + 1 + 1


def test_records_square() -> None:
    report = bridge.record_report(GENESIS_P, [("admitOcc", 0), ("halt",)], 2)
    assert report == {"histories": 7, "legal": 4, "max_length": 2}


def test_budget_register_commutes_for_any_numbered_system() -> None:
    report = bridge.budget_sim(lambda x, e: (x * e + 1) % 5, list(range(5)), [2, 3])
    assert report == {"squares": 10, "distinct_encodings": 5, "distinct_cores": 1}


def test_realize_refuses_and_accepts() -> None:
    halted = pstep(GENESIS_P, ("halt",))
    assert bridge.realize(bridge.witness_decoder,
                          [(GENESIS_P, halted, "admitOcc")]) is None
    assert bridge.realize(bridge.witness_decoder,
                          [(GENESIS_P, halted, "unknown")]) is None
    assert bridge.realize(bridge.witness_decoder,
                          [(GENESIS_P, halted, "halt")]) == [("halt",)]
    assert bridge.realize(bridge.witness_decoder, []) == []


def test_admission_never_shrinks() -> None:
    report = bridge.admission_report(2)
    assert report["keep"] != 0 and report["grow"] != 0 and report["refused"] != 0


# Negative controls: each injected defect must be caught by name.

def _drop_refusals(s: PS, e: PEvent) -> PS:
    t = pstep(s, e)
    return replace(t, refusals=()) if e[0] == "setBudget" else t


def _unhalt(s: PS, e: PEvent) -> PS:
    return replace(s, halted=False) if e[0] == "setLicense" and s.halted else pstep(s, e)


def _undo_occ(s: PS, e: PEvent) -> PS:
    if e[0] == "setBudget" and s.occ:
        return replace(s, occ=s.occ[:-1])
    return pstep(s, e)


def test_dichotomy_catches_a_shrinking_store() -> None:
    states = [PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),), prot=((0, 1),),
                 obs=(), refusals=((0, 1),))]
    with pytest.raises(AssertionError, match="neither keeps nor grows"):
        bridge.dichotomy(states, bridge.alphabet(), _drop_refusals)


def test_dichotomy_catches_a_revived_terminal() -> None:
    with pytest.raises(AssertionError, match="neither keeps nor grows"):
        bridge.dichotomy([replace(GENESIS_P, halted=True)], bridge.alphabet(), _unhalt)


def test_cycle_report_catches_a_core_cycle() -> None:
    states = bridge.reachable(2, bridge.alphabet(), [GENESIS_P], _undo_occ)
    with pytest.raises(AssertionError, match="moves a core field"):
        bridge.cycle_report(states, bridge.alphabet(), _undo_occ)


def test_budget_sim_catches_a_broken_square(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(bridge, "preplay", lambda h, s: s)
    with pytest.raises(AssertionError, match="square fails"):
        bridge.budget_sim(lambda x, _e: 1 - x, [0, 1], [0])


def test_record_report_catches_a_forged_record(monkeypatch: pytest.MonkeyPatch) -> None:
    def forged(s: PS, e: PEvent) -> TRecord:
        return replace(make_record(s, e), ev=("halt",))
    monkeypatch.setattr(bridge, "make_record", forged)
    with pytest.raises(AssertionError, match="record square fails"):
        bridge.record_report(GENESIS_P, [("admitOcc", 0)], 1)


def test_record_report_catches_a_legality_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(bridge, "legal_trace", lambda s, tr: False)
    with pytest.raises(AssertionError, match="legality mismatch"):
        bridge.record_report(GENESIS_P, [("admitOcc", 0)], 1)


def test_record_report_catches_dropped_accepted_records(
        monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(bridge, "build_trace", lambda s, h: ())
    with pytest.raises(AssertionError, match="accepted records differ"):
        bridge.record_report(GENESIS_P, [("admitOcc", 0)], 1)


def test_admission_report_catches_a_shrinking_step(monkeypatch: pytest.MonkeyPatch) -> None:
    def shrink(r: Regime, e: Event) -> Regime:
        t = step(r, e)
        if isinstance(e, Supply) and r.data:
            return Regime(r.data[:-1], r.forms, r.insts, r.rules, r.reqs)
        return t
    monkeypatch.setattr(bridge, "step", shrink)
    with pytest.raises(AssertionError, match="neither keeps nor grows"):
        bridge.admission_report(2)


@pytest.mark.parametrize("text", ['{"admission_depth": 1}', "[1, 2, 3]",
                                  '{"admission_depth": -1, "reachable_depth": 1, "record_length": 1}',
                                  '{"admission_depth": true, "reachable_depth": 1, "record_length": 1}'])
def test_bounds_reject_malformed_input(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                       text: str) -> None:
    fake = tmp_path / "bridge.py"
    (tmp_path / "input.json").write_text(text, encoding="utf-8")
    monkeypatch.setattr(bridge, "__file__", str(fake))
    with pytest.raises(ValueError, match="input.json"):
        bridge.bounds()


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


# Custody: consumed sources are pinned at their snapshot; drift at HEAD is
# reported, not failed.

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
