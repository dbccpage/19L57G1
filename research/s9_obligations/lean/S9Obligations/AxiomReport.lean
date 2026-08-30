import S9Obligations

-- Report inventory for `verify_lean.py`.  Reports are appended per part:
-- each part adds one `#print axioms <declaration>` line here for every
-- theorem it exports, and lists the same declaration, in the same order,
-- in `AXIOM_REPORT_DECLARATIONS` at the top of `verify_lean.py`.  The
-- inventory starts empty; an empty inventory is a receipt for nothing.

-- P1 (S9.1, the axiom lattice): S9Obligations/AxiomLattice.lean, in file order.
#print axioms S9Obligations.AxiomLattice.irreflClause_holds_iff
#print axioms S9Obligations.AxiomLattice.atom_head_clause_holds_on_full
#print axioms S9Obligations.AxiomLattice.non_falsum_clause_set_admits_selfdiff
#print axioms S9Obligations.AxiomLattice.falsum_clause_entails_irrefl
#print axioms S9Obligations.AxiomLattice.has_falsum_clause_entails_irrefl
#print axioms S9Obligations.AxiomLattice.transfers_iff_entails_irrefl
#print axioms S9Obligations.AxiomLattice.transfers_iff_has_falsum_clause
#print axioms S9Obligations.AxiomLattice.atom_head_clause_does_not_transfer
#print axioms S9Obligations.AxiomLattice.entails_irrefl_iff_has_falsum_clause
#print axioms S9Obligations.AxiomLattice.transfers_above_point_iff
#print axioms S9Obligations.AxiomLattice.reflexivePointForcesSingleton_holds_iff
#print axioms S9Obligations.AxiomLattice.reflexive_point_forces_singleton_irrefl_of_two_points
#print axioms S9Obligations.AxiomLattice.reflexive_point_forces_singleton_transfers_above_point
#print axioms S9Obligations.AxiomLattice.reflexive_point_forces_singleton_admits_selfdiff
#print axioms S9Obligations.AxiomLattice.reflexive_point_forces_singleton_not_entails_irrefl
#print axioms S9Obligations.AxiomLattice.reflexive_point_forces_singleton_f3_countermodel_above_point
#print axioms S9Obligations.AxiomLattice.pure_non_falsum_clause_set_holds_on_full
#print axioms S9Obligations.AxiomLattice.pure_one_point_full_implies_two_point_full
#print axioms S9Obligations.AxiomLattice.pure_transfer_above_point_iff_has_falsum_clause
#print axioms S9Obligations.AxiomLattice.pure_transfers_above_point_iff_entails_irrefl
#print axioms S9Obligations.AxiomLattice.reflexivePointForcesSingleton_holds_iff_of_decidableEq
#print axioms S9Obligations.AxiomLattice.transfers_above_point_of_entails_reflexive_point_forces_singleton
#print axioms S9Obligations.AxiomLattice.transfers_above_point_imp_entails_reflexive_point_forces_singleton

