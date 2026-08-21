"""Verify the source pin and protected-path boundary.

This script intentionally uses only the standard library.  It is a receipt
checker: a successful run verifies source bytes and the declared boundary; it
does not prove any mathematical claim made by the research modules.
"""

from __future__ import annotations

import hashlib
import json
import re
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


def _git(*args: str) -> str:
    process = subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    )
    return process.stdout.strip()


def _git_bytes(*args: str) -> bytes:
    process = subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
    )
    return process.stdout


def _git_succeeds(*args: str) -> bool:
    """Return whether Git accepts a read-only predicate command."""

    process = subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=False,
        capture_output=True,
    )
    return process.returncode == 0


def _sha256_git_blob(revision: str, relative: Path) -> str:
    """Hash a canonical Git blob, independent of checkout line endings."""

    object_name = f"{revision}:{relative.as_posix()}"
    return hashlib.sha256(_git_bytes("show", object_name)).hexdigest().upper()


def _read_manifest() -> dict[str, Any]:
    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("source manifest must be an object")
    return payload


def _required_string(entry: dict[str, Any], key: str, context: str) -> str:
    value = entry.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{context} missing nonempty string {key!r}")
    return value


def _required_string_list(entry: dict[str, Any], key: str, context: str) -> list[str]:
    value = entry.get(key)
    if not isinstance(value, list) or not value or not all(
        isinstance(item, str) and item for item in value
    ):
        raise ValueError(f"{context} missing nonempty string list {key!r}")
    return value


def _source_snapshot(manifest: dict[str, Any]) -> tuple[str, str]:
    source_snapshot = manifest.get("source_snapshot")
    if not isinstance(source_snapshot, dict):
        raise ValueError("source_snapshot must be an object")
    return (
        _required_string(source_snapshot, "commit", "source_snapshot"),
        _required_string(source_snapshot, "tree", "source_snapshot"),
    )


def _assert_safe_relative(path_text: str) -> Path:
    relative = Path(path_text)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"unsafe manifest path: {path_text}")
    if not path_text.replace("\\", "/").startswith("lean4/Derivation/"):
        raise ValueError(f"source lies outside declared Lean input tree: {path_text}")
    return relative


def _assert_safe_local_lean_path(path_text: str) -> Path:
    relative = Path(path_text)
    prefix = "research/primitive_difference_tower/lean/"
    normalized = path_text.replace("\\", "/")
    if relative.is_absolute() or ".." in relative.parts or not normalized.startswith(prefix):
        raise ValueError(f"Lean source lies outside the local fixture: {path_text}")
    return relative


def _strip_lean_comments_and_strings(source: str) -> str:
    """Remove Lean comments and strings before looking for qualified names."""

    output: list[str] = []
    index = 0
    block_depth = 0
    while index < len(source):
        if block_depth:
            if source.startswith("/-", index):
                block_depth += 1
                index += 2
            elif source.startswith("-/", index):
                block_depth -= 1
                index += 2
            else:
                if source[index] == "\n":
                    output.append("\n")
                index += 1
            continue
        if source.startswith("/-", index):
            block_depth = 1
            index += 2
            continue
        if source.startswith("--", index):
            newline = source.find("\n", index)
            if newline == -1:
                break
            output.append("\n")
            index = newline + 1
            continue
        if source[index] == '"':
            output.append(" ")
            index += 1
            while index < len(source):
                if source[index] == "\\":
                    index += 2
                elif source[index] == '"':
                    index += 1
                    break
                else:
                    if source[index] == "\n":
                        output.append("\n")
                    index += 1
            continue
        output.append(source[index])
        index += 1
    if block_depth:
        raise ValueError("Lean source has an unterminated block comment")
    return "".join(output)


def _verify_lean_source_citations(
    manifest: dict[str, Any], module_roles: dict[str, str], citation_symbols: dict[str, set[str]]
) -> list[str]:
    lean_source = manifest.get("lean_source")
    if not isinstance(lean_source, dict):
        raise ValueError("lean_source must be an object")
    relative = _assert_safe_local_lean_path(
        _required_string(lean_source, "path", "lean_source")
    )
    expected_imports = set(
        _required_string_list(lean_source, "imports", "lean_source")
    )
    raw_uses = lean_source.get("symbol_uses")
    if not isinstance(raw_uses, list) or not raw_uses:
        raise ValueError("lean_source missing nonempty symbol_uses list")
    expected_uses: set[tuple[str, str]] = set()
    uses_by_module: dict[str, set[str]] = {}
    for use in raw_uses:
        if not isinstance(use, dict):
            raise ValueError("lean_source symbol use must be an object")
        module_name = _required_string(use, "module", "lean_source symbol use")
        symbols = _required_string_list(use, "symbols", "lean_source symbol use")
        if module_name not in module_roles:
            raise ValueError(f"Lean source use is not a manifest module: {module_name}")
        namespace = module_name.rsplit(".", 1)[-1]
        module_symbols = uses_by_module.setdefault(module_name, set())
        for symbol in symbols:
            if symbol in module_symbols:
                raise ValueError(f"duplicate Lean source symbol declaration: {module_name}.{symbol}")
            module_symbols.add(symbol)
            expected_uses.add((namespace, symbol))
    for module_name, citation_symbol_set in citation_symbols.items():
        if not citation_symbol_set.issubset(uses_by_module.get(module_name, set())):
            raise ValueError(
                f"explicit transitive citation is absent from lean_source uses: {module_name}"
            )
    try:
        source = _git_bytes("show", f"HEAD:{relative.as_posix()}").decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"Lean source is not UTF-8: {relative}") from error
    scrubbed = _strip_lean_comments_and_strings(source)
    actual_imports = set(
        re.findall(r"(?m)^\s*import\s+([A-Za-z_][A-Za-z0-9_.]*)\s*$", scrubbed)
    )
    if actual_imports != expected_imports:
        raise ValueError(
            f"Lean source imports differ: expected {sorted(expected_imports)}, "
            f"got {sorted(actual_imports)}"
        )
    namespaces = {module.rsplit(".", 1)[-1] for module in module_roles}
    actual_uses = {
        (namespace, symbol)
        for namespace, symbol in re.findall(
            r"\b([A-Z][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_']*)", scrubbed
        )
        if namespace in namespaces
    }
    missing = expected_uses - actual_uses
    undeclared = actual_uses - expected_uses
    if missing or undeclared:
        raise ValueError(
            "Lean source symbol uses differ: "
            f"missing {sorted(missing)}, undeclared {sorted(undeclared)}"
        )
    return [
        f"lean source imports: {relative} {', '.join(sorted(actual_imports))}",
        f"lean source symbols: {len(actual_uses)} declared uses match",
    ]


