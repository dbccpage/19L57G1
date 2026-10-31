"""Unit 60 check: kernel-check the book's Lean for Unit 60.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u60_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.LadderGeneral
import Derivation.BoundaryCancellation

namespace Textbook.U60
open LadderGeneral BoundaryCancellation

/-! ## Proof-defect probe on `LadderGeneral.d2_zero_dims_2_3_4`
Conjuncts 1 and 2 of `d2_zero_dims_2_3_4` test `coeffN e (pushN (bdN t))`
for `e ∈ facets t`, which is one dimension above the support of `pushN (bdN t)`.
Consequently both conjuncts remain `true` even when `bdN`/`pushN` are replaced
by the signless `bdNoSign`/`pushNoSign` (for which boundary cancellation is
false). Conjunct 3 steps down twice (`q ∈ facets [0,1,2,3,4]`, `t2 ∈ facets q`)
and genuinely tests codimension-two faces: it becomes `false` under `bdNoSign`. -/

theorem support_dim2_is_1verts :
    (pushN (bdN [0, 1, 2])).map (·.2) = [[2], [1], [2], [0], [1], [0]] := by
  decide

theorem conj1_vacuous_signless :
    ((combs 5 2).all fun t =>
      (facets t).all fun e => coeffN e (pushNoSign (bdNoSign t)) == 0) = true := by
  decide

theorem conj2_vacuous_signless :
    ((combs 5 3).all fun q =>
      (facets q).all fun t2 => coeffN t2 (pushNoSign (bdNoSign q)) == 0) = true := by
  decide

theorem repaired_dim2_signless_fails :
    ((combs 5 2).all fun t =>
      (facets t).all fun e => (facets e).all fun v =>
        coeffN v (pushNoSign (bdNoSign t)) == 0) = false := by
  decide

theorem repaired_dim2_signed_holds :
    ((combs 5 2).all fun t =>
      (facets t).all fun e => (facets e).all fun v =>
        coeffN v (pushN (bdN t)) == 0) = true := by
  decide

theorem repaired_dim3_signed_holds :
    ((combs 5 3).all fun q =>
      (facets q).all fun t => (facets t).all fun e =>
        coeffN e (pushN (bdN q)) == 0) = true := by
  decide

set_option maxRecDepth 4096 in
theorem conj3_signless_fails :
    ((facets [0, 1, 2, 3, 4]).all fun q =>
      (facets q).all fun t2 =>
        coeffN t2 (pushNoSign (bdNoSign [0, 1, 2, 3, 4])) == 0) = false := by
  decide

/-- Concrete pairing on `[0, 1, 2, 3]` for `(a, b) = (1, 3)`: deleting index 3
then 1 gives `[0, 2]`, as does deleting index 1 then `3 - 1 = 2`, with opposite
signs `sgn 3 * sgn 1 = 1` and `sgn 1 * sgn 2 = -1`. -/
theorem pairing_example_0123 :
    (([0, 1, 2, 3] : List Nat).eraseIdx 3).eraseIdx 1 = [0, 2] ∧
    (([0, 1, 2, 3] : List Nat).eraseIdx 1).eraseIdx 2 = [0, 2] ∧
    dterm [0, 1, 2, 3] [0, 2] 3 1 = 1 ∧
    dterm [0, 1, 2, 3] [0, 2] 1 2 = -1 ∧
    dterm [0, 1, 2, 3] [0, 2] 3 1 + dterm [0, 1, 2, 3] [0, 2] 1 2 = 0 := by
  refine ⟨rfl, rfl, rfl, rfl, rfl⟩

/-- Non-monotone injective renaming `[2, 0, 1]` breaks `ascB` yet still satisfies
`d2_zero_unrestricted` at every vertex. -/
theorem scrambled_triangle_cancels :
    ascB [2, 0, 1] = false ∧
    coeffN [0] (pushN (bdN [2, 0, 1])) = 0 ∧
    coeffN [1] (pushN (bdN [2, 0, 1])) = 0 ∧
    coeffN [2] (pushN (bdN [2, 0, 1])) = 0 := by
  refine ⟨rfl, ?_, ?_, ?_⟩
  · exact d2_zero_unrestricted [2, 0, 1] [0]
  · exact d2_zero_unrestricted [2, 0, 1] [1]
  · exact d2_zero_unrestricted [2, 0, 1] [2]

/-- Zero is coefficientwise: the unreduced list still has six terms. -/
theorem nonempty_chain_zero_coefficients :
    (pushN (bdN [0,1,2])).length = 6 ∧
    ∀ target, coeffN target (pushN (bdN [0,1,2])) = 0 :=
  ⟨rfl, d2_zero_unrestricted [0,1,2]⟩

end Textbook.U60

#print axioms Textbook.U60.support_dim2_is_1verts
#print axioms Textbook.U60.conj1_vacuous_signless
#print axioms Textbook.U60.conj2_vacuous_signless
#print axioms Textbook.U60.repaired_dim2_signless_fails
#print axioms Textbook.U60.repaired_dim2_signed_holds
#print axioms Textbook.U60.repaired_dim3_signed_holds
#print axioms Textbook.U60.conj3_signless_fails
#print axioms Textbook.U60.pairing_example_0123
#print axioms Textbook.U60.scrambled_triangle_cancels
#print axioms Textbook.U60.nonempty_chain_zero_coefficients
#print axioms LadderGeneral.uniform_guarded_filler
#print axioms LadderGeneral.shell_refuses_general
#print axioms LadderGeneral.shell_no_self_fill
#print axioms LadderGeneral.pseudo_cell_countermodel
#print axioms LadderGeneral.wf_empty
#print axioms LadderGeneral.wf_nreplay
#print axioms LadderGeneral.d4_demo
#print axioms LadderGeneral.d4_wf
#print axioms LadderGeneral.d4_guard_load_bearing
#print axioms LadderGeneral.d2_zero_dims_2_3_4
#print axioms BoundaryCancellation.tri_transpose
#print axioms BoundaryCancellation.eraseIdx_swap
#print axioms BoundaryCancellation.sgn_cancel
#print axioms BoundaryCancellation.coeff_rect
#print axioms BoundaryCancellation.dterm_cancel
#print axioms BoundaryCancellation.rect_zero
#print axioms BoundaryCancellation.d2_zero_unrestricted
#print axioms BoundaryCancellation.d2_zero_general
#print axioms BoundaryCancellation.d2_zero_replayed
#print axioms BoundaryCancellation.eraseIdx_inj_of_asc
#print axioms BoundaryCancellation.codim2_distinct
#print axioms BoundaryCancellation.ascB_map
#print axioms BoundaryCancellation.d2_zero_renamed
#print axioms BoundaryCancellation.signless_countermodel
#print axioms BoundaryCancellation.illformed_countermodel
"""

