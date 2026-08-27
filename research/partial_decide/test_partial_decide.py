"""Tests for the partial metatheoretic decision grade and its provenance."""

from __future__ import annotations

import copy
import json
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from types import ModuleType, SimpleNamespace
from typing import cast
from unittest.mock import patch

from derivation.candidates import Bounds
from derivation.engine import READING_F, READING_L, Reading, challenge3_report
from derivation.iso import IsoBudgetError
from derivation.model import (
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    replay,
)

from c3_receipt import BOUNDS, MEASURES, receipt_bytes, receipt_payload
from partial_decide import (
    DecisionInputError,
    Grade,
    Measure,
    Tie,
    UniqueClass,
    UniqueDelta,
    decide,
    grade_kind,
    grade_payload,
)
from run_receipt import main as run_receipt_main
from verify_pins import (
    FINITE_G4_WITHDRAWAL,
    FRESH_RENDERER_FLAGS,
    RECEIPT_PATH,
    REQUIRED_TERMINALS,
    _assert_module_origin,
    _controlled_imports,
    _fresh_receipt,
    _format_package_census_difference,
    _internal_dependencies,
    _parse_tree_records,
    _read_pins,
    _require_hex,
    _require_regular_receipt_target,
    _safe_relative,
    _validate_g3_g4_status_payload,
    _validate_pin_structure,
    _validate_receipt_contract,
    verify,
)

SNAPSHOT_COMMIT = "24d1bc64bace9721472430347ca9d3af303e1347"
SNAPSHOT_TREE = "2e80261ef11b9bcd2fc3a87597892aafec83dbf6"
PINNED_MODULE_PATHS = {
    "derivation": PurePosixPath("code/derivation/__init__.py"),
    "derivation.model": PurePosixPath("code/derivation/model.py"),
    "derivation.observe": PurePosixPath("code/derivation/observe.py"),
    "derivation.candidates": PurePosixPath("code/derivation/candidates.py"),
    "derivation.iso": PurePosixPath("code/derivation/iso.py"),
    "derivation.engine": PurePosixPath("code/derivation/engine.py"),
}


def _literal_contract_payload() -> dict[str, object]:
    """Adapt only the terminals until the semantic integration commit lands."""

    serialized: object = json.loads(json.dumps(receipt_payload()))
    if not isinstance(serialized, dict):
        raise AssertionError("serialized receipt payload must be an object")
    payload = cast(dict[str, object], serialized)
    payload["terminals"] = list(REQUIRED_TERMINALS)
    return payload


def _receipt_grade_at(
    payload: dict[str, object], reading_index: int, measure: str
) -> dict[str, object]:
    readings = cast(list[dict[str, object]], payload["readings"])
    grades = cast(dict[str, object], readings[reading_index]["grades"])
    option = cast(dict[str, object], grades[measure])
    return cast(dict[str, object], option["grade"])


def _g1_status_payload() -> dict[str, object]:
    path = RECEIPT_PATH.parents[2] / "artifacts" / "g1_class_receipt.json"
    payload: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise AssertionError("G1 status receipt must be an object")
    return cast(dict[str, object], payload)


def _c3_grade(
    reading: Reading, measure: Measure, *, perm_budget: int = 100_000
) -> Grade | None:
    regime = replay(reading.genesis)
    return decide(
        regime,
        reading.target[0],
        reading.target[1],
        measure,
        BOUNDS,
        perm_budget=perm_budget,
    )


def _fresh_receipt_with_c3_injection(injection: str) -> None:
    source_here = RECEIPT_PATH.parent
    with tempfile.TemporaryDirectory(prefix="partial-decide-injection-") as raw:
        probe_here = Path(raw)
        for name in ("c3_receipt.py", "partial_decide.py", "SOURCE_PINS.json"):
            shutil.copyfile(source_here / name, probe_here / name)
        c3_path = probe_here / "c3_receipt.py"
        source = c3_path.read_text(encoding="utf-8")
        marker = "def receipt_bytes() -> bytes:\n    return ("
        replacement = "def receipt_bytes() -> bytes:\n" + injection + "\n    return ("
        if marker not in source:
            raise AssertionError("receipt_bytes injection marker moved")
        c3_path.write_text(source.replace(marker, replacement), encoding="utf-8")
        with patch("verify_pins.HERE", probe_here):
            _fresh_receipt(
                PINNED_MODULE_PATHS,
                snapshot_commit=SNAPSHOT_COMMIT,
                snapshot_tree=SNAPSHOT_TREE,
            )


