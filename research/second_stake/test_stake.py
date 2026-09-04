"""Fast structural tests for the frozen menu and committed receipts."""

from __future__ import annotations

import contextlib
import gzip
import hashlib
import io
import json
import pathlib
import re
import sys
import tempfile
import types
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
from derivation.iso import serialize  # noqa: E402
from derivation.model import AdmitDatum, AdmitForm, Regime, replay  # noqa: E402

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
    TEST_CALLERS = frozenset({__name__, "test_forbidden"})

    @staticmethod
    def bare_manifest(**updates: object) -> dict[str, object]:
        value: dict[str, object] = {
            "schema": "second_stake_source_manifest/v2",
            "snapshot_commit": "a" * 40,
            "freeze_commit": verify_pins.FREEZE_COMMIT,
            "sources": [],
            "spans": [],
            "frozen_texts": [
                {
                    "path": "research/second_stake/PROMPT.md",
                    "sha256": PROMPT_SHA,
                    "no_digits": True,
                },
                {
                    "path": "research/second_stake/PREDICTIONS.md",
                    "sha256": PREDICTIONS_SHA,
                    "no_digits": False,
                },
            ],
            "runtime_modules": [
                {
                    "name": name,
                    "path": path.as_posix(),
                    "pinned_source": name in verify_pins.PINNED_RUNTIME_MODULES,
                }
                for name, path in verify_pins.RUNTIME_MODULE_PATHS.items()
            ],
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
        self.assertIn(f"freeze: {verify_pins.FREEZE_COMMIT} (ancestor of HEAD)", lines)
        self.assertTrue(any("challenge_two" in line for line in lines))
        self.assertIn("runtime module census: 14", lines)

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
                    mock.patch.object(
                        verify_pins,
                        "FROZEN_POLICY",
                        {pathlib.PurePosixPath("frozen.txt"): no_digits},
                    ),
                    mock.patch.object(verify_pins.subprocess, "run", return_value=success),
                    mock.patch.object(verify_pins, "git_text", return_value="head"),
                    mock.patch.object(verify_pins, "blob", side_effect=(wanted, head)),
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
                return_value=self.bare_manifest(
                    frozen_texts=[], absent_at_snapshot=[presence]
                ),
            ),
            mock.patch.object(verify_pins, "FROZEN_POLICY", {}),
            mock.patch.object(verify_pins.subprocess, "run", return_value=success),
            mock.patch.object(verify_pins, "git_text", side_effect=fake_git_text),
        ):
            with self.assertRaisesRegex(ValueError, "presence record differs"):
                verify_pins.verify()

    def test_freeze_commit_hash_and_population_injections_are_refused(self) -> None:
        with mock.patch.object(
            verify_pins,
            "manifest",
            return_value=self.bare_manifest(freeze_commit="f" * 40),
        ):
            with self.assertRaisesRegex(ValueError, "original freeze"):
                verify_pins.verify()

        success = mock.Mock(returncode=0, stderr=b"", stdout=b"")
        entry = {
            "path": "frozen.txt",
            "sha256": verify_pins.digest(b"mutable replacement"),
            "no_digits": False,
        }
        with tempfile.TemporaryDirectory() as raw_directory:
            root = pathlib.Path(raw_directory)
            (root / "frozen.txt").write_bytes(b"mutable replacement")
            with (
                mock.patch.object(
                    verify_pins,
                    "manifest",
                    return_value=self.bare_manifest(frozen_texts=[entry]),
                ),
                mock.patch.object(verify_pins, "REPO", root),
                mock.patch.object(
                    verify_pins,
                    "FROZEN_POLICY",
                    {pathlib.PurePosixPath("frozen.txt"): False},
                ),
                mock.patch.object(verify_pins.subprocess, "run", return_value=success),
                mock.patch.object(verify_pins, "git_text", return_value="head"),
                mock.patch.object(verify_pins, "blob", return_value=b"original freeze"),
            ):
                with self.assertRaisesRegex(ValueError, "differs from freeze commit"):
                    verify_pins.verify()

        data = self.bare_manifest()
        cast(list[object], data["runtime_modules"]).pop()
        with self.assertRaisesRegex(ValueError, "closed census"):
            verify_pins.runtime_manifest(data)

    def test_runtime_origin_source_and_extra_module_injections_are_refused(self) -> None:
        modules = run_stake.runtime_modules(excluded_module_names=self.TEST_CALLERS)
        lines = verify_pins.verify_runtime_origins(modules)
        self.assertEqual(len(lines), len(verify_pins.RUNTIME_MODULE_PATHS))

        with self.assertRaisesRegex(ValueError, "population differs"):
            verify_pins.verify_runtime_origins(run_stake.runtime_modules())

        wrong_dual = types.ModuleType("dual")
        wrong_dual.__file__ = str(REPO / "research" / "observer_visibility" / "dual.py")
        wrong_modules = dict(modules)
        wrong_modules["dual"] = wrong_dual
        with self.assertRaisesRegex(ValueError, "origin differs: dual"):
                verify_pins.verify_runtime_origins(wrong_modules)

        missing_origin = types.ModuleType("dual")
        missing_origin_modules = dict(modules)
        missing_origin_modules["dual"] = missing_origin
        with self.assertRaisesRegex(ValueError, "has no file origin: dual"):
            verify_pins.verify_runtime_origins(missing_origin_modules)

        mutated = json.loads(json.dumps(verify_pins.manifest()))
        for entry in cast(list[dict[str, object]], mutated["sources"]):
            if entry["path"] == "research/identification_dual/dual.py":
                entry["sha256"] = "0" * 64
        with mock.patch.object(verify_pins, "manifest", return_value=mutated):
            with self.assertRaisesRegex(ValueError, "source bytes differ from the pin: dual"):
                verify_pins.verify_runtime_origins(modules)

        missing_pin = json.loads(json.dumps(verify_pins.manifest()))
        missing_pin["sources"] = [
            entry
            for entry in cast(list[dict[str, object]], missing_pin["sources"])
            if entry["path"] != "research/identification_dual/dual.py"
        ]
        with mock.patch.object(verify_pins, "manifest", return_value=missing_pin):
            with self.assertRaisesRegex(ValueError, "lacks a source pin: dual"):
                verify_pins.verify_runtime_origins(modules)

        extra = types.ModuleType("test_extra_probe")
        extra.__file__ = str(HERE / "check_coverage.py")
        sys.modules[extra.__name__] = extra
        try:
            with self.assertRaisesRegex(ValueError, "population differs"):
                verify_pins.verify_runtime_origins(
                    run_stake.runtime_modules(
                        excluded_module_names=self.TEST_CALLERS
                    )
                )
        finally:
            del sys.modules[extra.__name__]

    def test_additional_manifest_and_verifier_branches_fail_closed(self) -> None:
        cases: list[tuple[object, str]] = []
        for message in ("name", "duplicate", "boolean"):
            data = self.bare_manifest()
            runtime = cast(list[dict[str, object]], data["runtime_modules"])
            if message == "name":
                runtime[0]["name"] = None
                expected = "name must be non-empty text"
            elif message == "duplicate":
                runtime.append(dict(runtime[0]))
                expected = "duplicate runtime module"
            else:
                runtime[0]["pinned_source"] = "yes"
                expected = "pinned_source must be boolean"
            cases.append((data, expected))
        for data, expected in cases:
            with self.subTest(expected=expected):
                with self.assertRaisesRegex(ValueError, expected):
                    verify_pins.runtime_manifest(cast(dict[str, object], data))

        with mock.patch.object(
            verify_pins,
            "manifest",
            return_value=self.bare_manifest(schema="old"),
        ):
            with self.assertRaisesRegex(ValueError, "source manifest schema"):
                verify_pins.verify()

        success = mock.Mock(returncode=0, stderr=b"", stdout=b"")
        failure = mock.Mock(returncode=9, stderr=b"", stdout=b"")
        with (
            mock.patch.object(verify_pins, "manifest", return_value=self.bare_manifest()),
            mock.patch.object(
                verify_pins.subprocess, "run", side_effect=(success, failure)
            ),
            mock.patch.object(verify_pins, "git_text", return_value="head"),
        ):
            with self.assertRaisesRegex(ValueError, "freeze is not a verified ancestor"):
                verify_pins.verify()

        duplicate_frozen = self.bare_manifest()
        frozen = cast(list[dict[str, object]], duplicate_frozen["frozen_texts"])
        frozen.append(dict(frozen[0]))
        with (
            mock.patch.object(verify_pins, "manifest", return_value=duplicate_frozen),
            mock.patch.object(verify_pins.subprocess, "run", return_value=success),
            mock.patch.object(verify_pins, "git_text", return_value="head"),
        ):
            with self.assertRaisesRegex(ValueError, "duplicate frozen text"):
                verify_pins.verify()

        wrong_policy = self.bare_manifest()
        cast(list[dict[str, object]], wrong_policy["frozen_texts"])[0][
            "no_digits"
        ] = False
        with (
            mock.patch.object(verify_pins, "manifest", return_value=wrong_policy),
            mock.patch.object(verify_pins.subprocess, "run", return_value=success),
            mock.patch.object(verify_pins, "git_text", return_value="head"),
            mock.patch.object(
                verify_pins,
                "blob",
                return_value=(HERE / "PROMPT.md").read_bytes(),
            ),
        ):
            with self.assertRaisesRegex(ValueError, "no_digits policy differs"):
                verify_pins.verify()

        no_sources = self.bare_manifest(frozen_texts=[])
        with (
            mock.patch.object(verify_pins, "manifest", return_value=no_sources),
            mock.patch.object(verify_pins, "FROZEN_POLICY", {}),
            mock.patch.object(verify_pins.subprocess, "run", return_value=success),
            mock.patch.object(verify_pins, "git_text", return_value="head"),
        ):
            with self.assertRaisesRegex(ValueError, "lacks a source pin"):
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
        self.assertEqual(record["growth_kinds"], [])
        self.assertEqual(record["response_target_kinds"], [])
        self.assertIs(record["kind_populations_agree"], True)
        self.assertEqual(record["relabellings"], 0)
        self.assertTrue(all(node.certified for node in tree.nodes))
        self.assertEqual(generation.tree_stats(tree)["guard_nodes"], 0)

    def test_quotient_keeps_control_indices_and_menu_forgets_them(self) -> None:
        regime = replay(READINGS[0].genesis)
        menu_key = generation.quotient_key(regime, rule_named("E1"))
        control_key = generation.quotient_key(regime, rule_named("parity"))
        self.assertNotEqual(menu_key, control_key)
        self.assertEqual(generation.indexed_key(regime)[0], regime.n_data())
        self.assertNotEqual(
            generation.search_key(regime, rule_named("E1"), 0),
            generation.search_key(regime, rule_named("E1"), 1),
        )

    def test_one_refusal_does_not_suppress_an_answerable_demand(self) -> None:
        refused = (APART, (0, 1))
        answerable = (SAME, (0, 1))
        minima = generation.Minima("mu1", (1, -1), ((),), 1)
        with (
            mock.patch.object(
                generation, "demands", return_value=(refused, answerable)
            ),
            mock.patch.object(
                generation,
                "minimum_responses",
                side_effect=(None, minima),
            ),
            mock.patch.object(
                generation, "_quotient_deltas", return_value=[((), 1)]
            ),
            mock.patch.object(generation, "response_valid", return_value=True),
            mock.patch.object(generation, "_attach") as attach,
        ):
            tree = generation.build_tree(
                READINGS[0], rule_named("E1"), "mu1", node_guard=2
            )
        attach.assert_called_once()
        self.assertEqual(tree.nodes[0].status, "expanded_with_refusals")
        self.assertEqual(
            tree.refusals,
            [
                {
                    "node": 0,
                    "kind": APART,
                    "pair": [0, 1],
                    "data": tree.nodes[0].regime.n_data(),
                    "open_demands": 2,
                    "answerable_demands": 1,
                    "terminal": False,
                }
            ],
        )

    def test_edge_certificate_refuses_round_and_transport_mutations(self) -> None:
        tree = generation.build_tree(
            READINGS[0], rule_named("E1"), "mu1", max_data=3
        )
        edge = tree.edges[0]
        self.assertIsNone(generation.edge_replay_failure(tree, edge))

        child = tree.nodes[edge.child]
        original_rounds = child.response_rounds
        child.response_rounds += 1
        self.assertIn(
            "response-round mismatch",
            generation.edge_replay_failure(tree, edge) or "",
        )
        child.response_rounds = original_rounds

        original_transport = edge.datum_transport
        edge.datum_transport = tuple(0 for _ in original_transport)
        self.assertIn(
            "datum transport is not a bijection",
            generation.edge_replay_failure(tree, edge) or "",
        )
        edge.datum_transport = original_transport
        self.assertIsNone(generation.edge_replay_failure(tree, edge))

        original_form_transport = edge.form_transport
        edge.form_transport = (0, 0)
        self.assertIn(
            "form transport is not a bijection",
            generation.edge_replay_failure(tree, edge) or "",
        )
        edge.form_transport = original_form_transport

        original_parent = edge.parent
        edge.parent = -1
        self.assertIn("parent is outside", generation.edge_replay_failure(tree, edge) or "")
        edge.parent = original_parent
        original_child_id = edge.child
        edge.child = len(tree.nodes)
        self.assertIn("child is outside", generation.edge_replay_failure(tree, edge) or "")
        edge.child = original_child_id

        original_events = edge.events
        edge.events = (AdmitForm(0),)
        self.assertIn("event replay failed", generation.edge_replay_failure(tree, edge) or "")
        edge.events = original_events

        original_regime = child.regime
        child.regime = Regime(
            original_regime.data,
            original_regime.forms,
            original_regime.insts,
            original_regime.rules,
            frozenset({(0, 1)}),
        )
        self.assertIn(
            "transport does not reach",
            generation.edge_replay_failure(tree, edge) or "",
        )
        child.regime = original_regime
        self.assertIsNone(generation.edge_replay_failure(tree, edge))

        parent = tree.nodes[0]
        with self.assertRaisesRegex(AssertionError, "does not extend"):
            generation._attach(
                tree,
                rule_named("E1"),
                {},
                generation.deque(),
                parent,
                (),
                parent.response_rounds,
                "probe",
                None,
                (),
                (0, 0),
                1,
                1,
            )

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
        with mock.patch.object(
            generation,
            "tree_stats",
            return_value={
                "growth_demand_kinds": "bad",
                "response_target_kinds": [],
            },
        ):
            with self.assertRaisesRegex(TypeError, "tree growth kinds"):
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

        tree = generation.build_tree(
            READINGS[0], rule_named("E1"), "mu1", max_data=3
        )
        growth_edge = next(edge for edge in tree.edges if edge.target_pair is None)
        original_demands = growth_edge.info["new_demands"]
        growth_edge.info["new_demands"] = "bad"
        with self.assertRaisesRegex(TypeError, "new_demands must be a list"):
            generation.tree_stats(tree)
        growth_edge.info["new_demands"] = [["apart", 0]]
        with self.assertRaisesRegex(TypeError, "demand must be"):
            generation.tree_stats(tree)
        growth_edge.info["new_demands"] = original_demands

        with mock.patch.object(
            generation,
            "tree_stats",
            return_value={
                "growth_demand_kinds": [],
                "response_target_kinds": "bad",
            },
        ):
            with self.assertRaisesRegex(TypeError, "tree response kinds"):
                generation.rule_generation_record(
                    rule_named("E1"), [generation.Tree("L", "E1", "mu1")]
                )

    def test_small_invariance_paths_cover_refutation_and_refuse_unreplayed_orbits(self) -> None:
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
        self.assertEqual(orbit[0]["disposition"], "OPEN_AT_TRANSPORT_REPLAY")
        self.assertIn("not exhaustively replayed", cast(str, orbit[0]["obstruction"]))

    def test_growth_kind_scoring_does_not_substitute_response_targets(self) -> None:
        data = summary()
        generation_rows = json.loads(json.dumps(data["generation"]))
        invariance_rows = cast(list[dict[str, Json]], data["invariance"])
        ties = cast(dict[str, list[str]], data["tree_ties"])
        control_target = run_stake.control_target_record(invariance_rows)
        e1 = next(row for row in generation_rows if row["rule"] == "E1")

        e1["growth_kinds"] = ["apart"]
        e1["response_target_kinds"] = []
        _, detail = run_stake.score_predictions(
            generation_rows, invariance_rows, ties, control_target
        )
        p_g1 = next(row for row in detail if row["id"] == "P-G1")
        self.assertEqual(p_g1["verdict"], "MISS")

        e1["growth_kinds"] = []
        e1["response_target_kinds"] = ["apart"]
        _, detail = run_stake.score_predictions(
            generation_rows, invariance_rows, ties, control_target
        )
        p_g1 = next(row for row in detail if row["id"] == "P-G1")
        self.assertEqual(p_g1["verdict"], "HIT")

    def test_control_target_and_p_i4_require_both_constants_unrefuted(self) -> None:
        rows = json.loads(json.dumps(summary()["invariance"]))
        actual = run_stake.control_target_record(rows)
        self.assertEqual(actual["disposition"], "REFUTED")
        self.assertIs(actual["both_constant_controls_unrefuted"], True)
        self.assertIs(actual["p_i4_falsifier_found"], False)

        total_same = next(row for row in rows if row["rule"] == "total_same")
        total_same["disposition"] = "REFUTED"
        injected = run_stake.control_target_record(rows)
        self.assertIs(injected["both_constant_controls_unrefuted"], False)
        self.assertIs(injected["p_i4_falsifier_found"], True)


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
            refusals = cast(list[dict[str, object]], tree["refusals"])
            stats = cast(dict[str, object], tree["stats"])
            node_by_id = {cast(int, node["id"]): node for node in nodes}
            self.assertTrue(all(node["certified"] is True for node in nodes))
            self.assertIs(stats["all_edges_certified"], True)
            self.assertTrue(all(cast(int, edge["parent"]) < len(nodes) and cast(int, edge["child"]) < len(nodes) for edge in edges))
            for node in nodes:
                history = tuple(
                    event_from_json(cast(Mapping[str, Json], event))
                    for event in cast(list[object], node["history"])
                )
                self.assertEqual(regime_json(replay(history)), node["regime"])
            for edge in edges:
                self.assertIs(edge["certified"], True)
                parent = node_by_id[cast(int, edge["parent"])]
                child = node_by_id[cast(int, edge["child"])]
                parent_regime = regime_from_json(parent["regime"])
                child_regime = regime_from_json(child["regime"])
                events = tuple(
                    event_from_json(cast(Mapping[str, Json], event))
                    for event in cast(list[object], edge["events"])
                )
                after = replay(events, parent_regime)
                datum_transport = tuple(cast(list[int], edge["datum_transport"]))
                form_transport = tuple(cast(list[int], edge["form_transport"]))
                self.assertEqual(
                    serialize(after, datum_transport, form_transport),
                    serialize(
                        child_regime,
                        tuple(range(child_regime.n_data())),
                        tuple(range(len(child_regime.forms))),
                    ),
                )
                expected_rounds = cast(int, parent["response_rounds"]) + int(
                    edge["target_pair"] is not None
                )
                self.assertEqual(child["response_rounds"], expected_rounds)
            for refusal in refusals:
                node = node_by_id[cast(int, refusal["node"])]
                if refusal["terminal"] is True:
                    self.assertEqual(refusal["answerable_demands"], 0)
                    self.assertEqual(node["status"], "terminal_no_response")
                else:
                    self.assertGreater(cast(int, refusal["answerable_demands"]), 0)
                    self.assertEqual(node["status"], "expanded_with_refusals")

    def test_summary_records_exact_finite_terminal(self) -> None:
        data = summary()
        self.assertEqual(data["reached_regimes"], 847)
        self.assertEqual(
            cast(dict[str, object], data["predictions_scored"]),
            {
                "hit": 6,
                "missed": 9,
                "pending": 1,
                "unscored_declared_policy": 1,
            },
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
        controls_refuted = cast(dict[str, object], data["controls_refuted"])
        self.assertEqual(controls_refuted["disposition"], "REFUTED")
        self.assertEqual(
            controls_refuted["invariant_counterexamples"],
            ["total_apart", "total_same"],
        )
        p_c1 = next(
            row
            for row in cast(list[dict[str, object]], data["prediction_detail"])
            if row["id"] == "P-C1"
        )
        self.assertEqual(p_c1["verdict"], "UNSCORED_DECLARED_POLICY")

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
        self.assertEqual(by_name["E4"]["growth_kinds"], ["apart", "same"])
        self.assertEqual(by_name["E4"]["response_target_kinds"], ["apart", "same"])
        self.assertTrue(all(row["kind_populations_agree"] is True for row in generation_rows))
        self.assertEqual(by_name["E4"]["relabellings"], 683)
        self.assertEqual(by_name["E4"]["refusals"], 204)
        self.assertEqual(by_name["E4"]["fixpoints"], 152)
        self.assertEqual(by_name["E4"]["guard_nodes"], 151)
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


class TargetedLedgerReceiptTests(unittest.TestCase):
    """Resolve structured rule references and selected receipt-bound headlines."""

    def test_structured_ledger_references_resolve_against_receipt(self) -> None:
        data = summary()
        ledger = (HERE / "CLAIM_LEDGER.md").read_text("utf-8")
        generation_names = {
            cast(str, row["rule"])
            for row in cast(list[dict[str, object]], data["generation"])
        }
        invariance_names = {
            cast(str, row["rule"])
            for row in cast(list[dict[str, object]], data["invariance"])
        }
        generation_refs = set(re.findall(r"`generation\[([^]]+)\]`", ledger))
        invariance_refs = set(re.findall(r"`invariance\[([^]]+)\]`", ledger))
        self.assertTrue(generation_refs)
        self.assertTrue(invariance_refs)
        self.assertEqual(generation_refs - generation_names, set())
        self.assertEqual(invariance_refs - invariance_names, set())
        self.assertIn("`both_kind_members`", ledger)
        self.assertIn("both_kind_members", data)
        for terminal in re.findall(r"`([A-Z][A-Z0-9_]+)`", ledger):
            self.assertIn(terminal, cast(list[str], data["terminals"]))

    def test_ledger_and_status_headlines_equal_receipt_values(self) -> None:
        data = summary()
        ledger = (HERE / "CLAIM_LEDGER.md").read_text("utf-8")
        status = (HERE / "STATUS.md").read_text("utf-8")
        flat_ledger = re.sub(r"\s+", " ", ledger)
        flat_status = re.sub(r"\s+", " ", status)
        generation_rows = cast(list[dict[str, object]], data["generation"])
        by_generation = {cast(str, row["rule"]): row for row in generation_rows}
        invariance_rows = cast(list[dict[str, object]], data["invariance"])
        by_invariance = {cast(str, row["rule"]): row for row in invariance_rows}
        e4 = by_generation["E4"]
        e4_claim = (
            f"E4 generates apart and same under growth, re-labels "
            f"{e4['relabellings']} old pairs, records {e4['refusals']} refusals, "
            f"{e4['fixpoints']} fixpoints, and {e4['guard_nodes']} guarded nodes"
        )
        self.assertIn(e4_claim, flat_ledger)
        self.assertIn(e4_claim, flat_status)

        checks = cast(int, by_invariance["E1"]["checks"])
        for name in ("E1", "E2", "E5", "E7", "E8", "E9"):
            self.assertEqual(by_invariance[name]["checks"], checks)
            self.assertIn(
                f"{name} labels commute in all {checks:,} checked pair-renaming cases",
                flat_ledger,
            )
        self.assertIn(
            f"each non-orbit menu rule and each constant control passed {checks:,} pair-renaming cases",
            flat_status,
        )

        crosscheck = cast(dict[str, object], data["canonical_crosscheck"])
        canonical_claim = (
            f"same partition for {crosscheck['regimes_checked']} reached regimes; "
            f"{crosscheck['regimes_above_permutation_budget']} regimes are above the guard"
        )
        self.assertIn(canonical_claim, flat_ledger)
        self.assertIn(canonical_claim, flat_status)
        self.assertIn(
            f"generation trees supplied {data['reached_regimes']} distinct structural regimes",
            flat_status,
        )

        full = cast(dict[str, object], data["full_export"])
        self.assertIn(
            f"contains {full['uncompressed_bytes']:,} uncompressed bytes", flat_status
        )
        self.assertIn(cast(str, full["uncompressed_sha256"]), flat_status)
        self.assertIn(
            "The blanket proposition `controls_refuted` is REFUTED",
            flat_ledger,
        )
        score = cast(dict[str, object], data["predictions_scored"])
        score_claim = (
            f"{score['hit']} HIT, {score['missed']} MISS, "
            f"{score['unscored_declared_policy']} UNSCORED_DECLARED_POLICY, "
            f"and {score['pending']} PENDING"
        )
        self.assertIn(score_claim, flat_ledger)
        self.assertIn(score_claim, flat_status)


if __name__ == "__main__":
    unittest.main()
