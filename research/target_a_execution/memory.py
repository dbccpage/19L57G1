"""Retained internal records [p, x] and depth-2 ternary forms [b, p, x].

AuthorityEffect: None.
Configuration status: DECLARED_HOST_CONFIG.

This module implements the ladder of reading depths:
1. Depth 0 (Memoryless): Enablement reads active datum only: (3 + nops + k, (x, x)).
   Ceiling: Tapes are functional in single entries only.
2. Depth 1 (Retained Record): Enablement reads predecessor and active datum:
   (3 + nops + k, (p, x)).
   Ceiling: Tapes are functional in pairs; breaks the memoryless ceiling.
   Example: twist tape (0, 1, 0, 0) where datum 0 is followed by 1 and later by 0.
3. Depth 2 (Ternary Control): Enablement reads two past entries plus active datum:
   (3 + nops + k, (b, p, x)) on a TERNARY control form.
   Ceiling: Tapes are functional in triples; breaks the depth-1 pair ceiling.
   Example: twist2 tape (0, 1, 2, 0, 1, 0) where pair (0, 1) is followed by 2 and later by 0.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from control import State, ctrl_form, fire
from runner import ExecutionError, Graph, Terminal, run_det_of, step_det_of

RecordEnablement = frozenset[tuple[int, int, int]]  # (previous, active, op_k)
Depth2Enablement = frozenset[tuple[int, int, int, int]]  # (before, previous, active, op_k)


# ---------------------------------------------------------------------------
# Depth-1 Retained Record Reading [p, x]
# ---------------------------------------------------------------------------


def previous(s: State) -> int:
    """Return the datum prior to the active datum on the tape.

    If the tape has fewer than 2 entries, the active datum is its own predecessor.
    """
    return s.tape[-2] if len(s.tape) >= 2 else s.active


def renabled(g: Graph, count: int, p: int, x: int, k: int) -> bool:
    """Check if operation k is enabled at datum x given previous datum p."""
    f = ctrl_form(count, k)
    return (f, (p, x)) in g


def renabled_at(g: Graph, count: int, p: int, x: int) -> tuple[int, ...]:
    """Return all operation indices enabled at active datum x after previous datum p."""
    return tuple(k for k in range(count) if renabled(g, count, p, x, k))


def record_reader(s: State) -> tuple[int, ...]:
    """Extract operations enabled at active datum after previous datum on the tape."""
    return renabled_at(s.graph, s.nops, previous(s), s.active)


def rstep_det(s: State) -> Terminal | State:
    """Execute one deterministic step with depth-1 record reading."""
    return step_det_of(record_reader, s, fire)


def rrun_det(bound: int, s: State) -> tuple[Terminal, State]:
    """Run depth-1 record machine bounded by fuel/step limit."""
    return run_det_of(record_reader, bound, s, fire)


def build_record_program(
    n: int,
    ops: Sequence[Sequence[int]],
    hctrl: Sequence[tuple[int, int, int]],
) -> Graph:
    """Build graph with binary operation edges and binary record enablements [p, x]."""
    count = len(ops)
    edges: set[tuple[int, tuple[int, ...]]] = set()
    for k, op in enumerate(ops):
        for x in range(n):
            edges.add((3 + k, (x, op[x])))
    for p, x, k in hctrl:
        if not (0 <= p < n and 0 <= x < n and 0 <= k < count):
            raise ExecutionError(f"record enablement ({p}, {x}, {k}) out of bounds")
        edges.add((ctrl_form(count, k), (p, x)))
    return frozenset(edges)


# ---------------------------------------------------------------------------
# Depth-2 Ternary Control Reading [b, p, x]
# ---------------------------------------------------------------------------


def before(s: State) -> int:
    """Return the datum two entries prior to the active datum on the tape."""
    if len(s.tape) >= 3:
        return s.tape[-3]
    return previous(s)


def r2enabled(g: Graph, count: int, b: int, p: int, x: int, k: int) -> bool:
    """Check if operation k is enabled at x given predecessor p and earlier datum b.

    Stored as ternary instance: (3 + count + k, (b, p, x)).
    """
    f = ctrl_form(count, k)
    return (f, (b, p, x)) in g


def r2enabled_at(g: Graph, count: int, b: int, p: int, x: int) -> tuple[int, ...]:
    """Return all operation indices enabled at x given history (b, p)."""
    return tuple(k for k in range(count) if r2enabled(g, count, b, p, x, k))


def depth_reader(s: State) -> tuple[int, ...]:
    """Extract operations enabled at x given before(s) and previous(s)."""
    return r2enabled_at(s.graph, s.nops, before(s), previous(s), s.active)


def r2step_det(s: State) -> Terminal | State:
    """Execute one deterministic step with depth-2 ternary record reading."""
    return step_det_of(depth_reader, s, fire)


def r2run_det(bound: int, s: State) -> tuple[Terminal, State]:
    """Run depth-2 ternary record machine bounded by fuel/step limit."""
    return run_det_of(depth_reader, bound, s, fire)


def build_depth2_program(
    n: int,
    ops: Sequence[Sequence[int]],
    hctrl2: Sequence[tuple[int, int, int, int]],
) -> Graph:
    """Build graph with binary operation edges and ternary depth-2 enablements [b, p, x]."""
    count = len(ops)
    edges: set[tuple[int, tuple[int, ...]]] = set()
    for k, op in enumerate(ops):
        for x in range(n):
            edges.add((3 + k, (x, op[x])))
    for b, p, x, k in hctrl2:
        if not (0 <= b < n and 0 <= p < n and 0 <= x < n and 0 <= k < count):
            raise ExecutionError(f"depth-2 enablement ({b}, {p}, {x}, {k}) out of bounds")
        edges.add((ctrl_form(count, k), (b, p, x)))
    return frozenset(edges)


# ---------------------------------------------------------------------------
# Functionality Ceilings & Ladder Analysis
# ---------------------------------------------------------------------------


def windows(k: int, tape: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    """Return all contiguous sub-slices of length k from tape."""
    if k < 1:
        raise ExecutionError("window length must be >= 1")
    if len(tape) < k:
        return ()
    return tuple(tuple(tape[i : i + k]) for i in range(len(tape) - k + 1))


def functional(k: int, tape: Sequence[int]) -> bool:
    """Check if tape is functional in k entries.

    A tape is functional in k entries iff whenever two windows of length k + 1
    share the same prefix of length k, they have the exact same final entry:
        window1[:k] == window2[:k] ==> window1[k] == window2[k].
    - k = 1: Memoryless ceiling (single datum uniquely determines next).
    - k = 2: Depth-1 ceiling (pair of data uniquely determines next).
    - k = 3: Depth-2 ceiling (triple of data uniquely determines next).
    """
    seen: dict[tuple[int, ...], int] = {}
    for window in windows(k + 1, tape):
        key, val = window[:k], window[k]
        if seen.setdefault(key, val) != val:
            return False
    return True


# Canonical witness tapes demonstrating ceiling breaks:
TWIST_TAPE: tuple[int, ...] = (0, 1, 0, 0)
TWIST2_TAPE: tuple[int, ...] = (0, 1, 2, 0, 1, 0)
