"""Write receipts/dynamics_counts.json deterministically (``--out DIR``)."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

import dynamics_counts

HERE = Path(__file__).resolve().parent


def render() -> bytes:
    return (
        json.dumps(dynamics_counts.report(), indent=2, sort_keys=True, ensure_ascii=True) + "\n"
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
    (out / "dynamics_counts.json").write_bytes(render())
    r = dynamics_counts.report()
    print("counts identical:", r["counts_identical"])
    print("convention-read identical:", r["convention_read_identical"])
    print("square:", r["square"])
    print("cover:", r["cover"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
