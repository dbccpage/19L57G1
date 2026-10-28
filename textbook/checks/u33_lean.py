"""Unit 33 check: kernel-check the book's Lean for Unit 33.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u33_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.RuleBridge

namespace Textbook.U33
open Derivation

/-- `dropRules` by example: the rule item goes, the order of the rest stays. -/
theorem dropRules_example :
    dropRules [.newForm 1, .newRuleAll 0, .newInst 0 [1]] = [.newForm 1, .newInst 0 [1]] := rfl

/-- Dropping twice is dropping once. -/
theorem dropRules_idem : ∀ δ : List Item, dropRules (dropRules δ) = dropRules δ
  | [] => rfl
  | .newRuleAll _ :: rest => dropRules_idem rest
  | .newDatum :: rest => by
      show Item.newDatum :: dropRules (dropRules rest) = Item.newDatum :: dropRules rest
      rw [dropRules_idem rest]
  | .newForm a :: rest => by
      show Item.newForm a :: dropRules (dropRules rest) = Item.newForm a :: dropRules rest
      rw [dropRules_idem rest]
  | .newInst f args :: rest => by
      show Item.newInst f args :: dropRules (dropRules rest)
        = Item.newInst f args :: dropRules rest
      rw [dropRules_idem rest]

/-- A valid response to Challenge 3 that carries a rule item: the mark, a
second unary form, and the uniform rule on that second form. -/
def ruleDelta : List Item := [.newForm 1, .newInst 0 [0], .newForm 1, .newRuleAll 1]
def ruled : Regime := ⟨2, [1, 1], [(0, [0])], [1], [(0, 1)]⟩

theorem ruleDelta_applies : applyDelta R2L ruleDelta = some ruled := by decide

theorem ruleDelta_valid : validResponse R2L 0 1 ruleDelta := by
  refine ⟨ruled, ruleDelta_applies, ?_, ?_⟩
  · exact ⟨⟨0, [none]⟩, by decide, by decide⟩
  · intro q hq
    have : q = (0, 1) := by
      cases hq with
      | head => rfl
      | tail _ h => cases h
    rw [this]
    exact ⟨⟨0, [none]⟩, by decide, by decide⟩

theorem ruleDelta_dropped : dropRules ruleDelta = [.newForm 1, .newInst 0 [0], .newForm 1] := rfl

/-- Genesis's corollary at this delta: the drop is valid, has 3 items
against 4, and the same arity sum. -/
theorem ruleDelta_never_minimal :
    validResponse R2L 0 1 (dropRules ruleDelta) ∧
    (dropRules ruleDelta).length < ruleDelta.length ∧
    aritySum (dropRules ruleDelta) = aritySum ruleDelta :=
  rule_item_never_minimal (f := 1) (by decide) ruleDelta_valid

/-- The bridge at this delta: the dropped delta applied over ANY rule
field gives the same regime with that rule field. -/
theorem bridge_example (rs : List Nat) :
    applyDelta ⟨2, [], [], rs, [(0, 1)]⟩ (dropRules ruleDelta)
      = some ⟨2, [1, 1], [(0, [0])], rs, [(0, 1)]⟩ :=
  applyDelta_dropRules rs ruleDelta_applies

/-- The other direction is not free: ADDING the uniform rule on the only
form of the mark collapses the pair again. The subset condition in
`separable_of_subrules` is load-bearing. -/
theorem rule_on_mark_collapses : collapsed ⟨2, [1], [(0, [0])], [0], [(0, 1)]⟩ 0 1 := by
  intro c hc
  rw [one_unary_form_ctx_char _ rfl c] at hc
  subst hc
  decide

theorem rule_on_mark_not_separable : ¬ separable ⟨2, [1], [(0, [0])], [0], [(0, 1)]⟩ 0 1 :=
  fun h => separable_not_collapsed h rule_on_mark_collapses

end Textbook.U33

#print axioms Textbook.U33.dropRules_example
#print axioms Textbook.U33.dropRules_idem
#print axioms Textbook.U33.ruleDelta_applies
#print axioms Textbook.U33.ruleDelta_valid
#print axioms Textbook.U33.ruleDelta_never_minimal
#print axioms Textbook.U33.bridge_example
#print axioms Textbook.U33.rule_on_mark_collapses
#print axioms Textbook.U33.rule_on_mark_not_separable
#print axioms Derivation.applyDelta_dropRules
#print axioms Derivation.validResponse_dropRules
#print axioms Derivation.rule_item_never_minimal
#print axioms Derivation.separable_of_subrules
"""

EXPECTED = {
    "Textbook.U33.dropRules_example": PROPEXT,
    "Textbook.U33.dropRules_idem": PROPEXT,
    "Textbook.U33.ruleDelta_applies": PROPEXT,
    "Textbook.U33.ruleDelta_valid": BOTH,
    "Textbook.U33.ruleDelta_never_minimal": BOTH,
    "Textbook.U33.bridge_example": PROPEXT,
    "Textbook.U33.rule_on_mark_collapses": BOTH,
    "Textbook.U33.rule_on_mark_not_separable": BOTH,
    "Derivation.applyDelta_dropRules": PROPEXT,
    "Derivation.validResponse_dropRules": PROPEXT,
    "Derivation.rule_item_never_minimal": PROPEXT,
    "Derivation.separable_of_subrules": PROPEXT,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U33"))
