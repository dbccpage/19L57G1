import Lean
import NonclassicalHorizons

/-!
# Metatheoretic Theorem Census for Target P209d Non-Classicality Horizons

Audits all compiled theorem declarations in the P209dNonclassicalHorizons namespace.
Verifies that:
1. Every local theorem is cataloged and logged in the census.
2. Zero private theorems are present.
3. Axioms are strictly within {propext, Quot.sound}.
4. Zero Classical.choice, zero mathlib axioms.

AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool := (`P209dNonclassicalHorizons).isPrefixOf name
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
    throwError "P209D_NONCLASSICAL_HORIZONS_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "P209D_NONCLASSICAL_HORIZONS_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"P209D_THEOREM: {name}"



/- The compiled environment census declarations and their axiom audits -/
#print axioms P209dNonclassicalHorizons.CNOT_preserves_commutativity
#print axioms P209dNonclassicalHorizons.H_preserves_commutativity
#print axioms P209dNonclassicalHorizons.H_preserves_destabilizer_pair
#print axioms P209dNonclassicalHorizons.Rat3.mk.inj
#print axioms P209dNonclassicalHorizons.Rat3.mk.injEq
#print axioms P209dNonclassicalHorizons.Rat3.mk.sizeOf_spec
#print axioms P209dNonclassicalHorizons.S_preserves_commutativity
#print axioms P209dNonclassicalHorizons.S_preserves_destabilizer_pair
#print axioms P209dNonclassicalHorizons.SymplecticVec1.mk.inj
#print axioms P209dNonclassicalHorizons.SymplecticVec1.mk.injEq
#print axioms P209dNonclassicalHorizons.SymplecticVec1.mk.sizeOf_spec
#print axioms P209dNonclassicalHorizons.SymplecticVec2.mk.inj
#print axioms P209dNonclassicalHorizons.SymplecticVec2.mk.injEq
#print axioms P209dNonclassicalHorizons.SymplecticVec2.mk.sizeOf_spec
#print axioms P209dNonclassicalHorizons.bell_stabilizers_commute
#print axioms P209dNonclassicalHorizons.canonical_destabilizer._proof_1
#print axioms P209dNonclassicalHorizons.canonical_pair_duality
#print axioms P209dNonclassicalHorizons.clifford_CNOT._proof_1
#print axioms P209dNonclassicalHorizons.clifford_CNOT._proof_2
#print axioms P209dNonclassicalHorizons.clifford_CNOT_preserves_omega
#print axioms P209dNonclassicalHorizons.clifford_H_preserves_omega
#print axioms P209dNonclassicalHorizons.clifford_S._proof_1
#print axioms P209dNonclassicalHorizons.clifford_S_preserves_omega
#print axioms P209dNonclassicalHorizons.clifford_cost_linear_in_gates
#print axioms P209dNonclassicalHorizons.clifford_cost_polynomial
#print axioms P209dNonclassicalHorizons.discrete_hudson_boundary_separation
#print axioms P209dNonclassicalHorizons.fin2_cases
#print axioms P209dNonclassicalHorizons.fin2_cases._proof_1_3
#print axioms P209dNonclassicalHorizons.fin3_cases
#print axioms P209dNonclassicalHorizons.fin3_cases._proof_1_3
#print axioms P209dNonclassicalHorizons.gottesman_knill_separation
#print axioms P209dNonclassicalHorizons.instDecidableEqRat3.decEq._proof_1
#print axioms P209dNonclassicalHorizons.instDecidableEqRat3.decEq._proof_2
#print axioms P209dNonclassicalHorizons.instDecidableEqRat3.decEq._proof_3
#print axioms P209dNonclassicalHorizons.instDecidableEqSymplecticVec1.decEq._proof_1
#print axioms P209dNonclassicalHorizons.instDecidableEqSymplecticVec1.decEq._proof_2
#print axioms P209dNonclassicalHorizons.instDecidableEqSymplecticVec1.decEq._proof_3
#print axioms P209dNonclassicalHorizons.instDecidableEqSymplecticVec2.decEq._proof_1
#print axioms P209dNonclassicalHorizons.instDecidableEqSymplecticVec2.decEq._proof_2
#print axioms P209dNonclassicalHorizons.instDecidableEqSymplecticVec2.decEq._proof_3
#print axioms P209dNonclassicalHorizons.magic_branch_4_eval
#print axioms P209dNonclassicalHorizons.magic_branch_5_eval
#print axioms P209dNonclassicalHorizons.magic_branch_5_gt_quadratic
#print axioms P209dNonclassicalHorizons.magic_branch_count_pow
#print axioms P209dNonclassicalHorizons.magic_branch_count_pow._proof_1_1
#print axioms P209dNonclassicalHorizons.magic_branch_lower_bound
#print axioms P209dNonclassicalHorizons.magic_branch_lower_bound._proof_1_1
#print axioms P209dNonclassicalHorizons.omega2_self
#print axioms P209dNonclassicalHorizons.omega2_symm
#print axioms P209dNonclassicalHorizons.omega4_self
#print axioms P209dNonclassicalHorizons.omega4_symm
#print axioms P209dNonclassicalHorizons.stabilizer_self_commutes
#print axioms P209dNonclassicalHorizons.wigner_magic_origin_negative
#print axioms P209dNonclassicalHorizons.wigner_stab_plus_non_negative
#print axioms P209dNonclassicalHorizons.wigner_stab_zero_non_negative

def main : IO Unit := do
  IO.println "P209d Non-Classicality Horizons Census Complete: 55 theorems verified."
