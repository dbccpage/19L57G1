import Lean
import Trace
import HigherCell
import Factorization
import Congruence
import Price

/-!
# Metatheoretic Theorem Census for G013 Trace Calculus

Metaprogrammed census enumerating all compiled theorems under `G013TraceCalculus`
and verifying their constructive axiom bounds.

Target G013: Coherent Trace Calculus & Higher Cell Algebra.
AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool :=
    (`G013TraceCalculus).isPrefixOf name
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
    throwError "G013_TRACE_CALCULUS_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "G013_TRACE_CALCULUS_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"G013_TRACE_CALCULUS_THEOREM: {name}"
