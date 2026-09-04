"""Verify source blobs, quoted spans, and the two frozen rung texts."""

from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
from pathlib import PurePosixPath
from typing import cast

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
MANIFEST = HERE / "SOURCE_MANIFEST.json"

JsonObject = dict[str, object]


def git_bytes(*arguments: str) -> bytes:
    result = subprocess.run(
        ["git", *arguments], cwd=REPO, capture_output=True, check=False
    )
    if result.returncode != 0:
        error = result.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"git {' '.join(arguments)} failed: {error}")
    return result.stdout


def git_text(*arguments: str) -> str:
    return git_bytes(*arguments).decode("utf-8").strip()


def safe_path(value: object) -> PurePosixPath:
    if not isinstance(value, str) or not value:
        raise ValueError("manifest path must be non-empty text")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe manifest path: {value}")
    return path


def manifest() -> JsonObject:
    value: object = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("source manifest must be an object")
    return cast(JsonObject, value)


def entries(value: object, name: str) -> list[JsonObject]:
    if not isinstance(value, list):
        raise ValueError(f"manifest {name} must be a list")
    if not all(isinstance(item, dict) for item in value):
        raise ValueError(f"manifest {name} entries must be objects")
    return cast(list[JsonObject], value)


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def blob(revision: str, path: PurePosixPath) -> bytes:
    return git_bytes("show", f"{revision}:{path.as_posix()}")


def expected_sha(entry: JsonObject) -> str:
    value = entry.get("sha256")
    if not isinstance(value, str) or len(value) != 64:
        raise ValueError("manifest sha256 must be sixty-four hexadecimal digits")
    return value.lower()


def span_bytes(source: bytes, start: int, end: int) -> bytes:
    lines = source.splitlines(keepends=True)
    if start < 1 or end < start or end > len(lines):
        raise ValueError(f"invalid span {start}-{end} for source with {len(lines)} lines")
    return b"".join(lines[start - 1 : end])


def verify() -> list[str]:
    data = manifest()
    snapshot = data.get("snapshot_commit")
    if not isinstance(snapshot, str) or len(snapshot) != 40:
        raise ValueError("snapshot_commit must be a full commit id")
    relation = subprocess.run(
        ["git", "merge-base", "--is-ancestor", snapshot, "HEAD"],
        cwd=REPO,
        capture_output=True,
        check=False,
    )
    if relation.returncode != 0:
        raise ValueError(
            f"snapshot is not a verified ancestor of HEAD: git exit {relation.returncode}"
        )
    lines = [f"snapshot: {snapshot} (ancestor of {git_text('rev-parse', 'HEAD')})"]
    source_entries = entries(data.get("sources"), "sources")
    cached: dict[PurePosixPath, bytes] = {}
    for entry in source_entries:
        path = safe_path(entry.get("path"))
        wanted = expected_sha(entry)
        at_snapshot = blob(snapshot, path)
        at_head = blob("HEAD", path)
        if digest(at_snapshot) != wanted:
            raise ValueError(f"snapshot blob moved: {path}")
        if digest(at_head) != wanted:
            raise ValueError(f"HEAD blob moved: {path}")
        cached[path] = at_snapshot
        lines.append(f"source: {path} {wanted}")
    for entry in entries(data.get("spans"), "spans"):
        name = entry.get("name")
        if not isinstance(name, str):
            raise ValueError("span name must be text")
        path = safe_path(entry.get("path"))
        start, end = entry.get("start"), entry.get("end")
        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError(f"span bounds must be integers: {name}")
        wanted = expected_sha(entry)
        for revision in (snapshot, "HEAD"):
            actual = digest(span_bytes(blob(revision, path), start, end))
            if actual != wanted:
                raise ValueError(f"span moved at {revision}: {name}")
        lines.append(f"span: {name} {path}:{start}-{end} {wanted}")
    for entry in entries(data.get("frozen_texts"), "frozen_texts"):
        path = safe_path(entry.get("path"))
        wanted = expected_sha(entry)
        disk = REPO / pathlib.Path(*path.parts)
        if not disk.is_file():
            raise ValueError(f"frozen text missing from disk: {path}")
        if digest(disk.read_bytes()) != wanted:
            raise ValueError(f"frozen text moved on disk: {path}")
        if digest(blob("HEAD", path)) != wanted:
            raise ValueError(f"frozen text moved in HEAD: {path}")
        if entry.get("no_digits") is True and any(
            byte in b"0123456789" for byte in disk.read_bytes()
        ):
            raise ValueError(f"frozen text contains a digit: {path}")
        lines.append(f"frozen: {path} {wanted}")
    for entry in entries(data.get("absent_at_snapshot"), "absent_at_snapshot"):
        path = safe_path(entry.get("path"))
        listing = git_text("ls-tree", "-d", "--name-only", snapshot, path.as_posix())
        present = bool(listing)
        if present != bool(entry.get("present")):
            raise ValueError(f"snapshot presence record differs: {path}")
        lines.append(f"absent at snapshot: {path}")
    return lines


def main() -> int:
    try:
        lines = verify()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        return 1
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
