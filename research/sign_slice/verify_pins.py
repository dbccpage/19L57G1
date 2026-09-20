"""Verify SOURCE_MANIFEST.json: every pinned read-only source is
byte-identical at the snapshot and at HEAD, the snapshot is an exact
40-digit id and an ancestor of HEAD, and the frozen native PROMPT.md
still matches its recorded hash.  Exit 0 on success, 1 with a named
failure otherwise.  AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

# 2026-09-19: the computation and tests read this external input. The former
# consultation list also pinned documents that the executable tree never reads.
SOURCE_PATHS = ("contact/analysis/contact_countermodels.json",)


def git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args], capture_output=True, text=True, cwd=REPO, check=False
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {proc.stderr.strip()}")
    return proc.stdout.strip()


def write_manifest() -> int:
    """Regenerate the active input pins without moving the frozen snapshot."""
    path = HERE / "SOURCE_MANIFEST.json"
    manifest = json.loads(path.read_text("ascii"))
    snap = manifest["snapshot_commit"]
    if not re.fullmatch(r"[0-9a-f]{40}", snap):
        raise ValueError("snapshot commit must be an exact 40-digit id")
    git("merge-base", "--is-ancestor", snap, "HEAD")
    prompt_hash = hashlib.sha256((HERE / "PROMPT.md").read_bytes()).hexdigest()
    if prompt_hash != manifest["prompt_native_sha256"]:
        raise ValueError("PROMPT.md differs from its frozen hash")
    pins = {}
    for relative in SOURCE_PATHS:
        pinned = git("rev-parse", f"{snap}:{relative}")
        if git("rev-parse", f"HEAD:{relative}") != pinned:
            raise ValueError(f"consumed input changed since the snapshot: {relative}")
        pins[relative] = pinned
    manifest["pins"] = pins
    manifest["purpose"] = (
        "read-only external input consumed by the executable tests; "
        "2026-09-19: consultation-only pins withdrawn after import and file-read "
        "tracing; the original snapshot and native prompt freeze are retained"
    )
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                    encoding="ascii", newline="\n")
    print(f"wrote {len(pins)} active input pin; snapshot and native prompt unchanged")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    if args.write:
        try:
            return write_manifest()
        except (KeyError, OSError, RuntimeError, ValueError) as error:
            print(f"FAIL: {error}")
            return 1
    manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text("ascii"))
    if set(manifest["pins"]) != set(SOURCE_PATHS):
        print(f"FAIL: PIN_POPULATION: expected {list(SOURCE_PATHS)}")
        return 1
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
    if failures:
        return 1
    print(f"pins clean: {len(manifest['pins'])} sources at snapshot and HEAD;"
          " native PROMPT.md frozen")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
