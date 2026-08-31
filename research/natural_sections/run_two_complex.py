"""Write receipts/two_complex.json deterministically (``--out DIR``)."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

import two_complex

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
    report = two_complex.report()
    (out / "two_complex.json").write_bytes(render(report))
    surveys = report["surveys"]
    assert isinstance(surveys, list)
    for row in surveys:
        print(
            f"N={row['modulus']}: total {row['total']}, sections {row['sections']},"
            f" outer-zero {row['outer_zero']},"
            f" outer-zero-obstructed {row['outer_zero_obstructed']},"
            f" boundary identity {row['boundary_identity_everywhere']},"
            f" potential==flux {row['potential_matches_flux_criterion']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
