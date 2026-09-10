import EqualityOrder

open M104EqualityOrder

#print axioms presentation_implies_defeq
#print axioms defeq_implies_propeq_eval
#print axioms state_eq_implies_obseq
#print axioms defeq_not_implies_presentation
#print axioms obseq_not_implies_state_eq
#print axioms reach_refl
#print axioms reach_trans
#print axioms refines_refl
#print axioms refines_trans
#print axioms cost_refl
#print axioms cost_trans
#print axioms reachability_not_cost

def main : IO Unit := do
  IO.println "M104/M107 Equality Layers & Order Family Lean 4 Census:"
  IO.println "  - presentation_implies_defeq"
  IO.println "  - defeq_implies_propeq_eval"
  IO.println "  - state_eq_implies_obseq"
  IO.println "  - defeq_not_implies_presentation"
  IO.println "  - obseq_not_implies_state_eq"
  IO.println "  - reach_refl"
  IO.println "  - reach_trans"
  IO.println "  - refines_refl"
  IO.println "  - refines_trans"
  IO.println "  - cost_refl"
  IO.println "  - cost_trans"
  IO.println "  - reachability_not_cost"
