"""Unit 30 check: kernel-check the book's Lean for Unit 30.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u30_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Mention
import Derivation.Inertia

namespace Textbook.U30
open Derivation

/-- Three data, one unary form, nothing asserted. -/
def three : Regime := ⟨3, [1], [], [], []⟩

/-- The same with a mark on datum 2. -/
def marked2 : Regime := ⟨3, [1], [(0, [2])], [], []⟩

theorem marked2_is_append :
    marked2 = { three with insts := three.insts ++ [(0, [2])] } := rfl

/-- R3 at work: the mark mentions neither 0 nor 1, so (0, 1) stays collapsed. -/
theorem marked2_collapsed_01 : collapsed marked2 0 1 := by
  rw [marked2_is_append,
    collapsed_append_unmentioning three [(0, [2])] 0 1 (by decide) (by decide)]
  exact collapsed_of_no_insts three rfl 0 1

/-- The mark does separate datum 2 from datum 0: R3 is about the pair it names. -/
theorem marked2_separable_02 : separable marked2 0 2 :=
  ⟨⟨0, [none]⟩, by decide, by decide⟩

/-- The hypothesis is needed: an instance mentioning 0 separates (0, 1). -/
theorem mentioning_separates :
    separable { three with insts := three.insts ++ [(0, [0])] } 0 1 :=
  ⟨⟨0, [none]⟩, by decide, by decide⟩

/-- R2 at work: a fresh binary form, used by no instance and no rule. -/
theorem fresh_form_keeps :
    collapsed { marked2 with forms := marked2.forms ++ [2] } 0 1 ↔ collapsed marked2 0 1 :=
  collapsed_fresh_form marked2 0 1 2 (by decide) (by decide)

theorem fresh_form_collapsed_01 : collapsed { marked2 with forms := marked2.forms ++ [2] } 0 1 :=
  fresh_form_keeps.mpr marked2_collapsed_01

/-- Every plug mentions its datum, at the one-hole context. -/
theorem plug_mentions_two : (2 : Nat) ∈ (plug ⟨0, [none]⟩ 2).2 :=
  mem_plug_of_hole (List.mem_singleton.mpr rfl) 2

/-- And a context with no hole is not well formed, so the lemma's
hypothesis is never missing for a well-formed context. -/
theorem wf_has_hole (r : Regime) (c : Ctx) (h : wfCtx r c) : none ∈ c.slots :=
  h.2.2.1

end Textbook.U30

#print axioms Textbook.U30.marked2_collapsed_01
#print axioms Textbook.U30.marked2_separable_02
#print axioms Textbook.U30.mentioning_separates
#print axioms Textbook.U30.fresh_form_collapsed_01
#print axioms Textbook.U30.plug_mentions_two
#print axioms Textbook.U30.wf_has_hole
#print axioms Derivation.mem_plug_of_hole
#print axioms Derivation.collapsed_append_unmentioning
#print axioms Derivation.collapsed_fresh_datum
#print axioms Derivation.collapsed_fresh_form
"""

EXPECTED = {
    "Textbook.U30.marked2_collapsed_01": BOTH,
    "Textbook.U30.marked2_separable_02": BOTH,
    "Textbook.U30.mentioning_separates": BOTH,
    "Textbook.U30.fresh_form_collapsed_01": BOTH,
    "Textbook.U30.plug_mentions_two": BOTH,
    "Textbook.U30.wf_has_hole": PROPEXT,
    "Derivation.mem_plug_of_hole": BOTH,
    "Derivation.collapsed_append_unmentioning": BOTH,
    "Derivation.collapsed_fresh_datum": BOTH,
    "Derivation.collapsed_fresh_form": PROPEXT,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U30"))
