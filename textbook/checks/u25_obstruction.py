"""Unit 25 check: collapsing a witnessed pair collides, and is obstructed
exactly relative to the protected law. Runs Genesis's collapse_report and
the D2 merge by hand. The proof is PrimDiff.obstruction_under_irrefl.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u25_obstruction.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.primdiff import (  # noqa: E402
    D2, Pointed, a1, collapse_report, collision, enumerate_pointed, irreflexive,
    merge_map, pushforward, transpose,
)


def main() -> int:
    failures: list[object] = []
    f = merge_map(2, 0, 1)
    pushed = pushforward(D2.rel, f)
    print(f"merge of D2's two points: map {f}, pushforward {sorted(pushed)}, "
          f"collision {collision(D2.rel, f)}, pushforward irreflexive {irreflexive(pushed)}, "
          f"pushforward carries the pair: {(f[D2.a], f[D2.b]) in pushed}")
    if not collision(D2.rel, f) or irreflexive(pushed) or (f[D2.a], f[D2.b]) not in pushed:
        failures.append("D2 merge")
    ident = (0, 1)
    print(f"identity on D2: collision {collision(D2.rel, ident)}")
    # a relation that is not irreflexive still collides when its witnessed pair is merged
    self_rel = Pointed(2, frozenset({(0, 1), (1, 1)}), 0, 1)
    print(f"non-irreflexive relation {sorted(self_rel.rel)} merged: collision {collision(self_rel.rel, f)}")
    if not collision(self_rel.rel, f) or collision(D2.rel, ident):
        failures.append("premise")
    rep = collapse_report(3)
    art = json.loads((ROOT / "artifacts" / "primdiff.json").read_text())["collapse"]
    print(f"collapse_report(3): {rep}")
    if rep != art:
        failures.append("artifact")
    # the law is what makes it an obstruction: count merges that collide vs those whose
    # pushforward exists (all of them)
    collide = exist = 0
    for n in range(1, 4):
        for s in enumerate_pointed(n):
            for x in range(n):
                for y in range(x + 1, n):
                    g = merge_map(n, x, y)
                    exist += 1
                    if a1(s) and g[s.a] == g[s.b]:
                        collide += collision(s.rel, g)
                        assert collision(s.rel, g) == collision(transpose(s.rel), g)
    print(f"merges with the witnessed pair identified: {collide} collide; pushforwards that exist: {exist} of {exist}")
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
