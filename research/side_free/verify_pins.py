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
   its declared blob digest at the full pinned commit, which must exist and
   be an ancestor of ``HEAD``. Missing sources and unrelated commits fail.
   The former ``--allow-unreachable-pin`` bypass is obsolete and fails
   explicitly; vendored bytes alone do not discharge source provenance.

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


def walk_path(root: object, spec: str) -> object:
    cur = root
    for part in spec.split("."):
        if isinstance(cur, list):
            cur = cur[int(part)]
        elif isinstance(cur, dict):
            cur = cur[part]
        else:
            raise KeyError(part)
    return cur


def check_extracted_values() -> list[str]:
    """Every extracted number must still be what the receipt says at its path."""
    problems: list[str] = []
    receipt = json.loads((HERE / PIN_REL).read_text(encoding="utf-8"))
    meta = json.loads((HERE / "pinned" / "BOUNDARY_PIN.json").read_text(encoding="utf-8"))
    for spec, want in meta["extracted"].items():
        if spec.endswith(".classes.members"):
            continue
        try:
            cur = walk_path(receipt, spec)
        except (KeyError, IndexError, ValueError):
            problems.append(f"BOUNDARY_PIN.json cites {spec}, which the receipt has not")
            continue
        if cur != want:
            problems.append(
                f"BOUNDARY_PIN.json {spec} is {want!r}, the receipt says {cur!r}"
            )
    return problems


def vendored_receipts() -> list[dict[str, object]]:
    manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
    rows = manifest["vendored_receipts"]
    return sorted(rows, key=lambda row: int(str(row["challenge"])))


def check_vendored_receipts() -> list[str]:
    """The four pinned receipts the comparison reads, by bytes alone."""
    problems: list[str] = []
    for row in vendored_receipts():
        rel = str(row["local_path"])
        path = HERE / rel
        if not path.is_file():
            problems.append(f"the vendored receipt {rel} is missing")
            continue
        raw = path.read_bytes()
        if sha(raw) != row["sha256"]:
            problems.append(f"{rel}: sha256 {sha(raw)} wanted {row['sha256']}")
        if len(raw) != row["byte_count"]:
            problems.append(
                f"{rel}: byte count {len(raw)} wanted {row['byte_count']}"
            )
        if b"\r" in raw:
            problems.append(f"{rel} contains CR bytes")
        problems.extend(attribute_problems(rel, "byte-stable"))
    return problems


def check_declared_values() -> list[str]:
    """Every value the comparison declares must be what the pinned bytes say.

    The declaration is keyed CHALLENGE:JSON-PATH.  A hand edit of either side
    fails here by name, which is what makes the comparison's own gate real.
    """
    meta = json.loads((HERE / "pinned" / "BOUNDARY_PIN.json").read_text(encoding="utf-8"))
    declared = meta.get("declared_values")
    if not isinstance(declared, dict):
        return ["BOUNDARY_PIN.json carries no declared_values block"]
    receipts: dict[int, object] = {}
    for row in vendored_receipts():
        path = HERE / str(row["local_path"])
        if path.is_file():
            receipts[int(str(row["challenge"]))] = json.loads(
                path.read_text(encoding="utf-8")
            )
    problems: list[str] = []
    for key, want in sorted(declared.items()):
        head, _, spec = str(key).partition(":")
        try:
            challenge = int(head)
        except ValueError:
            problems.append(f"declared value {key} has no challenge index")
            continue
        if challenge not in receipts:
            problems.append(f"declared value {key} names no vendored receipt")
            continue
        try:
            cur = walk_path(receipts[challenge], spec)
        except (KeyError, IndexError, ValueError):
            problems.append(
                f"declared value {key} names a path the pinned receipt has not"
            )
            continue
        if cur != want:
            problems.append(
                f"declared value {key} is {want!r}, the pinned receipt says {cur!r}"
            )
    return problems


def check_pinned_commit() -> tuple[list[str], list[str]]:
    """Blob digests at the pinned commit.  Returns (problems, notes)."""
    manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
    commit = manifest["pinned_commit"]
    if (
        not isinstance(commit, str)
        or len(commit) != 40
        or any(char not in "0123456789abcdef" for char in commit)
    ):
        return ([f"SOURCE_MANIFEST.json pinned_commit is not a full commit SHA: {commit!r}"], [])
    probe = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=ROOT, capture_output=True
    )
    if probe.returncode != 0:
        return ([f"the pinned commit {commit} is unavailable in this clone"], [])
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
        cwd=ROOT,
        capture_output=True,
    )
    if ancestry.returncode != 0:
        detail = "is not an ancestor of HEAD" if ancestry.returncode == 1 else "ancestry check failed"
        return ([f"the pinned commit {commit} {detail}"], [])
    if not manifest["sources"]:
        return (["SOURCE_MANIFEST.json has no pinned sources"], [])
    problems: list[str] = []
    for source in manifest["sources"]:
        data = git_bytes(f"{commit}:{source['path']}")
        if data is None:
            problems.append(f"{commit} has no {source['path']}")
        elif sha(data) != source["sha256"]:
            problems.append(
                f"{source['path']} at {commit}: {sha(data)} wanted {source['sha256']}"
            )
    notes = [] if problems else [
        f"PASS: {len(manifest['sources'])} blobs at {commit}, an ancestor of HEAD"
    ]
    return (problems, notes)


def main(argv: list[str]) -> int:
    if "--allow-unreachable-pin" in argv:
        print("FAIL: obsolete --allow-unreachable-pin; source provenance cannot be skipped")
        return 1
    if argv:
        print(f"FAIL: unknown arguments: {' '.join(argv)}")
        return 1
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
    problems.extend(check_vendored_receipts())
    problems.extend(check_extracted_values())
    problems.extend(check_declared_values())
    commit_problems, commit_notes = check_pinned_commit()
    problems.extend(commit_problems)
    notes.extend(commit_notes)
    for name in ("pinned/boundary_challenge3.json", "pinned/BOUNDARY_PIN.json"):
        problems.extend(attribute_problems(name, "byte-stable"))
    receipts = sorted((HERE / "receipts").glob("*.json"))
    if not receipts:
        problems.append("no receipt is present; run run_side_free.py")
    # The rendered document is byte-compared beside the receipts, so it is
    # held to the same CR refusal and the same -text attribute.
    for receipt in [*receipts, HERE / "COMPARISON.md"]:
        if not receipt.is_file():
            problems.append(f"{receipt.name} is missing; run run_comparison.py")
            continue
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
    meta = json.loads((HERE / "pinned" / "BOUNDARY_PIN.json").read_text(encoding="utf-8"))
    declared = meta.get("declared_values") or {}
    print(
        f"pins ok: {len(FROZEN)} frozen file(s), the vendored pin "
        f"{PIN_SHA256[:12]} at {PIN_BYTES} bytes, "
        f"{len(vendored_receipts())} vendored receipt(s), "
        f"{len(declared)} declared value(s), {len(receipts)} receipt(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
