import Lean
import Ordinal
import Address
import Freshness
import Recursion

/-!
# Metatheoretic Theorem Census for G011 Finitary Substrate

Metaprogrammed census enumerating all compiled theorems under `FinitarySubstrate`
and verifying their constructive axiom bounds.

AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool :=
    (`FinitarySubstrate).isPrefixOf name
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
    throwError "FINITARY_SUBSTRATE_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "FINITARY_SUBSTRATE_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"FINITARY_SUBSTRATE_THEOREM: {name}"
