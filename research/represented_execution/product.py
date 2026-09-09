"""Two loci of activity on one carrier, and a run that moves them in turn.

AuthorityEffect: None.  Configuration status: DECLARED_HOST_CONFIG, as for
``control``: nothing here is a new machine.

Mirrors ``lean/Product.lean`` and ``lean/Schedule.lean``.  A product datum
carries a pair: ``pack(m, a, b) = m * a + b``, read back by ``fst_of`` and
``snd_of``.  Two finite settings give a product setting whose operations are
the first setting's acting on the first coordinate (``left_op``) and the
second's acting on the second (``right_op``).  It is an ordinary finite
setting of the merged class, so the merged encoder represents it and the
``control`` interpreter runs it unchanged: two loci are a *datum* here, not a
new machine.

A *schedule* names, at each datum, the one operation enabled there.  It is a
function of the datum, so it is carried by the enablement instances the
machine already reads — the interpreter is told nothing it was not told
before, and never has two operations to choose between.  That is what makes a
two-locus run possible without a host scheduler: the mirrored theorems are
``Schedule.enabledAt_scheduled`` and ``Schedule.scheduled_no_branch``.

The observations this module computes, all of them mirrored by theorems:
one locus moves per step (``Schedule.step_moves_one_locus``); two schedules
that move the loci in opposite orders reach the same datum by different tapes
(``Schedule.square_on_the_outcome``, ``square_fails_on_the_observation``); and
the tape read at one locus, with the repeats dropped, is that locus's own run
(``Schedule.locus1_is_its_own_run``).
"""

from __future__ import annotations

from typing import Callable, Sequence

import control as ct
import translation as tr
from execution import ExecutionError

Table = tuple[int, ...]


# ---------------------------------------------------------------------------
# Packing two loci into one datum
# ---------------------------------------------------------------------------


def pack(m: int, a: int, b: int) -> int:
    """The datum carrying the pair ``(a, b)`` when the second locus has ``m``
    data."""
    if m < 1:
        raise ExecutionError("the second locus is empty")
    return m * a + b


def fst_of(m: int, x: int) -> int:
    """The first locus of a product datum."""
    if m < 1:
        raise ExecutionError("the second locus is empty")
    if x < 0:
        raise ExecutionError("a datum is a count")
    return x // m


def snd_of(m: int, x: int) -> int:
    """The second locus of a product datum."""
    if m < 1:
        raise ExecutionError("the second locus is empty")
    if x < 0:
        raise ExecutionError("a datum is a count")
    return x % m


# ---------------------------------------------------------------------------
# The two families of moves, and the product setting
# ---------------------------------------------------------------------------


def left_op(m: int, n: int, f: Table) -> Table:
    """A move at the first locus: apply ``f`` there, keep the second."""
    return tuple(pack(m, f[fst_of(m, x)], snd_of(m, x)) for x in range(n * m))


def right_op(m: int, n: int, g: Table) -> Table:
    """A move at the second locus: apply ``g`` there, keep the first."""
    return tuple(pack(m, fst_of(m, x), g[snd_of(m, x)]) for x in range(n * m))


def swap_op(m: int, n: int) -> Table:
    """A move that is at neither locus: it exchanges them.  Apparatus for the
    failure case; it is not an operation of any product setting."""
    return tuple(pack(m, snd_of(m, x), fst_of(m, x)) for x in range(n * m))


def prod_setting(F: tr.FiniteSetting, G: tr.FiniteSetting) -> tr.FiniteSetting:
    """The product of two finite settings: the pairs as data, ``F``'s
    operations at the first locus and ``G``'s at the second, no stores, the
    endpoints paired."""
    m, n = G.n, F.n
    ops = tuple(left_op(m, n, f) for f in F.ops) + tuple(right_op(m, n, g) for g in G.ops)
    return tr.FiniteSetting(n * m, tr.NONE, tr.NONE, tr.NONE,
                            pack(m, F.a, G.a), pack(m, F.b, G.b), ops)


# ---------------------------------------------------------------------------
# A schedule carried in the data
# ---------------------------------------------------------------------------


def scheduled(F: tr.FiniteSetting, sched: Callable[[int], int]) -> ct.Controlled:
    """A controlled setting whose program names, at each datum, the one
    operation that fires there."""
    return ct.Controlled(F, frozenset((x, sched(x)) for x in range(F.n)))


def two_locus(F: tr.FiniteSetting, G: tr.FiniteSetting,
              sched: Callable[[int], int]) -> ct.Controlled:
    """The two-locus controlled setting: the product carrier and a schedule."""
    return scheduled(prod_setting(F, G), sched)


# ---------------------------------------------------------------------------
# Reading a tape at one locus
# ---------------------------------------------------------------------------


def locus(m: int, which: int, tape: Sequence[int]) -> tuple[int, ...]:
    """One locus, read off a tape: ``which`` is 0 for the first, 1 for the
    second."""
    if which not in (0, 1):
        raise ExecutionError("there are two loci")
    read = fst_of if which == 0 else snd_of
    return tuple(read(m, x) for x in tape)


def destutter(l: Sequence[int]) -> tuple[int, ...]:
    """Adjacent repeats dropped: what one locus's reading of the tape looks
    like once the steps that moved the *other* locus are forgotten."""
    out: list[int] = []
    for value in l:
        if not out or out[-1] != value:
            out.append(value)
    return tuple(out)


def moves_one_locus(m: int, tape: Sequence[int]) -> bool:
    """Every consecutive pair of the tape leaves one of the two loci where it
    was.  The mirrored theorem is ``Schedule.step_moves_one_locus``, which
    proves it of every step of every two-locus run, from the product's
    operations rather than from this tape."""
    return all(fst_of(m, x) == fst_of(m, y) or snd_of(m, x) == snd_of(m, y)
               for x, y in zip(tape, tape[1:]))
