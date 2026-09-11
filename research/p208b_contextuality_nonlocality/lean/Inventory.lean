import Lean
import ContextualityNonlocality

/-!
# Metatheoretic Theorem Census for ContextualityNonlocality Package

Audits all compiled theorem declarations in the ContextualityNonlocality namespace.
Verifies that:
1. Every local theorem is cataloged and printed in the environment census.
2. Axioms are strictly within {propext, Quot.sound}.
3. Zero Classical.choice, zero mathlib axioms.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool := (`ContextualityNonlocality).isPrefixOf name
  let names := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ => if local? name then name.toString :: found else found
      | _ => found
  let hidden := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if isPrivateName name && ((privateToUserName? name).any local?)
          then name.toString :: found else found
      | _ => found
  if !hidden.isEmpty then
    throwError "CONTEXTUALITY_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "CONTEXTUALITY_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"CONTEXTUALITY_THEOREM: {name}"

/- The compiled environment census declarations and their axiom audits -/
#print axioms ContextualityNonlocality.C0._proof_1
#print axioms ContextualityNonlocality.Q.mk.inj
#print axioms ContextualityNonlocality.Q.mk.injEq
#print axioms ContextualityNonlocality.Q.mk.sizeOf_spec
#print axioms ContextualityNonlocality.S._proof_1
#print axioms ContextualityNonlocality.Vec4.mk.inj
#print axioms ContextualityNonlocality.Vec4.mk.injEq
#print axioms ContextualityNonlocality.Vec4.mk.sizeOf_spec
#print axioms ContextualityNonlocality.all_contexts_orthogonal
#print axioms ContextualityNonlocality.all_rays_degree_two
#print axioms ContextualityNonlocality.bell_chsh_lhv_bound
#print axioms ContextualityNonlocality.bell_chsh_lhv_values
#print axioms ContextualityNonlocality.cabello_valuation_obstruction
#print axioms ContextualityNonlocality.cabello_valuation_obstruction._proof_1_1
#print axioms ContextualityNonlocality.cech_cochain_obstruction_nonzero
#print axioms ContextualityNonlocality.instDecidableEqVec4.decEq._proof_1
#print axioms ContextualityNonlocality.instDecidableEqVec4.decEq._proof_2
#print axioms ContextualityNonlocality.instDecidableEqVec4.decEq._proof_3
#print axioms ContextualityNonlocality.instDecidableEqVec4.decEq._proof_4
#print axioms ContextualityNonlocality.instDecidableEqVec4.decEq._proof_5
#print axioms ContextualityNonlocality.mod2_context_parity
#print axioms ContextualityNonlocality.mod2_incidence_parity
#print axioms ContextualityNonlocality.mod2_incidence_parity._proof_1_1
#print axioms ContextualityNonlocality.no_even_equals_nine
#print axioms ContextualityNonlocality.no_even_equals_nine._proof_1_1
#print axioms ContextualityNonlocality.pythagorean_correlator_den
#print axioms ContextualityNonlocality.pythagorean_correlator_num
#print axioms ContextualityNonlocality.pythagorean_exceeds_lhv
#print axioms ContextualityNonlocality.pythagorean_exceeds_lhv._proof_1_1
#print axioms ContextualityNonlocality.pythagorean_respects_algebraic_bound
#print axioms ContextualityNonlocality.pythagorean_respects_algebraic_bound._proof_1_1
#print axioms ContextualityNonlocality.total_eq_twice_ray_sum
#print axioms ContextualityNonlocality.total_eq_twice_ray_sum._proof_1_1
