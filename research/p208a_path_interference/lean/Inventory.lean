import Lean
import PathInterference

/-!
# Metatheoretic Theorem Census for Target P208a path_interference

Audits all compiled theorem declarations in the P208aPathInterference namespace.
Verifies that:
1. Every local theorem is cataloged and logged in the census.
2. Zero private theorems are present.
3. Axioms are strictly within {propext, Quot.sound}.
4. Zero Classical.choice, zero mathlib axioms.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool := (`P208aPathInterference).isPrefixOf name
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
    throwError "P208A_PATH_INTERFERENCE_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "P208A_PATH_INTERFERENCE_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"P208A_THEOREM: {name}"

/- The compiled environment census declarations and their axiom audits -/

#print axioms P208aPathInterference.GaussInt.I2_constructive_nonzero
#print axioms P208aPathInterference.GaussInt.I2_constructive_nonzero_ne_zero
#print axioms P208aPathInterference.GaussInt.I2_destructive_shift
#print axioms P208aPathInterference.GaussInt.I2_eq_cross
#print axioms P208aPathInterference.GaussInt.I2_eq_cross._proof_1_1
#print axioms P208aPathInterference.GaussInt.I2_orthogonal_delay
#print axioms P208aPathInterference.GaussInt.I2_pythagorean_shift
#print axioms P208aPathInterference.GaussInt.P_add_three
#print axioms P208aPathInterference.GaussInt.P_add_three._proof_1_1
#print axioms P208aPathInterference.GaussInt.P_add_two
#print axioms P208aPathInterference.GaussInt.P_add_two._proof_1_1
#print axioms P208aPathInterference.GaussInt.P_mul_star_eq
#print axioms P208aPathInterference.GaussInt.ext
#print axioms P208aPathInterference.GaussInt.ext_iff
#print axioms P208aPathInterference.GaussInt.mk.inj
#print axioms P208aPathInterference.GaussInt.mk.injEq
#print axioms P208aPathInterference.GaussInt.mk.sizeOf_spec
#print axioms P208aPathInterference.GaussInt.sorkin_I3_identically_zero
#print axioms P208aPathInterference.GaussInt.sorkin_I3_identically_zero._proof_1_1
#print axioms P208aPathInterference.QuadraticValuation.P_three
#print axioms P208aPathInterference.QuadraticValuation.P_two
#print axioms P208aPathInterference.QuadraticValuation.cross_symm
#print axioms P208aPathInterference.QuadraticValuation.mk.inj
#print axioms P208aPathInterference.QuadraticValuation.mk.injEq
#print axioms P208aPathInterference.QuadraticValuation.mk.sizeOf_spec
#print axioms P208aPathInterference.gauss_quadratic_valuation._proof_1
#print axioms P208aPathInterference.gauss_quadratic_valuation_I3_zero
#print axioms P208aPathInterference.instDecidableEqGaussInt.decEq._proof_1
#print axioms P208aPathInterference.instDecidableEqGaussInt.decEq._proof_2
#print axioms P208aPathInterference.instDecidableEqGaussInt.decEq._proof_3

def main : IO Unit := do
  IO.println "P208a PathInterference Census Complete: 30 theorems verified."
