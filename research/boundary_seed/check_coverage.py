"""The tree's own dual 95% gate.

Reads ``coverage.json`` produced from inside the tree; fails by name on a
missing or stale report, a file set that is not the tree's code, or either
measure under the bar.  Line and branch percentages are computed from their
separate counters: Coverage.py's ``percent_covered`` mixes the two whenever
branch measurement is enabled and is therefore not either gate.
"""

from __future__ import annotations

import datetime
import json
import pathlib
import sys
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
BAR = 95.0


def _count(row: dict[str, Any], key: str) -> int:
    value = row.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"coverage.json: {key} is not a count: {value!r}")
    return value


def percentages(totals: dict[str, Any]) -> tuple[float, float]:
    """Return the independent statement and branch percentages."""

    statements = _count(totals, "num_statements")
    covered_lines = _count(totals, "covered_lines")
    branches = _count(totals, "num_branches")
    covered_branches = _count(totals, "covered_branches")
    if statements <= 0:
        raise ValueError("coverage.json reports no statements")
    if branches <= 0:
        raise ValueError("coverage.json reports no branch data")
    if not 0 <= covered_lines <= statements:
        raise ValueError("coverage.json carries impossible line counters")
    if not 0 <= covered_branches <= branches:
        raise ValueError("coverage.json carries impossible branch counters")
    return (
        100.0 * covered_lines / statements,
        100.0 * covered_branches / branches,
    )


def main() -> int:
    report = HERE / "coverage.json"
    if not report.exists():
        print("FAIL: coverage.json missing; run coverage from inside the tree first")
        return 1
    try:
        payload: object = json.loads(report.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read coverage.json: {exc}")
        return 1
    if not isinstance(payload, dict):
        print("FAIL: coverage.json must contain an object")
        return 1
    data: dict[str, Any] = payload
    files = data.get("files")
    if not isinstance(files, dict):
        print("FAIL: coverage.json must carry a files object")
        return 1
    expected = sorted(
        str(p.relative_to(HERE)).replace("\\", "/")
        for p in (HERE / "code" / "boundary").rglob("*.py")
    )
    measured = sorted(str(k).replace("\\", "/") for k in files)
    if measured != expected:
        print(f"FAIL: measured files {measured} differ from tree code {expected}")
        return 1

    meta = data.get("meta")
    stamped = meta.get("timestamp") if isinstance(meta, dict) else None
    if not isinstance(stamped, str) or not stamped:
        print("FAIL: coverage.json carries no meta.timestamp; its age is unknown")
        return 1
    try:
        written = datetime.datetime.fromisoformat(stamped)
    except ValueError as exc:
        print(f"FAIL: coverage.json carries an invalid timestamp: {exc}")
        return 1
    newer = [
        path
        for path in sorted((HERE / "code" / "boundary").rglob("*.py"))
        if datetime.datetime.fromtimestamp(path.stat().st_mtime) > written
    ]
    if newer:
        print(
            "FAIL: coverage.json predates measured source files: "
            + ", ".join(str(path.relative_to(HERE)) for path in newer[:5])
        )
        return 1

    totals = data.get("totals")
    if not isinstance(totals, dict):
        print("FAIL: coverage.json must carry a totals object")
        return 1
    try:
        line, branch = percentages(totals)
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1
    print(f"line {line:.2f}% branch {branch:.2f}% over {len(measured)} files")
    if line < BAR or branch < BAR:
        print(f"FAIL: coverage under {BAR:.0f}% (line {line:.2f}, branch {branch:.2f})")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
