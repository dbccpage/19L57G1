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

Note, 2026-09-18.  The sentence "prints the axioms of all exported
theorems" was false through 827bf983, where this file printed 38 of the 56
theorems written in the five modules; the other 18 had no line here.  Those
18 lines are now added, in the groups marked below, so the sentence holds
for every theorem written in the source.  It does not reach the theorems
Lean generates beside a declaration (constructor injectivity and size
lemmas, `ofNat_ctorIdx`, proof-valued structure fields, and compiler-internal
auxiliary proofs); those have no line here.  `../verify_lean.py --check`
lists every theorem of the five modules from the compiled environment,
generated ones included, holds each to {propext, Quot.sound}, and requires
the lines of this file to name exactly the theorems written in the source.
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
-- added 2026-09-18: written in the source, no line here before
#print axioms Carrier.Sign.mul_pos
#print axioms Carrier.Sign.pos_mul
#print axioms Carrier.Sign.neg_neg
#print axioms Carrier.Sign.neg_pos
#print axioms Carrier.Sign.pos_neg
#print axioms Carrier.Sign.mul_comm
#print axioms Carrier.Sign.mul_assoc
#print axioms Carrier.Sign.neg_ne_pos
#print axioms Carrier.sgn2_comp
#print axioms Carrier.witness_projected_out

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
-- added 2026-09-18: written in the source, no line here before
#print axioms Movegraph.supply_is_identity
#print axioms Movegraph.trajectory_strictly_increases
#print axioms Movegraph.defect_has_nontrivial_inverse

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
-- added 2026-09-18: written in the source, no line here before
#print axioms ScaleDynamics.twins_differ_at_zero

-- Obstruction theorems
#print axioms Obstruction.pullback_coboundary_vanishes
#print axioms Obstruction.presentation_quotient_non_descent
#print axioms Obstruction.mod2_involution_cocycle
#print axioms Obstruction.w1_nontrivial
#print axioms Obstruction.rational_involution_defect_ne_zero
#print axioms Obstruction.not_rational_cocycle
#print axioms Obstruction.capability_cost_is_exact_coboundary
#print axioms Obstruction.capability_circulation_vanishes
-- added 2026-09-18: written in the source, no line here before
#print axioms Obstruction.Z2.add_zero
#print axioms Obstruction.Z2.zero_add
#print axioms Obstruction.Z2.one_add_one
#print axioms Obstruction.Z2.one_ne_zero

end Inventory

#print axioms Movegraph.nat_additive_invertibility
