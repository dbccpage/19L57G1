"""Unit 57 check: kernel-check the book's Lean for Unit 57.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u57_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.InterpreterBoundary

namespace Textbook.U57
open Represented Constitution InterpreterBoundary

/-- The kernel's code is the last of the 64, so its indexed world has 63 data. -/
theorem kernel_index : allDescs[63]? = some kernelDesc := by decide

/-- The diagonal against the kernel at its indexed world: one more note. -/
theorem diag_notes_at_kernel :
    (diag allDescs interpStep (indexWorld 63) (.note 0)).notes = [0, 999] ∧
    (interpStep kernelDesc (indexWorld 63) (.note 0)).notes = [0] := by
  constructor <;> rfl

/-- On the operational support the two agree there: the difference is in
notes alone (the exact scope of `tower_persists`). -/
theorem diag_supp_agrees_at_kernel :
    supp (diag allDescs interpStep (indexWorld 63) (.note 0)) =
      supp (interpStep kernelDesc (indexWorld 63) (.note 0)) := rfl

/-- So the diagonal is not the kernel's interpreter, as a function. -/
theorem diag_ne_kernel : diag allDescs interpStep ≠ interpStep kernelDesc := by
  intro h
  have h1 := congrArg (fun g => (g (indexWorld 63) (.note 0)).notes) h
  rw [diag_notes_at_kernel.1, diag_notes_at_kernel.2] at h1
  exact absurd h1 (by decide)

/-- Off the index range the diagonal returns its input unchanged. -/
theorem diag_off_range :
    diag allDescs interpStep (indexWorld 64) (.note 0) = indexWorld 64 := rfl

/-- Vacuity made visible: two assignments to the uncoded role, both
covering the coded family, disagreeing at `none`. -/
theorem two_assignments :
    ∃ I₁ I₂ : Option ConstitutionDesc → (World → Event → World),
      (∀ d, I₁ (some d) = interpStep d) ∧ (∀ d, I₂ (some d) = interpStep d) ∧
      I₁ none ≠ I₂ none := by
  obtain ⟨I₁, h₁, c₁⟩ := arbitrary_uncoded_assignment (fun w _ => w)
  obtain ⟨I₂, h₂, c₂⟩ :=
    arbitrary_uncoded_assignment (fun w _ => { w with notes := w.notes ++ [1] })
  refine ⟨I₁, I₂, c₁, c₂, ?_⟩
  intro h
  have := congrArg (fun g => (g genesis (.note 0)).notes) (h₁ ▸ h₂ ▸ h)
  exact absurd this (by decide)

/-- The typed-refusal evaluator, at one event. -/
theorem evalOpt_values :
    evalOpt none genesis (.admitTok 3) = none ∧
    evalOpt (some kernelDesc) genesis (.admitTok 3) = some ⟨[3], [], [], [], 0, true, []⟩ := by
  constructor <;> rfl

/-- The declared relation is one ordered pair and nothing else. -/
theorem boundary_single_pair :
    ∀ x y, boundarySetting.r x y → x = some kernelDesc ∧ y = none :=
  fun _ _ h => h

theorem boundary_not_symmetric : ¬ boundarySetting.r none (some kernelDesc) :=
  fun h => nomatch h.1

/-- The same carrier with the pair declared the other way round also
satisfies F: the orientation was chosen, not derived. -/
def reversedSetting : PrimitiveCore.Setting where
  X := Option ConstitutionDesc
  r := fun x y => x = none ∧ y = some kernelDesc
  a := none
  b := some kernelDesc
  ret := fun x y => x = none ∧ y = some kernelDesc
  prot := fun x y => x = none ∧ y = some kernelDesc
  Ops := fun _ => False

theorem reversed_is_F : PrimitiveCore.F reversedSetting :=
  ⟨⟨⟨rfl, rfl⟩, fun _x h => nomatch h.1.symm.trans h.2⟩, ⟨rfl, rfl⟩, ⟨rfl, rfl⟩⟩

/-- Collapse by a constant is obstructed; `isSome` keeps the endpoints apart,
so the obstruction theorem has no hypothesis to work with there. -/
theorem constant_collapse_obstructed :
    PrimDiff.FidelityObstruction PrimDiff.Irrefl boundarySetting.r
      (fun _ : Option ConstitutionDesc => (0 : Nat)) :=
  i5_collapse_obstructed _ rfl

theorem isSome_keeps_apart :
    (some kernelDesc : Option ConstitutionDesc).isSome ≠ (none : Option ConstitutionDesc).isSome := by
  decide

/-- `family_missed` at the sealed family is the same statement as the
renamed I5 theorem: same proof term. -/
theorem same_statement :
    (∃ f : World → Event → World, ∀ d ∈ allDescs, f ≠ interpStep d) :=
  i5_family_not_extensionally_complete

/-- Matched-index agreement is not global support agreement. -/
theorem diag_support_differs_elsewhere :
    supp (diag allDescs interpStep (indexWorld 64) (.admitTok 100)) ≠
      supp (interpStep kernelDesc (indexWorld 64) (.admitTok 100)) := by decide

/-- Appending data changes any output, regardless of what its evaluator did. -/
theorem data_append_differs (u : World) (n : Nat) :
    { u with data := u.data ++ [n] } ≠ u := by
  intro h
  have hlen := congrArg (fun w : World => w.data.length) h
  simp only [List.length_append, List.length_cons, List.length_nil] at hlen
  omega

end Textbook.U57

#print axioms Textbook.U57.kernel_index
#print axioms Textbook.U57.diag_notes_at_kernel
#print axioms Textbook.U57.diag_supp_agrees_at_kernel
#print axioms Textbook.U57.diag_ne_kernel
#print axioms Textbook.U57.diag_off_range
#print axioms Textbook.U57.two_assignments
#print axioms Textbook.U57.evalOpt_values
#print axioms Textbook.U57.boundary_single_pair
#print axioms Textbook.U57.boundary_not_symmetric
#print axioms Textbook.U57.reversed_is_F
#print axioms Textbook.U57.constant_collapse_obstructed
#print axioms Textbook.U57.isSome_keeps_apart
#print axioms Textbook.U57.same_statement
#print axioms Textbook.U57.diag_support_differs_elsewhere
#print axioms Textbook.U57.data_append_differs
#print axioms InterpreterBoundary.indexWorld_len
#print axioms InterpreterBoundary.diag_hit
#print axioms InterpreterBoundary.tower_persists
#print axioms InterpreterBoundary.i2_universal_in_class
#print axioms InterpreterBoundary.i3_refusal_code_returns_none
#print axioms InterpreterBoundary.i3_coded_member_returns_some
#print axioms InterpreterBoundary.arbitrary_uncoded_assignment
#print axioms InterpreterBoundary.family_missed
#print axioms InterpreterBoundary.i5_carrier_occurrences
#print axioms InterpreterBoundary.i5_boundary_is_A
#print axioms InterpreterBoundary.i5_boundary_is_F
#print axioms InterpreterBoundary.i5_collapse_obstructed
#print axioms InterpreterBoundary.i5_family_not_extensionally_complete
"""

