/-
AxiomReport: one report per exported theorem.  The build log's
reports are checked against the whitelist {propext, Quot.sound} by
`verify_lean.py`.
-/

import ConventionPrice

#print axioms ConventionPrice.holo_nil
#print axioms ConventionPrice.holo_cons
#print axioms ConventionPrice.xor_self'
#print axioms ConventionPrice.xor_false'
#print axioms ConventionPrice.false_xor'
#print axioms ConventionPrice.xor_mix
#print axioms ConventionPrice.xor_cancel_mid
#print axioms ConventionPrice.relabelled_eq
#print axioms ConventionPrice.slot_toggles_parity
#print axioms ConventionPrice.cycle_parity_sum
#print axioms ConventionPrice.chain_telescope
#print axioms ConventionPrice.pointwise_parity_blind
#print axioms ConventionPrice.chainSteps_consumed
#print axioms ConventionPrice.chainSteps_end
#print axioms ConventionPrice.pointwise_cycle_invariant
#print axioms ConventionPrice.cure_kills
#print axioms ConventionPrice.holo_all_false
#print axioms ConventionPrice.slot_group_sections
