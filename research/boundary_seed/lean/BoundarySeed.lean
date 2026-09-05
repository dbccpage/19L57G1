import BoundarySeed.Basic
import BoundarySeed.Challenge1

/-!
# The boundary derivation: root

Challenges 0 and 1.  Every theorem below has a `#print axioms` line, and
`verify_lean.py` compares the build log with the committed axiom log.
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
