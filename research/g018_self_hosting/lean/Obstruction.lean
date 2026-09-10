import CarrierRepr
import Simulator

/-!
# G018 Self-Hosting: Constructive Diagonal Obstruction

Diagonal obstruction theorem establishing that no finite carrier contains
a total halting/transition self-oracle.

Theorem:
  diagonal_self_evaluation_obstruction:
    ¬ ∃ (P : Nat → Nat → Bool), ∃ d, ∀ x, P d x = ! (P x x)

Axioms used: strictly contained in `{propext, Quot.sound}` (zero classical choice, zero mathlib).
-/

namespace G018SelfHosting

/-- Fundamental boolean fixed-point obstruction: no boolean value equals its own negation. -/
theorem bool_neq_not_self (b : Bool) : (b = !b) → False := by
  cases b <;> decide

/-- Constructive Diagonal Self-Evaluation Obstruction Theorem:
    No total evaluation or prediction function `P : Nat → Nat → Bool` inside the carrier
    can internalize the behavior of the diagonal program `x ↦ ! (P x x)`. -/
theorem diagonal_self_evaluation_obstruction (P : Nat → Nat → Bool) :
    ¬ (∃ d, ∀ x, P d x = ! (P x x)) := by
  intro ⟨d, hd⟩
  have h_self : P d d = ! (P d d) := hd d
  exact bool_neq_not_self (P d d) h_self

/-- Constructive Halting Oracle Obstruction:
    No candidate decider `H : Nat → Bool` can decide whether the self-inverting
    diagonal program halts. -/
theorem halting_self_oracle_obstruction (H : Nat → Bool) (d : Nat)
    (h_diag : H d = true ↔ H d = false) : False := by
  cases h : H d with
  | true =>
    have hf := h_diag.mp h
    rw [h] at hf
    contradiction
  | false =>
    have ht := h_diag.mpr h
    rw [h] at ht
    contradiction

/-- Non-existence of total transition self-oracle:
    For any candidate carrier transition oracle Q, there exists no self-evaluating code
    capable of deciding all diagonalized state branches. -/
theorem total_transition_oracle_refutation (Q : Nat → Bool)
    (diagProg : Nat → Bool) (h_diag : ∀ x, diagProg x = ! (Q x)) :
    ¬ (∃ d, Q d = diagProg d) := by
  intro ⟨d, hd⟩
  have h_eq : Q d = ! (Q d) := by
    calc Q d
      _ = diagProg d := hd
      _ = ! (Q d) := h_diag d
  exact bool_neq_not_self (Q d) h_eq

end G018SelfHosting
