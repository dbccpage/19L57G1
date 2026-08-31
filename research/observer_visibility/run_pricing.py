"""Write receipts/pricing.json."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

import pricing
from run_decide import assert_inside_tree

HERE = Path(__file__).resolve().parent


def render() -> bytes:
    return (
        json.dumps(pricing.report(), indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    ).encode("ascii")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(HERE / "receipts"))
    args = parser.parse_args(argv)
    try:
        out = assert_inside_tree(Path(args.out).resolve())
        out.mkdir(parents=True, exist_ok=True)
        (out / "pricing.json").write_bytes(render())
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    r = pricing.report()
    for key in ("Z2", "Z3", "Z4"):
        block = r[key]
        assert isinstance(block, dict)
        print(key, "zero_count", block["zero_count"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
