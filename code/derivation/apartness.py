"""Deterministic mirror of ``lean4/Derivation/Apartness.lean``.

Positive apartness (irreflexive, symmetric, cotransitive),
indistinguishability as its negation, the equivalence theorem
verified exhaustively over the declared finite universe, the
insufficiency countermodels with minimality checks, the orientation
separation, and the exact operation-preservation censuses.
"""

from __future__ import annotations

from itertools import product

from derivation.export import Json

Rel = frozenset[tuple[int, int]]


def all_relations(n: int) -> list[Rel]:
    pairs = [(i, j) for i in range(n) for j in range(n)]
    out: list[Rel] = []
    for bits in product((False, True), repeat=len(pairs)):
        out.append(frozenset(p for p, b in zip(pairs, bits) if b))
    return out


def is_irrefl(n: int, r: Rel) -> bool:
    return all((x, x) not in r for x in range(n))


def is_symm(n: int, r: Rel) -> bool:
    return all((y, x) in r for (x, y) in r)


def is_cotrans(n: int, r: Rel) -> bool:
    return all((x, z) in r or (z, y) in r
               for (x, y) in r for z in range(n))


def is_apart(n: int, r: Rel) -> bool:
    return is_irrefl(n, r) and is_symm(n, r) and is_cotrans(n, r)


def indist(r: Rel, x: int, y: int) -> bool:
    return (x, y) not in r


def indist_is_equivalence(n: int, r: Rel) -> bool:
    refl = all(indist(r, x, x) for x in range(n))
    symm = all((not indist(r, x, y)) or indist(r, y, x)
               for x in range(n) for y in range(n))
    trans = all((not (indist(r, x, y) and indist(r, y, z)))
                or indist(r, x, z)
                for x in range(n) for y in range(n)
                for z in range(n))
    return refl and symm and trans


def equivalence_theorem_exhaustive(max_n: int) -> bool:
    """Mirror of ``indist_equivalence``: on every relation of every
    carrier up to the bound, positive apartness makes
    indistinguishability an equivalence."""
    return all(indist_is_equivalence(n, r)
               for n in range(1, max_n + 1)
               for r in all_relations(n) if is_apart(n, r))


def insufficiency_countermodels() -> dict[str, Json]:
    """The three countermodels with minimality checks."""
    bare = frozenset({(0, 0)})
    d2 = frozenset({(0, 1)})
    tri = frozenset({(0, 1), (1, 0)})
    # minimality of the two-point symmetry failure: every irreflexive
    # relation on one point has equivalence indistinguishability
    min2 = all(indist_is_equivalence(1, r)
               for r in all_relations(1) if is_irrefl(1, r))
    # minimality of the three-point transitivity failure: among
    # irreflexive AND symmetric relations on two points (the class
    # witnessing the cotransitivity gap), indistinguishability is
    # already an equivalence — cotransitivity is automatic there
    min3 = all(indist_is_equivalence(2, r)
               for r in all_relations(2)
               if is_irrefl(2, r) and is_symm(2, r))
    return {
        "bare_breaks_refl": not indist(bare, 0, 0),
        "irrefl_alone_breaks_symm": (
            is_irrefl(2, d2)
            and indist(d2, 1, 0) and not indist(d2, 0, 1)),
        "symm_without_cotrans_breaks_trans": (
            is_irrefl(3, tri) and is_symm(3, tri)
            and not is_cotrans(3, tri)
            and indist(tri, 0, 2) and indist(tri, 2, 1)
            and not indist(tri, 0, 1)),
        "two_point_countermodel_minimal": min2,
        "three_point_countermodel_minimal": min3,
    }


def sym_closure(r: Rel) -> Rel:
    return frozenset(list(r) + [(y, x) for (x, y) in r])


def orientation_separation() -> dict[str, Json]:
    d2 = frozenset({(0, 1)})
    d2rev = frozenset({(1, 0)})
    return {
        "same_apartness": sym_closure(d2) == sym_closure(d2rev),
        "orientations_differ": d2 != d2rev,
        "swap_moves_retained_witness": (
            (0, 1) in d2 and (1, 0) not in d2),
        "apartness_is_apart": is_apart(2, sym_closure(d2)),
    }


def all_endofunctions(n: int) -> list[tuple[int, ...]]:
    return [f for f in product(range(n), repeat=n)]


def preserves_oriented(f: tuple[int, ...], a: int, b: int) -> bool:
    return f[a] == a and f[b] == b


def preserves_apart(f: tuple[int, ...], a: int, b: int) -> bool:
    return (f[a], f[b]) in {(a, b), (b, a)}


def operation_censuses(max_n: int) -> dict[str, Json]:
    """The exact preservation censuses: on the two-point carrier the
    oriented preservers are exactly the identity and the apartness
    preservers exactly the identity and the swap; on larger carriers
    the free points contribute the ``n^(n-2)`` factor."""
    per_n: dict[str, dict[str, int]] = {}
    for n in range(2, max_n + 1):
        fs = all_endofunctions(n)
        oriented = [f for f in fs if preserves_oriented(f, 0, 1)]
        apart = [f for f in fs if preserves_apart(f, 0, 1)]
        per_n[str(n)] = {
            "endofunctions": len(fs),
            "oriented_preservers": len(oriented),
            "apart_preservers": len(apart),
        }
    two = per_n["2"]
    idf = (0, 1)
    swap = (1, 0)
    fs2 = all_endofunctions(2)
    return {
        "per_carrier": per_n,
        "two_point_oriented_exactly_id": (
            [f for f in fs2 if preserves_oriented(f, 0, 1)]
            == [idf]),
        "two_point_apart_exactly_id_and_swap": (
            sorted(f for f in fs2 if preserves_apart(f, 0, 1))
            == sorted([idf, swap])),
        "two_point_constants_preserve_neither": all(
            not preserves_oriented(f, 0, 1)
            and not preserves_apart(f, 0, 1)
            for f in [(0, 0), (1, 1)]),
        "formula_oriented": "n^(n-2) (endpoints fixed, free points "
                            "unconstrained)",
        "formula_checked": all(
            per_n[str(n)]["oriented_preservers"] == n ** (n - 2)
            and per_n[str(n)]["apart_preservers"] == 2 * n ** (n - 2)
            for n in range(2, max_n + 1)),
        "two_point_census": two,
    }
