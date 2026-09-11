"""Read-only custody checks for the sealed derivation blobs this tree imports.

AuthorityEffect: None.

Pins ``code/derivation`` by Git tree plus SHA-256 of the six runtime
modules this tree imports, and ``lean4/Derivation`` plus Lean package
configuration when the local proofs import them.  ``prompt/``,
``paper/``, and ``artifacts/`` are unpinned.  There is no ``--repin``.
Working-tree bytes are compared to baseline blobs without consulting
index flags.  This guard does not claim proved equivalence to
``code/derivation/``.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType
from typing import Mapping

BASELINE_COMMIT = "a4dcddff1a8f8029beb9ec538d26150766dbbcd2"
PACKET = Path("research/alpha_engine")
SCHEMA = "alpha-engine-sources-v1"
CONSUMED_TREES = {
    "code/derivation": ".py",
    "lean4/Derivation": ".lean",
}
CONFIG_PATHS = (
    "lean4/Derivation.lean",
    "lean4/lean-toolchain",
    "lean4/lakefile.toml",
    "lean4/lake-manifest.json",
)
RUNTIME_PATHS = {
    "derivation": "code/derivation/__init__.py",
    "derivation.model": "code/derivation/model.py",
    "derivation.observe": "code/derivation/observe.py",
    "derivation.candidates": "code/derivation/candidates.py",
    "derivation.iso": "code/derivation/iso.py",
    "derivation.engine": "code/derivation/engine.py",
}
ARTIFACT_PATHS: tuple[str, ...] = ()


def canonical_text(raw: bytes) -> bytes:
    """Allow only the ordinary CRLF-to-LF text checkout normalization."""
    return raw.replace(b"\r\n", b"\n")


def _sha(raw: bytes) -> str:
    return hashlib.sha256(canonical_text(raw)).hexdigest()


def _git(root: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(root), "-c", "core.quotePath=false", *args],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise ValueError(result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for name, value in pairs:
        if name in result:
            raise ValueError(f"duplicate manifest key {name}")
        result[name] = value
    return result


def runtime_errors(root: Path, modules: Mapping[str, ModuleType]) -> list[str]:
    """Check the imported module census and both reported source origins."""
    errors: list[str] = []
    present = {
        name for name in modules
        if name == "derivation" or name.startswith("derivation.")
    }
    if present != set(RUNTIME_PATHS):
        errors.append(
            "RUNTIME_CENSUS: "
            f"missing={sorted(set(RUNTIME_PATHS) - present)} "
            f"unexpected={sorted(present - set(RUNTIME_PATHS))}"
        )
    for name, relative in RUNTIME_PATHS.items():
        module = modules.get(name)
        if module is None:
            continue
        expected = root / relative
        for label, value in (
            ("__file__", getattr(module, "__file__", None)),
            ("__spec__.origin", getattr(getattr(module, "__spec__", None), "origin", None)),
        ):
            try:
                actual = Path(value).resolve(strict=True) if isinstance(value, str) else None
                if actual != expected:
                    errors.append(
                        f"RUNTIME_ORIGIN: {name} {label}={value!r}; expected {expected}"
                    )
            except (OSError, RuntimeError):
                errors.append(
                    f"RUNTIME_ORIGIN: {name} {label}={value!r} is unavailable"
                )
    return errors


def worktree_matches_blob(
    root: Path, relative: str, blob: bytes
) -> str | None:
    """Compare working-tree bytes to a baseline blob, independent of the index."""
    path = root / relative
    try:
        if path.resolve(strict=True) != path:
            return f"SOURCE_ORIGIN: {relative} resolves outside its pinned path"
        raw = path.read_bytes()
    except OSError as exc:
        return f"SOURCE_UNAVAILABLE: {relative}: {exc}"
    if canonical_text(raw) != canonical_text(blob):
        return f"SOURCE_CHANGED: {relative}"
    return None


def tree_census(root: Path, tree: str, suffix: str) -> tuple[list[str], list[str]]:
    """Baseline and current consumable files of one pinned tree."""
    baseline = sorted(
        path
        for path in _git(
            root, "ls-tree", "-r", "--name-only", BASELINE_COMMIT, "--", tree
        ).decode().splitlines()
        if path.endswith(suffix)
    )
    current = sorted(
        path.relative_to(root).as_posix()
        for path in (root / tree).rglob("*" + suffix)
        if ".lake" not in path.relative_to(root).parts
    )
    return baseline, current


def _read_manifest(root: Path) -> dict[str, object] | list[str]:
    try:
        manifest = json.loads(
            (root / PACKET / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
        )
    except (OSError, ValueError, TypeError) as exc:
        return [f"MANIFEST_UNAVAILABLE: {exc}"]
    if not isinstance(manifest, dict) or manifest.get("schema") != SCHEMA:
        return [f"MANIFEST_SCHEMA: expected {SCHEMA} object"]
    if manifest.get("baseline_commit") != BASELINE_COMMIT:
        return ["MANIFEST_BASELINE: unexpected baseline commit"]
    if manifest.get("text_normalization") != "CRLF_TO_LF_ONLY":
        return ["MANIFEST_NORMALIZATION: expected CRLF_TO_LF_ONLY"]
    if manifest.get("runtime_modules") != RUNTIME_PATHS:
        return ["MANIFEST_RUNTIME_CENSUS: runtime module paths differ"]
    if set(manifest.get("consumed_trees", {})) != set(CONSUMED_TREES):
        return ["MANIFEST_CONSUMED_CENSUS: consumed tree paths differ"]
    if set(manifest.get("tree_census", {})) != set(CONSUMED_TREES):
        return ["MANIFEST_TREE_CENSUS: censused tree paths differ"]
    if set(manifest.get("source_sha256", {})) != set(RUNTIME_PATHS.values()) | set(CONFIG_PATHS):
        return ["MANIFEST_SOURCE_CENSUS: pinned source paths differ"]
    if set(manifest.get("artifact_sha256", {})) != set(ARTIFACT_PATHS):
        return ["MANIFEST_ARTIFACT_CENSUS: pinned artifact paths differ"]
    return manifest


def verify_sources(
    repo_root: Path | None = None, *, check_runtime: bool = True
) -> list[str]:
    """Return named failures; an empty list is a pass for this source scope."""
    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    loaded = _read_manifest(root)
    if isinstance(loaded, list):
        return loaded
    manifest = loaded
    errors: list[str] = []
    try:
        resolved = _git(
            root, "rev-parse", "--verify", f"{BASELINE_COMMIT}^{{commit}}"
        ).decode().strip()
        if resolved != BASELINE_COMMIT:
            return ["BASELINE_UNAVAILABLE: resolved commit differs"]
    except (OSError, ValueError) as exc:
        return [f"BASELINE_UNAVAILABLE: {exc}"]
    try:
        for tree, suffix in CONSUMED_TREES.items():
            tree_oid = _git(root, "rev-parse", f"{BASELINE_COMMIT}:{tree}").decode().strip()
            consumed = manifest["consumed_trees"]
            if not isinstance(consumed, dict) or consumed.get(tree) != tree_oid:
                errors.append(f"BASELINE_TREE_PIN: {tree}")
            baseline, current = tree_census(root, tree, suffix)
            census = manifest["tree_census"]
            if not isinstance(census, dict) or census.get(tree) != baseline:
                errors.append(f"MANIFEST_TREE_CENSUS: {tree} differs from baseline")
            if current != baseline:
                errors.append(
                    f"SOURCE_CENSUS: {tree}: "
                    f"missing={sorted(set(baseline) - set(current))} "
                    f"unexpected={sorted(set(current) - set(baseline))}"
                )
            for relative in baseline:
                blob = _git(root, "show", f"{BASELINE_COMMIT}:{relative}")
                failure = worktree_matches_blob(root, relative, blob)
                if failure:
                    errors.append(failure)
        hashes = manifest["source_sha256"]
        if not isinstance(hashes, dict):
            return ["MANIFEST_SOURCE_CENSUS: pinned source paths differ"]
        for relative, pinned_hash in hashes.items():
            blob = _git(root, "show", f"{BASELINE_COMMIT}:{relative}")
            if _sha(blob) != pinned_hash:
                errors.append(f"BASELINE_SOURCE_PIN: {relative}")
            census_map = manifest["tree_census"]
            if not isinstance(census_map, dict):
                return ["MANIFEST_TREE_CENSUS: censused tree paths differ"]
            censused_paths = {
                path
                for paths in census_map.values()
                if isinstance(paths, list)
                for path in paths
            }
            if relative in censused_paths:
                continue
            failure = worktree_matches_blob(root, relative, blob)
            if failure:
                errors.append(failure)
        consumed_args = (*CONSUMED_TREES, *CONFIG_PATHS)
        changed = set(
            _git(
                root,
                "diff",
                "--cached",
                "--name-only",
                "--no-ext-diff",
                BASELINE_COMMIT,
                "--",
                *consumed_args,
            ).decode().splitlines()
        )
        errors.extend(f"CONSUMED_TRACKED_DIFF: {path}" for path in sorted(changed))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        errors.append(f"SOURCE_INSPECTION_FAILED: {exc}")
    if errors or not check_runtime:
        return errors
    old_path = sys.path[:]
    try:
        sys.path.insert(0, str(root / "code"))
        for name in RUNTIME_PATHS:
            importlib.import_module(name)
    except Exception as exc:
        errors.append(f"RUNTIME_IMPORT: {exc}")
    finally:
        sys.path[:] = old_path
    errors.extend(runtime_errors(root, sys.modules))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    failures = verify_sources()
    for failure in failures:
        print(f"FAIL: {failure}")
    if not failures:
        print(
            "PASS: unchanged consumed sources and local runtime origins "
            f"at {BASELINE_COMMIT}"
        )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
