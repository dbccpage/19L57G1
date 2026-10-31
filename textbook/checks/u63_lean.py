"""Unit 63 check: kernel-check the book's Lean for Unit 63 (GraphGenesis).

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u63_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.GraphGenesis

namespace Textbook.U63
open PrimitivePassage Attachment GraphGenesis

-- Student exercise checks on blindPair
theorem blindPair_obst_true : obstP blindPair 0 1 = true := by decide

theorem blindPair_upBlock0_grows_occ :
    (replayP (upBlock blindPair 0) blindPair).occ = [0, 1, 2] ∧
    (replayP (upBlock blindPair 0) blindPair).obs = some [] := by decide

theorem separately_declared_supply_grows :
    (replayP [.admitOcc 7] genesisP).occ = [7] ∧
    IsResponseEvent (.admitOcc 7) = false := by decide

theorem proposal_cost_is_declared (s : PState) (P : ProposalRecord s) :
    ({ P with cost := 0 } : ProposalRecord s).block = P.block ∧
    ({ P with cost := 0 } : ProposalRecord s).cost = 0 := ⟨rfl, rfl⟩

end Textbook.U63

#print axioms Textbook.U63.separately_declared_supply_grows
#print axioms Textbook.U63.proposal_cost_is_declared

#print axioms Textbook.U63.blindPair_obst_true
#print axioms Textbook.U63.blindPair_upBlock0_grows_occ
#print axioms GraphGenesis.refineCol_only_obs
#print axioms GraphGenesis.addCol_only_obs
#print axioms GraphGenesis.extensionProposals_range_over_existing
#print axioms GraphGenesis.repairFamily_range_over_existing
#print axioms GraphGenesis.nextFamilyP_block_shape
#print axioms GraphGenesis.nextFamilyP_range_over_existing
#print axioms GraphGenesis.IsInternal_exact
#print axioms GraphGenesis.internal_is_response
#print axioms GraphGenesis.response_step_fixes_graph
#print axioms GraphGenesis.internal_step_fixes_graph
#print axioms GraphGenesis.replay_fixes_graph_of_all
#print axioms GraphGenesis.internal_family_cannot_grow_carrier
#print axioms GraphGenesis.response_replay_fixes_graph
#print axioms GraphGenesis.nextFamilyP_blocks_are_responses
#print axioms GraphGenesis.nextFamilyP_block_fixes_graph
#print axioms GraphGenesis.graph_growth_is_supplied
#print axioms GraphGenesis.proposal_confers_no_execution
#print axioms GraphGenesis.upProposal_executes
#print axioms GraphGenesis.proposal_transports
#print axioms GraphGenesis.proposal_family_retains_ties
#print axioms GraphGenesis.obstruction_resolved_in_carrier
#print axioms GraphGenesis.family_never_grows_carrier
#print axioms GraphGenesis.growth_demand_not_obstruction_consequence
#print axioms GraphGenesis.blindPair_resolution_keeps_carrier
"""

EXPECTED = {
    "Textbook.U63.separately_declared_supply_grows": BOTH,
    "Textbook.U63.proposal_cost_is_declared": BOTH,

    "Textbook.U63.blindPair_obst_true": BOTH,
    "Textbook.U63.blindPair_upBlock0_grows_occ": BOTH,
    "GraphGenesis.refineCol_only_obs": BOTH,
    "GraphGenesis.addCol_only_obs": BOTH,
    "GraphGenesis.extensionProposals_range_over_existing": BOTH,
    "GraphGenesis.repairFamily_range_over_existing": BOTH,
    "GraphGenesis.nextFamilyP_block_shape": BOTH,
    "GraphGenesis.nextFamilyP_range_over_existing": BOTH,
    "GraphGenesis.IsInternal_exact": NONE,
    "GraphGenesis.internal_is_response": NONE,
    "GraphGenesis.response_step_fixes_graph": BOTH,
    "GraphGenesis.internal_step_fixes_graph": BOTH,
    "GraphGenesis.replay_fixes_graph_of_all": BOTH,
    "GraphGenesis.internal_family_cannot_grow_carrier": BOTH,
    "GraphGenesis.response_replay_fixes_graph": BOTH,
    "GraphGenesis.nextFamilyP_blocks_are_responses": BOTH,
    "GraphGenesis.nextFamilyP_block_fixes_graph": BOTH,
    "GraphGenesis.graph_growth_is_supplied": BOTH,
    "GraphGenesis.proposal_confers_no_execution": BOTH,
    "GraphGenesis.upProposal_executes": BOTH,
    "GraphGenesis.proposal_transports": BOTH,
    "GraphGenesis.proposal_family_retains_ties": BOTH,
    "GraphGenesis.obstruction_resolved_in_carrier": BOTH,
    "GraphGenesis.family_never_grows_carrier": BOTH,
    "GraphGenesis.growth_demand_not_obstruction_consequence": BOTH,
    "GraphGenesis.blindPair_resolution_keeps_carrier": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U63"))
