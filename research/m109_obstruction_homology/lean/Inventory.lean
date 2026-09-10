import ObstructionHomology

open M109ObstructionHomology

#print axioms abstract_chain_nilpotency
#print axioms abstract_coboundary_nilpotency
#print axioms telescope_identity
#print axioms move_boundary_nilpotent
#print axioms move_coboundary_nilpotent
#print axioms stokes_coboundary_square
#print axioms boundary_is_cycle
#print axioms coboundary_is_cocycle
#print axioms obstruction_criterion
#print axioms native_rule_span_circulation
#print axioms native_rule_span_not_exact
#print axioms native_boundary_is_cycle

def main : IO Unit := do
  IO.println "Target M109 Obstruction Homology Lean 4 Census:"
  IO.println "  - abstract_chain_nilpotency"
  IO.println "  - abstract_coboundary_nilpotency"
  IO.println "  - telescope_identity"
  IO.println "  - move_boundary_nilpotent"
  IO.println "  - move_coboundary_nilpotent"
  IO.println "  - stokes_coboundary_square"
  IO.println "  - boundary_is_cycle"
  IO.println "  - coboundary_is_cocycle"
  IO.println "  - obstruction_criterion"
  IO.println "  - native_rule_span_circulation"
  IO.println "  - native_rule_span_not_exact"
  IO.println "  - native_boundary_is_cycle"
