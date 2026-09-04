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
            "covered_lines": 100,
            "num_statements": 100,
            "missing_lines": 0,
            "num_branches": 100,
            "num_partial_branches": 0,
            "covered_branches": 100,
            "missing_branches": 0,
        }
        return {
            "meta": {
                "branch_coverage": True,
                "timestamp": (
                    dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=1)
                ).isoformat()
            },
            "files": {name: {"summary": dict(summary)} for name in gate.MEASURED},
            "totals": {
                "num_statements": 300,
                "missing_lines": 0,
                "covered_lines": 300,
                "num_branches": 300,
                "num_partial_branches": 0,
                "missing_branches": 0,
                "covered_branches": 300,
            },
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

    def test_branch_measurement_metadata_is_required_true(self) -> None:
        temp, root = self.fixture()
        with temp:
            for value in (None, False, "true", 1):
                with self.subTest(value=value):
                    payload = self.report()
                    meta = payload["meta"]
                    assert isinstance(meta, dict)
                    if value is None:
                        del meta["branch_coverage"]
                    else:
                        meta["branch_coverage"] = value
                    with self.assertRaisesRegex(ValueError, "branch coverage enabled"):
                        self.check(root, payload)

    def test_every_branch_counter_is_required(self) -> None:
        temp, root = self.fixture()
        with temp:
            for key in (
                "num_branches",
                "num_partial_branches",
                "missing_branches",
                "covered_branches",
            ):
                with self.subTest(key=key):
                    payload = self.report()
                    files = payload["files"]
                    assert isinstance(files, dict)
                    item = files["nofirst.py"]
                    assert isinstance(item, dict)
                    summary = item["summary"]
                    assert isinstance(summary, dict)
                    del summary[key]
                    with self.assertRaisesRegex(ValueError, f"missing {key}"):
                        self.check(root, payload)

    def test_every_line_counter_is_required(self) -> None:
        temp, root = self.fixture()
        with temp:
            for key in ("num_statements", "missing_lines", "covered_lines"):
                with self.subTest(key=key):
                    payload = self.report()
                    files = payload["files"]
                    assert isinstance(files, dict)
                    item = files["nofirst.py"]
                    assert isinstance(item, dict)
                    summary = item["summary"]
                    assert isinstance(summary, dict)
                    del summary[key]
                    with self.assertRaisesRegex(ValueError, f"missing {key}"):
                        self.check(root, payload)

    def test_zero_branch_population_is_not_perfect_coverage(self) -> None:
        temp, root = self.fixture()
        with temp:
            payload = self.report()
            files = payload["files"]
            assert isinstance(files, dict)
            for item in files.values():
                assert isinstance(item, dict)
                summary = item["summary"]
                assert isinstance(summary, dict)
                summary["num_branches"] = 0
                summary["num_partial_branches"] = 0
                summary["covered_branches"] = 0
                summary["missing_branches"] = 0
            with self.assertRaisesRegex(ValueError, "zero branch population"):
                self.check(root, payload)

    def test_partial_branches_cannot_exceed_missing_branches(self) -> None:
        temp, root = self.fixture()
        with temp:
            payload = self.report()
            files = payload["files"]
            assert isinstance(files, dict)
            item = files["nofirst.py"]
            assert isinstance(item, dict)
            summary = item["summary"]
            assert isinstance(summary, dict)
            summary["num_partial_branches"] = 1
            summary["missing_branches"] = 0
            with self.assertRaisesRegex(ValueError, "impossible branch counters"):
                self.check(root, payload)

    def test_zero_statement_population_is_not_perfect_coverage(self) -> None:
        temp, root = self.fixture()
        with temp:
            payload = self.report()
            files = payload["files"]
            assert isinstance(files, dict)
            for item in files.values():
                assert isinstance(item, dict)
                summary = item["summary"]
                assert isinstance(summary, dict)
                summary["num_statements"] = 0
                summary["covered_lines"] = 0
                summary["missing_lines"] = 0
            with self.assertRaisesRegex(ValueError, "zero statement population"):
                self.check(root, payload)

    def test_covered_counter_equations_are_enforced(self) -> None:
        temp, root = self.fixture()
        with temp:
            for key, message in (
                ("covered_lines", "covered-line"),
                ("covered_branches", "covered-branch"),
            ):
                with self.subTest(key=key):
                    payload = self.report()
                    files = payload["files"]
                    assert isinstance(files, dict)
                    item = files["nofirst.py"]
                    assert isinstance(item, dict)
                    summary = item["summary"]
                    assert isinstance(summary, dict)
                    summary[key] = 99
                    with self.assertRaisesRegex(ValueError, message):
                        self.check(root, payload)

    def test_emitted_totals_must_equal_file_sums(self) -> None:
        temp, root = self.fixture()
        with temp:
            payload = self.report()
            totals = payload["totals"]
            assert isinstance(totals, dict)
            totals["covered_lines"] = 299
            with self.assertRaisesRegex(ValueError, "totals disagree for covered_lines"):
                self.check(root, payload)

    def test_top_level_totals_are_required(self) -> None:
        temp, root = self.fixture()
        with temp:
            payload = self.report()
            del payload["totals"]
            with self.assertRaisesRegex(ValueError, "no totals object"):
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
                summary["covered_lines"] = 94
                summary["percent_covered"] = 99.0
            totals = payload["totals"]
            assert isinstance(totals, dict)
            totals["missing_lines"] = 18
            totals["covered_lines"] = 282
            with self.assertRaisesRegex(ValueError, "line coverage .* below"):
                self.check(root, payload)


if __name__ == "__main__":
    unittest.main()
