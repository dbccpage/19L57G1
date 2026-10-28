"""Unit 45 check: kernel-check the book's Lean for Unit 45.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u45_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Represented

namespace Textbook.U45
open Represented

/-- The pigeonhole story of the paper, replayed from genesis. -/
def story : World :=
  replay [.setBudget 9, .admitTok 10, .admitTok 20, .admitTok 30,
    .require 0 1, .require 0 2, .require 1 2, .addView [0]] genesis

theorem story_values :
    story.data = [10, 20, 30] ∧ story.views = [[0]] ∧
    story.reqs = [(0, 1), (0, 2), (1, 2)] ∧ story.budget = 8 ∧
    violB story (1, 2) = true ∧ repairFamily story (1, 2) = [] ∧
    obstructedB story (1, 2) = true ∧ augOkB story [1] = true ∧
    quiescentB (step story (.addView [1])) = true := by decide

/-- The progress theorem applied: `WF` is discharged by `wf_replay`. -/
theorem story_progress_instance :
    (∃ m, m ∈ repairFamily story (1, 2)) ∨
      (obstructedB story (1, 2) = true ∧ augOkB story [1] = true ∧
        satB (augApply story [1]) (1, 2) = true) :=
  represented_progress (wf_replay _) (by decide)

/-- Which branch it is: the family is empty, so the right one. -/
theorem story_right_branch :
    obstructedB story (1, 2) = true ∧ augOkB story [1] = true ∧
      satB (augApply story [1]) (1, 2) = true := by decide

/-- The gates, and that one of them is replenished by an unguarded event. -/
theorem budget_gate_instance :
    step { story with budget := 0 } (.addView [1]) = { story with budget := 0 } := by decide

theorem budget_replenished_unguarded (w : World) (n : Nat) :
    (step w (.setBudget n)).budget = n := rfl

theorem license_gate_instance :
    step { story with augLicensed := false } (.addView [1]) =
      { story with augLicensed := false } :=
  progress_needs_license _ _ rfl

/-- Refusal needs the certificate: `(1, 2)` is obstructed, `(0, 1)` is satisfied. -/
theorem refuse_instance :
    (step story (.refuse 1 2)).refusals = [(1, 2)] ∧
      step story (.refuse 0 1) = story := by decide

/-- `notes_inert` in general, from `support_determines`. -/
theorem notes_inert_general (w : World) (n : List Nat) (e : Event) :
    supp (step { w with notes := n } e) = supp (step w e) :=
  support_determines { w with notes := n } w rfl e

/-- The kernel does not split the two worlds the head-picking semantics splits. -/
theorem kernel_ignores_order :
    satB (step headWorldA (.mark [] 1)) (0, 1) =
      satB (step headWorldB (.mark [] 1)) (0, 1) := by decide

theorem kernel_ignores_order_general :
    SameElems (repairFamily headWorldA (0, 1)) (repairFamily headWorldB (0, 1)) :=
  equiv_repairFamily order_sensitivity_splits_equivalents.1 (0, 1)

/-- The repairs the truncated search missed. -/
theorem trunc_family : repairFamily truncWorld (1, 2) = [([0], 1), ([0], 2)] := by decide

theorem repetition_data :
    (replay [.admitTok 5, .admitTok 5, .admitTok 5] genesis).data = [5] := by decide

/-- A violation appears only through `require`: after the augmentation
every recorded pair is satisfied, and a fresh pair nothing separates
breaks quiescence. -/
theorem require_makes_violation :
    quiescentB (step story (.addView [1])) = true ∧
    quiescentB (step (step story (.addView [1])) (.admitTok 40)) = true ∧
    quiescentB (step (step (step story (.addView [1])) (.admitTok 40)) (.require 2 3)) = false := by
  decide

theorem wit_instances : witValid [3, 3, 3] = true ∧ witValid [0] = false := by decide

theorem wit_identity_fails : witValid (prefixList (fun n => n) 1) = false :=
  wit_no_infinite (fun n => n)

/-- Panels: one evaluator certifies; adding a blind one breaks it; giving
that one the column restores it; the empty panel certifies nothing. -/
theorem panel_instances :
    certPosB [[[0]]] 0 1 = true ∧ certPosB [[[0]], [[0, 1]]] 0 1 = false ∧
    certPosB [[[0]], [[0], [0, 1]]] 0 1 = true ∧ certPosB [] 0 1 = false := by decide

theorem worldAt_two :
    (worldAt 2).data = [0, 1, 2] ∧ (worldAt 2).views = [[1], [2]] ∧
    (worldAt 2).reqs = [(0, 1), (0, 2)] ∧ quiescentB (worldAt 2) = true := by decide

end Textbook.U45

#print axioms Textbook.U45.story_values
#print axioms Textbook.U45.story_progress_instance
#print axioms Textbook.U45.story_right_branch
#print axioms Textbook.U45.budget_gate_instance
#print axioms Textbook.U45.budget_replenished_unguarded
#print axioms Textbook.U45.license_gate_instance
#print axioms Textbook.U45.refuse_instance
#print axioms Textbook.U45.notes_inert_general
#print axioms Textbook.U45.kernel_ignores_order
#print axioms Textbook.U45.kernel_ignores_order_general
#print axioms Textbook.U45.trunc_family
#print axioms Textbook.U45.repetition_data
#print axioms Textbook.U45.require_makes_violation
#print axioms Textbook.U45.wit_instances
#print axioms Textbook.U45.wit_identity_fails
#print axioms Textbook.U45.panel_instances
#print axioms Textbook.U45.worldAt_two
#print axioms Represented.support_determines
#print axioms Represented.repairFamily_retains_ties
#print axioms Represented.equiv_replay
#print axioms Represented.step_mark_sound
#print axioms Represented.aug_increases
#print axioms Represented.wf_replay
#print axioms Represented.represented_progress
#print axioms Represented.progress_needs_budget
#print axioms Represented.violation_only_from_require
#print axioms Represented.quiescent_stable
#print axioms Represented.productive_run
#print axioms Represented.wit_no_infinite
#print axioms Represented.cert_scope
#print axioms Represented.cert_not_correspondence
#print axioms Represented.incomplete_search_false_alarm
#print axioms Represented.order_sensitivity_splits_equivalents
#print axioms Represented.refusal_needs_certificate
"""

