"""The gates, the decided object, and every fairness guard.

Each guard here has a negative direction: the test asserts that the guard
FAILS when the defect it exists to catch is present.  A guard with no failing
case is not a guard, and this file is where that is held.
"""

from __future__ import annotations

import copy
import json
import pathlib
import sys
import unittest
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "code"))

from sidefree import candidates as ctl  # noqa: E402
from sidefree import control  # noqa: E402
from sidefree import mirror as mir  # noqa: E402
from sidefree.enumerate import (  # noqa: E402
    Json,
    eligible,
    enumerate_rows,
    everywhere_satisfying,
    key_json,
    minima,
    named,
    newly_available,
    permutations_of,
)
from sidefree.requirement import separates  # noqa: E402

TREE = pathlib.Path(__file__).resolve().parent.parent
RECORD: Any = control.decide()
ROWS: Any = control.control_rows()
MROWS: Any = control.mirror_rows()


class Gates(unittest.TestCase):
    def test_every_gate_passes_and_the_record_is_not_void(self) -> None:
        for name in ("G1", "G2", "G3", "G4", "G5", "G6"):
            gate = RECORD["gates"][name]
            self.assertTrue(gate["passed"], f"{name}: {gate['problems']}")
        self.assertTrue(RECORD["gates"]["all_passed"])
        self.assertFalse(RECORD["void"])

    def test_g1_names_the_four_pin_values(self) -> None:
        g1: Any = control.gate_pin_bytes()
        self.assertEqual(g1["sha256"], control.PIN_SHA256)
        self.assertEqual(g1["git_blob_sha1"], control.PIN_BLOB)
        self.assertEqual(g1["byte_count"], control.PIN_BYTES)
        self.assertFalse(g1["carries_cr"])

    def test_g1_reports_the_commit_check_and_never_omits_it(self) -> None:
        status = control.commit_check()["status"]
        self.assertIn(status, ("PASS", "SKIPPED", "FAIL"))
        self.assertTrue(str(control.commit_check()["reason"]))
        self.assertIn("residual", control.commit_check())

    def test_g4_covers_the_fourteen_rows_and_its_scope_is_stated(self) -> None:
        g4 = RECORD["gates"]["G4"]
        self.assertEqual(g4["row_count"], 14)
        self.assertEqual(g4["agreements"], 14)
        self.assertIn("not total over all 48 points", str(g4["scope"]))

    def test_g4_fails_when_a_pinned_verdict_is_mutated(self) -> None:
        """Negative: the decisive gate must catch a wrong recorded answer."""
        i, j = (0, 1)
        for reading in ("U", "O"):
            for row in control.pin_verdict_rows(reading):
                mutated: Any = copy.deepcopy(row)
                mutated["satisfies"] = not bool(mutated["satisfies"])
                perms = permutations_of(list(mutated["automorphism_entries"]))
                self.assertNotEqual(separates(perms, i, j), mutated["satisfies"])

    def test_g5_is_the_smuggle_tripwire_and_it_fires(self) -> None:
        g5 = RECORD["gates"]["G5"]
        self.assertTrue(g5["passed"])
        self.assertEqual(g5["report"]["violations"], 0)
        fired = RECORD["smuggle_tripwire"]
        self.assertEqual(fired["violations"], 12)
        self.assertTrue(fired["injection_live"])

    def test_g6_compares_every_row_of_both_readings(self) -> None:
        self.assertEqual(RECORD["gates"]["G6"]["rows_compared"], 96)

    def test_g6_fails_on_a_mirror_that_drifts_from_the_pin(self) -> None:
        """Negative: a divergence must VOID rather than adjust."""
        drifted = {r: [dict(row) for row in rows] for r, rows in MROWS.items()}
        drifted["U"][0]["mu1"] = 99
        gate: Any = control.gate_mirror_matches_the_pin(drifted)
        self.assertFalse(gate["passed"])
        self.assertTrue(any("mu1" in str(p) for p in gate["problems"]))

    def test_g6_fails_on_a_missing_row_and_on_a_wrong_space_size(self) -> None:
        short: Any = {r: [dict(row) for row in rows] for r, rows in MROWS.items()}
        removed = short["U"].pop()
        gate: Any = control.gate_mirror_matches_the_pin(short)
        self.assertFalse(gate["passed"])
        self.assertTrue(any("space size" in str(p) for p in gate["problems"]))
        renamed: Any = {r: [dict(row) for row in rows] for r, rows in MROWS.items()}
        renamed["U"][0]["name"] = "zzz_probe"
        gate = control.gate_mirror_matches_the_pin(renamed)
        self.assertFalse(gate["passed"])
        self.assertTrue(
            any("absent from the pin" in str(p) for p in gate["problems"])
        )
        self.assertIsInstance(removed, dict)


