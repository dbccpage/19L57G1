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
  Lake build, which the research job deliberately does not install; it is
  a manual receipt and says so, and counting it would let an unexercised
  file be excused by a threshold rather than named.

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
from typing import Any

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
REPORT = HERE / "coverage.json"

MEASURED = ("nofirst.py", "run_nofirst.py", "verify_pins.py")
EXCLUDED = {
    "check_coverage.py": "the meter must not measure itself",
    "verify_lean.py": "needs elan and a Lake build; a manual receipt by design",
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
    return pathlib.PurePath(raw.replace("\\", "/")).name


def check() -> list[str]:
    payload = _load()
    files = payload.get("files")
    if not isinstance(files, dict) or not files:
        raise ValueError("coverage.json lists no measured file")

    reported = {_rel(k): v for k, v in files.items()}
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
    for name in MEASURED:
        summary = reported[name].get("summary")
        if not isinstance(summary, dict):
            raise ValueError(f"{name} has no summary in the report")
        stmts = int(summary["num_statements"])
        missing = int(summary["missing_lines"])
        branches = int(summary.get("num_branches", 0))
        partial = int(summary.get("num_partial_branches", 0))
        missing_branches = int(summary.get("missing_branches", 0))
        covered_lines += stmts - missing
        total_lines += stmts
        covered_branches += branches - missing_branches
        total_branches += branches
        line_pct = 100.0 if not stmts else 100.0 * (stmts - missing) / stmts
        branch_pct = (
            100.0
            if not branches
            else 100.0 * (branches - missing_branches) / branches
        )
        lines.append(
            f"{name}: line {line_pct:.2f}% ({stmts - missing}/{stmts}),"
            f" branch {branch_pct:.2f}% ({branches - missing_branches}/{branches}),"
            f" partial {partial}"
        )

    line_total = 100.0 if not total_lines else 100.0 * covered_lines / total_lines
    branch_total = (
        100.0 if not total_branches else 100.0 * covered_branches / total_branches
    )
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
    except (KeyError, TypeError, ValueError) as exc:  # pragma: no cover
        print(f"FAIL: malformed coverage report: {exc}")
        return 1
    for line in lines:
        print(line)
    print(f"coverage clean: both thresholds at or above {FLOOR:.0f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
