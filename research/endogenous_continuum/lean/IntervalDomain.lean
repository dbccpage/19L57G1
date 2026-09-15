-- research/endogenous_continuum/lean/IntervalDomain.lean
-- Track 5: Overlapping Dyadic Intervals & Finite Overlap-Graph Connectedness
-- AuthorityEffect: None.

import InternalQuotienting

/-!
# Track 5: Overlapping Dyadic Intervals & Finite Overlap-Graph Connectedness

This module formalizes the Overlapping Dyadic Interval Domain:
1. `DyadicInterval`: Exact dyadic intervals ⟨scale, index⟩ representing
   the rational interval [index / 2^scale, (index + 2) / 2^scale] of width 2^{-(scale - 1)}.
2. `Overlaps`: Exact rational interior overlap via cross-multiplication.
3. `OverlappingChain`: Constructive path connectivity between overlapping intervals.
4. `canonical_cover_chain_connected`: Every pair of intervals at scale k is connected
   by an explicit constructive overlapping chain.
5. `discrete_boundary_witness` and `partition_boundary_overlap`: A finite binary
   cover-index partition with separated endpoints has an adjacent cross-label overlap.
6. `overlap_invariant_observable_constant`: Any observable that assigns equal
   values to overlapping intervals is constant across a same-scale chain.
7. `IntervalContractStep`: Locally confluent reduction of overlapping dyadic
   interval representations to irreducible canonical forms.
8. `refinement_children_chain_connected` and
   `left_refinement_images_chain_connected`: Explicit refinement children and
   left-child images remain connected in the finite overlap graph.

These results concern the declared finite overlap graph and contraction relation.
They do not define or prove connectedness of a point-set topology, an ordered-codomain
intermediate-value theorem, or an analytical/projective limit.

Axioms: strictly within {propext, Quot.sound}. Zero Mathlib.
-/

namespace IntervalDomain

set_option linter.unusedVariables false

-- ============================================================================
-- 1. Dyadic Interval Structure and Overlap
-- ============================================================================

/-- Exact dyadic interval `⟨scale, index⟩` representing `[index / 2^scale, (index + 2) / 2^scale]`.
    Every interval has width `2 / 2^scale = 1 / 2^{scale - 1}`. -/
structure DyadicInterval where
  scale : Nat
  index : Nat
  deriving DecidableEq, Repr

/-- Overlap relation for intervals at the same scale: indices differ by at most 1.
    For adjacent intervals `i` and `i + 1`, the overlapping interior is `[(i+1)/2^k, (i+2)/2^k]`,
    which has non-empty width `1 / 2^scale > 0`. -/
def OverlapsSameScale (I1 I2 : DyadicInterval) : Prop :=
  I1.scale = I2.scale ∧ I1.index ≤ I2.index + 1 ∧ I2.index ≤ I1.index + 1

instance (I1 I2 : DyadicInterval) : Decidable (OverlapsSameScale I1 I2) := by
  unfold OverlapsSameScale
  infer_instance

/-- General cross-scale overlap predicate via exact integer cross-multiplication:
    left1 * 2^scale2 < right2 * 2^scale1 ∧ left2 * 2^scale1 < right1 * 2^scale2. -/
def Overlaps (I1 I2 : DyadicInterval) : Prop :=
  I1.index * (2 ^ I2.scale) < (I2.index + 2) * (2 ^ I1.scale) ∧
  I2.index * (2 ^ I1.scale) < (I1.index + 2) * (2 ^ I2.scale)

instance (I1 I2 : DyadicInterval) : Decidable (Overlaps I1 I2) := by
  unfold Overlaps
  infer_instance

/-- Reflexivity of overlap: every interval overlaps itself. -/
theorem overlaps_refl (I : DyadicInterval) : Overlaps I I := by
  constructor
  · apply Nat.mul_lt_mul_of_pos_right
    · omega
    · apply Nat.two_pow_pos
  · apply Nat.mul_lt_mul_of_pos_right
    · omega
    · apply Nat.two_pow_pos

