"""One interpreter, parameterised by what it reads.

AuthorityEffect: None.  Configuration status: DECLARED_HOST_CONFIG, as for
``control``: this is the same machine, not a new one.

Mirrors ``lean/Runner.lean``.  Three families here run the same interpreter
with three different enablement reads.  The question the copying raised was
whether a reader must see more than the state.  It need not: all three are
functions ``State -> tuple[int, ...]``, so the runner is one function of a
reader and each family's runner is that function at its own reader.

The Lean states the identification as ``rfl`` — ``Control.stepDet`` *is*
``stepDetOf ctrlReader``.  Python cannot say that, so the families check it
instead, exhaustively over their declared populations: ``tests/test_runner.py``
here for the merged read, and the record-reading family's tests for the other
two.  A fourth read costs a reader and no runner at all.
"""

from __future__ import annotations

from typing import Callable

import control as ct
from execution import lookup

Reader = Callable[[ct.State], tuple[int, ...]]


def step_det_of(read: Reader, s: ct.State) -> ct.Terminal | ct.State:
    """The Lean ``stepDetOf``: fire the one operation the reader names, halt
    when it names none, stop with ``BRANCH`` when it names two.  It never
    selects."""
    named = read(s)
    if not named:
        return ct.Terminal.HALT
    if len(named) >= 2:
        return ct.Terminal.BRANCH
    fired = ct.fire(s, named[0])
    if fired is ct.Refusal.EXHAUSTED:
        return ct.Terminal.EXHAUSTED
    if fired is ct.Refusal.NO_EDGE:
        return ct.Terminal.REFUSE
    assert isinstance(fired, ct.State)
    return fired


def next_of(read: Reader, s: ct.State) -> ct.State:
    nxt = step_det_of(read, s)
    return s if isinstance(nxt, ct.Terminal) else nxt


def iter_of(read: Reader, n: int, s: ct.State) -> ct.State:
    for _ in range(n):
        s = next_of(read, s)
    return s


def obs_of(read: Reader, n: int, s: ct.State) -> tuple[int, ...]:
    return iter_of(read, n, s).tape


def run_det_of(read: Reader, bound: int, s: ct.State) -> tuple[ct.Terminal, ct.State]:
    while True:
        nxt = step_det_of(read, s)
        if isinstance(nxt, ct.Terminal):
            return (nxt, s)
        if bound <= 0:
            return (ct.Terminal.EXHAUSTED, s)
        s = nxt
        bound -= 1


def ctrl_reader(s: ct.State) -> tuple[int, ...]:
    """What the merged machine reads: the enablements at the active datum."""
    return ct.enabled_at(s.graph, s.nops, s.active)


def blind_reader(_: ct.State) -> tuple[int, ...]:
    """A reader that ignores the state: the machine halts at once."""
    return ()


def greedy_reader(_: ct.State) -> tuple[int, ...]:
    """A reader that names two everywhere: the machine always branches, and the
    runner refuses it exactly as each copy did."""
    return (0, 1)


def next_value_of(read: Reader, s: ct.State) -> int | None:
    """The datum the runner moves to, read from the program: the value of the
    one operation the reader names, and ``None`` when it names none or two, or
    there is no edge."""
    named = read(s)
    return lookup(3 + named[0], s.active, s.graph) if len(named) == 1 else None
