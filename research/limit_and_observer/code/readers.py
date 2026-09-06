"""The admitted reader: selection, reading, aggregation, and lawfulness.

Classification: admitted primitive of this rung (the triple and its two
admission events); derived definition (the induced relation); deterministic
computation (the lawfulness decision and every census below).

A reader reads only *through* the judgment grammar.  It is a function of the
reading applied to the bit pair at each context of its selection, and of
nothing else.  It never names a datum by index, and two tests enforce that:
its verdict is invariant under any relabelling of data preserving the regime,
and it cannot separate two data whose bit signatures agree at every context.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Iterator

from .grammar import Context, admission_bit, coverage_bit, data_pairs
from .regime import Pair, Regime

# A reading is the value table of ``b : Bool x Bool -> Bool`` at the bit pairs
# (A, B) in the order (FF, FT, TF, TT).
Reading = tuple[bool, bool, bool, bool]
BIT_PAIRS: tuple[tuple[bool, bool], ...] = (
    (False, False),
    (False, True),
    (True, False),
    (True, True),
)
ALL_READINGS: tuple[Reading, ...] = tuple(
    (v[0], v[1], v[2], v[3])
    for v in itertools.product((False, True), repeat=4)
)

# The sealed relation as a reading: A or B.
SEALED_READING: Reading = (False, True, True, True)
# The reading that declines the conflation: B alone.
ADMISSION_ONLY_READING: Reading = (False, True, False, True)

Aggregation = tuple[bool, ...]

#: The four induced-separation behaviours.  A behaviour is the pair
#: (the reading varies with the admission bit where coverage is absent,
#:  the reading varies with the admission bit where coverage is present).
BLIND = (False, False)
UNCOVERED = (True, False)
COVERED = (False, True)
EITHER = (True, True)
BEHAVIOURS: tuple[tuple[bool, bool], ...] = (BLIND, UNCOVERED, COVERED, EITHER)
BEHAVIOUR_NAMES: dict[tuple[bool, bool], str] = {
    BLIND: "blind",
    UNCOVERED: "uncovered",
    COVERED: "covered",
    EITHER: "either",
}


def complement(b: Reading) -> Reading:
    return (not b[0], not b[1], not b[2], not b[3])


def reading_class(b: Reading) -> Reading:
    """Canonical representative of the complement class of a reading.

    Separation is "the bit differs", so a reading and its complement induce
    the same separation everywhere and are one class."""
    return min(b, complement(b))


def behaviour(b: Reading) -> tuple[bool, bool]:
    """The induced-separation behaviour of a reading.

    At a fixed context the coverage bit is constant across data, so the
    reading either varies with the admission bit there or is constant there.
    The induced relation depends on the reading only through this pair."""
    return (b[0] != b[1], b[2] != b[3])


def reads_at(b: Reading, covered: bool) -> bool:
    """Whether the reading separates at a context with the given coverage."""
    return behaviour(b)[1] if covered else behaviour(b)[0]


def all_reading_classes() -> tuple[Reading, ...]:
    return tuple(sorted({reading_class(b) for b in ALL_READINGS}))


def non_constant_reading_classes() -> tuple[Reading, ...]:
    return tuple(
        c for c in all_reading_classes() if len(set(c)) != 1
    )


def all_aggregations(w_max: int) -> tuple[Aggregation, ...]:
    """Every total ``a : {0..w_max} -> Bool`` with ``a(0) = false``."""
    return tuple(
        (False,) + rest
        for rest in itertools.product((False, True), repeat=w_max)
    )


def lawful(a: Aggregation, w_max: int) -> bool:
    """Whether the induced non-separation relation is transitive over the
    whole of ``{0,1}^w`` — lawful *in general*, not merely at one state.

    ``DiffObs`` carries its equivalence laws as fields, so an observer is
    admitted only together with its proofs.  An unlawful aggregation induces
    no partition, so no class count is defined for it and no chain bound
    transports to it."""
    space = tuple(itertools.product((0, 1), repeat=w_max))

    def dist(u: tuple[int, ...], v: tuple[int, ...]) -> int:
        return sum(1 for k in range(w_max) if u[k] != v[k])

    for x in space:
        for y in space:
            if a[dist(x, y)]:
                continue
            for z in space:
                if not a[dist(y, z)] and a[dist(x, z)]:
                    return False
    return True


_LAWFUL_CACHE: dict[int, tuple[Aggregation, ...]] = {}


def lawful_aggregations(w_max: int) -> tuple[Aggregation, ...]:
    """Memoised: lawfulness is decided once per width, not once per call."""
    hit = _LAWFUL_CACHE.get(w_max)
    if hit is None:
        hit = tuple(a for a in all_aggregations(w_max) if lawful(a, w_max))
        _LAWFUL_CACHE[w_max] = hit
    return hit


def monotone_aggregations(w_max: int) -> tuple[Aggregation, ...]:
    """The lawful aggregations whose induced block count never falls when a
    context is added.

    This is **not** all of them, and the difference is load-bearing.  Adding a
    context can raise the separating count past a threshold and back out of
    it: under the parity aggregation two data separated at one context are
    identified once a second context also tells them apart.  Measured at width
    3: 2 of the 4 lawful aggregations are monotone (the blind one and
    'at least one separating context'); the other two are not, and
    tests/test_obstructions.py carries the countermodel.

    Consequence for the refinement obstruction: the block-count proof covers
    the monotone aggregations only.  For the other two the bound is a bounded
    computation over the declared population, and is reported as one."""
    out = []
    for a in lawful_aggregations(w_max):
        if all(
            not a[s] or a[s + 1] or s + 1 > w_max
            for s in range(w_max)
        ) and all(
            a[s] <= a[s + 1] for s in range(w_max)
        ):
            out.append(a)
    return tuple(out)


def unlawful_aggregations(w_max: int) -> tuple[Aggregation, ...]:
    """Refused by name, counted and reported — a named boundary, never a
    silent exclusion."""
    return tuple(a for a in all_aggregations(w_max) if not lawful(a, w_max))


@dataclass(frozen=True)
class Reader:
    """An admitted reader ``(K, b, a)``.

    ``selection`` is a tuple of contexts of the current regime, ``reading`` a
    total function of the bit pair, ``aggregation`` a total function of the
    count of separating contexts with ``a(0) = false``."""

    selection: tuple[Context, ...]
    reading: Reading
    aggregation: Aggregation

    def width(self) -> int:
        return len(self.selection)


def signature(r: Regime, reader: Reader, d: int) -> tuple[bool, ...]:
    """The reader's reading of one datum at each context of its selection."""
    return tuple(
        reads_at(reader.reading, coverage_bit(r, c))
        and admission_bit(r, c, d)
        for c in reader.selection
    )