/-- Symmetry of overlap. -/
theorem overlaps_symm {I1 I2 : DyadicInterval} (h : Overlaps I1 I2) : Overlaps I2 I1 :=
  ⟨h.2, h.1⟩

/-- Adjacent intervals at the same scale have an overlapping interior. -/
theorem adjacent_overlaps (k i : Nat) : Overlaps ⟨k, i⟩ ⟨k, i + 1⟩ := by
  constructor
  · have h1 : i < (i + 1) + 2 := by omega
    have hpos : 0 < 2 ^ k := Nat.two_pow_pos k
    exact Nat.mul_lt_mul_of_pos_right h1 hpos
  · have h2 : i + 1 < i + 2 := by omega
    have hpos : 0 < 2 ^ k := Nat.two_pow_pos k
    exact Nat.mul_lt_mul_of_pos_right h2 hpos

/-- Overlap is reflexive at the same scale. -/
theorem overlaps_same_scale_refl (k i : Nat) : Overlaps ⟨k, i⟩ ⟨k, i⟩ :=
  overlaps_refl ⟨k, i⟩

-- ============================================================================
-- 2. Constructive Overlapping Chains
-- ============================================================================

/-- An overlapping chain connecting two intervals via a finite sequence of overlapping steps. -/
inductive OverlappingChain : DyadicInterval → DyadicInterval → Prop where
  | refl (I : DyadicInterval) : OverlappingChain I I
  | step {I1 I2 I3 : DyadicInterval} : Overlaps I1 I2 → OverlappingChain I2 I3 → OverlappingChain I1 I3

/-- Reflexivity of overlapping chains. -/
theorem overlappingChain_refl (I : DyadicInterval) : OverlappingChain I I :=
  OverlappingChain.refl I

/-- Transitivity of overlapping chains. -/
theorem overlappingChain_trans {I1 I2 I3 : DyadicInterval}
    (h12 : OverlappingChain I1 I2) (h23 : OverlappingChain I2 I3) :
    OverlappingChain I1 I3 := by
  induction h12 with
  | refl _ => exact h23
  | step h12' _ ih => exact OverlappingChain.step h12' (ih h23)

/-- A single overlap step forms a chain. -/
theorem overlappingChain_single {I1 I2 : DyadicInterval} (h : Overlaps I1 I2) :
    OverlappingChain I1 I2 :=
  OverlappingChain.step h (OverlappingChain.refl I2)

/-- Symmetry of overlapping chains. -/
theorem overlappingChain_symm {I1 I2 : DyadicInterval}
    (h : OverlappingChain I1 I2) : OverlappingChain I2 I1 := by
  induction h with
  | refl I => exact OverlappingChain.refl I
  | step hov _ ih =>
      exact overlappingChain_trans ih (overlappingChain_single (overlaps_symm hov))

/-- Helper lemma: forward chain across non-negative delta. -/
theorem chain_connected_delta (k i : Nat) : ∀ (d : Nat),
    OverlappingChain ⟨k, i⟩ ⟨k, i + d⟩
  | 0 => OverlappingChain.refl ⟨k, i⟩
  | d + 1 => by
      have hadj : Overlaps ⟨k, i + d⟩ ⟨k, i + (d + 1)⟩ := adjacent_overlaps k (i + d)
      have hstep : OverlappingChain ⟨k, i + d⟩ ⟨k, i + (d + 1)⟩ :=
        overlappingChain_single hadj
      exact overlappingChain_trans (chain_connected_delta k i d) hstep

/-- Forward chain between indices when `i ≤ j`. -/
theorem chain_connected_of_le (k i j : Nat) (hij : i ≤ j) :
    OverlappingChain ⟨k, i⟩ ⟨k, j⟩ := by
  obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hij
  exact chain_connected_delta k i d

/-- Canonical cover chain connectedness: any two intervals at scale `k` are connected
    by an explicit finite overlapping chain. -/
