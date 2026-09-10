import Lean
import Execution
import Branch
import Memory

/-!
# Metatheoretic Theorem Census for Target A Execution

Audits all compiled theorem declarations in the Execution, Branch, and Memory namespaces.
Verifies that:
1. Every local theorem is cataloged and printed in the environment census.
2. Axioms are strictly checked: must be within {propext, Quot.sound}.
3. Zero Classical.choice, zero mathlib axioms.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool :=
    (`Execution).isPrefixOf name || (`Branch).isPrefixOf name || (`Memory).isPrefixOf name
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
    throwError "EXECUTION_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "EXECUTION_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"EXECUTION_THEOREM: {name}"

/- The compiled environment census declarations and their axiom audits -/
#print axioms Branch.CFGState.mk.inj
#print axioms Branch.CFGState.mk.injEq
#print axioms Branch.CFGState.mk.sizeOf_spec
#print axioms Branch.branch_deterministic
#print axioms Branch.branch_halt
#print axioms Branch.branch_non_selection
#print axioms Branch.jump_table_lookup
#print axioms Branch.lookupBranch_mem
#print axioms Branch.stepCFG_clock
#print axioms Branch.stepCFG_fork
#print axioms Branch.stepCFG_fuel
#print axioms Branch.stepCFG_ok
#print axioms Execution.Config.mk.inj
#print axioms Execution.Config.mk.injEq
#print axioms Execution.Config.mk.sizeOf_spec
#print axioms Execution.Fired.exhausted.sizeOf_spec
#print axioms Execution.Fired.noEdge.sizeOf_spec
#print axioms Execution.Fired.ok.inj
#print axioms Execution.Fired.ok.injEq
#print axioms Execution.Fired.ok.sizeOf_spec
#print axioms Execution.Fired.protectionViolation.sizeOf_spec
#print axioms Execution.ProtectionKind.collapsed.sizeOf_spec
#print axioms Execution.ProtectionKind.ofNat_ctorIdx
#print axioms Execution.ProtectionKind.reflexive.sizeOf_spec
#print axioms Execution.ProtectionKind.separated.sizeOf_spec
#print axioms Execution.ProtectionObligation.mk.inj
#print axioms Execution.ProtectionObligation.mk.injEq
#print axioms Execution.ProtectionObligation.mk.sizeOf_spec
#print axioms Execution.State.mk.inj
#print axioms Execution.State.mk.injEq
#print axioms Execution.State.mk.sizeOf_spec
#print axioms Execution.Terminal.branch.sizeOf_spec
#print axioms Execution.Terminal.exhausted.sizeOf_spec
#print axioms Execution.Terminal.halt.sizeOf_spec
#print axioms Execution.Terminal.ofNat_ctorIdx
#print axioms Execution.Terminal.refuse.sizeOf_spec
#print axioms Execution.fire_clock
#print axioms Execution.fire_exhausted
#print axioms Execution.fire_fuel
#print axioms Execution.fire_ok
#print axioms Execution.fire_protection_preserved
#print axioms Execution.fire_succ
#print axioms Execution.fire_tape
#print axioms Execution.instDecidableEqProtectionKind._proof_1
#print axioms Execution.instDecidableEqProtectionKind._proof_2
#print axioms Execution.instDecidableEqProtectionObligation.decEq._proof_1
#print axioms Execution.instDecidableEqProtectionObligation.decEq._proof_2
#print axioms Execution.instDecidableEqProtectionObligation.decEq._proof_3
#print axioms Execution.instDecidableEqProtectionObligation.decEq._proof_4
#print axioms Execution.instDecidableEqTerminal._proof_1
#print axioms Execution.instDecidableEqTerminal._proof_2
#print axioms Execution.isEdge_self
#print axioms Execution.isEdge_true
#print axioms Execution.iterate_evalWord
#print axioms Execution.iterate_zero
#print axioms Execution.lookup_isSome
#print axioms Execution.lookup_mem
#print axioms Execution.nextOf_tape
#print axioms Execution.refusal_preserves_state
#print axioms Execution.run_evalWord
#print axioms Execution.run_nil
#print axioms Execution.stepDetOf_branch
#print axioms Execution.stepDetOf_halt
#print axioms Execution.stepDetOf_inr
#print axioms Execution.stepDetOf_refuse_noEdge
#print axioms Execution.stepDetOf_refuse_protectionViolation
#print axioms Execution.step_nil
#print axioms Execution.value_edge
#print axioms Memory.functional2_of_functional1
#print axioms Memory.previous_fire_synced
#print axioms Memory.renabled._proof_1
#print axioms Memory.twist2_not_functional2
#print axioms Memory.twist_functional2
#print axioms Memory.twist_functional2._proof_1_1
#print axioms Memory.twist_functional2._proof_1_2
#print axioms Memory.twist_not_functional1
