"""The record read: an enablement that reads the retained record.

AuthorityEffect: None.  Configuration status: DECLARED_HOST_CONFIG — the
state is the represented execution family's ``State``, a metatheory record
carrying encoded instances.

Mirrors ``lean/Record.lean``.  A recorded setting adds an enablement
relation ``(p, x, k)``: operation ``k`` may fire at the active datum ``x``
when the datum before it on the record is ``p``.  It is represented in the
same device as the merged control machine — one binary form per operation
— by the instance ``(3 + nops + k, (p, x))`` instead of the self-instance
``(3 + nops + k, (x, x))``, so the program is again a regime of the sealed
grammar (``encode_r``, the sealed replay of ``events_r``).  The interpreter
is the merged one with one change: before reading the edge it reads the
record.  ``previous`` is the entry before the last on the tape (the start
is its own predecessor), ``renabled`` is the presence of the instance
``(3 + nops + k, (previous, active))``, and ``fire`` is the merged ``fire``
unchanged.  ``rrun`` fires the one enabled operation and stops with
``BRANCH`` when two are — it never selects.

``rprogram`` is computed directly as the set of instances the sealed replay
produces beyond the stores; ``tests/test_record.py`` checks the two agree on
every named program, every lifted memoryless program and a declared sample
of the record class, so the class enumeration in ``selection.py`` need not
replay the sealed engine a quarter of a million times.

A record program is **not an operation graph on its control forms**: several
instances of one control form may leave one record entry, which is what makes
the read a relation.  The merged memoryless reader — ``control.enabled``,
``control.enabled_at``, ``control.step_det`` and the observation ``limits.obs``
built on them — reads those forms through ``execution.lookup``, which refuses
a form with two edges leaving one datum by name.  It must therefore not be
applied to a record program; ``selection.py`` dispatches on the law's type,
and ``tests/test_record.py`` pins the refusal.
"""

from __future__ import annotations

from dataclasses import dataclass

import control as ct
import runner as rn
import translation as tr
from derivation.model import AdmitForm, AdmitInst, Event, Regime, replay
from execution import ExecutionError, Graph, lookup

RecordEnablement = frozenset[tuple[int, int, int]]
Word = tuple[int, ...]


# ---------------------------------------------------------------------------
# Recorded settings, the represented program, the reference step
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Recorded:
    """A finite setting with a record-reading enablement relation
    ``(previous, active, k)``."""

    F: tr.FiniteSetting
    hctrl: RecordEnablement

    def __post_init__(self) -> None:
        count = len(self.F.ops)
        for p, x, k in self.hctrl:
            if not (0 <= p < self.F.n and 0 <= x < self.F.n and 0 <= k < count):
                raise ExecutionError(f"record enablement ({p}, {x}, {k}) lies outside the setting")


def nops(C: Recorded) -> int:
    """The operation count, read as the shape of the merged encoding."""
    return len(tr.encode(C.F).forms) - 3


def ctrl_form(C: Recorded, k: int) -> int:
    return 3 + len(C.F.ops) + k


def rstep(C: Recorded, p: int, x: int, k: int, y: int) -> bool:
    """The reference step, stated on the setting before any encoding: with
    ``p`` on the record before ``x``, ``k`` is enabled and ``y`` is its value
    at ``x``.  A *check* the tests and the receipt use; the machine never
    calls it."""
    return k < len(C.F.ops) and (p, x, k) in C.hctrl and y == tr.run(C.F, (k,), x)


def events_r(C: Recorded) -> tuple[Event, ...]:
    """The admission history of the recorded regime: the merged encoder's
    events, one more binary form per operation, and the record enablements
    as instances ``(previous, active)`` on those forms."""
    out: list[Event] = list(tr.events(C.F))
    out.extend(AdmitForm(2) for _ in range(len(C.F.ops)))
    out.extend(AdmitInst(ctrl_form(C, k), (p, x)) for p, x, k in sorted(C.hctrl))
    return tuple(out)


def encode_r(C: Recorded) -> Regime:
    """The Lean ``encodeR``, as the sealed replay of ``events_r``."""
    return replay(events_r(C))


def rprogram(C: Recorded) -> Graph:
    """The Lean ``rprogram``: the operation graphs and the record
    enablements — the instances of the recorded regime on the forms beyond
    the stores.  Computed directly; ``test_record.py`` checks it against the
    sealed replay."""
    edges = {(3 + k, (x, g[x])) for k, g in enumerate(C.F.ops) for x in range(C.F.n)}
    records = {(ctrl_form(C, k), (p, x)) for p, x, k in C.hctrl}
    return frozenset(edges | records)


def rprogram_by_replay(C: Recorded) -> Graph:
    return frozenset(i for i in encode_r(C).insts if i[0] >= 3)


# ---------------------------------------------------------------------------
# Reading the record, and the interpreter
# ---------------------------------------------------------------------------


def present(f: int, p: int, x: int, g: Graph) -> bool:
    """Whether the instance ``(f, (p, x))`` is present: a relation is read,
    not a function."""
    return (f, (p, x)) in g


def renabled(g: Graph, count: int, p: int, x: int, k: int) -> bool:
    return present(3 + count + k, p, x, g)


