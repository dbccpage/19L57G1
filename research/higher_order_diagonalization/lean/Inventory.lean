import ObserverHierarchy
import SeparationCapacity
import Diagonalization

/-!
# Axiom Inventory Census for HigherOrderDiagonalization

Audit verifying all exported theorems depend strictly on {propext, Quot.sound}.
Zero mathlib, zero custom axioms, zero unproven escapes.
Narrowed 2026-09-18: the completeness claim above is WITHDRAWN.
Rechecked 2026-09-19: this file reports exactly the 35 theorem
constants named by its report lines below. The verifier requires that
exact named population. A fresh compiled-module census found
50 non-internal theorem constants in the three local modules, including
generated declarations and proof-valued instances; 15 are outside this
report list. These are compiled constants, not a count of explicit
theorem statements in source. The previous draft counts are superseded
by this population criterion.
A reported theorem includes the axioms of its dependencies. An
unreported declaration that no reported theorem uses remains outside
this audit. This note does not turn the named list into a full census.

AuthorityEffect: None.
-/

namespace HigherOrderDiagonalization.Audit

-- ObserverHierarchy theorems
#print axioms HigherOrderDiagonalization.flip_token_involutive
#print axioms HigherOrderDiagonalization.flip_seq_involutive
#print axioms HigherOrderDiagonalization.flip_seq_length
#print axioms HigherOrderDiagonalization.canon_seq_length
#print axioms HigherOrderDiagonalization.iso_refl
#print axioms HigherOrderDiagonalization.iso_symm
#print axioms HigherOrderDiagonalization.iso_trans
#print axioms HigherOrderDiagonalization.iso_equivalence
#print axioms HigherOrderDiagonalization.prefixK_canon_respects_iso
#print axioms HigherOrderDiagonalization.eval_lt_capacity
#print axioms HigherOrderDiagonalization.eval_respects_iso
#print axioms HigherOrderDiagonalization.observer_equiv_equivalence
#print axioms HigherOrderDiagonalization.observer_equiv_coarsening
#print axioms HigherOrderDiagonalization.compose_higher_order_respects_iso

-- SeparationCapacity theorems
#print axioms HigherOrderDiagonalization.natToBits_length
#print axioms HigherOrderDiagonalization.bitsToNat_natToBits
#print axioms HigherOrderDiagonalization.natToBits_injective
#print axioms HigherOrderDiagonalization.canonSeq_zero_head
#print axioms HigherOrderDiagonalization.testRegime_canon
#print axioms HigherOrderDiagonalization.testRegime_pairwise_non_isomorphic
#print axioms HigherOrderDiagonalization.test_family_size_gt_capacity
#print axioms HigherOrderDiagonalization.capacity_gap_strictly_positive
#print axioms HigherOrderDiagonalization.capacity_gap_asymptotic
#print axioms HigherOrderDiagonalization.capacity_gap_at_k_plus_2

-- Diagonalization theorems
#print axioms HigherOrderDiagonalization.length_filter_split
#print axioms HigherOrderDiagonalization.filter_nodup
#print axioms HigherOrderDiagonalization.nodup_filter_eq_le_one
#print axioms HigherOrderDiagonalization.nodup_length_le
#print axioms HigherOrderDiagonalization.upto_length
#print axioms HigherOrderDiagonalization.upto_mem
#print axioms HigherOrderDiagonalization.map_nodup_of_inj
#print axioms HigherOrderDiagonalization.pigeonhole
#print axioms HigherOrderDiagonalization.higher_order_diagonalization
#print axioms HigherOrderDiagonalization.diagonal_fiber_non_singleton
#print axioms HigherOrderDiagonalization.higher_order_diagonal_duality

end HigherOrderDiagonalization.Audit
