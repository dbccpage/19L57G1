"""Unit 68 check: kernel-check the book's Lean for Unit 68 (`ContactBridge`,
parked `DiffAnchor`, and `DiffAnchorCompat`).

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u68_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.ContactBridge
import Derivation.DiffAnchor
import Derivation.DiffAnchorCompat

namespace Textbook.U68
open DiffInterface ContactBridge ObsDescent

/-- Under pointwise decidability of `ZeroRel O`, indistinguishability in
`obsApart O` is transitive (`obsApart_indist_trans`). -/
theorem obsApart_indist_trans {X R : Type} (O : DiffObs X R)
    [∀ x y, Decidable (ZeroRel O x y)] :
    ∀ x y z, Apartness.Indist (obsApart O) x y →
      Apartness.Indist (obsApart O) y z →
      Apartness.Indist (obsApart O) x z :=
  fun x y z hxy hyz =>
    (indist_obsApart_iff O x z).mpr
      (O.zero_trans ((indist_obsApart_iff O x y).mp hxy)
        ((indist_obsApart_iff O y z).mp hyz))

/-- Audit probe: `apartObs` discharges `zero_refl` definitionally from the
admitted `IsApart.irrefl` field. -/
theorem apartObs_refl_is_irrefl {X : Type} (r : X → X → Prop)
    (h : Apartness.IsApart r) :
    @(apartObs r h).zero_refl = fun {x} => h.irrefl x := rfl

/-- Audit probe: `obsSetting` and `kernelStage` have empty retention and
protection stores by definition (`rfl`). -/
theorem empty_stores_by_policy {X R : Type} (O : DiffObs X R) (a b : X) :
    (obsSetting O a b).ret = (fun _ _ => False) ∧
    (obsSetting O a b).prot = (fun _ _ => False) ∧
    (kernelStage O).retained = (fun _ _ => False) :=
  ⟨rfl, rfl, rfl⟩

/-- `unit_total_not_repr` holds for any value type `R : Type`, not only `Prop`,
because `obsApart_irrefl` is value-type-polymorphic. -/
theorem unit_total_not_repr_any_R :
    ¬ ∃ (R : Type) (O : DiffObs Unit R),
        ∀ x y, obsApart O x y ↔ (fun _ _ : Unit => True) x y := by
  rintro ⟨R, O, hO⟩
  exact obsApart_irrefl O () ((hO () ()).mpr trivial)

/-- With no declared columns (`cols = []`), `DiffAnchor.colObs []` merges `0`
and `1` in the observer quotient. -/
theorem colObs_empty_merges :
    ObsQuotient.mk (DiffAnchor.colObs []) 0 =
      ObsQuotient.mk (DiffAnchor.colObs []) 1 :=
  (DiffAnchor.colObs_quotient_eq_iff_zeroP [] 0 1).mpr rfl

/-- With the declared column `[0]`, `DiffAnchor.colObs [[0]]` separates `0`
and `1` in the observer quotient. -/
theorem colObs_singleton_separates :
    ObsQuotient.mk (DiffAnchor.colObs [[0]]) 0 ≠
      ObsQuotient.mk (DiffAnchor.colObs [[0]]) 1 := by
  intro h
  have hz := (DiffAnchor.colObs_quotient_eq_iff_zeroP [[0]] 0 1).mp h
  revert hz
  decide

/-- Because `DiffAnchor.colObs cols` is `DeltaConstant`, its difference map
descends to `ObsQuotient (DiffAnchor.colObs cols)` in both arguments. -/
theorem colObs_delta_descends (cols : List (List Nat)) :
    ∃ F : ObsQuotient (DiffAnchor.colObs cols) →
        ObsQuotient (DiffAnchor.colObs cols) → List Bool × List Bool,
      ∀ x y, F (ObsQuotient.mk (DiffAnchor.colObs cols) x)
        (ObsQuotient.mk (DiffAnchor.colObs cols) y) =
          (DiffAnchor.colObs cols).delta x y :=
  (deltaDescend_exists_iff (DiffAnchor.colObs cols)).mpr
    (DiffAnchor.colObs_deltaConstant cols)

/-- Concrete instance of `pair_blocked_iff_collapse_collision`: with `cols = []`
(`0` and `1` zero-related), the identity view `id : Nat → Nat` has a collapse
collision at `ObsQuotient.mk (DiffAnchor.colObs [])`. -/
theorem colObs_empty_id_collision :
    PrimDiff.CollapseCollision (fun u v : Nat => u ≠ v)
      (ObsQuotient.mk (DiffAnchor.colObs [])) :=
  pair_blocked_is_collapse_collision (DiffAnchor.colObs []) (fun n => n)
    (x := 0) (y := 1)
    ((DiffAnchor.colObs_zeroRel_iff_zeroP [] 0 1).mpr rfl)
    (by decide)

def bookColor (x : Fin 3) : Bool := x.val == 2

theorem color_bridge_table :
    ZeroRel (kernelObs bookColor) 0 1 ∧
    obsApart (kernelObs bookColor) 0 2 ∧
    (∀ z : Fin 3, obsApart (kernelObs bookColor) 0 z ∨
      obsApart (kernelObs bookColor) z 2) := by
  change bookColor 0 = bookColor 1 ∧ bookColor 0 ≠ bookColor 2 ∧
    (∀ z : Fin 3, bookColor 0 ≠ bookColor z ∨ bookColor z ≠ bookColor 2)
  decide

end Textbook.U68

#print axioms Textbook.U68.color_bridge_table

#print axioms Textbook.U68.obsApart_indist_trans
#print axioms Textbook.U68.apartObs_refl_is_irrefl
#print axioms Textbook.U68.empty_stores_by_policy
#print axioms Textbook.U68.unit_total_not_repr_any_R
#print axioms Textbook.U68.colObs_empty_merges
#print axioms Textbook.U68.colObs_singleton_separates
#print axioms Textbook.U68.colObs_delta_descends
#print axioms Textbook.U68.colObs_empty_id_collision
#print axioms ContactBridge.obsApart_irrefl
#print axioms ContactBridge.obsApart_symm
#print axioms ContactBridge.obsApart_stable
#print axioms ContactBridge.obsSetting_a
#print axioms ContactBridge.obsSetting_bs
#print axioms ContactBridge.obsApart_cotrans
#print axioms ContactBridge.obsSetting_bc
#print axioms ContactBridge.obsSetting_d
#print axioms ContactBridge.apartObs_roundtrip
#print axioms ContactBridge.obsApart_isApart
#print axioms ContactBridge.indist_obsApart_iff
#print axioms ContactBridge.obsApart_repr_iff
#print axioms ContactBridge.unit_total_not_repr
#print axioms ContactBridge.d2_not_obs_complement
#print axioms ContactBridge.triSym_not_obs_complement
#print axioms ContactBridge.bool_bs_repr
#print axioms ContactBridge.d_not_witnessed_repr
#print axioms ContactBridge.cotrans_schema_iff_wlem
#print axioms ContactBridge.stability_schema_iff_dne
#print axioms ContactBridge.located_schema_implies_wlem
#print axioms ContactBridge.declared_zero_as_view
#print axioms ContactBridge.pair_blocked_iff_collapse_collision
#print axioms DiffAnchor.colObs_zeroRel_iff_zeroP
#print axioms DiffAnchor.colObs_quotient_eq_iff_zeroP
#print axioms DiffAnchor.colObs_deltaConstant
"""

