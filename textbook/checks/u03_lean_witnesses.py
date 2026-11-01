"""Unit 03 check: kernel-check the book's Lean for Unit 03.

The Lean source below is written for this book. It is not part of Genesis's
build, its axiom report or its gates. This script writes it to a temporary
directory and checks it against Genesis's compiled `Derivation` library,
then reads its `#print axioms` lines. AuthorityEffect: None.

Run from the repository root, after `lake build` in lean4/:

    python textbook/checks/u03_lean_witnesses.py

It runs `lake env lean` inside lean4/. To use a Lean binary and a directory
of compiled .olean files directly instead:

    python textbook/checks/u03_lean_witnesses.py --lean PATH --lean-path DIR

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

namespace Textbook.U03
open Derivation

/-- The token plays no part: any two supplies have the same outcome. -/
theorem supply_token_irrelevant (r : Regime) (t u : Nat) :
    stepE r (.supply t) = stepE r (.supply u) := rfl

/-- Equal resulting ledgers do not identify the supplied event. -/
theorem different_supplies_same_step (r : Regime) :
    (Event.supply 0 ≠ Event.supply 7) ∧
    stepE r (.supply 0) = stepE r (.supply 7) := by
  exact ⟨by decide, rfl⟩

/-- Admission is different: admitting a datum always changes the regime. -/
theorem admitDatum_changes (r : Regime) : stepE r .admitDatum ≠ some r := by
  intro h
  have h2 : r.data + 1 = r.data := congrArg Regime.data (Option.some.inj h)
  exact Nat.succ_ne_self r.data h2

/-- Admission does not wait for a supply: a history with no supply admits. -/
theorem admit_without_supply :
    replayE [.admitDatum] genesis = some ⟨1, [], [], [], []⟩ := rfl

/-- A supply at the head of a history can be dropped. -/
theorem replay_supply_cons (t : Nat) (h : List Event) (r : Regime) :
    replayE (.supply t :: h) r = replayE h r := rfl

/-- A history made only of supplies replays to its base. -/
theorem replay_only_supplies (h : List Event)
    (hs : ∀ e ∈ h, ∃ t, e = .supply t) (r : Regime) :
    replayE h r = some r := by
  induction h with
  | nil => rfl
  | cons e rest ih =>
    obtain ⟨t, rfl⟩ := hs e (List.Mem.head rest)
    rw [replay_supply_cons]
    exact ih (fun e' he' => hs e' (List.Mem.tail _ he'))

/-- Genesis's reading-L history with its four supplies removed reaches the
same regime. -/
theorem historyL_without_supplies :
    replayE [.admitDatum, .admitDatum, .impose 0 1] genesis = some R2L := by
  decide

/-- Reading F likewise, with its four supplies removed. -/
theorem historyF_without_supplies :
    replayE [.admitDatum, .admitDatum, .admitDatum, .impose 1 2] genesis
      = some R2F := by
  decide

/-- A probe, not a model: only the first two cases of `stepE`, every other
event rejected. Used only to locate where `propext` enters. -/
def stepProbe (r : Regime) : Event → Option Regime
  | .supply _ => some r
  | .admitDatum => some { r with data := r.data + 1 }
  | .admitForm _ => none
  | .admitInst _ _ => none
  | .admitRuleAll _ => none
  | .impose _ _ => none

theorem probe_supply_no_op (r : Regime) (t : Nat) :
    stepProbe r (.supply t) = some r := rfl

end Textbook.U03

#print axioms Textbook.U03.supply_token_irrelevant
#print axioms Textbook.U03.different_supplies_same_step
#print axioms Textbook.U03.admitDatum_changes
#print axioms Textbook.U03.admit_without_supply
#print axioms Textbook.U03.replay_supply_cons
#print axioms Textbook.U03.replay_only_supplies
#print axioms Textbook.U03.historyL_without_supplies
#print axioms Textbook.U03.historyF_without_supplies
#print axioms Textbook.U03.stepProbe
#print axioms Textbook.U03.probe_supply_no_op
#print axioms Derivation.stepE
#print axioms Derivation.insertNew
#print axioms List.getD
"""

P = "depends on axioms: [propext]"
NONE = "does not depend on any axioms"
EXPECTED = {
    "Textbook.U03.supply_token_irrelevant": P,
    "Textbook.U03.different_supplies_same_step": P,
    "Textbook.U03.admitDatum_changes": P,
    "Textbook.U03.admit_without_supply": P,
    "Textbook.U03.replay_supply_cons": P,
    "Textbook.U03.replay_only_supplies": P,
    "Textbook.U03.historyL_without_supplies": P,
    "Textbook.U03.historyF_without_supplies": P,
    "Textbook.U03.stepProbe": NONE,
    "Textbook.U03.probe_supply_no_op": NONE,
    "Derivation.stepE": P,
    "Derivation.insertNew": P,
    "List.getD": P,
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
        src = Path(tmp) / "U03.lean"
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
        line = f"'{name}' {want}"
        if line not in out:
            failures.append(name)
    print(f"axiom reports as expected: {len(EXPECTED) - len(failures)} of "
          f"{len(EXPECTED)}; failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
