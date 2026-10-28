"""Scaffold and custody tests for research/endogenous_continuum.

AuthorityEffect: None.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import hashlib
from research.endogenous_continuum.verify_sources import (
    MANIFEST_PATH,
    REPO_ROOT,
    check_sha256,
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


def test_verify_sources_rejects_empty_or_malformed_manifests() -> None:
    empty = json.dumps(
        {
            "schema": "endogenous_continuum-sources-v1",
            "authority_effect": None,
            "sources": [],
        }
    )
    with patch.object(Path, "read_text", return_value=empty):
        assert any("must be exactly" in error for error in verify_sources())

    with patch.object(Path, "read_text", return_value="{"):
        assert any("unreadable" in error for error in verify_sources())


def test_verify_sources_rejects_duplicate_and_escaping_paths() -> None:
    item = {
        "path": "../outside.py",
        "git_blob": "0" * 40,
        "sha256": "0" * 64,
    }
    manifest = json.dumps(
        {
            "schema": "endogenous_continuum-sources-v1",
            "authority_effect": None,
            "sources": [item, item],
        }
    )
    with patch.object(Path, "read_text", return_value=manifest):
        errors = verify_sources()
    assert any("repository-relative POSIX path" in error for error in errors)
    assert any("must be exactly" in error for error in errors)


def test_lean_scaffold_files_exist() -> None:
    lean_dir = Path(__file__).resolve().parent.parent / "lean"
    assert (lean_dir / "lakefile.toml").is_file()
    assert (lean_dir / "lean-toolchain").is_file()
    assert (lean_dir / "EndogenousContinuum.lean").is_file()
    assert (lean_dir / "Inventory.lean").is_file()


def test_check_sha256_accepts_lf_and_crlf_across_platforms() -> None:
    lf_bytes = b"line1\nline2\n"
    crlf_bytes = b"line1\r\nline2\r\n"
    lf_digest = hashlib.sha256(lf_bytes).hexdigest()
    crlf_digest = hashlib.sha256(crlf_bytes).hexdigest()
    assert check_sha256(lf_bytes, lf_digest)
    assert check_sha256(crlf_bytes, lf_digest)
    assert check_sha256(lf_bytes, crlf_digest)
    assert check_sha256(crlf_bytes, crlf_digest)
