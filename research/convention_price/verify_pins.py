"""Verify SOURCE_MANIFEST.json against the snapshot this tree was derived
against, and report what has moved since.

PROVENANCE, which fails: every pinned read-only source is byte-identical at
the snapshot, the snapshot is an exact 40-digit id and an ancestor of HEAD,
the frozen native PROMPT.md still matches its recorded hash, and
PREDICTIONS.md matches the last recorded freeze.

CURRENCY, reported on stdout as DRIFT lines and NOT a failure: a pinned
source that differs between the snapshot and HEAD.  Pass --require-current
to fail on drift instead.

2026-09-22, by the author's ruling: this file used to fail when a pinned
source differed at HEAD.  The snapshot blob is fixed history, so no repin
could satisfy both sides once another tree's pinned file changed, and this
check was red for that reason alone.  That HEAD-side failure is withdrawn;
the claim this tree makes is about its snapshot.

Exit 0 on success, 1 with a named failure otherwise.
AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import hashlib
import json
import re
import subprocess
from collections.abc import Sequence
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args], capture_output=True, text=True, cwd=REPO, check=False
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {proc.stderr.strip()}")
    return proc.stdout.strip()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify this tree's source pins.")
    parser.add_argument(
        "--require-current",
        action="store_true",
        help="also fail when a pinned source has moved between the snapshot and HEAD",
    )
    args = parser.parse_args(argv)
    manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text("ascii"))
    snap = manifest["snapshot_commit"]
    if not re.fullmatch(r"[0-9a-f]{40}", snap):
        print(f"FAIL: snapshot commit must be an exact 40-digit id: {snap}")
        return 1
    try:
        git("merge-base", "--is-ancestor", snap, "HEAD")
    except RuntimeError:
        print(f"FAIL: snapshot {snap} is not an ancestor of HEAD")
        return 1
    failures = 0
    drift: list[str] = []
    for path, want in sorted(manifest["pins"].items()):
        try:
            got = git("rev-parse", f"{snap}:{path}")
        except RuntimeError:
            print(f"FAIL: {path} missing at the snapshot")
            failures += 1
        else:
            if got != want:
                print(f"FAIL: {path} blob at the snapshot is {got}, pinned {want}")
                failures += 1
        try:
            at_head = git("rev-parse", f"HEAD:{path}")
        except RuntimeError as exc:
            if path in git("ls-tree", "-r", "--name-only", "HEAD", "--", path).splitlines():
                print(f"FAIL: could not read {path} at HEAD: {exc}")
                failures += 1
            else:
                drift.append(f"{path} is absent at HEAD")
        else:
            if at_head != want:
                drift.append(f"{path} blob at HEAD is {at_head}, pinned {want}")
    prompt_hash = hashlib.sha256((HERE / "PROMPT.md").read_bytes()).hexdigest()
    if prompt_hash != manifest["prompt_native_sha256"]:
        print(
            f"FAIL: PROMPT.md hash {prompt_hash} differs from frozen"
            f" {manifest['prompt_native_sha256']}"
        )
        failures += 1
    freezes = manifest["predictions_freezes"]
    if not freezes:
        print("FAIL: no predictions freeze recorded")
        failures += 1
    else:
        pred_hash = hashlib.sha256((HERE / "PREDICTIONS.md").read_bytes()).hexdigest()
        if pred_hash != freezes[-1]:
            print(
                f"FAIL: PREDICTIONS.md hash {pred_hash} differs from the last"
                f" recorded freeze {freezes[-1]}"
            )
            failures += 1
    if drift and args.require_current:
        for line in drift:
            print(f"FAIL: {line}")
        failures += len(drift)
    if failures:
        return 1
    for line in drift:
        print(f"DRIFT: {line}")
    print(
        f"pins clean: {len(manifest['pins'])} sources at the snapshot;"
        f" native PROMPT.md frozen; {len(freezes)} predictions freeze(s) recorded"
    )
    print(f"drift since the snapshot: {len(drift)} pinned path(s) moved at HEAD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
