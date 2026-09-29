import SecondRun

/-!
# The axiom report

One `#print axioms` line for every theorem of the package, in module
order.  `verify_lean.py` builds this module fresh and compares the
reports with a compiler census of the package in both directions.

AuthorityEffect: None.
-/

-- Kernel.lean
#print axioms SecondRun.Sealed.insertNew_nil
#print axioms SecondRun.Sealed.insertNew_of_not_mem
#print axioms SecondRun.Sealed.insertNew_of_mem
#print axioms SecondRun.Sealed.mem_insertNew
#print axioms SecondRun.Sealed.separable_not_collapsed
#print axioms SecondRun.Sealed.R2L_wf
#print axioms SecondRun.Sealed.R2F_wf
#print axioms SecondRun.Sealed.supply_no_op
#print axioms SecondRun.Sealed.genesis_underivable
#print axioms SecondRun.Sealed.underivable_of_empty
#print axioms SecondRun.Sealed.collapsed_of_no_insts
#print axioms SecondRun.Sealed.R2L_collapsed
#print axioms SecondRun.Sealed.R2F_collapsed
#print axioms SecondRun.Sealed.historyL_replays
#print axioms SecondRun.Sealed.historyF_replays
#print axioms SecondRun.Sealed.admission_without_expressive_increase
#print axioms SecondRun.Sealed.replayE_append

-- Run.lean
#print axioms SecondRun.Run.insertNew_length_le
#print axioms SecondRun.Run.insertNew_eq_or_succ
#print axioms SecondRun.Run.stepE_elems_le
#print axioms SecondRun.Run.stepE_elems_lt_of_ne
#print axioms SecondRun.Run.switch_keeps_regime
#print axioms SecondRun.Run.switch_switch
#print axioms SecondRun.Run.estep_elems_le
#print axioms SecondRun.Run.estep_elems_lt_of_ne
#print axioms SecondRun.Run.ereplay_elems_le
#print axioms SecondRun.Run.ereplay_regime_eq_of_elems_eq
#print axioms SecondRun.Run.ereplay_elems_lt_of_ne
#print axioms SecondRun.Run.no_return
#print axioms SecondRun.Run.cycle_regime_const
#print axioms SecondRun.Run.collapsed_through
#print axioms SecondRun.Run.not_separable_through
