"""Unit 35 check: kernel-check the book's Lean for Unit 35.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u35_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Progress
import Derivation.Minimality
import Derivation.Mention

namespace Textbook.U35
open Derivation

/-- The unary mark on two data is well formed. -/
theorem U0_wf : U0.wf := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [U0]

/-- Its one imposed demand is met. -/
theorem U0_reqs_met : ∀ q ∈ U0.reqs, separable U0 q.1 q.2 := by
  intro q hq
  have : q = (0, 1) := by
    cases hq with
    | head => rfl
    | tail _ h => cases h
  subst this
  exact ⟨⟨0, [none]⟩, by decide, by decide⟩

/-- Genesis's theorem at `U0`: a second fresh mark, on datum 1, is a
valid response to the (already met) demand `(0, 1)`. -/
theorem second_mark_valid :
    validResponse U0 0 1 [.newForm 1, .newInst U0.forms.length [1]] :=
  mark_progress U0 U0_wf 0 1 (by decide) (by decide) (by decide) U0_reqs_met

/-- The fresh form index at `U0` is 1: one form is already there. -/
theorem fresh_index : U0.forms.length = 1 := rfl

/-- On three bare data with no demand, the mark on datum 2 answers `(1, 2)`. -/
theorem bare3_mark_valid :
    validResponse ⟨3, [], [], [], []⟩ 1 2 [.newForm 1, .newInst 0 [2]] :=
  mark_progress ⟨3, [], [], [], []⟩
    (by refine ⟨?_, ?_, ?_, ?_⟩ <;> simp) 1 2 (by decide) (by decide) (by decide)
    (fun q hq => nomatch hq)

/-- Hypothesis 1 at work: with `(0, 1)` imposed and not yet met, the same
mark is not a valid response to `(1, 2)`, because it leaves `(0, 1)`
collapsed (the mention lemma). -/
theorem unmet_demand_blocks :
    ¬ validResponse ⟨3, [], [], [], [(0, 1)]⟩ 1 2 [.newForm 1, .newInst 0 [2]] := by
  rintro ⟨s, hs, -, hall⟩
  have happ : applyDelta (⟨3, [], [], [], [(0, 1)]⟩ : Regime) [.newForm 1, .newInst 0 [2]]
      = some ⟨3, [1], [(0, [2])], [], [(0, 1)]⟩ := by decide
  rw [happ] at hs
  injection hs with hs
  subst hs
  have hsep := hall (0, 1) (by simp)
  have base : collapsed (⟨3, [1], [], [], [(0, 1)]⟩ : Regime) 0 1 :=
    collapsed_of_no_insts _ rfl 0 1
  have hcol : collapsed (⟨3, [1], [(0, [2])], [], [(0, 1)]⟩ : Regime) 0 1 :=
    (collapsed_append_unmentioning ⟨3, [1], [], [], [(0, 1)]⟩
      [(0, [2])] 0 1 (by decide) (by decide)).mpr base
  exact separable_not_collapsed hsep hcol

/-- Hypothesis 2 at work: no context separates a datum from itself. -/
theorem no_self_separation (r : Regime) (d : Nat) : ¬ separable r d d :=
  fun ⟨_, _, h⟩ => h Iff.rfl

/-- So no delta is a valid response to a demand `(d, d)`. -/
theorem no_self_response (r : Regime) (d : Nat) (δ : List Item) :
    ¬ validResponse r d d δ :=
  fun ⟨s, _, hsep, _⟩ => no_self_separation s d hsep

/-- `derivable_extend` at `U0`: the old mark is derivable before and after
the second mark. -/
theorem old_mark_survives :
    derivable ⟨2, [1] ++ [1], [(0, [0])] ++ [(1, [1])], [], [(0, 1)]⟩ (0, [0]) ↔
      derivable U0 (0, [0]) :=
  derivable_extend U0_wf 1 (0, [0]) (by decide)

end Textbook.U35

#print axioms Textbook.U35.U0_wf
#print axioms Textbook.U35.U0_reqs_met
#print axioms Textbook.U35.second_mark_valid
#print axioms Textbook.U35.fresh_index
#print axioms Textbook.U35.bare3_mark_valid
#print axioms Textbook.U35.unmet_demand_blocks
#print axioms Textbook.U35.no_self_separation
#print axioms Textbook.U35.no_self_response
#print axioms Textbook.U35.old_mark_survives
#print axioms Derivation.mark_progress
#print axioms Derivation.derivable_extend
#print axioms Derivation.separable_of_subrules
"""

EXPECTED = {
    "Textbook.U35.U0_wf": BOTH,
    "Textbook.U35.U0_reqs_met": BOTH,
    "Textbook.U35.second_mark_valid": BOTH,
    "Textbook.U35.fresh_index": NONE,
    "Textbook.U35.bare3_mark_valid": BOTH,
    "Textbook.U35.unmet_demand_blocks": BOTH,
    "Textbook.U35.no_self_separation": PROPEXT,
    "Textbook.U35.no_self_response": PROPEXT,
    "Textbook.U35.old_mark_survives": BOTH,
    "Derivation.mark_progress": BOTH,
    "Derivation.derivable_extend": PROPEXT,
    "Derivation.separable_of_subrules": PROPEXT,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U35"))
