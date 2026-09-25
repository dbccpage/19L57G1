"""Source verification for research/m108_internal_algebra.

AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = Path(__file__).resolve().parent / "SOURCE_MANIFEST.json"


def check_sha256(data: bytes, expected: str) -> bool:
    h_raw = hashlib.sha256(data).hexdigest().lower()
    h_norm = hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest().lower()
    return expected.lower() in (h_raw, h_norm)


def check_git_blob(data: bytes, expected: str) -> bool:
    lf_data = data.replace(b"\r\n", b"\n")
    blob_norm = hashlib.sha1(f"blob {len(lf_data)}\0".encode() + lf_data).hexdigest().lower()
    blob_raw = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest().lower()
    return expected.lower() in (blob_norm, blob_raw)


def verify_sources() -> list[str]:
    errors: list[str] = []
    if not MANIFEST_PATH.exists():
        return ["SOURCE_MANIFEST.json missing"]
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    sources = manifest.get("sources")
    if not isinstance(sources, list):
        return ["SOURCE_MANIFEST.json has no sources"]
    # 2026-09-24: an empty list passes only when the manifest says why: the
    # tree consumes nothing outside its directory, or what it consumes is
    # named under unpinned_inputs.  An unexplained empty list still fails.
    declares_none = manifest.get("outside_inputs") == "none"
    unpinned = manifest.get("unpinned_inputs")
    names_unpinned = isinstance(unpinned, list) and bool(unpinned)
    if sources and declares_none:
        return ["SOURCE_MANIFEST.json declares outside_inputs none but pins sources"]
    if not sources and not (declares_none or names_unpinned):
        return ["SOURCE_MANIFEST.json has no sources"]
    for item in sources:
        if not isinstance(item, dict) or "path" not in item:
            errors.append("source entry missing path")
            continue
        p = REPO_ROOT / item["path"]
        if not p.is_file():
            errors.append(f"Missing source file: {item['path']}")
            continue
        data = p.read_bytes()
        if "sha256" in item and not check_sha256(data, item["sha256"]):
            actual = hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()
            errors.append(f"Hash mismatch for {item['path']}: expected {item['sha256']}, got {actual}")
        if "git_blob" in item and not check_git_blob(data, item["git_blob"]):
            lf_data = data.replace(b"\r\n", b"\n")
            actual_blob = hashlib.sha1(f"blob {len(lf_data)}\0".encode() + lf_data).hexdigest()
            errors.append(f"Git blob mismatch for {item['path']}: expected {item['git_blob']}, got {actual_blob}")
    return errors


def main() -> int:
    errs = verify_sources()
    if errs:
        for e in errs:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest["sources"]:
        print("PASS: all source pins match")
    elif manifest.get("outside_inputs") == "none":
        print("PASS: nothing pinned; the manifest declares no outside inputs")
    else:
        print("PASS: nothing pinned; the manifest names its unpinned inputs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
