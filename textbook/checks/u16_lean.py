"""Unit 16 check: kernel-check the book's Lean for Unit 16.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u16_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Minimality

namespace Textbook.U16
open Derivation

/-- The demand of Challenge 3, reading L: separate data 0 and 1. It is
recorded in the regime. -/
theorem demand_recorded_L : (0, 1) ∈ R2L.reqs := by decide

/-- Reading F records (1, 2). -/
theorem demand_recorded_F : (1, 2) ∈ R2F.reqs := by decide

/-- The current regime does not meet it: collapse (Unit 10) rules out a
witness (Unit 09). -/
theorem demand_fails_L : ¬ separable R2L 0 1 :=
  fun h => separable_not_collapsed h R2L_collapsed

theorem demand_fails_F : ¬ separable R2F 1 2 :=
  fun h => separable_not_collapsed h (R2F_collapsed 1 2)

/-- Stronger than "no witness": there is no well-formed context at all,
because no form has been admitted. -/
theorem no_context_L (c : Ctx) : ¬ wfCtx R2L c :=
  fun h => Nat.not_lt_zero _ h.1

theorem no_context_F (c : Ctx) : ¬ wfCtx R2F c :=
  fun h => Nat.not_lt_zero _ h.1

/-- Absence of a separating witness gives collapse. Double-negation
elimination is applied only to the individual context's decidable iff,
not to the global separability proposition. -/
theorem collapsed_of_not_separable (r : Regime) (d d' : Nat)
    (h : ¬ separable r d d') : collapsed r d d' :=
  fun c hc => Decidable.of_not_not (fun hn => h ⟨c, hc, hn⟩)

/-- The metatheory still tells the two data apart by index. -/
theorem indices_differ : (0 : Nat) ≠ 1 := Nat.zero_ne_one

/-- Every pair in `R2F` is collapsed, including the pair the demand names
and the two pairs it does not. -/
theorem R2F_all_pairs :
    collapsed R2F 0 1 ∧ collapsed R2F 0 2 ∧ collapsed R2F 1 2 :=
  ⟨R2F_collapsed 0 1, R2F_collapsed 0 2, R2F_collapsed 1 2⟩

end Textbook.U16

#print axioms Textbook.U16.demand_recorded_L
#print axioms Textbook.U16.demand_recorded_F
#print axioms Textbook.U16.demand_fails_L
#print axioms Textbook.U16.demand_fails_F
#print axioms Textbook.U16.no_context_L
#print axioms Textbook.U16.no_context_F
#print axioms Textbook.U16.collapsed_of_not_separable
#print axioms Textbook.U16.indices_differ
#print axioms Textbook.U16.R2F_all_pairs
#print axioms Derivation.R2L_collapsed
#print axioms Derivation.R2F_collapsed
#print axioms Derivation.separable_not_collapsed
"""

EXPECTED = {
    "Textbook.U16.demand_recorded_L": BOTH,
    "Textbook.U16.demand_recorded_F": BOTH,
    "Textbook.U16.demand_fails_L": PROPEXT,
    "Textbook.U16.demand_fails_F": PROPEXT,
    "Textbook.U16.no_context_L": PROPEXT,
    "Textbook.U16.no_context_F": PROPEXT,
    "Textbook.U16.collapsed_of_not_separable": BOTH,
    "Textbook.U16.indices_differ": NONE,
    "Textbook.U16.R2F_all_pairs": PROPEXT,
    "Derivation.R2L_collapsed": PROPEXT,
    "Derivation.R2F_collapsed": PROPEXT,
    "Derivation.separable_not_collapsed": PROPEXT,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U16"))
