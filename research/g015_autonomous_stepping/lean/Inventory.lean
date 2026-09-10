import AutonomousStepping

open G015AutonomousStepping

#print axioms inert_history_quiescent
#print axioms refusal_preserves_state
#print axioms resource_conservation
#print axioms finite_saturation_steps
#print axioms finite_saturation_resources

def main : IO Unit := do
  IO.println "G015 Autonomous Stepping Lean 4 Census:"
  IO.println "  - inert_history_quiescent"
  IO.println "  - refusal_preserves_state"
  IO.println "  - resource_conservation"
  IO.println "  - finite_saturation_steps"
  IO.println "  - finite_saturation_resources"
