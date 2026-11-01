"""Unit 19 check: kernel-check the book's Lean for Unit 19.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u19_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Minimality
import Derivation.Mention

namespace Textbook.U19
open Derivation

/-- The witness Genesis names: the hole in the first slot, datum 1 in
the second. -/
theorem BL_witness_wf : wfCtx BL ⟨0, [none, some 1]⟩ := by decide

/-- Plugged with 0 it is the admitted link; plugged with 1 it is not. -/
theorem BL_plug0 : plug ⟨0, [none, some 1]⟩ 0 = (0, [0, 1]) := rfl
theorem BL_plug1 : plug ⟨0, [none, some 1]⟩ 1 = (0, [1, 1]) := rfl
theorem BL_derivable_01 : derivable BL (0, [0, 1]) := by decide
theorem BL_not_derivable_11 : ¬ derivable BL (0, [1, 1]) := by decide

/-- The theorem, assembled from those four facts. -/
theorem BL_separable' : separable BL 0 1 :=
  ⟨⟨0, [none, some 1]⟩, BL_witness_wf,
   fun h => BL_not_derivable_11 (h.mp BL_derivable_01)⟩

/-- A second witness: the hole in the other slot. -/
theorem BL_second_witness : separable BL 0 1 :=
  ⟨⟨0, [some 0, none]⟩, by decide, by decide⟩

/-- Not every context is a witness: with datum 0 in the second slot the
plugging is derivable for neither datum. -/
theorem BL_non_witness :
    ¬ derivable BL (plug ⟨0, [none, some 0]⟩ 0) ∧
    ¬ derivable BL (plug ⟨0, [none, some 0]⟩ 1) := by decide

/-- `BL` is the result of applying the link delta to `R2L`. -/
theorem deltaBL_lands : applyDelta R2L deltaBL = some BL := by decide

/-- And that makes the delta a valid response (Genesis's `deltaBL_valid`,
re-assembled). -/
theorem deltaBL_valid' : validResponse R2L 0 1 deltaBL :=
  validResponse_R2L deltaBL BL deltaBL_lands BL_separable'

/-- `BL` is well formed. -/
theorem BL_wf : BL.wf := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [BL]

/-- A uniform rule makes every test positive, losing the distinction
while retaining the original link instance. -/
theorem BL_uniform_collapsed : collapsed { BL with rules := [0] } 0 1 := by
  intro c hc
  have hlt : c.form < 1 := hc.1
  have hf : c.form = 0 := by omega
  have hr : c.form ∈ ([0] : List Nat) := by simp [hf]
  exact ⟨fun _ => Or.inr hr, fun _ => Or.inr hr⟩

def pending : Regime := ⟨3, [], [], [], [(0, 1), (1, 2)]⟩
def partialRepair : Regime := ⟨3, [1], [(0, [0])], [], [(0, 1), (1, 2)]⟩

theorem partial_lands : applyDelta pending deltaU0 = some partialRepair := by decide

theorem partial_target_separated : separable partialRepair 0 1 :=
  ⟨⟨0, [none]⟩, by decide, by decide⟩

theorem partial_other_collapsed : collapsed partialRepair 1 2 :=
  (collapsed_append_unmentioning ⟨3, [1], [], [], [(0, 1), (1, 2)]⟩
    [(0, [0])] 1 2 (by decide) (by decide)).mpr
      (collapsed_of_no_insts _ rfl 1 2)

theorem partial_response_invalid : ¬ validResponse pending 0 1 deltaU0 := by
  intro ⟨s, hs, _, hall⟩
  have heq : partialRepair = s := Option.some.inj (partial_lands.symm.trans hs)
  subst s
  exact separable_not_collapsed (hall (1, 2) (by decide)) partial_other_collapsed

theorem middle_mark_meets_both : validResponse pending 0 1 deltaU1 := by
  refine ⟨⟨3, [1], [(0, [1])], [], [(0, 1), (1, 2)]⟩, by decide,
    ⟨⟨0, [none]⟩, by decide, by decide⟩, ?_⟩
  intro q hq
  have h : q = (0, 1) ∨ q = (1, 2) := by simpa [pending] using hq
  rcases h with h | h <;> subst q <;>
    exact ⟨⟨0, [none]⟩, by decide, by decide⟩

end Textbook.U19

#print axioms Textbook.U19.BL_witness_wf
#print axioms Textbook.U19.BL_plug0
#print axioms Textbook.U19.BL_derivable_01
#print axioms Textbook.U19.BL_not_derivable_11
#print axioms Textbook.U19.BL_separable'
#print axioms Textbook.U19.BL_second_witness
#print axioms Textbook.U19.BL_non_witness
#print axioms Textbook.U19.deltaBL_lands
#print axioms Textbook.U19.deltaBL_valid'
#print axioms Textbook.U19.BL_wf
#print axioms Textbook.U19.BL_uniform_collapsed
#print axioms Derivation.BL_separable
#print axioms Derivation.deltaBL_valid
#print axioms Derivation.validResponse_R2L
#print axioms Textbook.U19.partial_lands
#print axioms Textbook.U19.partial_target_separated
#print axioms Textbook.U19.partial_other_collapsed
#print axioms Textbook.U19.partial_response_invalid
#print axioms Textbook.U19.middle_mark_meets_both
"""

EXPECTED = {
    "Textbook.U19.BL_witness_wf": BOTH,
    "Textbook.U19.BL_plug0": NONE,
    "Textbook.U19.BL_derivable_01": BOTH,
    "Textbook.U19.BL_not_derivable_11": BOTH,
    "Textbook.U19.BL_separable'": BOTH,
    "Textbook.U19.BL_second_witness": BOTH,
    "Textbook.U19.BL_non_witness": BOTH,
    "Textbook.U19.deltaBL_lands": PROPEXT,
    "Textbook.U19.deltaBL_valid'": BOTH,
    "Textbook.U19.BL_wf": BOTH,
    "Textbook.U19.BL_uniform_collapsed": BOTH,
    "Derivation.BL_separable": BOTH,
    "Derivation.deltaBL_valid": BOTH,
    "Derivation.validResponse_R2L": PROPEXT,
    "Textbook.U19.partial_lands": PROPEXT,
    "Textbook.U19.partial_target_separated": BOTH,
    "Textbook.U19.partial_other_collapsed": BOTH,
    "Textbook.U19.partial_response_invalid": BOTH,
    "Textbook.U19.middle_mark_meets_both": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U19"))
