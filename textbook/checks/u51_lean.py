"""Unit 51 check: kernel-check the book's Lean for Unit 51.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u51_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.PrimitiveCore

namespace Textbook.U51
open PrimitiveCore

/-- The tally of the exported table, decided in Lean (Genesis proves only
its length). -/
theorem tally :
    (matrixCells.filter (fun c => c.2.2 == "IMPLIES")).length = 17 ∧
    (matrixCells.filter (fun c => c.2.2 == "COUNTERMODEL")).length = 51 ∧
    (matrixCells.filter (fun c => c.2.2 == "OPEN_LOCATED")).length = 4 := by
  decide

/-- Every OPEN cell targets the located axis. -/
theorem open_cells_target_bl :
    matrixCells.all (fun c => c.2.2 != "OPEN_LOCATED" || c.2.1 == "Bl") = true := by
  decide

/-- The nine readings on the oriented two-point model, assembled from the model facts. -/
theorem nine_on_d2Bare :
    W d2Bare ∧ A d2Bare ∧ ¬ Bs d2Bare ∧ Bc d2Bare ∧ Bl d2Bare ∧
    ¬ C d2Bare ∧ D d2Bare ∧ E d2Bare ∧ ¬ F d2Bare :=
  ⟨d2Bare_a.1, d2Bare_a, d2Bare_not_bs, d2Bare_bc, d2Bare_bl, d2Bare_not_c,
   imp_a_d _ d2Bare_a, (e_empty_iff_d d2Bare rfl).mpr (imp_a_d _ d2Bare_a), d2Bare_not_f⟩

/-- A demand without a difference: the one-point model with everything protected. -/
theorem demand_without_difference : C unitFull ∧ ¬ A unitFull ∧ ¬ D unitFull :=
  ⟨unitFull_c, unitFull_not_a, unitFull_not_d⟩

/-- The self-witness is located; W fails Bl through irreflexivity, not locatedness. -/
theorem self_witness_located : Located unitBare.r :=
  located_of_decidable (fun _ _ => True)

/-- Two implications chained give a third cell. -/
theorem f_to_d_by_chain : ∀ S : Setting, F S → D S :=
  fun S h => imp_a_d S (imp_f_a S h)

theorem bs_to_d_by_chain : ∀ S : Setting, Bs S → D S :=
  fun S h => imp_a_d S (imp_bs_a S h)

/-- Cotransitivity on two points is free, and fails at the third point of `tri`. -/
theorem d2_cotrans : Cotrans PrimDiff.D2 :=
  cotrans_auto_on_two _ PrimDiff.D2_irrefl

theorem tri_split_fails : ¬ (triR 0 2 ∨ triR 2 1) := by decide

/-- One admitted merger: the constant map is in the closure and identifies the pair. -/
theorem merger_in_closure :
    ∃ f, PrimDiff.Clos d2Merged.Ops f ∧ f false = f true :=
  ⟨fun _ => false, PrimDiff.Clos.base rfl, rfl⟩

/-- A book model: symmetric, protected, not retained, with one merger. C, Bs and D
hold; F and E fail. -/
def twoSym : Setting where
  X := Bool
  r := PrimDiff.S2
  a := false
  b := true
  ret := fun _ _ => False
  prot := fun _ _ => True
  Ops := fun f => f = fun _ => false

theorem twoSym_readings : C twoSym ∧ Bs twoSym ∧ D twoSym ∧ ¬ F twoSym ∧ ¬ E twoSym :=
  ⟨⟨Or.inl PrimDiff.D2_witness, True.intro⟩, s2Bare_bs,
   (D_iff_ne _).mpr (show (false : Bool) ≠ true by decide), fun h => h.2.1,
   fun h => h (fun _ => false) (PrimDiff.Clos.base rfl) rfl⟩

/-- D is exactly metatheoretic inequality, at an instance. -/
theorem d_at_bool : D d2Bare ↔ (false : Bool) ≠ true := D_iff_ne d2Bare

end Textbook.U51

#print axioms Textbook.U51.tally
#print axioms Textbook.U51.open_cells_target_bl
#print axioms Textbook.U51.nine_on_d2Bare
#print axioms Textbook.U51.demand_without_difference
#print axioms Textbook.U51.self_witness_located
#print axioms Textbook.U51.f_to_d_by_chain
#print axioms Textbook.U51.bs_to_d_by_chain
#print axioms Textbook.U51.d2_cotrans
#print axioms Textbook.U51.tri_split_fails
#print axioms Textbook.U51.merger_in_closure
#print axioms Textbook.U51.twoSym_readings
#print axioms Textbook.U51.d_at_bool
#print axioms PrimitiveCore.D_iff_ne
#print axioms PrimitiveCore.imp_a_d
#print axioms PrimitiveCore.nimp_w_d
#print axioms PrimitiveCore.nimp_c_a
#print axioms PrimitiveCore.nimp_c_d
#print axioms PrimitiveCore.imp_e_d
#print axioms PrimitiveCore.nimp_d_e
#print axioms PrimitiveCore.nimp_a_e
#print axioms PrimitiveCore.e_empty_iff_d
#print axioms PrimitiveCore.nimp_a_bc
#print axioms PrimitiveCore.nimp_bs_bc
#print axioms PrimitiveCore.cotrans_auto_on_two
#print axioms PrimitiveCore.located_of_decidable
#print axioms PrimitiveCore.prot_not_from_witness
#print axioms PrimitiveCore.ret_not_from_witness
#print axioms PrimitiveCore.bool_class
#print axioms PrimitiveCore.matrixCells_length
"""

EXPECTED = {
    "Textbook.U51.tally": NONE,
    "Textbook.U51.open_cells_target_bl": NONE,
    "Textbook.U51.nine_on_d2Bare": NONE,
    "Textbook.U51.demand_without_difference": NONE,
    "Textbook.U51.self_witness_located": NONE,
    "Textbook.U51.f_to_d_by_chain": NONE,
    "Textbook.U51.bs_to_d_by_chain": NONE,
    "Textbook.U51.d2_cotrans": NONE,
    "Textbook.U51.tri_split_fails": PROPEXT,
    "Textbook.U51.merger_in_closure": NONE,
    "Textbook.U51.twoSym_readings": NONE,
    "Textbook.U51.d_at_bool": NONE,
    "PrimitiveCore.D_iff_ne": NONE,
    "PrimitiveCore.imp_a_d": NONE,
    "PrimitiveCore.nimp_w_d": NONE,
    "PrimitiveCore.nimp_c_a": NONE,
    "PrimitiveCore.nimp_c_d": NONE,
    "PrimitiveCore.imp_e_d": NONE,
    "PrimitiveCore.nimp_d_e": NONE,
    "PrimitiveCore.nimp_a_e": NONE,
    "PrimitiveCore.e_empty_iff_d": NONE,
    "PrimitiveCore.nimp_a_bc": PROPEXT,
    "PrimitiveCore.nimp_bs_bc": PROPEXT,
    "PrimitiveCore.cotrans_auto_on_two": NONE,
    "PrimitiveCore.located_of_decidable": NONE,
    "PrimitiveCore.prot_not_from_witness": NONE,
    "PrimitiveCore.ret_not_from_witness": NONE,
    "PrimitiveCore.bool_class": BOTH,
    "PrimitiveCore.matrixCells_length": NONE,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U51"))
