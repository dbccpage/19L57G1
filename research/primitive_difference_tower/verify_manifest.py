"""Verify the sealed-input pin and protected-path boundary.

This script intentionally uses only the standard library.  It is a receipt
checker: a successful run verifies source bytes and the declared boundary; it
does not prove any mathematical claim made by the research modules.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
MANIFEST_PATH = HERE / "SOURCE_MANIFEST.json"
PROTECTED_PREFIXES = (
    "prompt/",
    "paper/",
    "code/",
    "lean4/Derivation/",
    "artifacts/",
)
INITIAL_UNTRACKED_PROTECTED = {"prompt/prompt_pr14.md"}


def _git(*args: str) -> str:
    process = subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    )
    return process.stdout.strip()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _read_manifest() -> dict[str, Any]:
    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("source manifest must be an object")
    return payload


def _assert_safe_relative(path_text: str) -> Path:
    relative = Path(path_text)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"unsafe manifest path: {path_text}")
    if not path_text.replace("\\", "/").startswith("lean4/Derivation/"):
        raise ValueError(f"source lies outside declared Lean input tree: {path_text}")
    return relative


def verify_manifest() -> list[str]:
    manifest = _read_manifest()
    lines: list[str] = []
    actual_commit = _git("rev-parse", "HEAD")
    actual_tree = _git("rev-parse", "HEAD^{tree}")
    if actual_commit != manifest["repository_commit"]:
        raise ValueError(
            f"commit mismatch: expected {manifest['repository_commit']}, got {actual_commit}"
        )
    if actual_tree != manifest["repository_tree"]:
        raise ValueError(
            f"tree mismatch: expected {manifest['repository_tree']}, got {actual_tree}"
        )
    lines.extend((f"commit: {actual_commit}", f"tree: {actual_tree}"))
    modules = manifest.get("modules")
    if not isinstance(modules, list) or not modules:
        raise ValueError("manifest modules must be a nonempty list")
    module_roles: dict[str, str] = {}
    for item in modules:
        if not isinstance(item, dict):
            raise ValueError("manifest module entry must be an object")
        module_name = str(item["module"])
        if module_name in module_roles:
            raise ValueError(f"duplicate manifest module: {module_name}")
        module_roles[module_name] = str(item["role"])
        relative = _assert_safe_relative(str(item["path"]))
        actual_hash = _sha256(REPO / relative)
        expected_hash = str(item["sha256"])
        if actual_hash != expected_hash:
            raise ValueError(
                f"hash mismatch for {relative}: expected {expected_hash}, got {actual_hash}"
            )
        lines.append(f"source: {relative} {actual_hash}")
    semantic_roots = manifest.get("semantic_roots")
    if not isinstance(semantic_roots, list) or not semantic_roots:
        raise ValueError("semantic_roots must be a nonempty list")
    for module_name in semantic_roots:
        if not isinstance(module_name, str) or module_roles.get(module_name) != "semantic root":
            raise ValueError(f"semantic root is not marked as such: {module_name}")
        lines.append(f"semantic root: {module_name}")
    citations = manifest.get("explicit_transitive_citations", [])
    if not isinstance(citations, list):
        raise ValueError("explicit_transitive_citations must be a list")
    for citation in citations:
        if not isinstance(citation, dict):
            raise ValueError("explicit transitive citation must be an object")
        module_name = citation.get("module")
        symbols = citation.get("symbols")
        if not isinstance(module_name, str) or module_roles.get(module_name) != "transitive compilation input":
            raise ValueError(f"citation is not a declared transitive input: {module_name}")
        if not isinstance(symbols, list) or not symbols or not all(isinstance(symbol, str) for symbol in symbols):
            raise ValueError(f"citation has no symbols: {module_name}")
        lines.append(f"explicit transitive citation: {module_name} {', '.join(symbols)}")
    return lines


def verify_protected_paths() -> list[str]:
    changed = _git("diff", "--name-only", "HEAD", "--", *PROTECTED_PREFIXES)
    if changed:
        raise ValueError(f"tracked protected-path changes:\n{changed}")
    untracked = _git("ls-files", "--others", "--exclude-standard", "--", *PROTECTED_PREFIXES)
    actual = {line.replace("\\", "/") for line in untracked.splitlines() if line}
    if actual != INITIAL_UNTRACKED_PROTECTED:
        raise ValueError(
            "protected untracked set changed: "
            f"expected {sorted(INITIAL_UNTRACKED_PROTECTED)}, got {sorted(actual)}"
        )
    return ["protected tracked paths: unchanged", "protected untracked paths: baseline matches"]


def main() -> int:
    try:
        lines = verify_manifest() + verify_protected_paths()
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
