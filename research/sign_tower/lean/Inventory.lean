import Carrier
import History
import Movegraph
import ScaleDynamics
import Obstruction

/-!
# Inventory: Axiom Audits for Prompt B Formal Proofs

Imports all Prompt B modules and prints the axioms of all exported theorems.
Verification Target: Axioms strictly within {propext, Quot.sound}. Zero sorry.

AuthorityEffect: None.
-/

namespace Inventory

-- Carrier theorems
#print axioms Carrier.canonical_orbit_invariance
#print axioms Carrier.observable_orbit_invariance
#print axioms Carrier.carrier_parity_blind
#print axioms Carrier.rigid_witness_inverts
#print axioms Carrier.rigid_witness_sign_inverts
#print axioms Carrier.symm_witness_preserved
#print axioms Carrier.symm_witness_sign_product

-- History theorems
#print axioms History.fresh_data_commute
#print axioms History.data_inst_causally_blocked
#print axioms History.data_inst_blocked_classification
#print axioms History.distinct_form_order_altering
#print axioms History.data_reorder_canonical_invariant
#print axioms History.data_transposition_parity_blind
#print axioms History.form_fiber_separation
#print axioms History.form_fiber_parity_balanced

-- Movegraph theorems
#print axioms Movegraph.constructor_monotonicity
#print axioms Movegraph.movegraph_acyclic
#print axioms Movegraph.kill_condition_2_fires
#print axioms Movegraph.mu1_nonnegative
#print axioms Movegraph.capability_not_isomorphic_to_signed_defect

-- ScaleDynamics theorems
#print axioms ScaleDynamics.rank_defect_strictly_positive
#print axioms ScaleDynamics.bonding_not_endomorphism
#print axioms ScaleDynamics.kill_condition_3_fires
#print axioms ScaleDynamics.twins_differ_at_scale_one
#print axioms ScaleDynamics.twins_are_distinct_threads
#print axioms ScaleDynamics.regime_has_no_alphabet_map
#print axioms ScaleDynamics.kolmogorov_cylinder_consistency
#print axioms ScaleDynamics.branching_ratio_unity
#print axioms ScaleDynamics.positivity_bridge_structural_gap

-- Obstruction theorems
#print axioms Obstruction.pullback_coboundary_vanishes
#print axioms Obstruction.presentation_quotient_non_descent
#print axioms Obstruction.mod2_involution_cocycle
#print axioms Obstruction.w1_nontrivial
#print axioms Obstruction.rational_involution_defect_ne_zero
#print axioms Obstruction.not_rational_cocycle
#print axioms Obstruction.capability_cost_is_exact_coboundary
#print axioms Obstruction.capability_circulation_vanishes

end Inventory

#print axioms Movegraph.nat_additive_invertibility
