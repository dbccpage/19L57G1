"""Build the public zip. AuthorityEffect: None."""

from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "000_no_self_authorization_public.zip"

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
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, f.relative_to(ROOT).as_posix())
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    sums = ROOT / "SHA256SUMS"
    lines = [f"{digest}  {OUT.name}\n"]
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        h = hashlib.sha256(f.read_bytes()).hexdigest()
        lines.append(f"{h}  {rel}\n")
    sums.write_text("".join(lines), encoding="utf-8")
    print(f"wrote {OUT} sha256={digest} files={len(files)}")


if __name__ == "__main__":
    main()
