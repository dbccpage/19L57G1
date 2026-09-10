"""Observer trace congruence and residual-free quotient dynamics.

Formalizes observer projections and observer trace congruence:
  States indistinguishable under all admitted observation projections preserve
  identical future continuation distributions without unrecorded residuals.

Target G013: Coherent Trace Calculus & Higher Cell Algebra.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, FrozenSet, List, Mapping, Optional, Sequence, Set, Tuple

from trace import State, Trace, Transition


@dataclass(frozen=True)
class ObservationProjection:
    """An observation projection mapping concrete states and transitions to observed data.

    Attributes:
        name: Name or tag of this observation channel.
        project_state: Function mapping a State to an observable observation datum.
        project_label: Function mapping a transition label to an observable action.
    """

    name: str
    project_state: Callable[[State], Any]
    project_label: Callable[[str], str] = lambda lbl: lbl

    def observe_state(self, state: State) -> Any:
        return self.project_state(state)

    def observe_transition(self, trans: Transition) -> Tuple[Any, str, Any]:
        return (
            self.project_state(trans.source),
            self.project_label(trans.label),
            self.project_state(trans.target),
        )

    def observe_trace(self, trace: Trace) -> Tuple[Any, ...]:
        """Produce the sequence of observations along the trace: (obs(s0), lbl1, obs(s1), ...)."""
        if trace.is_identity:
            return (self.project_state(trace.source),)
        seq: List[Any] = [self.project_state(trace.source)]
        for t in trace.transitions:
            seq.append(self.project_label(t.label))
            seq.append(self.project_state(t.target))
        return tuple(seq)


@dataclass
class TransitionSystem:
    """A discrete transition system with states and labeled step relations."""

    states: Dict[str, State]
    transitions: List[Transition]

    def __post_init__(self) -> None:
        self._out_edges: Dict[State, List[Transition]] = {s: [] for s in self.states.values()}
        for t in self.transitions:
            if t.source in self._out_edges:
                self._out_edges[t.source].append(t)

    def outgoing(self, state: State) -> List[Transition]:
        return self._out_edges.get(state, [])

    def step(self, state: State, label: str) -> Optional[State]:
        """Deterministic step for a given label."""
        for t in self.outgoing(state):
            if t.label == label:
                return t.target
        return None

    def execute_sequence(self, initial: State, labels: Sequence[str]) -> Optional[Trace]:
        """Execute a sequence of labels from an initial state."""
        current = initial
        steps: List[Transition] = []
        for lbl in labels:
            matched = None
            for t in self.outgoing(current):
                if t.label == lbl:
                    matched = t
                    break
            if matched is None:
                return None
            steps.append(matched)
            current = matched.target
        return Trace.from_steps(steps, source=initial)


@dataclass(frozen=True)
class CongruenceClass:
    """An equivalence class of observationally congruent states."""

    class_id: str
    observation: Any
    members: Tuple[State, ...]


@dataclass(frozen=True)
class ResidualAudit:
    """Receipt documenting whether any unrecorded residuals were detected."""

    is_congruent: bool
    num_classes: int
    unrecorded_residuals_detected: bool
    discrepancies: Tuple[str, ...] = ()


def check_observer_trace_congruence(
    s1: State,
    s2: State,
    system: TransitionSystem,
    projection: ObservationProjection,
    max_depth: int = 4,
) -> Tuple[bool, Optional[str]]:
    """Check whether states s1 and s2 are observationally congruent up to max_depth.
    Returns (is_congruent, failure_reason_if_any).
    """
    obs1 = projection.observe_state(s1)
    obs2 = projection.observe_state(s2)
    if obs1 != obs2:
        return False, f"Immediate observation mismatch: {obs1!r} != {obs2!r}"

    # BFS exploration of continuation paths
    queue: List[Tuple[State, State, List[str]]] = [(s1, s2, [])]
    visited: Set[Tuple[str, str, int]] = set()

    while queue:
        curr1, curr2, path = queue.pop(0)
        depth = len(path)
        if depth >= max_depth:
            continue

        pair_key = (curr1.state_id, curr2.state_id, depth)
        if pair_key in visited:
            continue
        visited.add(pair_key)

        out1 = {t.label: t.target for t in system.outgoing(curr1)}
        out2 = {t.label: t.target for t in system.outgoing(curr2)}

        # Observable action sets must match
        actions1 = set(out1.keys())
        actions2 = set(out2.keys())
        if actions1 != actions2:
            return False, f"Available actions differ at path {path}: {actions1} != {actions2}"

        for act in actions1:
            next1 = out1[act]
            next2 = out2[act]
            n_obs1 = projection.observe_state(next1)
            n_obs2 = projection.observe_state(next2)
            if n_obs1 != n_obs2:
                return False, (
                    f"Observation discrepancy after action {act!r} along path {path}: "
                    f"{n_obs1!r} != {n_obs2!r}"
                )
            queue.append((next1, next2, path + [act]))

    return True, None


def compute_congruence_partition(
    system: TransitionSystem,
    projection: ObservationProjection,
    max_depth: int = 4,
) -> List[CongruenceClass]:
    """Partition the state space into observer trace congruence classes."""
    states = list(system.states.values())
    partition: List[List[State]] = []

    for s in states:
        placed = False
        for group in partition:
            rep = group[0]
            congruent, _ = check_observer_trace_congruence(s, rep, system, projection, max_depth)
            if congruent:
                group.append(s)
                placed = True
                break
        if not placed:
            partition.append([s])

    classes: List[CongruenceClass] = []
    for idx, group in enumerate(partition):
        obs = projection.observe_state(group[0])
        classes.append(
            CongruenceClass(
                class_id=f"C{idx}",
                observation=obs,
                members=tuple(sorted(group, key=lambda s: s.state_id)),
            )
        )
    return classes


def audit_observer_residuals(
    system: TransitionSystem,
    projection: ObservationProjection,
    max_depth: int = 4,
) -> ResidualAudit:
    """Verify that states within each congruence class have identical future continuation
    observations without unrecorded residuals.
    """
    classes = compute_congruence_partition(system, projection, max_depth)
    discrepancies: List[str] = []

    for cls in classes:
        members = cls.members
        if len(members) <= 1:
            continue
        rep = members[0]
        for m in members[1:]:
            congruent, err = check_observer_trace_congruence(rep, m, system, projection, max_depth)
            if not congruent:
                discrepancies.append(f"Class {cls.class_id} member {m.state_id} diverged from {rep.state_id}: {err}")

    residuals_detected = len(discrepancies) > 0
    return ResidualAudit(
        is_congruent=not residuals_detected,
        num_classes=len(classes),
        unrecorded_residuals_detected=residuals_detected,
        discrepancies=tuple(discrepancies),
    )
