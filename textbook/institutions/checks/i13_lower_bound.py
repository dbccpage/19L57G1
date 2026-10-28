"""Unit 13 check: the probe lower bound and the merge adversary.

Checks:
  1. Unpromised minimax `game_value` on `range(n)` for `n = 1..4` equals
     `n * (n - 1) // 2` (`0, 1, 3, 6`);
  2. For every subset of fewer than 6 pairs on `range(4)`, the uncovered pair
     `(x, y)` yields `merge(x, y)` agreeing with `id` on all probed pairs while
     merging `(x, y)`;
  3. `cannot_read_checks` from `two_theorems/model.py` on `D = (0, 1, 2)`
     (`m = 1`) and `D = (0, 1, 2, 3)` (`m = 2`).
The proofs for every carrier are the Lean. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i13_lower_bound.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import _tree  # noqa: F401
from model import acquisition_values  # noqa: E402

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


def merge_actor(n: int, x: int, y: int) -> tuple[int, ...]:
    return tuple(x if z == y else z for z in range(n))


def main() -> int:
    acq = acquisition_values(4)
    unp = acq["unpromised"]
    half_sq = acq["half_square"]
    print(f"unpromised game values n=1..4: {unp}; n(n-1)/2: {half_sq}")

    all_pairs = list(itertools.combinations(range(4), 2))
    id4 = (0, 1, 2, 3)
    short_checked = 0
    short_bad = 0
    for k in range(len(all_pairs)):
        for probed in itertools.combinations(all_pairs, k):
            short_checked += 1
            uncovered = [pr for pr in all_pairs if pr not in probed]
            if not uncovered:
                short_bad += 1
                continue
            x, y = uncovered[0]
            m_xy = merge_actor(4, x, y)
            T_id = [(a, b, id4[a] == id4[b]) for a, b in probed]
            T_m = [(a, b, m_xy[a] == m_xy[b]) for a, b in probed]
            if T_id != T_m or m_xy[x] != m_xy[y] or id4[x] == id4[y]:
                short_bad += 1
    print(f"short probe sets (< 6 pairs on range(4)) checked: {short_checked}; violations: {short_bad}")

    tt_model = load_two_theorems_model()
    cr3 = tt_model.cannot_read_checks((0, 1, 2), 1)
    cr4 = tt_model.cannot_read_checks((0, 1, 2, 3), 2)
    print(f"cannot_read_checks D=(0,1,2), m=1: {cr3}; D=(0,1,2,3), m=2: {cr4}")

    ok = (
        unp == half_sq
        and short_bad == 0
        and cr3["failures"] == 0
        and cr4["failures"] == 0
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
