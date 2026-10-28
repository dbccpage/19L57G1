"""Unit 32 check: kernel-check the book's Lean for Unit 32.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u32_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.MinimalityF

namespace Textbook.U32
open Derivation

/-- The regime the genesis mark produces. -/
def genesisMark : Regime := ⟨3, [1], [(0, [0])], [], [(1, 2)]⟩

/-- The required pair stays collapsed under the genesis mark (the route of
`genesis_mark_not_separable`, spelled out). -/
theorem genesis_mark_collapsed_12 : collapsed genesisMark 1 2 := by
  have base : collapsed (⟨3, [1], [], [], [(1, 2)]⟩ : Regime) 1 2 :=
    collapsed_of_no_insts _ rfl 1 2
  exact (collapsed_append_unmentioning ⟨3, [1], [], [], [(1, 2)]⟩
    [(0, [0])] 1 2 (by decide) (by decide)).mpr base

/-- The genesis mark does separate something: the marked datum from each
required datum. It is not useless; it is aimed at the wrong pair. -/
theorem genesis_mark_separates_01 : separable genesisMark 0 1 :=
  ⟨⟨0, [none]⟩, by decide, by decide⟩

/-- So the genesis-mark delta is not a valid response in reading F. -/
theorem genesis_mark_delta_invalid :
    ¬ validResponse R2F 1 2 [.newForm 1, .newInst 0 [0]] := by
  rintro ⟨s, hs, hsep, -⟩
  have happ : applyDelta R2F [.newForm 1, .newInst 0 [0]] = some genesisMark := by
    decide
  rw [happ] at hs
  injection hs with hs
  subst hs
  exact genesis_mark_not_separable hsep

/-- The mark on the second required datum is valid (the twin of
`deltaU0F_valid`). -/
theorem deltaU2F_valid : validResponse R2F 1 2 [.newForm 1, .newInst 0 [2]] := by
  refine ⟨U2F, by decide, ?_, ?_⟩
  · exact ⟨⟨0, [none]⟩, by decide, by decide⟩
  · intro q hq
    have : q = (1, 2) := by
      cases hq with
      | head => rfl
      | tail _ h => cases h
    rw [this]
    exact ⟨⟨0, [none]⟩, by decide, by decide⟩

/-- Genesis's theorem applied to it: the result is U0F up to isomorphism. -/
theorem u2f_is_u0f_class :
    ∃ s, applyDelta R2F [.newForm 1, .newInst 0 [2]] = some s ∧ Nonempty (Iso s U0F) :=
  mu2_unique_F _ _ deltaU2F_valid (by decide)

/-- The transposition, on the three data. -/
theorem swap12_values : swap12 0 = 0 ∧ swap12 1 = 2 ∧ swap12 2 = 1 := by decide

/-- The three terminal cases of the F proof: a datum below 3 is 0, 1 or 2. -/
theorem three_cases (x : Nat) (hx : x < 3) : x = 0 ∨ x = 1 ∨ x = 2 := by omega

/-- Below cost 2 nothing is valid in reading F either (Genesis, cited). -/
theorem one_item_fails_F (a : Item) : ¬ validResponse R2F 1 2 [a] :=
  cost1_insufficient_F [a] (Nat.le_refl 1)

end Textbook.U32

#print axioms Textbook.U32.genesis_mark_collapsed_12
#print axioms Textbook.U32.genesis_mark_separates_01
#print axioms Textbook.U32.genesis_mark_delta_invalid
#print axioms Textbook.U32.deltaU2F_valid
#print axioms Textbook.U32.u2f_is_u0f_class
#print axioms Textbook.U32.swap12_values
#print axioms Textbook.U32.three_cases
#print axioms Textbook.U32.one_item_fails_F
#print axioms Derivation.genesis_mark_not_separable
#print axioms Derivation.mu2_unique_F
#print axioms Derivation.deltaU0F_valid
#print axioms Derivation.cost1_insufficient_F
"""

EXPECTED = {
    "Textbook.U32.genesis_mark_collapsed_12": BOTH,
    "Textbook.U32.genesis_mark_separates_01": BOTH,
    "Textbook.U32.genesis_mark_delta_invalid": BOTH,
    "Textbook.U32.deltaU2F_valid": BOTH,
    "Textbook.U32.u2f_is_u0f_class": BOTH,
    "Textbook.U32.swap12_values": NONE,
    "Textbook.U32.three_cases": BOTH,
    "Textbook.U32.one_item_fails_F": PROPEXT,
    "Derivation.genesis_mark_not_separable": BOTH,
    "Derivation.mu2_unique_F": BOTH,
    "Derivation.deltaU0F_valid": BOTH,
    "Derivation.cost1_insufficient_F": PROPEXT,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U32"))
