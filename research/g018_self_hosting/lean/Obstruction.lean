import CarrierRepr
import Simulator

/-!
# G018 Self-Hosting: Constructive Diagonal Obstruction

Conditional Boolean self-negation lemmas. This module does not construct a
machine-code evaluator or a fixed point connecting code to its own behavior.

Theorem:
  diagonal_self_evaluation_obstruction:
    ¬ ∃ (P : Nat → Nat → Bool), ∃ d, ∀ x, P d x = ! (P x x)

Axioms used: strictly contained in `{propext, Quot.sound}` (zero classical choice, zero mathlib).
-/

namespace G018SelfHosting

/-- Fundamental boolean fixed-point obstruction: no boolean value equals its own negation. -/
theorem bool_neq_not_self (b : Bool) : (b = !b) → False := by
  cases b <;> decide

/-- No row of an arbitrary Boolean table can equal the pointwise negation
    of its own diagonal entry. No machine representation is assumed. -/
theorem diagonal_self_evaluation_obstruction (P : Nat → Nat → Bool) :
    ¬ (∃ d, ∀ x, P d x = ! (P x x)) := by
  intro ⟨d, hd⟩
  have h_self : P d d = ! (P d d) := hd d
  exact bool_neq_not_self (P d d) h_self

/-- An explicitly assumed self-negating Boolean equivalence is contradictory.
    This statement has no evaluator or halting semantics. -/
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

/-- Under an assumed pointwise negation equation, no value of Q equals
    the corresponding value of diagProg. The assumed equation is not a
    constructed self-referential program. -/
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
