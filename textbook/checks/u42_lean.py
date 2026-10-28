"""Unit 42 check: kernel-check the book's Lean for Unit 42.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u42_lean.py

The two `*_trap` declarations measure the toolchain: on Lean 4.33.0 the
`BEq` route `n == n` at `Nat` carries `Classical.choice` and the
`decide` route does not, which is why Genesis's counting lemma is
written with `decide (x = B)`. AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

CHOICE = "depends on axioms: [propext, Classical.choice, Quot.sound]"

LEAN_SOURCE = """\
import Derivation.CapacityBound

namespace Textbook.U42
open Pigeonhole CapacityBound SeparationCapacity

/-- The trap the module header measures: `n == n` at `Nat` goes through
`ReflBEq Nat`, which carries `Classical.choice` on this toolchain. -/
theorem beq_trap (n : Nat) : (n == n) = true := beq_self_eq_true n

/-- The route Genesis takes instead. -/
theorem decide_route (n : Nat) : decide (n = n) = true := decide_eq_true rfl

theorem upto_three : upto 3 = [2, 1, 0] := rfl

/-- The counting lemma on an instance: three distinct values below 3. -/
theorem counting_instance : ([0, 2, 1] : List Nat).length ≤ 3 :=
  nodup_length_le 3 _ (by decide) (by decide)

/-- Four indices into three values collide. -/
theorem four_into_three :
    ∃ p, p < 4 ∧ ∃ q, q < 4 ∧ p ≠ q ∧ (fun t => t % 3) p = (fun t => t % 3) q :=
  pigeonhole 3 (fun t => t % 3) (fun p _ => Nat.mod_lt p (by decide))

theorem encode_examples : encode 2 [1, 0, 1] = 5 ∧ encode 2 [1, 1, 1] = 7 ∧ encode 3 [2, 2] = 8 := by
  decide

theorem encode_bound_instance : encode 2 [1, 0, 1] < 2 ^ 3 :=
  encode_lt 2 [1, 0, 1] (by decide)

theorem parity_ball : colourBall (fun x => x % 2) 2 1 = [1, 0, 1] := by decide

/-- The radius-1 parity view is local, with `g = encode 2`. -/
theorem parity_view_local :
    ViewLocal (fun i => encode 2 (colourBall (fun x => x % 2) i 1)) (fun x => x % 2) 1 :=
  ⟨encode 2, fun _ => rfl⟩

/-- Two points with the same colour ball get the same view. -/
theorem parity_blind_two_four :
    (fun i => encode 2 (colourBall (fun x => x % 2) i 1)) 2 =
    (fun i => encode 2 (colourBall (fun x => x % 2) i 1)) 4 :=
  local_view_blind parity_view_local (by decide)

theorem threshold_values :
    2 ^ (2 * 0 + 1) + 2 * 0 + 2 = 4 ∧ 2 ^ (2 * 1 + 1) + 2 * 1 + 2 = 12 ∧
    3 ^ (2 * 1 + 1) + 2 * 1 + 2 = 31 := by decide

/-- The bound at `k = 2, d = 0, n = 4`: the three deep points 1, 2, 3 take two values. -/
theorem capacity_two_zero_four :
    ∃ i j, i ≠ j ∧ 0 < i ∧ i + 0 < 4 ∧ 0 < j ∧ j + 0 < 4 ∧
      (fun x => x % 2) i = (fun x => x % 2) j :=
  capacity_bound (fun x => x % 2) (fun x => x % 2) 2 0 4
    (fun x => Nat.mod_lt x (by decide)) ⟨fun l => l.headD 0, fun _ => rfl⟩ (by decide)

/-- Below the threshold at radius 1: a two-colouring of `0..10` whose radius-1
view separates all eight deep points of the chain of length 11 (threshold 12).
The colours along `1..10` are a de Bruijn word: every 3-window is distinct.
Genesis exhibits the `d = 0` witness only; this is the book's `d = 1` witness. -/
def deBruijn : Nat → Nat := fun i => [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0].getD i 0

theorem deBruijn_windows :
    (List.range 8).map (fun t => encode 2 (colourBall deBruijn (t + 2) 1)) =
      [0, 4, 2, 5, 6, 7, 3, 1] := by
  decide

theorem deBruijn_separates_deep :
    ∀ i ∈ [2, 3, 4, 5, 6, 7, 8, 9], ∀ j ∈ [2, 3, 4, 5, 6, 7, 8, 9], i ≠ j →
      encode 2 (colourBall deBruijn i 1) ≠ encode 2 (colourBall deBruijn j 1) := by
  decide

end Textbook.U42

#print axioms Textbook.U42.beq_trap
#print axioms Textbook.U42.decide_route
#print axioms Textbook.U42.upto_three
#print axioms Textbook.U42.counting_instance
#print axioms Textbook.U42.four_into_three
#print axioms Textbook.U42.encode_examples
#print axioms Textbook.U42.encode_bound_instance
#print axioms Textbook.U42.parity_ball
#print axioms Textbook.U42.parity_view_local
#print axioms Textbook.U42.parity_blind_two_four
#print axioms Textbook.U42.threshold_values
#print axioms Textbook.U42.capacity_two_zero_four
#print axioms Textbook.U42.deBruijn_windows
#print axioms Textbook.U42.deBruijn_separates_deep
#print axioms Pigeonhole.nodup_length_le
#print axioms Pigeonhole.pigeonhole
#print axioms CapacityBound.encode_lt
#print axioms CapacityBound.encode_inj
#print axioms CapacityBound.local_view_blind
#print axioms CapacityBound.capacity_bound
#print axioms CapacityBound.local_view_can_separate
"""

EXPECTED = {
    "Textbook.U42.beq_trap": CHOICE,
    "Textbook.U42.decide_route": NONE,
    "Textbook.U42.upto_three": NONE,
    "Textbook.U42.counting_instance": BOTH,
    "Textbook.U42.four_into_three": BOTH,
    "Textbook.U42.encode_examples": NONE,
    "Textbook.U42.encode_bound_instance": BOTH,
    "Textbook.U42.parity_ball": NONE,
    "Textbook.U42.parity_view_local": NONE,
    "Textbook.U42.parity_blind_two_four": NONE,
    "Textbook.U42.threshold_values": NONE,
    "Textbook.U42.capacity_two_zero_four": BOTH,
    "Textbook.U42.deBruijn_windows": PROPEXT,
    "Textbook.U42.deBruijn_separates_deep": PROPEXT,
    "Pigeonhole.nodup_length_le": BOTH,
    "Pigeonhole.pigeonhole": BOTH,
    "CapacityBound.encode_lt": BOTH,
    "CapacityBound.encode_inj": BOTH,
    "CapacityBound.local_view_blind": NONE,
    "CapacityBound.capacity_bound": BOTH,
    "CapacityBound.local_view_can_separate": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U42"))
