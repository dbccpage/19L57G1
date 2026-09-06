"""Validate the one-time source freeze, not its mathematical stopping claims.

The marker is a deterministic manifest of its sole parent, avoiding a self-hash.
The marker commit changes only the marker. Every later source snapshot, index,
and working tree must preserve that source; only comparison.md may be added.
Ignored build products are outside the tracked source census. Untracked source
is refused, not silently excluded. A filename alone never retires isolation.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

ROOT = Path(__file__).resolve().parents[2]
REL = "research/boundary_seed"
MARKER = f"{REL}/FREEZE.md"
COMPARISON = f"{REL}/comparison.md"


def git(root: Path, *args: str, data: bytes | None = None) -> bytes:
    proc = subprocess.run(
        ["git", "--no-replace-objects", *args], cwd=root, input=data, capture_output=True, check=False
    )
    if proc.returncode:
        raise ValueError(
            f"git {' '.join(args)}: {proc.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return proc.stdout


def paths(data: bytes) -> list[str]:
    return [part.decode("utf-8") for part in data.split(b"\0") if part]


@dataclass(frozen=True)
class Blob:
    mode: str
    oid: str


def tree(root: Path, ref: str) -> dict[str, Blob]:
    """Independent path/mode population, limited to this write root."""
    out: dict[str, Blob] = {}
    folded: set[str] = set()
    for record in git(root, "ls-tree", "-r", "-z", ref, "--", REL).split(b"\0"):
        if not record:
            continue
        header, raw_path = record.split(b"\t", 1)
        mode, kind, oid = header.decode("ascii").split()
        path = raw_path.decode("utf-8")
        if (
            not path.startswith(REL + "/")
            or any(part in ("", ".", "..") for part in path.split("/"))
            or any(c in path for c in "\\:")
            or any(ord(c) < 32 for c in path)
            or path.casefold() in folded
        ):
            raise ValueError(f"{ref}: noncanonical or colliding source path {path!r}")
        if kind != "blob" or mode not in ("100644", "100755"):
            raise ValueError(f"{ref}:{path}: source must be a regular Git blob, got {mode}")
        folded.add(path.casefold())
        out[path] = Blob(mode, oid)
    return out


def blobs(root: Path, identifiers: list[str]) -> dict[str, bytes]:
    """Read exact Git bytes in one process, checking the independent batch frame."""
    unique = list(dict.fromkeys(identifiers))
    if not unique:
        return {}
    raw = git(root, "cat-file", "--batch", data=("\n".join(unique) + "\n").encode("ascii"))
    pos = 0
    out: dict[str, bytes] = {}
    for wanted in unique:
        end = raw.index(b"\n", pos)
        header = raw[pos:end].decode("ascii").split()
        if len(header) != 3 or header[:2] != [wanted, "blob"]:
            raise ValueError(f"Git batch frame for {wanted}: unexpected header {header}")
        size = int(header[2])
        pos = end + 1
        if size < 0 or raw[pos + size : pos + size + 1] != b"\n":
            raise ValueError(f"Git batch frame for {wanted}: invalid size or delimiter")
        out[wanted] = raw[pos : pos + size]
        pos += size + 1
    if pos != len(raw):
        raise ValueError("Git batch frame: unexpected trailing bytes")
    return out


def marker_bytes(root: Path, source: str) -> bytes:
    """Canonical manifest of every regular source blob at the exact parent SHA."""
    resolved = git(root, "rev-parse", f"{source}^{{commit}}").decode("ascii").strip()
    if source != resolved:
        raise ValueError("FREEZE.md source must be an exact full commit identifier")
    population = tree(root, source)
    if not population:
        raise ValueError("FREEZE.md source population is empty")
    for forbidden in (MARKER, COMPARISON):
        if forbidden in population:
            raise ValueError(f"{source}:{forbidden}: must not exist in the source parent")
    attr = git(root, "check-attr", f"--source={source}", "text", "--", MARKER)
    if not attr.rstrip().endswith(b": text: unset"):
        raise ValueError("FREEZE.md must be marked -text at its source parent")
    content = blobs(root, [blob.oid for blob in population.values()])
    rows = [
        {
            "path": path.removeprefix(REL + "/"),
            "mode": blob.mode,
            "bytes": len(content[blob.oid]),
            "sha256": hashlib.sha256(content[blob.oid]).hexdigest(),
        }
        for path, blob in sorted(population.items())
    ]
    payload = {
        "schema": "boundary-source-freeze-v1",
        "authority_effect": "None",
        "write_root": REL,
        "source_commit": source,
        "byte_domain": "Git blob bytes, not checkout line endings",
        "exclusions": ["FREEZE.md describes its parent; ignored generated files are not source"],
        "files": rows,
    }
    return (
        "# Source freeze\n\nAuthorityEffect: None.\n\n"
        "This manifest establishes source custody only, not the stopping conditions,\n"
        "a theorem, independent discovery, or authority. Only comparison.md may be\n"
        "added after this dedicated marker commit; defects it reveals remain OPEN.\n\n"
        "```json\n" + json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True)
        + "\n```\n"
    ).encode("utf-8")


def changed_local_paths(root: Path) -> list[str]:
    changed: set[str] = set()
    for args in (
        ("diff", "--cached", "--name-only", "--no-renames", "-z", "HEAD", "--", REL),
        ("diff", "--name-only", "--no-renames", "-z", "--", REL),
        ("ls-files", "--others", "--exclude-standard", "-z", "--", REL),
    ):
        changed.update(paths(git(root, *args)))
    return sorted(changed)


def local_source_problems(
    root: Path, baseline: dict[str, Blob], *, allow_comparison: bool,
) -> list[str]:
    """Inspect index and file bytes independently of Git's dirty-path flags."""
    problems: list[str] = []
    indexed: dict[str, Blob] = {}
    for record in git(root, "ls-files", "--stage", "-z", "--", REL).split(b"\0"):
        if not record:
            continue
        header, raw_path = record.split(b"\t", 1)
        mode, oid, stage = header.decode("ascii").split()
        path = raw_path.decode("utf-8")
        if mode not in ("100644", "100755") or stage != "0":
            problems.append(f"INDEX:{path}: source is not a resolved regular blob")
        indexed[path] = Blob(mode, oid)
    allowed = {COMPARISON} if allow_comparison else set()
    for path in sorted(set(baseline) | set(indexed)):
        if path not in allowed and baseline.get(path) != indexed.get(path):
            problems.append(f"INDEX:{path}: source changed after freeze or before generation")
    working: list[str] = []
    for path, blob in sorted(baseline.items()):
        local = root / path
        if local.is_symlink() or not local.is_file():
            problems.append(f"working:{path}: source missing or not a regular file")
            continue
        # Windows does not represent the executable bit; it remains checked in
        # the independent index census. Other hosts also check filesystem mode.
        mode = blob.mode if os.name == "nt" else (
            "100755" if local.stat().st_mode & stat.S_IXUSR else "100644"
        )
        if mode != blob.mode:
            problems.append(f"working:{path}: executable mode changed")
        working.append(path)
    if working:
        # C-quoted UTF-8 path lines; no shell expansion and no per-file process.
        inputs = ("\n".join(json.dumps(path, ensure_ascii=False) for path in working) + "\n").encode()
        hashes = git(root, "hash-object", "--stdin-paths", data=inputs).decode("ascii").splitlines()
        if len(hashes) != len(working):
            raise ValueError("working source hash population differs from its path census")
        for path, oid in zip(working, hashes, strict=True):
            if oid != baseline[path].oid:
                problems.append(f"working:{path}: source changed after freeze or before generation")
    for path in paths(git(root, "ls-files", "--others", "--exclude-standard", "-z", "--", REL)):
        if path not in allowed:
            problems.append(f"untracked:{path}: source changed after freeze or before generation")
    return problems


