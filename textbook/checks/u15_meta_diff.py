"""Unit 15 check: metatheoretic inequality without an asserted pair.

Runs Genesis's own Python enumeration of pointed structures. This is sample
computation, not a proof; the proof is PrimDiff.meta_diff_without_assertion.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u15_meta_diff.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.primdiff import (  # noqa: E402
    Pointed,
    a1,
    a1i,
    a3,
    enumerate_pointed,
    implication_matrix,
    irreflexive,
)


def main() -> int:
    failures: list[object] = []
    empty = Pointed(2, frozenset(), 0, 1)
    print(f"empty relation on two points: a3 {a3(empty)}, a1 {a1(empty)}, "
          f"irreflexive {irreflexive(empty.rel)}, a1i {a1i(empty)}")
    if not (a3(empty) and not a1(empty) and irreflexive(empty.rel)):
        failures.append("countermodel")

    d2 = Pointed(2, frozenset({(0, 1)}), 0, 1)
    print(f"D2, same points with the pair asserted: a1 {a1(d2)}, a3 {a3(d2)}")

    a3_not_a1 = a1_not_a3 = 0
    for n in range(1, 4):
        for s in enumerate_pointed(n):
            if a3(s) and not a1(s):
                a3_not_a1 += 1
            if a1(s) and not a3(s):
                a1_not_a3 += 1
    print(f"carrier <= 3: A3 without A1 in {a3_not_a1} structures; "
          f"A1 without A3 in {a1_not_a3} (Unit 23's direction)")
    if a3_not_a1 == 0:
        failures.append("no A3-not-A1")

    m = implication_matrix(3)
    art = json.loads((ROOT / "artifacts" / "primdiff.json").read_text())["implication_matrix"]
    cm = m["countermodels"]["A3->A1"]
    print(f"A3->A1: {m['implications']['A3->A1']}; recorded countermodel {cm['structure']} "
          f"(artifact {art['countermodels']['A3->A1']['structure']})")
    if m["implications"]["A3->A1"] is not False or cm != art["countermodels"]["A3->A1"]:
        failures.append("artifact")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
