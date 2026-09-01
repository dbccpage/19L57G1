"""Write receipts/layer_balance.json deterministically (``--out DIR``)."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

import layer_balance

HERE = Path(__file__).resolve().parent


def render(report: dict[str, object]) -> bytes:
    return (json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode(
        "ascii"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(HERE / "receipts"))
    args = parser.parse_args(argv)
    out = Path(args.out).resolve()
    if not out.is_relative_to(HERE):
        print(f"refusing to write outside research/natural_sections/: {out}", file=sys.stderr)
        return 1
    out.mkdir(parents=True, exist_ok=True)
    report = layer_balance.report()
    (out / "layer_balance.json").write_bytes(render(report))
    print(f"balance at part counts 1..12: {report['balance_1_12']}")
    print(
        f"agreement of the two computations to {report['bound']}:"
        f" {report['agreement_misses']} misses"
    )
    print(
        f"partition misses to {report['small_bound']}: {report['partition_misses']};"
        f" inversion misses: {report['inversion_misses']}"
    )
    print(f"running balance checkpoints: {report['running_balance_checkpoints']}")
    growth = report["growth"]
    assert isinstance(growth, dict)
    print(
        f"growth: max squared ratio {growth['max_squared_ratio_num']}"
        f"/{growth['max_squared_ratio_den']} at part count {growth['at_part_count']},"
        f" stays below the square root: {growth['stays_below_the_square_root']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
