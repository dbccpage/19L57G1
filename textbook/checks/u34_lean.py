"""Unit 34 check: kernel-check the book's Lean for Unit 34.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u34_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Rounds
import Derivation.Minimality

namespace Textbook.U34
open Derivation

/-- Two data, nothing imposed: the state before Challenge 3 is imposed. -/
def bare2 : Regime := ⟨2, [], [], [], []⟩

/-- One round: impose (0, 1), answer with the mark. The outcome is U0. -/
theorem one_round : respond bare2 0 1 deltaU0 = some U0 := by decide

/-- Its anatomy, read off: the demand is inserted, the datum count kept. -/
theorem one_round_anatomy : U0.reqs = insertNew bare2.reqs (0, 1) ∧ U0.data = bare2.data :=
  ⟨rfl, rfl⟩

/-- The two side conditions of a closed round hold here. -/
theorem one_round_fresh : (0, 1) ∉ bare2.reqs := by decide
theorem one_round_no_datum : Item.newDatum ∉ deltaU0 := by decide

/-- So it is a closed run of length one. -/
theorem run1 : ClosedRun bare2 [⟨(0, 1), deltaU0⟩] U0 :=
  ClosedRun.cons bare2 ⟨(0, 1), deltaU0⟩ U0 U0 [] one_round_fresh one_round_no_datum
    one_round (ClosedRun.nil U0)

/-- Genesis's unit-growth theorem at this round. -/
theorem one_round_grows : U0.reqs.length = bare2.reqs.length + 1 :=
  round_reqs_succ one_round_fresh one_round

/-- Genesis's bound at this run: 2 * 1 <= 2 * 1. -/
theorem run1_bound : 2 * 1 ≤ bare2.data * (bare2.data - 1) :=
  closedRun_round_bound_from_empty run1 rfl

/-- And in general: no closed run from two data makes two rounds. -/
theorem two_data_one_round {rds : List Round} {t : Regime}
    (h : ClosedRun bare2 rds t) : rds.length ≤ 1 := by
  have hb := closedRun_round_bound_from_empty h rfl
  have h2 : bare2.data = 2 := rfl
  rw [h2] at hb
  omega

/-- Three data: at most three rounds. -/
theorem three_data_three_rounds {rds : List Round} {t : Regime}
    (h : ClosedRun ⟨3, [], [], [], []⟩ rds t) : rds.length ≤ 3 := by
  have hb := closedRun_round_bound_from_empty h rfl
  have h3 : (⟨3, [], [], [], []⟩ : Regime).data = 3 := rfl
  rw [h3] at hb
  omega

/-- Why the shape is declared: R2L already holds (0, 1), so imposing it
again is not a fresh round; and a response that admits a datum is a round
whose datum count moves. -/
theorem R2L_target_not_fresh : (0, 1) ∈ R2L.reqs := by decide

theorem datum_round_moves_data :
    respond bare2 0 1 [.newDatum, .newForm 1, .newInst 0 [0]]
      = some ⟨3, [1], [(0, [0])], [], [(0, 1)]⟩ := by decide

/-- The requirement language of two and of three data. -/
theorem allPairs_two_three : allPairs 2 = [(0, 1)] ∧ allPairs 3 = [(0, 1), (0, 2), (1, 2)] := by
  decide

/-- `ClosedRun` does not require a valid response or a met demand. -/
def unanswered : Regime := ⟨2, [], [], [], [(0, 1)]⟩

theorem unanswered_closed : ClosedRun bare2 [⟨(0, 1), []⟩] unanswered :=
  ClosedRun.cons bare2 ⟨(0, 1), []⟩ unanswered unanswered []
    (by decide) (by decide) (by decide) (ClosedRun.nil unanswered)

theorem empty_response_invalid : ¬ validResponse bare2 0 1 [] := by
  rintro ⟨s, hs, hsep, _⟩
  have he : applyDelta bare2 [] = some bare2 := rfl
  rw [he] at hs
  injection hs with hs
  subst hs
  exact separable_not_collapsed hsep (collapsed_of_no_insts bare2 rfl 0 1)

theorem repeat_response_no_growth : respond U0 0 1 [] = some U0 := by decide

end Textbook.U34

#print axioms Textbook.U34.one_round
#print axioms Textbook.U34.one_round_anatomy
#print axioms Textbook.U34.run1
#print axioms Textbook.U34.one_round_grows
#print axioms Textbook.U34.run1_bound
#print axioms Textbook.U34.two_data_one_round
#print axioms Textbook.U34.three_data_three_rounds
#print axioms Textbook.U34.R2L_target_not_fresh
#print axioms Textbook.U34.datum_round_moves_data
#print axioms Textbook.U34.allPairs_two_three
#print axioms Textbook.U34.unanswered_closed
#print axioms Textbook.U34.empty_response_invalid
#print axioms Textbook.U34.repeat_response_no_growth
#print axioms Derivation.respond_anatomy
#print axioms Derivation.round_reqs_succ
#print axioms Derivation.round_data_eq
#print axioms Derivation.closedRun_round_bound_from_empty
"""

EXPECTED = {
    "Textbook.U34.one_round": PROPEXT,
    "Textbook.U34.one_round_anatomy": PROPEXT,
    "Textbook.U34.run1": BOTH,
    "Textbook.U34.one_round_grows": BOTH,
    "Textbook.U34.run1_bound": BOTH,
    "Textbook.U34.two_data_one_round": BOTH,
    "Textbook.U34.three_data_three_rounds": BOTH,
    "Textbook.U34.R2L_target_not_fresh": BOTH,
    "Textbook.U34.datum_round_moves_data": PROPEXT,
    "Textbook.U34.allPairs_two_three": NONE,
    "Textbook.U34.unanswered_closed": BOTH,
    "Textbook.U34.empty_response_invalid": PROPEXT,
    "Textbook.U34.repeat_response_no_growth": PROPEXT,
    "Derivation.respond_anatomy": PROPEXT,
    "Derivation.round_reqs_succ": PROPEXT,
    "Derivation.round_data_eq": PROPEXT,
    "Derivation.closedRun_round_bound_from_empty": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U34"))
