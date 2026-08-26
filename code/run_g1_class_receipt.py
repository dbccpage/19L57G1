"""Write the deterministic local finite-alphabet G1 receipt."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import write_json
from derivation.g1_class_receipt import build_receipt


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    payload = build_receipt(root)
    out_path = args.artifacts / "g1_class_receipt.json"
    write_json(out_path, payload)
    reports = payload["new_theorem_axiom_reports"]
    assert isinstance(reports, list)
    print(f"new theorem reports bound: {len(reports)}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

