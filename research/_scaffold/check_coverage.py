"""CANONICAL research-tree coverage gate — copy this into a new tree.

Independent 95% statement and branch gate over one research tree's Python.
When you start a new `research/<tree>/`, copy this file verbatim and edit ONLY
`REQUIRED_FILES` (the tree's own production modules).  Do NOT copy an older
tree's `check_coverage.py`: earlier copies matched omit directories with a
substring test (`part in path`, marked by `OMIT_PARTS`) and false-flagged a
module under a directory like `clean/` as a COVERAGE_LEAK.  This version matches
omit directories as PATH COMPONENTS (`OMIT_DIRS` + `_directories`) and computes
each percentage through a single numeric path (`_totals`/`_number`, rejecting
bool once).  `research/_scaffold/check_scaffold.py` fails if the old substring
form reappears anywhere.

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
# Directory names whose measured files are not this tree's own Python.  Matched
# as PATH COMPONENTS, not substrings: a file under a directory like ``clean/``
# or ``subtests/`` must not be mistaken for ``lean/``/``tests/``.
OMIT_DIRS = frozenset({"tests", "lean", ".lake"})
# EDIT THIS for a new tree: the tree's own production modules (including this
# file), each a bare basename measured under coverage.
REQUIRED_FILES: tuple[str, ...] = (
    "REPLACE_ME.py",
    "check_coverage.py",
)


def _basename(path: str) -> str:
    return path.replace("\\", "/").rsplit("/", 1)[-1]


def _directories(path: str) -> set[str]:
    """The directory components of ``path`` (its basename excluded)."""
    return set(path.replace("\\", "/").split("/")[:-1])


def _number(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("numeric coverage total required")
    return float(value)


def _totals(totals: Mapping[str, object]) -> tuple[float, float, float, float]:
    """The four coverage totals as floats.  The single numeric-extraction path;
    rejects bool and non-numeric so every caller agrees on what is valid."""
    return (
        _number(totals["covered_lines"]),
        _number(totals["num_statements"]),
        _number(totals["covered_branches"]),
        _number(totals["num_branches"]),
    )


def percentages(totals: Mapping[str, object]) -> tuple[float, float]:
    covered_lines, num_statements, covered_branches, num_branches = _totals(totals)
    return (
        100.0 * covered_lines / num_statements,
        100.0 * covered_branches / num_branches,
    )


def evaluate(payload: object) -> tuple[list[str], float | None, float | None]:
    """Named failures plus the computed percentages.

    Returns ``(errors, statement, branch)``; the percentages are ``None``
    whenever evaluation stopped before computing them, and the two enforced
    values when ``errors`` is empty.
    """
    if not isinstance(payload, dict):
        return (["COVERAGE_SHAPE: not an object"], None, None)
    totals = payload.get("totals")
    if not isinstance(totals, dict):
        return (["COVERAGE_TOTALS: missing"], None, None)
    files = payload.get("files")
    if not isinstance(files, dict) or not files:
        return (["COVERAGE_FILES: missing"], None, None)
    errors: list[str] = []
    measured = [_basename(path) for path in files]
    leaked = [path for path in files if _directories(path) & OMIT_DIRS]
    if leaked:
        errors.append("COVERAGE_LEAK: " + ", ".join(leaked[:5]))
    missing = sorted(set(REQUIRED_FILES) - set(measured))
    if missing:
        errors.append(f"COVERAGE_POPULATION: missing {missing}")
    try:
        covered_lines, num_statements, covered_branches, num_branches = _totals(totals)
    except (KeyError, TypeError, ValueError):
        errors.append("COVERAGE_TOTALS: covered_lines/num_statements/covered_branches/num_branches required")
        return (errors, None, None)
    if num_statements <= 0:
        errors.append("COVERAGE_TOTALS: no statements")
        return (errors, None, None)
    if num_branches <= 0:
        errors.append("COVERAGE_TOTALS: no branches; branch measurement is required")
        return (errors, None, None)
    statement = 100.0 * covered_lines / num_statements
    branch = 100.0 * covered_branches / num_branches
    if statement < THRESHOLD:
        errors.append(f"COVERAGE_STATEMENT: {statement:.2f}% (need {THRESHOLD:.0f}%)")
    if branch < THRESHOLD:
        errors.append(f"COVERAGE_BRANCH: {branch:.2f}% (need {THRESHOLD:.0f}%)")
    return (errors, statement, branch)


def report_errors(payload: object) -> list[str]:
    """Named failures of one coverage.json object.  Empty list is a pass."""
    return evaluate(payload)[0]


def main() -> int:
    if not REPORT.is_file():
        print("FAIL: coverage.json is missing; run the tests step under coverage first")
        return 1
    try:
        payload: object = json.loads(REPORT.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"FAIL: coverage.json unreadable: {exc}")
        return 1
    errors, statement, branch = evaluate(payload)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    assert statement is not None and branch is not None
    print(f"PASS: coverage statement {statement:.2f}% branch {branch:.2f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
