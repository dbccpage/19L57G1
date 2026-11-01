"""Unit 06 check: kernel-check the book's Lean for Unit 06.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u06_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Inertia
import Derivation.Erasure

namespace Textbook.U06
open Derivation

/-- Token-aware genesis: no tokens. -/
def tgenesis : TRegime := ⟨[], [], [], [], []⟩

/-- Re-admitting a present token changes nothing: it designates. -/
theorem readmit_designates (t : TRegime) (tok : Nat) (h : tok ∈ t.tokens) :
    stepT t (.admitDatum tok) = some t := by
  simp [stepT, h]

/-- Admitting an absent token appends it, in admission order. -/
theorem fresh_appends (t : TRegime) (tok : Nat) (h : tok ∉ t.tokens) :
    stepT t (.admitDatum tok) = some { t with tokens := t.tokens ++ [tok] } := by
  simp [stepT, h]

/-- Seen through erasure, a re-admission is a bare supply. -/
theorem readmit_erases_to_supply (t : TRegime) (tok : Nat) (h : tok ∈ t.tokens) :
    eraseEvent t (.admitDatum tok) = .supply tok := by
  simp [eraseEvent, h]

/-- Admitting ⟨A⟩ twice leaves one datum. -/
theorem twice_is_once :
    replayT [.admitDatum 1, .admitDatum 1] tgenesis = some ⟨[1], [], [], [], []⟩ := by
  decide

/-- The token-erased model cannot dedup on its own: two `admitDatum`
events count two. The dedup is carried by the erased *history*. -/
theorem erased_model_counts :
    replayE [.admitDatum, .admitDatum] genesis = some ⟨2, [], [], [], []⟩ := rfl

theorem erased_history_of_twice :
    eraseHistory tgenesis [.admitDatum 1, .admitDatum 1] = [.admitDatum, .supply 1] := by
  decide

/-- Admission order is kept by the token-aware state and is visible to the
metatheory: the two orders are two states. -/
theorem order_kept :
    replayT [.admitDatum 1, .admitDatum 2] tgenesis
      ≠ replayT [.admitDatum 2, .admitDatum 1] tgenesis := by
  decide

theorem same_outcome_different_events (t : TRegime) (tok : Nat) (h : tok ∈ t.tokens) :
    stepT t (.admitDatum tok) = stepT t (.supply tok) ∧
    (TEvent.admitDatum tok) ≠ TEvent.supply tok := by
  constructor
  · simp [stepT, h]
  · intro heq; cases heq

theorem raw_duplicates_are_not_cleaned :
    stepT ⟨[1,1], [], [], [], []⟩ (.admitDatum 1) =
      some ⟨[1,1], [], [], [], []⟩ := by decide

end Textbook.U06

#print axioms Textbook.U06.readmit_designates
#print axioms Textbook.U06.fresh_appends
#print axioms Textbook.U06.readmit_erases_to_supply
#print axioms Textbook.U06.twice_is_once
#print axioms Textbook.U06.erased_model_counts
#print axioms Textbook.U06.erased_history_of_twice
#print axioms Textbook.U06.order_kept
#print axioms Derivation.stepT
#print axioms Textbook.U06.same_outcome_different_events
#print axioms Textbook.U06.raw_duplicates_are_not_cleaned
"""

EXPECTED = {
    "Textbook.U06.readmit_designates": BOTH,
    "Textbook.U06.fresh_appends": BOTH,
    "Textbook.U06.readmit_erases_to_supply": BOTH,
    "Textbook.U06.twice_is_once": BOTH,
    "Textbook.U06.erased_model_counts": PROPEXT,
    "Textbook.U06.erased_history_of_twice": BOTH,
    "Textbook.U06.order_kept": BOTH,
    "Derivation.stepT": BOTH,
    "Textbook.U06.same_outcome_different_events": BOTH,
    "Textbook.U06.raw_duplicates_are_not_cleaned": BOTH,
}
_ = NONE

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U06"))
