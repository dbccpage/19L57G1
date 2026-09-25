/-
AxiomReport: one report per theorem of this rung's package, across every
module of the library, the reconstruction included.  `verify_lean.py`
derives the same census independently from the compiled environment and
fails if the two differ, in either direction, so a dropped print is a
failure rather than a silence.  Names are fully qualified, so the report
text and this list are the same strings.
AuthorityEffect: None.
-/

import SecondDuration


-- Kernel.lean (17)
#print axioms SecondDuration.Sealed.insertNew_nil
#print axioms SecondDuration.Sealed.insertNew_of_not_mem
#print axioms SecondDuration.Sealed.insertNew_of_mem
#print axioms SecondDuration.Sealed.mem_insertNew
#print axioms SecondDuration.Sealed.separable_not_collapsed
#print axioms SecondDuration.Sealed.R2L_wf
#print axioms SecondDuration.Sealed.R2F_wf
#print axioms SecondDuration.Sealed.supply_no_op
#print axioms SecondDuration.Sealed.genesis_underivable
#print axioms SecondDuration.Sealed.underivable_of_empty
#print axioms SecondDuration.Sealed.collapsed_of_no_insts
#print axioms SecondDuration.Sealed.R2L_collapsed
#print axioms SecondDuration.Sealed.R2F_collapsed
#print axioms SecondDuration.Sealed.historyL_replays
#print axioms SecondDuration.Sealed.historyF_replays
#print axioms SecondDuration.Sealed.admission_without_expressive_increase
#print axioms SecondDuration.Sealed.replayE_append

-- Rounds.lean (10)
#print axioms SecondDuration.Rounds.replayE_cons
#print axioms SecondDuration.Rounds.insertNew_grows
#print axioms SecondDuration.Rounds.step_parts
#print axioms SecondDuration.Rounds.growths_counted
#print axioms SecondDuration.Rounds.rest_counted
#print axioms SecondDuration.Rounds.growths_given_base
#print axioms SecondDuration.Rounds.rest_given_base
#print axioms SecondDuration.Rounds.after_le_rest
#print axioms SecondDuration.Rounds.naming_step
#print axioms SecondDuration.Rounds.naming_bounded

-- Gaps.lean (6)
#print axioms SecondDuration.Gaps.lead_splits
#print axioms SecondDuration.Gaps.segment_not_given_base
#print axioms SecondDuration.Gaps.gap_splits
#print axioms SecondDuration.Gaps.gap_not_from_genesis
#print axioms SecondDuration.Gaps.tail_forced
#print axioms SecondDuration.Gaps.pinned_by_requirement
