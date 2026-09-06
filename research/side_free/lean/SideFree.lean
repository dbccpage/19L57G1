import SideFree.Basic
import SideFree.Forget

/-!
# The side-free control: exported theorems and their axiom reports

Every theorem declared under lean/SideFree/ carries a #print axioms
line here, and verify_lean.py fails if one is missing.  Every report must
lie within {propext, Quot.sound}.

This package is a MANUAL RECEIPT: no CI job builds it.  That is a live
residual of this tree, recorded and not closed.
-/

#print axioms SideFree.admitMark_no_op
#print axioms SideFree.admitOccurrence_appends
#print axioms SideFree.admitOccurrence_size
#print axioms SideFree.base_exchange_is_an_automorphism
#print axioms SideFree.blank_congr
#print axioms SideFree.blank_length
#print axioms SideFree.exchange_is_not_the_identity
#print axioms SideFree.exchange_moves_zero_to_one
#print axioms SideFree.extra_mark_exchange_is_an_automorphism
#print axioms SideFree.forget_reflect
#print axioms SideFree.forget_rename
#print axioms SideFree.forgetful_lemma_forgetting_labels
#print axioms SideFree.forgetful_lemma_keeping_labels
#print axioms SideFree.free_separation_implies_sided_separation
#print axioms SideFree.free_separation_implies_sided_separation_forgetting_labels
#print axioms SideFree.genesis_size
#print axioms SideFree.keep_labels_exchange_is_an_automorphism
#print axioms SideFree.no_event_follows
#print axioms SideFree.no_judgment_at_genesis
#print axioms SideFree.reflect_length
#print axioms SideFree.reorder_length_congr
#print axioms SideFree.reorder_map
#print axioms SideFree.replay_append
#print axioms SideFree.replay_deterministic
#print axioms SideFree.replay_supply_inert
#print axioms SideFree.retainedPlus_replays_from_genesis
#print axioms SideFree.retained_judgments
#print axioms SideFree.retained_replays_from_genesis
#print axioms SideFree.retained_size
#print axioms SideFree.shared_policy_retains_one_mark
#print axioms SideFree.step_changes_only_by_admission
#print axioms SideFree.supply_is_not_an_admission
#print axioms SideFree.supply_no_op
#print axioms SideFree.withdrawal_does_not_move_zero_to_one
#print axioms SideFree.withdrawal_moves_no_index
