"""Overlapping Dyadic Interval Domain & Constructive Connectedness.

AuthorityEffect: None.

This module implements the companion Python model for Track 5:
1. DyadicInterval: Exact rational intervals [index / 2^scale, (index + 2) / 2^scale]
   of width 2^{-(scale - 1)}.
2. IntervalCover: Canonical dyadic covers of the unit interval [0, 1] with
   constructive overlapping chain extraction.
3. Absence of Clopen Partition: Locating boundary overlapping pairs in any binary
   partition, demonstrating topological connectedness constructively.
4. Constructive Intermediate Value Property: Invariance of overlap-respecting
   observables across the cover.
5. IntervalRewriteSystem: Confluent contraction to canonical normal forms.
6. Metric Capacity Scaling: Exact rational calculation of covering capacity
   and discrete dimensional scaling.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable, List, Optional, Set, Tuple


@dataclass(frozen=True)
class DyadicInterval:
    """Exact dyadic rational interval [index / 2^scale, (index + 2) / 2^scale].

    Every interval has width 2 / 2^scale = 1 / 2^{scale - 1}.
    Adjacent intervals at the same scale overlap on an interior of width 1 / 2^scale > 0.
    """

    scale: int
    index: int

    def __post_init__(self) -> None:
        if self.scale < 0:
            raise ValueError(f"scale must be non-negative, got {self.scale}")
        if self.index < 0:
            raise ValueError(f"index must be non-negative, got {self.index}")

    @property
    def left_endpoint(self) -> Fraction:
        """Exact rational left endpoint: index / 2^scale."""
        return Fraction(self.index, 1 << self.scale)

    @property
    def right_endpoint(self) -> Fraction:
        """Exact rational right endpoint: (index + 2) / 2^scale."""
        return Fraction(self.index + 2, 1 << self.scale)

    @property
    def midpoint(self) -> Fraction:
        """Exact rational midpoint: (index + 1) / 2^scale."""
        return Fraction(self.index + 1, 1 << self.scale)

    @property
    def width(self) -> Fraction:
        """Exact rational interval width: 2 / 2^scale = 1 / 2^{scale - 1}."""
        return Fraction(2, 1 << self.scale)

    def overlaps(self, other: DyadicInterval) -> bool:
        """Check whether two dyadic intervals have non-empty open interior intersection.

        Uses exact integer cross-multiplication:
        left1 * 2^scale2 < right2 * 2^scale1 and left2 * 2^scale1 < right1 * 2^scale2.
        """
        pow1 = 1 << self.scale
        pow2 = 1 << other.scale
        left1_scaled = self.index * pow2
        right2_scaled = (other.index + 2) * pow1
        left2_scaled = other.index * pow1
        right1_scaled = (self.index + 2) * pow2
        return left1_scaled < right2_scaled and left2_scaled < right1_scaled

    def intersection(self, other: DyadicInterval) -> Optional[Tuple[Fraction, Fraction]]:
        """Compute exact rational intersection interval if overlapping, else None."""
        if not self.overlaps(other):
            return None
        inter_left = max(self.left_endpoint, other.left_endpoint)
        inter_right = min(self.right_endpoint, other.right_endpoint)
        return (inter_left, inter_right)

    def refine(self) -> Tuple[DyadicInterval, DyadicInterval, DyadicInterval]:
        """Refine this interval into three overlapping subintervals at scale + 1.

        Child 0: [2*index / 2^{s+1}, (2*index + 2) / 2^{s+1}]
        Child 1: [(2*index + 1) / 2^{s+1}, (2*index + 3) / 2^{s+1}]
        Child 2: [(2*index + 2) / 2^{s+1}, (2*index + 4) / 2^{s+1}]
        """
        next_scale = self.scale + 1
        return (
            DyadicInterval(next_scale, 2 * self.index),
            DyadicInterval(next_scale, 2 * self.index + 1),
            DyadicInterval(next_scale, 2 * self.index + 2),
        )


@dataclass(frozen=True)
class IntervalCover:
    """Canonical overlapping dyadic cover of [0, 1] at scale k >= 1."""

    scale: int
    intervals: Tuple[DyadicInterval, ...]

    @classmethod
    def canonical(cls, scale: int) -> IntervalCover:
        """Construct the canonical cover of [0, 1] at scale k >= 1.

        Intervals have index 0, 1, ..., 2^scale - 2.
        """
        if scale < 1:
            raise ValueError(f"Canonical cover requires scale >= 1, got {scale}")
        num_intervals = (1 << scale) - 1
        items = tuple(DyadicInterval(scale, i) for i in range(num_intervals))
        return cls(scale=scale, intervals=items)

    def find_overlapping_chain(self, start_idx: int, target_idx: int) -> List[DyadicInterval]:
        """Constructively build an overlapping chain between two intervals in the cover."""
        if not (0 <= start_idx < len(self.intervals)):
            raise IndexError(f"start_idx {start_idx} out of range [0, {len(self.intervals)})")
        if not (0 <= target_idx < len(self.intervals)):
            raise IndexError(f"target_idx {target_idx} out of range [0, {len(self.intervals)})")

        if start_idx <= target_idx:
            step_dir = 1
            indices = list(range(start_idx, target_idx + 1, step_dir))
        else:
            step_dir = -1
            indices = list(range(start_idx, target_idx - 1, step_dir))

        chain = [self.intervals[idx] for idx in indices]
        # Verify chain connectivity
        for k in range(len(chain) - 1):
            if not chain[k].overlaps(chain[k + 1]):
                raise RuntimeError(
                    f"Chain connectivity broken between {chain[k]} and {chain[k + 1]}"
                )
        return chain

    def verify_no_clopen_partition(
        self, set_a: Set[int], set_b: Set[int]
    ) -> Tuple[DyadicInterval, DyadicInterval]:
        """Verify the absence of a clopen partition between set_a and set_b.

        Given a binary partition of cover indices where 0 in set_a and (N-1) in set_b,
        constructively returns the transition pair (I_m, I_{m+1}) where m in set_a
        and m+1 in set_b, verifying that the boundary strictly overlaps.
        """
        n = len(self.intervals)
        if 0 not in set_a:
            raise ValueError("set_a must contain index 0")
        if (n - 1) not in set_b:
            raise ValueError(f"set_b must contain the terminal index {n - 1}")

        # Locate first transition
        for m in range(n - 1):
            if m in set_a and (m + 1) in set_b:
                int_a = self.intervals[m]
                int_b = self.intervals[m + 1]
                if not int_a.overlaps(int_b):
                    raise RuntimeError(f"Unexpected non-overlap between adjacent {int_a} and {int_b}")
                return (int_a, int_b)

        raise RuntimeError("No transition index found; partition hypothesis violated")

    def check_intermediate_value_property(
        self, observable: Callable[[DyadicInterval], Any]
    ) -> bool:
        """Check whether an overlap-respecting observable is constant across the entire cover.

        If for all adjacent (and hence overlapping) intervals I_m, I_{m+1},
        observable(I_m) == observable(I_{m+1}), then observable(I_0) == observable(I_{N-1}).
        """
        n = len(self.intervals)
        first_val = observable(self.intervals[0])
        for i in range(n - 1):
            curr_val = observable(self.intervals[i])
            next_val = observable(self.intervals[i + 1])
            if curr_val != next_val:
                return False
        last_val = observable(self.intervals[n - 1])
        return bool(first_val == last_val)


class IntervalRewriteSystem:
    """Confluent rewrite reduction on dyadic intervals contracting toward minimal index."""

    @staticmethod
    def step(interval: DyadicInterval) -> Optional[DyadicInterval]:
        """One-step rewrite reduction: contracts index by 1 if index > 0."""
        if interval.index == 0:
            return None
        return DyadicInterval(interval.scale, interval.index - 1)

    @classmethod
    def normalize(cls, interval: DyadicInterval) -> Tuple[DyadicInterval, int]:
        """Reduce interval to irreducible normal form (scale, 0), returning steps taken."""
        steps = 0
        curr = interval
        while True:
            nxt = cls.step(curr)
            if nxt is None:
                break
            curr = nxt
            steps += 1
        return curr, steps

    @classmethod
    def verify_local_confluence(cls, scale: int, max_index: int) -> bool:
        """Verify local confluence: any one-step divergence joins at the common normal form."""
        for i in range(max_index + 1):
            inv = DyadicInterval(scale, i)
            # The rewrite is deterministic, hence trivially locally confluent
            step1 = cls.step(inv)
            step2 = cls.step(inv)
            if step1 != step2:
                return False
            norm1, _ = cls.normalize(inv)
            norm2, _ = cls.normalize(inv)
            if norm1 != norm2 or norm1.index != 0:
                return False
        return True


@dataclass(frozen=True)
class MetricCapacityReport:
    """Metric capacity scaling report over dyadic resolution levels."""

    scale: int
    resolution: Fraction
    covering_number: int
    log2_covering: float
    capacity_ratio: float


def compute_capacity_profile(max_scale: int) -> List[MetricCapacityReport]:
    """Compute metric capacity profile over scales k = 1 .. max_scale.

    Resolution epsilon_k = 2^{-(k - 1)}.
    Covering number N(epsilon_k) = 2^k - 1.
    Scaling dimension: log2(N(epsilon_k)) / log2(1 / epsilon_k) -> 1.0 as k -> infty.
    """
    import math

    if max_scale < 1:
        raise ValueError(f"max_scale must be >= 1, got {max_scale}")

    reports: List[MetricCapacityReport] = []
    for k in range(1, max_scale + 1):
        res = Fraction(1, 1 << (k - 1))
        n_cov = (1 << k) - 1
        log_n = math.log2(n_cov)
        denom = float(k - 1) if k > 1 else 1.0
        ratio = log_n / denom if k > 1 else 0.0
        reports.append(
            MetricCapacityReport(
                scale=k,
                resolution=res,
                covering_number=n_cov,
                log2_covering=log_n,
                capacity_ratio=ratio,
            )
        )
    return reports
