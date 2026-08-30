"""Write receipts/embedding.json deterministically (``--out DIR``)."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

import embedding

HERE = Path(__file__).resolve().parent


def assert_inside_tree(path: Path, root: Path | None = None) -> Path:
    """Refuse a write whose resolved path is not under this tree."""

    target = path.resolve()
    base = root.resolve() if root is not None else HERE
    if not target.is_relative_to(base):
        raise ValueError(f"refusing to write outside research/family_embedding/: {path}")
    return target


def render() -> bytes:
    return (
        json.dumps(embedding.report(), indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    ).encode("ascii")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(HERE / "receipts"))
    args = parser.parse_args(argv)
    try:
        out = assert_inside_tree(Path(args.out).resolve())
        out.mkdir(parents=True, exist_ok=True)
        (out / "embedding.json").write_bytes(render())
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    r = embedding.report()
    for name in ("obstructed", "clean"):
        block = r[name]
        assert isinstance(block, dict)
        print(
            name,
            "hom_inhabited",
            block["hom_inhabited"],
            "flat",
            block["flat_natural_section"],
            "H",
            block["h_natural_section"],
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
