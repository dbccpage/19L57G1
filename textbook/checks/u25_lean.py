"""Unit 25 check: kernel-check the book's Lean for Unit 25.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u25_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.PrimDiff

namespace Textbook.U25
open PrimDiff

/-- The theorem, re-proved with every step named. -/
theorem obstruction_under_irrefl' {α β : Type} {r : α → α → Prop}
    {a b : α} (h : r a b) {c : α → β} (hc : c a = c b) :
    FidelityObstruction Irrefl r c := by
  -- An obstruction is a collision together with the law failing downstream.
  constructor
  · -- the collision: the witnessed pair (a, b) is identified by c
    exact ⟨a, b, h, hc⟩
  · -- the law fails: the pushed relation has the self-pair at c a
    intro hi
    exact hi (c a) ⟨a, b, h, rfl, hc.symm⟩

/-- The merge of the two points of `D2` is obstructed under irreflexivity. -/
theorem D2_merge_obstructed :
    FidelityObstruction Irrefl D2 (fun _ : Bool => ()) :=
  obstruction_under_irrefl D2_witness rfl

/-- The same merge, with no law protected, is not an obstruction: the
pushforward exists and is a bare structure. -/
theorem D2_merge_bare : CollapseCollision D2 (fun _ : Bool => ()) ∧
    Push D2 (fun _ : Bool => ()) () () :=
  bare_collapse_admissible D2_witness rfl

/-- Relative to the trivial law nothing is ever obstructed. -/
theorem no_obstruction_without_law {α β : Type} (r : α → α → Prop)
    (c : α → β) : ¬ FidelityObstruction (fun _ => True) r c :=
  fun h => h.2 trivial

/-- Under irreflexivity, obstruction and collision coincide. -/
theorem obstruction_iff_collision {α β : Type} (r : α → α → Prop)
    (c : α → β) : FidelityObstruction Irrefl r c ↔ CollapseCollision r c :=
  ⟨fun h => h.1, fun h => ⟨h, collision_not_irrefl h⟩⟩

/-- The theorem has no irreflexivity premise on `r`: it applies to the
self-difference on `Unit` with the identity map. The only conditionality
is the protected law in the conclusion. -/
theorem obstruction_without_irrefl_premise :
    FidelityObstruction Irrefl (fun (_ : Unit) _ => True) id :=
  obstruction_under_irrefl (a := ()) (b := ()) trivial rfl

/-- A non-identifying map on `D2` does not collide: the identity. -/
theorem D2_identity_no_collision : ¬ CollapseCollision D2 id := by
  intro ⟨u, v, huv, hc⟩
  exact D2_irrefl u (by cases hc; exact huv)

/-- An additional property used to test the scope of FidelityObstruction. -/
def TransitiveHere {α : Type} (r : α → α → Prop) : Prop :=
  ∀ x y z, r x y → r y z → r x z

/-- Two disjoint arrows: 0 to 1 and 2 to 3. -/
def disjointArrows (x y : Fin 4) : Prop :=
  (x = 0 ∧ y = 1) ∨ (x = 2 ∧ y = 3)

/-- Identify the end of the first arrow with the start of the second. -/
def joinMiddle (x : Fin 4) : Fin 4 := if x = 2 then 1 else x

theorem disjoint_transitive : TransitiveHere disjointArrows := by
  intro x y z hxy hyz
  rcases hxy with h | h <;> rcases hyz with k | k
  all_goals
    have he := congrArg Fin.val (h.2.symm.trans k.1)
    cases he

theorem joined_not_transitive :
    ¬ TransitiveHere (Push disjointArrows joinMiddle) := by
  intro ht
  have e01 : Push disjointArrows joinMiddle 0 1 :=
    ⟨0, 1, Or.inl ⟨rfl, rfl⟩, by decide, by decide⟩
  have e13 : Push disjointArrows joinMiddle 1 3 :=
    ⟨2, 3, Or.inr ⟨rfl, rfl⟩, by decide, by decide⟩
  obtain ⟨u, v, hrel, hu, hv⟩ := ht 0 1 3 e01 e13
  cases hrel with
  | inl h =>
      rw [h.2] at hv
      exact (by decide : joinMiddle 1 ≠ (3 : Fin 4)) hv
  | inr h =>
      rw [h.1] at hu
      exact (by decide : joinMiddle 2 ≠ (0 : Fin 4)) hu

theorem join_no_collision : ¬ CollapseCollision disjointArrows joinMiddle := by
  intro ⟨u, v, hrel, hc⟩
  cases hrel with
  | inl h =>
      rw [h.1, h.2] at hc
      exact (by decide : joinMiddle (0 : Fin 4) ≠ joinMiddle 1) hc
  | inr h =>
      rw [h.1, h.2] at hc
      exact (by decide : joinMiddle (2 : Fin 4) ≠ joinMiddle 3) hc

theorem transitivity_loss_not_fidelity_obstruction :
    ¬ FidelityObstruction TransitiveHere disjointArrows joinMiddle :=
  fun h => join_no_collision h.1

end Textbook.U25

#print axioms Textbook.U25.obstruction_under_irrefl'
#print axioms Textbook.U25.D2_merge_obstructed
#print axioms Textbook.U25.D2_merge_bare
#print axioms Textbook.U25.no_obstruction_without_law
#print axioms Textbook.U25.obstruction_iff_collision
#print axioms Textbook.U25.obstruction_without_irrefl_premise
#print axioms Textbook.U25.D2_identity_no_collision
#print axioms Textbook.U25.disjoint_transitive
#print axioms Textbook.U25.joined_not_transitive
#print axioms Textbook.U25.join_no_collision
#print axioms Textbook.U25.transitivity_loss_not_fidelity_obstruction
#print axioms PrimDiff.obstruction_under_irrefl
#print axioms PrimDiff.collision_not_irrefl
#print axioms PrimDiff.bare_collapse_admissible
#print axioms PrimDiff.collapse_unobstructed_without_fidelity
"""

EXPECTED = {
    "Textbook.U25.obstruction_under_irrefl'": NONE,
    "Textbook.U25.D2_merge_obstructed": NONE,
    "Textbook.U25.D2_merge_bare": NONE,
    "Textbook.U25.no_obstruction_without_law": NONE,
    "Textbook.U25.obstruction_iff_collision": NONE,
    "Textbook.U25.obstruction_without_irrefl_premise": NONE,
    "Textbook.U25.D2_identity_no_collision": NONE,
    "Textbook.U25.disjoint_transitive": PROPEXT,
    "Textbook.U25.joined_not_transitive": PROPEXT,
    "Textbook.U25.join_no_collision": PROPEXT,
    "Textbook.U25.transitivity_loss_not_fidelity_obstruction": PROPEXT,
    "PrimDiff.obstruction_under_irrefl": NONE,
    "PrimDiff.collision_not_irrefl": NONE,
    "PrimDiff.bare_collapse_admissible": NONE,
    "PrimDiff.collapse_unobstructed_without_fidelity": NONE,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U25"))
