-- research/endogenous_continuum/lean/InternalQuotienting.lean
-- Track 4: Confluence-Driven Internal Quotienting
-- AuthorityEffect: None.

/-!
# Track 4: Confluence-Driven Internal Quotienting

This module formalizes an endogenous equivalence relation via local confluent rewrite rules,
replacing external global canonical orbit minimizers with constructive local confluence,
Newman's lemma, and joinability arguments.

Key results:
1. `local_joinability`: one-step divergences are joinable under local confluence.
2. `normal_form_unique`: confluent rewrites produce identical normal forms.
3. `newman_lemma`: local confluence and termination yield global confluence.
4. `endogenous_equivalence_refl`: Eqv is reflexive.
5. `endogenous_equivalence_symm`: Eqv is symmetric.
6. `endogenous_equivalence_trans`: Eqv is transitive.
7. `canonical_minimizer_elimination`: endogenous joinability substitutes for external orbit minimization.
8. `external_minimizer_subsumption`: any external selector coincides with the internal normal form.
-/

namespace InternalQuotienting

set_option linter.unusedVariables false

-- ============================================================================
-- 1. Rewrite Relations and Multi-Step Closure
-- ============================================================================

/-- Multi-step reflexive transitive closure of a local rewrite relation. -/
inductive ReflTransStep {Carrier : Type} (Step : Carrier → Carrier → Prop) : Carrier → Carrier → Prop where
  | refl (x : Carrier) : ReflTransStep Step x x
  | step {x y z : Carrier} : Step x y → ReflTransStep Step y z → ReflTransStep Step x z

/-- Reflexivity of multi-step reduction. -/
theorem reflTransStep_refl {Carrier : Type} (Step : Carrier → Carrier → Prop) (x : Carrier) :
    ReflTransStep Step x x :=
  ReflTransStep.refl x

/-- A single rewrite step embeds into the multi-step closure. -/
theorem reflTransStep_single {Carrier : Type} {Step : Carrier → Carrier → Prop} {x y : Carrier}
    (h : Step x y) : ReflTransStep Step x y :=
  ReflTransStep.step h (ReflTransStep.refl y)

/-- Transitivity of multi-step reduction. -/
theorem reflTransStep_trans {Carrier : Type} {Step : Carrier → Carrier → Prop} {x y z : Carrier}
    (hxy : ReflTransStep Step x y) (hyz : ReflTransStep Step y z) : ReflTransStep Step x z := by
  induction hxy with
  | refl _ => exact hyz
  | step hst _ ih => exact ReflTransStep.step hst (ih hyz)

-- ============================================================================
-- 2. Joinability, Confluence, and Normal Forms
-- ============================================================================

/-- Joinability: two states reach a common descendant via multi-step rewrites. -/
def Joinable {Carrier : Type} (Step : Carrier → Carrier → Prop) (y1 y2 : Carrier) : Prop :=
  ∃ z, ReflTransStep Step y1 z ∧ ReflTransStep Step y2 z

/-- Local confluence: one-step divergences can be joined. -/
def IsLocallyConfluent {Carrier : Type} (Step : Carrier → Carrier → Prop) : Prop :=
  ∀ x y1 y2, Step x y1 → Step x y2 → Joinable Step y1 y2

/-- One-step divergences are joinable under local confluence. -/
theorem local_joinability {Carrier : Type} (Step : Carrier → Carrier → Prop)
    (h_conf : IsLocallyConfluent Step) {x y1 y2 : Carrier}
    (h1 : Step x y1) (h2 : Step x y2) :
    Joinable Step y1 y2 :=
  h_conf x y1 y2 h1 h2

/-- Global confluence: arbitrary multi-step divergences can be joined. -/
def IsConfluent {Carrier : Type} (Step : Carrier → Carrier → Prop) : Prop :=
  ∀ x y1 y2, ReflTransStep Step x y1 → ReflTransStep Step x y2 → Joinable Step y1 y2

/-- Irreducible normal form: a state admitting no outgoing rewrite steps. -/
def IsNormalForm {Carrier : Type} (Step : Carrier → Carrier → Prop) (x : Carrier) : Prop :=
  ∀ y, ¬ Step x y

/-- A normal form cannot make any nontrivial rewrite steps. -/
theorem normal_form_terminal {Carrier : Type} {Step : Carrier → Carrier → Prop} {x z : Carrier}
    (hnf : IsNormalForm Step x) (hr : ReflTransStep Step x z) : x = z := by
  cases hr with
  | refl => rfl
  | step hst _ => exact (hnf _ hst).elim

/-- Confluent terminating rewrites produce identical normal forms. -/
theorem normal_form_unique {Carrier : Type} (Step : Carrier → Carrier → Prop)
    (h_conf : IsConfluent Step) {x n1 n2 : Carrier}
    (h1 : ReflTransStep Step x n1) (h2 : ReflTransStep Step x n2)
    (hnf1 : IsNormalForm Step n1) (hnf2 : IsNormalForm Step n2) :
    n1 = n2 := by
  obtain ⟨z, hz1, hz2⟩ := h_conf x n1 n2 h1 h2
  have e1 : n1 = z := normal_form_terminal hnf1 hz1
  have e2 : n2 = z := normal_form_terminal hnf2 hz2
  exact e1.trans e2.symm

