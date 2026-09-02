"""Tests for the balance_carrier tree: the observer recomputed, the menu
search replayed, the S2 routes compared where they overlap, the pinned
certificate fixtures re-decided, the growth checkpoints replayed to the
pinned values, and the committed receipts replayed byte for byte.
AuthorityEffect: None.
"""

from __future__ import annotations

# ruff: noqa: E402 -- bytecode suppression must precede tree-local imports

import json
import sys
import unittest
from collections import Counter
from itertools import permutations
from itertools import product as iproduct
from pathlib import Path
from typing import Any, ClassVar, cast

sys.dont_write_bytecode = True

import growth_checkpoints
import layer_observer
import register
import run_balance_carrier
import signed_table
import walk_carrier as wc
import verify_pins

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
HITS = ["S1b(W2)", "S2(W1,1,C1)", "S2(W3,1,Cbal)"]
PINNED_CHECKPOINTS = {
    "10": -1,
    "30": -3,
    "100": 1,
    "1000": 2,
    "10000": -23,
    "100000": -48,
    "1000000": 212,
}


def rows_of(block: dict[str, object], key: str) -> list[dict[str, Any]]:
    value = block[key]
    assert isinstance(value, list)
    return cast(list[dict[str, Any]], value)


def has_certificate_by_search(weights: list[int]) -> bool:
    """A brute-force search for a pairing into exact opposites plus a
    single-signed residual; the criterion must agree with it."""

    def search(counter: Counter[int], residual_sign: int) -> bool:
        wrong = [v for v, c in counter.items() if c > 0 and v * residual_sign < 0]
        if not wrong:
            return True
        v = wrong[0]
        if counter[-v] <= 0:
            return False
        counter[v] -= 1
        counter[-v] -= 1
        ok = search(counter, residual_sign)
        counter[v] += 1
        counter[-v] += 1
        return ok

    c = Counter(weights)
    return search(Counter(c), 1) or search(Counter(c), -1)


class LayerObserverTests(unittest.TestCase):
    def test_observer_agrees_with_brute_force_fresh_representations(self) -> None:
        report = layer_observer.report()
        self.assertEqual(report["observer_misses"], [])
        self.assertEqual(report["observer_misses_wrapped"], [])
        self.assertEqual(report["grade_misses"], [])
        self.assertEqual(report["divides_misses"], [])

    def test_observer_is_constant_on_fresh_members_and_reads_the_part_count(self) -> None:
        per_layer = layer_observer.fresh_values_per_layer(12)
        for pc in range(1, 13):
            self.assertEqual(per_layer[str(pc)], [pc])

    def test_two_names_of_one_element_read_one_value(self) -> None:
        # (1, 1) is one part of two; (3, 5) is three parts of six: the same element.
        self.assertTrue(layer_observer.same_element((1, 1), (3, 5)))
        self.assertEqual(layer_observer.raw_observer(1, 1), layer_observer.raw_observer(3, 5))
        self.assertEqual(layer_observer.raw_observer(3, 5), 2)


