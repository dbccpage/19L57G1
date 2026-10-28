"""Unit 28 check: the pair count and the closed-system round bound.

Computes Lean's `allPairs` in Python, checks `2 * length = n * (n - 1)`,
then runs Genesis's engine with supply disabled and checks that every
branch stops within n(n-1)/2 rounds, that each round adds exactly one
demand over a fixed datum count (the two hypotheses of
`strict_bounded_length`), and that the numbers match `artifacts/claims.json`.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u28_closure_bound.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.candidates import Bounds  # noqa: E402
from derivation.engine import READING_F, READING_L, build_tree  # noqa: E402
from derivation.observe import collapsed_pairs  # noqa: E402

BOUNDS = Bounds(max_items=2, max_arity=2)


def all_pairs(n: int) -> list[tuple[int, int]]:
    """Lean's `allPairs`: allPairs 0 = []; allPairs (n+1) = allPairs n ++
    [(i, n) for i < n]."""
    out: list[tuple[int, int]] = []
    for m in range(n):
        out += [(i, m) for i in range(m)]
    return out


def main() -> int:
    failures: list[str] = []
    print("n, allPairs n, 2*length, n*(n-1):")
    for n in range(6):
        ps = all_pairs(n)
        print(f"  {n} {ps} {2 * len(ps)} {n * (n - 1)}")
        if 2 * len(ps) != n * (n - 1):
            failures.append(f"allPairs {n}")

    claims = json.loads((ROOT / "artifacts" / "claims.json").read_text())
    rec = claims["CL-CLOSURE-TERMINATION"]
    for reading, name in ((READING_L, "L"), (READING_F, "F")):
        t = build_tree(reading, "mu1", BOUNDS, max_rounds=15,
                       pre_expansion_node_guard=200, supply=False)
        stats = t.stats()
        n = t.nodes[0].regime.n_data()
        bound = n * (n - 1) // 2
        depth = stats["max_depth"]
        print(f"reading {name}: {n} data, bound {bound}, deepest round {depth}, "
              f"statuses {stats['by_status']}")
        if not isinstance(depth, int) or depth > bound:
            failures.append(f"{name} depth")
        if "frontier_guard" in stats["by_status"]:
            failures.append(f"{name} guard")
        # the two hypotheses, edge by edge
        grow_one = data_fixed = True
        for e in t.edges:
            if e.kind != "creation":
                continue
            p, c = t.nodes[e.parent].regime, t.nodes[e.child].regime
            grow_one &= len(c.reqs) == len(p.reqs) + 1
            data_fixed &= c.n_data() == p.n_data()
        print(f"  every round adds one demand: {grow_one}; "
              f"datum count fixed: {data_fixed}")
        if not (grow_one and data_fixed):
            failures.append(f"{name} hypotheses")
        terminal = [x for x in t.nodes if x.status == "terminal_all_separated"]
        print(f"  terminal nodes {len(terminal)}, each with no collapsed pair: "
              f"{all(collapsed_pairs(x.regime) == () for x in terminal)}")
        if not terminal or any(collapsed_pairs(x.regime) != () for x in terminal):
            failures.append(f"{name} terminal")
        art = rec[name]
        print(f"  artifact: pair_bound {art['pair_bound']}, rounds_used "
              f"{art['rounds_used']}, within_bound {art['within_bound']}")
        if art["pair_bound"] != bound or art["rounds_used"] != depth:
            failures.append(f"{name} artifact")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
