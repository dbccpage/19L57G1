"""Unit 17 check: kernel-check the book's Lean for Unit 17.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u17_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Minimality

namespace Textbook.U17
open Derivation

/-- The two-datum regime before any demand. -/
def R2 : Regime := ⟨2, [], [], [], []⟩

/-- Imposing (0, 1) on it gives exactly the Challenge 3 regime. -/
theorem impose_gives_R2L : stepE R2 (.impose 0 1) = some R2L := by decide

/-- A demand on one datum and itself is rejected by the guard. -/
theorem impose_self_rejected (r : Regime) (d : Nat) :
    stepE r (.impose d d) = none := by
  simp [stepE]

/-- A demand naming a datum not yet admitted is rejected. -/
theorem impose_out_of_range : stepE R2 (.impose 0 2) = none := by decide

/-- A demand written the other way round is rejected: the guard fixes
the order `i < j`. -/
theorem impose_reversed_rejected : stepE R2 (.impose 1 0) = none := by
  decide

/-- The guard, stated as the condition under which an `impose` succeeds. -/
theorem impose_succeeds_iff (r : Regime) (i j : Nat) :
    (∃ s, stepE r (.impose i j) = some s) ↔ (i < j ∧ j < r.data) := by
  constructor
  · intro ⟨s, hs⟩
    simp only [stepE] at hs
    split at hs
    · assumption
    · cases hs
  · intro h
    refine ⟨{ r with reqs := insertNew r.reqs (i, j) }, ?_⟩
    simp [stepE, h]

/-- Every recorded demand is strictly ordered, in every regime a step
reaches from a regime whose demands were. -/
theorem step_keeps_reqs_ordered (r s : Regime) (e : Event)
    (hr : ∀ q ∈ r.reqs, q.1 < q.2) (hs : stepE r e = some s) :
    ∀ q ∈ s.reqs, q.1 < q.2 := by
  cases e with
  | supply t => cases Option.some.inj hs; exact hr
  | admitDatum => cases Option.some.inj hs; exact hr
  | admitForm a =>
      simp only [stepE] at hs
      split at hs
      · cases Option.some.inj hs; exact hr
      · cases hs
  | admitInst f args =>
      simp only [stepE] at hs
      split at hs
      · cases Option.some.inj hs; exact hr
      · cases hs
  | admitRuleAll f =>
      simp only [stepE] at hs
      split at hs
      · cases Option.some.inj hs; exact hr
      · cases hs
  | impose i j =>
      simp only [stepE] at hs
      split at hs
      next hij =>
        cases Option.some.inj hs
        intro q hq
        simp only [insertNew] at hq
        split at hq
        · exact hr q hq
        · cases List.mem_append.mp hq with
          | inl h => exact hr q h
          | inr h =>
              cases List.mem_singleton.mp h
              exact hij.1
      next => cases hs

/-- And so along every replay from a regime with ordered demands; in
particular from genesis, whose demands are none. -/
theorem replay_keeps_reqs_ordered (h : List Event) (r s : Regime)
    (hr : ∀ q ∈ r.reqs, q.1 < q.2) (hs : replayE h r = some s) :
    ∀ q ∈ s.reqs, q.1 < q.2 := by
  induction h generalizing r with
  | nil => cases Option.some.inj hs; exact hr
  | cons e rest ih =>
      simp only [replayE, List.foldlM] at hs
      cases he : stepE r e with
      | none => rw [he] at hs; cases hs
      | some r1 =>
          rw [he] at hs
          exact ih r1 (step_keeps_reqs_ordered r r1 e hr he) hs

/-- The ordering is what `isoRefl` asks for: the identity is an
isomorphism of `R2L` because its one demand is sorted. -/
def R2L_selfIso : Iso R2L R2L :=
  isoRefl R2L (fun q hq => by
    have : q = (0, 1) := by
      cases hq with
      | head => rfl
      | tail _ h => cases h
    rw [this]; decide)

/-- Recording an already present, admissible demand does not add a copy. -/
theorem repeated_demand_unchanged (r : Regime) (i j : Nat)
    (hguard : i < j ∧ j < r.data) (hmem : (i, j) ∈ r.reqs) :
    stepE r (.impose i j) = some r := by
  simp [stepE, hguard, insertNew_of_mem hmem]

/-- A successful event does not clean an arbitrary malformed base. -/
theorem malformed_base_survives :
    stepE ⟨2, [], [], [], [(1, 0)]⟩ (.impose 0 1) =
      some ⟨2, [], [], [], [(1, 0), (0, 1)]⟩ := by decide

theorem self_not_separable (r : Regime) (d : Nat) : ¬ separable r d d :=
  fun ⟨_, _, h⟩ => h ⟨fun hx => hx, fun hx => hx⟩

end Textbook.U17

#print axioms Textbook.U17.impose_gives_R2L
#print axioms Textbook.U17.impose_self_rejected
#print axioms Textbook.U17.impose_out_of_range
#print axioms Textbook.U17.impose_reversed_rejected
#print axioms Textbook.U17.impose_succeeds_iff
#print axioms Textbook.U17.step_keeps_reqs_ordered
#print axioms Textbook.U17.replay_keeps_reqs_ordered
#print axioms Textbook.U17.R2L_selfIso
#print axioms Textbook.U17.repeated_demand_unchanged
#print axioms Textbook.U17.malformed_base_survives
#print axioms Derivation.stepE
#print axioms Derivation.insertNew
#print axioms Textbook.U17.self_not_separable
"""

EXPECTED = {
    "Textbook.U17.impose_gives_R2L": PROPEXT,
    "Textbook.U17.impose_self_rejected": PROPEXT,
    "Textbook.U17.impose_out_of_range": PROPEXT,
    "Textbook.U17.impose_reversed_rejected": PROPEXT,
    "Textbook.U17.impose_succeeds_iff": PROPEXT,
    "Textbook.U17.step_keeps_reqs_ordered": PROPEXT,
    "Textbook.U17.replay_keeps_reqs_ordered": PROPEXT,
    "Textbook.U17.R2L_selfIso": BOTH,
    "Textbook.U17.repeated_demand_unchanged": PROPEXT,
    "Textbook.U17.malformed_base_survives": PROPEXT,
    "Derivation.stepE": PROPEXT,
    "Derivation.insertNew": PROPEXT,
    "Textbook.U17.self_not_separable": PROPEXT,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U17"))
