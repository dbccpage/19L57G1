"""Write the deterministic local finite-alphabet G1 artifact."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import write_json
from derivation.local_strategy import (
    DEFAULT_MAX_CHAIN,
    STRATEGIES,
    artifact_payload,
)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    parser.add_argument("--max-chain", type=int, default=DEFAULT_MAX_CHAIN)
    args = parser.parse_args(argv)
    payload = artifact_payload(args.max_chain)
    out_path = args.artifacts / "local_strategy.json"
    write_json(out_path, payload)
    print(f"strategies classified: {len(STRATEGIES)}")
    print("G1 terminal: G1_CLASS_EXCLUSION_PROVED")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
