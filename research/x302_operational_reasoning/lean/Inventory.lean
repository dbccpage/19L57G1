import OperationalReasoning

open X302OperationalReasoning

#print axioms axiom_leaf_support_empty
#print axioms hyp_leaf_support_singleton
#print axioms mp_support_mem_left
#print axioms mp_support_mem_right
#print axioms conj_intro_support_mem
#print axioms conj_elim_support_eq
#print axioms support_monotonicity
#print axioms direct_contradiction_conflict_set
#print axioms valuation_contradiction_conflict_set
#print axioms foundational_contradiction_no_hypothesis
#print axioms empty_support_disjoint
#print axioms axiom_immutability
#print axioms hitting_set_invalidates_conflict
#print axioms retraction_deactivates_conflict
#print axioms vacuous_revision_empty_hitting_set
#print axioms vacuous_revision_preserves_support
#print axioms derivation_soundness
#print axioms retraction_restores_consistency

def main : IO Unit := do
  IO.println "Target X302 Operational Reasoning Lean 4 Census:"
  IO.println "  - axiom_leaf_support_empty"
  IO.println "  - hyp_leaf_support_singleton"
  IO.println "  - mp_support_mem_left"
  IO.println "  - mp_support_mem_right"
  IO.println "  - conj_intro_support_mem"
  IO.println "  - conj_elim_support_eq"
  IO.println "  - support_monotonicity"
  IO.println "  - direct_contradiction_conflict_set"
  IO.println "  - valuation_contradiction_conflict_set"
  IO.println "  - foundational_contradiction_no_hypothesis"
  IO.println "  - empty_support_disjoint"
  IO.println "  - axiom_immutability"
  IO.println "  - hitting_set_invalidates_conflict"
  IO.println "  - retraction_deactivates_conflict"
  IO.println "  - vacuous_revision_empty_hitting_set"
  IO.println "  - vacuous_revision_preserves_support"
  IO.println "  - derivation_soundness"
  IO.println "  - retraction_restores_consistency"
