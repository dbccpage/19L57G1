import BoundarySeed.Basic
import BoundarySeed.Challenge1
import BoundarySeed.Challenge2
import BoundarySeed.Challenge3

/-!
# The boundary derivation: root

Challenges 0 to 3.  Every theorem declared under `lean/BoundarySeed/` has a
`#print axioms` line here, which `verify_lean.py` requires by name, and it
compares the build log with the committed axiom log.
-/

#print axioms BoundarySeed.supply_no_op
#print axioms BoundarySeed.step_changes_only_by_place
#print axioms BoundarySeed.genesis_initial_datum
#print axioms BoundarySeed.genesis_placement_nil
#print axioms BoundarySeed.no_observation_at_genesis
#print axioms BoundarySeed.O_name_judgment_at_genesis
#print axioms BoundarySeed.U_no_name_judgment_at_genesis
#print axioms BoundarySeed.contents_genesis
#print axioms BoundarySeed.sides_collapsed_at_genesis_U
#print axioms BoundarySeed.sides_distinct_at_genesis_O
#print axioms BoundarySeed.side_names_distinct
#print axioms BoundarySeed.map_not_not
#print axioms BoundarySeed.reflect_reflect
#print axioms BoundarySeed.reflect_genesis
#print axioms BoundarySeed.reflection_permitted_U
#print axioms BoundarySeed.reflection_not_permitted_O
#print axioms BoundarySeed.reflect_moves_a_mark
#print axioms BoundarySeed.replay_deterministic
#print axioms BoundarySeed.replay_supply_inert
#print axioms BoundarySeed.no_event_follows
#print axioms BoundarySeed.admitted_eq
#print axioms BoundarySeed.supply_preserves_holds
#print axioms BoundarySeed.step_reading
#print axioms BoundarySeed.step_initialDatum
#print axioms BoundarySeed.replay_reading
#print axioms BoundarySeed.replay_initialDatum
#print axioms BoundarySeed.step_preserves_sideNamed
#print axioms BoundarySeed.replay_preserves_sideNamed
#print axioms BoundarySeed.getD_append_left
#print axioms BoundarySeed.step_preserves_onSide
#print axioms BoundarySeed.replay_preserves_onSide
#print axioms BoundarySeed.getD_append_singleton
#print axioms BoundarySeed.place_new_judgment
#print axioms BoundarySeed.place_other_side_false
#print axioms BoundarySeed.admitted_onSide_true_iff
#print axioms BoundarySeed.admitted_U_no_sideNamed
#print axioms BoundarySeed.admitted_O_sideNamed
#print axioms BoundarySeed.admitted_contents_placed
#print axioms BoundarySeed.admitted_contents_other
#print axioms BoundarySeed.admitted_sides_differ
#print axioms BoundarySeed.reflect_step_supply
#print axioms BoundarySeed.reflect_step_place
#print axioms BoundarySeed.exchangeSide_exchangeSide
#print axioms BoundarySeed.map_exchangeSide_map_exchangeSide
#print axioms BoundarySeed.reflect_step
#print axioms BoundarySeed.reflect_replay
#print axioms BoundarySeed.reflect_admitted
#print axioms BoundarySeed.continuation_reflects
#print axioms BoundarySeed.other_continuation_is_a_reflection
#print axioms BoundarySeed.admitted_candidates_unequal
#print axioms BoundarySeed.candidates_related_U
#print axioms BoundarySeed.candidates_not_related_O
#print axioms BoundarySeed.invariant_judgment_does_not_separate
#print axioms BoundarySeed.bounded_invariant_judgment_does_not_separate
#print axioms BoundarySeed.onSide_separates_candidates
#print axioms BoundarySeed.no_event_follows_admitted
#print axioms BoundarySeed.retained_eq
#print axioms BoundarySeed.retained_placement_length
#print axioms BoundarySeed.retained_without_supplies
#print axioms BoundarySeed.retainedOtherOrder_eq
#print axioms BoundarySeed.retained_onSide_zero
#print axioms BoundarySeed.retained_onSide_one
#print axioms BoundarySeed.retained_onSide_beyond
#print axioms BoundarySeed.retained_onSide_true_iff
#print axioms BoundarySeed.retained_marks_differ_in_side
#print axioms BoundarySeed.retained_sideNamed
#print axioms BoundarySeed.retained_contents_false
#print axioms BoundarySeed.retained_contents_true
#print axioms BoundarySeed.retained_sides_differ
#print axioms BoundarySeed.exchangeFirstTwo_involutive
#print axioms BoundarySeed.swapFirstTwo_involutive
#print axioms BoundarySeed.exchangeMarks_involutive
#print axioms BoundarySeed.exchangeMarks_reflect_retained
#print axioms BoundarySeed.reflect_retained_ne
#print axioms BoundarySeed.exchangeMarks_retained_ne
#print axioms BoundarySeed.retainedOtherOrder_is_exchange
#print axioms BoundarySeed.retainedOtherOrder_ne_retained
#print axioms BoundarySeed.retained_composite_permitted_U
#print axioms BoundarySeed.retained_exchange_transports
#print axioms BoundarySeed.retained_marks_separated_by_a_side
#print axioms BoundarySeed.retained_judgments_survive
#print axioms BoundarySeed.retained_reading
#print axioms BoundarySeed.retained_initialDatum
#print axioms BoundarySeed.no_event_follows_retained
#print axioms BoundarySeed.composite_retained
#print axioms BoundarySeed.exchangeFirstTwo_zero
#print axioms BoundarySeed.exchangeFirstTwo_one
#print axioms BoundarySeed.retained_U_requirement_fails
#print axioms BoundarySeed.no_invariant_mark_property_separates_retained
#print axioms BoundarySeed.mark_form_is_not_invariant_under_the_composite
#print axioms BoundarySeed.countOn_nil
#print axioms BoundarySeed.countOn_cons
#print axioms BoundarySeed.countOn_map_not
#print axioms BoundarySeed.countOn_perm
#print axioms BoundarySeed.reflect_not_undone_by_renaming
#print axioms BoundarySeed.retainedPlus_eq
#print axioms BoundarySeed.retainedPlus_reading
#print axioms BoundarySeed.retainedPlus_initialDatum
#print axioms BoundarySeed.retainedPlus_placement
#print axioms BoundarySeed.retained_placement
#print axioms BoundarySeed.retainedPlus_counts_differ
#print axioms BoundarySeed.retainedPlus_reflection_is_not_an_automorphism
#print axioms BoundarySeed.retained_counts_equal
#print axioms BoundarySeed.retainedPlus_judgments_survive
#print axioms BoundarySeed.no_event_follows_retainedPlus
