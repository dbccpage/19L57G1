"""Unit 56 check: apartness, indistinguishability and the retained orientation.

Runs Genesis's mirror `code/derivation/apartness.py`: the equivalence
theorem exhaustively on every relation of carriers 1-3, the three
insufficiency countermodels and their minimality, the orientation
separation, and the preservation censuses to carrier 4, against
`artifacts/apartness.json`. Python (book): which clause of the equivalence
each dropped law breaks, over every relation on carriers 1-3 (the
"spent at exactly one clause" reading, checked as a census), and the
`n^(n-2)` count of oriented preservers as a formula.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u56_apartness.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.apartness import (  # noqa: E402
    all_endofunctions, all_relations, equivalence_theorem_exhaustive, indist,
    indist_is_equivalence, insufficiency_countermodels, is_apart, is_cotrans,
    is_irrefl, is_symm, operation_censuses, orientation_separation,
    preserves_apart, preserves_oriented, sym_closure,
)


def clauses(n: int, r: frozenset[tuple[int, int]]) -> tuple[bool, bool, bool]:
    """Python (book): the three clauses of the equivalence, separately."""
    refl = all(indist(r, x, x) for x in range(n))
    symm = all((not indist(r, x, y)) or indist(r, y, x)
               for x in range(n) for y in range(n))
    trans = all((not (indist(r, x, y) and indist(r, y, z))) or indist(r, x, z)
                for x in range(n) for y in range(n) for z in range(n))
    return refl, symm, trans


def main() -> int:
    failures: list[str] = []
    art = json.loads((ROOT / "artifacts" / "apartness.json").read_text())

    # --- the equivalence theorem, exhaustively (Lean 88-95)
    counts = {n: sum(1 for r in all_relations(n) if is_apart(n, r)) for n in (1, 2, 3)}
    print(f"apart relations per carrier: {counts}; every one has an equivalence "
          f"indistinguishability: {equivalence_theorem_exhaustive(3)}")
    if not equivalence_theorem_exhaustive(3) or counts != {1: 1, 2: 2, 3: 5}:
        failures.append("equivalence exhaustive")

    # Python (book): which clause each law buys. For every relation on 1-3
    # points: irreflexive <-> reflexive clause; with irreflexivity, symmetric
    # -> symmetric clause; with both, cotransitive -> transitive clause.
    law_buys = {"irrefl<->refl": True, "symm->symm": True, "cotrans->trans": True,
                "not_symm_breaks_symm": 0, "not_cotrans_breaks_trans": 0}
    for n in (1, 2, 3):
        for r in all_relations(n):
            refl, symm, trans = clauses(n, r)
            law_buys["irrefl<->refl"] &= (is_irrefl(n, r) == refl)
            if is_irrefl(n, r):
                law_buys["symm->symm"] &= (not is_symm(n, r)) or symm
                if not is_symm(n, r) and not symm:
                    law_buys["not_symm_breaks_symm"] += 1
                if is_symm(n, r):
                    law_buys["cotrans->trans"] &= (not is_cotrans(n, r)) or trans
                    if not is_cotrans(n, r) and not trans:
                        law_buys["not_cotrans_breaks_trans"] += 1
    print(f"Python (book) clause census over carriers 1-3: {law_buys}")
    if not (law_buys["irrefl<->refl"] and law_buys["symm->symm"]
            and law_buys["cotrans->trans"]):
        failures.append("clause census")

    # --- the countermodels (Lean 101-164)
    cm = insufficiency_countermodels()
    bare, d2, tri = frozenset({(0, 0)}), frozenset({(0, 1)}), frozenset({(0, 1), (1, 0)})
    print(f"bare {set(bare)} on 1 point: indist(0,0)={indist(bare, 0, 0)}")
    print(f"D2 {set(d2)} on 2 points: irrefl={is_irrefl(2, d2)} symm={is_symm(2, d2)} "
          f"indist(1,0)={indist(d2, 1, 0)} indist(0,1)={indist(d2, 0, 1)}")
    print(f"tri {set(tri)} on 3 points: irrefl={is_irrefl(3, tri)} symm={is_symm(3, tri)} "
          f"cotrans={is_cotrans(3, tri)} indist(0,2)={indist(tri, 0, 2)} "
          f"indist(2,1)={indist(tri, 2, 1)} indist(0,1)={indist(tri, 0, 1)}")
    print(f"insufficiency_countermodels(): {cm}")
    if cm != art["insufficiency"] or not all(cm.values()):
        failures.append("countermodels")

    # --- the orientation separation (Lean 170-219)
    ori = orientation_separation()
    print(f"Sym D2 = {set(sym_closure(d2))} = Sym D2rev: {ori['same_apartness']}; "
          f"D2 != D2rev: {ori['orientations_differ']}; swap moves (0,1): "
          f"{ori['swap_moves_retained_witness']}; S2 is apart: {ori['apartness_is_apart']}")
    if ori != art["orientation"] or not all(ori.values()):
        failures.append("orientation")

    # --- the censuses (Lean 226-335)
    ops = operation_censuses(4)
    fs2 = all_endofunctions(2)
    table = [(f, preserves_oriented(f, 0, 1), preserves_apart(f, 0, 1)) for f in fs2]
    print("the four operations on two points (f(0), f(1)) -> oriented, apart:")
    for f, o, a in table:
        print(f"  {f}: {o!s:5} {a}")
    print(f"per carrier: {ops['per_carrier']}")
    formula = all(ops["per_carrier"][str(n)]["oriented_preservers"] == n ** (n - 2)
                  and ops["per_carrier"][str(n)]["apart_preservers"] == 2 * n ** (n - 2)
                  for n in (2, 3, 4))
    print(f"Python (book): oriented preservers = n^(n-2) and apart preservers = 2 n^(n-2) "
          f"on carriers 2-4: {formula}")
    if ops != art["operations"] or not formula:
        failures.append("censuses")
    if table != [((0, 0), False, False), ((0, 1), True, True),
                 ((1, 0), False, True), ((1, 1), False, False)]:
        failures.append("two-point table")

    print(f"artifact bounds: {art['bounds']}; equivalence_exhaustive: {art['equivalence_exhaustive']}")
    if art["bounds"] != {"census_max_carrier": 4, "equivalence_exhaustive_max_carrier": 3}:
        failures.append("bounds")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
