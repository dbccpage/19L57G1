"""The judgment grammar, the two derivability bits, and the sealed relation.

Classification: metatheory apparatus computing object-language facts.

Re-implemented against the pinned sealed source ``code/derivation/observe.py``.

The one fact this whole tree turns on is that the sealed relation is an *or*
of two independent bits.  Pinned source, line 56, in full::

    def derivable(r, inst): return inst[0] in r.rules or inst in r.insts

* the **coverage bit** ``A(c)`` says the context's form carries the uniform
  all-tuples rule.  It does not depend on the datum plugged in.
* the **admission bit** ``B(c, d)`` says the plugging is an admitted instance.

``sealed_derivable = A or B``.  Reading the two apart is what a second
observer does, and nothing in the estate does it.
"""

from __future__ import annotations

from itertools import product
from typing import Iterator, Optional

from .regime import Inst, Pair, Regime

Slot = Optional[int]
Context = tuple[int, tuple[Slot, ...]]


def slot_tuples(arity: int, n_data: int) -> Iterator[tuple[Slot, ...]]:
    """All slot tuples of the arity over the data, hole first then data."""
    options: list[Slot] = [None] + list(range(n_data))
    yield from product(options, repeat=arity)


_CONTEXT_CACHE: dict[tuple[tuple[int, ...], int], tuple[Context, ...]] = {}


def contexts(r: Regime) -> tuple[Context, ...]:
    """Every context of the regime, deterministically ordered.

    A total function of ``(r.forms, r.n_data())`` and of nothing else — which
    is exactly why it is safe to memoise on that pair."""
    key = (r.forms, r.n_data())
    hit = _CONTEXT_CACHE.get(key)
    if hit is not None:
        return hit
    out: list[Context] = []
    for f, arity in enumerate(r.forms):
        for slots in slot_tuples(arity, r.n_data()):
            if any(s is None for s in slots):
                out.append((f, slots))
    _CONTEXT_CACHE[key] = tuple(out)
    return _CONTEXT_CACHE[key]


def plug(c: Context, d: int) -> Inst:
    f, slots = c
    return (f, tuple(d if s is None else s for s in slots))


def coverage_bit(r: Regime, c: Context) -> bool:
    """``A``: the context's form carries the uniform rule.  Datum-independent
    by construction, which is why a covered context is invisible to the
    sealed relation."""
    return c[0] in r.rules


def admission_bit(r: Regime, c: Context, d: int) -> bool:
    """``B``: the plugging of ``d`` into ``c`` is an admitted instance."""
    return plug(c, d) in r.insts


def sealed_derivable(r: Regime, inst: Inst) -> bool:
    """The sealed relation, re-implemented: coverage or admission."""
    return inst[0] in r.rules or inst in r.insts


def profile(r: Regime, d: int) -> frozenset[Context]:
    return frozenset(c for c in contexts(r) if sealed_derivable(r, plug(c, d)))


_PROFILE_CACHE: dict[Regime, tuple[frozenset[Context], ...]] = {}


def profiles(r: Regime) -> tuple[frozenset[Context], ...]:
    """Memoised on the regime, which is frozen and is the function's whole
    input.  The cache changes nothing about what is computed; it exists
    because many candidates share one regime."""
    hit = _PROFILE_CACHE.get(r)
    if hit is not None:
        return hit
    ctxs = contexts(r)
    out = tuple(
        frozenset(c for c in ctxs if sealed_derivable(r, plug(c, d)))
        for d in range(r.n_data())
    )
    _PROFILE_CACHE[r] = out
    return out


def data_pairs(n: int) -> tuple[Pair, ...]:
    return tuple((i, j) for i in range(n) for j in range(i + 1, n))


_RELATION_CACHE: dict[Regime, frozenset[Pair]] = {}


def sealed_relation(r: Regime) -> frozenset[Pair]:
    """The pairs the sealed observer separates: profiles differ.  Memoised on
    the regime for the same reason as ``profiles``."""
    hit = _RELATION_CACHE.get(r)
    if hit is not None:
        return hit
    profs = profiles(r)
    out = frozenset(
        (i, j) for (i, j) in data_pairs(r.n_data()) if profs[i] != profs[j]
    )
    _RELATION_CACHE[r] = out
    return out


def collapsed_pairs(r: Regime) -> tuple[Pair, ...]:
    """Pairs the sealed observer identifies, lexicographically ordered."""
    sep = sealed_relation(r)
    return tuple(p for p in data_pairs(r.n_data()) if p not in sep)
