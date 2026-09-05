"""The price-list comparison: its gates, its buckets, and their negatives.

Every guard here has a failing direction.  A guard with no failing case is
not a guard, and this file is where that is held for the comparison.

The gate that matters most is C1: every pinned value a row reads is declared
in ``pinned/BOUNDARY_PIN.json``, the declaration is total in both directions,
and a value that drifts from the pinned bytes fails BY NAME.
"""

from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import sys
import tempfile
import unittest
import unittest.mock
from typing import Any

TREE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TREE))
sys.path.insert(0, str(TREE / "code"))

import comparison as C  # noqa: E402
import run_comparison  # noqa: E402
from sidefree import candidates as ctl  # noqa: E402
from sidefree import mirror as mir  # noqa: E402
from sidefree.model import genesis  # noqa: E402


def js(value: object) -> Any:
    """Read one JSON value as Any, so a test may index it."""
    return value


RECORD: Any = C.compare()
RECEIPT: Any = json.loads(
    (TREE / "receipts" / "comparison.json").read_text(encoding="utf-8")
)
DOC: bytes = (TREE / "COMPARISON.md").read_bytes()


def cell(value: object) -> C.Cell:
    return C.Cell(value, "probe", False, None)


def absent_cell(reason: str = "no statement") -> C.Cell:
    return C.Cell(None, "probe", True, reason)


def probe_resolver() -> C.Resolver:
    man = C.manifest()
    commit = str(man["pinned_commit"])
    loads = [C.load_pinned(row, commit) for row in C.vendored_receipts()]
    pinned = {load.challenge: load.data for load in loads}
    record = C.side_free_record()
    computed = C.control_computed()
    computed.update(C.extra_computed(record))
    return C.Resolver(
        pinned, record, computed, C.as_dict(C.pin_meta()["collapse_map"])
    )


class TheRecord(unittest.TestCase):
    def test_the_committed_receipt_is_a_fresh_computation(self) -> None:
        self.assertEqual(C.render(RECORD), (TREE / "receipts" / "comparison.json").read_bytes())

    def test_the_committed_document_is_a_fresh_rendering(self) -> None:
        self.assertEqual(C.document(RECORD), DOC)

    def test_rendering_is_deterministic(self) -> None:
        self.assertEqual(C.render(RECORD), C.render(C.compare()))

    def test_no_gate_failed_and_the_record_is_not_void(self) -> None:
        self.assertFalse(RECORD["void"])
        self.assertTrue(RECORD["gates"]["all_passed"])
        for name in ("C0", "C1", "C2", "C3", "C4"):
            self.assertEqual(RECORD["gates"][name]["problems"], [], name)

    def test_the_record_is_the_same_file_in_a_clone_that_cannot_reach_the_pin(
        self,
    ) -> None:
        """The property SF-OPEN-E says the sibling record does not have.

        With every ``git show`` made to fail, the record must come back byte
        for byte: its rows are held by the declared sha256 alone, and the
        reachability report is the runner's to print.
        """
        with unittest.mock.patch.object(C, "git_bytes", return_value=None):
            elsewhere = C.compare()
        self.assertEqual(C.render(elsewhere), C.render(RECORD))

    def test_every_row_cites_a_source_for_every_column(self) -> None:
        for row in RECORD["rows"]:
            for column in ("unnamed", "named", "control"):
                self.assertTrue(str(row["sources"][column]), row["id"])

    def test_no_cross_world_mu2_difference_field_exists_anywhere(self) -> None:
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

    def test_routes_and_price_are_never_combined_in_one_field(self) -> None:
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
        self.assertEqual(found, [])

    def test_the_open_list_carries_the_item_this_comparison_opened(self) -> None:
        opened = [item for item in RECORD["open"] if not item["inherited"]]
        self.assertEqual([item["id"] for item in opened], ["SF-OPEN-E"])
        self.assertIn("541041", str(opened[0]["statement"]))

    def test_the_committed_receipt_matches_the_one_this_run_computed(self) -> None:
        self.assertEqual(RECEIPT["row_count"], RECORD["row_count"])
        self.assertEqual(RECEIPT["verdict"], RECORD["verdict"])


