import BoundarySeed.Basic

/-!
# The boundary derivation: root

Challenge 0 only.  Every theorem below has a `#print axioms` line, and
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
