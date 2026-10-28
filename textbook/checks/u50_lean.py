"""Unit 50 check: kernel-check the book's Lean for Unit 50.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u50_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Horizon

namespace Textbook.U50
open Represented Constitution Initiality Horizon

/-- The specification at stage 3, written out, and the generated world agrees. -/
theorem spec_three :
    specWorld 3 = ⟨[0, 1, 2, 3], [[1], [2], [3]], [(0, 1), (0, 2), (0, 3)], [], 0, true, []⟩ := by
  decide

theorem worldAt_three_by_spec : worldAt 3 = specWorld 3 := worldAt_spec 3

theorem worldAt_three_by_computation :
    worldAt 3 = ⟨[0, 1, 2, 3], [[1], [2], [3]], [(0, 1), (0, 2), (0, 3)], [], 0, true, []⟩ := by
  decide

/-- Block 3 from stage 2, through the three intermediate states. -/
theorem block_three_steps :
    step (specWorld 2) (.setBudget 1) = w1 2 ∧
    step (w1 2) (.admitTok 3) = w2 2 ∧
    step (w2 2) (.require 0 3) = w3 2 ∧
    step (w3 2) (.addView [3]) = specWorld 3 := by decide

/-- The guard facts at stage 2: the old columns are blind to the new
requirement, the new column separates it. -/
theorem columns_at_two :
    sepB [1] 0 3 = false ∧ sepB [2] 0 3 = false ∧ sepB [3] 0 3 = true := by decide

theorem old_cols_blind_instance : sepB [2] 0 3 = false :=
  old_cols_blind 2 (by decide)

/-- Instances of the every-stage theorems at stages no `decide` would reach cheaply. -/
theorem stage_ten_quiescent : quiescentB (worldAt 10) = true := worldAt_quiescent 10
theorem stage_hundred_wf : WF (worldAt 100) := worldAt_wf 100
theorem gen_hundred_quiescent : quiescentB (genWorld 100).w = true := gen_quiescent 100

theorem block_three_accepted : step (w3 3) (.addView [4]) = worldAt 4 :=
  (block_all_accepted 3).2.2.2.2

/-- The carrier at stage k has k + 1 elements, read off the specification. -/
theorem carrier_size (k : Nat) : (worldAt k).data.length = k + 1 := by
  rw [worldAt_spec]
  show (List.range (k + 1)).length = k + 1
  exact List.length_range

/-- "Changed" certifies "accepted" because every rejecting branch is the
identity; the converse fails: an unguarded event can change nothing. -/
theorem genesis_first_step : step genesis (.admitTok 0) = ⟨[0], [], [], [], 0, true, []⟩ := by
  decide

theorem unguarded_can_be_silent : step genesis (.setBudget 0) = genesis := by decide

/-- The budget trichotomy at two instances, and the arithmetic it rests on. -/
theorem nat_sub_saturates : (0 : Nat) - 1 = 0 := by decide

theorem budget_instances :
    (interpStep kernelDesc satNoopWorld (.mark [1] 0)).budget = 0 ∧
    (interpStep { kernelDesc with guardAccept := false, gateBudget := false }
      satNoopWorld (.mark [1] 0)).budget = 0 ∧
    (interpStep { kernelDesc with gateBudget := false } brokeWorld (.mark [] 0)).budget = 0 ∧
    (interpStep kernelDesc satWorld (.mark [0] 1)).budget = 9 ∧
    (interpStep kernelDesc satWorld (.setBudget 4)).budget = 4 := by decide

theorem trichotomy_instance (d : ConstitutionDesc) :
    (interpStep d brokeWorld (.mark [] 0)).budget = 0 := by
  rcases interp_budget_bound d brokeWorld (.mark [] 0) with h | h | ⟨n, hn, _⟩
  · rw [h]; rfl
  · rw [h]; rfl
  · cases hn

/-- With the budget gate off, the relaxed machine still cannot go below
zero: `markApply` is the identity off the view store, so the audit
countermodel is a no-op, while the same descriptor on a present view does act. -/
theorem relaxed_acts_on_present_view :
    interpStep { kernelDesc with guardAccept := false, gateBudget := false }
      satNoopWorld (.mark [0] 1) ≠ satNoopWorld := by decide

end Textbook.U50

#print axioms Textbook.U50.spec_three
#print axioms Textbook.U50.worldAt_three_by_spec
#print axioms Textbook.U50.worldAt_three_by_computation
#print axioms Textbook.U50.block_three_steps
#print axioms Textbook.U50.columns_at_two
#print axioms Textbook.U50.old_cols_blind_instance
#print axioms Textbook.U50.stage_ten_quiescent
#print axioms Textbook.U50.stage_hundred_wf
#print axioms Textbook.U50.gen_hundred_quiescent
#print axioms Textbook.U50.block_three_accepted
#print axioms Textbook.U50.carrier_size
#print axioms Textbook.U50.genesis_first_step
#print axioms Textbook.U50.unguarded_can_be_silent
#print axioms Textbook.U50.nat_sub_saturates
#print axioms Textbook.U50.budget_instances
#print axioms Textbook.U50.trichotomy_instance
#print axioms Textbook.U50.relaxed_acts_on_present_view
#print axioms Horizon.worldAt_spec
#print axioms Horizon.worldAt_quiescent
#print axioms Horizon.worldAt_wf
#print axioms Horizon.block_all_accepted
#print axioms Horizon.genesis_accepted
#print axioms Horizon.gen_quiescent
#print axioms Horizon.gen_wf
#print axioms Horizon.interp_budget_bound
#print axioms Horizon.budget_saturation_noop
#print axioms Horizon.mark_saturation_all_descs
"""

EXPECTED = {
    "Textbook.U50.spec_three": NONE,
    "Textbook.U50.worldAt_three_by_spec": BOTH,
    "Textbook.U50.worldAt_three_by_computation": BOTH,
    "Textbook.U50.block_three_steps": BOTH,
    "Textbook.U50.columns_at_two": BOTH,
    "Textbook.U50.old_cols_blind_instance": BOTH,
    "Textbook.U50.stage_ten_quiescent": BOTH,
    "Textbook.U50.stage_hundred_wf": BOTH,
    "Textbook.U50.gen_hundred_quiescent": BOTH,
    "Textbook.U50.block_three_accepted": BOTH,
    "Textbook.U50.carrier_size": BOTH,
    "Textbook.U50.genesis_first_step": BOTH,
    "Textbook.U50.unguarded_can_be_silent": BOTH,
    "Textbook.U50.nat_sub_saturates": NONE,
    "Textbook.U50.budget_instances": BOTH,
    "Textbook.U50.trichotomy_instance": BOTH,
    "Textbook.U50.relaxed_acts_on_present_view": BOTH,
    "Horizon.worldAt_spec": BOTH,
    "Horizon.worldAt_quiescent": BOTH,
    "Horizon.worldAt_wf": BOTH,
    "Horizon.block_all_accepted": BOTH,
    "Horizon.genesis_accepted": BOTH,
    "Horizon.gen_quiescent": BOTH,
    "Horizon.gen_wf": BOTH,
    "Horizon.interp_budget_bound": BOTH,
    "Horizon.budget_saturation_noop": BOTH,
    "Horizon.mark_saturation_all_descs": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U50"))
