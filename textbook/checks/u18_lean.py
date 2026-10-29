"""Unit 18 check: kernel-check the book's Lean for Unit 18.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u18_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Minimality

namespace Textbook.U18
open Derivation

/-- The empty delta changes nothing, so it inherits the failure of
Unit 16. -/
theorem empty_delta_fails : ¬ validResponse R2L 0 1 [] :=
  cost1_insufficient [] (Nat.zero_le 1)

/-- A new datum alone: the regime grows, the pair stays collapsed. -/
theorem datum_alone_applies : applyDelta R2L [.newDatum] = some ⟨3, [], [], [], [(0, 1)]⟩ := by
  decide

theorem datum_alone_fails : ¬ validResponse R2L 0 1 [.newDatum] :=
  cost1_insufficient _ (Nat.le_refl 1)

/-- A new form alone: it applies, but no instance uses it. -/
theorem form_alone_applies : applyDelta R2L [.newForm 2] = some ⟨2, [2], [], [], [(0, 1)]⟩ := by
  decide

theorem form_alone_fails : ¬ validResponse R2L 0 1 [.newForm 2] :=
  cost1_insufficient _ (Nat.le_refl 1)

/-- An instance alone does not even apply: there is no form to instance. -/
theorem inst_alone_rejected (f : Nat) (args : List Nat) :
    applyDelta R2L [.newInst f args] = none := by
  rw [applyDelta_single]
  simp [applyItem, R2L]

/-- A rule alone does not apply either. -/
theorem rule_alone_rejected (f : Nat) :
    applyDelta R2L [.newRuleAll f] = none := by
  rw [applyDelta_single]
  simp [applyItem, R2L]

/-- The general theorem, applied to a regime that is not one of the two
Challenge 3 regimes: five data, no forms, no instances, two demands. -/
def R5 : Regime := ⟨5, [], [], [], [(0, 1), (2, 4)]⟩

theorem R5_cost1_fails (δ : List Item) (hlen : δ.length ≤ 1) :
    ¬ validResponse R5 2 4 δ :=
  cost1_insufficient_general R5 rfl rfl 2 4 δ hlen

/-- The hypothesis `forms = []` is used: on a regime with a form, one item
can be a valid response. -/
def R2form : Regime := ⟨2, [1], [], [], [(0, 1)]⟩

theorem one_item_suffices_with_a_form :
    validResponse R2form 0 1 [.newInst 0 [0]] :=
  validResponse_R2L_like
where
  validResponse_R2L_like : validResponse R2form 0 1 [.newInst 0 [0]] :=
    ⟨⟨2, [1], [(0, [0])], [], [(0, 1)]⟩, by decide,
     ⟨⟨0, [none]⟩, by decide, by decide⟩,
     fun q hq => by
       have : q = (0, 1) := by
         cases hq with
         | head => rfl
         | tail _ h => cases h
       rw [this]
       exact ⟨⟨0, [none]⟩, by decide, by decide⟩⟩

/-- With no forms there is no well-formed context, even if a raw record
contains an instance naming an unknown form. -/
theorem no_forms_no_separation (r : Regime) (hf : r.forms = []) (i j : Nat) :
    ¬ separable r i j := by
  intro ⟨c, hc, _⟩
  have h := hc.1
  simp [hf] at h

def unknownFormRecord : Regime := ⟨2, [], [(0, [0, 1])], [], [(0, 1)]⟩

theorem unknown_form_not_separable : ¬ separable unknownFormRecord 0 1 :=
  no_forms_no_separation unknownFormRecord rfl 0 1

theorem unknown_form_not_wf : ¬ unknownFormRecord.wf := by
  intro h
  have hi := h.1 (0, [0, 1]) (by decide)
  exact Nat.not_lt_zero _ hi.1

end Textbook.U18

#print axioms Textbook.U18.empty_delta_fails
#print axioms Textbook.U18.datum_alone_applies
#print axioms Textbook.U18.datum_alone_fails
#print axioms Textbook.U18.form_alone_applies
#print axioms Textbook.U18.form_alone_fails
#print axioms Textbook.U18.inst_alone_rejected
#print axioms Textbook.U18.rule_alone_rejected
#print axioms Textbook.U18.R5_cost1_fails
#print axioms Textbook.U18.one_item_suffices_with_a_form
#print axioms Textbook.U18.no_forms_no_separation
#print axioms Textbook.U18.unknown_form_not_separable
#print axioms Textbook.U18.unknown_form_not_wf
#print axioms Derivation.cost1_insufficient_general
#print axioms Derivation.cost1_insufficient
#print axioms Derivation.cost1_insufficient_F
#print axioms Derivation.no_insts_no_separation
"""

EXPECTED = {
    "Textbook.U18.empty_delta_fails": PROPEXT,
    "Textbook.U18.datum_alone_applies": PROPEXT,
    "Textbook.U18.datum_alone_fails": PROPEXT,
    "Textbook.U18.form_alone_applies": PROPEXT,
    "Textbook.U18.form_alone_fails": PROPEXT,
    "Textbook.U18.inst_alone_rejected": PROPEXT,
    "Textbook.U18.rule_alone_rejected": PROPEXT,
    "Textbook.U18.R5_cost1_fails": PROPEXT,
    "Textbook.U18.one_item_suffices_with_a_form": BOTH,
    "Textbook.U18.no_forms_no_separation": PROPEXT,
    "Textbook.U18.unknown_form_not_separable": PROPEXT,
    "Textbook.U18.unknown_form_not_wf": BOTH,
    "Derivation.cost1_insufficient_general": PROPEXT,
    "Derivation.cost1_insufficient": PROPEXT,
    "Derivation.cost1_insufficient_F": PROPEXT,
    "Derivation.no_insts_no_separation": PROPEXT,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U18"))
