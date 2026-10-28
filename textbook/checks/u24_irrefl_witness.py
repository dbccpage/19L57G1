"""Unit 24 check: under irreflexivity a witnessed pair is distinct
(A1i implies A3). Sample computation; the proof is PrimDiff.irrefl_witness_ne.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u24_irrefl_witness.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.primdiff import (  # noqa: E402
    D2, S2, a1, a1i, a3, enumerate_pointed, implication_matrix, irreflexive,
)


def main() -> int:
    failures: list[object] = []
    for name, s in (("D2", D2), ("S2", S2)):
        print(f"{name}: rel {sorted(s.rel)}, a {s.a}, b {s.b}; a1i {a1i(s)}, a3 {a3(s)}")
        if not (a1i(s) and a3(s)):
            failures.append(name)
    m = implication_matrix(3)
    art = json.loads((ROOT / "artifacts" / "primdiff.json").read_text())
    print(f"A1i->A3 {m['implications']['A1i->A3']}; A3->A1i {m['implications']['A3->A1i']}; "
          f"artifact A1i->A3 {art['implication_matrix']['implications']['A1i->A3']}")
    if m["implications"]["A1i->A3"] is not True or m["implications"]["A3->A1i"] is not False:
        failures.append("matrix")
    total = 0
    for n in range(1, 4):
        for s in enumerate_pointed(n):
            if a1i(s):
                total += 1
                if s.a == s.b:
                    failures.append(("a1i with a=b", s.json()))
    print(f"structures with carrier <= 3 satisfying A1i: {total}, every one with a != b")
    two = art["two_element"]["minimal_carrier_by_axiom_set"]
    print(f"minimal carrier by axiom set (artifact): {two}")
    if two != {"bare": 1, "irreflexive": 2, "irreflexive+symmetric": 2}:
        failures.append("carrier")
    # the hypothesis does work: a1 alone does not give a3 (Unit 23)
    print(f"A1->A3 {m['implications']['A1->A3']}")
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
