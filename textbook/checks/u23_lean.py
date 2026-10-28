"""Unit 23 check: kernel-check the book's Lean for Unit 23.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u23_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.PrimDiff

namespace Textbook.U23
open PrimDiff

/-- The self-difference, named. -/
def selfDiff : Unit → Unit → Prop := fun _ _ => True

/-- It is a witnessed structure: the pair `((), ())` is asserted. -/
theorem selfDiff_witness : selfDiff () () := trivial

/-- Its two witnesses are the same point: assertion without distinctness. -/
theorem selfDiff_same : (() : Unit) = () := rfl

/-- It is not irreflexive. -/
theorem selfDiff_not_irrefl : ¬ Irrefl selfDiff := fun h => h () trivial

/-- It is symmetric. -/
theorem selfDiff_symm : ∀ x y, selfDiff x y → selfDiff y x := fun _ _ h => h

/-- A1 does not imply A3 (the schema refuted, with the carrier, relation
and pair exhibited). -/
theorem A1_not_A3 :
    ¬ ∀ (α : Type) (r : α → α → Prop) (a b : α), r a b → a ≠ b :=
  fun h => h Unit selfDiff () () trivial rfl

/-- Symmetry does not rescue it. -/
theorem symm_A1_not_A3 :
    ¬ ∀ (α : Type) (r : α → α → Prop), (∀ x y, r x y → r y x) →
      ∀ a b, r a b → a ≠ b :=
  fun h => h Unit selfDiff selfDiff_symm () () trivial rfl

/-- Any relation with a self-pair refutes irreflexivity, on any carrier. -/
theorem not_irrefl_of_self {α : Type} {r : α → α → Prop} {a : α}
    (h : r a a) : ¬ Irrefl r := fun hi => hi a h

/-- On `Bool` too: a self-difference at `true` is a structure. -/
theorem selfdiff_on_Bool : ∃ r : Bool → Bool → Prop, r true true :=
  ⟨fun x y => x = true ∧ y = true, ⟨rfl, rfl⟩⟩

/-- The Genesis countermodel re-proved with the witness named. -/
theorem selfdiff_consistent' : ∃ r : Unit → Unit → Prop, r () () :=
  ⟨selfDiff, selfDiff_witness⟩

end Textbook.U23

#print axioms Textbook.U23.selfDiff_witness
#print axioms Textbook.U23.selfDiff_same
#print axioms Textbook.U23.selfDiff_not_irrefl
#print axioms Textbook.U23.selfDiff_symm
#print axioms Textbook.U23.A1_not_A3
#print axioms Textbook.U23.symm_A1_not_A3
#print axioms Textbook.U23.not_irrefl_of_self
#print axioms Textbook.U23.selfdiff_on_Bool
#print axioms Textbook.U23.selfdiff_consistent'
#print axioms PrimDiff.selfdiff_consistent
#print axioms PrimDiff.symm_selfdiff_consistent
"""

EXPECTED = {
    "Textbook.U23.selfDiff_witness": NONE,
    "Textbook.U23.selfDiff_same": NONE,
    "Textbook.U23.selfDiff_not_irrefl": NONE,
    "Textbook.U23.selfDiff_symm": NONE,
    "Textbook.U23.A1_not_A3": NONE,
    "Textbook.U23.symm_A1_not_A3": NONE,
    "Textbook.U23.not_irrefl_of_self": NONE,
    "Textbook.U23.selfdiff_on_Bool": NONE,
    "Textbook.U23.selfdiff_consistent'": NONE,
    "PrimDiff.selfdiff_consistent": NONE,
    "PrimDiff.symm_selfdiff_consistent": NONE,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U23"))
