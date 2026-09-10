import RelationalSpacetime

open P201RelationalSpacetime

#print axioms dimensionless_ratio_invariant
#print axioms cross_dimension_disjoint
#print axioms future_equiv_refl
#print axioms future_equiv_symm
#print axioms future_equiv_trans
#print axioms future_equiv_step_congruence
#print axioms relational_clock_ratio

def main : IO Unit := do
  IO.println "P201/P202 Relational Dimensions & Clocks Lean 4 Census:"
  IO.println "  - dimensionless_ratio_invariant"
  IO.println "  - cross_dimension_disjoint"
  IO.println "  - future_equiv_refl"
  IO.println "  - future_equiv_symm"
  IO.println "  - future_equiv_trans"
  IO.println "  - future_equiv_step_congruence"
  IO.println "  - relational_clock_ratio"
