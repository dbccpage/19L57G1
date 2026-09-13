import DiagonalIdentity

-- Report inventory for `verify_lean.py`.  One `#print axioms` line per
-- exported theorem, in the same order as `AXIOM_REPORT_DECLARATIONS`.

#print axioms DiagonalIdentity.Covering.diagonal_bool
#print axioms DiagonalIdentity.Covering.flipFin_ne
#print axioms DiagonalIdentity.Covering.diagSeq_diff_at
#print axioms DiagonalIdentity.Covering.seq_uncountable
#print axioms DiagonalIdentity.Covering.diagThread_diff_seq
#print axioms DiagonalIdentity.Covering.thread_uncountable
#print axioms DiagonalIdentity.Covering.not_surjective_nat_to_thread
#print axioms DiagonalIdentity.Combinator.diagBool_is_diagFlip
#print axioms DiagonalIdentity.Combinator.diagSeq_is_diagFlip
#print axioms DiagonalIdentity.Combinator.diagFlip_ne_row
#print axioms DiagonalIdentity.Collapse.d2_constant_obstructs
#print axioms DiagonalIdentity.Collapse.identifying_push_not_irrefl
#print axioms DiagonalIdentity.Collapse.identifying_push_self_loop
#print axioms DiagonalIdentity.Split.collapse_yes_covering_no
#print axioms DiagonalIdentity.Split.family_miss_and_identifying_push
#print axioms DiagonalIdentity.Dual.rec_roundtrip
#print axioms DiagonalIdentity.Dual.cast_injective
#print axioms DiagonalIdentity.Dual.bool_ne_nat
#print axioms DiagonalIdentity.Dual.unit_ne_seq
#print axioms DiagonalIdentity.Dual.covering_family_type_ne_d2Const_type
#print axioms DiagonalIdentity.Dual.pair_id_iff_fidelity
#print axioms DiagonalIdentity.Dual.d2Const_not_injective
#print axioms DiagonalIdentity.Dual.d2Const_pair_id
#print axioms DiagonalIdentity.Dual.d2Const_not_as_covering_family
#print axioms DiagonalIdentity.Dual.d2Const_push_self_loop
#print axioms DiagonalIdentity.Dual.family_miss_diagSeq
#print axioms DiagonalIdentity.Dual.family_not_surjective
#print axioms DiagonalIdentity.Dual.family_not_as_d2_const
#print axioms DiagonalIdentity.Dual.covering_miss_witness_is_diagFlip
#print axioms DiagonalIdentity.Dual.dual_on_declared_carriers
