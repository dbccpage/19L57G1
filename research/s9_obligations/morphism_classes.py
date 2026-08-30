"""P2 -- S9.2: morphism classes and initiality of two-element objects.

PROMPT.md steps 14-18 and 20.  Finite computation only; nothing here is a
theorem, and the sweep is bounded by the carrier it reaches (step 19).
AuthorityEffect: None.

Declarations, made before anything is computed
----------------------------------------------

Menu (step 15).  A morphism condition is a predicate on a function
``f : X -> Y`` between two pointed structures ``(X, r, a, b)`` and
``(Y, r', a', b')``.  The menu is exactly the five conditions the prompt
requires; no sixth condition is added.

    P   designated points preserved     f a = a' and f b = b'
    E   edges preserved                 r x y -> r' (f x) (f y)
    NE  non-edges preserved             not r x y -> not r' (f x) (f y)
                                        (over decidable relations, as in this
                                        finite model, the same condition as
                                        r' (f x) (f y) -> r x y; the fast path
                                        tests that form)
    I   injective                       f x = f y -> x = y
    S   surjective                      every y' in Y is f x for some x

A morphism class is a subset of the menu; there are 2^5 = 32 classes.  A
``C``-morphism satisfies every condition in ``C``.  The class name is the
set written in menu order, ``{}`` for the empty class and ``{P,E}`` for
the class of point-preserving edge-preserving maps.

Object classes (step 15).  An object is a pointed structure ``(n, rel,
a, b)`` in the sense of ``derivation.primdiff.Pointed``, with the
asserted pair required: ``(a, b) in rel``.  Two object classes are
computed separately and never merged:

    primary    irreflexivity NOT imposed.  The designated pair may be
               diagonal (``a = b``), and loops are allowed, so the
               one-point self-difference ``({0}, {(0, 0)}, 0, 0)`` is an
               object.  This is the class ``D2_initial_pointed``
               quantifies over.
    secondary  irreflexivity imposed on every object: ``rel`` has no
               ``(x, x)``.  Then ``a != b`` follows and no one-point
               object exists.

Candidate objects (steps 16-17).  The candidates ``O`` are every object
of the class with carrier exactly 2, enumerated by ``enumerate_pointed(2)``
and filtered by the class predicate -- not hand-picked.  In the primary
class the candidates with ``a = b`` are included, because they are objects
of that class; in the secondary class they are absent, because ``(a, a)
in rel`` contradicts irreflexivity.  Candidates are quotiented by the
implemented ``pointed_isomorphic`` relation; the representative of a class
is its first member in ``enumerate_pointed`` order.

Initiality (step 16).  ``O`` is initial for class ``C`` over an object
class up to carrier ``N`` when for every object ``Y`` of that class with
carrier ``1..N`` there is exactly one ``C``-morphism ``O -> Y``.  A cell
``(object class, C, O)`` fails by existence when some ``Y`` has no
``C``-morphism, and by uniqueness when some ``Y`` has two.  The witness
recorded for either failure is the FIRST such ``Y`` in the order: carrier
ascending, then ``enumerate_pointed`` order.  Both failure kinds are
searched independently, so a cell can carry both witnesses.

Bounds (PREFLIGHT.md step 4, P2).  Object carrier ``N = 3`` required,
``N = 4`` attempted, ``N = 5`` refused by name.  Candidates have carrier
exactly 2.  Menu at most 8 conditions.  When a bound is hit the bounded
terminal is reported with the partial and nothing is extrapolated.

What the fast path is.  For a function ``f = (u, v)`` from a two-element
carrier, every menu condition depends only on the four relation bits of
``Y`` at ``(u,u), (u,v), (v,u), (v,v)``, on whether ``u`` and ``v`` hit
the designated points of ``Y``, on ``u = v``, and on whether ``{u, v}``
exhausts ``Y``'s carrier.  The sweep encodes that in a lookup key per
``(u, v)`` and counts morphisms per cell with bit-parallel masks.  The
slow path ``morphisms`` enumerates ``all_functions_between`` directly and
checks the conditions one by one; every recorded witness is re-checked
against it, and ``test_morphism_classes.py`` compares the two over the
whole required carrier.

Witness groups.  The Lean targets proposed in ``P2_FINDINGS.md`` each rest
on a group of cells sharing one kind of witness.  Those groups are declared
here as cell predicates (``PRIMARY_GROUPS``, ``SECONDARY_GROUPS``), and
every count about them is computed from the cells by ``witness_groups``
and written under the receipt key ``witness_groups``; the groups of each
object class partition its cells and the receipt says whether they do.
The ``lean_targets`` field of a group names PROPOSED statements, not
theorems; nothing here carries a cell in Lean.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Iterable, Iterator, Sequence

from derivation.primdiff import (
    D2,
    D2_REV,
    S2,
    Func,
    Pointed,
    all_functions_between,
    enumerate_pointed,
    pointed_isomorphic,
    preserves_rel,
)

import common

# ---------------------------------------------------------------------------
# The menu and the classes
# ---------------------------------------------------------------------------

MENU: tuple[tuple[str, str], ...] = (
    ("P", "designated points preserved: f a = a' and f b = b'"),
    ("E", "edges preserved: r x y -> r' (f x) (f y)"),
    (
        "NE",
        "non-edges preserved: not r x y -> not r' (f x) (f y) "
        "(over decidable relations, as in this finite model, the same condition as "
        "r' (f x) (f y) -> r x y; a Lean statement should keep the not -> not form "
        "or prove decidability first)",
    ),
    ("I", "injective: f x = f y -> x = y"),
    ("S", "surjective: every y' in the carrier of Y is f x for some x"),
)
MENU_NAMES: tuple[str, ...] = tuple(name for name, _ in MENU)
MENU_SIZE = len(MENU)
CLASS_COUNT = 1 << MENU_SIZE
BIT: dict[str, int] = {name: 1 << index for index, name in enumerate(MENU_NAMES)}
ALL_CLASS_MASKS: tuple[int, ...] = tuple(range(CLASS_COUNT))

# PREFLIGHT.md step 4, P2 -- copied, not re-declared.
REQUIRED_N = 3
ATTEMPTED_N = 4
REFUSED_N = 5
CANDIDATE_CARRIER = 2
MENU_SIZE_BOUND = 8
CLASS_COUNT_BOUND = 1 << MENU_SIZE_BOUND

PAIRS2: tuple[tuple[int, int], ...] = ((0, 0), (0, 1), (1, 0), (1, 1))


def class_members(cmask: int) -> tuple[str, ...]:
    """The conditions of a class, in menu order."""

    return tuple(name for index, name in enumerate(MENU_NAMES) if cmask >> index & 1)


def class_mask(members: Iterable[str]) -> int:
    mask = 0
    for name in members:
        mask |= BIT[name]
    return mask


def class_name(cmask: int) -> str:
    return "{" + ",".join(class_members(cmask)) + "}"


def class_sort_key(cmask: int) -> tuple[int, tuple[int, ...]]:
    members = class_members(cmask)
    return (len(members), tuple(MENU_NAMES.index(name) for name in members))


# ---------------------------------------------------------------------------
# Object classes, objects, candidates
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ObjectClass:
    key: str
    irreflexivity_imposed: bool
    description: str


OBJECT_CLASSES: tuple[ObjectClass, ...] = (
    ObjectClass(
        "primary",
        False,
        "pointed structures with the asserted pair (a, b) in rel; "
        "irreflexivity not imposed; a = b allowed; loops allowed",
    ),
    ObjectClass(
        "secondary",
        True,
        "pointed structures with the asserted pair (a, b) in rel and rel "
        "irreflexive (no (x, x) in rel); a != b follows",
    ),
)


def is_object(s: Pointed, irreflexivity_imposed: bool) -> bool:
    if (s.a, s.b) not in s.rel:
        return False
    if irreflexivity_imposed and any(x == y for (x, y) in s.rel):
        return False
    return True


def objects(n: int, irreflexivity_imposed: bool) -> Iterator[Pointed]:
    """Every object of the class on the carrier ``range(n)``, in
    ``enumerate_pointed`` order."""

    for s in enumerate_pointed(n):
        if is_object(s, irreflexivity_imposed):
            yield s


def render_pointed(s: Pointed) -> dict[str, object]:
    return {"n": s.n, "rel": common.render_relation(s.rel), "a": s.a, "b": s.b}


def relation_bits2(rel: frozenset[tuple[int, int]]) -> str:
    return "".join("1" if pair in rel else "0" for pair in PAIRS2)


def candidate_name(s: Pointed) -> str:
    """``O<a><b>_<bits>`` with the bits over (0,0), (0,1), (1,0), (1,1)."""

    return f"O{s.a}{s.b}_{relation_bits2(s.rel)}"


FULL2 = Pointed(2, frozenset(PAIRS2), 0, 1)
ALIASES: tuple[tuple[Pointed, str], ...] = (
    (D2, "D2"),
    (S2, "S2"),
    (D2_REV, "D2rev"),
    (FULL2, "FULL2"),
)


def alias_of(s: Pointed) -> str | None:
    for structure, alias in ALIASES:
        if structure == s:
            return alias
    return None


@dataclass(frozen=True)
class Candidate:
    name: str
    representative: Pointed
    members: tuple[Pointed, ...]
    alias: str | None

    def json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "alias": self.alias,
            "representative": render_pointed(self.representative),
            "member_count": len(self.members),
            "members": [candidate_name(m) for m in self.members],
        }


def raw_candidates(irreflexivity_imposed: bool) -> list[Pointed]:
    """Every object of the class with carrier exactly 2, enumerated."""

    return list(objects(CANDIDATE_CARRIER, irreflexivity_imposed))


def quotient_candidates(raw: Sequence[Pointed]) -> list[Candidate]:
    """Quotient by ``pointed_isomorphic``; representative = first member."""

    classes: list[list[Pointed]] = []
    for s in raw:
        for members in classes:
            if pointed_isomorphic(members[0], s):
                members.append(s)
                break
        else:
            classes.append([s])
    return [
        Candidate(candidate_name(members[0]), members[0], tuple(members), alias_of(members[0]))
        for members in classes
    ]


# ---------------------------------------------------------------------------
# The slow path: conditions checked one by one on enumerated functions
# ---------------------------------------------------------------------------


def condition_mask(f: Func, src: Pointed, dst: Pointed) -> int:
    """The set of menu conditions ``f : src -> dst`` satisfies, as a mask."""

    mask = 0
    if f[src.a] == dst.a and f[src.b] == dst.b:
        mask |= BIT["P"]
    if preserves_rel(f, src, dst):
        mask |= BIT["E"]
    if all(
        (f[x], f[y]) not in dst.rel
        for x in range(src.n)
        for y in range(src.n)
        if (x, y) not in src.rel
    ):
        mask |= BIT["NE"]
    if len(set(f)) == src.n:
        mask |= BIT["I"]
    if set(f) == set(range(dst.n)):
        mask |= BIT["S"]
    return mask


def morphisms(src: Pointed, dst: Pointed, cmask: int) -> list[Func]:
    """All ``C``-morphisms ``src -> dst`` in ``all_functions_between`` order."""

    return [
        f
        for f in all_functions_between(src.n, dst.n)
        if condition_mask(f, src, dst) & cmask == cmask
    ]


# ---------------------------------------------------------------------------
# The fast path: one lookup key per (u, v), bit-parallel counting per cell
# ---------------------------------------------------------------------------

KEY_BITS = 10
KEY_COUNT = 1 << KEY_BITS


def _subset_closure() -> tuple[int, ...]:
    """``closure[s]`` has bit ``c`` set for every class mask ``c`` subset of ``s``."""

    out = []
    for s in range(CLASS_COUNT):
        bits = 0
        for c in range(CLASS_COUNT):
            if c & ~s == 0:
                bits |= 1 << c
        out.append(bits)
    return tuple(out)


SUBSET_CLOSURE = _subset_closure()


def satisfied_mask(candidate: Pointed, key: int) -> int:
    """Menu conditions satisfied by the function ``(u, v)`` described by
    ``key`` out of ``candidate``.  Key layout: bits 0-3 the relation of
    ``Y`` at (u,u), (u,v), (v,u), (v,v); bit 4 ``u = a'``; bit 5 ``u = b'``;
    bit 6 ``v = a'``; bit 7 ``v = b'``; bit 8 ``u = v``; bit 9 ``{u, v}``
    exhausts ``Y``'s carrier."""

    pattern = key & 0b1111
    u_is_a = key >> 4 & 1
    u_is_b = key >> 5 & 1
    v_is_a = key >> 6 & 1
    v_is_b = key >> 7 & 1
    diagonal = key >> 8 & 1
    surjective = key >> 9 & 1
    o_bits = 0
    for index, pair in enumerate(PAIRS2):
        if pair in candidate.rel:
            o_bits |= 1 << index
    mask = 0
    hits_a = u_is_a if candidate.a == 0 else v_is_a
    hits_b = u_is_b if candidate.b == 0 else v_is_b
    if hits_a and hits_b:
        mask |= BIT["P"]
    if o_bits & ~pattern == 0:
        mask |= BIT["E"]
    if pattern & ~o_bits == 0:
        mask |= BIT["NE"]
    if not diagonal:
        mask |= BIT["I"]
    if surjective:
        mask |= BIT["S"]
    return mask


