"""Verify source custody, native freezes, and the write boundary.

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
from collections.abc import Iterable, Mapping
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
from typing import Any


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SNAPSHOT = "f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be"
SNAPSHOT_TREE = "c992aa1f6270399439f02319e436d2d789776f92"
WRITE_ROOT = "research/described_replay/"
MANIFEST = HERE / "SOURCE_MANIFEST.json"
HEX40 = re.compile(r"[0-9a-f]{40}\Z")

SOURCE_PATHS: tuple[str, ...] = (
    "CLAUDE.md",
    "code/derivation/model.py",
    "code/derivation/observe.py",
    "code/derivation/candidates.py",
    "code/derivation/iso.py",
    "code/derivation/engine.py",
    "code/derivation/export.py",
    "prompt/seed_prompt.md",
    "paper/paper_claim_ledger.md",
    "research/genesis_continuation/continuation_plan.md",
    "research/admission_sign_shadow/STATUS.md",
    "lean4/lean-toolchain",
)

SPAN_SPECS: tuple[tuple[str, int, int, str], ...] = (
    (
        "prompt/seed_prompt.md",
        96,
        96,
        "702107c247a7fdd83ac648a357eea5bbe60679344e08785b04dba95db881f32e",
    ),
    (
        "prompt/seed_prompt.md",
        110,
        110,
        "52a7e78214a86cab4790a78a6406200fcf79fd6421641b171033ae31b457a8e1",
    ),
    (
        "prompt/seed_prompt.md",
        188,
        188,
        "3d5b9cfb399cadc8a0a390ede7299f629ea26cea1b4119625ddf4fa9948feea2",
    ),
    (
        "paper/paper_claim_ledger.md",
        689,
        695,
        "8a185b3c88e8f41b31646da6d40a055470627c4709c860dd1d495a8c5cbb9cc9",
    ),
    (
        "research/genesis_continuation/continuation_plan.md",
        86,
        93,
        "96af59792dc84692b3590a4bd6e0cf02b11dd87566b46d7cbb65656cbd2e72ea",
    ),
    (
        "research/admission_sign_shadow/STATUS.md",
        59,
        60,
        "610a8679e3f79ceba1fb00ea5b228c6019d44c292c1df1289a96453a8db151a6",
    ),
)


class DuplicateNameError(ValueError):
    """A JSON object repeated a name."""


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateNameError(f"duplicate JSON name: {key}")
        result[key] = value
    return result


def git_bytes(*args: str) -> bytes:
    completed = subprocess.run(
        ["git", *args], cwd=REPO, check=False, capture_output=True
    )
    if completed.returncode != 0:
        message = completed.stderr.decode("utf-8", "replace").strip()
        raise ValueError(f"git {' '.join(args)} failed: {message}")
    return completed.stdout


def git_text(*args: str) -> str:
    return git_bytes(*args).decode("utf-8").strip()


def blob_bytes(revision: str, path: str) -> bytes:
    blob = git_text("rev-parse", f"{revision}:{path}")
    return git_bytes("cat-file", "blob", blob)


def lf_span(data: bytes, start: int, end: int) -> bytes:
    normalized = data.replace(b"\r\n", b"\n")
    lines = normalized.splitlines(keepends=True)
    if start < 1 or end < start or end > len(lines):
        raise ValueError(f"invalid span {start}-{end} for {len(lines)} lines")
    body = b"".join(lines[start - 1 : end])
    if not body.endswith(b"\n"):
        body += b"\n"
    return body


def source_entry(path: str) -> dict[str, object]:
    blob = git_text("rev-parse", f"{SNAPSHOT}:{path}")
    data = git_bytes("cat-file", "blob", blob)
    return {"git_blob": blob, "path": path, "sha256": sha256(data).hexdigest()}


def build_manifest() -> dict[str, object]:
    if not HEX40.fullmatch(SNAPSHOT) or not HEX40.fullmatch(SNAPSHOT_TREE):
        raise ValueError("source snapshot identifiers must be exact hashes")
    if git_text("rev-parse", SNAPSHOT) != SNAPSHOT:
        raise ValueError("source snapshot does not resolve exactly")
    if git_text("rev-parse", f"{SNAPSHOT}^{{tree}}") != SNAPSHOT_TREE:
        raise ValueError("source snapshot tree differs")
    spans = [
        {
            "end_line": end,
            "path": path,
            "sha256_lf_with_final_lf": wanted,
            "start_line": start,
        }
        for path, start, end, wanted in SPAN_SPECS
    ]
    return {
        "authority_effect": None,
        "predictions_freezes": [sha256((HERE / "PREDICTIONS.md").read_bytes()).hexdigest()],
        "prompt_native_sha256": sha256((HERE / "PROMPT.md").read_bytes()).hexdigest(),
        "snapshot_commit": SNAPSHOT,
        "snapshot_tree": SNAPSHOT_TREE,
        "sources": [source_entry(path) for path in SOURCE_PATHS],
        "spans": spans,
        "toolchains": {
            "lean4/lean-toolchain": blob_bytes(SNAPSHOT, "lean4/lean-toolchain")
            .decode("utf-8")
            .strip()
        },
        "write_root": WRITE_ROOT,
    }


def render_manifest() -> bytes:
    return (json.dumps(build_manifest(), indent=2, sort_keys=True) + "\n").encode(
        "ascii"
    )


def load_manifest() -> dict[str, Any]:
    loaded = json.loads(
        MANIFEST.read_text(encoding="ascii"), object_pairs_hook=_unique_object
    )
    if not isinstance(loaded, dict):
        raise ValueError("manifest root must be an object")
    return loaded


def _paths_from(command: tuple[str, ...]) -> set[str]:
    output = git_bytes(*command)
    return {
        raw.decode("utf-8", "replace").replace("\\", "/")
        for raw in output.split(b"\0")
        if raw
    }


def changed_paths() -> tuple[str, ...]:
    changed: set[str] = set()
    for command in (
        ("diff", "--name-only", "-z", SNAPSHOT, "HEAD", "--"),
        ("diff", "--cached", "--name-only", "-z", "--"),
        ("diff", "--name-only", "-z", "--"),
        ("ls-files", "--others", "--exclude-standard", "-z"),
    ):
        changed.update(_paths_from(command))
    return tuple(sorted(changed))


def scope_failures(paths: Iterable[str]) -> tuple[str, ...]:
    return tuple(
        sorted(
            path.replace("\\", "/")
            for path in paths
            if not path.replace("\\", "/").startswith(WRITE_ROOT)
        )
    )


def verify_source_objects(manifest: Mapping[str, Any]) -> list[str]:
    failures: list[str] = []
    if manifest.get("snapshot_commit") != SNAPSHOT:
        failures.append("snapshot commit differs")
    if manifest.get("snapshot_tree") != SNAPSHOT_TREE:
        failures.append("snapshot tree differs")
    if git_text("rev-parse", f"{SNAPSHOT}^{{tree}}") != SNAPSHOT_TREE:
        failures.append("resolved snapshot tree differs")
    head = git_text("rev-parse", "HEAD")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", SNAPSHOT, head], cwd=REPO
    )
    if ancestor.returncode != 0:
        failures.append("snapshot is not an ancestor of HEAD")
    entries = manifest.get("sources")
    if not isinstance(entries, list):
        return failures + ["sources must be a list"]
    by_path = {
        str(entry.get("path")): entry for entry in entries if isinstance(entry, dict)
    }
    if set(by_path) != set(SOURCE_PATHS):
        failures.append("source path census differs")
        return failures
    for path in SOURCE_PATHS:
        entry = by_path[path]
        wanted_blob = str(entry.get("git_blob"))
        wanted_sha = str(entry.get("sha256"))
        for revision in (SNAPSHOT, "HEAD"):
            try:
                blob = git_text("rev-parse", f"{revision}:{path}")
                data = git_bytes("cat-file", "blob", blob)
            except ValueError as error:
                failures.append(str(error))
                continue
            if blob != wanted_blob:
                failures.append(f"{path} blob differs at {revision}")
            if sha256(data).hexdigest() != wanted_sha:
                failures.append(f"{path} bytes differ at {revision}")
    return failures


def verify_spans(manifest: Mapping[str, Any]) -> list[str]:
    failures: list[str] = []
    entries = manifest.get("spans")
    if not isinstance(entries, list) or len(entries) != len(SPAN_SPECS):
        return ["span census differs"]
    observed = {
        (
            str(entry.get("path")),
            int(entry.get("start_line", 0)),
            int(entry.get("end_line", 0)),
        ): str(entry.get("sha256_lf_with_final_lf"))
        for entry in entries
        if isinstance(entry, dict)
    }
    expected = {(path, start, end): wanted for path, start, end, wanted in SPAN_SPECS}
    if observed != expected:
        failures.append("span declarations differ")
        return failures
    for (path, start, end), wanted in sorted(expected.items()):
        for revision in (SNAPSHOT, "HEAD"):
            try:
                got = sha256(lf_span(blob_bytes(revision, path), start, end)).hexdigest()
            except ValueError as error:
                failures.append(str(error))
                continue
            if got != wanted:
                failures.append(f"{path}:{start}-{end} span differs at {revision}")
    return failures


def verify(*, enforce_scope: bool) -> None:
    manifest = load_manifest()
    failures = verify_source_objects(manifest) + verify_spans(manifest)
    if manifest.get("authority_effect", "missing") is not None:
        failures.append("authority effect differs")
    if manifest.get("write_root") != WRITE_ROOT:
        failures.append("write root differs")
    prompt_hash = sha256((HERE / "PROMPT.md").read_bytes()).hexdigest()
    if manifest.get("prompt_native_sha256") != prompt_hash:
        failures.append("native prompt hash differs")
    predictions_hash = sha256((HERE / "PREDICTIONS.md").read_bytes()).hexdigest()
    if manifest.get("predictions_freezes") != [predictions_hash]:
        failures.append("predictions freeze differs")
    if MANIFEST.read_bytes() != render_manifest():
        failures.append("manifest bytes differ from deterministic renderer")
    if enforce_scope:
        invalid = scope_failures(changed_paths())
        if invalid:
            failures.append(f"paths outside write root changed: {list(invalid)}")
    if failures:
        raise ValueError("; ".join(failures))
    print(
        "pins clean: "
        f"snapshot={SNAPSHOT} sources={len(SOURCE_PATHS)} "
        f"spans={len(SPAN_SPECS)} scope={'checked' if enforce_scope else 'not-checked'}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--check-scope", action="store_true")
    args = parser.parse_args()
    if args.write:
        MANIFEST.write_bytes(render_manifest())
    verify(enforce_scope=args.write or args.check_scope)


if __name__ == "__main__":
    main()
