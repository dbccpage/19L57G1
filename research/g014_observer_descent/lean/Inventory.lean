import ObserverDescent

open G014ObserverDescent

#print axioms CarrierState.ext'
#print axioms gluing_preserves_observations
#print axioms gluing_unique
#print axioms failed_gluing_obstruction
#print axioms swap13_involutive
#print axioms natural_transport_commutation
#print axioms symmetric_duplicate_agreement
#print axioms duplicate_disagreement_witnesses_asymmetry

def main : IO Unit := do
  IO.println "G014 Multi-Observer Descent Lean 4 Census:"
  IO.println "  - CarrierState.ext'"
  IO.println "  - gluing_preserves_observations"
  IO.println "  - gluing_unique"
  IO.println "  - failed_gluing_obstruction"
  IO.println "  - swap13_involutive"
  IO.println "  - natural_transport_commutation"
  IO.println "  - symmetric_duplicate_agreement"
  IO.println "  - duplicate_disagreement_witnesses_asymmetry"
