"""Read-only custody checks for the sealed and merged inputs this family consumes.

AuthorityEffect: None.
The guard checks source identity and runtime origin, not theorem truth.
Runtime origin covers every module the machines execute: the eight sealed
``derivation`` modules, the merged ``translation``, and the represented
execution family's ``execution`` and ``control``.  A same-named module
resolved from anywhere else is named rather than silently accepted.  CRLF
checkout conversion is allowed for text inputs; pinned Git objects are never
rewritten.  There is deliberately no manifest generation or repair option.

Scope: exactly what this family consumes.  ``code/derivation`` supplies the
eight modules the merged encoder loads when the represented-execution
machines are imported.  ``lean4/Derivation`` supplies the sealed modules the
local proofs import; the merged ``local_reuse``, ``ignition``,
``magnification``, ``setting_translation`` and ``represented_execution`` Lean
trees the packages they build on; the ``setting_translation`` and
``represented_execution`` Python trees the encoder and the machines this
family observes.  The nine trees are pinned by their exact Git tree objects,
the Lean configuration of the six packages by digest, and the represented
execution family's artifact ``evidence/process.json`` — authored there, read
here, never written here — by digest at the commit at which that family is
frozen.  No export is read.  ``prompt`` and ``paper`` are not read and not
pinned.
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

BASELINE_COMMIT = "ab7cc9a521973f8ec69a1cc1a7e9a92591d13acd"
PACKET = Path("research/coherent_process_limits")
SCHEMA = "coherent-process-limits-sources-v1"
CONSUMED_TREES = {
    "code/derivation": ".py",
    "lean4/Derivation": ".lean",
    "research/local_reuse/lean": ".lean",
    "research/ignition/lean": ".lean",
    "research/magnification/lean": ".lean",
    "research/setting_translation/lean": ".lean",
    "research/setting_translation": ".py",
    "research/represented_execution/lean": ".lean",
    "research/represented_execution": ".py",
}
CONFIG_PATHS = (
    "lean4/Derivation.lean",
    "lean4/lean-toolchain",
    "lean4/lakefile.toml",
    "lean4/lake-manifest.json",
    "research/local_reuse/lean/lakefile.toml",
    "research/local_reuse/lean/lean-toolchain",
    "research/ignition/lean/lakefile.toml",
    "research/ignition/lean/lean-toolchain",
    "research/magnification/lean/lakefile.toml",
    "research/magnification/lean/lean-toolchain",
    "research/setting_translation/lean/lakefile.toml",
    "research/setting_translation/lean/lean-toolchain",
    "research/represented_execution/lean/lakefile.toml",
    "research/represented_execution/lean/lean-toolchain",
    "research/represented_execution/evidence/process.json",
)
RUNTIME_PATHS = {
    "derivation": "code/derivation/__init__.py",
    **{f"derivation.{name}": f"code/derivation/{name}.py" for name in (
        "model", "observe", "candidates", "iso", "engine", "export", "primitive_core"
    )},
    "translation": "research/setting_translation/translation.py",
    "execution": "research/represented_execution/execution.py",
    "control": "research/represented_execution/control.py",
}
# The directories the runtime census imports from, in the order the machines
# expect: the sealed code, then the consumed research trees.
IMPORT_ROOTS = ("code", "research/setting_translation", "research/represented_execution")


def canonical_text(raw: bytes) -> bytes:
    """Allow only the ordinary CRLF-to-LF text checkout normalization."""
    return raw.replace(b"\r\n", b"\n")


def _sha(raw: bytes) -> str:
    return hashlib.sha256(canonical_text(raw)).hexdigest()


def _git(root: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(root), "-c", "core.quotePath=false", *args],
        capture_output=True, check=False
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
    errors: list[str] = []
    present = {name for name in modules
               if name in RUNTIME_PATHS or name.startswith("derivation.")}
    if present != set(RUNTIME_PATHS):
        errors.append(
            f"RUNTIME_CENSUS: missing={sorted(set(RUNTIME_PATHS) - present)} "
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
                    errors.append(f"RUNTIME_ORIGIN: {name} {label}={value!r}; expected {expected}")
            except (OSError, RuntimeError):
                errors.append(f"RUNTIME_ORIGIN: {name} {label}={value!r} is unavailable")
    return errors


def tree_census(root: Path, tree: str, suffix: str) -> tuple[list[str], list[str]]:
    baseline = sorted(
        path for path in _git(root, "ls-tree", "-r", "--name-only", BASELINE_COMMIT,
                              "--", tree).decode().splitlines()
        if path.endswith(suffix)
    )
    current = sorted(
        path.relative_to(root).as_posix()
        for path in (root / tree).rglob("*" + suffix)
        if ".lake" not in path.relative_to(root).parts
    )
    return baseline, current


def verify_sources(repo_root: Path | None = None, *, check_runtime: bool = True) -> list[str]:
    """Return named failures; an empty list is a pass for this source scope."""
    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    errors: list[str] = []
    try:
        manifest = json.loads(
            (root / PACKET / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
        )
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
    except (OSError, ValueError, TypeError) as exc:
        return [f"MANIFEST_UNAVAILABLE: {exc}"]
    try:
        resolved = _git(root, "rev-parse", "--verify", f"{BASELINE_COMMIT}^{{commit}}").decode().strip()
        if resolved != BASELINE_COMMIT:
            return ["BASELINE_UNAVAILABLE: resolved commit differs"]
    except (OSError, ValueError) as exc:
        return [f"BASELINE_UNAVAILABLE: {exc}"]
    try:
        for tree, suffix in CONSUMED_TREES.items():
            tree_oid = _git(root, "rev-parse", f"{BASELINE_COMMIT}:{tree}").decode().strip()
            if manifest["consumed_trees"][tree] != tree_oid:
                errors.append(f"BASELINE_TREE_PIN: {tree}")
            baseline, current = tree_census(root, tree, suffix)
            if manifest["tree_census"][tree] != baseline:
                errors.append(f"MANIFEST_TREE_CENSUS: {tree} differs from baseline")
            if current != baseline:
                errors.append(
                    f"SOURCE_CENSUS: {tree}: missing={sorted(set(baseline) - set(current))} "
                    f"unexpected={sorted(set(current) - set(baseline))}"
                )
        for relative, pinned_hash in manifest["source_sha256"].items():
            blob = _git(root, "show", f"{BASELINE_COMMIT}:{relative}")
            if _sha(blob) != pinned_hash:
                errors.append(f"BASELINE_SOURCE_PIN: {relative}")
            source = root / relative
            try:
                if source.resolve(strict=True) != source:
                    errors.append(f"SOURCE_ORIGIN: {relative} resolves outside its pinned path")
                elif canonical_text(source.read_bytes()) != canonical_text(blob):
                    errors.append(f"SOURCE_CHANGED: {relative}")
            except OSError as exc:
                errors.append(f"SOURCE_UNAVAILABLE: {relative}: {exc}")
        consumed = (*CONSUMED_TREES, *CONFIG_PATHS)
        changed = set(_git(root, "diff", "--name-only", "--no-ext-diff", BASELINE_COMMIT,
                           "--", *consumed).decode().splitlines())
        changed.update(_git(root, "diff", "--cached", "--name-only", "--no-ext-diff", BASELINE_COMMIT,
                            "--", *consumed).decode().splitlines())
        errors.extend(f"CONSUMED_TRACKED_DIFF: {path}" for path in sorted(changed))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        errors.append(f"SOURCE_INSPECTION_FAILED: {exc}")
    if errors or not check_runtime:
        return errors
    old_path = sys.path[:]
    try:
        for index, relative in enumerate(IMPORT_ROOTS):
            sys.path.insert(index, str(root / relative))
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
        print(f"PASS: unchanged consumed sources and local runtime origins at {BASELINE_COMMIT}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
