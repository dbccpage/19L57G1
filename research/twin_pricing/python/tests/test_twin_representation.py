"""Unit tests for dyadic twin representations and quotient canonicalization."""

import pytest
from research.twin_pricing.python.twin_representation import (
    DyadicThread,
    generate_twin_pair,
    generate_scale_twins,
    are_elementary_twins,
    dyadic_valuation,
    canonical_quotient_key,
)


def test_scale_one_twins():
    """Verify scale 1 twins: 0·1^infty and 1·0^infty."""
    t_lo, t_hi = generate_twin_pair(1, ())
    assert t_lo.scale == 1
    assert t_hi.scale == 1
    assert t_lo.prefix == ()
    assert t_hi.prefix == ()

    # Differ at scale 1 (coordinate 0)
    assert t_lo.coordinate(0) == 0
    assert t_hi.coordinate(0) == 1
    assert t_lo.coordinate(0) != t_hi.coordinate(0)

    # Tail behavior
    assert t_lo.coordinate(1) == 1
    assert t_lo.coordinate(10) == 1
    assert t_hi.coordinate(1) == 0
    assert t_hi.coordinate(10) == 0

    assert are_elementary_twins(t_lo, t_hi)
    assert are_elementary_twins(t_hi, t_lo)


def test_twin_count_across_scales():
    """Verify that scale n generates exactly 2^(n-1) twin pairs."""
    for n in range(1, 8):
        twins = generate_scale_twins(n)
        assert len(twins) == 2 ** (n - 1)
        for t_lo, t_hi in twins:
            assert t_lo.scale == n
            assert t_hi.scale == n
            assert t_lo.prefix == t_hi.prefix
            assert t_lo.coordinate(n - 1) == 0
            assert t_hi.coordinate(n - 1) == 1
            assert are_elementary_twins(t_lo, t_hi)


def test_twins_differ_at_scale():
    """Verify that every twin pair differs at coordinate n - 1 (scale n)."""
    for n in range(1, 6):
        twins = generate_scale_twins(n)
        for t_lo, t_hi in twins:
            # Prefixes agree on 0..(n-2)
            for i in range(n - 1):
                assert t_lo.coordinate(i) == t_hi.coordinate(i)
            # Differ at coordinate n - 1
            assert t_lo.coordinate(n - 1) != t_hi.coordinate(n - 1)
            # Differ in thread space
            assert t_lo != t_hi


def test_dyadic_valuation_convergence():
    """Verify that numerical valuations of twin pairs agree in [0, 1]."""
    for n in range(1, 6):
        twins = generate_scale_twins(n)
        for t_lo, t_hi in twins:
            v_lo = dyadic_valuation(t_lo, depth=40)
            v_hi = dyadic_valuation(t_hi, depth=40)
            # Should agree within machine precision for depth 40
            assert abs(v_lo - v_hi) < 1e-11

            # Valuation should match the exact dyadic rational (2*int(w) + 1) / 2^n
            num, den = canonical_quotient_key(t_lo)
            exact_val = num / den
            assert abs(v_lo - exact_val) < 1e-11
            assert abs(v_hi - exact_val) < 1e-11


def test_canonical_quotient_identification():
    """Verify that canonical_quotient_key identifies lower and upper twins."""
    for n in range(1, 6):
        twins = generate_scale_twins(n)
        for t_lo, t_hi in twins:
            key_lo = canonical_quotient_key(t_lo)
            key_hi = canonical_quotient_key(t_hi)
            assert key_lo == key_hi
            # Check denominator is 2^n
            assert key_lo[1] == 2 ** n
            # Check numerator is odd
            assert key_lo[0] % 2 == 1


def test_invalid_thread_construction():
    """Negative controls on invalid thread construction."""
    with pytest.raises(ValueError):
        DyadicThread(prefix=(), discriminating_bit=0, tail_symbol=1, scale=0)
    with pytest.raises(ValueError):
        DyadicThread(prefix=(0, 1), discriminating_bit=0, tail_symbol=1, scale=2)
    with pytest.raises(ValueError):
        DyadicThread(prefix=(0,), discriminating_bit=2, tail_symbol=1, scale=2)
