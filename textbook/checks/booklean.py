"""Shared runner for the book's Lean (see textbook/README.md, "Lean (book)").

A unit's Lean check script holds its Lean source as a string and the axiom
report it expects, and calls ``main`` below. The source is written to a
temporary file and checked against Genesis's compiled ``Derivation``
library with Lean's kernel. Nothing here is part of Genesis's build, its
gates or ``artifacts/lean_axioms.txt``. AuthorityEffect: None.

Usage inside a check script (run from the repository root, after
``lake build`` in lean4/):

    from booklean import main
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U04"))

Command-line options the unit scripts inherit:

    --lean PATH --lean-path DIR    use a Lean binary and a directory of
                                   compiled .olean files instead of lake

Exit 0: checked, axioms as expected. Exit 1: Lean rejected the file or an
axiom report differs. Exit 2: no Lean found; nothing was checked.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROPEXT = "depends on axioms: [propext]"
QUOT = "depends on axioms: [Quot.sound]"
BOTH = "depends on axioms: [propext, Quot.sound]"
NONE = "does not depend on any axioms"


def run(args: argparse.Namespace, src: Path) -> subprocess.CompletedProcess[str] | None:
    root = Path(__file__).resolve().parents[2]
    if args.lean:
        env = dict(os.environ, LEAN_PATH=args.lean_path or "")
        cmd = [args.lean, str(src)]
        cwd = root
    else:
        lake = shutil.which("lake")
        if lake is None:
            return None
        cmd = [lake, "env", "lean", str(src)]
        env = dict(os.environ)
        cwd = root / "lean4"
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True,
                          text=True, encoding="utf-8")


def main(lean_source: str, expected: dict[str, str], unit: str) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lean", help="path to a lean binary")
    ap.add_argument("--lean-path", help="LEAN_PATH holding Derivation .olean files")
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / f"{unit}.lean"
        src.write_text(lean_source, encoding="utf-8")
        proc = run(args, src)
    if proc is None:
        print("no lake on PATH and no --lean given: nothing checked")
        return 2
    out = proc.stdout + proc.stderr
    print(out.strip())
    if proc.returncode != 0:
        print(f"lean exit code {proc.returncode}")
        return 1

    failures = [name for name, want in expected.items()
                if f"'{name}' {want}" not in out]
    print(f"axiom reports as expected: {len(expected) - len(failures)} of "
          f"{len(expected)}; failures: {failures}")
    return 1 if failures else 0
