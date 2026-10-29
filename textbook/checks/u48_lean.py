"""Unit 48 check: kernel-check the book's Lean for Unit 48.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u48_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Constitution

namespace Textbook.U48
open Represented Constitution

def story : World :=
  replay [.setBudget 9, .admitTok 10, .admitTok 20, .admitTok 30,
    .require 0 1, .require 0 2, .require 1 2, .addView [0]] genesis

/-- The generated history at stage 2, written out: the seed admission
and two tower blocks, each opened by its own budget event. -/
theorem tower_gen_two :
    towerGen 2 = [.admitTok 0, .setBudget 1, .admitTok 1, .require 0 1, .addView [1],
                  .setBudget 1, .admitTok 2, .require 0 2, .addView [2]] := by decide

/-- The world it replays to: three tokens, two columns, two requirements,
and the budget spent. -/
theorem gen_two_world :
    (genWorld 2).w.data = [0, 1, 2] ∧ (genWorld 2).w.views = [[1], [2]] ∧
    (genWorld 2).w.reqs = [(0, 1), (0, 2)] ∧ (genWorld 2).w.budget = 0 := by decide

/-- Reproduction at stage 5, by the theorem and by evaluation. -/
theorem reproduces_five : towerGen 5 = histUpTo 5 := driver_reproduces_tower 5
theorem reproduces_five_evaluated : towerGen 5 = histUpTo 5 := by decide

/-- The canonical numeral at stage 4 is 5 and is not admitted; the
Genesis theorem says so at every stage of the tower. -/
theorem fresh_instance :
    freshName (genWorld 4).w = 5 ∧ ¬ (freshName (genWorld 4).w ∈ (genWorld 4).w.data) := by
  decide
theorem fresh_on_tower_four : ¬ (freshName (worldAt 4) ∈ (worldAt 4).data) :=
  freshName_fresh_on_tower 4

/-- Off the tower the numeral can collide: a second world beside the
Genesis countermodel. -/
theorem collides_elsewhere :
    freshName { story with data := [0, 1, 3] } = 3 ∧ 3 ∈ ([0, 1, 3] : List Nat) := by decide

/-- The closure family on the pigeonhole story: no repair, both extensions. -/
theorem close_on_story :
    nextFamily ⟨story, .close⟩ = [[.addView [1]], [.addView [2]]] := by decide

/-- Completeness applied: the extension `[2]` of the violated pair is in the family. -/
theorem close_complete_instance : [Event.addView [2]] ∈ closeBlocks story :=
  closeBlocks_complete_aug (r := (1, 2)) (by decide) (by decide) (by decide)

/-- The stop outcome at the quiescent third generated world, and idleness anywhere. -/
theorem stop_instance : nextFamily ⟨(genWorld 3).w, .close⟩ = [] :=
  nextFamily_stop gen_three_quiescent
theorem idle_nothing (w : World) : nextFamily ⟨w, .idle⟩ = [] := rfl

/-- Two rungs of the ladder at concrete stages. -/
theorem ladder_prefix : towerGen 2 <+: towerGen 3 := tower_driver_autonomy.1 2
theorem ladder_growth : (genWorld 2).w.data.length < (genWorld 3).w.data.length :=
  tower_driver_autonomy.2.2.2.2.2 2

/-- The policy is a field no event writes: a base step keeps it, by definition. -/
theorem policy_kept (g : GWorld) (e : Event) :
    (⟨step g.w e, g.pol⟩ : GWorld).pol = g.pol := rfl

/-- Self-description applied to the story, and one relaxation that differs:
with deduplication off, a repeated token is admitted again. -/
theorem describe_instance :
    interpStep kernelDesc story (.addView [1]) = step story (.addView [1]) :=
  interp_describe _ _
theorem relaxed_dedup_differs :
    (interpStep { kernelDesc with dedupAdmit := false } story (.admitTok 10)).data =
      [10, 20, 30, 10] ∧
    (step story (.admitTok 10)).data = [10, 20, 30] := by decide

/-- The kernel's description is one of the 64; so is the all-off one. -/
theorem kernel_in_family : kernelDesc ∈ allDescs := allDescs_complete _
theorem all_off_in_family :
    (⟨false, false, false, false, false, false⟩ : ConstitutionDesc) ∈ allDescs := by decide

/-- Stopping belongs to the close policy; tower still emits its next block. -/
theorem quiescent_policy_difference :
    quiescentB (genWorld 1).w = true ∧
    nextFamily ⟨(genWorld 1).w, .close⟩ = [] ∧
    nextFamily ⟨(genWorld 1).w, .tower⟩ =
      [[.setBudget 1, .admitTok 2, .require 0 2, .addView [2]]] := by decide

/-- The two-singleton menu does not enumerate every structurally accepted column. -/
theorem accepted_outside_close_menu :
    augOkB story [0, 1] = true ∧ [Event.addView [0, 1]] ∉ closeBlocks story := by decide

/-- The candidate menu ignores budget; at zero, both emitted events are blocked. -/
theorem candidates_without_execution :
    let w := { story with budget := 0 }
    closeBlocks w = [[.addView [1]], [.addView [2]]] ∧
    step w (.addView [1]) = w ∧ step w (.addView [2]) = w := by decide

end Textbook.U48

#print axioms Textbook.U48.tower_gen_two
#print axioms Textbook.U48.gen_two_world
#print axioms Textbook.U48.reproduces_five
#print axioms Textbook.U48.reproduces_five_evaluated
#print axioms Textbook.U48.fresh_instance
#print axioms Textbook.U48.fresh_on_tower_four
#print axioms Textbook.U48.collides_elsewhere
#print axioms Textbook.U48.close_on_story
#print axioms Textbook.U48.close_complete_instance
#print axioms Textbook.U48.stop_instance
#print axioms Textbook.U48.idle_nothing
#print axioms Textbook.U48.ladder_prefix
#print axioms Textbook.U48.ladder_growth
#print axioms Textbook.U48.policy_kept
#print axioms Textbook.U48.describe_instance
#print axioms Textbook.U48.relaxed_dedup_differs
#print axioms Textbook.U48.kernel_in_family
#print axioms Textbook.U48.all_off_in_family
#print axioms Textbook.U48.quiescent_policy_difference
#print axioms Textbook.U48.accepted_outside_close_menu
#print axioms Textbook.U48.candidates_without_execution
#print axioms Constitution.closeBlocks_complete_repair
#print axioms Constitution.closeBlocks_complete_aug
#print axioms Constitution.nextFamily_stop
#print axioms Constitution.driver_reproduces_tower
#print axioms Constitution.freshName_fresh_on_tower
#print axioms Constitution.freshName_not_fresh_generally
#print axioms Constitution.gen_three_quiescent
#print axioms Constitution.tower_driver_autonomy
#print axioms Constitution.interp_describe
#print axioms Constitution.allDescs_length
#print axioms Constitution.allDescs_complete
"""

