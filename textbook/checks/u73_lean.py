from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

SNIPPET = r"""
import Derivation.Breaking
import Derivation.Composing

namespace Textbook.U73

open Breaking
open Composing

-- 1. Over emptyBreak, a selector is vacuously Represents, OrbitConstant, and Equivariant
--    (witnessing why an inhabitant w : B.Whole is required by no_orbit_constant_equivariant_endomap).
def emptySel : Selector emptyBreak := fun x => nomatch x

theorem emptySel_all_three :
    Represents emptyBreak emptySel ∧
    OrbitConstant emptyBreak emptySel ∧
    Equivariant emptyBreak emptySel :=
  ⟨(fun w => nomatch w), (fun w => nomatch w), (fun w => nomatch w)⟩

-- 2. On boolBreak, id is Represents and Equivariant, but NOT OrbitConstant
--    (dual to constFalse, which is Represents and OrbitConstant, but NOT Equivariant).
def idSel : Selector boolBreak := id

theorem idSel_equivariant_not_orbitConstant :
    (Represents boolBreak idSel ∧ Equivariant boolBreak idSel) ∧
    ¬ OrbitConstant boolBreak idSel := by
  refine ⟨⟨fun w => Or.inl rfl, fun _ => rfl⟩, ?_⟩
  intro h
  exact Bool.noConfusion (h false)

-- 3. On Tri, an involution fixing t0 and swapping t1 ↔ t2 has a common fixed point t0,
--    so selector_exists_at_common_fixed_point gives an orbit-constant equivariant selector.
def swap12 : Tri → Tri
  | .t0 => .t0
  | .t1 => .t2
  | .t2 => .t1

theorem swap12_has_selector :
    ∃ s : Tri → Tri,
      (∀ _ : Unit, ∀ w : Tri, s (swap12 w) = s w) ∧
      (∀ _ : Unit, ∀ w : Tri, s (swap12 w) = swap12 (s w)) :=
  selector_exists_at_common_fixed_point (fun (_ : Unit) => swap12) .t0 (fun _ => rfl)

-- 4. In Composing, allCompose satisfies full relational associativity RelAssoc
--    (showing RelAssoc is inhabited, whereas skewCompose refutes it).
theorem allCompose_relAssoc : RelAssoc allCompose := by
  intro a b c d f g k w
  exact ⟨fun _ => ⟨true, trivial, trivial⟩, fun _ => ⟨true, trivial, trivial⟩⟩

end Textbook.U73

#print axioms Textbook.U73.emptySel_all_three
#print axioms Textbook.U73.idSel_equivariant_not_orbitConstant
#print axioms Textbook.U73.swap12_has_selector
#print axioms Textbook.U73.allCompose_relAssoc
-- All 15 theorems in Breaking (7 in Derivation.lean + 8 omitted from Derivation.lean)
#print axioms Breaking.ne_image
#print axioms Breaking.two_cycle
#print axioms Breaking.fourBreak_not_singleOrbit
#print axioms Breaking.no_orbit_constant_equivariant_endomap
#print axioms Breaking.boolBreak_singleOrbit
#print axioms Breaking.constFalse_represents
#print axioms Breaking.constFalse_orbitConstant
#print axioms Breaking.constFalse_not_equivariant
#print axioms Breaking.imposable_but_not_equivariant
#print axioms Breaking.no_selector_of_no_common_fixed_point
#print axioms Breaking.no_common_fixed_point
#print axioms Breaking.no_orbit_constant_equivariant_selector
#print axioms Breaking.no_fixed_point_free_involution_on_Tri
#print axioms Breaking.selector_exists_at_common_fixed_point
#print axioms Breaking.selector_iff_common_fixed_point
-- All 7 theorems in parked Composing (audited via ParkedAudit.lean)
#print axioms Composing.composition_may_fail
#print axioms Composing.noneCompose_no_identity
#print axioms Composing.composite_may_be_nonunique
#print axioms Composing.selection_is_possible
#print axioms Composing.relAssocLeft_of_relAssoc
#print axioms Composing.skew_not_relAssocLeft
#print axioms Composing.skew_not_relAssoc
"""

EXPECTED = {
    "Textbook.U73.emptySel_all_three": NONE,
    "Textbook.U73.idSel_equivariant_not_orbitConstant": NONE,
    "Textbook.U73.swap12_has_selector": NONE,
    "Textbook.U73.allCompose_relAssoc": NONE,
    "Breaking.ne_image": NONE,
    "Breaking.two_cycle": NONE,
    "Breaking.fourBreak_not_singleOrbit": NONE,
    "Breaking.no_orbit_constant_equivariant_endomap": NONE,
    "Breaking.boolBreak_singleOrbit": NONE,
    "Breaking.constFalse_represents": NONE,
    "Breaking.constFalse_orbitConstant": NONE,
    "Breaking.constFalse_not_equivariant": NONE,
    "Breaking.imposable_but_not_equivariant": NONE,
    "Breaking.no_selector_of_no_common_fixed_point": NONE,
    "Breaking.no_common_fixed_point": NONE,
    "Breaking.no_orbit_constant_equivariant_selector": NONE,
    "Breaking.no_fixed_point_free_involution_on_Tri": NONE,
    "Breaking.selector_exists_at_common_fixed_point": NONE,
    "Breaking.selector_iff_common_fixed_point": NONE,
    "Composing.composition_may_fail": NONE,
    "Composing.noneCompose_no_identity": NONE,
    "Composing.composite_may_be_nonunique": NONE,
    "Composing.selection_is_possible": NONE,
    "Composing.relAssocLeft_of_relAssoc": NONE,
    "Composing.skew_not_relAssocLeft": NONE,
    "Composing.skew_not_relAssoc": NONE,
}


if __name__ == "__main__":
    raise SystemExit(main(SNIPPET, EXPECTED, "U73"))
