/-
AxiomReport: one report per theorem of this rung's package, across every
module of the library, the reconstructions included.  `verify_lean.py`
derives the same census independently from the compiled environment and
fails if the two differ, in either direction, so a dropped print is a
failure rather than a silence.  Names are fully qualified, so the report
text and this list are the same strings.
AuthorityEffect: None.
-/

import SecondResponse


-- Kernel.lean (17)
#print axioms SecondResponse.Sealed.insertNew_nil
#print axioms SecondResponse.Sealed.insertNew_of_not_mem
#print axioms SecondResponse.Sealed.insertNew_of_mem
#print axioms SecondResponse.Sealed.mem_insertNew
#print axioms SecondResponse.Sealed.separable_not_collapsed
#print axioms SecondResponse.Sealed.R2L_wf
#print axioms SecondResponse.Sealed.R2F_wf
#print axioms SecondResponse.Sealed.supply_no_op
#print axioms SecondResponse.Sealed.genesis_underivable
#print axioms SecondResponse.Sealed.underivable_of_empty
#print axioms SecondResponse.Sealed.collapsed_of_no_insts
#print axioms SecondResponse.Sealed.R2L_collapsed
#print axioms SecondResponse.Sealed.R2F_collapsed
#print axioms SecondResponse.Sealed.historyL_replays
#print axioms SecondResponse.Sealed.historyF_replays
#print axioms SecondResponse.Sealed.admission_without_expressive_increase
#print axioms SecondResponse.Sealed.replayE_append

-- Carry.lean (7)
#print axioms SecondResponse.Carry.map_inv
#print axioms SecondResponse.Carry.plug_mapCtx
#print axioms SecondResponse.Carry.plug_args_lt
#print axioms SecondResponse.Carry.wfCtx_mapCtx
#print axioms SecondResponse.Carry.derivable_fwd
#print axioms SecondResponse.Carry.derivable_bwd
#print axioms SecondResponse.Carry.derivable_mapCtx

-- Exhaust.lean (8)
#print axioms SecondResponse.Exhaust.exhausted_iff_not_distinguishes
#print axioms SecondResponse.Exhaust.holdsTwo_iff_distinguishes
#print axioms SecondResponse.Exhaust.exhausted_of_rule
#print axioms SecondResponse.Exhaust.exhausted_of_no_inst
#print axioms SecondResponse.Exhaust.exhausted_of_le_one
#print axioms SecondResponse.Exhaust.exhausted_iso
#print axioms SecondResponse.Exhaust.no_exhausted_at_genesis
#print axioms SecondResponse.Exhaust.exhaustion_at_one

-- ExhaustStep.lean (11)
#print axioms SecondResponse.ExhaustStep.getD_append_lt
#print axioms SecondResponse.ExhaustStep.step_data_le
#print axioms SecondResponse.ExhaustStep.ctx_step_keep
#print axioms SecondResponse.ExhaustStep.separable_step_keep
#print axioms SecondResponse.ExhaustStep.distinguishes_step_keep
#print axioms SecondResponse.ExhaustStep.exhausted_step_keep
#print axioms SecondResponse.ExhaustStep.fresh_form_exhausted
#print axioms SecondResponse.ExhaustStep.exhaustion_begun_by_inst
#print axioms SecondResponse.ExhaustStep.exhaustion_begun_by_rule
#print axioms SecondResponse.ExhaustStep.exhaustion_ended_by_datum
#print axioms SecondResponse.ExhaustStep.exhaustion_ended_by_inst

-- Move.lean (13)
#print axioms SecondResponse.Move.mem_plug_of_hole
#print axioms SecondResponse.Move.derivable_inst_unmentioned
#print axioms SecondResponse.Move.separable_inst_unmentioned
#print axioms SecondResponse.Move.collapsed_inst_unmentioned
#print axioms SecondResponse.Move.slots_ok_of_plug_mem
#print axioms SecondResponse.Move.collapsed_step_keep
#print axioms SecondResponse.Move.step_wf
#print axioms SecondResponse.Move.separation_needs_mention
#print axioms SecondResponse.Move.collapse_needs_mention_or_rule
#print axioms SecondResponse.Move.moved_pairs_meet_mentions
#print axioms SecondResponse.Move.separation_needs_inst
#print axioms SecondResponse.Move.one_inst_moves_two_pairs
#print axioms SecondResponse.Move.response_collapses_a_pair
