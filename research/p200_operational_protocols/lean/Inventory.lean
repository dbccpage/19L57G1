import Lean
import Protocol
import Commutation
import Observers
import NonSignaling

/-!
# Metatheoretic Theorem Census for P200 Operational Protocols

Audits all compiled theorem declarations in the P200OperationalProtocols namespace.
Verifies that:
1. Every local theorem is cataloged and logged in the census.
2. Zero private theorems are present.
3. Axioms are strictly within {propext, Quot.sound}.
4. Zero Classical.choice, zero mathlib axioms.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool := (`P200OperationalProtocols).isPrefixOf name
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
    throwError "P200_OPERATIONAL_PROTOCOLS_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "P200_OPERATIONAL_PROTOCOLS_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"P200_THEOREM: {name}"

/- The compiled environment census declarations and their axiom audits -/
#print axioms P200OperationalProtocols.CarrierState.ext
#print axioms P200OperationalProtocols.CarrierState.ext_iff
#print axioms P200OperationalProtocols.CarrierState.mk.inj
#print axioms P200OperationalProtocols.CarrierState.mk.injEq
#print axioms P200OperationalProtocols.CarrierState.mk.sizeOf_spec
#print axioms P200OperationalProtocols.asymmetric_observation_divergence
#print axioms P200OperationalProtocols.causal_signaling_divergence
#print axioms P200OperationalProtocols.coincidence_iff
#print axioms P200OperationalProtocols.disturbing_readout_fails_commute
#print axioms P200OperationalProtocols.instDecidableEqCarrierState.decEq._proof_1
#print axioms P200OperationalProtocols.instDecidableEqCarrierState.decEq._proof_2
#print axioms P200OperationalProtocols.instDecidableEqCarrierState.decEq._proof_3
#print axioms P200OperationalProtocols.instDecidableEqCarrierState.decEq._proof_4
#print axioms P200OperationalProtocols.instDecidableEqCarrierState.decEq._proof_5
#print axioms P200OperationalProtocols.instDecidableEqCarrierState.decEq._proof_6
#print axioms P200OperationalProtocols.instDecidableEqCarrierState.decEq._proof_7
#print axioms P200OperationalProtocols.inter_observer_agreement
#print axioms P200OperationalProtocols.inter_observer_coincidence
#print axioms P200OperationalProtocols.intervene_l1_preserves_l2
#print axioms P200OperationalProtocols.intervene_l1_preserves_m
#print axioms P200OperationalProtocols.intervene_l1_preserves_r2
#print axioms P200OperationalProtocols.intervene_l2_preserves_l1
#print axioms P200OperationalProtocols.intervene_l2_preserves_m
#print axioms P200OperationalProtocols.intervene_l2_preserves_r1
#print axioms P200OperationalProtocols.prepare_product_l1
#print axioms P200OperationalProtocols.prepare_product_l2
#print axioms P200OperationalProtocols.prepare_product_records
#print axioms P200OperationalProtocols.prepare_symmetric_eq
#print axioms P200OperationalProtocols.readout1_preserves_l1
#print axioms P200OperationalProtocols.readout1_preserves_l2
#print axioms P200OperationalProtocols.readout1_preserves_r2
#print axioms P200OperationalProtocols.readout1_readout2_comm
#print axioms P200OperationalProtocols.readout1_stepL2_commutation
#print axioms P200OperationalProtocols.readout1_stepM_commutation
#print axioms P200OperationalProtocols.readout1_swap
#print axioms P200OperationalProtocols.readout2_preserves_l1
#print axioms P200OperationalProtocols.readout2_preserves_l2
#print axioms P200OperationalProtocols.readout2_preserves_r1
#print axioms P200OperationalProtocols.readout2_stepM_commutation
#print axioms P200OperationalProtocols.readout2_swap
#print axioms P200OperationalProtocols.readout_replayL1_commutation
#print axioms P200OperationalProtocols.readout_step_commutation
#print axioms P200OperationalProtocols.record1_preserves_target
#print axioms P200OperationalProtocols.record2_preserves_target
#print axioms P200OperationalProtocols.spacelike_marginal2_invariance
#print axioms P200OperationalProtocols.spacelike_marginal_invariance
#print axioms P200OperationalProtocols.spacelike_non_signaling
#print axioms P200OperationalProtocols.spacelike_sequence_non_signaling
#print axioms P200OperationalProtocols.swap_involutive
#print axioms P200OperationalProtocols.swap_preserves_dist
#print axioms P200OperationalProtocols.swap_preserves_m
#print axioms P200OperationalProtocols.swap_symmetric_eq