def build_accept(candidates: Sequence[Candidate]) -> tuple[int, ...]:
    """``accept[key]`` has bit ``ci * 32 + c`` set when the function
    described by ``key`` is a ``c``-morphism out of candidate ``ci``."""

    table = []
    for key in range(KEY_COUNT):
        bits = 0
        for ci, candidate in enumerate(candidates):
            bits |= SUBSET_CLOSURE[satisfied_mask(candidate.representative, key)] << (
                ci * CLASS_COUNT
            )
        table.append(bits)
    return tuple(table)


def relation_mask(rel: frozenset[tuple[int, int]], n: int) -> int:
    bits = 0
    for x, y in rel:
        bits |= 1 << (x * n + y)
    return bits


def base_keys(n: int, rbits: int) -> list[tuple[int, int, int]]:
    """Per ``(u, v)``: the key bits that do not depend on the pointing."""

    out = []
    for u in range(n):
        for v in range(n):
            pattern = (
                (rbits >> (u * n + u) & 1)
                | (rbits >> (u * n + v) & 1) << 1
                | (rbits >> (v * n + u) & 1) << 2
                | (rbits >> (v * n + v) & 1) << 3
            )
            diagonal = 1 if u == v else 0
            surjective = 1 if (n == 1 or (n == 2 and u != v)) else 0
            out.append((u, v, pattern | diagonal << 8 | surjective << 9))
    return out


