"""Unit 08 check: kernel-check the book's Lean for Unit 08.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u08_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Basic

namespace Textbook.U08
open Derivation

/-- Two data, one unary form, no instances, no rules. -/
def two_one : Regime := ⟨2, [1], [], [], []⟩

/-- The unary context with its one slot a hole is well formed here. -/
theorem ctx_hole_wf : wfCtx two_one ⟨0, [none]⟩ := by decide

/-- A slot tuple with no hole is an instance, not a context. -/
theorem no_hole_not_ctx : ¬ wfCtx two_one ⟨0, [some 0]⟩ := by decide

/-- A slot count that does not match the arity is not a context. -/
theorem wrong_arity_not_ctx : ¬ wfCtx two_one ⟨0, [none, none]⟩ := by decide

/-- A form that is not admitted gives no context. -/
theorem no_form_not_ctx : ¬ wfCtx two_one ⟨1, [none]⟩ := by decide

/-- A filled slot must name an admitted datum. -/
theorem bad_datum_not_ctx : ¬ wfCtx ⟨2, [2], [], [], []⟩ ⟨0, [none, some 5]⟩ := by decide

/-- Plugging fills every hole with the same datum and leaves filled slots. -/
theorem plug_example : plug ⟨0, [none, some 1, none]⟩ 0 = (0, [0, 1, 0]) := rfl

/-- Derivable by an admitted instance. -/
theorem derivable_by_inst : derivable ⟨2, [1], [(0, [1])], [], []⟩ (0, [1]) := by decide

/-- Not derivable: the instance is absent and there is no rule. -/
theorem not_derivable : ¬ derivable ⟨2, [1], [(0, [1])], [], []⟩ (0, [0]) := by decide

/-- Derivable by a uniform rule, whatever the arguments. -/
theorem derivable_by_rule : derivable ⟨2, [1], [], [0], []⟩ (0, [7]) := by decide

/-- Two data that one instance tells apart: the witness context. -/
theorem sep_example : separable ⟨2, [1], [(0, [1])], [], []⟩ 0 1 :=
  ⟨⟨0, [none]⟩, by decide, by decide⟩

/-- With an instance on both, the unary context no longer separates them. -/
theorem both_marked_ctx_agrees :
    derivable ⟨2, [1], [(0, [0]), (0, [1])], [], []⟩ (plug ⟨0, [none]⟩ 0)
      ↔ derivable ⟨2, [1], [(0, [0]), (0, [1])], [], []⟩ (plug ⟨0, [none]⟩ 1) := by
  decide

end Textbook.U08

#print axioms Textbook.U08.ctx_hole_wf
#print axioms Textbook.U08.no_hole_not_ctx
#print axioms Textbook.U08.wrong_arity_not_ctx
#print axioms Textbook.U08.no_form_not_ctx
#print axioms Textbook.U08.bad_datum_not_ctx
#print axioms Textbook.U08.plug_example
#print axioms Textbook.U08.derivable_by_inst
#print axioms Textbook.U08.not_derivable
#print axioms Textbook.U08.derivable_by_rule
#print axioms Textbook.U08.sep_example
#print axioms Textbook.U08.both_marked_ctx_agrees
#print axioms Derivation.collapsed
#print axioms Derivation.separable
#print axioms Derivation.wfCtx
"""

EXPECTED = {
    "Textbook.U08.plug_example": NONE,
    "Derivation.collapsed": PROPEXT,
    "Derivation.separable": PROPEXT,
    "Derivation.wfCtx": PROPEXT,
}
for _n in ("ctx_hole_wf", "no_hole_not_ctx", "wrong_arity_not_ctx", "no_form_not_ctx",
           "bad_datum_not_ctx", "derivable_by_inst", "not_derivable",
           "derivable_by_rule", "sep_example", "both_marked_ctx_agrees"):
    EXPECTED[f"Textbook.U08.{_n}"] = BOTH

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U08"))
