"""Write receipts/conj_orbit.json deterministically (``--out DIR``)."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

import conj_orbit

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
    report = conj_orbit.report()
    (out / "conj_orbit.json").write_bytes(render(report))
    square = report["square_k2"]
    assert isinstance(square, dict)
    print(
        f"square k=2: {square['closed_walks']} closed walks up to length {square['max_len']};"
        f" holonomy group order {square['group_order']}"
    )
    for row in square["orbits"]:
        print(f"   orbit {row['orbit']}: twisted_unit {row['twisted_unit']}, agree {row['agree']}")
    print(f"all orbits agree: {square['all_orbits_agree']}")
    mini = report["mini_list"]
    assert isinstance(mini, dict)
    print(f"mini list: twisted_unit {mini['twisted_unit']}, total_unit {mini['total_unit']}")
    closure = report["unit_conjugation_closure"]
    assert isinstance(closure, dict)
    print(
        f"unit conjugation closure to length {closure['max_len']}: {closure['walks']} walks,"
        f" {closure['pairs']} pairs, {closure['violations']} violations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
