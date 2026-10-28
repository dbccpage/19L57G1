"""Unit 69 check: kernel-check the book's Lean for Unit 69 (`ContactKernel`).

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u69_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.ContactKernel

namespace Textbook.U69
open DiffInterface ContactKernel

/-- Audit probe: `boolKernel` satisfies `DeltaOnto`, so any two `VHom`s out of
`boolKernel` with equal carrier maps are equal (`vhom_unique_of_onto`). -/
theorem boolKernel_deltaOnto : DeltaOnto boolKernel := by
  intro v
  cases v with
  | false => exact ⟨false, false, rfl⟩
  | true => exact ⟨false, true, rfl⟩

/-- Audit probe: `vhom_unique_of_onto` instantiated at `boolKernel`. -/
theorem boolKernel_vhom_unique {X' R' : Type} (K' : WitnessedDiff X' R')
    (h₁ h₂ : VHom boolKernel K') (hf : h₁.f = h₂.f) : h₁ = h₂ :=
  vhom_unique_of_onto boolKernel K' boolKernel_deltaOnto h₁ h₂ hf

/-- Audit probe: `unitValKernel` is NOT `DeltaOnto`, because `2 : Nat` is off
the image of `unitValKernel.delta`. -/
theorem unitValKernel_not_deltaOnto : ¬ DeltaOnto unitValKernel := by
  intro h
  obtain ⟨x, y, hxy⟩ := h 2
  revert x y hxy
  decide

/-- Audit probe: `kernel_licenses_entry`'s second and third conjuncts are the
sealed constants `PrimitivePassage.kernel_enters_preretained`, independent of
the kernel `K`. -/
theorem kernel_licenses_entry_split {X R : Type} (K : WitnessedDiff X R) :
    (kernel_licenses_entry K).1 = kernel_endpoints_ne K ∧
    (kernel_licenses_entry K).2 = PrimitivePassage.kernel_enters_preretained :=
  ⟨rfl, rfl⟩

/-- Audit probe: `toSetting` has empty retention, protection, and operation
stores by definition (`rfl`). -/
theorem toSetting_empty_stores {X R : Type} (K : WitnessedDiff X R) :
    (toSetting K).ret = (fun _ _ => False) ∧
    (toSetting K).prot = (fun _ _ => False) ∧
    (toSetting K).Ops = (fun _ => False) :=
  ⟨rfl, rfl, rfl⟩

end Textbook.U69

#print axioms Textbook.U69.boolKernel_deltaOnto
#print axioms Textbook.U69.boolKernel_vhom_unique
#print axioms Textbook.U69.unitValKernel_not_deltaOnto
#print axioms Textbook.U69.kernel_licenses_entry_split
#print axioms Textbook.U69.toSetting_empty_stores
#print axioms ContactKernel.kernelApart_irrefl
#print axioms ContactKernel.kernel_endpoints_ne
#print axioms ContactKernel.no_kernel_on_subsingleton
#print axioms ContactKernel.toSetting_A
#print axioms ContactKernel.ofSetting_exact
#print axioms ContactKernel.ofSetting_ret_irrelevant
#print axioms ContactKernel.pair_choice_load_bearing
#print axioms ContactKernel.kernel_from_obs_iff_pair
#print axioms ContactKernel.eq_ofDiffObs_of_fields
#print axioms ContactKernel.kernel_no_witness_from_collapse
#print axioms ContactKernel.toDiffObs_fields
#print axioms ContactKernel.toDiffObs_apart
#print axioms ContactKernel.kernel_not_observer
#print axioms ContactKernel.kernel_zero_not_trans
#print axioms ContactKernel.kernel_not_bs
#print axioms ContactKernel.kernel_not_bc
#print axioms ContactKernel.kernel_located_of_decidable
#print axioms ContactKernel.kernel_not_c
#print axioms ContactKernel.kernel_not_f
#print axioms ContactKernel.kernel_to_w
#print axioms ContactKernel.kernel_to_d
#print axioms ContactKernel.kernel_to_e_empty
#print axioms ContactKernel.kernel_not_e_merged
#print axioms ContactKernel.no_kernel_over_allzero
#print axioms ContactKernel.value_presentation_fork
#print axioms ContactKernel.vhom_not_unique
#print axioms ContactKernel.vhom_unique_of_onto
#print axioms ContactKernel.boolKernel_apart_iff
#print axioms ContactKernel.apartObj_irrefl
#print axioms ContactKernel.apartObj_sym_of_observer
#print axioms ContactKernel.kernel_gateway_unique
#print axioms ContactKernel.kernel_gateway_injective
#print axioms ContactKernel.kernel_gateways_not_identical
#print axioms ContactKernel.kernel_no_terminal
#print axioms ContactKernel.kernel_no_terminal_collector
#print axioms ContactKernel.passage_gateway_unique
#print axioms ContactKernel.kernel_licenses_entry
#print axioms ContactKernel.entry_pre_observation
#print axioms ContactKernel.kernel_two_point_presentation
#print axioms ContactKernel.obs_eq_of_fields
#print axioms ContactKernel.toPair_ofPair
#print axioms ContactKernel.ofPair_toPair
#print axioms ContactKernel.ofPair_injective
#print axioms ContactKernel.transpose_kernel_ne
#print axioms ContactKernel.kernel_not_unique_of_pair
#print axioms ContactKernel.boolEqObs_nonzero_ft
#print axioms ContactKernel.boolEqObs_nonzero_tf
#print axioms ContactKernel.two_kernels_from_one_observer
#print axioms ContactKernel.pair_choice_not_unique
#print axioms ContactKernel.swapObs_boolEqObs
#print axioms ContactKernel.no_equivariant_pair_at_fixed_point
#print axioms ContactKernel.no_equivariant_pair_valued_map
#print axioms ContactKernel.contactCells_length
"""