def verify_manifest() -> list[str]:
    manifest = _read_manifest()
    lines: list[str] = []
    if _required_string(manifest, "schema", "source manifest") != "primitive_difference_tower_source_manifest/v3":
        raise ValueError("unsupported source manifest schema")
    actual_commit = _git("rev-parse", "HEAD")
    snapshot_commit, snapshot_tree = _source_snapshot(manifest)
    lines.extend(
        (
            f"verification commit: {actual_commit}",
            f"declared source snapshot: {snapshot_commit} / {snapshot_tree}",
            "hash basis: canonical Git blobs at verification commit",
        )
    )
    modules = manifest.get("modules")
    if not isinstance(modules, list) or not modules:
        raise ValueError("manifest modules must be a nonempty list")
    module_roles: dict[str, str] = {}
    for item in modules:
        if not isinstance(item, dict):
            raise ValueError("manifest module entry must be an object")
        module_name = _required_string(item, "module", "manifest module")
        if module_name in module_roles:
            raise ValueError(f"duplicate manifest module: {module_name}")
        module_roles[module_name] = _required_string(item, "role", "manifest module")
        relative = _assert_safe_relative(
            _required_string(item, "path", "manifest module")
        )
        actual_hash = _sha256_git_blob("HEAD", relative)
        expected_hash = _required_string(item, "sha256", "manifest module")
        if actual_hash != expected_hash:
            raise ValueError(
                f"hash mismatch for {relative}: expected {expected_hash}, got {actual_hash}"
            )
        lines.append(f"source: {relative} {actual_hash}")
    semantic_roots = manifest.get("semantic_roots")
    if not isinstance(semantic_roots, list) or not semantic_roots:
        raise ValueError("semantic_roots must be a nonempty list")
    for semantic_root in semantic_roots:
        if not isinstance(semantic_root, str) or module_roles.get(semantic_root) != "semantic root":
            raise ValueError(f"semantic root is not marked as such: {semantic_root}")
        lines.append(f"semantic root: {semantic_root}")
    citations = manifest.get("explicit_transitive_citations", [])
    if not isinstance(citations, list):
        raise ValueError("explicit_transitive_citations must be a list")
    citation_symbols: dict[str, set[str]] = {}
    for citation in citations:
        if not isinstance(citation, dict):
            raise ValueError("explicit transitive citation must be an object")
        citation_module = _required_string(
            citation, "module", "explicit transitive citation"
        )
        symbols = _required_string_list(
            citation, "symbols", "explicit transitive citation"
        )
        if module_roles.get(citation_module) != "transitive compilation input":
            raise ValueError(f"citation is not a declared transitive input: {citation_module}")
        if citation_module in citation_symbols:
            raise ValueError(f"duplicate explicit transitive citation: {citation_module}")
        citation_symbols[citation_module] = set(symbols)
        lines.append(f"explicit transitive citation: {citation_module} {', '.join(symbols)}")
    lines.extend(_verify_lean_source_citations(manifest, module_roles, citation_symbols))
    return lines


def verify_protected_paths() -> list[str]:
    manifest = _read_manifest()
    snapshot_commit, snapshot_tree = _source_snapshot(manifest)
    try:
        actual_snapshot_tree = _git("rev-parse", f"{snapshot_commit}^{{tree}}")
    except subprocess.CalledProcessError as error:
        raise ValueError(f"source snapshot is unavailable locally: {snapshot_commit}") from error
    if actual_snapshot_tree != snapshot_tree:
        raise ValueError(
            f"source snapshot tree mismatch: expected {snapshot_tree}, got {actual_snapshot_tree}"
        )
    if not _git_succeeds("merge-base", "--is-ancestor", snapshot_commit, "HEAD"):
        raise ValueError(f"source snapshot is not an ancestor of HEAD: {snapshot_commit}")
    historical = _git(
        "diff", "--name-only", snapshot_commit, "HEAD", "--", *PROTECTED_PREFIXES
    )
    if historical:
        raise ValueError(f"protected-path history changed since source snapshot:\n{historical}")
    changed = _git("diff", "--name-only", "HEAD", "--", *PROTECTED_PREFIXES)
    if changed:
        raise ValueError(f"tracked protected-path changes:\n{changed}")
    untracked = _git("ls-files", "--others", "--exclude-standard", "--", *PROTECTED_PREFIXES)
    actual = {line.replace("\\", "/") for line in untracked.splitlines() if line}
    lines = [
        "protected history since source snapshot: unchanged",
        "protected tracked paths: unchanged",
    ]
    if actual:
        lines.append(
            "protected untracked paths: observed but not Git/blob inputs: "
            f"{sorted(actual)}"
        )
    else:
        lines.append("protected untracked paths: none")
    return lines


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
