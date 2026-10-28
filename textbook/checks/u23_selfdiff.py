"""Unit 23 check: bare assertion is consistent with identity (A1 does not
imply A3). Sample computation over Genesis's pointed structures; the proof
is PrimDiff.selfdiff_consistent. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u23_selfdiff.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.primdiff import (  # noqa: E402
    Pointed, a1, a1i, a3, enumerate_pointed, implication_matrix, irreflexive,
)


def main() -> int:
    failures: list[object] = []
    one = Pointed(1, frozenset({(0, 0)}), 0, 0)
    sym = all((y, x) in one.rel for (x, y) in one.rel)
    print(f"one point, self-pair asserted: a1 {a1(one)}, a3 {a3(one)}, "
          f"irreflexive {irreflexive(one.rel)}, a1i {a1i(one)}, symmetric {sym}")
    if not (a1(one) and not a3(one) and not irreflexive(one.rel) and sym):
        failures.append("countermodel")
    m = implication_matrix(3)
    art = json.loads((ROOT / "artifacts" / "primdiff.json").read_text())["implication_matrix"]
    for key in ("A1->A3", "A1->A1i"):
        print(f"{key}: {m['implications'][key]}; countermodel {m['countermodels'][key]['structure']}; "
              f"artifact {art['countermodels'][key]['structure']}")
        same = json.loads(json.dumps(m["countermodels"][key])) == art["countermodels"][key]
        if m["implications"][key] is not False or not same:
            failures.append(key)
    print(f"A1i->A3: {m['implications']['A1i->A3']} (Unit 24)")
    counts = {}
    for n in range(1, 4):
        for s in enumerate_pointed(n):
            if a1(s) and not a3(s):
                counts[n] = counts.get(n, 0) + 1
    print(f"A1 without A3 by carrier size: {counts} (every one has a = b)")
    bad = [s for n in range(1, 4) for s in enumerate_pointed(n) if a1(s) and not a3(s) and s.a != s.b]
    if bad or sum(counts.values()) != 785:
        failures.append(("a1 not a3", sum(counts.values()), len(bad)))
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
