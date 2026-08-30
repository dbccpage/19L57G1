"""Write receipts/representation.json deterministically (``--out DIR``)."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

import representation

HERE = Path(__file__).resolve().parent


def render() -> bytes:
    return (
        json.dumps(representation.report(), indent=2, sort_keys=True, ensure_ascii=True) + "\n"
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
    (out / "representation.json").write_bytes(render())
    r = representation.report()
    for name in ("square", "chain", "star"):
        block = r[name]
        assert isinstance(block, dict)
        print(name, "re-presentation:", block["re_presentation"])
        deletion = block["deletion"]
        assert isinstance(deletion, dict)
        print(name, "deletion:", {k: v for k, v in deletion.items() if k != "hops"})
        if "cover" in block:
            print(name, "cover:", block["cover"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
