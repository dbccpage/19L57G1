"""Overlapping dyadic intervals and finite overlap-graph connectedness.

AuthorityEffect: None.

This module implements the companion Python model for Track 5:
1. DyadicInterval: Exact rational intervals [index / 2^scale, (index + 2) / 2^scale]
   of width 2^{-(scale - 1)}.
2. IntervalCover: Canonical dyadic covers of the unit interval [0, 1] with
   constructive overlapping chain extraction.
3. Partition boundary witness: locating an overlapping adjacent pair crossing a
   validated binary partition of a finite canonical cover.
4. Observable transport: checking constancy along the cover's overlap chain.
5. IntervalRewriteSystem: Confluent contraction to canonical normal forms.
6. Finite cover profile: exact resolutions and declared cover counts plus
   approximate logarithmic summaries.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from .projective_system import CoarseningMap, MoveEdge, MoveGraph


MAX_COVER_SCALE = 4096


def _require_natural(name: str, value: object) -> int:
    """Return an integer natural number, rejecting booleans and numeric lookalikes."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer, got {type(value).__name__}")
    if value < 0:
        raise ValueError(f"{name} must be non-negative, got {value}")
    return value


@dataclass(frozen=True)
class DyadicInterval:
    """Exact dyadic rational interval [index / 2^scale, (index + 2) / 2^scale].

    Every interval has width 2 / 2^scale = 1 / 2^{scale - 1}.
    Adjacent intervals at the same scale overlap on an interior of width 1 / 2^scale > 0.
    """

    scale: int
    index: int

    def __post_init__(self) -> None:
        _require_natural("scale", self.scale)
        _require_natural("index", self.index)

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

    def __post_init__(self) -> None:
        scale = _require_natural("scale", self.scale)
        if scale < 1:
            raise ValueError(f"Canonical cover requires scale >= 1, got {scale}")
        if not isinstance(self.intervals, tuple):
            raise TypeError("intervals must be a tuple")

        expected_count = (1 << scale) - 1
        if len(self.intervals) != expected_count:
            raise ValueError(
                f"canonical scale {scale} requires {expected_count} intervals, "
                f"got {len(self.intervals)}"
            )
        for expected_index, interval in enumerate(self.intervals):
            if not isinstance(interval, DyadicInterval):
                raise TypeError(f"intervals[{expected_index}] must be a DyadicInterval")
            if interval.scale != scale or interval.index != expected_index:
                raise ValueError(
                    f"intervals[{expected_index}] must equal "
                    f"DyadicInterval(scale={scale}, index={expected_index})"
                )

    @classmethod
    def canonical(cls, scale: int) -> IntervalCover:
        """Construct the canonical cover of [0, 1] at scale k >= 1.

        Intervals have index 0, 1, ..., 2^scale - 2.
        """
        scale = _require_natural("scale", scale)
        if scale < 1:
            raise ValueError(f"Canonical cover requires scale >= 1, got {scale}")
        num_intervals = (1 << scale) - 1
        items = tuple(DyadicInterval(scale, i) for i in range(num_intervals))
        return cls(scale=scale, intervals=items)

    def find_overlapping_chain(self, start_idx: int, target_idx: int) -> List[DyadicInterval]:
        """Constructively build an overlapping chain between two intervals in the cover."""
        if isinstance(start_idx, bool) or not isinstance(start_idx, int):
            raise TypeError(f"start_idx must be an integer, got {type(start_idx).__name__}")
        if isinstance(target_idx, bool) or not isinstance(target_idx, int):
            raise TypeError(f"target_idx must be an integer, got {type(target_idx).__name__}")
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

    def find_partition_boundary_overlap(
        self, set_a: Set[int], set_b: Set[int]
    ) -> Tuple[DyadicInterval, DyadicInterval]:
        """Return an adjacent overlap that crosses a validated binary partition.

        This is a finite overlap-graph witness. It is not, by itself, a theorem
        about a point-set topology on the represented real interval.
        """
        n = len(self.intervals)
        domain = set(range(n))
        if set_a & set_b:
            raise ValueError("set_a and set_b must be disjoint")
        if set_a | set_b != domain:
            raise ValueError("set_a and set_b must partition exactly the cover indices")
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

    def observable_is_constant_on_cover(
        self, observable: Callable[[DyadicInterval], Any]
    ) -> bool:
        """Check whether an observable is constant along every adjacent overlap.

        This finite equality-transport check does not assert a conventional
        intermediate-value theorem for an ordered codomain.
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
class FiniteCoverReport:
    """Declared finite-cover count with explicitly approximate log fields."""

    scale: int
    resolution: Fraction
    cover_count: int
    log2_cover_count: float
    approximate_log_ratio: float | None


def compute_cover_profile(max_scale: int) -> List[FiniteCoverReport]:
    """Compute declared canonical-cover counts for scales 1 through max_scale.

    Resolution epsilon_k = 2^{-(k - 1)}.
    Canonical cover count N(k) = 2^k - 1.
    The logarithm and ratio fields are floating approximations. The ratio is
    undefined at scale 1 and reported as None. No minimal-cover or limiting
    dimension claim follows from these finite summaries.
    """
    import math

    max_scale = _require_natural("max_scale", max_scale)
    if max_scale < 1:
        raise ValueError(f"max_scale must be >= 1, got {max_scale}")
    if max_scale > MAX_COVER_SCALE:
        raise ValueError(
            f"max_scale must be <= {MAX_COVER_SCALE}, got {max_scale}"
        )

    reports: List[FiniteCoverReport] = []
    for k in range(1, max_scale + 1):
        res = Fraction(1, 1 << (k - 1))
        n_cov = (1 << k) - 1
        log_n = math.log2(n_cov)
        ratio = log_n / float(k - 1) if k > 1 else None
        reports.append(
            FiniteCoverReport(
                scale=k,
                resolution=res,
                cover_count=n_cov,
                log2_cover_count=log_n,
                approximate_log_ratio=ratio,
            )
        )
    return reports


def create_interval_movegraph(scale: int) -> MoveGraph:
    """Create a discrete movegraph where states are DyadicInterval objects from the canonical cover.

    Edges connect adjacent overlapping intervals with exact operational step costs:
      mu1 = 1 / 2^scale  (overlap width / displacement)
      mu2 = 1 / 4^scale  (higher-order quadratic dissipation)
    """
    if not isinstance(scale, int) or isinstance(scale, bool) or scale < 1:
        raise ValueError(f"scale must be integer >= 1, got {scale}")

    cover = IntervalCover.canonical(scale)
    states = list(cover.intervals)
    step_mu1 = Fraction(1, 1 << scale)
    step_mu2 = Fraction(1, 1 << (2 * scale))

    edges: List[MoveEdge] = []
    for i in range(len(cover.intervals) - 1):
        u = cover.intervals[i]
        v = cover.intervals[i + 1]
        edges.append(
            MoveEdge(
                source=u,
                target=v,
                label=f"step_{i}->{i+1}",
                mu1=step_mu1,
                mu2=step_mu2,
            )
        )
        edges.append(
            MoveEdge(
                source=v,
                target=u,
                label=f"step_{i+1}->{i}",
                mu1=step_mu1,
                mu2=step_mu2,
            )
        )

    return MoveGraph.build(level=scale, states=states, edges=edges)


def create_interval_coarsening_map(coarse_scale: int, fine_scale: int) -> CoarseningMap:
    """Construct the canonical coarsening projection pi_{j, k} between interval movegraphs.

    Maps fine interval DyadicInterval(fine_scale, i) to
    DyadicInterval(coarse_scale, min(i >> (fine_scale - coarse_scale), 2^coarse_scale - 2)).
    """
    if (
        not isinstance(coarse_scale, int)
        or isinstance(coarse_scale, bool)
        or coarse_scale < 1
    ):
        raise ValueError(f"coarse_scale must be int >= 1, got {coarse_scale}")
    if (
        not isinstance(fine_scale, int)
        or isinstance(fine_scale, bool)
        or fine_scale < coarse_scale
    ):
        raise ValueError(
            f"fine_scale must be int >= coarse_scale ({coarse_scale}), got {fine_scale}"
        )

    fine_cover = IntervalCover.canonical(fine_scale)
    shift = fine_scale - coarse_scale
    max_coarse_idx = (1 << coarse_scale) - 2

    mapping: Dict[DyadicInterval, DyadicInterval] = {}
    for iv in fine_cover.intervals:
        c_idx = min(iv.index >> shift, max_coarse_idx)
        mapping[iv] = DyadicInterval(scale=coarse_scale, index=c_idx)

    return CoarseningMap(
        source_level=fine_scale,
        target_level=coarse_scale,
        state_map=mapping,
    )


@dataclass(frozen=True)
class CrossScaleCoverAnalysis:
    """Finite cross-scale cover-count and traversal-cost summary."""

    max_scale: int
    scale_reports: Tuple[FiniteCoverReport, ...]
    growth_ratios: Tuple[Fraction, ...]
    total_mu1_costs: Tuple[Fraction, ...]
    total_mu2_costs: Tuple[Fraction, ...]
    approximate_log_ratios: Tuple[float | None, ...]


def analyze_cross_scale_cover(max_scale: int) -> CrossScaleCoverAnalysis:
    """Summarize finite cover counts and traversal prices across declared scales."""
    if max_scale < 1:
        raise ValueError(f"max_scale must be >= 1, got {max_scale}")

    reports = tuple(compute_cover_profile(max_scale))
    growth_ratios_list: List[Fraction] = []
    total_mu1_list: List[Fraction] = []
    total_mu2_list: List[Fraction] = []
    approximate_ratios = [
        report.approximate_log_ratio for report in reports
    ]

    for k in range(1, max_scale + 1):
        step_count = (1 << k) - 2 if k >= 1 else 0
        total_mu1 = Fraction(step_count, 1 << k)
        total_mu2 = Fraction(step_count, 1 << (2 * k))
        total_mu1_list.append(total_mu1)
        total_mu2_list.append(total_mu2)

        n_cov = (1 << k) - 1
        if k < max_scale:
            next_cov = (1 << (k + 1)) - 1
            growth_ratios_list.append(Fraction(next_cov, n_cov))

    return CrossScaleCoverAnalysis(
        max_scale=max_scale,
        scale_reports=reports,
        growth_ratios=tuple(growth_ratios_list),
        total_mu1_costs=tuple(total_mu1_list),
        total_mu2_costs=tuple(total_mu2_list),
        approximate_log_ratios=tuple(approximate_ratios),
    )
