"""Unit 32 check: reading F adds one case to the mu2 uniqueness proof, and
the mention lemma kills it.

Sample computation within Genesis's declared bounds; the grammar-wide
proof is MinimalityF.mu2_unique_F. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u32_minimality_f.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.candidates import (  # noqa: E402
    Bounds, NewForm, NewInst, apply_delta, min_responses, mu2, response_valid_naive,
)
from derivation.engine import GENESIS_F, GENESIS_L, delta_label  # noqa: E402
from derivation.iso import isomorphic  # noqa: E402
from derivation.model import AdmitDatum, Impose, replay  # noqa: E402
from derivation.observe import collapsed_pairs, separable  # noqa: E402


def main() -> int:
    failures: list[object] = []
    for name, hist, target in (("L", GENESIS_L, (0, 1)), ("F", GENESIS_F, (1, 2))):
        base = replay((*hist, Impose(*target)))
        marks = [(NewForm(1), NewInst(0, (x,))) for x in range(base.n_data())]
        verdicts = [(x, response_valid_naive(base, target, d)) for x, d in enumerate(marks)]
        print(f"reading {name}: {base.n_data()} data, target {target}; "
              f"unary-mark deltas by marked datum: {verdicts}")
        valid = [x for x, ok in verdicts if ok]
        if name == "L" and valid != [0, 1]:
            failures.append("L marks")
        if name == "F" and valid != [1, 2]:
            failures.append("F marks")
        mr = min_responses(base, target, "mu2", Bounds(2, 2))
        res = [apply_delta(base, d) for d in mr.deltas]
        if any(set(r.reqs) != {target} for r in res):
            failures.append(("demand store", name))
        print(f"  mu2 minimum {mr.cost}: {[delta_label(base, d) for d in mr.deltas]}, "
              f"mu2 {[mu2(d) for d in mr.deltas]}, all isomorphic: "
              f"{all(isomorphic(res[0], r) for r in res)}")
        if mr.cost != (2, 1) or len(mr.deltas) != 2 or not all(isomorphic(res[0], r) for r in res):
            failures.append(("minimum", name))

    base = replay((*GENESIS_F, Impose(1, 2)))
    gm = apply_delta(base, (NewForm(1), NewInst(0, (0,))))
    print(f"F, the mark on the genesis datum 0: collapsed pairs {collapsed_pairs(gm)}; "
          f"separable(0, 1) {separable(gm, 0, 1)}, separable(1, 2) {separable(gm, 1, 2)}")
    if (1, 2) not in collapsed_pairs(gm) or not separable(gm, 0, 1):
        failures.append("genesis mark")
    # The exercise's four-datum variant is a finite check, not mu2_unique_F.
    g = replay([*(AdmitDatum(t) for t in ("spare0", "spare1", "a", "b")), Impose(2, 3)])
    verdicts = [response_valid_naive(g, (2, 3), (NewForm(1), NewInst(0, (x,))))
                for x in range(4)]
    print(f"four-datum exercise, marked indices 0,1,2,3: {verdicts}")
    if verdicts != [False, False, True, True]:
        failures.append("four-datum marks")
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
