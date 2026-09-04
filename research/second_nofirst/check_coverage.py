"""The dual ninety-five percent coverage gate, measured from inside this rung.

Reads ``coverage.json`` written from this directory and requires line AND
branch coverage each to reach ninety-five percent over this rung's
MEASURED SET, failing by name on anything short.

The measured set is declared here rather than inferred, and the two
exclusions are declared with their reasons:

* ``check_coverage.py`` itself is excluded because the meter must not
  measure itself; the root repository keeps ``ci/check_coverage.py``
  outside ``code/`` for the same reason;
* ``verify_lean.py`` is excluded because exercising it requires elan and a
  Lake build; it runs in the separate Lean job, and counting it in the
  Python job would let an unexercised file be excused by a threshold rather
  than named.

Everything else in this rung is measured: the computation, the runner, and
the pin verifier.  A file appearing in the report that is not in the
declared set fails, and a declared file missing from the report fails, so
the set cannot drift silently in either direction.

Like the root gate, this refuses a report it cannot date: if any measured
source has been modified since the report's timestamp, the report is
stale and the gate fails rather than passing on old numbers.

Exit 0 on success, 1 with a named failure otherwise.  AuthorityEffect: None.
"""

from __future__ import annotations

import json
import pathlib
import sys
import tomllib
from typing import Any

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
REPORT = HERE / "coverage.json"
CONFIG = HERE / "pyproject.toml"

MEASURED = ("nofirst.py", "run_nofirst.py", "verify_pins.py")
EXCLUDED = {
    "check_coverage.py": "the meter must not measure itself",
    "verify_lean.py": "needs elan and a Lake build; run in the separate Lean job",
}
FLOOR = 95.0


def _load() -> dict[str, Any]:
    if not REPORT.exists():
        raise ValueError(
            f"{REPORT.name} is missing; generate it from this directory with"
            " `python -m coverage run -m unittest discover -s . -p \"test_*.py\"`"
            " then `python -m coverage json -q`"
        )
    payload: object = json.loads(REPORT.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("coverage.json must be an object")
    return payload


def _rel(raw: str) -> str:
    path = pathlib.Path(raw)
    if path.is_absolute():
        try:
            return path.resolve().relative_to(HERE.resolve()).as_posix()
        except ValueError as exc:
            raise ValueError(f"coverage report path is outside the rung: {raw}") from exc
    return pathlib.PurePosixPath(raw.replace("\\", "/")).as_posix()


def _production_sources() -> set[str]:
    found: set[str] = set()
    for path in HERE.rglob("*.py"):
        relative = path.relative_to(HERE)
        if path.name.startswith("test_"):
            continue
        if any(part in {".git", ".lake", "__pycache__"} for part in relative.parts):
            continue
        found.add(relative.as_posix())
    return found


def _configured_measured() -> set[str]:
    payload = tomllib.loads(CONFIG.read_text(encoding="utf-8"))
    try:
        raw = payload["tool"]["coverage"]["run"]["include"]
    except (KeyError, TypeError) as exc:
        raise ValueError("pyproject.toml has no coverage include list") from exc
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        raise ValueError("pyproject.toml coverage include must be a list of paths")
    return {_rel(item) for item in raw}


def _counter(summary: dict[str, Any], key: str) -> int:
    if key not in summary:
        raise ValueError(f"coverage summary is missing {key}")
    value = summary[key]
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"coverage summary {key} must be a non-negative integer")
    return int(value)


