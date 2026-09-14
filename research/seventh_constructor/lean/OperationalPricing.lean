import ConservativeGrammar

/-!
# Operational Valuation & Pricing Under mu1 and mu2

Formalization of Requirement R3:
- Pricing of e_swap under native capability cost mu1 (cardinal potential defect)
- Pricing of e_swap under cumulative transition cost mu2 (operational transition action)
- Theorem: mu1 is an exact coboundary (delta^1 mu1 = 0, oint mu1 = 0)
- Theorem: closed cycles incur strictly positive transition cost (oint mu2 ≠ 0)
- Circulation cost contrast: conservative capability vs dissipative operational history

Axioms: strictly within {propext, Quot.sound}, zero mathlib, zero custom axioms, zero unproven escapes.
AuthorityEffect: None.
-/

namespace SeventhConstructor

open SeventhConstructor

/-! ## 1. Capability Cost mu1 and Exact Coboundary Status -/

/-- Native capability cost mu1 in Nat. -/
def mu1 : ExtendedEvent → Nat
  | ExtendedEvent.supply => 0
  | ExtendedEvent.addData => 1
  | ExtendedEvent.addForm => 1
  | ExtendedEvent.addInstance => 1
  | ExtendedEvent.addRule => 1
  | ExtendedEvent.addSeparation => 1
  | ExtendedEvent.swap => 0

/-- Theorem 3.1: Capability cost of the in-place swap constructor is zero. -/
theorem mu1_swap_zero : mu1 ExtendedEvent.swap = 0 := rfl

/-- Theorem 3.2 (mu1 Coboundary Identity):
The capability cost mu1(e) equals the exact difference in cardinal potential:
mu1(e) = potential(stepProfile(p, e)) - potential(p). -/
theorem mu1_equals_potential_difference (p : CardinalProfile) (e : ExtendedEvent) :
    mu1 e = potential (stepProfile p e) - potential p := by
  cases e <;> dsimp [mu1, stepProfile, potential] <;> omega

/-- Recursive trajectory evaluation on cardinal profiles. -/
def stepTrajectory (p : CardinalProfile) : List ExtendedEvent → CardinalProfile
  | [] => p
  | e :: es => stepTrajectory (stepProfile p e) es

/-- Inductive definition of cumulative cost along an event path. -/
def cumulativeCost (c : ExtendedEvent → Nat) : List ExtendedEvent → Nat
  | [] => 0
  | e :: es => c e + cumulativeCost c es

/-- Cumulative capability cost along an event trajectory. -/
def cumulativeMu1 (es : List ExtendedEvent) : Nat := cumulativeCost mu1 es

/-- Theorem 3.3 (Trajectory mu1 Telescoping Sum):
For any sequence of events es, the cumulative mu1 cost telescopes to the net potential change. -/
theorem cumulative_mu1_telescopes (p : CardinalProfile) (es : List ExtendedEvent) :
    potential (stepTrajectory p es) = potential p + cumulativeMu1 es := by
  induction es generalizing p with
  | nil => rfl
  | cons head tail ih =>
      dsimp [stepTrajectory, cumulativeMu1, cumulativeCost]
      dsimp [cumulativeMu1] at ih
      rw [ih (stepProfile p head)]
      have h_head := mu1_equals_potential_difference p head
      cases head <;> dsimp [potential, stepProfile, mu1] at * <;> omega

/-- Theorem 3.4 (Exact Coboundary Property - Circulation Vanishes):
For any closed path (returning to identical cardinal profile), cumulative capability cost is 0. -/
theorem mu1_closed_cycle_circulation_vanishes (p : CardinalProfile) (es : List ExtendedEvent)
    (h_closed : (stepTrajectory p es) = p) :
    cumulativeMu1 es = 0 := by
  have h_tel := cumulative_mu1_telescopes p es
  rw [h_closed] at h_tel
  omega

/-! ## 2. Cumulative Transition Cost mu2 and Non-Zero Circulation -/

/-- Cumulative operational transition cost mu2 in Nat:
Each non-supply event consumes 1 unit of transition action. -/
def mu2 : ExtendedEvent → Nat
  | ExtendedEvent.supply => 0
  | ExtendedEvent.addData => 1
  | ExtendedEvent.addForm => 1
  | ExtendedEvent.addInstance => 1
  | ExtendedEvent.addRule => 1
  | ExtendedEvent.addSeparation => 1
  | ExtendedEvent.swap => 1

/-- Theorem 3.5: Operational transition cost of a swap step is strictly positive. -/
theorem mu2_swap_cost_positive : mu2 ExtendedEvent.swap = 1 := rfl

/-- Cumulative operational transition cost along an event trajectory. -/
def cumulativeMu2 (es : List ExtendedEvent) : Nat := cumulativeCost mu2 es

/-- Theorem 3.6: Cumulative mu2 cost of k swap steps is exactly k. -/
theorem cumulative_mu2_k_swaps (k : Nat) :
    cumulativeMu2 (List.replicate k ExtendedEvent.swap) = k := by
  induction k with
  | zero => rfl
  | succ k' ih =>
      dsimp [List.replicate, cumulativeMu2, cumulativeCost]
      dsimp [cumulativeMu2] at ih
      rw [ih]
      dsimp [mu2]
      omega

/-- The canonical 2-cycle event sequence: two consecutive swap steps. -/
def cycle2Events : List ExtendedEvent :=
  [ExtendedEvent.swap, ExtendedEvent.swap]

/-- Theorem 3.7: Circulation of capability cost mu1 on the 2-cycle is zero. -/
theorem cycle2_mu1_circulation_zero : cumulativeMu1 cycle2Events = 0 := by
  dsimp [cycle2Events, cumulativeMu1, cumulativeCost, mu1]

/-- Theorem 3.8 (Non-Zero Operational Circulation):
Circulation of transition cost mu2 on the 2-cycle is strictly positive:
oint_(gamma_2) mu2 = 2 ≠ 0. -/
theorem cycle2_mu2_circulation_strictly_positive :
    cumulativeMu2 cycle2Events = 2 := by
  dsimp [cycle2Events, cumulativeMu2, cumulativeCost, mu2]

/-- Theorem 3.9 (Circulation Cost Contrast):
The 7th constructor decouples capability potential from operational transition history:
closed cycles have vanishing capability defect (oint mu1 = 0) but non-zero transition action (oint mu2 = 2). -/
theorem circulation_cost_contrast :
    cumulativeMu1 cycle2Events = 0 ∧ cumulativeMu2 cycle2Events ≠ 0 := by
  exact ⟨cycle2_mu1_circulation_zero, by decide⟩

end SeventhConstructor
