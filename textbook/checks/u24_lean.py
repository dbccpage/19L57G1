"""Unit 24 check: kernel-check the book's Lean for Unit 24.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u24_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.PrimDiff

namespace Textbook.U24
open PrimDiff

/-- The theorem, re-proved with every step named. -/
theorem irrefl_witness_ne' {α : Type} {r : α → α → Prop} (hi : Irrefl r)
    {a b : α} (h : r a b) : a ≠ b := by
  intro he
  -- he : a = b.  Rewrite the witness along it: r b b.
  have hbb : r b b := he ▸ h
  -- Irreflexivity forbids r b b.
  exact hi b hbb

/-- The converse: if every witnessed pair is distinct, the relation is
irreflexive. So the conditional is exact. -/
theorem irrefl_of_witness_ne {α : Type} {r : α → α → Prop}
    (h : ∀ a b, r a b → a ≠ b) : Irrefl r :=
  fun x hx => h x x hx rfl

theorem irrefl_iff_witness_ne {α : Type} (r : α → α → Prop) :
    Irrefl r ↔ ∀ a b, r a b → a ≠ b :=
  ⟨fun hi _ _ h => irrefl_witness_ne hi h, irrefl_of_witness_ne⟩

/-- Applied to the oriented two-element difference. -/
theorem D2_endpoints_ne : false ≠ true := irrefl_witness_ne D2_irrefl D2_witness

/-- Applied to the symmetric one. -/
theorem S2_endpoints_ne : false ≠ true :=
  irrefl_witness_ne S2_irrefl (Or.inl D2_witness)

/-- The hypothesis is necessary (Unit 23's countermodel, in this form). -/
theorem hypothesis_needed :
    ∃ (r : Unit → Unit → Prop) (a b : Unit), r a b ∧ a = b :=
  ⟨fun _ _ => True, (), (), trivial, rfl⟩

/-- The conclusion is metatheoretic: it is a statement about `=` on the
carrier, which the relation `r` does not mention. -/
theorem conclusion_is_meta {α : Type} {r : α → α → Prop} (hi : Irrefl r)
    {a b : α} (h : r a b) : ¬ (a = b) := irrefl_witness_ne hi h

/-- A particular unequal pair needs no global irreflexivity assumption:
another asserted pair in the same relation can be a self-pair. -/
def mixed (x y : Bool) : Prop :=
  (x = false ∧ y = true) ∨ (x = true ∧ y = true)

theorem mixed_specific_pair :
    mixed false true ∧ false ≠ true ∧ ¬ Irrefl mixed :=
  ⟨Or.inl ⟨rfl, rfl⟩, Bool.noConfusion,
   fun hi => hi true (Or.inr ⟨rfl, rfl⟩)⟩

end Textbook.U24

#print axioms Textbook.U24.irrefl_witness_ne'
#print axioms Textbook.U24.irrefl_of_witness_ne
#print axioms Textbook.U24.irrefl_iff_witness_ne
#print axioms Textbook.U24.D2_endpoints_ne
#print axioms Textbook.U24.S2_endpoints_ne
#print axioms Textbook.U24.hypothesis_needed
#print axioms Textbook.U24.conclusion_is_meta
#print axioms Textbook.U24.mixed_specific_pair
#print axioms PrimDiff.irrefl_witness_ne
#print axioms PrimDiff.D2_irrefl
#print axioms PrimDiff.D2_witness
"""

EXPECTED = {
    "Textbook.U24.irrefl_witness_ne'": NONE,
    "Textbook.U24.irrefl_of_witness_ne": NONE,
    "Textbook.U24.irrefl_iff_witness_ne": NONE,
    "Textbook.U24.D2_endpoints_ne": NONE,
    "Textbook.U24.S2_endpoints_ne": NONE,
    "Textbook.U24.hypothesis_needed": NONE,
    "Textbook.U24.conclusion_is_meta": NONE,
    "Textbook.U24.mixed_specific_pair": NONE,
    "PrimDiff.irrefl_witness_ne": NONE,
    "PrimDiff.D2_irrefl": NONE,
    "PrimDiff.D2_witness": NONE,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U24"))
