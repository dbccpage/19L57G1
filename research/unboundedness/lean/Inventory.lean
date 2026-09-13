import Lean
import Driver
import Unboundedness
import CostFloor
import ClosedFixpoint
import Metric
import Continuum
import TwoLociSystem
import Reader

/-!
Metatheoretic audit apparatus: enumerate the compiled theorem declarations
of this package's namespaces independently of source layout and of the
printed dependency reports.  AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let prefixes : List Name :=
    [ `Unboundedness, `CostFloor, `ClosedFixpoint, `Ignition.Driver
    , `Metric, `Continuum, `TwoLociSystem, `Reader ]
  let inScope (name : Name) : Bool :=
    prefixes.any (fun p => p.isPrefixOf name)
  let environment ← getEnv
  let names := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if inScope name && !isPrivateName name then name.toString :: found else found
      | _ => found
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "UNBOUNDEDNESS_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"UNBOUNDEDNESS_THEOREM: {name}"

/- The compiler generates these additional theorem declarations (equation
lemmas, auxiliary proof terms of `omega`/`decide`/`simp`).  Their reports
are included beside the authored reports, and the combined population is
compared with the independent environment census. -/
#print axioms ClosedFixpoint.no_four_closed_rounds_on_three_data._proof_1_1
#print axioms ClosedFixpoint.no_two_closed_rounds_on_two_data._proof_1_1
#print axioms ClosedFixpoint.reading_F_max_rounds._proof_1_1
#print axioms ClosedFixpoint.reading_L_max_rounds._proof_1_1
#print axioms Continuum.flipFin._proof_1
#print axioms Continuum.flipFin._proof_2
#print axioms Continuum.flipFin._proof_3
#print axioms Continuum.flipFin._proof_4
#print axioms CostFloor.valid_response_len_ge_two_at_genesis._proof_1_4
#print axioms CostFloor.valid_response_len_pos_of_collapsed._proof_1_3
#print axioms Ignition.Driver.DriverPath.brecOn
#print axioms Ignition.Driver.Measure.mu1.sizeOf_spec
#print axioms Ignition.Driver.Measure.mu2.sizeOf_spec
#print axioms Ignition.Driver.Measure.ofNat_ctorIdx
#print axioms Ignition.Driver.guarded_driver_refuses_at_round_bound._proof_1_1
#print axioms Ignition.Driver.instDecidableEqMeasure._proof_1
#print axioms Ignition.Driver.instDecidableEqMeasure._proof_2
#print axioms Ignition.Driver.isMin_no_rule._proof_1_1
#print axioms Ignition.Driver.lexLE_trans._proof_1_1
#print axioms Metric.eventually_periodic_dense._proof_1_1
#print axioms Metric.eventually_periodic_dense._proof_1_2
#print axioms Metric.functional_closed_limit._proof_1_1
#print axioms Metric.functional_closed_limit._proof_1_2
#print axioms Metric.functional_closed_limit._proof_1_3
#print axioms Metric.functional_closed_limit._proof_1_4
#print axioms Metric.functional_thread_is_eventually_periodic._proof_1_1
#print axioms Metric.functional_thread_is_eventually_periodic._proof_1_2
#print axioms Metric.functional_thread_is_eventually_periodic._proof_1_3
#print axioms Metric.functional_thread_is_eventually_periodic._proof_1_4
#print axioms Metric.functional_thread_is_eventually_periodic._proof_1_5
#print axioms Metric.nonfuncSeq2._proof_1
#print axioms Metric.nonfuncSeq2._proof_2
#print axioms Metric.nonfuncSeq3._proof_1
#print axioms Metric.nonfuncSeq3._proof_2
#print axioms Metric.nonfuncSeq3._proof_3
#print axioms Metric.nonfunctional_open_ball._proof_1_1
#print axioms Metric.nonfunctional_open_ball._proof_1_2
#print axioms Metric.nonfunctional_open_ball._proof_1_3
#print axioms Metric.nonfunctional_open_ball._proof_1_4
#print axioms Metric.seqAgrees.eq_1
#print axioms Metric.seqAgrees.eq_2
#print axioms Metric.seqAgrees.eq_def
#print axioms Metric.seqAgrees_iff._simp_1_6
#print axioms Metric.threadAgrees.eq_1
#print axioms Reader.Recorded.mk.inj
#print axioms Reader.Recorded.mk.injEq
#print axioms Reader.Recorded.mk.sizeOf_spec
#print axioms Reader.encodeR_wf._proof_1_1
#print axioms Reader.encodeR_wf._proof_1_2
#print axioms Reader.encodeR_wf._proof_1_3
#print axioms Reader.lookup_rprogram_op._proof_1_1
#print axioms Reader.lookup_rprogram_op._proof_1_2
#print axioms Reader.renabled_rprogram._proof_1_1
#print axioms Reader.renabled_rprogram._proof_1_2
#print axioms Reader.rsuccessors_complete._proof_1_1
#print axioms TwoLociSystem.seqFst._proof_1
#print axioms TwoLociSystem.seqPack._proof_1
#print axioms TwoLociSystem.seqSnd._proof_1
#print axioms TwoLociSystem.stageFst._proof_1
#print axioms TwoLociSystem.stagePack._proof_1
#print axioms TwoLociSystem.stageSnd._proof_1
#print axioms TwoLociSystem.threadFst._proof_1
#print axioms TwoLociSystem.threadPack._proof_1
#print axioms TwoLociSystem.threadProdSnd._proof_1
#print axioms TwoLociSystem.threadSnd._proof_1
#print axioms Unboundedness.driver_data_mono._proof_1_1
#print axioms Unboundedness.respond_data_mono._proof_1_1
#print axioms Unboundedness.xstep_unbounded_exists._proof_1_1
#print axioms Reader.demoSetting._proof_1
#print axioms Reader.demoSetting._proof_2
