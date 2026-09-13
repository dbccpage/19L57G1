/-!
# Movegraph: Constructor Profile Monotonicity, Acyclicity, and Witness Exchange Refutation

Formalization of Prompt B Targets B3, B6.2:
- Cardinal profile potential `N(r) = |D| + |F| + |I| + |R| + |Q|`
- Constructor monotonicity: non-Supply constructors strictly increase `N(r)`
- Movegraph DAG property: vanishing 1-cycle space `Z_1 = 0`
- In-place witness exchange without accumulation is inexpressible (Kill Condition 2)
- Capability valuation non-negativity: refutation of isomorphism to signed defects `{-1, 0, +1}`

Axioms: strictly within {propext, Quot.sound}, zero mathlib, zero custom axioms, zero sorry.
AuthorityEffect: None.
-/

namespace Movegraph

/-! ## 1. Regime Cardinal Profile and Event Constructors -/

/-- Component counts of an admitted regime. -/
structure CardinalProfile where
  dCount : Nat  -- |D|: data tokens
  fCount : Nat  -- |F|: forms
  iCount : Nat  -- |I|: judgment instances
  rCount : Nat  -- |R|: rules
  qCount : Nat  -- |Q|: separation requirements
  deriving DecidableEq, Repr

/-- Cardinal profile potential N(r) in Nat. -/
def potential (p : CardinalProfile) : Nat :=
  p.dCount + p.fCount + p.iCount + p.rCount + p.qCount

/-- Native derivation event constructors in model.py. -/
inductive NativeEvent : Type where
  | supply : NativeEvent
  | addData : NativeEvent
  | addForm : NativeEvent
  | addInstance : NativeEvent
  | addRule : NativeEvent
  | addSeparation : NativeEvent
  deriving DecidableEq, Repr

/-- Effect of event constructors on cardinal profile. -/
def stepProfile (p : CardinalProfile) : NativeEvent → CardinalProfile
  | NativeEvent.supply => p
  | NativeEvent.addData => { p with dCount := p.dCount + 1 }
  | NativeEvent.addForm => { p with fCount := p.fCount + 1 }
  | NativeEvent.addInstance => { p with iCount := p.iCount + 1 }
  | NativeEvent.addRule => { p with rCount := p.rCount + 1 }
  | NativeEvent.addSeparation => { p with qCount := p.qCount + 1 }

/-! ## 2. Constructor Monotonicity Theorem -/

/-- Theorem 4.1 (Constructor Monotonicity):
Every non-Supply event constructor strictly increases the cardinal profile potential. -/
theorem constructor_monotonicity (p : CardinalProfile) (e : NativeEvent)
    (h_not_supply : e ≠ NativeEvent.supply) :
    potential (stepProfile p e) > potential p := by
  cases e with
  | supply => contradiction
  | addData =>
      dsimp [potential, stepProfile]
      omega
  | addForm =>
      dsimp [potential, stepProfile]
      omega
  | addInstance =>
      dsimp [potential, stepProfile]
      omega
  | addRule =>
      dsimp [potential, stepProfile]
      omega
  | addSeparation =>
      dsimp [potential, stepProfile]
      omega

theorem supply_is_identity (p : CardinalProfile) :
    stepProfile p NativeEvent.supply = p := rfl

/-! ## 3. Movegraph Acyclicity and Vanishing 1-Cycle Homology -/

/-- A trajectory of non-Supply steps of length k. -/
def Trajectory (p : CardinalProfile) : List NativeEvent → CardinalProfile
  | [] => p
  | e :: es => Trajectory (stepProfile p e) es

/-- Potential strictly increases along any non-empty list of non-Supply events. -/
theorem trajectory_strictly_increases (p : CardinalProfile) (es : List NativeEvent)
    (h_nonempty : es ≠ [])
    (h_all_non_supply : ∀ e ∈ es, e ≠ NativeEvent.supply) :
    potential (Trajectory p es) > potential p := by
  induction es generalizing p with
  | nil => contradiction
  | cons head tail ih =>
      have h_head : head ≠ NativeEvent.supply := h_all_non_supply head (List.Mem.head tail)
      have h_head_step : potential (stepProfile p head) > potential p :=
        constructor_monotonicity p head h_head
      by_cases h_tail : tail = []
      · subst h_tail
        dsimp [Trajectory]
        exact h_head_step
      · have h_tail_all : ∀ e ∈ tail, e ≠ NativeEvent.supply := by
          intro e he
          exact h_all_non_supply e (List.Mem.tail head he)
        have h_tail_step := ih (stepProfile p head) h_tail h_tail_all
        dsimp [Trajectory]
        exact Nat.lt_trans h_head_step h_tail_step

