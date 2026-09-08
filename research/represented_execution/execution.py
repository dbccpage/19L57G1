"""Represented operations drive a process: the configuration machine.

AuthorityEffect: None.  Configuration status: DECLARED_HOST_CONFIG — a
``Config`` is a metatheory record whose ``graph`` field is a copy of the
encoded instances; the process reads encoded data and does not itself live
in the sealed grammar.

Mirrors ``lean/Execution.lean``.  The machine reads the encoded graph — the
instances ``(3 + k, (x, y))`` that the merged encoder gives the ``k``-th
operation — and never the operation tables of the setting: ``lookup``,
``step``, ``iterate``, ``run``, ``eval_word`` and ``resume`` take a graph or
a configuration and nothing else.  Only ``init`` sees a setting, and only
through the merged ``encode``: the encoder produces the represented input,
it is not the machine.  A word is a list of *operation indices*: ``step``
reads the edge of form ``3 + k`` leaving the active datum, where ``k`` is the
head of the word.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import translation as tr
from derivation.model import Inst

Graph = frozenset[Inst]


class ExecutionError(ValueError):
    """A named refusal of the machine."""


@dataclass(frozen=True)
class Config:
    """The Lean ``Config``: the encoded graph, the remaining word, the active
    datum, the output tape of data visited."""

    graph: Graph
    word: tuple[int, ...]
    active: int
    output: tuple[int, ...]


def lookup(f: int, x: int, graph: Graph) -> int | None:
    """The Lean ``lookup``: the value of the edge of form ``f`` leaving ``x``,
    or ``None`` when there is none.  The Lean reads the first such instance
    in list order; a faithful encoding has at most one, so on every encoding
    the two agree.  A graph with two edges leaving ``x`` on one form is not an
    operation graph and is refused by name rather than silently ordered."""
    ys = sorted(args[1] for form, args in graph if form == f and len(args) == 2 and args[0] == x)
    if len(ys) > 1:
        raise ExecutionError(f"form {f} has {len(ys)} edges leaving {x}: not an operation graph")
    return ys[0] if ys else None


def step(c: Config) -> Config | None:
    """One step: consume the head ``k`` of the word by reading the edge of
    form ``3 + k`` leaving the active datum.  No word, or no edge: no step."""
    if not c.word:
        return None
    k, rest = c.word[0], c.word[1:]
    y = lookup(3 + k, c.active, c.graph)
    if y is None:
        return None
    return Config(c.graph, rest, y, c.output + (y,))


def iterate(n: int, c: Config) -> Config | None:
    """Iterate ``step`` ``n`` times; a missing step is a refusal."""
    for _ in range(n):
        nxt = step(c)
        if nxt is None:
            return None
        c = nxt
    return c


def run(c: Config) -> Config | None:
    """``iterate step`` for the length of the word, as the Lean ``run`` is."""
    return iterate(len(c.word), c)


def eval_word(graph: Graph, word: Sequence[int], a: int) -> int | None:
    """The reference fold, reading the same graph through the same lookup."""
    for k in word:
        y = lookup(3 + k, a, graph)
        if y is None:
            return None
        a = y
    return a


def init(F: tr.FiniteSetting, word: Sequence[int], x: int) -> Config:
    """The Lean ``init``: the encoded instances as the graph, a word, a start
    datum, an empty tape.  The one function that sees a setting."""
    if not 0 <= x < F.n:
        raise ExecutionError("the start datum lies outside the carrier")
    return Config(frozenset(tr.encode(F).insts), tuple(word), x, ())


def resume(c: Config, v: Sequence[int]) -> Config | None:
    """Continue a halted configuration on a further word."""
    return run(Config(c.graph, tuple(v), c.active, c.output))


def replace_edge(graph: Graph, f: int, x: int, y: int) -> Graph:
    """The graph with the edge of form ``f`` leaving ``x`` redirected to ``y``:
    the old edge removed, the new one added.  Apparatus for the mutation
    tests; not part of the machine."""
    without = frozenset(i for i in graph if not (i[0] == f and len(i[1]) == 2 and i[1][0] == x))
    return without | {(f, (x, y))}


def remove_edge(graph: Graph, f: int, x: int) -> Graph:
    """The graph without the edge of form ``f`` leaving ``x``.  Apparatus for
    the refusal tests; not part of the machine."""
    return frozenset(i for i in graph if not (i[0] == f and len(i[1]) == 2 and i[1][0] == x))
