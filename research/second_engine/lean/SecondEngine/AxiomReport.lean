import SecondEngine

/-!
# The axiom report

One `#print axioms` line for every theorem of the package, in module
order.  `verify_lean.py` builds this module fresh and compares the
reports with a compiler census of the package in both directions.

AuthorityEffect: None.
-/

-- Kernel.lean
#print axioms SecondEngine.Sealed.insertNew_nil
#print axioms SecondEngine.Sealed.insertNew_of_not_mem
#print axioms SecondEngine.Sealed.insertNew_of_mem
#print axioms SecondEngine.Sealed.mem_insertNew
#print axioms SecondEngine.Sealed.separable_not_collapsed
#print axioms SecondEngine.Sealed.R2L_wf
#print axioms SecondEngine.Sealed.R2F_wf
#print axioms SecondEngine.Sealed.supply_no_op
#print axioms SecondEngine.Sealed.genesis_underivable
#print axioms SecondEngine.Sealed.underivable_of_empty
#print axioms SecondEngine.Sealed.collapsed_of_no_insts
#print axioms SecondEngine.Sealed.R2L_collapsed
#print axioms SecondEngine.Sealed.R2F_collapsed
#print axioms SecondEngine.Sealed.historyL_replays
#print axioms SecondEngine.Sealed.historyF_replays
#print axioms SecondEngine.Sealed.admission_without_expressive_increase
#print axioms SecondEngine.Sealed.replayE_append
-- Carry.lean
#print axioms SecondEngine.Carry.map_inv
#print axioms SecondEngine.Carry.plug_mapCtx
#print axioms SecondEngine.Carry.plug_args_lt
#print axioms SecondEngine.Carry.wfCtx_mapCtx
#print axioms SecondEngine.Carry.derivable_fwd
#print axioms SecondEngine.Carry.derivable_bwd
#print axioms SecondEngine.Carry.derivable_mapCtx
#print axioms SecondEngine.Carry.separable_iso
#print axioms SecondEngine.Carry.collapsed_iso
-- Orbit.lean
#print axioms SecondEngine.Orbit.sortPair_swap
#print axioms SecondEngine.Orbit.sortPair_map
#print axioms SecondEngine.Orbit.separable_iso_iff
#print axioms SecondEngine.Orbit.collapsed_iso_iff
#print axioms SecondEngine.Orbit.oneOrbit_iso
#print axioms SecondEngine.Orbit.reqMember_iso
-- Stake.lean
#print axioms SecondEngine.Stake.flip_flip
#print axioms SecondEngine.Stake.e3_flip_eq_e4
#print axioms SecondEngine.Stake.e4_flip_eq_e3
#print axioms SecondEngine.Stake.e1_never_demands
#print axioms SecondEngine.Stake.e1_flip_demands
#print axioms SecondEngine.Stake.e8_quiet_without_reqs
#print axioms SecondEngine.Stake.carried_flip
#print axioms SecondEngine.Stake.demand_carried
#print axioms SecondEngine.Stake.e1_carried
#print axioms SecondEngine.Stake.e3_carried
#print axioms SecondEngine.Stake.e4_carried
#print axioms SecondEngine.Stake.e8_carried
-- Genesis.lean
#print axioms SecondEngine.Genesis.genL_replays
#print axioms SecondEngine.Genesis.genL_one_orbit
#print axioms SecondEngine.Genesis.genL_collapsed
#print axioms SecondEngine.Genesis.e4_demands_at_genL
#print axioms SecondEngine.Genesis.e3_quiet_at_genL
#print axioms SecondEngine.Genesis.e1_flip_demands_at_genL
#print axioms SecondEngine.Genesis.minima_differ_at_genL
-- Engine.lean
#print axioms SecondEngine.EngineDef.fixpoint_of_halt
#print axioms SecondEngine.EngineDef.step_at_demand_is_response
#print axioms SecondEngine.EngineDef.run_named
#print axioms SecondEngine.EngineDef.e1_engine_quiet
#print axioms SecondEngine.EngineDef.e1_halt_no_step
-- Census.lean
#print axioms SecondEngine.Census.class_size
#print axioms SecondEngine.Census.literal_size
#print axioms SecondEngine.Census.count_ge_six
#print axioms SecondEngine.Census.count_six_members
#print axioms SecondEngine.Census.literal_count_ge_seven
#print axioms SecondEngine.Census.literal_count_seven_members
#print axioms SecondEngine.Census.literal_count2_seven_members
#print axioms SecondEngine.Census.no_one_declaration
#print axioms SecondEngine.Census.same_caps_e3_e4
#print axioms SecondEngine.Census.no_initial
#print axioms SecondEngine.Census.no_initial_of_two_measures
