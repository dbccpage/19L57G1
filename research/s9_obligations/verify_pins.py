"""Verify the S9-obligations tree's pins on the sealed inputs it reads.

Usage: python research/s9_obligations/verify_pins.py [--repin]

Four checks, and none of them implies the others:

* every sealed file this run reads still hashes, as the Git blob at HEAD,
  to its recorded SHA-256, so the receipts describe the inputs they were
  computed against.  The hash is taken over ``git show HEAD:path`` and is
  therefore independent of checkout line endings;
* the governing prompt still has its recorded Git blob id (PROMPT.md
  step 1: stop on drift);
* the recorded snapshot commit is an exact 40-digit lowercase hex id and
  never ``HEAD`` -- a pin on a moving name pins nothing;
* the worktree carries no change under any sealed prefix (PROMPT.md
  step 35): ``git status --porcelain -- prompt paper code lean4/Derivation
  artifacts`` must be empty.  That check is a pure function of the
  porcelain text so it can be tested against a synthetic line without
  touching a sealed path.

A pass says the inputs did not move and nothing sealed was touched.  It
says nothing about the mathematics computed from them, and it does not
authenticate the interpreter, Git, or this script.  Nothing in
``.github/workflows`` runs this script; a pass is a manual receipt for the
tree present when it ran.  AuthorityEffect: None.
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

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
PINS_PATH = HERE / "SOURCE_PINS.json"
SCHEMA = "s9_obligations_source_pins/v1"

# The sealed prefixes of CLAUDE.md, as pathspecs and as prefixes.  A
# top-level ``lean4/*.lean`` is outside the seal and outside this check.
SEALED_PATHSPECS = ("prompt", "paper", "code", "lean4/Derivation", "artifacts")
SEALED_PREFIXES = tuple(f"{spec}/" for spec in SEALED_PATHSPECS)


def _git_bytes(*args: str) -> bytes:
    result = subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, check=False
    )
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"git {' '.join(args)} failed: {stderr}")
    return result.stdout


def _git(*args: str) -> str:
    return _git_bytes(*args).decode("utf-8").strip()


def _sha256_git_blob(revision: str, relative: PurePosixPath) -> str:
    """Hash the Git blob itself, independent of checkout line endings."""

    return (
        hashlib.sha256(_git_bytes("show", f"{revision}:{relative.as_posix()}"))
        .hexdigest()
        .upper()
    )


def read_pins() -> dict[str, Any]:
    payload: object = json.loads(PINS_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("SOURCE_PINS.json must be an object")
    return payload


def _required_string(block: dict[str, Any], key: str, where: str) -> str:
    value = block.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{where}: missing string field {key!r}")
    return value


def _require_hex(value: str, width: int, where: str, *, uppercase: bool) -> None:
    alphabet = r"[0-9A-F]" if uppercase else r"[0-9a-f]"
    if re.fullmatch(f"{alphabet}{{{width}}}", value) is None:
        case = "uppercase" if uppercase else "lowercase"
        raise ValueError(f"{where} must be an exact {width}-digit {case} hex id")


def _safe_relative(raw: str) -> PurePosixPath:
    if "\\" in raw:
        raise ValueError(f"unsafe path separator in pins: {raw}")
    relative = PurePosixPath(raw)
    if (
        relative.is_absolute()
        or not relative.parts
        or any(part in ("", ".", "..") for part in relative.parts)
        or ":" in relative.parts[0]
    ):
        raise ValueError(f"unsafe path in pins: {raw}")
    return relative


def _under_sealed_prefix(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in SEALED_PREFIXES)


def sealed_prefix_violations(porcelain: str) -> list[str]:
    """Porcelain (v1) lines that name a path under a sealed prefix.

    Pure: takes the text of ``git status --porcelain=v1`` and returns the
    offending lines, so the refusal can be tested on a synthetic line
    without any sealed path ever being touched.  A rename record names two
    paths and is refused if either one is sealed.
    """

    violations: list[str] = []
    for line in porcelain.splitlines():
        if not line.strip():
            continue
        if len(line) < 4 or line[2] != " ":
            raise ValueError(f"malformed git status record: {line!r}")
        paths = [part.strip().strip('"') for part in line[3:].split(" -> ")]
        if any(_under_sealed_prefix(path) for path in paths):
            violations.append(line)
    return violations


def _live_porcelain() -> str:
    return _git_bytes(
        "status", "--porcelain=v1", "--untracked-files=all", "--", *SEALED_PATHSPECS
    ).decode("utf-8")


def verify(pins: dict[str, Any] | None = None) -> list[str]:
    """Run every check against HEAD; raise ``ValueError`` on the first failure."""

    if pins is None:
        pins = read_pins()
    lines: list[str] = []

    head = _git("rev-parse", "HEAD")
    _require_hex(head, 40, "verification commit", uppercase=False)
    lines.append(f"verification commit: {head}")

    schema = _required_string(pins, "schema", "pins")
    if schema != SCHEMA:
        raise ValueError(f"pins schema is {schema!r}, expected {SCHEMA!r}")

    snapshot = _required_string(pins, "snapshot_commit", "pins")
    _require_hex(snapshot, 40, "snapshot commit", uppercase=False)
    lines.append(f"snapshot commit: {snapshot}")

    prompt = pins.get("prompt")
    if not isinstance(prompt, dict):
        raise ValueError("pins must carry a 'prompt' object")
    prompt_path = _safe_relative(_required_string(prompt, "path", "prompt pin"))
    wanted_blob = _required_string(prompt, "blob", "prompt pin")
    _require_hex(wanted_blob, 40, "prompt blob id", uppercase=False)
    actual_blob = _git("rev-parse", f"HEAD:{prompt_path.as_posix()}")
    if actual_blob != wanted_blob:
        raise ValueError(
            f"prompt drift: {prompt_path} is blob {actual_blob} at HEAD, "
            f"pinned {wanted_blob}; stop"
        )
    lines.append(f"prompt: {prompt_path} {actual_blob}")

    sealed = pins.get("sealed_inputs")
    if not isinstance(sealed, list) or not sealed:
        raise ValueError("pins must list at least one sealed input")
    for item in sealed:
        if not isinstance(item, dict):
            raise ValueError("each sealed input entry must be an object")
        relative = _safe_relative(_required_string(item, "path", "sealed input"))
        if not _under_sealed_prefix(relative.as_posix()):
            raise ValueError(f"pinned input is not under a sealed prefix: {relative}")
        wanted = _required_string(item, "sha256", "sealed input")
        _require_hex(wanted, 64, f"sha256 for {relative}", uppercase=True)
        actual = _sha256_git_blob("HEAD", relative)
        if actual != wanted:
            raise ValueError(
                f"hash mismatch for {relative}: expected {wanted}, got {actual}"
            )
        lines.append(f"pin: {relative} {actual}")

    violations = sealed_prefix_violations(_live_porcelain())
    if violations:
        raise ValueError(
            "worktree carries changes under a sealed prefix:\n  "
            + "\n  ".join(violations)
        )
    lines.append("sealed prefixes clean: " + " ".join(SEALED_PATHSPECS))
    return lines


def repin() -> list[str]:
    """Rewrite recorded hashes and ids from the objects at HEAD.

    Performs NO verification. A repin is a write, and adopting a defect
    as the new baseline is exactly what it would hide -- the injection
    skill names regenerating a receipt under a live injection as the
    single easiest way to turn a real proof into a fake one. Run the
    plain verifier afterwards.
    """

    pins = read_pins()
    lines: list[str] = []
    prompt = pins.get("prompt")
    if not isinstance(prompt, dict):
        raise ValueError("pins must carry a 'prompt' object")
    prompt_path = _safe_relative(_required_string(prompt, "path", "prompt pin"))
    old_blob = prompt.get("blob")
    new_blob = _git("rev-parse", f"HEAD:{prompt_path.as_posix()}")
    if old_blob != new_blob:
        lines.append(f"reblobbed: {prompt_path} {old_blob} -> {new_blob}")
    prompt["blob"] = new_blob
    sealed = pins.get("sealed_inputs")
    if not isinstance(sealed, list):
        raise ValueError("pins must list sealed inputs")
    for item in sealed:
        if not isinstance(item, dict):
            raise ValueError("each sealed input entry must be an object")
        relative = _safe_relative(_required_string(item, "path", "sealed input"))
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
    lines.append("repinned; PREFLIGHT.md must be re-read by hand before trusting it")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the S9-obligations pins.")
    parser.add_argument(
        "--repin",
        action="store_true",
        help="rewrite recorded hashes from the objects at HEAD; verifies nothing",
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
