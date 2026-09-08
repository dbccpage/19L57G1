import Lean
import Reachable

/-!
Enumerate compiled theorem declarations independently of printed reports.
AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let names := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if (`Reachable).isPrefixOf name then name.toString :: found else found
      | _ => found
  let hidden := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if isPrivateName name && ((privateToUserName? name).any (`Reachable).isPrefixOf)
          then name.toString :: found else found
      | _ => found
  if !hidden.isEmpty then
    throwError "REACHABLE_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "REACHABLE_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"REACHABLE_THEOREM: {name}"

/- Reports for compiler-generated theorem declarations. Their population is
checked against the environment above, not against these print commands. -/
#print axioms Reachable.Reach.brecOn
#print axioms Reachable.formNoInst.eq_1
#print axioms Reachable.minResponse_formsUsed._proof_1_3
#print axioms Reachable.minResponse_formsUsed._proof_1_4
#print axioms Reachable.minResponse_formsUsed._proof_1_5
#print axioms Reachable.minResponse_no_rule._proof_1_1
#print axioms Reachable.rootF.eq_1
#print axioms Reachable.rootL.eq_1
#print axioms Reachable.ruledMark.eq_1
#print axioms Reachable.separable_appendForm._proof_1_1
#print axioms Reachable.separable_appendForm._proof_1_2
#print axioms Reachable.separable_appendForm._proof_1_3
#print axioms Reachable.wf_applyItem._proof_1_1
#print axioms Reachable.wf_applyItem._proof_1_2
