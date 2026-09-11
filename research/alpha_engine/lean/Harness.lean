import Derivation.Basic

/-!
Local proposal-evaluation-authorization harness.  Not a sealed
object-language development.

`License` is a metatheoretic record, not an `Event`.  `SearchPolicy`
output is a subset of the retained key set.  Uniqueness of a minimum
does not apply it.  Evaluation returns an `EvalResult` and performs
no admission.  These lemmas are about this harness; they do not prove
equivalence to `code/derivation/`.

AuthorityEffect: None.
-/

namespace Harness

open Derivation

/-- Identifier for a retained iso class in this harness.  Not a sealed
canonical-key theorem. -/
abbrev CanonKey := Nat

structure Proposal where
  token : Nat
  offerings : List (List Item)

structure RetainedClass where
  key : CanonKey
  members : List (List Item)

structure EvalResult where
  measure : Nat
  cost : Option (Nat × Nat)
  rawMinima : List (List Item)
  retained : List RetainedClass
  found : Bool

/-- Metatheoretic authorization record.  Not an `Event`.  No revoke
field.  No integer class selector. -/
structure License where
  granter : Nat
  scope : Nat
  authorized : List CanonKey

structure Node where
  history : List Event
  regime : Regime
  license : Option License

structure SearchPolicy where
  retained : List CanonKey
  explored : List CanonKey
  pruned : List CanonKey
  openKeys : List CanonKey

/-- A constructor outside the six sealed `Event` kinds.  Not added to
`Event`. -/
inductive ExtraCtor where
  | mk (tag : Nat)

/-- Grade stamps of the Python fold.  None of them is a `License`. -/
inductive GradeStamp where
  | tie
  | uniqueClass
  | uniqueDelta
  | noneStamp

/-! ## List helpers for the declared take-1 policy -/

theorem mem_of_mem_take {α : Type} {x : α} :
    ∀ (n : Nat) (l : List α), x ∈ List.take n l → x ∈ l
  | 0, _l, h => by cases h
  | _n + 1, [], h => by cases h
  | n + 1, y :: ys, h => by
      cases h with
      | head => exact List.Mem.head _
      | tail _ ht => exact List.Mem.tail _ (mem_of_mem_take n ys ht)

theorem mem_of_mem_drop {α : Type} {x : α} :
    ∀ (n : Nat) (l : List α), x ∈ List.drop n l → x ∈ l
  | 0, _l, h => h
  | _n + 1, [], h => by cases h
  | n + 1, y :: ys, h =>
      List.Mem.tail _ (mem_of_mem_drop n ys h)

theorem declared_first_length (retained : List CanonKey) :
    (retained.take 1).length + (retained.drop 1).length = retained.length := by
  cases retained with
  | nil => rfl
  | cons _k rest =>
      rw [List.take_succ_cons (i := 0), List.take_zero,
          List.drop_succ_cons (i := 0), List.drop_zero]
      change Nat.succ 0 + rest.length = rest.length + Nat.succ 0
      exact Nat.add_comm (Nat.succ 0) rest.length

/-! ## Proposal is Supply-shaped; evaluation performs no admission -/

def present (r : Regime) (_p : Proposal) : Regime := r

theorem present_leaves_regime (r : Regime) (p : Proposal) :
    present r p = r := rfl

def asAdmit (_p : Proposal) : Option Event := none

theorem proposal_is_not_admit (p : Proposal) : asAdmit p = none := rfl

/-- Pair projection: evaluation in this harness is `(base, eval base target)`.
Not a theorem about the Python `evaluate` function. -/
def runEval (base : Regime) (target : Nat × Nat)
    (eval : Regime → Nat × Nat → EvalResult) : Regime × EvalResult :=
  (base, eval base target)

theorem evaluation_does_not_admit
    (base : Regime) (target : Nat × Nat)
    (eval : Regime → Nat × Nat → EvalResult) :
    (runEval base target eval).1 = base := rfl

def eventsOfEval (_result : EvalResult) : List Event := []

theorem eval_carries_no_events (result : EvalResult) :
    eventsOfEval result = [] := rfl

