"""Verify the S9-obligations tree's source manifest against the repository.

Usage: python research/s9_obligations/verify_pins.py [--repin]

The manifest is ``SOURCE_MANIFEST.json`` (PROMPT.md step 3), in the shape of
``research/primitive_difference_tower/SOURCE_MANIFEST.json``: a source
snapshot ``{commit, tree}``, a hash basis, and one ``{path, sha256, role}``
entry per sealed file this run reads, plus the governing prompt pinned by
its Git blob id.  Six checks, and none of them implies the others:

* the snapshot commit is an exact 40-digit lowercase hex id (never
  ``HEAD``), RESOLVES to a commit object, is an ancestor of the
  verification HEAD (or HEAD itself), and carries the recorded tree.  An
  earlier version checked only the spelling: forty zeroes passed, and a
  reviewer showed it.  A snapshot that does not resolve pins nothing;
* every sealed file this run reads hashes to its recorded SHA-256 as the
  Git blob at the SNAPSHOT and again at HEAD, so the receipts describe the
  inputs they were computed against and those inputs have not moved
  since.  The hash is taken over ``git show <rev>:path`` and is therefore
  independent of checkout line endings;
* the governing prompt has its recorded Git blob id at the snapshot and
  at HEAD (PROMPT.md step 1: stop on drift);
* no tracked path under a sealed prefix differs between the snapshot and
  HEAD, so a sealed file this run did not pin cannot have moved either;
* the worktree carries nothing under a sealed prefix that is modified,
  untracked, or IGNORED-BUT-PRESENT (PROMPT.md step 35): ``git status
  --porcelain=v1 --untracked-files=all --ignored`` over the sealed
  pathspecs must be empty.  Ignored files count: an earlier version
  excluded them, and a reviewer showed that importing
  ``code/derivation/primdiff.py`` wrote ``code/derivation/__pycache__``
  inside the seal with the check still green.  The tree's own Python
  never writes bytecode (``common.py`` sets ``sys.dont_write_bytecode``
  before any sealed module is imported, and the documented commands set
  ``PYTHONDONTWRITEBYTECODE=1``), so a bytecode file under the seal was
  written by something else -- the root test suite, typically -- and the
  failure names it so it can be removed (``git clean -fdX code``).  The
  check is a pure function of the porcelain text so it can be tested
  against a synthetic line without touching a sealed path;
* every pinned path is relative, has no ``..``, no backslash, no drive
  letter, and lies under a sealed prefix.

A pass says the inputs did not move and nothing sealed was touched.  It
says nothing about the mathematics computed from them, and it does not
authenticate the interpreter, Git, or this script.  Nothing in
``.github/workflows`` runs this script; a pass is a manual receipt for the
tree present when it ran.  AuthorityEffect: None.
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
SCHEMA = "s9_obligations_source_manifest/v1"

# The sealed prefixes of CLAUDE.md, as pathspecs and as prefixes.  A
# top-level ``lean4/*.lean`` is outside this check.  The root file
# ``lean4/Derivation.lean`` is inside the seal by the author's ruling of
# 2026-09-18, but this check reads prefixes only and does not cover it.
# (2026-09-21: this comment used to call every top-level file outside the
# seal; that is withdrawn.)
SEALED_PATHSPECS = ("prompt", "paper", "code", "lean4/Derivation", "artifacts")
SEALED_PREFIXES = tuple(f"{spec}/" for spec in SEALED_PATHSPECS)


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
    """Hash the Git blob itself, independent of checkout line endings."""

    return (
        hashlib.sha256(_git_bytes("show", f"{revision}:{relative.as_posix()}"))
        .hexdigest()
        .upper()
    )


def _resolve_commit(commit: str) -> str:
    """The id ``commit`` resolves to as a commit object, or a refusal."""

    result = _run_git("rev-parse", "--verify", "--quiet", f"{commit}^{{commit}}")
    resolved = result.stdout.decode("utf-8").strip()
    if result.returncode != 0 or not resolved:
        raise ValueError(f"snapshot commit {commit} does not resolve to a commit object")
    return resolved


def _is_ancestor(commit: str, head: str) -> bool:
    """Whether ``commit`` is ``head`` or an ancestor of it."""

    result = _run_git("merge-base", "--is-ancestor", commit, head)
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    stderr = result.stderr.decode("utf-8", errors="replace").strip()
    raise ValueError(f"git merge-base --is-ancestor {commit} {head} failed: {stderr}")


def _sealed_diff(snapshot: str, head: str) -> list[str]:
    """Tracked paths under a sealed prefix that differ between two commits."""

    output = _git_bytes(
        "diff", "--name-only", "-z", snapshot, head, "--", *SEALED_PATHSPECS
    )
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


def sealed_prefix_violations(porcelain: str) -> list[str]:
    """Porcelain (v1) lines that name a path under a sealed prefix.

    Pure: takes the text of ``git status --porcelain=v1 --ignored`` and
    returns the offending lines, so the refusal can be tested on a
    synthetic line without any sealed path ever being touched.  A rename
    record names two paths and is refused if either one is sealed.  An
    ignored-file record (``!!``) is a violation like any other: a file
    present under the seal is a write under the seal, whatever
    ``.gitignore`` says about it.
    """

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


def _snapshot_block(manifest: dict[str, Any]) -> dict[str, Any]:
    block = manifest.get("source_snapshot")
    if not isinstance(block, dict):
        raise ValueError("manifest must carry a 'source_snapshot' object")
    return block


def _sources(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    sources = manifest.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("manifest must list at least one source")
    for item in sources:
        if not isinstance(item, dict):
            raise ValueError("each source entry must be an object")
    return sources


def _prompt_block(manifest: dict[str, Any]) -> tuple[PurePosixPath, str]:
    prompt = manifest.get("prompt")
    if not isinstance(prompt, dict):
        raise ValueError("manifest must carry a 'prompt' object")
    path = _safe_relative(_required_string(prompt, "path", "prompt pin"))
    blob = _required_string(prompt, "blob", "prompt pin")
    _require_hex(blob, 40, "prompt blob id", uppercase=False)
    return path, blob


def verify(manifest: dict[str, Any] | None = None) -> list[str]:
    """Run every check; raise ``ValueError`` on the first failure."""

    if manifest is None:
        manifest = read_manifest()
    lines: list[str] = []

    head = _git("rev-parse", "HEAD")
    _require_hex(head, 40, "verification commit", uppercase=False)
    lines.append(f"verification commit: {head}")

    schema = _required_string(manifest, "schema", "manifest")
    if schema != SCHEMA:
        raise ValueError(f"manifest schema is {schema!r}, expected {SCHEMA!r}")

    block = _snapshot_block(manifest)
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

    prompt_path, wanted_blob = _prompt_block(manifest)
    for revision in (snapshot, head):
        actual_blob = _git("rev-parse", f"{revision}:{prompt_path.as_posix()}")
        if actual_blob != wanted_blob:
            raise ValueError(
                f"prompt drift: {prompt_path} is blob {actual_blob} at "
                f"{revision}, pinned {wanted_blob}; stop"
            )
    lines.append(f"prompt: {prompt_path} {wanted_blob} (at snapshot and HEAD)")

    for item in _sources(manifest):
        relative = _safe_relative(_required_string(item, "path", "source"))
        if not _under_sealed_prefix(relative.as_posix()):
            raise ValueError(f"pinned source is not under a sealed prefix: {relative}")
        wanted = _required_string(item, "sha256", "source")
        _require_hex(wanted, 64, f"sha256 for {relative}", uppercase=True)
        _required_string(item, "role", f"source {relative}")
        for label, revision in (("snapshot", snapshot), ("HEAD", head)):
            actual = _sha256_git_blob(revision, relative)
            if actual != wanted:
                raise ValueError(
                    f"hash mismatch for {relative} at {label} {revision}: "
                    f"expected {wanted}, got {actual}"
                )
        lines.append(f"pin: {relative} {wanted} (at snapshot and HEAD)")

    moved = _sealed_diff(snapshot, head)
    if moved:
        raise ValueError(
            "tracked sealed paths differ between the snapshot and HEAD:\n  "
            + "\n  ".join(moved)
        )
    lines.append("sealed prefixes unchanged between snapshot and HEAD")

    violations = sealed_prefix_violations(_live_porcelain())
    if violations:
        raise ValueError(
            "worktree carries files under a sealed prefix (modified, untracked, "
            "or ignored-but-present; a '!!' record is a bytecode or build file "
            "written under the seal -- remove it, e.g. git clean -fdX code):\n  "
            + "\n  ".join(violations)
        )
    lines.append("sealed prefixes clean: " + " ".join(SEALED_PATHSPECS))
    return lines


def repin() -> list[str]:
    """Rewrite recorded hashes and ids from the objects at HEAD.

    Performs NO verification. A repin is a write, and adopting a defect
    as the new baseline is exactly what it would hide -- the injection
    skill names regenerating a receipt under a live injection as the
    single easiest way to turn a real proof into a fake one. Run the
    plain verifier afterwards.
    """

    manifest = read_manifest()
    lines: list[str] = []
    prompt = manifest.get("prompt")
    if not isinstance(prompt, dict):
        raise ValueError("manifest must carry a 'prompt' object")
    prompt_path = _safe_relative(_required_string(prompt, "path", "prompt pin"))
    old_blob = prompt.get("blob")
    new_blob = _git("rev-parse", f"HEAD:{prompt_path.as_posix()}")
    if old_blob != new_blob:
        lines.append(f"reblobbed: {prompt_path} {old_blob} -> {new_blob}")
    prompt["blob"] = new_blob
    for item in _sources(manifest):
        relative = _safe_relative(_required_string(item, "path", "source"))
        old = item.get("sha256")
        new = _sha256_git_blob("HEAD", relative)
        if old != new:
            lines.append(f"rehashed: {relative} {old} -> {new}")
        item["sha256"] = new
    head = _git("rev-parse", "HEAD")
    manifest["source_snapshot"] = {
        "commit": head,
        "tree": _git("rev-parse", "HEAD^{tree}"),
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    lines.append(
        "repinned; PREFLIGHT.md and common.SNAPSHOT_COMMIT must be revised by "
        "hand before trusting it"
    )
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the S9-obligations manifest.")
    parser.add_argument(
        "--repin",
        action="store_true",
        help="rewrite recorded hashes from the objects at HEAD; verifies nothing",
    )
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
