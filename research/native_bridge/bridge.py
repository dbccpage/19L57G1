"""Exact finite mirror of the native bridge theorems.

AuthorityEffect: None.  The sealed Python dynamics are consumed read-only
through their public functions: ``derivation.primitive_passage`` (the
passage step), ``derivation.trace_algebra`` and
``derivation.transition_alphabet`` (typed records), and
``derivation.model`` (the token-aware admission step).  Every check runs
over a declared finite battery and reports its counts; none of them is a
proof beyond that battery.  The general statements are the Lean theorems
named in ``CLAIMS.md``.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from itertools import product
import json
from pathlib import Path

from derivation.model import (
    EMPTY,
    AdmissionError,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Event,
    Impose,
    Regime,
    Supply,
    step,
)
from derivation.primitive_passage import GENESIS_P, PS, PEvent, preplay, pstep
from derivation.trace_algebra import (
    TRecord,
    aligned,
    build_trace,
    end_state,
    erase_trace,
    legal_trace,
    make_record,
    named_states,
)
from derivation.transition_alphabet import accepted, wf_class

Json = dict[str, object]
Core = tuple[object, ...]

# The declared battery: two occurrence positions, their ordered pairs,
# three columns, budgets zero to two, both license values, and the
# terminal.  Column refinement ranges over those columns and the empty one.
POSITIONS: tuple[int, ...] = (0, 1)
COLUMNS: tuple[tuple[int, ...], ...] = ((0,), (1,), (0, 1))
REFINED: tuple[tuple[int, ...], ...] = ((),) + COLUMNS
BUDGETS: tuple[int, ...] = (0, 1, 2)


def alphabet() -> tuple[PEvent, ...]:
    """The declared finite event alphabet, in a fixed order."""
    pairs = [(i, j) for i in POSITIONS for j in POSITIONS if i != j]
    events: list[PEvent] = [("admitOcc", t) for t in POSITIONS]
    for kind in ("assertWit", "admitWit", "protect", "refuse"):
        events.extend((kind, i, j) for i, j in pairs)
    events.append(("declareObs",))
    events.extend(("refineCol", v, p) for v in REFINED for p in POSITIONS)
    events.extend(("addCol", c) for c in COLUMNS)
    events.extend(("setBudget", n) for n in BUDGETS)
    events.extend(("setLicense", b) for b in (False, True))
    events.append(("halt",))
    return tuple(events)


def core(s: PS) -> Core:
    """Every field except budget and license (Lean ``core``)."""
    return (s.occ, s.asserted, s.wit, s.prot, s.obs, s.refusals, s.halted)


def size(s: PS) -> int:
    """Lean ``size``: store lengths, columns plus their lengths, terminal."""
    obs = 0 if s.obs is None else 1 + sum(1 + len(c) for c in s.obs)
    return (len(s.occ) + len(s.asserted) + len(s.wit) + len(s.prot) + obs
            + len(s.refusals) + int(s.halted))


Step = Callable[[PS, PEvent], PS]


def reachable(depth: int, events: Sequence[PEvent],
              starts: Sequence[PS] = (GENESIS_P,), f: Step = pstep) -> list[PS]:
    """States reachable from ``starts`` in at most ``depth`` steps, in
    breadth-first discovery order."""
    seen: dict[PS, None] = dict.fromkeys(starts)
    frontier = list(seen)
    for _ in range(depth):
        nxt: list[PS] = []
        for s in frontier:
            for e in events:
                t = f(s, e)
                if t not in seen:
                    seen[t] = None
                    nxt.append(t)
        frontier = nxt
    return list(seen)


def dichotomy(states: Sequence[PS], events: Sequence[PEvent],
              f: Step = pstep) -> Json:
    """Every step keeps the core or strictly grows the size."""
    keep = 0
    grow: dict[str, int] = {}
    for s in states:
        for e in events:
            t = f(s, e)
            if core(t) == core(s):
                keep += 1
            elif size(s) < size(t):
                kind = str(e[0])
                grow[kind] = grow.get(kind, 0) + 1
            else:
                raise AssertionError(f"step neither keeps nor grows: {s} {e}")
    return {"pairs": keep + sum(grow.values()), "keep": keep,
            "grow_by_kind": dict(sorted(grow.items()))}


def components(states: Sequence[PS], events: Sequence[PEvent],
               f: Step = pstep) -> list[list[PS]]:
    """Strongly connected components of the step graph restricted to
    ``states`` (edges that leave the set are dropped)."""
    index = {s: k for k, s in enumerate(states)}
    succ = [sorted({index[t] for e in events
                    if (t := f(s, e)) in index}) for s in states]
    order: list[int] = []
    seen = [False] * len(states)
    for root in range(len(states)):
        if seen[root]:
            continue
        seen[root] = True
        stack = [(root, 0)]
        while stack:
            v, k = stack.pop()
            if k < len(succ[v]):
                stack.append((v, k + 1))
                w = succ[v][k]
                if not seen[w]:
                    seen[w] = True
                    stack.append((w, 0))
            else:
                order.append(v)
    pred: list[list[int]] = [[] for _ in states]
    for v, ws in enumerate(succ):
        for w in ws:
            pred[w].append(v)
    comp = [-1] * len(states)
    result: list[list[PS]] = []
    for root in reversed(order):
        if comp[root] >= 0:
            continue
        members = [root]
        comp[root] = len(result)
        k = 0
        while k < len(members):
            for w in pred[members[k]]:
                if comp[w] < 0:
                    comp[w] = len(result)
                    members.append(w)
            k += 1
        result.append([states[m] for m in sorted(members)])
    return result


def cycle_report(states: Sequence[PS], events: Sequence[PEvent],
                 f: Step = pstep) -> Json:
    """Every component shares one core; only budget and license vary."""
    comps = components(states, events, f)
    nontrivial = [c for c in comps if len(c) > 1]
    varying: set[str] = set()
    for comp in nontrivial:
        if len({core(s) for s in comp}) != 1:
            raise AssertionError("a cycle moves a core field")
        if len({s.budget for s in comp}) > 1:
            varying.add("budget")
        if len({s.licensed for s in comp}) > 1:
            varying.add("licensed")
    return {"components": len(comps), "nontrivial": len(nontrivial),
            "largest": max(len(c) for c in comps),
            "varying_fields": sorted(varying)}


def records(s: PS, events: Sequence[PEvent]) -> tuple[TRecord, ...]:
    """Lean ``records``: one computed record per step, inert steps
    included."""
    out: list[TRecord] = []
    cur = s
    for e in events:
        r = make_record(cur, e)
        out.append(r)
        cur = r.post
    return tuple(out)


def histories(events: Sequence[PEvent], length: int) -> list[tuple[PEvent, ...]]:
    return [h for n in range(length + 1) for h in product(events, repeat=n)]


def record_report(start: PS, events: Sequence[PEvent], length: int) -> Json:
    """Typed records against native replay, over every history up to
    ``length`` events."""
    total = legal = 0
    for h in histories(events, length):
        tr = records(start, h)
        end = preplay(h, start)
        all_acc = True
        cur = start
        for e in h:
            all_acc = all_acc and accepted(cur, e) and wf_class(cur)
            cur = pstep(cur, e)
        if not (aligned(start, tr) and erase_trace(tr) == list(h)
                and end_state(start, tr) == end):
            raise AssertionError(f"record square fails: {h}")
        if legal_trace(start, tr) != all_acc:
            raise AssertionError(f"legality mismatch: {h}")
        accepted_records = tuple(r for r in tr if accepted(r.pre, r.ev))
        if accepted_records != build_trace(start, h):
            raise AssertionError(f"accepted records differ: {h}")
        total += 1
        legal += int(all_acc)
    return {"histories": total, "legal": legal, "max_length": length}


def budget_sim(g: Callable[[int, int], int], states: Sequence[int],
               events: Sequence[int]) -> Json:
    """The budget register: each source step is one budget write."""
    def enc(x: int) -> PS:
        return PS(budget=x)
    squares = 0
    for x in states:
        for e in events:
            if preplay([("setBudget", g(x, e))], enc(x)) != enc(g(x, e)):
                raise AssertionError(f"square fails at {x}, {e}")
            squares += 1
    encodings = {enc(x) for x in states}
    return {"squares": squares, "distinct_encodings": len(encodings),
            "distinct_cores": len({core(p) for p in encodings})}


def realize(dec: Callable[[str], PEvent | None],
            steps: Sequence[tuple[PS, PS, str]]) -> list[PEvent] | None:
    """Read a labelled step list back as native events, or refuse."""
    out: list[PEvent] = []
    for src, dst, label in steps:
        e = dec(label)
        if e is None or pstep(src, e) != dst:
            return None
        out.append(e)
    return out


def witness_decoder(label: str) -> PEvent | None:
    return {"admitOcc": ("admitOcc", 0), "halt": ("halt",)}.get(label)


def realize_report() -> Json:
    halted = pstep(GENESIS_P, ("halt",))
    one = pstep(GENESIS_P, ("admitOcc", 0))
    refused = realize(witness_decoder, [(GENESIS_P, halted, "admitOcc")])
    joined = preplay([("halt",)], GENESIS_P) == halted
    accepted_path = realize(witness_decoder, [(GENESIS_P, one, "admitOcc")])
    return {"mislabelled_refused": refused is None,
            "endpoints_joined": joined,
            "realized_events": [list(e) for e in accepted_path or []]}


def admission_alphabet() -> tuple[Event, ...]:
    return (Supply("x"), AdmitDatum("a"), AdmitDatum("b"), AdmitForm(1),
            AdmitInst(0, (0,)), AdmitInst(0, (1,)), AdmitRuleAll(0),
            Impose(0, 1))


def rsize(r: Regime) -> int:
    return len(r.data) + len(r.forms) + len(r.insts) + len(r.rules) + len(r.reqs)


def admission_report(depth: int) -> Json:
    """Every successful admission step keeps the regime or grows it."""
    seen: dict[Regime, None] = {EMPTY: None}
    frontier = [EMPTY]
    keep = grow = refused = 0
    for _ in range(depth):
        nxt: list[Regime] = []
        for r in frontier:
            for e in admission_alphabet():
                try:
                    t = step(r, e)
                except AdmissionError:
                    refused += 1
                    continue
                if t == r:
                    keep += 1
                elif rsize(r) < rsize(t):
                    grow += 1
                else:
                    raise AssertionError(f"admission neither keeps nor grows: {e}")
                if t not in seen:
                    seen[t] = None
                    nxt.append(t)
        frontier = nxt
    return {"regimes": len(seen), "keep": keep, "grow": grow,
            "refused": refused, "depth": depth}


def bounds() -> dict[str, int]:
    """The declared bounds, read from the pinned ``input.json``."""
    value = json.loads((Path(__file__).resolve().parent / "input.json")
                       .read_text(encoding="utf-8"))
    keys = {"admission_depth", "reachable_depth", "record_length"}
    if (not isinstance(value, dict) or set(value) != keys
            or not all(isinstance(value[k], int) and not isinstance(value[k], bool)
                       and value[k] >= 0 for k in keys)):
        raise ValueError("input.json: expected three nonnegative integer bounds")
    return {k: int(value[k]) for k in sorted(keys)}


def receipt() -> Json:
    b = bounds()
    events = alphabet()
    states = reachable(b["reachable_depth"], events, named_states())
    small = (("admitOcc", 0), ("admitOcc", 1), ("assertWit", 0, 1),
             ("setBudget", 1), ("setLicense", False), ("halt",))
    return {
        "authority_effect": "None",
        "alphabet": len(events),
        "bounds": dict(b),
        "states": len(states),
        "dichotomy": dichotomy(states, events),
        "cycles": cycle_report(states, events),
        "records": record_report(GENESIS_P, small, b["record_length"]),
        "toggle": budget_sim(lambda x, _e: 1 - x, [0, 1], [0]),
        "rotation": budget_sim(lambda x, e: (x + e) % 3, [0, 1, 2], [1, 2]),
        "realize": realize_report(),
        "admission": admission_report(b["admission_depth"]),
    }