theorem canonical_cover_chain_connected (k i j : Nat) :
    OverlappingChain ⟨k, i⟩ ⟨k, j⟩ := by
  rcases Nat.le_total i j with hle | hge
  · exact chain_connected_of_le k i j hle
  · exact overlappingChain_symm (chain_connected_of_le k j i hge)

-- ============================================================================
-- 3. Finite Partition Boundary Overlap
-- ============================================================================

/-- Discrete boundary witness: any binary partition of `{0, ..., n + 1}` containing
    `0 ∈ A` and `(n + 1) ∈ B` must contain a transition pair `m ∈ A` and `(m + 1) ∈ B`. -/
theorem discrete_boundary_witness : ∀ (n : Nat),
    ∀ (A B : Nat → Prop) [∀ i, Decidable (A i)] [∀ i, Decidable (B i)],
    A 0 → B (n + 1) → (∀ i ≤ n + 1, A i ∨ B i) →
    ∃ m ≤ n, A m ∧ B (m + 1) := by
  intro n
  induction n with
  | zero =>
      intro A B _ _ hA0 hB1 _
      exact ⟨0, Nat.le_refl 0, hA0, hB1⟩
  | succ n ih =>
      intro A B _ _ hA0 hBsucc h_cover
      by_cases hBn : B (n + 1)
      · have h_subcover : ∀ i ≤ n + 1, A i ∨ B i := fun i hi =>
          h_cover i (Nat.le_trans hi (Nat.le_succ (n + 1)))
        obtain ⟨m, hm_le, hAm, hBm1⟩ := ih A B hA0 hBn h_subcover
        exact ⟨m, Nat.le_trans hm_le (Nat.le_succ n), hAm, hBm1⟩
      · have hAn : A (n + 1) := by
          rcases h_cover (n + 1) (Nat.le_succ (n + 1)) with hA | hB
          · exact hA
          · exact (hBn hB).elim
        exact ⟨n + 1, Nat.le_refl (n + 1), hAn, hBsucc⟩

/-- Boundary overlap: a binary cover-index partition with `0` in `A` and `n + 1`
    in `B` contains an adjacent `A`-to-`B` pair whose intervals overlap. -/
theorem partition_boundary_overlap (k n : Nat) (A B : Nat → Prop)
    [∀ i, Decidable (A i)] [∀ i, Decidable (B i)]
    (hA0 : A 0) (hBN : B (n + 1))
    (h_cover : ∀ i ≤ n + 1, A i ∨ B i) :
    ∃ m ≤ n, A m ∧ B (m + 1) ∧ Overlaps ⟨k, m⟩ ⟨k, m + 1⟩ := by
  obtain ⟨m, hm, hAm, hBm⟩ := discrete_boundary_witness n A B hA0 hBN h_cover
  exact ⟨m, hm, hAm, hBm, adjacent_overlaps k m⟩

-- ============================================================================
-- 4. Overlap-Invariant Observable Transport
-- ============================================================================

/-- Transport of an observable along an overlapping chain: any observable respecting
    local overlap is constant along any overlapping chain. -/
theorem observable_transport_chain {α : Type} (f : DyadicInterval → α)
    (h_resp : ∀ I1 I2, Overlaps I1 I2 → f I1 = f I2)
    {I1 I2 : DyadicInterval} (h_chain : OverlappingChain I1 I2) :
    f I1 = f I2 := by
  induction h_chain with
  | refl _ => rfl
  | step hov _ ih => exact (h_resp _ _ hov).trans ih

/-- Any observable assigning equal values to overlapping intervals is constant
    across all intervals at a fixed scale. -/
theorem overlap_invariant_observable_constant {α : Type} (f : DyadicInterval → α)
    (h_resp : ∀ I1 I2, Overlaps I1 I2 → f I1 = f I2)
    (k i j : Nat) :
    f ⟨k, i⟩ = f ⟨k, j⟩ :=
  observable_transport_chain f h_resp (canonical_cover_chain_connected k i j)