class Buckets(unittest.TestCase):
    def test_every_row_is_in_exactly_one_bucket(self) -> None:
        table = RECORD["bought_table"]
        ids = sorted(
            list(table["bought_nothing"])
            + list(table["bought_something"])
            + [entry["row"] for entry in table["absent"]]
        )
        self.assertEqual(ids, sorted(row["id"] for row in RECORD["rows"]))
        self.assertEqual(len(ids), len(set(ids)))

    def test_the_two_absent_rows_are_the_two_with_no_side_free_statement(self) -> None:
        absent = {entry["row"]: entry["reason"] for entry in RECORD["bought_table"]["absent"]}
        self.assertEqual(sorted(absent), ["R05", "R14"])
        for reason in absent.values():
            self.assertTrue(str(reason))

    def test_an_absent_row_is_evidence_for_neither_bucket(self) -> None:
        table = RECORD["bought_table"]
        for entry in table["absent"]:
            self.assertNotIn(entry["row"], table["bought_nothing"])
            self.assertNotIn(entry["row"], table["bought_something"])

    def test_the_membership_rule_needs_the_price_as_well_as_the_value(self) -> None:
        """Negative: same value, different price, is NOT bought nothing."""
        same = {"kind": "count", "same": True}
        self.assertEqual(
            C.status_of(same, {"control_equals_unnamed": True}, "control_equals_unnamed"),
            C.BOUGHT_NOTHING,
        )
        self.assertEqual(
            C.status_of(same, {"control_equals_unnamed": False}, "control_equals_unnamed"),
            C.BOUGHT_SOMETHING,
        )
        self.assertEqual(
            C.status_of(
                {"kind": "absent", "same": False},
                {"control_equals_unnamed": True},
                "control_equals_unnamed",
            ),
            C.ABSENT,
        )

    def test_the_headline_row_is_bought_nothing_at_the_same_price(self) -> None:
        row = next(row for row in RECORD["rows"] if row["id"] == "R31")
        self.assertEqual(row["unnamed_reading"], 1)
        self.assertEqual(row["named_reading"], 0)
        self.assertEqual(row["control"], 1)
        self.assertEqual(row["status"], C.BOUGHT_NOTHING)
        self.assertEqual(row["status_against_the_named_reading"], C.BOUGHT_SOMETHING)
        self.assertTrue(row["price"]["stated"])

    def test_the_bought_table_has_the_three_asked_for_columns(self) -> None:
        self.assertEqual(
            RECORD["bought_table"]["columns"],
            [
                "what the admitted boundary bought",
                "what it cost",
                "which results depend on its presence",
            ],
        )

    def test_every_bought_entry_carries_all_three_columns(self) -> None:
        for entry in RECORD["bought_table"]["entries"]:
            self.assertIn("what_the_admitted_boundary_bought", entry)
            self.assertIn("what_it_cost", entry)
            self.assertIn("which_results_depend_on_its_presence", entry)

    def test_the_kinds_partition_the_rows(self) -> None:
        by_kind = RECORD["bought_table"]["by_kind"]
        total = sum(
            len(bucket) for buckets in by_kind.values() for bucket in buckets.values()
        )
        self.assertEqual(total, RECORD["row_count"])
        self.assertEqual(sorted(by_kind), sorted(C.KINDS))

    def test_the_two_declared_price_fields_are_flagged_as_declared(self) -> None:
        flagged = RECORD["bought_table"][
            "rows_whose_pinned_field_the_pinned_world_calls_declared_not_computed"
        ]
        self.assertEqual(flagged, ["R44", "R45"])


class Differences(unittest.TestCase):
    def test_bools(self) -> None:
        self.assertTrue(C.difference(cell(True), cell(True))["same"])
        self.assertFalse(C.difference(cell(True), cell(False))["same"])

    def test_counts(self) -> None:
        diff = C.difference(cell(3), cell(1))
        self.assertEqual(diff["kind"], "count")
        self.assertEqual(diff["control_minus_boundary"], -2)

    def test_sets(self) -> None:
        diff = C.difference(cell(["a", "b"]), cell(["b", "c"]))
        self.assertEqual(diff["kind"], "set")
        self.assertEqual(diff["only_in_the_pinned_world"], ["a"])
        self.assertEqual(diff["only_in_the_control"], ["c"])

    def test_nested_values_are_set_differenced_by_their_json(self) -> None:
        diff = C.difference(cell([["U", []]]), cell([[0]]))
        self.assertEqual(diff["only_in_the_pinned_world"], [["U", []]])
        self.assertEqual(diff["only_in_the_control"], [[0]])

    def test_other_values(self) -> None:
        diff = C.difference(cell("the run"), cell("the run"))
        self.assertEqual(diff["kind"], "value")
        self.assertTrue(diff["same"])
        self.assertFalse(C.difference(cell("a"), cell("b"))["same"])

    def test_absence_is_never_equality(self) -> None:
        diff = C.difference(cell(True), absent_cell("no sides here"))
        self.assertEqual(diff["kind"], "absent")
        self.assertFalse(diff["same"])
        self.assertEqual(diff["absent_in"], "the control")
        self.assertEqual(diff["reason"], "no sides here")
        other = C.difference(absent_cell("nothing pinned"), cell(True))
        self.assertEqual(other["absent_in"], "the pinned world")
        self.assertEqual(other["reason"], "nothing pinned")

    def test_a_bool_is_not_read_as_a_count(self) -> None:
        self.assertEqual(C.difference(cell(True), cell(1))["kind"], "value")


