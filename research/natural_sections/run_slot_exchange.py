"""Write receipts/slot_exchange.json deterministically (``--out DIR``)."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

import slot_exchange

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
    report = slot_exchange.report()
    (out / "slot_exchange.json").write_bytes(render(report))
    chars = report["characters"]
    assert isinstance(chars, dict)
    print(f"rotation counts k=1..8: {chars['rotation_counts']}")
    print(f"swap counts k=1..8: {chars['swap_counts']}")
    odd = report["odd_families"]
    assert isinstance(odd, dict)
    print(
        f"odd families bound {odd['bound']}: {odd['count']},"
        f" all totals zero {odd['all_totals_zero']},"
        f" pairing misses {odd['pairing_misses']}"
    )
    disc = report["discard"]
    assert isinstance(disc, dict)
    print(
        f"discard countermodel: full {disc['full_total']},"
        f" discarded {disc['discarded_total']}, conflatable {disc['conflatable']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
