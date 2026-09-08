"""Data-dependent control: the represented program drives the process.

AuthorityEffect: None.  Configuration status: DECLARED_HOST_CONFIG — a
``State`` is a metatheory record carrying encoded instances.

Mirrors ``lean/Control.lean``.  A controlled setting adds an enablement
relation ``(x, k)``: operation ``k`` may fire at datum ``x``.  It is
represented in the same device the merged encoder uses for stores and
operations — one more binary form per operation whose *self-instance*
``(3 + nops + k, (x, x))`` says ``k`` is enabled at ``x`` — so the program
is a regime of the sealed grammar (``encode_c``, the sealed replay of
``events_c``).  The machine loads the program only: the operation graphs and
the enablements (``program``), never the stores.

The interpreter is fixed while the program varies: ``enabled_at`` reads the
enablements at the active datum, ``fire`` reads the chosen operation's edge
and moves, ticking the clock and spending one fuel.  ``successors`` is the
whole family, one state per enabled operation; ``run`` fires the one enabled
operation and stops with ``BRANCH`` when two are — it never selects.  The
terminals are kept apart.  Nothing here names an operation table: the
operation count is the shape of the encoding, and every edge is read from
instances through the commit-1 ``lookup``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Sequence

import translation as tr
from derivation.model import AdmitForm, AdmitInst, Event, Regime, replay
from execution import ExecutionError, Graph, lookup

Enablement = frozenset[tuple[int, int]]


# ---------------------------------------------------------------------------
# Controlled settings, the represented program, the reference step
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Controlled:
    """A finite setting with an enablement relation ``(x, k)``."""

    F: tr.FiniteSetting
    ctrl: Enablement

    def __post_init__(self) -> None:
        count = nops(self)
        for x, k in self.ctrl:
            if not (0 <= x < self.F.n and 0 <= k < count):
                raise ExecutionError(f"enablement ({x}, {k}) lies outside the setting")


def nops(C: Controlled) -> int:
    """The operation count, read as the shape of the merged encoding: its
    forms beyond the three stores."""
    return len(tr.encode(C.F).forms) - 3


def ctrl_form(C: Controlled, k: int) -> int:
    return 3 + nops(C) + k


def cstep(C: Controlled, x: int, k: int, y: int) -> bool:
    """The reference step, stated on the setting before any encoding: ``k``
    is enabled at ``x`` and ``y`` is its value there.  A *check* the tests
    use; the machine never calls it."""
    return k < nops(C) and (x, k) in C.ctrl and y == tr.run(C.F, (k,), x)


def events_c(C: Controlled) -> tuple[Event, ...]:
    """The admission history of the controlled regime: the merged encoder's
    events, one more binary form per operation, and the enablements as
    self-instances on those forms."""
    out: list[Event] = list(tr.events(C.F))
    out.extend(AdmitForm(2) for _ in range(nops(C)))
    out.extend(AdmitInst(ctrl_form(C, k), (x, x)) for x, k in sorted(C.ctrl))
    return tuple(out)


def encode_c(C: Controlled) -> Regime:
    """The Lean ``encodeC``, as the sealed replay of ``events_c``."""
    return replay(events_c(C))


def program(C: Controlled) -> Graph:
    """The Lean ``program``: the operation graphs and the enablements — the
    instances of the controlled regime on the forms beyond the stores.  The
    stores are not loaded."""
    return frozenset(i for i in encode_c(C).insts if i[0] >= 3)


# ---------------------------------------------------------------------------
# The state and the interpreter
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class State:
    """The Lean ``State``: the program, the operation count that locates the
    control forms, the active datum, the tape of data visited, the semantic
    clock, the represented fuel."""

    graph: Graph
    nops: int
    active: int
    tape: tuple[int, ...]
    clock: int
    fuel: int


class Refusal(Enum):
    EXHAUSTED = "exhausted"
    NO_EDGE = "noEdge"


class Terminal(Enum):
    HALT = "halt"
    EXHAUSTED = "exhausted"
    REFUSE = "refuse"
    BRANCH = "branch"


def enabled(g: Graph, count: int, x: int, k: int) -> bool:
    """Operation ``k`` is enabled at ``x`` when the self-instance of its
    control form is present: the edge of that form leaving ``x`` returns ``x``."""
    y = lookup(3 + count + k, x, g)
    return y is not None and y == x


def enabled_at(g: Graph, count: int, x: int) -> tuple[int, ...]:
    """The enabled operations at ``x``, in index order.  Nothing reads its
    first element as a choice."""
    return tuple(k for k in range(count) if enabled(g, count, x, k))


def fire(s: State, k: int) -> State | Refusal:
    """Fire operation ``k`` at the active datum: with fuel left, read its
    edge, move, extend the tape, tick the clock, spend one fuel."""
    if s.fuel == 0:
        return Refusal.EXHAUSTED
    y = lookup(3 + k, s.active, s.graph)
    if y is None:
        return Refusal.NO_EDGE
    return State(s.graph, s.nops, y, s.tape + (y,), s.clock + 1, s.fuel - 1)


def successors(s: State) -> tuple[State, ...]:
    """The successor family: one state per enabled operation that fires."""
    out: list[State] = []
    for k in enabled_at(s.graph, s.nops, s.active):
        fired = fire(s, k)
        if isinstance(fired, State):
            out.append(fired)
    return tuple(out)


def step_det(s: State) -> Terminal | State:
    """The Lean ``stepDet``: a terminal, or the next state.  Halt when no
    operation is enabled; ``BRANCH`` when two are; otherwise fire the one."""
    en = enabled_at(s.graph, s.nops, s.active)
    if not en:
        return Terminal.HALT
    if len(en) >= 2:
        return Terminal.BRANCH
    fired = fire(s, en[0])
    if fired is Refusal.EXHAUSTED:
        return Terminal.EXHAUSTED
    if fired is Refusal.NO_EDGE:
        return Terminal.REFUSE
    assert isinstance(fired, State)
    return fired


def run_det(bound: int, s: State) -> tuple[Terminal, State]:
    """The Lean ``runDet``, bounded by a copy of the fuel."""
    while True:
        nxt = step_det(s)
        if isinstance(nxt, Terminal):
            return (nxt, s)
        if bound == 0:
            return (Terminal.EXHAUSTED, s)
        s = nxt
        bound -= 1


def run(s: State) -> tuple[Terminal, State]:
    return run_det(s.fuel, s)


def init(C: Controlled, x: int, fuel: int) -> State:
    """The Lean ``init``: the program, a start datum, the start on the tape,
    clock zero, a declared fuel.  Reads the setting only through the merged
    encoder; the designated pair is not read."""
    if not 0 <= x < C.F.n:
        raise ExecutionError("the start datum lies outside the carrier")
    if fuel < 0:
        raise ExecutionError("fuel is a count")
    return State(program(C), nops(C), x, (x,), 0, fuel)


def trace(C: Controlled, x: int, fuel: int) -> tuple[Terminal, State]:
    return run(init(C, x, fuel))


def with_ops(C: Controlled, ops: Sequence[tuple[int, ...]], ctrl: Enablement) -> Controlled:
    """A controlled setting on the same carrier and stores with other
    operations and enablements.  Apparatus for the tests."""
    F = tr.FiniteSetting(C.F.n, C.F.rel, C.F.ret, C.F.prot, C.F.a, C.F.b, tuple(ops))
    return Controlled(F, ctrl)
