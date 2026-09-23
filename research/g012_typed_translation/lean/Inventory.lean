import Lean
import Signature
import Codec
import Naturality
import Specialization
import NativeAdmission

/-!
# Metatheoretic Theorem Census for G012 Typed Translation

Metaprogrammed census enumerating all compiled declarations and theorems under
the `G012TypedTranslation` namespace and asserting that no hidden private
theorems exist.

AuthorityEffect: None.
Axiom boundary: strictly within {propext, Quot.sound}, zero Classical.choice, zero mathlib.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool :=
    (`G012TypedTranslation).isPrefixOf name
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
    throwError "G012_TYPED_TRANSLATION_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "G012_TYPED_TRANSLATION_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"G012_TYPED_TRANSLATION_THEOREM: {name}"
