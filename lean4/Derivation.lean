import Derivation.Basic
import Derivation.Inertia
import Derivation.Quot
import Derivation.Counting
import Derivation.Minimality
import Derivation.Progress
import Derivation.Erasure
import Derivation.Ext

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
