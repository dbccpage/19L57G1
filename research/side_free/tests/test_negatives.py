"""Every gate, driven to its failing case.

A gate that has never failed on the defect it exists to catch is only quiet.
This file makes each one fail by name, on a temporary copy or a temporary
rebinding, and never by editing a committed file.  No receipt, axiom log or
pin is written from here.
"""

from __future__ import annotations

import contextlib
import copy
import json
import pathlib
import sys
import tempfile
import unittest
from typing import Any, Iterator

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "code"))

from sidefree import candidates as ctl  # noqa: E402
from sidefree.model import Regime  # noqa: E402
from sidefree import control  # noqa: E402
from sidefree import mirror as mir  # noqa: E402
from sidefree.enumerate import Json  # noqa: E402
from sidefree.requirement import (  # noqa: E402
    REQUIREMENT,
    REQUIREMENT_SECOND_READING,
)

TREE = pathlib.Path(__file__).resolve().parent.parent
ROWS: Any = control.control_rows()
MROWS: Any = control.mirror_rows()


@contextlib.contextmanager
def swapped_pin(mutate: Any) -> Iterator[None]:
    """Run with a MUTATED COPY of the vendored pin in a temporary file.

    The committed bytes are never touched: the module's path constant is
    repointed for the duration and restored afterwards.
    """
    payload: Any = json.loads(control.PIN_PATH.read_text(encoding="utf-8"))
    assert callable(mutate)
    mutate(payload)
    original = control.PIN_PATH
    with tempfile.TemporaryDirectory() as directory:
        temporary = pathlib.Path(directory) / "probe.json"
        temporary.write_bytes(json.dumps(payload).encode("utf-8"))
        control.PIN_PATH = temporary
        try:
            yield
        finally:
            control.PIN_PATH = original


@contextlib.contextmanager
def swapped(module: object, name: str, value: object) -> Iterator[None]:
    original = getattr(module, name)
    setattr(module, name, value)
    try:
        yield
    finally:
        setattr(module, name, original)


