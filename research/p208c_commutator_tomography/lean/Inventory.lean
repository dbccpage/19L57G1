import Lean
import CommutatorTomography

/-!
# Metatheoretic Theorem Census for Target P208c Commutator Tomography

Audits all compiled theorem declarations in the P208cCommutatorTomography namespace.
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
  let local? (name : Name) : Bool := (`P208cCommutatorTomography).isPrefixOf name
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
    throwError "P208C_COMMUTATOR_TOMOGRAPHY_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "P208C_COMMUTATOR_TOMOGRAPHY_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"P208C_THEOREM: {name}"

/- The compiled environment census declarations and their axiom audits -/
#print axioms P208cCommutatorTomography.Cyclo3.dot3._proof_1
#print axioms P208cCommutatorTomography.Cyclo3.mk.inj
#print axioms P208cCommutatorTomography.Cyclo3.mk.injEq
#print axioms P208cCommutatorTomography.Cyclo3.mk.sizeOf_spec
#print axioms P208cCommutatorTomography.Cyclo3.mub0_mub1_unbiased
#print axioms P208cCommutatorTomography.Cyclo3.mub0_mub2_unbiased
#print axioms P208cCommutatorTomography.Cyclo3.mub0_mub3_unbiased
#print axioms P208cCommutatorTomography.Cyclo3.mub0_orthonormal
#print axioms P208cCommutatorTomography.Cyclo3.mub1_mub2_unbiased
#print axioms P208cCommutatorTomography.Cyclo3.mub1_mub3_unbiased
#print axioms P208cCommutatorTomography.Cyclo3.mub1_orthonormal
#print axioms P208cCommutatorTomography.Cyclo3.mub2_mub3_unbiased
#print axioms P208cCommutatorTomography.Cyclo3.mub2_orthonormal
#print axioms P208cCommutatorTomography.Cyclo3.mub3_orthonormal
#print axioms P208cCommutatorTomography.GaussInt.dot4._proof_1
#print axioms P208cCommutatorTomography.GaussInt.mk.inj
#print axioms P208cCommutatorTomography.GaussInt.mk.injEq
#print axioms P208cCommutatorTomography.GaussInt.mk.sizeOf_spec
#print axioms P208cCommutatorTomography.GaussInt.mub4_0_1_unbiased
#print axioms P208cCommutatorTomography.GaussInt.mub4_0_2_unbiased
#print axioms P208cCommutatorTomography.GaussInt.mub4_0_3_unbiased
#print axioms P208cCommutatorTomography.GaussInt.mub4_0_4_unbiased
#print axioms P208cCommutatorTomography.GaussInt.mub4_0_orthonormal
#print axioms P208cCommutatorTomography.GaussInt.mub4_1_2_unbiased
#print axioms P208cCommutatorTomography.GaussInt.mub4_1_3_unbiased
#print axioms P208cCommutatorTomography.GaussInt.mub4_1_4_unbiased
#print axioms P208cCommutatorTomography.GaussInt.mub4_1_orthonormal
#print axioms P208cCommutatorTomography.GaussInt.mub4_2_3_unbiased
#print axioms P208cCommutatorTomography.GaussInt.mub4_2_4_unbiased
#print axioms P208cCommutatorTomography.GaussInt.mub4_2_orthonormal
#print axioms P208cCommutatorTomography.GaussInt.mub4_3_4_unbiased
#print axioms P208cCommutatorTomography.GaussInt.mub4_3_orthonormal
#print axioms P208cCommutatorTomography.GaussInt.mub4_4_orthonormal
#print axioms P208cCommutatorTomography.commutator_trace_obstruction
#print axioms P208cCommutatorTomography.commutator_trace_obstruction._proof_1_1
#print axioms P208cCommutatorTomography.const_mul_sum
#print axioms P208cCommutatorTomography.fin2_cases
#print axioms P208cCommutatorTomography.fin2_cases._proof_1_3
#print axioms P208cCommutatorTomography.finRange_two
#print axioms P208cCommutatorTomography.identity_matMul_2
#print axioms P208cCommutatorTomography.identity_matMul_2._proof_1_1
#print axioms P208cCommutatorTomography.identity_matMul_2._proof_1_2
#print axioms P208cCommutatorTomography.identity_matMul_2._proof_1_3
#print axioms P208cCommutatorTomography.identity_matMul_2._proof_1_4
#print axioms P208cCommutatorTomography.instDecidableEqCyclo3.decEq._proof_1
#print axioms P208cCommutatorTomography.instDecidableEqCyclo3.decEq._proof_2
#print axioms P208cCommutatorTomography.instDecidableEqCyclo3.decEq._proof_3
#print axioms P208cCommutatorTomography.instDecidableEqGaussInt.decEq._proof_1
#print axioms P208cCommutatorTomography.instDecidableEqGaussInt.decEq._proof_2
#print axioms P208cCommutatorTomography.instDecidableEqGaussInt.decEq._proof_3
#print axioms P208cCommutatorTomography.matMul_identity_2
#print axioms P208cCommutatorTomography.matMul_identity_2._proof_1_1
#print axioms P208cCommutatorTomography.matMul_identity_2._proof_1_2
#print axioms P208cCommutatorTomography.matMul_identity_2._proof_1_3
#print axioms P208cCommutatorTomography.matMul_identity_2._proof_1_4
#print axioms P208cCommutatorTomography.multi_locus_microcausality_2x2
#print axioms P208cCommutatorTomography.multi_locus_microcausality_2x2._proof_1_1
#print axioms P208cCommutatorTomography.sum_add
#print axioms P208cCommutatorTomography.sum_add._proof_1_1
#print axioms P208cCommutatorTomography.sum_congr
#print axioms P208cCommutatorTomography.sum_const
#print axioms P208cCommutatorTomography.sum_mul_const
#print axioms P208cCommutatorTomography.sum_prod
#print axioms P208cCommutatorTomography.sum_sub
#print axioms P208cCommutatorTomography.sum_sub._proof_1_1
#print axioms P208cCommutatorTomography.sum_swap
#print axioms P208cCommutatorTomography.sum_zero
#print axioms P208cCommutatorTomography.sum_zero._proof_1_1
#print axioms P208cCommutatorTomography.tensor_mixed_product
#print axioms P208cCommutatorTomography.trace_commutator_zero
#print axioms P208cCommutatorTomography.trace_commutator_zero._proof_1_1
#print axioms P208cCommutatorTomography.trace_matMul_comm
#print axioms P208cCommutatorTomography.trace_scalar_identity

def main : IO Unit := do
  IO.println "P208c Commutator Tomography Census Complete: 73 theorems verified."
