"""Write receipts/holonomy_group.json deterministically (``--out DIR``)."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

import holonomy_fixture
import holonomy_group

HERE = Path(__file__).resolve().parent


def render() -> bytes:
    return (
        json.dumps(holonomy_group.report(), indent=2, sort_keys=True, ensure_ascii=True) + "\n"
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
    (out / "holonomy_group.json").write_bytes(render())
    for name, sites, edges in holonomy_fixture.fixtures():
        v = holonomy_group.analyse_k(name, sites, edges, 3)
        orders = ",".join(str(c.group_order) for c in v.components)
        print(
            f"k=3 {name}: {'section exists' if v.section_exists else 'NO natural section'}; "
            f"parity says {'clean' if v.parity_says_clean else 'obstructed'}; "
            f"objects {v.objects}, group order(s) {orders or '-'}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
