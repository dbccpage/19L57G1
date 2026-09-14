"""Unit tests for operational valuation pricing and asymptotic scaling."""

import pytest
from research.twin_pricing.python.valuation_pricing import (
    twin_count,
    mu1_scale,
    mu2_scale,
    cumulative_mu1,
    cumulative_mu2,
    cumulative_mu1_closed_form,
    cumulative_mu2_closed_form,
    markov_weighted_scale_cost,
    cumulative_markov_obstruction,
    verify_asymptotic_profile,
)


def test_twin_count():
    """Verify twin count formula across scales for c=2 and c=3."""
    for n in range(1, 10):
        assert twin_count(2, n) == 2 ** (n - 1)
        assert twin_count(3, n) == 2 * (3 ** (n - 1))


def test_mu1_scale_and_closed_form():
    """Verify mu1 pricing formulas and exact closed-form agreement."""
    for N in range(1, 16):
        # Scale cohort cost is 2^(N-1)
        assert mu1_scale(2, N) == 2 ** (N - 1)

        # Iterative sum agrees with 2^N - 1
        iter_cost = cumulative_mu1(2, N)
        closed_cost = cumulative_mu1_closed_form(N)
        assert iter_cost == closed_cost
        assert closed_cost == (2 ** N) - 1

        # Strict monotonicity
        if N > 1:
            assert cumulative_mu1(2, N) > cumulative_mu1(2, N - 1)


def test_mu2_scale_and_closed_form():
    """Verify mu2 pricing formulas and exact closed-form agreement."""
    for N in range(1, 16):
        # Scale cohort cost is N * 2^(N-1)
        assert mu2_scale(2, N) == N * (2 ** (N - 1))

        # Iterative sum agrees with (N - 1) * 2^N + 1
        iter_cost = cumulative_mu2(2, N)
        closed_cost = cumulative_mu2_closed_form(N)
        assert iter_cost == closed_cost
        assert closed_cost == (N - 1) * (2 ** N) + 1

        # Strict monotonicity
        if N > 1:
            assert cumulative_mu2(2, N) > cumulative_mu2(2, N - 1)


def test_markov_cylinder_weighted_measure():
    """Verify that Markov cylinder weighted cost is identically 0.5 per scale."""
    for n in range(1, 20):
        # 2^(-n) * 2^(n-1) = 0.5
        weighted = markov_weighted_scale_cost(n)
        assert abs(weighted - 0.5) < 1e-12

    # Linear divergence of cumulative Markov obstruction measure
    for N in range(1, 20):
        obs = cumulative_markov_obstruction(N)
        assert abs(obs - 0.5 * N) < 1e-12


def test_asymptotic_divergence():
    """Verify rapid divergence of cumulative costs as N grows."""
    # N = 10
    assert cumulative_mu1_closed_form(10) == 1023
    assert cumulative_mu2_closed_form(10) == 9 * 1024 + 1  # 9217

    # N = 20
    assert cumulative_mu1_closed_form(20) == 1048575
    assert cumulative_mu2_closed_form(20) == 19 * (2 ** 20) + 1

    # N = 30
    assert cumulative_mu1_closed_form(30) > 10 ** 9
    assert cumulative_mu2_closed_form(30) > 29 * (10 ** 9)


def test_verify_asymptotic_profile():
    """Verify comprehensive profiling harness."""
    result = verify_asymptotic_profile(max_N=15)
    assert len(result["verified_scales"]) == 15
    for N, c1, c2 in result["verified_scales"]:
        assert c1 == (2 ** N) - 1
        assert c2 == (N - 1) * (2 ** N) + 1


def test_negative_controls():
    """Verify input validation and error handling."""
    with pytest.raises(ValueError):
        twin_count(1, 1)
    with pytest.raises(ValueError):
        twin_count(2, 0)
    with pytest.raises(ValueError):
        cumulative_mu1(2, -1)
    with pytest.raises(ValueError):
        cumulative_mu2(2, -1)
    with pytest.raises(ValueError):
        markov_weighted_scale_cost(0)
    with pytest.raises(ValueError):
        cumulative_markov_obstruction(-1)


def test_large_scale_markov_cost_overflow_regression():
    """Verify that scale >= 1025 does not overflow float conversion."""
    for n in (1, 10, 1024, 1025, 2048, 10000):
        assert markov_weighted_scale_cost(n) == 0.5

    assert cumulative_markov_obstruction(1024) == 512.0
    assert cumulative_markov_obstruction(1025) == 512.5
    assert cumulative_markov_obstruction(2048) == 1024.0
    assert cumulative_markov_obstruction(10000) == 5000.0

