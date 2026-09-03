"""Tests for the fresh_characters tree: the two balance routes cross-checked,
the exponent word against the pinned step law, the stage-1 targets recomputed,
the stage-2 search replayed, the certificate criterion against a brute-force
search, the stage-3 recursion replayed, and the committed receipts replayed
byte for byte.

AuthorityEffect: None.
"""

from __future__ import annotations

import json
import sys
import unittest
from itertools import product as iproduct
from math import gcd
from pathlib import Path
from typing import Any, ClassVar, cast

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import characters as ch  # noqa: E402
import divisor_recursion as dr  # noqa: E402
import fresh_totals as ft  # noqa: E402
import magnitude_census as mc  # noqa: E402
import run_fresh_characters as run  # noqa: E402

PINNED_BALANCE_HEAD: list[int] = [1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0]
HITS: list[str] = ["V6/R1", "V6/Rlast"]


class BalanceRouteTests(unittest.TestCase):
    def test_the_two_balance_routes_agree_and_match_the_pinned_head(self) -> None:
        reference = ch.balance_table_reference(300)
        fast = ch.balance_table(300)
        self.assertEqual(reference, fast)
        self.assertEqual(fast[1:13], PINNED_BALANCE_HEAD)

    def test_the_pinned_divisor_recursion_holds_on_the_balance(self) -> None:
        bal = ch.balance_table(200)
        self.assertEqual(bal[1], 1)
        for n in range(2, 201):
            self.assertEqual(sum(bal[d] for d in ch.divisors(n)), 0, n)

    def test_the_pinned_checkpoints_are_reproduced(self) -> None:
        bal = ch.balance_table(1_000_000)
        for n, want in ft.PINNED_CHECKPOINTS.items():
            self.assertEqual(sum(bal[1 : n + 1]), want, n)


class ExponentWordTests(unittest.TestCase):
    def test_the_exponent_word_is_the_pinned_step_action(self) -> None:
        # the pinned `repAdd_val`: the step's value at a member is the member
        # multiplied by the step, taken in the part count
        for n in range(1, 40):
            for a in range(n):
                for c in range(n):
                    self.assertEqual(ch.exponent(n, a, c), (a * c) % n)

    def test_distinct_steps_give_distinct_exponent_words(self) -> None:
        for n in range(1, 30):
            words = {tuple(ch.exponent(n, a, c) for c in range(n)) for a in range(n)}
            self.assertEqual(len(words), n, n)

    def test_the_step_zero_word_is_constantly_the_zero_member(self) -> None:
        for n in range(1, 60):
            self.assertEqual(ch.fresh_exp(n, 0), [0] * ch.fresh_count(n), n)

    def test_the_word_restricts_along_every_divisor_arrow(self) -> None:
        for n in range(1, 30):
            for d in ch.divisors(n):
                q = n // d
                for a in range(n):
                    for c in range(d):
                        self.assertEqual(
                            ch.exponent(n, a, c * q), q * ch.exponent(d, a, c), (n, d, a, c)
                        )


class FreshPartTests(unittest.TestCase):
    def test_the_fresh_parts_multiply_back_to_the_layer_difference(self) -> None:
        for n in range(1, 61):
            acc: ch.Poly = [1]
            for d in ch.divisors(n):
                acc = _pmul(acc, ch.fresh_part(d))
            self.assertEqual(ch.trim(acc), ch.trim(ch.layer_diff(n)), n)

    def test_the_fresh_part_has_the_fresh_count_as_its_degree(self) -> None:
        for n in range(1, 61):
            self.assertEqual(len(ch.trim(ch.fresh_part(n))) - 1, ch.fresh_count(n), n)

    def test_division_by_a_monic_divisor_is_exact_where_it_should_be(self) -> None:
        for n in range(2, 40):
            quotient, remainder = ch.pdivmod(ch.layer_diff(n), ch.fresh_part(n))
            self.assertEqual(remainder, [], n)
            self.assertEqual(ch.trim(_pmul(quotient, ch.fresh_part(n))),
                             ch.trim(ch.layer_diff(n)), n)


def _pmul(p: ch.Poly, q: ch.Poly) -> ch.Poly:
    if not p or not q:
        return []
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q):
                out[i + j] += a * b
    return ch.trim(out)