class PinGate(unittest.TestCase):
    def test_a_flipped_digest_is_named(self) -> None:
        with swapped_pin(lambda payload: payload.update({"zzz_probe": 1})):
            gate: Any = control.gate_pin_bytes()
        self.assertFalse(gate["passed"])
        joined = " ".join(str(p) for p in gate["problems"])
        self.assertIn("sha256", joined)
        self.assertIn("git blob", joined)
        self.assertIn("byte count", joined)

    def test_a_cr_byte_in_the_pin_is_named(self) -> None:
        original = control.PIN_PATH
        with tempfile.TemporaryDirectory() as directory:
            temporary = pathlib.Path(directory) / "probe.json"
            temporary.write_bytes(control.PIN_PATH.read_bytes() + b"\r")
            control.PIN_PATH = temporary
            try:
                gate: Any = control.gate_pin_bytes()
            finally:
                control.PIN_PATH = original
        self.assertFalse(gate["passed"])
        self.assertTrue(any("CR bytes" in str(p) for p in gate["problems"]))

    def test_a_metadata_edit_is_named(self) -> None:
        meta: Any = json.loads(control.PIN_META_PATH.read_text(encoding="utf-8"))
        meta["vendored"]["byte_count"] = 1
        original = control.PIN_META_PATH
        with tempfile.TemporaryDirectory() as directory:
            temporary = pathlib.Path(directory) / "meta.json"
            temporary.write_text(json.dumps(meta), encoding="utf-8")
            control.PIN_META_PATH = temporary
            try:
                gate: Any = control.gate_pin_bytes()
            finally:
                control.PIN_META_PATH = original
        self.assertFalse(gate["passed"])
        self.assertTrue(any("byte_count" in str(p) for p in gate["problems"]))

    def test_a_non_object_pin_is_refused_by_name(self) -> None:
        original = control.PIN_PATH
        original_meta = control.PIN_META_PATH
        with tempfile.TemporaryDirectory() as directory:
            temporary = pathlib.Path(directory) / "probe.json"
            temporary.write_text("[]", encoding="utf-8")
            control.PIN_PATH = temporary
            control.PIN_META_PATH = temporary
            try:
                with self.assertRaises(TypeError):
                    control.pin_data()
                with self.assertRaises(TypeError):
                    control.pin_meta()
            finally:
                control.PIN_PATH = original
                control.PIN_META_PATH = original_meta

    def test_a_missing_vendored_block_is_refused(self) -> None:
        original = control.PIN_META_PATH
        with tempfile.TemporaryDirectory() as directory:
            temporary = pathlib.Path(directory) / "meta.json"
            temporary.write_text(json.dumps({"vendored": []}), encoding="utf-8")
            control.PIN_META_PATH = temporary
            try:
                with self.assertRaises(TypeError):
                    control.gate_pin_bytes()
            finally:
                control.PIN_META_PATH = original

    def test_a_malformed_reading_block_is_refused(self) -> None:
        with swapped_pin(lambda payload: payload.update({"readings": {"U": []}})):
            with self.assertRaises(TypeError):
                control.pin_reading("U")

        def break_points(payload: Any) -> None:
            payload["readings"]["U"]["points"] = 3
            payload["readings"]["U"]["base"] = []

        with swapped_pin(break_points):
            with self.assertRaises(TypeError):
                control.pin_rows("U", "points")
            with self.assertRaises(TypeError):
                control.pin_verdict_rows("U")


    def test_an_unreachable_pinned_commit_is_reported_as_skipped(self) -> None:
        """Negative: the conditional check must never pass quietly."""
        manifest: Any = json.loads(control.MANIFEST_PATH.read_text(encoding="utf-8"))
        manifest["pinned_commit"] = "0" * 40
        original = control.MANIFEST_PATH
        with tempfile.TemporaryDirectory() as directory:
            temporary = pathlib.Path(directory) / "manifest.json"
            temporary.write_text(json.dumps(manifest), encoding="utf-8")
            control.MANIFEST_PATH = temporary
            try:
                check: Any = control.commit_check()
            finally:
                control.MANIFEST_PATH = original
        self.assertEqual(check["status"], "SKIPPED")
        self.assertIn("unreachable", str(check["reason"]))
        self.assertIn("residual", check)


class RequirementGate(unittest.TestCase):
    def test_reinserting_the_deleted_phrase_is_named(self) -> None:
        injected = REQUIREMENT.replace(
            "internally separable", "internally separable under a reading"
        )
        with swapped(control, "REQUIREMENT", injected):
            gate: Any = control.gate_requirement_texts()
        self.assertFalse(gate["passed"])
        self.assertTrue(any("byte for byte" in str(p) for p in gate["problems"]))

    def test_a_deleted_word_in_the_control_string_is_named(self) -> None:
        with swapped(control, "REQUIREMENT", REQUIREMENT + " on a side"):
            gate: Any = control.gate_requirement_texts()
        self.assertFalse(gate["passed"])
        self.assertTrue(any("still name" in str(p) for p in gate["problems"]))

    def test_an_ambiguous_deletion_is_named(self) -> None:
        with swapped(control, "DELETED_FROM_DECLARED", " the"):
            gate: Any = control.gate_requirement_texts()
        self.assertFalse(gate["passed"])
        self.assertTrue(any("not unambiguous" in str(p) for p in gate["problems"]))

    def test_a_changed_second_reading_is_named(self) -> None:
        with swapped(
            control, "REQUIREMENT_SECOND_READING", REQUIREMENT_SECOND_READING + "."
        ):
            gate: Any = control.gate_requirement_texts()
        self.assertFalse(gate["passed"])

    def test_a_changed_retained_pair_is_named(self) -> None:
        with swapped(control, "RETAINED_MARKS", (0, 2)):
            gate: Any = control.gate_requirement_texts()
        self.assertFalse(gate["passed"])
        self.assertTrue(any("retained marks" in str(p) for p in gate["problems"]))


