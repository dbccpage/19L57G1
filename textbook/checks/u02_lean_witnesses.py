"""Unit 02 check: kernel-check the book's Lean for Unit 02.

The Lean source below is written for this book. It is not part of Genesis's
build, its axiom report or its gates. This script writes it to a temporary
directory and checks it against Genesis's compiled `Derivation` library,
then reads its `#print axioms` lines. AuthorityEffect: None.

Run from the repository root, after `lake build` in lean4/:

    python textbook/checks/u02_lean_witnesses.py

It runs `lake env lean` inside lean4/. To use a Lean binary and a directory
of compiled .olean files directly instead:

    python textbook/checks/u02_lean_witnesses.py --lean PATH --lean-path DIR

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

LEAN_SOURCE = """\
import Derivation.Inertia

namespace Textbook.U02
open Derivation

/-- Unit 01's theorem is the case `r = genesis` of Unit 02's. -/
theorem genesis_case (i : Inst) : ¬ derivable genesis i :=
  underivable_of_empty genesis rfl rfl i

/-- The Challenge 3 regime of reading L: two data, one imposed demand,
no forms, no instances, no rules. Nothing is derivable in it. -/
theorem r2l_case (i : Inst) : ¬ derivable R2L i :=
  underivable_of_empty R2L rfl rfl i

/-- Drop the no-rules hypothesis: one unary form with the rule on it. -/
def R : Regime := ⟨0, [1], [], [0], []⟩

/-- Drop the no-instances hypothesis: one datum, one unary form, one
admitted instance. -/
def R' : Regime := ⟨1, [1], [(0, [0])], [], []⟩

theorem R_wf : R.wf := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [R]

theorem R'_wf : R'.wf := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [R']

theorem R_replays :
    replayE [.admitForm 1, .admitRuleAll 0] genesis = some R := by
  decide

theorem R'_replays :
    replayE [.admitDatum, .admitForm 1, .admitInst 0 [0]] genesis = some R' := by
  decide

theorem R_insts : R.insts = [] := rfl

theorem R_derives : derivable R (0, [99]) :=
  Or.inr (List.Mem.head [])

theorem R'_rules : R'.rules = [] := rfl

theorem R'_derives : derivable R' (0, [0]) :=
  Or.inl (List.Mem.head [])

theorem R'_not_derives : ¬ derivable R' (0, [1]) := by
  intro h
  cases h with
  | inl h =>
    cases h with
    | tail _ h => cases h
  | inr h => cases h

end Textbook.U02

#print axioms Textbook.U02.genesis_case
#print axioms Textbook.U02.r2l_case
#print axioms Textbook.U02.R_wf
#print axioms Textbook.U02.R'_wf
#print axioms Textbook.U02.R_replays
#print axioms Textbook.U02.R'_replays
#print axioms Textbook.U02.R_insts
#print axioms Textbook.U02.R_derives
#print axioms Textbook.U02.R'_rules
#print axioms Textbook.U02.R'_derives
#print axioms Textbook.U02.R'_not_derives
"""

NONE = "does not depend on any axioms"
EXPECTED = {
    "genesis_case": NONE,
    "r2l_case": NONE,
    "R_wf": "depends on axioms: [propext, Quot.sound]",
    "R'_wf": "depends on axioms: [propext, Quot.sound]",
    "R_replays": "depends on axioms: [propext]",
    "R'_replays": "depends on axioms: [propext]",
    "R_insts": NONE,
    "R_derives": NONE,
    "R'_rules": NONE,
    "R'_derives": NONE,
    "R'_not_derives": NONE,
}


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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lean", help="path to a lean binary")
    ap.add_argument("--lean-path", help="LEAN_PATH holding Derivation .olean files")
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "U02.lean"
        src.write_text(LEAN_SOURCE, encoding="utf-8")
        proc = run(args, src)
    if proc is None:
        print("no lake on PATH and no --lean given: nothing checked")
        return 2
    out = proc.stdout + proc.stderr
    print(out.strip())
    if proc.returncode != 0:
        print(f"lean exit code {proc.returncode}")
        return 1

    failures: list[str] = []
    for name, want in EXPECTED.items():
        line = f"'Textbook.U02.{name}' {want}"
        if line not in out:
            failures.append(name)
    print(f"axiom reports as expected: {len(EXPECTED) - len(failures)} of "
          f"{len(EXPECTED)}; failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