class DecidedObject(unittest.TestCase):
    def test_the_headline(self) -> None:
        decided = RECORD["decided"]
        self.assertEqual(decided["side_free_minimum"], 1)
        self.assertEqual(decided["side_free_classes"], 1)
        self.assertTrue(decided["side_free_unique"])
        self.assertEqual(decided["delta_vs_unnamed"], 0)
        self.assertEqual(decided["delta_vs_named"], 1)
        self.assertEqual(
            decided["what_the_admitted_primitive_bought"], "NOTHING_IN_COST"
        )

    def test_the_withdrawal_ports_at_the_same_cost(self) -> None:
        port = RECORD["withdrawal_port"]
        self.assertTrue(port["same_cost"])
        self.assertEqual(port["control_mu1"], 1)
        self.assertEqual(port["pinned_mu1"], 1)
        self.assertTrue(port["capability_text_identical"])
        self.assertTrue(port["definition_level_here"])

    def test_the_verdict_value_is_a_declared_finite_set(self) -> None:
        self.assertEqual(control.verdict_value(False, 1, 0), "VOID")
        self.assertEqual(control.verdict_value(True, None, None), "NO_SATISFYING_CANDIDATE")
        self.assertEqual(control.verdict_value(True, 1, 0), "NOTHING_IN_COST")
        self.assertEqual(control.verdict_value(True, 2, 1), "COST_DIFFERENCE_1")

    def test_routes_and_price_are_separate_columns(self) -> None:
        decided = RECORD["decided"]
        self.assertEqual(decided["routes_bought_count"], 2)
        self.assertEqual(decided["plurality_vs_unnamed"], -2)
        self.assertEqual(
            decided["routes_the_admitted_primitive_bought"],
            ["extra_mark", "withdraw_reflection"],
        )

    def test_only_the_declaration_itself_names_routes_and_price_together(self) -> None:
        """The guard ``decided.plurality_is_not_price`` names, over THIS record.

        The sibling walk in ``tests/test_comparison.py`` runs over the price
        list's record and cannot see this one, so the receipt's own sentence
        is asserted here rather than on a record it does not cover.  The
        found set is pinned rather than required empty: the declaration that
        the two are never combined is itself a field whose name carries both
        words, in the primary block and in the secondary one, and an
        exclusion for it would be curated where an exact set is not.
        """
        found: list[str] = []

        def walk(node: object, path: str) -> None:
            if isinstance(node, dict):
                for key, value in node.items():
                    lowered = str(key).lower()
                    if ("route" in lowered or "plurality" in lowered) and (
                        "price" in lowered or "cost" in lowered
                    ):
                        found.append(f"{path}.{key}")
                    walk(value, f"{path}.{key}")
            elif isinstance(node, list):
                for index, value in enumerate(node):
                    walk(value, f"{path}[{index}]")

        walk(RECORD, "")
        self.assertEqual(
            sorted(found),
            [
                ".decided.plurality_is_not_price",
                ".secondary.decided.plurality_is_not_price",
            ],
        )

    def test_the_route_table_disagrees_at_exactly_one_cell(self) -> None:
        self.assertEqual(RECORD["route_disagreements"], ["extra_mark"])
        for row in RECORD["route_table"]:
            self.assertTrue(row["joined"], row["coordinate"])
            self.assertTrue(row["pinned_verdicts_uniform"], row["coordinate"])

    def test_a_renamed_coordinate_fails_the_join_by_name(self) -> None:
        """Negative: the join is by string equality, and a rename must show."""
        original = ctl.COORDINATES
        try:
            ctl.COORDINATES = ("withdraw_mark_permutation", "keep_labels", "extra_mark")
            routes = control.joined_routes()
            self.assertIn(("withdraw_mark_permutation", ["withdraw_mark_permutation"]), routes)
            pinned = {str(r["name"]) for r in control.pin_verdict_rows("U")}
            self.assertNotIn("withdraw_mark_permutation", pinned)
        finally:
            ctl.COORDINATES = original

    def test_the_collapse_map_joins_the_two_pinned_further_mark_points(self) -> None:
        routes = dict(control.joined_routes())
        self.assertEqual(routes["extra_mark"], ["extra_mark_0", "extra_mark_1"])


