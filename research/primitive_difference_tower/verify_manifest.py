"""Verify the source pin, the protected-path boundary, and the receipts.

This script intentionally uses only the standard library.  It is a receipt
checker: a successful run verifies source bytes, the declared boundary, and
that the committed finite receipt and the prose citing it agree with the code.
It does not prove any mathematical claim made by the research modules.

Nothing in ``.github/workflows`` runs this script.  A pass is a manual receipt
for the commit it names, and it goes stale silently until someone reruns it.

``--repin`` rewrites ``SOURCE_MANIFEST.json`` from the canonical blobs at
``HEAD`` and moves the source snapshot to ``HEAD``.  Prose that cites the old
snapshot must then be revised by hand; verification fails until it is.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Sequence

from finite_tower import MAX_HORIZON, render_report


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
MANIFEST_PATH = HERE / "SOURCE_MANIFEST.json"
RECEIPT_PATH = HERE / "receipts" / "finite_tower_0_15.json"
PROSE_PATHS = (HERE / "CLAIM_LEDGER.md", HERE / "FINDINGS.md")
SCHEMA = "primitive_difference_tower_source_manifest/v4"
SOURCE_TREE = "lean4/Derivation/"
LOCAL_LEAN_TREE = "research/primitive_difference_tower/lean/"
ROLE_ROOT = "semantic root"
ROLE_TRANSITIVE = "transitive compilation input"
PROTECTED_PREFIXES = (
    "prompt/",
    "paper/",
    "code/",
    "lean4/Derivation/",
    "artifacts/",
)

_DRIVE = re.compile(r"^[A-Za-z]:")
_CHAR_LITERAL = re.compile(r"'(?:\\(?:x[0-9A-Fa-f]{2}|u\{[0-9A-Fa-f]+\}|.)|[^'\\\n])'")
_IDENTIFIER_CHAR = re.compile(r"[A-Za-z0-9_'!?.]")
_IMPORT_LINE = re.compile(r"(?m)^\s*import\s+([A-Za-z_][A-Za-z0-9_.]*)\s*$")
_QUALIFIED_NAME = re.compile(r"\b([A-Z][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_']*)")


def _git_bytes(*args: str) -> bytes:
    process = subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
    )
    return process.stdout


def _git(*args: str) -> str:
    """Run Git and decode its output as UTF-8 regardless of the process locale."""

    return _git_bytes(*args).decode("utf-8").strip()


def _is_ancestor(ancestor: str, descendant: str) -> bool:
    """Decide ancestry, refusing to read an undecided predicate as a negative.

    ``git merge-base --is-ancestor`` exits 1 for "no" and with other codes when
    it could not decide at all, for example on a shallow clone that lacks the
    ancestor.  Only the first is a verdict.
    """

    process = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=REPO,
        check=False,
        capture_output=True,
    )
    if process.returncode == 0:
        return True
    if process.returncode == 1:
        return False
    detail = process.stderr.decode("utf-8", errors="replace").strip()
    raise ValueError(
        f"ancestry of {ancestor} was not decided: git merge-base exited "
        f"{process.returncode}: {detail}"
    )


def _sha256_git_blob(revision: str, relative: PurePosixPath) -> str:
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


def _safe_relative(path_text: str, tree: str, label: str) -> PurePosixPath:
    """Accept only a plain relative path inside ``tree``, on every platform.

    Backslashes are normalized before the path is split, so a ``..`` component
    written with backslashes cannot pass as one opaque name on POSIX, where
    ``Path`` does not treat a backslash as a separator.
    """

    normalized = path_text.replace("\\", "/")
    parts = normalized.split("/")
    if (
        normalized.startswith("/")
        or _DRIVE.match(normalized)
        or ".." in parts
        or "." in parts
        or "" in parts
    ):
        raise ValueError(f"unsafe manifest path: {path_text}")
    if not normalized.startswith(tree):
        raise ValueError(f"{label} lies outside {tree}: {path_text}")
    return PurePosixPath(normalized)


def _strip_lean_comments_and_strings(source: str) -> str:
    """Remove Lean comments, strings, and character literals before scanning.

    An unterminated block comment or string literal raises instead of silently
    scrubbing the rest of the file, where a qualified name could hide.
    """

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
            terminated = False
            while index < len(source):
                if source[index] == "\\":
                    index += 2
                elif source[index] == '"':
                    index += 1
                    terminated = True
                    break
                else:
                    if source[index] == "\n":
                        output.append("\n")
                    index += 1
            if not terminated:
                raise ValueError("Lean source has an unterminated string literal")
            continue
        if source[index] == "'" and (not output or not _IDENTIFIER_CHAR.match(output[-1])):
            literal = _CHAR_LITERAL.match(source, index)
            if literal:
                output.append(" ")
                index = literal.end()
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
    relative = _safe_relative(
        _required_string(lean_source, "path", "lean_source"), LOCAL_LEAN_TREE, "Lean source"
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
    # The source policy, enforced in both directions: a transitive module may
    # be used only through an explicit citation naming exactly the symbols
    # used, and every explicit citation must correspond to a real use.
    for module_name, used in sorted(uses_by_module.items()):
        if module_roles[module_name] == ROLE_ROOT:
            continue
        cited = citation_symbols.get(module_name)
        if cited is None:
            raise ValueError(
                f"Lean source uses transitive module {module_name} "
                "without an explicit transitive citation"
            )
        if cited != used:
            raise ValueError(
                f"explicit transitive citation for {module_name} does not match "
                f"lean_source uses: cited {sorted(cited)}, used {sorted(used)}"
            )
    for module_name in sorted(citation_symbols):
        if module_name not in uses_by_module:
            raise ValueError(
                f"explicit transitive citation is absent from lean_source uses: {module_name}"
            )
    try:
        source = _git_bytes("show", f"HEAD:{relative.as_posix()}").decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"Lean source is not UTF-8: {relative}") from error
    scrubbed = _strip_lean_comments_and_strings(source)
    actual_imports = set(_IMPORT_LINE.findall(scrubbed))
    if actual_imports != expected_imports:
        raise ValueError(
            f"Lean source imports differ: expected {sorted(expected_imports)}, "
            f"got {sorted(actual_imports)}"
        )
    namespaces = {module.rsplit(".", 1)[-1] for module in module_roles}
    actual_uses = {
        (namespace, symbol)
        for namespace, symbol in _QUALIFIED_NAME.findall(scrubbed)
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
        f"lean source imports: {relative.as_posix()} {', '.join(sorted(actual_imports))}",
        f"lean source symbols: {len(actual_uses)} declared uses match",
    ]


def verify_manifest() -> list[str]:
    manifest = _read_manifest()
    lines: list[str] = []
    if _required_string(manifest, "schema", "source manifest") != SCHEMA:
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
        role = _required_string(item, "role", "manifest module")
        if role not in (ROLE_ROOT, ROLE_TRANSITIVE):
            raise ValueError(f"unknown manifest role for {module_name}: {role}")
        module_roles[module_name] = role
        relative = _safe_relative(
            _required_string(item, "path", "manifest module"), SOURCE_TREE, "source"
        )
        actual_hash = _sha256_git_blob("HEAD", relative)
        expected_hash = _required_string(item, "sha256", "manifest module")
        if actual_hash != expected_hash:
            raise ValueError(
                f"hash mismatch for {relative}: expected {expected_hash}, got {actual_hash}"
            )
        lines.append(f"source: {relative.as_posix()} {actual_hash}")
    semantic_roots = manifest.get("semantic_roots")
    if not isinstance(semantic_roots, list) or not semantic_roots:
        raise ValueError("semantic_roots must be a nonempty list")
    for semantic_root in semantic_roots:
        if not isinstance(semantic_root, str) or module_roles.get(semantic_root) != ROLE_ROOT:
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
        if module_roles.get(citation_module) != ROLE_TRANSITIVE:
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
        raise ValueError(
            f"source snapshot is unavailable locally (shallow clone?): {snapshot_commit}"
        ) from error
    if actual_snapshot_tree != snapshot_tree:
        raise ValueError(
            f"source snapshot tree mismatch: expected {snapshot_tree}, got {actual_snapshot_tree}"
        )
    if not _is_ancestor(snapshot_commit, "HEAD"):
        raise ValueError(f"source snapshot is not an ancestor of HEAD: {snapshot_commit}")
    # Every commit since the snapshot is inspected, not just the two endpoint
    # trees: a protected edit that a later commit reverts byte-for-byte leaves
    # the endpoint diff empty, and default history simplification would prune
    # such a touch on a merged side branch.  --full-history walks every parent.
    touching = _git(
        "log", "--full-history", "--format=%H", f"{snapshot_commit}..HEAD",
        "--", *PROTECTED_PREFIXES,
    )
    if touching:
        raise ValueError(
            "commits since the source snapshot touched a protected path:\n" + touching
        )
    changed = _git("diff", "--name-only", "HEAD", "--", *PROTECTED_PREFIXES)
    if changed:
        raise ValueError(f"tracked protected-path changes:\n{changed}")
    untracked = _git("ls-files", "--others", "--exclude-standard", "--", *PROTECTED_PREFIXES)
    actual = {line.replace("\\", "/") for line in untracked.splitlines() if line}
    lines = [
        "protected history since source snapshot: no commit touched a protected path",
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


def verify_receipt_and_prose() -> list[str]:
    """Check the committed receipt against the code and the prose against both.

    The receipt hash and the snapshot commit are quoted in two prose files; a
    regeneration or a repin that forgets either one fails here by name.
    """

    expected = render_report(MAX_HORIZON)
    actual = RECEIPT_PATH.read_bytes()
    receipt_name = RECEIPT_PATH.relative_to(HERE).as_posix()
    if actual != expected:
        raise ValueError(
            f"{receipt_name} differs from render_report({MAX_HORIZON}); "
            "regenerate it with run_finite_tower.py"
        )
    digest = hashlib.sha256(actual).hexdigest().upper()
    snapshot_commit, _ = _source_snapshot(_read_manifest())
    lines = [f"receipt: {receipt_name} {digest}"]
    for prose in PROSE_PATHS:
        text = prose.read_text(encoding="utf-8")
        missing = [
            label
            for label, token in (("receipt SHA-256", digest), ("snapshot commit", snapshot_commit))
            if token not in text
        ]
        if missing:
            raise ValueError(f"{prose.name} does not cite the current {' and '.join(missing)}")
        lines.append(f"prose cites receipt and snapshot: {prose.name}")
    return lines


def repin_manifest() -> list[str]:
    """Rewrite module hashes from the blobs at HEAD and move the snapshot there."""

    manifest = _read_manifest()
    modules = manifest.get("modules")
    if not isinstance(modules, list) or not modules:
        raise ValueError("manifest modules must be a nonempty list")
    head = _git("rev-parse", "HEAD")
    tree = _git("rev-parse", "HEAD^{tree}")
    lines: list[str] = []
    for item in modules:
        if not isinstance(item, dict):
            raise ValueError("manifest module entry must be an object")
        relative = _safe_relative(
            _required_string(item, "path", "manifest module"), SOURCE_TREE, "source"
        )
        new_hash = _sha256_git_blob("HEAD", relative)
        old_hash = item.get("sha256")
        if new_hash != old_hash:
            lines.append(f"rehashed: {relative.as_posix()} {old_hash} -> {new_hash}")
        item["sha256"] = new_hash
    previous_commit, _ = _source_snapshot(manifest)
    manifest["source_snapshot"] = {"commit": head, "tree": tree}
    MANIFEST_PATH.write_bytes(
        (json.dumps(manifest, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
    )
    lines.append(f"source snapshot: {previous_commit} -> {head}")
    lines.append(
        "prose citing the previous snapshot must be revised by hand; "
        "verification fails until it is"
    )
    return lines


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="verify the source pin, protected boundary, receipt, and prose citations"
    )
    parser.add_argument(
        "--repin",
        action="store_true",
        help="rewrite SOURCE_MANIFEST.json from the blobs at HEAD and move the snapshot to HEAD",
    )
    args = parser.parse_args(argv)
    try:
        if args.repin:
            lines = repin_manifest()
        else:
            lines = verify_manifest() + verify_protected_paths() + verify_receipt_and_prose()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
