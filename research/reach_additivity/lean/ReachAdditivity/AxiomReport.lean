import ReachAdditivity.Additive

/-!
# Axiom reports

One `#print axioms` per theorem of `Additive.lean`.  The audit in
`../verify_lean.py` requires every theorem DECLARED in that source to appear
here, not merely every report to be listed: removing a line here removes its
report too, so a self-diff cannot see a silent drop.

`AuthorityEffect: None.`
-/

#print axioms ReachAdditivity.actList_nil
#print axioms ReachAdditivity.actList_cons
#print axioms ReachAdditivity.actList_append
#print axioms ReachAdditivity.diff_additive
#print axioms ReachAdditivity.pathTotal_eq
#print axioms ReachAdditivity.path_independent
#print axioms ReachAdditivity.circulation_zero
#print axioms ReachAdditivity.count_additive
#print axioms ReachAdditivity.Loop.keep_is_a_closed_walk
#print axioms ReachAdditivity.Loop.diff_zero_on_the_closed_walk
#print axioms ReachAdditivity.Loop.count_is_not_a_difference
#print axioms ReachAdditivity.Unsigned.natDiff_additive_of_monotone
#print axioms ReachAdditivity.Unsigned.natDiff_not_additive
#print axioms ReachAdditivity.Unsigned.signed_is_additive_on_the_same_model
