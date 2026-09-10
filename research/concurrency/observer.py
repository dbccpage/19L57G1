"""W06 Observer record exchange simulation and formalization mirror.

Models two observers receiving projected observations of a shared multi-locus
carrier (L1 x L2 x M):
1. Projections: π1(s) = (s.l1, s.m), π2(s) = (s.l2, s.m)
2. Symmetry and initial agreement: when s.l1 == s.l2, π1(s) == π2(s)
3. Represented message transmission through M
4. Decision divergence driven by the transmitted message
5. Negative control: non-transmitted state updates isolate information flow

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Tuple

from carrier import State3, proj1, proj2


def is_symmetric(s: State3) -> bool:
    """A carrier state is symmetric iff both observers' local coordinates are identical."""
    return s.l1 == s.l2


@dataclass
class Observer:
    """An observer with a projected view and local decision policy."""

    name: str
    projection: Callable[[State3], Tuple[int, int]]
    decision_policy: Callable[[Tuple[int, int]], Any]

    def observe(self, s: State3) -> Tuple[int, int]:
        """Obtain projected observation of the carrier."""
        return self.projection(s)

    def decide(self, s: State3) -> Any:
        """Make a local decision based strictly on the projected observation."""
        return self.decision_policy(self.observe(s))


def transmit_l1(s: State3) -> State3:
    """Observer 1 transmits its local coordinate to message buffer M."""
    return State3(l1=s.l1, l2=s.l2, m=s.l1)


def transmit_val(v: int, s: State3) -> State3:
    """Observer 1 transmits an arbitrary represented value to M."""
    return State3(l1=s.l1, l2=s.l2, m=v)


def receive_m(s: State3) -> State3:
    """Observer 2 receives the message from M and stores it in L2."""
    return State3(l1=s.l1, l2=s.m, m=s.m)


def exchange_round(s: State3) -> State3:
    """Complete message exchange round: O1 transmits to M, O2 receives into L2."""
    return receive_m(transmit_l1(s))


def local_step_l1(f: Callable[[int], int], s: State3) -> State3:
    """Uncoupled local step by Observer 1 (modifies L1 without touching M)."""
    return State3(l1=f(s.l1), l2=s.l2, m=s.m)


def run_symmetric_agreement_experiment(
    symmetric_states: list[State3],
    decision_policy: Callable[[Tuple[int, int]], Any],
) -> dict[str, Any]:
    """Verify that identical decision policies on symmetric states yield 100% agreement."""
    o1 = Observer("O1", proj1, decision_policy)
    o2 = Observer("O2", proj2, decision_policy)

    total = len(symmetric_states)
    agreements = 0
    for s in symmetric_states:
        if not is_symmetric(s):
            continue
        d1 = o1.decide(s)
        d2 = o2.decide(s)
        if d1 == d2:
            agreements += 1

    return {
        "total_symmetric_states": total,
        "agreements": agreements,
        "agreement_rate": agreements / total if total > 0 else 1.0,
        "perfect_agreement": agreements == total,
    }


def run_decision_divergence_experiment(
    s0: State3, s1: State3
) -> dict[str, Any]:
    """Demonstrate decision divergence between two runs differing only in O1's initial state."""
    # Pre-condition check: O2 initial states and message buffers must be identical
    if s0.l2 != s1.l2 or s0.m != s1.m:
        raise ValueError("s0 and s1 must share identical l2 and m initial coordinates.")
    if s0.l1 == s1.l1:
        raise ValueError("s0 and s1 must have distinct l1 coordinates.")

    final0 = exchange_round(s0)
    final1 = exchange_round(s1)

    diverged = final0.l2 != final1.l2

    return {
        "initial_s0": s0.to_tuple(),
        "initial_s1": s1.to_tuple(),
        "final_s0": final0.to_tuple(),
        "final_s1": final1.to_tuple(),
        "o2_initial_agreed": s0.l2 == s1.l2,
        "o2_final_diverged": diverged,
        "o2_final_values": (final0.l2, final1.l2),
    }


def run_negative_control_experiment(
    s0: State3, s1: State3, local_f: Callable[[int], int]
) -> dict[str, Any]:
    """Verify that uncoupled local steps by O1 cannot cause O2's state to diverge."""
    if s0.l2 != s1.l2 or s0.m != s1.m:
        raise ValueError("s0 and s1 must share identical l2 and m initial coordinates.")

    # O1 takes local step without writing to M
    step0 = receive_m(local_step_l1(local_f, s0))
    step1 = receive_m(local_step_l1(local_f, s1))

    isolated = step0.l2 == step1.l2

    return {
        "initial_s0": s0.to_tuple(),
        "initial_s1": s1.to_tuple(),
        "step_s0": step0.to_tuple(),
        "step_s1": step1.to_tuple(),
        "o2_remained_identical": isolated,
    }
