"""Write receipts/quotient_mass.json deterministically (``--out DIR``)."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

import quotient_mass

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
    report = quotient_mass.report()
    (out / "quotient_mass.json").write_bytes(render(report))
    surveys = report["surveys"]
    assert isinstance(surveys, list)
    for row in surveys:
        print(
            f"N={row['modulus']}: classes {row['class_count']},"
            f" orbits N^3 {row['orbit_sizes_all_n_cubed']},"
            f" supp price matches QM3 {row['supp_price_matches_qm3']},"
            f" counts {row['supp_price_counts']},"
            f" circ antidiagonal exact {row['circ_antidiagonal_exact']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
