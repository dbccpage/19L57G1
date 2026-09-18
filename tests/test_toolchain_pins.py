"""One Lean toolchain everywhere, and one Python version at the repository root.

The sealed package pins its Lean release in ``lean4/lean-toolchain``.  Elan
builds a Lean file with the nearest ``lean-toolchain`` at or above its
directory, and falls back to its own default when there is none, so two
compilers can arise from a second pin or from a missing one.  These tests
require every tracked pin to equal the sealed pin, every tracked Lean file to
have a pin at or above it, and every research script that writes the release
into a receipt as a string to name the sealed release.

For Python, ``.python-version`` (which uv reads), the root mypy target, and
the ``python-version`` of each setup step in the written workflow must name
the same version.  Research trees with their own ``pyproject.toml`` set their
own mypy targets and are not covered.

Populations come from ``git ls-files``, so an untracked build directory can
neither add a pin nor hide one.  Pins are compared after stripping
surrounding whitespace: some end without a newline and some check out with
CRLF, and neither changes the release elan selects.
"""

from __future__ import annotations

import functools
import re
import subprocess
import tomllib
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parent.parent
SEALED_PIN = "lean4/lean-toolchain"
PIN_NAME = "lean-toolchain"
RELEASE_LITERAL = re.compile(r"leanprover/lean4:v[0-9][0-9A-Za-z.\-]*")
WORKFLOW_PYTHON = re.compile(r"""python-version:\s*["']?([0-9.]+)["']?""")


@functools.cache
def _tracked() -> tuple[str, ...]:
    proc = subprocess.run(["git", "ls-files", "-z"], capture_output=True, cwd=REPO, check=False)
    assert proc.returncode == 0, "git ls-files failed: " + proc.stderr.decode("utf-8", "replace")
    return tuple(p for p in proc.stdout.decode("utf-8").split("\0") if p)


def _text(rel: str) -> str:
    return (REPO / rel).read_bytes().decode("utf-8").strip()


def _sealed() -> str:
    sealed = _text(SEALED_PIN)
    assert sealed, f"{SEALED_PIN} is empty"
    return sealed


def test_every_tracked_toolchain_pin_matches_the_sealed_pin() -> None:
    pins = [p for p in _tracked() if PurePosixPath(p).name == PIN_NAME]
    assert SEALED_PIN in pins, f"the census of {PIN_NAME} files cannot see {SEALED_PIN}"
    sealed = _sealed()
    offending = [f"  {rel}: {_text(rel)!r}" for rel in pins if _text(rel) != sealed]
    assert not offending, (
        f"{len(offending)} tracked {PIN_NAME} file(s) differ from {SEALED_PIN} "
        f"({sealed!r}):\n" + "\n".join(offending)
    )


def test_every_tracked_lean_file_has_a_pin_at_or_above_it() -> None:
    pinned_dirs = {PurePosixPath(p).parent for p in _tracked() if PurePosixPath(p).name == PIN_NAME}
    unpinned = sorted({
        str(PurePosixPath(p).parent)
        for p in _tracked()
        if p.endswith(".lean")
        and not any(d in pinned_dirs for d in [PurePosixPath(p).parent, *PurePosixPath(p).parents])
    })
    assert not unpinned, (
        "Lean files with no lean-toolchain at or above them, so elan uses its default "
        "release:\n" + "\n".join(f"  {d}/" for d in unpinned)
    )


def test_research_scripts_name_the_sealed_release() -> None:
    sealed = _sealed()
    offending = [
        f"  {rel}: {literal}"
        for rel in _tracked()
        if rel.startswith("research/") and rel.endswith(".py")
        for literal in sorted(set(RELEASE_LITERAL.findall((REPO / rel).read_text(encoding="utf-8"))))
        if literal != sealed
    ]
    assert not offending, f"release strings that differ from {sealed!r}:\n" + "\n".join(offending)


def test_one_python_version_at_the_root() -> None:
    wanted = _text(".python-version")
    mypy = tomllib.loads((REPO / "pyproject.toml").read_text(encoding="utf-8"))["tool"]["mypy"]
    text = (REPO / ".github" / "workflows" / "verify.yml").read_text(encoding="utf-8")
    workflow = WORKFLOW_PYTHON.findall(text)
    setups = text.count("uses: actions/setup-python@")
    assert setups and len(workflow) == setups, (
        f"{setups} setup-python steps but {len(workflow)} python-version values read"
    )
    assert {wanted, mypy["python_version"], *workflow} == {wanted}, (
        f".python-version {wanted!r}, root mypy target {mypy['python_version']!r}, "
        f"workflow {workflow}"
    )
