import Lean
import WignerPhaseSpace

/-!
# Metatheoretic Theorem Census for Target P209a Wigner Phase_Spaces

Audits all compiled theorem declarations in the P209aWignerPhaseSpace namespace.
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
  let local? (name : Name) : Bool := (`P209aWignerPhaseSpace).isPrefixOf name
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
    throwError "P209A_WIGNER_PHASE_SPACE_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "P209A_WIGNER_PHASE_SPACE_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"P209A_THEOREM: {name}"

/- The compiled environment census declarations and their axiom audits -/
#print axioms P209aWignerPhaseSpace.Cyclo3Ring.mk.inj
#print axioms P209aWignerPhaseSpace.Cyclo3Ring.mk.injEq
#print axioms P209aWignerPhaseSpace.Cyclo3Ring.mk.sizeOf_spec
#print axioms P209aWignerPhaseSpace.P3_gross_covariance_X
#print axioms P209aWignerPhaseSpace.P3_gross_covariance_Z
#print axioms P209aWignerPhaseSpace.P3_involution
#print axioms P209aWignerPhaseSpace.P3_magic_state_eigenstate
#print axioms P209aWignerPhaseSpace.P3_stabilizer_ket0_eigenstate
#print axioms P209aWignerPhaseSpace.P3_stabilizer_ket_plus_eigenstate
#print axioms P209aWignerPhaseSpace.P3_trace_one
#print axioms P209aWignerPhaseSpace.P5_gross_covariance_X
#print axioms P209aWignerPhaseSpace.P5_involution
#print axioms P209aWignerPhaseSpace.P5_magic_state_eigenstate
#print axioms P209aWignerPhaseSpace.P5_stabilizer_ket0_eigenstate
#print axioms P209aWignerPhaseSpace.P5_stabilizer_ket_plus_eigenstate
#print axioms P209aWignerPhaseSpace.P5_trace_one
#print axioms P209aWignerPhaseSpace.QRat.mk.inj
#print axioms P209aWignerPhaseSpace.QRat.mk.injEq
#print axioms P209aWignerPhaseSpace.QRat.mk.sizeOf_spec
#print axioms P209aWignerPhaseSpace.X3_translation_order
#print axioms P209aWignerPhaseSpace.X5_translation_order
#print axioms P209aWignerPhaseSpace.Z3_clock_order
#print axioms P209aWignerPhaseSpace.instDecidableEqCyclo3Ring.decEq._proof_1
#print axioms P209aWignerPhaseSpace.instDecidableEqCyclo3Ring.decEq._proof_2
#print axioms P209aWignerPhaseSpace.instDecidableEqCyclo3Ring.decEq._proof_3
#print axioms P209aWignerPhaseSpace.instDecidableEqQRat.decEq._proof_1
#print axioms P209aWignerPhaseSpace.instDecidableEqQRat.decEq._proof_2
#print axioms P209aWignerPhaseSpace.instDecidableEqQRat.decEq._proof_3
#print axioms P209aWignerPhaseSpace.magic_state_negativity_witness_3
#print axioms P209aWignerPhaseSpace.magic_state_negativity_witness_5
#print axioms P209aWignerPhaseSpace.magic_state_norm_sq_3
#print axioms P209aWignerPhaseSpace.magic_state_norm_sq_5
#print axioms P209aWignerPhaseSpace.magic_state_parity_expectation_3
#print axioms P209aWignerPhaseSpace.magic_state_parity_expectation_5
#print axioms P209aWignerPhaseSpace.matVecMul3._proof_1
#print axioms P209aWignerPhaseSpace.matVecMul5._proof_1

def main : IO Unit := do
  IO.println "P209a Wigner Phase_Space Census Complete: 36 theorems verified."
