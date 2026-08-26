"""Write the deterministic finite G4 engine-import-branch artifact."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import write_json
from derivation.g4_engine_import_branch import g4_report


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    args = parser.parse_args(argv)
    payload = g4_report()
    out_path = args.artifacts / "g4_engine_import_branch.json"
    write_json(out_path, payload)
    print(f"obstructions checked: {payload['total_obstructions_checked']}")
    terminal_values = payload["terminals"]
    assert isinstance(terminal_values, list)
    print(f"terminals: {', '.join(str(item) for item in terminal_values)}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
