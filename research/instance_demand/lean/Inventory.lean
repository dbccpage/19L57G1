import Lean
import InstanceDemand
import ClosureMaterialization
import RepresentedEmitter
import EmissionDynamics

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

#print axioms InstanceDemand.Closure.addMany.eq_1
#print axioms InstanceDemand.Closure.addMany_mem._simp_1_2
#print axioms InstanceDemand.Closure.answer_separates._simp_1_3
#print axioms InstanceDemand.Closure.answer_separates._simp_1_4
#print axioms InstanceDemand.Closure.answered.eq_1
#print axioms InstanceDemand.Closure.base.eq_1
#print axioms InstanceDemand.Closure.events.eq_1
#print axioms InstanceDemand.Closure.generated_pairs_answerable._proof_1_1
#print axioms InstanceDemand.Closure.generated_pairs_answerable._proof_1_2
#print axioms InstanceDemand.Closure.materialize.eq_1
#print axioms InstanceDemand.Closure.materialize_collapsed._simp_1_1
#print axioms InstanceDemand.Closure.materialize_derivable._simp_1_1
#print axioms InstanceDemand.Closure.materialize_separable._simp_1_1
#print axioms InstanceDemand.Closure.materialized_pairs._simp_1_2
#print axioms InstanceDemand.Closure.materialized_pairs._simp_1_3
#print axioms InstanceDemand.Closure.pending._proof_1
#print axioms InstanceDemand.Closure.pending.eq_1
#print axioms InstanceDemand.Closure.pending_mem._simp_1_2
#print axioms InstanceDemand.Closure.readPair.eq_1
#print axioms InstanceDemand.Closure.response.eq_1
#print axioms InstanceDemand.Closure.responseEvents.eq_1
#print axioms InstanceDemand.Closure.storeMany.eq_1
#print axioms InstanceDemand.Closure.tuples_mem._simp_1_1
#print axioms InstanceDemand.Closure.tuples_mem._simp_1_2
#print axioms InstanceDemand.Closure.tuples_mem._simp_1_3
#print axioms InstanceDemand.Closure.uniformEntries.eq_1
#print axioms InstanceDemand.Closure.uniformEntries_mem._simp_1_2
#print axioms InstanceDemand.Closure.uniformEntries_mem._simp_1_3
#print axioms InstanceDemand.Closure.wfInst.eq_1

#print axioms InstanceDemand.Emitter.answer_separates._proof_1_3
#print axioms InstanceDemand.Emitter.answer_separates._simp_1_4
#print axioms InstanceDemand.Emitter.answered.eq_1
#print axioms InstanceDemand.Emitter.covered_emission_collapsed._proof_1_3
#print axioms InstanceDemand.Emitter.covered_emission_collapsed._simp_1_1
#print axioms InstanceDemand.Emitter.covered_emission_collapsed._simp_1_2
#print axioms InstanceDemand.Emitter.edges.eq_1
#print axioms InstanceDemand.Emitter.edges_mem._simp_1_2
#print axioms InstanceDemand.Emitter.edges_mem._simp_1_3
#print axioms InstanceDemand.Emitter.emit.eq_1
#print axioms InstanceDemand.Emitter.histories_no_impose._simp_1_2
#print axioms InstanceDemand.Emitter.instructions.eq_1
#print axioms InstanceDemand.Emitter.instructions_mem._simp_1_2
#print axioms InstanceDemand.Emitter.instructions_mem._simp_1_3
#print axioms InstanceDemand.Emitter.length_three._proof_1_1
#print axioms InstanceDemand.Emitter.length_two._proof_1_1
#print axioms InstanceDemand.Emitter.pending._proof_1
#print axioms InstanceDemand.Emitter.pending.eq_1
#print axioms InstanceDemand.Emitter.pending_mem._simp_1_2
#print axioms InstanceDemand.Emitter.pending_mem._simp_1_3
#print axioms InstanceDemand.Emitter.raw_mem._simp_1_1
#print axioms InstanceDemand.Emitter.response.eq_1
#print axioms InstanceDemand.Emitter.responseEvents.eq_1
#print axioms InstanceDemand.Emitter.seed.eq_1
#print axioms InstanceDemand.Emitter.seedHistory.eq_1
#print axioms InstanceDemand.Emitter.seed_collapsed._proof_1_4
#print axioms InstanceDemand.Emitter.seed_collapsed._proof_1_5
#print axioms InstanceDemand.Emitter.seed_collapsed._simp_1_2
#print axioms InstanceDemand.Emitter.seed_collapsed._simp_1_3
#print axioms InstanceDemand.Emitter.unruled_emission_separates._proof_1_3

-- Stage 4 generated theorem reports.
#print axioms InstanceDemand.Dynamics.chain.eq_1
#print axioms InstanceDemand.Dynamics.chain_covered_collapsed._proof_1_3
#print axioms InstanceDemand.Dynamics.chain_covered_collapsed._simp_1_1
#print axioms InstanceDemand.Dynamics.chain_covered_collapsed._simp_1_2
#print axioms InstanceDemand.Dynamics.missing._proof_1
#print axioms InstanceDemand.Dynamics.missing.eq_1
#print axioms InstanceDemand.Dynamics.pending_not_instruction._proof_1_1
#print axioms InstanceDemand.Dynamics.reaches_fixed._proof_1_1
#print axioms InstanceDemand.Dynamics.reaches_fixed._proof_1_2
#print axioms InstanceDemand.Dynamics.slots.eq_1
#print axioms InstanceDemand.Dynamics.slots_mem._simp_1_2
#print axioms InstanceDemand.Dynamics.stable_after_budget._proof_1_1
#print axioms InstanceDemand.Dynamics.stable_by_budget._proof_1_1
#print axioms InstanceDemand.Emitter.codes.eq_1
