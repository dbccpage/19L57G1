"""Artifact regeneration gate.

Usage: python ci/compare_artifacts.py <committed-dir> <regenerated-dir>

* every committed ``*.json`` must be byte-identical to its regeneration;
* every committed ``full/*.json.gz`` must decompress to bytes identical
  to its regeneration's decompression (compression bytes may differ
  across zlib builds; the exported content may not);
* every summary's ``full_export_sha256`` must equal the SHA-256 of the
  decompressed full export;
* the two directories must hold the SAME SET of exports.

The set check is the half that makes the runner census in
``.github/workflows/verify.yml`` a glob rather than a hand list.  Walking
the committed side catches a committed artifact that stopped being
regenerated -- a runner renamed, deleted, or dropped out of the census.
Walking the regenerated side catches the opposite: a runner that ran and
produced an export nobody committed, which is otherwise invisible here
because every other check iterates the committed directory.

Both of those were previously reported by an uncaught ``FileNotFoundError``
rather than by a named failure.  The exit status is unchanged -- missing
files failed the gate before and fail it now; only the diagnostic differs.
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
        if not other.is_file():
            failures.append(f"missing regeneration: {path.name}")
            continue
        if path.read_bytes() != other.read_bytes():
            failures.append(f"byte mismatch: {path.name}")
    fulls = sorted((committed / "full").glob("*.json.gz"))
    for path in fulls:
        other_path = regenerated / "full" / path.name
        if not other_path.is_file():
            failures.append(f"missing regeneration: full/{path.name}")
            continue
        raw = gzip.decompress(path.read_bytes())
        other = gzip.decompress(other_path.read_bytes())
        if raw != other:
            failures.append(f"content mismatch: full/{path.name}")
        summary_name = path.name.replace(".json.gz", "_summary.json")
        summary_path = committed / summary_name
        if not summary_path.is_file():
            failures.append(f"missing committed summary: {summary_name}")
            continue
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if hashlib.sha256(raw).hexdigest() != summary["full_export_sha256"]:
            failures.append(f"summary hash mismatch: {summary_name}")
    # The other direction. Every check above starts from the committed
    # directory, so an export produced by a runner nobody committed is
    # invisible to all of them.
    committed_names = {path.name for path in json_files}
    for path in sorted(regenerated.glob("*.json")):
        if path.name not in committed_names:
            failures.append(f"regenerated but not committed: {path.name}")
    full_names = {path.name for path in fulls}
    for path in sorted((regenerated / "full").glob("*.json.gz")):
        if path.name not in full_names:
            failures.append(f"regenerated but not committed: full/{path.name}")
    for failure in failures:
        print(f"FAIL: {failure}")
    if not failures:
        print(
            f"artifacts reproducible: {len(json_files)} json files "
            f"byte-identical, {len(fulls)} full exports content-identical "
            "and hash-pinned, export sets equal in both directions"
        )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
