"""Build the public zip. AuthorityEffect: None."""

from __future__ import annotations

import hashlib
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "000_no_self_authorization_public.zip"

# A constant, so the archive's bytes depend on content and nothing else.
# 1980-01-01 is the zip epoch: the earliest value the format can store.
FIXED_MTIME = (1980, 1, 1, 0, 0, 0)
# 0o644 in the high half, as zip stores unix permissions.
FIXED_MODE = 0o644 << 16

INCLUDE = (
    "000_no_self_authorization.md",
    "000_no_self_authorization_change_log.md",
    "000_no_self_authorization_claim_ledger.md",
    "linkedin_essay.md",
    "attack_list.md",
    "situating.md",
    "README.md",
    "LICENSE",
    "pyproject.toml",
    "src",
    "tests",
    "docs",
    "jupyter_notebooks",
    "public_export",
)


def _iter_files() -> list[Path]:
    files: list[Path] = []
    for name in INCLUDE:
        p = ROOT / name
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            files.extend(
                q
                for q in p.rglob("*")
                if q.is_file()
                and "__pycache__" not in q.parts
                and q.suffix != ".pyc"
                and ".ipynb_checkpoints" not in q.parts
            )
    return sorted(files)


def main() -> None:
    files = _iter_files()
    if OUT.exists():
        OUT.unlink()

    # Written with an explicit ZipInfo per entry, not zf.write(), because
    # zf.write() copies the file's mtime and st_mode into the archive.
    # The committed zip built that way carried ten distinct wall-clock
    # timestamps, so rebuilding it on any other checkout produced a
    # different digest and SHA256SUMS could not be verified by anyone but
    # its author -- which is the whole purpose of shipping the sums.
    # Same reason and same fix as the repository's *.json.gz exports,
    # which CLAUDE.md pins to a fixed mtime and compression level.
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for f in files:
            info = zipfile.ZipInfo(
                filename=f.relative_to(ROOT).as_posix(),
                date_time=FIXED_MTIME,
            )
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = FIXED_MODE
            zf.writestr(info, f.read_bytes())

    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    sums = ROOT / "SHA256SUMS"
    lines = [f"{digest}  {OUT.name}\n"]
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        h = hashlib.sha256(f.read_bytes()).hexdigest()
        lines.append(f"{h}  {rel}\n")
    # LF explicitly: a CRLF rewrite would change every digest line's bytes
    # while changing no digest, which reads as corruption.
    sums.write_bytes("".join(lines).encode("utf-8"))
    print(f"wrote {OUT} sha256={digest} files={len(files)}")


def verify() -> int:
    """Check SHA256SUMS against the tree. Returns an exit status.

    The build alone cannot detect a post-build mutation -- the committed
    zip shipped notebooks that had been edited after it was built, and
    nothing failed. This is the check that catches that, and it reads the
    same _iter_files() population the build writes, so the two cannot
    disagree about what the public face contains.
    """
    sums = ROOT / "SHA256SUMS"
    if not sums.is_file():
        print("FAIL: SHA256SUMS is missing")
        return 1
    recorded: dict[str, str] = {}
    for line in sums.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        h, rel = line.split("  ", 1)
        recorded[rel] = h

    failures: list[str] = []
    if OUT.is_file():
        actual = hashlib.sha256(OUT.read_bytes()).hexdigest()
        if recorded.get(OUT.name) != actual:
            failures.append(f"{OUT.name}: zip digest does not match SHA256SUMS")
    else:
        failures.append(f"{OUT.name}: missing")

    listed = {r for r in recorded if r != OUT.name}
    present = {f.relative_to(ROOT).as_posix() for f in _iter_files()}
    for rel in sorted(listed - present):
        failures.append(f"{rel}: in SHA256SUMS, absent from the tree")
    for rel in sorted(present - listed):
        failures.append(f"{rel}: in the tree, absent from SHA256SUMS")
    for rel in sorted(listed & present):
        actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        if recorded[rel] != actual:
            failures.append(f"{rel}: content changed since the build")

    for failure in failures:
        print(f"FAIL: {failure}")
    if failures:
        print(
            f"\n{len(failures)} failure(s). Rebuild with "
            "`python scripts/build_zip.py` AFTER the last content change, "
            "never before."
        )
        return 1
    print(f"public object verified: zip + {len(present)} files match SHA256SUMS")
    return 0


if __name__ == "__main__":
    if "--verify" in sys.argv[1:]:
        raise SystemExit(verify())
    main()
