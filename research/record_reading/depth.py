"""A record read two entries deep, and the ladder of reading depths.

AuthorityEffect: None.  Configuration status: DECLARED_HOST_CONFIG, as for
``record``: the state is a metatheory record carrying encoded instances.

Mirrors ``lean/Depth.lean``.  A depth-two enablement reads ``(before,
previous, active)`` and is represented on a **ternary** control form, one per
operation, with instances ``(3 + nops + k, (b, p, x))``.  The sealed grammar
needs no change for that: ``Regime.wf`` bounds a form's arity below by one and
not above, so a regime of mixed arity — binary stores and operation graphs
beside ternary enablements — is a regime as the grammar already stands
(``Depth.encodeR2_wf``).

The ladder this module computes:

* a memoryless run's tape is functional in its **single entries** — equal
  entries have equal successors;
* a depth-one run's tape is functional in its **pairs** and need not be
  functional in its entries;
* a depth-two run's tape is functional in its **triples** and need not be
  functional in its pairs.

The Lean proves the three ceilings (``Observe.obs_functional``,
``Record.robs_functional``, ``Depth.r2obs_functional``) and that the ladder
only grows (``Depth.triples_of_pairs``, ``Depth.quads_of_triples``).  What
this module adds is the exhaustive count: over *every* deterministic program
of each depth on a declared two-point setting, which tapes are realised, and
that each ceiling holds of every one of them while the rung below fails on
some.  A machine of depth ``d`` for ``d > 2`` is not built, here or in the
Lean; ``functional`` is written for any window size so that the statement
being checked is the same one at every rung.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product as tuples
from typing import Iterator, Sequence

import control as ct
import record as rc
import translation as tr
from derivation.model import AdmitForm, AdmitInst, Event, Regime, replay
from execution import ExecutionError, Graph

Depth2Enablement = frozenset[tuple[int, int, int, int]]
Word = tuple[int, ...]


# ---------------------------------------------------------------------------
# Depth-two recorded settings and their represented program
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Recorded2:
    """A finite setting with an enablement reading two entries of the record:
    ``(before, previous, active, k)``."""

    F: tr.FiniteSetting
    hctrl2: Depth2Enablement

    def __post_init__(self) -> None:
        count = len(self.F.ops)
        for b, p, x, k in self.hctrl2:
            if not (0 <= b < self.F.n and 0 <= p < self.F.n and 0 <= x < self.F.n
                    and 0 <= k < count):
                raise ExecutionError(
                    f"depth-two enablement ({b}, {p}, {x}, {k}) lies outside the setting")


def ctrl_form(C: Recorded2, k: int) -> int:
    return 3 + len(C.F.ops) + k


def forms_of(nops: int) -> tuple[int, ...]:
    """The Lean ``formsOf``: three binary stores, one binary form per
    operation graph, and one **ternary** form per enablement."""
    return (2,) * (3 + nops) + (3,) * nops


def r2step(C: Recorded2, b: int, p: int, x: int, k: int, y: int) -> bool:
    """The reference step, stated on the setting before any encoding.  A
    *check* the tests and the receipt use; the machine never calls it."""
    return (k < len(C.F.ops) and (b, p, x, k) in C.hctrl2
            and y == tr.run(C.F, (k,), x))


def events_r2(C: Recorded2) -> tuple[Event, ...]:
    """The admission history: the merged encoder's events, one ternary form
    per operation, and the enablements as ternary instances."""
    out: list[Event] = list(tr.events(C.F))
    out.extend(AdmitForm(3) for _ in range(len(C.F.ops)))
    out.extend(AdmitInst(ctrl_form(C, k), (b, p, x)) for b, p, x, k in sorted(C.hctrl2))
    return tuple(out)


def encode_r2(C: Recorded2) -> Regime:
    """The Lean ``encodeR2``, as the sealed replay of ``events_r2``.  That it
    is well formed is the sealed grammar accepting mixed arity."""
    return replay(events_r2(C))


def r2program(C: Recorded2) -> Graph:
    edges = {(3 + k, (x, g[x])) for k, g in enumerate(C.F.ops) for x in range(C.F.n)}
    records = {(ctrl_form(C, k), (b, p, x)) for b, p, x, k in C.hctrl2}
    return frozenset(edges | records)


def r2program_by_replay(C: Recorded2) -> Graph:
    return frozenset(i for i in encode_r2(C).insts if i[0] >= 3)


# ---------------------------------------------------------------------------
# Reading two entries, and the interpreter
# ---------------------------------------------------------------------------


def r2enabled(g: Graph, count: int, b: int, p: int, x: int, k: int) -> bool:
    """Membership, not a lookup: several instances of one ternary control
    form share a prefix, so the read is a relation."""
    return (3 + count + k, (b, p, x)) in g


def r2enabled_at(g: Graph, count: int, b: int, p: int, x: int) -> tuple[int, ...]:
    return tuple(k for k in range(count) if r2enabled(g, count, b, p, x, k))


def before(s: ct.State) -> int:
    """The datum two before the last on the record; a record too short for it
    falls back to the one before the last, as that falls back to the active
    datum."""
    return s.tape[-3] if len(s.tape) >= 3 else rc.previous(s)


def r2step_det(s: ct.State) -> ct.Terminal | ct.State:
    en = r2enabled_at(s.graph, s.nops, before(s), rc.previous(s), s.active)
    if not en:
        return ct.Terminal.HALT
    if len(en) >= 2:
        return ct.Terminal.BRANCH
    fired = ct.fire(s, en[0])
    if fired is ct.Refusal.EXHAUSTED:
        return ct.Terminal.EXHAUSTED
    if fired is ct.Refusal.NO_EDGE:
        return ct.Terminal.REFUSE
    assert isinstance(fired, ct.State)
    return fired


def r2next(s: ct.State) -> ct.State:
    nxt = r2step_det(s)
    return s if isinstance(nxt, ct.Terminal) else nxt


def r2iter(n: int, s: ct.State) -> ct.State:
    if n < 0:
        raise ExecutionError("a scale is a count")
    for _ in range(n):
        s = r2next(s)
    return s


def r2obs(n: int, s: ct.State) -> Word:
    return r2iter(n, s).tape


def r2init(C: Recorded2, x: int, fuel: int) -> ct.State:
    if not 0 <= x < C.F.n:
        raise ExecutionError("the start datum lies outside the carrier")
    if fuel < 0:
        raise ExecutionError("fuel is a count")
    return ct.State(r2program(C), len(C.F.ops), x, (x,), 0, fuel)


def r2trace(C: Recorded2, x: int, fuel: int) -> tuple[ct.Terminal, ct.State]:
    s = r2init(C, x, fuel)
    while True:
        nxt = r2step_det(s)
        if isinstance(nxt, ct.Terminal):
            return (nxt, s)
        s = nxt


def lift2(C: rc.Recorded) -> Recorded2:
    """A depth-one setting read as a depth-two one: the enablement ignores the
    entry it is newly given."""
    return Recorded2(C.F, frozenset((b, p, x, k) for b in range(C.F.n)
                                    for p, x, k in C.hctrl))


# ---------------------------------------------------------------------------
# The ladder: windows of a tape, and functionality in them
# ---------------------------------------------------------------------------


def windows(k: int, tape: Sequence[int]) -> tuple[Word, ...]:
    """Every contiguous run of ``k`` entries, in order."""
    if k < 1:
        raise ExecutionError("a window has a length")
    return tuple(tuple(tape[i:i + k]) for i in range(len(tape) - k + 1))


def functional(k: int, tape: Sequence[int]) -> bool:
    """The tape is functional in ``k`` entries: two windows of ``k + 1``
    agreeing on their first ``k`` agree on the last.  ``k = 1`` is
    memorylessness, ``k = 2`` the ceiling of a depth-one read, ``k = 3`` the
    ceiling of a depth-two read."""
    seen: dict[Word, int] = {}
    for window in windows(k + 1, tape):
        key, value = window[:k], window[k]
        if seen.setdefault(key, value) != value:
            return False
    return True


# ---------------------------------------------------------------------------
# The exhaustive sweep over deterministic programs of each depth
# ---------------------------------------------------------------------------


def keys(depth: int, n: int) -> tuple[Word, ...]:
    """The keys a machine of this depth reads: tuples of ``depth`` data."""
    return tuple(tuples(range(n), repeat=depth))


def deterministic_choices(depth: int, n: int, count: int) -> Iterator[dict[Word, int]]:
    """Every assignment of at most one operation to each key: ``count`` means
    "no operation enabled here", so the machine halts there."""
    for values in tuples(range(count + 1), repeat=len(keys(depth, n))):
        yield {key: value for key, value in zip(keys(depth, n), values) if value < count}


def realized_tapes(depth: int, F: tr.FiniteSetting, fuel: int) -> set[Word]:
    """Every tape realised by a deterministic program of this depth, from
    every datum of the carrier, at this fuel."""
    count = len(F.ops)
    out: set[Word] = set()
    for choice in deterministic_choices(depth, F.n, count):
        for start in range(F.n):
            if depth == 1:
                C1 = ct.Controlled(F, frozenset((key[0], k) for key, k in choice.items()))
                out.add(ct.trace(C1, start, fuel)[1].tape)
            elif depth == 2:
                C2 = rc.Recorded(F, frozenset((key[0], key[1], k) for key, k in choice.items()))
                out.add(rc.rtrace(C2, start, fuel)[1].tape)
            elif depth == 3:
                C3 = Recorded2(F, frozenset((key[0], key[1], key[2], k)
                                            for key, k in choice.items()))
                out.add(r2trace(C3, start, fuel)[1].tape)
            else:
                raise ExecutionError("no machine of that depth is built")
    return out


def ladder(F: tr.FiniteSetting, fuel: int) -> list[dict[str, object]]:
    """For each built depth: how many tapes it realises, that every one of
    them meets that depth's ceiling, and whether any of them breaks the
    ceiling of the depth below.

    The ``window`` column is the length of the window the ceiling speaks of:
    a machine reading ``d`` entries is functional in ``d`` and its tapes are
    windows of ``d + 1``.  A rung is *strict* when it realises a tape the rung
    below could not — which by the ceiling below is exactly a tape that breaks
    that ceiling.
    """
    rows: list[dict[str, object]] = []
    below: set[Word] = set()
    for depth in (1, 2, 3):
        tapes = realized_tapes(depth, F, fuel)
        rows.append({
            "entries_read": depth,
            "window": depth + 1,
            "tapes_realised": len(tapes),
            "every_tape_meets_this_ceiling": all(functional(depth, tape) for tape in tapes),
            "tapes_breaking_the_ceiling_below": sorted(
                list(tape) for tape in tapes if depth > 1 and not functional(depth - 1, tape)),
            "strictly_more_than_the_depth_below": depth > 1 and bool(tapes - below),
            "tapes_the_depth_below_cannot_realise": sorted(list(tape) for tape in tapes - below)
            if depth > 1 else [],
        })
        below = tapes
    return rows
