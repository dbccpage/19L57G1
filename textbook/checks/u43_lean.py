"""Unit 43 check: kernel-check the book's Lean for Unit 43.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u43_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.G1Class

namespace Textbook.U43
open LocalFiniteAlphabet G1Class CapacityBound SeparationCapacity Generator

/-- `Fires` does not read its strategy: the two propositions are the same term. -/
theorem fires_ignores_strategy : Fires bare = Fires valued := rfl

/-- The inherited obstruction at length 3 is the middle pair. -/
theorem base_obstructed_three : BaseObstructed 3 1 2 :=
  ⟨by omega, by omega, by omega, by decide⟩

/-- Per-pair marking and valued marking are the same colouring and the same view;
only the declared tag differs. -/
theorem perPair_valued_same_functions :
    perPairFreshMark.colour = valued.colour ∧ perPairFreshMark.view = valued.view :=
  ⟨rfl, rfl⟩

theorem perPair_valued_tags_differ :
    perPairFreshMark.importDiscipline ≠ valued.importDiscipline := by
  decide

/-- The third conjunct of the class theorem follows from the second alone. -/
theorem cycle_from_not_clears {d : Nat} (S : LocalStrategy d) (h : ¬ Clears S) :
    ¬ (Fires S ∧ Clears S ∧ ¬ RecurringImport S) :=
  fun c => h c.2.1

/-- The G3 counterexample needs nothing about the valued rule: any clearing member fires. -/
theorem any_clearing_member_fires {d : Nat} (S : LocalStrategy d) (h : Clears S) :
    Clears S ∧ Fires S :=
  ⟨h, fires_every_strategy S⟩

/-- The bare view at length 3: the middle pair shares the code 7. -/
theorem bare_views_three :
    bare.view 3 0 = 4 ∧ bare.view 3 1 = 7 ∧ bare.view 3 2 = 7 ∧ bare.view 3 3 = 3 := by
  decide

/-- Depth-two at length 4 separates the three deep points, and at length 5 merges 2 and 3. -/
theorem depthTwo_views_four :
    depthTwo.view 4 1 = 508 ∧ depthTwo.view 4 2 = 511 ∧ depthTwo.view 4 3 = 255 := by
  decide

theorem depthTwo_fails_at_five : ¬ ClearsOn depthTwo 5 :=
  fun h => h 2 3 ⟨by omega, by omega, by omega, by decide⟩ (by decide)

/-- A book member: two colours, radius 0. Finite, so it does not clear; threshold 4;
it clears length 3 and fails at length 4 on the pair (1, 3). -/
def parity : LocalStrategy 0 := zeroRadiusStrategy .oneTime (fun _ i => i % 2)

theorem parity_finite : FiniteDeclaration 2 parity :=
  fun _ x => Nat.mod_lt x (by decide)

theorem parity_not_clears : ¬ Clears parity :=
  finite_local_not_clears parity 2 parity_finite

theorem parity_threshold : 2 ^ (2 * 0 + 1) + 2 * 0 + 2 = 4 := rfl

theorem parity_collision_four :
    ∃ i j, i ≠ j ∧ 0 < i ∧ i + 0 < 4 ∧ 0 < j ∧ j + 0 < 4 ∧ parity.view 4 i = parity.view 4 j :=
  strategy_capacity_collision parity 2 4 parity_finite (by decide)

theorem parity_fails_at_four : ¬ ClearsOn parity 4 :=
  fun h => h 1 3 ⟨by omega, by omega, by omega, by decide⟩ (by decide)

theorem parity_clears_three : ClearsOn parity 3 := by
  intro i j hij
  rcases hij with ⟨hi, hj, hne, hprofile⟩
  have hint := (depth1_obstructions_are_exactly_middle_pairs 3 i j (by omega) hi hj hne).mp hprofile
  have hi' : i = 1 ∨ i = 2 := by omega
  have hj' : j = 1 ∨ j = 2 := by omega
  rcases hi' with rfl | rfl <;> rcases hj' with rfl | rfl <;> first | contradiction | decide

/-- The Lean class lets the factor `g` depend on the length `n`; this member's view
adds `n` to the colour, so no single factor serves every length. -/
def shifting : LocalStrategy 0 where
  importDiscipline := .oneTime
  colour := fun _ i => i % 2
  view := fun n i => n + i % 2
  locality := fun n => ⟨fun xs => n + xs.headD 0, fun _ => rfl⟩

theorem shifting_finite : FiniteDeclaration 2 shifting :=
  fun _ x => Nat.mod_lt x (by decide)

theorem shifting_not_clears : ¬ Clears shifting :=
  finite_local_not_clears shifting 2 shifting_finite

end Textbook.U43

#print axioms Textbook.U43.fires_ignores_strategy
#print axioms Textbook.U43.base_obstructed_three
#print axioms Textbook.U43.perPair_valued_same_functions
#print axioms Textbook.U43.perPair_valued_tags_differ
#print axioms Textbook.U43.cycle_from_not_clears
#print axioms Textbook.U43.any_clearing_member_fires
#print axioms Textbook.U43.bare_views_three
#print axioms Textbook.U43.depthTwo_views_four
#print axioms Textbook.U43.depthTwo_fails_at_five
#print axioms Textbook.U43.parity_finite
#print axioms Textbook.U43.parity_not_clears
#print axioms Textbook.U43.parity_threshold
#print axioms Textbook.U43.parity_collision_four
#print axioms Textbook.U43.parity_fails_at_four
#print axioms Textbook.U43.parity_clears_three
#print axioms Textbook.U43.shifting_finite
#print axioms Textbook.U43.shifting_not_clears
#print axioms LocalFiniteAlphabet.fires_every_strategy
#print axioms LocalFiniteAlphabet.strategy_capacity_collision
#print axioms LocalFiniteAlphabet.finite_local_not_clears
#print axioms LocalFiniteAlphabet.g1_local_finite_alphabet_class
#print axioms LocalFiniteAlphabet.depthTwo_clears_n4
#print axioms LocalFiniteAlphabet.valued_clears
#print axioms LocalFiniteAlphabet.valued_not_finite
#print axioms G1Class.g1_class_exclusion
#print axioms G1Class.clears_does_not_imply_not_fires
"""

