"""Verify SOURCE_MANIFEST.json: every pinned read-only source is
byte-identical at the snapshot and at HEAD, the snapshot is an exact
40-digit id and an ancestor of HEAD, the frozen native PROMPT.md still
matches its recorded hash, and PREDICTIONS.md matches the last recorded
freeze.  Exit 0 on success, 1 with a named failure otherwise.
AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import hashlib
import json
import re
import subprocess
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


def main() -> int:
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
    for path, want in sorted(manifest["pins"].items()):
        for rev in (snap, "HEAD"):
            try:
                got = git("rev-parse", f"{rev}:{path}")
            except RuntimeError:
                print(f"FAIL: {path} missing at {rev}")
                failures += 1
                continue
            if got != want:
                print(f"FAIL: {path} blob at {rev} is {got}, pinned {want}")
                failures += 1
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
    if failures:
        return 1
    print(
        f"pins clean: {len(manifest['pins'])} sources at snapshot and HEAD;"
        f" native PROMPT.md frozen; {len(freezes)} predictions freeze(s) recorded"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
