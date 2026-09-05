/-
Axiom reports for every exported theorem of `research/limit_and_observer`.

The build log is compared byte for byte against `receipts/lean_axioms.txt` by
`verify_lean.py`.  Every report must lie within `{propext, Quot.sound}`.

This receipt is MANUAL: no CI gate runs `verify_lean.py`, here or in any other
research tree.  CLAUDE.md records that as the last live residual, and this
tree sits squarely inside it.
-/
import LimitObserver

#print axioms LimitObserver.sealed_is_blind_where_covered
#print axioms LimitObserver.sealed_reads_admission_where_uncovered
#print axioms LimitObserver.rival_separates_where_sealed_identifies
#print axioms LimitObserver.rival_agrees_where_uncovered
#print axioms LimitObserver.strict_ge
#print axioms LimitObserver.chain_bounded
#print axioms LimitObserver.refinement_demand_unsatisfiable
#print axioms LimitObserver.refinement_obstruction_survives_growth
#print axioms LimitObserver.diffCount_self
#print axioms LimitObserver.fresh_data_are_never_separated
#print axioms LimitObserver.growth_defeats_every_reader
#print axioms LimitObserver.novel_forces_constant
#print axioms LimitObserver.no_novel_verdict_on_a_mixed_sequence
#print axioms LimitObserver.stage_local_verdict_is_not_novel
#print axioms LimitObserver.sealed_behaviour
#print axioms LimitObserver.admission_only_behaviour
#print axioms LimitObserver.behaviour_determines_separation
