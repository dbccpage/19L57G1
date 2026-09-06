"""Check every pin of research/limit_and_observer, at the snapshot and at HEAD.

Run from the repository root:

    python research/limit_and_observer/verify_pins.py

Pins are sha256 of the **canonical Git blob**, never of the worktree file: the
two differ for every file under ``code/`` and ``lean4/`` in a CRLF checkout
and agree only for ``artifacts/**``.  Recomputing the same way on every
platform is the whole point of declaring the convention once.

Exit 0 on success, 1 on any failure, with the failing object named.

AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys

TREE = "research/limit_and_observer"
MANIFEST = os.path.join(TREE, "SOURCE_MANIFEST.json")
SNAPSHOT_RE = re.compile(r"^[0-9a-f]{40}$")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def git(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args], check=True, stdout=subprocess.PIPE
    ).stdout


def blob_sha256(commit: str, path: str) -> str | None:
    try:
        return hashlib.sha256(git("show", f"{commit}:{path}")).hexdigest()
    except subprocess.CalledProcessError:
        return None


def main() -> None:
    if not os.path.isfile(MANIFEST):
        fail(f"{MANIFEST} is missing; run from the repository root")
    with open(MANIFEST, encoding="utf-8") as fh:
        manifest = json.load(fh)

    snapshot = manifest["snapshot"]
    if not SNAPSHOT_RE.match(snapshot):
        fail("source snapshot commit must be an exact 40-digit lowercase hex id")
    try:
        git("cat-file", "-e", f"{snapshot}^{{commit}}")
    except subprocess.CalledProcessError:
        fail(f"snapshot {snapshot} is not reachable in this repository")
    try:
        git("merge-base", "--is-ancestor", snapshot, "HEAD")
    except subprocess.CalledProcessError:
        fail(f"snapshot {snapshot} is not an ancestor of HEAD")

    problems = 0
    for group in ("frozen", "pins"):
        for path, want in sorted(manifest[group].items()):
            at_snapshot = blob_sha256(snapshot, path)
            at_head = blob_sha256("HEAD", path)
            if at_snapshot is None:
                print(f"FAIL: {path} does not exist at the snapshot")
                problems += 1
                continue
            if at_snapshot != want:
                print(
                    f"FAIL: hash mismatch for {path}\n"
                    f"  wanted   {want}\n  snapshot {at_snapshot}"
                )
                problems += 1
            if at_head != at_snapshot:
                print(
                    f"FAIL: {path} moved between the snapshot and HEAD\n"
                    f"  snapshot {at_snapshot}\n  HEAD     {at_head}"
                )
                problems += 1

    # The frozen texts are frozen, and "frozen" means the bytes on disk too.
    #
    # This check was added because its injection found the hole: appending one
    # byte to PREDICTIONS.md in the worktree left every pin above green,
    # because those compare git objects at the snapshot and at HEAD and never
    # look at the working tree.  A frozen input edited but not committed was
    # invisible.  This is the same custody preflight research/partial_decide
    # runs before rendering its receipt.
    for path in sorted(manifest["frozen"]):
        if not os.path.isfile(path):
            print(f"FAIL: frozen input {path} is missing from the worktree")
            problems += 1
            continue
        with open(path, "rb") as fh:
            on_disk = hashlib.sha256(fh.read()).hexdigest()
        committed = blob_sha256("HEAD", path)
        if on_disk != committed:
            print(
                f"FAIL: frozen input {path} has worktree changes\n"
                f"  on disk   {on_disk}\n  committed {committed}"
            )
            problems += 1

    # Custody: a *tracked* file of this tree modified but not committed
    # means the receipt on disk is not the receipt of the committed tree.
    # Untracked files are not custody failures - a tree being built has
    # plenty of them.
    dirty = git("diff", "--name-only", "HEAD", "--", TREE).decode().strip()
    if dirty:
        print(
            "FAIL: tracked files of research/limit_and_observer have "
            "worktree changes:"
        )
        for line in dirty.splitlines():
            print(f"  {line}")
        problems += 1

    # Receipts carry no CR bytes: .gitattributes marks receipts/** -text, so a
    # CR byte would survive into the committed object and break byte equality
    # on another platform.
    receipts = os.path.join(TREE, "receipts")
    if os.path.isdir(receipts):
        for name in sorted(os.listdir(receipts)):
            full = os.path.join(receipts, name)
            if not os.path.isfile(full):
                continue
            with open(full, "rb") as fh:
                if b"\r" in fh.read():
                    print(f"FAIL: {name} contains CR bytes")
                    problems += 1
    else:
        print(f"FAIL: {receipts} is missing")
        problems += 1

    # The transport attribute must be committed as -text for the frozen texts
    # and the receipts, or a CRLF conversion would break every hash above.
    attrs = git("check-attr", "text", "--",
                os.path.join(TREE, "receipts", "price.json"),
                os.path.join(TREE, "REQUIREMENTS.md")).decode()
    for line in attrs.strip().splitlines():
        if not line.endswith(": unset"):
            print(f"FAIL: transport attribute must be committed as -text: {line}")
            problems += 1

    if problems:
        fail(f"{problems} pin problem(s)")
    print(
        f"limit_and_observer pins clean: "
        f"{len(manifest['pins'])} pinned sources, "
        f"{len(manifest['frozen'])} frozen inputs, snapshot {snapshot[:12]}"
    )


if __name__ == "__main__":
    main()
