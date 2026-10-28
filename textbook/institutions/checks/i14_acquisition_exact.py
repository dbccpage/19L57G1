"""Unit 14 check: the complete table acquires, and representation vs acquisition.

Checks:
  1. On `range(4)`, for every partition `p`, the complete transcript `fullT` of
     6 probes builds `tableE` sharp for `p`, and `logE` of `m = 2` views built
     from `acquired` is sharp for `p`;
  2. `sufficiency_checks` and `sharp_fixes_partition_check` from
     `two_theorems/model.py` on `D = (0, 1, 2)` and `D = (0, 1, 2, 3)`.
The proofs for every carrier are the Lean. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i14_acquisition_exact.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import _tree  # noqa: F401
from model import partitions, sharp  # noqa: E402

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


def full_t(n: int, p: tuple[int, ...]) -> tuple[tuple[int, int, bool], ...]:
    return tuple((x, y, p[x] == p[y]) for x, y in itertools.combinations(range(n), 2))


def same_t(T: tuple[tuple[int, int, bool], ...], a: int, b: int) -> bool:
    if a == b:
        return True
    return any(((x == a and y == b) or (x == b and y == a)) and ans for x, y, ans in T)


def table_e(n: int, T: tuple[tuple[int, int, bool], ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(b for b in range(n) if same_t(T, a, b)) for a in range(n))


def main() -> int:
    tt_model = load_two_theorems_model()
    D4 = (0, 1, 2, 3)
    parts4 = partitions(4)
    table_bad = 0
    log_bad = 0
    for p in parts4:
        T = full_t(4, p)
        E = table_e(4, T)
        if not sharp(4, E, p):
            table_bad += 1
        acq_p = tt_model.joint_presentation(D4, tt_model.questions(E))
        log_e = tt_model.bit_observer(D4, tt_model.fiber_index(D4, acq_p), 2)
        if not sharp(4, log_e, p):
            log_bad += 1
    print(f"partitions on range(4) checked: {len(parts4)}; tableE bad: {table_bad}; logE(m=2) bad: {log_bad}")

    s3_1 = tt_model.sufficiency_checks((0, 1, 2), 1)
    s3_2 = tt_model.sufficiency_checks((0, 1, 2), 2)
    s4_2 = tt_model.sufficiency_checks((0, 1, 2, 3), 2)
    p3_2 = tt_model.sharp_fixes_partition_check((0, 1, 2), 2)
    p4_2 = tt_model.sharp_fixes_partition_check((0, 1, 2, 3), 2)
    print(f"sufficiency_checks D3 m=1: {s3_1}; D3 m=2: {s3_2}; D4 m=2: {s4_2}")
    print(f"sharp_fixes_partition_check D3 m=2: {p3_2}; D4 m=2: {p4_2}")

    ok = (
        table_bad == 0
        and log_bad == 0
        and s3_1["violations"] == 0
        and s3_2["violations"] == 0
        and s4_2["violations"] == 0
        and s3_1["sufficient_not_sharp"] > 0
        and s3_1["consistent_not_sufficient"] > 0
        and p3_2["violations"] == 0
        and p3_2["observer_differs"] == 0
        and p4_2["violations"] == 0
        and p4_2["observer_differs"] == 0
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
