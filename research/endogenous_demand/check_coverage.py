"""Independent 95% line and branch gate over this tree's Python.

AuthorityEffect: None.  Reads ``coverage.json`` written by the tests step.
Does not measure sealed ``code/``.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "coverage.json"
THRESHOLD = 95.0
OMIT_PARTS = ("tests/", "lean/", ".lake/")
# Drivers are exercised by verify.py as subprocesses; coverage is of the
# computational modules (grammar, candidates, reader, this file).


def main() -> int:
    if not REPORT.is_file():
        print("FAIL: coverage.json is missing; run the tests step under coverage first")
        return 1
    payload = json.loads(REPORT.read_text(encoding="utf-8"))
    totals = payload.get("totals")
    if not isinstance(totals, dict):
        print("FAIL: coverage.json has no totals")
        return 1
    files = payload.get("files")
    if not isinstance(files, dict) or not files:
        print("FAIL: coverage.json has no files")
        return 1
    measured = [path.replace("\\", "/") for path in files]
    leaked = [path for path in measured if any(part in path for part in OMIT_PARTS)]
    if leaked:
        print("FAIL: coverage report includes omitted paths: " + ", ".join(leaked[:5]))
        return 1
    line = float(totals["percent_covered"])
    # coverage.py 7 stores branch coverage as percent_covered_display or
    # as covered_branches / num_branches.  Prefer the explicit branch percent.
    covered_b = float(totals.get("covered_branches", 0))
    num_b = float(totals.get("num_branches", 0))
    branch = (100.0 * covered_b / num_b) if num_b else 100.0
    if line < THRESHOLD or branch < THRESHOLD:
        print(f"FAIL: coverage line {line:.2f}% branch {branch:.2f}% (need {THRESHOLD:.0f}% each)")
        return 1
    print(f"PASS: coverage line {line:.2f}% branch {branch:.2f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
