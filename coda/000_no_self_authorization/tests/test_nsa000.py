"""100% coverage of src/nsa000. AuthorityEffect: None."""

from __future__ import annotations

from pathlib import Path

import pytest

from nsa000.born_lift import (
    born_from_weights,
    modulus_squared,
    optional_amplitude_lift,
)
from nsa000.figures import write_default
from nsa000.gauges import Castle, better, height_measure, width_measure
from nsa000.selection import evaluate_set, report_one
from nsa000.ties import Orientation, cost_two_orientations, iso_classes


def test_gauges_reverse() -> None:
    a = Castle("A", height=3.0, width=1.0)
    b = Castle("B", height=1.0, width=3.0)
    assert better(a, b, height_measure) == "A"
    assert better(a, b, width_measure) == "B"
    assert better(a, a, height_measure) == "tie"


def test_ties_three_concrete_two_classes() -> None:
    items = cost_two_orientations()
    assert len(items) == 3
    classes = iso_classes(items)
    assert len(classes) == 2
    assert items[2] == items[0].flipped()


def test_iso_self_flip_and_merge() -> None:
    x = Orientation(marked="L", label="same")
    # already-grouped mate path: pass flip after original
    classes = iso_classes((x, x.flipped()))
    assert len(classes) == 1
    # singleton with no mate present
    lone = iso_classes((x,))
    assert len(lone) == 1


def test_selection_unauthorized_when_undeclared() -> None:
    pool = evaluate_set(frozenset({1, 2, 3}))
    silent = report_one(pool, 2, declare=False)
    open_ = report_one(pool, 2, declare=True)
    assert silent.unauthorized
    assert not open_.unauthorized
    assert silent.pool_size == 3


def test_selection_errors() -> None:
    with pytest.raises(ValueError):
        evaluate_set(frozenset())
    with pytest.raises(ValueError):
        report_one(frozenset({1}), 9, declare=True)


def test_born_and_lift() -> None:
    w = (1.0, 3.0)
    p = born_from_weights(w)
    assert abs(sum(p) - 1.0) < 1e-12
    amps = optional_amplitude_lift(w, (0.0, 1.2))
    recovered = born_from_weights(modulus_squared(amps))
    assert all(abs(a - b) < 1e-12 for a, b in zip(p, recovered))


def test_born_errors() -> None:
    with pytest.raises(ValueError):
        born_from_weights((-1.0, 1.0))
    with pytest.raises(ValueError):
        born_from_weights((0.0, 0.0))
    with pytest.raises(ValueError):
        optional_amplitude_lift((1.0, 1.0), (0.0,))


def test_figures(tmp_path: Path) -> None:
    a, b = write_default(tmp_path)
    assert a.is_file() and a.stat().st_size > 0
    assert b.is_file() and b.stat().st_size > 0