-- P2 (S9.2, morphism classes): S9Obligations/MorphismClasses.lean, in file order.
#print axioms S9Obligations.MorphismClasses.not_both
#print axioms S9Obligations.MorphismClasses.injective_of_ne
#print axioms S9Obligations.MorphismClasses.two_element_pointed_map_unique
#print axioms S9Obligations.MorphismClasses.D2_initial_P_E
#print axioms S9Obligations.MorphismClasses.FULL2_initial_P_NE
#print axioms S9Obligations.MorphismClasses.no_injection_into_point
#print axioms S9Obligations.MorphismClasses.no_surjection_onto_three
#print axioms S9Obligations.MorphismClasses.two_copies_not_unique
#print axioms S9Obligations.MorphismClasses.diagonal_candidate_not_pointed_into_D2
#print axioms S9Obligations.MorphismClasses.extra_edge_not_into_D2
#print axioms S9Obligations.MorphismClasses.non_edge_not_into_point
#print axioms S9Obligations.MorphismClasses.pointed_map_injective_of_irrefl
#print axioms S9Obligations.MorphismClasses.two_element_initial_P_I_irrefl
#print axioms S9Obligations.MorphismClasses.D2_initial_P_E_I_irrefl
#print axioms S9Obligations.MorphismClasses.S2_initial_P_NE_irrefl
#print axioms S9Obligations.MorphismClasses.S2_initial_P_NE_I_irrefl
#print axioms S9Obligations.MorphismClasses.S2_not_P_E_into_D2
#print axioms S9Obligations.MorphismClasses.D2_not_P_NE_into_S2
#print axioms S9Obligations.MorphismClasses.no_surjection_onto_three_irrefl
#print axioms S9Obligations.MorphismClasses.two_irrefl_copies_not_unique
#print axioms S9Obligations.MorphismClasses.initial_P_iff
#print axioms S9Obligations.MorphismClasses.initial_P_E_iff
#print axioms S9Obligations.MorphismClasses.initial_P_NE_iff
#print axioms S9Obligations.MorphismClasses.not_initial_P_E_NE
#print axioms S9Obligations.MorphismClasses.admits_primary_iff
#print axioms S9Obligations.MorphismClasses.admits_primary_exactly
#print axioms S9Obligations.MorphismClasses.admits_secondary_iff
#print axioms S9Obligations.MorphismClasses.admits_secondary_exactly

-- P3 (S9.3, witness types): S9Obligations/WitnessTypes.lean, in file order.
#print axioms S9Obligations.WitnessTypes.cardTwo
#print axioms S9Obligations.WitnessTypes.cardPosIff
#print axioms S9Obligations.WitnessTypes.v1ListLength
#print axioms S9Obligations.WitnessTypes.v2AnonListLength
#print axioms S9Obligations.WitnessTypes.v1V2AnonListLength
#print axioms S9Obligations.WitnessTypes.v1V2AnonListNodup
#print axioms S9Obligations.WitnessTypes.v1ListNodup
#print axioms S9Obligations.WitnessTypes.v2AnonListNodup
#print axioms S9Obligations.WitnessTypes.v1ListReadsCountsOnly
#print axioms S9Obligations.WitnessTypes.sharedTransport
#print axioms S9Obligations.WitnessTypes.someSharedTransport
#print axioms S9Obligations.WitnessTypes.twoSharedTransport
#print axioms S9Obligations.WitnessTypes.S9_3_sep_presence_equal
#print axioms S9Obligations.WitnessTypes.S9_3_sep_count_equal
#print axioms S9Obligations.WitnessTypes.S9_3_sep_V1_indistinguishable
#print axioms S9Obligations.WitnessTypes.S9_3_sep_V2_ANON_separates
#print axioms S9Obligations.WitnessTypes.sepExactlyOneV2AnonQuestionDiffers
#print axioms S9Obligations.WitnessTypes.S9_3_sep_not_isomorphic
#print axioms S9Obligations.WitnessTypes.sepRawDataDiffer
#print axioms S9Obligations.WitnessTypes.sepPresenceS2
#print axioms S9Obligations.WitnessTypes.sepPresenceIrrefl
#print axioms S9Obligations.WitnessTypes.S9_3_inv_V1_V2_ANON_indistinguishable
#print axioms S9Obligations.WitnessTypes.S9_3_inv_count_equal
#print axioms S9Obligations.WitnessTypes.invSharedCounts
#print axioms S9Obligations.WitnessTypes.invTwoShared
#print axioms S9Obligations.WitnessTypes.S9_3_inv_not_isomorphic
#print axioms S9Obligations.WitnessTypes.invRawDataDiffer
#print axioms S9Obligations.WitnessTypes.invPresenceS2
#print axioms S9Obligations.WitnessTypes.invPresenceIrrefl
#print axioms S9Obligations.WitnessTypes.evalReadsCounts
#print axioms S9Obligations.WitnessTypes.v1ListReadsCounts
#print axioms S9Obligations.WitnessTypes.sepV1IndistinguishableViaCounts
