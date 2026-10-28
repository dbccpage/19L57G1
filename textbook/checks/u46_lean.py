"""Unit 46 check: kernel-check the book's Lean for Unit 46.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u46_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Completion

namespace Textbook.U46
open Represented Completion RefusalFrontier

/-- The pigeonhole story of Unit 45, again. -/
def story : World :=
  replay [.setBudget 9, .admitTok 10, .admitTok 20, .admitTok 30,
    .require 0 1, .require 0 2, .require 1 2, .addView [0]] genesis

/-- Transport: the common-state obstruction is the kernel's violation. -/
theorem transport_instance :
    obstC (ofWorld story) 1 2 = true ∧ obstC (ofWorld story) 0 1 = false ∧
    sepC (ofWorld story) 0 1 = true := by decide

/-- The stated identification: the kernel feeds one store to two fields. -/
theorem same_store (w : World) : (ofWorld w).retained = (ofWorld w).protectedReqs := rfl

/-- The extension family is a filter: both orientations under the violation,
one each where a singleton is already a view. -/
theorem family_instances :
    augFamily story (1, 2) = [[1], [2]] ∧ augFamily story (0, 1) = [[1]] ∧
    augFamily story (0, 2) = [[2]] := by decide

theorem rule1_instance :
    (∃ m, m ∈ repairFamily story (1, 2)) ∨
      (obstructedB story (1, 2) = true ∧
        [1] ∈ augFamily story (1, 2) ∧ [2] ∈ augFamily story (1, 2)) :=
  rule1_repair_or_extension (wf_replay _) (by decide)

/-- The other orientation also discharges the pair. -/
theorem other_orientation_discharges :
    satB (augApply story [2]) (1, 2) = true ∧ quiescentB (step story (.addView [2])) = true := by decide

/-- Refusal, then extension: the record stays and the extension still fires. -/
theorem refusal_then_extension :
    (step (step story (.refuse 1 2)) (.addView [1])).views = [[0], [1]] ∧
    (step (step story (.refuse 1 2)) (.addView [1])).refusals = [(1, 2)] := by decide

theorem refusal_recordable_instance : (1, 2) ∈ (step story (.refuse 1 2)).refusals :=
  refusal_recordable (by decide)

/-- The signature: same-level work keeps it, expressive change grows it. -/
theorem signature_instances :
    sigOf story = (3, 1) ∧ sigOf (step story (.addView [1])) = (3, 2) ∧
    sigOf (step story (.admitTok 40)) = (4, 1) ∧
    sigOf (step truncWorld (.mark [0] 1)) = sigOf truncWorld ∧
    (step truncWorld (.mark [0] 1)).views = [[1, 0]] := by decide

theorem fidelity_instance : obstructedB { story with reqs := [] } (1, 2) = false :=
  (rule1_needs_fidelity _ rfl _).2

def owW : World :=
  { data := [10, 20], views := [[0]], reqs := [(0, 1)], refusals := [], budget := 9,
    augLicensed := true, notes := [] }

/-- A retraction is same-level by the signature and still breaks preservation. -/
theorem retraction_same_signature :
    sigOf (retractFirstMark owW) = sigOf owW ∧ satB (retractFirstMark owW) (0, 1) = false := by decide

/-- A witness is not a separation: give the oriented object one column and
the obstruction goes. -/
theorem d2_with_view :
    obstC d2Common 0 1 = true ∧ obstC { d2Common with views := [[0]] } 0 1 = false := by decide

theorem swap_twice : swapC (swapC d2Common) = d2Common := by decide

/-- What the swap does to the symmetric object: the relation store is the
same set in the other order, the protection store is the other pair. -/
theorem s2_swapped :
    (swapC s2Common).posWitness = [(1, 0), (0, 1)] ∧ (swapC s2Common).retained = [(1, 0)] := by decide

/-- The chain at depth 3 in the common state: its one column, the tags,
separates the root from everything and nothing else. -/
theorem chain_three :
    (ofPState (reflState 3)).carrier = [0, 1, 2, 3] ∧
    (ofPState (reflState 3)).posWitness = [(0, 1), (1, 2), (2, 3)] ∧
    sepC (ofPState (reflState 3)) 0 1 = true ∧
    zeroC (ofPState (reflState 3)) 1 2 = true := by decide

theorem meta_inert_instance :
    obstC { d2Common with metaDistinct := [] } 0 1 = obstC d2Common 0 1 :=
  (meta_distinctness_inert d2Common [] 0 1).2

end Textbook.U46

#print axioms Textbook.U46.transport_instance
#print axioms Textbook.U46.same_store
#print axioms Textbook.U46.family_instances
#print axioms Textbook.U46.rule1_instance
#print axioms Textbook.U46.other_orientation_discharges
#print axioms Textbook.U46.refusal_then_extension
#print axioms Textbook.U46.refusal_recordable_instance
#print axioms Textbook.U46.signature_instances
#print axioms Textbook.U46.fidelity_instance
#print axioms Textbook.U46.retraction_same_signature
#print axioms Textbook.U46.d2_with_view
#print axioms Textbook.U46.swap_twice
#print axioms Textbook.U46.s2_swapped
#print axioms Textbook.U46.chain_three
#print axioms Textbook.U46.meta_inert_instance
#print axioms Completion.ofWorld_obstruction
#print axioms Completion.obstC_conditions_independent
#print axioms Completion.chain_transport
#print axioms Completion.d2_transport_oriented
#print axioms Completion.s2_state_not_swap_invariant
#print axioms Completion.witness_not_separation
#print axioms Completion.separation_not_witness
#print axioms Completion.meta_distinctness_inert
#print axioms Completion.augFamily_retains_ties
#print axioms Completion.rule1_repair_or_extension
#print axioms Completion.refusal_recordable
#print axioms Completion.refusal_object_inert
#print axioms Completion.refusal_non_absorbing
#print axioms Completion.action_dichotomy
#print axioms Completion.rule1_needs_fidelity
#print axioms Completion.retraction_breaks_preservation
"""

