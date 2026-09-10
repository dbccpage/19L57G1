import Trace
import HigherCell

/-!
# Additive price cocycles on traces and 2-cell homotopy price invariance

Target G013: Coherent Trace Calculus & Higher Cell Algebra.
Constructive formalization in Lean 4 without Classical.choice or Mathlib.
AuthorityEffect: None.
-/

namespace G013TraceCalculus

/-- A valuation assigner mapping elementary steps to non-negative costs. -/
def CostFun (σ : Type) := {src dst : σ} → Step σ src dst → Nat

/-- Total price valuation of an execution trace. -/
def tracePrice {σ : Type} (cost : CostFun σ) {s dst : σ} : Trace σ s dst → Nat
  | .nil _ => 0
  | .cons st rest => cost st + tracePrice cost rest

/-- Zero cost on identity 1-cells. -/
theorem price_nil_zero {σ : Type} (cost : CostFun σ) (s : σ) :
    tracePrice cost (Trace.nil s) = 0 :=
  rfl

/-- Cocycle additivity theorem:
The price of a concatenated trace is strictly the sum of the constituent trace prices:
  C(p * q) = C(p) + C(q). -/
theorem price_concat_additive {σ : Type} (cost : CostFun σ) {s mid dst : σ}
    (p : Trace σ s mid) (q : Trace σ mid dst) :
    tracePrice cost (concat p q) = tracePrice cost p + tracePrice cost q := by
  induction p with
  | nil _ =>
    change tracePrice cost q = 0 + tracePrice cost q
    rw [Nat.zero_add]
  | cons st rest ih =>
    change cost st + tracePrice cost (concat rest q) = (cost st + tracePrice cost rest) + tracePrice cost q
    rw [ih]
    rw [Nat.add_assoc]

/-- Left identity cancellation preserves trace price. -/
theorem price_id_left_invariance {σ : Type} (cost : CostFun σ) {s dst : σ} (p : Trace σ s dst) :
    tracePrice cost (concat (Trace.nil s) p) = tracePrice cost p :=
  rfl

/-- Right identity cancellation preserves trace price. -/
theorem price_id_right_invariance {σ : Type} (cost : CostFun σ) {s dst : σ} (p : Trace σ s dst) :
    tracePrice cost (concat p (Trace.nil dst)) = tracePrice cost p := by
  rw [concat_nil]

/-- Associativity preserves trace price. -/
theorem price_assoc_invariance {σ : Type} (cost : CostFun σ) {s1 s2 s3 s4 : σ}
    (p : Trace σ s1 s2) (q : Trace σ s2 s3) (r : Trace σ s3 s4) :
    tracePrice cost (concat (concat p q) r) = tracePrice cost (concat p (concat q r)) := by
  rw [concat_assoc]

/-- Commuting diamond homotopy invariance:
If the sum of costs along commuting branches coincides, the 2-cell preserves trace price. -/
theorem price_commute_invariance {σ : Type} (cost : CostFun σ) {s mid1 mid2 dst : σ}
    (st1 : Step σ s mid1) (st2 : Step σ mid1 dst)
    (st3 : Step σ s mid2) (st4 : Step σ mid2 dst)
    (h_cost : cost st1 + cost st2 = cost st3 + cost st4) :
    tracePrice cost (Trace.cons st1 (Trace.cons st2 (Trace.nil dst))) =
    tracePrice cost (Trace.cons st3 (Trace.cons st4 (Trace.nil dst))) := by
  change cost st1 + (cost st2 + 0) = cost st3 + (cost st4 + 0)
  rw [Nat.add_zero, Nat.add_zero]
  exact h_cost

/-- Horizontal composition preserves price equality:
If C(p1) = C(q1) and C(p2) = C(q2), then C(p1 * p2) = C(q1 * q2). -/
theorem price_h_comp_invariance {σ : Type} (cost : CostFun σ) {s1 s2 s3 : σ}
    {p1 q1 : Trace σ s1 s2} {p2 q2 : Trace σ s2 s3}
    (h1 : tracePrice cost p1 = tracePrice cost q1)
    (h2 : tracePrice cost p2 = tracePrice cost q2) :
    tracePrice cost (concat p1 p2) = tracePrice cost (concat q1 q2) := by
  rw [price_concat_additive, price_concat_additive, h1, h2]

/-- Vertical composition preserves price equality:
If C(p) = C(q) and C(q) = C(r), then C(p) = C(r). -/
theorem price_v_comp_invariance {σ : Type} (cost : CostFun σ) {s dst : σ}
    {p q r : Trace σ s dst}
    (h1 : tracePrice cost p = tracePrice cost q)
    (h2 : tracePrice cost q = tracePrice cost r) :
    tracePrice cost p = tracePrice cost r :=
  h1.trans h2

end G013TraceCalculus
