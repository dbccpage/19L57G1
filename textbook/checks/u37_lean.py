"""Unit 37 check: kernel-check the book's Lean for Unit 37.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u37_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.ObserverInventory

namespace Textbook.U37
open PrimDiff ObserverInventory

/-- The four local states are four: each adjacent pair differs at a pair. -/
theorem D2_ne_D2rev : D2 ≠ D2rev := by
  intro h
  have : D2rev false true := h ▸ D2_witness
  exact Bool.noConfusion this.1

theorem D2rev_ne_S2 : D2rev ≠ S2 := by
  intro h
  have : D2rev false true := h ▸ (Or.inl D2_witness : S2 false true)
  exact Bool.noConfusion this.1

theorem empty_ne_S2 : EmptyRel ≠ S2 := by
  intro h
  have : EmptyRel false true := h ▸ (Or.inl D2_witness : S2 false true)
  exact this

/-- `D2rev` is irreflexive, so the census applies to it and lands on
its own disjunct. -/
theorem D2rev_irrefl : Irrefl D2rev := by
  intro x ⟨h1, h2⟩
  rw [h1] at h2
  exact Bool.noConfusion h2

theorem census_at_D2rev :
    D2rev = EmptyRel ∨ D2rev = D2 ∨ D2rev = D2rev ∨ D2rev = S2 :=
  bool_irrefl_full_classification D2rev D2rev_irrefl

/-- A relation with a self-loop is outside the census: not irreflexive. -/
theorem loop_not_irrefl : ¬ Irrefl (fun x y : Bool => x = false ∧ y = false) :=
  fun hi => hi false ⟨rfl, rfl⟩

/-- Both reversal maps are involutions. -/
theorem pushNot_involutive (r : Bool → Bool → Prop) : pushNot (pushNot r) = r := by
  funext x y
  simp [pushNot]

/-- Transpose fixes the symmetric state. -/
theorem transpose_S2 : Transpose S2 = S2 := by
  funext x y
  apply propext
  show (D2 y x ∨ D2 x y) ↔ (D2 x y ∨ D2 y x)
  exact Or.comm

/-- The residuals on the other two states. -/
theorem residuals_rest :
    edgeCount EmptyRel = 0 ∧ isSymBit EmptyRel = 0 ∧
    edgeCount D2rev = 1 ∧ isSymBit D2rev = 0 := by
  decide

/-- The witness data, read at the oriented pair. -/
theorem witness_presence : (0 < oneW false true) ∧ ¬ (0 < zeroW false true) := by
  decide

/-- Irreflexivity does not single out a local state: two of them satisfy it. -/
theorem irrefl_underdetermined : Irrefl EmptyRel ∧ Irrefl D2 ∧ EmptyRel ≠ D2 :=
  ⟨empty_irrefl, D2_irrefl, empty_ne_D2⟩

/-- The maps slot, re-decided: the swap is an automorphism of `S2` only. -/
theorem swap_auto_S2_only :
    (∀ x y, S2 x y ↔ S2 (!x) (!y)) ∧ ¬ (∀ x y, D2 x y ↔ D2 (!x) (!y)) := by
  decide

end Textbook.U37

#print axioms Textbook.U37.D2_ne_D2rev
#print axioms Textbook.U37.D2rev_ne_S2
#print axioms Textbook.U37.empty_ne_S2
#print axioms Textbook.U37.D2rev_irrefl
#print axioms Textbook.U37.census_at_D2rev
#print axioms Textbook.U37.loop_not_irrefl
#print axioms Textbook.U37.pushNot_involutive
#print axioms Textbook.U37.transpose_S2
#print axioms Textbook.U37.residuals_rest
#print axioms Textbook.U37.witness_presence
#print axioms Textbook.U37.irrefl_underdetermined
#print axioms Textbook.U37.swap_auto_S2_only
#print axioms ObserverInventory.bool_irrefl_full_classification
#print axioms ObserverInventory.witnesses_are_data
#print axioms ObserverInventory.transpose_ne_pushNot
#print axioms ObserverInventory.residuals_not_unique
"""

EXPECTED = {
    "Textbook.U37.D2_ne_D2rev": NONE,
    "Textbook.U37.D2rev_ne_S2": NONE,
    "Textbook.U37.empty_ne_S2": NONE,
    "Textbook.U37.D2rev_irrefl": NONE,
    "Textbook.U37.census_at_D2rev": BOTH,
    "Textbook.U37.loop_not_irrefl": NONE,
    "Textbook.U37.pushNot_involutive": BOTH,
    "Textbook.U37.transpose_S2": BOTH,
    "Textbook.U37.residuals_rest": NONE,
    "Textbook.U37.witness_presence": PROPEXT,
    "Textbook.U37.irrefl_underdetermined": NONE,
    "Textbook.U37.swap_auto_S2_only": NONE,
    "ObserverInventory.bool_irrefl_full_classification": BOTH,
    "ObserverInventory.witnesses_are_data": PROPEXT,
    "ObserverInventory.transpose_ne_pushNot": NONE,
    "ObserverInventory.residuals_not_unique": NONE,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U37"))