def renabled_at(g: Graph, count: int, p: int, x: int) -> tuple[int, ...]:
    """The operations enabled at ``x`` after ``p``, in index order.  Nothing
    reads its first element as a choice."""
    return tuple(k for k in range(count) if renabled(g, count, p, x, k))


def previous(s: ct.State) -> int:
    """The datum before the last on the record; a record of one entry has
    that entry as its own predecessor."""
    return s.tape[-2] if len(s.tape) >= 2 else s.active


def synced(s: ct.State) -> bool:
    return len(s.tape) >= 1 and s.tape[-1] == s.active


def rsuccessors(s: ct.State) -> tuple[ct.State, ...]:
    out: list[ct.State] = []
    for k in renabled_at(s.graph, s.nops, previous(s), s.active):
        fired = ct.fire(s, k)
        if isinstance(fired, ct.State):
            out.append(fired)
    return tuple(out)


def record_reader(s: ct.State) -> tuple[int, ...]:
    """What the record-reading machine reads: the enablements at the active
    datum after the one before it on the record.  The Lean
    ``Record.recordReader``, and a function of the *state* — which is what
    makes this machine the generic interpreter at a reader rather than a
    fourth copy of it (``Record.rstepDet_is_generic``)."""
    return renabled_at(s.graph, s.nops, previous(s), s.active)


def rstep_det(s: ct.State) -> ct.Terminal | ct.State:
    """The Lean ``rstepDet``, which is ``Runner.stepDetOf`` at this reader —
    by ``rfl`` there and by delegation here.  The body this replaced was
    ``control.step_det`` with the key swapped, and it carried a divergence the
    delegation removes: it stopped on ``bound == 0`` where the merged runner
    stops on ``bound <= 0``, so a hand-built state with negative fuel looped."""
    return rn.step_det_of(record_reader, s)


def rrun_det(bound: int, s: ct.State) -> tuple[ct.Terminal, ct.State]:
    return rn.run_det_of(record_reader, bound, s)


def rrun(s: ct.State) -> tuple[ct.Terminal, ct.State]:
    return rrun_det(s.fuel, s)


def rinit(C: Recorded, x: int, fuel: int) -> ct.State:
    """The Lean ``rinit``: the program, a start datum, the start on the
    record, clock zero, a declared fuel."""
    if not 0 <= x < C.F.n:
        raise ExecutionError("the start datum lies outside the carrier")
    if fuel < 0:
        raise ExecutionError("fuel is a count")
    return ct.State(rprogram(C), len(C.F.ops), x, (x,), 0, fuel)


def rtrace(C: Recorded, x: int, fuel: int) -> tuple[ct.Terminal, ct.State]:
    return rrun(rinit(C, x, fuel))


def rnext(s: ct.State) -> ct.State:
    """One step of the runner; a terminal keeps the state."""
    return rn.next_of(record_reader, s)


def riter(n: int, s: ct.State) -> ct.State:
    if n < 0:
        raise ExecutionError("a scale is a count")
    return rn.iter_of(record_reader, n, s)


def robs(n: int, s: ct.State) -> Word:
    """The observation at scale ``n``: the record after ``n`` steps."""
    return riter(n, s).tape


# ---------------------------------------------------------------------------
# The memoryless class embeds; the record forgotten
# ---------------------------------------------------------------------------


def lift(C: ct.Controlled) -> Recorded:
    """A controlled setting read as a recorded one: the enablement ignores
    the record (one instance per admitted record entry)."""
    return Recorded(C.F, frozenset((p, x, k) for p in range(C.F.n) for x, k in C.ctrl))


def forget(C: Recorded) -> ct.Controlled:
    """A recorded setting read as a controlled one: the record is forgotten
    and the enablement is read at the datum as its own predecessor."""
    return ct.Controlled(C.F, frozenset((x, k) for p, x, k in C.hctrl if p == x))


# ---------------------------------------------------------------------------
# The named programs on the observed family's setting
# ---------------------------------------------------------------------------

# The transcribed setting of the coherent process limits family (its Lean
# ``Observe.base``): the cycle, the constant map, the climb — in index order.
BASE_TABLES: tuple[Word, ...] = ((1, 2, 0), (0, 0, 0), (1, 2, 2))

# The cycle at 0 after 0, the constant map at 1 after 0, the constant map at
# 0 after 1: the run from 0 visits 0, 1, 0, 0 (the Lean ``twist``).
TWIST: RecordEnablement = frozenset({(0, 0, 0), (0, 1, 1), (1, 0, 1)})


def twist(F: tr.FiniteSetting) -> Recorded:
    return Recorded(F, TWIST)


def turncoat(F: tr.FiniteSetting) -> Recorded:
    """The cycle everywhere except after 2 at datum 0, where the constant map
    fires (the Lean ``Select.turncoat``)."""
    return Recorded(F, frozenset((p, x, 1 if (p, x) == (2, 0) else 0)
                                 for p in range(F.n) for x in range(F.n)))


def check_base(F: tr.FiniteSetting) -> None:
    """Refuse a setting whose operation tables, in index order, are not the
    transcribed ones the Lean programs are stated on."""
    if F.n != 3 or tuple(F.ops) != BASE_TABLES:
        raise ExecutionError(f"the identified setting {F.ops} is not the transcribed base {BASE_TABLES}")
