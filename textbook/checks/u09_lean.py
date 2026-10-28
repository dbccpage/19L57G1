"""Unit 09 check: kernel-check the book's Lean for Unit 09.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u09_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, PROPEXT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Minimality

namespace Textbook.U09
open Derivation

/-- The theorem, re-proved with every step named. -/
theorem separable_not_collapsed' (r : Regime) (d d' : Nat)
    (h : separable r d d') : ¬ collapsed r d d' := by
  intro hc
  obtain ⟨c, hwf, hne⟩ := h
  have hiff : derivable r (plug c d) ↔ derivable r (plug c d') := hc c hwf
  exact hne hiff

/-- The other direction, constructive because both sides are decidable:
no witness at all means every context agrees. -/
theorem collapsed_of_not_separable (r : Regime) (d d' : Nat)
    (h : ¬ separable r d d') : collapsed r d d' := by
  intro c hwf
  by_cases hiff : derivable r (plug c d) ↔ derivable r (plug c d')
  · exact hiff
  · exact absurd ⟨c, hwf, hiff⟩ h

/-- Collapse is exactly the absence of a witness. -/
theorem collapsed_iff_not_separable (r : Regime) (d d' : Nat) :
    collapsed r d d' ↔ ¬ separable r d d' :=
  ⟨fun hc hs => separable_not_collapsed hs hc, collapsed_of_not_separable r d d'⟩

/-- The unary-mark regime: datum 1 marked, datum 0 not. Separable, so not
collapsed; the witness is the one-hole unary context. -/
theorem U1_not_collapsed : ¬ collapsed U1 0 1 :=
  separable_not_collapsed U1_separable

/-- A regime with no witness: the empty one. Not separable, so collapsed. -/
theorem empty_two_collapsed : collapsed ⟨2, [], [], [], []⟩ 0 1 := by
  intro c hwf
  exact absurd hwf.1 (by simp)

end Textbook.U09

#print axioms Textbook.U09.separable_not_collapsed'
#print axioms Textbook.U09.collapsed_of_not_separable
#print axioms Textbook.U09.collapsed_iff_not_separable
#print axioms Textbook.U09.U1_not_collapsed
#print axioms Textbook.U09.empty_two_collapsed
#print axioms Derivation.separable_not_collapsed
#print axioms Derivation.U1_separable
"""

EXPECTED = {
    "Textbook.U09.separable_not_collapsed'": PROPEXT,
    "Textbook.U09.collapsed_of_not_separable": BOTH,
    "Textbook.U09.collapsed_iff_not_separable": BOTH,
    "Textbook.U09.U1_not_collapsed": BOTH,
    "Textbook.U09.empty_two_collapsed": PROPEXT,
    "Derivation.separable_not_collapsed": PROPEXT,
    "Derivation.U1_separable": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U09"))
