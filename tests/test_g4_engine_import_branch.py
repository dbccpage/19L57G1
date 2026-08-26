"""Tests for the finite G4 Challenge-3 correspondence."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from derivation.candidates import NewDatum, NewForm, NewInst, canonical_delta
from derivation.engine import READING_F, READING_L
from derivation.g4_engine_import_branch import (
    BOUNDS,
    FIRST_N,
    LAST_N,
    classify_mark,
    g4_report,
    minimum_classes,
    obstruction_stream,
)
from derivation.model import replay

import run_g4_engine_import_branch


def test_obstruction_stream_is_the_exact_declared_range() -> None:
    counts = [len(obstruction_stream(n)) for n in range(FIRST_N, LAST_N + 1)]
    assert counts == [1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91]
    assert sum(counts) == 455
    assert obstruction_stream(3) == ((1, 2),)
    with pytest.raises(ValueError):
        obstruction_stream(2)
    with pytest.raises(ValueError):
        obstruction_stream(16)


def test_mark_classifier_rejects_outside_arguments_and_wrong_shapes() -> None:
    base = replay(READING_F.genesis)
    target = READING_F.target
    unary = canonical_delta((NewForm(1), NewInst(0, (target[0],))))
    pair = canonical_delta((NewForm(2), NewInst(0, target)))
    outside = canonical_delta((NewForm(2), NewInst(0, (target[0], 0))))
    wrong_form = canonical_delta((NewForm(1), NewInst(1, (target[0],))))
    assert classify_mark(base, target, unary) == "unary_endpoint_mark"
    assert classify_mark(base, target, pair) == "pair_only_fresh_mark"
    assert classify_mark(base, target, outside) == "outside_target_argument"
    assert classify_mark(base, target, wrong_form) == "not_fresh_form_instance"
    assert classify_mark(base, target, (NewDatum(),)) == (
        "not_fresh_form_instance"
    )


def test_mu2_holds_in_both_readings() -> None:
    for reading in (READING_L, READING_F):
        classes = minimum_classes(reading, "mu2")
        assert len(classes) == 1
        assert classes[0].mark_class == "unary_endpoint_mark"
        assert classes[0].accepted_pair_mark


def test_mu1_reading_split_is_retained() -> None:
    l_classes = minimum_classes(READING_L, "mu1")
    f_classes = minimum_classes(READING_F, "mu1")
    assert len(l_classes) == 3
    assert all(item.accepted_pair_mark for item in l_classes)
    assert len(f_classes) == 5
    assert [item.mark_class for item in f_classes].count(
        "outside_target_argument"
    ) == 2
    assert BOUNDS.max_items == 2 and BOUNDS.max_arity == 2


def test_report_keeps_first_failure_and_exact_terminals() -> None:
    report = g4_report()
    assert report["total_obstructions_checked"] == 455
    assert report["measure_holds_in_every_reading"] == {
        "mu1": False,
        "mu2": True,
    }
    assert report["terminals"] == [
        "G4_HOLDS_UNDER_MU2",
        "G4_FAILS_AT_<3,mu1,reading_F_outside_target_argument>",
    ]
    failure = report["first_failure"]
    assert isinstance(failure, dict)
    assert failure["n"] == 3
    assert failure["chain_pair"] == [1, 2]
    assert failure["reading"] == "F"
    assert failure["measure"] == "mu1"


def test_runner_is_byte_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    assert run_g4_engine_import_branch.main(["--artifacts", str(first)]) == 0
    assert run_g4_engine_import_branch.main(["--artifacts", str(second)]) == 0
    left = first / "g4_engine_import_branch.json"
    right = second / "g4_engine_import_branch.json"
    assert left.read_bytes() == right.read_bytes()
    payload = json.loads(left.read_text(encoding="utf-8"))
    assert payload["bounds"]["first_n"] == 3
    assert payload["bounds"]["last_n"] == 15
