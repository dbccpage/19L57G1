"""Higher 2-cells representing replay equivalences between computational routes.

Formalizes 2-cells between parallel 1-cells, horizontal and vertical composition,
and the Middle Four Interchange Law.

Target G013: Coherent Trace Calculus & Higher Cell Algebra.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional, Sequence, Tuple

from trace import State, Trace, Transition


class Cell2Kind(str, Enum):
    """Classification of 2-cell generators and composite derivations."""

    IDENTITY = "IDENTITY"
    INDEPENDENT_COMMUTE = "INDEPENDENT_COMMUTE"
    ID_CANCEL_LEFT = "ID_CANCEL_LEFT"
    ID_CANCEL_RIGHT = "ID_CANCEL_RIGHT"
    INVERSE_CANCEL = "INVERSE_CANCEL"
    VERTICAL_COMPOSITION = "VERTICAL_COMPOSITION"
    HORIZONTAL_COMPOSITION = "HORIZONTAL_COMPOSITION"
    SYMMETRY = "SYMMETRY"


@dataclass(frozen=True)
class Cell2:
    """A 2-cell alpha : p => q between parallel 1-cells p, q with identical 0-cell endpoints.

    Attributes:
        source_trace: 1-cell source path p : s -> t.
        target_trace: 1-cell target path q : s -> t.
        kind: Classification of this 2-cell.
        description: Natural-language justification or derivation record.
        children: Subordinate 2-cells for composite constructions.
    """

    source_trace: Trace
    target_trace: Trace
    kind: Cell2Kind
    description: str = ""
    children: Tuple[Cell2, ...] = ()

    def __post_init__(self) -> None:
        # Strict endpoint matching between parallel 1-cells
        if self.source_trace.source != self.target_trace.source:
            raise ValueError(
                f"2-cell source and target traces must have identical initial 0-cells: "
                f"{self.source_trace.source.state_id!r} != {self.target_trace.source.state_id!r}"
            )
        if self.source_trace.target != self.target_trace.target:
            raise ValueError(
                f"2-cell source and target traces must have identical terminal 0-cells: "
                f"{self.source_trace.target.state_id!r} != {self.target_trace.target.state_id!r}"
            )

    @property
    def source_0cell(self) -> State:
        """Initial 0-cell of the bounded 1-cells."""
        return self.source_trace.source

    @property
    def target_0cell(self) -> State:
        """Terminal 0-cell of the bounded 1-cells."""
        return self.source_trace.target

    @classmethod
    def id_cell(cls, trace: Trace) -> Cell2:
        """Construct the identity 2-cell id_p : p => p."""
        return cls(
            source_trace=trace,
            target_trace=trace,
            kind=Cell2Kind.IDENTITY,
            description=f"Identity 2-cell on trace {trace}",
        )

    @classmethod
    def commute(
        cls,
        step_a: Transition,
        step_b: Transition,
        step_b_prime: Transition,
        step_a_prime: Transition,
        justification: str = "Independent transition commutation",
    ) -> Cell2:
        """Construct an elementary commutation 2-cell for a diamond:
        s0 --[a]--> s1 --[b]--> s_dst  vs  s0 --[b']--> s2 --[a']--> s_dst
        """
        trace_ab = Trace.from_steps([step_a, step_b])
        trace_ba = Trace.from_steps([step_b_prime, step_a_prime])
        if trace_ab.source != trace_ba.source or trace_ab.target != trace_ba.target:
            raise ValueError("Commuting transitions must form a closed diamond with identical endpoints.")
        return cls(
            source_trace=trace_ab,
            target_trace=trace_ba,
            kind=Cell2Kind.INDEPENDENT_COMMUTE,
            description=justification,
        )

    @classmethod
    def cancel_id_left(cls, trace: Trace) -> Cell2:
        """Construct 2-cell id_s * trace => trace."""
        id_tr = Trace.id_trace(trace.source)
        lhs = id_tr.concat(trace)
        return cls(
            source_trace=lhs,
            target_trace=trace,
            kind=Cell2Kind.ID_CANCEL_LEFT,
            description="Left identity cancellation",
        )

    @classmethod
    def cancel_id_right(cls, trace: Trace) -> Cell2:
        """Construct 2-cell trace * id_t => trace."""
        id_tr = Trace.id_trace(trace.target)
        lhs = trace.concat(id_tr)
        return cls(
            source_trace=lhs,
            target_trace=trace,
            kind=Cell2Kind.ID_CANCEL_RIGHT,
            description="Right identity cancellation",
        )

    def symm(self) -> Cell2:
        """Invert the 2-cell direction: (p => q) becomes (q => p)."""
        return Cell2(
            source_trace=self.target_trace,
            target_trace=self.source_trace,
            kind=Cell2Kind.SYMMETRY,
            description=f"Symmetry of ({self.description})",
            children=(self,),
        )

    def __repr__(self) -> str:
        return (
            f"Cell2({self.kind.value}: "
            f"[{self.source_trace}] => [{self.target_trace}])"
        )


def v_compose(alpha: Cell2, beta: Cell2) -> Cell2:
    """Vertical composition of 2-cells (circ_1):
    alpha : p => q
    beta  : q => r
    result: (beta circ_1 alpha) : p => r
    """
    if alpha.target_trace != beta.source_trace:
        raise ValueError(
            f"Cannot vertically compose 2-cells with non-matching intermediate 1-cells: "
            f"alpha target={alpha.target_trace} != beta source={beta.source_trace}"
        )
    return Cell2(
        source_trace=alpha.source_trace,
        target_trace=beta.target_trace,
        kind=Cell2Kind.VERTICAL_COMPOSITION,
        description=f"({beta.description}) o_1 ({alpha.description})",
        children=(alpha, beta),
    )


def h_compose(alpha: Cell2, beta: Cell2) -> Cell2:
    """Horizontal composition of 2-cells (circ_0 / star):
    alpha : p1 => q1  (p1, q1 : s -> t)
    beta  : p2 => q2  (p2, q2 : t -> u)
    result: (alpha circ_0 beta) : (p1 * p2) => (q1 * q2)
    """
    if alpha.target_0cell != beta.source_0cell:
        raise ValueError(
            f"Cannot horizontally compose 2-cells with non-matching boundary 0-cells: "
            f"alpha target 0-cell={alpha.target_0cell.state_id!r} != "
            f"beta source 0-cell={beta.source_0cell.state_id!r}"
        )
    src_composite = alpha.source_trace.concat(beta.source_trace)
    tgt_composite = alpha.target_trace.concat(beta.target_trace)
    return Cell2(
        source_trace=src_composite,
        target_trace=tgt_composite,
        kind=Cell2Kind.HORIZONTAL_COMPOSITION,
        description=f"({alpha.description}) o_0 ({beta.description})",
        children=(alpha, beta),
    )


def verify_interchange_law(
    alpha1: Cell2,
    alpha2: Cell2,
    beta1: Cell2,
    beta2: Cell2,
) -> Tuple[bool, Cell2, Cell2]:
    """Evaluate and verify the Middle Four Interchange Law:
    For alpha1 : p1 => q1, alpha2 : q1 => r1 (between s and t)
        beta1  : p2 => q2, beta2  : q2 => r2 (between t and u)

    Compute:
      left_composite  = h_compose(v_compose(alpha1, alpha2), v_compose(beta1, beta2))
      right_composite = v_compose(h_compose(alpha1, beta1), h_compose(alpha2, beta2))

    Returns:
      (is_coherent, left_composite, right_composite)
    """
    # Left composition: first vertical, then horizontal
    v_alpha = v_compose(alpha1, alpha2)  # p1 => r1
    v_beta = v_compose(beta1, beta2)    # p2 => r2
    left_composite = h_compose(v_alpha, v_beta)  # p1 * p2 => r1 * r2

    # Right composition: first horizontal, then vertical
    h_top = h_compose(alpha1, beta1)    # p1 * p2 => q1 * q2
    h_bot = h_compose(alpha2, beta2)    # q1 * q2 => r1 * r2
    right_composite = v_compose(h_top, h_bot)  # p1 * p2 => r1 * r2

    # Both must coincide in their 1-cell boundaries:
    coherent = (
        left_composite.source_trace == right_composite.source_trace
        and left_composite.target_trace == right_composite.target_trace
    )
    return coherent, left_composite, right_composite


class ReplayEquivalence:
    """Witnesses and checks replay equivalence across computational routes."""

    @staticmethod
    def are_endpoints_equal(p: Trace, q: Trace) -> bool:
        """Check whether two traces share identical 0-cell endpoints."""
        return p.source == q.source and p.target == q.target

    @staticmethod
    def can_commute_adjacent(
        trace: Trace,
        index: int,
        commute_predicate: Any,
    ) -> Optional[Trace]:
        """Attempt to rewrite a trace by commuting adjacent steps at index and index+1."""
        if index < 0 or index >= trace.length - 1:
            return None
        s1 = trace.transitions[index]
        s2 = trace.transitions[index + 1]
        pair = commute_predicate(s1, s2)
        if pair is None:
            return None
        s1_new, s2_new = pair
        new_transitions = (
            trace.transitions[:index]
            + (s1_new, s2_new)
            + trace.transitions[index + 2 :]
        )
        return Trace.from_steps(new_transitions, source=trace.source)

    @staticmethod
    def verify_confluence(divergent_traces: Sequence[Trace]) -> bool:
        """Verify confluence: all traces in the sequence share identical endpoints."""
        if not divergent_traces:
            return True
        ref = divergent_traces[0]
        return all(t.source == ref.source and t.target == ref.target for t in divergent_traces)
