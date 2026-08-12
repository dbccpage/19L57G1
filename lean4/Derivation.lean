import Derivation.Basic
import Derivation.Inertia
import Derivation.Quot
import Derivation.Counting
import Derivation.Minimality
import Derivation.Progress
import Derivation.Erasure
import Derivation.Ext
import Derivation.PrimDiff
import Derivation.Bridge
import Derivation.Refusal
import Derivation.RefusalFrontier
import Derivation.Generator
import Derivation.DiffInterface
import Derivation.Represented

/-!
# Axiom reports

One `#print axioms` per exported theorem cited by the paper.  The build log
of this module is the axiom report artifact.
-/

open Derivation

-- Challenge 0-2
#print axioms Derivation.supply_no_op
#print axioms Derivation.genesis_underivable
#print axioms Derivation.underivable_of_empty
#print axioms Derivation.collapsed_of_no_insts
#print axioms Derivation.R2L_collapsed
#print axioms Derivation.R2F_collapsed
#print axioms Derivation.historyL_replays
#print axioms Derivation.historyF_replays
#print axioms Derivation.admission_without_expressive_increase
#print axioms Derivation.replayE_append
#print axioms Derivation.separable_not_collapsed

-- Abstraction barrier
#print axioms Derivation.quotient_barrier
#print axioms Derivation.quot_barrier
#print axioms Derivation.barrier_R2L

-- Counting / termination
#print axioms Derivation.index_le_strict_mono
#print axioms Derivation.strict_bounded_length
#print axioms Derivation.no_supply_round_bound
#print axioms Derivation.allPairs_length

-- Challenge 3 minimality
#print axioms Derivation.U0_separable
#print axioms Derivation.U1_separable
#print axioms Derivation.BL_separable
#print axioms Derivation.BD_separable
#print axioms Derivation.deltaU0_valid
#print axioms Derivation.deltaU1_valid
#print axioms Derivation.deltaBL_valid
#print axioms Derivation.deltaBD_valid
#print axioms Derivation.cost1_insufficient_general
#print axioms Derivation.cost1_insufficient
#print axioms Derivation.cost1_insufficient_F
#print axioms Derivation.deltaU0F_valid
#print axioms Derivation.U0_not_iso_BL
#print axioms Derivation.U0_not_iso_BD
#print axioms Derivation.BL_not_iso_BD
#print axioms Derivation.mu1_minimum_not_unique
#print axioms Derivation.deltaK_applies
#print axioms Derivation.markK_separable
#print axioms Derivation.deltaK_valid
#print axioms Derivation.deltaK_length
#print axioms Derivation.markK_pairwise_noniso
#print axioms Derivation.mu2_unique

-- Progress and pruning
#print axioms Derivation.mark_progress
#print axioms Derivation.separable_of_subrules

-- Token-erasure simulation (Lean as an abstraction of the token-aware
-- admission semantics)
#print axioms Derivation.erase_step
#print axioms Derivation.erase_replay

-- Membership extensionality (list representation vs set semantics)
#print axioms Derivation.derivable_ext
#print axioms Derivation.wfCtx_ext
#print axioms Derivation.collapsed_ext
#print axioms Derivation.separable_ext
#print axioms Derivation.applyItem_ext
#print axioms Derivation.applyDelta_ext
#print axioms Derivation.validResponse_ext

-- Primitive difference (self-contained investigation)
#print axioms PrimDiff.irrefl_witness_ne
#print axioms PrimDiff.selfdiff_consistent
#print axioms PrimDiff.symm_selfdiff_consistent
#print axioms PrimDiff.meta_diff_without_assertion
#print axioms PrimDiff.factors_through_point_iff
#print axioms PrimDiff.no_witness_on_subsingleton
#print axioms PrimDiff.D2_irrefl
#print axioms PrimDiff.S2_irrefl
#print axioms PrimDiff.D2_witness
#print axioms PrimDiff.D2_initial_pointed
#print axioms PrimDiff.one_point_hosts_bare_witness
#print axioms PrimDiff.witnessed_irrefl_on_every_larger_carrier
#print axioms PrimDiff.push_witness
#print axioms PrimDiff.collision_of_identifying_witness
#print axioms PrimDiff.collision_not_irrefl
#print axioms PrimDiff.bare_collapse_admissible
#print axioms PrimDiff.obstruction_under_irrefl
#print axioms PrimDiff.collapse_unobstructed_without_fidelity
#print axioms PrimDiff.collision_transpose_invariant
#print axioms PrimDiff.orientation_data_invisible_to_collapse
#print axioms PrimDiff.bool_irrefl_witness_classification
#print axioms PrimDiff.D2_not_pointed_iso_S2
#print axioms PrimDiff.D2_S2_collapse_equiv
#print axioms PrimDiff.symmetric_no_equivariant_classifier
#print axioms PrimDiff.swap_is_S2_automorphism
#print axioms PrimDiff.oriented_rigid
#print axioms PrimDiff.oriented_classifier_exists
#print axioms PrimDiff.single_oriented_witness_consistent
#print axioms PrimDiff.multiplicity_invisible_to_presence
#print axioms PrimDiff.repetition_no_new_content
#print axioms PrimDiff.repetition_new_occurrence
#print axioms PrimDiff.const_presentation_unfaithful
#print axioms PrimDiff.id_presentation_faithful
#print axioms PrimDiff.clos_empty_id
#print axioms PrimDiff.irred_empty_iff_ne
#print axioms PrimDiff.irred_antitone
#print axioms PrimDiff.merger_erases

