"""Pins of the side-free control.

Four things are checked, and the difference between them matters.

1. **The two frozen files.**  ``DESIGN.md`` and ``PREDICTIONS.md`` were
   committed alone, before any code of this tree existed.  Their bytes must
   match the digests below in the working tree, the index, ``HEAD``, and every
   reachable commit that touched the path.  A shallow clone is refused rather
   than presented as a complete history.

2. **The vendored pin.**  ``pinned/boundary_challenge3.json`` must have the
   declared sha256, git blob id and byte count, and must carry no CR byte.
   These three are recomputable from the bytes with no git at all, so they
   hold in any clone.

3. **The pinned commit.**  Every file of ``SOURCE_MANIFEST.json`` must have
   its declared blob digest at the pinned commit.  That commit lives on an
   UNMERGED branch which a fresh clone of the remote does not carry, so this
   check can be unavailable.  It is then reported as SKIPPED with the reason
   and the residual named -- never as a pass.  By default an unreachable
   pinned commit FAILS; ``--allow-unreachable-pin`` downgrades it to the
   reported SKIP, and only the CI step passes that flag, with a comment
   saying why.

4. **Byte stability.**  Every receipt and every pinned file refuses CR bytes
   and must be committed ``-text``, so the same check means the same thing on
   Windows and on POSIX.

Exit 1 with the offending source on any drift.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
REL = "research/side_free"

# Frozen before any code of this tree existed; see the commit that carries
# them alone.  Never edited afterwards.
FROZEN: dict[str, str] = {
    "DESIGN.md": "7cd9d5487614e6b542a53371f10f19a1daa2ace7447c5132695b6f1ce4a0880e",
    "PREDICTIONS.md": (
        "24d6bdf5a6a7be653f1dd49d316457e92c43bfe58cebd2cc7a96149e1f517049"
    ),
}

PIN_REL = "pinned/boundary_challenge3.json"
PIN_SHA256 = "e4904075aaa07dd05a2f9d0cba313e77b6eb965a44efecb5cff51864f70a64ab"
PIN_BLOB = "dbb4cce3cdd49d15d0784c2a73bf7afeab9de7a0"
PIN_BYTES = 220518


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def git_bytes(spec: str) -> bytes | None:
    proc = subprocess.run(["git", "show", spec], cwd=ROOT, capture_output=True)
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


def check_frozen(rel: str, want: str) -> list[str]:
    """The bytes must be ``want`` everywhere the file has ever appeared."""
    problems: list[str] = []
    path = HERE / rel
    if not path.is_file():
        problems.append(f"working copy of {rel} is missing")
    elif sha(path.read_bytes()) != want:
        problems.append(
            f"working copy of {rel}: {sha(path.read_bytes())} wanted {want}"
        )
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
                f"history {commit[:12]} copy of {rel}: {sha(historical)} wanted {want}"
            )
    problems.extend(attribute_problems(rel, "frozen"))
    return problems


def check_vendored_pin() -> list[str]:
    """The three digests, recomputable from the bytes with no git at all."""
    problems: list[str] = []
    path = HERE / PIN_REL
    if not path.is_file():
        return [f"the vendored pin {PIN_REL} is missing"]
    raw = path.read_bytes()
    if sha(raw) != PIN_SHA256:
        problems.append(f"{PIN_REL}: sha256 {sha(raw)} wanted {PIN_SHA256}")
    if blob_id(raw) != PIN_BLOB:
        problems.append(f"{PIN_REL}: git blob {blob_id(raw)} wanted {PIN_BLOB}")
    if len(raw) != PIN_BYTES:
        problems.append(f"{PIN_REL}: byte count {len(raw)} wanted {PIN_BYTES}")
    if b"\r" in raw:
        problems.append(f"{PIN_REL} contains CR bytes")
    return problems


def check_extracted_values() -> list[str]:
    """Every extracted number must still be what the receipt says at its path."""
    problems: list[str] = []
    receipt = json.loads((HERE / PIN_REL).read_text(encoding="utf-8"))
    meta = json.loads((HERE / "pinned" / "BOUNDARY_PIN.json").read_text(encoding="utf-8"))
    for spec, want in meta["extracted"].items():
        if spec.endswith(".classes.members"):
            continue
        cur: object = receipt
        try:
            for part in spec.split("."):
                if isinstance(cur, list):
                    cur = cur[int(part)]
                elif isinstance(cur, dict):
                    cur = cur[part]
                else:
                    raise KeyError(part)
        except (KeyError, IndexError, ValueError):
            problems.append(f"BOUNDARY_PIN.json cites {spec}, which the receipt has not")
            continue
        if cur != want:
            problems.append(
                f"BOUNDARY_PIN.json {spec} is {want!r}, the receipt says {cur!r}"
            )
    return problems


def check_pinned_commit(allow_unreachable: bool) -> tuple[list[str], list[str]]:
    """Blob digests at the pinned commit.  Returns (problems, notes)."""
    manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
    commit = manifest["pinned_commit"]
    probe = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=ROOT, capture_output=True
    )
    if probe.returncode != 0:
        message = (
            f"the pinned commit {commit} is unreachable in this clone; it is on "
            f"an unmerged branch that a fresh clone of the remote does not "
            f"carry.  The vendored bytes are still fixed by sha256, git blob id "
            f"and byte count, which need no git at all"
        )
        residual = (
            "RESIDUAL, recorded and not closed: the link from the vendored "
            "bytes to that commit is only as strong as that branch's "
            "reachability here"
        )
        if allow_unreachable:
            return ([], [f"SKIPPED: {message}", residual])
        return ([f"{message} (pass --allow-unreachable-pin to downgrade)"], [residual])
    problems: list[str] = []
    for source in manifest["sources"]:
        data = git_bytes(f"{commit}:{source['path']}")
        if data is None:
            problems.append(f"{commit} has no {source['path']}")
        elif sha(data) != source["sha256"]:
            problems.append(
                f"{source['path']} at {commit}: {sha(data)} wanted {source['sha256']}"
            )
    return (problems, [f"PASS: {len(manifest['sources'])} blobs at {commit}"])


def main(argv: list[str]) -> int:
    allow_unreachable = "--allow-unreachable-pin" in argv
    problems: list[str] = []
    notes: list[str] = []
    shallow = subprocess.run(
        ["git", "rev-parse", "--is-shallow-repository"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    if shallow != "false":
        problems.append(
            "repository history is shallow; the frozen-history audit is incomplete"
        )
    for rel, want in FROZEN.items():
        problems.extend(check_frozen(rel, want))
    problems.extend(check_vendored_pin())
    problems.extend(check_extracted_values())
    commit_problems, commit_notes = check_pinned_commit(allow_unreachable)
    problems.extend(commit_problems)
    notes.extend(commit_notes)
    for name in ("pinned/boundary_challenge3.json", "pinned/BOUNDARY_PIN.json"):
        problems.extend(attribute_problems(name, "byte-stable"))
    receipts = sorted((HERE / "receipts").glob("*.json"))
    if not receipts:
        problems.append("no receipt is present; run run_side_free.py")
    for receipt in receipts:
        if b"\r" in receipt.read_bytes():
            problems.append(f"{receipt.name} contains CR bytes")
        problems.extend(
            attribute_problems(receipt.relative_to(HERE).as_posix(), "byte-stable")
        )
    for note in notes:
        print(f"note: {note}")
    for problem in problems:
        print(f"FAIL: {problem}")
    if problems:
        return 1
    print(
        f"pins ok: {len(FROZEN)} frozen file(s), the vendored pin "
        f"{PIN_SHA256[:12]} at {PIN_BYTES} bytes, {len(receipts)} receipt(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
