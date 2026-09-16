-- research/endogenous_continuum/lean/DualCertificate.lean
-- Track 7: Dual Certificate Verification & Hierarchical Pruning
-- AuthorityEffect: None.

import ProjectiveSystem

namespace DualCertificate

open ProjectiveSystem

set_option linter.unusedVariables false

-- ============================================================================
-- 1. Explicit Inductive Path Type and Operational Cost Measures
-- ============================================================================

/-- An explicit inductive directed path from source `u` to destination `w` over vertex type `V`. -/
inductive Path (V : Type) : V → V → Type where
  | refl (v : V) : Path V v v
  | step {u v w : V} (t : MoveTransition V) (h_src : t.src = u) (h_dst : t.dst = v) (p : Path V v w) : Path V u w

/-- Cumulative native capability cost (primary cost Σ μ1) along an inductive path. -/
def pathCost {V : Type} {u w : V} : Path V u w → Nat
  | Path.refl _ => 0
  | Path.step t _ _ p => t.mu1 + pathCost p

/-- Cumulative representation dissipation (secondary cost Σ μ2) along an inductive path. -/
def pathDissipation {V : Type} {u w : V} : Path V u w → Nat
  | Path.refl _ => 0
  | Path.step t _ _ p => t.mu2 + pathDissipation p

/-- Length (number of transitions) of an inductive path. -/
def pathLength {V : Type} {u w : V} : Path V u w → Nat
  | Path.refl _ => 0
  | Path.step _ _ _ p => 1 + pathLength p

-- ============================================================================
-- 2. Dual Potential and Admissibility
-- ============================================================================

/-- Admissibility condition for a dual potential `y : V → Nat` on a transition `t`:
    `y(t.dst) ≤ y(t.src) + t.mu1`.
    This edge inequality lets potential differences lower-bound path costs. -/
def IsAdmissibleOnTransition {V : Type} (y : V → Nat) (t : MoveTransition V) : Prop :=
  y t.dst ≤ y t.src + t.mu1

/-- A path is admissible under dual potential `y` if every transition in the path is admissible. -/
def IsAdmissiblePath {V : Type} (y : V → Nat) {u w : V} : Path V u w → Prop
  | Path.refl _ => True
  | Path.step t _ _ p => IsAdmissibleOnTransition y t ∧ IsAdmissiblePath y p

/-- Single-step dual potential inequality: `y t.dst ≤ y t.src + t.mu1`. -/
theorem dual_step_bound {V : Type} (y : V → Nat) (t : MoveTransition V)
    (h : IsAdmissibleOnTransition y t) :
    y t.dst ≤ y t.src + t.mu1 :=
  h

/-- Fundamental Theorem of Dual Potential:
    For any admissible path from `u` to `w`, `y w ≤ y u + pathCost p`.
    The potential difference `y w - y u` provides a certified
    lower bound for the discrete primary path cost. -/
theorem dual_path_bound {V : Type} (y : V → Nat) {u w : V} (p : Path V u w)
    (h_adm : IsAdmissiblePath y p) :
    y w ≤ y u + pathCost p := by
  induction p with
  | refl v =>
    dsimp [pathCost]
    exact Nat.le_refl (y v)
  | step t h_src h_dst p_tail ih =>
    dsimp [pathCost]
    cases h_adm with
    | intro ht hp =>
      dsimp [IsAdmissibleOnTransition] at ht
      have ih_bound := ih hp
      subst h_src h_dst
      omega

-- ============================================================================
-- 3. Exact Duality Receipts and Certified Refusal
-- ============================================================================

/-- Certified dual lower-bound refusal:
    If `y w > y u + budget`, then NO admissible path from `u` to `w` can have
    `pathCost p ≤ budget`. Every admissible path must strictly exceed the budget. -/
theorem dual_refusal_soundness {V : Type} (y : V → Nat) {u w : V} (budget : Nat)
    (h_refusal : y w > y u + budget) (p : Path V u w) (h_adm : IsAdmissiblePath y p) :
    pathCost p > budget := by
  have h_bound := dual_path_bound y p h_adm
  omega

/-- Duality Gap Non-negativity:
    For any admissible path from `u` to `w`, `y u + pathCost p ≥ y w`. -/
theorem duality_gap_nonnegative {V : Type} (y : V → Nat) {u w : V} (p : Path V u w)
    (h_adm : IsAdmissiblePath y p) :
    y w ≤ y u + pathCost p :=
  dual_path_bound y p h_adm

/-- Zero Duality Gap Certifies Global Path Optimality:
    If an admissible path `p` attains `pathCost p + y u = y w`, then `p` is a
    globally minimal-cost path among all admissible paths from `u` to `w`. -/
theorem optimal_path_zero_gap {V : Type} (y : V → Nat) {u w : V}
    (p_opt : Path V u w) (h_opt_adm : IsAdmissiblePath y p_opt)
    (h_tight : pathCost p_opt + y u = y w)
    (p_other : Path V u w) (h_other_adm : IsAdmissiblePath y p_other) :
    pathCost p_opt ≤ pathCost p_other := by
  have h_other := dual_path_bound y p_other h_other_adm
  omega

