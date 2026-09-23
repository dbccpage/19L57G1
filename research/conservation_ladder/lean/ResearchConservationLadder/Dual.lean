/-!
# Exact first derivatives by dual numbers

AuthorityEffect: None.  A dual number over the integers is a pair
`re + du ε` with `ε² = 0`.  Polynomial expressions in numbered variables are
evaluated both over the integers and over dual numbers.  The directional
derivative `ddir` is defined by the sum and product rules, syntactically.

Proved here:

* `evalD_eq`: evaluating over dual numbers returns the integer value and,
  in the `ε` coefficient, exactly the directional derivative.  This is the
  only sense of differentiation used in this tree.
* `ddir_zero`, `ddir_add`, `ddir_smul`: the derivative is linear in the
  direction.

Nothing here uses limits, real numbers, or a library of algebra.
-/

namespace ResearchConservationLadder

/-- Dual numbers over the integers. -/
structure Dual where
  re : Int
  du : Int
deriving Repr, DecidableEq

namespace Dual

def add (a b : Dual) : Dual := ⟨a.re + b.re, a.du + b.du⟩
def mul (a b : Dual) : Dual := ⟨a.re * b.re, a.re * b.du + a.du * b.re⟩
def neg (a : Dual) : Dual := ⟨-a.re, -a.du⟩
def const (c : Int) : Dual := ⟨c, 0⟩

end Dual

/-- Polynomial expressions over the integers in variables `var 0, var 1, …`. -/
inductive Expr where
  | var (i : Nat)
  | const (c : Int)
  | add (a b : Expr)
  | mul (a b : Expr)
  | neg (a : Expr)
deriving Repr

namespace Expr

def sub (a b : Expr) : Expr := add a (neg b)
def sq (a : Expr) : Expr := mul a a

/-- Integer evaluation at an assignment `ρ`. -/
def eval (ρ : Nat → Int) : Expr → Int
  | var i => ρ i
  | const c => c
  | add a b => eval ρ a + eval ρ b
  | mul a b => eval ρ a * eval ρ b
  | neg a => -eval ρ a

/-- Dual-number evaluation at a dual assignment. -/
def evalD (σ : Nat → Dual) : Expr → Dual
  | var i => σ i
  | const c => Dual.const c
  | add a b => Dual.add (evalD σ a) (evalD σ b)
  | mul a b => Dual.mul (evalD σ a) (evalD σ b)
  | neg a => Dual.neg (evalD σ a)

/-- The directional derivative at `ρ` in direction `τ`, by the sum and
product rules. -/
def ddir (ρ τ : Nat → Int) : Expr → Int
  | var i => τ i
  | const _ => 0
  | add a b => ddir ρ τ a + ddir ρ τ b
  | mul a b => eval ρ a * ddir ρ τ b + ddir ρ τ a * eval ρ b
  | neg a => -ddir ρ τ a

/-- **Dual evaluation is exact differentiation.** -/
theorem evalD_eq (ρ τ : Nat → Int) (e : Expr) :
    evalD (fun i => ⟨ρ i, τ i⟩) e = ⟨eval ρ e, ddir ρ τ e⟩ := by
  induction e with
  | var i => rfl
  | const c => rfl
  | add a b iha ihb => simp only [evalD, iha, ihb, Dual.add, eval, ddir]
  | mul a b iha ihb => simp only [evalD, iha, ihb, Dual.mul, eval, ddir]
  | neg a iha => simp only [evalD, iha, Dual.neg, eval, ddir]

theorem ddir_zero (ρ : Nat → Int) (e : Expr) : ddir ρ (fun _ => 0) e = 0 := by
  induction e with
  | var i => rfl
  | const c => rfl
  | add a b iha ihb => simp only [ddir, iha, ihb, Int.add_zero]
  | mul a b iha ihb => simp only [ddir, iha, ihb, Int.mul_zero, Int.zero_mul, Int.add_zero]
  | neg a iha => simp only [ddir, iha, Int.neg_zero]

theorem ddir_add (ρ τ₁ τ₂ : Nat → Int) (e : Expr) :
    ddir ρ (fun i => τ₁ i + τ₂ i) e = ddir ρ τ₁ e + ddir ρ τ₂ e := by
  induction e with
  | var i => rfl
  | const c => rfl
  | add a b iha ihb => simp only [ddir, iha, ihb]; omega
  | mul a b iha ihb =>
      simp only [ddir, iha, ihb, Int.mul_add, Int.add_mul]; omega
  | neg a iha => simp only [ddir, iha]; omega

theorem ddir_smul (ρ τ : Nat → Int) (k : Int) (e : Expr) :
    ddir ρ (fun i => k * τ i) e = k * ddir ρ τ e := by
  induction e with
  | var i => rfl
  | const c => simp [ddir]
  | add a b iha ihb => simp only [ddir, iha, ihb, Int.mul_add]
  | mul a b iha ihb =>
      simp only [ddir, iha, ihb, Int.mul_add, Int.mul_left_comm, Int.mul_assoc]
  | neg a iha => simp only [ddir, iha, Int.mul_neg]

end Expr

end ResearchConservationLadder
