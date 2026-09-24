"""Verify the natural-sections tree's source manifest against the repository.

Usage: python research/natural_sections/verify_pins.py

The manifest is ``SOURCE_MANIFEST.json``, in the shape of
``research/primitive_difference_tower/SOURCE_MANIFEST.json``: a source
snapshot ``{commit, tree}``, a hash basis, semantic roots, and one
``{module, path, sha256, role}`` entry per sealed module the Lean package
compiles.  Seven checks, and none of them implies the others:

* the snapshot commit is an exact 40-digit lowercase hex id (never
  ``HEAD``), RESOLVES to a commit object, is an ancestor of the
  verification HEAD (or HEAD itself), and carries the recorded tree;
* every module hashes to its recorded SHA-256 as the Git blob at the
  SNAPSHOT, so the theorems were checked against the sealed sources they
  name; whether a module has moved since is reported (below);
* the module list is EXACTLY the import closure of the semantic roots,
  computed from the ``import Derivation.*`` lines of the snapshot blobs
  and compared in both directions -- a module the package compiles but
  the manifest does not pin fails, and so does a pinned module nothing
  imports;
* each module's path is the sealed path its name denotes, and every
  pinned path is relative, has no ``..``, no backslash, no drive letter,
  and lies under a sealed prefix;
* a tracked path under a sealed prefix that differs between the snapshot
  and HEAD is reported, like a moved module (below);
* the worktree carries nothing under a sealed prefix that is modified,
  untracked, or ignored-but-present (``git status --porcelain
  --untracked-files=all --ignored=matching``): a gitignored bytecode or
  build file inside the seal is a write inside the seal.  This tree's
  own Python never writes bytecode (``sys.dont_write_bytecode`` is set
  before any import), so such a file was written by something else and
  the failure names it (``git clean -fdX code`` removes the usual one);
* the check of the sealed prefixes is a pure function of the porcelain
  text so it can be tested on a synthetic record.

Pins certify the snapshot (2026-09-23, applying the author's ruling of
2026-09-22).  PROVENANCE fails, as listed above.  CURRENCY is printed as
``DRIFT:`` lines, then a ``drift since the snapshot:`` count, and does not
fail: a pinned module that moved or is absent at HEAD, or a tracked sealed
path that differs between the snapshot and HEAD.  ``--require-current``
restores that failure.  This file used to fail on both.  The snapshot blob
is fixed history, so every authorized sealed edit turned it red until a
repin, whatever this tree claimed.

A pass says the inputs matched at the snapshot and nothing sealed was
touched in the worktree.  It
says nothing about the mathematics, and it does not authenticate the
interpreter, Git, or this script.  Nothing in ``.github/workflows`` runs
this script; a pass is a manual receipt.  AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
from pathlib import PurePosixPath
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
MANIFEST_PATH = HERE / "SOURCE_MANIFEST.json"
SCHEMA = "natural_sections_source_manifest/v1"

SEALED_PATHSPECS = ("prompt", "paper", "code", "lean4/Derivation", "artifacts")
SEALED_PREFIXES = tuple(f"{spec}/" for spec in SEALED_PATHSPECS)

_IMPORT = re.compile(rb"(?m)^import\s+(Derivation\.[A-Za-z0-9_.]+)\s*$")


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


def _sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest().upper()


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


def _sealed_diff(snapshot: str, head: str) -> list[str]:
    output = _git_bytes("diff", "--name-only", "-z", snapshot, head, "--", *SEALED_PATHSPECS)
    return sorted(part.decode("utf-8") for part in output.split(b"\0") if part)


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


def module_path(module: str) -> str:
    """The sealed path a ``Derivation.*`` module name denotes."""

    if not re.fullmatch(r"Derivation(\.[A-Za-z0-9_]+)+", module):
        raise ValueError(f"not a sealed module name: {module}")
    return "lean4/" + module.replace(".", "/") + ".lean"


def import_closure(roots: list[str], blob_of: Any) -> dict[str, bytes]:
    """The transitive ``import Derivation.*`` closure of ``roots``.

    ``blob_of(module)`` returns the module's bytes; the closure is read
    from those bytes, never from the checkout.
    """

    closure: dict[str, bytes] = {}
    stack = list(roots)
    while stack:
        module = stack.pop()
        if module in closure:
            continue
        blob = blob_of(module)
        closure[module] = blob
        stack.extend(match.decode("utf-8") for match in _IMPORT.findall(blob))
    return closure


def sealed_prefix_violations(porcelain: str) -> list[str]:
    """Porcelain (v1) records naming a path under a sealed prefix; pure."""

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
        "status", "--porcelain=v1", "--untracked-files=all", "--ignored=matching",
        "--", *SEALED_PATHSPECS,
    ).decode("utf-8")


def _modules(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    modules = manifest.get("modules")
    if not isinstance(modules, list) or not modules:
        raise ValueError("manifest must list at least one module")
    for item in modules:
        if not isinstance(item, dict):
            raise ValueError("each module entry must be an object")
    return modules


def _roots(manifest: dict[str, Any]) -> list[str]:
    roots = manifest.get("semantic_roots")
    if not isinstance(roots, list) or not roots or not all(isinstance(r, str) for r in roots):
        raise ValueError("manifest must list at least one semantic root")
    return list(roots)


def _head_drift(head: str, relative: PurePosixPath, wanted: str) -> list[str]:
    """How a pinned module differs at HEAD, reported rather than failed.

    A path that is tracked at HEAD but cannot be read is still a failure:
    that is a Git read error, not drift.
    """
    try:
        at_head = _sha256(_git_bytes("show", f"{head}:{relative.as_posix()}"))
    except ValueError as exc:
        listed = _git("ls-tree", "-r", "--name-only", head, "--", relative.as_posix())
        if relative.as_posix() in listed.splitlines():
            raise ValueError(f"could not read {relative} at HEAD: {exc}") from exc
        return [f"{relative} is absent at HEAD"]
    if at_head != wanted:
        return [f"{relative} at HEAD is {at_head}, pinned {wanted}"]
    return []


def verify(
    manifest: dict[str, Any] | None = None, *, require_current: bool = False
) -> list[str]:
    """Run every check; raise ``ValueError`` on the first failure."""

    if manifest is None:
        manifest = read_manifest()
    lines: list[str] = []
    drift: list[str] = []

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
    if _resolve_commit(snapshot) != snapshot:
        raise ValueError(f"snapshot commit {snapshot} resolved to a different object")
    if not _is_ancestor(snapshot, head):
        raise ValueError(f"snapshot commit {snapshot} is not an ancestor of HEAD {head}")
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

    pinned: dict[str, str] = {}
    for item in _modules(manifest):
        module = _required_string(item, "module", "module entry")
        relative = _safe_relative(_required_string(item, "path", f"module {module}"))
        if relative.as_posix() != module_path(module):
            raise ValueError(
                f"module/path mismatch: {module} denotes {module_path(module)}, "
                f"manifest says {relative}"
            )
        if not _under_sealed_prefix(relative.as_posix()):
            raise ValueError(f"pinned module is not under a sealed prefix: {relative}")
        wanted = _required_string(item, "sha256", f"module {module}")
        _require_hex(wanted, 64, f"sha256 for {module}", uppercase=True)
        _required_string(item, "role", f"module {module}")
        if module in pinned:
            raise ValueError(f"module pinned twice: {module}")
        actual = _sha256(_git_bytes("show", f"{snapshot}:{relative.as_posix()}"))
        if actual != wanted:
            raise ValueError(
                f"hash mismatch for {relative} at snapshot {snapshot}: "
                f"expected {wanted}, got {actual}"
            )
        drift.extend(_head_drift(head, relative, wanted))
        pinned[module] = wanted
        lines.append(f"pin: {module} {wanted} (at the snapshot)")

    roots = _roots(manifest)
    closure = import_closure(
        roots, lambda module: _git_bytes("show", f"{snapshot}:{module_path(module)}")
    )
    missing = sorted(set(closure) - set(pinned))
    extra = sorted(set(pinned) - set(closure))
    if missing or extra:
        raise ValueError(
            f"module list is not the import closure of {roots}: "
            f"unpinned {missing}, pinned but unreachable {extra}"
        )
    lines.append(f"import closure of {roots}: {len(closure)} module(s), all pinned")

    moved = _sealed_diff(snapshot, head)
    drift.extend(f"sealed path {name} differs between the snapshot and HEAD" for name in moved)
    if drift and require_current:
        raise ValueError(
            "pinned inputs moved between the snapshot and HEAD (--require-current):\n  "
            + "\n  ".join(drift)
        )

    violations = sealed_prefix_violations(_live_porcelain())
    if violations:
        raise ValueError(
            "worktree carries files under a sealed prefix (modified, untracked, "
            "or ignored-but-present; a '!!' record is a bytecode or build file "
            "written under the seal -- remove it, e.g. git clean -fdX code):\n  "
            + "\n  ".join(violations)
        )
    lines.append("sealed prefixes clean: " + " ".join(SEALED_PATHSPECS))
    lines.extend(f"DRIFT: {line}" for line in drift)
    lines.append(
        f"drift since the snapshot: {len(drift)} pinned module(s) or sealed path(s)"
        " moved at HEAD"
    )
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify the natural_sections manifest.")
    parser.add_argument(
        "--require-current",
        action="store_true",
        help="also fail when a pinned module or sealed path has moved between the snapshot and HEAD",
    )
    args = parser.parse_args(argv)
    try:
        lines = verify(require_current=args.require_current)
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
