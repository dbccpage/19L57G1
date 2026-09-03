"""Verify the sealed sources this tree imports and the frozen texts.

Usage: python research/identification_dual/verify_pins.py [--repin]

Checks, none implying the others:

* every sealed module in ``SOURCE_MANIFEST.json`` still hashes, as a
  canonical Git blob at HEAD, to its recorded sha256;
* the recorded snapshot commit exists and is an ancestor of HEAD, with
  ``git merge-base`` exit codes other than one reported as undecided
  rather than as "not an ancestor";
* the frozen challenge and prediction texts still hash, as blobs at HEAD,
  to the values recorded when they were frozen.

A pass says the inputs did not move.  It says nothing about the
mathematics.  ``--repin`` rewrites the source hashes from HEAD and
verifies nothing; the frozen texts are never repinned by this script.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
from pathlib import PurePosixPath
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
MANIFEST = HERE / "SOURCE_MANIFEST.json"


def _git_bytes(*args: str) -> bytes:
    result = subprocess.run(["git", *args], cwd=REPO, capture_output=True, check=False)
    if result.returncode != 0:
        raise ValueError(
            f"git {' '.join(args)} failed: "
            f"{result.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return result.stdout


def _git(*args: str) -> str:
    return _git_bytes(*args).decode("utf-8").strip()


def _blob_sha256(revision: str, relative: PurePosixPath) -> str:
    return hashlib.sha256(_git_bytes("show", f"{revision}:{relative.as_posix()}")).hexdigest()


def _read_manifest() -> dict[str, Any]:
    payload: object = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("SOURCE_MANIFEST.json must be an object")
    return payload


def _safe(raw: object) -> PurePosixPath:
    if not isinstance(raw, str) or not raw:
        raise ValueError("path must be a non-empty string")
    relative = PurePosixPath(raw)
    if relative.is_absolute() or any(part == ".." for part in relative.parts):
        raise ValueError(f"unsafe path in manifest: {raw}")
    return relative


def _ancestor(snapshot: str) -> str:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", snapshot, "HEAD"],
        cwd=REPO, capture_output=True, check=False,
    )
    if result.returncode == 0:
        return "ancestor"
    if result.returncode == 1:
        return "not an ancestor"
    return f"undecided (git exit {result.returncode})"


def verify() -> list[str]:
    manifest = _read_manifest()
    lines: list[str] = []
    head = _git("rev-parse", "HEAD")
    lines.append(f"verification commit: {head}")
    snapshot = manifest.get("snapshot_commit")
    if not isinstance(snapshot, str) or len(snapshot) != 40:
        raise ValueError("snapshot_commit must be a 40-digit commit id")
    relation = _ancestor(snapshot)
    if relation != "ancestor":
        raise ValueError(f"snapshot {snapshot} is {relation} of HEAD")
    lines.append(f"snapshot commit: {snapshot} (ancestor of HEAD)")
    sources = manifest.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("manifest must list at least one sealed source")
    for item in sources:
        if not isinstance(item, dict):
            raise ValueError("each source entry must be an object")
        relative = _safe(item.get("path"))
        wanted = item.get("sha256")
        if not isinstance(wanted, str):
            raise ValueError(f"missing sha256 for {relative}")
        actual = _blob_sha256("HEAD", relative).upper()
        if actual != wanted.upper():
            raise ValueError(
                f"hash mismatch for {relative}: expected {wanted}, got {actual}"
            )
        lines.append(f"source: {relative} {actual}")
    frozen = manifest.get("frozen_texts")
    if not isinstance(frozen, list) or not frozen:
        raise ValueError("manifest must list the frozen texts")
    for item in frozen:
        if not isinstance(item, dict):
            raise ValueError("each frozen text entry must be an object")
        relative = _safe(item.get("path"))
        wanted = item.get("sha256")
        if not isinstance(wanted, str):
            raise ValueError(f"missing sha256 for {relative}")
        actual = _blob_sha256("HEAD", relative)
        if actual != wanted:
            raise ValueError(
                f"frozen text moved: {relative}: expected {wanted}, got {actual}"
            )
        lines.append(f"frozen: {relative} {actual}")
    return lines


def repin() -> list[str]:
    manifest = _read_manifest()
    lines: list[str] = []
    sources = manifest.get("sources")
    if not isinstance(sources, list):
        raise ValueError("manifest must list sources")
    for item in sources:
        if not isinstance(item, dict):
            raise ValueError("each source entry must be an object")
        relative = _safe(item.get("path"))
        old = item.get("sha256")
        new = _blob_sha256("HEAD", relative).upper()
        if old != new:
            lines.append(f"rehashed: {relative} {old} -> {new}")
        item["sha256"] = new
    manifest["snapshot_commit"] = _git("rev-parse", "HEAD")
    MANIFEST.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8", newline="\n",
    )
    lines.append("repinned sources; frozen texts untouched; STATUS.md must be re-read by hand")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the identification-dual pins.")
    parser.add_argument("--repin", action="store_true", help="rewrite source hashes from HEAD; verifies nothing")
    args = parser.parse_args()
    try:
        lines = repin() if args.repin else verify()
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
