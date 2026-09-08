import Lean
import Ignition

/-!
Metatheoretic audit apparatus: enumerate the compiled theorem declarations
of the `Ignition` namespace independently of source layout and of the
printed dependency reports.  AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let names := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if (`Ignition).isPrefixOf name then name.toString :: found else found
      | _ => found
  let hidden := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if isPrivateName name && ((privateToUserName? name).any (`Ignition).isPrefixOf)
          then name.toString :: found else found
      | _ => found
  if !hidden.isEmpty then
    throwError "IGNITION_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "IGNITION_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"IGNITION_THEOREM: {name}"

/- The compiler generates these additional theorem declarations (equation
lemmas, auxiliary proof terms of `omega`/`decide`/`simp`).  Their reports
are included beside the authored reports of `Ignition.lean`, and the
combined population is compared with the independent environment census. -/
#print axioms Ignition.applyItem_wf._proof_1_1
#print axioms Ignition.applyItem_wf._proof_1_2
#print axioms Ignition.blockState.eq_1
#print axioms Ignition.blockState_ne._proof_1_2
#print axioms Ignition.block_is_transStep._proof_1_1
#print axioms Ignition.ctxList._proof_1
#print axioms Ignition.fresh_pair_not_req._proof_1_1
#print axioms Ignition.markDelta_applies._proof_1_1
#print axioms Ignition.mem_ctxList._simp_1_1
#print axioms Ignition.mem_ctxList._simp_1_2
#print axioms Ignition.mem_ctxList._simp_1_3
#print axioms Ignition.mem_ctxList._simp_1_4
#print axioms Ignition.mem_tuples._simp_1_3
#print axioms Ignition.mem_tuples._simp_1_4
#print axioms Ignition.runState_data._proof_1_3
#print axioms Ignition.runState_forms._proof_1_3
#print axioms Ignition.runState_reqs._proof_1_3
#print axioms Ignition.slotOptions.eq_1
#print axioms Ignition.two_grows_response._proof_1_1
#print axioms Ignition.two_grows_response._proof_1_2
#print axioms Ignition.unmentioned_of_ge._proof_1_1
