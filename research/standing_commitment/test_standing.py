"""Tests for the standing_commitment tree: the Lean statements recomputed in
Python, the race replayed, the countermodel checked, and the committed
receipt replayed byte for byte.  AuthorityEffect: None.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import run_standing as run  # noqa: E402
import standing as st  # noqa: E402


class LeanStatementsRecomputed(unittest.TestCase):
    """Each test here recomputes a statement the Lean package proves."""

    def test_growth_adds_exactly_the_new_datum_pairs(self) -> None:
        # `demands_grow` and `demand_count_grows`
        for n in range(0, 30):
            data = list(range(n))
            fresh = st.generated_by_growth("total", data, n)
            self.assertEqual(len(fresh), n)
            self.assertEqual(fresh, [(n, e) for e in data])

    def test_growth_generates_a_pair_the_old_state_did_not_carry(self) -> None:
        # `growth_generates`
        data = [0, 1, 2]
        fresh = st.generated_by_growth("total", data, 3)
        old = st.pairs_of(data)
        for r in fresh:
            self.assertNotIn(r, old)

    def test_pairs_of_matches_the_lean_recursion(self) -> None:
        # `pairsOf_cons` and `pairsOf_length_cons`
        for n in range(0, 12):
            data = list(range(n))
            self.assertEqual(len(st.pairs_of(data)), n * (n - 1) // 2)
            if n:
                head, rest = data[0], data[1:]
                self.assertEqual(
                    st.pairs_of(data), [(head, e) for e in rest] + st.pairs_of(rest)
                )

    def test_the_empty_commitment_generates_nothing(self) -> None:
        # `empty_commitment_generates_nothing`
        for n in range(0, 40):
            self.assertEqual(st.generated_by_growth("empty", list(range(n)), n), [])
        self.assertEqual(st.race("empty", 40, 0)["generated"], 0)

    def test_the_decided_accounting_instance(self) -> None:
        # `accounting_instance`: 3 -> 6 -> 10
        self.assertEqual(len(st.pairs_of([1, 2, 3])), 3)
        self.assertEqual(len(st.pairs_of([4, 1, 2, 3])), 6)
        self.assertEqual(len(st.pairs_of([5, 4, 1, 2, 3])), 10)


class RaceTests(unittest.TestCase):
    def test_a_discharged_state_reopens_on_growth(self) -> None:
        # the computational face of `fixpoint_reopens`
        for name in ("total", "adjacent", "shared_parity"):
            log = st.race(name, 24, 1)["log"]
            assert isinstance(log, list)
            reopened = [
                r for r in log
                if int(str(r["round"])) > 0 and int(str(r["generated"])) > 0
            ]
            self.assertTrue(reopened, name)

    def test_the_clearing_budget_is_the_peak_on_the_frozen_family(self) -> None:
        for name in run.FROZEN:
            for rounds in run.ROUNDS:
                self.assertEqual(
                    run.peak(name, rounds),
                    st.threshold(name, rounds, rounds + 2),
                    (name, rounds),
                )

    def test_the_bounded_commitment_refutes_that_regularity(self) -> None:
        for rounds in run.ROUNDS:
            self.assertNotEqual(
                run.peak("bounded", rounds),
                st.threshold("bounded", rounds, rounds + 2),
                rounds,
            )
            self.assertEqual(st.threshold("bounded", rounds, rounds + 2), 1, rounds)

    def test_generation_is_non_decreasing_exactly_on_the_frozen_family(self) -> None:
        for name in run.FROZEN + run.POST_FREEZE:
            log = st.race(name, 24, 0)["log"]
            assert isinstance(log, list)
            gens = [int(str(x["generated"])) for x in log]
            monotone = all(a <= b for a, b in zip(gens, gens[1:]))
            self.assertEqual(monotone, name in run.FROZEN, name)

    def test_an_unbounded_commitment_outruns_a_fixed_budget(self) -> None:
        short = st.race("total", 24, 1)["final_backlog"]
        long = st.race("total", 48, 1)["final_backlog"]
        self.assertGreater(int(str(long)), 2 * int(str(short)))

    def test_a_bounded_commitment_does_not(self) -> None:
        for rounds in (24, 48, 96):
            self.assertEqual(st.race("bounded", rounds, 1)["final_backlog"], 0, rounds)


class ReceiptTests(unittest.TestCase):
    def test_committed_receipt_replays_byte_for_byte(self) -> None:
        report = run.build()
        want = (HERE / "receipts" / "standing_commitment.json").read_bytes()
        got = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
        self.assertEqual(got, want)


if __name__ == "__main__":
    unittest.main()
