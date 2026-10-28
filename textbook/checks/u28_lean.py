"""Unit 28 check: kernel-check the book's Lean for Unit 28.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u28_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Counting

namespace Textbook.U28
open Derivation

/-- The pair language of four data, computed. -/
theorem allPairs_four :
    allPairs 4 = [(0, 1), (0, 2), (1, 2), (0, 3), (1, 3), (2, 3)] := by
  decide

theorem allPairs_four_length : (allPairs 4).length = 6 := by decide

/-- Genesis's law at n = 4: 2 * 6 = 4 * 3. -/
theorem allPairs_four_law : 2 * (allPairs 4).length = 4 * 3 := allPairs_length 4

/-- The identity is a strictly increasing measure. -/
theorem id_strict (L : Nat) :
    ∀ i, i + 1 < L → (fun k : Nat => k) i < (fun k : Nat => k) (i + 1) :=
  fun i _ => Nat.lt_succ_self i

/-- A run measured by the identity and capped at 3 has at most 4 states. -/
theorem run_capped_at_three (L : Nat) (hb : ∀ i, i < L → (fun k : Nat => k) i ≤ 3) :
    L ≤ 4 :=
  strict_bounded_length (fun k => k) L 3 (id_strict L) hb

/-- The three-datum instance of the conditional law: bound 3 * 2 / 2 = 3,
so at most 4 states. -/
theorem three_data_bound (f : Nat → Nat) (L : Nat)
    (hs : ∀ i, i + 1 < L → f i < f (i + 1))
    (hb : ∀ i, i < L → f i ≤ 3) : L ≤ 4 :=
  no_supply_round_bound f L 3 hs hb

/-- Strict growth is load-bearing: a constant measure is bounded by 0 along
a run of length 2, and 2 is not at most 0 + 1. -/
theorem no_bound_without_growth :
    ¬ (∀ (f : Nat → Nat) (L B : Nat), (∀ i, i < L → f i ≤ B) → L ≤ B + 1) := by
  intro h
  have h2 : 2 ≤ 0 + 1 := h (fun _ => 0) 2 0 (fun _ _ => Nat.le_refl 0)
  omega

/-- The bound is load-bearing too: the identity grows strictly and a run
of any length satisfies the growth hypothesis alone. -/
theorem no_bound_without_cap (L : Nat) :
    ∀ i, i + 1 < L → (fun k : Nat => k) i < (fun k : Nat => k) (i + 1) :=
  id_strict L

end Textbook.U28

#print axioms Textbook.U28.allPairs_four
#print axioms Textbook.U28.allPairs_four_length
#print axioms Textbook.U28.allPairs_four_law
#print axioms Textbook.U28.run_capped_at_three
#print axioms Textbook.U28.three_data_bound
#print axioms Textbook.U28.no_bound_without_growth
#print axioms Derivation.index_le_strict_mono
#print axioms Derivation.strict_bounded_length
#print axioms Derivation.no_supply_round_bound
#print axioms Derivation.allPairs_length
"""

EXPECTED = {
    "Textbook.U28.allPairs_four": NONE,
    "Textbook.U28.allPairs_four_length": NONE,
    "Textbook.U28.allPairs_four_law": BOTH,
    "Textbook.U28.run_capped_at_three": BOTH,
    "Textbook.U28.three_data_bound": BOTH,
    "Textbook.U28.no_bound_without_growth": BOTH,
    "Derivation.index_le_strict_mono": BOTH,
    "Derivation.strict_bounded_length": BOTH,
    "Derivation.no_supply_round_bound": BOTH,
    "Derivation.allPairs_length": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U28"))