class SearchTests(unittest.TestCase):
    found: ClassVar[dict[str, object]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.found = ft.search(60)

    def test_the_menu_has_twenty_four_pairs_and_exactly_the_two_hits(self) -> None:
        self.assertEqual(self.found["menu_size"], 24)
        self.assertEqual(self.found["hits"], HITS)
        self.assertEqual(self.found["terminal"], "TOTAL_IDENTITY_BOUNDED")

    def test_no_carrier_other_than_the_fresh_part_quotient_meets_the_stage(self) -> None:
        rows = cast(list[dict[str, Any]], self.found["candidates"])
        for row in rows:
            if row["carrier"] != "V6":
                self.assertFalse(row["meets_stage_2"], row["pair"])

    def test_the_hits_agree_with_the_balance_past_the_search_bound(self) -> None:
        bal = ch.balance_table(200)
        for label in HITS:
            carrier, rule = label.split("/")
            for n in range(1, 201):
                self.assertEqual(
                    ch.total(carrier, n, ch.step_of(rule, n)).integer_total, bal[n], (label, n)
                )

    def test_the_additive_carrier_never_totals_the_fresh_count(self) -> None:
        for n in range(1, 40):
            rep = ch.total("V1", n, 0)
            self.assertFalse(rep.is_integer_total, n)

    def test_the_unit_value_carrier_totals_the_fresh_count_at_every_step(self) -> None:
        for n in range(1, 40):
            for a in range(n):
                self.assertEqual(ch.total("V2", n, a).integer_total, ch.fresh_count(n), (n, a))


class RecursionTests(unittest.TestCase):
    def test_the_divisor_sum_of_the_totals_is_the_part_count_at_the_zero_step(self) -> None:
        for n in range(1, 41):
            self.assertEqual(dr.divisor_total("V6", n, 0), n, n)

    def test_the_divisor_sum_vanishes_at_every_other_step(self) -> None:
        for n in range(1, 41):
            for a in range(1, n):
                self.assertEqual(dr.divisor_total("V6", n, a), 0, (n, a))

    def test_the_totals_depend_on_the_step_only_through_the_shared_divisor(self) -> None:
        for n in range(1, 41):
            seen: dict[int, int] = {}
            for a in range(n):
                value = dr.integer_total("V6", n, a)
                assert value is not None
                g = gcd(a, n)
                if g in seen:
                    self.assertEqual(seen[g], value, (n, a))
                else:
                    seen[g] = value


class CensusTests(unittest.TestCase):
    def test_the_criterion_matches_a_brute_force_search(self) -> None:
        for weights in iproduct(range(-2, 3), repeat=5):
            lst = list(weights)
            self.assertEqual(
                mc.certificate_decision(lst)["certificate_exists"],
                mc.has_certificate_by_search(lst),
                lst,
            )

    def test_the_smallest_refusing_row_is_the_recorded_one(self) -> None:
        row = mc.row_family("V6", 3)
        self.assertEqual(row, [2, -1, -1])
        self.assertEqual(sum(row or []), 0)
        self.assertFalse(mc.certificate_decision(row or [])["certificate_exists"])
        self.assertFalse(mc.has_certificate_by_search(row or []))

    def test_every_term_family_carries_one_magnitude(self) -> None:
        for carrier in mc.TERM_CARRIERS:
            for n in range(1, 41):
                for a in range(n):
                    fam = mc.term_family(carrier, n, a)
                    if fam is None:
                        continue
                    self.assertLessEqual(len(mc.magnitudes_present(fam)), 1, (carrier, n, a))

    def test_every_row_family_of_the_hit_carrier_totals_to_zero_above_one(self) -> None:
        for n in range(2, 61):
            fam = mc.row_family("V6", n)
            assert fam is not None
            self.assertEqual(sum(fam), 0, n)


class ReceiptTests(unittest.TestCase):
    def test_committed_receipts_replay_byte_for_byte(self) -> None:
        report = run.build(60)
        want = (HERE / "receipts" / "fresh_characters.json").read_bytes()
        got = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
        self.assertEqual(got, want)
        self.assertEqual(
            run.tau(report).encode("utf-8"), (HERE / "receipts" / "tau.yaml").read_bytes()
        )


if __name__ == "__main__":
    unittest.main()
