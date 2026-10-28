import Derivation
import Derivation.Composing
#print axioms Derivation.R2L_wf
#print axioms Derivation.R2F_wf
#print axioms Derivation.mem_insertNew
#print axioms Derivation.insertNew_of_mem
#check @Derivation.quotient_barrier
#check @Derivation.quot_barrier
#check @Derivation.no_supply_round_bound
#print axioms Composing.composition_may_fail
-- vacuity probe: is collapseRel a Setoid? no. Check that Quot (collapseRel R2L) has 1 class on {0,1} only via barrier
example : Derivation.R2L ≠ Derivation.R2F := by decide
