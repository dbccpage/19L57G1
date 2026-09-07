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
                     "prompt/input.md", "paper/claim.md", "lean4/Derivation/Example.lean",
                     "artifacts/example.json"):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"# fixture source\n")
    # Explicit paths; this fixture has no user work to collect.
    git(root, "add", "--", *guard.SEALED_TREES, *guard.CONFIG_PATHS)
    git(root, "commit", "--quiet", "-m", "Fixture baseline")
    baseline = git(root, "rev-parse", "HEAD").decode().strip()
    monkeypatch.setattr(guard, "BASELINE_COMMIT", baseline)
    manifest = {
        "schema": "local-reuse-sources-v1",
        "baseline_commit": baseline,
        "text_normalization": "CRLF_TO_LF_ONLY",
        "runtime_modules": guard.RUNTIME_PATHS,
        "sealed_trees": {path: git(root, "rev-parse", f"{baseline}:{path}").decode().strip()
                         for path in guard.SEALED_TREES},
        "source_sha256": {path: hashlib.sha256(git(root, "show", f"{baseline}:{path}")).hexdigest()
                          for path in (*guard.RUNTIME_PATHS.values(), *guard.CONFIG_PATHS)},
        "derivation_python_census": sorted(guard.RUNTIME_PATHS.values()),
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
    assert f"SEALED_TRACKED_DIFF: {relative}" in failures


def test_changed_sealed_source_outside_runtime_is_named(source_fixture: Path) -> None:
    (source_fixture / "paper/claim.md").write_bytes(b"injected claim\n")
    assert "SEALED_TRACKED_DIFF: paper/claim.md" in guard.verify_sources(source_fixture, check_runtime=False)


def test_staged_sealed_change_is_detected_even_after_working_file_recovery(source_fixture: Path) -> None:
    source = source_fixture / "paper/claim.md"
    original = source.read_bytes()
    source.write_bytes(b"injected staged claim\n")
    git(source_fixture, "add", "--", "paper/claim.md")
    source.write_bytes(original)
    assert "SEALED_TRACKED_DIFF: paper/claim.md" in guard.verify_sources(source_fixture, check_runtime=False)


@pytest.mark.parametrize("relative", ["code/derivation/new.py", "lean4/Derivation/New.lean"])
def test_untracked_source_census_change_is_named(source_fixture: Path, relative: str) -> None:
    (source_fixture / relative).write_bytes(b"# injected source\n")
    failures = guard.verify_sources(source_fixture, check_runtime=False)
    assert any("CENSUS:" in failure and relative in failure for failure in failures)


def test_missing_baseline_fails_closed(source_fixture: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    missing = "0" * 40
    monkeypatch.setattr(guard, "BASELINE_COMMIT", missing)
    path = source_fixture / guard.PACKET / "SOURCE_MANIFEST.json"
    manifest = json.loads(path.read_text())
    manifest["baseline_commit"] = missing
    path.write_text(json.dumps(manifest), encoding="utf-8")
    assert any(failure.startswith("BASELINE_UNAVAILABLE:")
               for failure in guard.verify_sources(source_fixture, check_runtime=False))


@pytest.mark.parametrize("field", ["source_sha256", "sealed_trees", "derivation_python_census"])
def test_manifest_cannot_adopt_source_drift(source_fixture: Path, field: str) -> None:
    path = source_fixture / guard.PACKET / "SOURCE_MANIFEST.json"
    manifest = json.loads(path.read_text())
    if field == "source_sha256":
        source = source_fixture / "code/derivation/model.py"
        source.write_bytes(b"# changed and adopted\n")
        manifest[field]["code/derivation/model.py"] = hashlib.sha256(source.read_bytes()).hexdigest()
    elif field == "sealed_trees":
        manifest[field]["code"] = "0" * 40
    else:
        manifest[field].append("code/derivation/invented.py")
    path.write_text(json.dumps(manifest), encoding="utf-8")
    failures = guard.verify_sources(source_fixture, check_runtime=False)
    assert any("PIN:" in failure or "MANIFEST_DERIVATION_CENSUS:" in failure for failure in failures)


def test_unrelated_later_commit_is_allowed(source_fixture: Path) -> None:
    path = source_fixture / "research/unrelated.txt"
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