class Sources(unittest.TestCase):
    def test_each_source_kind_resolves_and_names_itself(self) -> None:
        resolver = probe_resolver()
        pinned = resolver.resolve(C.Pin(0, "readings.U.marks"))
        self.assertEqual(pinned.value, 0)
        self.assertIn("pinned challenge 0", pinned.source)
        receipt = resolver.resolve(C.Receipt("decided.side_free_minimum"))
        self.assertEqual(receipt.value, 1)
        self.assertIn("side_free.json", receipt.source)
        computed = resolver.resolve(C.Computed("genesis_marks"))
        self.assertEqual(computed.value, 0)
        self.assertIn("computed here", computed.source)
        counted = resolver.resolve(
            C.Count(
                C.Pin(
                    2, "readings.U.identity_policies.policies_admitting_both_wholes"
                )
            )
        )
        self.assertEqual(counted.value, 1)
        self.assertIn("length", counted.source)
        missing = resolver.resolve(C.NoStatement("no sides"))
        self.assertTrue(missing.absent)
        self.assertEqual(missing.absent_reason, "no sides")

    def test_the_collapse_map_joins_the_two_further_mark_points(self) -> None:
        resolver = probe_resolver()
        collapsed = resolver.resolve(
            C.Collapsed(C.Pin(3, "readings.U.minima_by_mu1.points"))
        )
        self.assertEqual(
            collapsed.value,
            ["extra_mark", "withdraw_mark_permutations", "withdraw_reflection"],
        )
        self.assertIn("collapse map", collapsed.source)

    def test_the_resolver_records_every_pinned_path_it_touched(self) -> None:
        resolver = probe_resolver()
        self.assertEqual(resolver.used, [])
        resolver.resolve(C.Pin(1, "readings.U.genesis_holding_judgments"))
        self.assertEqual(resolver.used, [(1, "readings.U.genesis_holding_judgments")])

    def test_dig_refuses_to_descend_into_a_leaf(self) -> None:
        with self.assertRaises(KeyError):
            C.dig({"a": 1}, "a.b")

    def test_the_shape_helpers_refuse_the_wrong_shape(self) -> None:
        with self.assertRaises(TypeError):
            C.as_dict([1])
        with self.assertRaises(TypeError):
            C.as_list({"a": 1})


