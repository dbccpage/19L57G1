"""Unit 71 check: kernel-check the book's Lean for Unit 71.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u71_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.PresentationRelativity
import Derivation.ClosureSymmetry
import Derivation.ResidualClosure

namespace Textbook.U71
open Compression PresentationRelativity ClosureSymmetry ResidualClosure

/-- Audit note: on the empty carrier `[]`, every map factors through every
other, so `¬ FactorsOn [] p q` is unsatisfiable. -/
theorem factorsOn_nil (p q : Nat → Nat) : FactorsOn [] p q :=
  ⟨fun _ => 0, fun _ hx => nomatch hx⟩

/-- Smallest concrete directional residual on `D = [0, 1]`: constant zero
identifies `0` and `1` while `id` separates them. -/
def const0 : Nat → Nat := fun _ => 0

def res01 : DirectionalResidual [0, 1] const0 id where
  left := 0
  right := 1
  left_mem := by simp
  right_mem := by simp
  identified := rfl
  separated := by decide

theorem const0_id_not_identical :
    ¬ PresentationIdentityOn [0, 1] const0 id :=
  directionalResidual_refutes_identity res01

theorem const0_id_not_factors :
    ¬ FactorsOn [0, 1] const0 id :=
  residual_refutes_factorization res01

/-- Concrete evaluation of class counts before and after joint refinement. -/
theorem const0_id_counts :
    classCount [0, 1] [const0] = 1 ∧
    classCount [0, 1] [jointPresentation [0, 1] const0 id] = 2 := by
  constructor <;> decide

theorem const0_id_joint_strict :
    FactorsOn [0, 1] (jointPresentation [0, 1] const0 id) const0 ∧
    FactorsOn [0, 1] (jointPresentation [0, 1] const0 id) id ∧
    classCount [0, 1] [const0] <
      classCount [0, 1] [jointPresentation [0, 1] const0 id] :=
  jointPresentation_strict_of_factorization_failure
    [0, 1] const0 id const0_id_not_factors

/-- The transposition symmetry break built from `res01`. -/
def break01 : InternalSymmetryBreak [0, 1] const0 id :=
  residual_to_internal_symmetry_break res01

theorem break01_swaps :
    break01.symmetry 0 = 1 ∧ break01.symmetry 1 = 0 ∧ break01.symmetry 2 = 2 := by
  refine ⟨?_, ?_, ?_⟩ <;> decide

/-- Audit finding (`ClosureSymmetry.md` §6, §11.2): `InternalSymmetryBreak`
admits involutions that are not single transpositions. On `D = [0, 1, 2, 3]`,
`doubleSwap` swaps `0 ↔ 1` and `2 ↔ 3`, moving four points. -/
def doubleSwap (x : Nat) : Nat :=
  if x = 0 then 1
  else if x = 1 then 0
  else if x = 2 then 3
  else if x = 3 then 2
  else x

theorem doubleSwap_involutive (x : Nat) : doubleSwap (doubleSwap x) = x := by
  unfold doubleSwap
  split <;> rename_i h0
  · subst h0; rfl
  · split <;> rename_i h1
    · subst h1; rfl
    · split <;> rename_i h2
      · subst h2; rfl
      · split <;> rename_i h3
        · subst h3; rfl
        · rfl

def doubleSwapBreak : InternalSymmetryBreak [0, 1, 2, 3] const0 id where
  symmetry := doubleSwap
  involutive := doubleSwap_involutive
  domain_preserved := by
    intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx ⊢
    rcases hx with rfl | rfl | rfl | rfl <;> decide
  p_invariant := fun _ _ => rfl
  point := 0
  point_mem := by simp
  q_not_invariant := by decide

theorem doubleSwap_moves_four :
    doubleSwap 0 ≠ 0 ∧ doubleSwap 1 ≠ 1 ∧
    doubleSwap 2 ≠ 2 ∧ doubleSwap 3 ≠ 3 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> decide

/-- Closing the current obstruction `r → q` on `D = [0, 1]` via `r = id`. -/
theorem const0_id_closed :
    ¬ InvariantUnderOn [0, 1] id break01.symmetry ∧
    id (break01.symmetry break01.point) ≠ id break01.point ∧
    classCount [0, 1] [const0] < classCount [0, 1] [id] ∧
    ¬ Nonempty (DirectionalResidual [0, 1] id id) ∧
    ¬ Nonempty (InternalSymmetryBreak [0, 1] id id) :=
  common_refinement_closes_current_obstruction break01
    ⟨const0, fun _ _ => rfl⟩ ⟨id, fun _ _ => rfl⟩

/-- Audit note (`ResidualClosure.md` §6): closing the current obstruction
`r → q` says nothing about a later comparison `q'`. Here `r = q = div2`
closes `r → q`, while `r → id` still has a directional residual at `(0, 1)`. -/
def div2 : Nat → Nat := fun x => x / 2

def res_div2_id : DirectionalResidual [0, 1, 2] div2 id where
  left := 0
  right := 1
  left_mem := by simp
  right_mem := by simp
  identified := rfl
  separated := by decide

theorem closed_current_not_future :
    ¬ Nonempty (DirectionalResidual [0, 1, 2] div2 div2) ∧
    Nonempty (DirectionalResidual [0, 1, 2] div2 id) :=
  ⟨current_directional_residual_is_empty ⟨id, fun _ _ => rfl⟩, ⟨res_div2_id⟩⟩

def bookP (x : Nat) : Nat := if x = 2 then 1 else 0
def bookQ (x : Nat) : Nat := if x = 0 then 0 else 1

theorem three_item_refinement_counts :
    classCount [0,1,2] [bookP] = 2 ∧
    classCount [0,1,2] [bookP,bookP] = 2 ∧
    classCount [0,1,2] [bookP,bookQ] = 3 := by decide

end Textbook.U71

#print axioms Textbook.U71.three_item_refinement_counts

#print axioms Textbook.U71.factorsOn_nil
#print axioms Textbook.U71.const0_id_not_identical
#print axioms Textbook.U71.const0_id_not_factors
#print axioms Textbook.U71.const0_id_counts
#print axioms Textbook.U71.const0_id_joint_strict
#print axioms Textbook.U71.break01_swaps
#print axioms Textbook.U71.doubleSwap_involutive
#print axioms Textbook.U71.doubleSwap_moves_four
#print axioms Textbook.U71.const0_id_closed
#print axioms Textbook.U71.closed_current_not_future
#print axioms PresentationRelativity.presentationIdentity_iff_fiberIdentity
#print axioms PresentationRelativity.directionalResidual_refutes_identity
#print axioms PresentationRelativity.presentationIdentity_iff_residualEmpty
#print axioms PresentationRelativity.presentationIdentity_equivalence
#print axioms PresentationRelativity.identityRelativeToQuestions_iff
#print axioms PresentationRelativity.splitsAt_iff_directionalResidualAt
#print axioms PresentationRelativity.classCount_lt_of_refinement_split
#print axioms PresentationRelativity.forced_split_of_factorization_failure
#print axioms PresentationRelativity.jointPresentation_strict_of_factorization_failure
#print axioms PresentationRelativity.Metatheory.attempted_absolute_identification_collapses_to_equality
#print axioms PresentationRelativity.Metatheory.attempted_absolute_polarities_are_refuted
#print axioms PresentationRelativity.notes_update_kernel_results_agree
#print axioms PresentationRelativity.panel_extension_refines_equivalence
#print axioms PresentationRelativity.certNeg_extension_implies_source
#print axioms PresentationRelativity.panel_extension_changes_verdict_not_world
#print axioms PresentationRelativity.declared_generator_index_comparison_does_not_factor
#print axioms PresentationRelativity.declared_generator_index_comparison_forces_refinement
#print axioms ClosureSymmetry.transpose_involutive
#print axioms ClosureSymmetry.residual_nonempty_iff_internal_symmetry_break_nonempty
#print axioms ClosureSymmetry.closure_failure_iff_internal_symmetry_break
#print axioms ResidualClosure.carrying_right_face_loses_generating_invariance
#print axioms ResidualClosure.common_refinement_strictly_splits_left_face
#print axioms ResidualClosure.common_refinement_closes_current_obstruction
"""

