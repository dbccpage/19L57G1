import InternalAlgebra

open InternalAlgebra

#print axioms eval_subst
#print axioms freeMonoidLift_eta
#print axioms freeMonoidLift_append
#print axioms freeMonoid_universal_arrow_unique
#print axioms evalSum_eta
#print axioms evalSum_append
#print axioms lift2_mk
#print axioms quot_mul_assoc
#print axioms quot_one_mul
#print axioms quot_mul_one
#print axioms quot_representative_independence
#print axioms factorMap_commutes
#print axioms factorMap_map_mul
#print axioms factorHom_unique

def main : IO Unit := do
  IO.println "Target M108 General Internal Universal Algebra Lean 4 Census:"
  IO.println "  - eval_subst"
  IO.println "  - freeMonoidLift_eta"
  IO.println "  - freeMonoidLift_append"
  IO.println "  - freeMonoid_universal_arrow_unique"
  IO.println "  - evalSum_eta"
  IO.println "  - evalSum_append"
  IO.println "  - lift2_mk"
  IO.println "  - quot_mul_assoc"
  IO.println "  - quot_one_mul"
  IO.println "  - quot_mul_one"
  IO.println "  - quot_representative_independence"
  IO.println "  - factorMap_commutes"
  IO.println "  - factorMap_map_mul"
  IO.println "  - factorHom_unique"