EXPECTED = {
    "Textbook.U48.tower_gen_two": BOTH,
    "Textbook.U48.gen_two_world": BOTH,
    "Textbook.U48.reproduces_five": BOTH,
    "Textbook.U48.reproduces_five_evaluated": BOTH,
    "Textbook.U48.fresh_instance": BOTH,
    "Textbook.U48.fresh_on_tower_four": BOTH,
    "Textbook.U48.collides_elsewhere": BOTH,
    "Textbook.U48.close_on_story": BOTH,
    "Textbook.U48.close_complete_instance": BOTH,
    "Textbook.U48.stop_instance": BOTH,
    "Textbook.U48.idle_nothing": BOTH,
    "Textbook.U48.ladder_prefix": BOTH,
    "Textbook.U48.ladder_growth": BOTH,
    "Textbook.U48.policy_kept": BOTH,
    "Textbook.U48.describe_instance": BOTH,
    "Textbook.U48.relaxed_dedup_differs": BOTH,
    "Textbook.U48.kernel_in_family": PROPEXT,
    "Textbook.U48.all_off_in_family": PROPEXT,
    "Textbook.U48.quiescent_policy_difference": BOTH,
    "Textbook.U48.accepted_outside_close_menu": BOTH,
    "Textbook.U48.candidates_without_execution": BOTH,
    "Constitution.closeBlocks_complete_repair": BOTH,
    "Constitution.closeBlocks_complete_aug": BOTH,
    "Constitution.nextFamily_stop": BOTH,
    "Constitution.driver_reproduces_tower": BOTH,
    "Constitution.freshName_fresh_on_tower": BOTH,
    "Constitution.freshName_not_fresh_generally": BOTH,
    "Constitution.gen_three_quiescent": BOTH,
    "Constitution.tower_driver_autonomy": BOTH,
    "Constitution.interp_describe": BOTH,
    "Constitution.allDescs_length": NONE,
    "Constitution.allDescs_complete": PROPEXT,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U48"))
