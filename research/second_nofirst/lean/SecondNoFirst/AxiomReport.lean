/-
AxiomReport: one report per theorem of this rung's package, across every
module of the library, the two reconstructions included.  The list is
regenerated from the modules themselves, and `verify_lean.py` derives the
same census independently and fails if the two differ.  Names are fully
qualified so the report text and this list are the same strings.
AuthorityEffect: None.
-/

import SecondNoFirst

-- Inert.lean (11)
#print axioms SecondNoFirst.Inert.demand_congr
#print axioms SecondNoFirst.Inert.stepE_impose
#print axioms SecondNoFirst.Inert.impose_preserves_demands
#print axioms SecondNoFirst.Inert.stepE_admitForm
#print axioms SecondNoFirst.Inert.getD_append_left
#print axioms SecondNoFirst.Inert.wfCtx_addForm_left
#print axioms SecondNoFirst.Inert.new_form_derives_nothing
#print axioms SecondNoFirst.Inert.collapsed_addForm
#print axioms SecondNoFirst.Inert.separable_addForm
#print axioms SecondNoFirst.Inert.admitForm_preserves_demands
#print axioms SecondNoFirst.Inert.three_kinds_are_demand_inert

-- Inherited.lean (10)
#print axioms SecondNoFirst.Inherited.pairsOf_cons
#print axioms SecondNoFirst.Inherited.pairsOf_mem
#print axioms SecondNoFirst.Inherited.demands_congr
#print axioms SecondNoFirst.Inherited.satB_grow
#print axioms SecondNoFirst.Inherited.demands_grow
#print axioms SecondNoFirst.Inherited.growth_generates
#print axioms SecondNoFirst.Inherited.fixpoint_reopens
#print axioms SecondNoFirst.Inherited.filter_of_false
#print axioms SecondNoFirst.Inherited.empty_commitment_has_no_demand
#print axioms SecondNoFirst.Inherited.empty_commitment_generates_nothing

-- Kernel.lean (7)
#print axioms SecondNoFirst.Sealed.insertNew_of_not_mem
#print axioms SecondNoFirst.Sealed.insertNew_of_mem
#print axioms SecondNoFirst.Sealed.separable_not_collapsed
#print axioms SecondNoFirst.Sealed.supply_no_op
#print axioms SecondNoFirst.Sealed.genesis_underivable
#print axioms SecondNoFirst.Sealed.underivable_of_empty
#print axioms SecondNoFirst.Sealed.collapsed_of_no_insts

-- NoFirst.lean (11)
#print axioms SecondNoFirst.NoFirst.supplies_preserve_regime
#print axioms SecondNoFirst.NoFirst.supply_preserves_demands
#print axioms SecondNoFirst.NoFirst.supplies_preserve_demands
#print axioms SecondNoFirst.NoFirst.demand_needs_label
#print axioms SecondNoFirst.NoFirst.demand_depends_only_on_the_label
#print axioms SecondNoFirst.NoFirst.grammar_carries_no_stake
#print axioms SecondNoFirst.NoFirst.no_first_demand
#print axioms SecondNoFirst.NoFirst.collapsed_not_separable
#print axioms SecondNoFirst.NoFirst.collapsed_of_not_separable
#print axioms SecondNoFirst.NoFirst.apart_demand_of_no_forms
#print axioms SecondNoFirst.NoFirst.demand_iff_apart_of_no_insts

-- Propagate.lean (22)
#print axioms SecondNoFirst.Propagate.growth_generates_pinned
#print axioms SecondNoFirst.Propagate.stepE_admitDatum
#print axioms SecondNoFirst.Propagate.growR_forms
#print axioms SecondNoFirst.Propagate.growR_insts
#print axioms SecondNoFirst.Propagate.growR_rules
#print axioms SecondNoFirst.Propagate.growR_data
#print axioms SecondNoFirst.Propagate.derivable_growR
#print axioms SecondNoFirst.Propagate.wfCtx_growR
#print axioms SecondNoFirst.Propagate.collapsed_of_growR
#print axioms SecondNoFirst.Propagate.growth_generates_apart
#print axioms SecondNoFirst.Propagate.growth_generates_apart_of_no_insts
#print axioms SecondNoFirst.Propagate.growth_generates_same
#print axioms SecondNoFirst.Propagate.mem_plug_of_hole
#print axioms SecondNoFirst.Propagate.fresh_profile
#print axioms SecondNoFirst.Propagate.collapsed_of_both_empty
#print axioms SecondNoFirst.Propagate.apart_at_most_one
#print axioms SecondNoFirst.Propagate.allApart_label
#print axioms SecondNoFirst.Propagate.allApart_demand_iff
#print axioms SecondNoFirst.Propagate.collapsed_trans
#print axioms SecondNoFirst.Propagate.apart_at_most_one_new_demand
#print axioms SecondNoFirst.Propagate.apart_no_old_demand
#print axioms SecondNoFirst.Propagate.apart_at_most_one_demand_after_growth

-- Run.lean (9)
#print axioms SecondNoFirst.Run.replayE_cons
#print axioms SecondNoFirst.Run.replayE_nil
#print axioms SecondNoFirst.Run.wf_addForm
#print axioms SecondNoFirst.Run.wf_addReq
#print axioms SecondNoFirst.Run.wf_step_inert
#print axioms SecondNoFirst.Run.demands_step_inert
#print axioms SecondNoFirst.Run.demands_replay_inert
#print axioms SecondNoFirst.Run.no_demand_is_first_under_an_inert_run
#print axioms SecondNoFirst.Run.free_stake_no_demand_along_any_run

-- Stake.lean (5)
#print axioms SecondNoFirst.Stake.stake_irrefl
#print axioms SecondNoFirst.Stake.demands_subset_labelled
#print axioms SecondNoFirst.Stake.free_stake_no_demand
#print axioms SecondNoFirst.Stake.labelled_cases
#print axioms SecondNoFirst.Stake.reconstruction_matches
