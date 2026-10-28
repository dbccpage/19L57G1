"""Unit 06 check: degradation, aggregates, and loss.

Checks:
  1. `aggregates_inert` and `essential_iff` on `range(3)` over all families of
     at most two partitions and all partitions as the extra/removed member;
  2. `aggregate_hides_exceeding` and `consensus_after_loss` from
     `actor_institution/model.py`;
  3. `guess_checks` on `D = (0, 1, 2, 3)` from `two_theorems/model.py`.
The proofs for every carrier are the Lean. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i06_degradation.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import _tree  # noqa: F401
from model import examples, information, knows, partitions  # noqa: E402

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
    families = [()] + [(p,) for p in parts] + list(itertools.combinations(parts, 2))
    agg_checked = 0
    agg_bad = 0
    ess_checked = 0
    ess_bad = 0
    for Q in families:
        known_members = tuple(m for m in parts if knows(3, Q, m))
        agg_checked += 1
        if information(3, Q + known_members) != information(3, Q):
            agg_bad += 1
        for q in parts:
            if knows(3, Q + known_members, q) != knows(3, Q, q):
                agg_bad += 1
        for p in parts:
            ess_checked += 1
            dropped_lt = information(3, Q) < information(3, Q + (p,))
            if dropped_lt != (not knows(3, Q, p)):
                ess_bad += 1

    ex = examples()
    agg_hides = ex["aggregate_hides_exceeding"]
    loss = ex["consensus_after_loss"]
    print(f"aggregates_inert checked: {agg_checked} (bad: {agg_bad}); essential_iff checked: {ess_checked} (bad: {ess_bad})")
    print(f"aggregate_hides_exceeding: {agg_hides}")
    print(f"consensus_after_loss: {loss}")

    tt_model = load_two_theorems_model()
    guess = tt_model.guess_checks((0, 1, 2, 3))
    print(f"two_theorems guess_checks on D=(0,1,2,3): {guess}")

    ok = (
        agg_bad == 0
        and ess_bad == 0
        and agg_hides == [[0, 1, 2, 3], True, False]
        and loss == [True, True, True, False]
        and guess["guess"] is True
        and guess["own_guess_invisible"] is True
        and guess["visible_to_family"] is True
        and guess["another_member_splits"] is True
        and guess["grounded_for_family"] is True
        and guess["shared_by_half_alone"] is True
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
