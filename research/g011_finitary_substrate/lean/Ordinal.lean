/-!
# Finitary Ordinals: Endogenous Inductive Foundation

Pure inductive construction of finite ordinals, identity, order, and arithmetic
without reliance on host Nat, host pointers, or host memory order.

AuthorityEffect: None.
Axiom boundary: strictly within {propext, Quot.sound}, zero Classical.choice, zero mathlib.
-/

namespace FinitarySubstrate

/-- Endogenous inductive ordinal: either zero or successor of an ordinal. -/
inductive Ordinal where
  | zero : Ordinal
  | succ : Ordinal → Ordinal
  deriving DecidableEq, Repr

namespace Ordinal

/-! ## 1. Identity and Distinctness -/

theorem zero_ne_succ (a : Ordinal) : zero ≠ succ a := by
  intro h
  nomatch h

theorem succ_ne_zero (a : Ordinal) : succ a ≠ zero := by
  intro h
  nomatch h

theorem succ_inj {a b : Ordinal} (h : succ a = succ b) : a = b := by
  cases h
  rfl

theorem succ_inj_iff (a b : Ordinal) : succ a = succ b ↔ a = b := by
  constructor
  · exact succ_inj
  · intro h; rw [h]

/-! ## 2. Order Relations -/

/-- Endogenous non-strict less-or-equal test. -/
def le : Ordinal → Ordinal → Bool
  | .zero, _ => true
  | .succ _, .zero => false
  | .succ a, .succ b => le a b

/-- Endogenous strict less-than test. -/
def lt (a b : Ordinal) : Bool := le (succ a) b

/-- Endogenous maximum of two ordinals. -/
def max (a b : Ordinal) : Ordinal :=
  bif le a b then b else a

theorem zero_le (a : Ordinal) : le zero a = true := by
  cases a <;> rfl

theorem le_refl (a : Ordinal) : le a a = true := by
  induction a with
  | zero => rfl
  | succ a ih => exact ih

theorem le_zero {a : Ordinal} (h : le a zero = true) : a = zero := by
  cases a with
  | zero => rfl
  | succ a => contradiction

theorem succ_le_succ {a b : Ordinal} : le (succ a) (succ b) = le a b := rfl

theorem le_succ_self (a : Ordinal) : le a (succ a) = true := by
  induction a with
  | zero => rfl
  | succ a ih => exact ih

theorem le_trans {a b c : Ordinal} (h1 : le a b = true) (h2 : le b c = true) : le a c = true := by
  induction a generalizing b c with
  | zero => exact zero_le c
  | succ a ih_a =>
      cases b with
      | zero => contradiction
      | succ b =>
          cases c with
          | zero => contradiction
          | succ c =>
              have h1' : le a b = true := h1
              have h2' : le b c = true := h2
              exact ih_a h1' h2'

theorem le_antisymm {a b : Ordinal} (h1 : le a b = true) (h2 : le b a = true) : a = b := by
  induction a generalizing b with
  | zero =>
      have hz : b = zero := le_zero h2
      exact hz.symm
  | succ a ih =>
      cases b with
      | zero => contradiction
      | succ b =>
          have h1' : le a b = true := h1
          have h2' : le b a = true := h2
          have hab : a = b := ih h1' h2'
          rw [hab]

theorem lt_irrefl (a : Ordinal) : lt a a = false := by
  induction a with
  | zero => rfl
  | succ a ih => exact ih

theorem lt_succ_self (a : Ordinal) : lt a (succ a) = true := le_refl (succ a)

theorem lt_trans {a b c : Ordinal} (h1 : lt a b = true) (h2 : lt b c = true) : lt a c = true := by
  -- lt a b means le (succ a) b
  -- lt b c means le (succ b) c
  -- le (succ a) (succ b) = le a b
  -- we know le (succ a) b = true, and le b (succ b) = true, so le (succ a) (succ b) = true
  have h_b_succ : le b (succ b) = true := le_succ_self b
  have h_succ_a_succ_b : le (succ a) (succ b) = true := le_trans h1 h_b_succ
  exact le_trans h_succ_a_succ_b h2

theorem not_le_and_lt {a b : Ordinal} (h1 : le a b = true) (h2 : lt b a = true) : False := by
  have h_circ : lt b b = true := by
    have h_le : le (succ b) b = true := le_trans h2 h1
    exact h_le
  have h_ir : lt b b = false := lt_irrefl b
  rw [h_ir] at h_circ
  contradiction

theorem trichotomy (a b : Ordinal) :
    (lt a b = true ∧ a ≠ b) ∨ (a = b ∧ lt a b = false ∧ lt b a = false) ∨ (lt b a = true ∧ a ≠ b) := by
  induction a generalizing b with
  | zero =>
      cases b with
      | zero =>
          right; left
          refine ⟨rfl, rfl, rfl⟩
      | succ b =>
          left
          refine ⟨zero_le b, zero_ne_succ b⟩
  | succ a ih =>
      cases b with
      | zero =>
          right; right
          refine ⟨zero_le a, succ_ne_zero a⟩
      | succ b =>
          cases ih b with
          | inl h =>
              left
              refine ⟨h.1, fun heq => h.2 (succ_inj heq)⟩
          | inr h =>
              cases h with
              | inl heq =>
                  right; left
                  have hab := heq.1
                  rw [hab]
                  refine ⟨rfl, lt_irrefl (succ b), lt_irrefl (succ b)⟩
              | inr hgt =>
                  right; right
                  refine ⟨hgt.1, fun heq => hgt.2 (succ_inj heq)⟩