-- The bridge: provenance of the primitive-difference ingredients
#print axioms Bridge.stepT_preserves_atMostTok
#print axioms Bridge.single_token_carrier_bound
#print axioms Bridge.second_token_required
#print axioms Bridge.no_admitForm_no_forms
#print axioms Bridge.no_forms_no_witness
#print axioms Bridge.irrefl_law_not_entailed
#print axioms Bridge.equivariant_witness_is_S2
#print axioms Bridge.equivariant_not_D2
#print axioms Bridge.no_swap_fixed_offdiag_pair
#print axioms Bridge.order_visible_to_metatheory
#print axioms Bridge.order_erased_at_object_level

-- Refusal as a difference source
#print axioms Refusal.silent_eq_meta
#print axioms Refusal.marker_state_invisible
#print axioms Refusal.markers_invisible
#print axioms Refusal.nonreify_carrier_bound
#print axioms Refusal.fact_state_changes
#print axioms Refusal.silent_state_fixed
#print axioms Refusal.reifyUntagged_eq_occurrence
#print axioms Refusal.reifyUntagged_replay_eq_occurrence
#print axioms Refusal.reifyUntagged_two_admissions
#print axioms Refusal.reifyTagged_two_admissions
#print axioms Refusal.tag_separates
#print axioms Refusal.occurrence_state_swap_invariant
#print axioms Refusal.tagged_state_not_swap_invariant
#print axioms Refusal.canonical_designation
#print axioms Refusal.tagged_translation_separable
#print axioms Refusal.untagged_translation_collapsed

-- Frontier Run 006: refusal, reflection, and the remaining bridge
#print axioms RefusalFrontier.silent_repetition_inert
#print axioms RefusalFrontier.trace_erasure
#print axioms RefusalFrontier.histories_collapse
#print axioms RefusalFrontier.mono_code_swap_invariant
#print axioms RefusalFrontier.distinct_code_not_swap_invariant
#print axioms RefusalFrontier.singleton_algebra_monochrome
#print axioms RefusalFrontier.distinction_needs_two_constructors
#print axioms RefusalFrontier.judgment_variant_second_judgment_not_datum
#print axioms RefusalFrontier.judgment_carrier_bound
#print axioms RefusalFrontier.priced_bridge_closes
#print axioms RefusalFrontier.priced_bridge_oriented
#print axioms RefusalFrontier.min_witnessed_route_closes
#print axioms RefusalFrontier.bridge_facts_not_law
#print axioms RefusalFrontier.equivariant_output_invariant
#print axioms RefusalFrontier.untyped_reflect_fixpoint
#print axioms RefusalFrontier.toggle_two_cycle
#print axioms RefusalFrontier.reflective_chain_growth
#print axioms RefusalFrontier.reflective_chain_is_initial_segment
#print axioms RefusalFrontier.reflective_chain_successor_relation
#print axioms RefusalFrontier.reflective_chain_irreflexive_facts

-- F5: the composite generator (reflective growth + pair-separation
-- closure)
#print axioms Generator.reflective_chain_tags
#print axioms Generator.chain_tagged_iff
#print axioms Generator.chain_hasIn_iff
#print axioms Generator.chain_hasOut_iff
#print axioms Generator.middle_profile
#print axioms Generator.endpoint0_profile
#print axioms Generator.endpointN_profile
#print axioms Generator.depth1_obstructions_are_exactly_middle_pairs
#print axioms Generator.generation_never_dries
#print axioms Generator.automark_presence_vacuous
#print axioms Generator.le_foldr_max
#print axioms Generator.finite_marks_outrun
#print axioms Generator.valued_marks_collapse_generation
#print axioms Generator.middle_swap_not_relation_preserving
#print axioms Generator.depth2_separates_near_ends_n4
#print axioms Generator.depth2_obstruction_n5

