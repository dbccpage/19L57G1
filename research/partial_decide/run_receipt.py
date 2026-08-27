"""Print or deliberately regenerate the verified partial-Decide receipt.

Bootstrap boundary: this entry point and ``verify_pins.py`` necessarily start
before the verifier can establish their own Git custody.  After that early
preflight, receipt rendering runs in a fresh ``-I -B -S`` child before any
receipt or derivation module is imported there.  The isolated child narrows
ambient Python startup; it does not authenticate the already-running entry
point/verifier, interpreter, standard library, Git executable, or pin JSON.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import stat
import sys
import tempfile

from verify_pins import RECEIPT_PATH, render_verified_receipt


REPARSE_POINT = int(getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def _is_reparse(metadata: os.stat_result) -> bool:
    attributes = int(getattr(metadata, "st_file_attributes", 0))
    tag = int(getattr(metadata, "st_reparse_tag", 0))
    return bool(tag or (REPARSE_POINT and attributes & REPARSE_POINT))


def _require_regular(metadata: os.stat_result, label: str) -> None:
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISREG(metadata.st_mode)
        or _is_reparse(metadata)
    ):
        raise OSError(f"{label} must be a regular non-reparse file")


def _existing_target_mode(target: Path) -> int | None:
    try:
        metadata = os.lstat(target)
    except FileNotFoundError:
        return None
    _require_regular(metadata, f"receipt target {target}")
    return stat.S_IMODE(metadata.st_mode)


def _cleanup_after_error(
    descriptor: int | None,
    temporary: Path | None,
    original: BaseException,
) -> None:
    failures: list[OSError] = []
    if descriptor is not None:
        try:
            os.close(descriptor)
        except OSError as close_error:
            failures.append(close_error)
    if temporary is not None:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        except OSError as unlink_error:
            failures.append(unlink_error)
    if failures:
        details = "; ".join(str(item) for item in failures)
        raise OSError(
            f"receipt write failed ({original}); cleanup also failed: {details}"
        ) from failures[-1]


def write_receipt_atomic(target: Path, payload: bytes) -> None:
    """Atomically install exact LF receipt bytes at a safe regular target."""

    if b"\r" in payload:
        raise ValueError("receipt payload contains CR bytes")
    if not payload.endswith(b"\n") or payload.endswith(b"\n\n"):
        raise ValueError("receipt payload must end with exactly one LF")
    target_mode = _existing_target_mode(target)
    descriptor: int | None = None
    temporary: Path | None = None
    temporary_identity: tuple[int, int] | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            dir=target.parent,
            prefix=f".{target.name}.",
            suffix=".tmp",
        )
        temporary = Path(temporary_name)
        temporary_metadata = os.fstat(descriptor)
        _require_regular(temporary_metadata, f"receipt temporary file {temporary}")
        temporary_identity = (temporary_metadata.st_dev, temporary_metadata.st_ino)
        if os.name != "nt":
            os.chmod(descriptor, 0o644 if target_mode is None else target_mode)
        with os.fdopen(descriptor, "wb", closefd=True) as stream:
            descriptor = None
            written = stream.write(payload)
            if written != len(payload):
                raise OSError(
                    f"short receipt write: wrote {written} of {len(payload)} bytes"
                )
            stream.flush()
            os.fsync(stream.fileno())

        current_temporary = os.lstat(temporary)
        _require_regular(current_temporary, f"receipt temporary file {temporary}")
        if (current_temporary.st_dev, current_temporary.st_ino) != temporary_identity:
            raise OSError(f"receipt temporary file identity changed: {temporary}")

        # Recheck immediately before replacement so a target changed to a
        # link, reparse point, directory, or other special file is refused.
        _existing_target_mode(target)
        os.replace(temporary, target)
        temporary = None
    except BaseException as error:
        _cleanup_after_error(descriptor, temporary, error)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help=(
            "atomically replace the existing regular receipt target with the "
            "current verified deterministic bytes"
        ),
    )
    args = parser.parse_args()
    try:
        payload = render_verified_receipt()
    except (
        ImportError,
        OSError,
        RuntimeError,
        ValueError,
    ) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 1
    if args.write:
        try:
            write_receipt_atomic(RECEIPT_PATH, payload)
        except (OSError, ValueError) as error:
            print(f"REFUSED: {error}", file=sys.stderr)
            return 1
        print(f"wrote {RECEIPT_PATH}")
    else:
        sys.stdout.buffer.write(payload)
    return 0


__all__ = ["main", "write_receipt_atomic"]


if __name__ == "__main__":
    raise SystemExit(main())
