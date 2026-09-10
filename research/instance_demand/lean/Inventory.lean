import Lean
import InstanceDemand

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let names := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if (`InstanceDemand).isPrefixOf name then name.toString :: found else found
      | _ => found
  let hidden := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if isPrivateName name && ((privateToUserName? name).any (`InstanceDemand).isPrefixOf)
          then name.toString :: found else found
      | _ => found
  if !hidden.isEmpty then throwError "INSTANCE_DEMAND_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then throwError "INSTANCE_DEMAND_THEOREM_CENSUS_EMPTY"
  for name in sorted do logInfo m!"INSTANCE_DEMAND_THEOREM: {name}"

#print axioms InstanceDemand.covered.eq_1
#print axioms InstanceDemand.covered_pair_collapsed._proof_1_1
#print axioms InstanceDemand.genesis_instance_origin._simp_1_2
#print axioms InstanceDemand.lone.eq_1
#print axioms InstanceDemand.replay_insts_mem._simp_1_1
#print axioms InstanceDemand.replay_insts_mem._simp_1_2
#print axioms InstanceDemand.replay_insts_mem._simp_1_3
#print axioms InstanceDemand.step_insts_mem._simp_1_1
#print axioms InstanceDemand.step_insts_mem._simp_1_2
