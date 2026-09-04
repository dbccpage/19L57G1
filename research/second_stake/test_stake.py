"""Fast structural tests for the frozen menu and committed receipts."""

from __future__ import annotations

import contextlib
import gzip
import hashlib
import io
import json
import pathlib
import sys
import tempfile
import unittest
from typing import Mapping, cast
from unittest import mock

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

import verify_pins  # noqa: E402
import generation  # noqa: E402
import observables  # noqa: E402
import run_stake  # noqa: E402
from rules import (  # noqa: E402
    APART,
    FREE,
    SAME,
    CONTROLS,
    MENU,
    StakeRule,
    label_map,
    label_of,
    rule_named,
)

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
    @staticmethod
    def bare_manifest(**updates: object) -> dict[str, object]:
        value: dict[str, object] = {
            "snapshot_commit": "a" * 40,
            "sources": [],
            "spans": [],
            "frozen_texts": [],
            "absent_at_snapshot": [],
        }
        value.update(updates)
        return value

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
            verify_pins.safe_path(None)
        with self.assertRaises(ValueError):
            verify_pins.safe_path("../escape")
        with self.assertRaises(ValueError):
            verify_pins.entries({}, "x")
        with self.assertRaises(ValueError):
            verify_pins.entries([{}, "not-an-object"], "x")
        with self.assertRaises(ValueError):
            verify_pins.expected_sha({"sha256": "short"})
        with self.assertRaises(ValueError):
            verify_pins.span_bytes(b"one\n", 2, 2)

    def test_pin_io_and_manifest_fail_closed(self) -> None:
        failed = mock.Mock(returncode=1, stderr=b"named git failure", stdout=b"")
        with mock.patch.object(verify_pins.subprocess, "run", return_value=failed):
            with self.assertRaisesRegex(ValueError, "named git failure"):
                verify_pins.git_bytes("show", "missing:path")

        with tempfile.TemporaryDirectory() as raw_directory:
            path = pathlib.Path(raw_directory) / "manifest.json"
            path.write_text("[]", encoding="utf-8")
            with mock.patch.object(verify_pins, "MANIFEST", path):
                with self.assertRaisesRegex(ValueError, "must be an object"):
                    verify_pins.manifest()

    def test_snapshot_relation_and_source_blob_failures_are_named(self) -> None:
        success = mock.Mock(returncode=0, stderr=b"", stdout=b"")
        failure = mock.Mock(returncode=7, stderr=b"", stdout=b"")
        with mock.patch.object(
            verify_pins, "manifest", return_value=self.bare_manifest(snapshot_commit="short")
        ):
            with self.assertRaisesRegex(ValueError, "full commit id"):
                verify_pins.verify()
        with (
            mock.patch.object(verify_pins, "manifest", return_value=self.bare_manifest()),
            mock.patch.object(verify_pins.subprocess, "run", return_value=failure),
        ):
            with self.assertRaisesRegex(ValueError, "git exit 7"):
                verify_pins.verify()

        good = b"pinned source\n"
        entry = {"path": "source.txt", "sha256": verify_pins.digest(good)}
        manifest = self.bare_manifest(sources=[entry])
        common = (
            mock.patch.object(verify_pins, "manifest", return_value=manifest),
            mock.patch.object(verify_pins.subprocess, "run", return_value=success),
            mock.patch.object(verify_pins, "git_text", return_value="head"),
        )
        with common[0], common[1], common[2], mock.patch.object(
            verify_pins, "blob", return_value=b"moved"
        ):
            with self.assertRaisesRegex(ValueError, "snapshot blob moved"):
                verify_pins.verify()
        with (
            mock.patch.object(verify_pins, "manifest", return_value=manifest),
            mock.patch.object(verify_pins.subprocess, "run", return_value=success),
            mock.patch.object(verify_pins, "git_text", return_value="head"),
            mock.patch.object(verify_pins, "blob", side_effect=(good, b"moved")),
        ):
            with self.assertRaisesRegex(ValueError, "HEAD blob moved"):
                verify_pins.verify()

    def test_span_failures_are_named(self) -> None:
        success = mock.Mock(returncode=0, stderr=b"", stdout=b"")
        base_patches = (
            mock.patch.object(verify_pins.subprocess, "run", return_value=success),
            mock.patch.object(verify_pins, "git_text", return_value="head"),
        )
        cases = (
            ({"name": None, "path": "s", "start": 1, "end": 1, "sha256": "0" * 64}, "name must be text"),
            ({"name": "span", "path": "s", "start": "1", "end": 1, "sha256": "0" * 64}, "bounds must be integers"),
        )
        for entry, message in cases:
            with self.subTest(message=message):
                with (
                    mock.patch.object(
                        verify_pins,
                        "manifest",
                        return_value=self.bare_manifest(spans=[entry]),
                    ),
                    mock.patch.object(verify_pins.subprocess, "run", return_value=success),
                    mock.patch.object(verify_pins, "git_text", return_value="head"),
                ):
                    with self.assertRaisesRegex(ValueError, message):
                        verify_pins.verify()

        moved = {
            "name": "span",
            "path": "s",
            "start": 1,
            "end": 1,
            "sha256": verify_pins.digest(b"expected\n"),
        }
        with (
            mock.patch.object(
                verify_pins, "manifest", return_value=self.bare_manifest(spans=[moved])
            ),
            base_patches[0],
            base_patches[1],
            mock.patch.object(verify_pins, "blob", return_value=b"moved\n"),
        ):
            with self.assertRaisesRegex(ValueError, "span moved"):
                verify_pins.verify()

    def test_frozen_text_and_presence_failures_are_named(self) -> None:
        success = mock.Mock(returncode=0, stderr=b"", stdout=b"")
        with tempfile.TemporaryDirectory() as raw_directory:
            root = pathlib.Path(raw_directory)
            frozen = root / "frozen.txt"

            def run_frozen(raw: bytes | None, wanted: bytes, head: bytes, no_digits: bool = False) -> None:
                if raw is None:
                    frozen.unlink(missing_ok=True)
                else:
                    frozen.write_bytes(raw)
                entry = {
                    "path": "frozen.txt",
                    "sha256": verify_pins.digest(wanted),
                    "no_digits": no_digits,
                }
                with (
                    mock.patch.object(
                        verify_pins,
                        "manifest",
                        return_value=self.bare_manifest(frozen_texts=[entry]),
                    ),
                    mock.patch.object(verify_pins, "REPO", root),
                    mock.patch.object(verify_pins.subprocess, "run", return_value=success),
                    mock.patch.object(verify_pins, "git_text", return_value="head"),
                    mock.patch.object(verify_pins, "blob", return_value=head),
                ):
                    verify_pins.verify()

            with self.assertRaisesRegex(ValueError, "missing from disk"):
                run_frozen(None, b"good", b"good")
            with self.assertRaisesRegex(ValueError, "moved on disk"):
                run_frozen(b"bad", b"good", b"good")
            with self.assertRaisesRegex(ValueError, "moved in HEAD"):
                run_frozen(b"good", b"good", b"bad")
            with self.assertRaisesRegex(ValueError, "contains a digit"):
                run_frozen(b"digit 1", b"digit 1", b"digit 1", True)

        presence = {"path": "parallel", "present": False}

        def fake_git_text(*arguments: str) -> str:
            return "head" if arguments[0] == "rev-parse" else "parallel"

        with (
            mock.patch.object(
                verify_pins,
                "manifest",
                return_value=self.bare_manifest(absent_at_snapshot=[presence]),
            ),
            mock.patch.object(verify_pins.subprocess, "run", return_value=success),
            mock.patch.object(verify_pins, "git_text", side_effect=fake_git_text),
        ):
            with self.assertRaisesRegex(ValueError, "presence record differs"):
                verify_pins.verify()

    def test_pin_main_reports_success_and_failure(self) -> None:
        output = io.StringIO()
        with (
            mock.patch.object(verify_pins, "verify", side_effect=ValueError("probe")),
            contextlib.redirect_stdout(output),
        ):
            self.assertEqual(verify_pins.main(), 1)
        self.assertIn("FAIL: probe", output.getvalue())
        output = io.StringIO()
        with (
            mock.patch.object(verify_pins, "verify", return_value=["verified"]),
            contextlib.redirect_stdout(output),
        ):
            self.assertEqual(verify_pins.main(), 0)
        self.assertEqual(output.getvalue().strip(), "verified")


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
        with self.assertRaises(ValueError):
            observables.profile_size(self.collapsed, 2)
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
        invalid = StakeRule("bad", (), lambda regime, i, j: "bad", "control")
        with self.assertRaisesRegex(ValueError, "rule bad returned"):
            invalid.label(self.collapsed, 0, 1)

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
        self.assertEqual(generation._json({2, 1}), [1, 2])
        with self.assertRaises(TypeError):
            generation._json(object())
        missing = generation.Tree("L", "absent", "mu1")
        with self.assertRaises(ValueError):
            generation._tree_rule(missing)

    def test_defensive_helpers_and_guard_quotient(self) -> None:
        collision = Regime(
            ("stake_g2", "stake_g2_1"), (), frozenset(), frozenset(), frozenset()
        )
        self.assertEqual(generation._fresh_token(collision), "stake_g2_2")
        with self.assertRaises(TypeError):
            generation._json_int("not-an-integer")
        with mock.patch.object(generation, "tree_stats", return_value={"kinds_answered": "bad"}):
            with self.assertRaisesRegex(TypeError, "tree kinds"):
                generation.rule_generation_record(
                    rule_named("E1"), [generation.Tree("L", "E1", "mu1")]
                )
        regime = replay(READINGS[0].genesis)
        with mock.patch.object(
            generation, "quotient_key", side_effect=generation.IsoBudgetError("guard")
        ):
            self.assertEqual(
                generation._quotient_deltas(regime, rule_named("E1"), ((),)),
                [((), 1)],
            )

    def test_small_invariance_paths_cover_refutation_and_orbit_transport(self) -> None:
        data = summary()
        rows = cast(list[dict[str, object]], data["invariance"])
        parity_row = next(row for row in rows if row["rule"] == "parity")
        witness = regime_from_json(parity_row["source_regime"])
        refuted = generation.invariance_records((rule_named("parity"),), (witness,))
        self.assertEqual(refuted[0]["disposition"], "REFUTED")

        collapsed = Regime(("a", "b"), (), frozenset(), frozenset(), frozenset())
        direct = generation.invariance_record(rule_named("E1"), (collapsed,))
        self.assertEqual(direct["disposition"], "CHECKED")
        orbit = generation.invariance_records((rule_named("E3"),), (collapsed,))
        self.assertEqual(orbit[0]["disposition"], "CHECKED")


