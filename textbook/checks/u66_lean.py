"""Unit 66 check: kernel-check the book's Lean for Unit 66 (TraceAlgebra).

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u66_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.TraceAlgebra

namespace Textbook.U66
open PrimitivePassage TransitionAlphabet TraceAlgebra

def lEx : List PEvent :=
  [.setBudget 1, .setBudget 1, .addCol [0], .addCol [0], .halt, .admitOcc 9]

def lPrime : List PEvent :=
  [.setBudget 2, .setBudget 1, .addCol [0], .halt]

theorem exercise_nf_eq :
    nf lEx = [.setBudget 1, .addCol [0], .halt] ∧
    noRedex (nf lEx) = true ∧
    nf lPrime ≠ nf lEx := by
  decide

theorem exercise_unscoped_eqv (s : PState) :
    replayP lPrime s = replayP (nf lEx) s := by
  have h12 : step (step s (.setBudget 2)) (.setBudget 1) = step s (.setBudget 1) := by
    cases hh : s.halted with
    | true => rw [step_halted s (.setBudget 2) hh]
    | false =>
        rw [step_setBudget_live s 2 hh,
          step_setBudget_live (budS s 2) 1 (show (budS s 2).halted = false from hh),
          step_setBudget_live s 1 hh]
        rfl
  change replayP [.addCol [0], .halt] (step (step s (.setBudget 2)) (.setBudget 1))
    = replayP [.addCol [0], .halt] (step s (.setBudget 1))
  rw [h12]

theorem budget_write_order :
    (replayP [.setBudget 1, .setBudget 2] genesisP).budget = 2 ∧
    (replayP [.setBudget 2, .setBudget 1] genesisP).budget = 1 := by decide

end Textbook.U66

#print axioms Textbook.U66.budget_write_order

#print axioms Textbook.U66.exercise_nf_eq
#print axioms Textbook.U66.exercise_unscoped_eqv
#print axioms TraceAlgebra.step_eq_ite
#print axioms TraceAlgebra.inert_iff_guard_fails
#print axioms TraceAlgebra.terminal_absorbs
#print axioms TraceAlgebra.replayP_halted
#print axioms TraceAlgebra.trace_absorbs
#print axioms TraceAlgebra.v_not_mem_map
#print axioms TraceAlgebra.colOk_false_of_mem
#print axioms TraceAlgebra.refineOk_false_of_not_mem
#print axioms TraceAlgebra.guardHolds_post_false
#print axioms TraceAlgebra.step_idem
#print axioms TraceAlgebra.retention_idem
#print axioms TraceAlgebra.terminal_idem
#print axioms TraceAlgebra.replay_erases
#print axioms TraceAlgebra.legal_trace_replays
#print axioms TraceAlgebra.comm_setLicense
#print axioms TraceAlgebra.comm_setBudget
#print axioms TraceAlgebra.comm_setBudget_setLicense
#print axioms TraceAlgebra.comm_admitOcc
#print axioms TraceAlgebra.noncomm_license_extension
#print axioms TraceAlgebra.noncomm_budget_extension
#print axioms TraceAlgebra.noncomm_terminal
#print axioms TraceAlgebra.noncomm_supply_retention
#print axioms TraceAlgebra.noncomm_same_store
#print axioms TraceAlgebra.same_store_observationally_equal
#print axioms TraceAlgebra.internal_trace_preserves_occ
#print axioms TraceAlgebra.internal_trace_preserves_license
#print axioms TraceAlgebra.internal_blocks_cannot_supply_or_license
#print axioms TraceAlgebra.refusal_persists_step
#print axioms TraceAlgebra.refusal_persists_replay
#print axioms TraceAlgebra.refusal_not_erasable
#print axioms TraceAlgebra.replay_eqv_scoped
#print axioms TraceAlgebra.replay_eqv_not_unscoped
#print axioms TraceAlgebra.rw_sound
#print axioms TraceAlgebra.rwStar_sound
#print axioms TraceAlgebra.rw_length
#print axioms TraceAlgebra.rw_preserves_nf
#print axioms TraceAlgebra.rwStar_preserves_nf
#print axioms TraceAlgebra.nf_noRedex
#print axioms TraceAlgebra.noRedex_nf_eq
#print axioms TraceAlgebra.rwStar_to_nf
#print axioms TraceAlgebra.rw_confluent
#print axioms TraceAlgebra.nf_unique
#print axioms TraceAlgebra.nf_sound
#print axioms TraceAlgebra.rewrite_not_complete
"""

EXPECTED = {
    "Textbook.U66.budget_write_order": BOTH,

    "Textbook.U66.exercise_nf_eq": NONE,
    "Textbook.U66.exercise_unscoped_eqv": BOTH,
    "TraceAlgebra.step_eq_ite": BOTH,
    "TraceAlgebra.inert_iff_guard_fails": BOTH,
    "TraceAlgebra.terminal_absorbs": BOTH,
    "TraceAlgebra.replayP_halted": BOTH,
    "TraceAlgebra.trace_absorbs": BOTH,
    "TraceAlgebra.v_not_mem_map": BOTH,
    "TraceAlgebra.colOk_false_of_mem": BOTH,
    "TraceAlgebra.refineOk_false_of_not_mem": BOTH,
    "TraceAlgebra.guardHolds_post_false": BOTH,
    "TraceAlgebra.step_idem": BOTH,
    "TraceAlgebra.retention_idem": BOTH,
    "TraceAlgebra.terminal_idem": BOTH,
    "TraceAlgebra.replay_erases": BOTH,
    "TraceAlgebra.legal_trace_replays": BOTH,
    "TraceAlgebra.comm_setLicense": BOTH,
    "TraceAlgebra.comm_setBudget": BOTH,
    "TraceAlgebra.comm_setBudget_setLicense": BOTH,
    "TraceAlgebra.comm_admitOcc": BOTH,
    "TraceAlgebra.noncomm_license_extension": BOTH,
    "TraceAlgebra.noncomm_budget_extension": BOTH,
    "TraceAlgebra.noncomm_terminal": BOTH,
    "TraceAlgebra.noncomm_supply_retention": BOTH,
    "TraceAlgebra.noncomm_same_store": BOTH,
    "TraceAlgebra.same_store_observationally_equal": BOTH,
    "TraceAlgebra.internal_trace_preserves_occ": BOTH,
    "TraceAlgebra.internal_trace_preserves_license": BOTH,
    "TraceAlgebra.internal_blocks_cannot_supply_or_license": BOTH,
    "TraceAlgebra.refusal_persists_step": BOTH,
    "TraceAlgebra.refusal_persists_replay": BOTH,
    "TraceAlgebra.refusal_not_erasable": BOTH,
    "TraceAlgebra.replay_eqv_scoped": BOTH,
    "TraceAlgebra.replay_eqv_not_unscoped": BOTH,
    "TraceAlgebra.rw_sound": BOTH,
    "TraceAlgebra.rwStar_sound": BOTH,
    "TraceAlgebra.rw_length": BOTH,
    "TraceAlgebra.rw_preserves_nf": NONE,
    "TraceAlgebra.rwStar_preserves_nf": NONE,
    "TraceAlgebra.nf_noRedex": NONE,
    "TraceAlgebra.noRedex_nf_eq": PROPEXT,
    "TraceAlgebra.rwStar_to_nf": NONE,
    "TraceAlgebra.rw_confluent": NONE,
    "TraceAlgebra.nf_unique": PROPEXT,
    "TraceAlgebra.nf_sound": BOTH,
    "TraceAlgebra.rewrite_not_complete": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U66"))
