"""Data-dependent control and execution driven by encoded graph instances.

AuthorityEffect: None.
Configuration status: DECLARED_HOST_CONFIG.

This module implements data-driven control where operation enablement is
represented directly as graph data. Operation `k` is enabled at datum `x` by
adding one binary form per operation and asserting the reflexive self-instance:
    (3 + nops + k, (x, x))

Key properties:
- Determinism enforced, not assumed: if two or more operations are enabled,
  the interpreter explicitly refuses to select, halting with Terminal.BRANCH.
- Strict resource ledger: fuel is spent monotonically (-1) on each step;
  clock measures exact operation applications (+1).
- Non-deterministic successor family: `successors` exposes all possible branch
  transitions for relational analysis without arbitrarily choosing one.
- Terminals strictly distinct: HALT, EXHAUSTED, REFUSE, BRANCH.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from runner import (
    ExecutionError,
    Graph,
    Refusal,
    Terminal,
    check_word,
    lookup,
    run_det_of,
    step_det_of,
)

Enablement = frozenset[tuple[int, int]]


@dataclass(frozen=True)
class State:
    """The interpreter state carrying program graph, operation count, active datum,
    tape of visited data, operation clock, fuel, and represented protection obligations
    and designated pair constraints (Spec 1504).
    """

    graph: Graph
    nops: int
    active: int
    tape: tuple[int, ...]
    clock: int
    fuel: int
    protection_obligations: tuple[int, ...] = ()
    designated_pair: tuple[int, int] | None = None

    def __post_init__(self) -> None:
        if self.nops < 0:
            raise ExecutionError("nops must be non-negative")
        if self.active < 0:
            raise ExecutionError("active datum must be non-negative")
        if self.clock < 0:
            raise ExecutionError("clock must be non-negative")


@dataclass(frozen=True)
class Controlled:
    """A finite setting with carrier size n, operation mappings, and an enablement relation."""

    n: int
    ops: tuple[tuple[int, ...], ...]
    ctrl: Enablement

    def __post_init__(self) -> None:
        count = len(self.ops)
        for k, op in enumerate(self.ops):
            if len(op) != self.n:
                raise ExecutionError(f"op {k} length {len(op)} does not match carrier {self.n}")
            for x, y in enumerate(op):
                if not (0 <= y < self.n):
                    raise ExecutionError(f"op {k}({x}) = {y} lies outside carrier {self.n}")
        for x, k in self.ctrl:
            if not (0 <= x < self.n and 0 <= k < count):
                raise ExecutionError(f"enablement ({x}, {k}) lies outside setting bounds")


def nops(C: Controlled) -> int:
    """The number of operations in the setting."""
    return len(C.ops)


def ctrl_form(count: int, k: int) -> int:
    """The form index assigned to the control enablement of operation k."""
    return 3 + count + k


def build_program(
    n: int,
    ops: Sequence[Sequence[int]],
    ctrl: Sequence[tuple[int, int]],
) -> Graph:
    """Build the program graph containing operation edges and control self-instances.

    - Op edges: (3 + k, (x, ops[k][x]))
    - Control edges: (3 + nops + k, (x, x))
    """
    count = len(ops)
    edges: set[tuple[int, tuple[int, ...]]] = set()
    for k, op in enumerate(ops):
        for x in range(n):
            edges.add((3 + k, (x, op[x])))
    for x, k in ctrl:
        edges.add((ctrl_form(count, k), (x, x)))
    return frozenset(edges)


def encode_c(C: Controlled) -> Graph:
    """Produce the program graph from a Controlled setting."""
    return build_program(C.n, C.ops, tuple(C.ctrl))


def enabled(g: Graph, count: int, x: int, k: int) -> bool:
    """Check if operation k is enabled at datum x via its self-instance."""
    f = ctrl_form(count, k)
    return (f, (x, x)) in g


def enabled_at(g: Graph, count: int, x: int) -> tuple[int, ...]:
    """Return all operation indices enabled at datum x, in index order.

    The list order is purely nominal; the interpreter never selects by list order.
    """
    return tuple(k for k in range(count) if enabled(g, count, x, k))


def fire(s: State, k: int) -> State | Refusal:
    """Fire operation k at the active datum.

    - With fuel > 0, reads edge 3 + k from active datum.
    - If edge is missing: returns Refusal.NO_EDGE.
    - If fuel <= 0: returns Refusal.EXHAUSTED.
    - Otherwise: moves to target y, appends y to tape, increments clock, decrements fuel.
    """
    check_word((k,))
    if s.fuel <= 0:
        return Refusal.EXHAUSTED
    y = lookup(3 + k, s.active, s.graph)
    if y is None:
        return Refusal.NO_EDGE
    return State(
        graph=s.graph,
        nops=s.nops,
        active=y,
        tape=s.tape + (y,),
        clock=s.clock + 1,
        fuel=s.fuel - 1,
        protection_obligations=s.protection_obligations,
        designated_pair=s.designated_pair,
    )


def successors(s: State) -> tuple[State, ...]:
    """The family of all valid successor states from s."""
    out: list[State] = []
    for k in enabled_at(s.graph, s.nops, s.active):
        res = fire(s, k)
        if isinstance(res, State):
            out.append(res)
    return tuple(out)


def ctrl_reader(s: State) -> tuple[int, ...]:
    """Reader function extracting operations enabled at the active datum."""
    return enabled_at(s.graph, s.nops, s.active)


def step_det(s: State) -> Terminal | State:
    """One deterministic step of the control machine.

    Refusal to select on non-deterministic forks:
    - 0 enabled -> Terminal.HALT
    - >= 2 enabled -> Terminal.BRANCH
    - 1 enabled -> fire operation
    """
    return step_det_of(ctrl_reader, s, fire)


def run_det(bound: int, s: State) -> tuple[Terminal, State]:
    """Run step_det bounded by fuel/step limit."""
    return run_det_of(ctrl_reader, bound, s, fire)


def run(s: State) -> tuple[Terminal, State]:
    """Run state to completion or refusal, bounded by its own fuel."""
    return run_det(s.fuel, s)


def init(
    C: Controlled,
    x: int,
    fuel: int,
    protection_obligations: tuple[int, ...] = (),
    designated_pair: tuple[int, int] | None = None,
) -> State:
    """Initialize state from a Controlled setting with given start datum and fuel."""
    if not (0 <= x < C.n):
        raise ExecutionError(f"start datum {x} lies outside carrier {C.n}")
    if fuel < 0:
        raise ExecutionError("fuel must be non-negative")
    return State(
        graph=encode_c(C),
        nops=nops(C),
        active=x,
        tape=(x,),
        clock=0,
        fuel=fuel,
        protection_obligations=protection_obligations,
        designated_pair=designated_pair,
    )


def trace(C: Controlled, x: int, fuel: int) -> tuple[Terminal, State]:
    """Run an initial state to completion."""
    return run(init(C, x, fuel))
