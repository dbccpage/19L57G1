"""Unit 52 check: morphisms of pointed witnessed relations, counted.

Python (book): Genesis has no Python mirror of `PrimitiveCats`. This
script reuses Genesis's `derivation.primdiff` (pointed structures,
point-preserving maps, relation preservation, automorphisms) and counts
morphisms on carriers of at most three points: the unique map out of the
oriented two-point object into every witnessed target; the symmetric
object's maps, which exist only into symmetric targets; the two maps out
of a three-point object; the pointed and unpointed automorphisms; and the
faithful presentations of the three-point and two-point sources (the two
incomparable cuts, no weakly terminal presentation within the bound, the
free point's two maps). Every count is a bounded search and is labelled
as such. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u52_primitive_cats.py
"""
from __future__ import annotations

import sys
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.primdiff import (  # noqa: E402
    D2, S2, Func, Pointed, a1, automorphisms, enumerate_pointed,
    irreflexive, pointed_maps, preserves_rel,
)

# Lean's objects as pointed structures (false = 0, true = 1).
D2_OBJ = D2                                                  # d2Obj
S2_OBJ = S2                                                  # s2Obj
D2_SWAP = Pointed(2, frozenset({(1, 0)}), 1, 0)              # d2SwapObj
UNIT_SELF = Pointed(1, frozenset({(0, 0)}), 0, 0)            # the one-point self-witness
BIG0 = Pointed(3, frozenset({(0, 1)}), 0, 1)                 # bigObj 0 (= bigObj3)
WIDE0 = Pointed(2, frozenset({(0, 1)}), 0, 1)                # wideObj 0


def homs(src: Pointed, dst: Pointed) -> list[Func]:
    """Lean's `Hom src dst`: point-preserving maps that carry every edge."""
    return [f for f in pointed_maps(src, dst) if preserves_rel(f, src, dst)]


def symmetric(s: Pointed) -> bool:
    return all((y, x) in s.rel for (x, y) in s.rel)


def witnessed(max_n: int) -> list[Pointed]:
    """Every object of `PtdRel` on a carrier of at most max_n points."""
    return [s for n in range(1, max_n + 1) for s in enumerate_pointed(n) if a1(s)]


# Presentations: a map q from the source's occurrences into a carrier
# range(m), faithful when it keeps the witnessed pair apart.
def presentations(k: int, max_m: int) -> list[tuple[int, Func]]:
    out = []
    for m in range(1, max_m + 1):
        for q in product(range(m), repeat=k):
            if q[0] != q[1]:
                out.append((m, q))
    return out


def phoms(p: tuple[int, Func], r: tuple[int, Func]) -> list[Func]:
    """Lean's `PHom p r`: maps h with h (p.q x) = r.q x at every occurrence x."""
    mp, qp = p
    mr, qr = r
    return [h for h in product(range(mr), repeat=mp)
            if all(h[qp[x]] == qr[x] for x in range(len(qp)))]


