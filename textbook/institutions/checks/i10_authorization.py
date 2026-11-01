"""Unit 10 check: scoped authorization and the five-link chain.

Checks:
  1. On range(3), empty/singleton families and one ordering of each distinct
     partition pair, with all 27 report tables: knows(3, Q, s) holds iff
     `residuals(3, Q, s)` is empty (`scoped_sound_refuses_residual` for
     `knowsB`), and `knows` authorizes both `(0, 0, 0)` and `(1, 1, 1)` on
     every selected Q (authorization_not_correctness). Not all ordered lists
     or arbitrary scoped-sound rules;
  2. `reports_do_not_certify` and `grounded_here_not_there` from
     `two_theorems/model.py`.
The proofs for every carrier are the Lean. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i10_authorization.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import _tree  # noqa: F401
from model import knows, partitions, residuals  # noqa: E402

TWO_THEOREMS = Path(__file__).resolve().parents[3] / "research" / "two_theorems"


def load_two_theorems_model():
    saved = sys.modules.get("model")
    sys.path.insert(0, str(TWO_THEOREMS))
    try:
        del sys.modules["model"]
        import model as tt_model  # type: ignore[no-redef]
        return tt_model
    finally:
        sys.path.pop(0)
        if saved is not None:
            sys.modules["model"] = saved


def main() -> int:
    parts = partitions(3)
    fams = [()] + [(p,) for p in parts] + list(itertools.combinations(parts, 2))
    claims = list(itertools.product(range(3), repeat=3))
    checked = 0
    bad = 0
    c0 = (0, 0, 0)
    c1 = (1, 1, 1)
    for Q in fams:
        if not (knows(3, Q, c0) and knows(3, Q, c1)):
            bad += 1
        for s in claims:
            checked += 1
            has_res = len(residuals(3, Q, s)) > 0
            if knows(3, Q, s) != (not has_res):
                bad += 1
    print(f"(Q, s) authorization/residual pairs checked: {checked}; violations: {bad}")

    tt_model = load_two_theorems_model()
    D3 = (0, 1, 2)
    pool3 = [
        tt_model.Table({x: x % 2 for x in D3}),
        tt_model.Table({x: x // 2 for x in D3}),
        tt_model.Table({x: (x == 1) * 1 for x in D3}),
        tt_model.Table({x: 0 for x in D3}),
    ]
    gc = tt_model.grounding_checks(D3, pool3, 2)
    print(
        f"reports_do_not_certify: {gc['reports_do_not_certify']}; "
        f"grounded_here_not_there: {gc['grounded_here_not_there']}"
    )

    ok = (
        bad == 0
        and gc["reports_do_not_certify"] is True
        and gc["grounded_here_not_there"] is True
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