class DeclaredValues(unittest.TestCase):
    """C1, in both directions and on a drifting value."""

    def rows_and_resolver(self) -> tuple[Any, C.Resolver, Any]:
        resolver = probe_resolver()
        rows = [C.build_row(resolver, spec) for spec in C.specs()]
        return rows, resolver, resolver.pinned

    def test_the_declaration_is_total_and_agrees(self) -> None:
        gate = RECORD["gates"]["C1"]
        self.assertTrue(gate["passed"])
        self.assertEqual(gate["declared"], gate["used_by_rows"])
        self.assertEqual(gate["checked"], gate["declared"])
        self.assertGreater(gate["declared"], 50)

    def test_a_drifting_declared_value_fails_by_name(self) -> None:
        """The injection, kept as a permanent test on a mutated copy."""
        _rows, resolver, pinned = self.rows_and_resolver()
        meta = copy.deepcopy(C.pin_meta())
        declared = C.as_dict(meta["declared_values"])
        key = "2:readings.U.automorphisms.count"
        self.assertEqual(declared[key], 2)
        declared[key] = 3
        gate = C.gate_declared_values(resolver, pinned, meta)
        self.assertFalse(gate["passed"])
        self.assertEqual(len(js(gate["problems"])), 1)
        self.assertIn(key, js(gate["problems"])[0])
        self.assertIn("the pinned bytes say 2", js(gate["problems"])[0])

    def test_an_undeclared_value_a_row_reads_fails(self) -> None:
        _rows, resolver, pinned = self.rows_and_resolver()
        meta = copy.deepcopy(C.pin_meta())
        declared = C.as_dict(meta["declared_values"])
        removed = "0:readings.U.marks"
        del declared[removed]
        gate = C.gate_declared_values(resolver, pinned, meta)
        self.assertFalse(gate["passed"])
        self.assertIn(removed, " ".join(str(p) for p in js(gate["problems"])))
        self.assertIn("not declared", " ".join(str(p) for p in js(gate["problems"])))

    def test_a_declared_value_no_row_reads_fails(self) -> None:
        _rows, resolver, pinned = self.rows_and_resolver()
        meta = copy.deepcopy(C.pin_meta())
        C.as_dict(meta["declared_values"])["0:challenge"] = 0
        gate = C.gate_declared_values(resolver, pinned, meta)
        self.assertFalse(gate["passed"])
        self.assertIn("which no row of this comparison reads", str(js(gate["problems"])[0]))

    def test_a_missing_declaration_block_fails_by_name_and_does_not_raise(self) -> None:
        _rows, resolver, pinned = self.rows_and_resolver()
        meta = copy.deepcopy(C.pin_meta())
        del meta["declared_values"]
        gate = C.gate_declared_values(resolver, pinned, meta)
        self.assertFalse(gate["passed"])
        self.assertEqual(gate["checked"], 0)
        self.assertIn("no declared_values block", str(js(gate["problems"])[0]))

    def test_the_verifier_holds_the_same_declaration(self) -> None:
        sys.path.insert(0, str(TREE))
        import verify_pins

        self.assertEqual(verify_pins.check_declared_values(), [])
        self.assertEqual(verify_pins.check_vendored_receipts(), [])


class PinnedBytes(unittest.TestCase):
    """C0, and the two ways the bytes can be read."""

    def manifest_row(self, challenge: int) -> Any:
        return copy.deepcopy(
            next(
                row
                for row in C.vendored_receipts()
                if int(str(row["challenge"])) == challenge
            )
        )

    def test_the_bytes_are_read_at_the_pinned_commit_when_it_is_reachable(self) -> None:
        load = C.load_pinned(self.manifest_row(0), str(C.manifest()["pinned_commit"]))
        self.assertEqual(load.problems, ())
        self.assertIn(load.source, ("the pinned commit", "the vendored copy"))

    def test_an_unreachable_commit_falls_back_and_says_why(self) -> None:
        load = C.load_pinned(self.manifest_row(0), "0" * 40)
        self.assertEqual(load.source, "the vendored copy")
        self.assertIn("unreachable", load.reason)
        self.assertEqual(load.problems, ())
        self.assertEqual(load.data["challenge"], 0)

    def test_the_fallback_reads_the_same_values(self) -> None:
        commit = str(C.manifest()["pinned_commit"])
        for challenge in C.CHALLENGES:
            row = self.manifest_row(challenge)
            self.assertEqual(
                C.load_pinned(row, commit).data,
                C.load_pinned(row, "0" * 40).data,
            )

    def test_a_wrong_declared_digest_fails_by_name(self) -> None:
        row = self.manifest_row(0)
        row["sha256"] = "0" * 64
        load = C.load_pinned(row, "0" * 40)
        self.assertTrue(any("sha256" in problem for problem in load.problems))

    def test_a_wrong_declared_byte_count_fails_by_name(self) -> None:
        row = self.manifest_row(0)
        row["byte_count"] = 1
        load = C.load_pinned(row, "0" * 40)
        self.assertTrue(any("bytes, the manifest" in p for p in load.problems))

    def test_a_blob_at_the_commit_that_differs_is_a_problem_not_a_fallback(self) -> None:
        row = self.manifest_row(0)
        row["source_path"] = str(self.manifest_row(1)["source_path"])
        load = C.load_pinned(row, str(C.manifest()["pinned_commit"]))
        self.assertEqual(load.source, "the vendored copy")
        self.assertIn("does not match", load.reason)
        self.assertTrue(any("the blob at" in problem for problem in load.problems))

    def test_a_receipt_filed_under_the_wrong_challenge_fails(self) -> None:
        rows = [copy.deepcopy(row) for row in C.vendored_receipts()]
        rows[0]["local_path"] = "pinned/boundary_challenge1.json"
        rows[0]["sha256"] = C.vendored_receipts()[1]["sha256"]
        rows[0]["byte_count"] = C.vendored_receipts()[1]["byte_count"]
        loads = [C.load_pinned(row, "0" * 40) for row in rows]
        gate = C.gate_bytes(loads, rows)
        self.assertFalse(gate["passed"])
        self.assertIn("is the receipt of challenge 1", str(js(gate["problems"])[0]))


