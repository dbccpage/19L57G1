-- research/endogenous_continuum/lean/AdaptiveBudget.lean
-- Track 8: Allocation Conservation & Bounded Execution Arithmetic
-- AuthorityEffect: None.

import DualCertificate

namespace AdaptiveBudget

open ProjectiveSystem
open DualCertificate

set_option linter.unusedVariables false

-- ============================================================================
-- 1. Candidate Targets & Budget State
-- ============================================================================

/-- An active candidate exploration target with an allocated budget and priority. -/
structure CandidateTarget (V : Type) where
  id : Nat
  src : V
  dst : V
  allocatedBudget : Nat
  priority : Nat

/-- Cumulative sum of allocated budgets across a list of active candidates. -/
def sumAllocated {V : Type} : List (CandidateTarget V) → Nat
  | [] => 0
  | c :: cs => c.allocatedBudget + sumAllocated cs

/-- Allocation state before consumption is represented separately. -/
structure BudgetState (V : Type) where
  totalBudget : Nat
  unallocatedBudget : Nat
  activeCandidates : List (CandidateTarget V)

/-- Natural-number allocation conservation invariant (no consumed field):
    `totalBudget = unallocatedBudget + sumAllocated activeCandidates`. -/
def PreservesBudgetConservation {V : Type} (st : BudgetState V) : Prop :=
  st.totalBudget = st.unallocatedBudget + sumAllocated st.activeCandidates

-- ============================================================================
-- 2. Budget Conservation Invariants & Proofs
-- ============================================================================

/-- Empty candidate list has zero allocated budget. -/
theorem sumAllocated_nil {V : Type} :
    sumAllocated ([] : List (CandidateTarget V)) = 0 := by
  rfl

/-- Cons distributes allocated budget additively. -/
theorem sumAllocated_cons {V : Type} (c : CandidateTarget V) (cs : List (CandidateTarget V)) :
    sumAllocated (c :: cs) = c.allocatedBudget + sumAllocated cs := by
  rfl

/-- Initial budget state with all funds in `unallocatedBudget` preserves conservation. -/
theorem budget_conservation_init {V : Type} (B : Nat) :
    PreservesBudgetConservation (BudgetState.mk (V := V) B B []) := by
  dsimp [PreservesBudgetConservation, sumAllocated]

/-- Allocating a budget slice `b ≤ st.unallocatedBudget` to a new candidate preserves conservation. -/
theorem allocation_preserves_conservation {V : Type} (st : BudgetState V)
    (h_cons : PreservesBudgetConservation st)
    (b : Nat) (h_le : b ≤ st.unallocatedBudget)
    (new_c : CandidateTarget V) (h_b : new_c.allocatedBudget = b) :
    PreservesBudgetConservation (BudgetState.mk
      st.totalBudget
      (st.unallocatedBudget - b)
      (new_c :: st.activeCandidates)) := by
  dsimp [PreservesBudgetConservation, sumAllocated]
  rw [h_b]
  have h_orig : st.totalBudget = st.unallocatedBudget + sumAllocated st.activeCandidates := h_cons
  omega

/-- Reclaiming the allocated budget of a candidate (e.g. upon certified refusal) preserves conservation. -/
theorem reclaim_refused_preserves_conservation {V : Type} (st : BudgetState V)
    (h_cons : PreservesBudgetConservation st)
    (c : CandidateTarget V) (cs : List (CandidateTarget V))
    (h_active : st.activeCandidates = c :: cs) :
    PreservesBudgetConservation (BudgetState.mk
      st.totalBudget
      (st.unallocatedBudget + c.allocatedBudget)
      cs) := by
  dsimp [PreservesBudgetConservation, sumAllocated]
  have h_orig : st.totalBudget = st.unallocatedBudget + sumAllocated st.activeCandidates := h_cons
  rw [h_active] at h_orig
  dsimp [sumAllocated] at h_orig
  omega

/-- Redistributing unallocated budget across two active candidate slices preserves conservation. -/
theorem redistribute_preserves_conservation {V : Type} (st : BudgetState V)
    (h_cons : PreservesBudgetConservation st)
    (b1 b2 : Nat) (h_split : b1 + b2 ≤ st.unallocatedBudget)
    (c1 c2 : CandidateTarget V)
    (h1 : c1.allocatedBudget = b1)
    (h2 : c2.allocatedBudget = b2) :
    PreservesBudgetConservation (BudgetState.mk
      st.totalBudget
      (st.unallocatedBudget - (b1 + b2))
      (c1 :: c2 :: st.activeCandidates)) := by
  dsimp [PreservesBudgetConservation, sumAllocated]
  rw [h1, h2]
  have h_orig : st.totalBudget = st.unallocatedBudget + sumAllocated st.activeCandidates := h_cons
  omega

-- ============================================================================
-- 3. Soundness of Budget Reclamation under Certified Refusal
-- ============================================================================

/-- Conditional refusal bound for one supplied fine path. The conclusion needs
    the explicit lifted-admissibility hypothesis `h_adm`; this theorem does not
    establish that hypothesis for an executable coarsening map. -/
theorem reclaimed_refusal_completeness {V_fine V_coarse : Type}
    (π : V_fine → V_coarse) (y_coarse : V_coarse → Nat)
    (c : CandidateTarget V_fine)
    (h_refusal : y_coarse (π c.dst) > y_coarse (π c.src) + c.allocatedBudget)
    (p_fine : Path V_fine c.src c.dst)
    (h_adm : IsAdmissiblePath (liftDualPotential π y_coarse) p_fine) :
    pathCost p_fine > c.allocatedBudget := by
  exact hierarchical_refusal_soundness π y_coarse c.allocatedBudget h_refusal p_fine h_adm

-- ============================================================================
-- 4. Monotonic Budget Consumption and Bounded Agent Termination
-- ============================================================================

/-- Monotonic budget consumption:
    Executing an operational transition with positive cost `cost ≥ 1` strictly decreases
    remaining budget, preventing infinite zero-cost cycles. -/
theorem monotone_budget_consumption (b cost : Nat) (h_pos : cost ≥ 1) (h_le : cost ≤ b) :
    b - cost < b := by
  omega

/-- If a unit-per-step accounting equation writes `B = steps + remaining`,
    then the number of recorded steps is at most `B`. -/
theorem finite_exploration_bound (B steps remaining : Nat)
    (h_account : B = steps + remaining) :
    steps ≤ B := by
  omega

end AdaptiveBudget
