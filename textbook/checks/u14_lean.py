"""Unit 14 check: kernel-check the book's Lean for Unit 14.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u14_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.PrimDiff

namespace Textbook.U14
open PrimDiff

/-- The theorem, re-proved with every step named. -/
theorem factors_through_point_iff' {α : Type} (a b : α) :
    (∃ p : Unit → α, p () = a ∧ p () = b) ↔ a = b := by
  constructor
  · intro ⟨p, h1, h2⟩
    -- h1 : p () = a, h2 : p () = b; so a = p () = b
    exact h1.symm.trans h2
  · intro he
    -- the constant map at a; its value is a, and also b since a = b
    exact ⟨fun _ => a, rfl, he ▸ rfl⟩

/-- A map out of the point is the constant map at its one value. -/
theorem point_map_constant {α : Type} (p : Unit → α) :
    p = fun _ => p () := by
  funext u
  cases u
  rfl

/-- On `Bool`: the selection of `false` and `true` does not factor. -/
theorem no_factor_false_true :
    ¬ ∃ p : Unit → Bool, p () = false ∧ p () = true :=
  fun h => Bool.noConfusion ((factors_through_point_iff false true).mp h)

/-- And the selection of `true` and `true` does. -/
theorem factor_true_true : ∃ p : Unit → Bool, p () = true ∧ p () = true :=
  (factors_through_point_iff true true).mpr rfl

/-- A3 read as a predicate: non-factorization is metatheoretic inequality,
on every type. -/
theorem A3_is_ne {α : Type} (a b : α) :
    (¬ ∃ p : Unit → α, p () = a ∧ p () = b) ↔ a ≠ b :=
  not_congr (factors_through_point_iff a b)

end Textbook.U14

#print axioms Textbook.U14.factors_through_point_iff'
#print axioms Textbook.U14.point_map_constant
#print axioms Textbook.U14.no_factor_false_true
#print axioms Textbook.U14.factor_true_true
#print axioms Textbook.U14.A3_is_ne
#print axioms PrimDiff.factors_through_point_iff
"""

EXPECTED = {
    "Textbook.U14.factors_through_point_iff'": NONE,
    "Textbook.U14.point_map_constant": QUOT,
    "Textbook.U14.no_factor_false_true": NONE,
    "Textbook.U14.factor_true_true": NONE,
    "Textbook.U14.A3_is_ne": NONE,
    "PrimDiff.factors_through_point_iff": NONE,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U14"))
