"""Unit 41 check: kernel-check the book's Lean for Unit 41.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u41_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.SeparationCapacity

namespace Textbook.U41
open SeparationCapacity Generator RefusalFrontier

/-- The ball is the index window; at the left end truncated subtraction shifts it. -/
theorem ball_values : ball 2 1 = [1, 2, 3] ∧ ball 0 1 = [0, 1, 2] ∧ ball 5 2 = [3, 4, 5, 6, 7] := by
  decide

/-- Radius-one profiles at length 4 (elements 1 and 3) and length 5 (element 2), in full. -/
theorem profileD_values :
    profileD 4 1 1 = [(false, false, true), (true, true, true), (true, true, true)] ∧
    profileD 4 3 1 = [(true, true, true), (true, true, true), (true, true, false)] ∧
    profileD 5 2 1 = [(true, true, true), (true, true, true), (true, true, true)] := by
  decide

/-- The deep profile is constant, by the theorem rather than by evaluation. -/
theorem deep_profile_nine : profileD 9 4 3 = (List.range 7).map (fun _ => (true, true, true)) :=
  profileD_deep 9 4 3 (by omega) (by omega)

/-- Radius 2 is outrun at length 7 by the pair (3, 4). -/
theorem outrun_radius_two : profileD 7 3 2 = profileD 7 4 2 :=
  depth_d_outrun 7 3 4 2 (by omega) (by omega) (by omega) (by omega)

theorem obstruction_radius_two :
    ∃ i j, i ≠ j ∧ 2 < i ∧ i + 2 < 7 ∧ 2 < j ∧ j + 2 < 7 ∧ profileD 7 i 2 = profileD 7 j 2 :=
  depth_d_obstruction 2 7 (by omega)

/-- At length 2d + 3 the pair (d + 1, d + 2) collides, for every radius. -/
theorem threshold_every_radius (d : Nat) :
    profileD (2 * d + 3) (d + 1) d = profileD (2 * d + 3) (d + 2) d :=
  depth_d_outrun _ _ _ _ (by omega) (by omega) (by omega) (by omega)

/-- Below the threshold there is no deep pair at all: at length 4 and radius 1
the deep interior is the single point 2. -/
theorem no_deep_pair_at_four :
    ¬ ∃ i j : Nat, i ≠ j ∧ 1 < i ∧ i + 1 < 4 ∧ 1 < j ∧ j + 1 < 4 := by
  rintro ⟨i, j, hne, hi0, hi1, hj0, hj1⟩
  omega

/-- On an interior point the depth-2 record is the three neighbouring depth-1 profiles. -/
theorem depth2_is_three_profiles :
    profile2 (reflState 5) 2 =
      (profile1 (reflState 5) 2, [profile1 (reflState 5) 1], [profile1 (reflState 5) 3]) :=
  profile2_interior 5 2 (by omega) (by omega)

/-- The general correspondence, at one interior pair of a chain of length 10. -/
theorem correspondence_at_ten :
    profile2 (reflState 10) 4 = profile2 (reflState 10) 6 ↔ profileD 10 4 1 = profileD 10 6 1 :=
  radius_one_agrees_with_sealed_depth2 10 4 6 (by omega) (by omega) (by omega) (by omega)

/-- The two carried instances, read off the Genesis theorems. -/
theorem carried_instances : profileD 5 2 1 = profileD 5 3 1 ∧ profileD 4 1 1 ≠ profileD 4 3 1 :=
  ⟨radius_one_agrees_with_sealed_depth2_n5.2.1, radius_one_agrees_with_sealed_depth2_n4.2.1⟩

/-- Off the interior the correspondence is not claimed, and it fails: the shifted
ball gives the seed of length 5 the same radius-one profile as element 1, while
their depth-2 records differ. The hypotheses `0 < i` are not idle. -/
theorem seed_breaks_correspondence :
    profileD 5 0 1 = profileD 5 1 1 ∧ profile2 (reflState 5) 0 ≠ profile2 (reflState 5) 1 ∧
    profile2 (reflState 5) 0 = ((false, false, true), [], [(true, true, true)]) := by
  decide

end Textbook.U41

#print axioms Textbook.U41.ball_values
#print axioms Textbook.U41.profileD_values
#print axioms Textbook.U41.deep_profile_nine
#print axioms Textbook.U41.outrun_radius_two
#print axioms Textbook.U41.obstruction_radius_two
#print axioms Textbook.U41.threshold_every_radius
#print axioms Textbook.U41.no_deep_pair_at_four
#print axioms Textbook.U41.depth2_is_three_profiles
#print axioms Textbook.U41.correspondence_at_ten
#print axioms Textbook.U41.carried_instances
#print axioms Textbook.U41.seed_breaks_correspondence
#print axioms SeparationCapacity.profileD_deep
#print axioms SeparationCapacity.depth_d_outrun
#print axioms SeparationCapacity.depth_d_obstruction
#print axioms SeparationCapacity.profile2_interior
#print axioms SeparationCapacity.radius_one_agrees_with_sealed_depth2
#print axioms SeparationCapacity.radius_one_agrees_with_sealed_depth2_n5
#print axioms SeparationCapacity.radius_one_agrees_with_sealed_depth2_n4
"""

EXPECTED = {
    "Textbook.U41.ball_values": NONE,
    "Textbook.U41.profileD_values": BOTH,
    "Textbook.U41.deep_profile_nine": BOTH,
    "Textbook.U41.outrun_radius_two": BOTH,
    "Textbook.U41.obstruction_radius_two": BOTH,
    "Textbook.U41.threshold_every_radius": BOTH,
    "Textbook.U41.no_deep_pair_at_four": BOTH,
    "Textbook.U41.depth2_is_three_profiles": BOTH,
    "Textbook.U41.correspondence_at_ten": BOTH,
    "Textbook.U41.carried_instances": BOTH,
    "Textbook.U41.seed_breaks_correspondence": BOTH,
    "SeparationCapacity.profileD_deep": BOTH,
    "SeparationCapacity.depth_d_outrun": BOTH,
    "SeparationCapacity.depth_d_obstruction": BOTH,
    "SeparationCapacity.profile2_interior": BOTH,
    "SeparationCapacity.radius_one_agrees_with_sealed_depth2": BOTH,
    "SeparationCapacity.radius_one_agrees_with_sealed_depth2_n5": BOTH,
    "SeparationCapacity.radius_one_agrees_with_sealed_depth2_n4": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U41"))
