import Lean
import Harness

/-!
Metatheoretic audit apparatus: enumerate the compiled theorem declarations
of the `Harness` namespace independently of source layout and of the
printed dependency reports.  AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let names := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if (`Harness).isPrefixOf name && !name.isInternalDetail then
            name.toString :: found
          else found
      | _ => found
  let hidden := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if isPrivateName name && ((privateToUserName? name).any (`Harness).isPrefixOf)
          then name.toString :: found else found
      | _ => found
  if !hidden.isEmpty then
    throwError "HARNESS_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "HARNESS_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"HARNESS_THEOREM: {name}"

/- Generated-declaration reports named by the environment census. -/
#print axioms Harness.EvalResult.mk.inj
#print axioms Harness.EvalResult.mk.injEq
#print axioms Harness.EvalResult.mk.sizeOf_spec
#print axioms Harness.ExtraCtor.mk.inj
#print axioms Harness.ExtraCtor.mk.injEq
#print axioms Harness.ExtraCtor.mk.sizeOf_spec
#print axioms Harness.GradeStamp.noneStamp.sizeOf_spec
#print axioms Harness.GradeStamp.tie.sizeOf_spec
#print axioms Harness.GradeStamp.uniqueClass.sizeOf_spec
#print axioms Harness.GradeStamp.uniqueDelta.sizeOf_spec
#print axioms Harness.License.mk.inj
#print axioms Harness.License.mk.injEq
#print axioms Harness.License.mk.sizeOf_spec
#print axioms Harness.Node.mk.inj
#print axioms Harness.Node.mk.injEq
#print axioms Harness.Node.mk.sizeOf_spec
#print axioms Harness.Proposal.mk.inj
#print axioms Harness.Proposal.mk.injEq
#print axioms Harness.Proposal.mk.sizeOf_spec
#print axioms Harness.RetainedClass.mk.inj
#print axioms Harness.RetainedClass.mk.injEq
#print axioms Harness.RetainedClass.mk.sizeOf_spec
#print axioms Harness.SearchPolicy.mk.inj
#print axioms Harness.SearchPolicy.mk.injEq
#print axioms Harness.SearchPolicy.mk.sizeOf_spec
