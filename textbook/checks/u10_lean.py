"""Unit 10 check: kernel-check the book's Lean for Unit 10.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u10_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Inertia
import Derivation.Minimality

namespace Textbook.U10
open Derivation

/-- The theorem, re-proved with every step named. -/
theorem collapsed_of_no_insts' (r : Regime) (hi : r.insts = [])
    (d d' : Nat) : collapsed r d d' := by
  intro c _
  constructor
  · intro h
    cases h with
    | inl hmem => rw [hi] at hmem; cases hmem
    | inr hrule => exact Or.inr hrule
  · intro h
    cases h with
    | inl hmem => rw [hi] at hmem; cases hmem
    | inr hrule => exact Or.inr hrule

/-- A uniform rule floods every datum alike: with the rule and no
instances, both pluggings are derivable, and the pair stays collapsed. -/
def ruled : Regime := ⟨2, [1], [], [0], [(0, 1)]⟩

theorem ruled_both_derivable :
    derivable ruled (plug ⟨0, [none]⟩ 0) ∧ derivable ruled (plug ⟨0, [none]⟩ 1) := by
  decide

theorem ruled_collapsed : collapsed ruled 0 1 :=
  collapsed_of_no_insts ruled rfl 0 1

/-- Forms alone do not separate either. -/
theorem forms_only_collapsed : collapsed ⟨3, [1, 2, 5], [], [], []⟩ 1 2 :=
  collapsed_of_no_insts _ rfl 1 2

/-- The hypothesis is needed: one instance separates. -/
theorem one_inst_separates : separable U1 0 1 := U1_separable

/-- So `U1` is a regime whose instance list is not empty, as it must be. -/
theorem U1_has_inst : U1.insts ≠ [] := by decide

end Textbook.U10

#print axioms Textbook.U10.collapsed_of_no_insts'
#print axioms Textbook.U10.ruled_both_derivable
#print axioms Textbook.U10.ruled_collapsed
#print axioms Textbook.U10.forms_only_collapsed
#print axioms Textbook.U10.one_inst_separates
#print axioms Textbook.U10.U1_has_inst
#print axioms Derivation.collapsed_of_no_insts
#print axioms Derivation.R2L_collapsed
#print axioms Derivation.R2F_collapsed
"""

EXPECTED = {n: PROPEXT for n in (
    "Textbook.U10.collapsed_of_no_insts'", "Textbook.U10.ruled_both_derivable",
    "Textbook.U10.ruled_collapsed", "Textbook.U10.forms_only_collapsed",
    "Textbook.U10.one_inst_separates", "Textbook.U10.U1_has_inst",
    "Derivation.collapsed_of_no_insts", "Derivation.R2L_collapsed",
    "Derivation.R2F_collapsed")}
EXPECTED["Textbook.U10.ruled_both_derivable"] = BOTH
EXPECTED["Textbook.U10.one_inst_separates"] = BOTH
EXPECTED["Textbook.U10.U1_has_inst"] = NONE

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U10"))
