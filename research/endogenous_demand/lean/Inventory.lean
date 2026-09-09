import Lean
import EndogenousDemand

/-!
Metatheoretic audit apparatus: enumerate the compiled theorem declarations
of the `EndogenousDemand` namespace independently of source layout and of
the printed dependency reports.  AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let names := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if (`EndogenousDemand).isPrefixOf name then name.toString :: found else found
      | _ => found
  let hidden := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if isPrivateName name && ((privateToUserName? name).any (`EndogenousDemand).isPrefixOf)
          then name.toString :: found else found
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
