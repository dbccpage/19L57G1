"""Unit 21 check: the mu1 minimum is not unique.

Runs Genesis's own enumeration (declared bounds: 2 items, arity 2) and its
implemented isomorphism. Sample computation, not a proof; the proofs are
mu1_minimum_not_unique, U0_not_iso_BL, BL_not_iso_BD, markK_pairwise_noniso.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u21_mu1_not_unique.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.candidates import Bounds, NewForm, NewInst, apply_delta, min_responses  # noqa: E402
from derivation.engine import GENESIS_F, GENESIS_L, delta_label  # noqa: E402
from derivation.iso import canonical, group_by_canonical, isomorphic  # noqa: E402
from derivation.model import Impose, replay, step  # noqa: E402


def main() -> int:
    failures: list[object] = []
    art = json.loads((ROOT / "artifacts" / "challenges.json").read_text())["challenge3"]
    for name, hist, target in (("L", GENESIS_L, (0, 1)), ("F", GENESIS_F, (1, 2))):
        base = replay(hist)
        mr = min_responses(base, target, "mu1", Bounds(2, 2))
        # classes are taken with the demand recorded, as the engine does: the
        # isomorphism must carry the required pair to the required pair
        results = [step(apply_delta(base, d), Impose(*target)) for d in mr.deltas]
        groups = group_by_canonical(zip(results, mr.deltas))
        labels = sorted({delta_label(base, d) for d in mr.deltas})
        print(f"reading {name}: mu1 minimum {mr.cost}, {len(mr.deltas)} deltas, "
              f"{len(groups)} isomorphism classes; labels {labels}")
        for d in mr.deltas:
            print(f"  {delta_label(base, d):16} {d}")
        want = {"L": (6, 3), "F": (10, 5)}[name]
        if (len(mr.deltas), len(groups)) != want:
            failures.append(("counts", name, len(mr.deltas), len(groups)))
        art_labels = sorted(c["label"] for c in art[name]["mu1"]["iso_classes"])
        class_labels = sorted(delta_label(base, g[0]) for g in groups.values())
        print(f"  class representatives: {class_labels}")
        if art_labels != class_labels:
            failures.append(("artifact classes", name, art_labels, class_labels))
        print(f"  artifact classes: {art_labels}")

    base = replay(GENESIS_L)
    u0 = apply_delta(base, (NewForm(1), NewInst(0, (0,))))
    u1 = apply_delta(base, (NewForm(1), NewInst(0, (1,))))
    bl = apply_delta(base, (NewForm(2), NewInst(0, (0, 1))))
    bl_rev = apply_delta(base, (NewForm(2), NewInst(0, (1, 0))))
    bd = apply_delta(base, (NewForm(2), NewInst(0, (0, 0))))
    print(f"U0 ~ U1: {isomorphic(u0, u1)}; BL ~ BL(1,0): {isomorphic(bl, bl_rev)}; "
          f"U0 ~ BL: {isomorphic(u0, bl)}; U0 ~ BD: {isomorphic(u0, bd)}; "
          f"BL ~ BD: {isomorphic(bl, bd)}")
    if not (isomorphic(u0, u1) and isomorphic(bl, bl_rev)) or isomorphic(u0, bl) \
            or isomorphic(u0, bd) or isomorphic(bl, bd):
        failures.append("classes")
    # arity invariant: the canonical key records the form arities
    print(f"canonical(U0) forms {canonical(u0)[1]}, canonical(BL) forms {canonical(bl)[1]}")

    # the infinite family: k-ary marks for k = 1..5 are valid and pairwise non-isomorphic
    marks = [apply_delta(base, (NewForm(k), NewInst(0, (1,) * k))) for k in range(1, 6)]
    from derivation.observe import separable
    seps = [separable(m, 0, 1) for m in marks]
    pair_iso = [(i + 1, j + 1) for i in range(5) for j in range(i + 1, 5)
                if isomorphic(marks[i], marks[j])]
    print(f"k-ary marks k=1..5 separate: {seps}; isomorphic pairs: {pair_iso}")
    if not all(seps) or pair_iso:
        failures.append("markK")
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