def _bits_of(value: int) -> Iterator[int]:
    while value:
        low = value & -value
        yield low.bit_length() - 1
        value ^= low


@dataclass(frozen=True)
class Cell:
    candidate: int
    cmask: int
    existence_failure: Pointed | None
    uniqueness_failure: tuple[Pointed, Func, Func] | None

    @property
    def initial(self) -> bool:
        return self.existence_failure is None and self.uniqueness_failure is None


@dataclass(frozen=True)
class Sweep:
    object_class: ObjectClass
    candidates: tuple[Candidate, ...]
    max_n: int
    objects_by_carrier: dict[int, int]
    cells: tuple[Cell, ...]

    def cell(self, candidate: int, cmask: int) -> Cell:
        return self.cells[candidate * CLASS_COUNT + cmask]


def sweep(object_class: ObjectClass, candidates: Sequence[Candidate], max_n: int) -> Sweep:
    """Decide every cell ``(C, O)`` over all objects with carrier ``1..max_n``.

    Each witness found by the fast path is re-checked with ``morphisms``
    (the slow path) before it is recorded.
    """

    irr = object_class.irreflexivity_imposed
    cell_count = len(candidates) * CLASS_COUNT
    all_cells = (1 << cell_count) - 1
    accept = build_accept(candidates)
    live_existence = all_cells
    live_uniqueness = all_cells
    existence: dict[int, Pointed] = {}
    uniqueness: dict[int, tuple[Pointed, Func, Func]] = {}
    objects_by_carrier: dict[int, int] = {}
    for n in range(1, max_n + 1):
        count = 0
        last_rel: frozenset[tuple[int, int]] | None = None
        keys: list[tuple[int, int, int]] = []
        for s in enumerate_pointed(n):
            if not is_object(s, irr):
                continue
            count += 1
            if s.rel is not last_rel:
                # enumerate_pointed yields every pointing of one relation
                # consecutively, sharing the frozenset; identity is exact.
                last_rel = s.rel
                keys = base_keys(n, relation_mask(s.rel, n))
            a, b = s.a, s.b
            seen_once = 0
            seen_twice = 0
            for u, v, base in keys:
                key = base
                if u == a:
                    key |= 1 << 4
                if u == b:
                    key |= 1 << 5
                if v == a:
                    key |= 1 << 6
                if v == b:
                    key |= 1 << 7
                m = accept[key]
                seen_twice |= seen_once & m
                seen_once |= m
            zero = live_existence & ~seen_once & all_cells
            multi = live_uniqueness & seen_twice
            if zero:
                live_existence &= ~zero
                for cell in _bits_of(zero):
                    ci, cmask = divmod(cell, CLASS_COUNT)
                    found = morphisms(candidates[ci].representative, s, cmask)
                    if found:
                        raise AssertionError(
                            f"fast path reported no morphism but the slow path found {found}"
                        )
                    existence[cell] = s
            if multi:
                live_uniqueness &= ~multi
                for cell in _bits_of(multi):
                    ci, cmask = divmod(cell, CLASS_COUNT)
                    found = morphisms(candidates[ci].representative, s, cmask)
                    if len(found) < 2:
                        raise AssertionError(
                            f"fast path reported two morphisms but the slow path found {found}"
                        )
                    uniqueness[cell] = (s, found[0], found[1])
        objects_by_carrier[n] = count
    cells = tuple(
        Cell(ci, cmask, existence.get(ci * CLASS_COUNT + cmask), uniqueness.get(ci * CLASS_COUNT + cmask))
        for ci in range(len(candidates))
        for cmask in range(CLASS_COUNT)
    )
    return Sweep(object_class, tuple(candidates), max_n, objects_by_carrier, cells)


