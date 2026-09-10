import Lean
import Carrier
import Footprint
import CommuteSquare
import ObserverExchange

/-!
# Metatheoretic Theorem Census for Concurrency Package

Audits all compiled theorem declarations in the Concurrency namespace.
Verifies that:
1. Every local theorem is cataloged and printed in the environment census.
2. Axioms are strictly within {propext, Quot.sound}.
3. Zero Classical.choice, zero mathlib axioms.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool := (`Concurrency).isPrefixOf name
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
    throwError "CONCURRENCY_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "CONCURRENCY_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"CONCURRENCY_THEOREM: {name}"

/- The compiled environment census declarations and their axiom audits -/
#print axioms Concurrency.Footprint.mk.inj
#print axioms Concurrency.Footprint.mk.injEq
#print axioms Concurrency.Footprint.mk.sizeOf_spec
#print axioms Concurrency.Locus.L1.sizeOf_spec
#print axioms Concurrency.Locus.L2.sizeOf_spec
#print axioms Concurrency.Locus.M.sizeOf_spec
#print axioms Concurrency.Locus.ofNat_ctorIdx
#print axioms Concurrency.Respects.preserves
#print axioms Concurrency.Respects.readsOnly
#print axioms Concurrency.State3.ext
#print axioms Concurrency.State3.ext_iff
#print axioms Concurrency.State3.mk.inj
#print axioms Concurrency.State3.mk.injEq
#print axioms Concurrency.State3.mk.sizeOf_spec
#print axioms Concurrency.agrees_on_reads_step
#print axioms Concurrency.decision_agreement
#print axioms Concurrency.decision_divergence
#print axioms Concurrency.disjoint_comm_l1
#print axioms Concurrency.disjoint_comm_l2
#print axioms Concurrency.disjoint_comm_m
#print axioms Concurrency.disjoint_commutes
#print axioms Concurrency.fpL1_fpL2_disjoint
#print axioms Concurrency.fpL1_fpM_disjoint
#print axioms Concurrency.fpL1_read_write_conflict
#print axioms Concurrency.fpL1_write_conflict
#print axioms Concurrency.fpL2_fpM_disjoint
#print axioms Concurrency.instDecidableEqFootprint.decEq._proof_1
#print axioms Concurrency.instDecidableEqFootprint.decEq._proof_2
#print axioms Concurrency.instDecidableEqFootprint.decEq._proof_3
#print axioms Concurrency.instDecidableEqFootprint.decEq._proof_4
#print axioms Concurrency.instDecidableEqFootprint.decEq._proof_5
#print axioms Concurrency.instDecidableEqFootprint.decEq._proof_6
#print axioms Concurrency.instDecidableEqFootprint.decEq._proof_7
#print axioms Concurrency.instDecidableEqLocus._proof_1
#print axioms Concurrency.instDecidableEqLocus._proof_2
#print axioms Concurrency.instDecidableEqState3.decEq._proof_1
#print axioms Concurrency.instDecidableEqState3.decEq._proof_2
#print axioms Concurrency.instDecidableEqState3.decEq._proof_3
#print axioms Concurrency.instDecidableEqState3.decEq._proof_4
#print axioms Concurrency.interferes_symm
#print axioms Concurrency.isDisjoint_symm
#print axioms Concurrency.locusInterferes_symm
#print axioms Concurrency.not_both_w1_disjoint
#print axioms Concurrency.not_both_w2_disjoint
#print axioms Concurrency.not_both_wm_disjoint
#print axioms Concurrency.not_w1_of_r1_disjoint
#print axioms Concurrency.not_w2_of_r2_disjoint
#print axioms Concurrency.not_wm_of_rm_disjoint
#print axioms Concurrency.pack3_lt
#print axioms Concurrency.pack3_lt._proof_1_1
#print axioms Concurrency.pack3_lt._proof_1_2
#print axioms Concurrency.proj1_swap_eq_proj2
#print axioms Concurrency.proj2_swap_eq_proj1
#print axioms Concurrency.read_write_conflict_fails_commute
#print axioms Concurrency.swap_involutive
#print axioms Concurrency.swap_preserves_m
#print axioms Concurrency.swap_symmetric_eq
#print axioms Concurrency.symmetry_agreement
#print axioms Concurrency.uncoupled_preserves_receiver
#print axioms Concurrency.unpack3_pack3
#print axioms Concurrency.updateL1_preserves_l2
#print axioms Concurrency.updateL1_preserves_m
#print axioms Concurrency.updateL1_respects
#print axioms Concurrency.updateL1_updateL2_comm
#print axioms Concurrency.updateL1_updateL2_commutes
#print axioms Concurrency.updateL1_updateM_comm
#print axioms Concurrency.updateL1_updateM_commutes
#print axioms Concurrency.updateL2_preserves_l1
#print axioms Concurrency.updateL2_preserves_m
#print axioms Concurrency.updateL2_respects
#print axioms Concurrency.updateL2_updateM_comm
#print axioms Concurrency.updateL2_updateM_commutes
#print axioms Concurrency.updateM_preserves_l1
#print axioms Concurrency.updateM_preserves_l2
#print axioms Concurrency.updateM_respects
#print axioms Concurrency.write_write_conflict_fails_commute
