"""Tests for spacelike non-signaling and marginal distribution invariance."""

import pytest
from embedded_observer import create_duplicate_observers
from non_signaling import (
    compute_marginal_r2_distribution,
    simulate_causal_propagation_contrast,
    simulate_correlated_pair_protocol,
    total_variation_distance,
    verify_spacelike_non_signaling,
)
from protocol import CarrierState


def test_spacelike_non_signaling_exhaustive_interventions() -> None:
    _, obs2 = create_duplicate_observers(probe_fn=lambda x: x % 4)

    # Balanced ensemble of 100 states
    states = [
        CarrierState(l1=a, l2=b, m=0, r1=0, r2=0)
        for a in range(10)
        for b in range(10)
    ]

    interventions = {
        "identity": lambda x: x,
        "shift_1": lambda x: (x + 1) % 10,
        "shift_5": lambda x: (x + 5) % 10,
        "constant_zero": lambda x: 0,
        "constant_nine": lambda x: 9,
        "multiplier": lambda x: (x * 3) % 10,
    }

    report = verify_spacelike_non_signaling(states, interventions, obs2)
    assert report.non_signaling_satisfied
    assert report.max_total_variation_distance == 0.0
    assert report.total_states_tested == 100


def test_non_signaling_on_skewed_ensemble() -> None:
    _, obs2 = create_duplicate_observers(probe_fn=lambda x: x)

    # Skewed state distribution: L1 is highly non-uniform, L2 is arbitrary
    states = (
        [CarrierState(l1=0, l2=1)] * 50
        + [CarrierState(l1=1, l2=2)] * 30
        + [CarrierState(l1=2, l2=1)] * 20
    )

    interventions = {
        "noop": lambda x: x,
        "invert": lambda x: 2 - x,
        "set_constant": lambda x: 99,
    }

    report = verify_spacelike_non_signaling(states, interventions, obs2)
    assert report.non_signaling_satisfied
    assert report.max_total_variation_distance == 0.0


def test_correlated_pair_coincidence_without_signaling() -> None:
    res = simulate_correlated_pair_protocol(
        n_trials=400,
        modulus=4,
        intervention_1=lambda x: (x + 1) % 4,
    )
    assert res["unperturbed_coincidence_rate"] == 1.0
    assert res["is_non_signaling"]
    assert res["marginal_tvd"] == 0.0


def test_causal_propagation_contrast_distinguishes_signaling() -> None:
    res = simulate_causal_propagation_contrast(
        CarrierState(),
        intervention_val=7,
    )
    # Spacelike: zero shift
    assert not res["spacelike_shift_detected"]
    # Post-propagation through M: shift detected
    assert res["causal_shift_detected"]
    assert res["information_transferred_post_coupling"]
