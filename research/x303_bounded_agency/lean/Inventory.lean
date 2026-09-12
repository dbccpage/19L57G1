import BoundedAgency

open X303BoundedAgency

-- Core Mandatory Theorems
#print axioms viability_preservation
#print axioms causal_action_selection_soundness
#print axioms state_preservation_on_refusal
#print axioms fuel_monotonicity

-- Companion Theorems and Lemmas
#print axioms licensed_action_preserves_viability
#print axioms step_causal_action_selection_soundness
#print axioms state_preservation_on_refusal_state
#print axioms fuel_monotonicity_action
#print axioms fuel_monotonicity_refusal
#print axioms fuel_monotonicity_le
#print axioms zero_unilateral_authority
#print axioms fuel_exhaustion_refusal
#print axioms memory_bounded
#print axioms pareto_dominance_irreflexive
#print axioms pareto_dominance_transitive
#print axioms pareto_dominance_asymmetric

def main : IO Unit := do
  IO.println "Target X303 Bounded Operational Agency Lean 4 Census:"
  IO.println "  - viability_preservation"
  IO.println "  - causal_action_selection_soundness"
  IO.println "  - state_preservation_on_refusal"
  IO.println "  - fuel_monotonicity"
  IO.println "  - licensed_action_preserves_viability"
  IO.println "  - step_causal_action_selection_soundness"
  IO.println "  - state_preservation_on_refusal_state"
  IO.println "  - fuel_monotonicity_action"
  IO.println "  - fuel_monotonicity_refusal"
  IO.println "  - fuel_monotonicity_le"
  IO.println "  - zero_unilateral_authority"
  IO.println "  - fuel_exhaustion_refusal"
  IO.println "  - memory_bounded"
  IO.println "  - pareto_dominance_irreflexive"
  IO.println "  - pareto_dominance_transitive"
  IO.println "  - pareto_dominance_asymmetric"