/-! ## License is not Event -/

def asEvent (_lic : License) : Option Event := none

theorem license_is_not_event (lic : License) : asEvent lic = none := rfl

def extraAsEvent (_e : ExtraCtor) : Option Event := none

theorem extra_ctor_refused (e : ExtraCtor) : extraAsEvent e = none := rfl

def licenseFromGrade (_g : GradeStamp) : Option License := none

theorem grade_stamp_is_not_license (g : GradeStamp) :
    licenseFromGrade g = none := rfl

/-! ## SearchPolicy: explored is a subset of retained -/

def censusOk (p : SearchPolicy) : Prop :=
  (∀ k, k ∈ p.explored → k ∈ p.retained) ∧
  (∀ k, k ∈ p.pruned → k ∈ p.retained) ∧
  (∀ k, k ∈ p.openKeys → k ∈ p.retained) ∧
  p.explored.length + p.pruned.length + p.openKeys.length = p.retained.length

def declaredExploreFirst (retained : List CanonKey) : SearchPolicy :=
  { retained := retained
    explored := retained.take 1
    pruned := []
    openKeys := retained.drop 1 }

theorem declaredExploreFirst_censusOk (retained : List CanonKey) :
    censusOk (declaredExploreFirst retained) := by
  refine ⟨?exp, ?prn, ?opn, ?sum⟩
  · intro k hk
    exact mem_of_mem_take 1 retained hk
  · intro k hk
    cases hk
  · intro k hk
    exact mem_of_mem_drop 1 retained hk
  · exact declared_first_length retained

theorem policy_explored_subset (p : SearchPolicy) (h : censusOk p) :
    ∀ k, k ∈ p.explored → k ∈ p.retained :=
  h.1

theorem fabricated_not_explored
    (p : SearchPolicy) (k : CanonKey)
    (h : censusOk p) (hn : k ∉ p.retained) : k ∉ p.explored :=
  fun hin => hn (h.1 k hin)

/-! ## Uniqueness does not apply; denial writes no license -/

def isUnique (result : EvalResult) : Prop :=
  result.found = true ∧
  result.retained.length = 1 ∧
  result.rawMinima.length = 1

def applyUnique (_n : Node) (_result : EvalResult) : Option Node := none

theorem uniqueness_does_not_apply (n : Node) (result : EvalResult)
    (_h : isUnique result) : applyUnique n result = none := rfl

def applyLicensed (n : Node) (lic : License) (key : CanonKey) : Option Node :=
  if lic.authorized.contains key then
    some { n with license := some lic }
  else
    none

theorem denied_license_eq_none (n : Node) (lic : License) (key : CanonKey)
    (h : lic.authorized.contains key = false) :
    applyLicensed n lic key = none := by
  unfold applyLicensed
  rw [h, if_neg Bool.false_ne_true]

def keyByIndex (_retained : List CanonKey) (_index : Nat) : Option CanonKey :=
  none

theorem keyByIndex_refused (retained : List CanonKey) (index : Nat) :
    keyByIndex retained index = none := rfl

def leftoverAsDemand (_pairs : List (Nat × Nat)) : Option (Nat × Nat) := none

theorem leftover_is_not_demand (pairs : List (Nat × Nat)) :
    leftoverAsDemand pairs = none := rfl

end Harness

#print axioms Harness.mem_of_mem_take
#print axioms Harness.mem_of_mem_drop
#print axioms Harness.declared_first_length
#print axioms Harness.present_leaves_regime
#print axioms Harness.proposal_is_not_admit
#print axioms Harness.evaluation_does_not_admit
#print axioms Harness.eval_carries_no_events
#print axioms Harness.license_is_not_event
#print axioms Harness.extra_ctor_refused
#print axioms Harness.grade_stamp_is_not_license
#print axioms Harness.declaredExploreFirst_censusOk
#print axioms Harness.policy_explored_subset
#print axioms Harness.fabricated_not_explored
#print axioms Harness.uniqueness_does_not_apply
#print axioms Harness.denied_license_eq_none
#print axioms Harness.keyByIndex_refused
#print axioms Harness.leftover_is_not_demand
