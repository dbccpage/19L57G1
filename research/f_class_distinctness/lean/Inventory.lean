import Lean
import FClassDistinctness

/-!
Metatheoretic audit apparatus: enumerate the compiled theorem declarations
of the `FClassDistinctness` namespace independently of source layout.
AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let names := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if (`FClassDistinctness).isPrefixOf name && !name.isInternalDetail then
            name.toString :: found
          else found
      | _ => found
  let hidden := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if isPrivateName name && ((privateToUserName? name).any (`FClassDistinctness).isPrefixOf)
          then name.toString :: found else found
      | _ => found
  if !hidden.isEmpty then
    throwError "F_CLASS_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "F_CLASS_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"F_CLASS_THEOREM: {name}"