class ReceiptTests(unittest.TestCase):
    def test_full_receipt_hash_and_replay_certificates(self) -> None:
        small = summary()
        full_path = HERE / "receipts" / "full" / "stake_full.json.gz"
        compressed = full_path.read_bytes()
        self.assertEqual(compressed[:10], b"\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\xff")
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
        self.assertEqual(gzip.decompress(run_stake.deterministic_gzip(b"")), b"")
        with self.assertRaises(TypeError):
            run_stake._as_str_list("not a list")
        with self.assertRaises(TypeError):
            run_stake._as_int("not an integer")

    def test_sibling_baseline_rejects_malformed_receipts(self) -> None:
        malformed = (
            ([], "must be an object"),
            ({}, "lacks bounds or summary"),
            ({"bounds": {}, "summary": {}}, "lacks its control summary"),
            ({"bounds": {}, "summary": {"by_commitment": {}}}, "lacks control"),
        )
        with tempfile.TemporaryDirectory() as raw_directory:
            path = pathlib.Path(raw_directory) / "sibling.json"
            with mock.patch.object(run_stake, "SIBLING_RECEIPT", path):
                for value, message in malformed:
                    with self.subTest(message=message):
                        path.write_text(json.dumps(value), encoding="utf-8")
                        with self.assertRaisesRegex(ValueError, message):
                            run_stake.sibling_baseline()

    def test_tie_and_label_equivalence_edge_paths(self) -> None:
        with self.assertRaisesRegex(TypeError, "tree_signatures"):
            run_stake._signature_tuple({"tree_signatures": []})
        self.assertEqual(
            run_stake.tie_map(
                [{"rule": "outside", "tree_signatures": {}}], MENU[:1]
            ),
            {"E1": []},
        )
        collapsed = Regime(("a", "b"), (), frozenset(), frozenset(), frozenset())
        with mock.patch.object(run_stake, "label_map", return_value=()):
            equal = run_stake.label_equivalence((collapsed,), MENU[:2])
        self.assertEqual(equal, {"E1": ["E2"], "E2": ["E1"]})
        with mock.patch.object(
            run_stake,
            "label_map",
            side_effect=observables.ObservableGuardError("guard"),
        ):
            guarded = run_stake.label_equivalence((collapsed,), MENU[:2])
        self.assertEqual(guarded, {"E1": [], "E2": []})

    def test_receipt_io_and_cli_failure_paths(self) -> None:
        with tempfile.TemporaryDirectory(dir=HERE) as raw_directory:
            root = pathlib.Path(raw_directory)
            summary_path = root / "nested" / "summary.json"
            full_path = root / "full" / "full.json.gz"
            with mock.patch.object(run_stake, "render_receipts", return_value=(b"summary", b"full")):
                run_stake.write_receipts(summary_path, full_path)
                self.assertEqual(summary_path.read_bytes(), b"summary")
                self.assertEqual(full_path.read_bytes(), b"full")
                summary_path.unlink()
                full_path.unlink()
                self.assertEqual(
                    run_stake.check_receipts(summary_path, full_path),
                    [
                        "receipt differs: " + str(summary_path.relative_to(HERE)),
                        "receipt differs: " + str(full_path.relative_to(HERE)),
                    ],
                )

            output = io.StringIO()
            with (
                mock.patch.object(run_stake, "check_receipts", return_value=["one", "two"]),
                contextlib.redirect_stdout(output),
            ):
                self.assertEqual(run_stake.main(["--check"]), 1)
            self.assertEqual(output.getvalue().splitlines(), ["FAIL: one", "FAIL: two"])

            output = io.StringIO()
            with (
                mock.patch.object(run_stake, "write_receipts") as writer,
                contextlib.redirect_stdout(output),
            ):
                self.assertEqual(
                    run_stake.main(
                        ["--out", str(summary_path), "--full", str(full_path)]
                    ),
                    0,
                )
            writer.assert_called_once_with(summary_path, full_path)
            self.assertIn(f"wrote {summary_path}", output.getvalue())


if __name__ == "__main__":
    unittest.main()
