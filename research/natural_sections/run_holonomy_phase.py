"""Write receipts/holonomy_phase.json deterministically (``--out DIR``)."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

import holonomy_phase

HERE = Path(__file__).resolve().parent


def render() -> bytes:
    return (
        json.dumps(holonomy_phase.report(), indent=2, sort_keys=True, ensure_ascii=True) + "\n"
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
    (out / "holonomy_phase.json").write_bytes(render())
    for name, entry in holonomy_phase.summary().items():
        comps = entry["components"]
        assert isinstance(comps, list)
        detail = "; ".join(
            f"order {c['group_order']}"
            f"{' perm-trivial' if c['permutation_part_trivial'] else ''}"
            f"{' phase-trivial' if c['phase_part_trivial'] else ''}"
            f" pair={c['fixed_pair_exists']}"
            for c in comps
        )
        print(f"{name}: {'section exists' if entry['section_exists'] else 'NO natural section'} [{detail}]")
    for phi in range(holonomy_phase.N + 1):
        c = holonomy_phase.one_on_each(phi, holonomy_phase.N)
        print(
            f"one on each, flux {phi}: order {c.group_order},"
            f" permutation part {'trivial' if c.permutation_part_trivial else 'NONTRIVIAL'},"
            f" fixed pair {c.fixed_pair_exists}"
        )
    print("gauge invariance:", all(holonomy_phase.gauge_check().values()))
    print("periodicity:", holonomy_phase.periodicity_check())
    print("refinement compatibility:", holonomy_phase.refinement_check())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