-- The native primitive-difference interface (caller-requested package)
#print axioms DiffInterface.zeroRel_equivalence
#print axioms DiffInterface.kernel_zeroRel
#print axioms DiffInterface.obsQuotient_eq_of_zero
#print axioms DiffInterface.no_guard_no_obstruction
#print axioms DiffInterface.unretained_not_active
#print axioms DiffInterface.distinguished_not_active
#print axioms DiffInterface.bare_reflection_certifies_active_obstruction
#print axioms DiffInterface.refines_preserves_distinctions
#print axioms DiffInterface.closure_preserves_old_distinctions
#print axioms DiffInterface.closure_kills_demanded
#print axioms DiffInterface.closure_adds_no_obstruction
#print axioms DiffInterface.drive_terminates
#print axioms DiffInterface.cview_distinct_mono
#print axioms DiffInterface.tower_closed
#print axioms DiffInterface.tower_obstruction
#print axioms DiffInterface.swapTop_view
#print axioms DiffInterface.swapTop_live_inj
#print axioms DiffInterface.tower_step_composes
#print axioms DiffInterface.tower_successor_step
#print axioms DiffInterface.mem_activePairs
#print axioms DiffInterface.mem_activePairs_iff_active
#print axioms DiffInterface.closed_measure_zero
#print axioms DiffInterface.preclose_measure_pos
#print axioms DiffInterface.tower_demand_characterized
#print axioms DiffInterface.tower_demand_bound
#print axioms DiffInterface.towerNext_decrease
#print axioms DiffInterface.tower_fuel_terminates
#print axioms DiffInterface.bool_view_pigeonhole
#print axioms DiffInterface.bool_grammar_obstruction
#print axioms DiffInterface.no_bool_view_is_closed
#print axioms DiffInterface.cm_freshness
#print axioms DiffInterface.cm_tagging
#print axioms DiffInterface.cm_edge
#print axioms DiffInterface.cm_hash
#print axioms DiffInterface.cm_repetition

-- Represented progress without an outside
#print axioms Represented.bool_eq_of_iff
#print axioms Represented.or_not_eq_true
#print axioms Represented.replay_deterministic
#print axioms Represented.replay_nil
#print axioms Represented.replay_append
#print axioms Represented.support_determines
#print axioms Represented.internal_support
#print axioms Represented.notes_inert
#print axioms Represented.repairFamily_sound
#print axioms Represented.repairFamily_complete
#print axioms Represented.repairFamily_retains_ties
#print axioms Represented.equiv_step
#print axioms Represented.equiv_replay
#print axioms Represented.equiv_repairFamily
#print axioms Represented.mark_discharges
#print axioms Represented.mark_preserves
#print axioms Represented.step_mark_sound
#print axioms Represented.satB_aug
#print axioms Represented.aug_preserves_satisfied
#print axioms Represented.aug_increases
#print axioms Represented.wf_genesis
#print axioms Represented.wf_step
#print axioms Represented.wf_replay
#print axioms Represented.represented_progress
#print axioms Represented.progress_needs_budget
#print axioms Represented.progress_needs_license
#print axioms Represented.violation_only_from_require
#print axioms Represented.quiescent_stable
#print axioms Represented.histUpTo_prefix
#print axioms Represented.admit_data_fresh
#print axioms Represented.worldAt_data
#print axioms Represented.worldAt_growth
#print axioms Represented.productive_run
#print axioms Represented.worldAt_three_quiescent
#print axioms Represented.wit_all_lengths
#print axioms Represented.wit_no_infinite
#print axioms Represented.cert_scope
#print axioms Represented.cert_not_correspondence
#print axioms Represented.cert_panel_relative
#print axioms Represented.scheduler_hidden
#print axioms Represented.gensym_hidden
#print axioms Represented.oracle_hidden
#print axioms Represented.incomplete_search_false_alarm
#print axioms Represented.augmentation_destroys_old_replay
#print axioms Represented.repetition_not_progress
#print axioms Represented.order_sensitivity_splits_equivalents
#print axioms Represented.refusal_needs_certificate
#print axioms Represented.refusals_are_represented
