"""Artifact regeneration gate.

Usage: python ci/compare_artifacts.py <committed-dir> <regenerated-dir>

* every committed ``*.json`` must be byte-identical to its regeneration;
* every committed ``full/*.json.gz`` must decompress to bytes identical
  to its regeneration's decompression (compression bytes may differ
  across zlib builds; the exported content may not);
* every summary's ``full_export_sha256`` must equal the SHA-256 of the
  decompressed full export.
"""

import gzip
import hashlib
import json
import pathlib
import sys


def main() -> int:
    committed = pathlib.Path(sys.argv[1])
    regenerated = pathlib.Path(sys.argv[2])
    failures: list[str] = []
    json_files = sorted(committed.glob("*.json"))
    for path in json_files:
        other = regenerated / path.name
        if path.read_bytes() != other.read_bytes():
            failures.append(f"byte mismatch: {path.name}")
    fulls = sorted((committed / "full").glob("*.json.gz"))
    for path in fulls:
        raw = gzip.decompress(path.read_bytes())
        other = gzip.decompress(
            (regenerated / "full" / path.name).read_bytes()
        )
        if raw != other:
            failures.append(f"content mismatch: full/{path.name}")
        summary_name = path.name.replace(".json.gz", "_summary.json")
        summary = json.loads(
            (committed / summary_name).read_text(encoding="utf-8")
        )
        if hashlib.sha256(raw).hexdigest() != summary["full_export_sha256"]:
            failures.append(f"summary hash mismatch: {summary_name}")
    for failure in failures:
        print(f"FAIL: {failure}")
    if not failures:
        print(
            f"artifacts reproducible: {len(json_files)} json files "
            f"byte-identical, {len(fulls)} full exports content-identical "
            "and hash-pinned"
        )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
