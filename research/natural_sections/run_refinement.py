"""Write receipts/refinement.json deterministically (``--out DIR``)."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

import refinement

HERE = Path(__file__).resolve().parent


def render() -> bytes:
    return (
        json.dumps(refinement.report(), indent=2, sort_keys=True, ensure_ascii=True) + "\n"
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
    (out / "refinement.json").write_bytes(render())
    r = refinement.report()
    body = r["rounds"]
    assert isinstance(body, dict)
    for name, rs in sorted(body.items()):
        for row in rs:
            print(
                f"{name} round {row['round']}: objects {row['objects']}, hops {row['hops']},"
                f" odd {row['odd_generators']}, section {row['section_exists']}"
            )
    print("verdicts invariant:", r["verdict_invariant_across_rounds"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
