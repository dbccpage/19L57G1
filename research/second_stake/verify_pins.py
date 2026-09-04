"""Verify source blobs, quoted spans, and the two frozen rung texts."""

from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
from pathlib import PurePosixPath
from types import ModuleType
from typing import Mapping, cast

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
MANIFEST = HERE / "SOURCE_MANIFEST.json"
FREEZE_COMMIT = "d4d5830e53d33e98404cb502ac2e694a871cb091"
FROZEN_POLICY: dict[PurePosixPath, bool] = {
    PurePosixPath("research/second_stake/PROMPT.md"): True,
    PurePosixPath("research/second_stake/PREDICTIONS.md"): False,
}
RUNTIME_MODULE_PATHS: dict[str, PurePosixPath] = {
    "derivation": PurePosixPath("code/derivation/__init__.py"),
    "derivation.candidates": PurePosixPath("code/derivation/candidates.py"),
    "derivation.engine": PurePosixPath("code/derivation/engine.py"),
    "derivation.export": PurePosixPath("code/derivation/export.py"),
    "derivation.iso": PurePosixPath("code/derivation/iso.py"),
    "derivation.model": PurePosixPath("code/derivation/model.py"),
    "derivation.observe": PurePosixPath("code/derivation/observe.py"),
    "dual": PurePosixPath("research/identification_dual/dual.py"),
    "two_sided": PurePosixPath("research/two_sided_commitment/two_sided.py"),
    "generation": PurePosixPath("research/second_stake/generation.py"),
    "observables": PurePosixPath("research/second_stake/observables.py"),
    "rules": PurePosixPath("research/second_stake/rules.py"),
    "run_stake": PurePosixPath("research/second_stake/run_stake.py"),
    "verify_pins": PurePosixPath("research/second_stake/verify_pins.py"),
}
PINNED_RUNTIME_MODULES = frozenset(
    {
        "derivation",
        "derivation.candidates",
        "derivation.engine",
        "derivation.export",
        "derivation.iso",
        "derivation.model",
        "derivation.observe",
        "dual",
        "two_sided",
    }
)

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


def runtime_manifest(data: JsonObject) -> dict[str, tuple[PurePosixPath, bool]]:
    """Parse the closed runtime-module census from the provenance manifest."""

    result: dict[str, tuple[PurePosixPath, bool]] = {}
    for entry in entries(data.get("runtime_modules"), "runtime_modules"):
        name = entry.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError("runtime module name must be non-empty text")
        if name in result:
            raise ValueError(f"duplicate runtime module: {name}")
        pinned = entry.get("pinned_source")
        if not isinstance(pinned, bool):
            raise ValueError(f"runtime module pinned_source must be boolean: {name}")
        result[name] = (safe_path(entry.get("path")), pinned)
    expected = {
        name: (path, name in PINNED_RUNTIME_MODULES)
        for name, path in RUNTIME_MODULE_PATHS.items()
    }
    if result != expected:
        raise ValueError("runtime module manifest differs from the closed census")
    return result


def normalized_source(value: bytes) -> bytes:
    """Normalize checkout line endings to the LF bytes stored in Git blobs."""

    return value.replace(b"\r\n", b"\n")


def verify_runtime_origins(modules: Mapping[str, ModuleType]) -> list[str]:
    """Bind every executed project module to its declared repository source."""

    data = manifest()
    declared = runtime_manifest(data)
    if set(modules) != set(declared):
        raise ValueError("runtime module population differs from the closed census")
    source_hashes = {
        safe_path(entry.get("path")): expected_sha(entry)
        for entry in entries(data.get("sources"), "sources")
    }
    lines: list[str] = []
    for name, (path, pinned) in declared.items():
        module_file = getattr(modules[name], "__file__", None)
        if not isinstance(module_file, str):
            raise ValueError(f"runtime module has no file origin: {name}")
        actual = pathlib.Path(module_file).resolve()
        expected = (REPO / pathlib.Path(*path.parts)).resolve()
        if str(actual).casefold() != str(expected).casefold():
            raise ValueError(
                f"runtime module origin differs: {name}: expected {path}, got {actual}"
            )
        if pinned:
            wanted = source_hashes.get(path)
            if wanted is None:
                raise ValueError(f"pinned runtime module lacks a source pin: {name}")
            if digest(normalized_source(actual.read_bytes())) != wanted:
                raise ValueError(f"runtime source bytes differ from the pin: {name}")
        lines.append(f"runtime: {name} {path}")
    return lines


def verify() -> list[str]:
    data = manifest()
    if data.get("schema") != "second_stake_source_manifest/v2":
        raise ValueError("source manifest schema must be second_stake_source_manifest/v2")
    freeze = data.get("freeze_commit")
    if freeze != FREEZE_COMMIT:
        raise ValueError(f"freeze_commit must be the original freeze {FREEZE_COMMIT}")
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
    freeze_relation = subprocess.run(
        ["git", "merge-base", "--is-ancestor", freeze, "HEAD"],
        cwd=REPO,
        capture_output=True,
        check=False,
    )
    if freeze_relation.returncode != 0:
        raise ValueError(
            f"freeze is not a verified ancestor of HEAD: git exit {freeze_relation.returncode}"
        )
    lines.append(f"freeze: {freeze} (ancestor of HEAD)")
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
    frozen_entries: dict[PurePosixPath, JsonObject] = {}
    for entry in entries(data.get("frozen_texts"), "frozen_texts"):
        path = safe_path(entry.get("path"))
        if path in frozen_entries:
            raise ValueError(f"duplicate frozen text: {path}")
        frozen_entries[path] = entry
    if set(frozen_entries) != set(FROZEN_POLICY):
        raise ValueError("frozen text manifest differs from the closed freeze population")
    for path, no_digits in FROZEN_POLICY.items():
        entry = frozen_entries[path]
        wanted = expected_sha(entry)
        at_freeze = blob(FREEZE_COMMIT, path)
        if digest(at_freeze) != wanted:
            raise ValueError(f"frozen manifest hash differs from freeze commit: {path}")
        if entry.get("no_digits") is not no_digits:
            raise ValueError(f"frozen no_digits policy differs: {path}")
        disk = REPO / pathlib.Path(*path.parts)
        if not disk.is_file():
            raise ValueError(f"frozen text missing from disk: {path}")
        if digest(disk.read_bytes()) != wanted:
            raise ValueError(f"frozen text moved on disk: {path}")
        if digest(blob("HEAD", path)) != wanted:
            raise ValueError(f"frozen text moved in HEAD: {path}")
        if no_digits and any(
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
    declared_runtime = runtime_manifest(data)
    source_paths = {safe_path(entry.get("path")) for entry in source_entries}
    for name, (path, pinned) in declared_runtime.items():
        if pinned and path not in source_paths:
            raise ValueError(f"pinned runtime module lacks a source pin: {name}")
    lines.append(f"runtime module census: {len(declared_runtime)}")
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