class CapabilityGate(unittest.TestCase):
    def test_one_altered_capability_character_is_named(self) -> None:
        altered = dict(ctl.CAPABILITY_OF)
        altered["keep_labels"] = altered["keep_labels"].replace("label", "labels", 1)
        with swapped(ctl, "CAPABILITY_OF", altered):
            gate: Any = control.gate_capability_texts()
        self.assertFalse(gate["passed"])
        self.assertTrue(
            any("not byte-identical" in str(p) for p in gate["problems"])
        )

    def test_a_renamed_coordinate_is_named(self) -> None:
        renamed = ("withdraw_mark_permutations", "keep_label", "extra_mark")
        altered = dict(ctl.CAPABILITY_OF)
        altered["keep_label"] = altered["keep_labels"]
        with swapped(ctl, "COORDINATES", renamed), swapped(ctl, "CAPABILITY_OF", altered):
            gate: Any = control.gate_capability_texts()
        self.assertFalse(gate["passed"])
        joined = " ".join(str(p) for p in gate["problems"])
        self.assertIn("keep_label", joined)

    def test_a_coordinate_moved_across_the_criterion_is_named(self) -> None:
        def add_a_side_word(payload: Any) -> None:
            block = payload["candidate_space"]["capability_of"]
            block["keep_labels"] = block["keep_labels"] + ", one per side"

        with swapped_pin(add_a_side_word):
            gate: Any = control.gate_capability_texts()
        self.assertFalse(gate["passed"])
        self.assertTrue(
            any("mechanical partition" in str(p) for p in gate["problems"])
        )

    def test_a_malformed_coordinate_list_is_refused(self) -> None:
        def break_list(payload: Any) -> None:
            payload["candidate_space"]["coordinates"] = "not a list"

        with swapped_pin(break_list):
            with self.assertRaises(TypeError):
                control.gate_capability_texts()


class VerdictGate(unittest.TestCase):
    def test_a_mutated_pinned_verdict_is_named(self) -> None:
        def flip(payload: Any) -> None:
            payload["readings"]["U"]["base"]["satisfies"] = True

        with swapped_pin(flip):
            gate: Any = control.gate_verdict_replay()
        self.assertFalse(gate["passed"])
        self.assertTrue(any("row base" in str(p) for p in gate["problems"]))

    def test_a_malformed_entry_list_is_refused(self) -> None:
        def break_entries(payload: Any) -> None:
            payload["readings"]["U"]["base"]["automorphism_entries"] = 3

        with swapped_pin(break_entries):
            with self.assertRaises(TypeError):
                control.gate_verdict_replay()


class LemmaGate(unittest.TestCase):
    def test_a_lemma_violation_is_named(self) -> None:
        injected: Any = mir.forgetful_lemma(True)
        with swapped(mir, "forgetful_lemma", lambda _inject: injected):
            gate: Any = control.gate_forgetful_lemma()
        self.assertFalse(gate["passed"])
        self.assertTrue(any("lemma fails" in str(p) for p in gate["problems"]))

    def test_a_corollary_violation_and_a_vacuous_census_are_named(self) -> None:
        broken: Any = dict(mir.forgetful_lemma(False))
        broken["corollary_holds"] = False
        broken["first_corollary_violation"] = {"probe": True}
        broken["non_vacuous"] = False
        with swapped(mir, "forgetful_lemma", lambda _inject: broken):
            gate: Any = control.gate_forgetful_lemma()
        self.assertFalse(gate["passed"])
        joined = " ".join(str(p) for p in gate["problems"])
        self.assertIn("corollary fails", joined)
        self.assertIn("vacuous", joined)


