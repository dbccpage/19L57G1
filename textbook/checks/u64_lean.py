"""Unit 64 check: kernel-check the book's Lean for Unit 64 (WeightProfile).

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u64_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.WeightProfile

namespace Textbook.U64
open WeightProfile

-- Audit check 1: zero_scale_boundary conclusion holds without 0 < total l w
theorem zero_scale_boundary_unconditional (l : List Nat) (w : Weights) :
    SameProfile l (fun _ => 0) w ∧
      total l (fun _ => 0) = 0 ∧ ¬ 0 < total l (fun _ => 0) := by
  refine ⟨?_, ?_, ?_⟩
  · simpa using profile_scale_raw l 0 w
  · simpa using total_scale l 0 w
  · have hz : total l (fun _ => 0) = 0 := by
      simpa using total_scale l 0 w
    rw [hz]
    omega

-- Audit check 2: presentation_profile_redundant and unsigned_decoration_determined
-- hold on the duplicated list [0, 0] with CarrierList dropped
theorem dup_presentation_profile_redundant (m c : Nat → Nat) (w : Weights)
    (h : ∀ p ∈ ([0, 0] : List Nat), m (c p) = w p) :
    SameProfile [0, 0] (fun p => m (c p)) w := by
  intro p hp
  show m (c p) * total [0, 0] w = w p * total [0, 0] (fun q => m (c q))
  rw [h p hp, total_congr [0, 0] (fun q => m (c q)) w h]

theorem dup_unsigned_determined (c d : Nat → Nat) (w : Weights)
    (hc : ∀ p ∈ ([0, 0] : List Nat), sq (c p) = w p)
    (hd : ∀ p ∈ ([0, 0] : List Nat), sq (d p) = w p) :
    ∀ p ∈ ([0, 0] : List Nat), c p = d p := by
  intro p hp
  exact sq_injective (c p) (d p) ((hc p hp).trans (hd p hp).symm)

-- Student exercise: transitivity fails across a zero-total middle assignment
def uEx : Weights | 0 => 1 | 1 => 2 | _ => 0
def vEx : Weights | _ => 0
def wEx : Weights | 0 => 2 | 1 => 1 | _ => 0

theorem zero_middle_breaks_trans :
    SameProfile [0, 1] uEx vEx ∧
    SameProfile [0, 1] vEx wEx ∧
    ¬ SameProfile [0, 1] uEx wEx := by
  refine ⟨?_, ?_, ?_⟩
  · intro p _
    change uEx p * 0 = 0 * 3
    omega
  · intro p _
    change 0 * 3 = wEx p * 0
    omega
  · intro h
    have h0 := h 0 (by decide)
    change 1 * 3 = 2 * 3 at h0
    omega

theorem readOut_2_3_diff :
    readOut 2 3 1 1 * readOut 2 3 1 1 = 25 ∧
    readOut 2 3 1 (-1) * readOut 2 3 1 (-1) = 1 ∧
    readOut 2 3 1 1 * readOut 2 3 1 1 - readOut 2 3 1 (-1) * readOut 2 3 1 (-1) = 4 * (2 * 3) := by
  decide

end Textbook.U64

#print axioms Textbook.U64.zero_scale_boundary_unconditional
#print axioms Textbook.U64.dup_presentation_profile_redundant
#print axioms Textbook.U64.dup_unsigned_determined
#print axioms Textbook.U64.zero_middle_breaks_trans
#print axioms Textbook.U64.readOut_2_3_diff
#print axioms WeightProfile.duplicate_list_not_carrier
#print axioms WeightProfile.profile_refl
#print axioms WeightProfile.profile_symm
#print axioms WeightProfile.profile_trans
#print axioms WeightProfile.profile_scale_raw
#print axioms WeightProfile.profile_scale_positive
#print axioms WeightProfile.profile_equivalence_positive
#print axioms WeightProfile.zero_scale_boundary
#print axioms WeightProfile.profile_iff_ray
#print axioms WeightProfile.profile_support
#print axioms WeightProfile.profile_order
#print axioms WeightProfile.profile_forgets_total
#print axioms WeightProfile.presentation_profile_redundant
#print axioms WeightProfile.presentations_agree_on_profile
#print axioms WeightProfile.sq_mono
#print axioms WeightProfile.sq_injective
#print axioms WeightProfile.unsigned_decoration_determined
#print axioms WeightProfile.signed_square_presentations_split
#print axioms WeightProfile.presentation_scope
#print axioms WeightProfile.sq_mul
#print axioms WeightProfile.sq_add_sub
#print axioms WeightProfile.descent_iff_subsingleton_support
#print axioms WeightProfile.decoratedCarrierShape_exists
#print axioms WeightProfile.claimedReadOutUniqueness_false
#print axioms WeightProfile.finite_scope_summary
"""

EXPECTED = {
    "Textbook.U64.zero_scale_boundary_unconditional": BOTH,
    "Textbook.U64.dup_presentation_profile_redundant": BOTH,
    "Textbook.U64.dup_unsigned_determined": BOTH,
    "Textbook.U64.zero_middle_breaks_trans": BOTH,
    "Textbook.U64.readOut_2_3_diff": NONE,
    "WeightProfile.duplicate_list_not_carrier": PROPEXT,
    "WeightProfile.profile_refl": NONE,
    "WeightProfile.profile_symm": NONE,
    "WeightProfile.profile_trans": BOTH,
    "WeightProfile.profile_scale_raw": BOTH,
    "WeightProfile.profile_scale_positive": BOTH,
    "WeightProfile.profile_equivalence_positive": BOTH,
    "WeightProfile.zero_scale_boundary": BOTH,
    "WeightProfile.profile_iff_ray": BOTH,
    "WeightProfile.profile_support": BOTH,
    "WeightProfile.profile_order": NONE,
    "WeightProfile.profile_forgets_total": BOTH,
    "WeightProfile.presentation_profile_redundant": BOTH,
    "WeightProfile.presentations_agree_on_profile": BOTH,
    "WeightProfile.sq_mono": BOTH,
    "WeightProfile.sq_injective": BOTH,
    "WeightProfile.unsigned_decoration_determined": BOTH,
    "WeightProfile.signed_square_presentations_split": BOTH,
    "WeightProfile.presentation_scope": BOTH,
    "WeightProfile.sq_mul": PROPEXT,
    "WeightProfile.sq_add_sub": BOTH,
    "WeightProfile.descent_iff_subsingleton_support": BOTH,
    "WeightProfile.decoratedCarrierShape_exists": NONE,
    "WeightProfile.claimedReadOutUniqueness_false": BOTH,
    "WeightProfile.finite_scope_summary": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U64"))
