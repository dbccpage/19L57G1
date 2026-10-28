"""Unit 44 check: kernel-check the book's Lean for Unit 44.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u44_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.DiffInterface

namespace Textbook.U44
open DiffInterface

/-- A kernel observer is zero exactly on equal views: horizon 2 cannot tell 2 from 5. -/
theorem kernel_zero_instance : ZeroRel (kernelObs (cview 2)) 2 5 := by
  show min 2 2 = min 5 2
  decide

theorem kernel_apart_instance : ¬ ZeroRel (kernelObs (cview 2)) 1 5 := by
  show ¬ (min 1 2 = min 5 2)
  decide

/-- The quotient identifies the zero pair; `Quot.sound` enters here and only here. -/
theorem quotient_instance :
    ObsQuotient.mk (kernelObs (cview 0)) 0 = ObsQuotient.mk (kernelObs (cview 0)) 1 :=
  obsQuotient_eq_of_zero _ (by show min 0 0 = min 1 0; decide)

/-- The three conjuncts, spelled out on the smallest stale stage. -/
theorem active_instance : ActiveObstruction (mkStage 2 0) 0 1 :=
  ⟨⟨by omega, by omega⟩, by show min 0 0 = min 1 0; decide, by omega, by omega, by omega⟩

/-- The same pair in Genesis's unguarded countermodel stage: the `¬ Active` conjunct of
`cm_freshness` is the removal of protection, nothing about the point. -/
theorem fresh_unguarded_vs_guarded :
    ¬ ActiveObstruction freshUnguarded 0 1 ∧ ActiveObstruction (mkStage 2 0) 0 1 :=
  ⟨cm_freshness.2.2, active_instance⟩

/-- Protect the tagging stage and the tagged pair is active. -/
def tagGuarded : Stage Nat (Bool × Bool) :=
  { tagStage with guarded := fun i j => i < 3 ∧ j < 3 ∧ i ≠ j }

theorem tagging_active_when_protected : ActiveObstruction tagGuarded 1 2 :=
  ⟨⟨by omega, by omega⟩, by show tagView 1 = tagView 2; decide, by omega, by omega, by omega⟩

/-- The measure, computed: closed stages are 0; the stale stage (n+2, n) is 2 for every n
shown; a stage two horizons stale has more. -/
theorem measure_values :
    measureC 3 2 = 0 ∧ measureC 3 1 = 2 ∧ measureC 4 2 = 2 ∧ measureC 4 1 = 6 ∧
    activePairs 4 2 = [(2, 3), (3, 2)] := by
  decide

/-- The top swap exchanges `n` and `n + 1`, fixes the rest of the live region, and is
not view-preserving outside it. -/
theorem swapTop_values : swapTop 3 3 = 4 ∧ swapTop 3 4 = 3 ∧ swapTop 3 1 = 1 := by decide

theorem swapTop_off_live : cview 3 (swapTop 3 7) ≠ cview 3 7 := by decide

/-- The demand list at index 3, and the discharge of one demanded pair by the closure step. -/
theorem demand_three : towerDemandList 3 = [(3, 4), (4, 3)] := rfl

theorem closure_kills_instance : ¬ ActiveObstruction (towerClosure 2).apply 2 3 :=
  closure_kills_demanded (towerClosure 2) 2 3 (Or.inl ⟨rfl, rfl⟩)

/-- The concrete driver takes exactly one step: fuel 2 closes, fuel 1 starves. -/
theorem drive_two_closes : drive towerNext 2 (5, 3) = .closed (5, 4) := rfl

theorem drive_one_starves : drive towerNext 1 (5, 3) = .outOfFuel (5, 4) := rfl

/-- A three-valued view closes three points: the Boolean grammar is what forces the
obstruction, not the three points. -/
theorem three_values_close :
    ∀ x y : Nat, x ≠ y → ¬ ZeroRel (kernelObs (fun i : Nat => i)) x y :=
  fun _ _ h hz => h hz

/-- One Boolean view, its surviving pair, by the Genesis theorem and by evaluation. -/
theorem bool_instance : ActiveObstruction (bStage (fun i => decide (i = 0))) 1 2 :=
  ⟨⟨by omega, by omega⟩, by show decide (1 = 0) = decide (2 = 0); decide, by omega, by omega, by omega⟩

end Textbook.U44

#print axioms Textbook.U44.kernel_zero_instance
#print axioms Textbook.U44.kernel_apart_instance
#print axioms Textbook.U44.quotient_instance
#print axioms Textbook.U44.active_instance
#print axioms Textbook.U44.fresh_unguarded_vs_guarded
#print axioms Textbook.U44.tagging_active_when_protected
#print axioms Textbook.U44.measure_values
#print axioms Textbook.U44.swapTop_values
#print axioms Textbook.U44.swapTop_off_live
#print axioms Textbook.U44.demand_three
#print axioms Textbook.U44.closure_kills_instance
#print axioms Textbook.U44.drive_two_closes
#print axioms Textbook.U44.drive_one_starves
#print axioms Textbook.U44.three_values_close
#print axioms Textbook.U44.bool_instance
#print axioms DiffInterface.zeroRel_equivalence
#print axioms DiffInterface.bare_reflection_certifies_active_obstruction
#print axioms DiffInterface.closure_kills_demanded
#print axioms DiffInterface.closure_adds_no_obstruction
#print axioms DiffInterface.drive_terminates
#print axioms DiffInterface.tower_obstruction
#print axioms DiffInterface.tower_step_composes
#print axioms DiffInterface.closed_measure_zero
#print axioms DiffInterface.tower_fuel_terminates
#print axioms DiffInterface.bool_grammar_obstruction
#print axioms DiffInterface.cm_freshness
"""

EXPECTED = {
    "Textbook.U44.kernel_zero_instance": NONE,
    "Textbook.U44.kernel_apart_instance": NONE,
    "Textbook.U44.quotient_instance": QUOT,
    "Textbook.U44.active_instance": BOTH,
    "Textbook.U44.fresh_unguarded_vs_guarded": BOTH,
    "Textbook.U44.tagging_active_when_protected": BOTH,
    "Textbook.U44.measure_values": NONE,
    "Textbook.U44.swapTop_values": NONE,
    "Textbook.U44.swapTop_off_live": NONE,
    "Textbook.U44.demand_three": NONE,
    "Textbook.U44.closure_kills_instance": BOTH,
    "Textbook.U44.drive_two_closes": NONE,
    "Textbook.U44.drive_one_starves": NONE,
    "Textbook.U44.three_values_close": NONE,
    "Textbook.U44.bool_instance": BOTH,
    "DiffInterface.zeroRel_equivalence": NONE,
    "DiffInterface.bare_reflection_certifies_active_obstruction": NONE,
    "DiffInterface.closure_kills_demanded": NONE,
    "DiffInterface.closure_adds_no_obstruction": NONE,
    "DiffInterface.drive_terminates": BOTH,
    "DiffInterface.tower_obstruction": BOTH,
    "DiffInterface.tower_step_composes": BOTH,
    "DiffInterface.closed_measure_zero": BOTH,
    "DiffInterface.tower_fuel_terminates": BOTH,
    "DiffInterface.bool_grammar_obstruction": BOTH,
    "DiffInterface.cm_freshness": NONE,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U44"))
