"""Adversarial tests for the rung-local coverage gate."""

from __future__ import annotations

import datetime as dt
import json
import pathlib
import tempfile
import unittest
from unittest import mock

import check_coverage as gate


class CoverageGateTests(unittest.TestCase):
    def fixture(self) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path]:
        temp = tempfile.TemporaryDirectory()
        root = pathlib.Path(temp.name)
        for name in set(gate.MEASURED) | set(gate.EXCLUDED):
            (root / name).write_text("pass\n", encoding="utf-8")
        (root / "pyproject.toml").write_text(
            "[tool.coverage.run]\n"
            "branch = true\n"
            f"include = {json.dumps(list(gate.MEASURED))}\n",
            encoding="utf-8",
        )
        return temp, root

    @staticmethod
    def report() -> dict[str, object]:
        summary = {
            "num_statements": 100,
            "missing_lines": 0,
            "num_branches": 100,
            "num_partial_branches": 0,
            "missing_branches": 0,
        }
        return {
            "meta": {
                "timestamp": (
                    dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=1)
                ).isoformat()
            },
            "files": {name: {"summary": dict(summary)} for name in gate.MEASURED},
        }

    def check(self, root: pathlib.Path, payload: dict[str, object]) -> list[str]:
        report = root / "coverage.json"
        report.write_text(json.dumps(payload), encoding="utf-8")
        with mock.patch.multiple(
            gate,
            HERE=root,
            REPORT=report,
            CONFIG=root / "pyproject.toml",
        ):
            return gate.check()

    def test_unlisted_production_module_fails_closed(self) -> None:
        temp, root = self.fixture()
        with temp:
            (root / "unlisted.py").write_text("pass\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "production module census"):
                self.check(root, self.report())

    def test_nested_path_cannot_hide_behind_a_known_basename(self) -> None:
        temp, root = self.fixture()
        with temp:
            payload = self.report()
            files = payload["files"]
            assert isinstance(files, dict)
            files["nested/nofirst.py"] = files["nofirst.py"]
            with self.assertRaisesRegex(ValueError, "nested/nofirst.py"):
                self.check(root, payload)

    def test_impossible_counters_are_rejected(self) -> None:
        temp, root = self.fixture()
        with temp:
            payload = self.report()
            files = payload["files"]
            assert isinstance(files, dict)
            item = files["nofirst.py"]
            assert isinstance(item, dict)
            summary = item["summary"]
            assert isinstance(summary, dict)
            summary["missing_lines"] = 101
            with self.assertRaisesRegex(ValueError, "more missing lines"):
                self.check(root, payload)

    def test_combined_percentage_cannot_rescue_low_line_coverage(self) -> None:
        temp, root = self.fixture()
        with temp:
            payload = self.report()
            files = payload["files"]
            assert isinstance(files, dict)
            for item in files.values():
                assert isinstance(item, dict)
                summary = item["summary"]
                assert isinstance(summary, dict)
                summary["missing_lines"] = 6
                summary["percent_covered"] = 99.0
            with self.assertRaisesRegex(ValueError, "line coverage .* below"):
                self.check(root, payload)


if __name__ == "__main__":
    unittest.main()
