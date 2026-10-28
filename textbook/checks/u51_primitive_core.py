"""Unit 51 check: nine readings of one difference, the 72-cell matrix.

Runs Genesis's finite scan in `code/derivation/primitive_core.py` over
every Setting on carriers of one, two and three points (with the declared
store and operation choices), evaluates the nine candidate readings on
each, prints the 9 x 9 matrix with the status Lean assigns to each cell,
checks the tally 17 / 51 / 4, the key-minimal witnesses of the cells the
lesson teaches, the absence of any A-but-not-Bc setting on two or fewer
points (Lean `cotrans_auto_on_two`), the two-element classification, and
the two artifacts.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u51_primitive_core.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation import primitive_core as P  # noqa: E402


def show(s: P.Setting) -> str:
    return (f"n={s.n} r={sorted(s.r)} a={s.a} b={s.b} ret={sorted(s.ret)} "
            f"prot={sorted(s.prot)} ops={len(s.ops)}")


def main() -> int:
    failures: list[str] = []
    scan = P.scan_settings()
    report = P.matrix_report(scan)
    cands = P.candidates_payload(scan)
    print(f"settings scanned: {scan.total}; candidate extents {scan.counts}")

    print("the matrix (row = source, column = target; I implies, C countermodel, O open):")
    names = list(P.CANDIDATES)
    print("      " + " ".join(f"{q:>3}" for q in names))
    counts = {"IMPLIES": 0, "COUNTERMODEL": 0, "OPEN_LOCATED": 0}
    cells = report["cells"]
    assert isinstance(cells, dict)
    for p in names:
        row = []
        for q in names:
            if p == q:
                row.append("  .")
                continue
            st = cells[f"{p}->{q}"]["status"]
            counts[st] += 1
            row.append(f"{'I' if st == 'IMPLIES' else 'C' if st == 'COUNTERMODEL' else 'O':>3}")
        print(f"  {p:>3} " + " ".join(row))
    print(f"  tally {counts}; expected_equals_computed {report['expected_equals_computed']}")
    if counts != {"IMPLIES": 17, "COUNTERMODEL": 51, "OPEN_LOCATED": 4} or not report["expected_equals_computed"]:
        failures.append("tally")

    print("the cells the lesson teaches, with the key-minimal witness found by the scan and Lean's name:")
    teach = ["W->D", "A->D", "C->A", "C->D", "E->D", "D->E", "A->E", "A->Bc", "Bs->Bc", "A->Bs", "A->C", "A->F", "F->C", "D->W", "E->W"]
    for cell in teach:
        c = cells[cell]
        w = scan.witnesses[cell]
        print(f"  {cell:>6}: {c['status']:<12} {c['lean']:<12} " + (show(w) if w is not None else "(implication)"))
        if c["lean"] != P.lean_tag(cell, c["status"]):
            failures.append(f"tag {cell}")
    for cell in sorted(P.EXPECTED_OPEN):
        print(f"  {cell:>6}: {cells[cell]['status']:<12} {cells[cell]['lean']:<12} no finite countermodel can exist (every finite decidable relation is located)")
        if scan.witnesses[cell] is not None:
            failures.append(f"open {cell}")

    print("cotransitivity first bites at three points:")
    abc = scan.witnesses["A->Bc"]
    print(f"  any A-but-not-Bc setting on at most two points: {scan.cotrans_violation_le2}; "
          f"the key-minimal A->Bc witness has n = {abc.n if abc else None}")
    if scan.cotrans_violation_le2 or abc is None or abc.n != 3:
        failures.append("cotrans")
    tri = P.Setting(3, frozenset({(0, 1)}), 0, 1, frozenset(), frozenset(), frozenset())
    ev = P.evaluate(tri)
    print(f"  Lean's `tri` evaluated: {ev}")
    if not (ev["A"] and not ev["Bc"] and ev["D"] and ev["E"] and not ev["C"]):
        failures.append("tri")

    print("Lean's one- and two-point models evaluated:")
    models = {
        "unitBare": P.Setting(1, frozenset({(0, 0)}), 0, 0, frozenset(), frozenset(), frozenset()),
        "unitFull": P.Setting(1, frozenset({(0, 0)}), 0, 0, frozenset({(0, 0)}), frozenset({(0, 0)}), frozenset()),
        "d2Bare": P.Setting(2, frozenset({(0, 1)}), 0, 1, frozenset(), frozenset(), frozenset()),
        "d2Merged": P.Setting(2, frozenset({(0, 1)}), 0, 1, frozenset(), frozenset(), P.ops_family("const_0", 2)),
        "s2Bare": P.Setting(2, frozenset({(0, 1), (1, 0)}), 0, 1, frozenset(), frozenset(), frozenset()),
        "boolEmpty": P.Setting(2, frozenset(), 0, 1, frozenset(), frozenset(), frozenset()),
    }
    want = {
        "unitBare": {"W": True, "A": False, "C": False, "D": False, "E": False},
        "unitFull": {"C": True, "A": False, "D": False},
        "d2Bare": {"A": True, "Bs": False, "Bc": True, "C": False, "D": True, "E": True, "F": False},
        "d2Merged": {"A": True, "E": False},
        "s2Bare": {"Bs": True, "C": False, "F": False},
        "boolEmpty": {"W": False, "D": True, "E": True},
    }
    for name, s in models.items():
        ev = P.evaluate(s)
        ok = all(ev[k] == v for k, v in want[name].items())
        print(f"  {name:>10}: " + " ".join(f"{k}={'T' if ev[k] else 'F'}" for k in names) + f"  as Lean proves: {ok}")
        if not ok:
            failures.append(name)

    tec = P.two_element_classification()
    print(f"two-element classification: survivors {tec['survivors']} (count {tec['survivor_count']})")
    if tec["survivor_count"] != 2:
        failures.append("bool_class")

    art_m = json.loads((ROOT / "artifacts" / "primitive_implication_matrix.json").read_text())
    art_c = json.loads((ROOT / "artifacts" / "primitive_candidates.json").read_text())
    print(f"artifacts: matrix equals {report == art_m}; candidates equals {cands == art_c}; "
          f"Bl equals A in the finite universe: {art_c['bl_equals_a_in_finite_universe']}")
    if report != art_m or cands != art_c:
        failures.append("artifact")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
