"""Unit 15 check: fixing a partition, and the promised-count refutation.

Checks:
  1. `fixes_converse_check(n)` for `n = 1..4` from `actor_institution/model.py`
     (`0` violations across all 760 transcripts);
  2. `acquisition_values(5)` from `actor_institution/model.py`:
     - under the "at most N classes" reading (`at_most`), the minimax game
       value matches `N(N-1)//2 + (n-N)*(N-1)` for all `1 <= N <= n <= 5`
       (`at_most_mismatches == []`);
     - under the "exactly N classes" reading (`exactly`), `n = N` has game
       value `0` while the formula gives `n(n-1)//2` (`exact_promise_zero_probes_two`
       at `n = N = 2`, mismatches `['2,2', '3,3', '4,4', '5,5']`).
The proofs for every carrier are the Lean. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i15_promise_refuted.py
"""
from __future__ import annotations

import _tree  # noqa: F401
from model import acquisition_values, fixes_converse_check  # noqa: E402


def main() -> int:
    fc = {n: fixes_converse_check(n) for n in range(1, 5)}
    print(f"fixes_converse_check n=1..4: {fc}")

    acq = acquisition_values(5)
    at_most_mm = acq["at_most_mismatches"]
    exactly_mm = acq["exactly_mismatches"]
    ex_22 = acq["exactly"]["2,2"]
    print(f"at_most_mismatches (n <= 5): {at_most_mm}")
    print(f"exactly_mismatches (n <= 5): {exactly_mm}; exactly['2,2'] [game, formula]: {ex_22}")

    ok = (
        all(v["violations"] == 0 for v in fc.values())
        and at_most_mm == []
        and exactly_mm == ["2,2", "3,3", "4,4", "5,5"]
        and ex_22 == [0, 1]
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
