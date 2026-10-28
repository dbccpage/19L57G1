"""Unit 19 check: kernel-check the book's Lean for Unit 19.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u19_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Minimality

namespace Textbook.U19
open Derivation

/-- The witness Genesis names: the hole in the first slot, datum 1 in
the second. -/
theorem BL_witness_wf : wfCtx BL ⟨0, [none, some 1]⟩ := by decide

/-- Plugged with 0 it is the admitted link; plugged with 1 it is not. -/
theorem BL_plug0 : plug ⟨0, [none, some 1]⟩ 0 = (0, [0, 1]) := rfl
theorem BL_plug1 : plug ⟨0, [none, some 1]⟩ 1 = (0, [1, 1]) := rfl
theorem BL_derivable_01 : derivable BL (0, [0, 1]) := by decide
theorem BL_not_derivable_11 : ¬ derivable BL (0, [1, 1]) := by decide

/-- The theorem, assembled from those four facts. -/
theorem BL_separable' : separable BL 0 1 :=
  ⟨⟨0, [none, some 1]⟩, BL_witness_wf,
   fun h => BL_not_derivable_11 (h.mp BL_derivable_01)⟩

/-- A second witness: the hole in the other slot. -/
theorem BL_second_witness : separable BL 0 1 :=
  ⟨⟨0, [some 0, none]⟩, by decide, by decide⟩

/-- Not every context is a witness: with datum 0 in the second slot the
plugging is derivable for neither datum. -/
theorem BL_non_witness :
    ¬ derivable BL (plug ⟨0, [none, some 0]⟩ 0) ∧
    ¬ derivable BL (plug ⟨0, [none, some 0]⟩ 1) := by decide

/-- `BL` is the result of applying the link delta to `R2L`. -/
theorem deltaBL_lands : applyDelta R2L deltaBL = some BL := by decide

/-- And that makes the delta a valid response (Genesis's `deltaBL_valid`,
re-assembled). -/
theorem deltaBL_valid' : validResponse R2L 0 1 deltaBL :=
  validResponse_R2L deltaBL BL deltaBL_lands BL_separable'

/-- `BL` is well formed. -/
theorem BL_wf : BL.wf := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [BL]

end Textbook.U19

#print axioms Textbook.U19.BL_witness_wf
#print axioms Textbook.U19.BL_plug0
#print axioms Textbook.U19.BL_derivable_01
#print axioms Textbook.U19.BL_not_derivable_11
#print axioms Textbook.U19.BL_separable'
#print axioms Textbook.U19.BL_second_witness
#print axioms Textbook.U19.BL_non_witness
#print axioms Textbook.U19.deltaBL_lands
#print axioms Textbook.U19.deltaBL_valid'
#print axioms Textbook.U19.BL_wf
#print axioms Derivation.BL_separable
#print axioms Derivation.deltaBL_valid
#print axioms Derivation.validResponse_R2L
"""

EXPECTED = {
    "Textbook.U19.BL_witness_wf": BOTH,
    "Textbook.U19.BL_plug0": NONE,
    "Textbook.U19.BL_derivable_01": BOTH,
    "Textbook.U19.BL_not_derivable_11": BOTH,
    "Textbook.U19.BL_separable'": BOTH,
    "Textbook.U19.BL_second_witness": BOTH,
    "Textbook.U19.BL_non_witness": BOTH,
    "Textbook.U19.deltaBL_lands": PROPEXT,
    "Textbook.U19.deltaBL_valid'": BOTH,
    "Textbook.U19.BL_wf": BOTH,
    "Derivation.BL_separable": BOTH,
    "Derivation.deltaBL_valid": BOTH,
    "Derivation.validResponse_R2L": PROPEXT,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U19"))
