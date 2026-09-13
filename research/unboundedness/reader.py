"""A reader that reads the retained record beside the active datum.

AuthorityEffect: None. Configuration status: DECLARED_HOST_CONFIG.

Mirrors lean/Reader.lean. The machine reads the previous datum from the
tape beside the active one. Enablement is represented as a binary form with
instances (3 + nops + k, (p, x)), where p is the previous datum from the
tape and x is the active datum. When the tape has length at least 2, the machine reads [previous, active]
from the tape; on a record of length 1, it reads [active, active], matching
the self-instance start convention. History-dependence claims are inhabited
only for `len(tape) >= 2`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import control as ct
import translation as tr
from derivation.model import AdmitForm, AdmitInst, Event, Regime, replay
from execution import ExecutionError, Graph

RecordEnablement = frozenset[tuple[int, int, int]]


@dataclass(frozen=True)
class Recorded:
    """A finite setting with a record-reading enablement relation (p, x, k).

    AuthorityEffect: None.
    """

    F: tr.FiniteSetting
    hctrl: RecordEnablement
    _nops: int = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_nops", len(tr.encode(self.F).forms) - 3)
        count = self._nops
        for p, x, k in self.hctrl:
            if not (0 <= p < self.F.n and 0 <= x < self.F.n and 0 <= k < count):
                raise ExecutionError(f"record enablement ({p}, {x}, {k}) lies outside the setting")


def nops(C: Recorded) -> int:
    """The operation count, read as the shape of the merged encoding.

    The Lean uses ``C.F.ops.length`` instead. The two coincide on a faithful
    encoder; ``tests/test_reader.py`` checks the identity on the settings
    this tree builds. Cached on the frozen dataclass so encode is not
    re-run from every call site.

    AuthorityEffect: None.
    """
    return C._nops


def ctrl_form(C: Recorded, k: int) -> int:
    """The control form of operation k.

    AuthorityEffect: None.
    """
    return 3 + nops(C) + k


def rstep(C: Recorded, p: int, x: int, k: int, y: int) -> bool:
    """The reference step: with p before x on the tape, operation k is enabled
    and moves to y.

    AuthorityEffect: None.
    """
    return k < nops(C) and (p, x, k) in C.hctrl and y == tr.run(C.F, (k,), x)


def events_r(C: Recorded) -> tuple[Event, ...]:
    """The admission history of the recorded regime: one more binary form per
    operation, and the enablements as instances (ctrl_form, (p, x)).

    AuthorityEffect: None.
    """
    out: list[Event] = list(tr.events(C.F))
    out.extend(AdmitForm(2) for _ in range(nops(C)))
    out.extend(AdmitInst(ctrl_form(C, k), (p, x)) for p, x, k in sorted(C.hctrl))
    return tuple(out)


def encode_r(C: Recorded) -> Regime:
    """The recorded regime as replay of events_r.

    AuthorityEffect: None.
    """
    return replay(events_r(C))


def rprogram(C: Recorded) -> Graph:
    """The operation graphs and record enablements.

    AuthorityEffect: None.
    """
    return frozenset(i for i in encode_r(C).insts if i[0] >= 3)


def previous(s: ct.State) -> int:
    """The datum before the active datum on the tape.

    AuthorityEffect: None. When the tape has length at least 2, returns the
    second-to-last datum. On a tape of length 1, returns the active datum.
    """
    if len(s.tape) >= 2:
        return s.tape[-2]
    return s.active


def present(f: int, p: int, x: int, g: Graph) -> bool:
    """Whether instance (f, (p, x)) is in graph g.

    AuthorityEffect: None.
    """
    return (f, (p, x)) in g


def renabled(g: Graph, count: int, p: int, x: int, k: int) -> bool:
    """Operation k is enabled at active x following previous p.

    AuthorityEffect: None.
    """
    return present(3 + count + k, p, x, g)


def renabled_at(g: Graph, count: int, p: int, x: int) -> tuple[int, ...]:
    """Enabled operations in index order.

    AuthorityEffect: None.
    """
    return tuple(k for k in range(count) if renabled(g, count, p, x, k))


def record_reader(s: ct.State) -> tuple[int, ...]:
    """The reader consulting [previous, active] from the state tape.

    AuthorityEffect: None.
    """
    return renabled_at(s.graph, s.nops, previous(s), s.active)


def rsuccessors(s: ct.State) -> list[ct.State]:
    """Successors under the record reader.

    AuthorityEffect: None.
    """
    out: list[ct.State] = []
    for k in record_reader(s):
        fired = ct.fire(s, k)
        if isinstance(fired, ct.State):
            out.append(fired)
    return out


def rinit(C: Recorded, x: int, fuel: int) -> ct.State:
    """Initial state for a recorded setting.

    AuthorityEffect: None.
    """
    return ct.State(rprogram(C), nops(C), x, (x,), 0, fuel)
