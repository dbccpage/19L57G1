"""Verify the sources this rung consumes and the frozen texts it froze.

Usage: python research/second_class/verify_pins.py [--repin | --require-current]

A hand copy of `research/second_duration/verify_pins.py`, with this rung's
usage line and description; the checks are unchanged.  A defect repaired
in one copy stays live in the others until carried by hand.

Checks, none implying the others:

* the recorded snapshot commit exists and is an ancestor of HEAD, with
  ``git merge-base`` exit codes other than one reported as undecided
  rather than as "not an ancestor";
* every consumed source hashes, as a canonical Git blob, to its recorded
  sha256 at the snapshot; a source that moved between the snapshot and
  HEAD is a drift, REPORTED (below), and a repin is a logged act, never a
  rewrite;
* every recorded SPAN hashes to its recorded sha256 at the snapshot; a
  span that moved at HEAD is REPORTED the same way.  A blob pin and a
  span pin are different guarantees: a blob pin says the file did not
  move, and a span pin says the exact lines this rung quotes or
  reconstructs did not move.  A file can be edited far from
  a span, which fails the blob pin and passes the span pin; recording both
  says which happened;
* the absent-at-snapshot record is checked AT THE SNAPSHOT, not at HEAD,
  because it is a historical statement;
* the frozen challenge and prediction texts still hash, as blobs at HEAD,
  to the values recorded when they were frozen.

Pins certify the snapshot (2026-09-25, applying the author's ruling of
2026-09-22).  A source or span that moved or is absent at HEAD is printed
as a ``DRIFT:`` line, then a ``drift since the snapshot:`` count, and does
not fail; ``--require-current`` restores that failure.  The frozen texts
live in this rung's own write root, so a moved frozen text still fails.
This file used to fail on a source that moved at HEAD, so every
authorized sealed edit turned it red until a repin.

A pass says the inputs matched at the snapshot.  It says nothing about the
mathematics, and nothing about whether the reconstructions in ``lean/``
are faithful to the sources they pin.  That is checked declaration by
declaration in ``test_reconstruction.py``, against the blobs AT THE
SNAPSHOT; what that check omits is pinned there and read by hand.

``--repin`` rewrites the source and span hashes from HEAD and verifies
nothing; the frozen texts are never repinned by this script.  A repin is
never done under a live injection.

AuthorityEffect: None.
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

sys.dont_write_bytecode = True

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


def _blob(revision: str, relative: PurePosixPath) -> bytes:
    return _git_bytes("show", f"{revision}:{relative.as_posix()}")


def _blob_sha256(revision: str, relative: PurePosixPath) -> str:
    return hashlib.sha256(_blob(revision, relative)).hexdigest()


def _span_sha256(revision: str, relative: PurePosixPath, first: int, last: int) -> str:
    """The hash of lines ``first``..``last`` inclusive, one-based, with line
    endings normalized to LF so a checkout convention cannot move a span."""
    text = _blob(revision, relative).decode("utf-8")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    if last > len(lines):
        raise ValueError(
            f"span {relative}:{first}-{last} runs past the end of the file"
            f" ({len(lines)} lines)"
        )
    segment = "\n".join(lines[first - 1 : last]) + "\n"
    return hashlib.sha256(segment.encode("utf-8")).hexdigest()


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
        cwd=REPO,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        return "ancestor"
    if result.returncode == 1:
        return "not an ancestor"
    return f"undecided (git exit {result.returncode})"


def _int(item: dict[str, Any], key: str) -> int:
    value = item.get(key)
    if not isinstance(value, int):
        raise ValueError(f"{key} must be an integer, got {value!r}")
    return value


def _tracked_at_head(relative: PurePosixPath) -> bool:
    listed = _git("ls-tree", "-r", "--name-only", "HEAD", "--", relative.as_posix())
    return relative.as_posix() in listed.splitlines()


def verify(require_current: bool = False) -> list[str]:
    manifest = _read_manifest()
    lines: list[str] = []
    drift: list[str] = []
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
        raise ValueError("manifest must list at least one consumed source")
    for item in sources:
        if not isinstance(item, dict):
            raise ValueError("each source entry must be an object")
        relative = _safe(item.get("path"))
        wanted = item.get("sha256")
        if not isinstance(wanted, str):
            raise ValueError(f"missing sha256 for {relative}")
        at_snapshot = _blob_sha256(snapshot, relative).upper()
        if at_snapshot != wanted.upper():
            raise ValueError(
                f"hash mismatch at the snapshot for {relative}: "
                f"expected {wanted}, got {at_snapshot}"
            )
        try:
            at_head = _blob_sha256("HEAD", relative).upper()
        except ValueError as exc:
            if _tracked_at_head(relative):
                raise ValueError(f"could not read {relative} at HEAD: {exc}") from exc
            drift.append(f"source {relative} is absent at HEAD")
        else:
            if at_head != wanted.upper():
                drift.append(f"source moved at HEAD for {relative}: expected {wanted}, got {at_head}")
        lines.append(f"source: {relative} {at_snapshot}")

    spans = manifest.get("spans")
    if not isinstance(spans, list) or not spans:
        raise ValueError("manifest must list at least one span")
    for item in spans:
        if not isinstance(item, dict):
            raise ValueError("each span entry must be an object")
        relative = _safe(item.get("path"))
        first = _int(item, "first_line")
        last = _int(item, "last_line")
        if first < 1 or last < first:
            raise ValueError(f"span bounds out of order for {relative}")
        wanted = item.get("sha256")
        if not isinstance(wanted, str):
            raise ValueError(f"missing span sha256 for {relative}")
        at_snapshot = _span_sha256(snapshot, relative, first, last)
        if at_snapshot != wanted:
            raise ValueError(
                f"span mismatch at the snapshot for {relative}:{first}-{last}: "
                f"expected {wanted}, got {at_snapshot}"
            )
        try:
            span_head = _span_sha256("HEAD", relative, first, last)
        except ValueError as exc:
            if str(exc).startswith("git ") and _tracked_at_head(relative):
                raise ValueError(
                    f"could not read span {relative}:{first}-{last} at HEAD: {exc}"
                ) from exc
            drift.append(f"span {relative}:{first}-{last} cannot be read at HEAD: {exc}")
        else:
            if span_head != wanted:
                drift.append(
                    f"span moved at HEAD for {relative}:{first}-{last}: "
                    f"expected {wanted}, got {span_head}"
                )
        lines.append(f"span: {relative}:{first}-{last} {at_snapshot}")

    absent = manifest.get("absent_at_snapshot")
    if not isinstance(absent, list):
        raise ValueError("manifest must list absent_at_snapshot (possibly empty)")
    for item in absent:
        if not isinstance(item, dict):
            raise ValueError("each absent entry must be an object")
        relative = _safe(item.get("path"))
        result = subprocess.run(
            ["git", "ls-tree", "-d", "--name-only", snapshot, relative.as_posix()],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
        )
        present = result.returncode == 0 and bool(result.stdout.strip())
        if present != bool(item.get("present_at_snapshot")):
            raise ValueError(
                f"absent-at-snapshot record wrong for {relative}: present={present}"
            )
        lines.append(
            f"absent at snapshot: {relative} (pull request {item.get('pull_request')})"
        )

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

    if drift and require_current:
        raise ValueError(
            "pinned inputs moved between the snapshot and HEAD (--require-current):\n  "
            + "\n  ".join(drift)
        )
    lines.extend(f"DRIFT: {line}" for line in drift)
    lines.append(f"drift since the snapshot: {len(drift)} source(s) or span(s) moved at HEAD")
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
    spans = manifest.get("spans")
    if not isinstance(spans, list):
        raise ValueError("manifest must list spans")
    for item in spans:
        if not isinstance(item, dict):
            raise ValueError("each span entry must be an object")
        relative = _safe(item.get("path"))
        first = _int(item, "first_line")
        last = _int(item, "last_line")
        old = item.get("sha256")
        new = _span_sha256("HEAD", relative, first, last)
        if old != new:
            lines.append(f"rehashed span: {relative}:{first}-{last} {old} -> {new}")
        item["sha256"] = new
    manifest["snapshot_commit"] = _git("rev-parse", "HEAD")
    MANIFEST.write_bytes(
        (json.dumps(manifest, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
    )
    lines.append(
        "repinned sources and spans; frozen texts untouched;"
        " STATUS.md and CLAIM_LEDGER.md must be re-read by hand"
    )
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the rung-eight pins.")
    parser.add_argument(
        "--repin",
        action="store_true",
        help="rewrite source and span hashes from HEAD; verifies nothing",
    )
    parser.add_argument(
        "--require-current",
        action="store_true",
        help="also fail when a source or span has moved between the snapshot and HEAD",
    )
    args = parser.parse_args()
    try:
        lines = repin() if args.repin else verify(require_current=args.require_current)
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
