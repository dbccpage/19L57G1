"""The rung's own coverage gate.  AuthorityEffect: None.

Usage, from inside this tree::

    python -m coverage run -m unittest discover -s . -p "test_*.py"
    python -m coverage json -q
    python check_coverage.py

``research/second/SEED.md`` requires line AND branch coverage of at least
ninety-five percent each, measured from inside the rung.  Rung zero left that
as an operator claim, and this rung shipped below both thresholds -- 90.40%
line and 85.55% branch -- with no step anywhere that would have said so.  A
threshold nothing measures is not a threshold.

Four checks, none implying the others, each modelled on ``ci/check_coverage.py``
and each failing BY NAME:

* line percent, computed as covered statements over total statements, is at
  least ninety-five;
* branch percent, computed as covered branches over total branches, is at
  least ninety-five -- ``coverage``'s own ``percent_covered`` mixes the two
  into one number and satisfying it does not satisfy these;
* the measured file set is exactly the tree's own non-test modules.  This is
  the check that catches the failure this gate was written after: a module
  named in ``[tool.coverage.run] source`` that no test imports is dropped
  from the report with a warning on stderr and no failure anywhere.  A
  dropped module reads as a smaller denominator, which makes the percentage
  go UP;
* no measured source has been modified since the report was written, so a
  stale report cannot certify a source it never saw.  It errs conservatively:
  touching a file without changing it fails until the report is regenerated,
  which is the safe direction.

This file lives outside the measured set on purpose: the gate does not
measure itself.  It reads ``coverage.json`` and writes nothing.

Classification: metatheory apparatus.  A pass says the suite executed that
much of this tree's own code.  It says nothing about whether the tests assert
anything worth asserting, and nothing at all about the mathematics.
"""

from __future__ import annotations

import json
import pathlib
import sys
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
REPORT = HERE / "coverage.json"

LINE_FLOOR = 95.0
BRANCH_FLOOR = 95.0
SKIP_PARTS = frozenset(
    {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "__pycache__",
        "tests",
    }
)


def _production_modules(here: pathlib.Path) -> tuple[str, ...]:
    """Recursively census production modules independently of coverage config."""

    modules: list[str] = []
    for path in here.rglob("*.py"):
        relative = path.relative_to(here)
        name = relative.as_posix()
        if name == "check_coverage.py" or path.name.startswith("test_"):
            continue
        if any(part in SKIP_PARTS for part in relative.parts[:-1]):
            continue
        modules.append(name)
    return tuple(sorted(modules))


# The report must contain every production module found above, neither more
# nor less.  A new unimported module omitted from pyproject's source list is
# therefore a missing report row rather than a smaller, greener denominator.
MEASURED = _production_modules(HERE)


def _read(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        raise ValueError(
            f"{path.name} is missing; run coverage and 'coverage json -q' first"
        )
    payload: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path.name} must be an object")
    return payload


def _num(row: dict[str, Any], key: str) -> int:
    value = row.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"coverage.json: {key} is not a count: {value!r}")
    return value


def _percent(covered: int, total: int, what: str) -> float:
    if total <= 0:
        raise ValueError(f"coverage.json reports no {what} at all")
    return 100.0 * covered / total


def check() -> list[str]:
    report = _read(REPORT)
    files = report.get("files")
    if not isinstance(files, dict):
        raise ValueError("coverage.json must carry a files object")
    measured = sorted(
        pathlib.PurePosixPath(name.replace("\\", "/")).as_posix() for name in files
    )
    if any(
        pathlib.PurePosixPath(name).is_absolute()
        or ".." in pathlib.PurePosixPath(name).parts
        for name in measured
    ):
        raise ValueError(f"coverage.json carries an unsafe measured path: {measured}")
    if len(measured) != len(set(measured)):
        raise ValueError(
            f"coverage.json carries duplicate normalized paths: {measured}"
        )
    if measured != sorted(MEASURED):
        raise ValueError(
            "measured file set differs from the tree's own modules: "
            f"measured {measured}, wanted {sorted(MEASURED)}"
        )

    meta = report.get("meta")
    if not isinstance(meta, dict):
        raise ValueError("coverage.json must carry a meta object")
    stamp = meta.get("timestamp")
    if not isinstance(stamp, str) or not stamp:
        raise ValueError("coverage.json carries no meta.timestamp to date it by")
    written = REPORT.stat().st_mtime
    stale = sorted(
        name
        for name in MEASURED
        if (HERE / name).exists() and (HERE / name).stat().st_mtime > written
    )
    if stale:
        raise ValueError(
            "a measured source is newer than the report; regenerate it: "
            + ", ".join(stale)
        )

    totals = report.get("totals")
    if not isinstance(totals, dict):
        raise ValueError("coverage.json must carry a totals object")
    line = _percent(
        _num(totals, "covered_lines"), _num(totals, "num_statements"), "statements"
    )
    branch = _percent(
        _num(totals, "covered_branches"), _num(totals, "num_branches"), "branches"
    )
    failures: list[str] = []
    if line < LINE_FLOOR:
        failures.append(f"line coverage {line:.2f}% is below {LINE_FLOOR:.0f}%")
    if branch < BRANCH_FLOOR:
        failures.append(f"branch coverage {branch:.2f}% is below {BRANCH_FLOOR:.0f}%")
    if failures:
        raise ValueError("; ".join(failures))

    return [
        f"measured: {', '.join(measured)} (dated {stamp})",
        f"line coverage {line:.2f}% of {_num(totals, 'num_statements')} statements",
        f"branch coverage {branch:.2f}% of {_num(totals, 'num_branches')} branches",
        f"second_stream coverage gate: both thresholds of {LINE_FLOOR:.0f}% met",
    ]


def main() -> int:
    try:
        lines = check()
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":  # pragma: no cover - the entry point, run by hand
    sys.exit(main())
