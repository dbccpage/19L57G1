"""Unit 12 check: probing an actor, and finite question tables.

Checks:
  1. `run_length_le`, `run_consistent`, and `run_congr` on `range(4)` across
     one adaptive protocol, all 15 partition representatives `p, p'`, and
     budgets 0..4 (1,125 ordered actor-pair/budget comparisons);
  2. `finite_question_space` and `encoding_checks` from `two_theorems/model.py`
     on `D = (0, 1, 2, 3)` and `D = (0, 1, 2)`.
The proofs for every carrier are the Lean. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i12_probing.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import _tree  # noqa: F401
from model import consistent, partitions  # noqa: E402

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


def run_protocol(proto, p: tuple[int, ...], k: int) -> tuple[tuple[int, int, bool], ...]:
    T: list[tuple[int, int, bool]] = []
    for _ in range(k):
        nxt = proto(tuple(T))
        if nxt is None:
            break
        x, y = nxt
        T.append((x, y, p[x] == p[y]))
    return tuple(T)


def adaptive_proto(T: tuple[tuple[int, int, bool], ...]) -> tuple[int, int] | None:
    if len(T) == 0:
        return (0, 1)
    if len(T) == 1:
        return (1, 2) if T[0][2] else (0, 2)
    if len(T) == 2:
        return (2, 3) if T[1][2] else (1, 3)
    return None


def main() -> int:
    parts = partitions(4)
    congr_checked = 0
    congr_bad = 0
    for k in range(5):
        for p in parts:
            Tp = run_protocol(adaptive_proto, p, k)
            if len(Tp) > k or not consistent(p, Tp):
                congr_bad += 1
            for q in parts:
                congr_checked += 1
                agrees_on_asked = all((q[x] == q[y]) == ans for x, y, ans in Tp)
                Tq = run_protocol(adaptive_proto, q, k)
                if agrees_on_asked and Tq != Tp:
                    congr_bad += 1
    print(f"run_congr / consistency checks on range(4): {congr_checked}; violations: {congr_bad}")

    tt_model = load_two_theorems_model()
    D4 = (0, 1, 2, 3)
    pool4 = [
        tt_model.Table({x: x % 2 for x in D4}),
        tt_model.Table({x: x // 2 for x in D4}),
        tt_model.Table({x: (x == 1) * 1 for x in D4}),
        tt_model.Table({x: 0 for x in D4}),
    ]
    D3 = (0, 1, 2)
    pool3 = [
        tt_model.Table({x: x % 2 for x in D3}),
        tt_model.Table({x: x // 2 for x in D3}),
        tt_model.Table({x: (x == 1) * 1 for x in D3}),
        tt_model.Table({x: 0 for x in D3}),
    ]
    fqs3 = tt_model.finite_question_space(D3, pool3, 2)
    enc4 = tt_model.encoding_checks(D4, pool4, 2)
    enc3 = tt_model.encoding_checks(D3, pool3, 2)
    print(f"finite_question_space(D3): {fqs3}")
    print(f"encoding_checks(D4): {enc4}; encoding_checks(D3): {enc3}")

    ok = (
        congr_bad == 0
        and fqs3["tables"] == 27
        and fqs3["representative_mismatch"] == 0
        and fqs3["know_or_witness_over_all_tables"] is True
        and enc4["violations"] == 0
        and enc3["violations"] == 0
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
