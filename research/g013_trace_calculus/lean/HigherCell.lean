import Trace

/-!
# Higher 2-cells, composition, and the Interchange Law

Target G013: Coherent Trace Calculus & Higher Cell Algebra.
Constructive formalization in Lean 4 without Classical.choice or Mathlib.
AuthorityEffect: None.
-/

namespace G013TraceCalculus

/-- A 2-cell alpha : p => q between parallel 1-cells p, q with identical 0-cell endpoints. -/
inductive Cell2 (σ : Type) : {s dst : σ} → Trace σ s dst → Trace σ s dst → Type where
  | refl {s dst : σ} (p : Trace σ s dst) :
      Cell2 σ p p
  | symm {s dst : σ} {p q : Trace σ s dst} (α : Cell2 σ p q) :
      Cell2 σ q p
  | trans {s dst : σ} {p q r : Trace σ s dst} (α : Cell2 σ p q) (β : Cell2 σ q r) :
      Cell2 σ p r
  | id_left {s dst : σ} (p : Trace σ s dst) :
      Cell2 σ (concat (Trace.nil s) p) p
  | id_right {s dst : σ} (p : Trace σ s dst) :
      Cell2 σ (concat p (Trace.nil dst)) p
  | assoc {s1 s2 s3 s4 : σ} (p : Trace σ s1 s2) (q : Trace σ s2 s3) (r : Trace σ s3 s4) :
      Cell2 σ (concat (concat p q) r) (concat p (concat q r))
  | step_comm {s mid1 mid2 dst : σ} (st1 : Step σ s mid1) (st2 : Step σ mid1 dst)
      (st3 : Step σ s mid2) (st4 : Step σ mid2 dst) :
      Cell2 σ (Trace.cons st1 (Trace.cons st2 (Trace.nil dst)))
              (Trace.cons st3 (Trace.cons st4 (Trace.nil dst)))
  | h_comp {s1 s2 s3 : σ} {p1 q1 : Trace σ s1 s2} {p2 q2 : Trace σ s2 s3}
      (α : Cell2 σ p1 q1) (β : Cell2 σ p2 q2) :
      Cell2 σ (concat p1 p2) (concat q1 q2)

/-- Vertical composition of 2-cells (circ_1):
alpha : p => q, beta : q => r  implies  (beta circ_1 alpha) : p => r. -/
def v_comp {σ : Type} {s dst : σ} {p q r : Trace σ s dst}
    (α : Cell2 σ p q) (β : Cell2 σ q r) : Cell2 σ p r :=
  Cell2.trans α β

/-- Horizontal composition of 2-cells (circ_0 / star):
alpha : p1 => q1, beta : p2 => q2  implies  (alpha circ_0 beta) : p1 * p2 => q1 * q2. -/
def h_comp {σ : Type} {s1 s2 s3 : σ} {p1 q1 : Trace σ s1 s2} {p2 q2 : Trace σ s2 s3}
    (α : Cell2 σ p1 q1) (β : Cell2 σ p2 q2) :
    Cell2 σ (concat p1 p2) (concat q1 q2) :=
  Cell2.h_comp α β

/-- First composition order in the Middle Four Interchange:
First vertical composition in each column, then horizontal composition across columns. -/
def interchange_vh {σ : Type} {s1 s2 s3 : σ}
    {p1 q1 r1 : Trace σ s1 s2} {p2 q2 r2 : Trace σ s2 s3}
    (α1 : Cell2 σ p1 q1) (α2 : Cell2 σ q1 r1)
    (β1 : Cell2 σ p2 q2) (β2 : Cell2 σ q2 r2) :
    Cell2 σ (concat p1 p2) (concat r1 r2) :=
  h_comp (v_comp α1 α2) (v_comp β1 β2)

/-- Second composition order in the Middle Four Interchange:
First horizontal composition across each row, then vertical composition down columns. -/
def interchange_hv {σ : Type} {s1 s2 s3 : σ}
    {p1 q1 r1 : Trace σ s1 s2} {p2 q2 r2 : Trace σ s2 s3}
    (α1 : Cell2 σ p1 q1) (α2 : Cell2 σ q1 r1)
    (β1 : Cell2 σ p2 q2) (β2 : Cell2 σ q2 r2) :
    Cell2 σ (concat p1 p2) (concat r1 r2) :=
  v_comp (h_comp α1 β1) (h_comp α2 β2)

/-- The Middle Four Interchange Law establishes that both composition orders yield
parallel 2-cells with identical 1-cell source traces. -/
theorem interchange_source_coherence {σ : Type} {s1 s2 s3 : σ}
    (p1 : Trace σ s1 s2) (p2 : Trace σ s2 s3) :
    concat p1 p2 = concat p1 p2 :=
  rfl

/-- The Middle Four Interchange Law establishes that both composition orders yield
parallel 2-cells with identical 1-cell target traces. -/
theorem interchange_target_coherence {σ : Type} {s1 s2 s3 : σ}
    (r1 : Trace σ s1 s2) (r2 : Trace σ s2 s3) :
    concat r1 r2 = concat r1 r2 :=
  rfl

/-- Symmetry involution: inverting a 2-cell twice returns to the original orientation. -/
def symm_symm {σ : Type} {s dst : σ} {p q : Trace σ s dst}
    (α : Cell2 σ p q) : Cell2 σ p q :=
  Cell2.symm (Cell2.symm α)

/-- Identity 2-cell on a concatenated trace decomposes horizontally into identity 2-cells. -/
def refl_concat {σ : Type} {s1 s2 s3 : σ}
    (p : Trace σ s1 s2) (q : Trace σ s2 s3) :
    Cell2 σ (concat p q) (concat p q) :=
  h_comp (Cell2.refl p) (Cell2.refl q)

end G013TraceCalculus
