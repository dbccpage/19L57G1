"""Custody failures injected into temporary fixtures, never sealed originals."""

from __future__ import annotations

import hashlib
from importlib.machinery import ModuleSpec
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verify_sources as guard

UNCONSUMED = ("prompt/input.md", "paper/claim.md", "artifacts/example.json")


def git(root: Path, *args: str) -> bytes:
    return subprocess.run(["git", "-C", str(root), *args], check=True,
                          capture_output=True).stdout


@pytest.fixture
def source_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Small independent repository with the same custody shapes."""
    root = tmp_path / "fixture"
    root.mkdir()
    git(root, "init", "--quiet")
    git(root, "config", "core.autocrlf", "false")
    git(root, "config", "user.name", "Custody fixture")
    git(root, "config", "user.email", "fixture@example.invalid")
    for relative in (*guard.RUNTIME_PATHS.values(), *guard.CONFIG_PATHS,
                     "lean4/Derivation/Example.lean", *UNCONSUMED):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"# fixture source\n")
    # Explicit paths; this fixture has no user work to collect.
    git(root, "add", "--", *guard.CONSUMED_TREES, *guard.CONFIG_PATHS, *UNCONSUMED)
    git(root, "commit", "--quiet", "-m", "Fixture baseline")
    baseline = git(root, "rev-parse", "HEAD").decode().strip()
    monkeypatch.setattr(guard, "BASELINE_COMMIT", baseline)
    manifest = {
        "schema": guard.SCHEMA,
        "baseline_commit": baseline,
        "text_normalization": "CRLF_TO_LF_ONLY",
        "runtime_modules": guard.RUNTIME_PATHS,
        "consumed_trees": {tree: git(root, "rev-parse", f"{baseline}:{tree}").decode().strip()
                           for tree in guard.CONSUMED_TREES},
        "tree_census": {tree: guard.tree_census(root, tree, suffix)[0]
                        for tree, suffix in guard.CONSUMED_TREES.items()},
        "source_sha256": {path: hashlib.sha256(git(root, "show", f"{baseline}:{path}")).hexdigest()
                          for path in (*guard.RUNTIME_PATHS.values(), *guard.CONFIG_PATHS)},
    }
    packet = root / guard.PACKET
    packet.mkdir(parents=True)
    (packet / "SOURCE_MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
    return root


def test_exact_fixture_passes_and_crlf_checkout_is_accepted(source_fixture: Path) -> None:
    assert guard.verify_sources(source_fixture, check_runtime=False) == []
    for relative in (*guard.RUNTIME_PATHS.values(), *guard.CONFIG_PATHS):
        source = source_fixture / relative
        source.write_bytes(source.read_bytes().replace(b"\n", b"\r\n"))
    # Git's ordinary checkout normalization is part of the declared contract.
    git(source_fixture, "config", "core.autocrlf", "true")
    assert guard.verify_sources(source_fixture, check_runtime=False) == []


@pytest.mark.parametrize("relative", ["code/derivation/model.py", "lean4/lean-toolchain"])
def test_changed_pinned_source_is_named(source_fixture: Path, relative: str) -> None:
    (source_fixture / relative).write_bytes(b"# injected different payload\n")
    failures = guard.verify_sources(source_fixture, check_runtime=False)
    assert f"SOURCE_CHANGED: {relative}" in failures
    assert f"CONSUMED_TRACKED_DIFF: {relative}" in failures


def test_a_changed_but_unpinned_file_in_a_consumed_tree_is_named(source_fixture: Path) -> None:
    """The tree diff covers what the seven module pins do not."""
    other = source_fixture / "code/derivation/other.py"
    other.write_bytes(b"# fixture source\n")
    git(source_fixture, "add", "--", "code/derivation/other.py")
    git(source_fixture, "commit", "--quiet", "-m", "Later change inside a consumed tree")
    assert "CONSUMED_TRACKED_DIFF: code/derivation/other.py" in guard.verify_sources(
        source_fixture, check_runtime=False)


@pytest.mark.parametrize("relative", UNCONSUMED)
def test_a_change_outside_the_consumed_trees_is_not_reported(source_fixture: Path, relative: str) -> None:
    """Schema v1 reported this and schema v2 deliberately does not.

    This packet reads nothing under prompt, paper or artifacts, so a change
    there cannot alter any recorded result. v1 pinned all five sealed trees,
    which made the packet unverifiable on unrelated commits with no repair
    path -- a red that said nothing about the evidence.
    """
    (source_fixture / relative).write_bytes(b"injected unrelated change\n")
    assert guard.verify_sources(source_fixture, check_runtime=False) == []


@pytest.mark.parametrize("relative", ["prompt/scratch.md", "paper/notes.txt", "artifacts/tmp.json"])
def test_a_stray_untracked_file_outside_the_import_path_is_not_reported(
        source_fixture: Path, relative: str) -> None:
    """Also withdrawn from v1: a scratch file is not a source-integrity breach.

    v1 used `git ls-files --others` over all five trees, so any untracked file
    anywhere in them stopped both receipts from being checked at all.
    """
    path = source_fixture / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"scratch\n")
    assert guard.verify_sources(source_fixture, check_runtime=False) == []


def test_staged_change_to_a_consumed_source_survives_working_file_recovery(source_fixture: Path) -> None:
    source = source_fixture / "code/derivation/observe.py"
    original = source.read_bytes()
    source.write_bytes(b"injected staged payload\n")
    git(source_fixture, "add", "--", "code/derivation/observe.py")
    source.write_bytes(original)
    assert "CONSUMED_TRACKED_DIFF: code/derivation/observe.py" in guard.verify_sources(
        source_fixture, check_runtime=False)


@pytest.mark.parametrize("relative", ["code/derivation/new.py", "lean4/Derivation/New.lean"])
def test_untracked_source_census_change_is_named(source_fixture: Path, relative: str) -> None:
    """An untracked file a build or an import WOULD pick up is still refused."""
    (source_fixture / relative).write_bytes(b"# injected source\n")
    failures = guard.verify_sources(source_fixture, check_runtime=False)
    assert any("SOURCE_CENSUS:" in failure and relative in failure for failure in failures)


def test_missing_baseline_fails_closed(source_fixture: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    missing = "0" * 40
    monkeypatch.setattr(guard, "BASELINE_COMMIT", missing)
    path = source_fixture / guard.PACKET / "SOURCE_MANIFEST.json"
    manifest = json.loads(path.read_text())
    manifest["baseline_commit"] = missing
    path.write_text(json.dumps(manifest), encoding="utf-8")
    assert any(failure.startswith("BASELINE_UNAVAILABLE:")
               for failure in guard.verify_sources(source_fixture, check_runtime=False))


def test_a_duplicate_manifest_key_is_refused(source_fixture: Path) -> None:
    """Last-wins JSON semantics would let a second key overwrite a pin."""
    path = source_fixture / guard.PACKET / "SOURCE_MANIFEST.json"
    text = path.read_text(encoding="utf-8")
    doubled = text.replace('{"schema"', '{"baseline_commit": "0", "schema"', 1)
    path.write_text(doubled, encoding="utf-8")
    assert any("duplicate manifest key" in failure
               for failure in guard.verify_sources(source_fixture, check_runtime=False))


@pytest.mark.parametrize("field", ["source_sha256", "consumed_trees", "tree_census"])
def test_manifest_cannot_adopt_source_drift(source_fixture: Path, field: str) -> None:
    path = source_fixture / guard.PACKET / "SOURCE_MANIFEST.json"
    manifest = json.loads(path.read_text())
    if field == "source_sha256":
        source = source_fixture / "code/derivation/model.py"
        source.write_bytes(b"# changed and adopted\n")
        manifest[field]["code/derivation/model.py"] = hashlib.sha256(source.read_bytes()).hexdigest()
    elif field == "consumed_trees":
        manifest[field]["code/derivation"] = "0" * 40
    else:
        manifest[field]["code/derivation"].append("code/derivation/invented.py")
    path.write_text(json.dumps(manifest), encoding="utf-8")
    failures = guard.verify_sources(source_fixture, check_runtime=False)
    assert any("PIN:" in failure or "MANIFEST_TREE_CENSUS:" in failure for failure in failures)


def test_unrelated_later_commit_is_allowed(source_fixture: Path) -> None:
    path = source_fixture / "research/unrelated.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("Later unrelated research\n", encoding="utf-8")
    git(source_fixture, "add", "--", "research/unrelated.txt")
    git(source_fixture, "commit", "--quiet", "-m", "Unrelated research")
    assert guard.verify_sources(source_fixture, check_runtime=False) == []


def test_runtime_origin_and_census_are_independently_checked(source_fixture: Path, tmp_path: Path) -> None:
    modules: dict[str, ModuleType] = {}
    for name, relative in guard.RUNTIME_PATHS.items():
        module = ModuleType(name)
        module.__file__ = str(source_fixture / relative)
        module.__spec__ = ModuleSpec(name, loader=None, origin=module.__file__)
        modules[name] = module
    assert guard.runtime_errors(source_fixture, modules) == []
    foreign = tmp_path / "foreign_model.py"
    foreign.write_bytes((source_fixture / "code/derivation/model.py").read_bytes())
    modules["derivation.model"].__file__ = str(foreign)
    assert any(failure.startswith("RUNTIME_ORIGIN: derivation.model __file__")
               for failure in guard.runtime_errors(source_fixture, modules))
    modules["derivation.model"].__file__ = str(source_fixture / "code/derivation/model.py")
    modules["derivation.model"].__spec__.origin = str(foreign)
    assert any("__spec__.origin" in failure for failure in guard.runtime_errors(source_fixture, modules))
    modules["derivation.unpinned"] = ModuleType("derivation.unpinned")
    assert any(failure.startswith("RUNTIME_CENSUS:") for failure in guard.runtime_errors(source_fixture, modules))


def test_lone_cr_is_not_accepted_as_checkout_conversion() -> None:
    assert guard.canonical_text(b"a\rb\n") != guard.canonical_text(b"a\nb\n")