def sweep_direct(
    object_class: ObjectClass, candidates: Sequence[Candidate], max_n: int
) -> Sweep:
    """The same classification by the slow path alone (for cross-checks)."""

    irr = object_class.irreflexivity_imposed
    existence: dict[int, Pointed] = {}
    uniqueness: dict[int, tuple[Pointed, Func, Func]] = {}
    objects_by_carrier: dict[int, int] = {}
    for n in range(1, max_n + 1):
        count = 0
        for s in objects(n, irr):
            count += 1
            functions = all_functions_between(CANDIDATE_CARRIER, n)
            for ci, candidate in enumerate(candidates):
                masks = [condition_mask(f, candidate.representative, s) for f in functions]
                for cmask in range(CLASS_COUNT):
                    cell = ci * CLASS_COUNT + cmask
                    found = [f for f, m in zip(functions, masks) if m & cmask == cmask]
                    if not found and cell not in existence:
                        existence[cell] = s
                    if len(found) >= 2 and cell not in uniqueness:
                        uniqueness[cell] = (s, found[0], found[1])
        objects_by_carrier[n] = count
    cells = tuple(
        Cell(ci, cmask, existence.get(ci * CLASS_COUNT + cmask), uniqueness.get(ci * CLASS_COUNT + cmask))
        for ci in range(len(candidates))
        for cmask in range(CLASS_COUNT)
    )
    return Sweep(object_class, tuple(candidates), max_n, objects_by_carrier, cells)


# ---------------------------------------------------------------------------
# Step 14: the D2_initial_pointed cell, checked directly
# ---------------------------------------------------------------------------


def d2_pointed_maps_direct(max_n: int) -> dict[str, object]:
    """For every object of the primary class up to ``max_n``: the number of
    point-preserving functions ``D2 -> Y`` and whether that function also
    preserves the oriented edge -- the theorem's exact quantification,
    checked with the slow path."""

    checked = 0
    unique = 0
    unique_and_edge_preserving = 0
    for n in range(1, max_n + 1):
        for s in objects(n, False):
            checked += 1
            point_maps = [
                f
                for f in all_functions_between(CANDIDATE_CARRIER, n)
                if f[D2.a] == s.a and f[D2.b] == s.b
            ]
            if len(point_maps) == 1:
                unique += 1
                if preserves_rel(point_maps[0], D2, s):
                    unique_and_edge_preserving += 1
    return {
        "carrier_reached": max_n,
        "objects_checked": checked,
        "objects_with_exactly_one_point_preserving_map": unique,
        "objects_where_that_map_preserves_the_edge": unique_and_edge_preserving,
        "agrees_with_theorem": checked == unique == unique_and_edge_preserving,
    }


# ---------------------------------------------------------------------------
# Step 18: the shape of the admitting set, as a set property
# ---------------------------------------------------------------------------


def shape(admitting: Iterable[int]) -> dict[str, object]:
    """Minimal and maximal admitting classes under inclusion, and whether
    the admitting set is an interval ``[lower, upper]`` -- checked as a set
    property, not only through the existence of a least and a greatest
    element.  ``admitting`` is a collection of class masks."""

    members = sorted(set(admitting), key=class_sort_key)
    member_set = set(members)
    minimal = [c for c in members if not any(d != c and d & ~c == 0 for d in members)]
    maximal = [c for c in members if not any(d != c and c & ~d == 0 for d in members)]
    result: dict[str, object] = {
        "admitting_classes": [class_name(c) for c in members],
        "admitting_count": len(members),
        "minimal": [class_name(c) for c in minimal],
        "maximal": [class_name(c) for c in maximal],
        "is_interval": False,
        "lower": None,
        "upper": None,
        "incomparable_pair": None,
        "gap": None,
        "terminal": None,
    }
    if not members:
        result["reason"] = "the admitting set is empty"
        return result
    lower = members[0]
    upper = 0
    for c in members:
        lower &= c
        upper |= c
    between = [c for c in ALL_CLASS_MASKS if lower & ~c == 0 and c & ~upper == 0]
    gaps = [c for c in between if c not in member_set]

    def first_incomparable(pool: Sequence[int]) -> tuple[int, int] | None:
        for i, c in enumerate(pool):
            for d in pool[i + 1 :]:
                if c & ~d and d & ~c:
                    return (c, d)
        return None

    # Only a pair among the maximal elements (then the join is not a member)
    # or among the minimal elements (then the meet is not a member) defeats
    # intervalhood.  Two incomparable non-extremal members do not: the
    # interval [{}, {P,E}] contains {P} and {E}.  So no fallback to an
    # arbitrary pair of members is taken; when both extremes are unique the
    # only way to fail is a gap, and the gap is what is reported.
    pair = first_incomparable(maximal)
    pair_source: str | None = "maximal" if pair is not None else None
    if pair is None:
        pair = first_incomparable(minimal)
        pair_source = "minimal" if pair is not None else None
    is_interval = lower in member_set and upper in member_set and not gaps
    result["is_interval"] = is_interval
    result["incomparable_pair_source"] = None
    if is_interval:
        result["lower"] = class_name(lower)
        result["upper"] = class_name(upper)
        result["terminal"] = "S9_2_INTERVAL_SHAPE"
    else:
        result["terminal"] = "S9_2_INCOMPARABLE_CLASSES"
        if pair is not None:
            result["incomparable_pair"] = [class_name(pair[0]), class_name(pair[1])]
            result["incomparable_pair_source"] = pair_source
        if gaps:
            result["gap"] = class_name(gaps[0])
        if pair is not None:
            result["reason"] = (
                f"not an interval: two {pair_source} admitting classes are incomparable, "
                f"{class_name(pair[0])} and {class_name(pair[1])}"
            )
        else:
            result["reason"] = (
                "not an interval: the minimal and maximal admitting classes are unique but "
                f"the class {class_name(gaps[0])} between them does not admit"
            )
    return result


def bounded_result(obj: Mapping[str, object], bound_reached: int) -> dict[str, object]:
    """PREFLIGHT.md step 4 receipt convention: every result object that
    depends on a bound carries ``bounded`` and ``bound_reached``."""

    out: dict[str, object] = dict(obj)
    out["bounded"] = True
    out["bound_reached"] = bound_reached
    return out


# ---------------------------------------------------------------------------
# Witness groups: the groups the proposed Lean targets rest on, counted from
# the cells and never stated by hand
# ---------------------------------------------------------------------------

SELF1 = Pointed(1, frozenset({(0, 0)}), 0, 0)
WITNESS_ALIASES: tuple[tuple[Pointed, str], ...] = ALIASES + ((SELF1, "SELF1"),)


