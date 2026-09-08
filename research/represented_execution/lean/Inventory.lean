import Lean
import Execution

/-!
Metatheoretic audit apparatus: enumerate the compiled theorem declarations
of the `Execution` namespace independently of source layout and of the
printed dependency reports.  AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool := (`Execution).isPrefixOf name
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
    throwError "EXECUTION_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "EXECUTION_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"EXECUTION_THEOREM: {name}"


/- The compiler generates these additional theorem declarations for the
`Config` structure (constructor injectivity and the size specification).
Their reports are included beside the authored reports of `Execution.lean`,
and the combined population is compared with the independent environment
census. -/
#print axioms Execution.Config.mk.inj
#print axioms Execution.Config.mk.injEq
#print axioms Execution.Config.mk.sizeOf_spec
