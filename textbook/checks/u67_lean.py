"""Unit 67 check: kernel-check the book's Lean for Unit 67 (`ObsDescent`).

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u67_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.ObsDescent

namespace Textbook.U67
open DiffInterface ObsDescent

/-- Every element of `Bool` maps to the same equivalence class under
`collapseAllObs`. -/
theorem collapseAll_one_class :
    ObsQuotient.mk collapseAllObs true = ObsQuotient.mk collapseAllObs false :=
  obsQuotient_eq_of_zero collapseAllObs trivial

/-- Concrete instance of `view_descends_pair_blocked` on `collapseAllObs`:
the constant view `fun _ => true` descends, while the pair `(true, z)` with the
identity does not. -/
theorem collapseAll_flagship :
    (∃ F : ObsQuotient collapseAllObs → Bool,
        ∀ z, F (ObsQuotient.mk collapseAllObs z) = true) ∧
      ¬ ∃ F : ObsQuotient collapseAllObs → Bool × Bool,
          ∀ z, F (ObsQuotient.mk collapseAllObs z) = (true, z) :=
  view_descends_pair_blocked collapseAllObs (fun _ => true) (fun z => z)
    (fun _ _ _ => rfl) (x := true) (y := false) trivial Bool.noConfusion

/-- Every kernel observer `kernelObs view` has a class-constant difference map
`DeltaConstant`. -/
theorem kernelObs_deltaConstant {X V : Type} (view : X → V) :
    DeltaConstant (kernelObs view) := by
  intro x x' y y' hx hy
  have hx' : view x = view x' := hx
  have hy' : view y = view y' := hy
  show (view x, view y) = (view x', view y')
  rw [hx', hy']

/-- The integer subtraction observer `intDiffObs` has a class-constant
difference map `DeltaConstant`. -/
theorem intDiffObs_deltaConstant : DeltaConstant intDiffObs := by
  intro x x' y y' hx hy
  have hx' : x - x' = 0 := hx
  have hy' : y - y' = 0 := hy
  show x - y = x' - y'
  omega

/-- On a subsingleton carrier, every map `f : X → Y` is class-constant for
every observer `O`. -/
theorem subsingleton_carrier_classConstant {X R Y : Type} [Subsingleton X]
    (O : DiffObs X R) (f : X → Y) : ClassConstant O f :=
  fun x y _ => congrArg f (Subsingleton.elim x y)

end Textbook.U67

#print axioms Textbook.U67.collapseAll_one_class
#print axioms Textbook.U67.collapseAll_flagship
#print axioms Textbook.U67.kernelObs_deltaConstant
#print axioms Textbook.U67.intDiffObs_deltaConstant
#print axioms Textbook.U67.subsingleton_carrier_classConstant
#print axioms ObsDescent.obsQuotient_exact
#print axioms ObsDescent.obsQuotient_mk_eq_iff
#print axioms ObsDescent.obsQuotient_mk_surjective
#print axioms ObsDescent.descend_mk
#print axioms ObsDescent.descend_exists_iff
#print axioms ObsDescent.descend_unique
#print axioms ObsDescent.descend_blocked_of_witness
#print axioms ObsDescent.deltaDescend_exists_iff
#print axioms ObsDescent.deltaDescend_unique
#print axioms ObsDescent.classConstant_pair_iff
#print axioms ObsDescent.view_descends_pair_blocked
#print axioms ObsDescent.classConstant_comp_mk_iff
#print axioms ObsDescent.descendMod_exists_iff
#print axioms ObsDescent.value_orientation_survives
#print axioms ObsDescent.collapseAllObs_not_deltaConstant
#print axioms ObsDescent.classConstant_iff_fiberConstant_all
#print axioms ObsDescent.descend_iff_factorsOn_all
#print axioms ObsDescent.fiberConstant_fixed_D_not_classConstant
#print axioms ObsDescent.sigEq_append_iff
"""

EXPECTED = {
    "Textbook.U67.collapseAll_one_class": QUOT,
    "Textbook.U67.collapseAll_flagship": QUOT,
    "Textbook.U67.kernelObs_deltaConstant": NONE,
    "Textbook.U67.intDiffObs_deltaConstant": BOTH,
    "Textbook.U67.subsingleton_carrier_classConstant": NONE,
    "ObsDescent.obsQuotient_exact": PROPEXT,
    "ObsDescent.obsQuotient_mk_eq_iff": BOTH,
    "ObsDescent.obsQuotient_mk_surjective": NONE,
    "ObsDescent.descend_mk": NONE,
    "ObsDescent.descend_exists_iff": QUOT,
    "ObsDescent.descend_unique": QUOT,
    "ObsDescent.descend_blocked_of_witness": QUOT,
    "ObsDescent.deltaDescend_exists_iff": QUOT,
    "ObsDescent.deltaDescend_unique": QUOT,
    "ObsDescent.classConstant_pair_iff": NONE,
    "ObsDescent.view_descends_pair_blocked": QUOT,
    "ObsDescent.classConstant_comp_mk_iff": BOTH,
    "ObsDescent.descendMod_exists_iff": BOTH,
    "ObsDescent.value_orientation_survives": BOTH,
    "ObsDescent.collapseAllObs_not_deltaConstant": NONE,
    "ObsDescent.classConstant_iff_fiberConstant_all": NONE,
    "ObsDescent.descend_iff_factorsOn_all": QUOT,
    "ObsDescent.fiberConstant_fixed_D_not_classConstant": NONE,
    "ObsDescent.sigEq_append_iff": PROPEXT,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U67"))