def witness_label(s: Pointed) -> str:
    """A deterministic name for a witness object: its alias when it has one
    (D2, S2, FULL2; SELF1 is the one-point self-difference), otherwise
    ``n<n>:<edges>:a<a>b<b>`` with the edges as ``xy`` digit pairs in sorted
    order, so ``n3:01:a0b1`` is the three-point object with the one edge
    (0, 1) pointed at (0, 1)."""

    for structure, alias in WITNESS_ALIASES:
        if structure == s:
            return alias
    edges = ";".join(f"{x}{y}" for x, y in sorted(s.rel))
    return f"n{s.n}:{edges}:a{s.a}b{s.b}"


@dataclass(frozen=True)
class GroupSpec:
    """A named group of cells: a predicate on (class mask, candidate, cell)
    and the names of the proposed Lean statements that would cover it."""

    name: str
    cell_predicate: str
    lean_targets: tuple[str, ...]
    select: Callable[[int, Candidate, Cell], bool]


def _has(cmask: int, *names: str) -> bool:
    return all(cmask & BIT[name] for name in names)


def _lacks(cmask: int, *names: str) -> bool:
    return not any(cmask & BIT[name] for name in names)


def _is_class(cmask: int, *names: str) -> bool:
    return cmask == class_mask(names)


# The proposed Lean target names, in the order P2_FINDINGS.md numbers them.
# Names only: the statements live in P2_FINDINGS.md and nothing is proved.
LEAN_TARGET_NAMES: tuple[str, ...] = (
    "two_element_pointed_map_unique",
    "D2_initial_P_E",
    "FULL2_initial_P_NE",
    "no_injection_into_point",
    "no_surjection_onto_three",
    "two_copies_not_unique",
    "diagonal_candidate_not_pointed_into_D2",
    "extra_edge_not_into_D2",
    "non_edge_not_into_point",
    "pointed_map_injective_of_irrefl",
    "S2_initial_P_NE_irrefl",
    "S2_not_P_E_into_D2",
    "D2_not_P_NE_into_S2",
    "no_surjection_onto_three_irrefl",
    "two_irrefl_copies_not_unique",
)

PRIMARY_GROUPS: tuple[GroupSpec, ...] = (
    GroupSpec(
        "I_classes",
        "class contains I",
        ("no_injection_into_point",),
        lambda c, o, cell: _has(c, "I"),
    ),
    GroupSpec(
        "S_without_I_classes",
        "class contains S and not I",
        ("no_surjection_onto_three",),
        lambda c, o, cell: _has(c, "S") and _lacks(c, "I"),
    ),
    GroupSpec(
        "no_P_I_S_classes",
        "class contains none of P, I, S",
        ("two_copies_not_unique",),
        lambda c, o, cell: _lacks(c, "P", "I", "S"),
    ),
    GroupSpec(
        "P_class_initial",
        "class {P}, cell initial",
        ("two_element_pointed_map_unique",),
        lambda c, o, cell: _is_class(c, "P") and cell.initial,
    ),
    GroupSpec(
        "P_class_non_initial",
        "class {P}, cell not initial",
        ("diagonal_candidate_not_pointed_into_D2",),
        lambda c, o, cell: _is_class(c, "P") and not cell.initial,
    ),
    GroupSpec(
        "P_E_class",
        "class {P,E}",
        ("D2_initial_P_E", "diagonal_candidate_not_pointed_into_D2", "extra_edge_not_into_D2"),
        lambda c, o, cell: _is_class(c, "P", "E"),
    ),
    GroupSpec(
        "P_NE_class",
        "class {P,NE}",
        ("FULL2_initial_P_NE", "non_edge_not_into_point", "diagonal_candidate_not_pointed_into_D2"),
        lambda c, o, cell: _is_class(c, "P", "NE"),
    ),
    GroupSpec(
        "P_E_NE_class",
        "class {P,E,NE}",
        ("non_edge_not_into_point", "diagonal_candidate_not_pointed_into_D2", "extra_edge_not_into_D2"),
        lambda c, o, cell: _is_class(c, "P", "E", "NE"),
    ),
)

SECONDARY_GROUPS: tuple[GroupSpec, ...] = (
    GroupSpec(
        "S_classes",
        "class contains S",
        ("no_surjection_onto_three_irrefl",),
        lambda c, o, cell: _has(c, "S"),
    ),
    GroupSpec(
        "no_P_no_S_classes",
        "class contains neither P nor S",
        ("two_irrefl_copies_not_unique",),
        lambda c, o, cell: _lacks(c, "P", "S"),
    ),
    GroupSpec(
        "P_without_S_initial",
        "class contains P and not S, cell initial",
        (
            "two_element_pointed_map_unique",
            "pointed_map_injective_of_irrefl",
            "D2_initial_P_E",
            "S2_initial_P_NE_irrefl",
        ),
        lambda c, o, cell: _has(c, "P") and _lacks(c, "S") and cell.initial,
    ),
    GroupSpec(
        "P_without_S_non_initial",
        "class contains P and not S, cell not initial",
        ("S2_not_P_E_into_D2", "D2_not_P_NE_into_S2"),
        lambda c, o, cell: _has(c, "P") and _lacks(c, "S") and not cell.initial,
    ),
)

GROUPS_BY_OBJECT_CLASS: dict[str, tuple[GroupSpec, ...]] = {
    "primary": PRIMARY_GROUPS,
    "secondary": SECONDARY_GROUPS,
}


