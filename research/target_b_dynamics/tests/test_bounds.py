"""Tests for bounds.py: Quantitative rational bounds, chain functionality, and non-density."""

from fractions import Fraction
import pytest

from bounds import (
    TWIST_TAPE,
    CompletionRefusal,
    is_chain,
    is_functional,
    pairs_of,
    precision_budget,
    rational_frequency,
    rational_frequency_error,
    refuse_circle_quotient,
    refuse_continuum_completion,
    refuse_dyadic_quotient,
    run_cycle_program,
    verify_rational_error_bound,
    verify_twist_tape_not_functional,
    verify_zeros_bounds,
    zeros,
    zeros_closed_form,
)


def test_zeros_formula_and_bounds() -> None:
    for length in range(1, 100):
        z = zeros(length)
        assert z == zeros_closed_form(length)
        assert verify_zeros_bounds(length) is True
        assert verify_rational_error_bound(length) is True


def test_rational_frequency_precision_budget() -> None:
    epsilons = [Fraction(1, 10), Fraction(1, 50), Fraction(1, 100), Fraction(1, 1000)]
    for eps in epsilons:
        l_req = precision_budget(eps)
        err = rational_frequency_error(l_req)
        assert err <= eps


def test_chain_functionality_and_twist_tape() -> None:
    # A genuine functional chain (e.g. cycle tape)
    cycle_tape = (0, 1, 2, 0, 1, 2, 0)
    pairs = pairs_of(cycle_tape)
    assert is_functional(pairs) is True

    # TWIST_TAPE contains (0, 1) and (0, 2)
    assert verify_twist_tape_not_functional() is True
    twist_pairs = pairs_of(TWIST_TAPE)
    assert is_functional(twist_pairs) is False

    # TWIST_TAPE cannot be a chain of any single-valued function
    cyc_next = lambda x: (x + 1) % 3
    assert is_chain(cyc_next, TWIST_TAPE) is False


def test_run_cycle_program_target_a() -> None:
    for steps in [3, 6, 12, 24, 48]:
        tape, z_count, freq, bound_ok = run_cycle_program(steps)
        length = steps + 1
        assert len(tape) == length
        assert z_count == zeros(length)
        assert bound_ok is True
        # Check rational frequency within bound
        assert abs(freq - Fraction(1, 3)) <= Fraction(2, 3 * length)


def test_refusal_handlers() -> None:
    with pytest.raises(CompletionRefusal, match="Refused continuum completion"):
        refuse_continuum_completion("thread space is R")

    with pytest.raises(CompletionRefusal, match="Refused circle completion"):
        refuse_circle_quotient("discrete cycle is S1")

    with pytest.raises(CompletionRefusal, match="Refused dyadic twin identification"):
        refuse_dyadic_quotient("0111... = 1000...")
