"""Unit 31 check: kernel-check the book's Lean for Unit 31.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u31_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.TransitionTransport

namespace Textbook.U31
open Derivation

/-- The renaming carries the unmarked pair to the marked pair and back. -/
theorem mapReq_swap_01 : mapReq regSwap.f (0, 1) = (2, 3) := by decide
theorem mapReq_swap_23 : mapReq regSwap.f (2, 3) = (0, 1) := by decide

/-- The renamed regression regime: the marks move to data 0 and 1. -/
theorem renamed_regRegime :
    renameRegimeR regSwap.f regRegime = ⟨4, [1], [(0, [0]), (0, [1])], [], []⟩ := by
  decide

/-- `mapReq` forgets the order of a pair. -/
theorem mapReq_comm (f : Nat → Nat) (i j : Nat) : mapReq f (i, j) = mapReq f (j, i) := by
  simp [mapReq, Nat.min_comm, Nat.max_comm]

/-- So the action is not injective on regimes with a disordered demand:
two different regimes have one image. -/
theorem not_injective_on_disordered :
    renameRegimeR regSwap.f ⟨4, [1], [], [], [(0, 1)]⟩
      = renameRegimeR regSwap.f ⟨4, [1], [], [], [(1, 0)]⟩
    ∧ (⟨4, [1], [], [], [(0, 1)]⟩ : Regime) ≠ ⟨4, [1], [], [], [(1, 0)]⟩ :=
  ⟨by decide, by decide⟩

/-- Padding: below 4 the renaming acts, at 4 and above it is the identity. -/
theorem padF_values : padF 4 regSwap.f 0 = 2 ∧ padF 4 regSwap.f 4 = 4 ∧ padF 4 regSwap.f 7 = 7 := by
  decide

/-- The other collapsed pair of the regression regime. -/
theorem reg_collapsed_23 : collapsed regRegime 2 3 := by
  intro c hc
  rw [one_unary_form_ctx_char regRegime rfl c] at hc
  subst hc
  decide

/-- Genesis's transport at this renaming: collapse of (0, 1) in the original
is collapse of (2, 3) in the renamed regime. -/
theorem swap_carries_collapse :
    collapsed (renameRegimeR regSwap.f regRegime) 2 3 ↔ collapsed regRegime 0 1 :=
  collapsed_renameR regSwap regRegime rfl 0 1

/-- In the renamed regime (0, 1) is the MARKED pair and (0, 2) is separated:
the same index pair, the other role. -/
theorem renamed_separable_02 : separable (renameRegimeR regSwap.f regRegime) 0 2 :=
  ⟨⟨0, [none]⟩, by decide, by decide⟩

/-- In the original, (0, 2) is separated too, but there 0 is the unmarked
datum: the one-hole context answers no on 0 and yes on 2. -/
theorem reg_separable_02 : separable regRegime 0 2 :=
  ⟨⟨0, [none]⟩, by decide, by decide⟩

end Textbook.U31

#print axioms Textbook.U31.mapReq_swap_01
#print axioms Textbook.U31.renamed_regRegime
#print axioms Textbook.U31.mapReq_comm
#print axioms Textbook.U31.not_injective_on_disordered
#print axioms Textbook.U31.padF_values
#print axioms Textbook.U31.reg_collapsed_23
#print axioms Textbook.U31.swap_carries_collapse
#print axioms Textbook.U31.renamed_separable_02
#print axioms Textbook.U31.reg_separable_02
#print axioms Derivation.validResponse_rename
#print axioms Derivation.transStep_rename_fwd
#print axioms Derivation.transStep_image_total
#print axioms Derivation.least_pair_selection_not_congruent
"""

EXPECTED = {
    "Textbook.U31.mapReq_swap_01": NONE,
    "Textbook.U31.renamed_regRegime": NONE,
    "Textbook.U31.mapReq_comm": PROPEXT,
    "Textbook.U31.not_injective_on_disordered": NONE,
    "Textbook.U31.padF_values": NONE,
    "Textbook.U31.reg_collapsed_23": BOTH,
    "Textbook.U31.swap_carries_collapse": BOTH,
    "Textbook.U31.renamed_separable_02": BOTH,
    "Textbook.U31.reg_separable_02": BOTH,
    "Derivation.validResponse_rename": BOTH,
    "Derivation.transStep_rename_fwd": BOTH,
    "Derivation.transStep_image_total": BOTH,
    "Derivation.least_pair_selection_not_congruent": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U31"))
