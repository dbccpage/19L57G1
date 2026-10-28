"""Unit 20 check: kernel-check the book's Lean for Unit 20.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u20_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Minimality

namespace Textbook.U20
open Derivation

/-- Genesis's witness for the self-loop: the hole first, datum 0 second. -/
theorem BD_witness_wf : wfCtx BD ⟨0, [none, some 0]⟩ := by decide
theorem BD_plug0 : plug ⟨0, [none, some 0]⟩ 0 = (0, [0, 0]) := rfl
theorem BD_plug1 : plug ⟨0, [none, some 0]⟩ 1 = (0, [1, 0]) := rfl
theorem BD_derivable_00 : derivable BD (0, [0, 0]) := by decide
theorem BD_not_derivable_10 : ¬ derivable BD (0, [1, 0]) := by decide

theorem BD_separable' : separable BD 0 1 :=
  ⟨⟨0, [none, some 0]⟩, BD_witness_wf,
   fun h => BD_not_derivable_10 (h.mp BD_derivable_00)⟩

/-- The context that worked for the link does not work here: with datum
1 in the second slot neither plugging is derivable. -/
theorem BD_link_context_fails :
    ¬ derivable BD (plug ⟨0, [none, some 1]⟩ 0) ∧
    ¬ derivable BD (plug ⟨0, [none, some 1]⟩ 1) := by decide

/-- The context with two holes is also a witness: plugging both holes
with 0 gives the loop, with 1 gives nothing. -/
theorem BD_two_holes : separable BD 0 1 :=
  ⟨⟨0, [none, none]⟩, by decide, by decide⟩

/-- The two-hole context does not separate the link: neither plugging is
the admitted instance (0, [0, 1]). -/
theorem BL_two_holes_fail :
    ¬ derivable BL (plug ⟨0, [none, none]⟩ 0) ∧
    ¬ derivable BL (plug ⟨0, [none, none]⟩ 1) := by decide

/-- The self-loop delta lands on `BD` and is a valid response. -/
theorem deltaBD_lands : applyDelta R2L deltaBD = some BD := by decide
theorem deltaBD_valid' : validResponse R2L 0 1 deltaBD :=
  validResponse_R2L deltaBD BD deltaBD_lands BD_separable'

/-- The link and the self-loop are different results (Genesis). -/
theorem link_not_loop : Iso BL BD → False := BL_not_iso_BD

end Textbook.U20

#print axioms Textbook.U20.BD_witness_wf
#print axioms Textbook.U20.BD_derivable_00
#print axioms Textbook.U20.BD_not_derivable_10
#print axioms Textbook.U20.BD_separable'
#print axioms Textbook.U20.BD_link_context_fails
#print axioms Textbook.U20.BD_two_holes
#print axioms Textbook.U20.BL_two_holes_fail
#print axioms Textbook.U20.deltaBD_lands
#print axioms Textbook.U20.deltaBD_valid'
#print axioms Textbook.U20.link_not_loop
#print axioms Derivation.BD_separable
#print axioms Derivation.deltaBD_valid
#print axioms Derivation.BL_not_iso_BD
"""

EXPECTED = {
    "Textbook.U20.BD_witness_wf": BOTH,
    "Textbook.U20.BD_derivable_00": BOTH,
    "Textbook.U20.BD_not_derivable_10": BOTH,
    "Textbook.U20.BD_separable'": BOTH,
    "Textbook.U20.BD_link_context_fails": BOTH,
    "Textbook.U20.BD_two_holes": BOTH,
    "Textbook.U20.BL_two_holes_fail": BOTH,
    "Textbook.U20.deltaBD_lands": PROPEXT,
    "Textbook.U20.deltaBD_valid'": BOTH,
    "Textbook.U20.link_not_loop": BOTH,
    "Derivation.BD_separable": BOTH,
    "Derivation.deltaBD_valid": BOTH,
    "Derivation.BL_not_iso_BD": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U20"))