EXPECTED = {
    "Textbook.U45.story_values": BOTH,
    "Textbook.U45.story_progress_instance": BOTH,
    "Textbook.U45.story_right_branch": BOTH,
    "Textbook.U45.budget_gate_instance": BOTH,
    "Textbook.U45.budget_replenished_unguarded": BOTH,
    "Textbook.U45.license_gate_instance": BOTH,
    "Textbook.U45.refuse_instance": BOTH,
    "Textbook.U45.notes_inert_general": BOTH,
    "Textbook.U45.kernel_ignores_order": BOTH,
    "Textbook.U45.kernel_ignores_order_general": BOTH,
    "Textbook.U45.trunc_family": BOTH,
    "Textbook.U45.repetition_data": BOTH,
    "Textbook.U45.require_makes_violation": BOTH,
    "Textbook.U45.wit_instances": NONE,
    "Textbook.U45.wit_identity_fails": BOTH,
    "Textbook.U45.panel_instances": BOTH,
    "Textbook.U45.worldAt_two": BOTH,
    "Represented.support_determines": BOTH,
    "Represented.repairFamily_retains_ties": BOTH,
    "Represented.equiv_replay": BOTH,
    "Represented.step_mark_sound": BOTH,
    "Represented.aug_increases": BOTH,
    "Represented.wf_replay": BOTH,
    "Represented.represented_progress": BOTH,
    "Represented.progress_needs_budget": BOTH,
    "Represented.violation_only_from_require": BOTH,
    "Represented.quiescent_stable": BOTH,
    "Represented.productive_run": BOTH,
    "Represented.wit_no_infinite": BOTH,
    "Represented.cert_scope": BOTH,
    "Represented.cert_not_correspondence": BOTH,
    "Represented.incomplete_search_false_alarm": BOTH,
    "Represented.order_sensitivity_splits_equivalents": BOTH,
    "Represented.refusal_needs_certificate": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U45"))
