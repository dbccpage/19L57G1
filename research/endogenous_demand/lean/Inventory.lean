import Lean
import EndogenousDemand
import EndogenousDemandObstruction

/-!
Metatheoretic audit apparatus: enumerate the compiled theorem declarations
of this tree's proof modules independently of source layout and of the
printed dependency reports.  AuthorityEffect: None.

The census is by module, not by namespace.  Until 2026-09-24 it enumerated
only the `EndogenousDemand` namespace and imported only `EndogenousDemand`,
so the seventeen theorems of `EndogenousDemandObstruction`, the termination
bound among them, were outside the recorded audit.  A theorem written in any
namespace of either module is now in the census.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let audited : List Name := [`EndogenousDemand, `EndogenousDemandObstruction]
  let moduleNames := environment.allImportedModuleNames
  let inAudited (name : Name) : Bool :=
    match environment.getModuleIdxFor? name with
    | some index => audited.contains (moduleNames[index.toNat]!)
    | none => false
  let names := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if inAudited name && !isPrivateName name then name.toString :: found else found
      | _ => found
  let hidden := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if inAudited name && isPrivateName name then name.toString :: found else found
      | _ => found
  if !hidden.isEmpty then
    throwError "ENDOGENOUS_DEMAND_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "ENDOGENOUS_DEMAND_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"ENDOGENOUS_DEMAND_THEOREM: {name}"

/- Generated-declaration reports are appended after the first successful
   compilation names them. -/

#print axioms EndogenousDemandObstruction.EndogenousStep.fresh
#print axioms EndogenousDemandObstruction.EndogenousStep.no_grow
#print axioms EndogenousDemandObstruction.EndogenousStep.step
#print axioms EndogenousDemandObstruction.endogenous_obstruction_no_excess._proof_1_1
#print axioms EndogenousDemandObstruction.endogenous_trace_le_binom2._proof_1_1
