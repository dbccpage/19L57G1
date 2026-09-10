/-!
# G001 Target-Class Charter — Constructive Specification

Pre-registers 9 independent adequacy criteria and their 4-way dimension
partition under the frozen status `TOE_TARGET_CLASS_FROZEN`.

Constructive Core: `#print axioms` strictly within `{propext, Quot.sound}`.
AuthorityEffect: None.
-/

namespace Charter

/-- The 9 independent adequacy criteria identifiers. -/
inductive CriterionID where
  | computational : CriterionID
  | reasoning : CriterionID
  | representational : CriterionID
  | foundational : CriterionID
  | physical : CriterionID
  | empirical : CriterionID
  | calculusUniqueness : CriterionID
  | physicalModelUniqueness : CriterionID
  | comparisonMorphisms : CriterionID
  deriving DecidableEq, Repr

/-- Canonical discrete indexing of criteria into natural numbers 0..8. -/
def CriterionID.toNat : CriterionID → Nat
  | .computational            => 0
  | .reasoning                => 1
  | .representational         => 2
  | .foundational             => 3
  | .physical                 => 4
  | .empirical                => 5
  | .calculusUniqueness       => 6
  | .physicalModelUniqueness  => 7
  | .comparisonMorphisms      => 8

/-- Index mapping is strictly injective. -/
theorem CriterionID.toNat_inj {a b : CriterionID} (h : a.toNat = b.toNat) : a = b := by
  cases a <;> cases b <;> first
  | rfl
  | contradiction

/-- The 4 overarching adequacy dimensions. -/
inductive Dimension where
  | computational : Dimension
  | mathematical  : Dimension
  | physical      : Dimension
  | empirical     : Dimension
  deriving DecidableEq, Repr

/-- Partition of the 9 criteria into the 4 foundational dimensions. -/
def CriterionID.dimension : CriterionID → Dimension
  | .computational            => Dimension.computational
  | .representational         => Dimension.computational
  | .reasoning                => Dimension.mathematical
  | .foundational             => Dimension.mathematical
  | .calculusUniqueness       => Dimension.mathematical
  | .physical                 => Dimension.physical
  | .physicalModelUniqueness  => Dimension.physical
  | .empirical                => Dimension.empirical
  | .comparisonMorphisms      => Dimension.empirical

/-- Exhaustive list of pre-registered criteria. -/
def allCriteria : List CriterionID := [
  CriterionID.computational,
  CriterionID.reasoning,
  CriterionID.representational,
  CriterionID.foundational,
  CriterionID.physical,
  CriterionID.empirical,
  CriterionID.calculusUniqueness,
  CriterionID.physicalModelUniqueness,
  CriterionID.comparisonMorphisms
]

theorem allCriteria_length : allCriteria.length = 9 := rfl

/-- Membership decidability on the pre-registered list. -/
theorem computational_mem_allCriteria : CriterionID.computational ∈ allCriteria := by
  decide

theorem reasoning_mem_allCriteria : CriterionID.reasoning ∈ allCriteria := by
  decide

theorem representational_mem_allCriteria : CriterionID.representational ∈ allCriteria := by
  decide

theorem foundational_mem_allCriteria : CriterionID.foundational ∈ allCriteria := by
  decide

theorem physical_mem_allCriteria : CriterionID.physical ∈ allCriteria := by
  decide

theorem empirical_mem_allCriteria : CriterionID.empirical ∈ allCriteria := by
  decide

theorem calculusUniqueness_mem_allCriteria : CriterionID.calculusUniqueness ∈ allCriteria := by
  decide

theorem physicalModelUniqueness_mem_allCriteria : CriterionID.physicalModelUniqueness ∈ allCriteria := by
  decide

theorem comparisonMorphisms_mem_allCriteria : CriterionID.comparisonMorphisms ∈ allCriteria := by
  decide

/-- The pre-registered list has pairwise distinct elements (no duplicates). -/
theorem allCriteria_nodup : allCriteria.Nodup := by
  decide

/-- Frozen charter record enforcing pre-registered status. -/
structure CharterRecord where
  frozen : Bool
  status : String
  criteriaCount : Nat

/-- Canonical frozen instance representing TOE_TARGET_CLASS_FROZEN. -/
def frozenCharter : CharterRecord := {
  frozen := true,
  status := "TOE_TARGET_CLASS_FROZEN",
  criteriaCount := 9
}

theorem frozenCharter_frozen : frozenCharter.frozen = true := rfl
theorem frozenCharter_count : frozenCharter.criteriaCount = 9 := rfl
theorem frozenCharter_status : frozenCharter.status = "TOE_TARGET_CLASS_FROZEN" := rfl

end Charter

#print axioms Charter.CriterionID.toNat_inj
#print axioms Charter.allCriteria_length
#print axioms Charter.computational_mem_allCriteria
#print axioms Charter.reasoning_mem_allCriteria
#print axioms Charter.representational_mem_allCriteria
#print axioms Charter.foundational_mem_allCriteria
#print axioms Charter.physical_mem_allCriteria
#print axioms Charter.empirical_mem_allCriteria
#print axioms Charter.calculusUniqueness_mem_allCriteria
#print axioms Charter.physicalModelUniqueness_mem_allCriteria
#print axioms Charter.comparisonMorphisms_mem_allCriteria
#print axioms Charter.allCriteria_nodup
#print axioms Charter.frozenCharter_frozen
#print axioms Charter.frozenCharter_count
#print axioms Charter.frozenCharter_status