def main() -> int:
    failures: list[str] = []
    objs = witnessed(3)
    print(f"objects of PtdRel on 1..3 points (bounded search): {len(objs)}")

    counts = [len(homs(D2_OBJ, t)) for t in objs]
    print(f"maps out of d2Obj: every target receives exactly one: "
          f"{set(counts) == {1}} (d2_initial)")
    if set(counts) != {1}:
        failures.append("d2 initial")
    counts_swap = [len(homs(D2_SWAP, t)) for t in objs]
    print(f"maps out of d2SwapObj: exactly one each: {set(counts_swap) == {1}}; "
          f"d2SwapObj == d2Obj as a presentation: {D2_SWAP == D2_OBJ} (two_initials_not_identical)")
    if set(counts_swap) != {1} or D2_SWAP == D2_OBJ:
        failures.append("swap initial")
    print(f"wideObj 0 is d2Obj: {WIDE0 == D2_OBJ}; its maps out, one each: "
          f"{set(len(homs(WIDE0, t)) for t in objs) == {1}} (audit finding 1)")

    # injectivity of the unique map
    inj_irrefl = all(len(set(homs(D2_OBJ, t)[0])) == 2 for t in objs if irreflexive(t.rel))
    unit_map = homs(D2_OBJ, UNIT_SELF)[0]
    print(f"into irreflexive targets the unique map is injective: {inj_irrefl} "
          f"(d2_map_injective); into the one-point self-witness it is {unit_map}: "
          f"collapsed (d2_map_not_injective_without_irrefl)")
    if not inj_irrefl or len(set(unit_map)) != 1:
        failures.append("injectivity")

    # which objects within the bound are initial against targets within the bound
    initial_in_bound = [s for s in objs if all(len(homs(s, t)) == 1 for t in objs)]
    print(f"objects initial against every target within the bound: "
          f"{[s.json() for s in initial_in_bound]}")
    if sorted(sorted(s.rel) for s in initial_in_bound) != [[(0, 1)], [(1, 0)]]:
        failures.append("initial census")

    # s2Obj
    s2_counts = {len(homs(S2_OBJ, t)) for t in objs if symmetric(t)}
    s2_nonsym_zero = [t for t in objs if not symmetric(t) and len(homs(S2_OBJ, t)) == 0]
    print(f"maps out of s2Obj into symmetric targets: {s2_counts} (s2_initial_sym); "
          f"into d2Obj: {len(homs(S2_OBJ, D2_OBJ))} (s2_no_hom_to_d2); "
          f"non-symmetric targets receiving none: {len(s2_nonsym_zero)}")
    if s2_counts != {1} or homs(S2_OBJ, D2_OBJ):
        failures.append("s2")

    # three points: two maps
    big = homs(BIG0, D2_OBJ)
    print(f"maps bigObj 0 -> d2Obj: {big} (bigHomA, bigHomB; larger_not_initial)")
    if len(big) != 2:
        failures.append("bigObj")

    # automorphisms
    print(f"pointed automorphisms: d2Obj {automorphisms(D2_OBJ, True)}, "
          f"s2Obj {automorphisms(S2_OBJ, True)} (pointed_rigid); unpointed: "
          f"d2 {automorphisms(D2_OBJ, False)}, s2 {automorphisms(S2_OBJ, False)} "
          f"(s2_swap_isRelAuto, d2_swap_not_isRelAuto)")
    if automorphisms(S2_OBJ, True) != [(0, 1)] or len(automorphisms(S2_OBJ, False)) != 2:
        failures.append("autos")

    # presentations of the three-point source
    pres3 = presentations(3, 3)
    merge_a, merge_b = (2, (0, 1, 0)), (2, (1, 0, 0))
    id3 = (3, (0, 1, 2))
    print(f"faithful presentations of Fin 3 into carriers of at most 3 points: {len(pres3)}")
    print(f"  phoms mergeA -> mergeB: {len(phoms(merge_a, merge_b))}, "
          f"mergeB -> mergeA: {len(phoms(merge_b, merge_a))} (no_phom_merge*)")
    print(f"  maps out of idPres3: one into each: "
          f"{all(len(phoms(id3, r)) == 1 for r in pres3)} (pres_initial)")
    receivers = [t for t in pres3 if all(phoms(p, t) for p in pres3)]
    print(f"  presentations receiving a map from every presentation within the bound: "
          f"{len(receivers)} (no_terminal_pres)")
    if phoms(merge_a, merge_b) or phoms(merge_b, merge_a) or receivers:
        failures.append("pres3")

    # presentations of the two-point source
    pres2 = presentations(2, 3)
    id2, swap2, free2 = (2, (0, 1)), (2, (1, 0)), (3, (0, 1))
    print(f"faithful presentations of Bool into carriers of at most 3 points: {len(pres2)}")
    print(f"  phoms into idPres2 from idPres2 {len(phoms(id2, id2))}, from swapPres2 "
          f"{len(phoms(swap2, id2))} (phom2_unique_exists_*)")
    epi_unique = all(len(phoms(p, id2)) <= 1 for p in pres2 if set(p[1]) == set(range(p[0])))
    print(f"  surjective presentations send at most one map into idPres2: {epi_unique} "
          f"(phom2_unique_of_epi)")
    free_counts = {t: len(phoms(free2, t)) for t in pres2}
    print(f"  maps out of freePres2 into each target = size of the target's carrier: "
          f"{all(c == t[0] for t, c in free_counts.items())}; never one: "
          f"{1 not in free_counts.values()} (no_terminal_pres2)")
    if not epi_unique or 1 in free_counts.values():
        failures.append("pres2")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
