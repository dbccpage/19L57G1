"""Unit 26 check: kernel-check the book's Lean for Unit 26.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u26_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Bridge

namespace Textbook.U26
open PrimDiff Bridge

/-- The extension the Genesis proof builds, named. -/
def withSelf {α : Type} (r : α → α → Prop) (a : α) : α → α → Prop :=
  fun x y => r x y ∨ (x = a ∧ y = a)

theorem withSelf_extends {α : Type} (r : α → α → Prop) (a : α) :
    ∀ x y, r x y → withSelf r a x y := fun _ _ h => Or.inl h

theorem withSelf_self {α : Type} (r : α → α → Prop) (a : α) :
    withSelf r a a a := Or.inr ⟨rfl, rfl⟩

theorem withSelf_not_irrefl {α : Type} (r : α → α → Prop) (a : α) :
    ¬ Irrefl (withSelf r a) := fun hi => hi a (withSelf_self r a)

/-- The theorem, re-proved from the named pieces. -/
theorem irrefl_law_not_entailed' {α : Type} (r : α → α → Prop) (a : α) :
    ∃ r' : α → α → Prop, (∀ x y, r x y → r' x y) ∧ ¬ Irrefl r' :=
  ⟨withSelf r a, withSelf_extends r a, withSelf_not_irrefl r a⟩

/-- On `D2`: the facts `{false r true}` are irreflexive as facts, and
one bare-signature extension of them is not. -/
theorem D2_facts_irrefl : Irrefl D2 := D2_irrefl
theorem D2_extension_not_irrefl : ¬ Irrefl (withSelf D2 false) :=
  withSelf_not_irrefl D2 false
theorem D2_extension_keeps_witness : withSelf D2 false false true :=
  Or.inl D2_witness

/-- No relation on an inhabited carrier has the law as a consequence of
its facts: whatever `r` is, some extension breaks it. Stated on `Bool`. -/
theorem no_facts_entail_law :
    ¬ ∃ r : Bool → Bool → Prop,
      ∀ r' : Bool → Bool → Prop, (∀ x y, r x y → r' x y) → Irrefl r' :=
  fun ⟨r, h⟩ =>
    (irrefl_law_not_entailed r false).elim fun r' ⟨hsub, hni⟩ => hni (h r' hsub)

/-- The contrast with Unit 24: from a witness *and the law* one gets
distinctness; from the witness alone one gets neither the law nor its
negation. -/
theorem law_is_extra {α : Type} (r : α → α → Prop) (a : α) :
    (Irrefl r → ∀ x y, r x y → x ≠ y) ∧
    (∃ r', (∀ x y, r x y → r' x y) ∧ ¬ Irrefl r') :=
  ⟨fun hi _ _ h => irrefl_witness_ne hi h, irrefl_law_not_entailed r a⟩

end Textbook.U26

#print axioms Textbook.U26.withSelf_extends
#print axioms Textbook.U26.withSelf_self
#print axioms Textbook.U26.withSelf_not_irrefl
#print axioms Textbook.U26.irrefl_law_not_entailed'
#print axioms Textbook.U26.D2_facts_irrefl
#print axioms Textbook.U26.D2_extension_not_irrefl
#print axioms Textbook.U26.D2_extension_keeps_witness
#print axioms Textbook.U26.no_facts_entail_law
#print axioms Textbook.U26.law_is_extra
#print axioms Bridge.irrefl_law_not_entailed
"""

EXPECTED = {
    "Textbook.U26.withSelf_extends": NONE,
    "Textbook.U26.withSelf_self": NONE,
    "Textbook.U26.withSelf_not_irrefl": NONE,
    "Textbook.U26.irrefl_law_not_entailed'": NONE,
    "Textbook.U26.D2_facts_irrefl": NONE,
    "Textbook.U26.D2_extension_not_irrefl": NONE,
    "Textbook.U26.D2_extension_keeps_witness": NONE,
    "Textbook.U26.no_facts_entail_law": NONE,
    "Textbook.U26.law_is_extra": NONE,
    "Bridge.irrefl_law_not_entailed": NONE,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U26"))
