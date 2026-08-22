"""Verify the blind-restart kernel and its scoring key.

Usage: python research/blind_restart/verify_pins.py [--repin]

Three checks, and none of them implies the others:

* every artifact the key reads still hashes to its recorded SHA-256, so
  the key describes the exports it was written against;
* every field the key asserts actually resolves in those artifacts, so
  the key cannot cite a value that was renamed or removed. A hash pin
  proves the source did not move; it does not prove the key names
  anything real. That distinction is taken from the sibling export
  surface, where it is the check the other sibling lacks;
* the kernel does not contain the answers.

The third is the one this tree exists for. A staged prompt that states
its own expected results is a leading question, and a solver agreeing
with it is not evidence. The proposal this tree answers asked for "typed
holes, never prefilled answers" and then tabulated the answers; the
principle was right and the table broke it. Here the principle is a gate.

The leak rule is deliberately blunt, because a subtle rule would be
arguable and this one is not: the kernel carries no decimal digit and no
standalone truth or absence token, in any case. Every expected value in
the key is a number, a truth value, an absence, or a list of numbers, so
none of them can be written in the kernel without tripping it. The cost
is that the kernel spells its quantities as words. That is a cheap price
for a mechanical check.

Nothing here judges a solver's reasoning, and a pass is not evidence
about the mathematics. See STATUS.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
from pathlib import PurePosixPath
from typing import Any

from scoring_key import STAGES, artifact_names, expected

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
PINS_PATH = HERE / "SOURCE_PINS.json"
KERNEL_PATH = HERE / "KERNEL.md"

_DIGIT = re.compile(r"[0-9]")

# The three JSON literals an expected value can be written as. The
# English word "none" was in this set briefly and is deliberately out of
# it: a packet encodes an absent successor as ``null``, so "none" bought
# no coverage while failing on ordinary prose. A rule that fires on
# sentences it has no business reading gets suppressed by whoever meets
# it next, and then the real rule is gone too.
_TRUTH_TOKEN = re.compile(r"(?<![A-Za-z])(true|false|null)(?![A-Za-z])", re.I)


def _git_bytes(*args: str) -> bytes:
    result = subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, check=False
    )
    if result.returncode != 0:
        raise ValueError(
            f"git {' '.join(args)} failed: "
            f"{result.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return result.stdout


def _git(*args: str) -> str:
    return _git_bytes(*args).decode("utf-8").strip()


def _sha256_git_blob(revision: str, relative: PurePosixPath) -> str:
    """Hash a canonical Git blob, independent of checkout line endings."""

    return (
        hashlib.sha256(_git_bytes("show", f"{revision}:{relative.as_posix()}"))
        .hexdigest()
        .upper()
    )


def _read_pins() -> dict[str, Any]:
    payload: object = json.loads(PINS_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("SOURCE_PINS.json must be an object")
    return payload


def _required_string(block: dict[str, Any], key: str, where: str) -> str:
    value = block.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{where}: missing string field {key!r}")
    return value


def _safe_relative(raw: str) -> PurePosixPath:
    relative = PurePosixPath(raw)
    if relative.is_absolute() or any(part == ".." for part in relative.parts):
        raise ValueError(f"unsafe path in pins: {raw}")
    return relative


def check_leak(kernel_text: str) -> list[str]:
    """Fail if the kernel could hand a solver any expected value.

    Runs the blunt token rules first. They are what makes the value scan
    below sound: once no digit and no truth token survives in the kernel,
    a value scan cannot be defeated by spacing or formatting.
    """

    findings: list[str] = []
    for number, line in enumerate(kernel_text.splitlines(), start=1):
        for match in _DIGIT.finditer(line):
            findings.append(
                f"kernel line {number} carries the digit {match.group(0)!r}: "
                f"{line.strip()!r}"
            )
            break
        for match in _TRUTH_TOKEN.finditer(line):
            findings.append(
                f"kernel line {number} carries the token {match.group(0)!r}: "
                f"{line.strip()!r}"
            )
            break

    if findings:
        return findings

    for stage_id, fields in expected().items():
        for name, value in fields.items():
            rendered = json.dumps(value, separators=(",", ":"))
            if rendered in kernel_text:
                findings.append(
                    f"kernel states the expected value for {stage_id}.{name}: "
                    f"{rendered}"
                )
    return findings


def verify() -> list[str]:
    pins = _read_pins()
    lines: list[str] = []

    head = _git("rev-parse", "HEAD")
    lines.append(f"verification commit: {head}")

    if not STAGES:
        raise ValueError("the stage population is empty; the key is broken")

    artifacts = pins.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("pins must list at least one artifact")

    pinned: set[str] = set()
    for item in artifacts:
        if not isinstance(item, dict):
            raise ValueError("each artifact entry must be an object")
        relative = _safe_relative(_required_string(item, "path", "pinned artifact"))
        wanted = _required_string(item, "sha256", "pinned artifact")
        actual = _sha256_git_blob("HEAD", relative)
        if actual != wanted:
            raise ValueError(
                f"hash mismatch for {relative}: expected {wanted}, got {actual}"
            )
        lines.append(f"artifact: {relative} {actual}")
        pinned.add(relative.name)

    # Every artifact the key reads must be pinned. Without this the key
    # could quietly grow a dependency on an unpinned export and the hash
    # check above would still pass, having inspected the wrong set.
    unpinned = sorted(set(artifact_names()) - pinned)
    if unpinned:
        raise ValueError("key reads unpinned artifacts: " + ", ".join(unpinned))

    resolved = expected()
    fields = sum(len(v) for v in resolved.values())
    if not fields:
        raise ValueError("the key resolved no fields; refusing to report a pass")
    lines.append(
        f"key resolves: {fields} field(s) across {len(resolved)} stage(s)"
    )

    leaks = check_leak(KERNEL_PATH.read_text(encoding="utf-8"))
    if leaks:
        raise ValueError("kernel leaks expected values:\n  " + "\n  ".join(leaks))
    lines.append(f"kernel clean: {KERNEL_PATH.name} states no expected value")

    return lines


def repin() -> list[str]:
    """Rewrite recorded hashes from the blobs at HEAD.

    Performs NO verification. A repin is a write, and adopting a defect
    as the new baseline is exactly what it would hide -- the injection
    skill names regenerating a receipt under a live injection as the
    single easiest way to turn a real proof into a fake one. Run the
    plain verifier afterwards.
    """

    pins = _read_pins()
    lines: list[str] = []
    artifacts = pins.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError("pins must list artifacts")
    for item in artifacts:
        if not isinstance(item, dict):
            raise ValueError("each artifact entry must be an object")
        relative = _safe_relative(_required_string(item, "path", "pinned artifact"))
        old = item.get("sha256")
        new = _sha256_git_blob("HEAD", relative)
        if old != new:
            lines.append(f"rehashed: {relative} {old} -> {new}")
        item["sha256"] = new
    pins["snapshot_commit"] = _git("rev-parse", "HEAD")
    PINS_PATH.write_text(
        json.dumps(pins, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    lines.append("repinned; STATUS.md must be re-read by hand before trusting it")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the blind-restart kernel.")
    parser.add_argument(
        "--repin",
        action="store_true",
        help="rewrite recorded hashes from the blobs at HEAD; verifies nothing",
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
