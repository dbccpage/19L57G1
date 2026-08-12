"""Independent coverage gate: line and branch coverage must EACH reach
95% over project Python code (``coverage.json`` from ``coverage json``).
Lives outside ``code/`` so it is not itself part of the measured code."""

import json
import sys


def main() -> int:
    totals = json.load(open("coverage.json", encoding="utf-8"))["totals"]
    line = (
        totals["covered_lines"]
        / (totals["covered_lines"] + totals["missing_lines"])
        * 100.0
    )
    branch = totals["covered_branches"] / totals["num_branches"] * 100.0
    print(f"line coverage   {line:6.2f}%  (gate 95%)")
    print(f"branch coverage {branch:6.2f}%  (gate 95%)")
    return 0 if line >= 95.0 and branch >= 95.0 else 1


if __name__ == "__main__":
    sys.exit(main())