-- ============================================================================
-- 5. Scale Refinement
-- ============================================================================

/-- Scale refinement children: interval `⟨k, i⟩` refines into three overlapping
    intervals at scale `k + 1`: `⟨k+1, 2i⟩`, `⟨k+1, 2i+1⟩`, and `⟨k+1, 2i+2⟩`. -/
def refineChild0 (I : DyadicInterval) : DyadicInterval :=
  ⟨I.scale + 1, 2 * I.index⟩

def refineChild1 (I : DyadicInterval) : DyadicInterval :=
  ⟨I.scale + 1, 2 * I.index + 1⟩

def refineChild2 (I : DyadicInterval) : DyadicInterval :=
  ⟨I.scale + 1, 2 * I.index + 2⟩

/-- Refinement children are chain-connected at scale `k + 1`. -/
theorem refinement_children_chain_connected (I : DyadicInterval) :
    OverlappingChain (refineChild0 I) (refineChild2 I) := by
  have h01 : Overlaps (refineChild0 I) (refineChild1 I) :=
    adjacent_overlaps (I.scale + 1) (2 * I.index)
  have h12 : Overlaps (refineChild1 I) (refineChild2 I) := by
    have hadj := adjacent_overlaps (I.scale + 1) (2 * I.index + 1)
    have heq : 2 * I.index + 1 + 1 = 2 * I.index + 2 := by omega
    change Overlaps ⟨I.scale + 1, 2 * I.index + 1⟩ ⟨I.scale + 1, 2 * I.index + 2⟩
    exact heq ▸ hadj
  exact OverlappingChain.step h01 (OverlappingChain.step h12 (OverlappingChain.refl _))

/-- The left child overlaps the parent interval across scales. -/
theorem refine_child0_overlaps_parent (I : DyadicInterval) :
    Overlaps (refineChild0 I) I := by
  unfold refineChild0 Overlaps
  have hpos : 0 < 2 ^ I.scale := Nat.two_pow_pos I.scale
  have hpow : 2 ^ (I.scale + 1) = (2 ^ I.scale) * 2 := rfl
  rw [hpow]
  constructor
  · have hlt : (2 * I.index) * 2 ^ I.scale < (2 * I.index + 4) * 2 ^ I.scale :=
      Nat.mul_lt_mul_of_pos_right (by omega) hpos
    have heq_rhs : (I.index + 2) * (2 ^ I.scale * 2) = (2 * I.index + 4) * 2 ^ I.scale := by
      calc
        (I.index + 2) * (2 ^ I.scale * 2) = (I.index + 2) * (2 * 2 ^ I.scale) := by rw [Nat.mul_comm (2 ^ I.scale) 2]
        _ = ((I.index + 2) * 2) * 2 ^ I.scale := by rw [← Nat.mul_assoc]
        _ = (2 * I.index + 4) * 2 ^ I.scale := by
          have : (I.index + 2) * 2 = 2 * I.index + 4 := by omega
          rw [this]
    rw [heq_rhs]
    exact hlt
  · have hlt : (2 * I.index) * 2 ^ I.scale < (2 * I.index + 2) * 2 ^ I.scale :=
      Nat.mul_lt_mul_of_pos_right (by omega) hpos
    have heq_lhs : I.index * (2 ^ I.scale * 2) = (2 * I.index) * 2 ^ I.scale := by
      calc
        I.index * (2 ^ I.scale * 2) = I.index * (2 * 2 ^ I.scale) := by rw [Nat.mul_comm (2 ^ I.scale) 2]
        _ = (I.index * 2) * 2 ^ I.scale := by rw [← Nat.mul_assoc]
        _ = (2 * I.index) * 2 ^ I.scale := by rw [Nat.mul_comm I.index 2]
    rw [heq_lhs]
    exact hlt

