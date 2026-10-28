"""Tests of the finite model.  AuthorityEffect: None.

Each test re-runs a check of ``model.py`` and asserts the outcome the Lean
library proves.  A failing test means the model and the library disagree,
or the pins drifted; a passing test proves nothing beyond its bounds.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import model  # noqa: E402


def test_polarization_on_box() -> None:
    assert model.polarization_failures(model.load()["polarization_box"]) == []


def test_readout_separates_exactly_by_cross_term() -> None:
    assert model.fiber_pairs_without_cross_criterion(2) == 0


def test_instance_meets_challenge() -> None:
    report = model.instance_report()
    assert report["information_weights"] == 1
    assert report["information_with_readout"] == 3
    assert report["knows"] is False
    assert report["challenge"] is True
    assert report["readouts"] == [4, 2, 0]


def test_orbit_count_is_half_order_plus_one() -> None:
    for order in range(1, model.load()["max_order"] + 1):
        assert model.orbits(order) == order // 2 + 1


def test_least_order_is_two_k_minus_two() -> None:
    bound = model.load()
    for k in range(2, bound["max_multiplicity"] + 1):
        assert model.least_order(k, bound["max_order"]) == 2 * k - 2
    assert model.least_order(1, bound["max_order"]) == 1


def test_signs_carry_two_and_three_needs_four() -> None:
    assert model.orbits(2) == 2
    assert model.orbits(3) == 2
    assert model.orbits(4) == 3


def test_mu4_readout_is_conjugation_invariant() -> None:
    values = model.mu4_readouts()
    assert values == [4, 2, 0, 2]
    assert all(values[j] == values[(4 - j) % 4] for j in range(4))


def test_challenge_mentions_no_amplitude() -> None:
    """Encoding check: the challenge reads only presentations on the carrier."""
    carrier = [0, 1]
    assert model.challenge(carrier, [lambda x: 0], lambda x: x) is True
    assert model.challenge(carrier, [lambda x: x], lambda x: x) is False
