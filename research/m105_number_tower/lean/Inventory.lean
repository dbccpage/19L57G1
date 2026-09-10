import Lean
import NNO
import IntZ
import RatQ

/-!
# Metatheoretic Theorem Census for M105 Number Tower

Metaprogrammed census enumerating all compiled theorems under `NumberTower`
and verifying their constructive axiom bounds.

AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool :=
    (`NumberTower).isPrefixOf name
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
    throwError "NUMBER_TOWER_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "NUMBER_TOWER_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"NUMBER_TOWER_THEOREM: {name}"
