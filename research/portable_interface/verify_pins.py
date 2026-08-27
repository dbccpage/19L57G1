"""Verify the portable export surface against the sealed sources.

Usage: python research/portable_interface/verify_pins.py [--repin]

Two checks, both of which must hold for INTERFACE.md to be worth reading:

* every module named in SOURCE_PINS.json still hashes to its recorded
  SHA-256, so the interface describes the sources it was written against;
* every exported declaration named in SOURCE_PINS.json is actually
  declared in the module it is attributed to, so the interface cannot
  cite a theorem that does not exist or has been renamed.

The second check is the one that matters most. A hash pin proves the
source did not move; it does not prove the interface names anything real.
Both directions are needed and neither implies the other.

The ``research`` workflow job runs this script on every pull request and push
to ``main``, followed by this tree's unit tests and strict typing. That gate
checks hashes and declaration resolution; it does not build Lean or judge the
interface prose.

This tree is an EXPORT surface. It names only objects this repository
constructs, in this repository's own vocabulary. Nothing external is
named here, and nothing external may be added: the direction of the
bridge is what makes it a bridge rather than a merge.
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

# Declaration forms this repository actually uses at column zero.
_DECL_KEYWORDS = ("theorem", "def", "structure", "abbrev", "inductive")


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
    payload = json.loads(PINS_PATH.read_text(encoding="utf-8"))
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


def _declared_names(relative: PurePosixPath) -> set[str]:
    """Names declared at column zero in a Lean source.

    Anchored at line start on purpose. A docstring line that happens to
    begin with the word ``theorem`` has defeated a grep-based count in
    this repository twice; requiring the keyword to open the line and be
    followed by an identifier is what separates a declaration from prose
    about one.
    """

    text = _git_bytes("show", f"HEAD:{relative.as_posix()}").decode("utf-8")
    pattern = re.compile(
        r"^(?:" + "|".join(_DECL_KEYWORDS) + r")\s+([A-Za-z_][A-Za-z0-9_'.]*)",
        re.M,
    )
    return set(pattern.findall(text))


def verify_pins() -> list[str]:
    pins = _read_pins()
    lines: list[str] = []

    head = _git("rev-parse", "HEAD")
    lines.append(f"verification commit: {head}")

    modules = pins.get("modules")
    if not isinstance(modules, list) or not modules:
        raise ValueError("pins must list at least one module")

    declared: dict[str, set[str]] = {}
    for item in modules:
        if not isinstance(item, dict):
            raise ValueError("each module entry must be an object")
        relative = _safe_relative(_required_string(item, "path", "pin module"))
        expected = _required_string(item, "sha256", "pin module")
        actual = _sha256_git_blob("HEAD", relative)
        if actual != expected:
            raise ValueError(
                f"hash mismatch for {relative}: expected {expected}, got {actual}"
            )
        lines.append(f"source: {relative} {actual}")
        declared[relative.as_posix()] = _declared_names(relative)

    exports = pins.get("exports")
    if not isinstance(exports, list) or not exports:
        raise ValueError("pins must list at least one export")

    missing: list[str] = []
    for item in exports:
        if not isinstance(item, dict):
            raise ValueError("each export entry must be an object")
        name = _required_string(item, "name", "export")
        module = _required_string(item, "module", "export")
        if module not in declared:
            raise ValueError(f"export {name} names unpinned module {module}")
        if name not in declared[module]:
            missing.append(f"{module}:{name}")

    if missing:
        raise ValueError(
            "exports declared in no pinned source: " + ", ".join(sorted(missing))
        )

    lines.append(f"exports resolve: {len(exports)} declaration(s) across "
                 f"{len(declared)} pinned module(s)")
    return lines


def repin() -> list[str]:
    """Rewrite recorded hashes from the blobs at HEAD.

    Performs NO verification: a repin run is a write, and adopting a
    defect as the new baseline is exactly what it would hide. Run the
    plain verifier afterwards, and revise INTERFACE.md by hand.
    """

    pins = _read_pins()
    lines: list[str] = []
    modules = pins.get("modules")
    if not isinstance(modules, list):
        raise ValueError("pins must list modules")
    for item in modules:
        if not isinstance(item, dict):
            raise ValueError("each module entry must be an object")
        relative = _safe_relative(_required_string(item, "path", "pin module"))
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
    lines.append("repinned; INTERFACE.md must be re-read by hand before trusting it")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repin",
        action="store_true",
        help="rewrite recorded hashes from the blobs at HEAD; verifies nothing",
    )
    args = parser.parse_args()
    try:
        lines = repin() if args.repin else verify_pins()
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
