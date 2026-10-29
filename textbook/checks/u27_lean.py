"""Unit 27 check: kernel-check the book's Lean for Unit 27.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u27_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Quot

universe u v

namespace Textbook.U27
open Derivation

/-- The barrier, re-proved with the two steps named. -/
theorem quot_barrier' {α : Sort u} {β : Sort v} (rel : α → α → Prop)
    (f : Quot rel → β) {a b : α} (h : rel a b) :
    f (Quot.mk rel a) = f (Quot.mk rel b) := by
  have hq : Quot.mk rel a = Quot.mk rel b := Quot.sound h
  exact congrArg f hq

/-- A function on the raw carrier is under no barrier: the identity on
`Nat` tells 0 from 1. -/
theorem raw_function_separates : (fun n : Nat => n) 0 ≠ (fun n : Nat => n) 1 := by
  decide

/-- A function that respects the collapse relation descends to the
quotient; the descended function is what the barrier is about. -/
def descend (g : Nat → Bool) (hg : ∀ a b, collapseRel R2L a b → g a = g b) :
    Quot (collapseRel R2L) → Bool :=
  Quot.lift g hg

theorem descend_agrees (g : Nat → Bool)
    (hg : ∀ a b, collapseRel R2L a b → g a = g b) :
    descend g hg (Quot.mk _ 0) = descend g hg (Quot.mk _ 1) :=
  barrier_R2L (descend g hg)

/-- The descended function returns `g 0` on both classes. -/
theorem descend_value (g : Nat → Bool)
    (hg : ∀ a b, collapseRel R2L a b → g a = g b) :
    descend g hg (Quot.mk _ 1) = g 0 :=
  (descend_agrees g hg).symm

/-- The same instance for reading F, where all three pairs are collapsed. -/
theorem barrier_R2F {β : Sort v} (f : Quot (collapseRel R2F) → β) (d d' : Nat) :
    f (Quot.mk _ d) = f (Quot.mk _ d') :=
  quot_barrier (collapseRel R2F) f (R2F_collapsed d d')

/-- Collapse compares answers by iff, giving reflexivity and transitivity. -/
theorem collapse_refl (r : Regime) (d : Nat) : collapseRel r d d :=
  fun _ _ => Iff.rfl

theorem collapse_trans (r : Regime) {a b c : Nat}
    (hab : collapseRel r a b) (hbc : collapseRel r b c) : collapseRel r a c :=
  fun ctx hc => (hab ctx hc).trans (hbc ctx hc)

def collapseSetoid (r : Regime) : Setoid Nat where
  r := collapseRel r
  iseqv := ⟨collapse_refl r, fun h ctx hc => (h ctx hc).symm,
            fun hab hbc => collapse_trans r hab hbc⟩

/-- A raw generating relation need not itself contain every pair whose
quotient values become equal. -/
def rawLink (a b : Nat) : Prop := (a = 0 ∧ b = 1) ∨ (a = 1 ∧ b = 2)

theorem raw_chain_quotient :
    ¬ rawLink 0 2 ∧ Quot.mk rawLink 0 = Quot.mk rawLink 2 := by
  constructor
  · intro h
    cases h with
    | inl h => cases h.2
    | inr h => cases h.1
  · exact (@Quot.sound Nat rawLink 0 1 (Or.inl ⟨rfl, rfl⟩)).trans
          (@Quot.sound Nat rawLink 1 2 (Or.inr ⟨rfl, rfl⟩))

end Textbook.U27

#print axioms Textbook.U27.quot_barrier'
#print axioms Textbook.U27.raw_function_separates
#print axioms Textbook.U27.descend_agrees
#print axioms Textbook.U27.descend_value
#print axioms Textbook.U27.barrier_R2F
#print axioms Textbook.U27.collapse_refl
#print axioms Textbook.U27.collapse_trans
#print axioms Textbook.U27.collapseSetoid
#print axioms Textbook.U27.raw_chain_quotient
#print axioms Derivation.quotient_barrier
#print axioms Derivation.quot_barrier
#print axioms Derivation.barrier_R2L
"""

EXPECTED = {
    "Textbook.U27.quot_barrier'": QUOT,
    "Textbook.U27.raw_function_separates": NONE,
    "Textbook.U27.descend_agrees": BOTH,
    "Textbook.U27.descend_value": BOTH,
    "Textbook.U27.barrier_R2F": BOTH,
    "Textbook.U27.collapse_refl": PROPEXT,
    "Textbook.U27.collapse_trans": PROPEXT,
    "Textbook.U27.collapseSetoid": PROPEXT,
    "Textbook.U27.raw_chain_quotient": BOTH,
    "Derivation.quotient_barrier": QUOT,
    "Derivation.quot_barrier": QUOT,
    "Derivation.barrier_R2L": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U27"))
