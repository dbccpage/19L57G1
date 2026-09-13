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
