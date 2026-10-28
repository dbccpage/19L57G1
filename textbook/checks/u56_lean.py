"""Unit 56 check: kernel-check the book's Lean for Unit 56.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u56_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Apartness

namespace Textbook.U56
open Apartness PrimDiff PrimitiveCore

/-- The three-point countermodel fails exactly cotransitivity: the edge
(0,1) is apart, and the third point 2 is apart from neither end. -/
theorem tri_not_cotrans : ¬ Cotrans triSymRel := by
  intro h
  have := h 0 1 (Or.inl ⟨rfl, rfl⟩) 2
  rcases this with h | h <;> simp [triSymRel] at h

theorem tri_not_apart : ¬ IsApart triSymRel := fun h => tri_not_cotrans h.cotrans

/-- A three-point relation that is apart: every two different points. -/
def ne3 : Fin 3 → Fin 3 → Prop := fun x y => x ≠ y

theorem ne3_isApart : IsApart ne3 :=
  { irrefl := fun x h => h rfl,
    symm := fun _ _ h => fun e => h e.symm,
    cotrans := by
      intro x y hxy z
      by_cases hxz : x = z
      · exact Or.inr (fun e => hxy (hxz.trans e))
      · exact Or.inl hxz }

/-- Its indistinguishability is an equivalence, by the theorem, and it is
equality: two points are indistinguishable exactly when they are equal. -/
theorem ne3_indist_equiv :
    (∀ x, Indist ne3 x x) ∧ (∀ x y, Indist ne3 x y → Indist ne3 y x) ∧
    (∀ x y z, Indist ne3 x y → Indist ne3 y z → Indist ne3 x z) :=
  indist_equivalence ne3_isApart

theorem ne3_indist_iff (x y : Fin 3) : Indist ne3 x y ↔ x = y := by
  unfold Indist ne3
  constructor
  · intro h; exact Decidable.of_not_not h
  · intro h hne; exact hne h

/-- The two-point apartness and the oriented relation, pair by pair. -/
theorem s2_table :
    S2 false true ∧ S2 true false ∧ ¬ S2 false false ∧ ¬ S2 true true := by
  refine ⟨Or.inl ⟨rfl, rfl⟩, Or.inr ⟨rfl, rfl⟩, ?_, ?_⟩ <;> decide

theorem d2_table :
    D2 false true ∧ ¬ D2 true false ∧ ¬ D2 false false ∧ ¬ D2 true true := by
  decide

/-- Indistinguishability under S2 is equality on Bool. -/
theorem s2_indist_iff (x y : Bool) : Indist S2 x y ↔ x = y := by
  cases x <;> cases y <;> simp [Indist, S2, Sym, D2]

/-- Under the oriented relation alone, indistinguishability is not
symmetric: the clause the countermodel breaks, as values. -/
theorem d2_indist_values :
    Indist D2 true false ∧ ¬ Indist D2 false true :=
  irrefl_alone_breaks_symm

/-- The four operations on two points, classified. -/
theorem four_operations :
    PreservesOriented id ∧ PreservesApart id ∧
    ¬ PreservesOriented Bool.not ∧ PreservesApart Bool.not ∧
    ¬ PreservesOriented (fun _ => false) ∧ ¬ PreservesApart (fun _ => false) ∧
    ¬ PreservesOriented (fun _ => true) ∧ ¬ PreservesApart (fun _ => true) :=
  ⟨id_preserves_oriented, id_preserves_apart, swap_breaks_oriented, swap_preserves_apart,
   (collapse_preserves_neither false).1, (collapse_preserves_neither false).2,
   (collapse_preserves_neither true).1, (collapse_preserves_neither true).2⟩

/-- Genesis's two characterisations, applied to the swap composed with
itself: it preserves the apartness, so it is the identity or the swap; it
preserves the orientation, so it is the identity. -/
theorem swap_twice_apart : PreservesApart (Bool.not ∘ Bool.not) := Or.inl ⟨rfl, rfl⟩

theorem swap_twice_is_id_or_swap :
    (Bool.not ∘ Bool.not) = id ∨ (Bool.not ∘ Bool.not) = Bool.not :=
  apart_preserver_pair _ swap_twice_apart

theorem swap_twice_is_id : (Bool.not ∘ Bool.not) = id :=
  oriented_preserver_unique _ ⟨rfl, rfl⟩

/-- The family holding only the swap: its closure contains an operation
that does not preserve the orientation, by `clos_oriented_iff` read
right to left. -/
def swapFamily : (Bool → Bool) → Prop := fun f => f = Bool.not

theorem swap_family_not_oriented :
    ¬ (∀ f, Clos swapFamily f → PreservesOriented f) := by
  intro h
  have := (clos_oriented_iff swapFamily).mp h Bool.not rfl
  exact swap_breaks_oriented this

/-- The family holding only the identity: the closure preserves the
orientation, and every member is the identity. -/
def idFamily : (Bool → Bool) → Prop := fun f => f = id

theorem id_family_oriented : ∀ f, Clos idFamily f → PreservesOriented f :=
  (clos_oriented_iff idFamily).mpr (fun f hf => hf ▸ id_preserves_oriented)

theorem id_family_trivial : ∀ f, idFamily f → f = id :=
  oriented_family_trivial idFamily (fun f hf => hf ▸ id_preserves_oriented)

/-- The orientation is data the apartness cannot see: the swap fixes S2
pair by pair and moves the retained witness. -/
theorem swap_fixes_apartness_moves_witness :
    (∀ x y, S2 x y ↔ S2 (Bool.not x) (Bool.not y)) ∧
    D2 false true ∧ ¬ D2 (Bool.not false) (Bool.not true) :=
  ⟨swap_is_S2_automorphism, retained_orientation_not_swap_invariant.1,
   retained_orientation_not_swap_invariant.2⟩

end Textbook.U56

#print axioms Textbook.U56.tri_not_cotrans
#print axioms Textbook.U56.tri_not_apart
#print axioms Textbook.U56.ne3_isApart
#print axioms Textbook.U56.ne3_indist_equiv
#print axioms Textbook.U56.ne3_indist_iff
#print axioms Textbook.U56.s2_table
#print axioms Textbook.U56.d2_table
#print axioms Textbook.U56.s2_indist_iff
#print axioms Textbook.U56.d2_indist_values
#print axioms Textbook.U56.four_operations
#print axioms Textbook.U56.swap_twice_apart
#print axioms Textbook.U56.swap_twice_is_id_or_swap
#print axioms Textbook.U56.swap_twice_is_id
#print axioms Textbook.U56.swap_family_not_oriented
#print axioms Textbook.U56.id_family_oriented
#print axioms Textbook.U56.id_family_trivial
#print axioms Textbook.U56.swap_fixes_apartness_moves_witness
#print axioms Apartness.indist_equivalence
#print axioms Apartness.bare_breaks_refl
#print axioms Apartness.irrefl_alone_breaks_symm
#print axioms Apartness.subsingleton_indist_total
#print axioms Apartness.symm_without_cotrans_breaks_trans
#print axioms Apartness.two_point_indist_trans
#print axioms Apartness.s2_isApart
#print axioms Apartness.orientations_same_apartness
#print axioms Apartness.orientations_differ
#print axioms Apartness.retained_orientation_not_swap_invariant
#print axioms Apartness.oriented_preserver_unique
#print axioms Apartness.apart_preserver_pair
#print axioms Apartness.collapse_preserves_neither
#print axioms Apartness.clos_oriented_iff
#print axioms Apartness.oriented_family_trivial
#print axioms PrimitiveCore.cotrans_auto_on_two
"""

