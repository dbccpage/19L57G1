"""Finite two-object fixtures for the flat-to-indexed embedding.

One arrow spine, parameterized by the loop kind.  ``Hom`` is the grouping
of those arrows by ``(src, tgt)``; H-naturality is decided on that table,
independently of the Arr walk.  Emptying Hom while keeping Arr makes the
two sides disagree.  Deterministic, standard library only.
AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from typing import Literal

Obj = Literal["a", "b"]
Kind = Literal["id", "neg"]
Pair = tuple[bool, bool]
Arrow = tuple[str, Obj, Obj, Kind]
HomCell = tuple[Obj, Obj]
HomTable = dict[HomCell, list[Arrow]]

OBJECTS: tuple[Obj, ...] = ("a", "b")
PAIRS: tuple[Pair, ...] = ((False, True), (True, False))
ARROW_SPINE: tuple[tuple[str, Obj, Obj], ...] = (
    ("loopA", "a", "a"),
    ("loopB", "b", "b"),
    ("crossAB", "a", "b"),
    ("crossBA", "b", "a"),
)


def apply_iso(kind: Kind, pair: Pair) -> Pair:
    if kind == "neg":
        return (not pair[0], not pair[1])
    return pair


def arrows(loop_kind: Kind) -> tuple[Arrow, ...]:
    out: list[Arrow] = []
    for name, src, tgt in ARROW_SPINE:
        kind: Kind = loop_kind if src == tgt else "id"
        out.append((name, src, tgt, kind))
    return tuple(out)


def arrows_obstructed() -> tuple[Arrow, ...]:
    return arrows("neg")


def arrows_clean() -> tuple[Arrow, ...]:
    return arrows("id")


def empty_hom() -> HomTable:
    return {(s, t): [] for s in OBJECTS for t in OBJECTS}


def hom_table(arrs: tuple[Arrow, ...]) -> HomTable:
    table = empty_hom()
    for arr in arrs:
        _name, src, tgt, _kind = arr
        table[(src, tgt)].append(arr)
    return table


def hom_occupancy(hom: HomTable) -> dict[str, int]:
    return {f"{src}->{tgt}": len(hom[(src, tgt)]) for src in OBJECTS for tgt in OBJECTS}


def hom_inhabited(hom: HomTable) -> bool:
    return all(len(cell) > 0 for cell in hom.values())


def uses_neg(arrs: tuple[Arrow, ...]) -> bool:
    return any(kind == "neg" for _name, _src, _tgt, kind in arrs)


def fixed_point_free_on_carrier() -> bool:
    return all(apply_iso("neg", (b, b)) != (b, b) for b in (False, True))


def assignment_natural(arrs: tuple[Arrow, ...], section: dict[Obj, Pair]) -> bool:
    return all(apply_iso(kind, section[src]) == section[tgt] for _name, src, tgt, kind in arrs)


def assignment_h_natural(hom: HomTable, section: dict[Obj, Pair]) -> bool:
    return all(
        apply_iso(kind, section[a]) == section[b]
        for (a, b), cell in hom.items()
        for _name, _src, _tgt, kind in cell
    )


def sections() -> list[dict[Obj, Pair]]:
    out: list[dict[Obj, Pair]] = []
    for pa in PAIRS:
        for pb in PAIRS:
            out.append({"a": pa, "b": pb})
    return out


def has_natural_section(arrs: tuple[Arrow, ...]) -> bool:
    return any(assignment_natural(arrs, section) for section in sections())


def has_h_natural_section(hom: HomTable) -> bool:
    return any(assignment_h_natural(hom, section) for section in sections())


def fixture_report(name: str, arrs: tuple[Arrow, ...]) -> dict[str, object]:
    hom = hom_table(arrs)
    flat = has_natural_section(arrs)
    indexed = has_h_natural_section(hom)
    return {
        "name": name,
        "objects": list(OBJECTS),
        "arrows": [{"name": n, "src": s, "tgt": t, "iso": k} for n, s, t, k in arrs],
        "hom_occupancy": hom_occupancy(hom),
        "hom_inhabited": hom_inhabited(hom),
        "uses_negIso": uses_neg(arrs),
        "negIso_fixed_point_free_on_carrier": fixed_point_free_on_carrier(),
        "admissible_pair_count": len(PAIRS),
        "flat_natural_section": flat,
        "h_natural_section": indexed,
        "flat_and_h_agree": flat == indexed,
    }


def report() -> dict[str, object]:
    obstructed = fixture_report("obstructed", arrows_obstructed())
    clean = fixture_report("clean", arrows_clean())
    return {
        "schema": "family_embedding_fixtures/v1",
        "hom_construction": "{ f : F.Arr // F.src f = a ∧ F.tgt f = b }",
        "obstructed": obstructed,
        "clean": clean,
        "iff_on_fixtures": (
            bool(obstructed["flat_and_h_agree"]) and bool(clean["flat_and_h_agree"])
        ),
    }