EXPECTED = {
    "Textbook.U71.three_item_refinement_counts": NONE,

    "Textbook.U71.factorsOn_nil": NONE,
    "Textbook.U71.const0_id_not_identical": BOTH,
    "Textbook.U71.const0_id_not_factors": BOTH,
    "Textbook.U71.const0_id_counts": NONE,
    "Textbook.U71.const0_id_joint_strict": BOTH,
    "Textbook.U71.break01_swaps": PROPEXT,
    "Textbook.U71.doubleSwap_involutive": NONE,
    "Textbook.U71.doubleSwap_moves_four": NONE,
    "Textbook.U71.const0_id_closed": BOTH,
    "Textbook.U71.closed_current_not_future": BOTH,
    "PresentationRelativity.presentationIdentity_iff_fiberIdentity": QUOT,
    "PresentationRelativity.directionalResidual_refutes_identity": QUOT,
    "PresentationRelativity.presentationIdentity_iff_residualEmpty": QUOT,
    "PresentationRelativity.presentationIdentity_equivalence": QUOT,
    "PresentationRelativity.identityRelativeToQuestions_iff": QUOT,
    "PresentationRelativity.splitsAt_iff_directionalResidualAt": QUOT,
    "PresentationRelativity.classCount_lt_of_refinement_split": BOTH,
    "PresentationRelativity.forced_split_of_factorization_failure": BOTH,
    "PresentationRelativity.jointPresentation_strict_of_factorization_failure": BOTH,
    "PresentationRelativity.Metatheory.attempted_absolute_identification_collapses_to_equality": NONE,
    "PresentationRelativity.Metatheory.attempted_absolute_polarities_are_refuted": NONE,
    "PresentationRelativity.notes_update_kernel_results_agree": BOTH,
    "PresentationRelativity.panel_extension_refines_equivalence": BOTH,
    "PresentationRelativity.certNeg_extension_implies_source": BOTH,
    "PresentationRelativity.panel_extension_changes_verdict_not_world": BOTH,
    "PresentationRelativity.declared_generator_index_comparison_does_not_factor": BOTH,
    "PresentationRelativity.declared_generator_index_comparison_forces_refinement": BOTH,
    "ClosureSymmetry.transpose_involutive": PROPEXT,
    "ClosureSymmetry.residual_nonempty_iff_internal_symmetry_break_nonempty": PROPEXT,
    "ClosureSymmetry.closure_failure_iff_internal_symmetry_break": BOTH,
    "ResidualClosure.carrying_right_face_loses_generating_invariance": QUOT,
    "ResidualClosure.common_refinement_strictly_splits_left_face": BOTH,
    "ResidualClosure.common_refinement_closes_current_obstruction": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U71"))