EXPECTED = {
    "Textbook.U60.support_dim2_is_1verts": NONE,
    "Textbook.U60.nonempty_chain_zero_coefficients": BOTH,
    "Textbook.U60.conj1_vacuous_signless": NONE,
    "Textbook.U60.conj2_vacuous_signless": NONE,
    "Textbook.U60.repaired_dim2_signless_fails": NONE,
    "Textbook.U60.repaired_dim2_signed_holds": NONE,
    "Textbook.U60.repaired_dim3_signed_holds": NONE,
    "Textbook.U60.conj3_signless_fails": NONE,
    "Textbook.U60.pairing_example_0123": NONE,
    "Textbook.U60.scrambled_triangle_cancels": BOTH,
    "LadderGeneral.uniform_guarded_filler": BOTH,
    "LadderGeneral.shell_refuses_general": BOTH,
    "LadderGeneral.shell_no_self_fill": BOTH,
    "LadderGeneral.pseudo_cell_countermodel": BOTH,
    "LadderGeneral.wf_empty": NONE,
    "LadderGeneral.wf_nreplay": BOTH,
    "LadderGeneral.d4_demo": BOTH,
    "LadderGeneral.d4_wf": BOTH,
    "LadderGeneral.d4_guard_load_bearing": BOTH,
    "LadderGeneral.d2_zero_dims_2_3_4": NONE,
    "BoundaryCancellation.tri_transpose": BOTH,
    "BoundaryCancellation.eraseIdx_swap": BOTH,
    "BoundaryCancellation.sgn_cancel": BOTH,
    "BoundaryCancellation.coeff_rect": BOTH,
    "BoundaryCancellation.dterm_cancel": BOTH,
    "BoundaryCancellation.rect_zero": BOTH,
    "BoundaryCancellation.d2_zero_unrestricted": BOTH,
    "BoundaryCancellation.d2_zero_general": BOTH,
    "BoundaryCancellation.d2_zero_replayed": BOTH,
    "BoundaryCancellation.eraseIdx_inj_of_asc": BOTH,
    "BoundaryCancellation.codim2_distinct": BOTH,
    "BoundaryCancellation.ascB_map": PROPEXT,
    "BoundaryCancellation.d2_zero_renamed": BOTH,
    "BoundaryCancellation.signless_countermodel": NONE,
    "BoundaryCancellation.illformed_countermodel": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U60"))
