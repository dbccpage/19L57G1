"""Source verification for research/p209b_clifford_symplectic."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = Path(__file__).resolve().parent / "SOURCE_MANIFEST.json"


def verify_sources() -> list[str]:
    errors: list[str] = []
    if not MANIFEST_PATH.exists():
        return ["SOURCE_MANIFEST.json missing"]
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    for item in manifest.get("sources", []):
        p = REPO_ROOT / item["path"]
        if not p.exists():
            errors.append(f"Missing source file: {item['path']}")
            continue
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        if h.lower() != item["sha256"].lower():
            errors.append(f"Hash mismatch for {item['path']}: expected {item['sha256']}, got {h}")
    return errors


def main() -> int:
    errs = verify_sources()
    if errs:
        for e in errs:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print("PASS: all source pins match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
