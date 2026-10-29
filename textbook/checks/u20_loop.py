"""Unit 20 check: the binary self-loop separates the two data, and is not
the link.

Runs Genesis's own Python model. This is sample computation, not a proof;
the proofs are Derivation.BD_separable and BL_not_iso_BD.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u20_loop.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.candidates import (  # noqa: E402
    Bounds,
    NewForm,
    NewInst,
    NodeView,
    apply_delta,
    response_valid_fast,
)
from derivation.engine import GENESIS_L  # noqa: E402
from derivation.iso import isomorphic  # noqa: E402
from derivation.model import AdmitRuleAll, replay, step  # noqa: E402
from derivation.observe import contexts, derivable, plug, profile, separable, witness  # noqa: E402


def main() -> int:
    failures: list[object] = []
    base = replay(GENESIS_L)
    bd = apply_delta(base, (NewForm(2), NewInst(0, (0, 0))))
    bl = apply_delta(base, (NewForm(2), NewInst(0, (0, 1))))
    print(f"BD: forms={bd.forms} insts={sorted(bd.insts)}")

    # 1. Which contexts witness the loop.
    witnesses = []
    for c in contexts(bd):
        d0, d1 = derivable(bd, plug(c, 0)), derivable(bd, plug(c, 1))
        print(f"  {c}: plug 0 -> {plug(c, 0)} {d0}; plug 1 -> {plug(c, 1)} {d1}"
              f"{'  <- witness' if d0 != d1 else ''}")
        if d0 != d1:
            witnesses.append(c)
    print(f"witnesses: {witnesses}; Genesis's witness(): {witness(bd, 0, 1)}; "
          f"Lean's: (0, (None, 0))")
    if (witnesses != [(0, (None, None)), (0, (None, 0)), (0, (0, None))]
            or (0, (None, 0)) not in witnesses):
        failures.append("witnesses")
    print(f"profile(0)={sorted(profile(bd, 0), key=str)} profile(1)="
          f"{sorted(profile(bd, 1), key=str)}")

    # 2. The link's witness is not the loop's and the two-hole context
    # separates the loop but not the link.
    c_link, c_two = (0, (None, 1)), (0, (None, None))
    link_on_bd = derivable(bd, plug(c_link, 0)) != derivable(bd, plug(c_link, 1))
    two_on_bl = derivable(bl, plug(c_two, 0)) != derivable(bl, plug(c_two, 1))
    print(f"(0,(None,1)) separates BD: {link_on_bd}; (0,(None,None)) "
          f"separates BL: {two_on_bl}")
    if link_on_bd or two_on_bl:
        failures.append("cross")

    # 3. Valid response; the loop on datum 1 is its mirror image.
    view = NodeView.of(base)
    for d in ((NewForm(2), NewInst(0, (0, 0))), (NewForm(2), NewInst(0, (1, 1)))):
        if not response_valid_fast(view, (0, 1), d):
            failures.append(("valid", d))
    bd1 = apply_delta(base, (NewForm(2), NewInst(0, (1, 1))))
    print(f"isomorphic(BD, loop on 1): {isomorphic(bd, bd1)}; "
          f"isomorphic(BL, BD): {isomorphic(bl, bd)}")
    if not isomorphic(bd, bd1) or isomorphic(bl, bd):
        failures.append("iso")

    uniform = step(bd, AdmitRuleAll(0))
    print(f"uniform rule retains loop={uniform.insts == bd.insts}; "
          f"separable={separable(uniform, 0, 1)}")
    if uniform.insts != bd.insts or separable(uniform, 0, 1):
        failures.append("mention alone is not sufficient")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