EXPECTED = {
    "Textbook.U69.boolKernel_deltaOnto": NONE,
    "Textbook.U69.boolKernel_vhom_unique": QUOT,
    "Textbook.U69.unitValKernel_not_deltaOnto": NONE,
    "Textbook.U69.kernel_licenses_entry_split": BOTH,
    "Textbook.U69.toSetting_empty_stores": NONE,
    "ContactKernel.kernelApart_irrefl": NONE,
    "ContactKernel.kernel_endpoints_ne": NONE,
    "ContactKernel.no_kernel_on_subsingleton": NONE,
    "ContactKernel.toSetting_A": NONE,
    "ContactKernel.ofSetting_exact": NONE,
    "ContactKernel.ofSetting_ret_irrelevant": NONE,
    "ContactKernel.pair_choice_load_bearing": NONE,
    "ContactKernel.kernel_from_obs_iff_pair": NONE,
    "ContactKernel.eq_ofDiffObs_of_fields": NONE,
    "ContactKernel.kernel_no_witness_from_collapse": NONE,
    "ContactKernel.toDiffObs_fields": NONE,
    "ContactKernel.toDiffObs_apart": NONE,
    "ContactKernel.kernel_not_observer": NONE,
    "ContactKernel.kernel_zero_not_trans": PROPEXT,
    "ContactKernel.kernel_not_bs": NONE,
    "ContactKernel.kernel_not_bc": PROPEXT,
    "ContactKernel.kernel_located_of_decidable": NONE,
    "ContactKernel.kernel_not_c": NONE,
    "ContactKernel.kernel_not_f": NONE,
    "ContactKernel.kernel_to_w": NONE,
    "ContactKernel.kernel_to_d": NONE,
    "ContactKernel.kernel_to_e_empty": NONE,
    "ContactKernel.kernel_not_e_merged": NONE,
    "ContactKernel.no_kernel_over_allzero": NONE,
    "ContactKernel.value_presentation_fork": NONE,
    "ContactKernel.vhom_not_unique": NONE,
    "ContactKernel.vhom_unique_of_onto": QUOT,
    "ContactKernel.boolKernel_apart_iff": NONE,
    "ContactKernel.apartObj_irrefl": NONE,
    "ContactKernel.apartObj_sym_of_observer": NONE,
    "ContactKernel.kernel_gateway_unique": QUOT,
    "ContactKernel.kernel_gateway_injective": NONE,
    "ContactKernel.kernel_gateways_not_identical": NONE,
    "ContactKernel.kernel_no_terminal": PROPEXT,
    "ContactKernel.kernel_no_terminal_collector": PROPEXT,
    "ContactKernel.passage_gateway_unique": BOTH,
    "ContactKernel.kernel_licenses_entry": BOTH,
    "ContactKernel.entry_pre_observation": BOTH,
    "ContactKernel.kernel_two_point_presentation": NONE,
    "ContactKernel.obs_eq_of_fields": NONE,
    "ContactKernel.toPair_ofPair": NONE,
    "ContactKernel.ofPair_toPair": NONE,
    "ContactKernel.ofPair_injective": NONE,
    "ContactKernel.transpose_kernel_ne": NONE,
    "ContactKernel.kernel_not_unique_of_pair": NONE,
    "ContactKernel.boolEqObs_nonzero_ft": NONE,
    "ContactKernel.boolEqObs_nonzero_tf": NONE,
    "ContactKernel.two_kernels_from_one_observer": NONE,
    "ContactKernel.pair_choice_not_unique": NONE,
    "ContactKernel.swapObs_boolEqObs": QUOT,
    "ContactKernel.no_equivariant_pair_at_fixed_point": QUOT,
    "ContactKernel.no_equivariant_pair_valued_map": QUOT,
    "ContactKernel.contactCells_length": NONE,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U69"))