EXPECTED = {
    "Textbook.U43.fires_ignores_strategy": BOTH,
    "Textbook.U43.base_obstructed_three": BOTH,
    "Textbook.U43.perPair_valued_same_functions": PROPEXT,
    "Textbook.U43.perPair_valued_tags_differ": PROPEXT,
    "Textbook.U43.cycle_from_not_clears": BOTH,
    "Textbook.U43.any_clearing_member_fires": BOTH,
    "Textbook.U43.bare_views_three": BOTH,
    "Textbook.U43.depthTwo_views_four": BOTH,
    "Textbook.U43.depthTwo_fails_at_five": BOTH,
    "Textbook.U43.parity_finite": PROPEXT,
    "Textbook.U43.parity_not_clears": BOTH,
    "Textbook.U43.parity_threshold": NONE,
    "Textbook.U43.parity_collision_four": BOTH,
    "Textbook.U43.parity_fails_at_four": BOTH,
    "Textbook.U43.parity_clears_three": BOTH,
    "Textbook.U43.shifting_finite": NONE,
    "Textbook.U43.shifting_not_clears": BOTH,
    "LocalFiniteAlphabet.fires_every_strategy": BOTH,
    "LocalFiniteAlphabet.strategy_capacity_collision": BOTH,
    "LocalFiniteAlphabet.finite_local_not_clears": BOTH,
    "LocalFiniteAlphabet.g1_local_finite_alphabet_class": BOTH,
    "LocalFiniteAlphabet.depthTwo_clears_n4": BOTH,
    "LocalFiniteAlphabet.valued_clears": BOTH,
    "LocalFiniteAlphabet.valued_not_finite": PROPEXT,
    "G1Class.g1_class_exclusion": BOTH,
    "G1Class.clears_does_not_imply_not_fires": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U43"))
