"""Pins of the boundary derivation.

The seed and every frozen prediction must have the declared bytes in the
working tree, index, HEAD, and every reachable commit that touched the path.
The history check refuses a shallow clone rather than presenting a partial
history as a complete one.  Byte-stable files must also be marked ``-text``
so the same check means the same thing on Windows and POSIX.  Receipts refuse
CR bytes.  Exit 1 with the offending source on any drift.
"""

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
    "challenge1/PREDICTIONS.md": (
        "7cf17e56fffb4e45d4100750010265582fa921fabeed7fb1b84aa798f6e56dc7"
    ),
    "challenge2/PREDICTIONS.md": (
        "95f9371b030b8df64b4842a5df7be695d9e7f1b2311a300e78d915a701c16474"
    ),
    "challenge3/PREDICTIONS.md": (
        "27057895c47e5bd718b0ea8e51689f3325cef78102c912c6feea8e913a7e7755"
    ),
    "challenge4/PREDICTIONS.md": (
        "42371f458e23ce89885a76c542863c112482c0ca6b4f1d9ff6a058b3c21f2041"
    ),
    "challenge5/PREDICTIONS.md": (
        "b3aab18d8e5a0700e563862ef7a884248badefbc7c653df0e00097044e3d99de"
    ),
    "continuation/stage1/PREDICTIONS.md": (
        "ac401dafbfa5072f04b6ab532992eae41391f87b6fe4441592b86804c4bf8313"
    ),
    "continuation/stage2/PREDICTIONS.md": (
        "f4b3ebf85ad0176352647a606e8dd856674fb153d89e10e17d48f4734cf26f06"
    ),
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(spec: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "show", spec], cwd=ROOT, capture_output=True
    )
    return proc.stdout if proc.returncode == 0 else None


def history(rel: str) -> list[str]:
    proc = subprocess.run(
        ["git", "rev-list", "--reverse", "HEAD", "--", f"{REL}/{rel}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in proc.stdout.splitlines() if line]


def text_is_unset(rel: str, source: str) -> bool:
    options: list[str] = []
    if source == "index":
        options.append("--cached")
    elif source == "HEAD":
        options.append("--source=HEAD")
    elif source != "working tree":
        raise ValueError(f"unknown attribute source: {source}")
    proc = subprocess.run(
        ["git", "check-attr", *options, "text", "--", f"{REL}/{rel}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout.rstrip().endswith(": text: unset")


def attribute_problems(rel: str, kind: str) -> list[str]:
    return [
        f"{source} attributes: {rel} is {kind} but is not marked -text"
        for source in ("working tree", "index", "HEAD")
        if not text_is_unset(rel, source)
    ]


def check(rel: str, want: str) -> list[str]:
    problems: list[str] = []
    path = HERE / rel
    if not path.is_file():
        problems.append(f"working copy of {rel} is missing")
    else:
        working = path.read_bytes()
        if sha(working) != want:
            problems.append(f"working copy of {rel}: {sha(working)} wanted {want}")
    indexed = git_bytes(f":{REL}/{rel}")
    if indexed is None:
        problems.append(f"{rel} is not present in the index")
    elif sha(indexed) != want:
        problems.append(f"index copy of {rel}: {sha(indexed)} wanted {want}")
    committed = git_bytes(f"HEAD:{REL}/{rel}")
    if committed is None:
        problems.append(f"{rel} is not committed at HEAD")
    elif sha(committed) != want:
        problems.append(f"HEAD copy of {rel}: {sha(committed)} wanted {want}")
    for commit in history(rel):
        historical = git_bytes(f"{commit}:{REL}/{rel}")
        if historical is None:
            problems.append(f"history {commit[:12]} has no {rel}")
        elif sha(historical) != want:
            problems.append(
                f"history {commit[:12]} copy of {rel}: "
                f"{sha(historical)} wanted {want}"
            )
    problems.extend(attribute_problems(rel, "byte-pinned"))
    return problems


def main() -> int:
    problems: list[str] = []
    shallow = subprocess.run(
        ["git", "rev-parse", "--is-shallow-repository"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    if shallow != "false":
        problems.append("repository history is shallow; frozen-history audit is incomplete")
    problems.extend(check("SEED.md", SEED_SHA256))
    for rel, want in FROZEN.items():
        problems.extend(check(rel, want))
    for receipt in sorted((HERE / "receipts").glob("*.json")):
        if b"\r" in receipt.read_bytes():
            problems.append(f"{receipt.name} contains CR bytes")
        rel = receipt.relative_to(HERE).as_posix()
        problems.extend(attribute_problems(rel, "byte-stable"))
    problems.extend(attribute_problems("lean/axioms.txt", "byte-stable"))
    if history("FREEZE.md"):
        print("note: committed FREEZE.md marker; pre-freeze source scan is retired")
    for p in problems:
        print(f"FAIL: {p}")
    if problems:
        return 1
    print(f"pins ok: seed {SEED_SHA256[:12]} and {len(FROZEN)} frozen prediction file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
