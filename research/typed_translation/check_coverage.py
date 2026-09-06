"""Fresh, exact-file-set, independent 95 percent line and branch gate."""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
BAR = 95.0


def measured_files() -> list[str]:
    return sorted(
        path.relative_to(HERE).as_posix()
        for path in (HERE / "code" / "typed_translation").rglob("*.py")
    )


def _count(row: dict[str, Any], key: str) -> int:
    value = row.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"coverage.json: {key} is not an integer count")
    return value


def percentages(totals: dict[str, Any]) -> tuple[float, float]:
    statements = _count(totals, "num_statements")
    covered_lines = _count(totals, "covered_lines")
    branches = _count(totals, "num_branches")
    covered_branches = _count(totals, "covered_branches")
    if statements <= 0 or branches <= 0:
        raise ValueError("coverage report has an empty line or branch denominator")
    if not 0 <= covered_lines <= statements or not 0 <= covered_branches <= branches:
        raise ValueError("coverage report carries impossible counters")
    return 100.0 * covered_lines / statements, 100.0 * covered_branches / branches


def main() -> int:
    path = HERE / "coverage.json"
    if not path.is_file():
        print("FAIL: coverage.json is missing")
        return 1
    try:
        raw: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read coverage.json: {exc}")
        return 1
    if not isinstance(raw, dict):
        print("FAIL: coverage.json is not an object")
        return 1
    files = raw.get("files")
    if not isinstance(files, dict):
        print("FAIL: coverage.json has no files object")
        return 1
    measured = sorted(str(name).replace("\\", "/") for name in files)
    expected = measured_files()
    if measured != expected:
        print(f"FAIL: measured files {measured} differ from tree code {expected}")
        return 1
    meta = raw.get("meta")
    timestamp = meta.get("timestamp") if isinstance(meta, dict) else None
    if not isinstance(timestamp, str):
        print("FAIL: coverage.json has no timestamp")
        return 1
    try:
        written = datetime.datetime.fromisoformat(timestamp)
    except ValueError as exc:
        print(f"FAIL: invalid coverage timestamp: {exc}")
        return 1
    stale = [
        name
        for name in expected
        if datetime.datetime.fromtimestamp((HERE / name).stat().st_mtime) > written
    ]
    if stale:
        print(f"FAIL: coverage predates measured source: {', '.join(stale)}")
        return 1
    totals = raw.get("totals")
    if not isinstance(totals, dict):
        print("FAIL: coverage.json has no totals object")
        return 1
    try:
        line, branch = percentages(totals)
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1
    print(f"line {line:.2f}% branch {branch:.2f}% over {len(measured)} files")
    if line < BAR or branch < BAR:
        print(f"FAIL: coverage under {BAR:.0f}%")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