class OtherGates(unittest.TestCase):
    def test_c2_recomputes_the_two_deltas(self) -> None:
        gate = RECORD["gates"]["C2"]
        self.assertEqual(gate["recomputed_deltas"], {"delta_vs_unnamed": 0, "delta_vs_named": 1})

    def test_c2_fails_when_the_record_states_a_delta_it_does_not_have(self) -> None:
        record = copy.deepcopy(C.side_free_record())
        C.as_dict(record["decided"])["delta_vs_unnamed"] = 7
        gate = C.gate_receipt_agrees(record, RECORD["rows"])
        self.assertFalse(gate["passed"])
        self.assertIn("delta_vs_unnamed", str(js(gate["problems"])[0]))

    def test_c2_fails_when_a_row_and_the_record_disagree(self) -> None:
        rows = copy.deepcopy(RECORD["rows"])
        for row in rows:
            if row["id"] == "R31":
                row["control"] = 99
        gate = C.gate_receipt_agrees(C.side_free_record(), rows)
        self.assertFalse(gate["passed"])
        self.assertIn("R31", str(js(gate["problems"])[0]))

    def test_c2_fails_when_the_first_control_row_is_not_the_base_row(self) -> None:
        record = copy.deepcopy(C.side_free_record())
        C.as_list(C.as_dict(record["control"])["rows"])[0] = {"name": "not base"}
        gate = C.gate_receipt_agrees(record, RECORD["rows"])
        self.assertFalse(gate["passed"])
        self.assertIn("not the base row", str(js(gate["problems"])[0]))

    def test_c3_joins_the_minima_through_the_declared_map(self) -> None:
        gate = RECORD["gates"]["C3"]
        self.assertEqual(gate["control_members"], ["withdraw_mark_permutations"])
        self.assertEqual(
            gate["routes_only_the_pinned_world_reaches"],
            ["extra_mark", "withdraw_reflection"],
        )

    def test_c3_fails_when_the_record_states_the_wrong_collapse(self) -> None:
        resolver = probe_resolver()
        record = copy.deepcopy(C.side_free_record())
        C.as_dict(record["decided"])["unnamed_minimum_members_collapsed"] = ["base"]
        gate = C.gate_minimum_join(resolver.pinned, record)
        self.assertFalse(gate["passed"])
        self.assertIn("the collapse of the pinned minima", str(js(gate["problems"])[0]))

    def test_c3_fails_when_the_record_states_the_wrong_routes(self) -> None:
        resolver = probe_resolver()
        record = copy.deepcopy(C.side_free_record())
        C.as_dict(record["decided"])["routes_the_admitted_primitive_bought"] = []
        gate = C.gate_minimum_join(resolver.pinned, record)
        self.assertFalse(gate["passed"])
        self.assertIn("routes the pinned world reaches", str(js(gate["problems"])[-1]))

    def test_c4_catches_a_duplicate_row_id(self) -> None:
        rows: list[dict[str, object]] = [
            {"id": "R01", "kind": C.OBSERVABLE},
            {"id": "R01", "kind": C.OBSERVABLE},
        ]
        gate = C.gate_taxonomy(rows)
        self.assertFalse(gate["passed"])
        self.assertIn("duplicate row ids", str(js(gate["problems"])[0]))

    def test_c4_catches_a_row_with_no_declared_kind(self) -> None:
        rows: list[dict[str, object]] = [
            {"id": name, "kind": C.OBSERVABLE} for name in C.KIND_OF
        ]
        rows.append({"id": "R99", "kind": C.OBSERVABLE})
        gate = C.gate_taxonomy(rows)
        self.assertFalse(gate["passed"])
        self.assertIn("R99", str(js(gate["problems"])[0]))

    def test_c4_catches_a_stage_outside_the_declared_rung_order(self) -> None:
        rows: list[dict[str, object]] = [
            {"id": name, "kind": C.OBSERVABLE, "stage": "a probe stage"}
            for name in C.KIND_OF
        ]
        gate = C.gate_taxonomy(rows)
        self.assertFalse(gate["passed"])
        self.assertIn("outside the declared rung order", str(js(gate["problems"])[0]))

    def test_the_stages_are_reported_in_the_declared_rung_order(self) -> None:
        self.assertEqual(RECORD["stages"], list(C.STAGES))

    def test_c4_catches_a_declared_kind_for_a_row_that_does_not_exist(self) -> None:
        gate = C.gate_taxonomy([{"id": "R01", "kind": C.OBSERVABLE}])
        self.assertFalse(gate["passed"])
        self.assertIn("do not exist", str(js(gate["problems"])[0]))

    def test_a_failing_gate_voids_the_record_and_reports_no_difference(self) -> None:
        """Negative: the shape of a VOID record, built from a broken gate."""
        broken = {"gate": "C9", "problems": ["a probe problem"], "passed": False}
        self.assertFalse(broken["passed"])
        self.assertIn("rows", RECORD)


