"""Fast structural tests for the frozen menu and committed receipts."""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import json
import pathlib
import sys
import unittest
from typing import Mapping, cast

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _path in (REPO / "code",):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))
if str(HERE) in sys.path:
    sys.path.remove(str(HERE))
sys.path.insert(0, str(HERE))

from derivation.candidates import NewForm  # noqa: E402
from derivation.engine import READINGS  # noqa: E402
from derivation.export import Json, event_from_json, regime_json  # noqa: E402
from derivation.model import Regime, replay  # noqa: E402

import generation  # noqa: E402
import observables  # noqa: E402
import run_stake  # noqa: E402
from rules import (  # noqa: E402
    APART,
    FREE,
    SAME,
    CONTROLS,
    MENU,
    label_map,
    label_of,
    rule_named,
)

_VERIFY_SPEC = importlib.util.spec_from_file_location(
    "second_stake_verify_pins", HERE / "verify_pins.py"
)
assert _VERIFY_SPEC is not None and _VERIFY_SPEC.loader is not None
verify_pins = importlib.util.module_from_spec(_VERIFY_SPEC)
_VERIFY_SPEC.loader.exec_module(verify_pins)

PROMPT_SHA = "4bd0b507f322c95219bf684a24653696cc976521a5e478e730e5397e4992b12c"
PREDICTIONS_SHA = "efd3893006b4b59e80a10a4a1b067afe0453101987ca51cf6ae54a3cc9b6c07f"


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summary() -> dict[str, object]:
    value: object = json.loads((HERE / "receipts" / "stake.json").read_text("utf-8"))
    assert isinstance(value, dict)
    return cast(dict[str, object], value)


def full_receipt() -> dict[str, object]:
    raw = gzip.decompress((HERE / "receipts" / "full" / "stake_full.json.gz").read_bytes())
    value: object = json.loads(raw)
    assert isinstance(value, dict)
    return cast(dict[str, object], value)


def regime_from_json(value: object) -> Regime:
    assert isinstance(value, dict)
    data = cast(list[str], value["data"])
    forms = cast(list[int], value["forms"])
    inst_rows = cast(list[list[object]], value["insts"])
    rules = cast(list[int], value["rules"])
    reqs = cast(list[list[int]], value["reqs"])
    insts = frozenset(
        (cast(int, row[0]), tuple(cast(list[int], row[1]))) for row in inst_rows
    )
    return Regime(
        tuple(data),
        tuple(forms),
        insts,
        frozenset(rules),
        frozenset((row[0], row[1]) for row in reqs),
    )


class FreezeAndPinTests(unittest.TestCase):
    def test_frozen_hashes_and_prompt_digit_gate(self) -> None:
        self.assertEqual(sha(HERE / "PROMPT.md"), PROMPT_SHA)
        self.assertEqual(sha(HERE / "PREDICTIONS.md"), PREDICTIONS_SHA)
        self.assertFalse(any(byte in b"0123456789" for byte in (HERE / "PROMPT.md").read_bytes()))

    def test_source_and_span_pins(self) -> None:
        lines = verify_pins.verify()
        self.assertTrue(any(line.startswith("snapshot:") for line in lines))
        self.assertTrue(any("challenge_two" in line for line in lines))

    def test_pin_parser_rejects_unsafe_and_malformed_values(self) -> None:
        with self.assertRaises(ValueError):
            verify_pins.safe_path("../escape")
        with self.assertRaises(ValueError):
            verify_pins.entries({}, "x")
        with self.assertRaises(ValueError):
            verify_pins.expected_sha({"sha256": "short"})
        with self.assertRaises(ValueError):
            verify_pins.span_bytes(b"one\n", 2, 2)


class ObservableAndRuleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.collapsed = Regime(("a", "b"), (), frozenset(), frozenset(), frozenset())
        self.split = Regime(
            ("a", "b"),
            (1,),
            frozenset({(0, (0,))}),
            frozenset(),
            frozenset(),
        )

    def test_observable_values_on_collapsed_and_split_pairs(self) -> None:
        self.assertEqual(observables.held_pairs(self.collapsed), ((0, 1),))
        self.assertTrue(observables.profile_equal(self.collapsed, 0, 1))
        self.assertTrue(observables.profile_empty(self.collapsed, 0))
        self.assertEqual(observables.profile_size(self.collapsed, 0), 0)
        self.assertEqual(observables.class_count(self.collapsed), 1)
        self.assertTrue(observables.one_orbit(self.collapsed, 0, 1))
        self.assertFalse(observables.profile_equal(self.split, 0, 1))
        self.assertEqual(sorted((observables.profile_size(self.split, 0), observables.profile_size(self.split, 1))), [0, 1])
        self.assertEqual(observables.class_count(self.split), 2)

    def test_checked_pair_and_observable_guard_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            observables.checked_pair(self.collapsed, 0, 0)
        with self.assertRaises(ValueError):
            observables.profile_empty(self.collapsed, 2)
        guarded = Regime(tuple("abcd"), (1,) * 8, frozenset(), frozenset(), frozenset())
        with self.assertRaises(observables.ObservableGuardError):
            observables.one_orbit(guarded, 0, 1)

    def test_menu_is_frozen_and_total_on_two_examples(self) -> None:
        self.assertEqual([rule.name for rule in MENU], [f"E{n}" for n in range(1, 10)])
        self.assertEqual([rule.capability_count for rule in MENU], [1, 1, 1, 1, 1, 2, 1, 1, 1])
        self.assertEqual(
            [label_of(rule, self.collapsed, 0, 1) for rule in MENU],
            [SAME, SAME, SAME, APART, SAME, SAME, FREE, FREE, SAME],
        )
        self.assertEqual(
            [label_of(rule_named(name), self.split, 0, 1) for name in ("E1", "E2", "E5", "E7", "E9")],
            [APART, APART, APART, APART, APART],
        )
        with self.assertRaises(KeyError):
            rule_named("absent")

    def test_requirement_reader_and_controls(self) -> None:
        required = Regime(("a", "b"), (), frozenset(), frozenset(), frozenset({(0, 1)}))
        self.assertTrue(observables.requirement_member(required, 1, 0))
        self.assertEqual(label_of(rule_named("E8"), required, 0, 1), APART)
        self.assertEqual(
            [(rule.name, rule.index_reading) for rule in CONTROLS],
            [("total_apart", False), ("total_same", False), ("parity", True), ("residue_three", True), ("chain", True)],
        )

    def test_renaming_commutes_for_non_orbit_menu_on_example(self) -> None:
        pi = (1, 0)
        transported = observables.renamed(self.split, pi, (0,))
        for name in ("E1", "E2", "E5", "E7", "E8", "E9"):
            self.assertEqual(label_of(rule_named(name), self.split, 0, 1), label_of(rule_named(name), transported, 0, 1))
        self.assertEqual(len(observables.observable_record(self.collapsed, (0, 1))), 6)


class GenerationUnitTests(unittest.TestCase):
    def test_unknown_measure_and_bad_delta_are_refused(self) -> None:
        regime = replay(READINGS[0].genesis)
        rule = rule_named("E4")
        target = generation.demands(regime, rule)[0]
        with self.assertRaises(ValueError):
            generation.minimum_responses(regime, rule, target, "unknown")
        self.assertFalse(generation.response_valid(regime, rule, target, (NewForm(0),)))

    def test_small_self_honouring_tree_is_a_growth_chain(self) -> None:
        tree = generation.build_tree(READINGS[0], rule_named("E1"), "mu1", max_data=3)
        record = generation.rule_generation_record(rule_named("E1"), [tree])
        self.assertEqual(record["kinds"], [])
        self.assertEqual(record["relabellings"], 0)
        self.assertTrue(all(node.certified for node in tree.nodes))
        self.assertEqual(generation.tree_stats(tree)["guard_nodes"], 0)

    def test_quotient_keeps_control_indices_and_menu_forgets_them(self) -> None:
        regime = replay(READINGS[0].genesis)
        menu_key = generation.quotient_key(regime, rule_named("E1"))
        control_key = generation.quotient_key(regime, rule_named("parity"))
        self.assertNotEqual(menu_key, control_key)
        self.assertEqual(generation.indexed_key(regime)[0], regime.n_data())

    def test_json_adapter_and_rule_registry_fail_by_name(self) -> None:
        with self.assertRaises(TypeError):
            generation._json(object())
        missing = generation.Tree("L", "absent", "mu1")
        with self.assertRaises(ValueError):
            generation.tree_stats(missing)


