/-
The theorem-level core of the bounded typed-translation result.

The natural-number counts are the exact finite witnesses used by the Python
census.  The statements do not promote the bounded carrier to an unbounded
translation theorem.
-/

namespace TypedTranslation

/-- One fixed rule block cannot balance both the no-instance witness and the
one-instance witness.  The same additions `left` and `right` occur in both
equations; state inspection is absent by hypothesis. -/
theorem memoryless_fixed_block_obstruction (left right : Nat)
    (noInstance : 1 + left = 1 + right)
    (oneInstance : 2 + left = 1 + right) : False := by
  omega

/-- A nonempty side-symmetric image contains at least two raw marks, so its
state-changing event count cannot equal the source form event's count of one. -/
theorem symmetric_form_cost_obstruction (left right : Nat)
    (symmetric : left = right) (nonempty : 0 < left + right) :
    left + right ≠ 1 := by
  omega

/-- The two source fields retained behind the projected observation. -/
structure Provenance where
  instanceBits : Bool × Bool
  ruleBit : Bool
  deriving DecidableEq

/-- Distinct retained instance or rule fields prevent state equality, even
when a separate projected observation happens to agree. -/
theorem retained_provenance_not_equal (left right : Provenance)
    (different : left.instanceBits ≠ right.instanceBits ∨ left.ruleBit ≠ right.ruleBit) :
    left ≠ right := by
  intro equal
  cases equal
  exact different.elim (fun h => h rfl) (fun h => h rfl)

end TypedTranslation