class EndowmentAndCensus(unittest.TestCase):
    def test_the_ledger_names_its_mismatching_rows(self) -> None:
        """Named, split into priced and unpriced, and flagged where declared.

        The three belong in one test because the suite's size is pinned by the
        registered CI step and moving it is a separate, deliberate act; the
        assertions are what the ledger's own summary sentence now claims.
        """
        ledger = RECORD["endowment_ledger"]
        self.assertIn("declarations_at_genesis", ledger["mismatching_rows"])
        self.assertIn("judgments_holding_at_genesis", ledger["mismatching_rows"])
        self.assertEqual(len(ledger["named_mismatches"]), 2)
        flagged = {
            str(row["row"]): list(row["declared_columns"])
            for row in ledger["rows"]
            if row["declared_columns"]
        }
        self.assertEqual(
            flagged,
            {
                "declarations_at_genesis": ["control", "unnamed", "named"],
                "coordinates_the_genesis_declaration_fixes": ["control"],
            },
        )
        self.assertEqual(sorted(flagged), sorted(ledger["rows_with_a_declared_column"]))
        self.assertEqual(
            sorted(flagged), sorted(ledger["why_the_declared_cells_are_declared"])
        )
        unmatchable = [
            entry for entry in ledger["named_mismatches"] if "UNMATCHABLE" in str(entry)
        ]
        self.assertEqual(len(unmatchable), 1)
        priced = ledger["mismatching_rows_with_a_stated_price"]
        unpriced = ledger["mismatching_rows_with_no_stated_price"]
        self.assertEqual(priced, ["coordinates_the_genesis_declaration_fixes"])
        self.assertEqual(sorted(priced + unpriced), sorted(ledger["mismatching_rows"]))
        self.assertEqual(set(priced) & set(unpriced), set())
        for row in ledger["rows"]:
            has_price = "price_if_bought" in row
            named = str(row["row"]) in priced
            self.assertEqual(
                named, has_price and str(row["row"]) in ledger["mismatching_rows"]
            )

    def test_the_declared_census_counts_cells_and_never_rows(self) -> None:
        """The counts the live documents write, held where they are computed.

        Four declared CELLS across two declared ROWS, and the two numbers are
        not interchangeable: a scoring note headed "two cells" was carrying
        the row count under the cell word, so both are asserted here and the
        prose names these fields rather than restating them.  The cell
        population is rows times columns and the two censuses partition it,
        so a cell cannot be dropped from both.
        """
        ledger = RECORD["endowment_ledger"]
        self.assertEqual(ledger["columns"], ["control", "unnamed", "named"])
        self.assertEqual(len(ledger["rows"]), 7)
        self.assertEqual(len(ledger["declared_cells"]), 4)
        self.assertEqual(len(ledger["computed_cells"]), 17)
        self.assertEqual(len(ledger["rows_with_a_declared_column"]), 2)
        self.assertEqual(
            len(ledger["rows"]) - len(ledger["rows_with_a_declared_column"]), 5
        )
        self.assertEqual(
            len(ledger["declared_cells"]) + len(ledger["computed_cells"]),
            len(ledger["rows"]) * len(ledger["columns"]),
        )
        self.assertEqual(
            set(ledger["declared_cells"]) & set(ledger["computed_cells"]), set()
        )
        self.assertEqual(
            ledger["declared_cells"],
            [
                "declarations_at_genesis:control",
                "declarations_at_genesis:unnamed",
                "declarations_at_genesis:named",
                "coordinates_the_genesis_declaration_fixes:control",
            ],
        )

    def test_definition_level_is_computed_and_not_asserted(self) -> None:
        """Declared on BOTH sides, which is what `comparison.py` means by it.

        The whole `declarations_at_genesis` row is declared in every column;
        the control cell of the coordinates row stands beside two computed
        reading cells and is therefore NOT definition-level.  The ledger's
        prose asserted the classification for both, and this is the flag that
        decides it instead.
        """
        ledger = RECORD["endowment_ledger"]
        self.assertEqual(ledger["definition_level_rows"], ["declarations_at_genesis"])
        for row in ledger["rows"]:
            self.assertEqual(
                row["definition_level"],
                len(row["declared_columns"]) == len(ledger["columns"]),
                str(row["row"]),
            )

    def test_the_by_row_projection_drops_no_field(self) -> None:
        """The keyed view carries every field of the row it keys.

        It used to enumerate three columns, so `declared_columns` was written
        onto the rows and lost before any consumer read a cell through it --
        and `comparison.py` reads cells only through this projection.  A
        projection that enumerates what it keeps loses the next field too.
        """
        ledger = RECORD["endowment_ledger"]
        by_row = ledger["by_row"]
        self.assertEqual(sorted(by_row), sorted(str(r["row"]) for r in ledger["rows"]))
        for row in ledger["rows"]:
            self.assertEqual(
                by_row[str(row["row"])],
                {key: value for key, value in row.items() if key != "row"},
            )
        self.assertEqual(
            by_row["coordinates_the_genesis_declaration_fixes"]["declared_columns"],
            ["control"],
        )

    def test_the_numeric_rows(self) -> None:
        by_row = RECORD["endowment_ledger"]["by_row"]
        self.assertEqual(by_row["coordinates_the_genesis_declaration_fixes"]["named"], 2)
        self.assertEqual(by_row["judgments_holding_at_genesis"]["named"], 2)
        self.assertEqual(by_row["judgments_holding_at_genesis"]["control"], 0)
        self.assertEqual(
            by_row["renamings_at_the_retained_regime"]["control"]["generators"], 1
        )
        self.assertEqual(
            by_row["renamings_at_the_retained_regime"]["unnamed"]["generators"], 2
        )

    def test_the_judgment_forms_are_computed_and_not_asserted(self) -> None:
        self.assertEqual(control.control_judgment_forms(), ["Admitted"])
        self.assertEqual(control.mirror_judgment_forms("U"), ["OnSide"])
        self.assertEqual(control.mirror_judgment_forms("O"), ["OnSide", "SideNamed"])

    def test_the_censuses_reproduce_the_declared_fractions(self) -> None:
        census = RECORD["censuses"]["withdrawal"]
        self.assertEqual(census["mirror"]["cells"], 64)
        self.assertEqual(census["mirror"]["separating_with_permutations_kept"], 28)
        self.assertEqual(census["mirror"]["separating_with_permutations_withdrawn"], 64)
        self.assertEqual(census["control"]["cells"], 8)
        self.assertEqual(census["control"]["separating_with_permutations_kept"], 2)
        self.assertEqual(census["control"]["separating_with_permutations_withdrawn"], 8)

    def test_the_observation_grammar_is_proved_inert(self) -> None:
        grammar = RECORD["observation_grammar"]
        self.assertTrue(grammar["inert"])
        self.assertEqual(grammar["census_cells_where_it_separates"], 0)
        self.assertGreater(grammar["census_cells_checked"], 0)
        self.assertEqual(grammar["extension_at_genesis"], 0)


