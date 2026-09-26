"""The handoff command reports skips and failures; the demonstrations hold offline."""

from __future__ import annotations

import ast
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parents[1] / "code"))

import handoff_demo  # noqa: E402
import verify  # noqa: E402

# Modules that would reach a model provider or the network.
OFFLINE_REFUSED = (
    "anthropic",
    "openai",
    "httpx",
    "aiohttp",
    "requests",
    "urllib",
    "http",
    "socket",
    "ssl",
)


class VerifyCommand(unittest.TestCase):
    def test_unittest_skip_is_named(self) -> None:
        output = (
            "test_a (tests.test_x.Case.test_a) ... ok\n"
            "test_b (tests.test_x.Case.test_b) ... skipped 'no record'\n"
            "OK (skipped=1)\n"
        )
        self.assertEqual(
            verify.skipped_checks(output), ["tests.test_x.Case.test_b"]
        )

    def test_unittest_skip_after_a_docstring_line_is_named(self) -> None:
        output = (
            "test_b (tests.test_x.Case.test_b)\n"
            "A docstring line. ... skipped 'no record'\n"
            "OK (skipped=1)\n"
        )
        self.assertEqual(
            verify.skipped_checks(output), ["tests.test_x.Case.test_b"]
        )

    def test_pytest_skip_is_named(self) -> None:
        output = (
            "SKIPPED [1] tests/test_iso.py:12: slow\n"
            "65 passed, 1 skipped in 2.00s\n"
        )
        self.assertEqual(
            verify.skipped_checks(output), ["[1] tests/test_iso.py:12: slow"]
        )

    def test_counted_but_unnamed_skip_is_still_reported(self) -> None:
        self.assertEqual(
            verify.skipped_checks("Ran 3 tests\nOK (skipped=2)\n"),
            ["unnamed skipped test", "unnamed skipped test"],
        )
        self.assertEqual(
            verify.skipped_checks("orphan ... skipped 'r'\n"),
            ["orphan ... skipped 'r'"],
        )

    def test_no_skip(self) -> None:
        self.assertEqual(verify.skipped_checks("Ran 3 tests\nOK\n"), [])

    def test_ok_lines_are_hidden_and_others_shown(self) -> None:
        output = (
            "test_a (x.C.test_a) ... ok\n"
            "test_c (x.C.test_c)\n"
            "Docstring. ... ok\n"
            "FAIL: test_b\nOK\n"
        )
        self.assertEqual(verify.shown(output), "FAIL: test_b\nOK")

    def test_every_required_step_is_listed(self) -> None:
        self.assertEqual(
            [step.name for step in verify.STEPS],
            [
                "sources",
                "tests",
                "coverage_json",
                "coverage",
                "mypy",
                "lean",
                "computation",
                "handoff",
                "kernel_tests",
            ],
        )
        for relative in verify.KERNEL_TESTS:
            self.assertTrue((verify.REPO / relative).is_file(), relative)


class HandoffDemonstrations(unittest.TestCase):
    def test_every_independent_check_holds(self) -> None:
        record = handoff_demo.compute()
        checks = record["independent_checks"]
        assert isinstance(checks, dict)
        self.assertGreaterEqual(len(checks), 20)
        self.assertEqual(
            sorted(name for name, ok in checks.items() if ok is not True), []
        )
        demos = record["demonstrations"]
        assert isinstance(demos, dict)
        self.assertEqual(
            sorted(demos),
            ["accepted_transition", "bounded_stop", "refused", "retained_ties"],
        )
        self.assertEqual(record["model_provider"], "none")

    def test_committed_record_matches(self) -> None:
        fresh, failed = handoff_demo.record_bytes()
        self.assertEqual(failed, [])
        on_disk = handoff_demo.RECORD.read_bytes().replace(b"\r\n", b"\n")
        self.assertEqual(on_disk, fresh)

    def test_no_provider_or_network_import_in_the_tree(self) -> None:
        for path in sorted(ROOT.glob("*.py")):
            tree = ast.parse(path.read_bytes().decode("utf-8"))
            for node in ast.walk(tree):
                names: list[str] = []
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    names = [node.module]
                for name in names:
                    self.assertNotIn(
                        name.split(".")[0], OFFLINE_REFUSED, f"{path.name}: {name}"
                    )


if __name__ == "__main__":
    unittest.main()
