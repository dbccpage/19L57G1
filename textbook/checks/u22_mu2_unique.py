"""Unit 22 check: under mu2 the minimum is the unary mark, up to isomorphism.

Sample computation within Genesis's declared bounds; the grammar-wide proof
is mu2_unique (reading L) and mu2_unique_F. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u22_mu2_unique.py
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.candidates import (  # noqa: E402
    Bounds, NewDatum, NewForm, NewInst, NewRuleAll, apply_delta,
    min_responses, mu2, response_valid_naive,
)
from derivation.engine import GENESIS_F, GENESIS_L, delta_label  # noqa: E402
from derivation.iso import isomorphic  # noqa: E402
from derivation.model import AdmissionError, replay  # noqa: E402


def items(n_data: int, max_arity: int):
    yield NewDatum()
    for a in range(1, max_arity + 1):
        yield NewForm(a)
    for f in range(2):
        yield NewRuleAll(f)
        for a in range(1, max_arity + 1):
            for args in itertools.product(range(n_data + 1), repeat=a):
                yield NewInst(f, args)


def main() -> int:
    failures: list[object] = []
    art = json.loads((ROOT / "artifacts" / "challenges.json").read_text())["challenge3"]
    for name, hist, target in (("L", GENESIS_L, (0, 1)), ("F", GENESIS_F, (1, 2))):
        base = replay(hist)
        mr = min_responses(base, target, "mu2", Bounds(2, 2))
        print(f"reading {name}: mu2 minimum {mr.cost}; deltas "
              f"{[delta_label(base, d) for d in mr.deltas]}")
        res = [apply_delta(base, d) for d in mr.deltas]
        allsame = all(isomorphic(res[0], r) for r in res)
        print(f"  all minima isomorphic: {allsame}; artifact minimum {art[name]['mu2']['minimum_cost']}, "
              f"classes {[c['label'] for c in art[name]['mu2']['iso_classes']]}")
        if mr.cost != (2, 1) or not allsame or art[name]["mu2"]["minimum_cost"] != [2, 1]:
            failures.append(("minimum", name))
        # every two-item delta over a generous grammar slice: those valid with arity sum <= 1
        n = base.n_data()
        cheap_valid = []
        zero_valid = []
        for a, b in itertools.product(list(items(n, 3)), repeat=2):
            d = (a, b)
            try:
                ok = response_valid_naive(base, target, d)
            except AdmissionError:
                ok = False
            if ok:
                s = mu2(d)[1]
                if s == 0:
                    zero_valid.append(d)
                if s <= 1:
                    cheap_valid.append(d)
        mark = apply_delta(base, (NewForm(1), NewInst(0, (target[1],))))
        iso_all = all(isomorphic(apply_delta(base, d), mark) for d in cheap_valid)
        print(f"  two-item deltas over a 3-arity slice: {len(cheap_valid)} valid with arity sum <= 1, "
              f"all isomorphic to the unary mark: {iso_all}; valid with arity sum 0: {len(zero_valid)}")
        if not iso_all or zero_valid or not cheap_valid:
            failures.append(("grammar slice", name))
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
