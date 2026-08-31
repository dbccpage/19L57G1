"""Write receipts/budget_meter.json deterministically (``--out DIR``)."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

import budget_meter

HERE = Path(__file__).resolve().parent


def render(report: dict[str, object]) -> bytes:
    return (
        json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    ).encode("ascii")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(HERE / "receipts"))
    args = parser.parse_args(argv)
    out = Path(args.out).resolve()
    if not out.is_relative_to(HERE):
        print(f"refusing to write outside research/natural_sections/: {out}", file=sys.stderr)
        return 1
    out.mkdir(parents=True, exist_ok=True)
    r = budget_meter.report()
    (out / "budget_meter.json").write_bytes(render(r))
    print("decider all within budget:", r["decider_all_within_budget"])
    print("decider all verdicts match:", r["decider_all_verdicts_match"])
    meter_rows = r["sum_meter_square"]
    assert isinstance(meter_rows, list)
    for row in meter_rows:
        print(
            f"sum meter len {row['max_len']}: {row['closed_walks']} walks,"
            f" {row['steps']} steps, within linear budget: {row['within_budget']}"
        )
    print("growth factors:", r["sum_meter_growth_factors"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