class SearchTests(unittest.TestCase):
    bal: ClassVar[list[int]]
    runb: ClassVar[list[int]]
    found: ClassVar[dict[str, object]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.bal = wc.balance_table(2_000)
        cls.runb = wc.running_balance_table(cls.bal)
        cls.found = wc.search(cls.bal, cls.runb)

    def test_menu_has_ninety_candidates_and_exactly_the_three_hits(self) -> None:
        self.assertEqual(self.found["menu_size"], 90)
        self.assertEqual(self.found["hits"], HITS)

    def test_no_s1_and_no_s3_candidate_meets_stage_2(self) -> None:
        for row in rows_of(self.found, "candidates"):
            if row["kind"] in ("S1", "S3"):
                self.assertFalse(row["meets_stage_2"], row["menu"])

    def test_walk_sum_with_weight_minus_one_is_the_balance(self) -> None:
        self.assertEqual(wc.walk_sums("W2", 2_000, self.bal), self.bal)

    def test_chain_enumeration_agrees_with_the_recursion(self) -> None:
        for windex in wc.WEIGHTS:
            ws = wc.walk_sums(windex, 120, self.bal)
            for m in range(1, 121):
                self.assertEqual(wc.walk_sum_literal(windex, m, self.bal), ws[m], (windex, m))

    def test_unpruned_alternating_sum_equals_the_supported_sum(self) -> None:
        for label in ("S2(W1,1,C1)", "S2(W3,1,Cbal)", "S2(W2,-1,C-1)", "S2(W3,0,Cbal)", "S2(W4,0,C1)"):
            w, d, c = wc.parse_s2(label)
            for n in range(1, 8):
                rows = wc.table(w, d, c, n, self.bal)
                self.assertEqual(
                    wc.table_count_literal(rows), wc.table_count_supported(rows), (label, n)
                )

    def test_supported_sum_agrees_with_elimination_and_the_column_route(self) -> None:
        for label in ("S2(W1,1,C1)", "S2(W3,1,Cbal)", "S2(W2,-1,C-1)", "S2(W4,-1,C-bal)"):
            w, d, c = wc.parse_s2(label)
            for n in range(1, 41):
                rows = wc.table(w, d, c, n, self.bal)
                supported = wc.table_count_supported(rows)
                self.assertEqual(supported, wc.table_count_elimination(rows), (label, n))
                self.assertEqual(
                    supported, wc.table_count_column_route(w, d, c, n, self.bal), (label, n)
                )

    def test_column_route_matches_the_running_balance_at_every_N_to_600(self) -> None:
        for label in ("S2(W1,1,C1)", "S2(W3,1,Cbal)"):
            w, d, c = wc.parse_s2(label)
            for n in range(1, 601):
                self.assertEqual(
                    wc.table_count_column_route(w, d, c, n, self.bal), self.runb[n], (label, n)
                )

    def test_column_route_refuses_a_zero_diagonal(self) -> None:
        with self.assertRaises(ValueError):
            wc.table_count_column_route("W1", 0, "C1", 5, self.bal)

    def test_sign_is_the_inversion_parity(self) -> None:
        self.assertEqual(wc.inversion_sign((0, 1, 2)), 1)
        self.assertEqual(wc.inversion_sign((1, 0, 2)), -1)
        self.assertEqual(wc.inversion_sign((2, 0, 1)), 1)
        signs = [wc.inversion_sign(p) for p in permutations(range(4))]
        self.assertEqual(sum(1 for s in signs if s == 1), 12)

    def test_sections_are_enumerated_not_factored(self) -> None:
        # the enumeration must agree with the product of the arrow sums (a METATHEORY cross-check)
        for windex in wc.WEIGHTS:
            for n in range(1, 9):
                product = 1
                for m in range(2, n + 1):
                    product *= sum(
                        wc.weight(windex, d, m, self.bal) for d in wc.proper_divisors(m)
                    )
                self.assertEqual(wc.sections_count(windex, n, self.bal), product, (windex, n))


class SignedFamilyTests(unittest.TestCase):
    bal: ClassVar[list[int]]
    runb: ClassVar[list[int]]
    fam: ClassVar[dict[str, object]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.bal = wc.balance_table(200)
        cls.runb = wc.running_balance_table(cls.bal)
        cls.fam = signed_table.report(HITS, cls.bal, cls.runb)

    def test_pinned_fixtures_are_redecided(self) -> None:
        fixtures = self.fam["pinned_fixtures"]
        assert isinstance(fixtures, dict)
        wedge = cast(dict[str, Any], fixtures["wedge"])
        witness = cast(dict[str, Any], fixtures["witness"])
        self.assertFalse(wedge["certificate_exists"])
        self.assertTrue(witness["certificate_exists"])

    def test_every_family_has_magnitude_one_and_totals_the_running_balance(self) -> None:
        rows = rows_of(self.fam, "rows")
        self.assertEqual(len(rows), 9)
        for row in rows:
            self.assertTrue(row["every_magnitude_is_one"], row["menu"])
            self.assertTrue(row["total_equals_running_balance"], row["menu"])
            self.assertTrue(row["certificate"]["certificate_exists"], row["menu"])
        self.assertEqual(self.fam["terminal"], "DEGENERACY_PERSISTS")

    def test_s1b_family_is_the_chain_weights(self) -> None:
        terms = signed_table.s1b_terms("W2", 6, self.bal)
        # chains to 1..6: 1 + 1 + 1 + 2 + 1 + 3 = 9 chains
        self.assertEqual(len(terms), 9)
        self.assertEqual(sum(terms), self.runb[6])

    def test_domination_criterion_matches_a_search_for_certificates(self) -> None:
        for weights in iproduct(range(-2, 3), repeat=5):
            lst = list(weights)
            self.assertEqual(
                signed_table.certificate_decision(lst)["certificate_exists"],
                has_certificate_by_search(lst),
                lst,
            )


class GrowthCheckpointTests(unittest.TestCase):
    def test_checkpoints_to_ten_thousand_replay_the_pinned_values(self) -> None:
        bal = wc.balance_table(10_000)
        runb = wc.running_balance_table(bal)
        report = growth_checkpoints.report(bal, runb)
        rows = rows_of(report, "checkpoints")
        self.assertEqual([r["N"] for r in rows], [10, 30, 100, 1_000, 10_000])
        for r in rows:
            self.assertTrue(r["agree"], r)
            self.assertEqual(r["direct"], PINNED_CHECKPOINTS[str(r["N"])], r)
        self.assertEqual(report["checkpoint_misses"], [])
        maximum = cast(dict[str, Any], report["running_maximum"])
        self.assertEqual(maximum["max_squared_ratio"], [4, 5])
        self.assertEqual(maximum["at_part_count"], 5)
        self.assertTrue(maximum["square_stays_below_n_in_window"])
        self.assertEqual(report["terminal"], "GROWTH_OPEN_UNCHANGED")

    def test_ratio_decimal_is_integer_arithmetic(self) -> None:
        self.assertEqual(growth_checkpoints.ratio_decimal(2, 5), "0.894427")
        self.assertEqual(growth_checkpoints.ratio_decimal(0, 7), "0.000000")


class ReceiptTests(unittest.TestCase):
    def test_source_projections_and_both_prediction_freezes_are_bound(self) -> None:
        manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text("ascii"))
        for spec in manifest["reconstructions"]:
            source = verify_pins.git("show", f"{manifest['snapshot_commit']}:{spec['source_path']}")
            expected = verify_pins.reconstructed_lines(source, spec)
            local = (REPO / spec["local_path"]).read_bytes().split(b"\n")
            first = spec["local_first_line"]
            last = spec["local_last_line"]
            actual = local[first - 1 : last]
            self.assertEqual(actual, expected, spec["local_path"])
            mutated = actual.copy()
            mutated[0] += b" "
            self.assertNotEqual(mutated, expected, spec["local_path"])
        predictions = (HERE / "PREDICTIONS.md").read_bytes()
        boundary = manifest["predictions_first_freeze_boundary"].encode("ascii")
        hashes = verify_pins.prediction_freeze_hashes(predictions, boundary)
        self.assertEqual(hashes, manifest["predictions_freezes"])
        prefix_mutation = bytes([predictions[0] ^ 1]) + predictions[1:]
        self.assertNotEqual(
            verify_pins.prediction_freeze_hashes(prefix_mutation, boundary), hashes
        )
        final_mutation = predictions[:-1] + bytes([predictions[-1] ^ 1])
        final_hashes = verify_pins.prediction_freeze_hashes(final_mutation, boundary)
        self.assertEqual(final_hashes[0], hashes[0])
        self.assertNotEqual(final_hashes[1], hashes[1])

    def test_committed_receipts_replay_byte_for_byte(self) -> None:
        report = run_balance_carrier.build_report(wc.CHECKPOINTS[-1])
        self.assertEqual(
            (HERE / "receipts" / "balance_carrier.json").read_bytes(),
            run_balance_carrier.render(report),
        )
        self.assertEqual(
            (HERE / "receipts" / "tau.yaml").read_bytes(), run_balance_carrier.render_tau(report)
        )

    def test_receipt_checkpoints_equal_the_pinned_sibling_receipt(self) -> None:
        ours = json.loads((HERE / "receipts" / "balance_carrier.json").read_text("ascii"))
        theirs = json.loads(
            (REPO / "research" / "natural_sections" / "receipts" / "layer_balance.json").read_text(
                "ascii"
            )
        )
        rows = ours["stage_4_growth_checkpoints"]["checkpoints"]
        got = {str(r["N"]): r["direct"] for r in rows}
        self.assertEqual(got, theirs["running_balance_checkpoints"])
        self.assertEqual(got, PINNED_CHECKPOINTS)
        growth = ours["stage_4_growth_checkpoints"]["running_maximum"]
        self.assertEqual(
            growth["max_squared_ratio"],
            [theirs["growth"]["max_squared_ratio_num"], theirs["growth"]["max_squared_ratio_den"]],
        )
        self.assertEqual(growth["at_part_count"], theirs["growth"]["at_part_count"])

    def test_register_rows_are_the_hits_and_the_leftovers_are_named(self) -> None:
        ours = json.loads((HERE / "receipts" / "balance_carrier.json").read_text("ascii"))
        rows = ours["stage_5_register"]["rows"]
        self.assertEqual([r["menu"] for r in rows], HITS)
        names = [lo["name"] for lo in ours["stage_5_register"]["leftovers"]]
        self.assertEqual(len(names), 4)
        self.assertTrue(any("next rung" in n for n in names))
        self.assertEqual(
            ours["stage_5_register"]["protected_opens_unchanged"], list(register.PROTECTED_OPENS)
        )


if __name__ == "__main__":
    unittest.main()