def separating_count(r: Regime, reader: Reader, i: int, j: int) -> int:
    """``s``: contexts of the selection at which the reading differs."""
    si, sj = signature(r, reader, i), signature(r, reader, j)
    return sum(1 for k in range(len(si)) if si[k] != sj[k])


def separates(r: Regime, reader: Reader, i: int, j: int) -> bool:
    s = separating_count(r, reader, i, j)
    if s >= len(reader.aggregation):
        raise ValueError(
            f"separating count {s} exceeds the declared aggregation width"
        )
    return reader.aggregation[s]


def induced_relation(r: Regime, reader: Reader) -> frozenset[Pair]:
    """The pairs the reader separates at this regime."""
    return frozenset(
        (i, j)
        for (i, j) in data_pairs(r.n_data())
        if separates(r, reader, i, j)
    )


def induced_blocks(r: Regime, reader: Reader) -> int:
    """The number of blocks of the reader's induced partition.

    Defined only for a lawful reader; the caller decides lawfulness."""
    rel = induced_relation(r, reader)
    n = r.n_data()
    block: list[int] = list(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) not in rel and block[j] != block[i]:
                old, new = block[j], block[i]
                block = [new if b == old else b for b in block]
    return len(set(block))


def state_lawful(r: Regime, reader: Reader) -> bool:
    """Whether the reader's non-separation relation is transitive *at this
    state*.  Reported as its own class: state-lawful is weaker than lawful in
    general and must never be mistaken for it."""
    rel = induced_relation(r, reader)
    n = r.n_data()
    for i in range(n):
        for j in range(n):
            for k in range(n):
                ij = (min(i, j), max(i, j))
                jk = (min(j, k), max(j, k))
                ik = (min(i, k), max(i, k))
                if i == j or j == k or i == k:
                    continue
                if ij not in rel and jk not in rel and ik in rel:
                    return False
    return True


def full_selection_reader(
    r: Regime, b: Reading, w: int
) -> Reader:
    """A reader over *every* context of the regime.

    Metatheory apparatus, never admitted: its width is unbounded and so it is
    not reachable by any delta.  It exists to state the sealed observer as a
    point of the reader space."""
    from .grammar import contexts as _contexts

    ctx = _contexts(r)
    agg: Aggregation = (False,) + (True,) * max(len(ctx), w)
    return Reader(ctx, b, agg)


def sealed_as_reader(r: Regime) -> Reader:
    """The sealed observation relation, expressed in the reader space.

    Selection: every context.  Reading: the sealed ``A or B``.  Aggregation:
    ``s >= 1``.  Equality with ``grammar.sealed_relation`` is asserted over
    the whole population by test, not by this docstring."""
    return full_selection_reader(r, SEALED_READING, 1)


def iter_readers(
    r: Regime, w: int, w_max: int, lawful_only: bool = True
) -> Iterator[Reader]:
    """Every reader of exactly the given width over the regime's contexts."""
    from .grammar import contexts as _contexts

    if w > w_max:
        return
    ctx = _contexts(r)
    aggs = (
        lawful_aggregations(w_max) if lawful_only else all_aggregations(w_max)
    )
    for sel in itertools.combinations(ctx, w):
        for b in all_reading_classes():
            for a in aggs:
                yield Reader(sel, b, a)
