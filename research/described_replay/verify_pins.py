"""Verify source custody, native freezes, and the write boundary.

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import copy
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, replace
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import stat
import subprocess
from typing import Any, Literal, cast

from receipt_io import JSONValue, deterministic_json_bytes, write_bytes_atomic


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SNAPSHOT = "f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be"
SNAPSHOT_TREE = "c992aa1f6270399439f02319e436d2d789776f92"
FREEZE_COMMIT = "950b0a75982c8a0c80c33a74d98f9d2a7eba1457"
WRITE_ROOT = "research/described_replay/"
OUTSIDE_BET_COMMITMENT = (
    "5534f09d5cfcbb20b45fdc1ee42c615d4af224c5ced973dda5b74d522bb1cfd6"
)
MANIFEST = HERE / "SOURCE_MANIFEST.json"
PIN_RECEIPT = HERE / "receipts" / "pins" / "injections.json"
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
_FILE_ATTRIBUTE_REPARSE_POINT = 0x400

PATH_POPULATION_COMMANDS: tuple[tuple[str, ...], ...] = (
    ("diff", "--name-only", "-z", SNAPSHOT, "HEAD", "--"),
    ("diff", "--cached", "--name-only", "-z", "--"),
    ("diff", "--name-only", "-z", "--"),
    ("ls-files", "--others", "--exclude-standard", "-z"),
    ("ls-files", "--others", "--ignored", "--exclude-standard", "-z"),
)

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


@dataclass(frozen=True)
class VerificationState:
    resolved_snapshot_tree: str
    snapshot_is_ancestor: bool
    source_objects: Mapping[tuple[str, str], tuple[str, bytes]]
    freeze_parent: str
    native_freezes: Mapping[str, tuple[bytes, bytes, bytes]]


@dataclass(frozen=True)
class PinReceiptEntry:
    kind: Literal["file", "directory", "reparse", "other"]
    payload: bytes | None


class DuplicateNameError(ValueError):
    """A JSON object repeated a name."""


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateNameError(f"duplicate JSON name: {key}")
        result[key] = value
    return result


def _git_environment() -> dict[str, str]:
    environment = dict(os.environ)
    environment["GIT_CONFIG_GLOBAL"] = os.devnull
    environment["GIT_CONFIG_NOSYSTEM"] = "1"
    return environment


def git_bytes(*args: str) -> bytes:
    completed = subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=False,
        capture_output=True,
        env=_git_environment(),
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


def git_object(revision: str, path: str) -> tuple[str, bytes]:
    blob = git_text("rev-parse", f"{revision}:{path}")
    return blob, git_bytes("cat-file", "blob", blob)


def capture_verification_state() -> VerificationState:
    head = git_text("rev-parse", "HEAD")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", SNAPSHOT, head],
        cwd=REPO,
        check=False,
        capture_output=True,
        env=_git_environment(),
    )
    source_objects = {
        (revision, path): git_object(revision, path)
        for path in SOURCE_PATHS
        for revision in (SNAPSHOT, "HEAD")
    }
    native_freezes = {
        name: (
            blob_bytes(FREEZE_COMMIT, f"{WRITE_ROOT}{name}"),
            blob_bytes("HEAD", f"{WRITE_ROOT}{name}"),
            (HERE / name).read_bytes(),
        )
        for name in ("PROMPT.md", "PREDICTIONS.md")
    }
    return VerificationState(
        resolved_snapshot_tree=git_text("rev-parse", f"{SNAPSHOT}^{{tree}}"),
        snapshot_is_ancestor=ancestor.returncode == 0,
        source_objects=source_objects,
        freeze_parent=git_text("rev-parse", f"{FREEZE_COMMIT}^"),
        native_freezes=native_freezes,
    )


def lf_span(data: bytes, start: int, end: int) -> bytes:
    normalized = data.replace(b"\r\n", b"\n")
    lines = normalized.splitlines(keepends=True)
    if start < 1 or end < start or end > len(lines):
        raise ValueError(f"invalid span {start}-{end} for {len(lines)} lines")
    body = b"".join(lines[start - 1 : end])
    if not body.endswith(b"\n"):
        body += b"\n"
    return body


def source_entry(
    path: str, state: VerificationState | None = None
) -> dict[str, object]:
    blob, data = (
        git_object(SNAPSHOT, path)
        if state is None
        else state.source_objects[(SNAPSHOT, path)]
    )
    return {"git_blob": blob, "path": path, "sha256": sha256(data).hexdigest()}


def build_manifest(state: VerificationState | None = None) -> dict[str, object]:
    if not HEX40.fullmatch(SNAPSHOT) or not HEX40.fullmatch(SNAPSHOT_TREE):
        raise ValueError("source snapshot identifiers must be exact hashes")
    if git_text("rev-parse", SNAPSHOT) != SNAPSHOT:
        raise ValueError("source snapshot does not resolve exactly")
    resolved_tree = (
        git_text("rev-parse", f"{SNAPSHOT}^{{tree}}")
        if state is None
        else state.resolved_snapshot_tree
    )
    if resolved_tree != SNAPSHOT_TREE:
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
    predictions_bytes = (
        (HERE / "PREDICTIONS.md").read_bytes()
        if state is None
        else state.native_freezes["PREDICTIONS.md"][2]
    )
    prompt_bytes = (
        (HERE / "PROMPT.md").read_bytes()
        if state is None
        else state.native_freezes["PROMPT.md"][2]
    )
    return {
        "authority_effect": None,
        "freeze_commit": FREEZE_COMMIT,
        "outside_bet_commitment_sha256": OUTSIDE_BET_COMMITMENT,
        "predictions_freezes": [sha256(predictions_bytes).hexdigest()],
        "prompt_native_sha256": sha256(prompt_bytes).hexdigest(),
        "snapshot_commit": SNAPSHOT,
        "snapshot_tree": SNAPSHOT_TREE,
        "sources": [source_entry(path, state) for path in SOURCE_PATHS],
        "spans": spans,
        "toolchains": {
            "lean4/lean-toolchain": (
                blob_bytes(SNAPSHOT, "lean4/lean-toolchain")
                if state is None
                else state.source_objects[(SNAPSHOT, "lean4/lean-toolchain")][1]
            )
            .decode("utf-8")
            .strip()
        },
        "write_root": WRITE_ROOT,
    }


def render_manifest(state: VerificationState | None = None) -> bytes:
    return deterministic_json_bytes(cast(JSONValue, build_manifest(state)))


def load_manifest_bytes(raw: bytes) -> dict[str, Any]:
    loaded = json.loads(raw.decode("ascii"), object_pairs_hook=_unique_object)
    if not isinstance(loaded, dict):
        raise ValueError("manifest root must be an object")
    return loaded


def load_manifest() -> dict[str, Any]:
    return load_manifest_bytes(MANIFEST.read_bytes())


def _paths_from(command: tuple[str, ...]) -> set[str]:
    output = git_bytes(*command)
    return {
        raw.decode("utf-8", "replace").replace("\\", "/")
        for raw in output.split(b"\0")
        if raw
    }


def merge_path_populations(populations: Iterable[Iterable[str]]) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                path.replace("\\", "/")
                for population in populations
                for path in population
                if path
            }
        )
    )


def changed_paths() -> tuple[str, ...]:
    return merge_path_populations(
        _paths_from(command) for command in PATH_POPULATION_COMMANDS
    )


def scope_failures(paths: Iterable[str]) -> tuple[str, ...]:
    return tuple(
        sorted(
            path.replace("\\", "/")
            for path in paths
            if not path.replace("\\", "/").startswith(WRITE_ROOT)
        )
    )


def scope_failure_messages(paths: Iterable[str]) -> list[str]:
    invalid = scope_failures(paths)
    return (
        [f"paths outside write root changed: {list(invalid)}"] if invalid else []
    )


def manifest_declaration_failures(
    manifest: Mapping[str, Any], expected: Mapping[str, Any]
) -> list[str]:
    failures: list[str] = []
    scalar_fields = (
        ("authority_effect", "authority effect differs"),
        ("freeze_commit", "freeze commit differs"),
        ("outside_bet_commitment_sha256", "outside bet commitment differs"),
        ("predictions_freezes", "predictions freeze differs"),
        ("prompt_native_sha256", "native prompt hash differs"),
        ("snapshot_commit", "snapshot commit differs"),
        ("snapshot_tree", "snapshot tree differs"),
        ("toolchains", "toolchain declaration differs"),
        ("write_root", "write root differs"),
    )
    for field, message in scalar_fields:
        if manifest.get(field, "missing") != expected.get(field, "missing"):
            failures.append(message)

    sources = manifest.get("sources")
    expected_sources = expected.get("sources")
    if not isinstance(sources, list) or not isinstance(expected_sources, list):
        failures.append("sources must be a list")
    else:
        source_paths = [
            str(entry.get("path")) for entry in sources if isinstance(entry, dict)
        ]
        expected_paths = [
            str(entry.get("path"))
            for entry in expected_sources
            if isinstance(entry, dict)
        ]
        if (
            len(source_paths) != len(sources)
            or len(expected_paths) != len(expected_sources)
            or sorted(source_paths) != sorted(expected_paths)
        ):
            failures.append("source path census differs")
        else:
            observed_by_path = {
                str(entry["path"]): entry
                for entry in sources
                if isinstance(entry, dict) and "path" in entry
            }
            expected_by_path = {
                str(entry["path"]): entry
                for entry in expected_sources
                if isinstance(entry, dict) and "path" in entry
            }
            for path in sorted(expected_by_path):
                if observed_by_path.get(path) != expected_by_path[path]:
                    failures.append(f"source declaration differs: {path}")

    if manifest.get("spans") != expected.get("spans"):
        failures.append("span declarations differ")
    return failures


def verify_source_objects(
    manifest: Mapping[str, Any], state: VerificationState | None = None
) -> list[str]:
    active = capture_verification_state() if state is None else state
    failures: list[str] = []
    if manifest.get("snapshot_commit") != SNAPSHOT:
        failures.append("snapshot commit differs")
    if manifest.get("snapshot_tree") != SNAPSHOT_TREE:
        failures.append("snapshot tree differs")
    if active.resolved_snapshot_tree != SNAPSHOT_TREE:
        failures.append("resolved snapshot tree differs")
    if not active.snapshot_is_ancestor:
        failures.append("snapshot is not an ancestor of HEAD")
    entries = manifest.get("sources")
    if not isinstance(entries, list):
        return failures + ["sources must be a list"]
    by_path = {
        str(entry.get("path")): entry for entry in entries if isinstance(entry, dict)
    }
    if len(entries) != len(SOURCE_PATHS) or set(by_path) != set(SOURCE_PATHS):
        failures.append("source path census differs")
        return failures
    for path in SOURCE_PATHS:
        entry = by_path[path]
        wanted_blob = str(entry.get("git_blob"))
        wanted_sha = str(entry.get("sha256"))
        for revision in (SNAPSHOT, "HEAD"):
            try:
                blob, data = active.source_objects[(revision, path)]
            except KeyError:
                failures.append(f"source object absent at {revision}:{path}")
                continue
            if blob != wanted_blob:
                failures.append(f"{path} blob differs at {revision}")
            if sha256(data).hexdigest() != wanted_sha:
                failures.append(f"{path} bytes differ at {revision}")
    return failures


def verify_spans(
    manifest: Mapping[str, Any], state: VerificationState | None = None
) -> list[str]:
    active = capture_verification_state() if state is None else state
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
                data = active.source_objects[(revision, path)][1]
                got = sha256(lf_span(data, start, end)).hexdigest()
            except KeyError:
                failures.append(f"span source absent at {revision}:{path}")
                continue
            except ValueError as error:
                failures.append(str(error))
                continue
            if got != wanted:
                failures.append(f"{path}:{start}-{end} span differs at {revision}")
    return failures


def verify_native_freezes(
    manifest: Mapping[str, Any], state: VerificationState | None = None
) -> list[str]:
    active = capture_verification_state() if state is None else state
    failures: list[str] = []
    if manifest.get("freeze_commit") != FREEZE_COMMIT:
        failures.append("freeze commit differs")
    if active.freeze_parent != SNAPSHOT:
        failures.append("freeze commit parent differs from source snapshot")
    for name in ("PROMPT.md", "PREDICTIONS.md"):
        frozen, head, current = active.native_freezes[name]
        if head != frozen:
            failures.append(f"{name} differs from freeze commit at HEAD")
        if current != frozen:
            failures.append(f"{name} differs from freeze commit in worktree")
    return failures


def manifest_bytes_failures(observed: bytes, expected: bytes) -> list[str]:
    return (
        ["manifest bytes differ from deterministic renderer"]
        if observed != expected
        else []
    )


def _is_reparse(info: os.stat_result) -> bool:
    attributes = int(getattr(info, "st_file_attributes", 0))
    tag = int(getattr(info, "st_reparse_tag", 0))
    return bool(attributes & _FILE_ATTRIBUTE_REPARSE_POINT) or tag != 0


def _same_identity(left: os.stat_result, right: os.stat_result) -> bool:
    return left.st_dev == right.st_dev and left.st_ino == right.st_ino


def _plain_file_payload(path: Path, before: os.stat_result) -> bytes:
    flags = os.O_RDONLY | int(getattr(os, "O_BINARY", 0))
    no_follow = int(getattr(os, "O_NOFOLLOW", 0))
    descriptor = os.open(path, flags | no_follow)
    try:
        opened = os.fstat(descriptor)
        if (
            not stat.S_ISREG(opened.st_mode)
            or _is_reparse(opened)
            or not _same_identity(before, opened)
        ):
            raise ValueError(f"pin receipt identity changed before read: {path.name}")
        with os.fdopen(descriptor, "rb", closefd=True) as handle:
            descriptor = -1
            payload = handle.read()
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    after = path.lstat()
    if (
        not stat.S_ISREG(after.st_mode)
        or stat.S_ISLNK(after.st_mode)
        or _is_reparse(after)
        or not _same_identity(opened, after)
    ):
        raise ValueError(f"pin receipt identity changed during read: {path.name}")
    return payload


def pin_receipt_snapshot() -> dict[str, PinReceiptEntry]:
    directory = PIN_RECEIPT.parent
    if not directory.exists():
        return {}
    root_info = directory.lstat()
    if (
        not stat.S_ISDIR(root_info.st_mode)
        or stat.S_ISLNK(root_info.st_mode)
        or _is_reparse(root_info)
    ):
        raise ValueError("pin receipt root is not a plain directory")
    snapshot: dict[str, PinReceiptEntry] = {}
    for path in sorted(directory.iterdir(), key=lambda item: item.name):
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode) or _is_reparse(info):
            snapshot[path.name] = PinReceiptEntry("reparse", None)
        elif stat.S_ISREG(info.st_mode):
            snapshot[path.name] = PinReceiptEntry(
                "file", _plain_file_payload(path, info)
            )
        elif stat.S_ISDIR(info.st_mode):
            snapshot[path.name] = PinReceiptEntry("directory", None)
        else:
            snapshot[path.name] = PinReceiptEntry("other", None)
    return snapshot


def pin_receipt_snapshot_failures(
    snapshot: Mapping[str, PinReceiptEntry], expected: bytes
) -> list[str]:
    expected_census = (PIN_RECEIPT.name,)
    observed_census = tuple(sorted(snapshot))
    failures: list[str] = []
    if observed_census != expected_census:
        failures.append(
            f"pin receipt census differs: got={list(observed_census)} "
            f"wanted={list(expected_census)}"
        )
    for name in observed_census:
        entry = snapshot[name]
        if entry.kind != "file":
            failures.append(
                f"pin receipt entry is not a plain regular file: {name} "
                f"({entry.kind})"
            )
    receipt = snapshot.get(PIN_RECEIPT.name)
    if receipt is not None and receipt.kind == "file" and receipt.payload != expected:
        failures.append("pin injection receipt differs")
    return failures


def _manifest_probe(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return copy.deepcopy(dict(manifest))


def _injection_row(
    identifier: str,
    observed: list[str],
    expected: list[str],
    recovered: bool,
    *,
    population: str = "manifest",
) -> JSONValue:
    if observed != expected:
        raise ValueError(
            f"pin injection {identifier} differed: got={observed} wanted={expected}"
        )
    if not recovered:
        raise ValueError(f"pin injection {identifier} did not recover")
    return {
        "expected_failures": cast(list[JSONValue], expected),
        "id": identifier,
        "observed_failures": cast(list[JSONValue], observed),
        "population": population,
        "recovered": recovered,
    }


def _state_with_source_object(
    state: VerificationState,
    key: tuple[str, str],
    value: tuple[str, bytes] | None,
) -> VerificationState:
    objects = dict(state.source_objects)
    if value is None:
        del objects[key]
    else:
        objects[key] = value
    return replace(state, source_objects=objects)


def _state_with_native(
    state: VerificationState,
    name: str,
    value: tuple[bytes, bytes, bytes],
) -> VerificationState:
    freezes = dict(state.native_freezes)
    freezes[name] = value
    return replace(state, native_freezes=freezes)


def _duplicate_manifest_failures(raw: bytes) -> list[str]:
    try:
        load_manifest_bytes(raw)
    except (DuplicateNameError, UnicodeDecodeError, json.JSONDecodeError) as error:
        return [str(error)]
    return []


def render_pin_injections(state: VerificationState | None = None) -> bytes:
    active = capture_verification_state() if state is None else state
    baseline = build_manifest(active)
    rows: list[JSONValue] = []

    source_recovered = verify_source_objects(baseline, active) == []
    probe = _manifest_probe(baseline)
    sources = cast(list[Any], probe["sources"])
    sources.pop()
    rows.append(
        _injection_row(
            "source_census",
            verify_source_objects(probe, active),
            ["source path census differs"],
            source_recovered,
            population="source_objects",
        )
    )

    probe = _manifest_probe(baseline)
    sources = cast(list[Any], probe["sources"])
    source = cast(dict[str, Any], sources[0])
    source["sha256"] = "0" * 64
    rows.append(
        _injection_row(
            "source_digest",
            verify_source_objects(probe, active),
            [
                f"{SOURCE_PATHS[0]} bytes differ at {SNAPSHOT}",
                f"{SOURCE_PATHS[0]} bytes differ at HEAD",
            ],
            source_recovered,
            population="source_objects",
        )
    )

    head_key = ("HEAD", SOURCE_PATHS[0])
    head_blob, head_bytes = active.source_objects[head_key]
    probe_state = _state_with_source_object(
        active, head_key, ("0" * len(head_blob), head_bytes)
    )
    rows.append(
        _injection_row(
            "source_head_blob",
            verify_source_objects(baseline, probe_state),
            [f"{SOURCE_PATHS[0]} blob differs at HEAD"],
            source_recovered,
            population="source_objects",
        )
    )
    probe_state = _state_with_source_object(
        active, head_key, (head_blob, head_bytes + b"probe")
    )
    rows.append(
        _injection_row(
            "source_head_bytes",
            verify_source_objects(baseline, probe_state),
            [f"{SOURCE_PATHS[0]} bytes differ at HEAD"],
            source_recovered,
            population="source_objects",
        )
    )
    probe_state = _state_with_source_object(active, head_key, None)
    rows.append(
        _injection_row(
            "source_head_absent",
            verify_source_objects(baseline, probe_state),
            [f"source object absent at HEAD:{SOURCE_PATHS[0]}"],
            source_recovered,
            population="source_objects",
        )
    )
    rows.append(
        _injection_row(
            "resolved_snapshot_tree",
            verify_source_objects(
                baseline, replace(active, resolved_snapshot_tree="0" * 40)
            ),
            ["resolved snapshot tree differs"],
            source_recovered,
            population="source_objects",
        )
    )
    rows.append(
        _injection_row(
            "snapshot_ancestry",
            verify_source_objects(
                baseline, replace(active, snapshot_is_ancestor=False)
            ),
            ["snapshot is not an ancestor of HEAD"],
            source_recovered,
            population="source_objects",
        )
    )

    span_recovered = verify_spans(baseline, active) == []
    probe = _manifest_probe(baseline)
    spans = cast(list[Any], probe["spans"])
    span = cast(dict[str, Any], spans[0])
    span["sha256_lf_with_final_lf"] = "0" * 64
    rows.append(
        _injection_row(
            "span_declaration",
            verify_spans(probe, active),
            ["span declarations differ"],
            span_recovered,
            population="span_objects",
        )
    )
    span_path, span_start, span_end, _ = SPAN_SPECS[0]
    span_key = ("HEAD", span_path)
    span_blob, span_bytes = active.source_objects[span_key]
    span_lines = span_bytes.splitlines(keepends=True)
    target_line = span_lines[span_start - 1]
    span_lines[span_start - 1] = b"X" + target_line[1:]
    probe_state = _state_with_source_object(
        active, span_key, (span_blob, b"".join(span_lines))
    )
    rows.append(
        _injection_row(
            "span_head_bytes",
            verify_spans(baseline, probe_state),
            [f"{span_path}:{span_start}-{span_end} span differs at HEAD"],
            span_recovered,
            population="span_objects",
        )
    )

    declaration_recovered = manifest_declaration_failures(baseline, baseline) == []
    scalar_cases = (
        ("freeze_commit", "freeze_commit", "freeze commit differs"),
        ("native_prompt_hash", "prompt_native_sha256", "native prompt hash differs"),
        ("predictions_hash", "predictions_freezes", "predictions freeze differs"),
        ("snapshot_commit", "snapshot_commit", "snapshot commit differs"),
        ("snapshot_tree", "snapshot_tree", "snapshot tree differs"),
        ("toolchains", "toolchains", "toolchain declaration differs"),
        (
            "outside_bet_commitment",
            "outside_bet_commitment_sha256",
            "outside bet commitment differs",
        ),
        ("write_root", "write_root", "write root differs"),
        ("authority_effect", "authority_effect", "authority effect differs"),
    )
    for identifier, field, message in scalar_cases:
        probe = _manifest_probe(baseline)
        probe[field] = "in-memory-probe"
        rows.append(
            _injection_row(
                identifier,
                manifest_declaration_failures(probe, baseline),
                [message],
                declaration_recovered,
                population="manifest_declarations",
            )
        )

    freeze_recovered = verify_native_freezes(baseline, active) == []
    rows.append(
        _injection_row(
            "freeze_parent",
            verify_native_freezes(
                baseline, replace(active, freeze_parent="0" * 40)
            ),
            ["freeze commit parent differs from source snapshot"],
            freeze_recovered,
            population="native_freezes",
        )
    )
    native_name = "PREDICTIONS.md"
    frozen, head, current = active.native_freezes[native_name]
    probe_state = _state_with_native(
        active, native_name, (frozen, head + b"probe", current)
    )
    rows.append(
        _injection_row(
            "freeze_head_bytes",
            verify_native_freezes(baseline, probe_state),
            [f"{native_name} differs from freeze commit at HEAD"],
            freeze_recovered,
            population="native_freezes",
        )
    )
    probe_state = _state_with_native(
        active, native_name, (frozen, head, current + b"probe")
    )
    rows.append(
        _injection_row(
            "freeze_worktree_bytes",
            verify_native_freezes(baseline, probe_state),
            [f"{native_name} differs from freeze commit in worktree"],
            freeze_recovered,
            population="native_freezes",
        )
    )

    manifest_render = deterministic_json_bytes(cast(JSONValue, baseline))
    rows.append(
        _injection_row(
            "manifest_bytes",
            manifest_bytes_failures(manifest_render + b"probe", manifest_render),
            ["manifest bytes differ from deterministic renderer"],
            manifest_bytes_failures(manifest_render, manifest_render) == [],
            population="manifest_bytes",
        )
    )
    duplicate_raw = b'{"authority_effect":null,"authority_effect":null}\n'
    duplicate_expected = ["duplicate JSON name: authority_effect"]
    rows.append(
        _injection_row(
            "duplicate_manifest_name",
            _duplicate_manifest_failures(duplicate_raw),
            duplicate_expected,
            _duplicate_manifest_failures(manifest_render) == [],
            population="manifest_decoder",
        )
    )

    pin_expected = b"baseline\n"
    pin_baseline = {
        PIN_RECEIPT.name: PinReceiptEntry("file", pin_expected),
    }
    pin_recovered = pin_receipt_snapshot_failures(pin_baseline, pin_expected) == []
    rows.append(
        _injection_row(
            "pin_receipt_missing",
            pin_receipt_snapshot_failures({}, pin_expected),
            [
                "pin receipt census differs: got=[] "
                "wanted=['injections.json']"
            ],
            pin_recovered,
            population="pin_receipts",
        )
    )
    probe_pin = dict(pin_baseline)
    probe_pin["extra.json"] = PinReceiptEntry("file", b"{}\n")
    rows.append(
        _injection_row(
            "pin_receipt_extra_file",
            pin_receipt_snapshot_failures(probe_pin, pin_expected),
            [
                "pin receipt census differs: "
                "got=['extra.json', 'injections.json'] "
                "wanted=['injections.json']"
            ],
            pin_recovered,
            population="pin_receipts",
        )
    )
    probe_pin = dict(pin_baseline)
    probe_pin["extra"] = PinReceiptEntry("directory", None)
    rows.append(
        _injection_row(
            "pin_receipt_nonplain",
            pin_receipt_snapshot_failures(probe_pin, pin_expected),
            [
                "pin receipt census differs: got=['extra', 'injections.json'] "
                "wanted=['injections.json']",
                "pin receipt entry is not a plain regular file: extra (directory)",
            ],
            pin_recovered,
            population="pin_receipts",
        )
    )
    probe_pin = {
        PIN_RECEIPT.name: PinReceiptEntry("reparse", None),
    }
    rows.append(
        _injection_row(
            "pin_receipt_reparse",
            pin_receipt_snapshot_failures(probe_pin, pin_expected),
            [
                "pin receipt entry is not a plain regular file: "
                "injections.json (reparse)"
            ],
            pin_recovered,
            population="pin_receipts",
        )
    )
    probe_pin = {
        PIN_RECEIPT.name: PinReceiptEntry("file", b"changed\n"),
    }
    rows.append(
        _injection_row(
            "pin_receipt_bytes",
            pin_receipt_snapshot_failures(probe_pin, pin_expected),
            ["pin injection receipt differs"],
            pin_recovered,
            population="pin_receipts",
        )
    )

    ignored_probe = merge_path_populations(
        (
            (f"{WRITE_ROOT}.cache/inside.probe",),
            ("research/described_replay_escape/.cache/outside.probe",),
        )
    )
    rows.append(
        _injection_row(
            "ignored_untracked_scope",
            scope_failure_messages(ignored_probe),
            [
                "paths outside write root changed: "
                "['research/described_replay_escape/.cache/outside.probe']"
            ],
            scope_failure_messages((f"{WRITE_ROOT}.cache/inside.probe",)) == [],
            population="git_ignored_untracked",
        )
    )

    payload: JSONValue = {
        "authority_effect": None,
        "injection_count": len(rows),
        "rows": rows,
        "terminal": "PIN_VERIFIER_INJECTIONS_REPLAYED",
    }
    return deterministic_json_bytes(payload)


def pin_receipt_failures(expected: bytes) -> list[str]:
    return pin_receipt_snapshot_failures(pin_receipt_snapshot(), expected)


def verify(*, enforce_scope: bool, state: VerificationState | None = None) -> None:
    active = capture_verification_state() if state is None else state
    manifest = load_manifest()
    expected_manifest = build_manifest(active)
    rendered_manifest = deterministic_json_bytes(cast(JSONValue, expected_manifest))
    rendered_pin_receipt = render_pin_injections(active)
    failures = (
        manifest_declaration_failures(manifest, expected_manifest)
        + verify_source_objects(manifest, active)
        + verify_spans(manifest, active)
        + verify_native_freezes(manifest, active)
    )
    failures.extend(manifest_bytes_failures(MANIFEST.read_bytes(), rendered_manifest))
    failures.extend(pin_receipt_failures(rendered_pin_receipt))
    if enforce_scope:
        failures.extend(scope_failure_messages(changed_paths()))
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
    state = capture_verification_state()
    if args.write:
        write_bytes_atomic(MANIFEST, render_manifest(state))
        PIN_RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        write_bytes_atomic(PIN_RECEIPT, render_pin_injections(state))
    verify(enforce_scope=args.write or args.check_scope, state=state)


if __name__ == "__main__":
    main()
