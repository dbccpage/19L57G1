"""Write receipts/holonomy_fixture.json deterministically (``--out DIR``)."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

import holonomy_fixture

HERE = Path(__file__).resolve().parent


def render() -> bytes:
    return (
        json.dumps(holonomy_fixture.report(), indent=2, sort_keys=True, ensure_ascii=True)
        + "\n"
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
    (out / "holonomy_fixture.json").write_bytes(render())
    for name, exists in sorted(holonomy_fixture.summary().items()):
        print(f"{name}: {'section exists' if exists else 'NO natural section'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
