/-
AxiomReport: one report per theorem of this rung's package, across every
module of the library, the reconstructions included.  `verify_lean.py`
derives the same census independently from the compiled environment and
fails if the two differ, in either direction, so a dropped print is a
failure rather than a silence.  Names are fully qualified, so the report
text and this list are the same strings.
AuthorityEffect: None.
-/

import SecondProfile


-- Kernel.lean (17)
#print axioms SecondProfile.Sealed.insertNew_nil
#print axioms SecondProfile.Sealed.insertNew_of_not_mem
#print axioms SecondProfile.Sealed.insertNew_of_mem
#print axioms SecondProfile.Sealed.mem_insertNew
#print axioms SecondProfile.Sealed.separable_not_collapsed
#print axioms SecondProfile.Sealed.R2L_wf
#print axioms SecondProfile.Sealed.R2F_wf
#print axioms SecondProfile.Sealed.supply_no_op
#print axioms SecondProfile.Sealed.genesis_underivable
#print axioms SecondProfile.Sealed.underivable_of_empty
#print axioms SecondProfile.Sealed.collapsed_of_no_insts
#print axioms SecondProfile.Sealed.R2L_collapsed
#print axioms SecondProfile.Sealed.R2F_collapsed
#print axioms SecondProfile.Sealed.historyL_replays
#print axioms SecondProfile.Sealed.historyF_replays
#print axioms SecondProfile.Sealed.admission_without_expressive_increase
#print axioms SecondProfile.Sealed.replayE_append

-- Carry.lean (9)
#print axioms SecondProfile.Carry.map_inv
#print axioms SecondProfile.Carry.plug_mapCtx
#print axioms SecondProfile.Carry.plug_args_lt
#print axioms SecondProfile.Carry.wfCtx_mapCtx
#print axioms SecondProfile.Carry.derivable_fwd
#print axioms SecondProfile.Carry.derivable_bwd
#print axioms SecondProfile.Carry.derivable_mapCtx
#print axioms SecondProfile.Carry.separable_iso
#print axioms SecondProfile.Carry.collapsed_iso

-- Classes.lean (8)
#print axioms SecondProfile.Classes.collapsed_refl
#print axioms SecondProfile.Classes.collapsed_symm
#print axioms SecondProfile.Classes.collapsed_trans
#print axioms SecondProfile.Classes.holdsTwo_iso
#print axioms SecondProfile.Classes.reps_iso
#print axioms SecondProfile.Classes.holdsTwo_of_reps
#print axioms SecondProfile.Classes.reps_of_no_insts
#print axioms SecondProfile.Classes.no_twoness_without_insts

-- Stage.lean (11)
#print axioms SecondProfile.Stage.insertNew_le
#print axioms SecondProfile.Stage.step_parts_le
#print axioms SecondProfile.Stage.replay_parts_le
#print axioms SecondProfile.Stage.holdsTwo_parts
#print axioms SecondProfile.Stage.twoness_needs_four
#print axioms SecondProfile.Stage.twoness_needs_two_L
#print axioms SecondProfile.Stage.twoness_needs_two_F
#print axioms SecondProfile.Stage.twoness_at_four
#print axioms SecondProfile.Stage.twoness_at_two_L
#print axioms SecondProfile.Stage.twoness_at_two_F
#print axioms SecondProfile.Stage.two_classes_at_four

-- Keep.lean (5)
#print axioms SecondProfile.Keep.getD_append_lt
#print axioms SecondProfile.Keep.separable_step_keep
#print axioms SecondProfile.Keep.holdsTwo_step_keep
#print axioms SecondProfile.Keep.twoness_lost_by_inst
#print axioms SecondProfile.Keep.twoness_lost_by_rule
