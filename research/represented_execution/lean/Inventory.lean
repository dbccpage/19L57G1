import Lean
import Execution
import Control
import Product
import Schedule
import Rename
import Runner

/-!
Metatheoretic audit apparatus: enumerate the compiled theorem declarations
of the `Execution`, `Control`, `Product`, `Schedule`, `Rename` and `Runner`
namespaces independently of source layout and of the printed dependency reports.  AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool :=
    (`Execution).isPrefixOf name || (`Control).isPrefixOf name ||
      (`Product).isPrefixOf name || (`Schedule).isPrefixOf name ||
      (`Rename).isPrefixOf name || (`Runner).isPrefixOf name
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


/- The compiler generates these additional theorem declarations for the
`Config`, `Controlled` and `State` structures (constructor injectivity and
the size specifications), and for the side conditions of the recursive proofs
and of the finite settings declared in `Schedule.lean`; and, for the
`Renaming` structure of `Rename.lean`, its four Prop-valued field
projections, which Lean classifies as theorems.  Their reports are included
beside the authored reports of the five modules, and the combined population
is compared with the independent environment census. -/
#print axioms Control.successors_complete._proof_1_1
#print axioms Product.fst_lt._proof_1_1
#print axioms Product.pack_lt._proof_1_1
#print axioms Product.prodSetting._proof_1
#print axioms Product.prodSetting._proof_2
#print axioms Product.prodSetting._proof_3
#print axioms Schedule.filter_range_eq_nil._proof_1_3
#print axioms Schedule.filter_range_eq_nil._proof_1_4
#print axioms Schedule.filter_range_eq_single._proof_1_3
#print axioms Schedule.filter_range_eq_single._proof_1_4
#print axioms Schedule.scheduled_no_branch._proof_1_1
#print axioms Schedule.two._proof_1
#print axioms Schedule.two._proof_2
#print axioms Schedule.two._proof_3
#print axioms Execution.Config.mk.inj
#print axioms Execution.Config.mk.injEq
#print axioms Execution.Config.mk.sizeOf_spec
#print axioms Control.Controlled.mk.inj
#print axioms Control.Controlled.mk.injEq
#print axioms Control.Controlled.mk.sizeOf_spec
#print axioms Control.Fired.exhausted.sizeOf_spec
#print axioms Control.Fired.noEdge.sizeOf_spec
#print axioms Control.Fired.ok.inj
#print axioms Control.Fired.ok.injEq
#print axioms Control.Fired.ok.sizeOf_spec
#print axioms Control.State.mk.inj
#print axioms Control.State.mk.injEq
#print axioms Control.State.mk.sizeOf_spec
#print axioms Control.Terminal.branch.sizeOf_spec
#print axioms Control.Terminal.exhausted.sizeOf_spec
#print axioms Control.Terminal.halt.sizeOf_spec
#print axioms Control.Terminal.ofNat_ctorIdx
#print axioms Control.Terminal.refuse.sizeOf_spec
#print axioms Control.enabled_program._proof_1_1
#print axioms Control.enabled_program._proof_1_2
#print axioms Control.encodeC_wf._proof_1_1
#print axioms Control.encodeC_wf._proof_1_2
#print axioms Control.encodeC_wf._proof_1_3
#print axioms Control.instDecidableEqTerminal._proof_1
#print axioms Control.instDecidableEqTerminal._proof_2
#print axioms Control.live_successor._proof_1_1
#print axioms Control.lookup_program_op._proof_1_1
#print axioms Control.lookup_program_op._proof_1_2
#print axioms Rename.Renaming.bwd_lt
#print axioms Rename.Renaming.fwd_lt
#print axioms Rename.Renaming.left
#print axioms Rename.Renaming.mk.inj
#print axioms Rename.Renaming.mk.injEq
#print axioms Rename.Renaming.mk.sizeOf_spec
#print axioms Rename.Renaming.right
#print axioms Rename.flipRenaming._proof_1
#print axioms Rename.getD_map._proof_1_3
#print axioms Rename.renameSetting._proof_1
#print axioms Rename.renameSetting._proof_2
#print axioms Rename.renameSetting._proof_3
#print axioms Rename.rename_fire._proof_1_1
#print axioms Rename.rename_fire._proof_1_4
#print axioms Runner.stepDetOf_of_two._proof_1_1
#print axioms Runner.stepDetOf_of_two._proof_1_2