@dataclass(frozen=True)
class FreezeAudit:
    commit: str | None
    problems: tuple[str, ...]

    @property
    def frozen(self) -> bool:
        return self.commit is not None and not self.problems


def audit(root: Path = ROOT, *, working: bool = True) -> FreezeAudit:
    """Fail closed for a malformed marker, incomplete history, or source revision."""
    problems: list[str] = []
    freeze: str | None = None
    try:
        graft_path = Path(git(root, "rev-parse", "--git-path", "info/grafts").decode().strip())
        if not graft_path.is_absolute():
            graft_path = root / graft_path
        if graft_path.exists():
            raise ValueError("FREEZE.md: legacy Git graft file prevents exact-history custody")
        if git(root, "rev-parse", "--is-shallow-repository").strip() != b"false":
            raise ValueError("FREEZE.md: shallow history cannot establish a one-time source freeze")
        additions = git(
            root, "log", "--full-history", "--no-renames", "--diff-filter=A",
            "--format=%H", "HEAD", "--", MARKER,
        ).decode("ascii").splitlines()
        if not additions:
            if git(root, "log", "--full-history", "--format=%H", "HEAD", "--", COMPARISON).strip():
                problems.append("comparison.md appears in history before a committed freeze")
            if working:
                for path in changed_local_paths(root):
                    if path in (MARKER, COMPARISON):
                        problems.append(f"{path}: uncommitted file cannot retire source isolation")
            return FreezeAudit(None, tuple(problems))
        if len(additions) != 1:
            raise ValueError(f"FREEZE.md: expected one creation commit, found {len(additions)}")
        freeze = additions[0]
        parents = git(root, "rev-list", "--parents", "-n", "1", freeze).decode("ascii").split()[1:]
        if len(parents) != 1:
            raise ValueError(f"FREEZE.md {freeze}: marker commit must have exactly one parent")
        source = parents[0]
        changed = paths(git(root, "diff", "--name-only", "--no-renames", "-z", source, freeze))
        if changed != [MARKER]:
            problems.append(f"FREEZE.md {freeze}: dedicated commit must change only {MARKER}: {changed}")
        if git(root, "log", "--full-history", "--format=%H", source, "--", COMPARISON).strip():
            problems.append("comparison.md appears in source history before the freeze")
        expected = marker_bytes(root, source)
        frozen_tree = tree(root, freeze)
        marker = frozen_tree.get(MARKER)
        if marker is None or marker.mode != "100644":
            raise ValueError(f"FREEZE.md {freeze}: marker must be a nonexecutable regular file")
        if blobs(root, [marker.oid])[marker.oid] != expected:
            problems.append(f"FREEZE.md {freeze}: bytes differ from the exact complete parent manifest {source}")
        baseline = tree(root, source)
        baseline[MARKER] = marker
        commits = git(
            root, "rev-list", "--reverse", "--full-history",
            f"{freeze}..HEAD", "--", REL,
        ).decode("ascii").splitlines()
        descendants = set(git(
            root, "rev-list", "--ancestry-path", f"{freeze}..HEAD",
        ).decode("ascii").splitlines()) | {freeze, "HEAD"}
        # HEAD is checked even when it did not itself modify the write root.
        commits = list(dict.fromkeys([freeze, *commits, "HEAD"]))
        for commit in commits:
            current = tree(root, commit)
            if commit not in descendants and not current:
                parents = git(root, "rev-list", "--parents", "-n", "1", commit).decode("ascii").split()[1:]
                if any(tree(root, parent) for parent in parents):
                    problems.append(f"{commit}:{REL}: newly reachable history deletes the source root")
                continue
            for path in sorted(set(baseline) | set(current)):
                if path == MARKER and commit not in descendants and path not in current:
                    continue
                if path == COMPARISON:
                    if commit not in descendants and path in current:
                        problems.append(f"{commit}:comparison.md is not descended from the freeze")
                    continue
                if current.get(path) != baseline.get(path):
                    problems.append(f"{commit}:{path}: source changed after freeze")
        if working:
            problems.extend(local_source_problems(root, baseline, allow_comparison=True))
            local_marker = root / MARKER
            if local_marker.is_symlink() or not local_marker.is_file() or local_marker.read_bytes() != expected:
                problems.append("working:FREEZE.md: raw marker bytes differ from the parent manifest")
            comparison = root / COMPARISON
            if comparison.is_symlink() or (comparison.exists() and not comparison.is_file()):
                problems.append("working:comparison.md: comparison must be a regular file")
    except (ValueError, OSError, UnicodeError) as exc:
        problems.append(str(exc))
    return FreezeAudit(freeze, tuple(problems))


