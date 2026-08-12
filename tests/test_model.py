"""Tests for regimes, admission events, and replay."""

from __future__ import annotations

import pytest

from derivation.model import (
    EMPTY,
    AdmissionError,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Impose,
    Regime,
    Supply,
    certify,
    replay,
    step,
)


def test_supply_is_not_admission() -> None:
    assert step(EMPTY, Supply("<>")) == EMPTY
    assert step(EMPTY, Supply("anything")) == EMPTY


def test_admit_datum_appends_in_order() -> None:
    r = replay([AdmitDatum("<a>"), AdmitDatum("<ab>")])
    assert r.data == ("<a>", "<ab>")
    assert r.n_data() == 2


def test_admit_datum_dedups_on_presentation_identity() -> None:
    r = replay([AdmitDatum("<a>"), AdmitDatum("<a>")])
    assert r.data == ("<a>",)


def test_admit_form_and_arity_validation() -> None:
    r = step(EMPTY, AdmitForm(2))
    assert r.forms == (2,)
    with pytest.raises(AdmissionError):
        step(EMPTY, AdmitForm(0))


def test_admit_inst_validation() -> None:
    base = replay([AdmitDatum("x"), AdmitDatum("y"), AdmitForm(2)])
    good = step(base, AdmitInst(0, (0, 1)))
    assert (0, (0, 1)) in good.insts
    with pytest.raises(AdmissionError):
        step(base, AdmitInst(1, (0, 1)))  # unknown form
    with pytest.raises(AdmissionError):
        step(base, AdmitInst(0, (0,)))  # arity mismatch
    with pytest.raises(AdmissionError):
        step(base, AdmitInst(0, (0, 2)))  # argument out of range


def test_admit_rule_all_validation() -> None:
    base = replay([AdmitDatum("x"), AdmitForm(1)])
    ruled = step(base, AdmitRuleAll(0))
    assert 0 in ruled.rules
    with pytest.raises(AdmissionError):
        step(base, AdmitRuleAll(3))


def test_impose_validation() -> None:
    base = replay([AdmitDatum("x"), AdmitDatum("y")])
    r = step(base, Impose(0, 1))
    assert (0, 1) in r.reqs
    with pytest.raises(AdmissionError):
        step(base, Impose(1, 0))
    with pytest.raises(AdmissionError):
        step(base, Impose(0, 2))


def test_replay_certify_and_tamper_detection() -> None:
    history = [AdmitDatum("x"), AdmitForm(1), AdmitInst(0, (0,))]
    r = replay(history)
    assert certify(history, r)
    tampered = Regime(
        r.data, r.forms, r.insts | {(0, (0,))} - {(0, (0,))} | set(), r.rules,
        frozenset({(0, 0)}),
    )
    assert not certify(history, tampered)


def test_replay_from_base_composes() -> None:
    h1 = [AdmitDatum("x")]
    h2 = [AdmitForm(1), AdmitInst(0, (0,))]
    assert replay(h1 + h2) == replay(h2, replay(h1))
