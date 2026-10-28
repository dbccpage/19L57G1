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

end Textbook.U25

#print axioms Textbook.U25.obstruction_under_irrefl'
#print axioms Textbook.U25.D2_merge_obstructed
#print axioms Textbook.U25.D2_merge_bare
#print axioms Textbook.U25.no_obstruction_without_law
#print axioms Textbook.U25.obstruction_iff_collision
#print axioms Textbook.U25.obstruction_without_irrefl_premise
#print axioms Textbook.U25.D2_identity_no_collision
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
    "PrimDiff.obstruction_under_irrefl": NONE,
    "PrimDiff.collision_not_irrefl": NONE,
    "PrimDiff.bare_collapse_admissible": NONE,
    "PrimDiff.collapse_unobstructed_without_fidelity": NONE,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U25"))
