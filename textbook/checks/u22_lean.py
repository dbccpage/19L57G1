"""Unit 22 check: kernel-check the book's Lean for Unit 22.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u22_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Minimality
import Derivation.MinimalityF

namespace Textbook.U22
open Derivation

/-- `aritySum` splits at the head. -/
theorem aritySum_cons (a : Item) (rest : List Item) :
    aritySum (a :: rest) = aritySum [a] + aritySum rest := by
  cases a <;> simp [aritySum]

/-- One item of arity sum zero, applied to a form-less, instance-less
regime, leaves it form-less and instance-less (or does not apply). -/
theorem applyItem_zero_keeps_bare (r : Regime) (hf : r.forms = [])
    (hi : r.insts = []) (it : Item) (hz : aritySum [it] = 0) (s : Regime)
    (h : applyItem r it = some s) : s.forms = [] ∧ s.insts = [] := by
  cases it with
  | newDatum =>
      cases Option.some.inj h
      exact ⟨hf, hi⟩
  | newForm a =>
      have ha : a = 0 := by simpa [aritySum] using hz
      subst ha
      simp [applyItem] at h
  | newInst f args =>
      simp only [applyItem] at h
      rw [if_neg (by simp [hf])] at h
      cases h
  | newRuleAll f =>
      simp only [applyItem] at h
      rw [if_neg (by simp [hf])] at h
      cases h

/-- No valid two-item response has new-form arity sum 0: the mu2 floor
`(2, 1)` is attained, not merely bounded (the paper's "absence of valid
(2, 0) deltas"). -/
theorem no_arity_zero_response (a b : Item)
    (hval : validResponse R2L 0 1 [a, b]) (har : aritySum [a, b] = 0) :
    False := by
  obtain ⟨s, happ, hsep, -⟩ := hval
  rw [applyDelta_pair] at happ
  have hab := aritySum_cons a [b]
  have ha0 : aritySum [a] = 0 := by omega
  have hb0 : aritySum [b] = 0 := by omega
  cases h1 : applyItem R2L a with
  | none => rw [h1] at happ; cases happ
  | some r1 =>
      rw [h1] at happ
      have hr1 := applyItem_zero_keeps_bare R2L rfl rfl a ha0 r1 h1
      have hs := applyItem_zero_keeps_bare r1 hr1.1 hr1.2 b hb0 s happ
      exact no_insts_no_separation hs.2 hsep

/-- The unary mark on datum 1 is a valid two-item response of arity sum 1,
so the theorem's hypotheses are met and its conclusion names an
isomorphism onto `U0`. -/
theorem mark1_is_U0_class :
    ∃ s, applyDelta R2L deltaU1 = some s ∧ Nonempty (Iso s U0) :=
  mu2_unique (.newForm 1) (.newInst 0 [1]) deltaU1_valid (by decide)

/-- The link is excluded by the hypothesis, not by the conclusion. -/
theorem link_arity_two : ¬ aritySum deltaBL ≤ 1 := by decide

/-- A two-item delta of arity sum at most one has at most one form, and
that form is unary (the shape the proof's live branch uses). -/
theorem form_in_cheap_delta (c : Nat) (b : Item)
    (har : aritySum [Item.newForm c, b] ≤ 1) : c ≤ 1 := by
  have h := aritySum_cons (.newForm c) [b]
  have hc : aritySum [Item.newForm c] = c := by simp [aritySum]
  omega

/-- mu2 is lexicographic: item count first. Both minima of Unit 21 cost
two items; their arity sums 1 and 2 break the tie. -/
theorem mu2_breaks_tie : aritySum deltaU0 < aritySum deltaBL := by decide

end Textbook.U22

#print axioms Textbook.U22.aritySum_cons
#print axioms Textbook.U22.applyItem_zero_keeps_bare
#print axioms Textbook.U22.no_arity_zero_response
#print axioms Textbook.U22.mark1_is_U0_class
#print axioms Textbook.U22.link_arity_two
#print axioms Textbook.U22.form_in_cheap_delta
#print axioms Textbook.U22.mu2_breaks_tie
#print axioms Derivation.mu2_unique
#print axioms Derivation.mu2_unique_F
#print axioms Derivation.isoRefl
"""

EXPECTED = {
    "Textbook.U22.aritySum_cons": PROPEXT,
    "Textbook.U22.applyItem_zero_keeps_bare": PROPEXT,
    "Textbook.U22.no_arity_zero_response": BOTH,
    "Textbook.U22.mark1_is_U0_class": BOTH,
    "Textbook.U22.link_arity_two": PROPEXT,
    "Textbook.U22.form_in_cheap_delta": BOTH,
    "Textbook.U22.mu2_breaks_tie": PROPEXT,
    "Derivation.mu2_unique": BOTH,
    "Derivation.mu2_unique_F": BOTH,
    "Derivation.isoRefl": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U22"))
