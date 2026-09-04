"""Independent line and branch threshold for the rung-local Python source."""

from __future__ import annotations

import argparse
import json
import pathlib
from typing import cast

HERE = pathlib.Path(__file__).resolve().parent
SOURCES = frozenset(
    {
        "generation.py",
        "observables.py",
        "rules.py",
        "run_stake.py",
        "verify_pins.py",
    }
)

JsonObject = dict[str, object]


def percentage(covered: int, total: int) -> float:
    return 100.0 if total == 0 else 100.0 * covered / total


def load_report(path: pathlib.Path) -> JsonObject:
    value: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("coverage report must be an object")
    return cast(JsonObject, value)


def check(path: pathlib.Path, threshold: float = 95.0) -> list[str]:
    if not path.is_file():
        return [f"coverage report missing: {path.name}"]
    try:
        report = load_report(path)
        files = report.get("files")
        totals = report.get("totals")
        if not isinstance(files, dict) or not isinstance(totals, dict):
            raise ValueError("coverage report lacks files or totals")
        measured = {pathlib.PurePath(str(name)).name for name in files}
        failures: list[str] = []
        if measured != SOURCES:
            failures.append(
                "coverage file set differs: "
                f"expected {sorted(SOURCES)}, got {sorted(measured)}"
            )
        covered_lines = totals.get("covered_lines")
        statements = totals.get("num_statements")
        covered_branches = totals.get("covered_branches")
        branches = totals.get("num_branches")
        if not all(
            isinstance(value, int)
            for value in (covered_lines, statements, covered_branches, branches)
        ):
            raise ValueError("coverage totals are not integers")
        line = percentage(
            cast(int, covered_lines), cast(int, statements)
        )
        branch = percentage(
            cast(int, covered_branches), cast(int, branches)
        )
        if line < threshold:
            failures.append(f"line coverage {line:.2f}% is below {threshold:.2f}%")
        if branch < threshold:
            failures.append(f"branch coverage {branch:.2f}% is below {threshold:.2f}%")
        if not failures:
            print(f"line coverage: {line:.2f}%")
            print(f"branch coverage: {branch:.2f}%")
        return failures
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [str(exc)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=pathlib.Path, default=HERE / "coverage.json")
    parser.add_argument("--threshold", type=float, default=95.0)
    args = parser.parse_args()
    failures = check(args.report, args.threshold)
    for failure in failures:
        print(f"FAIL: {failure}")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
