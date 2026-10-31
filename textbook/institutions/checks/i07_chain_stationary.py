"""Unit 07 check: finite extension chains have a stationary step; nesting.

Checks:
  1. `chain_check(3)`: 32 starting partition subsets times 5^3 addition
     sequences. Each step adds one absent partition or retains the family;
     cases can repeat the same four-stage chain. A three-stage strict case
     is also sought;
  2. Empty/singleton families and one ordering of each distinct partition
     pair on range(3), appending one partition: test the stationary cases
     and known partition questions. Not all stationary extension steps;
  3. `nest_checks` on `D = (0, 1, 2, 3)` from `two_theorems/model.py`.
The proofs for every carrier are the Lean. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i07_chain_stationary.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import _tree  # noqa: F401
from model import chain_check, information, knows, partitions  # noqa: E402

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
    cc = chain_check(3)
    print(f"chain_check(3): {cc}")

    parts = partitions(3)
    fams = [()] + [(p,) for p in parts] + list(itertools.combinations(parts, 2))
    stat_steps = 0
    stat_bad = 0
    for Q in fams:
        for p in parts:
            Qp = Q + (p,)
            if information(3, Qp) == information(3, Q):
                stat_steps += 1
                if not knows(3, Q, p):
                    stat_bad += 1
                for q in parts:
                    if knows(3, Qp, q) != knows(3, Q, q):
                        stat_bad += 1
    print(f"stationary steps checked: {stat_steps}; disagreements: {stat_bad}")

    tt_model = load_two_theorems_model()
    D4 = (0, 1, 2, 3)
    pool4 = [
        tt_model.Table({x: x % 2 for x in D4}),
        tt_model.Table({x: x // 2 for x in D4}),
        tt_model.Table({x: (x == 1) * 1 for x in D4}),
        tt_model.Table({x: 0 for x in D4}),
    ]
    nest = tt_model.nest_checks(D4, pool4, 2)
    print(f"two_theorems nest_checks on D=(0,1,2,3): {nest}")

    constant = (0, 0, 0)
    p = (0, 0, 1)
    q = (0, 1, 1)
    plateau_chain = ((), (constant,), (constant, p), (constant, p, q))
    plateau_counts = [information(3, family) for family in plateau_chain]
    print(f"a stationary step followed by later growth: {plateau_counts}")
    ok = (
        plateau_counts == [1, 1, 2, 3]
        and cc["chains"] == 4000
        and cc["violations"] == 0
        and cc["shorter_chain_without_stationary_step"] is True
        and stat_bad == 0
        and nest["knows_violations"] == 0
        and nest["information_violations"] == 0
        and nest["collapse_violations"] == 0
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