def _count_labels(labels: Iterable[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    return {label: counts[label] for label in sorted(counts)}


def select_cells(result: Sweep, spec: GroupSpec) -> list[tuple[int, Candidate, Cell]]:
    """The cells of ``result`` that ``spec`` selects, in table order."""

    selected: list[tuple[int, Candidate, Cell]] = []
    for cmask in ALL_CLASS_MASKS:
        for ci, candidate in enumerate(result.candidates):
            cell = result.cell(ci, cmask)
            if spec.select(cmask, candidate, cell):
                selected.append((cmask, candidate, cell))
    return selected


def group_report(result: Sweep, spec: GroupSpec) -> dict[str, object]:
    """Every count about one group, computed from the cells."""

    selected = select_cells(result, spec)
    existence = [cell.existence_failure for _, _, cell in selected if cell.existence_failure]
    uniqueness = [cell.uniqueness_failure for _, _, cell in selected if cell.uniqueness_failure]
    non_initial = [(cand, cell) for _, cand, cell in selected if not cell.initial]
    return {
        "cell_predicate": spec.cell_predicate,
        "lean_targets": list(spec.lean_targets),
        "classes": [class_name(c) for c in sorted({c for c, _, _ in selected}, key=class_sort_key)],
        "cells": len(selected),
        "initial": sum(1 for _, _, cell in selected if cell.initial),
        "existence_failures": len(existence),
        "uniqueness_failures": len(uniqueness),
        "existence_witness_counts": _count_labels(witness_label(y) for y in existence),
        "existence_witness_carriers": {
            str(n): count for n, count in sorted(_count_labels(str(y.n) for y in existence).items(), key=lambda kv: int(kv[0]))
        },
        "uniqueness_witness_counts": _count_labels(witness_label(y) for y, _, _ in uniqueness),
        "non_initial_diagonal_candidates": sum(
            1 for cand, _ in non_initial if cand.representative.a == cand.representative.b
        ),
        "non_initial_off_diagonal_candidates": sum(
            1 for cand, _ in non_initial if cand.representative.a != cand.representative.b
        ),
    }


def no_p_summary(result: Sweep) -> dict[str, object]:
    """The cells whose class lacks P: how each one fails, counted."""

    cells = [
        result.cell(ci, cmask)
        for cmask in ALL_CLASS_MASKS
        if _lacks(cmask, "P")
        for ci in range(len(result.candidates))
    ]
    without_uniqueness = [cell for cell in cells if cell.uniqueness_failure is None]
    return {
        "cells": len(cells),
        "initial": sum(1 for cell in cells if cell.initial),
        "with_uniqueness_witness": sum(1 for cell in cells if cell.uniqueness_failure is not None),
        "without_uniqueness_witness": len(without_uniqueness),
        "with_existence_witness": sum(1 for cell in cells if cell.existence_failure is not None),
        "without_existence_witness": sum(1 for cell in cells if cell.existence_failure is None),
        "without_any_witness": sum(1 for cell in cells if cell.initial),
        "classes_without_uniqueness_witness": [
            class_name(c)
            for c in sorted(
                {cell.cmask for cell in without_uniqueness}, key=class_sort_key
            )
        ],
        "existence_witness_counts_without_uniqueness_witness": _count_labels(
            witness_label(cell.existence_failure)
            for cell in without_uniqueness
            if cell.existence_failure is not None
        ),
    }


def witness_groups(result: Sweep, specs: Sequence[GroupSpec]) -> dict[str, object]:
    """The named groups of one object class, each counted from the cells,
    with the check that they partition the cells."""

    hits = [0] * len(result.cells)
    counts: list[int] = []
    for spec in specs:
        selected = select_cells(result, spec)
        counts.append(len(selected))
        for cmask, _, cell in selected:
            hits[cell.candidate * CLASS_COUNT + cmask] += 1
    groups = {spec.name: group_report(result, spec) for spec in specs}
    return {
        "note": "every count here is computed from the table's cells; lean_targets names "
        "proposed statements in P2_FINDINGS.md, none of which is proved by this part",
        "partition_order": [spec.name for spec in specs],
        "partition_cell_counts": counts,
        "partition_cell_total": sum(counts),
        "table_cells": len(result.cells),
        "partition_is_disjoint_and_exhaustive": all(h == 1 for h in hits),
        "groups": groups,
        "no_P_classes": no_p_summary(result),
        "witness_legend": {alias: render_pointed(s) for s, alias in WITNESS_ALIASES if alias != "D2rev"},
    }


# ---------------------------------------------------------------------------
# Receipt assembly
# ---------------------------------------------------------------------------


def witness_json(cell: Cell) -> tuple[object, object]:
    existence: object = None
    if cell.existence_failure is not None:
        existence = {"witness": render_pointed(cell.existence_failure)}
    uniqueness: object = None
    if cell.uniqueness_failure is not None:
        y, f1, f2 = cell.uniqueness_failure
        uniqueness = {
            "witness": render_pointed(y),
            "morphism_1": list(f1),
            "morphism_2": list(f2),
        }
    return existence, uniqueness


def table_rows(result: Sweep) -> list[dict[str, object]]:
    rows = []
    for cmask in sorted(ALL_CLASS_MASKS, key=class_sort_key):
        for ci, candidate in enumerate(result.candidates):
            cell = result.cell(ci, cmask)
            existence, uniqueness = witness_json(cell)
            rows.append(
                {
                    "object_class": result.object_class.key,
                    "class": class_name(cmask),
                    "class_conditions": list(class_members(cmask)),
                    "object": candidate.name,
                    "object_alias": candidate.alias,
                    "initial": cell.initial,
                    "existence_failure": existence,
                    "uniqueness_failure": uniqueness,
                    "bounded": True,
                    "bound_reached": result.max_n,
                }
            )
    return rows


def admitting_masks(result: Sweep) -> list[int]:
    return sorted(
        {
            cmask
            for cmask in ALL_CLASS_MASKS
            for ci in range(len(result.candidates))
            if result.cell(ci, cmask).initial
        },
        key=class_sort_key,
    )


def ties(result: Sweep) -> dict[str, object]:
    per_class: dict[str, object] = {}
    classes_with_ties = []
    max_tie = 0
    for cmask in sorted(ALL_CLASS_MASKS, key=class_sort_key):
        retained = [
            candidate.name
            for ci, candidate in enumerate(result.candidates)
            if result.cell(ci, cmask).initial
        ]
        if retained:
            per_class[class_name(cmask)] = {"count": len(retained), "retained": retained}
            max_tie = max(max_tie, len(retained))
            if len(retained) >= 2:
                classes_with_ties.append(class_name(cmask))
    return {
        "per_class": per_class,
        "classes_with_ties": classes_with_ties,
        "max_tie": max_tie,
        "quotient": "pointed_isomorphic (derivation.primdiff), representative = first member",
    }


def initial_matrix(result: Sweep) -> dict[str, list[str]]:
    return {
        class_name(cmask): [
            candidate.name
            for ci, candidate in enumerate(result.candidates)
            if result.cell(ci, cmask).initial
        ]
        for cmask in sorted(ALL_CLASS_MASKS, key=class_sort_key)
    }


def failure_summary(result: Sweep) -> dict[str, int]:
    existence_only = uniqueness_only = both = initial = 0
    for cell in result.cells:
        e = cell.existence_failure is not None
        u = cell.uniqueness_failure is not None
        if e and u:
            both += 1
        elif e:
            existence_only += 1
        elif u:
            uniqueness_only += 1
        else:
            initial += 1
    return {
        "cells": len(result.cells),
        "initial": initial,
        "existence_failure_only": existence_only,
        "uniqueness_failure_only": uniqueness_only,
        "both_failures": both,
    }


def d2_cell_record(primary: Sweep) -> dict[str, object]:
    """Step 14: ``D2_initial_pointed`` restated in the menu's vocabulary and
    located in the table."""

    d2_index = next(
        ci for ci, candidate in enumerate(primary.candidates) if candidate.representative == D2
    )
    p_only = primary.cell(d2_index, class_mask(["P"]))
    p_and_e = primary.cell(d2_index, class_mask(["P", "E"]))
    return {
        "theorem": "PrimDiff.D2_initial_pointed",
        "source": "lean4/Derivation/PrimDiff.lean",
        "quantification": {
            "objects": "every type alpha, every r : alpha -> alpha -> Prop, every a b with r a b; "
            "no irreflexivity hypothesis; a = b not excluded",
            "existence": "some f : Bool -> alpha with f false = a, f true = b, and "
            "forall x y, D2 x y -> r (f x) (f y)",
            "uniqueness": "every g : Bool -> alpha with g false = a and g true = b equals f "
            "pointwise; NO edge condition is imposed on g",
        },
        "in_menu_terms": {
            "object_class": "primary",
            "object": primary.candidates[d2_index].name,
            "object_alias": "D2",
            "existence_class": class_name(class_mask(["P", "E"])),
            "uniqueness_class": class_name(class_mask(["P"])),
            "reading": "D2 is initial for the class {P}, and the unique {P}-morphism is "
            "moreover an {E}-morphism; hence D2 is also initial for {P,E}",
        },
        "recorded_cell": {
            "object_class": "primary",
            "class": class_name(class_mask(["P"])),
            "object": primary.candidates[d2_index].name,
            "initial_in_table": p_only.initial,
        },
        "corollary_cell": {
            "object_class": "primary",
            "class": class_name(class_mask(["P", "E"])),
            "object": primary.candidates[d2_index].name,
            "initial_in_table": p_and_e.initial,
        },
        "model_agrees_at_bound": p_only.initial and p_and_e.initial,
        "bounded": True,
        "bound_reached": primary.max_n,
        "direct_check": d2_pointed_maps_direct(REQUIRED_N),
    }


def same_cells(left: Sweep, right: Sweep) -> bool:
    """Whether two sweeps agree cell for cell (initiality and both witnesses)."""

    return left.cells == right.cells


def declared_bounds() -> dict[str, object]:
    return {
        "source": "research/s9_obligations/PREFLIGHT.md, step 4, P2",
        "object_carrier": {
            "required": REQUIRED_N,
            "attempted": ATTEMPTED_N,
            "refused_by_name": REFUSED_N,
        },
        "candidate_carrier": CANDIDATE_CARRIER,
        "menu_size_bound": MENU_SIZE_BOUND,
        "class_count_bound": CLASS_COUNT_BOUND,
        "on_bound_hit": "report S9_2_CLASSES_BOUNDED at the carrier reached with the partial "
        "(cells named); never extrapolate; a carrier-general claim needs a Lean theorem "
        "naming the general case",
    }


def compute(max_n: int) -> dict[str, object]:
    """The whole P2 computation at object-carrier bound ``max_n``."""

    if max_n > ATTEMPTED_N:
        raise ValueError(f"carrier N = {max_n} is refused by name (PREFLIGHT.md step 4, P2)")
    sweeps: dict[str, Sweep] = {}
    required_sweeps: dict[str, Sweep] = {}
    candidates_json: dict[str, object] = {}
    for object_class in OBJECT_CLASSES:
        raw = raw_candidates(object_class.irreflexivity_imposed)
        candidates = quotient_candidates(raw)
        sweeps[object_class.key] = sweep(object_class, candidates, max_n)
        required_sweeps[object_class.key] = (
            sweeps[object_class.key]
            if max_n == REQUIRED_N
            else sweep(object_class, candidates, min(max_n, REQUIRED_N))
        )
        candidates_json[object_class.key] = {
            "raw_count": len(raw),
            "raw": [candidate_name(s) for s in raw],
            "a_eq_b_included": not object_class.irreflexivity_imposed,
            "a_eq_b_reason": (
                "included: the primary class does not impose irreflexivity, so a "
                "two-element structure with a = b and (a, a) in rel is an object of it"
                if not object_class.irreflexivity_imposed
                else "excluded: (a, a) in rel contradicts irreflexivity, so no such "
                "structure is an object of the secondary class"
            ),
            "iso_class_count": len(candidates),
            "classes": [candidate.json() for candidate in candidates],
        }

    primary = sweeps["primary"]
    secondary = sweeps["secondary"]
    tables: dict[str, object] = {}
    shapes: dict[str, object] = {}
    tie_report: dict[str, object] = {}
    matrices: dict[str, object] = {}
    summaries: dict[str, object] = {}
    groups: dict[str, object] = {}
    bounds_reached: dict[str, object] = {
        "menu_size": MENU_SIZE,
        "class_count": CLASS_COUNT,
    }
    for key, result in sweeps.items():
        tables[key] = bounded_result(
            {"row_count": len(result.cells), "rows": table_rows(result)}, result.max_n
        )
        shapes[key] = bounded_result(shape(admitting_masks(result)), result.max_n)
        tie_report[key] = bounded_result(ties(result), result.max_n)
        matrices[key] = bounded_result({"by_class": initial_matrix(result)}, result.max_n)
        summaries[key] = bounded_result(failure_summary(result), result.max_n)
        groups[key] = bounded_result(
            witness_groups(result, GROUPS_BY_OBJECT_CLASS[key]), result.max_n
        )
        bounds_reached[key] = {
            "carrier_reached": result.max_n,
            "required_carrier_reached": result.max_n >= REQUIRED_N,
            "attempted_carrier_completed": result.max_n >= ATTEMPTED_N,
            "objects_checked_by_carrier": {
                str(n): count for n, count in sorted(result.objects_by_carrier.items())
            },
            "objects_checked_total": sum(result.objects_by_carrier.values()),
            "candidate_iso_classes": len(result.candidates),
            "cells": len(result.cells),
            "table_identical_at_required_carrier": same_cells(result, required_sweeps[key]),
            "required_carrier": required_sweeps[key].max_n,
        }

    terminals = terminal_list(sweeps, shapes, tie_report)
    return {
        "header": common.receipt_header(),
        "part": "P2",
        "subject": "S9.2 -- morphism classes and initiality of two-element objects",
        "numbering_note": "S9.1, S9.2, S9.3 are the first three bullets of section S9 of "
        "paper/primitive_difference.md in order; the numbering is the prompt's, not the paper's",
        "authority_effect": "None",
        "declared_bounds": declared_bounds(),
        "bounds_reached": bounds_reached,
        "menu": [{"name": name, "definition": definition} for name, definition in MENU],
        "menu_size": MENU_SIZE,
        "class_count": CLASS_COUNT,
        "classes": [class_name(c) for c in sorted(ALL_CLASS_MASKS, key=class_sort_key)],
        "object_classes": {
            object_class.key: {
                "irreflexivity_imposed": object_class.irreflexivity_imposed,
                "asserted_pair_required": True,
                "diagonal_pair_allowed": not object_class.irreflexivity_imposed,
                "description": object_class.description,
                "carriers": list(range(1, max_n + 1)),
            }
            for object_class in OBJECT_CLASSES
        },
        "candidates": candidates_json,
        "witness_order": "first failing object Y in the order: carrier ascending, then "
        "enumerate_pointed order; existence and uniqueness searched independently",
        "d2_initial_pointed_cell": d2_cell_record(primary),
        "tables": tables,
        "initial_objects_by_class": matrices,
        "cell_summary": summaries,
        "shape": shapes,
        "ties": tie_report,
        "witness_groups": groups,
        "python_only_scope": bounded_result(
            {
                "reproduces_s9_fifth_bullet": True,
                "statement": "the exhaustiveness of this sweep over every object with carrier "
                f"<= {max_n} lives in Python only; no Lean theorem states that the finite "
                "scope was swept, and any Lean theorem for a cell is carrier-general by a "
                "uniform argument, not by formalizing the sweep",
            },
            max_n,
        ),
        "lean": {
            "carried_by_this_part": False,
            "note": "P2 proposes Lean targets in P2_FINDINGS.md; S9_2_CLASSES_CLASSIFIED, "
            "LEAN_CARRIED and LEAN_NOT_CARRIED are the Lean stage's terminals",
            "proposed_target_names": list(LEAN_TARGET_NAMES),
            "proposed_target_count": len(LEAN_TARGET_NAMES),
            "sealed_theorem_cell": {
                "theorem": "PrimDiff.D2_initial_pointed",
                "object_class": "primary",
                "class": class_name(class_mask(["P"])),
                "object": "O01_0100",
                "relation": "the sealed theorem's statement implies this cell's carrier-general "
                "form by dropping the edge clause from its existence half; that one-step "
                "corollary is proposed as two_element_pointed_map_unique for the a = 0, "
                "b = 1 candidates and is not carried here",
            },
        },
        "terminals": terminals,
        "not_in_scope": ["OB-1", "S6.6", "S9 last bullet (inscription bridge)"],
        "secondary_note": "the secondary (irreflexive) table is reported separately and is "
        "never merged into the primary table",
        "d2_secondary_cell": {
            "object_class": "secondary",
            "class": class_name(class_mask(["P"])),
            "object": "O01_0100",
            "initial_in_table": secondary.cell(
                next(
                    ci
                    for ci, candidate in enumerate(secondary.candidates)
                    if candidate.representative == D2
                ),
                class_mask(["P"]),
            ).initial,
        },
    }


def terminal_list(
    sweeps: dict[str, Sweep], shapes: dict[str, object], tie_report: dict[str, object]
) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for key, result in sweeps.items():
        out.append(
            {
                "terminal": "S9_2_CLASSES_BOUNDED",
                "scope": f"object class {key}: every cell of the {len(result.cells)}-cell "
                f"table is finite computation, bounded by object carrier N = {result.max_n} "
                f"({sum(result.objects_by_carrier.values())} objects); initiality quantifies "
                "over all objects and the sweep reaches only N",
            }
        )
    for key, result in sweeps.items():
        sh = shapes[key]
        assert isinstance(sh, dict)
        terminal = sh["terminal"]
        if terminal is None:
            continue
        if terminal == "S9_2_INTERVAL_SHAPE":
            scope = (
                f"object class {key}: the admitting set is the interval "
                f"[{sh['lower']}, {sh['upper']}] under inclusion, bounded by N = {result.max_n}"
            )
        else:
            detail = (
                f"incomparable pair {sh['incomparable_pair']}"
                if sh["incomparable_pair"] is not None
                else f"gap {sh['gap']}"
            )
            scope = (
                f"object class {key}: the admitting set {sh['admitting_classes']} is not an "
                f"interval under inclusion ({detail}); minimal {sh['minimal']}, maximal "
                f"{sh['maximal']}; bounded by N = {result.max_n}"
            )
        out.append({"terminal": str(terminal), "scope": scope})
    for key, result in sweeps.items():
        tr = tie_report[key]
        assert isinstance(tr, dict)
        classes = tr["classes_with_ties"]
        assert isinstance(classes, list)
        if classes:
            per_class = tr["per_class"]
            assert isinstance(per_class, dict)
            counts = ", ".join(f"{c}: {per_class[c]['count']}" for c in classes)
            out.append(
                {
                    "terminal": "TIES_RETAINED",
                    "scope": f"object class {key}: every non-isomorphic two-element object "
                    f"initial for a class is retained; classes with ties and counts: {counts}; "
                    f"bounded by N = {result.max_n}",
                }
            )
    reached = max(result.max_n for result in sweeps.values())
    out.append(
        {
            "terminal": "PYTHON_ONLY_SCOPE_DECLARED",
            "scope": "the P2 sweep reproduces S9's fifth bullet for the S9.2 table: its "
            f"exhaustiveness over every object with carrier <= {reached} lives in Python "
            f"only, bounded by N = {reached}; no Lean theorem states that the scope was swept",
        }
    )
    out.append(
        {
            "terminal": "REFUSED",
            "scope": f"object carrier N = {REFUSED_N} for P2, refused by name (PREFLIGHT.md step 4)",
        }
    )
    return out
