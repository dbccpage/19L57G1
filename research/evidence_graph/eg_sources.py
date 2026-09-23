"""Immutable source access and resolving spans. AuthorityEffect: None."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import gzip
import json
from pathlib import Path
import re
import subprocess
from typing import Any, TypedDict

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
FREEZE_COMMIT = "1d4d1aee64091751357cf2e9735deab9f677adca"
FROZEN_FILES = ("SCHEMA.json", "input.json", "source_population.json")
HEX40 = re.compile(r"[0-9a-f]{40}")


class SourceRef(TypedDict):
    snapshot: str
    path: str
    blob: str
    file_sha256: str
    start_line: int
    end_line: int
    span_sha256: str


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def read_object(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    value: Any = json.loads(gzip.decompress(raw) if path.suffix == ".gz" else raw)
    if not isinstance(value, dict):
        raise ValueError(f"OBJECT_REQUIRED: {path.name}")
    return value


def git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=False)
    if result.returncode:
        raise ValueError(f"GIT_READ_FAILED: {' '.join(args)}: {result.stderr.decode('utf-8', 'replace').strip()}")
    return result.stdout


@dataclass(frozen=True)
class Blob:
    path: str
    mode: str
    blob: str
    size: int

    def record(self) -> dict[str, str | int]:
        return {"path": self.path, "mode": self.mode, "blob": self.blob, "size": self.size}


def tree_blobs(repo: Path, snapshot: str) -> list[Blob]:
    if not HEX40.fullmatch(snapshot):
        raise ValueError("SNAPSHOT_INVALID")
    result: list[Blob] = []
    for row in git(repo, "ls-tree", "-r", "-l", "-z", snapshot).split(b"\0"):
        if not row:
            continue
        metadata, name = row.split(b"\t", 1)
        mode, kind, blob, size = metadata.decode("ascii").split()
        path = name.decode("utf-8")
        if kind != "blob" or mode not in {"100644", "100755"}:
            raise ValueError(f"SOURCE_KIND_UNSUPPORTED: {path}: {mode} {kind}")
        if path.startswith("/") or ".." in path.split("/"):
            raise ValueError(f"SOURCE_PATH_INVALID: {path}")
        result.append(Blob(path, mode, blob, int(size)))
    if not result:
        raise ValueError("SOURCE_POPULATION_EMPTY")
    return sorted(result, key=lambda item: item.path)


class Snapshot:
    """A fixed, independently enumerated Git tree, never a mutable path view."""

    def __init__(self, repo: Path, snapshot: str, population: dict[str, Any] | None = None) -> None:
        self.repo = repo
        self.snapshot = snapshot
        blobs = tree_blobs(repo, snapshot)
        self.files = {item.path: item for item in blobs}
        self.cache: dict[str, bytes] = {}
        self.line_cache: dict[str, list[bytes]] = {}
        self.digest_cache: dict[str, str] = {}
        if population is not None:
            if population.get("snapshot") != snapshot or population.get("files") != [b.record() for b in blobs]:
                raise ValueError("SOURCE_POPULATION_MISMATCH")
            if population.get("tree") != git(repo, "rev-parse", snapshot + "^{tree}").decode().strip():
                raise ValueError("SOURCE_TREE_MISMATCH")
        ancestry = subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", snapshot, "HEAD"], capture_output=True)
        if ancestry.returncode == 1:
            raise ValueError("SOURCE_SNAPSHOT_NOT_ANCESTOR")
        if ancestry.returncode:
            raise ValueError("SOURCE_ANCESTRY_UNAVAILABLE")

    def preload(self, paths: list[str]) -> None:
        pending = sorted({self.files[path].blob for path in paths if self.files[path].blob not in self.cache})
        if not pending:
            return
        result = subprocess.run(["git", "-C", str(self.repo), "cat-file", "--batch"],
                                input=("\n".join(pending) + "\n").encode("ascii"), capture_output=True)
        if result.returncode:
            raise ValueError("SOURCE_BATCH_READ_FAILED")
        offset = 0
        for expected in pending:
            end = result.stdout.find(b"\n", offset)
            if end < 0:
                raise ValueError("SOURCE_BATCH_HEADER_MISSING")
            fields = result.stdout[offset:end].decode("ascii").split()
            if len(fields) != 3 or fields[:2] != [expected, "blob"]:
                raise ValueError(f"SOURCE_BATCH_OBJECT_MISMATCH: {expected}")
            length = int(fields[2])
            raw = result.stdout[end + 1:end + 1 + length]
            if len(raw) != length or result.stdout[end + 1 + length:end + 2 + length] != b"\n":
                raise ValueError("SOURCE_BATCH_TRUNCATED")
            actual = hashlib.sha1(b"blob " + str(length).encode() + b"\0" + raw).hexdigest()
            if actual != expected:
                raise ValueError("SOURCE_BATCH_DIGEST_MISMATCH")
            self.cache[expected] = raw
            offset = end + length + 2
        if offset != len(result.stdout):
            raise ValueError("SOURCE_BATCH_EXTRA_OUTPUT")

    def raw(self, path: str) -> bytes:
        if path not in self.files:
            raise ValueError(f"SOURCE_MISSING: {path}")
        self.preload([path])
        return self.cache[self.files[path].blob]

    def text(self, path: str) -> str:
        raw = self.raw(path)
        if b"\0" in raw:
            raise ValueError(f"SOURCE_NOT_TEXT: {path}")
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError(f"SOURCE_NOT_UTF8: {path}") from error

    def reference(self, path: str, start: int = 1, end: int | None = None) -> SourceRef:
        raw = self.raw(path)
        if path not in self.line_cache:
            self.line_cache[path] = raw.splitlines(keepends=True)
            self.digest_cache[path] = digest(raw)
        lines = self.line_cache[path]
        if not lines:
            raise ValueError(f"SOURCE_EMPTY_SPAN: {path}")
        stop = len(lines) if end is None else end
        if type(start) is not int or type(stop) is not int or not 1 <= start <= stop <= len(lines):
            raise ValueError(f"SOURCE_SPAN_INVALID: {path}:{start}:{stop}")
        return {"snapshot": self.snapshot, "path": path, "blob": self.files[path].blob,
                "file_sha256": self.digest_cache[path], "start_line": start, "end_line": stop,
                "span_sha256": digest(b"".join(lines[start - 1:stop]))}

    def resolve(self, reference: SourceRef) -> str:
        expected = self.reference(reference["path"], reference["start_line"], reference["end_line"])
        if reference != expected:
            raise ValueError(f"SOURCE_REFERENCE_MISMATCH: {reference['path']}")
        return b"".join(self.line_cache[reference["path"]][reference["start_line"] - 1:reference["end_line"]]).decode("utf-8")

    def drift(self, head: str = "HEAD") -> list[dict[str, str]]:
        current = {row.path: row.blob for row in tree_blobs(self.repo, git(self.repo, "rev-parse", head).decode().strip())}
        return [{"path": path, "snapshot_blob": row.blob, "head_blob": current.get(path, "MISSING")}
                for path, row in sorted(self.files.items()) if current.get(path) != row.blob]


def verify_freeze(repo: Path = REPO, here: Path = HERE) -> None:
    for name in FROZEN_FILES:
        recorded = git(repo, "show", f"{FREEZE_COMMIT}:research/evidence_graph/{name}")
        if (here / name).read_bytes() != recorded:
            raise ValueError(f"FROZEN_INPUT_CHANGED: {name}")


def load_snapshot(repo: Path = REPO, here: Path = HERE) -> Snapshot:
    verify_freeze(repo, here)
    config = read_object(here / "input.json")
    return Snapshot(repo, str(config["source_snapshot"]), read_object(here / str(config["population_file"])))
