import PathDependentCost.Cochain

/-!
# Axiom reports

One `#print axioms` per theorem of `Cochain.lean`.  `../verify_lean.py`
requires every theorem DECLARED in that source to appear here, not merely
every report to be listed: removing a line here removes its report too, so
a self-diff cannot see a silent drop.

`AuthorityEffect: None.`
-/

#print axioms PathDependentCost.actList_append
#print axioms PathDependentCost.sumEdges_nil
#print axioms PathDependentCost.sumEdges_additive
#print axioms PathDependentCost.additive_empty_zero
#print axioms PathDependentCost.additive_eq_sumEdges
#print axioms PathDependentCost.exact_agrees_on_two_routes
#print axioms PathDependentCost.not_exact_of_routes_differ
#print axioms PathDependentCost.le_actList
#print axioms PathDependentCost.closed_directed_walk_is_stationary
#print axioms PathDependentCost.Commit.span_reads_the_state
#print axioms PathDependentCost.Commit.routes_agree
#print axioms PathDependentCost.Commit.commit_early
#print axioms PathDependentCost.Commit.commit_late
#print axioms PathDependentCost.Commit.span_prices_the_order
#print axioms PathDependentCost.Commit.span_is_additive
#print axioms PathDependentCost.Commit.span_is_not_exact
#print axioms PathDependentCost.Commit.count_cannot_see_the_order
