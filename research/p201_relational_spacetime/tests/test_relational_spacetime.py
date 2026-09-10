"""Unit tests for Target P201 / P202 Relational Quantities & Causal Clocks."""

from __future__ import annotations

from fractions import Fraction
import pytest

try:
    from research.p201_relational_spacetime.relational_spacetime import (
        CalibrationStandard,
        PhysicalDimension,
        RelationalQuantity,
        RelationalState,
        are_future_equivalent,
        compute_dimensionless_ratio,
        future_trajectory,
        measure_relative_clock_rate,
        step_relational,
        verify_p201_p202_invariants,
    )
except ModuleNotFoundError:
    from relational_spacetime import (
        CalibrationStandard,
        PhysicalDimension,
        RelationalQuantity,
        RelationalState,
        are_future_equivalent,
        compute_dimensionless_ratio,
        future_trajectory,
        measure_relative_clock_rate,
        step_relational,
        verify_p201_p202_invariants,
    )


def test_unit_covariance() -> None:
    u1 = CalibrationStandard("UnitA", PhysicalDimension.LENGTH, Fraction(1, 1))
    u2 = CalibrationStandard("UnitB", PhysicalDimension.LENGTH, Fraction(1, 10))

    q1 = RelationalQuantity(Fraction(5, 1), PhysicalDimension.LENGTH, u1)
    # Scale factor 1/10 implies value should be 5 / (1/10) = 50
    q2 = q1.rescale_standard(u2, scale_factor=Fraction(1, 10))
    assert q2.value == Fraction(50, 1)
    assert q2.standard == u2


def test_dimensionless_ratio_invariance() -> None:
    meter = CalibrationStandard("Meter", PhysicalDimension.LENGTH, Fraction(1, 1))
    cm = CalibrationStandard("Centimeter", PhysicalDimension.LENGTH, Fraction(1, 100))

    q_a1 = RelationalQuantity(Fraction(3, 1), PhysicalDimension.LENGTH, meter)
    q_b1 = RelationalQuantity(Fraction(9, 1), PhysicalDimension.LENGTH, meter)
    ratio1 = compute_dimensionless_ratio(q_a1, q_b1).unwrap()

    q_a2 = q_a1.rescale_standard(cm, Fraction(1, 100))
    q_b2 = q_b1.rescale_standard(cm, Fraction(1, 100))
    ratio2 = compute_dimensionless_ratio(q_a2, q_b2).unwrap()

    assert ratio1 == ratio2 == Fraction(1, 3)


def test_cross_dimension_refusal() -> None:
    meter = CalibrationStandard("Meter", PhysicalDimension.LENGTH, Fraction(1, 1))
    second = CalibrationStandard("Second", PhysicalDimension.DURATION, Fraction(1, 1))

    q_len = RelationalQuantity(Fraction(10, 1), PhysicalDimension.LENGTH, meter)
    q_dur = RelationalQuantity(Fraction(5, 1), PhysicalDimension.DURATION, second)

    res = compute_dimensionless_ratio(q_len, q_dur)
    assert res.is_err()
    assert "Refusal: dimension mismatch" in res.unwrap_err()


def test_future_test_congruence() -> None:
    s1 = RelationalState.create({"a": 10, "b": 1})
    s2 = RelationalState.create({"a": 10, "b": 1})
    assert are_future_equivalent(s1, s2, horizon=8)

    # Congruence: if s1 ~_F s2 then step(s1) ~_F step(s2)
    s1_next = step_relational(s1)
    s2_next = step_relational(s2)
    assert are_future_equivalent(s1_next, s2_next, horizon=8)


def test_relational_clock_synchronization_in_Q() -> None:
    s = RelationalState.create({"a": 0, "b": 0})
    for _ in range(16):
        s = step_relational(s)

    assert s.clock_fast.ticks == 16
    assert s.clock_slow.ticks == 8

    # Gear ratio: 16 / 8 = 2/1 in Q
    rate = measure_relative_clock_rate(RelationalState.create({"a": 0, "b": 0}), s).unwrap()
    assert rate == Fraction(2, 1)


def test_verify_invariants_comprehensive() -> None:
    res = verify_p201_p202_invariants()
    assert res["status"] == "PASS"
    assert res["unit_covariance_verified"] is True
    assert res["dimensionless_invariance_verified"] is True
    assert res["cross_dimension_refusal_verified"] is True
    assert res["future_test_congruence_verified"] is True
    assert res["relational_clock_synchronization_exact_in_Q"] is True
