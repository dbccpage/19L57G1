"""0-cells (states), 1-cells (execution traces), and replay mechanics.

Target G013: Coherent Trace Calculus & Higher Cell Algebra.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping, Optional, Sequence, Tuple


@dataclass(frozen=True)
class State:
    """A 0-cell representing a discrete state.

    Attributes:
        state_id: Unique string identifier for the state.
        payload: Immutable key-value mapping of state fields.
    """

    state_id: str
    payload: Tuple[Tuple[str, Any], ...] = ()

    @classmethod
    def create(cls, state_id: str, data: Optional[Mapping[str, Any]] = None) -> State:
        """Create a state from a dictionary or mapping."""
        if data is None:
            return cls(state_id=state_id, payload=())
        sorted_pairs = tuple(sorted((k, v) for k, v in data.items()))
        return cls(state_id=state_id, payload=sorted_pairs)

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a field value from the payload."""
        for k, v in self.payload:
            if k == key:
                return v
        return default

    def with_update(self, new_id: str, **updates: Any) -> State:
        """Produce a new state with updated payload attributes."""
        current = dict(self.payload)
        current.update(updates)
        return State.create(new_id, current)

    def __repr__(self) -> str:
        if not self.payload:
            return f"State({self.state_id!r})"
        payload_str = ", ".join(f"{k}={v!r}" for k, v in self.payload)
        return f"State({self.state_id!r}, {payload_str})"


@dataclass(frozen=True)
class Transition:
    """An elementary transition step between two 0-cells.

    Attributes:
        source: Pre-state (source 0-cell).
        target: Post-state (target 0-cell).
        label: Name of the transition action/event.
        cost: Non-negative valuation/price associated with the step.
    """

    source: State
    target: State
    label: str
    cost: float = 0.0

    def __post_init__(self) -> None:
        if self.cost < 0.0:
            raise ValueError(f"Transition cost must be non-negative, got {self.cost}")

    def __repr__(self) -> str:
        return f"({self.source.state_id} --[{self.label}]--> {self.target.state_id})"


@dataclass(frozen=True)
class Trace:
    """A 1-cell representing an execution trace as a sequence of chained transitions.

    Attributes:
        source: Initial 0-cell.
        target: Terminal 0-cell.
        transitions: Ordered sequence of transitions forming a contiguous path.
    """

    source: State
    target: State
    transitions: Tuple[Transition, ...]

    def __post_init__(self) -> None:
        if not self.transitions:
            if self.source != self.target:
                raise ValueError(
                    f"Empty trace must have identical source and target, "
                    f"got source={self.source.state_id!r}, target={self.target.state_id!r}"
                )
            return

        # Check contiguous chain
        if self.transitions[0].source != self.source:
            raise ValueError(
                f"First transition source {self.transitions[0].source.state_id!r} "
                f"does not match trace source {self.source.state_id!r}"
            )

        for i in range(len(self.transitions) - 1):
            curr_target = self.transitions[i].target
            next_source = self.transitions[i + 1].source
            if curr_target != next_source:
                raise ValueError(
                    f"Discontinuous trace at index {i}: transition target {curr_target.state_id!r} "
                    f"!= next source {next_source.state_id!r}"
                )

        if self.transitions[-1].target != self.target:
            raise ValueError(
                f"Last transition target {self.transitions[-1].target.state_id!r} "
                f"does not match trace target {self.target.state_id!r}"
            )

    @property
    def length(self) -> int:
        """Number of transition steps in the trace."""
        return len(self.transitions)

    @property
    def is_identity(self) -> bool:
        """Whether this trace is a 0-step identity 1-cell."""
        return len(self.transitions) == 0

    @classmethod
    def id_trace(cls, state: State) -> Trace:
        """Construct the identity 1-cell id_s : s -> s."""
        return cls(source=state, target=state, transitions=())

    @classmethod
    def from_step(cls, step: Transition) -> Trace:
        """Construct a 1-step trace from an elementary transition."""
        return cls(source=step.source, target=step.target, transitions=(step,))

    @classmethod
    def from_steps(cls, steps: Sequence[Transition], source: Optional[State] = None) -> Trace:
        """Construct a trace from a contiguous sequence of transitions."""
        if not steps:
            if source is None:
                raise ValueError("Source state required when constructing an empty trace.")
            return cls.id_trace(source)
        src = steps[0].source if source is None else source
        dst = steps[-1].target
        return cls(source=src, target=dst, transitions=tuple(steps))

    def concat(self, other: Trace) -> Trace:
        """Concatenate two 1-cells: (self : s -> t) * (other : t -> u) => (s -> u)."""
        if self.target != other.source:
            raise ValueError(
                f"Cannot concatenate traces with mismatched endpoints: "
                f"left target={self.target.state_id!r}, right source={other.source.state_id!r}"
            )
        if self.is_identity:
            return other
        if other.is_identity:
            return self
        return Trace(
            source=self.source,
            target=other.target,
            transitions=self.transitions + other.transitions,
        )

    def __add__(self, other: Trace) -> Trace:
        return self.concat(other)

    def replay(self, initial: Optional[State] = None) -> list[State]:
        """Execute/replay the trace, generating the exact sequence of intermediate states."""
        if initial is not None and initial != self.source:
            raise ValueError(
                f"Replay initial state {initial.state_id!r} does not match trace source {self.source.state_id!r}"
            )
        states = [self.source]
        for step in self.transitions:
            states.append(step.target)
        return states

    def intermediate_states(self) -> list[State]:
        """Return the list of all visited states [s_0, s_1, ..., s_k]."""
        return self.replay()

    def labels(self) -> list[str]:
        """Return sequence of transition labels."""
        return [t.label for t in self.transitions]

    def slice_trace(self, start: int, end: int) -> Trace:
        """Extract a sub-trace between step indices [start, end)."""
        if start < 0 or end > len(self.transitions) or start > end:
            raise IndexError(f"Invalid trace slice indices: start={start}, end={end}, len={len(self.transitions)}")
        sub_transitions = self.transitions[start:end]
        if not sub_transitions:
            state = self.transitions[start].source if start < len(self.transitions) else self.target
            return Trace.id_trace(state)
        return Trace.from_steps(sub_transitions)

    def __repr__(self) -> str:
        if self.is_identity:
            return f"Trace(id_{self.source.state_id})"
        step_labels = " -> ".join(t.label for t in self.transitions)
        return f"Trace({self.source.state_id} =[{step_labels}]=> {self.target.state_id})"
