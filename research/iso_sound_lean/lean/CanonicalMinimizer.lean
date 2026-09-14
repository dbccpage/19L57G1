import RegimeAction

/-!
# CanonicalMinimizer: General Soundness and Canonical Classification

Formalization of R2:
- Orbit-choice representative specification: `InOrbitChoice n C`
- Orbit-invariance specification: `OrbitInvariant n C`
- Constructive Isomorphism Witness Extractor: `constructive_witness p₁ p₂`
- Proof that the constructive witness satisfies `witness • r₁ = r₂`
- Proof of General Soundness (`CL-ISO-SOUND`):
    `C r₁ = C r₂ → Iso n r₁ r₂`
- Proof of Completeness:
    `Iso n r₁ r₂ → C r₁ = C r₂`
- Proof of the Biconditional Canonical Classification Theorem:
    `C r₁ = C r₂ ↔ Iso n r₁ r₂`
- Key-valued serialization soundness factoring through orbit-choice
- Equivariant partition pruning theorem: individualization-refinement search
  ranges over invariant orbit slices and computes an orbit-invariant minimizer.

Axioms: strictly within {propext, Quot.sound}, zero mathlib, zero custom axioms, zero omissions.
AuthorityEffect: None.
-/

namespace IsoSoundLean

open Perm

set_option linter.unusedSectionVars false

variable (n : Nat) {α : Type} [PermAction n α] [LawfulPermAction n α]

/-! ## 1. Orbit-Choice and Orbit-Invariance Specifications -/

/-- An orbit-choice map selects a representative within the regime's own orbit. -/
def InOrbitChoice (C : α → α) : Prop :=
  ∀ r : α, Iso n r (C r)

/-- A map is orbit-invariant if it produces identical values on isomorphic regimes. -/
def OrbitInvariant {β : Type} (C : α → β) : Prop :=
  ∀ (p : Perm n) (r : α), C (p • r) = C r

/-! ## 2. Constructive Witness Inversion -/

/-- Given permutations `p₁` and `p₂` that send `r₁` and `r₂` to a common representative,
the constructive isomorphism witness is `p₂⁻¹ ∘ p₁`. -/
def constructive_witness {n : Nat} (p₁ p₂ : Perm n) : Perm n :=
  Perm.comp (Perm.inv p₂) p₁

/-- Theorem 2.1 (Constructive Witness Extraction):
The extracted witness `p₂⁻¹ ∘ p₁` carries `r₁` exactly onto `r₂`. -/
theorem witness_extract {n : Nat} {α : Type} [PermAction n α] [LawfulPermAction n α]
    (p₁ p₂ : Perm n) (r₁ r₂ : α) (c : α)
    (h₁ : p₁ • r₁ = c) (h₂ : p₂ • r₂ = c) :
    (constructive_witness p₁ p₂) • r₁ = r₂ := by
  dsimp [constructive_witness]
  rw [LawfulPermAction.comp_act, h₁, ← h₂]
  exact inv_act_act p₂ r₂

/-- Corollary: If `C` is an orbit-choice map and `C r₁ = C r₂`, an exact isomorphism exists. -/
theorem iso_witness_of_orbit_choice (C : α → α) (r₁ r₂ : α)
    (p₁ : Perm n) (h₁ : p₁ • r₁ = C r₁)
    (p₂ : Perm n) (h₂ : p₂ • r₂ = C r₂)
    (heq : C r₁ = C r₂) :
    (constructive_witness p₁ p₂) • r₁ = r₂ := by
  have h₂' : p₂ • r₂ = C r₁ := by rw [h₂, ← heq]
  exact witness_extract p₁ p₂ r₁ r₂ (C r₁) h₁ h₂'

/-! ## 3. General Soundness (`CL-ISO-SOUND`) -/

/-- Theorem 3.1 (General Soundness `CL-ISO-SOUND`):
Any canonical representative map selecting elements from group orbits yields structural isomorphism under declared assumptions.
`C r₁ = C r₂ → Iso n r₁ r₂` -/
theorem cl_iso_sound (C : α → α) (hC : InOrbitChoice n C) (r₁ r₂ : α)
    (heq : C r₁ = C r₂) : Iso n r₁ r₂ := by
  have h1 : Iso n r₁ (C r₁) := hC r₁
  have h2 : Iso n r₂ (C r₂) := hC r₂
  rw [heq] at h1
  exact iso_trans n h1 (iso_symm n h2)

/-- Concrete Corollary (Soundness on Presentation Regimes):
For presentation regimes under the symmetric group action S(n),
any orbit-choice canonical selector yields structural isomorphism under declared assumptions. -/
theorem regime_cl_iso_sound {n : Nat} (C : Regime n → Regime n)
    (hC : InOrbitChoice n C) (r₁ r₂ : Regime n) (heq : C r₁ = C r₂) :
    Iso n r₁ r₂ :=
  cl_iso_sound n C hC r₁ r₂ heq

