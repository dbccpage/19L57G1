/-
AxiomReport: one report per theorem of this rung's package, across every
module of the library, the reconstruction included.  `verify_lean.py`
derives the same census independently from the compiled environment and
fails if the two differ, in either direction, so a dropped print is a
failure rather than a silence.  Names are fully qualified, so the report
text and this list are the same strings.
AuthorityEffect: None.
-/

import SecondSuccession

-- Kernel.lean (17)
#print axioms SecondSuccession.Sealed.insertNew_nil
#print axioms SecondSuccession.Sealed.insertNew_of_not_mem
#print axioms SecondSuccession.Sealed.insertNew_of_mem
#print axioms SecondSuccession.Sealed.mem_insertNew
#print axioms SecondSuccession.Sealed.separable_not_collapsed
#print axioms SecondSuccession.Sealed.R2L_wf
#print axioms SecondSuccession.Sealed.R2F_wf
#print axioms SecondSuccession.Sealed.supply_no_op
#print axioms SecondSuccession.Sealed.genesis_underivable
#print axioms SecondSuccession.Sealed.underivable_of_empty
#print axioms SecondSuccession.Sealed.collapsed_of_no_insts
#print axioms SecondSuccession.Sealed.R2L_collapsed
#print axioms SecondSuccession.Sealed.R2F_collapsed
#print axioms SecondSuccession.Sealed.historyL_replays
#print axioms SecondSuccession.Sealed.historyF_replays
#print axioms SecondSuccession.Sealed.admission_without_expressive_increase
#print axioms SecondSuccession.Sealed.replayE_append

-- Count.lean (11)
#print axioms SecondSuccession.Count.size_genesis
#print axioms SecondSuccession.Count.replayE_cons
#print axioms SecondSuccession.Count.supply_uncounted
#print axioms SecondSuccession.Count.insertNew_grows
#print axioms SecondSuccession.Count.step_grows
#print axioms SecondSuccession.Count.changes_counted
#print axioms SecondSuccession.Count.changes_path_free
#print axioms SecondSuccession.Count.changes_from_genesis
#print axioms SecondSuccession.Count.changes_given_base
#print axioms SecondSuccession.Count.changes_le_admitting
#print axioms SecondSuccession.Count.admitting_le_every

-- Readings.lean (6)
#print axioms SecondSuccession.Readings.every_splits
#print axioms SecondSuccession.Readings.admitting_splits
#print axioms SecondSuccession.Readings.base_matters
#print axioms SecondSuccession.Readings.every_not_given_base
#print axioms SecondSuccession.Readings.admitting_not_given_base
#print axioms SecondSuccession.Readings.changing_not_of_regime