theorem le_max_left (a b : Ordinal) : le a (max a b) = true := by
  change le a (bif le a b then b else a) = true
  cases h : le a b with
  | false =>
      change le a a = true
      exact le_refl a
  | true =>
      change le a b = true
      exact h

theorem le_max_right (a b : Ordinal) : le b (max a b) = true := by
  change le b (bif le a b then b else a) = true
  cases h : le a b with
  | true =>
      change le b b = true
      exact le_refl b
  | false =>
      change le b a = true
      cases htri : trichotomy a b with
      | inl hlt =>
          have h_le_a_b : le a b = true := le_trans (le_succ_self a) hlt.1
          rw [h] at h_le_a_b
          contradiction
      | inr hrest =>
          cases hrest with
          | inl heq =>
              rw [heq.1]
              exact le_refl b
          | inr hgt =>
              exact le_trans (le_succ_self b) hgt.1

/-! ## 3. Inductive Arithmetic -/

/-- Pure inductive addition: `0 + b = b`, `(succ a) + b = succ (a + b)`. -/
def add : Ordinal → Ordinal → Ordinal
  | .zero, b => b
  | .succ a, b => .succ (add a b)

/-- Pure inductive multiplication: `0 * b = 0`, `(succ a) * b = b + (a * b)`. -/
def mul : Ordinal → Ordinal → Ordinal
  | .zero, _ => .zero
  | .succ a, b => add b (mul a b)

/-- Predecessor: `pred 0 = 0`, `pred (succ a) = a`. -/
def pred : Ordinal → Ordinal
  | .zero => .zero
  | .succ a => a

/-- Truncated difference: `sub a 0 = a`, `sub 0 (succ b) = 0`, `sub (succ a) (succ b) = sub a b`. -/
def sub : Ordinal → Ordinal → Ordinal
  | a, .zero => a
  | .zero, .succ _ => .zero
  | .succ a, .succ b => sub a b

theorem add_zero (a : Ordinal) : add a zero = a := by
  induction a with
  | zero => rfl
  | succ a ih =>
      change succ (add a zero) = succ a
      rw [ih]

theorem add_succ (a b : Ordinal) : add a (succ b) = succ (add a b) := by
  induction a with
  | zero => rfl
  | succ a ih =>
      change succ (add a (succ b)) = succ (succ (add a b))
      rw [ih]

theorem add_assoc (a b c : Ordinal) : add (add a b) c = add a (add b c) := by
  induction a with
  | zero => rfl
  | succ a ih =>
      change succ (add (add a b) c) = succ (add a (add b c))
      rw [ih]

theorem add_comm (a b : Ordinal) : add a b = add b a := by
  induction a with
  | zero =>
      rw [add_zero]
      rfl
  | succ a ih =>
      change succ (add a b) = add b (succ a)
      rw [ih, add_succ]

theorem mul_zero (a : Ordinal) : mul a zero = zero := by
  induction a with
  | zero => rfl
  | succ a ih =>
      change add zero (mul a zero) = zero
      rw [ih]
      rfl

theorem mul_succ (a b : Ordinal) : mul a (succ b) = add a (mul a b) := by
  induction a with
  | zero => rfl
  | succ a ih =>
      change add (succ b) (mul a (succ b)) = add (succ a) (add b (mul a b))
      rw [ih]
      -- Goal: add (succ b) (add a (mul a b)) = succ (add a (add b (mul a b)))
      change succ (add b (add a (mul a b))) = succ (add a (add b (mul a b)))
      congr 1
      rw [← add_assoc b a (mul a b), add_comm b a, add_assoc a b (mul a b)]

theorem mul_add (a b c : Ordinal) : mul (add a b) c = add (mul a c) (mul b c) := by
  induction a with
  | zero => rfl
  | succ a ih =>
      change add c (mul (add a b) c) = add (add c (mul a c)) (mul b c)
      rw [ih]
      rw [add_assoc c (mul a c) (mul b c)]

theorem mul_assoc (a b c : Ordinal) : mul (mul a b) c = mul a (mul b c) := by
  induction a with
  | zero => rfl
  | succ a ih =>
      change mul (add b (mul a b)) c = add (mul b c) (mul a (mul b c))
      rw [mul_add, ih]

theorem mul_comm (a b : Ordinal) : mul a b = mul b a := by
  induction a with
  | zero =>
      rw [mul_zero]
      rfl
  | succ a ih =>
      change add b (mul a b) = mul b (succ a)
      rw [mul_succ, ih, add_comm]

theorem pred_zero : pred zero = zero := rfl

theorem pred_succ (a : Ordinal) : pred (succ a) = a := rfl

theorem sub_self (a : Ordinal) : sub a a = zero := by
  induction a with
  | zero => rfl
  | succ a ih => exact ih

theorem sub_zero (a : Ordinal) : sub a zero = a := by
  cases a <;> rfl

theorem sub_add_cancel (a b : Ordinal) : sub (add a b) b = a := by
  induction b generalizing a with
  | zero =>
      rw [add_zero, sub_zero]
  | succ b ih =>
      rw [add_succ]
      -- sub (succ (add a b)) (succ b) = sub (add a b) b
      change sub (add a b) b = a
      exact ih a

/-! ## 4. Structural Induction Principles -/

theorem ordinal_induction {P : Ordinal → Prop} (h0 : P zero) (hs : ∀ o, P o → P (succ o)) (o : Ordinal) : P o := by
  induction o with
  | zero => exact h0
  | succ o ih => exact hs o ih

end Ordinal

end FinitarySubstrate
