"""Verify this tree's source manifest against the repository.

Usage: python research/seventh_constructor/verify_sources.py [--repin]

The manifest pins the sealed model and iso modules,
along with the Movegraph research modules consumed from sign_tower.
Sealed prefixes must stay clean.

A pass says the inputs did not move. AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
MANIFEST_PATH = HERE / "SOURCE_MANIFEST.json"
SCHEMA = "seventh_constructor_source_manifest/v1"

SEALED_PATHSPECS = ("prompt", "paper", "code", "lean4/Derivation", "artifacts")
SEALED_PREFIXES = tuple(f"{spec}/" for spec in SEALED_PATHSPECS)
RESEARCH_PREFIXES = (
    "research/sign_tower/",
)


def _run_git(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, check=False)


def _git_bytes(*args: str) -> bytes:
    result = _run_git(*args)
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"git {' '.join(args)} failed: {stderr}")
    return result.stdout


def _git(*args: str) -> str:
    return _git_bytes(*args).decode("utf-8").strip()


def _sha256_git_blob(revision: str, relative: PurePosixPath) -> str:
    return hashlib.sha256(_git_bytes("show", f"{revision}:{relative.as_posix()}")).hexdigest().upper()


def _resolve_commit(commit: str) -> str:
    result = _run_git("rev-parse", "--verify", "--quiet", f"{commit}^{{commit}}")
    resolved = result.stdout.decode("utf-8").strip()
    if result.returncode != 0 or not resolved:
        raise ValueError(f"snapshot commit {commit} does not resolve to a commit object")
    return resolved


def _is_ancestor(commit: str, head: str) -> bool:
    result = _run_git("merge-base", "--is-ancestor", commit, head)
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    stderr = result.stderr.decode("utf-8", errors="replace").strip()
    raise ValueError(f"git merge-base --is-ancestor {commit} {head} failed: {stderr}")


def read_manifest() -> dict[str, Any]:
    payload: object = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("SOURCE_MANIFEST.json must be an object")
    return payload


def _required_string(block: dict[str, Any], key: str, where: str) -> str:
    value = block.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{where}: missing string field {key!r}")
    return value


def _require_hex(value: str, width: int, where: str, *, uppercase: bool) -> None:
    alphabet = r"[0-9A-F]" if uppercase else r"[0-9a-f]"
    if re.fullmatch(f"{alphabet}{{{width}}}", value) is None:
        case = "uppercase" if uppercase else "lowercase"
        raise ValueError(f"{where} must be an exact {width}-digit {case} hex id")


def _safe_relative(raw: str) -> PurePosixPath:
    if "\\" in raw:
        raise ValueError(f"unsafe path separator in manifest: {raw}")
    relative = PurePosixPath(raw)
    if (
        relative.is_absolute()
        or not relative.parts
        or any(part in ("", ".", "..") for part in relative.parts)
        or ":" in relative.parts[0]
    ):
        raise ValueError(f"unsafe path in manifest: {raw}")
    return relative


def _under_sealed_prefix(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in SEALED_PREFIXES)


def _under_allowed_research_prefix(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in RESEARCH_PREFIXES)


def sealed_prefix_violations(porcelain: str) -> list[str]:
    violations: list[str] = []
    for line in porcelain.splitlines():
        if not line.strip():
            continue
        if len(line) < 4 or line[2] != " ":
            raise ValueError(f"malformed git status record: {line!r}")
        paths = [part.strip().strip('"') for part in line[3:].split(" -> ")]
        if any(_under_sealed_prefix(path) for path in paths):
            violations.append(line)
    return violations


def _live_porcelain() -> str:
    return _git_bytes(
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
        "--ignored=matching",
        "--",
        *SEALED_PATHSPECS,
    ).decode("utf-8")


def _sources(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    sources = manifest.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("manifest must list at least one source")
    for item in sources:
        if not isinstance(item, dict):
            raise ValueError("each source entry must be an object")
    return sources


def verify(manifest: dict[str, Any] | None = None) -> list[str]:
    if manifest is None:
        manifest = read_manifest()
    lines: list[str] = []

    head = _git("rev-parse", "HEAD")
    _require_hex(head, 40, "verification commit", uppercase=False)
    lines.append(f"verification commit: {head}")

    schema = _required_string(manifest, "schema", "manifest")
    if schema != SCHEMA:
        raise ValueError(f"manifest schema is {schema!r}, expected {SCHEMA!r}")

    block = manifest.get("source_snapshot")
    if not isinstance(block, dict):
        raise ValueError("manifest must carry a 'source_snapshot' object")
    snapshot = _required_string(block, "commit", "source snapshot")
    _require_hex(snapshot, 40, "snapshot commit", uppercase=False)
    resolved = _resolve_commit(snapshot)
    if resolved != snapshot:
        raise ValueError(f"snapshot commit {snapshot} resolved to {resolved}")
    if not _is_ancestor(snapshot, head):
        raise ValueError(
            f"snapshot commit {snapshot} is not an ancestor of HEAD {head}"
        )
    wanted_tree = _required_string(block, "tree", "source snapshot")
    _require_hex(wanted_tree, 40, "snapshot tree", uppercase=False)
    actual_tree = _git("rev-parse", f"{snapshot}^{{tree}}")
    if actual_tree != wanted_tree:
        raise ValueError(
            f"snapshot tree mismatch: {snapshot} carries tree {actual_tree}, "
            f"manifest records {wanted_tree}"
        )
    relation = "HEAD itself" if snapshot == head else "an ancestor of HEAD"
    lines.append(f"snapshot commit: {snapshot} tree {actual_tree} ({relation})")

    for item in _sources(manifest):
        relative = _safe_relative(_required_string(item, "path", "source"))
        path = relative.as_posix()
        role = _required_string(item, "role", f"source {relative}")
        if role == "sealed input":
            if not _under_sealed_prefix(path):
                raise ValueError(f"sealed input is not under a sealed prefix: {relative}")
        elif role == "research input":
            if not _under_allowed_research_prefix(path):
                raise ValueError(f"research input is not under an allowed prefix: {relative}")
        else:
            raise ValueError(f"unknown source role {role!r} for {relative}")
        wanted = _required_string(item, "sha256", "source")
        _require_hex(wanted, 64, f"sha256 for {relative}", uppercase=True)
        for label, revision in (("snapshot", snapshot), ("HEAD", head)):
            actual = _sha256_git_blob(revision, relative)
            if actual != wanted:
                raise ValueError(
                    f"hash mismatch for {relative} at {label} {revision}: "
                    f"expected {wanted}, got {actual}"
                )
        lines.append(f"pin: {relative} {wanted} ({role}; at snapshot and HEAD)")

    moved = _git_bytes("diff", "--name-only", "-z", snapshot, head, "--", *SEALED_PATHSPECS)
    names = sorted(part.decode("utf-8") for part in moved.split(b"\0") if part)
    if names:
        raise ValueError(
            "tracked sealed paths differ between the snapshot and HEAD:\n  "
            + "\n  ".join(names)
        )
    lines.append("sealed prefixes unchanged between snapshot and HEAD")

    violations = sealed_prefix_violations(_live_porcelain())
    if violations:
        raise ValueError(
            "worktree carries files under a sealed prefix:\n  " + "\n  ".join(violations)
        )
    lines.append("sealed prefixes clean: " + " ".join(SEALED_PATHSPECS))
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify seventh_constructor source manifest.")
    args = parser.parse_args()
    try:
        lines = verify()
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
