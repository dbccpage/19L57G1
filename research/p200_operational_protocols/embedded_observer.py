"""Duplicate embedded observers related by presentation symmetries.

Models:
1. Observers embedded within the carrier substrate at distinct loci.
2. Presentation symmetries:
   - Swap involution exchanging target and record registers (L1 <-> L2, R1 <-> R2).
   - Coordinate renamings and translations.
3. Covariance / equivariance:
   Readout operations commute with presentation symmetries:
       Readout_2(swap(s)) = swap(Readout_1(s))
4. Inter-observer agreement:
   On symmetric preparations (s.l1 == s.l2), duplicate observers record identical
   marks when executing identical local readout protocols.

AuthorityEffect: None.
Axiom Scope: Constructive finite carrier operations without external host oracles.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Tuple

from protocol import (
    CarrierState,
    Locus,
    coincidence_evaluator,
    record_distance,
)


@dataclass(frozen=True)
class EmbeddedObserver:
    """An observer embedded within the carrier at a specific locus."""

    observer_id: str
    target_locus: Locus
    record_locus: Locus
    probe_fn: Callable[[int], int] = lambda x: x

    def readout(self, s: CarrierState) -> CarrierState:
        """Execute local readout into the embedded record register."""
        val = getattr(s, self.target_locus.name.lower())
        mark = self.probe_fn(val)
        if self.record_locus == Locus.R1:
            return CarrierState(l1=s.l1, l2=s.l2, m=s.m, r1=mark, r2=s.r2, dist=s.dist)
        elif self.record_locus == Locus.R2:
            return CarrierState(l1=s.l1, l2=s.l2, m=s.m, r1=s.r1, r2=mark, dist=s.dist)
        else:
            raise ValueError(f"Invalid record locus: {self.record_locus}")

        target_val = int(getattr(s, self.target_locus.name.lower()))
        record_val = int(getattr(s, self.record_locus.name.lower()))
        return (target_val, record_val)

    def get_record(self, s: CarrierState) -> int:
        """Retrieve recorded mark from embedded memory."""
        return int(getattr(s, self.record_locus.name.lower()))


# -------------------------------------------------------------------------
# Presentation Symmetries
# -------------------------------------------------------------------------

def swap_symmetry(s: CarrierState) -> CarrierState:
    """Swap involution exchanging Observer 1 (L1, R1) and Observer 2 (L2, R2)."""
    return CarrierState(
        l1=s.l2,
        l2=s.l1,
        m=s.m,
        r1=s.r2,
        r2=s.r1,
        dist=s.dist,
    )


def translate_symmetry(s: CarrierState, shift: int, modulus: int) -> CarrierState:
    """Uniform cyclic coordinate translation across both observer loci."""
    return CarrierState(
        l1=(s.l1 + shift) % modulus,
        l2=(s.l2 + shift) % modulus,
        m=s.m,
        r1=s.r1,
        r2=s.r2,
        dist=s.dist,
    )


def is_symmetric_state(s: CarrierState) -> bool:
    """Check whether carrier state is invariant under observer swap."""
    return s.l1 == s.l2 and s.r1 == s.r2


# -------------------------------------------------------------------------
# Duplicate Observers Creation and Execution
# -------------------------------------------------------------------------

def create_duplicate_observers(
    probe_fn: Callable[[int], int] = lambda x: x
) -> Tuple[EmbeddedObserver, EmbeddedObserver]:
    """Instantiate duplicate observers related by locus swap symmetry."""
    obs1 = EmbeddedObserver("observer_1", Locus.L1, Locus.R1, probe_fn)
    obs2 = EmbeddedObserver("observer_2", Locus.L2, Locus.R2, probe_fn)
    return (obs1, obs2)


def run_joint_protocol(
    obs1: EmbeddedObserver, obs2: EmbeddedObserver, s: CarrierState
) -> CarrierState:
    """Execute joint readout protocol where both observers record their target loci."""
    s1 = obs1.readout(s)
    s2 = obs2.readout(s1)
    return s2


def check_inter_observer_agreement(
    obs1: EmbeddedObserver, obs2: EmbeddedObserver, s: CarrierState
) -> bool:
    """Check whether joint readout yields matching record marks."""
    final_state = run_joint_protocol(obs1, obs2, s)
    return coincidence_evaluator(final_state)


def check_equivariance(
    obs1: EmbeddedObserver, obs2: EmbeddedObserver, s: CarrierState
) -> bool:
    """Verify equivariance under swap symmetry:

    obs2.readout(swap(s)) == swap(obs1.readout(s))
    """
    left = obs2.readout(swap_symmetry(s))
    right = swap_symmetry(obs1.readout(s))
    return left == right
