"""Pins of the boundary derivation: the seed's bytes at HEAD and in the
working tree, and every frozen prediction file.  Also refuses CR bytes in
any receipt.  Exit 1 with the offending name on any drift."""

from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
REL = "research/boundary_seed"

SEED_SHA256 = "ba30bcd600d8232f054f3b4d9a5d03caafaa7442dfd8095643f39cfcea1ad0be"
FROZEN: dict[str, str] = {
    "challenge0/PREDICTIONS.md": (
        "a03ee8127e83603af75c56c4061bcbe9dc1689c3b56b90854148dfb9856cc395"
    ),
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def head_bytes(rel: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "show", f"HEAD:{REL}/{rel}"], cwd=ROOT, capture_output=True
    )
    return proc.stdout if proc.returncode == 0 else None


def check(rel: str, want: str) -> list[str]:
    problems: list[str] = []
    working = (HERE / rel).read_bytes()
    if sha(working) != want:
        problems.append(f"working copy of {rel}: {sha(working)} wanted {want}")
    committed = head_bytes(rel)
    if committed is None:
        problems.append(f"{rel} is not committed at HEAD")
    elif sha(committed) != want:
        problems.append(f"HEAD copy of {rel}: {sha(committed)} wanted {want}")
    return problems


def main() -> int:
    problems = check("SEED.md", SEED_SHA256)
    for rel, want in FROZEN.items():
        problems.extend(check(rel, want))
    for receipt in sorted((HERE / "receipts").glob("*.json")):
        if b"\r" in receipt.read_bytes():
            problems.append(f"{receipt.name} contains CR bytes")
    if (HERE / "FREEZE.md").exists():
        print("note: FREEZE.md exists; the blindness scan is retired")
    for p in problems:
        print(f"FAIL: {p}")
    if problems:
        return 1
    print(f"pins ok: seed {SEED_SHA256[:12]} and {len(FROZEN)} frozen prediction file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