def check() -> list[str]:
    payload = _load()
    expected = set(MEASURED) | set(EXCLUDED)
    discovered = _production_sources()
    if discovered != expected:
        raise ValueError(
            "production module census differs:"
            f" missing from declarations={sorted(discovered - expected)},"
            f" declared but absent={sorted(expected - discovered)}"
        )
    configured = _configured_measured()
    if configured != set(MEASURED):
        raise ValueError(
            "pyproject coverage include differs from MEASURED:"
            f" configured={sorted(configured)}, expected={sorted(MEASURED)}"
        )
    files = payload.get("files")
    if not isinstance(files, dict) or not files:
        raise ValueError("coverage.json lists no measured file")

    reported: dict[str, Any] = {}
    for raw, value in files.items():
        if not isinstance(raw, str):
            raise ValueError("coverage report file names must be strings")
        relative = _rel(raw)
        if relative in reported:
            raise ValueError(f"coverage report repeats normalized path {relative}")
        reported[relative] = value
    for name in MEASURED:
        if name not in reported:
            raise ValueError(
                f"{name} is declared measured but is absent from the report"
            )
    for name in sorted(reported):
        if name not in MEASURED and name not in EXCLUDED:
            raise ValueError(
                f"{name} is in the report but is neither declared measured"
                " nor declared excluded"
            )

    meta = payload.get("meta")
    if not isinstance(meta, dict):
        raise ValueError("coverage.json carries no meta block")
    if meta.get("branch_coverage") is not True:
        raise ValueError("coverage.json was not measured with branch coverage enabled")
    stamp = meta.get("timestamp")
    if not isinstance(stamp, str):
        raise ValueError("coverage.json carries no meta.timestamp")
    from datetime import datetime

    when = datetime.fromisoformat(stamp).timestamp()
    for name in MEASURED:
        source = HERE / name
        if source.stat().st_mtime > when + 1:
            raise ValueError(
                f"{name} was modified after the report was written"
                f" ({stamp}); regenerate coverage.json"
            )

    lines: list[str] = []
    failures: list[str] = []
    covered_lines = 0
    total_lines = 0
    covered_branches = 0
    total_branches = 0
    total_partial_branches = 0
    for name in MEASURED:
        report = reported[name]
        if not isinstance(report, dict):
            raise ValueError(f"{name} has no file object in the report")
        summary = report.get("summary")
        if not isinstance(summary, dict):
            raise ValueError(f"{name} has no summary in the report")
        stmts = _counter(summary, "num_statements")
        missing = _counter(summary, "missing_lines")
        reported_covered_lines = _counter(summary, "covered_lines")
        branches = _counter(summary, "num_branches")
        partial = _counter(summary, "num_partial_branches")
        missing_branches = _counter(summary, "missing_branches")
        reported_covered_branches = _counter(summary, "covered_branches")
        if missing > stmts:
            raise ValueError(f"{name} has more missing lines than statements")
        if (
            missing_branches > branches
            or partial > branches
            or partial > missing_branches
        ):
            raise ValueError(f"{name} has impossible branch counters")
        if reported_covered_lines != stmts - missing:
            raise ValueError(f"{name} has inconsistent covered-line counters")
        if reported_covered_branches != branches - missing_branches:
            raise ValueError(f"{name} has inconsistent covered-branch counters")
        covered_lines += stmts - missing
        total_lines += stmts
        covered_branches += branches - missing_branches
        total_branches += branches
        total_partial_branches += partial
        line_pct = 100.0 if not stmts else 100.0 * (stmts - missing) / stmts
        branch_pct = 100.0 * (branches - missing_branches) / branches if branches else 0.0
        lines.append(
            f"{name}: line {line_pct:.2f}% ({stmts - missing}/{stmts}),"
            f" branch {branch_pct:.2f}% ({branches - missing_branches}/{branches}),"
            f" partial {partial}"
        )

    if not total_lines:
        raise ValueError("coverage report has a zero statement population")
    line_total = 100.0 * covered_lines / total_lines
    if not total_branches:
        raise ValueError("coverage report has a zero branch population")
    branch_total = 100.0 * covered_branches / total_branches
    totals = payload.get("totals")
    if not isinstance(totals, dict):
        raise ValueError("coverage.json carries no totals object")
    expected_totals = {
        "num_statements": total_lines,
        "missing_lines": total_lines - covered_lines,
        "covered_lines": covered_lines,
        "num_branches": total_branches,
        "num_partial_branches": total_partial_branches,
        "missing_branches": total_branches - covered_branches,
        "covered_branches": covered_branches,
    }
    for key, expected_value in expected_totals.items():
        if _counter(totals, key) != expected_value:
            raise ValueError(f"coverage totals disagree for {key}")
    lines.append(
        f"measured set: line {line_total:.2f}%"
        f" ({covered_lines}/{total_lines}),"
        f" branch {branch_total:.2f}% ({covered_branches}/{total_branches})"
    )
    for name, reason in sorted(EXCLUDED.items()):
        lines.append(f"excluded: {name} -- {reason}")

    if line_total < FLOOR:
        failures.append(f"line coverage {line_total:.2f}% is below {FLOOR:.0f}%")
    if branch_total < FLOOR:
        failures.append(f"branch coverage {branch_total:.2f}% is below {FLOOR:.0f}%")
    if failures:
        raise ValueError("; ".join(failures))
    return lines


def main() -> int:
    try:
        lines = check()
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1
    except (KeyError, TypeError, OverflowError) as exc:  # pragma: no cover
        print(f"FAIL: malformed coverage report: {exc}")
        return 1
    for line in lines:
        print(line)
    print(f"coverage clean: both thresholds at or above {FLOOR:.0f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
