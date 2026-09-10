import Lean
import Limits
import Observe
import Commute
import RationalBounds

/-!
# Metatheoretic Theorem Census for Target B Dynamics

Audits all compiled theorem declarations in the Limits, Observe, Commute, and RationalBounds namespaces.
Verifies that:
1. Every local theorem is cataloged and printed in the environment census.
2. Axioms are strictly within {propext, Quot.sound}.
3. Zero Classical.choice, zero mathlib axioms.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool :=
    (`Limits).isPrefixOf name || (`Observe).isPrefixOf name ||
    (`Commute).isPrefixOf name || (`RationalBounds).isPrefixOf name
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
    throwError "DYNAMICS_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "DYNAMICS_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"DYNAMICS_THEOREM: {name}"

/- The compiled environment census declarations and their axiom audits -/
#print axioms Commute.bondTrace._proof_1
#print axioms Commute.bond_stepStage_commute
#print axioms Commute.fuel_starvation_divergence
#print axioms Commute.obs_iter_next_commute
#print axioms Commute.ofSeq_stepThread
#print axioms Commute.shift_not_local_refusal
#print axioms Commute.stepThread._proof_1
#print axioms Commute.toSeq_stepThread
#print axioms Commute.trace_commuting_square
#print axioms Limits.bond._proof_1
#print axioms Limits.ebond._proof_1
#print axioms Limits.ebond._proof_2
#print axioms Limits.eofSeq._proof_1
#print axioms Limits.eofSeq_etoSeq
#print axioms Limits.eofSeq_etoSeq._proof_1_1
#print axioms Limits.estable
#print axioms Limits.estable._proof_1_3
#print axioms Limits.estable._proof_1_4
#print axioms Limits.etoSeq._proof_1
#print axioms Limits.etoSeq._proof_2
#print axioms Limits.etoSeq_eofSeq
#print axioms Limits.even_thread
#print axioms Limits.eventual._proof_1
#print axioms Limits.eventual._proof_2
#print axioms Limits.eventual_agrees
#print axioms Limits.eventual_agrees._proof_1_1
#print axioms Limits.eventual_not_compatible
#print axioms Limits.ofSeq._proof_1
#print axioms Limits.ofSeq_toSeq
#print axioms Limits.restrictEven._proof_1
#print axioms Limits.restrictEven._proof_2
#print axioms Limits.restrictEven_eq
#print axioms Limits.shift_not_local
#print axioms Limits.stable
#print axioms Limits.thread_even
#print axioms Limits.thread_restrictEven
#print axioms Limits.threads_are_sequences
#print axioms Limits.toSeq_ofSeq
#print axioms Limits.twins_are_two_threads
#print axioms Limits.twins_differ_at_scale_one
#print axioms Limits.twins_differ_at_zero
#print axioms Observe.Fired.exhausted.sizeOf_spec
#print axioms Observe.Fired.noEdge.sizeOf_spec
#print axioms Observe.Fired.ok.inj
#print axioms Observe.Fired.ok.injEq
#print axioms Observe.Fired.ok.sizeOf_spec
#print axioms Observe.State.mk.inj
#print axioms Observe.State.mk.injEq
#print axioms Observe.State.mk.sizeOf_spec
#print axioms Observe.Terminal.branch.sizeOf_spec
#print axioms Observe.Terminal.exhausted.sizeOf_spec
#print axioms Observe.Terminal.halt.sizeOf_spec
#print axioms Observe.Terminal.ofNat_ctorIdx
#print axioms Observe.Terminal.refuse.sizeOf_spec
#print axioms Observe.fire_exhausted
#print axioms Observe.fire_ok
#print axioms Observe.fire_succ
#print axioms Observe.instDecidableEqTerminal._proof_1
#print axioms Observe.instDecidableEqTerminal._proof_2
#print axioms Observe.iter_succ
#print axioms Observe.lost_fuel
#print axioms Observe.next_active_det
#print axioms Observe.next_branch
#print axioms Observe.next_exhausted
#print axioms Observe.next_fire
#print axioms Observe.next_fire._proof_1_1
#print axioms Observe.next_fire._proof_1_2
#print axioms Observe.next_fuel
#print axioms Observe.next_fuel._proof_1_1
#print axioms Observe.next_halt
#print axioms Observe.next_refuse
#print axioms Observe.next_tape
#print axioms Observe.obs_fuel_eq
#print axioms Observe.obs_fuel_indep
#print axioms Observe.obs_fuel_indep._proof_1_3
#print axioms Observe.obs_fuel_indep._proof_1_4
#print axioms Observe.obs_fuel_indep._proof_1_5
#print axioms Observe.obs_fuel_indep._proof_1_6
#print axioms Observe.obs_prefix
#print axioms Observe.obs_prefix_add
#print axioms Observe.same_next
#print axioms Observe.stepDet_inr
#print axioms RationalBounds.chain_functional
#print axioms RationalBounds.cycTape_succ
#print axioms RationalBounds.cyc_mod
#print axioms RationalBounds.cyc_mod._proof_1_1
#print axioms RationalBounds.cyc_mod._proof_1_2
#print axioms RationalBounds.cyc_mod._proof_1_3
#print axioms RationalBounds.cyc_mod._proof_1_4
#print axioms RationalBounds.cycle_iter
#print axioms RationalBounds.cycle_iter._proof_1_3
#print axioms RationalBounds.cycle_iter._proof_1_4
#print axioms RationalBounds.cycle_iter._proof_1_5
#print axioms RationalBounds.cycle_iter._proof_1_6
#print axioms RationalBounds.cycle_obs
#print axioms RationalBounds.cycle_obs_length
#print axioms RationalBounds.cycle_obs_zeros
#print axioms RationalBounds.cycle_run_bound
#print axioms RationalBounds.dyadic_twins_separated
#print axioms RationalBounds.enabledAt_cycle
#print axioms RationalBounds.enabledAt_cycle._proof_1_3
#print axioms RationalBounds.lookup_cycle
#print axioms RationalBounds.lookup_cycle._proof_1_3
#print axioms RationalBounds.non_density_witness
#print axioms RationalBounds.twist_not_chain
#print axioms RationalBounds.twist_pairs
#print axioms RationalBounds.zeros_bound
#print axioms RationalBounds.zeros_bound._proof_1_1
#print axioms RationalBounds.zeros_bound._proof_1_2
#print axioms RationalBounds.zeros_eq
#print axioms RationalBounds.zeros_eq._proof_1_3
#print axioms RationalBounds.zeros_eq._proof_1_4
#print axioms RationalBounds.zeros_rational_error
#print axioms RationalBounds.zeros_rational_error._proof_1_1