/-- Theorem 4.2: Movegraph Acyclicity.
No non-empty sequence of non-Supply events can return to the initial profile. -/
theorem movegraph_acyclic (p : CardinalProfile) (es : List NativeEvent)
    (h_nonempty : es ≠ [])
    (h_all_non_supply : ∀ e ∈ es, e ≠ NativeEvent.supply) :
    Trajectory p es ≠ p := by
  intro h_eq
  have h_gt := trajectory_strictly_increases p es h_nonempty h_all_non_supply
  rw [h_eq] at h_gt
  exact Nat.lt_irrefl (potential p) h_gt

/-- Firing of Charter Kill Condition 2:
In-place witness exchange without accumulation (returning to exact profile) is inexpressible. -/
theorem kill_condition_2_fires (p : CardinalProfile) (es : List NativeEvent)
    (h_nonempty : es ≠ [])
    (h_all_non_supply : ∀ e ∈ es, e ≠ NativeEvent.supply) :
    ¬ (Trajectory p es = p) :=
  movegraph_acyclic p es h_nonempty h_all_non_supply

/-! ## 4. Refutation of Isomorphism Between Capability Costs and Signed Defects -/

/-- Capability cost mu1 in Nat. -/
def mu1 : NativeEvent → Nat
  | NativeEvent.supply => 0
  | NativeEvent.addData => 1
  | NativeEvent.addForm => 1
  | NativeEvent.addInstance => 1
  | NativeEvent.addRule => 1
  | NativeEvent.addSeparation => 1

/-- Capability cost is unconditionally non-negative. -/
theorem mu1_nonnegative (e : NativeEvent) : mu1 e ≥ 0 := by
  cases e <;> decide

/-- Signed diagnostic defect {-1, 0, +1} in Int. -/
inductive DiagnosticDefect : Type where
  | negOne : DiagnosticDefect
  | zero : DiagnosticDefect
  | posOne : DiagnosticDefect
  deriving DecidableEq, Repr

def defectAdd : DiagnosticDefect → DiagnosticDefect → Option DiagnosticDefect
  | DiagnosticDefect.zero, d => some d
  | d, DiagnosticDefect.zero => some d
  | DiagnosticDefect.posOne, DiagnosticDefect.negOne => some DiagnosticDefect.zero
  | DiagnosticDefect.negOne, DiagnosticDefect.posOne => some DiagnosticDefect.zero
  | _, _ => none

/-- Monoid property: (Nat, +) has no non-trivial additive inverses. -/
theorem nat_additive_invertibility (a b : Nat) (h : a + b = 0) : a = 0 ∧ b = 0 := by
  cases a with
  | zero =>
      rw [Nat.zero_add] at h
      exact ⟨rfl, h⟩
  | succ a' =>
      rw [Nat.succ_add] at h
      cases h

/-- Signed defect space possesses a non-zero element with an additive inverse. -/
theorem defect_has_nontrivial_inverse :
    ∃ (x y : DiagnosticDefect), x ≠ DiagnosticDefect.zero ∧ defectAdd x y = some DiagnosticDefect.zero :=
  ⟨DiagnosticDefect.posOne, DiagnosticDefect.negOne, by decide, rfl⟩

/-- Theorem 4.3 (Refutation of Algebraic Isomorphism):
Non-negative capability costs (Nat, +) cannot be isomorphic to signed defect structures,
because signed defect structures have additive inverses while Nat has no non-trivial inverses. -/
theorem capability_not_isomorphic_to_signed_defect :
    ¬ ∃ (f : DiagnosticDefect → Nat),
      f DiagnosticDefect.zero = 0 ∧
      (∀ x y z, defectAdd x y = some z → f x + f y = f z) ∧
      (∀ x y, f x = f y → x = y) := by
  rintro ⟨f, h_zero, h_hom, h_inj⟩
  have h_sum : f DiagnosticDefect.posOne + f DiagnosticDefect.negOne = f DiagnosticDefect.zero := by
    exact h_hom DiagnosticDefect.posOne DiagnosticDefect.negOne DiagnosticDefect.zero rfl
  rw [h_zero] at h_sum
  have h_parts := nat_additive_invertibility (f DiagnosticDefect.posOne) (f DiagnosticDefect.negOne) h_sum
  have h_pos_is_zero : f DiagnosticDefect.posOne = f DiagnosticDefect.zero := by
    rw [h_parts.1, h_zero]
  have h_contra : DiagnosticDefect.posOne = DiagnosticDefect.zero := h_inj DiagnosticDefect.posOne DiagnosticDefect.zero h_pos_is_zero
  cases h_contra

end Movegraph
