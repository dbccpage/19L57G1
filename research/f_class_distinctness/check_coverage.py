"""Independent 95% statement and branch gate over this tree's Python.

AuthorityEffect: None.  Reads ``coverage.json`` written by the tests step.
Does not measure sealed ``code/``.

Statement coverage is ``covered_lines / num_statements``.  It is not
``percent_covered``, which combines statements and branches when branch
measurement is on.  The two thresholds are enforced separately.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "coverage.json"
THRESHOLD = 95.0
OMIT_PARTS = ("tests/", "lean/", ".lake/")
REQUIRED_FILES: tuple[str, ...] = (
    "classes.py",
    "check_coverage.py",
)


def _basename(path: str) -> str:
    return path.replace("\\", "/").rsplit("/", 1)[-1]


def report_errors(payload: object) -> list[str]:
    """Named failures of one coverage.json object.  Empty list is a pass."""
    if not isinstance(payload, dict):
        return ["COVERAGE_SHAPE: not an object"]
    totals = payload.get("totals")
    if not isinstance(totals, dict):
        return ["COVERAGE_TOTALS: missing"]
    files = payload.get("files")
    if not isinstance(files, dict) or not files:
        return ["COVERAGE_FILES: missing"]
    errors: list[str] = []
    measured = [_basename(path) for path in files]
    leaked = [path for path in files if any(part in path.replace("\\", "/") for part in OMIT_PARTS)]
    if leaked:
        errors.append("COVERAGE_LEAK: " + ", ".join(leaked[:5]))
    missing = sorted(set(REQUIRED_FILES) - set(measured))
    if missing:
        errors.append(f"COVERAGE_POPULATION: missing {missing}")
    try:
        covered_lines = float(totals["covered_lines"])
        num_statements = float(totals["num_statements"])
        covered_branches = float(totals["covered_branches"])
        num_branches = float(totals["num_branches"])
    except (KeyError, TypeError, ValueError):
        errors.append("COVERAGE_TOTALS: covered_lines/num_statements/covered_branches/num_branches required")
        return errors
    if num_statements <= 0:
        errors.append("COVERAGE_TOTALS: no statements")
        return errors
    if num_branches <= 0:
        errors.append("COVERAGE_TOTALS: no branches; branch measurement is required")
        return errors
    statement = 100.0 * covered_lines / num_statements
    branch = 100.0 * covered_branches / num_branches
    if statement < THRESHOLD:
        errors.append(
            f"COVERAGE_STATEMENT: {statement:.2f}% (need {THRESHOLD:.0f}%)"
        )
    if branch < THRESHOLD:
        errors.append(
            f"COVERAGE_BRANCH: {branch:.2f}% (need {THRESHOLD:.0f}%)"
        )
    return errors


def _number(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("numeric coverage total required")
    return float(value)


def percentages(totals: Mapping[str, object]) -> tuple[float, float]:
    covered_lines = _number(totals["covered_lines"])
    num_statements = _number(totals["num_statements"])
    covered_branches = _number(totals["covered_branches"])
    num_branches = _number(totals["num_branches"])
    return (
        100.0 * covered_lines / num_statements,
        100.0 * covered_branches / num_branches,
    )


def main() -> int:
    if not REPORT.is_file():
        print("FAIL: coverage.json is missing; run the tests step under coverage first")
        return 1
    try:
        payload: object = json.loads(REPORT.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"FAIL: coverage.json unreadable: {exc}")
        return 1
    errors = report_errors(payload)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    assert isinstance(payload, dict)
    totals = payload["totals"]
    assert isinstance(totals, dict)
    statement, branch = percentages(totals)
    print(f"PASS: coverage statement {statement:.2f}% branch {branch:.2f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
