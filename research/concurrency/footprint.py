"""Operational footprints and derived interaction dependency graph.

Derives interaction dependency graphs directly from read/write access footprints
without background spatial metrics or coordinate embeddings.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Iterable, Set, Tuple

from carrier import State3


class Locus(str, Enum):
    """Loci of the three-locus carrier."""

    L1 = "L1"
    L2 = "L2"
    M = "M"


@dataclass(frozen=True)
class Footprint:
    """Read and write footprints over loci {L1, L2, M}."""

    r1: bool
    r2: bool
    rm: bool
    w1: bool
    w2: bool
    wm: bool

    @classmethod
    def from_loci(
        cls, reads: Iterable[Locus] | None = None, writes: Iterable[Locus] | None = None
    ) -> Footprint:
        """Construct footprint from sets/iterables of read and written loci."""
        r_set = set(reads or [])
        w_set = set(writes or [])
        return cls(
            r1=Locus.L1 in r_set,
            r2=Locus.L2 in r_set,
            rm=Locus.M in r_set,
            w1=Locus.L1 in w_set,
            w2=Locus.L2 in w_set,
            wm=Locus.M in w_set,
        )

    @property
    def reads(self) -> Set[Locus]:
        """Set of loci read by this footprint."""
        res: set[Locus] = set()
        if self.r1:
            res.add(Locus.L1)
        if self.r2:
            res.add(Locus.L2)
        if self.rm:
            res.add(Locus.M)
        return res

    @property
    def writes(self) -> Set[Locus]:
        """Set of loci written by this footprint."""
        res: set[Locus] = set()
        if self.w1:
            res.add(Locus.L1)
        if self.w2:
            res.add(Locus.L2)
        if self.wm:
            res.add(Locus.M)
        return res


def locus_interferes(w_a: bool, r_a: bool, w_b: bool, r_b: bool) -> bool:
    """Check Bernstein conflict condition on a single locus.

    Conflict occurs if one writes and the other reads or writes.
    """
    return (w_a and (r_b or w_b)) or (w_b and (r_a or w_a))


def interferes(f1: Footprint, f2: Footprint) -> bool:
    """Check if two footprints interfere on any locus."""
    return (
        locus_interferes(f1.w1, f1.r1, f2.w1, f2.r1)
        or locus_interferes(f1.w2, f1.r2, f2.w2, f2.r2)
        or locus_interferes(f1.wm, f1.rm, f2.wm, f2.rm)
    )


def is_disjoint(f1: Footprint, f2: Footprint) -> bool:
    """Two footprints are disjoint iff they do not interfere on any locus."""
    return not interferes(f1, f2)


# Predefined canonical footprints
FP_L1 = Footprint.from_loci(reads=[Locus.L1], writes=[Locus.L1])
FP_L2 = Footprint.from_loci(reads=[Locus.L2], writes=[Locus.L2])
FP_M = Footprint.from_loci(reads=[Locus.M], writes=[Locus.M])

FP_READ_M_WRITE_L1 = Footprint.from_loci(reads=[Locus.M], writes=[Locus.L1])
FP_READ_M_WRITE_L2 = Footprint.from_loci(reads=[Locus.M], writes=[Locus.L2])
FP_READ_L1_WRITE_M = Footprint.from_loci(reads=[Locus.L1], writes=[Locus.M])


@dataclass
class OperationRecord:
    """An operation accompanied by its declared access footprint and implementation."""

    name: str
    footprint: Footprint
    apply: Callable[[State3], State3]


class DependencyGraph:
    """Interaction dependency graph derived solely from access footprints.

    No spatial metric or coordinate embedding is assumed.
    """

    def __init__(self, operations: list[OperationRecord]) -> None:
        self.operations = operations
        self.names = [op.name for op in operations]
        self._by_name = {op.name: op for op in operations}

        # Derive edges strictly from access overlaps (conflict)
        self.edges: list[Tuple[str, str]] = []
        for i in range(len(operations)):
            for j in range(i + 1, len(operations)):
                op_i = operations[i]
                op_j = operations[j]
                if interferes(op_i.footprint, op_j.footprint):
                    self.edges.append((op_i.name, op_j.name))

    def has_edge(self, u: str, v: str) -> bool:
        """Check if an interaction dependency edge exists between two operations."""
        return (u, v) in self.edges or (v, u) in self.edges

    def neighbors(self, u: str) -> list[str]:
        """Return all operations dependent on u."""
        res: list[str] = []
        for a, b in self.edges:
            if a == u:
                res.append(b)
            elif b == u:
                res.append(a)
        return sorted(res)

    def independent_pairs(self) -> list[Tuple[str, str]]:
        """Return all unordered pairs of operations that are independent (disjoint)."""
        pairs: list[Tuple[str, str]] = []
        for i in range(len(self.operations)):
            for j in range(i + 1, len(self.operations)):
                u = self.names[i]
                v = self.names[j]
                if not self.has_edge(u, v):
                    pairs.append((u, v))
        return pairs

    def interfering_pairs(self) -> list[Tuple[str, str]]:
        """Return all unordered pairs of operations that interfere."""
        return list(self.edges)
