"""Unit 04 check (book Lean): the six event kinds are all there is.

Kernel-checks the book's Lean for Unit 04 against Genesis's compiled
library. Not part of Genesis's build or gates. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u04_lean.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from booklean import BOTH, NONE, PROPEXT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Inertia

namespace Textbook.U04
open Derivation

/-- Every event is one of the six kinds, and no other: the grammar is
closed. -/
theorem event_is_one_of_six (e : Event) :
    (∃ t, e = .supply t) ∨ e = .admitDatum ∨ (∃ a, e = .admitForm a) ∨
    (∃ f args, e = .admitInst f args) ∨ (∃ f, e = .admitRuleAll f) ∨
    (∃ i j, e = .impose i j) := by
  cases e with
  | supply t => exact Or.inl ⟨t, rfl⟩
  | admitDatum => exact Or.inr (Or.inl rfl)
  | admitForm a => exact Or.inr (Or.inr (Or.inl ⟨a, rfl⟩))
  | admitInst f args => exact Or.inr (Or.inr (Or.inr (Or.inl ⟨f, args, rfl⟩)))
  | admitRuleAll f => exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨f, rfl⟩))))
  | impose i j => exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr ⟨i, j, rfl⟩))))

/-- With no event, nothing moves: the empty history replays to its base. -/
theorem no_event_no_change (r : Regime) : replayE [] r = some r := rfl

/-- Every change of ledger is indexed by an event: if a one-event history
changes the regime, that event was not a supply. -/
theorem change_needs_non_supply (r s : Regime) (e : Event)
    (h : replayE [e] r = some s) (hne : s ≠ r) : ∀ t, e ≠ .supply t := by
  intro t het
  subst het
  exact hne (Option.some.inj h).symm

end Textbook.U04

#print axioms Textbook.U04.event_is_one_of_six
#print axioms Textbook.U04.no_event_no_change
#print axioms Textbook.U04.change_needs_non_supply
"""

EXPECTED = {
    "Textbook.U04.event_is_one_of_six": NONE,
    "Textbook.U04.no_event_no_change": PROPEXT,
    "Textbook.U04.change_needs_non_supply": PROPEXT,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U04"))
