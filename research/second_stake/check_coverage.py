"""Independent line and branch threshold for the rung-local Python source."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
from typing import cast

HERE = pathlib.Path(__file__).resolve().parent

JsonObject = dict[str, object]
COUNTERS = (
    "covered_lines",
    "missing_lines",
    "num_statements",
    "covered_branches",
    "missing_branches",
    "num_branches",
    "num_partial_branches",
)


def percentage(covered: int, total: int) -> float:
    if total <= 0:
        raise ValueError("coverage population must be positive")
    return 100.0 * covered / total


def load_report(path: pathlib.Path) -> JsonObject:
    value: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("coverage report must be an object")
    return cast(JsonObject, value)


def production_sources() -> frozenset[str]:
    """Derive the rung-local production population independently of coverage."""

    return frozenset(
        path.name
        for path in HERE.glob("*.py")
        if path.name != "check_coverage.py" and not path.name.startswith("test_")
    )


def normalized_report_path(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("coverage path must be a nonempty string")
    if "\\" in value:
        raise ValueError(f"coverage path is not normalized relative POSIX: {value}")
    pure = pathlib.PurePosixPath(value)
    if (
        pure.is_absolute()
        or pathlib.PureWindowsPath(value).is_absolute()
        or any(part in {".", ".."} for part in pure.parts)
        or pure.as_posix() != value
    ):
        raise ValueError(f"coverage path is not normalized relative POSIX: {value}")
    return value


def counters(value: object, location: str) -> dict[str, int]:
    if not isinstance(value, dict):
        raise ValueError(f"{location} is not an object")
    result: dict[str, int] = {}
    for name in COUNTERS:
        item = value.get(name)
        if type(item) is not int or item < 0:
            raise ValueError(f"{location}.{name} must be a nonnegative integer")
        result[name] = item
    if result["covered_lines"] + result["missing_lines"] != result["num_statements"]:
        raise ValueError(f"{location} line counters do not add up")
    if (
        result["covered_branches"] + result["missing_branches"]
        != result["num_branches"]
    ):
        raise ValueError(f"{location} branch counters do not add up")
    if result["num_partial_branches"] > result["missing_branches"]:
        raise ValueError(f"{location} partial branches exceed missing branches")
    return result


def report_epoch(meta: object) -> float:
    if not isinstance(meta, dict):
        raise ValueError("coverage report lacks metadata")
    if meta.get("branch_coverage") is not True:
        raise ValueError("coverage metadata branch_coverage must be true")
    timestamp = meta.get("timestamp")
    if not isinstance(timestamp, str):
        raise ValueError("coverage metadata timestamp is missing")
    try:
        parsed = dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("coverage metadata timestamp is invalid") from exc
    return parsed.timestamp()


def check(path: pathlib.Path, threshold: float = 95.0) -> list[str]:
    if not path.is_file():
        return [f"coverage report missing: {path.name}"]
    try:
        report = load_report(path)
        measured_at = report_epoch(report.get("meta"))
        files = report.get("files")
        totals = report.get("totals")
        if not isinstance(files, dict) or not isinstance(totals, dict):
            raise ValueError("coverage report lacks files or totals")
        measured_list = [normalized_report_path(name) for name in files]
        basenames: dict[str, str] = {}
        for name in measured_list:
            basename = pathlib.PurePosixPath(name).name
            previous = basenames.get(basename)
            if previous is not None and previous != name:
                raise ValueError(f"coverage path basename collision: {basename}")
            basenames[basename] = name
        measured = set(measured_list)
        sources = production_sources()
        failures: list[str] = []
        if measured != sources:
            failures.append(
                "coverage file set differs: "
                f"expected {sorted(sources)}, got {sorted(measured)}"
            )
            return failures
        file_counters: dict[str, dict[str, int]] = {}
        for name in sorted(sources):
            record = files[name]
            if not isinstance(record, dict):
                raise ValueError(f"coverage file record is not an object: {name}")
            summary = counters(record.get("summary"), f"coverage file {name}")
            if summary["num_statements"] == 0:
                raise ValueError(f"coverage file statement population is empty: {name}")
            if summary["num_branches"] == 0:
                raise ValueError(f"coverage file branch population is empty: {name}")
            file_counters[name] = summary
            source = HERE / name
            if measured_at < source.stat().st_mtime:
                failures.append(f"coverage report is stale for {name}")
        total_counters = counters(totals, "coverage totals")
        for name in COUNTERS:
            summed = sum(summary[name] for summary in file_counters.values())
            if total_counters[name] != summed:
                raise ValueError(f"coverage totals do not equal file counters: {name}")
        if total_counters["num_statements"] == 0:
            raise ValueError("coverage statement population is empty")
        if total_counters["num_branches"] == 0:
            raise ValueError("coverage branch population is empty")
        line = percentage(total_counters["covered_lines"], total_counters["num_statements"])
        branch = percentage(total_counters["covered_branches"], total_counters["num_branches"])
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
