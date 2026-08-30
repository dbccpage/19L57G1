"""Write receipts/weighted_sum.json deterministically (``--out DIR``)."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

import weighted_sum

HERE = Path(__file__).resolve().parent


def render() -> bytes:
    return (
        json.dumps(weighted_sum.report(), indent=2, sort_keys=True, ensure_ascii=True) + "\n"
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
    (out / "weighted_sum.json").write_bytes(render())
    for f in weighted_sum.fixtures():
        r = weighted_sum.analyse(*f)
        print(f"{r.name}: {r.walks} closed walks up to length {r.max_len}; total_unit {r.total_unit}, total_sign {r.total_sign}")
        for pair, v in sorted(r.pairs.items()):
            print(f"   pair {pair}: twisted_unit {v['twisted_unit']}, twisted_sign {v['twisted_sign']}, movers {v['movers']}")
    print("orbit counterexample:", weighted_sum.orbit_counterexample())
    print("every value:", weighted_sum.every_value([-3, -1, 0, 2, 7]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
