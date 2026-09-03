from __future__ import annotations

import json
import os
import stat
import tempfile
from pathlib import Path
from typing import Never, TypeAlias, cast


JSONScalar: TypeAlias = None | bool | int | float | str
JSONValue: TypeAlias = JSONScalar | list["JSONValue"] | dict[str, "JSONValue"]

WRITE_ROOT = Path(__file__).resolve().parent
_FILE_ATTRIBUTE_REPARSE_POINT = 0x400


class DuplicateNameError(ValueError):
    pass


def _reject_duplicate_names(
    pairs: list[tuple[str, JSONValue]],
) -> dict[str, JSONValue]:
    result: dict[str, JSONValue] = {}
    for name, value in pairs:
        if name in result:
            raise DuplicateNameError(f"duplicate JSON object name: {name!r}")
        result[name] = value
    return result


def _reject_nonstandard_number(name: str) -> Never:
    raise ValueError(f"non-standard JSON number: {name}")


def strict_json_loads(
    raw: str | bytes | bytearray,
    *,
    source: str = "JSON input",
) -> JSONValue:
    try:
        return cast(
            JSONValue,
            json.loads(
                raw,
                object_pairs_hook=_reject_duplicate_names,
                parse_constant=_reject_nonstandard_number,
            ),
        )
    except (DuplicateNameError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid {source}: {error}") from error


def load_json_object(path: Path) -> dict[str, JSONValue]:
    value = strict_json_loads(path.read_bytes(), source=str(path))
    if not isinstance(value, dict):
        raise ValueError(f"invalid {path}: JSON root must be an object")
    return value


def deterministic_json_bytes(value: JSONValue) -> bytes:
    rendered = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=True,
        indent=2,
        sort_keys=True,
    )
    return (rendered + "\n").encode("ascii")


def _is_reparse(info: os.stat_result) -> bool:
    attributes = int(getattr(info, "st_file_attributes", 0))
    tag = int(getattr(info, "st_reparse_tag", 0))
    return bool(attributes & _FILE_ATTRIBUTE_REPARSE_POINT) or tag != 0


def _require_plain_directory(path: Path) -> os.stat_result:
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode):
        raise ValueError(f"receipt parent is not a plain directory: {path}")
    if _is_reparse(info):
        raise ValueError(f"receipt parent is a reparse point: {path}")
    return info


def _existing_plain_file(path: Path) -> os.stat_result | None:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode):
        raise ValueError(f"receipt target is not a plain regular file: {path}")
    if _is_reparse(info):
        raise ValueError(f"receipt target is a reparse point: {path}")
    return info


def _same_identity(left: os.stat_result, right: os.stat_result) -> bool:
    return left.st_dev == right.st_dev and left.st_ino == right.st_ino


def _resolved_target(target: Path) -> Path:
    root = WRITE_ROOT.resolve(strict=True)
    if target.is_absolute():
        candidate = target
    else:
        if ".." in target.parts:
            raise ValueError(f"receipt target contains parent traversal: {target}")
        candidate = root / target
    resolved = candidate.resolve(strict=False)
    if resolved == root or not resolved.is_relative_to(root):
        raise ValueError(f"receipt target is outside the write root: {target}")
    return resolved


def _validate_payload(payload: bytes) -> None:
    if b"\r" in payload:
        raise ValueError("receipt bytes must be LF-only")
    if not payload.endswith(b"\n") or payload[:-1].endswith(b"\n"):
        raise ValueError("receipt bytes must end in exactly one LF")


def write_bytes_atomic(target: Path, payload: bytes) -> Path:
    _validate_payload(payload)
    destination = _resolved_target(target)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.parent.resolve(strict=True) != destination.parent:
        raise ValueError(f"receipt parent resolves elsewhere: {destination.parent}")

    parent_before = _require_plain_directory(destination.parent)
    target_before = _existing_plain_file(destination)
    file_descriptor: int | None = None
    temporary: Path | None = None
    try:
        file_descriptor, temporary_name = tempfile.mkstemp(
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
        )
        temporary = Path(temporary_name)
        opened = os.fstat(file_descriptor)
        if not stat.S_ISREG(opened.st_mode) or _is_reparse(opened):
            raise ValueError(f"temporary receipt is not a plain file: {temporary}")

        with os.fdopen(file_descriptor, "wb", closefd=True) as handle:
            file_descriptor = None
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())

        temporary_after = temporary.lstat()
        if not _same_identity(opened, temporary_after):
            raise RuntimeError("temporary receipt identity changed before replacement")
        if not stat.S_ISREG(temporary_after.st_mode) or _is_reparse(temporary_after):
            raise ValueError(f"temporary receipt changed type: {temporary}")

        parent_after = _require_plain_directory(destination.parent)
        if not _same_identity(parent_before, parent_after):
            raise RuntimeError("receipt parent identity changed before replacement")

        target_after = _existing_plain_file(destination)
        if target_before is None:
            if target_after is not None:
                raise RuntimeError("receipt target appeared before replacement")
        elif target_after is None or not _same_identity(target_before, target_after):
            raise RuntimeError("receipt target identity changed before replacement")
        else:
            os.chmod(temporary, stat.S_IMODE(target_before.st_mode))

        os.replace(temporary, destination)
        temporary = None
        return destination
    except BaseException as error:
        if file_descriptor is not None:
            try:
                os.close(file_descriptor)
            except OSError:
                pass
        if temporary is not None:
            try:
                temporary.unlink(missing_ok=True)
            except BaseException as cleanup_error:
                raise RuntimeError(
                    f"receipt write failed ({error!r}) and temporary cleanup failed "
                    f"({cleanup_error!r})"
                ) from error
        raise


def write_json_atomic(target: Path, value: JSONValue) -> Path:
    return write_bytes_atomic(target, deterministic_json_bytes(value))


__all__ = [
    "DuplicateNameError",
    "JSONValue",
    "WRITE_ROOT",
    "deterministic_json_bytes",
    "load_json_object",
    "strict_json_loads",
    "write_bytes_atomic",
    "write_json_atomic",
]