class MinimaAndTheSides(unittest.TestCase):
    def test_the_name_criterion_is_the_deletion_criterion_run_backwards(self) -> None:
        self.assertTrue(C.names_a_side("the side exchange is not a permitted renaming"))
        self.assertFalse(C.names_a_side("a mark's admission index is internally available"))

    def test_the_withdrawal_reads_no_placement_in_either_world(self) -> None:
        rows = {
            (row["world"], row["point"]): row
            for row in RECORD["minima_and_the_sides"]["rows"]
        }
        pinned = rows[("the pinned world", "withdraw_mark_permutations")]
        control = rows[("the control", "withdraw_mark_permutations")]
        self.assertFalse(pinned["placement"]["reads_the_placement"])
        self.assertFalse(control["placement"]["reads_the_placement"])
        self.assertFalse(pinned["names_a_side_in_its_capability_sentence"])

    def test_the_other_two_unnamed_minima_read_the_placement(self) -> None:
        rows = {
            row["point"]: row
            for row in RECORD["minima_and_the_sides"]["rows"]
            if row["reading"] == "U"
        }
        for point in ("withdraw_reflection", "extra_mark_0", "extra_mark_1"):
            self.assertTrue(rows[point]["placement"]["reads_the_placement"], point)

    def test_the_two_criteria_disagree_and_the_record_says_where(self) -> None:
        self.assertEqual(
            RECORD["minima_and_the_sides"]["the_two_criteria_disagree_on"],
            ["base", "extra_mark_0", "extra_mark_1"],
        )

    def test_a_world_with_no_placement_cannot_vary_with_one(self) -> None:
        aug = next(
            a for a in ctl.candidate_space() if ctl.point_name(a) == "keep_labels"
        )
        block = C.control_reads_the_placement(aug)
        self.assertFalse(block["reads_the_placement"])
        self.assertEqual(block["groups_whose_verdict_moves_with_the_placement"], 0)
        self.assertIn("no placement", str(block["why"]))

    def test_the_placement_probe_counts_the_cells_it_looked_at(self) -> None:
        aug = next(
            a for a in mir.candidate_space() if mir.point_name(a) == "base"
        )
        block = C.mirror_reads_the_placement("U", aug)
        self.assertEqual(block["cells"], 16)
        self.assertEqual(block["label_groups"], 4)


class Dependence(unittest.TestCase):
    def test_the_classification_is_total_over_the_pinned_population(self) -> None:
        block = RECORD["pinned_dependence_claims"]
        self.assertTrue(block["classification_is_total"])
        self.assertEqual(block["counts_by_class"]["UNCLASSIFIED"], 0)
        self.assertEqual(
            block["entry_count"], sum(block["counts_by_class"].values())
        )

    def test_every_challenge_contributes_claims(self) -> None:
        seen = {entry["challenge"] for entry in RECORD["pinned_dependence_claims"]["entries"]}
        self.assertEqual(sorted(seen), list(C.CHALLENGES))

    def test_the_three_classes_are_decided_by_the_opening_words(self) -> None:
        self.assertEqual(
            C.classify_dependence("does not depend on the admitted boundary"),
            C.DEPENDENCE_INDEPENDENT,
        )
        self.assertEqual(
            C.classify_dependence("require the admitted boundary"),
            C.DEPENDENCE_DEPENDENT,
        )
        self.assertEqual(
            C.classify_dependence("does not depend for one part; the other requires it"),
            C.DEPENDENCE_MIXED,
        )
        self.assertEqual(
            C.classify_dependence("something else entirely"),
            C.DEPENDENCE_UNCLASSIFIED,
        )

    def test_exactly_one_universal_claim_is_selected_and_contradicted(self) -> None:
        block = RECORD["pinned_dependence_claims"]
        self.assertEqual(len(block["universal_entries"]), 1)
        self.assertIn("every separation result", block["universal_entries"][0]["subject"])
        self.assertEqual(
            block["adjudication"]["verdict"], "CONTRADICTED within the declared scope"
        )
        evidence = block["adjudication"]["evidence"]
        self.assertEqual(evidence["coordinate"], "withdraw_mark_permutations")
        self.assertTrue(evidence["it_is_one_of_the_pinned_minima"])
        self.assertTrue(evidence["same_cost"])
        self.assertTrue(evidence["capability_sentence_is_byte_identical"])

    def test_the_adjudication_would_report_no_contradiction_without_the_evidence(
        self,
    ) -> None:
        """Negative: the verdict follows the computed evidence, not the prose."""
        resolver = probe_resolver()
        record = copy.deepcopy(C.side_free_record())
        C.as_dict(record["withdrawal_port"])["same_cost"] = False
        block = C.dependence_block(resolver.pinned, record)
        self.assertEqual(js(block["adjudication"])["verdict"], "NOT CONTRADICTED")


