"""The tree's own dual 95% gate.  Reads coverage.json produced from inside
the tree; fails by name on a missing report, a file set that is not the
tree's code, or either measure under the bar."""

from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
BAR = 95.0


def main() -> int:
    report = HERE / "coverage.json"
    if not report.exists():
        print("FAIL: coverage.json missing; run coverage from inside the tree first")
        return 1
    data = json.loads(report.read_text(encoding="utf-8"))
    expected = sorted(
        str(p.relative_to(HERE)).replace("\\", "/")
        for p in (HERE / "code" / "boundary").glob("*.py")
    )
    measured = sorted(k.replace("\\", "/") for k in data["files"])
    if measured != expected:
        print(f"FAIL: measured files {measured} differ from tree code {expected}")
        return 1
    totals = data["totals"]
    line = float(totals["percent_covered"])
    branch_total = int(totals.get("num_branches", 0))
    branch_hit = int(totals.get("covered_branches", 0))
    if branch_total == 0:
        print("FAIL: no branch data; run coverage with branch measurement")
        return 1
    branch = 100.0 * branch_hit / branch_total
    print(f"line {line:.2f}% branch {branch:.2f}% over {len(measured)} files")
    if line < BAR or branch < BAR:
        print(f"FAIL: coverage under {BAR:.0f}% (line {line:.2f}, branch {branch:.2f})")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