class Policies(unittest.TestCase):
    def test_the_shared_policy_refuses_the_subject_rather_than_answering(self) -> None:
        block = RECORD["identity_policies"]
        self.assertEqual(block["shared_policy"]["marks"], 1)
        self.assertFalse(block["shared_policy"]["requirement_has_a_subject"])
        self.assertIn("not admitted", str(block["shared_policy"]["refusal_of_the_subject"]))
        self.assertEqual(block["declared_policy"]["marks"], 2)

    def test_the_removed_refusal_is_recorded_and_not_absorbed(self) -> None:
        block = RECORD["identity_policies"]
        self.assertEqual(block["removed_refusal"]["status"], "REMOVED, not absorbed")
        self.assertTrue(
            block["removed_refusal_computed_consequence"][
                "second_admission_of_an_admitted_label_is_a_no_op"
            ]
        )

    def test_the_never_supplied_refusal_still_fires_by_name(self) -> None:
        message = RECORD["identity_policies"]["never_supplied_token_refusal"]
        self.assertIn("was not supplied before admission", str(message))

    def test_the_caller_histories_report_the_order_fact_with_its_reason(self) -> None:
        block = RECORD["caller_histories"]
        self.assertTrue(block["the_two_orders_give_the_same_regime"])
        self.assertIn("NOT", str(block["order_fact_reason"]))
        self.assertEqual(
            [w["presented_position"] for w in block["wholes"]], ["before", "after"]
        )