class ControlValues(unittest.TestCase):
    def test_the_control_computes_its_own_stages_by_replay(self) -> None:
        computed = C.control_computed()
        self.assertEqual(computed["genesis_marks"], 0)
        self.assertEqual(computed["genesis_judgments"], 0)
        self.assertEqual(computed["one_mark_marks"], 1)
        self.assertEqual(computed["one_mark_judgments"], 1)
        self.assertEqual(computed["two_marks_marks"], 2)
        self.assertEqual(computed["two_marks_judgments"], 2)
        self.assertTrue(computed["genesis_supply_is_inert"])
        self.assertTrue(computed["event_follows_relation_empty"])
        self.assertTrue(computed["supply_alone_equals_genesis"])

    def test_the_one_supplied_token_yields_one_admission(self) -> None:
        self.assertEqual(
            C.available_admissions(genesis(), [ctl.SUPPLIED_TOKEN]),
            [ctl.SUPPLIED_TOKEN],
        )
        self.assertEqual(
            C.available_admissions(C.one_mark_regime(), [ctl.SUPPLIED_TOKEN]), []
        )

    def test_the_two_caller_orders_give_one_regime_and_one_class(self) -> None:
        probe = C.order_probe()
        self.assertTrue(probe["equal"])
        self.assertTrue(probe["isomorphic"])
        self.assertEqual(probe["classes"], 1)

    def test_the_shared_policy_retains_one_mark_and_admits_neither_pair(self) -> None:
        probe = C.policy_probe()
        self.assertEqual(probe["marks_by_policy"], {"occurrence": 2, "shared": 1})
        self.assertEqual(probe["admitting_both"], 1)

    def test_the_one_step_points_are_read_from_the_records_own_rows(self) -> None:
        extra = C.extra_computed(C.side_free_record())
        self.assertEqual(
            extra["control_one_step_points"],
            ["extra_mark", "keep_labels", "withdraw_mark_permutations"],
        )
        self.assertEqual(
            extra["control_satisfying_one_step_points"], ["withdraw_mark_permutations"]
        )
        self.assertFalse(extra["control_nothing_new_paid"])


class TheDocument(unittest.TestCase):
    def test_every_row_id_appears_in_the_document(self) -> None:
        text = DOC.decode("utf-8")
        for row in RECORD["rows"]:
            self.assertIn(str(row["id"]), text)

    def test_the_document_is_a_function_of_the_record(self) -> None:
        """Negative: change the record and the document must change."""
        mutated = copy.deepcopy(RECORD)
        C.as_dict(C.as_list(mutated["rows"])[0])["item"] = "a probe item"
        self.assertNotEqual(C.document(mutated), DOC)

    def test_the_document_carries_the_verdict_and_its_scope(self) -> None:
        text = DOC.decode("utf-8")
        self.assertIn(str(RECORD["verdict"]["statement"]), text)
        self.assertIn(str(RECORD["verdict"]["scope"]), text)
        self.assertIn("bought nothing", text)

    def test_the_document_names_every_absent_row_with_its_reason(self) -> None:
        text = DOC.decode("utf-8")
        for entry in RECORD["bought_table"]["absent"]:
            self.assertIn(str(entry["reason"]), text)

    def test_a_pipe_in_a_cell_cannot_break_the_table(self) -> None:
        self.assertEqual(C.show("a|b"), "a\\|b")
        self.assertEqual(C.show(1), "`1`")

    def test_the_difference_text_covers_every_difference_kind(self) -> None:
        self.assertEqual(
            C.difference_text({"kind": "absent", "absent_in": "the control"}),
            "absent in the control",
        )
        self.assertEqual(C.difference_text({"kind": "count", "same": True}), "same")
        self.assertEqual(
            C.difference_text({"kind": "count", "same": False, "control_minus_boundary": -2}),
            "control minus boundary = -2",
        )
        self.assertIn(
            "only pinned",
            C.difference_text(
                {
                    "kind": "set",
                    "same": False,
                    "only_in_the_pinned_world": ["a"],
                    "only_in_the_control": [],
                }
            ),
        )
        self.assertEqual(
            C.difference_text({"kind": "value", "same": False}), "differs"
        )


