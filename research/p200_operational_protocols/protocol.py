"""Operational protocols embedded within the process carrier.

Defines:
- Multi-locus carrier state: target physical loci, mediating channels,
  and embedded observer record registers.
- Footprints and Bernstein disjointness.
- Operational protocol stages:
  1. Preparations (initializing state regions)
  2. Interventions (local perturbations at designated loci)
  3. Records (persistent memory marks in dedicated observer registers)
  4. Comparisons (coincidence evaluators and record distances)
  5. Embedded measurement instruments (non-disturbing and disturbing readouts)

AuthorityEffect: None.
Axiom Scope: Constructive finite carrier operations with zero host oracles.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Optional, Tuple


class Locus(Enum):
    """Discrete loci within the carrier substrate."""

    L1 = auto()    # Target physical subsystem 1
    L2 = auto()    # Target physical subsystem 2
    M = auto()     # Shared coupling / mediating channel
    R1 = auto()    # Embedded observer 1 record register
    R2 = auto()    # Embedded observer 2 record register
    DIST = auto()  # Disturbance diagnostic register


@dataclass(frozen=True)
class CarrierState:
    """Discrete state of the multi-locus carrier."""

    l1: int = 0
    l2: int = 0
    m: int = 0
    r1: int = 0
    r2: int = 0
    dist: int = 0

    def is_valid(self, n1: int, n2: int, nm: int, nr1: int, nr2: int) -> bool:
        """Check whether coordinates satisfy capacity limits."""
        return (
            0 <= self.l1 < n1
            and 0 <= self.l2 < n2
            and 0 <= self.m < nm
            and 0 <= self.r1 < nr1
            and 0 <= self.r2 < nr2
            and self.dist >= 0
        )

    def to_tuple(self) -> Tuple[int, int, int, int, int, int]:
        return (self.l1, self.l2, self.m, self.r1, self.r2, self.dist)


@dataclass(frozen=True)
class Footprint:
    """Read and write footprints across carrier loci."""

    reads: frozenset[Locus]
    writes: frozenset[Locus]

    def is_disjoint(self, other: Footprint) -> bool:
        """Check Bernstein disjointness conditions:

        1. No write-write conflict: writes & other.writes == empty
        2. No read-write conflict: reads & other.writes == empty
        3. No write-read conflict: writes & other.reads == empty
        """
        if self.writes & other.writes:
            return False
        if self.reads & other.writes:
            return False
        if self.writes & other.reads:
            return False
        return True


# -------------------------------------------------------------------------
# Preparations: Initializing state regions
# -------------------------------------------------------------------------

def prepare_product(s: CarrierState, v1: int, v2: int, m: int = 0) -> CarrierState:
    """Prepare independent product state on L1 and L2, clearing records."""
    return CarrierState(l1=v1, l2=v2, m=m, r1=0, r2=0, dist=0)


def prepare_symmetric(s: CarrierState, v: int, m: int = 0) -> CarrierState:
    """Prepare symmetric correlated state where l1 == l2."""
    return CarrierState(l1=v, l2=v, m=m, r1=0, r2=0, dist=0)


# -------------------------------------------------------------------------
# Interventions: Local perturbations at designated loci
# -------------------------------------------------------------------------

def intervene_l1(s: CarrierState, f: Callable[[int], int]) -> CarrierState:
    """Apply local intervention strictly at Locus 1."""
    return CarrierState(l1=f(s.l1), l2=s.l2, m=s.m, r1=s.r1, r2=s.r2, dist=s.dist)


def intervene_l2(s: CarrierState, g: Callable[[int], int]) -> CarrierState:
    """Apply local intervention strictly at Locus 2."""
    return CarrierState(l1=s.l1, l2=g(s.l2), m=s.m, r1=s.r1, r2=s.r2, dist=s.dist)


def intervene_m(s: CarrierState, h: Callable[[int], int]) -> CarrierState:
    """Apply intervention at shared coupling locus M."""
    return CarrierState(l1=s.l1, l2=s.l2, m=h(s.m), r1=s.r1, r2=s.r2, dist=s.dist)


# -------------------------------------------------------------------------
# Records: Persistent marks in dedicated observer registers
# -------------------------------------------------------------------------

def record_1(s: CarrierState, val: int) -> CarrierState:
    """Write persistent record mark into Observer 1 register R1."""
    return CarrierState(l1=s.l1, l2=s.l2, m=s.m, r1=val, r2=s.r2, dist=s.dist)


def record_2(s: CarrierState, val: int) -> CarrierState:
    """Write persistent record mark into Observer 2 register R2."""
    return CarrierState(l1=s.l1, l2=s.l2, m=s.m, r1=s.r1, r2=val, dist=s.dist)


# -------------------------------------------------------------------------
# Comparisons: Coincidence evaluators and record distances
# -------------------------------------------------------------------------

def coincidence_evaluator(s: CarrierState) -> bool:
    """Evaluate whether recorded marks of Observer 1 and Observer 2 match."""
    return s.r1 == s.r2


def record_distance(s: CarrierState) -> int:
    """Compute absolute difference between observer records."""
    return abs(s.r1 - s.r2)


# -------------------------------------------------------------------------
# Embedded Measurement Instruments
# -------------------------------------------------------------------------

@dataclass(frozen=True)
class MeasurementInstrument:
    """An embedded measurement instrument executing within the carrier."""

    name: str
    target_locus: Locus
    record_locus: Locus
    probe_fn: Callable[[int], int]
    is_disturbing: bool = False
    disturb_fn: Optional[Callable[[int], int]] = None
    disturbance_cost: int = 0

    @property
    def footprint(self) -> Footprint:
        """Derive operational access footprint."""
        reads = {self.target_locus}
        writes = {self.record_locus}
        if self.is_disturbing:
            writes.add(self.target_locus)
            writes.add(Locus.DIST)
        return Footprint(reads=frozenset(reads), writes=frozenset(writes))

    def execute(self, s: CarrierState) -> CarrierState:
        """Execute instrument readout on carrier state."""
        target_val = int(getattr(s, self.target_locus.name.lower()))
        measured_val = self.probe_fn(target_val)

        new_l1 = s.l1
        new_l2 = s.l2
        new_dist = s.dist

        if self.is_disturbing and self.disturb_fn is not None:
            disturbed_val = self.disturb_fn(target_val)
            if self.target_locus == Locus.L1:
                new_l1 = disturbed_val
            elif self.target_locus == Locus.L2:
                new_l2 = disturbed_val
            new_dist += self.disturbance_cost

        new_r1 = measured_val if self.record_locus == Locus.R1 else s.r1
        new_r2 = measured_val if self.record_locus == Locus.R2 else s.r2

        return CarrierState(
            l1=new_l1,
            l2=new_l2,
            m=s.m,
            r1=new_r1,
            r2=new_r2,
            dist=new_dist,
        )


def non_disturbing_readout_1(
    s: CarrierState, probe_fn: Callable[[int], int] = lambda x: x
) -> CarrierState:
    """Standard non-disturbing readout of L1 into R1."""
    return CarrierState(l1=s.l1, l2=s.l2, m=s.m, r1=probe_fn(s.l1), r2=s.r2, dist=s.dist)


def non_disturbing_readout_2(
    s: CarrierState, probe_fn: Callable[[int], int] = lambda x: x
) -> CarrierState:
    """Standard non-disturbing readout of L2 into R2."""
    return CarrierState(l1=s.l1, l2=s.l2, m=s.m, r1=s.r1, r2=probe_fn(s.l2), dist=s.dist)


def disturbing_readout_1(
    s: CarrierState,
    probe_fn: Callable[[int], int] = lambda x: x,
    disturb_fn: Callable[[int], int] = lambda x: (x + 1) % 10,
    cost: int = 1,
) -> CarrierState:
    """Disturbing readout of L1 into R1 with state modification and price recording."""
    return CarrierState(
        l1=disturb_fn(s.l1),
        l2=s.l2,
        m=s.m,
        r1=probe_fn(s.l1),
        r2=s.r2,
        dist=s.dist + cost,
    )


# Projections
def proj_1(s: CarrierState) -> Tuple[int, int]:
    """Projected observation for Observer 1: (target state L1, record mark R1)."""
    return (s.l1, s.r1)


def proj_2(s: CarrierState) -> Tuple[int, int]:
    """Projected observation for Observer 2: (target state L2, record mark R2)."""
    return (s.l2, s.r2)


def marginal_2(s: CarrierState) -> int:
    """Marginal record mark at Observer 2."""
    return s.r2
