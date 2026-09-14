import ConservativeGrammar
import MovegraphTopology
import OperationalPricing

/-!
# Axiom Inventory Census for SeventhConstructor

Audit verifying all exported theorems depend only on {propext, Quot.sound}.
AuthorityEffect: None.
-/

namespace SeventhConstructor.Audit

-- ConservativeGrammar theorems
#print axioms SeventhConstructor.swap_preserves_cardinal_potential
#print axioms SeventhConstructor.native_non_supply_increases_potential
#print axioms SeventhConstructor.supply_is_identity
#print axioms SeventhConstructor.admitting_regime_has_swap
#print axioms SeventhConstructor.transposition_involutive
#print axioms SeventhConstructor.swap_data_cardinality
#print axioms SeventhConstructor.swap_instances_cardinality
#print axioms SeventhConstructor.swap_regime_involutive
#print axioms SeventhConstructor.swap_preserves_internal_scope

-- MovegraphTopology theorems
#print axioms SeventhConstructor.native_movegraph_acyclic
#print axioms SeventhConstructor.r1_instances_eval
#print axioms SeventhConstructor.r0_ne_r1
#print axioms SeventhConstructor.swap_returns_to_r0
#print axioms SeventhConstructor.gamma2_boundary_r0
#print axioms SeventhConstructor.gamma2_boundary_r1
#print axioms SeventhConstructor.gamma2_is_cycle
#print axioms SeventhConstructor.z1_extended_nontrivial
#print axioms SeventhConstructor.swap_step_isomorphic
#print axioms SeventhConstructor.quotient_cycle_collapse
#print axioms SeventhConstructor.presentation_quotient_obstruction

-- OperationalPricing theorems
#print axioms SeventhConstructor.mu1_swap_zero
#print axioms SeventhConstructor.mu1_equals_potential_difference
#print axioms SeventhConstructor.cumulative_mu1_telescopes
#print axioms SeventhConstructor.mu1_closed_cycle_circulation_vanishes
#print axioms SeventhConstructor.mu2_swap_cost_positive
#print axioms SeventhConstructor.cycle2_mu1_circulation_zero
#print axioms SeventhConstructor.cycle2_mu2_circulation_strictly_positive
#print axioms SeventhConstructor.circulation_cost_contrast

end SeventhConstructor.Audit