class DecisionGradeTests(unittest.TestCase):
    def test_c3_mu1_retains_all_tied_classes(self) -> None:
        cases = ((READING_L, 6, 3), (READING_F, 10, 5))
        for reading, raw_count, class_count in cases:
            with self.subTest(reading=reading.name):
                grade = _c3_grade(reading, "mu1")
                self.assertIsInstance(grade, Tie)
                assert isinstance(grade, Tie)
                self.assertEqual(len(grade.quotient.minimum.raw_minima), raw_count)
                self.assertEqual(len(grade.quotient.classes), class_count)
                self.assertEqual(
                    sum(len(item.members) for item in grade.quotient.classes),
                    raw_count,
                )
                self.assertTrue(
                    all(len(item.members) == 2 for item in grade.quotient.classes)
                )

    def test_c3_mu2_is_unique_class_not_unique_delta(self) -> None:
        for reading in (READING_L, READING_F):
            with self.subTest(reading=reading.name):
                grade = _c3_grade(reading, "mu2")
                self.assertIsInstance(grade, UniqueClass)
                assert isinstance(grade, UniqueClass)
                self.assertEqual(len(grade.quotient.classes), 1)
                self.assertEqual(len(grade.quotient.minimum.raw_minima), 2)
                self.assertEqual(len(grade.quotient.classes[0].members), 2)

    def test_c3_unique_delta_grade_is_empty(self) -> None:
        grades = [
            _c3_grade(reading, measure)
            for reading in (READING_L, READING_F)
            for measure in MEASURES
        ]
        self.assertFalse(any(isinstance(grade, UniqueDelta) for grade in grades))

    def test_grade_counts_match_official_challenge3_report(self) -> None:
        for reading in (READING_L, READING_F):
            report = challenge3_report(reading, BOUNDS)
            for measure in MEASURES:
                with self.subTest(reading=reading.name, measure=measure):
                    official = report[measure]
                    self.assertIsInstance(official, dict)
                    assert isinstance(official, dict)
                    grade = _c3_grade(reading, measure)
                    self.assertIsNotNone(grade)
                    assert grade is not None
                    minimum = (
                        grade.minimum
                        if isinstance(grade, UniqueDelta)
                        else grade.quotient.minimum
                    )
                    class_count = (
                        1
                        if isinstance(grade, UniqueDelta)
                        else len(grade.quotient.classes)
                    )
                    official_classes = official["iso_classes"]
                    self.assertIsInstance(official_classes, list)
                    assert isinstance(official_classes, list)
                    self.assertEqual(
                        len(minimum.raw_minima),
                        official["valid_deltas_at_minimum"],
                    )
                    self.assertEqual(class_count, len(official_classes))

    def test_none_means_no_response_inside_supplied_bounds(self) -> None:
        reading = READING_L
        regime = replay(reading.genesis)
        grade = decide(
            regime,
            reading.target[0],
            reading.target[1],
            "mu1",
            Bounds(max_items=1, max_arity=2),
        )
        self.assertIsNone(grade)
        self.assertEqual(
            grade_payload(grade),
            {
                "kind": "none",
                "meaning": "no valid response inside the declared finite bounds",
            },
        )

    def test_unique_delta_exists_away_from_c3_and_can_be_empty(self) -> None:
        regime = replay(
            (
                AdmitDatum("a"),
                AdmitDatum("b"),
                AdmitForm(1),
                AdmitInst(0, (0,)),
            )
        )
        grade = decide(regime, 0, 1, "mu1", Bounds())
        self.assertIsInstance(grade, UniqueDelta)
        assert isinstance(grade, UniqueDelta)
        self.assertEqual(grade.delta, ())
        self.assertNotIn("classes", grade_payload(grade))

    def test_call_is_deterministic_and_does_not_mutate_base(self) -> None:
        base = replay(READING_F.genesis)
        before = base
        first = decide(base, 1, 2, "mu1", BOUNDS)
        second = decide(base, 1, 2, "mu1", BOUNDS)
        self.assertEqual(first, second)
        self.assertEqual(base, before)

    def test_serialization_names_no_representative(self) -> None:
        grade = _c3_grade(READING_L, "mu1")
        payload = grade_payload(grade)
        self.assertNotIn("representative", repr(payload))
        self.assertEqual(payload["kind"], "tie")

    def test_invalid_requests_are_errors_not_none(self) -> None:
        regime = replay(READING_L.genesis)
        invalid_measure = cast(Measure, "mu3")
        with self.assertRaises(DecisionInputError):
            decide(regime, 0, 1, invalid_measure, BOUNDS)
        with self.assertRaises(DecisionInputError):
            decide(regime, 1, 0, "mu1", BOUNDS)
        with self.assertRaises(DecisionInputError):
            decide(regime, 0, 2, "mu1", BOUNDS)
        with self.assertRaises(DecisionInputError):
            decide(regime, 0, 1, "mu1", Bounds(max_items=3))
        with self.assertRaises(DecisionInputError):
            decide(regime, 0, 1, "mu1", Bounds(max_arity=-1))
        with self.assertRaises(DecisionInputError):
            decide(regime, 0, 1, "mu1", BOUNDS, perm_budget=0)
        with self.assertRaises(DecisionInputError):
            decide(regime, True, 1, "mu1", BOUNDS)
        with self.assertRaises(DecisionInputError):
            decide(regime, 0, False, "mu1", BOUNDS)

    def test_rule_bearing_base_is_outside_declared_domain(self) -> None:
        regime = replay(
            (
                AdmitDatum("a"),
                AdmitDatum("b"),
                AdmitForm(1),
                AdmitRuleAll(0),
            )
        )
        with self.assertRaises(DecisionInputError):
            decide(regime, 0, 1, "mu1", BOUNDS)

    def test_isomorphism_budget_exhaustion_is_not_none(self) -> None:
        regime = replay(
            (
                AdmitDatum("a"),
                AdmitDatum("b"),
                AdmitDatum("c"),
                AdmitDatum("d"),
            )
        )
        with self.assertRaises(IsoBudgetError):
            decide(regime, 0, 1, "mu2", BOUNDS, perm_budget=1)

    def test_raw_delta_payload_is_literal_not_authorizing(self) -> None:
        regime = replay(
            (
                AdmitDatum("a"),
                AdmitDatum("b"),
                AdmitForm(1),
                AdmitInst(0, (0,)),
            )
        )
        grade = decide(regime, 0, 1, "mu1", Bounds())
        self.assertEqual(grade_kind(grade), "unique_delta")
        payload = grade_payload(grade)
        self.assertEqual(payload["delta"], [])
        self.assertNotIn("apply", payload)


