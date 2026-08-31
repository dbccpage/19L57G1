"""Write receipts/q_one.json deterministically (``--out DIR``)."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

import q_one

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
    report = q_one.report()
    (out / "q_one.json").write_bytes(render(report))
    laws = report["group_laws"]
    assert isinstance(laws, dict)
    print(
        f"group laws to index {laws['max_index']}: {laws['pairs']} pairs,"
        f" assoc misses {laws['assoc_misses']}, comm misses {laws['comm_misses']},"
        f" inverse misses {laws['inv_misses']}"
    )
    compat = report["layer_compat"]
    assert isinstance(compat, dict)
    print(f"layer compatibility: {compat['checks']} checks, {compat['misses']} misses")
    print(f"orders of layer-one elements k=0..7: {report['orders_of_layer_one']}")
    print(f"reduced counts at part counts 1..8: {report['reduced_counts']}")
    joints = report["joint_layers"]
    assert isinstance(joints, list)
    print(f"joint layers of the pinned lists: {[case['joint'] for case in joints]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
