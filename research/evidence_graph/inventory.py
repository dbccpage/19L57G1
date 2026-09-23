"""Regenerate the source census, without promoting evidence. AuthorityEffect: None."""
from __future__ import annotations

import argparse
import gzip
from pathlib import Path
from typing import Any

from eg_census import headlines, import_census
from eg_inventory import tree_inventory
from eg_sources import HERE, canonical, load_snapshot, read_object


def inventory() -> dict[str, Any]:
    snapshot = load_snapshot()
    imports = import_census(snapshot)
    trees = tree_inventory(snapshot, imports)
    blocks = headlines(snapshot, read_object(HERE / "input.json"))
    return {"schema": 1, "source_snapshot": snapshot.snapshot, "authority_effect": "None",
            "trees": trees, "headlines": blocks, "imports": imports,
            "summary": {"source_files": len(snapshot.files), "source_trees": len(trees),
                        "gate11": sum(row["registration"] == "workflow (gate 11)" for row in trees),
                        "local_only": sum(row["registration"] == "local receipt only" for row in trees),
                        "parked": [row["name"] for row in trees if row["maintenance_status"] == "parked"],
                        "public_files": len({row["source"]["path"] for row in blocks}), "public_blocks": len(blocks),
                        "research_lean_files": imports["tracked_lean_files"], "direct_native_import_files": len(imports["direct_files"]),
                        "direct_native_import_trees": len(imports["direct_trees"])}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=HERE / "evidence" / "inventory.json.gz")
    args = parser.parse_args()
    record = inventory()
    raw = gzip.compress(canonical(record), mtime=0)
    if args.write:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(raw)
    elif not args.output.is_file() or args.output.read_bytes() != raw:
        raise ValueError("INVENTORY_DIFFERS")
    print(canonical(record["summary"]).decode("utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
