import TwinRelation
import QuotientTopology
import ValuationPricing

/-!
# Inventory: Environment Census and Axiom Dependency Verification

Verifies that all exported theorems across `TwinRelation`, `QuotientTopology`,
and `ValuationPricing` depend strictly on `{propext, Quot.sound}` only,
with zero mathlib dependencies and zero unapproved axioms.

AuthorityEffect: None.
-/

-- TwinRelation theorems
#print axioms TwinRelation.twins_differ_at_scale
#print axioms TwinRelation.twins_are_distinct
#print axioms TwinRelation.scale_one_twins_differ
#print axioms TwinRelation.twins_are_related
#print axioms TwinRelation.twin_pair_distinct_and_related

-- QuotientTopology theorems
#print axioms QuotientTopology.twin_collapse_in_quotient
#print axioms QuotientTopology.separation_quotient_contrast
#print axioms QuotientTopology.adjacent_cylinders_glue
#print axioms QuotientTopology.quotient_destroys_clopen_separation
#print axioms QuotientTopology.locally_constant_chain
#print axioms QuotientTopology.twin_collapse_predicate_transport
#print axioms QuotientTopology.quotient_points_distinct_iff
#print axioms QuotientTopology.distinct_quotient_points_representatives_non_equivalent
#print axioms QuotientTopology.scale_one_valuation_difference
#print axioms QuotientTopology.dyadic_valuation_difference_at_depth
#print axioms QuotientTopology.dyadic_valuation_integer_difference

-- ValuationPricing theorems
#print axioms ValuationPricing.twinCount_base2
#print axioms ValuationPricing.twinCount_strictly_positive
#print axioms ValuationPricing.mu1Scale_base2
#print axioms ValuationPricing.cumulative_mu1_formula
#print axioms ValuationPricing.mu2Scale_base2
#print axioms ValuationPricing.cumulative_mu2_formula
#print axioms ValuationPricing.mu1_strictly_divergent
#print axioms ValuationPricing.cumulative_mu1_unbounded
#print axioms ValuationPricing.mu2_strictly_divergent
#print axioms ValuationPricing.cumulative_mu2_unbounded
#print axioms ValuationPricing.markov_weighted_scale_identity
#print axioms ValuationPricing.markov_obstruction_diverges
#print axioms ValuationPricing.markov_obstruction_unbounded
#print axioms ValuationPricing.finite_stage_price_finite
#print axioms ValuationPricing.continuum_price_infinite
