"""Unit 05 check: the shared carrier is an admission.

Checks:
  1. `correspondence_matters`: `[p1, p2]` knows `q3` on `range(3)`, while
     re-indexing `p2` by swapping 0 and 1 breaks `knows`;
  2. `knows_rename`: over all permutations of `range(3)`, all families of at
     most two partitions, and all partitions as the claim, simultaneous
     renaming leaves `knows` unchanged;
  3. `correspondence_checks` from `two_theorems`: faithfulness of the constant
     map, `faithful_actor_iff`, `sharp_pullback_iff`, and
     `fiberConstant_of_sharp_pullback`.
The proofs for every carrier are the Lean. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i05_correspondence.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import _tree  # noqa: F401
from model import P1, P2, Q3, examples, knows, partitions  # noqa: E402

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


def rename_table(t: tuple[int, ...], inv_perm: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(t[inv_perm[x]] for x in range(len(t)))


def main() -> int:
    corr = examples()["correspondence_matters"]
    print(f"correspondence_matters (knows before swap, knows after swap): {corr}")

    parts = partitions(3)
    families = [()] + [(p,) for p in parts] + list(itertools.combinations(parts, 2))
    rename_checked = 0
    rename_bad = 0
    for perm in itertools.permutations(range(3)):
        inv = [0, 0, 0]
        for i, p_i in enumerate(perm):
            inv[p_i] = i
        inv_t = tuple(inv)
        for fam in families:
            fam_ren = tuple(rename_table(p, inv_t) for p in fam)
            for q in parts:
                q_ren = rename_table(q, inv_t)
                rename_checked += 1
                if knows(3, fam, q) != knows(3, fam_ren, q_ren):
                    rename_bad += 1
    print(f"knows_rename cases checked: {rename_checked}; disagreements: {rename_bad}")

    tt_model = load_two_theorems_model()
    D3 = (0, 1, 2)
    pool3 = [
        tt_model.Table({x: x % 2 for x in D3}),
        tt_model.Table({x: x // 2 for x in D3}),
        tt_model.Table({x: (x == 1) * 1 for x in D3}),
    ]
    tt_corr = tt_model.correspondence_checks(D3, pool3, 2)
    print(f"two_theorems correspondence_checks on D=(0,1,2): {tt_corr}")

    ok = (
        corr == [True, False]
        and rename_bad == 0
        and tt_corr["constant_faithful"] is False
        and tt_corr["constant_collapses_all"] is True
        and tt_corr["empty_actor_constant"] is True
        and tt_corr["faithful_actor_mismatch"] == 0
        and tt_corr["sharp_pullback_mismatch"] == 0
        and tt_corr["fiber_constant_violation"] == 0
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
