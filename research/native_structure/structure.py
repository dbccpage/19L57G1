"""Exact finite mirror of the native structure theorems.

AuthorityEffect: None.  Consumes the sealed passage dynamics and the
``native_bridge`` tree's ``bridge.py`` (alphabet, core, reachable states)
read-only.  Every check runs over the declared battery in ``input.json``
and reports its counts; the general statements are the Lean theorems named
in ``CLAIMS.md``.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import replace
import json
from pathlib import Path

from bridge import alphabet, core, reachable
from derivation.primitive_passage import PS, PEvent, preplay, pstep
from derivation.trace_algebra import named_states

Json = dict[str, object]
Cost = Callable[[PS, PEvent], int]

FUNDED = frozenset({"refineCol", "addCol"})
LICENSE_SENSITIVE = frozenset({"addCol", "setLicense", "halt"})


def bounds() -> dict[str, int]:
    """The declared bounds, read from the pinned ``input.json``."""
    value = json.loads((Path(__file__).resolve().parent / "input.json")
                       .read_text(encoding="utf-8"))
    keys = {"square_depth", "descent_depth", "history_length"}
    if (not isinstance(value, dict) or set(value) != keys
            or not all(isinstance(value[k], int) and not isinstance(value[k], bool)
                       and value[k] >= 0 for k in keys)):
        raise ValueError("input.json: expected three nonnegative integer bounds")
    return {k: int(value[k]) for k in sorted(keys)}


def commutes(u: PS, e1: PEvent, e2: PEvent) -> bool:
    return pstep(pstep(u, e1), e2) == pstep(pstep(u, e2), e1)


def d_square(c: Cost, u: PS, e1: PEvent, e2: PEvent) -> int:
    """Lean ``dSquare``: the boundary of the square, paired with ``c``."""
    return c(u, e1) + c(pstep(u, e1), e2) - c(u, e2) - c(pstep(u, e2), e1)


def budget_delta(s: PS, e: PEvent) -> int:
    return pstep(s, e).budget - s.budget


def writes(s: PS, e: PEvent) -> int:
    return 0 if pstep(s, e) == s else 1


def path_cost(c: Cost, s: PS, events: Sequence[PEvent]) -> int:
    total = 0
    for e in events:
        total += c(s, e)
        s = pstep(s, e)
    return total


def square_report(states: Sequence[PS], events: Sequence[PEvent]) -> Json:
    """Commuting squares, and the closedness of two costs on them."""
    commuting = noncommuting = delta_open = writes_open = 0
    for u in states:
        for i, e1 in enumerate(events):
            for e2 in events[i + 1:]:
                if not commutes(u, e1, e2):
                    noncommuting += 1
                    continue
                commuting += 1
                delta_open += int(d_square(budget_delta, u, e1, e2) != 0)
                writes_open += int(d_square(writes, u, e1, e2) != 0)
    if delta_open:
        raise AssertionError("the exact budget cost is open on a commuting square")
    return {"commuting": commuting, "noncommuting": noncommuting,
            "budget_delta_open": delta_open, "writes_open": writes_open}


def telescoping_report(start: PS, events: Sequence[PEvent], length: int) -> Json:
    """The budget cost telescopes along every history up to ``length``."""
    histories: list[tuple[PEvent, ...]] = [()]
    frontier: list[tuple[PEvent, ...]] = [()]
    for _ in range(length):
        frontier = [h + (e,) for h in frontier for e in events]
        histories.extend(frontier)
    for h in histories:
        if path_cost(budget_delta, start, h) != preplay(h, start).budget - start.budget:
            raise AssertionError(f"budget cost does not telescope: {h}")
    loops = [h for h in histories if h and preplay(h, start) == start
             and path_cost(writes, start, h) != 0]
    return {"histories": len(histories), "writes_nonzero_loops": len(loops),
            "shortest_loop": [list(e) for e in min(loops, key=len)] if loops else []}


def descent_report(states: Sequence[PS], events: Sequence[PEvent]) -> Json:
    """States with equal cores step to equal cores, except under the two
    funded events."""
    groups: dict[object, list[PS]] = {}
    for s in states:
        groups.setdefault(core(s), []).append(s)
    checked = 0
    violations: dict[str, int] = {}
    for members in groups.values():
        for k, s in enumerate(members):
            for t in members[k + 1:]:
                for e in events:
                    same = core(pstep(s, e)) == core(pstep(t, e))
                    kind = str(e[0])
                    if kind in FUNDED:
                        violations[kind] = violations.get(kind, 0) + int(not same)
                    elif not same:
                        raise AssertionError(f"unfunded event fails descent: {e}")
                    else:
                        checked += 1
    return {"core_classes": len(groups), "unfunded_checked": checked,
            "funded_violations": dict(sorted(violations.items()))}


def act_state(pi: Callable[[int], int], s: PS) -> PS:
    return replace(s, occ=tuple(pi(t) for t in s.occ))


def act_event(pi: Callable[[int], int], e: PEvent) -> PEvent:
    if e[0] == "admitOcc":
        t = e[1]
        assert isinstance(t, int)
        return ("admitOcc", pi(t))
    return e


def equivariance_failures(pi: Callable[[int], int], states: Sequence[PS],
                          events: Sequence[PEvent]) -> int:
    return sum(pstep(act_state(pi, s), act_event(pi, e)) != act_state(pi, pstep(s, e))
               for s in states for e in events)


def frame_report(states: Sequence[PS], events: Sequence[PEvent]) -> Json:
    """The sealed license frame yields a commuting square at every state."""
    squares = 0
    for u in states:
        for b in (False, True):
            for e in events:
                if e[0] in LICENSE_SENSITIVE:
                    continue
                if not commutes(u, ("setLicense", b), e):
                    raise AssertionError(f"license frame fails: {e}")
                squares += 1
    return {"license_frame_squares": squares}


def receipt() -> Json:
    b = bounds()
    events = alphabet()
    squares_at = reachable(b["square_depth"], events, named_states())
    descent_at = reachable(b["descent_depth"], events, named_states())
    small: tuple[PEvent, ...] = (("setBudget", 0), ("setBudget", 1),
                                 ("setLicense", False), ("setLicense", True))
    swap01 = {0: 1, 1: 0}
    return {
        "authority_effect": "None",
        "bounds": dict(b),
        "square_states": len(squares_at),
        "squares": square_report(squares_at, events),
        "telescoping": telescoping_report(named_states()[0], small, b["history_length"]),
        "descent_states": len(descent_at),
        "descent": descent_report(descent_at, events),
        "equivariance": {
            "shift_failures": equivariance_failures(lambda t: t + 5, descent_at, events),
            "swap_failures": equivariance_failures(lambda t: swap01.get(t, t),
                                                   descent_at, events),
            "constant_failures": equivariance_failures(lambda t: 0, descent_at, events),
        },
        "frame": frame_report(squares_at, events),
    }
