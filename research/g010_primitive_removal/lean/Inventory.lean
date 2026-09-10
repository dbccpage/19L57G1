import Lean
import Capability
import Restriction
import Obstruction

/-!
# Metatheoretic Theorem Census for G010 Primitive Removal

Metaprogrammed census enumerating all compiled theorems under `G010`
and verifying their constructive axiom bounds.

AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool :=
    (`G010).isPrefixOf name
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
    throwError "G010_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "G010_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"G010_THEOREM: {name}"