/-- The middle child overlaps the parent interval across scales. -/
theorem refine_child1_overlaps_parent (I : DyadicInterval) :
    Overlaps (refineChild1 I) I := by
  unfold refineChild1 Overlaps
  have hpos : 0 < 2 ^ I.scale := Nat.two_pow_pos I.scale
  have hpow : 2 ^ (I.scale + 1) = (2 ^ I.scale) * 2 := rfl
  rw [hpow]
  constructor
  · have hlt : (2 * I.index + 1) * 2 ^ I.scale < (2 * I.index + 4) * 2 ^ I.scale :=
      Nat.mul_lt_mul_of_pos_right (by omega) hpos
    have heq_rhs : (I.index + 2) * (2 ^ I.scale * 2) = (2 * I.index + 4) * 2 ^ I.scale := by
      calc
        (I.index + 2) * (2 ^ I.scale * 2) = (I.index + 2) * (2 * 2 ^ I.scale) := by rw [Nat.mul_comm (2 ^ I.scale) 2]
        _ = ((I.index + 2) * 2) * 2 ^ I.scale := by rw [← Nat.mul_assoc]
        _ = (2 * I.index + 4) * 2 ^ I.scale := by
          have : (I.index + 2) * 2 = 2 * I.index + 4 := by omega
          rw [this]
    rw [heq_rhs]
    exact hlt
  · have hlt : (2 * I.index) * 2 ^ I.scale < (2 * I.index + 3) * 2 ^ I.scale :=
      Nat.mul_lt_mul_of_pos_right (by omega) hpos
    have heq_lhs : I.index * (2 ^ I.scale * 2) = (2 * I.index) * 2 ^ I.scale := by
      calc
        I.index * (2 ^ I.scale * 2) = I.index * (2 * 2 ^ I.scale) := by rw [Nat.mul_comm (2 ^ I.scale) 2]
        _ = (I.index * 2) * 2 ^ I.scale := by rw [← Nat.mul_assoc]
        _ = (2 * I.index) * 2 ^ I.scale := by rw [Nat.mul_comm I.index 2]
    have heq_rhs : (2 * I.index + 1 + 2) * 2 ^ I.scale = (2 * I.index + 3) * 2 ^ I.scale := by
      have : 2 * I.index + 1 + 2 = 2 * I.index + 3 := by omega
      rw [this]
    rw [heq_lhs, heq_rhs]
    exact hlt

/-- Left-child images of two same-scale intervals are connected at the refined scale. -/
theorem left_refinement_images_chain_connected (k i j : Nat) :
    OverlappingChain (refineChild0 ⟨k, i⟩) (refineChild0 ⟨k, j⟩) :=
  canonical_cover_chain_connected (k + 1) (2 * i) (2 * j)

-- ============================================================================
-- 6. Confluent Interval Rewriting of Overlapping Approximations
-- ============================================================================

/-- One-step confluent rewrite rule on dyadic intervals:
    Adjacent overlapping representations contract toward canonical minimal-index form. -/
inductive IntervalContractStep : DyadicInterval → DyadicInterval → Prop where
  | contract_succ (k i : Nat) :
      IntervalContractStep ⟨k, i + 1⟩ ⟨k, i⟩

/-- Reflexive-transitive closure of interval contraction. -/
def IntervalContractClosure := InternalQuotienting.ReflTransStep IntervalContractStep

/-- Single step contraction theorem. -/
theorem contract_step_single (k i : Nat) :
    IntervalContractClosure ⟨k, i + 1⟩ ⟨k, i⟩ :=
  InternalQuotienting.reflTransStep_single (IntervalContractStep.contract_succ k i)

/-- Local confluence of interval contraction: any two one-step divergences are joinable. -/
theorem interval_contract_locally_confluent :
    InternalQuotienting.IsLocallyConfluent IntervalContractStep := by
  intro x y1 y2 h1 h2
  cases h1 with
  | contract_succ k i =>
      cases h2 with
      | contract_succ _ _ =>
          exact ⟨(DyadicInterval.mk k i), InternalQuotienting.ReflTransStep.refl _, InternalQuotienting.ReflTransStep.refl _⟩