class SecondMeasures(unittest.TestCase):
    def test_no_cross_world_mu2_difference_field_exists_anywhere(self) -> None:
        """Negative: the receipt must carry no raw cross-world mu2 difference."""
        found: list[str] = []

        def walk(node: object, path: str) -> None:
            if isinstance(node, dict):
                for key, value in node.items():
                    lowered = str(key).lower()
                    if (
                        "mu2" in lowered
                        and "restricted" not in lowered
                        and any(
                            word in lowered
                            for word in ("delta", "difference", "diff", "vs", "minus")
                        )
                    ):
                        found.append(f"{path}.{key}")
                    walk(value, f"{path}.{key}")
            elif isinstance(node, list):
                for index, value in enumerate(node):
                    walk(value, f"{path}[{index}]")

        walk(RECORD, "")
        self.assertEqual(found, [])

    def test_the_restricted_measure_is_zero_in_all_three_columns(self) -> None:
        block = RECORD["second_measures"]
        self.assertEqual(block["control_minima_by_mu2_restricted"]["minimum"], 0)
        self.assertEqual(block["mirror_minima_by_mu2_restricted"]["U"]["minimum"], 0)
        self.assertEqual(block["mirror_minima_by_mu2_restricted"]["O"]["minimum"], 0)
        self.assertEqual(block["problems"], [])

    def test_the_data_join_against_the_pin_covers_every_row(self) -> None:
        for reading in ("U", "O"):
            join = RECORD["second_measures"]["data_join_against_the_pin"][reading]
            self.assertEqual(join["rows_joined"], 48)
            self.assertEqual(join["mismatched_rows"], [])

    def test_the_data_join_would_name_a_divergence(self) -> None:
        """Negative: the join must be able to disagree."""
        from_pin = control.mu2_restricted_from_pin("U")
        self.assertEqual(from_pin["keep_labels"], 1)
        self.assertEqual(from_pin["base"], 0)

    def test_the_non_comparability_is_declared_beside_the_numbers(self) -> None:
        self.assertIn("NO cross-world", str(RECORD["second_measures"]["declaration"]))


class KeyChoiceAndSecondary(unittest.TestCase):
    def test_the_key_choice_is_shown_not_to_be_load_bearing(self) -> None:
        block = RECORD["key_choice_invariance"]
        self.assertTrue(block["agree_everywhere"])
        self.assertEqual(block["problems"], [])
        self.assertEqual(len(block["rows"]), 8)
        for row in block["rows"]:
            self.assertTrue(row["agree"])

    def test_the_secondary_flips_the_answer_and_never_decides(self) -> None:
        secondary = RECORD["secondary"]
        self.assertEqual(
            secondary["control_everywhere_satisfying"], ["withdraw_mark_permutations"]
        )
        self.assertEqual(
            secondary["decided"]["what_the_admitted_primitive_bought"],
            "NO_SATISFYING_CANDIDATE",
        )
        self.assertEqual(secondary["decided"]["unnamed_minimum"], 1)
        self.assertEqual(secondary["decided"]["unnamed_classes"], 2)
        self.assertEqual(
            RECORD["decided"]["what_the_admitted_primitive_bought"], "NOTHING_IN_COST"
        )

    def test_the_exclusion_is_computed_in_each_world_over_its_own_census(self) -> None:
        self.assertEqual(control.exclude_for_mirror([], MROWS, "U"), [])
        self.assertEqual(
            control.exclude_for_mirror(["x"], MROWS, "U"),
            everywhere_satisfying(eligible(MROWS["U"])),
        )


