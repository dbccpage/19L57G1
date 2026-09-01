"""Primitive-difference candidate space: exhaustive finite enumeration.

Classification: metatheory apparatus.  Everything here is deterministic
enumeration over a declared finite universe of *settings*; nothing
assumes the regime model of the earlier development.

A *setting* is ``(n, r, a, b, ret, prot, ops)``: a carrier ``range(n)``
with ``n <= 3``, a relation ``r`` (set of ordered pairs), a designated
pair ``(a, b)``, a retention relation ``ret``, a protection relation
``prot``, and an admitted endofunction family ``ops`` given by function
tables.  The base data ``(n, r, a, b)`` is enumerated exhaustively; the
decorations ``(ret, prot, ops)`` range over a declared list only, and
the exact bounds are recorded in the artifact under ``bounds``:

* ``ret``  in {empty, {(a, b)}}
* ``prot`` in {empty, {(a, b)}}
* ``ops``  in {empty, {identity}, {const_0}}

Candidate readings of primitive difference (predicates on settings),
matching the Lean spec cell for cell:

* ``W``  -- witnessed: ``(a, b) in r``;
* ``A``  -- ``W`` and ``r`` irreflexive;
* ``Bs`` -- ``A`` and ``r`` symmetric;
* ``Bc`` -- ``A`` and ``r`` cotransitive: every asserted pair splits
            every point ``z`` (``(x, z) in r or (z, y) in r``);
* ``Bl`` -- ``A`` and ``r`` located.  In this finite encoded universe
            every relation is a decidable table and decidable relations
            are located (Lean: ``located_of_decidable``), so ``Bl``
            coincides extensionally with ``A`` here; the Prop-level gap
            is metatheoretic and the cells targeting ``Bl`` from
            sources without locatedness stay OPEN (``EXPECTED_OPEN``);
* ``C``  -- ``W`` and ``(a, b) in prot``;
* ``D``  -- metatheoretic inequality ``a != b``;
* ``E``  -- irreducible: no member of the closure of ``ops`` under
            identity and composition identifies ``a`` with ``b``;
* ``F``  -- ``A`` and ``(a, b) in ret`` and ``(a, b) in prot``.

For every ordered pair of distinct candidates the enumerator searches
the whole declared universe for a countermodel and keeps the witness
that is minimal under the declared key ``(n, len(r),
len(ret) + len(prot), len(ops), sorted(r), a, b)`` (ties broken
deterministically by ``(sorted(ret), sorted(prot), sorted(ops))``).
The computed table is cross-checked against ``EXPECTED_MATRIX`` (the
statuses proved on the Lean side); any mismatch raises.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterator, Mapping, Optional, Sequence

Rel = frozenset[tuple[int, int]]
Func = tuple[int, ...]
Partition = tuple[tuple[int, ...], ...]

MAX_N = 3

CANDIDATES: tuple[str, ...] = (
    "W", "A", "Bs", "Bc", "Bl", "C", "D", "E", "F",
)

RET_CHOICES: tuple[str, ...] = ("empty", "designated_pair")
PROT_CHOICES: tuple[str, ...] = ("empty", "designated_pair")
OPS_CHOICES: tuple[str, ...] = ("empty", "identity", "const_0")

BL_NOTE = (
    "In the finite encoded universe every relation is a decidable "
    "table, and a decidable relation is located (Lean: "
    "located_of_decidable), so Bl coincides extensionally with A "
    "here.  The Prop-level gap between A and locatedness is "
    "metatheoretic; the matrix cells from A-implying sources into Bl "
    "are therefore declared OPEN_LOCATED (EXPECTED_OPEN) instead of "
    "being closed by the finite search, which by construction finds "
    "no countermodel for them."
)

A_BC_MINIMALITY = (
    "carrier 3 minimum, cotransitivity automatic at 2 "
    "(Lean cotrans_auto_on_two)"
)


@dataclass(frozen=True)
class Setting:
    """One point of the declared finite universe."""

    n: int
    r: Rel
    a: int
    b: int
    ret: Rel
    prot: Rel
    ops: frozenset[Func]

    def json(self) -> dict[str, object]:
        return {
            "n": self.n,
            "r": [list(p) for p in sorted(self.r)],
            "a": self.a,
            "b": self.b,
            "ret": [list(p) for p in sorted(self.ret)],
            "prot": [list(p) for p in sorted(self.prot)],
            "ops": [list(f) for f in sorted(self.ops)],
        }


def identity_table(n: int) -> Func:
    return tuple(range(n))


def const0_table(n: int) -> Func:
    return tuple(0 for _ in range(n))


def ops_family(choice: str, n: int) -> frozenset[Func]:
    if choice == "empty":
        return frozenset()
    if choice == "identity":
        return frozenset({identity_table(n)})
    if choice == "const_0":
        return frozenset({const0_table(n)})
    raise ValueError(f"unknown ops choice: {choice!r}")


def decoration_rel(choice: str, a: int, b: int) -> Rel:
    if choice == "empty":
        return frozenset()
    if choice == "designated_pair":
        return frozenset({(a, b)})
    raise ValueError(f"unknown decoration choice: {choice!r}")


def enumerate_base(n: int) -> Iterator[tuple[Rel, int, int]]:
    """All ``(r, a, b)`` on the carrier ``range(n)``: relations by bit
    mask over the row-major pair list, then designated points,
    ascending -- a fixed deterministic order."""
    pairs = [(x, y) for x in range(n) for y in range(n)]
    for mask in range(1 << len(pairs)):
        r = frozenset(p for k, p in enumerate(pairs) if mask >> k & 1)
        for a in range(n):
            for b in range(n):
                yield (r, a, b)


def enumerate_settings() -> Iterator[Setting]:
    """The declared finite universe in a fixed deterministic order:
    carriers ascending, base data as in ``enumerate_base``, then the
    declared decoration lists in declared order.  At ``n = 1`` the
    identity and const_0 tables coincide extensionally; enumeration
    items are not deduplicated (recorded in ``bounds``)."""
    for n in range(1, MAX_N + 1):
        for r, a, b in enumerate_base(n):
            for ret_choice in RET_CHOICES:
                for prot_choice in PROT_CHOICES:
                    for ops_choice in OPS_CHOICES:
                        yield Setting(
                            n,
                            r,
                            a,
                            b,
                            decoration_rel(ret_choice, a, b),
                            decoration_rel(prot_choice, a, b),
                            ops_family(ops_choice, n),
                        )


# ---------------------------------------------------------------------------
# Candidate evaluators
# ---------------------------------------------------------------------------


def irreflexive(r: Rel) -> bool:
    return all(x != y for (x, y) in r)


def symmetric(r: Rel) -> bool:
    return all((y, x) in r for (x, y) in r)


def cotransitive(n: int, r: Rel) -> bool:
    """Every asserted pair splits every point: for all ``(x, y)`` in
    ``r`` and all ``z``, ``(x, z)`` in ``r`` or ``(z, y)`` in ``r``."""
    return all(
        (x, z) in r or (z, y) in r for (x, y) in r for z in range(n)
    )


def compose(f: Func, g: Func) -> Func:
    return tuple(f[g[x]] for x in range(len(g)))


def closure(n: int, family: Sequence[Func]) -> frozenset[Func]:
    """Closure of an endofunction family under identity and
    composition: actual function tables, iterated to fixpoint."""
    out: set[Func] = {identity_table(n)} | set(family)
    changed = True
    while changed:
        changed = False
        for f in sorted(out):
            for g in sorted(out):
                h = compose(f, g)
                if h not in out:
                    out.add(h)
                    changed = True
    return frozenset(out)


_CLOSURE_CACHE: dict[tuple[int, frozenset[Func]], frozenset[Func]] = {}


def closure_cached(n: int, ops: frozenset[Func]) -> frozenset[Func]:
    key = (n, ops)
    if key not in _CLOSURE_CACHE:
        _CLOSURE_CACHE[key] = closure(n, sorted(ops))
    return _CLOSURE_CACHE[key]


def evaluate(s: Setting) -> dict[str, bool]:
    """All nine candidate readings on one setting.  ``Bl`` is encoded
    as ``A``: locatedness is automatic on decidable finite relations
    (see ``BL_NOTE``)."""
    w = (s.a, s.b) in s.r
    a = w and irreflexive(s.r)
    return {
        "W": w,
        "A": a,
        "Bs": a and symmetric(s.r),
        "Bc": a and cotransitive(s.n, s.r),
        "Bl": a,
        "C": w and (s.a, s.b) in s.prot,
        "D": s.a != s.b,
        "E": all(
            f[s.a] != f[s.b] for f in closure_cached(s.n, s.ops)
        ),
        "F": a and (s.a, s.b) in s.ret and (s.a, s.b) in s.prot,
    }


# ---------------------------------------------------------------------------
# The implication matrix
# ---------------------------------------------------------------------------

WitnessKey = tuple[
    int,
    int,
    int,
    int,
    tuple[tuple[int, int], ...],
    int,
    int,
    tuple[tuple[int, int], ...],
    tuple[tuple[int, int], ...],
    tuple[Func, ...],
]


def witness_key(s: Setting) -> WitnessKey:
    """The declared minimality key ``(n, len(r), len(ret)+len(prot),
    len(ops), sorted(r), a, b)``; ties broken deterministically by
    ``(sorted(ret), sorted(prot), sorted(ops))``."""
    return (
        s.n,
        len(s.r),
        len(s.ret) + len(s.prot),
        len(s.ops),
        tuple(sorted(s.r)),
        s.a,
        s.b,
        tuple(sorted(s.ret)),
        tuple(sorted(s.prot)),
        tuple(sorted(s.ops)),
    )


def cell_names() -> list[str]:
    return [f"{p}->{q}" for p in CANDIDATES for q in CANDIDATES if p != q]


@dataclass(frozen=True)
class ScanResult:
    """One pass over the declared universe: per-candidate extents, the
    key-minimal countermodel per ordered cell (or ``None``), and the
    sub-bound cotransitivity check for the ``A->Bc`` cell."""

    total: int
    counts: dict[str, int]
    witnesses: dict[str, Optional[Setting]]
    cotrans_violation_le2: bool


def scan_settings() -> ScanResult:
    counts = {name: 0 for name in CANDIDATES}
    witnesses: dict[str, Optional[Setting]] = {
        cell: None for cell in cell_names()
    }
    keys: dict[str, WitnessKey] = {}
    cotrans_violation_le2 = False
    total = 0
    for s in enumerate_settings():
        total += 1
        preds = evaluate(s)
        for name in CANDIDATES:
            if preds[name]:
                counts[name] += 1
        cotrans_violation_le2 = cotrans_violation_le2 or (
            s.n <= 2 and preds["A"] and not preds["Bc"]
        )
        key = witness_key(s)
        for p in CANDIDATES:
            if not preds[p]:
                continue
            for q in CANDIDATES:
                if p == q or preds[q]:
                    continue
                cell = f"{p}->{q}"
                if witnesses[cell] is None or key < keys[cell]:
                    witnesses[cell] = s
                    keys[cell] = key
    return ScanResult(total, counts, witnesses, cotrans_violation_le2)


#: Cells whose Lean status is OPEN: the source implies ``A`` but not
#: locatedness, and the finite universe cannot separate them because
#: every finite decidable relation is located.
EXPECTED_OPEN: frozenset[str] = frozenset(
    {"A->Bl", "Bs->Bl", "Bc->Bl", "F->Bl"}
)

#: The 72 ordered cells with the statuses as computed here AND as
#: proved on the Lean side (tags ``imp_*`` / ``nimp_*`` /
#: ``open_cell_*_bl``); ``matrix_report`` verifies the two agree and
#: raises on any mismatch.
EXPECTED_MATRIX: dict[str, str] = {
    # W: bare witness.  The one-point self-witness (n=1, r={(0,0)},
    # a=b=0) refutes every strengthening at once.
    "W->A": "COUNTERMODEL",
    "W->Bs": "COUNTERMODEL",
    "W->Bc": "COUNTERMODEL",
    "W->Bl": "COUNTERMODEL",
    "W->C": "COUNTERMODEL",
    "W->D": "COUNTERMODEL",
    "W->E": "COUNTERMODEL",
    "W->F": "COUNTERMODEL",
    # A: irreflexive witness.
    "A->W": "IMPLIES",
    "A->Bs": "COUNTERMODEL",  # oriented edge, carrier 2
    "A->Bc": "COUNTERMODEL",  # carrier 3 minimum; automatic at n <= 2
    "A->Bl": "OPEN_LOCATED",
    "A->C": "COUNTERMODEL",
    "A->D": "IMPLIES",
    "A->E": "COUNTERMODEL",  # needs the admitted constant map
    "A->F": "COUNTERMODEL",
    # Bs: symmetric irreflexive witness.
    "Bs->W": "IMPLIES",
    "Bs->A": "IMPLIES",
    "Bs->Bc": "COUNTERMODEL",  # symmetric edge on carrier 3
    "Bs->Bl": "OPEN_LOCATED",
    "Bs->C": "COUNTERMODEL",
    "Bs->D": "IMPLIES",
    "Bs->E": "COUNTERMODEL",
    "Bs->F": "COUNTERMODEL",
    # Bc: cotransitive irreflexive witness.
    "Bc->W": "IMPLIES",
    "Bc->A": "IMPLIES",
    "Bc->Bs": "COUNTERMODEL",  # oriented edge, cotransitive at n = 2
    "Bc->Bl": "OPEN_LOCATED",
    "Bc->C": "COUNTERMODEL",
    "Bc->D": "IMPLIES",
    "Bc->E": "COUNTERMODEL",
    "Bc->F": "COUNTERMODEL",
    # Bl: encoded as A in the finite universe.  Its countermodels are
    # decidable, hence located, hence genuine Bl-countermodels.
    "Bl->W": "IMPLIES",
    "Bl->A": "IMPLIES",
    "Bl->Bs": "COUNTERMODEL",
    "Bl->Bc": "COUNTERMODEL",
    "Bl->C": "COUNTERMODEL",
    "Bl->D": "IMPLIES",
    "Bl->E": "COUNTERMODEL",
    "Bl->F": "COUNTERMODEL",
    # C: protected witness.  The one-point protected self-witness
    # refutes everything except the W projection.
    "C->W": "IMPLIES",
    "C->A": "COUNTERMODEL",  # carrier 1
    "C->Bs": "COUNTERMODEL",
    "C->Bc": "COUNTERMODEL",
    "C->Bl": "COUNTERMODEL",
    "C->D": "COUNTERMODEL",  # carrier 1
    "C->E": "COUNTERMODEL",
    "C->F": "COUNTERMODEL",
    # D: metatheoretic inequality carries no object-level structure.
    "D->W": "COUNTERMODEL",
    "D->A": "COUNTERMODEL",
    "D->Bs": "COUNTERMODEL",
    "D->Bc": "COUNTERMODEL",
    "D->Bl": "COUNTERMODEL",
    "D->C": "COUNTERMODEL",
    "D->E": "COUNTERMODEL",  # needs the admitted constant map
    "D->F": "COUNTERMODEL",
    # E: the closure always contains the identity, so irreducibility
    # contains the identity test and nothing else.
    "E->W": "COUNTERMODEL",
    "E->A": "COUNTERMODEL",
    "E->Bs": "COUNTERMODEL",
    "E->Bc": "COUNTERMODEL",
    "E->Bl": "COUNTERMODEL",
    "E->C": "COUNTERMODEL",
    "E->D": "IMPLIES",
    "E->F": "COUNTERMODEL",
    # F: retained protected irreflexive witness: all conjunction
    # projections hold; the lateral axes still fail.
    "F->W": "IMPLIES",
    "F->A": "IMPLIES",
    "F->Bs": "COUNTERMODEL",
    "F->Bc": "COUNTERMODEL",  # carrier 3, as for A->Bc
    "F->Bl": "OPEN_LOCATED",
    "F->C": "IMPLIES",
    "F->D": "IMPLIES",
    "F->E": "COUNTERMODEL",
}


def lean_tag(cell: str, status: str) -> str:
    p, q = cell.split("->")
    if status == "IMPLIES":
        return f"imp_{p.lower()}_{q.lower()}"
    if status == "COUNTERMODEL":
        return f"nimp_{p.lower()}_{q.lower()}"
    return f"open_cell_{p.lower()}_bl"


def matrix_report(
    scan: ScanResult,
    expected: Mapping[str, str] = EXPECTED_MATRIX,
    expected_open: frozenset[str] = EXPECTED_OPEN,
) -> dict[str, object]:
    """Cross-check the computed matrix against the expected table and
    build the artifact payload; any mismatch raises ``ValueError``.

    Per cell, ``status`` is the resolved status (IMPLIES cells carry a
    Lean implication proof; OPEN_LOCATED cells are the declared
    Prop-level locatedness gaps) and ``search`` is the raw finite
    search outcome (COUNTERMODEL / NO_COUNTERMODEL_IN_BOUNDS)."""
    for cell in sorted(expected_open):
        if not cell.endswith("->Bl"):
            raise ValueError(
                f"declared OPEN cell {cell!r} does not target Bl"
            )
    cells = cell_names()
    if sorted(expected) != sorted(cells):
        raise ValueError(
            "expected matrix must cover exactly the 72 ordered cells"
        )
    out_cells: dict[str, object] = {}
    status_counts = {"IMPLIES": 0, "COUNTERMODEL": 0, "OPEN_LOCATED": 0}
    for cell in cells:
        status = expected[cell]
        witness = scan.witnesses[cell]
        if status not in status_counts:
            raise ValueError(f"unknown status {status!r} for {cell!r}")
        if status == "COUNTERMODEL":
            if witness is None:
                raise ValueError(
                    f"{cell}: expected COUNTERMODEL, none found in "
                    "bounds"
                )
        elif witness is not None:
            raise ValueError(
                f"{cell}: expected {status}, search found a countermodel"
            )
        if status == "OPEN_LOCATED" and cell not in expected_open:
            raise ValueError(
                f"{cell}: OPEN_LOCATED outside the declared OPEN set"
            )
        if status != "OPEN_LOCATED" and cell in expected_open:
            raise ValueError(
                f"{cell}: declared OPEN but expected {status}"
            )
        status_counts[status] += 1
        out_cells[cell] = {
            "status": status,
            "search": (
                "COUNTERMODEL"
                if witness is not None
                else "NO_COUNTERMODEL_IN_BOUNDS"
            ),
            "witness": witness.json() if witness is not None else None,
            "lean": lean_tag(cell, status),
        }
    if scan.cotrans_violation_le2:
        raise ValueError(
            "cotransitivity must be automatic for candidate A at n <= 2"
        )
    a_bc = scan.witnesses["A->Bc"]
    if a_bc is None or a_bc.n != 3:
        raise ValueError(
            "the minimal A->Bc countermodel must live on carrier 3"
        )
    return {
        "cells": out_cells,
        "expected_equals_computed": True,
        "status_counts": status_counts,
        "open_cells": sorted(expected_open),
        "minimality_assertions": {"A->Bc": A_BC_MINIMALITY},
    }


# ---------------------------------------------------------------------------
# The two-element classification
# ---------------------------------------------------------------------------


def two_element_classification(
    expected_survivors: tuple[Rel, ...] = (
        frozenset({(0, 1)}),
        frozenset({(0, 1), (1, 0)}),
    ),
) -> dict[str, object]:
    """All relations on the two-element carrier with ``a = 0, b = 1``
    that satisfy ``A``, compared up to relation equality: exactly the
    oriented edge and the symmetric pair survive (Lean:
    ``bool_irrefl_witness_classification``).  Raises on any deviation
    from ``expected_survivors``."""
    survivors: list[Rel] = []
    for r, a, b in enumerate_base(2):
        if (a, b) != (0, 1):
            continue
        s = Setting(2, r, a, b, frozenset(), frozenset(), frozenset())
        if evaluate(s)["A"]:
            survivors.append(r)
    if sorted(tuple(sorted(r)) for r in survivors) != sorted(
        tuple(sorted(r)) for r in expected_survivors
    ):
        raise ValueError(
            "two-element classification deviates from the expected "
            "survivor list"
        )
    labels = {1: "oriented", 2: "symmetric"}
    return {
        "carrier": 2,
        "designated": [0, 1],
        "survivor_count": len(survivors),
        "survivors": [
            {
                "label": labels[len(r)],
                "r": [list(p) for p in sorted(r)],
            }
            for r in sorted(survivors, key=lambda r: (len(r), sorted(r)))
        ],
        "lean": "bool_irrefl_witness_classification",
    }


# ---------------------------------------------------------------------------
# Presentation branching, finite mirror
# ---------------------------------------------------------------------------


def surjections(n: int, m: int) -> list[Func]:
    return [f for f in product(range(m), repeat=n) if len(set(f)) == m]


def kernel(q: Func) -> Rel:
    n = len(q)
    return frozenset(
        (x, y) for x in range(n) for y in range(n) if q[x] == q[y]
    )


def partition_of(q: Func) -> Partition:
    blocks: dict[int, list[int]] = {}
    for x, v in enumerate(q):
        blocks.setdefault(v, []).append(x)
    return tuple(sorted(tuple(sorted(bl)) for bl in blocks.values()))


def presentation_branching(
    expected_maximal: tuple[Partition, ...] = (
        ((0,), (1, 2)),
        ((0, 2), (1,)),
    ),
) -> dict[str, object]:
    """Presentation branching, finite mirror: source carrier 3 with the
    designated edge ``(0, 1)``; presentations are surjections onto
    ``range(m)`` with ``m <= 3``, faithful when ``q(0) != q(1)``.

    Coarseness direction (documented): ``q1 <= q2`` iff ``ker(q1)`` is
    a SUBSET of ``ker(q2)``.  A larger kernel identifies more, so
    ``q2`` is the coarser presentation and the maximal elements are
    the coarsest faithful presentations.

    Of the three two-block partitions of the carrier, ``{0,1}|{2}``
    merges the designated edge and is unfaithful, so the faithful
    maximal-coarse kernel classes number exactly two; they are
    incomparable, so no faithful presentation is coarser-or-equal to
    all others (no weakly terminal presentation).  Raises on any
    deviation from ``expected_maximal``."""
    faithful: list[Func] = []
    for m in range(1, 4):
        for q in surjections(3, m):
            if q[0] != q[1]:
                faithful.append(q)
    kernels: dict[Partition, Rel] = {}
    map_counts: dict[Partition, int] = {}
    for q in faithful:
        part = partition_of(q)
        kernels[part] = kernel(q)
        map_counts[part] = map_counts.get(part, 0) + 1
    parts = sorted(kernels)
    maximal = [
        part
        for part in parts
        if not any(
            other != part and kernels[part] < kernels[other]
            for other in parts
        )
    ]
    weakly_terminal = [
        part
        for part in parts
        if all(kernels[other] <= kernels[part] for other in parts)
    ]
    if tuple(maximal) != tuple(sorted(expected_maximal)):
        raise ValueError(
            "maximal-coarse faithful kernel classes deviate from the "
            "expected list"
        )
    all_two_block = sorted(
        {partition_of(q) for q in surjections(3, 2)}
    )
    unfaithful_two_block = [p for p in all_two_block if p not in parts]
    return {
        "source": {"n": 3, "edge": [0, 1]},
        "coarseness": (
            "q1 <= q2 iff ker(q1) subset-of ker(q2); a larger kernel "
            "identifies more, so maximal = coarsest faithful"
        ),
        "faithful_surjection_count": len(faithful),
        "kernel_class_count": len(parts),
        "kernel_classes": [
            {
                "partition": [list(bl) for bl in part],
                "image_size": len(part),
                "map_count": map_counts[part],
            }
            for part in parts
        ],
        "maximal_coarse_class_count": len(maximal),
        "maximal_coarse_partitions": [
            [list(bl) for bl in part] for part in maximal
        ],
        "two_block_partitions_total": len(all_two_block),
        "unfaithful_two_block_partitions": [
            [list(bl) for bl in part] for part in unfaithful_two_block
        ],
        "no_weakly_terminal": len(weakly_terminal) == 0,
        "note": (
            "Of the three two-block partitions of the carrier, "
            "{0,1}|{2} merges the designated edge and is unfaithful; "
            "the two faithful coarsest kernel classes are "
            "incomparable, so no faithful presentation is "
            "coarser-or-equal to all others (finite mirror of the "
            "no-weakly-terminal finding)."
        ),
    }


# ---------------------------------------------------------------------------
# Artifact payloads
# ---------------------------------------------------------------------------


def bounds_json(total: int) -> dict[str, object]:
    return {
        "carriers": [1, 2, 3],
        "relations": "all subsets of X x X, enumerated exhaustively",
        "designated_points": "all ordered pairs (a, b) in X x X",
        "ret_choices": list(RET_CHOICES),
        "prot_choices": list(PROT_CHOICES),
        "ops_choices": list(OPS_CHOICES),
        "ops_note": (
            "at n = 1 the identity and const_0 tables coincide; "
            "enumeration items are counted without deduplication"
        ),
        "settings_enumerated": total,
        "witness_key": (
            "(n, len(r), len(ret)+len(prot), len(ops), sorted(r), a, "
            "b); ties broken by (sorted(ret), sorted(prot), "
            "sorted(ops))"
        ),
    }


def candidates_payload(scan: ScanResult) -> dict[str, object]:
    return {
        "bounds": bounds_json(scan.total),
        "candidate_counts": dict(scan.counts),
        "two_element_classification": two_element_classification(),
        "bl_equals_a_in_finite_universe": True,
        "bl_note": BL_NOTE,
        "presentation_branching": presentation_branching(),
    }
