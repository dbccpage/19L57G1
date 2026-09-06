import BoundarySeed.Continuation1

/-!
# Continuation stage 2: null minima and a finite supply prefix

These are scoped apparatus theorems. Validity is a premise, never inferred
from supply inertia. The Python configuration and quotient correspondence
remain open. The concrete prefix is the declared index generator of stage 1.
-/

namespace BoundarySeed

def IsMinimumResponse {α : Type} (valid : α → Prop) (cost : α → Nat) (x : α) : Prop :=
  valid x ∧ ∀ y, valid y → cost x ≤ cost y

theorem zero_valid_is_minimum {α : Type} (valid : α → Prop) (cost : α → Nat)
    (z : α) (hv : valid z) (hc : cost z = 0) : IsMinimumResponse valid cost z := by
  constructor
  · exact hv
  · intro y _
    rw [hc]
    exact Nat.zero_le _

theorem minimum_has_zero_cost {α : Type} (valid : α → Prop) (cost : α → Nat)
    (z x : α) (hv : valid z) (hc : cost z = 0)
    (hm : IsMinimumResponse valid cost x) : cost x = 0 := by
  have h := hm.2 z hv
  rw [hc] at h
  exact Nat.le_zero.mp h

theorem unique_zero_is_only_minimum {α : Type} (valid : α → Prop) (cost : α → Nat)
    (z x : α) (hv : valid z) (hc : cost z = 0)
    (hz : ∀ y, cost y = 0 → y = z)
    (hm : IsMinimumResponse valid cost x) : x = z :=
  hz x (minimum_has_zero_cost valid cost z x hv hc hm)

theorem valid_null_is_not_no_response {α : Type} (valid : α → Prop)
    (z : α) (hv : valid z) : ¬ (∀ x, ¬ valid x) := by
  intro h
  exact h z hv

def nullSupplyRun : Nat → Regime → Regime
  | 0, state => state
  | n + 1, state => nullSupplyRun n (step state .supply)

theorem nullSupplyRun_preserves_state (n : Nat) (state : Regime) :
    nullSupplyRun n state = state := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [nullSupplyRun, step] using ih

def acceptedCount : List Bool → Nat
  | [] => 0
  | accepted :: rest => (if accepted then 1 else 0) + acceptedCount rest

theorem null_responses_accept_zero (n : Nat) :
    acceptedCount (List.replicate n false) = 0 := by
  induction n with
  | zero => rfl
  | succ n ih => simp [List.replicate_succ, acceptedCount, ih]

theorem attempts_can_exceed_accepted :
    (List.replicate 4 false).length = 4 ∧ acceptedCount (List.replicate 4 false) = 0 := by
  decide

def supplyPrefix : Nat → List Nat → List Nat
  | 0, _ => []
  | fuel + 1, record =>
    match firstMissing record domainSize with
    | none => []
    | some i => i :: supplyPrefix fuel (i :: record)

def recordAfterPrefix : Nat → List Nat → List Nat
  | 0, record => record
  | fuel + 1, record =>
    match firstMissing record domainSize with
    | none => record
    | some i => recordAfterPrefix fuel (i :: record)

theorem supplyPrefix_length_le (fuel : Nat) :
    ∀ record, (supplyPrefix fuel record).length ≤ fuel := by
  induction fuel with
  | zero => intro record; simp [supplyPrefix]
  | succ fuel ih =>
    intro record
    cases h : firstMissing record domainSize with
    | none => simp [supplyPrefix, h]
    | some i => simpa [supplyPrefix, h] using Nat.succ_le_succ (ih (i :: record))

theorem supplyPrefix_successor_census (fuel : Nat) (record : List Nat) (i : Nat)
    (h : firstMissing record domainSize = some i) :
    supplyPrefix (fuel + 1) record = i :: supplyPrefix fuel (i :: record) := by
  simp [supplyPrefix, h]

theorem supplyPrefix_first_four : supplyPrefix 4 presentedIndices = [2, 3, 4, 5] := rfl

theorem supplyPrefix_exact_frontier :
    firstMissing (recordAfterPrefix 4 presentedIndices) domainSize = some 6 := rfl

theorem supplyPrefix_frontier_is_not_exhaustion :
    firstMissing (recordAfterPrefix 4 presentedIndices) domainSize ≠ none := by
  rw [supplyPrefix_exact_frontier]
  simp

theorem stage2_root_budget : nodes 7 3 4 = 847 ∧ nodes 5 3 4 = 605 := by
  decide

end BoundarySeed
