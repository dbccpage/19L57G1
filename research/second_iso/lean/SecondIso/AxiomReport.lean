/-
AxiomReport: one report per theorem of this rung's package, across every
module of the library, the four reconstructions included.  `verify_lean.py`
derives the same census independently from the compiled environment and
fails if the two differ, in either direction, so a dropped print is a
failure rather than a silence.  Names are fully qualified, so the report
text and this list are the same strings.
AuthorityEffect: None.
-/

import SecondIso


-- Kernel.lean (17)
#print axioms SecondIso.Sealed.insertNew_nil
#print axioms SecondIso.Sealed.insertNew_of_not_mem
#print axioms SecondIso.Sealed.insertNew_of_mem
#print axioms SecondIso.Sealed.mem_insertNew
#print axioms SecondIso.Sealed.separable_not_collapsed
#print axioms SecondIso.Sealed.R2L_wf
#print axioms SecondIso.Sealed.R2F_wf
#print axioms SecondIso.Sealed.supply_no_op
#print axioms SecondIso.Sealed.genesis_underivable
#print axioms SecondIso.Sealed.underivable_of_empty
#print axioms SecondIso.Sealed.collapsed_of_no_insts
#print axioms SecondIso.Sealed.R2L_collapsed
#print axioms SecondIso.Sealed.R2F_collapsed
#print axioms SecondIso.Sealed.historyL_replays
#print axioms SecondIso.Sealed.historyF_replays
#print axioms SecondIso.Sealed.admission_without_expressive_increase
#print axioms SecondIso.Sealed.replayE_append

-- IsoKernel.lean (8)
#print axioms SecondIso.Sealed.map_eq_self_of_mem
#print axioms SecondIso.Sealed.plug_args_lt
#print axioms SecondIso.Sealed.Iso.symm_dmap
#print axioms SecondIso.Sealed.Iso.plug_cmap
#print axioms SecondIso.Sealed.Iso.wfCtx_cmap
#print axioms SecondIso.Sealed.Iso.derivable_imap
#print axioms SecondIso.Sealed.Iso.collapsed_fwd
#print axioms SecondIso.Sealed.Iso.collapsed_transport

-- Inherited.lean (6)
#print axioms SecondIso.Inherited.stake_irrefl
#print axioms SecondIso.Inherited.demands_subset_labelled
#print axioms SecondIso.Inherited.free_stake_no_demand
#print axioms SecondIso.Inherited.labelled_cases
#print axioms SecondIso.Inherited.collapsed_not_separable
#print axioms SecondIso.Inherited.collapsed_of_not_separable

-- IndexSlice.lean (4)
#print axioms SecondIso.IndexSlice.stateAt_zero
#print axioms SecondIso.IndexSlice.stateAt_full
#print axioms SecondIso.IndexSlice.quiet_before_the_index
#print axioms SecondIso.IndexSlice.first_demand_unique

-- Transport.lean (14)
#print axioms SecondIso.Transport.separable_symm
#print axioms SecondIso.Transport.collapsed_symm
#print axioms SecondIso.Transport.honour_symm
#print axioms SecondIso.Transport.dmap_inj
#print axioms SecondIso.Transport.separable_fwd
#print axioms SecondIso.Transport.separable_transport
#print axioms SecondIso.Transport.honour_transport
#print axioms SecondIso.Transport.uniform_freeStake
#print axioms SecondIso.Transport.uniform_allApart
#print axioms SecondIso.Transport.uniform_allSame
#print axioms SecondIso.Transport.uniform_preserved
#print axioms SecondIso.Transport.demand_transport
#print axioms SecondIso.Transport.hasDemand_transport_of_uniform
#print axioms SecondIso.Transport.hasDemand_iff_of_uniform

-- Trajectory.lean (9)
#print axioms SecondIso.Trajectory.related_symm
#print axioms SecondIso.Trajectory.matched_symm
#print axioms SecondIso.Trajectory.related_some_left
#print axioms SecondIso.Trajectory.first_demand_transport
#print axioms SecondIso.Trajectory.first_demand_matched_of_uniform
#print axioms SecondIso.Trajectory.stepE_renameSupply
#print axioms SecondIso.Trajectory.replayE_renameSupply
#print axioms SecondIso.Trajectory.stateAt_renameSupply
#print axioms SecondIso.Trajectory.first_demand_renameSupply

-- Check.lean (12)
#print axioms SecondIso.Check.unary_ctx_slots
#print axioms SecondIso.Check.collapsed_of_unary
#print axioms SecondIso.Check.separable_of_unary_witness
#print axioms SecondIso.Check.sepB_sound
#print axioms SecondIso.Check.colB_sound
#print axioms SecondIso.Check.honourCheck_sound
#print axioms SecondIso.Check.dishonourCheck_sound
#print axioms SecondIso.Check.noDemandCheck_sound
#print axioms SecondIso.Check.demandCheck_sound
#print axioms SecondIso.Check.index_of_check
#print axioms SecondIso.Check.no_index_of_check
#print axioms SecondIso.Check.related_of_relBy

-- Countermodel.lean (14)
#print axioms SecondIso.Countermodel.parity_not_uniform
#print axioms SecondIso.Countermodel.residue_not_uniform
#print axioms SecondIso.Countermodel.chain_not_uniform
#print axioms SecondIso.Countermodel.demand_not_class_invariant
#print axioms SecondIso.Countermodel.matched_P
#print axioms SecondIso.Countermodel.matched_Q
#print axioms SecondIso.Countermodel.index_P2_parity
#print axioms SecondIso.Countermodel.quiet_P1_parity
#print axioms SecondIso.Countermodel.index_P2_chain
#print axioms SecondIso.Countermodel.quiet_P1_chain
#print axioms SecondIso.Countermodel.index_Q2_residue
#print axioms SecondIso.Countermodel.quiet_Q1_residue
#print axioms SecondIso.Countermodel.first_count_not_trajectory_invariant
#print axioms SecondIso.Countermodel.iso_index
