"""Every tracked Lean toolchain pin names the sealed package's toolchain.

The sealed package pins its Lean release in ``lean4/lean-toolchain``, and the
research packages that require it by path compile its modules under their own
pin.  Two pins would mean two compilers for the same sealed sources, so this
test walks every tracked ``lean-toolchain`` file and requires its content to
equal the sealed pin's.

The population comes from ``git ls-files``, so an untracked build directory can
neither add a pin nor hide one.  Content is compared after stripping
surrounding whitespace: some tracked pins end without a newline and some check
out with CRLF line endings, and neither changes which release elan selects.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SEALED_PIN = "lean4/lean-toolchain"
PIN_NAME = "lean-toolchain"


def _tracked_toolchain_pins() -> list[str]:
    """Every tracked path whose final component is ``lean-toolchain``."""
    proc = subprocess.run(
        ["git", "ls-files", "-z"], capture_output=True, cwd=REPO, check=False
    )
    assert proc.returncode == 0, (
        "git ls-files failed: " + proc.stderr.decode("utf-8", "replace")
    )
    pins: list[str] = []
    for raw in proc.stdout.split(b"\0"):
        if not raw:
            continue
        rel = raw.decode("utf-8", "replace").replace("\\", "/")
        if rel.rsplit("/", 1)[-1] == PIN_NAME:
            pins.append(rel)
    return sorted(pins)


def _pin_content(rel: str) -> str | None:
    """Stripped content of a pin, or ``None`` if the tracked file is absent."""
    path = REPO / rel
    if not path.is_file():
        return None
    return path.read_bytes().decode("utf-8", "replace").strip()


def test_census_contains_the_sealed_pin() -> None:
    # Guards the enumeration itself: a census that cannot see the sealed pin
    # would compare nothing and pass.
    pins = _tracked_toolchain_pins()
    assert SEALED_PIN in pins, (
        f"{SEALED_PIN} is not in the tracked census of {PIN_NAME} files: {pins}"
    )


def test_every_tracked_toolchain_pin_matches_the_sealed_pin() -> None:
    sealed = _pin_content(SEALED_PIN)
    assert sealed, f"{SEALED_PIN} is missing or empty"
    offending: list[str] = []
    for rel in _tracked_toolchain_pins():
        content = _pin_content(rel)
        if content != sealed:
            shown = "<missing from working tree>" if content is None else repr(content)
            offending.append(f"  {rel}: {shown}")
    assert not offending, (
        f"{len(offending)} tracked {PIN_NAME} file(s) differ from "
        f"{SEALED_PIN} ({sealed!r}):\n" + "\n".join(offending)
    )
