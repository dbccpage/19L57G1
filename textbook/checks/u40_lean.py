"""Unit 40 check: kernel-check the book's Lean for Unit 40.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u40_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Generator

namespace Textbook.U40
open Generator RefusalFrontier

/-- The tag store of the chain of length 3, read off the Genesis theorem. -/
theorem tags_three : (reflState 3).tags = [1, 2, 3] := by
  rw [reflective_chain_tags]; rfl

/-- The whole depth-1 profile table of the chain of length 4. -/
theorem profile_table_four :
    profile1 (reflState 4) 0 = (false, false, true) ∧
    profile1 (reflState 4) 1 = (true, true, true) ∧
    profile1 (reflState 4) 2 = (true, true, true) ∧
    profile1 (reflState 4) 3 = (true, true, true) ∧
    profile1 (reflState 4) 4 = (true, true, false) := by decide

/-- The same table by the three class theorems, not by computation. -/
theorem profile_table_four_by_classes :
    profile1 (reflState 4) 0 = (false, false, true) ∧
    profile1 (reflState 4) 2 = (true, true, true) ∧
    profile1 (reflState 4) 4 = (true, true, false) :=
  ⟨endpoint0_profile 4 (by omega), middle_profile 4 2 (by omega) (by omega),
   endpointN_profile 4 (by omega)⟩

/-- Length 2 has no obstruction: 1 is interior, 2 is the tip. -/
theorem no_fire_at_two : profile1 (reflState 2) 1 ≠ profile1 (reflState 2) 2 := by
  decide

/-- Length 3 is the first that fires. -/
theorem fires_at_three : profile1 (reflState 3) 1 = profile1 (reflState 3) 2 :=
  (generation_never_dries 3 (by omega)).2

/-- The exactness iff at length 4, element 1 against the others. -/
theorem obstructions_of_one_at_four :
    ¬ profile1 (reflState 4) 1 = profile1 (reflState 4) 0 ∧
    profile1 (reflState 4) 1 = profile1 (reflState 4) 3 ∧
    ¬ profile1 (reflState 4) 1 = profile1 (reflState 4) 4 := by
  refine ⟨?_, ?_, ?_⟩
  · intro h
    have := (depth1_obstructions_are_exactly_middle_pairs 4 1 0 (by omega) (by omega)
      (by omega) (by omega)).mp h
    omega
  · exact (depth1_obstructions_are_exactly_middle_pairs 4 1 3 (by omega) (by omega)
      (by omega) (by omega)).mpr ⟨by omega, by omega, by omega, by omega⟩
  · intro h
    have := (depth1_obstructions_are_exactly_middle_pairs 4 1 4 (by omega) (by omega)
      (by omega) (by omega)).mp h
    omega

/-- Marks 1, 2, 3 are outrun: the Genesis witness is length 6, pair (4, 5). -/
theorem outrun_instance :
    profile1 (reflState 6) 4 = profile1 (reflState 6) 5 ∧ 4 ∉ [1, 2, 3] ∧ 5 ∉ [1, 2, 3] := by
  refine ⟨?_, by decide, by decide⟩
  rw [middle_profile 6 4 (by omega) (by omega), middle_profile 6 5 (by omega) (by omega)]

theorem outrun_general : ∃ n i j, 1 ≤ i ∧ i < n ∧ 1 ≤ j ∧ j < n ∧ i ≠ j ∧
    i ∉ [1, 2, 3] ∧ j ∉ [1, 2, 3] ∧ profile1 (reflState n) i = profile1 (reflState n) j :=
  finite_marks_outrun [1, 2, 3]

/-- The valued profile separates 1 from 2 at length 3 while its structural
part does not: the separation is the index alone. -/
theorem valued_separates_by_index_only :
    profileV (reflState 3) 1 ≠ profileV (reflState 3) 2 ∧
    (profileV (reflState 3) 1).1 = (profileV (reflState 3) 2).1 :=
  ⟨valued_marks_collapse_generation 3 1 2 (by omega), fires_at_three⟩

theorem swap12_values : swap12 0 = 0 ∧ swap12 1 = 2 ∧ swap12 2 = 1 ∧ swap12 3 = 3 := by
  decide

theorem swap_breaks_edge_at_three :
    (0, 1) ∈ (reflState 3).rel ∧ (swap12 0, swap12 1) ∉ (reflState 3).rel :=
  middle_swap_not_relation_preserving 3 (by omega)

/-- Depth 2 at length 4: what elements 1 and 3 look like. -/
theorem depth2_values_four :
    profile2 (reflState 4) 1 =
      ((true, true, true), [(false, false, true)], [(true, true, true)]) ∧
    profile2 (reflState 4) 3 =
      ((true, true, true), [(true, true, true)], [(true, true, false)]) := by decide

/-- Depth 2 at length 5: elements 2 and 3 look alike, and so do 2 and 4 at length 6. -/
theorem depth2_values_five :
    profile2 (reflState 5) 2 = ((true, true, true), [(true, true, true)], [(true, true, true)]) ∧
    profile2 (reflState 5) 3 = profile2 (reflState 5) 2 ∧
    profile2 (reflState 6) 2 = profile2 (reflState 6) 4 := by decide

end Textbook.U40

#print axioms Textbook.U40.tags_three
#print axioms Textbook.U40.profile_table_four
#print axioms Textbook.U40.profile_table_four_by_classes
#print axioms Textbook.U40.no_fire_at_two
#print axioms Textbook.U40.fires_at_three
#print axioms Textbook.U40.obstructions_of_one_at_four
#print axioms Textbook.U40.outrun_instance
#print axioms Textbook.U40.outrun_general
#print axioms Textbook.U40.valued_separates_by_index_only
#print axioms Textbook.U40.swap12_values
#print axioms Textbook.U40.swap_breaks_edge_at_three
#print axioms Textbook.U40.depth2_values_four
#print axioms Textbook.U40.depth2_values_five
#print axioms Generator.reflective_chain_tags
#print axioms Generator.depth1_obstructions_are_exactly_middle_pairs
#print axioms Generator.generation_never_dries
#print axioms Generator.automark_presence_vacuous
#print axioms Generator.finite_marks_outrun
#print axioms Generator.valued_marks_collapse_generation
#print axioms Generator.middle_swap_not_relation_preserving
#print axioms Generator.depth2_obstruction_n5
"""

EXPECTED = {
    "Textbook.U40.tags_three": PROPEXT,
    "Textbook.U40.profile_table_four": BOTH,
    "Textbook.U40.profile_table_four_by_classes": BOTH,
    "Textbook.U40.no_fire_at_two": BOTH,
    "Textbook.U40.fires_at_three": BOTH,
    "Textbook.U40.obstructions_of_one_at_four": BOTH,
    "Textbook.U40.outrun_instance": BOTH,
    "Textbook.U40.outrun_general": BOTH,
    "Textbook.U40.valued_separates_by_index_only": BOTH,
    "Textbook.U40.swap12_values": NONE,
    "Textbook.U40.swap_breaks_edge_at_three": BOTH,
    "Textbook.U40.depth2_values_four": BOTH,
    "Textbook.U40.depth2_values_five": BOTH,
    "Generator.reflective_chain_tags": PROPEXT,
    "Generator.depth1_obstructions_are_exactly_middle_pairs": BOTH,
    "Generator.generation_never_dries": BOTH,
    "Generator.automark_presence_vacuous": BOTH,
    "Generator.finite_marks_outrun": BOTH,
    "Generator.valued_marks_collapse_generation": BOTH,
    "Generator.middle_swap_not_relation_preserving": BOTH,
    "Generator.depth2_obstruction_n5": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U40"))