def write_marker(root: Path = ROOT) -> None:
    """Generate, but do not commit, the manifest after the source is complete."""
    result = audit(root)
    if result.commit is not None or result.problems:
        raise ValueError("FREEZE.md cannot be generated: " + "; ".join(result.problems or ("already frozen",)))
    changed = changed_local_paths(root)
    if changed:
        raise ValueError(f"FREEZE.md requires committed, clean source; pending paths: {changed}")
    source = git(root, "rev-parse", "HEAD").decode("ascii").strip()
    local_problems = local_source_problems(root, tree(root, source), allow_comparison=False)
    if local_problems:
        raise ValueError("FREEZE.md requires unchanged source: " + "; ".join(local_problems))
    destination = root / MARKER
    rendered = marker_bytes(root, source)
    # Exclusive creation also refuses an ignored, pre-existing marker.
    with destination.open("xb") as stream:
        stream.write(rendered)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="generate a dedicated marker for clean HEAD")
    parser.add_argument("--require-frozen", action="store_true")
    args = parser.parse_args()
    if args.write:
        try:
            write_marker()
        except (ValueError, OSError) as exc:
            print(f"FAIL: {exc}")
            return 1
        print("generated FREEZE.md; source isolation remains active until the dedicated commit is validated")
        return 0
    result = audit()
    for problem in result.problems:
        print(f"FAIL: {problem}")
    if result.problems or (args.require_frozen and not result.frozen):
        if not result.problems:
            print("FAIL: FREEZE.md has not been committed")
        return 1
    print(f"freeze verified: {result.commit}" if result.frozen else "not frozen: source isolation remains active")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