class ReceiptTests(unittest.TestCase):
    def test_full_receipt_hash_and_replay_certificates(self) -> None:
        small = summary()
        full_path = HERE / "receipts" / "full" / "stake_full.json.gz"
        compressed = full_path.read_bytes()
        self.assertEqual(compressed[:10], b"\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff")
        raw = gzip.decompress(compressed)
        export = cast(dict[str, object], small["full_export"])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), export["uncompressed_sha256"])
        self.assertEqual(len(raw), export["uncompressed_bytes"])
        full = full_receipt()
        trees = cast(list[dict[str, object]], full["trees"])
        self.assertEqual(len(trees), len(MENU + CONTROLS) * len(READINGS) * 2)
        for tree in trees:
            nodes = cast(list[dict[str, object]], tree["nodes"])
            edges = cast(list[dict[str, object]], tree["edges"])
            self.assertTrue(all(node["certified"] is True for node in nodes))
            self.assertTrue(all(cast(int, edge["parent"]) < len(nodes) and cast(int, edge["child"]) < len(nodes) for edge in edges))
            for node in nodes:
                history = tuple(
                    event_from_json(cast(Mapping[str, Json], event))
                    for event in cast(list[object], node["history"])
                )
                self.assertEqual(regime_json(replay(history)), node["regime"])

    def test_summary_records_exact_finite_terminal(self) -> None:
        data = summary()
        self.assertEqual(data["reached_regimes"], 845)
        self.assertEqual(
            cast(dict[str, object], data["predictions_scored"]),
            {"hit": 8, "missed": 8, "pending": 1, "vacuous": 0},
        )
        terminals = cast(list[str], data["terminals"])
        self.assertIn("NO_ENDOGENOUS_STAKE_IN_MENU", terminals)
        self.assertIn("OB1_UNCHANGED", terminals)
        self.assertEqual(data["both_kind_members"], [])
        self.assertEqual(data["input_count"], {
            "value": 2,
            "proof": None,
            "sentence": "A rule class is a declaration; no menu member is forced and no unique survivor is proved.",
        })

    def test_sibling_control_baseline_is_pinned_and_scope_separated(self) -> None:
        data = summary()
        baseline = cast(dict[str, object], data["sibling_control_baseline"])
        self.assertEqual(
            baseline["receipt_sha256"],
            "863d3503425647fb2bbaafa8583736e6284d3fdda0a512c9ed039ededf0ae4d3",
        )
        bounds = cast(dict[str, object], baseline["bounds"])
        self.assertEqual(bounds["max_data"], 5)
        self.assertIn("data bound four", cast(str, baseline["comparison"]))

    def test_control_refutations_name_replayable_witnesses(self) -> None:
        data = summary()
        rows = cast(list[dict[str, object]], data["invariance"])
        by_name = {cast(str, row["rule"]): row for row in rows}
        for name in ("parity", "residue_three", "chain"):
            row = by_name[name]
            regime = regime_from_json(row["source_regime"])
            pair = tuple(cast(list[int], row["pair"]))
            pi = tuple(cast(list[int], row["datum_renaming"]))
            phi = tuple(cast(list[int], row["form_renaming"]))
            mapped = tuple(sorted((pi[pair[0]], pi[pair[1]])))
            after = observables.renamed(regime, pi, phi)
            self.assertNotEqual(
                label_of(rule_named(name), regime, *pair),
                label_of(rule_named(name), after, *mapped),
            )
        self.assertEqual(by_name["total_apart"]["disposition"], "CHECKED")
        self.assertEqual(by_name["total_same"]["disposition"], "CHECKED")

    def test_generation_register_keeps_ties_and_guarded_members(self) -> None:
        data = summary()
        generation_rows = cast(list[dict[str, object]], data["generation"])
        by_name = {cast(str, row["rule"]): row for row in generation_rows}
        self.assertEqual(by_name["E4"]["kinds"], ["apart", "same"])
        self.assertEqual(by_name["E4"]["relabellings"], 537)
        self.assertEqual(by_name["E4"]["refusals"], 105)
        self.assertEqual(by_name["E4"]["fixpoints"], 123)
        self.assertEqual(by_name["E4"]["guard_nodes"], 89)
        ties = cast(dict[str, list[str]], data["tree_ties"])
        self.assertEqual(len(ties["E1"]), 7)
        self.assertEqual(ties["E4"], [])
        self.assertEqual(data["retained_menu"], [f"E{n}" for n in range(1, 10)])

    def test_deterministic_gzip_and_helper_errors(self) -> None:
        raw = b"stake\n" * 10
        first = run_stake.deterministic_gzip(raw)
        self.assertEqual(first, run_stake.deterministic_gzip(raw))
        self.assertEqual(gzip.decompress(first), raw)
        with self.assertRaises(TypeError):
            run_stake._as_str_list("not a list")
        with self.assertRaises(TypeError):
            run_stake._as_int("not an integer")


if __name__ == "__main__":
    unittest.main()