EXPECTED = {
    "Textbook.U46.transport_instance": BOTH,
    "Textbook.U46.same_store": NONE,
    "Textbook.U46.family_instances": BOTH,
    "Textbook.U46.rule1_instance": BOTH,
    "Textbook.U46.other_orientation_discharges": BOTH,
    "Textbook.U46.refusal_then_extension": BOTH,
    "Textbook.U46.refusal_recordable_instance": BOTH,
    "Textbook.U46.signature_instances": BOTH,
    "Textbook.U46.fidelity_instance": BOTH,
    "Textbook.U46.retraction_same_signature": BOTH,
    "Textbook.U46.d2_with_view": BOTH,
    "Textbook.U46.swap_twice": NONE,
    "Textbook.U46.s2_swapped": NONE,
    "Textbook.U46.chain_three": BOTH,
    "Textbook.U46.meta_inert_instance": BOTH,
    "Completion.ofWorld_obstruction": BOTH,
    "Completion.obstC_conditions_independent": BOTH,
    "Completion.chain_transport": PROPEXT,
    "Completion.d2_transport_oriented": NONE,
    "Completion.s2_state_not_swap_invariant": NONE,
    "Completion.witness_not_separation": BOTH,
    "Completion.separation_not_witness": BOTH,
    "Completion.meta_distinctness_inert": BOTH,
    "Completion.augFamily_retains_ties": BOTH,
    "Completion.rule1_repair_or_extension": BOTH,
    "Completion.refusal_recordable": BOTH,
    "Completion.refusal_object_inert": BOTH,
    "Completion.refusal_non_absorbing": BOTH,
    "Completion.action_dichotomy": BOTH,
    "Completion.rule1_needs_fidelity": BOTH,
    "Completion.retraction_breaks_preservation": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U46"))
