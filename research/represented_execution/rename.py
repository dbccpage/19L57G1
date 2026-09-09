"""Renaming the carrier: the machine does not read the names of the data.

AuthorityEffect: None.  Configuration status: DECLARED_HOST_CONFIG, as for
``control``: nothing here is a new machine.

Mirrors ``lean/Rename.lean``.  A datum is a number here only because
something had to be written down.  A *renaming* is a permutation of the
carrier; it carries a finite setting to a renamed one (every operation
conjugated, every store read through the inverse, the endpoints moved), a
controlled setting to a renamed one, and a run to the renamed run.

The Lean proves the correspondence for every controlled setting, every
renaming and every start (``Rename.rename_run``, ``rename_tape``).  What this
module adds is the sweep: over every permutation of a small carrier and every
deterministic program on it, that the renamed run ends at the same terminal,
with the same clock and fuel, at the renamed datum and with the renamed
record.  The failure case is kept beside it: a map that is not a permutation
has no inverse on the carrier, and ``renaming`` refuses it by name rather
than producing a setting whose operations are not the conjugates of anything.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from typing import Sequence

import control as ct
import translation as tr
from execution import ExecutionError

Word = tuple[int, ...]


@dataclass(frozen=True)
class Renaming:
    """A permutation of ``range(n)``, given as the table of its values, with
    the inverse computed and checked rather than supplied."""

    n: int
    fwd: Word

    def __post_init__(self) -> None:
        if self.n < 1:
            raise ExecutionError("the carrier is empty")
        if len(self.fwd) != self.n:
            raise ExecutionError("a renaming names every datum exactly once")
        if sorted(self.fwd) != list(range(self.n)):
            raise ExecutionError("a renaming has a two-sided inverse; this map has none")

    @property
    def bwd(self) -> Word:
        inverse = [0] * self.n
        for x, y in enumerate(self.fwd):
            inverse[y] = x
        return tuple(inverse)


def identity(n: int) -> Renaming:
    return Renaming(n, tuple(range(n)))


def rename_table(sigma: Renaming, table: Word) -> Word:
    """The conjugate of an operation: undo the renaming, apply, redo it."""
    bwd = sigma.bwd
    return tuple(sigma.fwd[table[bwd[x]]] for x in range(sigma.n))


def rename_pairs(sigma: Renaming, store: frozenset[tuple[int, int]]) -> frozenset[tuple[int, int]]:
    return frozenset((sigma.fwd[x], sigma.fwd[y]) for x, y in store)


def rename_setting(F: tr.FiniteSetting, sigma: Renaming) -> tr.FiniteSetting:
    """The Lean ``renameSetting``."""
    if sigma.n != F.n:
        raise ExecutionError("the renaming is of another carrier")
    return tr.FiniteSetting(
        F.n, rename_pairs(sigma, F.rel), rename_pairs(sigma, F.ret), rename_pairs(sigma, F.prot),
        sigma.fwd[F.a], sigma.fwd[F.b], tuple(rename_table(sigma, g) for g in F.ops))


def rename_controlled(C: ct.Controlled, sigma: Renaming) -> ct.Controlled:
    """The Lean ``renameControlled``: the enablement read through the inverse."""
    return ct.Controlled(rename_setting(C.F, sigma),
                         frozenset((sigma.fwd[x], k) for x, k in C.ctrl))


def rename_word(sigma: Renaming, tape: Sequence[int]) -> Word:
    """A record, renamed."""
    return tuple(sigma.fwd[x] for x in tape)


def transports(C: ct.Controlled, sigma: Renaming, start: int, fuel: int) -> bool:
    """Whether the renamed run is the renamed run: same terminal, same clock,
    same fuel, the renamed datum and the renamed record.  The mirrored
    theorems are ``Rename.rename_run`` and ``rename_tape``, which prove it of
    every controlled setting, renaming and start rather than of a sweep."""
    terminal, state = ct.trace(C, start, fuel)
    other, renamed = ct.trace(rename_controlled(C, sigma), sigma.fwd[start], fuel)
    return (terminal is other and renamed.clock == state.clock and renamed.fuel == state.fuel
            and renamed.active == sigma.fwd[state.active]
            and renamed.tape == rename_word(sigma, state.tape))


def sweep(F: tr.FiniteSetting, fuel: int) -> dict[str, object]:
    """Every permutation of the carrier against every deterministic program
    on it, from every datum."""
    renamings = [Renaming(F.n, order) for order in permutations(range(F.n))]
    count = len(F.ops)
    programs: list[ct.Controlled] = []
    for choices in _assignments(F.n, count):
        programs.append(ct.Controlled(F, frozenset((x, k) for x, k in choices.items())))
    checked = 0
    for C in programs:
        for sigma in renamings:
            for start in range(F.n):
                if not transports(C, sigma, start, fuel):
                    raise ExecutionError(
                        f"the run of {sorted(C.ctrl)} from {start} does not transport under "
                        f"{sigma.fwd}")
                checked += 1
    return {
        "carrier": F.n,
        "ops_in_index_order": [list(g) for g in F.ops],
        "renamings": len(renamings),
        "programs": len(programs),
        "runs_checked": checked,
        "fuel": fuel,
        "every_run_transports": True,
    }


def _assignments(n: int, count: int) -> list[dict[int, int]]:
    """Every deterministic enablement: at most one operation per datum."""
    out: list[dict[int, int]] = [{}]
    for x in range(n):
        grown: list[dict[int, int]] = []
        for partial in out:
            grown.append(dict(partial))
            for k in range(count):
                extended = dict(partial)
                extended[x] = k
                grown.append(extended)
        out = grown
    return out
