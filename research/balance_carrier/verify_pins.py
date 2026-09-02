"""Verify SOURCE_MANIFEST.json: every pinned read-only source is
byte-identical at the snapshot and at HEAD; every pinned span (a line
range of a pinned file, hashed as its LF-joined lines with trailing LF)
matches at the snapshot and at HEAD; the snapshot is an exact 40-digit id
and an ancestor of HEAD; no tracked path under a sealed prefix differs
between the snapshot and HEAD; the worktree carries nothing modified or
untracked outside the write root; the frozen native PROMPT.md still
matches its recorded hash; and PREDICTIONS.md matches the last recorded
freeze.  Exit 0 on success, 1 with a named failure otherwise.  A manual
receipt: no CI gate runs this file.  AuthorityEffect: None.
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
WRITE_ROOT = "research/balance_carrier/"
SEALED_PATHSPECS = ("prompt", "paper", "code", "lean4/Derivation", "artifacts")


def git(*args: str) -> bytes:
    proc = subprocess.run(["git", *args], capture_output=True, cwd=REPO, check=False)
    if proc.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)}: {proc.stderr.decode('utf-8', 'replace').strip()}"
        )
    return proc.stdout


def git_text(*args: str) -> str:
    return git(*args).decode("utf-8").strip()


def span_hash(blob: bytes, first: int, last: int) -> str:
    lines = blob.split(b"\n")
    if first < 1 or last < first or last > len(lines):
        raise RuntimeError(f"span {first}-{last} outside the blob's {len(lines)} lines")
    chunk = b"\n".join(lines[first - 1 : last]) + b"\n"
    return hashlib.sha256(chunk).hexdigest()


def outside_write_root(porcelain: str) -> list[str]:
    """Porcelain records naming a path outside the write root; pure."""
    out: list[str] = []
    for line in porcelain.splitlines():
        if not line.strip():
            continue
        paths = [p.strip().strip('"') for p in line[3:].split(" -> ")]
        if any(not p.replace("\\", "/").startswith(WRITE_ROOT) for p in paths):
            out.append(line)
    return out


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
                got = git_text("rev-parse", f"{rev}:{path}")
            except RuntimeError:
                print(f"FAIL: {path} missing at {rev}")
                failures += 1
                continue
            if got != want:
                print(f"FAIL: {path} blob at {rev} is {got}, pinned {want}")
                failures += 1
    for span in manifest["spans"]:
        path = span["path"]
        if path not in manifest["pins"]:
            print(f"FAIL: span path {path} is not itself pinned")
            failures += 1
        for rev in (snap, "HEAD"):
            try:
                blob = git("show", f"{rev}:{path}")
                got = span_hash(blob, int(span["first_line"]), int(span["last_line"]))
            except RuntimeError as exc:
                print(f"FAIL: span {path}:{span['first_line']}-{span['last_line']} at {rev}: {exc}")
                failures += 1
                continue
            if got != span["sha256"]:
                print(
                    f"FAIL: span {path}:{span['first_line']}-{span['last_line']} at {rev}"
                    f" hashes {got}, pinned {span['sha256']}"
                )
                failures += 1
    moved = [
        p
        for p in git("diff", "--name-only", "-z", snap, "HEAD", "--", *SEALED_PATHSPECS)
        .decode("utf-8")
        .split("\0")
        if p
    ]
    if moved:
        print("FAIL: tracked sealed paths differ between the snapshot and HEAD: " + ", ".join(moved))
        failures += 1
    porcelain = git("status", "--porcelain=v1", "--untracked-files=all").decode("utf-8")
    stray = outside_write_root(porcelain)
    if stray:
        print("FAIL: worktree carries changes outside the write root:\n  " + "\n  ".join(stray))
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
        f"pins clean: {len(manifest['pins'])} sources and {len(manifest['spans'])} spans"
        f" at snapshot and HEAD; sealed prefixes unchanged; nothing outside the write"
        f" root; native PROMPT.md frozen; {len(freezes)} predictions freeze(s) recorded"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
