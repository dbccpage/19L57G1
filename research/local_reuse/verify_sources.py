"""Read-only custody checks for this diagnostic's unchanged Genesis inputs.

AuthorityEffect: None
The guard checks source identity and runtime origin, not theorem truth.  CRLF
checkout conversion is allowed for text inputs; pinned Git objects are never
rewritten.  There is deliberately no manifest generation or repair option.

**Scope: what this packet consumes, and nothing else.**  Two trees can change
what this packet computed.  ``code/derivation`` supplies the seven modules
``audit.py`` imports and drives.  ``lean4/Derivation`` supplies the modules
``lean/LocalReuse.lean`` imports, whose whole content the proofs depend on, so
that tree is pinned by its exact Git tree object.  Both are pinned here.

``prompt``, ``paper`` and ``artifacts`` are **not** pinned.  Schema v1 pinned
all five sealed trees by tree object and diffed all five against the baseline.
That was withdrawn: this packet reads none of those three, so churn in them
could not change any recorded result, and pinning them made the packet
unverifiable on unrelated commits with no repair path -- a red that says
nothing about the evidence.  The narrower pin is not a weaker claim about this
packet's inputs; it is the same claim, stated over the inputs it has.

Untracked files are refused only where a build or an import would pick them
up: a ``.py`` under ``code/derivation`` or a ``.lean`` under
``lean4/Derivation``.  Schema v1 refused every untracked file under all five
trees, so an unrelated scratch file anywhere in the repository reported a
source-integrity failure and stopped both receipts from being checked at all.
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

BASELINE_COMMIT = "93853697ed845284ecbb9a9b51a78c9bf5b070cb"
PACKET = Path("research/local_reuse")
SCHEMA = "local-reuse-sources-v2"
# tree -> the suffix whose files a build or an import would consume there.
CONSUMED_TREES = {"code/derivation": ".py", "lean4/Derivation": ".lean"}
CONFIG_PATHS = (
    "lean4/Derivation.lean",
    "lean4/lean-toolchain",
    "lean4/lakefile.toml",
    "lean4/lake-manifest.json",
)
RUNTIME_PATHS = {
    "derivation": "code/derivation/__init__.py",
    **{f"derivation.{name}": f"code/derivation/{name}.py" for name in (
        "model", "observe", "candidates", "iso", "engine", "export"
    )},
}


def canonical_text(raw: bytes) -> bytes:
    """Allow only the ordinary CRLF-to-LF text checkout normalization."""
    return raw.replace(b"\r\n", b"\n")


def _sha(raw: bytes) -> str:
    return hashlib.sha256(canonical_text(raw)).hexdigest()


def _git(root: Path, *args: str) -> bytes:
    result = subprocess.run(
        # -c core.quotePath=false so a non-ASCII path is compared as itself
        # rather than as git's C-escaped rendering of itself.
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
    present = {name for name in modules if name == "derivation" or name.startswith("derivation.")}
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
    """The baseline and current consumable files of one pinned tree.

    Current includes untracked files, because an untracked ``.py`` on the
    import path or an untracked ``.lean`` in the elaborated tree changes what
    runs.  An untracked file of any other kind, anywhere, does not.
    """
    baseline = sorted(
        path for path in _git(root, "ls-tree", "-r", "--name-only", BASELINE_COMMIT,
                              "--", tree).decode().splitlines()
        if path.endswith(suffix)
    )
    current = sorted(
        path.relative_to(root).as_posix()
        for path in (root / tree).rglob("*" + suffix)
    )
    return baseline, current


def verify_sources(repo_root: Path | None = None, *, check_runtime: bool = True) -> list[str]:
    """Return named failures; an empty list is a pass for this source scope.

    The baseline must remain available locally.  Later unrelated commits are
    allowed; changes under the two consumed trees or the explicitly pinned Lean
    configuration are rejected.

    Runtime checking imports the seven modules only after their files pass.
    That ordering holds for this function alone: a caller that imports
    ``derivation`` at its own module scope has already run that code before
    calling here.  ``run.py`` imports ``audit`` inside ``receipt_bytes`` for
    exactly this reason, and the origin check below is what catches an
    already-loaded foreign copy either way.
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
        print(f"PASS: unchanged consumed sources and local runtime origins at {BASELINE_COMMIT}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