EXPECTED = {
    "Textbook.U68.color_bridge_table": PROPEXT,

    "Textbook.U68.obsApart_indist_trans": NONE,
    "Textbook.U68.apartObs_refl_is_irrefl": NONE,
    "Textbook.U68.empty_stores_by_policy": NONE,
    "Textbook.U68.unit_total_not_repr_any_R": NONE,
    "Textbook.U68.colObs_empty_merges": BOTH,
    "Textbook.U68.colObs_singleton_separates": BOTH,
    "Textbook.U68.colObs_delta_descends": BOTH,
    "Textbook.U68.colObs_empty_id_collision": BOTH,
    "ContactBridge.obsApart_irrefl": NONE,
    "ContactBridge.obsApart_symm": NONE,
    "ContactBridge.obsApart_stable": NONE,
    "ContactBridge.obsSetting_a": NONE,
    "ContactBridge.obsSetting_bs": NONE,
    "ContactBridge.obsApart_cotrans": NONE,
    "ContactBridge.obsSetting_bc": NONE,
    "ContactBridge.obsSetting_d": NONE,
    "ContactBridge.apartObs_roundtrip": NONE,
    "ContactBridge.obsApart_isApart": NONE,
    "ContactBridge.indist_obsApart_iff": NONE,
    "ContactBridge.obsApart_repr_iff": NONE,
    "ContactBridge.unit_total_not_repr": NONE,
    "ContactBridge.d2_not_obs_complement": NONE,
    "ContactBridge.triSym_not_obs_complement": PROPEXT,
    "ContactBridge.bool_bs_repr": NONE,
    "ContactBridge.d_not_witnessed_repr": NONE,
    "ContactBridge.cotrans_schema_iff_wlem": NONE,
    "ContactBridge.stability_schema_iff_dne": NONE,
    "ContactBridge.located_schema_implies_wlem": NONE,
    "ContactBridge.declared_zero_as_view": BOTH,
    "ContactBridge.pair_blocked_iff_collapse_collision": BOTH,
    "DiffAnchor.colObs_zeroRel_iff_zeroP": BOTH,
    "DiffAnchor.colObs_quotient_eq_iff_zeroP": BOTH,
    "DiffAnchor.colObs_deltaConstant": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U68"))
