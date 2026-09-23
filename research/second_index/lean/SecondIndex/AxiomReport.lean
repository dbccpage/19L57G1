/-
AxiomReport: one report per theorem of this rung's package, across every
module of the library, the two reconstructions included.  `verify_lean.py`
derives the same census independently from the compiled environment and
fails if the two differ, in either direction, so a dropped print is a
failure rather than a silence.  Names are fully qualified, so the report
text and this list are the same strings.
AuthorityEffect: None.
-/

import SecondIndex


-- Countermodel.lean (14)
#print axioms SecondIndex.Countermodel.shared_regime_of_two_histories
#print axioms SecondIndex.Countermodel.twoData_demand
#print axioms SecondIndex.Countermodel.twoData_has_demand
#print axioms SecondIndex.Countermodel.separated_separates
#print axioms SecondIndex.Countermodel.separated_has_no_demand
#print axioms SecondIndex.Countermodel.no_demand_at_small_prefix
#print axioms SecondIndex.Countermodel.index_of_historyA
#print axioms SecondIndex.Countermodel.index_of_historyB
#print axioms SecondIndex.Countermodel.index_of_ceaseHistory
#print axioms SecondIndex.Countermodel.index_is_not_a_function_of_the_reached_regime
#print axioms SecondIndex.Countermodel.no_state_function_gives_the_index
#print axioms SecondIndex.Countermodel.the_ceasing_event_is_not_inert
#print axioms SecondIndex.Countermodel.demand_can_cease
#print axioms SecondIndex.Countermodel.first_demand_index

-- Index.lean (29)
#print axioms SecondIndex.Index.stateAt_zero
#print axioms SecondIndex.Index.stateAt_full
#print axioms SecondIndex.Index.replayE_singleton
#print axioms SecondIndex.Index.stateAt_succ
#print axioms SecondIndex.Index.quiet_before_the_index
#print axioms SecondIndex.Index.first_demand_unique
#print axioms SecondIndex.Index.first_demand_zero_iff_base_carries_one
#print axioms SecondIndex.Index.free_stake_has_no_index
#print axioms SecondIndex.Index.stepE_admitDatum
#print axioms SecondIndex.Index.stepE_admitInst
#print axioms SecondIndex.Index.stepE_admitRuleAll
#print axioms SecondIndex.Index.wf_addDatum
#print axioms SecondIndex.Index.wf_addInst
#print axioms SecondIndex.Index.wf_addRule
#print axioms SecondIndex.Index.wf_step_any
#print axioms SecondIndex.Index.wf_replayE
#print axioms SecondIndex.Index.wf_stateAt
#print axioms SecondIndex.Index.first_demand_follows_a_changing_event
#print axioms SecondIndex.Index.inert_run_carries_no_index
#print axioms SecondIndex.Index.demand_needs_two_data
#print axioms SecondIndex.Index.no_demand_of_data_le_one
#print axioms SecondIndex.Index.data_of_step
#print axioms SecondIndex.Index.data_le_step
#print axioms SecondIndex.Index.data_le_replay
#print axioms SecondIndex.Index.data_le_stateAt
#print axioms SecondIndex.Index.no_index_below_two_from_the_empty_base
#print axioms SecondIndex.Index.least_witness_from
#print axioms SecondIndex.Index.least_witness
#print axioms SecondIndex.Index.first_demand_exists_when_a_demand_is_decidable

-- Inherited.lean (27)
#print axioms SecondIndex.Inherited.stake_irrefl
#print axioms SecondIndex.Inherited.demands_subset_labelled
#print axioms SecondIndex.Inherited.free_stake_no_demand
#print axioms SecondIndex.Inherited.labelled_cases
#print axioms SecondIndex.Inherited.supply_preserves_demands
#print axioms SecondIndex.Inherited.demand_needs_label
#print axioms SecondIndex.Inherited.collapsed_not_separable
#print axioms SecondIndex.Inherited.collapsed_of_not_separable
#print axioms SecondIndex.Inherited.apart_demand_of_no_forms
#print axioms SecondIndex.Inherited.demand_iff_apart_of_no_insts
#print axioms SecondIndex.Inherited.demand_congr
#print axioms SecondIndex.Inherited.stepE_impose
#print axioms SecondIndex.Inherited.impose_preserves_demands
#print axioms SecondIndex.Inherited.stepE_admitForm
#print axioms SecondIndex.Inherited.getD_append_left
#print axioms SecondIndex.Inherited.wfCtx_addForm_left
#print axioms SecondIndex.Inherited.new_form_derives_nothing
#print axioms SecondIndex.Inherited.collapsed_addForm
#print axioms SecondIndex.Inherited.separable_addForm
#print axioms SecondIndex.Inherited.admitForm_preserves_demands
#print axioms SecondIndex.Inherited.replayE_cons
#print axioms SecondIndex.Inherited.replayE_nil
#print axioms SecondIndex.Inherited.wf_addForm
#print axioms SecondIndex.Inherited.wf_addReq
#print axioms SecondIndex.Inherited.wf_step_inert
#print axioms SecondIndex.Inherited.demands_step_inert
#print axioms SecondIndex.Inherited.demands_replay_inert

-- Kernel.lean (17)
#print axioms SecondIndex.Sealed.insertNew_nil
#print axioms SecondIndex.Sealed.insertNew_of_not_mem
#print axioms SecondIndex.Sealed.insertNew_of_mem
#print axioms SecondIndex.Sealed.mem_insertNew
#print axioms SecondIndex.Sealed.separable_not_collapsed
#print axioms SecondIndex.Sealed.R2L_wf
#print axioms SecondIndex.Sealed.R2F_wf
#print axioms SecondIndex.Sealed.supply_no_op
#print axioms SecondIndex.Sealed.genesis_underivable
#print axioms SecondIndex.Sealed.underivable_of_empty
#print axioms SecondIndex.Sealed.collapsed_of_no_insts
#print axioms SecondIndex.Sealed.R2L_collapsed
#print axioms SecondIndex.Sealed.R2F_collapsed
#print axioms SecondIndex.Sealed.historyL_replays
#print axioms SecondIndex.Sealed.historyF_replays
#print axioms SecondIndex.Sealed.admission_without_expressive_increase
#print axioms SecondIndex.Sealed.replayE_append
