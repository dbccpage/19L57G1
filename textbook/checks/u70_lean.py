"""Unit 70 check: kernel-check the book's Lean for Unit 70 (`PresentationNaturality`).

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u70_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.PresentationNaturality

namespace Textbook.U70
open DiffInterface ContactKernel PresentationNaturality

/-- Audit probe: over the one-object family `autoFamily O F`, existence of a
natural section is equivalent to existence of an admissible pair fixed by
`F.mapPair` (`fixed_pair_of_natural_section` and constant-section converse). -/
theorem natural_section_iff_fixed_pair {X R : Type}
    (O : DiffObs X R) (F : PresIso O O) :
    (∃ s : Sec (autoFamily O F), IsNatural (autoFamily O F) s) ↔
      (∃ p : NonZeroPair O, F.mapPair p = p) := by
  constructor
  · rintro ⟨s, hs⟩
    exact fixed_pair_of_natural_section O F s hs
  · rintro ⟨p, hp⟩
    exact ⟨fun _ => p, fun _ => hp⟩

/-- Audit probe: in `twoFamilyNeg` and `twoFamilyPos`, the cross-object arrow
types `twoHom .bool .four` and `twoHom .four .bool` are `Empty` by `rfl`. -/
theorem twoHom_cross_empty :
    twoHom .bool .four = Empty ∧ twoHom .four .bool = Empty :=
  ⟨rfl, rfl⟩

/-- On `Card4`, the admissible pair `(e1, e2)` is moved by `twIso.mapPair`
(unlike `card4Pair = (e3, e4)`, which is fixed). -/
def card4MovedPair : NonZeroPair card4Obs :=
  ⟨(.e1, .e2), fun h => Card4.noConfusion (h : Card4.e1 = Card4.e2)⟩

theorem twIso_moves_e1_e2 :
    twIso.mapPair card4MovedPair ≠ card4MovedPair := by
  intro h
  have h1 : Card4.e2 = Card4.e1 :=
    congrArg Prod.fst (congrArg Subtype.val h)
  exact Card4.noConfusion h1

/-- On `Card4`, the transposed pair `(e4, e3)` is a second admissible pair
fixed by `twIso.mapPair`, giving a second natural section over
`autoFamily card4Obs twIso`. -/
def card4PairSwap : NonZeroPair card4Obs :=
  ⟨(.e4, .e3), fun h => Card4.noConfusion (h : Card4.e4 = Card4.e3)⟩

theorem twIso_fixes_card4PairSwap :
    twIso.mapPair card4PairSwap = card4PairSwap := by
  apply Subtype.ext
  rfl

end Textbook.U70

#print axioms Textbook.U70.natural_section_iff_fixed_pair
#print axioms Textbook.U70.twoHom_cross_empty
#print axioms Textbook.U70.twIso_moves_e1_e2
#print axioms Textbook.U70.twIso_fixes_card4PairSwap
#print axioms PresentationNaturality.Bij.fwd_injective
#print axioms PresentationNaturality.zeroRel_transport
#print axioms PresentationNaturality.refl_car
#print axioms PresentationNaturality.trans_car
#print axioms PresentationNaturality.symm_car_left
#print axioms PresentationNaturality.symm_car_right
#print axioms PresentationNaturality.symm_symm_car
#print axioms PresentationNaturality.viable_transport
#print axioms PresentationNaturality.no_natural_section_of_fixed_point_free
#print axioms PresentationNaturality.fixed_pair_of_natural_section
#print axioms PresentationNaturality.negIso_fixed_point_free
#print axioms PresentationNaturality.no_natural_section_boolEq
#print axioms PresentationNaturality.selection_is_possible_naturality_is_not
#print axioms PresentationNaturality.tw_involutive
#print axioms PresentationNaturality.card4_natural_section
#print axioms PresentationNaturality.card4_has_natural_section
#print axioms PresentationNaturality.naturality_separates_presentations
#print axioms PresentationNaturality.bool_obstruction_and_sealed_selector
#print axioms PresentationNaturality.mapPair_refl
#print axioms PresentationNaturality.mapPair_trans
#print axioms PresentationNaturality.mapPair_symm_left
#print axioms PresentationNaturality.mapPair_symm_right
#print axioms PresentationNaturality.no_natural_section_of_endo
#print axioms PresentationNaturality.hAuto_iff_auto
#print axioms PresentationNaturality.twIso_fixes_card4Pair
#print axioms PresentationNaturality.twoFamilyNeg_no_section
#print axioms PresentationNaturality.twoFamilyPos_natural
#print axioms PresentationNaturality.twoFamilyPos_has_section
#print axioms PresentationNaturality.heterogeneous_naturality_separates
"""

EXPECTED = {
    "Textbook.U70.natural_section_iff_fixed_pair": NONE,
    "Textbook.U70.twoHom_cross_empty": NONE,
    "Textbook.U70.twIso_moves_e1_e2": NONE,
    "Textbook.U70.twIso_fixes_card4PairSwap": NONE,
    "PresentationNaturality.Bij.fwd_injective": NONE,
    "PresentationNaturality.zeroRel_transport": NONE,
    "PresentationNaturality.refl_car": NONE,
    "PresentationNaturality.trans_car": NONE,
    "PresentationNaturality.symm_car_left": NONE,
    "PresentationNaturality.symm_car_right": NONE,
    "PresentationNaturality.symm_symm_car": NONE,
    "PresentationNaturality.viable_transport": NONE,
    "PresentationNaturality.no_natural_section_of_fixed_point_free": NONE,
    "PresentationNaturality.fixed_pair_of_natural_section": NONE,
    "PresentationNaturality.negIso_fixed_point_free": NONE,
    "PresentationNaturality.no_natural_section_boolEq": NONE,
    "PresentationNaturality.selection_is_possible_naturality_is_not": NONE,
    "PresentationNaturality.tw_involutive": NONE,
    "PresentationNaturality.card4_natural_section": NONE,
    "PresentationNaturality.card4_has_natural_section": NONE,
    "PresentationNaturality.naturality_separates_presentations": NONE,
    "PresentationNaturality.bool_obstruction_and_sealed_selector": QUOT,
    "PresentationNaturality.mapPair_refl": NONE,
    "PresentationNaturality.mapPair_trans": NONE,
    "PresentationNaturality.mapPair_symm_left": NONE,
    "PresentationNaturality.mapPair_symm_right": NONE,
    "PresentationNaturality.no_natural_section_of_endo": NONE,
    "PresentationNaturality.hAuto_iff_auto": NONE,
    "PresentationNaturality.twIso_fixes_card4Pair": NONE,
    "PresentationNaturality.twoFamilyNeg_no_section": NONE,
    "PresentationNaturality.twoFamilyPos_natural": NONE,
    "PresentationNaturality.twoFamilyPos_has_section": NONE,
    "PresentationNaturality.heterogeneous_naturality_separates": NONE,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U70"))
