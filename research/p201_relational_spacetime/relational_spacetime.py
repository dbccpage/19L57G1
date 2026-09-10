"""Target P201 / P202: Relational Dimensions, Calibration & Causal Relational Clocks.

This module formalizes:
1. Relational quantities, typed dimensions, and unit covariance.
2. Exact dimensionless invariants independent of reference calibration standards.
3. Causal dependency, endogenous succession, and future-test state congruence.
4. Embedded relational clocks and clock synchronization with exact rational rates in Q.
5. Prohibition of external time schedulers and illegal cross-dimensional scalarization.

AuthorityEffect: None.
Claim Hygiene: Discrete finite carrier models; all properties exact and constructive.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Any, Callable, Generic, Mapping, Sequence, TypeVar

T = TypeVar("T")
E = TypeVar("E")


@dataclass(frozen=True)
class Result(Generic[T, E]):
    """Monadic Result type for explicit failure and refusal tracking."""

    _value: T | None
    _error: E | None
    _is_ok: bool

    @classmethod
    def ok(cls, value: T) -> Result[T, E]:
        return cls(_value=value, _error=None, _is_ok=True)

    @classmethod
    def err(cls, error: E) -> Result[T, E]:
        return cls(_value=None, _error=error, _is_ok=False)

    def is_ok(self) -> bool:
        return self._is_ok

    def is_err(self) -> bool:
        return not self._is_ok

    def unwrap(self) -> T:
        if not self._is_ok:
            raise ValueError(f"Called unwrap on Err: {self._error}")
        assert self._value is not None
        return self._value

    def unwrap_err(self) -> E:
        if self._is_ok:
            raise ValueError("Called unwrap_err on Ok")
        assert self._error is not None
        return self._error


class PhysicalDimension(Enum):
    LENGTH = "LENGTH"
    DURATION = "DURATION"
    COUNT = "COUNT"
    ACTION = "ACTION"


@dataclass(frozen=True)
class CalibrationStandard:
    """An admitted reference standard fixing a unit of measurement."""

    name: str
    dimension: PhysicalDimension
    base_magnitude: Fraction  # Relative to internal substrate ticks


@dataclass(frozen=True)
class RelationalQuantity:
    """A quantity measured relationally with respect to a chosen reference standard."""

    value: Fraction  # Measured numerical value Q(x; U) in Q
    dimension: PhysicalDimension
    standard: CalibrationStandard

    def rescale_standard(
        self, new_standard: CalibrationStandard, scale_factor: Fraction
    ) -> RelationalQuantity:
        """Unit covariance: If standard is scaled by lambda (U' = lambda U),
        the measured quantity transforms as lambda^(-1) * value.
        """
        if self.dimension != new_standard.dimension:
            raise ValueError("Cannot rescale standard across different dimensions")
        if scale_factor <= Fraction(0, 1):
            raise ValueError("Scale factor must be strictly positive")
        return RelationalQuantity(
            value=self.value / scale_factor,
            dimension=self.dimension,
            standard=new_standard,
        )


def compute_dimensionless_ratio(
    q1: RelationalQuantity, q2: RelationalQuantity
) -> Result[Fraction, str]:
    """Compute the dimensionless ratio between two quantities of identical dimension.

    Theorem: The ratio q1 / q2 is independent of the choice of reference standard.
    Fails with explicit refusal if dimensions mismatch (preventing illegal scalarization).
    """
    if q1.dimension != q2.dimension:
        return Result.err(
            f"Refusal: dimension mismatch between {q1.dimension.value} and {q2.dimension.value}"
        )
    if q2.value == Fraction(0, 1):
        return Result.err("Refusal: division by zero magnitude")

    # If standards differ, convert to common base magnitude
    mag1 = q1.value * q1.standard.base_magnitude
    mag2 = q2.value * q2.standard.base_magnitude
    return Result.ok(mag1 / mag2)


# -----------------------------------------------------------------------------
# P202: Causal Dependency, Future-Test Congruence & Relational Clocks
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class ClockSubsystem:
    """An internal monotonic counter representing an embedded relational clock."""

    ticks: int
    period: int  # Ticks every 'period' global steps


@dataclass(frozen=True)
class RelationalState:
    """Carrier state with internal relational clocks and registers."""

    registers: tuple[tuple[str, int], ...]
    clock_fast: ClockSubsystem  # Advances every step (period=1)
    clock_slow: ClockSubsystem  # Advances every 2 steps (period=2)
    step_index: int

    @classmethod
    def create(cls, registers: Mapping[str, int]) -> RelationalState:
        return cls(
            registers=tuple(sorted(registers.items())),
            clock_fast=ClockSubsystem(ticks=0, period=1),
            clock_slow=ClockSubsystem(ticks=0, period=2),
            step_index=0,
        )

    def get_reg(self, name: str) -> int:
        for k, v in self.registers:
            if k == name:
                return v
        raise KeyError(name)

    def observable_readout(self) -> tuple[int, ...]:
        """Projected observable readout at current step."""
        return tuple(v for _, v in self.registers)


def step_relational(state: RelationalState) -> RelationalState:
    """Endogenous transition step advancing internal clocks and mutating registers."""
    next_step = state.step_index + 1
    next_fast = ClockSubsystem(ticks=state.clock_fast.ticks + 1, period=1)
    next_slow_ticks = state.clock_slow.ticks + (1 if next_step % 2 == 0 else 0)
    next_slow = ClockSubsystem(ticks=next_slow_ticks, period=2)

    # Dynamic transition rule: increment reg_a, cycle reg_b mod 4
    new_regs = {
        "a": state.get_reg("a") + 1,
        "b": (state.get_reg("b") + 1) % 4,
    }
    return RelationalState(
        registers=tuple(sorted(new_regs.items())),
        clock_fast=next_fast,
        clock_slow=next_slow,
        step_index=next_step,
    )


def future_trajectory(state: RelationalState, horizon: int) -> tuple[tuple[int, ...], ...]:
    """Compute trajectory of future observable readouts up to horizon."""
    curr = state
    trajectory = []
    for _ in range(horizon):
        trajectory.append(curr.observable_readout())
        curr = step_relational(curr)
    return tuple(trajectory)


def are_future_equivalent(
    s1: RelationalState, s2: RelationalState, horizon: int
) -> bool:
    """Check future-test equivalence: identical observable trajectories for horizon steps."""
    return future_trajectory(s1, horizon) == future_trajectory(s2, horizon)


def measure_relative_clock_rate(
    initial: RelationalState, final: RelationalState
) -> Result[Fraction, str]:
    """Compute the relative rate between slow and fast embedded relational clocks in Q."""
    delta_fast = final.clock_fast.ticks - initial.clock_fast.ticks
    delta_slow = final.clock_slow.ticks - initial.clock_slow.ticks
    if delta_slow == 0:
        return Result.err("Zero elapsed duration on slow clock")
    return Result.ok(Fraction(delta_fast, delta_slow))


def verify_p201_p202_invariants() -> dict[str, Any]:
    """Comprehensive check of relational dimensions, covariance, and clock synchronization."""
    # 1. P201 Unit Covariance & Dimensionless Invariants:
    meter = CalibrationStandard("Meter", PhysicalDimension.LENGTH, Fraction(1, 1))
    cm = CalibrationStandard("Centimeter", PhysicalDimension.LENGTH, Fraction(1, 100))

    # Object X has magnitude 2 meters
    q_x_meter = RelationalQuantity(Fraction(2, 1), PhysicalDimension.LENGTH, meter)
    # Rescale to cm: scale factor is 1/100, measured value is 2 / (1/100) = 200
    q_x_cm = q_x_meter.rescale_standard(cm, scale_factor=Fraction(1, 100))
    assert q_x_cm.value == Fraction(200, 1)

    # Object Y has magnitude 5 meters (500 cm)
    q_y_meter = RelationalQuantity(Fraction(5, 1), PhysicalDimension.LENGTH, meter)
    q_y_cm = q_y_meter.rescale_standard(cm, scale_factor=Fraction(1, 100))

    ratio_in_meters = compute_dimensionless_ratio(q_x_meter, q_y_meter).unwrap()
    ratio_in_cm = compute_dimensionless_ratio(q_x_cm, q_y_cm).unwrap()
    assert ratio_in_meters == ratio_in_cm == Fraction(2, 5)

    # Cross-dimensional ratio refusal
    second = CalibrationStandard("Second", PhysicalDimension.DURATION, Fraction(1, 1))
    q_dur = RelationalQuantity(Fraction(3, 1), PhysicalDimension.DURATION, second)
    cross_res = compute_dimensionless_ratio(q_x_meter, q_dur)
    assert cross_res.is_err()
    assert "Refusal" in cross_res.unwrap_err()

    # 2. P202 Future-Test Congruence:
    s_init1 = RelationalState.create({"a": 0, "b": 0})
    s_init2 = RelationalState.create({"a": 0, "b": 0})
    assert are_future_equivalent(s_init1, s_init2, horizon=10)

    # Step congruence: step(s1) ~_F step(s2)
    s_step1 = step_relational(s_init1)
    s_step2 = step_relational(s_init2)
    assert are_future_equivalent(s_step1, s_step2, horizon=10)

    # 3. P202 Relational Clock Synchronization:
    curr = s_init1
    for _ in range(10):
        curr = step_relational(curr)
    rate_res = measure_relative_clock_rate(s_init1, curr)
    assert rate_res.is_ok()
    # Ratio of fast clock ticks to slow clock ticks: 10 fast / 5 slow = 2 / 1
    assert rate_res.unwrap() == Fraction(2, 1)

    return {
        "status": "PASS",
        "unit_covariance_verified": True,
        "dimensionless_invariance_verified": True,
        "cross_dimension_refusal_verified": True,
        "future_test_congruence_verified": True,
        "relational_clock_synchronization_exact_in_Q": True,
    }
