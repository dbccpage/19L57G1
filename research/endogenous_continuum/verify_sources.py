"""Source verification for research/endogenous_continuum.

AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = Path(__file__).resolve().parent / "SOURCE_MANIFEST.json"
MANIFEST_SCHEMA = "endogenous_continuum-sources-v1"
EXPECTED_SOURCE_PATHS = (
    "code/derivation/iso.py",
    "code/derivation/model.py",
    "code/derivation/observe.py",
)
_HEX = frozenset("0123456789abcdef")


def check_sha256(data: bytes, expected: str) -> bool:
    h_raw = hashlib.sha256(data).hexdigest().lower()
    h_norm = hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest().lower()
    return expected.lower() in (h_raw, h_norm)


def check_git_blob(data: bytes, expected: str) -> bool:
    lf_data = data.replace(b"\r\n", b"\n")
    blob_norm = hashlib.sha1(f"blob {len(lf_data)}\0".encode() + lf_data).hexdigest().lower()
    blob_raw = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest().lower()
    return expected.lower() in (blob_norm, blob_raw)


def _valid_hex(value: object, length: int) -> bool:
    return (
        isinstance(value, str)
        and len(value) == length
        and set(value.lower()).issubset(_HEX)
    )


def verify_sources(
    manifest_path: Path = MANIFEST_PATH,
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    errors: list[str] = []
    if not manifest_path.is_file():
        return ["SOURCE_MANIFEST.json missing"]
    try:
        parsed: Any = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"SOURCE_MANIFEST.json is unreadable: {exc}"]
    if not isinstance(parsed, dict):
        return ["SOURCE_MANIFEST.json root must be an object"]
    manifest: dict[str, Any] = parsed
    expected_top_keys = {"schema", "authority_effect", "sources"}
    if set(manifest) != expected_top_keys:
        errors.append(
            "Manifest keys must be exactly "
            f"{sorted(expected_top_keys)}, got {sorted(manifest)}"
        )
    if manifest.get("schema") != MANIFEST_SCHEMA:
        errors.append(f"Manifest schema must be {MANIFEST_SCHEMA!r}")
    if manifest.get("authority_effect", object()) is not None:
        errors.append("Manifest authority_effect must be null")
    sources = manifest.get("sources")
    if not isinstance(sources, list):
        errors.append("Manifest sources must be a list")
        return errors

    seen_paths: list[str] = []
    repo_resolved = repo_root.resolve()
    for index, item in enumerate(sources):
        if not isinstance(item, dict):
            errors.append(f"Source entry {index} must be an object")
            continue
        expected_item_keys = {"path", "git_blob", "sha256"}
        if set(item) != expected_item_keys:
            errors.append(
                f"Source entry {index} keys must be exactly {sorted(expected_item_keys)}"
            )
            continue
        path_value = item.get("path")
        if not isinstance(path_value, str) or not path_value:
            errors.append(f"Source entry {index} path must be a non-empty string")
            continue
        if "\\" in path_value or Path(path_value).is_absolute() or ".." in Path(path_value).parts:
            errors.append(f"Source path must be a repository-relative POSIX path: {path_value!r}")
            continue
        seen_paths.append(path_value)
        if not _valid_hex(item.get("sha256"), 64):
            errors.append(f"Invalid sha256 pin for {path_value}")
            continue
        if not _valid_hex(item.get("git_blob"), 40):
            errors.append(f"Invalid git_blob pin for {path_value}")
            continue
        p = (repo_root / path_value).resolve()
        try:
            p.relative_to(repo_resolved)
        except ValueError:
            errors.append(f"Source path escapes repository root: {path_value}")
            continue
        if not p.is_file():
            errors.append(f"Missing source file: {path_value}")
            continue
        data = p.read_bytes()
        if "sha256" in item and not check_sha256(data, item["sha256"]):
            actual = hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()
            errors.append(f"Hash mismatch for {path_value}: expected {item['sha256']}, got {actual}")
        if "git_blob" in item and not check_git_blob(data, item["git_blob"]):
            lf_data = data.replace(b"\r\n", b"\n")
            actual_blob = hashlib.sha1(f"blob {len(lf_data)}\0".encode() + lf_data).hexdigest()
            errors.append(f"Git blob mismatch for {path_value}: expected {item['git_blob']}, got {actual_blob}")

    if len(seen_paths) != len(set(seen_paths)):
        errors.append("Manifest source paths must be unique")
    if tuple(sorted(seen_paths)) != EXPECTED_SOURCE_PATHS:
        errors.append(
            f"Manifest source paths must be exactly {list(EXPECTED_SOURCE_PATHS)}, "
            f"got {sorted(seen_paths)}"
        )
    return errors


def main() -> int:
    errs = verify_sources()
    if errs:
        for e in errs:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print("PASS: all source pins match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
