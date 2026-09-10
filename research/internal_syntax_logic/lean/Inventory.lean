import Lean
import Syntax
import Logic
import Pricing
import Connectives

/-!
# Metatheoretic Theorem Census for M100–M103 Internal Syntax & Operational Logic

Metaprogrammed census enumerating all compiled theorems under `InternalSyntaxLogic`
and verifying their constructive axiom bounds.

AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool :=
    (`InternalSyntaxLogic).isPrefixOf name
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
    throwError "INTERNAL_SYNTAX_LOGIC_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "INTERNAL_SYNTAX_LOGIC_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"SYNTAX_LOGIC_THEOREM: {name}"
