"""Unit 15 check: kernel-check the book's Lean for Unit 15.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u15_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.PrimDiff

namespace Textbook.U15
open PrimDiff

/-- The relation that asserts nothing, on any carrier. -/
def emptyRel (α : Type) : α → α → Prop := fun _ _ => False

/-- The theorem, re-proved with every step named. -/
theorem meta_diff_without_assertion' :
    ∃ r : Bool → Bool → Prop, ¬ r false true ∧ false ≠ true :=
  ⟨emptyRel Bool,
   -- ¬ emptyRel Bool false true is ¬ False, proved by the identity
   fun h => h,
   -- false ≠ true: the two constructors of Bool are distinct
   Bool.noConfusion⟩

/-- The same on any type, for any two metatheoretically distinct points. -/
theorem meta_diff_without_assertion_any {α : Type} (a b : α) (hne : a ≠ b) :
    ∃ r : α → α → Prop, ¬ r a b ∧ a ≠ b :=
  ⟨emptyRel α, fun h => h, hne⟩

/-- The empty relation is irreflexive: the law of A1i can be in force while
nothing is asserted. The law alone asserts nothing. -/
theorem emptyRel_irrefl (α : Type) : Irrefl (emptyRel α) :=
  fun _ h => h

/-- The contrast: `D2` is a relation on `Bool` that does assert the pair. -/
theorem D2_asserts : D2 false true := ⟨rfl, rfl⟩

/-- A3 holds and A1 fails for the empty relation at (false, true); A1 holds
for `D2` at the same pair. Same carrier, same points, different relation. -/
theorem same_points_different_relations :
    (¬ emptyRel Bool false true) ∧ D2 false true ∧ false ≠ true :=
  ⟨fun h => h, D2_asserts, Bool.noConfusion⟩

end Textbook.U15

#print axioms Textbook.U15.meta_diff_without_assertion'
#print axioms Textbook.U15.meta_diff_without_assertion_any
#print axioms Textbook.U15.emptyRel_irrefl
#print axioms Textbook.U15.D2_asserts
#print axioms Textbook.U15.same_points_different_relations
#print axioms PrimDiff.meta_diff_without_assertion
#print axioms PrimDiff.D2
"""

EXPECTED = {
    "Textbook.U15.meta_diff_without_assertion'": NONE,
    "Textbook.U15.meta_diff_without_assertion_any": NONE,
    "Textbook.U15.emptyRel_irrefl": NONE,
    "Textbook.U15.D2_asserts": NONE,
    "Textbook.U15.same_points_different_relations": NONE,
    "PrimDiff.meta_diff_without_assertion": NONE,
    "PrimDiff.D2": NONE,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U15"))