/-- Contraction to zero index is achievable for any interval at scale `k`. -/
theorem contract_to_zero (k i : Nat) :
    IntervalContractClosure ⟨k, i⟩ ⟨k, 0⟩ := by
  induction i with
  | zero =>
      exact InternalQuotienting.ReflTransStep.refl (DyadicInterval.mk k 0)
  | succ i ih =>
      exact InternalQuotienting.ReflTransStep.step (IntervalContractStep.contract_succ k i) ih

/-- Joinability of any two intervals at the same scale under interval contraction. -/
theorem intervals_same_scale_joinable (k i j : Nat) :
    InternalQuotienting.Joinable IntervalContractStep ⟨k, i⟩ ⟨k, j⟩ := by
  refine ⟨DyadicInterval.mk k 0, contract_to_zero k i, contract_to_zero k j⟩

/-- Scale is invariant under interval contraction steps. -/
theorem interval_contract_step_scale : ∀ {x y : DyadicInterval},
    IntervalContractStep x y → y.scale = x.scale
  | _, _, IntervalContractStep.contract_succ k i => rfl

/-- Scale is invariant under multi-step interval contraction. -/
theorem reflTrans_contract_scale : ∀ {x y : DyadicInterval},
    InternalQuotienting.ReflTransStep IntervalContractStep x y → y.scale = x.scale
  | x, _, InternalQuotienting.ReflTransStep.refl _ => rfl
  | x, z, InternalQuotienting.ReflTransStep.step hst htail => by
      have h1 := interval_contract_step_scale hst
      have h2 := reflTrans_contract_scale htail
      exact h2.trans h1

/-- Global confluence of interval contraction. -/
theorem interval_contract_confluent :
    InternalQuotienting.IsConfluent IntervalContractStep := by
  intro x y1 y2 hy1 hy2
  have h1 : y1.scale = x.scale := reflTrans_contract_scale hy1
  have h2 : y2.scale = x.scale := reflTrans_contract_scale hy2
  refine ⟨(⟨x.scale, 0⟩ : DyadicInterval), ?_, ?_⟩
  · have hy1_to_zero : InternalQuotienting.ReflTransStep IntervalContractStep ⟨y1.scale, y1.index⟩ ⟨y1.scale, 0⟩ :=
      contract_to_zero y1.scale y1.index
    have heq1 : (⟨y1.scale, y1.index⟩ : DyadicInterval) = y1 := by cases y1; rfl
    have heq2 : (⟨y1.scale, 0⟩ : DyadicInterval) = ⟨x.scale, 0⟩ := by rw [h1]
    exact heq1 ▸ heq2 ▸ hy1_to_zero
  · have hy2_to_zero : InternalQuotienting.ReflTransStep IntervalContractStep ⟨y2.scale, y2.index⟩ ⟨y2.scale, 0⟩ :=
      contract_to_zero y2.scale y2.index
    have heq1 : (⟨y2.scale, y2.index⟩ : DyadicInterval) = y2 := by cases y2; rfl
    have heq2 : (⟨y2.scale, 0⟩ : DyadicInterval) = ⟨x.scale, 0⟩ := by rw [h2]
    exact heq1 ▸ heq2 ▸ hy2_to_zero

/-- Endogenous equivalence on intervals coincides with joinability. -/
theorem interval_equivalence_iff_joinable (k i j : Nat) :
    InternalQuotienting.Eqv IntervalContractStep ⟨k, i⟩ ⟨k, j⟩ ↔
    InternalQuotienting.Joinable IntervalContractStep ⟨k, i⟩ ⟨k, j⟩ :=
  InternalQuotienting.eqv_iff_joinable IntervalContractStep interval_contract_confluent ⟨k, i⟩ ⟨k, j⟩

end IntervalDomain