EXPECTED = {
    "Textbook.U57.kernel_index": PROPEXT,
    "Textbook.U57.diag_support_differs_elsewhere": BOTH,
    "Textbook.U57.data_append_differs": BOTH,
    "Textbook.U57.diag_notes_at_kernel": BOTH,
    "Textbook.U57.diag_supp_agrees_at_kernel": BOTH,
    "Textbook.U57.diag_ne_kernel": BOTH,
    "Textbook.U57.diag_off_range": BOTH,
    "Textbook.U57.two_assignments": BOTH,
    "Textbook.U57.evalOpt_values": BOTH,
    "Textbook.U57.boundary_single_pair": NONE,
    "Textbook.U57.boundary_not_symmetric": NONE,
    "Textbook.U57.reversed_is_F": NONE,
    "Textbook.U57.constant_collapse_obstructed": NONE,
    "Textbook.U57.isSome_keeps_apart": NONE,
    "Textbook.U57.same_statement": BOTH,
    "InterpreterBoundary.indexWorld_len": PROPEXT,
    "InterpreterBoundary.diag_hit": PROPEXT,
    "InterpreterBoundary.tower_persists": BOTH,
    "InterpreterBoundary.i2_universal_in_class": BOTH,
    "InterpreterBoundary.i3_refusal_code_returns_none": BOTH,
    "InterpreterBoundary.i3_coded_member_returns_some": BOTH,
    "InterpreterBoundary.arbitrary_uncoded_assignment": BOTH,
    "InterpreterBoundary.family_missed": BOTH,
    "InterpreterBoundary.i5_carrier_occurrences": NONE,
    "InterpreterBoundary.i5_boundary_is_A": NONE,
    "InterpreterBoundary.i5_boundary_is_F": NONE,
    "InterpreterBoundary.i5_collapse_obstructed": NONE,
    "InterpreterBoundary.i5_family_not_extensionally_complete": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U57"))