-- ============================================================================
-- 3. Termination and Newman's Lemma
-- ============================================================================

/-- Termination (strong normalization): accessibility of all states under Step. -/
def IsTerminating {Carrier : Type} (Step : Carrier → Carrier → Prop) : Prop :=
  ∀ x, Acc (fun y x => Step x y) x

/-- Newman's Lemma: constructive derivation of global confluence from local confluence and termination. -/
theorem newman_lemma {Carrier : Type} (Step : Carrier → Carrier → Prop)
    (h_term : IsTerminating Step) (h_lc : IsLocallyConfluent Step) :
    IsConfluent Step := by
  intro x
  induction (h_term x) with
  | intro x _ ih =>
    intro y1 y2 hy1 hy2
    cases hy1 with
    | refl =>
      exact ⟨y2, hy2, ReflTransStep.refl y2⟩
    | step hst1 hy1_tail =>
      cases hy2 with
      | refl =>
        exact ⟨y1, ReflTransStep.refl y1, ReflTransStep.step hst1 hy1_tail⟩
      | step hst2 hy2_tail =>
        obtain ⟨w, hw1, hw2⟩ := h_lc x _ _ hst1 hst2
        obtain ⟨u, hu1, hu2⟩ := ih _ hst1 y1 w hy1_tail hw1
        have hx2_to_u : ReflTransStep Step _ u := reflTransStep_trans hw2 hu2
        obtain ⟨z, hz1, hz2⟩ := ih _ hst2 u y2 hx2_to_u hy2_tail
        exact ⟨z, reflTransStep_trans hu1 hz1, hz2⟩

/-- Corrollary: terminating locally confluent rewrites have unique normal forms. -/
theorem normal_form_unique_of_terminating {Carrier : Type} (Step : Carrier → Carrier → Prop)
    (h_term : IsTerminating Step) (h_lc : IsLocallyConfluent Step) {x n1 n2 : Carrier}
    (h1 : ReflTransStep Step x n1) (h2 : ReflTransStep Step x n2)
    (hnf1 : IsNormalForm Step n1) (hnf2 : IsNormalForm Step n2) :
    n1 = n2 :=
  normal_form_unique Step (newman_lemma Step h_term h_lc) h1 h2 hnf1 hnf2

-- ============================================================================
-- 4. Endogenous Equivalence Relation
-- ============================================================================

/-- Endogenous equivalence relation: symmetric-transitive closure of rewrite reachability. -/
inductive Eqv {Carrier : Type} (Step : Carrier → Carrier → Prop) : Carrier → Carrier → Prop where
  | refl (x : Carrier) : Eqv Step x x
  | step {x y : Carrier} : Step x y → Eqv Step x y
  | symm {x y : Carrier} : Eqv Step x y → Eqv Step y x
  | trans {x y z : Carrier} : Eqv Step x y → Eqv Step y z → Eqv Step x z

/-- Eqv is reflexive. -/
theorem endogenous_equivalence_refl {Carrier : Type} (Step : Carrier → Carrier → Prop) (x : Carrier) :
    Eqv Step x x :=
  Eqv.refl x

/-- Eqv is symmetric. -/
theorem endogenous_equivalence_symm {Carrier : Type} (Step : Carrier → Carrier → Prop) {x y : Carrier}
    (h : Eqv Step x y) : Eqv Step y x :=
  Eqv.symm h

/-- Eqv is transitive. -/
theorem endogenous_equivalence_trans {Carrier : Type} (Step : Carrier → Carrier → Prop) {x y z : Carrier}
    (hxy : Eqv Step x y) (hyz : Eqv Step y z) : Eqv Step x z :=
  Eqv.trans hxy hyz

-- ============================================================================
-- 5. Coincidence of Equivalence and Joinability
-- ============================================================================

/-- Multi-step reachability embeds into endogenous equivalence. -/
theorem eqv_of_reflTransStep {Carrier : Type} {Step : Carrier → Carrier → Prop} {x y : Carrier}
    (h : ReflTransStep Step x y) : Eqv Step x y := by
  induction h with
  | refl _ => exact Eqv.refl _
  | step hst _ ih => exact Eqv.trans (Eqv.step hst) ih

/-- Joinability implies endogenous equivalence. -/
theorem eqv_of_joinable {Carrier : Type} {Step : Carrier → Carrier → Prop} {x y : Carrier}
    (hj : Joinable Step x y) : Eqv Step x y := by
  obtain ⟨z, hxz, hyz⟩ := hj
  exact Eqv.trans (eqv_of_reflTransStep hxz) (Eqv.symm (eqv_of_reflTransStep hyz))

