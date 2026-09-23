"""Inspect scoped records without opening the entire generated graph. AuthorityEffect: None."""
from __future__ import annotations

import argparse
import json
from typing import Any

from eg_sources import HERE, read_object


def select(graph: dict[str, Any], identifier: str | None = None, source: str | None = None,
           line: int | None = None) -> list[dict[str, Any]]:
    if identifier is not None:
        return [row for rows in graph["records"].values() for row in rows if row["id"] == identifier]
    return [row for row in graph["records"]["headline"] if row["source"]["path"] == source
            and (line is None or row["source"]["start_line"] <= line <= row["source"]["end_line"])]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--id")
    mode.add_argument("--source")
    parser.add_argument("--line", type=int)
    args = parser.parse_args()
    rows = select(read_object(HERE / "evidence" / "graph.json.gz"), args.id, args.source, args.line)
    if not rows:
        raise ValueError("RECORD_NOT_FOUND")
    print(json.dumps(rows, ensure_ascii=True, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