class Enumerator(unittest.TestCase):
    def test_the_enumerator_names_neither_carrier(self) -> None:
        """The one code path must be generic, and this is what holds it."""
        import ast

        source = (
            pathlib.Path(control.__file__).parent / "enumerate.py"
        ).read_text("utf-8")
        imported: list[str] = []
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.append(node.module)
        for name in imported:
            self.assertNotIn("candidates", name)
            self.assertNotIn("mirror", name)
            self.assertNotIn("model", name)

    def test_the_measures_are_computed_by_the_enumerator(self) -> None:
        self.assertEqual(newly_available({"a": True}, {"a": False}, ["a"]), 1)
        self.assertEqual(newly_available({"a": True}, {"a": True}, ["a"]), 0)

    def test_key_json_renders_a_key_and_refuses_a_non_key(self) -> None:
        self.assertEqual(key_json((1, ("a", "z"))), [1, ["a", "z"]])
        with self.assertRaises(TypeError):
            key_json({"not": "a key"})

    def test_permutations_of_refuses_a_malformed_entry(self) -> None:
        with self.assertRaises(TypeError):
            permutations_of([{"permutation": 3}])

    def test_the_minima_retain_every_tied_class(self) -> None:
        m: Any = minima(MROWS["U"], "mu1")
        self.assertEqual(m["class_count"], 3)
        self.assertFalse(m["unique"])

    def test_the_minima_report_an_empty_satisfying_set(self) -> None:
        empty: Any = minima([r for r in ROWS if not r["satisfies"]], "mu1")
        self.assertIsNone(empty["minimum"])
        self.assertEqual(empty["class_count"], 0)
        self.assertFalse(empty["unique"])

    def test_named_refuses_an_absent_row(self) -> None:
        with self.assertRaises(KeyError):
            named(ROWS, "no such point")

    def test_everywhere_satisfying_refuses_a_malformed_census(self) -> None:
        with self.assertRaises(TypeError):
            everywhere_satisfying([{"name": "x", "route_census": 3}])

    def test_the_carrier_view_refuses_a_candidate_of_the_other_world(self) -> None:
        carrier = ctl.SideFreeCarrier()
        with self.assertRaises(TypeError):
            carrier.point_name(mir.NULL_AUGMENTATION)

    def test_every_row_replays_from_genesis_and_agrees_with_its_carrier(self) -> None:
        for table in (ROWS, *MROWS.values()):
            for row in table:
                self.assertTrue(row["certified"], row["name"])
                self.assertTrue(row["replays_from_genesis"], row["name"])
                self.assertTrue(row["initial_datum_unchanged"], row["name"])
                self.assertTrue(row["event_follows_relation_empty"], row["name"])
                self.assertTrue(row["carrier_separability_agrees"], row["name"])


class RenderAndBounds(unittest.TestCase):
    def test_the_receipt_is_deterministic_and_within_its_bound(self) -> None:
        first = control.render(control.decide())
        second = control.render(control.decide())
        self.assertEqual(first, second)
        self.assertNotIn(b"\r", first)
        self.assertLess(len(first), 1_000_000)

    def test_the_record_carries_no_environment_value(self) -> None:
        text = control.render(RECORD).decode("utf-8")
        self.assertNotIn(str(TREE), text)
        self.assertNotIn("Users", text)

    def test_dig_reads_a_dotted_path_and_refuses_a_bad_one(self) -> None:
        self.assertEqual(control.dig({"a": [{"b": 1}]}, "a.0.b"), 1)
        with self.assertRaises(KeyError):
            control.dig({"a": 1}, "a.b")


if __name__ == "__main__":
    unittest.main()
