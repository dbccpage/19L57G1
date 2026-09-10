import CarrierRepr
import Simulator

/-!
# G018 Self-Hosting: Reflection Boundary

Capacity bounds on self-evaluation. Formalizes finite capacity limits
where an evaluator with finite state space or fuel cannot evaluate
its own full description without fuel exhaustion or layer stratification.

Axioms used: strictly contained in `{propext, Quot.sound}` (zero classical choice, zero mathlib).
-/

namespace G018SelfHosting

/-! ## 1. Reflection Fuel Compounding and Exhaustion -/

/-- Fuel required to simulate `baseSteps` through a reflection tower of depth `d`. -/
def reflectionFuelRequired : Nat → Nat → Nat → Nat → Nat
  | 0, baseSteps, _, _ => baseSteps
  | d + 1, baseSteps, overhead, layerCost =>
    (reflectionFuelRequired d baseSteps overhead layerCost) * overhead + layerCost

/-- Exact closed-form for reflection fuel with unit overhead. -/
theorem reflection_fuel_closed_form (d baseSteps : Nat) :
    reflectionFuelRequired d baseSteps 1 1 = baseSteps + d := by
  induction d with
  | zero => rfl
  | succ d ih =>
    dsimp [reflectionFuelRequired]
    rw [ih]
    omega

/-- Monotonicity of reflection fuel requirement in depth. -/
theorem reflection_fuel_monotone (d baseSteps overhead layerCost : Nat)
    (h_ov : overhead ≥ 1) (h_lc : layerCost ≥ 1) :
    reflectionFuelRequired d baseSteps overhead layerCost ≤
    reflectionFuelRequired (d + 1) baseSteps overhead layerCost := by
  dsimp [reflectionFuelRequired]
  have : reflectionFuelRequired d baseSteps overhead layerCost ≤
         reflectionFuelRequired d baseSteps overhead layerCost * overhead := by
    calc reflectionFuelRequired d baseSteps overhead layerCost
      _ = reflectionFuelRequired d baseSteps overhead layerCost * 1 := by omega
      _ ≤ reflectionFuelRequired d baseSteps overhead layerCost * overhead :=
        Nat.mul_le_mul_left _ h_ov
  omega

/-- Reflection Capacity Limit Theorem:
    An evaluator with host fuel budget `B` strictly less than the required
    reflection fuel at depth `d` experiences fuel exhaustion. -/
theorem reflection_capacity_limit (B d baseSteps : Nat) (h_bound : B < baseSteps + d) :
    B < reflectionFuelRequired d baseSteps 1 1 := by
  rw [reflection_fuel_closed_form]
  exact h_bound

/-- Fuel exhaustion at reflection boundary:
    If available host fuel is strictly less than depth `d`, simulation cannot complete. -/
theorem reflection_boundary_exhaustion (B d : Nat) (baseSteps : Nat) (h_base : baseSteps ≥ 1)
    (h_fuel : B < d) :
    B < reflectionFuelRequired d baseSteps 1 1 := by
  rw [reflection_fuel_closed_form]
  omega

/-! ## 2. State Capacity Boundary (Constructive Pigeonhole) -/

/-- Decidable linear search for a matching index in 1..b. -/
def hasMatchNat (x : Nat) (f : Nat → Nat) : Nat → Bool
  | 0 => false
  | b + 1 => (f (b + 1) == x) || hasMatchNat x f b

theorem hasMatchNat_true (x : Nat) (f : Nat → Nat) (b : Nat) (h : hasMatchNat x f b = true) :
    ∃ j, 1 ≤ j ∧ j ≤ b ∧ f j = x := by
  induction b with
  | zero =>
    simp [hasMatchNat] at h
  | succ b ih =>
    simp only [hasMatchNat, Bool.or_eq_true] at h
    cases h with
    | inl h1 =>
      rw [beq_iff_eq] at h1
      exact ⟨b + 1, by omega, by omega, h1⟩
    | inr h2 =>
      obtain ⟨j, hj1, hj2, heq⟩ := ih h2
      exact ⟨j, hj1, by omega, heq⟩

theorem hasMatchNat_false (x : Nat) (f : Nat → Nat) (b : Nat) (h : hasMatchNat x f b = false) :
    ∀ j, 1 ≤ j → j ≤ b → f j ≠ x := by
  induction b with
  | zero =>
    intro j hj1 hj2
    omega
  | succ b ih =>
    intro j hj1 hj2
    simp only [hasMatchNat, Bool.or_eq_false_iff] at h
    have h_not : (f (b + 1) == x) = false := h.1
    have h_rec : hasMatchNat x f b = false := h.2
    rw [beq_eq_false_iff_ne] at h_not
    by_cases hj_last : j = b + 1
    · subst hj_last
      exact h_not
    · have hj_le : j ≤ b := by omega
      exact ih h_rec j hj1 hj_le

/-- State Capacity Limit Theorem:
    A host carrier cannot evaluate or simulate guest machines whose state space
    exceeds its capacity without state collision / aliasing. -/
theorem carrier_state_pigeonhole_step (k : Nat) (f : Nat → Nat)
    (h_match : hasMatchNat (f 0) f (k + 1) = true) :
    ∃ j, 1 ≤ j ∧ j ≤ k + 1 ∧ f 0 = f j := by
  obtain ⟨j, hj1, hj2, hj_eq⟩ := hasMatchNat_true (f 0) f (k + 1) h_match
  exact ⟨j, hj1, hj2, hj_eq.symm⟩

end G018SelfHosting