class MirrorGate(unittest.TestCase):
    def test_a_wrong_refused_bundle_count_is_named(self) -> None:
        rows: Any = {r: [dict(row) for row in table] for r, table in MROWS.items()}
        rows["U"][0]["bundles"] = not bool(rows["U"][0]["bundles"])
        gate: Any = control.gate_mirror_matches_the_pin(rows)
        self.assertFalse(gate["passed"])
        self.assertTrue(
            any("refused bundles" in str(p) or "bundles" in str(p) for p in gate["problems"])
        )

    def test_a_wrong_detail_field_is_named(self) -> None:
        rows: Any = {r: [dict(row) for row in table] for r, table in MROWS.items()}
        for row in rows["U"]:
            if str(row["name"]) == "base":
                row["orbit_size"] = 99
        gate: Any = control.gate_mirror_matches_the_pin(rows)
        self.assertFalse(gate["passed"])
        self.assertTrue(any("orbit_size" in str(p) for p in gate["problems"]))

    def test_a_wrong_minimum_and_wrong_classes_are_named(self) -> None:
        rows: Any = {r: [dict(row) for row in table] for r, table in MROWS.items()}
        for row in rows["U"]:
            if str(row["name"]) == "withdraw_reflection":
                row["satisfies"] = False
        gate: Any = control.gate_mirror_matches_the_pin(rows)
        self.assertFalse(gate["passed"])
        joined = " ".join(str(p) for p in gate["problems"])
        self.assertIn("minima", joined)

    def test_a_malformed_pinned_minima_block_is_refused(self) -> None:
        def break_minima(payload: Any) -> None:
            payload["readings"]["U"]["minima_by_mu1"] = []

        with swapped_pin(break_minima):
            with self.assertRaises(TypeError):
                control.gate_mirror_matches_the_pin(MROWS)


