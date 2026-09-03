"""Render or check every deterministic Python receipt for this rung.

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
import os
from pathlib import Path
import stat
from typing import Literal, Mapping, TypeAlias, cast

from class_replay import (
    render_class_replay,
    render_description_stage,
    render_stepper_stage,
)
from cost_ledger import render_cost_ledger
from diagonal import render_diagonal_stage
from receipt_io import (
    JSONValue,
    deterministic_json_bytes,
    strict_json_loads,
    write_bytes_atomic,
)
from register import render_register, render_tau


HERE = Path(__file__).resolve().parent
RECEIPTS = HERE / "receipts" / "python"
_FILE_ATTRIBUTE_REPARSE_POINT = 0x400
CORE_PAYLOAD_NAMES: tuple[str, ...] = (
    "description.json",
    "stepper.json",
    "class_replay.json",
    "diagonal.json",
    "cost_ledger.json",
    "register.json",
    "tau.json",
)
INJECTION_NAME = "injections.json"
PAYLOAD_NAMES: tuple[str, ...] = (*CORE_PAYLOAD_NAMES, INJECTION_NAME)
ALL_NAMES: tuple[str, ...] = (*PAYLOAD_NAMES, "machine_receipt.json")


@dataclass(frozen=True)
class ReceiptEntry:
    kind: "ReceiptKind"
    payload: bytes | None


ReceiptKind: TypeAlias = Literal["file", "directory", "reparse", "other"]


def render_payloads() -> dict[str, JSONValue]:
    return {
        "class_replay.json": cast(JSONValue, render_class_replay()),
        "cost_ledger.json": cast(JSONValue, render_cost_ledger()),
        "description.json": cast(JSONValue, render_description_stage()),
        "diagonal.json": cast(JSONValue, render_diagonal_stage()),
        "register.json": cast(JSONValue, render_register()),
        "stepper.json": cast(JSONValue, render_stepper_stage()),
        "tau.json": cast(JSONValue, render_tau()),
    }


def _is_reparse(info: os.stat_result) -> bool:
    attributes = int(getattr(info, "st_file_attributes", 0))
    tag = int(getattr(info, "st_reparse_tag", 0))
    return bool(attributes & _FILE_ATTRIBUTE_REPARSE_POINT) or tag != 0


def _same_identity(left: os.stat_result, right: os.stat_result) -> bool:
    return left.st_dev == right.st_dev and left.st_ino == right.st_ino


def _receipt_kind(info: os.stat_result) -> ReceiptKind:
    if stat.S_ISLNK(info.st_mode) or _is_reparse(info):
        return "reparse"
    if stat.S_ISREG(info.st_mode):
        return "file"
    if stat.S_ISDIR(info.st_mode):
        return "directory"
    return "other"


def receipt_root_failures(kind: ReceiptKind) -> list[str]:
    return (
        []
        if kind == "directory"
        else [f"Python receipt root is not a plain directory ({kind})"]
    )


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
            raise ValueError(f"Python receipt identity changed before read: {path.name}")
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
        raise ValueError(f"Python receipt identity changed during read: {path.name}")
    return payload


def receipt_snapshot(receipt_dir: Path = RECEIPTS) -> dict[str, ReceiptEntry]:
    if not receipt_dir.exists():
        return {}
    root_info = receipt_dir.lstat()
    root_failures = receipt_root_failures(_receipt_kind(root_info))
    if root_failures:
        raise ValueError("; ".join(root_failures))
    snapshot: dict[str, ReceiptEntry] = {}
    for path in sorted(receipt_dir.iterdir(), key=lambda item: item.name):
        info = path.lstat()
        kind = _receipt_kind(info)
        if kind == "file":
            snapshot[path.name] = ReceiptEntry(
                "file", _plain_file_payload(path, info)
            )
        else:
            snapshot[path.name] = ReceiptEntry(kind, None)
    return snapshot


def _object_from_entry(name: str, entry: ReceiptEntry) -> dict[str, JSONValue]:
    if entry.kind != "file" or entry.payload is None:
        raise ValueError(f"Python receipt entry is not a plain regular file: {name}")
    loaded = strict_json_loads(entry.payload, source=name)
    if not isinstance(loaded, dict):
        raise ValueError(f"invalid {name}: JSON root must be an object")
    return loaded


def snapshot_failures(
    rendered: Mapping[str, bytes],
    snapshot: Mapping[str, ReceiptEntry],
    *,
    all_names: tuple[str, ...] = ALL_NAMES,
    payload_names: tuple[str, ...] = PAYLOAD_NAMES,
) -> list[str]:
    failures: list[str] = []
    observed_names = tuple(sorted(snapshot))
    wanted_names = tuple(sorted(all_names))
    if observed_names != wanted_names:
        failures.append(
            f"Python receipt census differs: got={list(observed_names)} "
            f"wanted={list(wanted_names)}"
        )
    for name in observed_names:
        entry = snapshot[name]
        if entry.kind != "file":
            failures.append(
                "Python receipt entry is not a plain regular file: "
                f"{name} ({entry.kind})"
            )

    objects: dict[str, dict[str, JSONValue]] = {}
    for name in all_names:
        candidate = snapshot.get(name)
        if candidate is None or candidate.kind != "file" or candidate.payload is None:
            continue
        try:
            objects[name] = _object_from_entry(name, candidate)
        except ValueError as error:
            failures.append(str(error))
            continue
        if candidate.payload != rendered[name]:
            failures.append(f"Python receipt differs: {name}")

    machine = objects.get("machine_receipt.json")
    if machine is not None:
        hashes = machine.get("output_sha256")
        if not isinstance(hashes, dict):
            failures.append("machine receipt output hash map is absent")
        elif all(
            name in snapshot
            and snapshot[name].kind == "file"
            and snapshot[name].payload is not None
            for name in payload_names
        ):
            observed_hashes: JSONValue = {
                name: sha256(cast(bytes, snapshot[name].payload)).hexdigest()
                for name in payload_names
            }
            if hashes != observed_hashes:
                failures.append("machine receipt output hash map differs")
    return failures


def _checked_injection_row(
    identifier: str,
    observed: list[str],
    expected: list[str],
    recovered: bool,
) -> JSONValue:
    if observed != expected:
        raise ValueError(
            f"Python receipt injection {identifier} differed: "
            f"got={observed} wanted={expected}"
        )
    if not recovered:
        raise ValueError(f"Python receipt injection {identifier} did not recover")
    return {
        "expected_failures": cast(list[JSONValue], expected),
        "id": identifier,
        "observed_failures": cast(list[JSONValue], observed),
        "recovered": recovered,
    }


def _injection_row(
    identifier: str,
    rendered: Mapping[str, bytes],
    snapshot: Mapping[str, ReceiptEntry],
    expected: list[str],
    recovered: bool,
) -> JSONValue:
    observed = snapshot_failures(
        rendered,
        snapshot,
        all_names=("probe.json", "machine_receipt.json"),
        payload_names=("probe.json",),
    )
    return _checked_injection_row(identifier, observed, expected, recovered)


def render_output_injections() -> bytes:
    probe_payload = deterministic_json_bytes({"value": "baseline"})
    probe_machine = deterministic_json_bytes(
        {"output_sha256": {"probe.json": sha256(probe_payload).hexdigest()}}
    )
    rendered = {
        "machine_receipt.json": probe_machine,
        "probe.json": probe_payload,
    }
    baseline = {
        name: ReceiptEntry("file", payload) for name, payload in rendered.items()
    }
    recovered = snapshot_failures(
        rendered,
        baseline,
        all_names=("probe.json", "machine_receipt.json"),
        payload_names=("probe.json",),
    ) == []
    rows: list[JSONValue] = []

    probe = dict(baseline)
    probe["probe.json"] = ReceiptEntry(
        "file", deterministic_json_bytes({"value": "changed"})
    )
    rows.append(
        _injection_row(
            "payload_bytes",
            rendered,
            probe,
            [
                "Python receipt differs: probe.json",
                "machine receipt output hash map differs",
            ],
            recovered,
        )
    )

    probe = dict(baseline)
    probe["extra.json"] = ReceiptEntry("file", b"{}\n")
    rows.append(
        _injection_row(
            "extra_file",
            rendered,
            probe,
            [
                "Python receipt census differs: "
                "got=['extra.json', 'machine_receipt.json', 'probe.json'] "
                "wanted=['machine_receipt.json', 'probe.json']"
            ],
            recovered,
        )
    )

    probe = dict(baseline)
    probe["extra"] = ReceiptEntry("directory", None)
    rows.append(
        _injection_row(
            "extra_directory",
            rendered,
            probe,
            [
                "Python receipt census differs: "
                "got=['extra', 'machine_receipt.json', 'probe.json'] "
                "wanted=['machine_receipt.json', 'probe.json']",
                "Python receipt entry is not a plain regular file: "
                "extra (directory)",
            ],
            recovered,
        )
    )

    for identifier, kind in (
        ("reparse_entry", "reparse"),
        ("other_entry", "other"),
    ):
        probe = dict(baseline)
        probe["probe.json"] = ReceiptEntry(cast(ReceiptKind, kind), None)
        rows.append(
            _injection_row(
                identifier,
                rendered,
                probe,
                [
                    "Python receipt entry is not a plain regular file: "
                    f"probe.json ({kind})"
                ],
                recovered,
            )
        )

    probe = dict(baseline)
    del probe["probe.json"]
    rows.append(
        _injection_row(
            "missing_file",
            rendered,
            probe,
            [
                "Python receipt census differs: got=['machine_receipt.json'] "
                "wanted=['machine_receipt.json', 'probe.json']"
            ],
            recovered,
        )
    )

    invalid_cases = (
        (
            "invalid_json",
            b"{\n",
            "invalid probe.json: Expecting property name enclosed in double quotes: "
            "line 2 column 1 (char 2)",
        ),
        (
            "duplicate_json_name",
            b'{"same":1,"same":2}\n',
            "invalid probe.json: duplicate JSON object name: 'same'",
        ),
        (
            "non_object_json",
            b"[]\n",
            "invalid probe.json: JSON root must be an object",
        ),
    )
    for identifier, invalid_payload, diagnostic in invalid_cases:
        probe = dict(baseline)
        probe["probe.json"] = ReceiptEntry("file", invalid_payload)
        rows.append(
            _injection_row(
                identifier,
                rendered,
                probe,
                [diagnostic, "machine receipt output hash map differs"],
                recovered,
            )
        )

    probe = dict(baseline)
    probe["machine_receipt.json"] = ReceiptEntry(
        "file", deterministic_json_bytes({"terminal": "probe"})
    )
    rows.append(
        _injection_row(
            "hash_map_absent",
            rendered,
            probe,
            [
                "Python receipt differs: machine_receipt.json",
                "machine receipt output hash map is absent",
            ],
            recovered,
        )
    )

    probe = dict(baseline)
    probe["machine_receipt.json"] = ReceiptEntry(
        "file",
        deterministic_json_bytes({"output_sha256": {"probe.json": "0" * 64}}),
    )
    rows.append(
        _injection_row(
            "hash_map_value",
            rendered,
            probe,
            [
                "Python receipt differs: machine_receipt.json",
                "machine receipt output hash map differs",
            ],
            recovered,
        )
    )

    rows.append(
        _checked_injection_row(
            "receipt_root_reparse",
            receipt_root_failures("reparse"),
            ["Python receipt root is not a plain directory (reparse)"],
            receipt_root_failures("directory") == [],
        )
    )

    payload: JSONValue = {
        "authority_effect": None,
        "injection_count": len(rows),
        "rows": rows,
        "terminal": "PYTHON_RECEIPT_INJECTIONS_REPLAYED",
    }
    return deterministic_json_bytes(payload)


def render_outputs() -> dict[str, bytes]:
    payloads = render_payloads()
    rendered = {
        name: deterministic_json_bytes(payloads[name]) for name in CORE_PAYLOAD_NAMES
    }
    rendered[INJECTION_NAME] = render_output_injections()
    class_payload = payloads["class_replay.json"]
    cost_payload = payloads["cost_ledger.json"]
    diagonal_payload = payloads["diagonal.json"]
    register_payload = payloads["register.json"]
    assert isinstance(class_payload, dict)
    assert isinstance(cost_payload, dict)
    assert isinstance(diagonal_payload, dict)
    assert isinstance(register_payload, dict)
    reporter = diagonal_payload["reporter_search"]
    self_description = diagonal_payload["self_description"]
    assert isinstance(reporter, dict)
    assert isinstance(self_description, dict)
    machine: JSONValue = {
        "authority_effect": None,
        "class_id": class_payload["class_id"],
        "class_replay_terminal": class_payload["terminal"],
        "cost_terminal": cost_payload["terminal"],
        "lean_receipt": "manual_verify_lean_separate",
        "output_sha256": {
            name: sha256(rendered[name]).hexdigest() for name in PAYLOAD_NAMES
        },
        "protected_opens": register_payload["opens_unchanged"],
        "register_terminal": register_payload["terminal"],
        "reporter_terminal": reporter["terminal"],
        "self_description_terminal": self_description["terminal"],
        "terminal": "REGISTER_WRITTEN",
        "unbounded": "OPEN_UNBOUNDED",
    }
    rendered["machine_receipt.json"] = deterministic_json_bytes(machine)
    return rendered


def output_census() -> tuple[str, ...]:
    snapshot = receipt_snapshot()
    nonplain = [name for name, entry in snapshot.items() if entry.kind != "file"]
    if nonplain:
        raise ValueError(f"Python receipt census contains non-files: {nonplain}")
    return tuple(sorted(snapshot))


def check_outputs(rendered: dict[str, bytes]) -> None:
    failures = snapshot_failures(rendered, receipt_snapshot())
    if failures:
        raise ValueError("; ".join(failures))


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = render_outputs()
    if args.write:
        RECEIPTS.mkdir(parents=True, exist_ok=True)
        for name in ALL_NAMES:
            write_bytes_atomic(RECEIPTS / name, rendered[name])
    check_outputs(rendered)
    print(
        f"Python receipt replay clean: outputs={len(ALL_NAMES)} "
        f"terminal=REGISTER_WRITTEN"
    )


if __name__ == "__main__":
    main()
