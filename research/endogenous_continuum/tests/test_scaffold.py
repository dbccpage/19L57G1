"""Scaffold and custody tests for research/endogenous_continuum.

AuthorityEffect: None.
"""

from __future__ import annotations

import json
from pathlib import Path

from research.endogenous_continuum.verify_sources import (
    MANIFEST_PATH,
    REPO_ROOT,
    verify_sources,
)


def test_source_manifest_exists() -> None:
    assert MANIFEST_PATH.is_file(), f"SOURCE_MANIFEST.json missing at {MANIFEST_PATH}"


def test_source_manifest_schema_and_entries() -> None:
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert data.get("schema") == "endogenous_continuum-sources-v1"
    assert data.get("authority_effect") is None
    sources = data.get("sources", [])
    paths = {s["path"] for s in sources}
    expected = {
        "code/derivation/model.py",
        "code/derivation/iso.py",
        "code/derivation/observe.py",
    }
    assert paths == expected, f"Manifest sources mismatch: expected {expected}, got {paths}"


def test_verify_sources_passes() -> None:
    errors = verify_sources()
    assert not errors, f"verify_sources reported errors: {errors}"


def test_lean_scaffold_files_exist() -> None:
    lean_dir = Path(__file__).resolve().parent.parent / "lean"
    assert (lean_dir / "lakefile.toml").is_file()
    assert (lean_dir / "lean-toolchain").is_file()
    assert (lean_dir / "EndogenousContinuum.lean").is_file()
    assert (lean_dir / "Inventory.lean").is_file()
