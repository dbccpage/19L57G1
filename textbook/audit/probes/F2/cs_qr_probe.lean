import Derivation.ResidualClosure
import Derivation.QuotientRetention
open Compression PresentationRelativity ClosureSymmetry QuotientRetention
#print axioms ClosureSymmetry.closure_failure_iff_internal_symmetry_break
#print axioms ResidualClosure.common_refinement_closes_current_obstruction
#print axioms QuotientRetention.collapseMap_injective_iff_reverse_refinement
#print axioms PresentationDescent.faithful_descent_iff_round_trip_coherent
-- An InternalSymmetryBreak may use a symmetry that is NOT a transposition:
-- e.g. a 2-cycle on {0,1} with D = [0,1,2], p constant, q = id. Its existence
-- is equivalent (not identical) to a residual.
example : InternalSymmetryBreak [0,1,2] (fun _ => 0) id :=
  { symmetry := transpose 0 1, involutive := transpose_involutive 0 1,
    domain_preserved := by decide, p_invariant := by intros; rfl,
    point := 0, point_mem := by simp, q_not_invariant := by decide }
-- Degenerate residual with left = right is impossible (separated : q l ≠ q r).
example (D : List Nat) (p q : Nat → Nat) (r : DirectionalResidual D p q) : r.left ≠ r.right :=
  fun h => r.separated (by rw [h])
-- QuotientRetention: coarse = indiscrete on Bool, fine = equality: the collapse is not injective.
def eqS : Setoid Bool := ⟨(· = ·), ⟨fun _ => rfl, fun h => h.symm, fun h1 h2 => h1.trans h2⟩⟩
def allS : Setoid Bool := ⟨fun _ _ => True, ⟨fun _ => trivial, fun _ => trivial, fun _ _ => trivial⟩⟩
example : ¬ Function.Injective (collapseMap (fine := eqS) (coarse := allS) ⟨fun _ => trivial⟩) :=
  failed_identification_makes_collapse_noninjective _ (x := false) (y := true) trivial (fun h => Bool.noConfusion h)