/-- Under confluence, endogenous equivalence implies joinability (Church-Rosser). -/
theorem joinable_of_eqv {Carrier : Type} (Step : Carrier → Carrier → Prop)
    (h_conf : IsConfluent Step) {x y : Carrier}
    (h : Eqv Step x y) : Joinable Step x y := by
  induction h with
  | refl u =>
    exact ⟨u, ReflTransStep.refl u, ReflTransStep.refl u⟩
  | step hst =>
    exact ⟨_, reflTransStep_single hst, ReflTransStep.refl _⟩
  | symm _ ih =>
    obtain ⟨z, h1, h2⟩ := ih
    exact ⟨z, h2, h1⟩
  | trans _ _ ih1 ih2 =>
    obtain ⟨u, hxu, hyu⟩ := ih1
    obtain ⟨v, hyv, hzv⟩ := ih2
    obtain ⟨w, huw, hvw⟩ := h_conf _ u v hyu hyv
    exact ⟨w, reflTransStep_trans hxu huw, reflTransStep_trans hzv hvw⟩

/-- Coincidence of endogenous equivalence and joinability in confluent systems. -/
theorem eqv_iff_joinable {Carrier : Type} (Step : Carrier → Carrier → Prop)
    (h_conf : IsConfluent Step) (x y : Carrier) :
    Eqv Step x y ↔ Joinable Step x y :=
  ⟨joinable_of_eqv Step h_conf, eqv_of_joinable⟩

-- ============================================================================
-- 6. Canonical Minimizer Elimination
-- ============================================================================

/-- Canonical minimizer elimination: endogenous joinability substitutes for external orbit minimization.
    Two states are in the same endogenous equivalence class if and only if their internal normal
    forms coincide. -/
theorem canonical_minimizer_elimination {Carrier : Type} (Step : Carrier → Carrier → Prop)
    (h_conf : IsConfluent Step) {x y n_x n_y : Carrier}
    (hx : ReflTransStep Step x n_x) (hy : ReflTransStep Step y n_y)
    (hnf_x : IsNormalForm Step n_x) (hnf_y : IsNormalForm Step n_y) :
    Eqv Step x y ↔ n_x = n_y := by
  constructor
  · intro heqv
    obtain ⟨z, hxz, hyz⟩ := joinable_of_eqv Step h_conf heqv
    obtain ⟨wx, h_nx_wx, h_z_wx⟩ := h_conf x n_x z hx hxz
    have enx : n_x = wx := normal_form_terminal hnf_x h_nx_wx
    obtain ⟨wy, h_ny_wy, h_z_wy⟩ := h_conf y n_y z hy hyz
    have eny : n_y = wy := normal_form_terminal hnf_y h_ny_wy
    have h_z_nx : ReflTransStep Step z n_x := enx ▸ h_z_wx
    have h_z_ny : ReflTransStep Step z n_y := eny ▸ h_z_wy
    obtain ⟨w, h_nx_w, h_ny_w⟩ := h_conf z n_x n_y h_z_nx h_z_ny
    have e1 : n_x = w := normal_form_terminal hnf_x h_nx_w
    have e2 : n_y = w := normal_form_terminal hnf_y h_ny_w
    exact e1.trans e2.symm
  · intro heq
    have hx' : ReflTransStep Step x n_y := heq ▸ hx
    exact eqv_of_joinable ⟨n_y, hx', hy⟩

/-- Structure representing an external canonical orbit minimizer selector. -/
structure ExternalCanonicalMinimizer {Carrier : Type} (Step : Carrier → Carrier → Prop) where
  select : Carrier → Carrier
  orbit_invariant : ∀ a b, Eqv Step a b → select a = select b
  normal_form_fixed : ∀ n, IsNormalForm Step n → select n = n

/-- External minimizer subsumption: any external selector is identical to the internal normal form. -/
theorem external_minimizer_subsumption {Carrier : Type} (Step : Carrier → Carrier → Prop)
    (M : ExternalCanonicalMinimizer Step) {x n : Carrier}
    (hx : ReflTransStep Step x n) (hnf : IsNormalForm Step n) :
    M.select x = n := by
  have heqv : Eqv Step x n := eqv_of_reflTransStep hx
  have h_inv : M.select x = M.select n := M.orbit_invariant x n heqv
  have h_fix : M.select n = n := M.normal_form_fixed n hnf
  exact h_inv.trans h_fix

-- ============================================================================
-- 7. Axiom Census Audit
-- ============================================================================

#print axioms local_joinability
#print axioms normal_form_unique
#print axioms newman_lemma
#print axioms normal_form_unique_of_terminating
#print axioms endogenous_equivalence_refl
#print axioms endogenous_equivalence_symm
#print axioms endogenous_equivalence_trans
#print axioms eqv_of_reflTransStep
#print axioms eqv_of_joinable
#print axioms joinable_of_eqv
#print axioms eqv_iff_joinable
#print axioms canonical_minimizer_elimination
#print axioms external_minimizer_subsumption

end InternalQuotienting