class ReportGuards(unittest.TestCase):
    def test_the_json_readers_refuse_a_wrong_shape_by_name(self) -> None:
        self.assertEqual(control.as_list([1]), [1])
        self.assertEqual(control.as_dict({"a": 1}), {"a": 1})
        with self.assertRaises(TypeError) as caught:
            control.as_list({"a": 1})
        self.assertIn("expected a list", str(caught.exception))
        with self.assertRaises(TypeError) as caught:
            control.as_dict([1])
        self.assertIn("expected an object", str(caught.exception))

    def test_the_generator_count_refuses_a_malformed_row(self) -> None:
        with self.assertRaises(TypeError):
            control.generators({"permitted_renamings": 3}, ("mark_permutations",))

    def test_the_endowment_refuses_a_row_with_no_collateral_facts(self) -> None:
        rows: Any = [dict(r) for r in ROWS]
        for row in rows:
            if str(row["name"]) == "base":
                row["collateral_facts"] = 3
        with self.assertRaises(TypeError):
            control.endowment_ledger(rows, MROWS)

    def test_the_data_join_refuses_a_malformed_pinned_block(self) -> None:
        def break_base(payload: Any) -> None:
            payload["readings"]["U"]["base"] = []

        with swapped_pin(break_base):
            with self.assertRaises(TypeError):
                control.mu2_restricted_from_pin("U")

        def break_base_facts(payload: Any) -> None:
            payload["readings"]["U"]["base"]["collateral_facts"] = 3

        with swapped_pin(break_base_facts):
            with self.assertRaises(TypeError):
                control.mu2_restricted_from_pin("U")

        def break_point_facts(payload: Any) -> None:
            payload["readings"]["U"]["points"][0]["collateral_facts"] = 3

        with swapped_pin(break_point_facts):
            with self.assertRaises(TypeError):
                control.mu2_restricted_from_pin("U")

    def test_the_data_join_names_a_divergence(self) -> None:
        def bump(payload: Any) -> None:
            payload["readings"]["U"]["points"][0]["collateral_facts"][
                "order_internally_available"
            ] = True

        with swapped_pin(bump):
            block: Any = control.mu2_block(ROWS, MROWS)
        self.assertNotEqual(block["problems"], [])

    def test_the_key_choice_block_refuses_a_malformed_row(self) -> None:
        with self.assertRaises(TypeError):
            control.key_choice_block([{"name": "x", "satisfies_under_key_choice": 3}])

    def test_the_key_choice_block_names_a_disagreement(self) -> None:
        block: Any = control.key_choice_block(
            [{"name": "probe", "satisfies_under_key_choice": {"arity": True, "empty": False}}]
        )
        self.assertFalse(block["agree_everywhere"])
        self.assertTrue(any("disagree" in str(p) for p in block["problems"]))

    def test_the_residue_judgment_can_separate_where_it_is_asked_to(self) -> None:
        """The inertness claim is over the census, not over the predicate."""
        self.assertTrue(control.admitted_separates(Regime(("a",))))
        self.assertFalse(control.admitted_separates(Regime(("a", "a"))))

    def test_the_form_collector_reports_an_absent_form(self) -> None:
        self.assertEqual(control.forms_with_a_holding_instance([("X", False)]), [])
        self.assertEqual(control.forms_with_a_holding_instance([("X", True)]), ["X"])

    def test_the_refusal_capture_reports_nothing_when_nothing_is_refused(self) -> None:
        self.assertIsNone(control.refusal_message(lambda: None))
        self.assertEqual(
            control.refusal_message(lambda: (_ for _ in ()).throw(ValueError("named"))),
            "named",
        )

    def test_the_decided_object_reports_an_absent_minimum(self) -> None:
        """Negative: with nothing satisfying anywhere, no difference is reported."""
        blank_rows: Any = [dict(r, satisfies=False) for r in ROWS]
        blank_mirror: Any = {
            reading: [dict(r, satisfies=False) for r in table]
            for reading, table in MROWS.items()
        }
        decided: Any = control.decided_object(blank_rows, blank_mirror, True)
        self.assertIsNone(decided["side_free_minimum"])
        self.assertIsNone(decided["delta_vs_unnamed"])
        self.assertEqual(
            decided["what_the_admitted_primitive_bought"], "NO_SATISFYING_CANDIDATE"
        )

    def test_a_side_free_minimum_with_no_pinned_minimum_reports_no_difference(
        self,
    ) -> None:
        blank_mirror: Any = {
            reading: [dict(r, satisfies=False) for r in table]
            for reading, table in MROWS.items()
        }
        decided: Any = control.decided_object(ROWS, blank_mirror, True)
        self.assertEqual(decided["side_free_minimum"], 1)
        self.assertIsNone(decided["delta_vs_unnamed"])
        self.assertIsNone(decided["delta_vs_named"])
        self.assertEqual(decided["routes_the_admitted_primitive_bought"], [])

    def test_a_failed_gate_voids_the_record(self) -> None:
        decided: Any = control.decided_object(ROWS, MROWS, False)
        self.assertEqual(decided["what_the_admitted_primitive_bought"], "VOID")

    def test_a_minimum_with_several_members_reports_no_definition_level_flag(
        self,
    ) -> None:
        decided: Any = control.decided_object(MROWS["U"], MROWS, True)
        self.assertIsNone(decided["side_free_minimum_is_definition_level"])


class MirrorCarrierExtras(unittest.TestCase):
    def test_a_fresh_label_keyed_admission_appends(self) -> None:
        r = mir.Regime("U", (), ())
        self.assertEqual(mir.step(r, mir.AdmitMark("a", 1)).placement, (1,))

    def test_the_deep_copy_of_a_row_is_not_the_row(self) -> None:
        row = copy.deepcopy(ROWS[0])
        self.assertEqual(row["name"], ROWS[0]["name"])
        self.assertIsNot(row, ROWS[0])


if __name__ == "__main__":
    unittest.main()
