"""Unit 08 check: determination is not truth.

Checks:
  1. `information_without_determination`: `(PARITY4,)` has information 2 on
     `range(4)` and does not know `HALF4`;
  2. `determination_not_truth` and `truth_is_a_further_question`;
  3. `truth_from_admitted_target` and `agreement_known_of_admitted` over all
     families of at most two partitions on `range(3)`, all claims `q`, and all
     targets `t`.
The proofs for every carrier are the Lean. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i08_determination_not_truth.py
"""
from __future__ import annotations

import itertools

import _tree  # noqa: F401
from model import examples, knows, partitions  # noqa: E402


def agree_q(q: tuple[int, ...], t: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(1 if qx == tx else 0 for qx, tx in zip(q, t))


def main() -> int:
    info_no_det = examples()["information_without_determination"]
    print(f"information_without_determination (info(PARITY4), knows(PARITY4, HALF4)): {info_no_det}")

    c0 = (0, 0)
    c1 = (1, 1)
    id2 = (0, 1)
    det_not_truth = knows(2, (), c0) and knows(2, (), c1) and (c0 != c1)
    further_q = [knows(2, (), c0), knows(2, (), agree_q(c0, id2))]
    print(f"determination_not_truth on range(2): {det_not_truth}; truth_is_a_further_question: {further_q}")

    parts = partitions(3)
    fams = [(p,) for p in parts] + list(itertools.combinations(parts, 2))
    all_tables = list(itertools.product(range(3), repeat=3))
    checked = 0
    bad = 0
    for Q in fams:
        for t in Q:
            for q in all_tables:
                checked += 1
                if q == t and not knows(3, Q, q):
                    bad += 1
                if knows(3, Q, q) and not knows(3, Q, agree_q(q, t)):
                    bad += 1
    print(f"admitted-target checks on range(3): {checked}; violations: {bad}")

    ok = (
        info_no_det == [2, False]
        and det_not_truth is True
        and further_q == [True, False]
        and bad == 0
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
