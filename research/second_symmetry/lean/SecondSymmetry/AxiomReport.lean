/-
AxiomReport: one report per theorem of this rung's package, across every
module of the library, the two reconstructions included.  `verify_lean.py`
derives the same census independently from the compiled environment and
fails if the two differ, in either direction, so a dropped print is a
failure rather than a silence.  Names are fully qualified, so the report
text and this list are the same strings.
AuthorityEffect: None.
-/

import SecondSymmetry

-- Kernel.lean (17)
#print axioms SecondSymmetry.Sealed.insertNew_nil
#print axioms SecondSymmetry.Sealed.insertNew_of_not_mem
#print axioms SecondSymmetry.Sealed.insertNew_of_mem
#print axioms SecondSymmetry.Sealed.mem_insertNew
#print axioms SecondSymmetry.Sealed.separable_not_collapsed
#print axioms SecondSymmetry.Sealed.R2L_wf
#print axioms SecondSymmetry.Sealed.R2F_wf
#print axioms SecondSymmetry.Sealed.supply_no_op
#print axioms SecondSymmetry.Sealed.genesis_underivable
#print axioms SecondSymmetry.Sealed.underivable_of_empty
#print axioms SecondSymmetry.Sealed.collapsed_of_no_insts
#print axioms SecondSymmetry.Sealed.R2L_collapsed
#print axioms SecondSymmetry.Sealed.R2F_collapsed
#print axioms SecondSymmetry.Sealed.historyL_replays
#print axioms SecondSymmetry.Sealed.historyF_replays
#print axioms SecondSymmetry.Sealed.admission_without_expressive_increase
#print axioms SecondSymmetry.Sealed.replayE_append

-- IsoKernel.lean (0)

-- Aut.lean (7)
#print axioms SecondSymmetry.Aut.sameMaps_symm
#print axioms SecondSymmetry.Aut.supply_keeps
#print axioms SecondSymmetry.Aut.stepE_inst
#print axioms SecondSymmetry.Aut.stepE_rule
#print axioms SecondSymmetry.Aut.stepE_req
#print axioms SecondSymmetry.Aut.stepE_datum
#print axioms SecondSymmetry.Aut.stepE_form

-- Meet.lean (20)
#print axioms SecondSymmetry.Aut.map_fix
#print axioms SecondSymmetry.Aut.map_agree
#print axioms SecondSymmetry.Aut.inst_back
#print axioms SecondSymmetry.Aut.inst_fwd_back
#print axioms SecondSymmetry.Aut.sortPair_round
#print axioms SecondSymmetry.Aut.inst_fixed_of_survives
#print axioms SecondSymmetry.Aut.inst_survives_of_fixed
#print axioms SecondSymmetry.Aut.inst_descends_of_fixed
#print axioms SecondSymmetry.Aut.inst_meet
#print axioms SecondSymmetry.Aut.inst_meet_after
#print axioms SecondSymmetry.Aut.rule_fixed_of_survives
#print axioms SecondSymmetry.Aut.rule_survives_of_fixed
#print axioms SecondSymmetry.Aut.rule_descends_of_fixed
#print axioms SecondSymmetry.Aut.rule_meet
#print axioms SecondSymmetry.Aut.rule_meet_after
#print axioms SecondSymmetry.Aut.req_fixed_of_survives
#print axioms SecondSymmetry.Aut.req_survives_of_fixed
#print axioms SecondSymmetry.Aut.req_descends_of_fixed
#print axioms SecondSymmetry.Aut.req_meet
#print axioms SecondSymmetry.Aut.req_meet_after

-- Grow.lean (13)
#print axioms SecondSymmetry.Aut.ext_lt
#print axioms SecondSymmetry.Aut.ext_ge
#print axioms SecondSymmetry.Aut.ext_range
#print axioms SecondSymmetry.Aut.ext_inverse
#print axioms SecondSymmetry.Aut.datum_lift
#print axioms SecondSymmetry.Aut.getD_append_lt
#print axioms SecondSymmetry.Aut.form_lift
#print axioms SecondSymmetry.Aut.insertNew_cases
#print axioms SecondSymmetry.Aut.size_step
#print axioms SecondSymmetry.Aut.replayE_cons
#print axioms SecondSymmetry.Aut.size_counts_changes
#print axioms SecondSymmetry.Aut.size_replay_mono
#print axioms SecondSymmetry.Aut.no_return

-- Witness.lean (7)
#print axioms SecondSymmetry.Aut.inst_loss
#print axioms SecondSymmetry.Aut.inst_gain
#print axioms SecondSymmetry.Aut.rule_loss
#print axioms SecondSymmetry.Aut.rule_gain
#print axioms SecondSymmetry.Aut.req_loss
#print axioms SecondSymmetry.Aut.req_gain
#print axioms SecondSymmetry.Aut.kinds_move_both_ways
