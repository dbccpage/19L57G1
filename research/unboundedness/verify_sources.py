"""Read-only custody checks for the sealed inputs this family consumes.

AuthorityEffect: None.
The guard checks source identity and runtime origin, not theorem truth.  CRLF
checkout conversion is allowed for text inputs; pinned Git objects are never
rewritten.  There is deliberately no manifest generation or repair option.

Scope: exactly what this family consumes.  ``code/derivation`` supplies the
modules ``unboundedness.py`` imports.  ``lean4/Derivation`` supplies the
sealed modules the local proofs import; ``research/local_reuse/lean``,
``research/ignition/lean``, ``research/represented_execution/lean``,
``research/setting_translation/lean`` and
``research/coherent_process_limits/lean`` supply the merged packages the
Lake package requires.  Runtime origin of the translation and represented-
execution modules ``reader.py`` imports is pinned by path.  No export is
read.  ``prompt`` and ``paper`` are not pinned.

Untracked files are refused only where a build or an import would pick them
up: a ``.py`` under ``code/derivation`` or a ``.lean`` under a consumed Lean
tree.

2026-09-25: the seven directory pins are retired.  Each of
``code/derivation``, ``lean4/Derivation``, ``research/local_reuse/lean``, ``research/ignition/lean``, ``research/represented_execution/lean``, ``research/setting_translation/lean``, ``research/coherent_process_limits/lean`` was pinned whole, by Git
tree object, a suffix census and a tracked diff, so an edit to any file in
them failed this check whether or not this family reads it.  The pins are
now the files it consumes, measured by importing every module of the tree in
a child interpreter, by the files its tests open, and by the import closure
of its Lean package through its Lake requires: ``RUNTIME_PATHS``,
``CONFIG_PATHS`` and ``ARTIFACT_PATHS`` (as before) and ``LEAN_PATHS``, each
by digest at the baseline, compared with the working tree and covered by the
tracked diff.  An import of a file outside them has to edit a pinned file,
which fails, and an extra module fails the runtime census.  The statements
above that the directories are pinned by Git tree object, and the refusal of
untracked files, are withdrawn with them.

2026-09-25: ``research/magnification/lean/lakefile.toml`` and ``research/magnification/lean/lean-toolchain`` are added to
``CONFIG_PATHS``.  They are in the Lake require closure and were consumed and
not pinned by any file or directory pin.
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

BASELINE_COMMIT = "75564f7796c11aefd40045cb5dc2eed3479af9b9"
PACKET = Path("research/unboundedness")
SCHEMA = "unboundedness-sources-v2"
# tree -> the suffix whose files a build or an import would consume there.
# 2026-09-25: the Lean import closure of the local package through its Lake
# requires, measured; it replaces the directory pins.
LEAN_PATHS = (
    "lean4/Derivation/Attachment.lean",
    "lean4/Derivation/Basic.lean",
    "lean4/Derivation/Bridge.lean",
    "lean4/Derivation/CapacityBound.lean",
    "lean4/Derivation/Compression.lean",
    "lean4/Derivation/CountTransport.lean",
    "lean4/Derivation/Counting.lean",
    "lean4/Derivation/Erasure.lean",
    "lean4/Derivation/Ext.lean",
    "lean4/Derivation/Generator.lean",
    "lean4/Derivation/HigherStructure.lean",
    "lean4/Derivation/Inertia.lean",
    "lean4/Derivation/Mention.lean",
    "lean4/Derivation/Minimality.lean",
    "lean4/Derivation/NoOutside.lean",
    "lean4/Derivation/Pigeonhole.lean",
    "lean4/Derivation/PresentationRelativity.lean",
    "lean4/Derivation/PrimDiff.lean",
    "lean4/Derivation/PrimitiveCore.lean",
    "lean4/Derivation/PrimitivePassage.lean",
    "lean4/Derivation/Progress.lean",
    "lean4/Derivation/Refusal.lean",
    "lean4/Derivation/RefusalFrontier.lean",
    "lean4/Derivation/Represented.lean",
    "lean4/Derivation/Rounds.lean",
    "lean4/Derivation/RuleBridge.lean",
    "lean4/Derivation/SeparationCapacity.lean",
    "lean4/Derivation/TraceAlgebra.lean",
    "lean4/Derivation/TransitionAlphabet.lean",
    "lean4/Derivation/TransitionTransport.lean",
    "research/coherent_process_limits/lean/Chain.lean",
    "research/coherent_process_limits/lean/Limits.lean",
    "research/coherent_process_limits/lean/Periodic.lean",
    "research/coherent_process_limits/lean/Steps.lean",
    "research/coherent_process_limits/lean/TwoLoci.lean",
    "research/ignition/lean/Ignition.lean",
    "research/local_reuse/lean/LocalReuse.lean",
    "research/represented_execution/lean/Control.lean",
    "research/represented_execution/lean/Execution.lean",
    "research/represented_execution/lean/Product.lean",
    "research/represented_execution/lean/Rename.lean",
    "research/represented_execution/lean/Runner.lean",
    "research/represented_execution/lean/Schedule.lean",
    "research/setting_translation/lean/Chains.lean",
    "research/setting_translation/lean/Translation.lean",
)
CONFIG_PATHS = (
    "lean4/Derivation.lean",
    "lean4/lean-toolchain",
    "lean4/lakefile.toml",
    "lean4/lake-manifest.json",
    "research/local_reuse/lean/lakefile.toml",
    "research/local_reuse/lean/lean-toolchain",
    "research/ignition/lean/lakefile.toml",
    "research/ignition/lean/lean-toolchain",
    "research/represented_execution/lean/lakefile.toml",
    "research/represented_execution/lean/lean-toolchain",
    "research/setting_translation/lean/lakefile.toml",
    "research/setting_translation/lean/lean-toolchain",
    "research/coherent_process_limits/lean/lakefile.toml",
    "research/coherent_process_limits/lean/lean-toolchain",
    "research/magnification/lean/lakefile.toml",
    "research/magnification/lean/lean-toolchain",
)
RUNTIME_PATHS = {
    "derivation": "code/derivation/__init__.py",
    **{f"derivation.{name}": f"code/derivation/{name}.py" for name in (
        "model", "observe", "candidates", "iso", "engine", "export", "primitive_core"
    )},
    "translation": "research/setting_translation/translation.py",
    "execution": "research/represented_execution/execution.py",
    "control": "research/represented_execution/control.py",
    "runner": "research/represented_execution/runner.py",
}
# This family reads no export.  The key is present so a missing census fails
# closed rather than by a missing-field exception.
ARTIFACT_PATHS: tuple[str, ...] = ()


def canonical_text(raw: bytes) -> bytes:
    """Allow only the ordinary CRLF-to-LF text checkout normalization."""
    return raw.replace(b"\r\n", b"\n")


def _sha(raw: bytes) -> str:
    return hashlib.sha256(canonical_text(raw)).hexdigest()


def _raw_sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


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
    """Check the actual module census and both reported source origins."""
    errors: list[str] = []
    present = {
        name for name in modules
        if name in RUNTIME_PATHS or name == "derivation" or name.startswith("derivation.")
    }
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


def verify_sources(repo_root: Path | None = None, *, check_runtime: bool = True) -> list[str]:
    """Return named failures; an empty list is a pass for this source scope.

    The baseline must remain available locally.  Later unrelated commits are
    allowed; changes under the consumed trees, the pinned configuration or the
    pinned exports are rejected.  Runtime checking imports the seven modules
    only after their files pass.
    """
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
        if "consumed_trees" in manifest or "tree_census" in manifest:
            return ["MANIFEST_TREE_PINS: whole-directory pins were retired on 2026-09-25"]
        if set(manifest.get("source_sha256", {})) != (
            set(RUNTIME_PATHS.values()) | set(CONFIG_PATHS) | set(LEAN_PATHS)
        ):
            return ["MANIFEST_SOURCE_CENSUS: pinned source paths differ"]
        if set(manifest.get("artifact_sha256", {})) != set(ARTIFACT_PATHS):
            return ["MANIFEST_ARTIFACT_CENSUS: pinned artifact paths differ"]
    except (OSError, ValueError, TypeError) as exc:
        return [f"MANIFEST_UNAVAILABLE: {exc}"]
    try:
        resolved = _git(root, "rev-parse", "--verify", f"{BASELINE_COMMIT}^{{commit}}").decode().strip()
        if resolved != BASELINE_COMMIT:
            return ["BASELINE_UNAVAILABLE: resolved commit differs"]
    except (OSError, ValueError) as exc:
        return [f"BASELINE_UNAVAILABLE: {exc}"]
    try:
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
        for relative, pinned_hash in manifest["artifact_sha256"].items():
            blob = _git(root, "show", f"{BASELINE_COMMIT}:{relative}")
            if _raw_sha(blob) != pinned_hash:
                errors.append(f"BASELINE_ARTIFACT_PIN: {relative}")
            artifact = root / relative
            try:
                if artifact.read_bytes() != blob:
                    errors.append(f"ARTIFACT_CHANGED: {relative}")
            except OSError as exc:
                errors.append(f"ARTIFACT_UNAVAILABLE: {relative}: {exc}")
        consumed = (*RUNTIME_PATHS.values(), *LEAN_PATHS, *CONFIG_PATHS, *ARTIFACT_PATHS)
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
        sys.path.insert(0, str(root / "code"))
        sys.path.insert(0, str(root / "research" / "setting_translation"))
        sys.path.insert(0, str(root / "research" / "represented_execution"))
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