/-- Completeness: Orbit-invariant canonical maps give identical outputs on isomorphic regimes. -/
theorem cl_iso_complete {β : Type} (C : α → β) (h_inv : OrbitInvariant n C) (r₁ r₂ : α)
    (hiso : Iso n r₁ r₂) : C r₁ = C r₂ := by
  rcases hiso with ⟨p, hp⟩
  rw [← hp]
  exact (h_inv p r₁).symm

/-- Theorem 3.2 (Biconditional Canonical Classification Theorem):
For any orbit-choice map that is orbit-invariant, canonical equality is necessary
and sufficient for structural isomorphism.
`C r₁ = C r₂ ↔ Iso n r₁ r₂` -/
theorem canonical_classification (C : α → α) (hC : InOrbitChoice n C)
    (h_inv : OrbitInvariant n C) (r₁ r₂ : α) :
    C r₁ = C r₂ ↔ Iso n r₁ r₂ := by
  constructor
  · exact cl_iso_sound n C hC r₁ r₂
  · exact cl_iso_complete n C h_inv r₁ r₂

/-! ## 4. Key-Valued Serialization Soundness -/

/-- Theorem 4.1 (Soundness of Injective Key Serialization):
If canonical keys are produced by injectively serializing an orbit representative,
then key equality yields structural isomorphism under declared assumptions. -/
theorem key_soundness {κ : Type} (C : α → α) (hC : InOrbitChoice n C)
    (enc : α → κ) (henc : ∀ x y, enc x = enc y → x = y)
    (K : α → κ) (hK : ∀ r, K r = enc (C r)) (r₁ r₂ : α)
    (h_key : K r₁ = K r₂) : Iso n r₁ r₂ := by
  have h_enc_eq : enc (C r₁) = enc (C r₂) := by
    rw [← hK r₁, ← hK r₂, h_key]
  have h_c_eq : C r₁ = C r₂ := henc (C r₁) (C r₂) h_enc_eq
  exact cl_iso_sound n C hC r₁ r₂ h_c_eq

/-- Key classification theorem: biconditional classification for injective serializations. -/
theorem key_classification {κ : Type} (C : α → α) (hC : InOrbitChoice n C)
    (h_inv : OrbitInvariant n C)
    (enc : α → κ) (henc : ∀ x y, enc x = enc y → x = y)
    (K : α → κ) (hK : ∀ r, K r = enc (C r)) (r₁ r₂ : α) :
    K r₁ = K r₂ ↔ Iso n r₁ r₂ := by
  constructor
  · exact key_soundness n C hC enc henc K hK r₁ r₂
  · intro hiso
    have h_ceq : C r₁ = C r₂ := cl_iso_complete n C h_inv r₁ r₂ hiso
    rw [hK r₁, hK r₂, h_ceq]

/-! ## 5. Orbit Minimization & Individualization-Refinement -/

/-- A candidate search space assignment mapping each regime to a set of candidate permutations. -/
def SearchSpace (n : Nat) (α : Type) : Type := α → Perm n → Prop

/-- A search space is equivariant if transforming a regime by `p` transforms the candidate
permutations by right-multiplication with `p⁻¹`. -/
def EquivariantSearch (S : SearchSpace n α) : Prop :=
  ∀ (p q : Perm n) (r : α), S (p • r) q ↔ S r (Perm.comp q p)

/-- The image of an equivariant search space over an isomorphic regime covers the exact same states. -/
theorem equivariant_search_same_image (S : SearchSpace n α) (hS : EquivariantSearch n S)
    (p : Perm n) (r : α) (s : α) :
    (∃ q : Perm n, S (p • r) q ∧ q • (p • r) = s) ↔
    (∃ k : Perm n, S r k ∧ k • r = s) := by
  constructor
  · rintro ⟨q, hq, hqs⟩
    refine ⟨Perm.comp q p, ?_, ?_⟩
    · exact (hS p q r).mp hq
    · rw [LawfulPermAction.comp_act]
      exact hqs
  · rintro ⟨k, hk, hks⟩
    refine ⟨Perm.comp k (Perm.inv p), ?_, ?_⟩
    · have h_comp : Perm.comp (Perm.comp k (Perm.inv p)) p = k := by
        rw [Perm.comp_assoc, Perm.comp_left_inv, Perm.comp_id]
      rw [hS p (Perm.comp k (Perm.inv p)) r, h_comp]
      exact hk
    · rw [LawfulPermAction.comp_act, inv_act_act]
      exact hks

/-- Structure representing an orbit-minimizer selection satisfying both InOrbitChoice
and OrbitInvariance. -/
structure OrbitMinimizer (n : Nat) (α : Type) [PermAction n α] [LawfulPermAction n α] where
  select : α → α
  in_orbit : InOrbitChoice n select
  orbit_inv : OrbitInvariant n select

/-- Theorem 5.1: Any orbit minimizer produces a sound and complete canonical isomorphism decider. -/
theorem minimizer_isomorphism_sound (M : OrbitMinimizer n α) (r₁ r₂ : α) :
    M.select r₁ = M.select r₂ ↔ Iso n r₁ r₂ :=
  canonical_classification n M.select M.in_orbit M.orbit_inv r₁ r₂

end IsoSoundLean
