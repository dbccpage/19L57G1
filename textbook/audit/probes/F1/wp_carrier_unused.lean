import Derivation.WeightProfile
open WeightProfile

-- Is the duplicate-free carrier policy load-bearing in the redundancy theorem?
-- Same proof as presentation_profile_redundant, with CarrierList dropped and a
-- duplicated carrier [0, 0]: it still goes through.
example (m c : Nat → Nat) (w : Weights) (h : ∀ p ∈ [0, 0], m (c p) = w p) :
    SameProfile [0, 0] (fun p => m (c p)) w := by
  intro p hp
  show m (c p) * total [0, 0] w = w p * total [0, 0] (fun q => m (c q))
  rw [h p hp, total_congr [0, 0] (fun q => m (c q)) w h]

-- unsigned determination likewise needs only the pointwise equations
example (c d : Nat → Nat) (w : Weights)
    (hc : ∀ p ∈ [0, 0], sq (c p) = w p) (hd : ∀ p ∈ [0, 0], sq (d p) = w p) :
    ∀ p ∈ [0, 0], c p = d p :=
  fun p hp => sq_injective (c p) (d p) ((hc p hp).trans (hd p hp).symm)

-- the unused hypothesis of zero_scale_boundary: the conclusion holds without it
example (l : List Nat) (w : Weights) :
    SameProfile l (fun _ => 0) w ∧ total l (fun _ => 0) = 0 := by
  refine ⟨by simpa using profile_scale_raw l 0 w, by simpa using total_scale l 0 w⟩

#print axioms WeightProfile.descent_iff_subsingleton_support
#print axioms WeightProfile.claimedReadOutUniqueness_false
#print axioms WeightProfile.profile_iff_ray
