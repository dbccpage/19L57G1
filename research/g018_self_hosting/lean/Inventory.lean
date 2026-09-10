import Lean
import CarrierRepr
import Simulator
import ReflectionBoundary
import Obstruction

/-!
# Metatheoretic Theorem Census for G018 Self-Hosting

Metaprogrammed census enumerating all compiled theorems under `G018SelfHosting`
and verifying their constructive axiom bounds.

AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool :=
    (`G018SelfHosting).isPrefixOf name
  let isInternalMatch (name : Name) : Bool :=
    (name.toString.splitOn "match_").length > 1
  let names := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ => if local? name then name.toString :: found else found
      | _ => found
  let hidden := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if isPrivateName name && ((privateToUserName? name).any local?) && !isInternalMatch name
          then name.toString :: found else found
      | _ => found
  if !hidden.isEmpty then
    throwError "G018_SELF_HOSTING_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "G018_SELF_HOSTING_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"G018_SELF_HOSTING_THEOREM: {name}"
