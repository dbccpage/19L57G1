from __future__ import annotations

import argparse
import json
from pathlib import Path

from model import connector_payload


def render() -> bytes:
    return (json.dumps(connector_payload(), indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = Path(__file__).resolve().parent / "receipts" / "connector.json"
    if args.write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(render())
    if not path.exists() or path.read_bytes() != render():
        raise ValueError("connector receipt differs from deterministic renderer")
    print("connector receipt replay clean: IMPORT_ISOLATED_BUT_NOT_REMOVED")


if __name__ == "__main__":
    main()
