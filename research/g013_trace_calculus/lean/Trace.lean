/-!
# 0-cells (states), 1-cells (execution traces), and trace concatenation

Target G013: Coherent Trace Calculus & Higher Cell Algebra.
Constructive formalization in Lean 4 without Classical.choice or Mathlib.
AuthorityEffect: None.
-/

namespace G013TraceCalculus

/-- An elementary directed transition step between two 0-cells. -/
inductive Step (σ : Type) : σ → σ → Type where
  | mk (src dst : σ) (label : String) : Step σ src dst

/-- A 1-cell representing an execution trace as a sequence of chained steps. -/
inductive Trace (σ : Type) : σ → σ → Type where
  | nil (s : σ) : Trace σ s s
  | cons {s mid dst : σ} (step : Step σ s mid) (rest : Trace σ mid dst) : Trace σ s dst

/-- Concatenation of two 1-cells with matching endpoints: p : s -> mid, q : mid -> dst. -/
def concat {σ : Type} {s mid dst : σ} : Trace σ s mid → Trace σ mid dst → Trace σ s dst
  | .nil _, q => q
  | .cons st rest, q => .cons st (concat rest q)

/-- The length (step count) of a trace. -/
def length {σ : Type} {s dst : σ} : Trace σ s dst → Nat
  | .nil _ => 0
  | .cons _ rest => 1 + length rest

/-- The source 0-cell of a trace. -/
def sourceOf {σ : Type} {s dst : σ} (_ : Trace σ s dst) : σ := s

/-- The target 0-cell of a trace. -/
def targetOf {σ : Type} {s dst : σ} (_ : Trace σ s dst) : σ := dst

/-- Left identity law: nil * p = p. -/
theorem nil_concat {σ : Type} {s dst : σ} (p : Trace σ s dst) :
    concat (Trace.nil s) p = p :=
  rfl

/-- Right identity law: p * nil = p. -/
theorem concat_nil {σ : Type} {s dst : σ} (p : Trace σ s dst) :
    concat p (Trace.nil dst) = p := by
  induction p with
  | nil _ => rfl
  | cons st rest ih =>
    exact congrArg (Trace.cons st) ih

/-- Associativity of 1-cell composition: (p * q) * r = p * (q * r). -/
theorem concat_assoc {σ : Type} {s1 s2 s3 s4 : σ}
    (p : Trace σ s1 s2) (q : Trace σ s2 s3) (r : Trace σ s3 s4) :
    concat (concat p q) r = concat p (concat q r) := by
  induction p with
  | nil _ => rfl
  | cons st rest ih =>
    exact congrArg (Trace.cons st) (ih q)

/-- Length of an identity trace is zero. -/
theorem length_nil {σ : Type} (s : σ) :
    length (Trace.nil s) = 0 :=
  rfl

/-- Length is additive under trace concatenation. -/
theorem length_concat {σ : Type} {s mid dst : σ}
    (p : Trace σ s mid) (q : Trace σ mid dst) :
    length (concat p q) = length p + length q := by
  induction p with
  | nil _ =>
    change length q = 0 + length q
    rw [Nat.zero_add]
  | cons st rest ih =>
    change 1 + length (concat rest q) = (1 + length rest) + length q
    rw [ih]
    rw [Nat.add_assoc]

/-- Target of a concatenated trace is the target of the suffix. -/
theorem targetOf_concat {σ : Type} {s mid dst : σ}
    (p : Trace σ s mid) (q : Trace σ mid dst) :
    targetOf (concat p q) = targetOf q := by
  cases p with
  | nil _ => rfl
  | cons _ _ => rfl

/-- Source of a concatenated trace is the source of the prefix. -/
theorem sourceOf_concat {σ : Type} {s mid dst : σ}
    (p : Trace σ s mid) (q : Trace σ mid dst) :
    sourceOf (concat p q) = sourceOf p := by
  cases p with
  | nil _ => rfl
  | cons _ _ => rfl

end G013TraceCalculus