EXPECTED = {
    "Textbook.U56.tri_not_cotrans": PROPEXT,
    "Textbook.U56.tri_not_apart": PROPEXT,
    "Textbook.U56.ne3_isApart": NONE,
    "Textbook.U56.ne3_indist_equiv": NONE,
    "Textbook.U56.ne3_indist_iff": NONE,
    "Textbook.U56.s2_table": NONE,
    "Textbook.U56.d2_table": NONE,
    "Textbook.U56.s2_indist_iff": PROPEXT,
    "Textbook.U56.d2_indist_values": NONE,
    "Textbook.U56.four_operations": NONE,
    "Textbook.U56.swap_twice_apart": NONE,
    "Textbook.U56.swap_twice_is_id_or_swap": QUOT,
    "Textbook.U56.swap_twice_is_id": QUOT,
    "Textbook.U56.swap_family_not_oriented": NONE,
    "Textbook.U56.id_family_oriented": NONE,
    "Textbook.U56.id_family_trivial": QUOT,
    "Textbook.U56.swap_fixes_apartness_moves_witness": NONE,
    "Apartness.indist_equivalence": NONE,
    "Apartness.bare_breaks_refl": NONE,
    "Apartness.irrefl_alone_breaks_symm": NONE,
    "Apartness.subsingleton_indist_total": NONE,
    "Apartness.symm_without_cotrans_breaks_trans": PROPEXT,
    "Apartness.two_point_indist_trans": NONE,
    "Apartness.s2_isApart": NONE,
    "Apartness.orientations_same_apartness": NONE,
    "Apartness.orientations_differ": NONE,
    "Apartness.retained_orientation_not_swap_invariant": NONE,
    "Apartness.oriented_preserver_unique": QUOT,
    "Apartness.apart_preserver_pair": QUOT,
    "Apartness.collapse_preserves_neither": NONE,
    "Apartness.clos_oriented_iff": NONE,
    "Apartness.oriented_family_trivial": QUOT,
    "PrimitiveCore.cotrans_auto_on_two": NONE,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U56"))