-- ============================================================================
-- 4. Dissipative Cycle Pruning
-- ============================================================================

/-- Dissipation Positivity on Positive-Dissipation Steps:
    If every transition in a non-empty cycle has `mu2 ≥ 1`, the cumulative dissipation
    is strictly positive (`pathDissipation ≥ 1`). -/
theorem cycle_dissipation_strictly_positive {V : Type} {u v : V} (t : MoveTransition V)
    (h_src : t.src = u) (h_dst : t.dst = v) (p : Path V v u)
    (h_mu2 : t.mu2 ≥ 1) :
    pathDissipation (Path.step t h_src h_dst p) ≥ 1 := by
  dsimp [pathDissipation]
  omega

/-- Dissipative Cycle Termination Bound:
    An agent with a total representation budget `B_rep` cannot execute more than `B_rep`
    strictly dissipative transitions (`mu2 ≥ 1`). -/
theorem dissipative_length_bounded {V : Type} {u w : V} (p : Path V u w)
    (h_steps : ∀ t : MoveTransition V, t.mu2 ≥ 1) :
    pathDissipation p ≥ pathLength p := by
  induction p with
  | refl v =>
    dsimp [pathDissipation, pathLength]
    omega
  | step t h_src h_dst tail ih =>
    dsimp [pathDissipation, pathLength]
    have ht := h_steps t
    omega

-- ============================================================================
-- 5. Hierarchical Coarse-to-Fine Projection and Pruning
-- ============================================================================

/-- Coarsened Dual Potential Lift:
    Given a coarsening map `π : V_fine → V_coarse` and a coarse dual potential
    `y_coarse : V_coarse → Nat`, the lifted potential `y_fine(v) = y_coarse(π v)`. -/
def liftDualPotential {V_fine V_coarse : Type} (π : V_fine → V_coarse)
    (y_coarse : V_coarse → Nat) : V_fine → Nat :=
  fun v => y_coarse (π v)

/-- Preservation of Admissibility under Coarsening Graph Morphism:
    If a fine transition `t_fine` projects under `π` to a valid coarse transition `t_coarse`
    with `t_fine.mu1 = t_coarse.mu1`, then admissibility of `y_coarse` on `t_coarse` implies
    admissibility of the lifted potential on `t_fine`. -/
theorem coarsening_preserves_admissibility {V_fine V_coarse : Type}
    (π : V_fine → V_coarse) (y_coarse : V_coarse → Nat)
    (t_fine : MoveTransition V_fine) (t_coarse : MoveTransition V_coarse)
    (h_src : π t_fine.src = t_coarse.src)
    (h_dst : π t_fine.dst = t_coarse.dst)
    (h_cost : t_fine.mu1 = t_coarse.mu1)
    (h_adm : IsAdmissibleOnTransition y_coarse t_coarse) :
    IsAdmissibleOnTransition (liftDualPotential π y_coarse) t_fine := by
  dsimp [IsAdmissibleOnTransition, liftDualPotential]
  rw [h_src, h_dst, h_cost]
  exact h_adm

/-- Coarsening Collapse Admissibility:
    If a fine transition `t_fine` collapses to an identity step under `π` (`π t_fine.src = π t_fine.dst`),
    the lifted potential is trivially admissible regardless of coarse potential values. -/
theorem coarsening_collapse_admissibility {V_fine V_coarse : Type}
    (π : V_fine → V_coarse) (y_coarse : V_coarse → Nat)
    (t_fine : MoveTransition V_fine)
    (h_collapse : π t_fine.src = π t_fine.dst) :
    IsAdmissibleOnTransition (liftDualPotential π y_coarse) t_fine := by
  dsimp [IsAdmissibleOnTransition, liftDualPotential]
  rw [h_collapse]
  omega

/-- Conditional hierarchical refusal theorem:
    If the coarse dual potential satisfies `y_coarse(π w) > y_coarse(π u) + budget`,
    then NO fine-scale path whose transitions lift to admissible coarse steps can
    attain `pathCost p_fine ≤ budget`.
    The conclusion applies only when the lifted potential is explicitly
    admissible along the supplied fine path. -/
theorem hierarchical_refusal_soundness {V_fine V_coarse : Type}
    (π : V_fine → V_coarse) (y_coarse : V_coarse → Nat)
    {u w : V_fine} (budget : Nat)
    (h_coarse_refusal : y_coarse (π w) > y_coarse (π u) + budget)
    (p_fine : Path V_fine u w)
    (h_lift_adm : IsAdmissiblePath (liftDualPotential π y_coarse) p_fine) :
    pathCost p_fine > budget := by
  have h_lifted_refusal : (liftDualPotential π y_coarse) w > (liftDualPotential π y_coarse) u + budget := by
    dsimp [liftDualPotential]
    exact h_coarse_refusal
  exact dual_refusal_soundness (liftDualPotential π y_coarse) budget h_lifted_refusal p_fine h_lift_adm

end DualCertificate
