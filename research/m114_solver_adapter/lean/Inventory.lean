import SolverAdapter

open SolverAdapter

#print axioms primal_soundness
#print axioms int_nat_mul_le_mul
#print axioms dual_combination_le
#print axioms farkas_dual_soundness
#print axioms fuel_monotonicity
#print axioms refusal_preserves_state

def main : IO Unit := do
  IO.println "Target M114 Solver Adapter Lean Census:"
  IO.println "  - primal_soundness"
  IO.println "  - int_nat_mul_le_mul"
  IO.println "  - dual_combination_le"
  IO.println "  - farkas_dual_soundness"
  IO.println "  - fuel_monotonicity"
  IO.println "  - refusal_preserves_state"