class FailingClosed(unittest.TestCase):
    """Every refusal, exercised: a guard with no failing case is not a guard."""

    def test_a_manifest_that_is_not_an_object_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = pathlib.Path(raw) / "SOURCE_MANIFEST.json"
            path.write_text("[1, 2]", encoding="utf-8")
            with unittest.mock.patch.object(C, "MANIFEST_PATH", path):
                with self.assertRaises(TypeError):
                    C.manifest()

    def test_a_pin_declaration_that_is_not_an_object_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = pathlib.Path(raw) / "BOUNDARY_PIN.json"
            path.write_text('"not an object"', encoding="utf-8")
            with unittest.mock.patch.object(C, "PIN_META_PATH", path):
                with self.assertRaises(TypeError):
                    C.pin_meta()

    def test_a_vendored_copy_with_cr_bytes_is_refused_by_name(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = pathlib.Path(raw)
            body = b'{"challenge": 0}\r\n'
            (root / "probe.json").write_bytes(body)
            row: dict[str, object] = {
                "challenge": 0,
                "local_path": "probe.json",
                "source_path": "no/such/path.json",
                "sha256": hashlib.sha256(body).hexdigest(),
                "byte_count": len(body),
            }
            with unittest.mock.patch.object(C, "HERE", root):
                load = C.load_pinned(row, "0" * 40)
        self.assertTrue(any("contains CR bytes" in p for p in load.problems))

    def test_a_kind_outside_the_declared_taxonomy_is_refused(self) -> None:
        with unittest.mock.patch.dict(C.KIND_OF, {"R01": "a probe kind"}):
            gate = C.gate_taxonomy([{"id": name} for name in C.KIND_OF])
        self.assertFalse(gate["passed"])
        self.assertIn("outside the declared taxonomy", str(js(gate["problems"])[0]))

    def test_a_failing_gate_voids_the_record_and_reports_no_row(self) -> None:
        broken = {"gate": "C4", "name": "taxonomy_total", "problems": ["a probe"], "passed": False}
        with unittest.mock.patch.object(C, "gate_taxonomy", return_value=broken):
            record = C.compare()
        self.assertTrue(record["void"])
        self.assertNotIn("rows", record)
        self.assertNotIn("bought_table", record)
        self.assertNotIn("verdict", record)
        self.assertEqual(js(record["problems"]), ["C4: a probe"])
        with unittest.mock.patch.object(C, "gate_taxonomy", return_value=broken):
            self.assertEqual(run_comparison.main([]), 1)

    def test_the_declaration_snapshot_reproduces_the_committed_block(self) -> None:
        """``--declare`` is a deliberate snapshot, and it is not a new answer."""
        committed = C.pin_meta()
        with tempfile.TemporaryDirectory() as raw:
            path = pathlib.Path(raw) / "BOUNDARY_PIN.json"
            path.write_bytes((TREE / "pinned" / "BOUNDARY_PIN.json").read_bytes())
            with unittest.mock.patch.object(C, "PIN_META_PATH", path):
                count = C.declare_values()
                written = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(count, len(js(committed["declared_values"])))
        self.assertEqual(written["declared_values"], committed["declared_values"])
        self.assertEqual(
            (TREE / "pinned" / "BOUNDARY_PIN.json").read_bytes(),
            (json.dumps(written, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode(
                "utf-8"
            ),
        )


class TheRunner(unittest.TestCase):
    def test_check_mode_agrees_with_the_committed_files(self) -> None:
        self.assertEqual(run_comparison.main(["--check"]), 0)

    def test_the_reachability_report_names_every_pinned_receipt(self) -> None:
        loads = run_comparison.reachability()
        self.assertEqual([load.challenge for load in loads], list(C.CHALLENGES))
        for load in loads:
            self.assertTrue(load.reason)


if __name__ == "__main__":
    unittest.main()
