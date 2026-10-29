"""Unit 39 check: kernel-check the book's Lean for Unit 39.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u39_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.RefusalFrontier

namespace Textbook.U39
open RefusalFrontier Refusal Derivation

/-- T1 at a concrete history: two repeats and a marker leave the state fixed. -/
theorem silent_inert_here :
    [REvent.admitTok 0, .marker 3, .admitTok 0].foldl (stepR .silent) ⟨[0], [], 0⟩ = ⟨[0], [], 0⟩ :=
  silent_repetition_inert _ _ (by
    intro e he tok htok
    subst htok
    simp at he
    simp [he])

/-- T2: the traced runner reports a new admission, then an existing one. -/
theorem traced_results :
    (stepTraced emptyR (.admitTok 0)).1 = .isNew ∧
    (stepTraced (stepTraced emptyR (.admitTok 0)).2 (.admitTok 0)).1 = .existing := by
  decide

/-- Three presentations erase to the same state as one. -/
theorem histories_collapse_three :
    replayR .silent [.admitTok 0, .admitTok 0, .admitTok 0] = replayR .silent [.admitTok 0] := by
  decide

/-- T4: the judgment variant after three presentations, by the horizon-free bound. -/
theorem judgment_bound_three :
    (([0, 0, 0] : List Nat).foldl stepJ ⟨[], []⟩).data = [] ∨
    (([0, 0, 0] : List Nat).foldl stepJ ⟨[], []⟩).data = [0] :=
  judgment_carrier_bound _ _ (Or.inl rfl) (by intro t ht; simp at ht; omega)

/-- T5: the two closing states, written out. -/
theorem bridge_state_value : bridgeState = ⟨[0, 0], [1], [(0, 1)]⟩ := by decide
theorem min_state_value : minState = ⟨[.tok 0, .receipt 1], [(0, 1)]⟩ := by decide

/-- A third presentation under the minimum route adds a second receipt
linked to the subject: a star from index 0, not a chain. -/
theorem min_third_presentation :
    stepM minState 0 = ⟨[.tok 0, .receipt 1, .receipt 2], [(0, 1), (0, 2)]⟩ := by
  decide

/-- Under reflection the second link runs from receipt to receipt: a chain. -/
theorem refl_two : reflState 2 = ⟨[0, 1, 2], [1, 2], [(0, 1), (1, 2)]⟩ := by decide

/-- The protocol-level swap is an involution on the bridge state. -/
theorem swapP_twice_bridge : swapP (swapP bridgeState) = bridgeState := by decide

/-- T6 with a witness that is not constantly true: the bridge facts plus
one self-edge at 0 extend the facts and break the law, and still deny (1, 0). -/
def bridgePlusLoop : Nat → Nat → Prop :=
  fun x y => (x, y) ∈ bridgeState.rel ∨ (x = 0 ∧ y = 0)

theorem bridge_plus_loop_extends :
    (∀ x y, (x, y) ∈ bridgeState.rel → bridgePlusLoop x y) ∧
    ¬ PrimDiff.Irrefl bridgePlusLoop ∧ ¬ bridgePlusLoop 1 0 := by
  refine ⟨fun x y h => Or.inl h, fun hi => hi 0 (Or.inr ⟨rfl, rfl⟩), ?_⟩
  intro h
  rcases h with h | h
  · rw [bridge_state_value] at h
    simp at h
  · exact absurd h.1 (by decide)

/-- T7 on `Bool` with the swap: the ceiling has no fixed point to speak about,
so it constrains nothing there. -/
theorem not_has_no_fixed_point : ∀ b : Bool, (!b) ≠ b := by decide

theorem ceiling_on_bool (F : Bool → Bool) (h : ∀ s, F (!s) = !(F s)) :
    ∀ s, (!s) = s → (!(F s)) = F s :=
  equivariant_output_invariant (fun s => !s) (fun r => !r) F h

/-- T8: the chain's facts at depth 3 and the untyped fixpoint, concretely. -/
theorem chain_three_facts :
    (reflState 3).data = [0, 1, 2, 3] ∧ (reflState 3).rel = [(0, 1), (1, 2), (2, 3)] :=
  ⟨reflective_chain_is_initial_segment 3, reflective_chain_successor_relation 3⟩

theorem untyped_from_false : stepU (stepU false) = stepU false := untyped_reflect_fixpoint false

/-- Receipt payloads are retained in the literal MItem representation.
Forgetting them is a separate observation, not record equality. -/
theorem receipt_payloads_retained :
    MItem.receipt 1 ≠ MItem.receipt 2 ∧
    ([MItem.tok 0, .receipt 1, .receipt 2] : List MItem) ≠
      [.tok 0, .receipt 2, .receipt 1] := by decide

end Textbook.U39

#print axioms Textbook.U39.silent_inert_here
#print axioms Textbook.U39.traced_results
#print axioms Textbook.U39.histories_collapse_three
#print axioms Textbook.U39.judgment_bound_three
#print axioms Textbook.U39.bridge_state_value
#print axioms Textbook.U39.min_state_value
#print axioms Textbook.U39.min_third_presentation
#print axioms Textbook.U39.refl_two
#print axioms Textbook.U39.swapP_twice_bridge
#print axioms Textbook.U39.bridge_plus_loop_extends
#print axioms Textbook.U39.not_has_no_fixed_point
#print axioms Textbook.U39.ceiling_on_bool
#print axioms Textbook.U39.chain_three_facts
#print axioms Textbook.U39.untyped_from_false
#print axioms Textbook.U39.receipt_payloads_retained
#print axioms RefusalFrontier.silent_repetition_inert
#print axioms RefusalFrontier.trace_erasure
#print axioms RefusalFrontier.judgment_carrier_bound
#print axioms RefusalFrontier.priced_bridge_closes
#print axioms RefusalFrontier.min_witnessed_route_closes
#print axioms RefusalFrontier.equivariant_output_invariant
#print axioms RefusalFrontier.reflective_chain_is_initial_segment
"""

EXPECTED = {
    "Textbook.U39.silent_inert_here": BOTH,
    "Textbook.U39.traced_results": BOTH,
    "Textbook.U39.histories_collapse_three": BOTH,
    "Textbook.U39.judgment_bound_three": BOTH,
    "Textbook.U39.bridge_state_value": BOTH,
    "Textbook.U39.min_state_value": PROPEXT,
    "Textbook.U39.min_third_presentation": PROPEXT,
    "Textbook.U39.refl_two": NONE,
    "Textbook.U39.swapP_twice_bridge": BOTH,
    "Textbook.U39.bridge_plus_loop_extends": BOTH,
    "Textbook.U39.not_has_no_fixed_point": NONE,
    "Textbook.U39.ceiling_on_bool": NONE,
    "Textbook.U39.chain_three_facts": PROPEXT,
    "Textbook.U39.untyped_from_false": NONE,
    "Textbook.U39.receipt_payloads_retained": NONE,
    "RefusalFrontier.silent_repetition_inert": BOTH,
    "RefusalFrontier.trace_erasure": BOTH,
    "RefusalFrontier.judgment_carrier_bound": BOTH,
    "RefusalFrontier.priced_bridge_closes": BOTH,
    "RefusalFrontier.min_witnessed_route_closes": PROPEXT,
    "RefusalFrontier.equivariant_output_invariant": NONE,
    "RefusalFrontier.reflective_chain_is_initial_segment": PROPEXT,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U39"))
