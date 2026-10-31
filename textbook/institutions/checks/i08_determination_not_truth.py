"""Unit 08 check: determination is not truth.

Checks:
  1. `information_without_determination`: `(PARITY4,)` has information 2 on
     `range(4)` and does not know `HALF4`;
  2. `determination_not_truth` and `truth_is_a_further_question`;
  3. `truth_from_admitted_target` and `agreement_known_of_admitted` over all
     families of at most two partitions on `range(3)`, all claims `q`, and all
     targets `t`;
  4. Correlated errors across levels of authority (`report_count` vs independent
     witnesses): three actors `p1, p2, p3` sharing the blind spot `p(0)==p(1)==p(2)`
     produce 3 unanimous reports and 2 concurring intermediate division summaries
     `S_A, S_B`, yet `information` stays at 2 (`1` distinct represented partition)
     and aggregation at both levels still determines the defective claim `q_err`
     while failing on target `HALF4`.
The proofs for every carrier are the Lean. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i08_determination_not_truth.py
"""
from __future__ import annotations

import itertools

import _tree  # noqa: F401
from model import HALF4, PARITY4, examples, information, knows, partitions, representative  # noqa: E402


def rep_table(n: int, family: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    return tuple(representative(n, family, x) for x in range(n))


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

    # 4. Three actors with correlated blind spot across two authority levels
    p1 = (0, 0, 0, 1)
    p2 = (10, 10, 10, 11)
    p3 = (20, 20, 20, 21)
    q_err = (0, 0, 0, 1)
    Q_sub = (p1, p2, p3)
    report_count = len(Q_sub)
    distinct_partitions = len({rep_table(4, (p,)) for p in Q_sub})
    info_1 = information(4, (p1,))
    info_3 = information(4, Q_sub)
    S_A = rep_table(4, (p1, p2))
    S_B = rep_table(4, (p2, p3))
    Q_top = (S_A, S_B)
    info_top = information(4, Q_top)
    correlated_ok = (
        report_count == 3
        and distinct_partitions == 1
        and info_1 == 2
        and info_3 == 2
        and info_top == 2
        and all(knows(4, (p,), q_err) for p in Q_sub)
        and knows(4, Q_sub, q_err)
        and knows(4, Q_top, q_err)
        and not knows(4, Q_sub, HALF4)
        and not knows(4, Q_top, HALF4)
        and q_err != HALF4
        and information(4, (p1, PARITY4)) > info_3
    )
    print(
        f"correlated blind-spot hierarchy: report_count={report_count}, "
        f"distinct_partitions={distinct_partitions}, "
        f"info(1..3..top)=({info_1}, {info_3}, {info_top}), "
        f"determines_err={knows(4, Q_top, q_err)}, knows_target={knows(4, Q_top, HALF4)}"
    )

    target_scope = (
        not knows(2, (c0,), id2)
        and knows(2, (id2,), c0)
        and c0 != id2
        and knows(2, (), agree_q(id2, id2))
        and not knows(2, (), id2)
    )
    print(f"target admission does not create truth; agreement can be known alone: {target_scope}")
    ok = (
        target_scope
        and info_no_det == [2, False]
        and det_not_truth is True
        and further_q == [True, False]
        and bad == 0
        and correlated_ok
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