class ReceiptAndPinTests(unittest.TestCase):
    def test_committed_receipt_is_byte_identical(self) -> None:
        self.assertEqual(RECEIPT_PATH.read_bytes(), receipt_bytes())

    def test_receipt_carries_required_terminals(self) -> None:
        payload = receipt_payload()
        terminals = payload["terminals"]
        self.assertIsInstance(terminals, list)
        assert isinstance(terminals, list)
        self.assertEqual(
            terminals,
            list(REQUIRED_TERMINALS),
        )
        self.assertEqual(payload["authority_effect"], "None")

    def test_literal_receipt_contract_rejects_renderer_constant_drift(self) -> None:
        payload = _literal_contract_payload()
        _validate_receipt_contract(
            payload,
            snapshot_commit=SNAPSHOT_COMMIT,
            snapshot_tree=SNAPSHOT_TREE,
        )
        with patch("c3_receipt.MEASURES", ("mu1", "mu1")):
            drifted = _literal_contract_payload()
        with self.assertRaisesRegex(ValueError, "grades"):
            _validate_receipt_contract(
                drifted,
                snapshot_commit=SNAPSHOT_COMMIT,
                snapshot_tree=SNAPSHOT_TREE,
            )
        _validate_receipt_contract(
            _literal_contract_payload(),
            snapshot_commit=SNAPSHOT_COMMIT,
            snapshot_tree=SNAPSHOT_TREE,
        )

    def test_literal_receipt_contract_rejects_snapshot_bounds_and_counts(self) -> None:
        mutations: list[tuple[str, dict[str, object], str]] = []
        wrong_snapshot = copy.deepcopy(_literal_contract_payload())
        wrong_snapshot["source_snapshot"] = {
            "commit": "0" * 40,
            "tree": SNAPSHOT_TREE,
        }
        mutations.append(("snapshot", wrong_snapshot, "source_snapshot"))

        wrong_bounds = copy.deepcopy(_literal_contract_payload())
        readings = cast(list[dict[str, object]], wrong_bounds["readings"])
        grades = cast(dict[str, object], readings[0]["grades"])
        option = cast(dict[str, object], grades["mu1"])
        grade = cast(dict[str, object], option["grade"])
        grade["bounds"] = {"max_arity": 2, "max_items": 1}
        mutations.append(("bounds", wrong_bounds, "bounds"))

        wrong_count = copy.deepcopy(_literal_contract_payload())
        readings = cast(list[dict[str, object]], wrong_count["readings"])
        grades = cast(dict[str, object], readings[1]["grades"])
        option = cast(dict[str, object], grades["mu2"])
        grade = cast(dict[str, object], option["grade"])
        grade["raw_minimum_count"] = 3
        mutations.append(("count", wrong_count, "raw-minimum count"))

        for name, mutated, message in mutations:
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError, message):
                    _validate_receipt_contract(
                        mutated,
                        snapshot_commit=SNAPSHOT_COMMIT,
                        snapshot_tree=SNAPSHOT_TREE,
                    )

    def test_literal_receipt_contract_rejects_bool_integer_substitutions(self) -> None:
        bool_target = copy.deepcopy(_literal_contract_payload())
        readings = cast(list[dict[str, object]], bool_target["readings"])
        readings[0]["target"] = [False, True]
        for measure in ("mu1", "mu2"):
            _receipt_grade_at(bool_target, 0, measure)["target"] = [False, True]

        bool_count = copy.deepcopy(_literal_contract_payload())
        _receipt_grade_at(bool_count, 0, "mu2")["iso_class_count"] = True

        bool_cost = copy.deepcopy(_literal_contract_payload())
        minimum_cost = cast(
            dict[str, object],
            _receipt_grade_at(bool_cost, 0, "mu2")["minimum_cost"],
        )
        minimum_cost["new_form_arity_sum"] = True

        mutations = (
            ("target", bool_target, "target"),
            ("class_count", bool_count, "class count"),
            ("minimum_cost", bool_cost, "minimum cost"),
        )
        for name, mutated, message in mutations:
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError, message):
                    _validate_receipt_contract(
                        mutated,
                        snapshot_commit=SNAPSHOT_COMMIT,
                        snapshot_tree=SNAPSHOT_TREE,
                    )

    def test_literal_receipt_contract_rejects_null_and_duplicate_minima(self) -> None:
        null_minima = copy.deepcopy(_literal_contract_payload())
        grade = _receipt_grade_at(null_minima, 0, "mu1")
        grade["raw_minima"] = [None] * 6
        classes = cast(list[dict[str, object]], grade["classes"])
        for response_class in classes:
            response_class["members"] = [None] * cast(int, response_class["size"])
        with self.assertRaisesRegex(ValueError, "delta must be a list"):
            _validate_receipt_contract(
                null_minima,
                snapshot_commit=SNAPSHOT_COMMIT,
                snapshot_tree=SNAPSHOT_TREE,
            )

        duplicate_minima = copy.deepcopy(_literal_contract_payload())
        grade = _receipt_grade_at(duplicate_minima, 0, "mu1")
        raw_minima = cast(list[object], grade["raw_minima"])
        first = copy.deepcopy(raw_minima[0])
        grade["raw_minima"] = [copy.deepcopy(first) for _ in raw_minima]
        classes = cast(list[dict[str, object]], grade["classes"])
        for response_class in classes:
            response_class["members"] = [
                copy.deepcopy(first) for _ in range(cast(int, response_class["size"]))
            ]
        with self.assertRaisesRegex(ValueError, "raw minima are not unique"):
            _validate_receipt_contract(
                duplicate_minima,
                snapshot_commit=SNAPSHOT_COMMIT,
                snapshot_tree=SNAPSHOT_TREE,
            )

    def test_literal_receipt_contract_closes_delta_and_canonical_key_shapes(self) -> None:
        selected_delta = copy.deepcopy(_literal_contract_payload())
        raw_minima = cast(
            list[list[dict[str, object]]],
            _receipt_grade_at(selected_delta, 0, "mu1")["raw_minima"],
        )
        raw_minima[0][0]["selected_delta"] = "INJECTION"
        with self.assertRaisesRegex(ValueError, "keys differ"):
            _validate_receipt_contract(
                selected_delta,
                snapshot_commit=SNAPSHOT_COMMIT,
                snapshot_tree=SNAPSHOT_TREE,
            )

        adapter_key = copy.deepcopy(_literal_contract_payload())
        classes = cast(
            list[dict[str, object]],
            _receipt_grade_at(adapter_key, 0, "mu1")["classes"],
        )
        classes[0]["canonical_key"] = ["panel_adapter", [], [], [], []]
        with self.assertRaisesRegex(ValueError, "nonnegative integer"):
            _validate_receipt_contract(
                adapter_key,
                snapshot_commit=SNAPSHOT_COMMIT,
                snapshot_tree=SNAPSHOT_TREE,
            )

    def test_source_pin_schema_rejects_extra_root_and_nested_keys(self) -> None:
        base = _read_pins()
        _validate_pin_structure(base)
        mutations: list[tuple[str, dict[str, object], str]] = []

        extra_root = copy.deepcopy(base)
        extra_root["response_authorization"] = {"selected_delta": 0}
        mutations.append(("root", extra_root, "SOURCE_PINS keys differ"))

        extra_snapshot = copy.deepcopy(base)
        cast(dict[str, object], extra_snapshot["source_snapshot"])["symbolic"] = "HEAD"
        mutations.append(("snapshot", extra_snapshot, "source_snapshot keys differ"))

        extra_package = copy.deepcopy(base)
        cast(dict[str, object], extra_package["source_package"])["adapter"] = True
        mutations.append(("source_package", extra_package, "source_package keys differ"))

        extra_module = copy.deepcopy(base)
        cast(list[dict[str, object]], extra_module["modules"])[0]["authority"] = "yes"
        mutations.append(("module", extra_module, "modules\\[0\\] keys differ"))

        extra_status = copy.deepcopy(base)
        cast(list[dict[str, object]], extra_status["status_inputs"])[0][
            "totalized"
        ] = True
        mutations.append(("status", extra_status, "status_inputs\\[0\\] keys differ"))

        extra_import = copy.deepcopy(base)
        authorized = cast(
            dict[str, dict[str, object]], extra_import["authorized_imports"]
        )
        authorized["research/partial_decide/partial_decide.py"][
            "response_authorization"
        ] = ["selected_delta"]
        mutations.append(("import", extra_import, "invalid authorized module"))

        extra_consumer = copy.deepcopy(base)
        authorized = cast(
            dict[str, dict[str, object]], extra_consumer["authorized_imports"]
        )
        authorized["research/partial_decide/zzz_adapter.py"] = {}
        mutations.append(("consumer", extra_consumer, "consumer keys differ"))

        for name, mutated, message in mutations:
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError, message):
                    _validate_pin_structure(mutated)

    def test_g3_g4_status_contract_rejects_drift_and_competing_terminals(self) -> None:
        base = _g1_status_payload()
        _validate_g3_g4_status_payload(base)

        status_drift = copy.deepcopy(base)
        cast(dict[str, object], status_drift["statuses"])["g4"] = "G4_HOLDS"

        competing = copy.deepcopy(base)
        cast(list[str], competing["terminals"]).append("G4_HOLDS_UNDER_MU2")

        lost_withdrawal = copy.deepcopy(base)
        cast(list[str], lost_withdrawal["withdrawn_sentences"]).remove(
            FINITE_G4_WITHDRAWAL
        )

        mutations = (
            ("status", status_drift, "statuses.g3/g4"),
            ("competing", competing, "competing G3/G4 terminals"),
            ("withdrawal", lost_withdrawal, "finite-G4 withdrawal"),
        )
        for name, mutated, message in mutations:
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError, message):
                    _validate_g3_g4_status_payload(mutated)

    def test_panel_metadata_cannot_replace_engine_grade(self) -> None:
        payload = receipt_payload()
        panel = payload["panel_input"]
        self.assertIsInstance(panel, dict)
        assert isinstance(panel, dict)
        self.assertEqual(
            panel["status"], "not_connected_without_a_declared_correspondence"
        )

    def test_pin_verifier_passes_current_exact_sources(self) -> None:
        lines = verify()
        self.assertTrue(any(line.startswith("source snapshot:") for line in lines))
        self.assertTrue(any(line.startswith("receipt:") for line in lines))

    def test_pin_paths_reject_escape_and_absolute_inputs(self) -> None:
        with self.assertRaises(ValueError):
            _safe_relative("../code/derivation/model.py")
        with self.assertRaises(ValueError):
            _safe_relative("code\\derivation\\model.py")
        absolute = str(Path.cwd().anchor + "outside.py")
        with self.assertRaises(ValueError):
            _safe_relative(absolute)

    def test_exact_git_and_digest_ids_reject_symbolic_wrong_case_and_width(self) -> None:
        _require_hex("a" * 40, 40, "commit", uppercase=False)
        _require_hex("A" * 64, 64, "digest", uppercase=True)
        bad = (
            ("HEAD", 40, False),
            ("a" * 39, 40, False),
            ("A" * 40, 40, False),
            ("A" * 63, 64, True),
            ("a" * 64, 64, True),
            ("G" * 64, 64, True),
        )
        for value, width, uppercase in bad:
            with self.subTest(value=value[:8], width=width, uppercase=uppercase):
                with self.assertRaises(ValueError):
                    _require_hex(value, width, "probe", uppercase=uppercase)

    def test_dependency_scan_discovers_package_root_and_relative_submodules(self) -> None:
        source = "from derivation import represented\nfrom . import observe\n"
        module_map = {
            "derivation": PurePosixPath("code/derivation/__init__.py"),
            "derivation.candidates": PurePosixPath("code/derivation/candidates.py"),
            "derivation.observe": PurePosixPath("code/derivation/observe.py"),
            "derivation.represented": PurePosixPath("code/derivation/represented.py"),
        }
        with patch("verify_pins._source_text", return_value=source):
            actual = _internal_dependencies(
                "derivation.candidates",
                PurePosixPath("code/derivation/candidates.py"),
                module_map,
            )
        self.assertEqual(
            actual,
            {"derivation", "derivation.observe", "derivation.represented"},
        )

    def test_dependency_scan_handles_nested_packages_and_rejects_wildcards(self) -> None:
        module_map = {
            "derivation": PurePosixPath("code/derivation/__init__.py"),
            "derivation.pkg": PurePosixPath("code/derivation/pkg/__init__.py"),
            "derivation.pkg.child": PurePosixPath("code/derivation/pkg/child.py"),
            "derivation.consumer": PurePosixPath("code/derivation/consumer.py"),
        }
        with patch(
            "verify_pins._source_text",
            return_value="from derivation.pkg import child\n",
        ):
            actual = _internal_dependencies(
                "derivation.consumer",
                module_map["derivation.consumer"],
                module_map,
            )
        self.assertEqual(
            actual,
            {"derivation", "derivation.pkg", "derivation.pkg.child"},
        )
        with patch(
            "verify_pins._source_text",
            return_value="from derivation.pkg import *\n",
        ):
            with self.assertRaisesRegex(ValueError, "wildcard"):
                _internal_dependencies(
                    "derivation.consumer",
                    module_map["derivation.consumer"],
                    module_map,
                )

    def test_tree_parser_rejects_symlinks_and_gitlinks(self) -> None:
        object_id = b"a" * 40
        regular = b"100644 blob " + object_id + b"\tcode/derivation/model.py\0"
        self.assertEqual(
            set(_parse_tree_records(regular, "probe")),
            {PurePosixPath("code/derivation/model.py")},
        )
        for mode, object_type in ((b"120000", b"blob"), (b"160000", b"commit")):
            with self.subTest(mode=mode.decode("ascii")):
                raw = mode + b" " + object_type + b" " + object_id
                raw += b"\tcode/derivation/probe.py\0"
                with self.assertRaisesRegex(ValueError, "non-regular"):
                    _parse_tree_records(raw, "probe")

    def test_package_census_difference_names_each_disputed_path(self) -> None:
        declared = {PurePosixPath("research/partial_decide/declared.py")}
        head = {
            PurePosixPath("research/partial_decide/declared.py"),
            PurePosixPath("research/partial_decide/zzz_consumer_probe.py"),
        }
        tracked = set(head)
        self.assertEqual(
            _format_package_census_difference(declared, head, tracked),
            "research/partial_decide/zzz_consumer_probe.py "
            "[declaration=no, HEAD=yes, index=yes]",
        )

    def test_consumer_scan_rejects_dynamic_loaders_and_external_helpers(self) -> None:
        cases = (
            "import importlib.util\n",
            "import runpy as loader\n",
            "from builtins import __import__ as loader\n",
            "value = __import__('outside_helper')\n",
            "import outside_helper\n",
        )
        relative = PurePosixPath("research/partial_decide/probe.py")
        for source in cases:
            with self.subTest(source=source.strip()):
                with patch("verify_pins._source_text", return_value=source):
                    with self.assertRaises(ValueError):
                        _controlled_imports(
                            relative,
                            {"partial_decide"},
                            enforce_dynamic_policy=True,
                        )

    def test_fresh_renderer_audits_imports_during_receipt_bytes(self) -> None:
        injection = (
            "    import builtins\n"
            "    getattr(builtins, \"__import__\")(\"derivation.represented\")"
        )
        with self.assertRaisesRegex(ValueError, "unauthorized import derivation.represented"):
            _fresh_receipt_with_c3_injection(injection)
        rendered, _ = _fresh_receipt(
            PINNED_MODULE_PATHS,
            snapshot_commit=SNAPSHOT_COMMIT,
            snapshot_tree=SNAPSHOT_TREE,
        )
        self.assertEqual(rendered, receipt_bytes())

    def test_fresh_renderer_rechecks_loaded_modules_after_receipt_bytes(self) -> None:
        injection = (
            "    import sys\n"
            "    import types\n"
            "    probe = types.ModuleType(\"derivation.runtime_probe\")\n"
            "    sys.modules[\"derivation.runtime_probe\"] = probe"
        )
        with self.assertRaisesRegex(ValueError, "after receipt_bytes derivation modules"):
            _fresh_receipt_with_c3_injection(injection)
        rendered, _ = _fresh_receipt(
            PINNED_MODULE_PATHS,
            snapshot_commit=SNAPSHOT_COMMIT,
            snapshot_tree=SNAPSHOT_TREE,
        )
        self.assertEqual(rendered, receipt_bytes())

    def test_fresh_renderer_flags_exclude_site_and_ambient_packages(self) -> None:
        self.assertEqual(FRESH_RENDERER_FLAGS, ("-I", "-B", "-S"))
        result = subprocess.run(
            [
                sys.executable,
                *FRESH_RENDERER_FLAGS,
                "-c",
                (
                    "import sys; "
                    "print('site' in sys.modules); "
                    "print(any('site-packages' in item.replace('\\\\', '/').lower() "
                    "for item in sys.path))"
                ),
            ],
            capture_output=True,
            check=False,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ["False", "False"])

    def test_receipt_target_requires_regular_non_reparse_file(self) -> None:
        probe = Path("receipt-probe.json")
        regular = SimpleNamespace(st_mode=stat.S_IFREG, st_file_attributes=0)
        with patch.object(Path, "lstat", return_value=regular):
            _require_regular_receipt_target(probe)

        missing = FileNotFoundError("INJECTION missing receipt")
        with patch.object(Path, "lstat", side_effect=missing):
            with self.assertRaisesRegex(ValueError, "existing regular file"):
                _require_regular_receipt_target(probe)

        symlink = SimpleNamespace(st_mode=stat.S_IFLNK, st_file_attributes=0)
        with patch.object(Path, "lstat", return_value=symlink):
            with self.assertRaisesRegex(ValueError, "regular non-symlink"):
                _require_regular_receipt_target(probe)

        reparse = SimpleNamespace(st_mode=stat.S_IFREG, st_file_attributes=0x400)
        with patch.object(Path, "lstat", return_value=reparse):
            with self.assertRaisesRegex(ValueError, "non-reparse"):
                _require_regular_receipt_target(probe)

    def test_custody_preflight_precedes_source_parsing(self) -> None:
        with patch(
            "verify_pins._bootstrap_custody",
            side_effect=ValueError("INJECTION dirty executable probe"),
        ), patch("verify_pins._source_text") as source_text:
            with self.assertRaisesRegex(ValueError, "dirty executable probe"):
                verify()
            source_text.assert_not_called()

    def test_writer_refuses_unverified_render_then_recovers(self) -> None:
        with tempfile.TemporaryDirectory(prefix="partial-decide-writer-") as raw:
            output = Path(raw) / "receipt.json"
            with patch.object(sys, "argv", ["run_receipt.py", "--write"]), patch(
                "run_receipt.RECEIPT_PATH", output
            ), patch(
                "run_receipt.render_verified_receipt",
                side_effect=ValueError("INJECTION dirty source probe"),
            ):
                self.assertEqual(run_receipt_main(), 1)
            self.assertFalse(output.exists())

            expected = b"verified receipt probe\n"
            with patch.object(sys, "argv", ["run_receipt.py", "--write"]), patch(
                "run_receipt.RECEIPT_PATH", output
            ), patch("run_receipt.render_verified_receipt", return_value=expected):
                self.assertEqual(run_receipt_main(), 0)
            self.assertEqual(output.read_bytes(), expected)

    def test_runtime_origin_checks_file_spec_and_package_path(self) -> None:
        expected = Path.cwd() / "probe.py"
        module = ModuleType("probe")
        module.__file__ = str(expected)
        setattr(module, "__spec__", SimpleNamespace(origin=str(expected)))
        _assert_module_origin(module, expected, "probe")

        module.__file__ = str(expected.with_name("wrong.py"))
        with self.assertRaises(ValueError):
            _assert_module_origin(module, expected, "probe")
        module.__file__ = str(expected)
        setattr(
            module,
            "__spec__",
            SimpleNamespace(origin=str(expected.with_name("wrong.py"))),
        )
        with self.assertRaises(ValueError):
            _assert_module_origin(module, expected, "probe")

        package_init = expected.parent / "derivation" / "__init__.py"
        package = ModuleType("derivation")
        package.__file__ = str(package_init)
        setattr(package, "__spec__", SimpleNamespace(origin=str(package_init)))
        setattr(package, "__path__", [str(expected.parent / "shadow")])
        with self.assertRaises(ValueError):
            _assert_module_origin(package, package_init, "derivation")


if __name__ == "__main__":
    unittest.main()
