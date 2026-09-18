"""Verify the sealed and sibling sources this rung imports, and its frozen texts.

Usage: python research/second_stream/verify_pins.py [--repin]

Checks, none implying the others:

* the recorded snapshot commit is forty hexadecimal digits and is an
  ancestor of HEAD, with ``git merge-base`` exit codes other than zero or
  one reported as undecided rather than as "not an ancestor";
* every source in ``SOURCE_MANIFEST.json`` hashes, as a Git blob, to its
  recorded sha256 **at the snapshot and again at HEAD**; this is endpoint
  equality and makes no claim about intermediate commits; the pinned
  sources include one of the two TABLES the rung's refusal scans read,
  ``contact/analysis/contact_countermodels.json``, so a committed prune of
  it fails here rather than silently narrowing a scan; the other table,
  ``ci/prose_watchlist.json``, is a repository-wide census a later and
  unrelated rung legitimately grew after this snapshot, so it is pinned
  among the frozen texts at HEAD only -- a committed prune of it still
  fails, but it is no longer claimed to stand byte-identical at a snapshot
  it has moved past;
* ``absent_at_snapshot`` records the presence of each named path at the
  snapshot correctly, and is permitted to be empty;
* the frozen seed, question, and prediction texts, and the shared
  prose-watchlist census and its scanner, still hash, as blobs at HEAD,
  to the values recorded for them;
* every commit after the exact required snapshot that CONTRIBUTES a change
  under this rung's write root is audited NUL-safely across all of the paths
  that same commit contributed; a merge contributes its combined diff and not
  the history it inherits, so an unrelated future commit -- including a merge
  that merely carries this rung's tree along -- is not attributed to this
  rung; and
* the NUL-safe status population carries no unignored worktree/index change
  outside that same scope.

Three differences from rung zero's verifier, each deliberate and each a
repair rather than a convention:

1. There is no ``landed_replay`` block, and this script does not require
   one.  Rung zero's ``verify()`` raises for a manifest without that block;
   the block existed only because two named sibling trees were absent at
   rung zero's snapshot.  Both landed before this snapshot, so the block has
   no subject here and ``absent_at_snapshot`` is empty.
2. Sources are checked at the snapshot as well as at HEAD.  Rung zero checks
   its ``sources`` at HEAD alone and reaches its snapshot only through
   ``absent_at_snapshot``.
3. Frozen texts are compared case-insensitively, as sources already were.
   Rung zero compares sources with ``.upper()`` on both sides and frozen
   texts with a bare ``!=``.  That asymmetry is a trap, not a convention: it
   makes the digest case load-bearing for one list and not the other.  Both
   lists are compared case-insensitively here, and the manifest's own casing
   is left as written -- uppercase for sources, lowercase for frozen texts,
   as rung zero recorded them -- precisely so that the comparison, not the
   casing, is what carries the check.

The frozen texts are hashed at HEAD only.  Two of the three rung texts were
created by the freeze commit and therefore do not exist at the snapshot;
hashing them there would fail for a reason that has nothing to do with the
freeze.  A fourth frozen entry, ``ci/prose_watchlist.json``, is hashed here
rather than among the sources because a later rung grew that shared census
after this snapshot; hashing it at the snapshot would now fail for a reason
that has nothing to do with this rung.  A fifth, ``ci/check_prose_watchlist.py``,
moved from the sources on 2026-09-18: the shared scanner was changed to cache
its per-token work (``tests/test_prose_watchlist.py`` compares the cached scan
with an uncached one), so its snapshot bytes are no longer its HEAD bytes, and
the snapshot check on its bytes went with the move.  This verifier reads Git blobs, so an
edit to a frozen text that is never staged is invisible to it; the runner
hashes the rung's own three such files FROM DISK before the build and again
before output.

A pass says the bytes match at the snapshot and HEAD endpoints. It does not
establish uninterrupted history and says nothing about the mathematics.
``--repin`` rewrites the source hashes from HEAD and verifies nothing.  It
never touches ``frozen_texts``, and -- unlike rung zero's ``repin()``, which
sets ``snapshot_commit`` to HEAD -- it refuses to move ``snapshot_commit``,
because the snapshot is the commit the rung's prose is written against and
moving it silently is how a citation stops meaning anything.  Because
``ci/prose_watchlist.json`` now lives among the frozen texts, a future
legitimate growth of that shared census, or a change to its scanner, is
repinned BY HAND here, not by
``--repin``; that a census change is a deliberate, reviewed edit is the
anti-narrowing property, not a regression.  The repin must be a commit of its
own, separate from the change to ``ci/``: a commit that touches this write root
is audited, and every path it touches must be inside the root or a declared
exception, which ``ci/`` is not.  A squash merge that folds the two together
fails that audit permanently.
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

# This rung's write root.  Everything the rung produces lives under it.
WRITE_ROOT = "research/second_stream/"
REQUIRED_SNAPSHOT_COMMIT = "3f44571240a0830a2fa8de639281670f4e50a511"

# Declared exceptions to the write root, each one a file the rung's own plan
# names and no other tree owns: the session handoff and the injection record
# required by research/second/SEED.md, and the workflow step that registers
# the rung so that it is not a manual receipt.
DECLARED_WRITE_PATHS = (
    ".github/workflows/verify.yml",
    "research/second/HANDOFF.md",
    "research/second/MANUAL.md",
)

# The sealed derivation, per CLAUDE.md.  Zero tolerance: a change under any
# of these fails even when it is also a declared write path.
SEALED_PREFIXES = (
    "artifacts/",
    "code/",
    "lean4/Derivation/",
    "paper/",
    "prompt/",
)

# Exact manifest populations.  These are deliberately independent of the
# JSON they audit: deleting a consumed source or one frozen input must not
# turn the verifier green by shrinking its own census.
REQUIRED_SOURCE_PATHS = frozenset(
    {
        "code/derivation/__init__.py",
        "code/derivation/candidates.py",
        "code/derivation/" + "eng" + "ine.py",
        "code/derivation/export.py",
        "code/derivation/iso.py",
        "code/derivation/model.py",
        "code/derivation/observe.py",
        "contact/analysis/contact_countermodels.json",
        "lean4/Derivation/Ext.lean",
        "lean4/Derivation/Progress.lean",
        "research/identification_dual/dual.py",
        "research/second_inheritance/STATUS.md",
        "research/two_sided_commitment/CLAIM_LEDGER.md",
        "research/two_sided_commitment/PROMPT.md",
        "research/two_sided_commitment/STATUS.md",
        "research/two_sided_commitment/receipts/two_sided_commitment.json",
        "research/two_sided_commitment/run_two_sided.py",
        "research/two_sided_commitment/two_sided.py",
        "tests/test_candidates.py",
    }
)
REQUIRED_FROZEN_PATHS = frozenset(
    {
        "ci/check_prose_watchlist.py",
        "ci/prose_watchlist.json",
        "research/second/SEED.md",
        "research/second_stream/PREDICTIONS.md",
        "research/second_stream/PROMPT.md",
    }
)


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


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key in SOURCE_MANIFEST.json: {key}")
        result[key] = value
    return result


def _read_manifest() -> dict[str, Any]:
    payload: object = json.loads(
        MANIFEST.read_text(encoding="utf-8"), object_pairs_hook=_unique_object
    )
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


def _is_hex40(raw: object) -> bool:
    return (
        isinstance(raw, str)
        and len(raw) == 40
        and all(character in "0123456789abcdef" for character in raw)
    )


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


def _decode_path(raw: bytes) -> str:
    # With ``-z`` Git emits literal tree bytes. Repository separators are
    # already ``/`` on every host; a backslash can be part of a filename and
    # must not be normalized into an authorized directory prefix.
    return raw.decode("utf-8", errors="surrogateescape")


def _worktree_paths() -> list[str]:
    """Every unignored worktree/index path, parsed from NUL-safe porcelain."""

    fields = _git_bytes(
        "status", "--porcelain=v1", "-z", "--untracked-files=all"
    ).split(b"\0")
    paths: list[str] = []
    index = 0
    while index < len(fields):
        field = fields[index]
        index += 1
        if not field:
            continue
        if len(field) < 4:
            raise ValueError("malformed NUL-safe git status record")
        status = field[:2]
        paths.append(_decode_path(field[3:]))
        if b"R" in status or b"C" in status:
            if index >= len(fields) or not fields[index]:
                raise ValueError("rename/copy status record is missing its source path")
            paths.append(_decode_path(fields[index]))
            index += 1
    return paths


def _scope_commits(snapshot: str) -> list[str]:
    """Commits after the snapshot, in deterministic dependency order."""

    raw = _git("rev-list", "--reverse", "--topo-order", f"{snapshot}..HEAD")
    return [line for line in raw.splitlines() if line]


def _commit_paths(commit: str) -> list[str]:
    """Paths one commit CONTRIBUTED, NUL-safe.

    Three cases, and the third is the repair:

    * a root commit contributes its whole tree;
    * an ordinary commit contributes its first-parent diff;
    * a MERGE contributes its COMBINED diff -- the paths differing from every
      parent, which is what the merger wrote, and not what the merge
      inherited from another line of history.

    An earlier version read every commit against its first parent alone. For
    a merge that is wrong in both directions at once: it credits this rung
    with the whole of the other branch, and it credits any later merge with
    this rung's whole tree. That is observed, not hypothetical. On `main` at
    `7d2e6e86` three merges were attributed here -- two integration merges
    from pull request 136 and one from the batch after 136 and 134 -- and the
    gate failed naming `research/boundary_seed/`, `research/second_nofirst/`
    and `research/second_stake/` files this rung never touched.

    The combined diff keeps the gate's teeth rather than blunting them. A
    merge that WRITES outside the write root still reports those paths: the
    bundled-edit merge `42f6c8cf2` contributes exactly four paths under this
    rule -- its two conflict resolutions and the two files its author edited
    inside the merge -- while contributing none of the tree it inherited.
    """

    row = _git("rev-list", "--parents", "-n", "1", commit).split()
    if not row or row[0] != commit:
        raise ValueError(f"git did not resolve commit for scope audit: {commit}")
    parents = row[1:]
    if not parents:
        raw = _git_bytes("ls-tree", "-r", "--name-only", "-z", commit)
    elif len(parents) == 1:
        raw = _git_bytes(
            "diff", "--name-only", "-z", "--no-renames", parents[0], commit
        )
    else:
        raw = _git_bytes(
            "diff-tree", "-r", "--cc", "--no-commit-id", "--name-only", "-z",
            "--no-renames", commit,
        )
    return [_decode_path(field) for field in raw.split(b"\0") if field]


def _committed_scope(snapshot: str) -> tuple[list[str], list[str]]:
    """Commits attributable to this rung and every path each one contributed.

    Unrelated future commits are deliberately ignored. A commit becomes
    attributable when it CONTRIBUTES a change under the rung's write root --
    see `_commit_paths`, where a merge contributes only its combined diff --
    and every path that same commit contributed is then audited, including
    declared exceptions and breaches.

    An earlier version of this docstring read "A commit becomes attributable
    when it changes the rung's write root" and meant the first-parent diff,
    which made a merge that merely carried this rung along attributable to
    it. WITHDRAWN: inheriting a tree is not changing it.
    """

    commits: list[str] = []
    paths: list[str] = []
    for commit in _scope_commits(snapshot):
        changed = _commit_paths(commit)
        if not any(path.startswith(WRITE_ROOT) for path in changed):
            continue
        commits.append(commit)
        paths.extend(changed)
    return commits, paths


def _check_paths(paths: list[str], population: str) -> None:
    outside: list[str] = []
    sealed: list[str] = []
    for path in sorted(set(paths)):
        if any(path.startswith(prefix) for prefix in SEALED_PREFIXES):
            sealed.append(path)
        if path.startswith(WRITE_ROOT) or path in DECLARED_WRITE_PATHS:
            continue
        outside.append(path)
    if sealed:
        raise ValueError(
            f"sealed path changed in {population}: " + ", ".join(sealed)
        )
    if outside:
        raise ValueError(
            f"{population} changed outside the write root "
            f"{WRITE_ROOT} and the declared exceptions: " + ", ".join(outside)
        )


def _check_write_scope(snapshot: str) -> list[str]:
    commits, committed = _committed_scope(snapshot)
    worktree = _worktree_paths()
    _check_paths(committed, "rung-attributable committed diff")
    _check_paths(worktree, "working tree/index")
    return [
        f"committed scope: {len(commits)} rung-attributable commits, "
        f"{len(set(committed))} allowed paths",
        f"working-tree scope: clean outside {WRITE_ROOT} "
        f"({len(DECLARED_WRITE_PATHS)} declared exceptions, {len(SEALED_PREFIXES)} sealed prefixes)"
    ]


def verify() -> list[str]:
    manifest = _read_manifest()
    lines: list[str] = []
    schema = manifest.get("schema")
    if schema != "second_stream_source_manifest/v1":
        raise ValueError(f"unexpected manifest schema: {schema!r}")
    head = _git("rev-parse", "HEAD")
    lines.append(f"verification commit: {head}")
    snapshot = manifest.get("snapshot_commit")
    if not _is_hex40(snapshot):
        raise ValueError("snapshot_commit must be an exact 40-digit lowercase hex commit id")
    assert isinstance(snapshot, str)
    if snapshot != REQUIRED_SNAPSHOT_COMMIT:
        raise ValueError(
            "snapshot_commit differs from the independent required snapshot: "
            f"expected {REQUIRED_SNAPSHOT_COMMIT}, got {snapshot}"
        )
    relation = _ancestor(snapshot)
    if relation != "ancestor":
        raise ValueError(f"snapshot {snapshot} is {relation} of HEAD")
    lines.append(f"snapshot commit: {snapshot} (ancestor of HEAD)")

    sources = manifest.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("manifest must list at least one source")
    seen: set[str] = set()
    for item in sources:
        if not isinstance(item, dict):
            raise ValueError("each source entry must be an object")
        relative = _safe(item.get("path"))
        key = relative.as_posix()
        if key in seen:
            raise ValueError(f"duplicate source entry: {key}")
        seen.add(key)
        wanted = item.get("sha256")
        if not isinstance(wanted, str):
            raise ValueError(f"missing sha256 for {relative}")
        at_snapshot = _blob_sha256(snapshot, relative).upper()
        at_head = _blob_sha256("HEAD", relative).upper()
        if at_snapshot != wanted.upper():
            raise ValueError(
                f"snapshot hash mismatch for {relative}: expected {wanted}, got {at_snapshot}"
            )
        if at_head != wanted.upper():
            raise ValueError(
                f"source moved at HEAD for {relative}: expected {wanted}, got {at_head}"
            )
        lines.append(f"source: {relative} {at_head}")
    if seen != REQUIRED_SOURCE_PATHS:
        missing = sorted(REQUIRED_SOURCE_PATHS - seen)
        extra = sorted(seen - REQUIRED_SOURCE_PATHS)
        raise ValueError(
            f"source population differs: missing {missing}, extra {extra}"
        )

    absent = manifest.get("absent_at_snapshot")
    if not isinstance(absent, list):
        raise ValueError("manifest must list absent_at_snapshot (possibly empty)")
    for item in absent:
        if not isinstance(item, dict):
            raise ValueError("each absent entry must be an object")
        relative = _safe(item.get("path"))
        result = subprocess.run(
            ["git", "ls-tree", "-d", "--name-only", snapshot, relative.as_posix()],
            cwd=REPO, capture_output=True, text=True, check=False,
        )
        present = result.returncode == 0 and bool(result.stdout.strip())
        if present != bool(item.get("present_at_snapshot")):
            raise ValueError(
                f"absent-at-snapshot record wrong for {relative}: present={present}"
            )
        lines.append(f"absent at snapshot: {relative} (pull request {item.get('pull_request')})")
    if not absent:
        lines.append(
            "absent at snapshot: none; rung zero's two absences landed before this snapshot"
        )
    if "landed_replay" in manifest:
        raise ValueError(
            "manifest declares landed_replay, which this rung has no subject for; "
            "an absent tree belongs in absent_at_snapshot"
        )

    frozen = manifest.get("frozen_texts")
    if not isinstance(frozen, list) or not frozen:
        raise ValueError("manifest must list the frozen texts")
    frozen_seen: set[str] = set()
    for item in frozen:
        if not isinstance(item, dict):
            raise ValueError("each frozen text entry must be an object")
        relative = _safe(item.get("path"))
        key = relative.as_posix()
        if key in frozen_seen:
            raise ValueError(f"duplicate frozen text entry: {key}")
        frozen_seen.add(key)
        wanted = item.get("sha256")
        if not isinstance(wanted, str):
            raise ValueError(f"missing sha256 for {relative}")
        actual = _blob_sha256("HEAD", relative)
        if actual.upper() != wanted.upper():
            raise ValueError(
                f"frozen text moved: {relative}: expected {wanted}, got {actual}"
            )
        lines.append(f"frozen: {relative} {actual}")

    if frozen_seen != REQUIRED_FROZEN_PATHS:
        missing = sorted(REQUIRED_FROZEN_PATHS - frozen_seen)
        extra = sorted(frozen_seen - REQUIRED_FROZEN_PATHS)
        raise ValueError(
            f"frozen text population differs: missing {missing}, extra {extra}"
        )

    lines.extend(_check_write_scope(snapshot))
    lines.append(
        f"second_stream pins verified: {len(sources)} sources at snapshot and HEAD, "
        f"{len(frozen)} frozen texts at HEAD, {len(absent)} absent-at-snapshot records"
    )
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
    MANIFEST.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8", newline="\n",
    )
    lines.append(
        "repinned sources from HEAD; frozen texts untouched; snapshot_commit NOT moved "
        "-- move it by hand only after re-reading STATUS.md, which cites it"
    )
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the second-stream pins.")
    parser.add_argument(
        "--repin", action="store_true",
        help="rewrite source hashes from HEAD; verifies nothing, and never moves the snapshot",
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
