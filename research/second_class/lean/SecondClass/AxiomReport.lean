/-
AxiomReport: one report per theorem of this rung's package, across every
module of the library, the reconstructions included.  `verify_lean.py`
derives the same census independently from the compiled environment and
fails if the two differ, in either direction, so a dropped print is a
failure rather than a silence.  Names are fully qualified, so the report
text and this list are the same strings.
AuthorityEffect: None.
-/

import SecondClass


-- Kernel.lean (17)
#print axioms SecondClass.Sealed.insertNew_nil
#print axioms SecondClass.Sealed.insertNew_of_not_mem
#print axioms SecondClass.Sealed.insertNew_of_mem
#print axioms SecondClass.Sealed.mem_insertNew
#print axioms SecondClass.Sealed.separable_not_collapsed
#print axioms SecondClass.Sealed.R2L_wf
#print axioms SecondClass.Sealed.R2F_wf
#print axioms SecondClass.Sealed.supply_no_op
#print axioms SecondClass.Sealed.genesis_underivable
#print axioms SecondClass.Sealed.underivable_of_empty
#print axioms SecondClass.Sealed.collapsed_of_no_insts
#print axioms SecondClass.Sealed.R2L_collapsed
#print axioms SecondClass.Sealed.R2F_collapsed
#print axioms SecondClass.Sealed.historyL_replays
#print axioms SecondClass.Sealed.historyF_replays
#print axioms SecondClass.Sealed.admission_without_expressive_increase
#print axioms SecondClass.Sealed.replayE_append

-- Rounds.lean (8)
#print axioms SecondClass.Rounds.replayE_cons
#print axioms SecondClass.Rounds.insertNew_grows
#print axioms SecondClass.Rounds.step_parts
#print axioms SecondClass.Rounds.growths_counted
#print axioms SecondClass.Rounds.rest_counted
#print axioms SecondClass.Rounds.changes_counted
#print axioms SecondClass.Rounds.replayE_split
#print axioms SecondClass.Rounds.still_of_no_changes

-- Count.lean (15)
#print axioms SecondClass.Count.nodup_map_of_inv
#print axioms SecondClass.Count.length_le_of_nodup_sub
#print axioms SecondClass.Count.count_le_of_inv
#print axioms SecondClass.Count.range_nodup
#print axioms SecondClass.Count.data_le
#print axioms SecondClass.Count.forms_le
#print axioms SecondClass.Count.iso_data
#print axioms SecondClass.Count.iso_forms
#print axioms SecondClass.Count.sortPair_of_le
#print axioms SecondClass.Count.sortPair_map
#print axioms SecondClass.Count.insts_le
#print axioms SecondClass.Count.rules_le
#print axioms SecondClass.Count.reqs_le
#print axioms SecondClass.Count.components_iso
#print axioms SecondClass.Count.size_iso

-- Clean.lean (7)
#print axioms SecondClass.Clean.nodup_insertNew
#print axioms SecondClass.Clean.getD_append_lt
#print axioms SecondClass.Clean.clean_step
#print axioms SecondClass.Clean.clean_replay
#print axioms SecondClass.Clean.genesis_clean
#print axioms SecondClass.Clean.R2L_clean
#print axioms SecondClass.Clean.R2F_clean

-- Recur.lean (4)
#print axioms SecondClass.Recur.no_return_class
#print axioms SecondClass.Recur.recurrence_is_stutter
#print axioms SecondClass.Recur.counts_of_class
#print axioms SecondClass.Recur.counts_of_class_genesis

-- Counter.lean (7)
#print axioms SecondClass.Counter.insts_need_nodup
#print axioms SecondClass.Counter.insts_need_wf
#print axioms SecondClass.Counter.rules_need_nodup
#print axioms SecondClass.Counter.rules_need_wf
#print axioms SecondClass.Counter.reqs_need_nodup
#print axioms SecondClass.Counter.reqs_need_wf
#print axioms SecondClass.Counter.counts_not_of_class
