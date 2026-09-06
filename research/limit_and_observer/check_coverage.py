"""The independent dual coverage gate for this tree.

Lives outside ``code/`` on purpose so it is not part of the measured source.
It reads ``coverage.json``, so generate that first, and it refuses to believe
a report it cannot date: a stale report is the failure mode that actually
happens, and only the timestamp check catches a branch switch that leaves the
file set identical.

AuthorityEffect: None.
"""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, "coverage.json")
THRESHOLD = 95.0


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def main() -> None:
    if not os.path.isfile(REPORT):
        fail("coverage.json is missing; run coverage first")
    with open(REPORT, encoding="utf-8") as fh:
        data = json.load(fh)

    measured = sorted(
        os.path.normpath(p) for p in data["files"]
    )
    expected = sorted(
        os.path.normpath(os.path.relpath(os.path.join(root, name), HERE))
        for root, _dirs, files in os.walk(os.path.join(HERE, "code"))
        for name in files
        if name.endswith(".py")
    )
    if not expected:
        fail("no measured source found; the gate would be vacuous")
    if measured != expected:
        fail(
            "the measured file set differs from code/**/*.py\n"
            f"  only measured: {sorted(set(measured) - set(expected))}\n"
            f"  only expected: {sorted(set(expected) - set(measured))}"
        )

    stamp = data.get("meta", {}).get("timestamp")
    if not stamp:
        fail("coverage.json carries no timestamp; refusing to date it")
    import datetime

    when = datetime.datetime.fromisoformat(stamp).timestamp()
    for rel in expected:
        full = os.path.join(HERE, rel)
        if os.path.getmtime(full) > when + 1:
            fail(
                f"{rel} was modified after the report was written; "
                "regenerate coverage"
            )

    totals = data["totals"]
    statements = totals.get("num_statements", 0)
    if statements == 0:
        fail("no statement data; refusing an empty line census")
    line = 100.0 * totals["covered_lines"] / statements
    covered_b = totals.get("covered_branches", 0)
    total_b = totals.get("num_branches", 0)
    if total_b == 0:
        fail("no branch data; run coverage with --branch")
    branch = 100.0 * covered_b / total_b

    problems = []
    if line < THRESHOLD:
        problems.append(f"line coverage {line:.2f}% is below {THRESHOLD}%")
    if branch < THRESHOLD:
        problems.append(f"branch coverage {branch:.2f}% is below {THRESHOLD}%")
    if problems:
        for name, f in sorted(data["files"].items()):
            s = f["summary"]
            ns = s.get("num_statements", 0)
            l = 100.0 * s.get("covered_lines", 0) / ns if ns else 100.0
            nb = s.get("num_branches", 0)
            b = 100.0 * s.get("covered_branches", 0) / nb if nb else 100.0
            if l < THRESHOLD or b < THRESHOLD:
                print(
                    f"  {name}: line {l:.1f}% "
                    f"branch {b:.1f}%"
                )
        fail("; ".join(problems))
    print(
        f"limit_and_observer coverage clean: line {line:.2f}%, "
        f"branch {branch:.2f}%, {len(expected)} measured sources"
    )


if __name__ == "__main__":
    main()
