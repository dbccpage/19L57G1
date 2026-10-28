"""Unit 55 check: kernel-check the book's Lean for Unit 55.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u55_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.HigherStructure

namespace Textbook.U55
open HigherStructure PrimitivePassage

/-- The first three blocks of the driver, written out. -/
theorem blocks :
    growBlock 0 = [.admitOcc 0] ∧
    growBlock 1 = [.admitOcc 1, .assertWit 0 1, .admitWit 0 1, .protect 0 1,
                   .declareObs, .setBudget 1, .addCol [0]] ∧
    growBlock 2 = [.admitOcc 2, .assertWit 1 2, .admitWit 1 2, .protect 1 2,
                   .setBudget 1, .addCol [1]] := by
  refine ⟨rfl, rfl, rfl⟩

/-- Stage 3 of the growth, computed: the path on four occurrences. -/
theorem stage_three :
    (graphAt 3).occ = [0, 1, 2, 3] ∧
    (graphAt 3).wit = [(0, 1), (1, 2), (2, 3)] ∧
    (graphAt 3).obs = some [[0], [1], [2]] ∧
    (graphAt 3).budget = 0 := by
  decide

/-- Genesis's characterisation at that stage. -/
theorem stage_three_is_path : graphAt 3 = pathState 2 := graphAt_spec 2

/-- Inside round 3 (`m = 1`): the obstruction is in force at `preCol 1`,
the extension `[2]` is proposed, and executing it lands on `pathState 2`. -/
theorem round_three_obstructed : obstP (preCol 1) 2 3 = true := round_obstruction 1
theorem round_three_proposal : [2] ∈ extensionProposals (preCol 1) 2 3 := round_two_rule 1
theorem round_three_lands : step (preCol 1) (.addCol [2]) = pathState 2 := round_resolution 1

/-- The same three facts by computation, so the reader can see the
values rather than the schema. -/
theorem round_three_values :
    obstP (preCol 1) 2 3 = true ∧
    extensionProposals (preCol 1) 2 3 = [[2], [3]] ∧
    step (preCol 1) (.addCol [2]) = pathState 2 := by
  decide

/-- Before the budget event the obstruction is already there and the
column cannot yet be added: the budget gates the resolution, not the
obstruction. -/
theorem budget_gates_round :
    obstP (g3 1) 2 3 = true ∧ step (g3 1) (.addCol [2]) = g3 1 := by
  decide

/-- Quiescence at stage 3, by computation and by the theorem. -/
theorem stage_three_quiet :
    ((graphAt 3).prot.all (fun r => !obstP (graphAt 3) r.1 r.2)) = true := by
  decide

theorem stage_three_quiet_schema :
    ∀ r ∈ (graphAt 3).prot, obstP (graphAt 3) r.1 r.2 = false :=
  graphAt_quiescent 2

/-- The residue is 1 at stage 3, and it is the same for the path on three
occurrences, which is connected, and for three occurrences with the
edges (0,1), (1,2) and a third occurrence 3 with no edge, which is not:
the residue does not decide connectedness. -/
theorem residue_three : ((graphAt 3).occ.length : Int) - ((graphAt 3).wit.length : Int) = 1 :=
  path_connectivity_residue 2

theorem residue_blind :
    (([0, 1, 2, 3] : List Nat).length : Int) - (([(0, 1), (1, 2), (0, 2)] : List (Nat × Nat)).length : Int)
      = (([0, 1, 2, 3] : List Nat).length : Int) - (([(0, 1), (1, 2), (2, 0)] : List (Nat × Nat)).length : Int) := by
  decide

/-- The complex after the six edges, and the ladder at dimension 2 there. -/
def edgeStage : Complex := creplay (k4Events.take 10) emptyComplex

theorem edge_stage_value :
    edgeStage = ⟨[0, 1, 2, 3], [(0, 1), (1, 2), (2, 3), (0, 2), (1, 3), (0, 3)], [], []⟩ := by
  decide

theorem ladder_two_here :
    (0, 1, 2) ∈ (cstep edgeStage (.addT 0 1 2)).c2 ∧ cstep edgeStage (.addT 0 1 2) ≠ edgeStage :=
  ladder_dim2 edgeStage 0 1 2 (by decide)

theorem ladder_three_here :
    (0, 1, 2, 3) ∈ (cstep k4Boundary (.addQ 0 1 2 3)).c3 ∧
      cstep k4Boundary (.addQ 0 1 2 3) ≠ k4Boundary :=
  ladder_dim3 k4Boundary 0 1 2 3 filling_not_forced.1

/-- The last step of the log is exactly the solid cell. -/
theorem last_step_is_solid : cstep k4Boundary (.addQ 0 1 2 3) = k4 := by decide

/-- A boundary one face short is refused at dimensions 2 and 3. -/
theorem horn_two_refused :
    cstep ⟨[0, 1, 2], [(0, 1), (1, 2)], [], []⟩ (.addT 0 1 2)
      = ⟨[0, 1, 2], [(0, 1), (1, 2)], [], []⟩ := by
  decide

theorem horn_three_refused :
    cstep (creplay (k4Events.take 13) emptyComplex) (.addQ 0 1 2 3)
      = creplay (k4Events.take 13) emptyComplex := by
  decide

/-- Audit finding 1 made visible: the alternating statistic takes two
different values at two stages of one growth, and it moves when a vertex
is admitted to the finished complex. -/
theorem altNum_not_invariant :
    altNum (creplay (k4Events.take 4) emptyComplex) ≠ altNum (creplay (k4Events.take 10) emptyComplex) ∧
    altNum (cstep k4 (.addV 4)) = 2 := by
  decide

/-- The census on five occurrences, which the Lean module does not state
(the artifact does): a fourth value of a finite count, not a growth law. -/
theorem cut_census_five : cutCensus 5 0 1 = 8 := by decide

/-- The composite boundary of one triangle, written out, and its
coefficients. -/
theorem push_triangle :
    push1 (bd2 (0, 1, 2)) = [(1, 2), (-1, 1), (-1, 2), (1, 0), (1, 1), (-1, 0)] ∧
    coeffV 0 (push1 (bd2 (0, 1, 2))) = 0 ∧
    coeffV 1 (push1 (bd2 (0, 1, 2))) = 0 ∧
    coeffV 2 (push1 (bd2 (0, 1, 2))) = 0 := by
  decide

end Textbook.U55

#print axioms Textbook.U55.blocks
#print axioms Textbook.U55.stage_three
#print axioms Textbook.U55.stage_three_is_path
#print axioms Textbook.U55.round_three_obstructed
#print axioms Textbook.U55.round_three_proposal
#print axioms Textbook.U55.round_three_lands
#print axioms Textbook.U55.round_three_values
#print axioms Textbook.U55.budget_gates_round
#print axioms Textbook.U55.stage_three_quiet
#print axioms Textbook.U55.stage_three_quiet_schema
#print axioms Textbook.U55.residue_three
#print axioms Textbook.U55.residue_blind
#print axioms Textbook.U55.edge_stage_value
#print axioms Textbook.U55.ladder_two_here
#print axioms Textbook.U55.ladder_three_here
#print axioms Textbook.U55.last_step_is_solid
#print axioms Textbook.U55.horn_two_refused
#print axioms Textbook.U55.horn_three_refused
#print axioms Textbook.U55.altNum_not_invariant
#print axioms Textbook.U55.cut_census_five
#print axioms Textbook.U55.push_triangle
#print axioms HigherStructure.graphAt_spec
#print axioms HigherStructure.round_obstruction
#print axioms HigherStructure.round_two_rule
#print axioms HigherStructure.round_resolution
#print axioms HigherStructure.round_creation_record
#print axioms HigherStructure.graph_growth
#print axioms HigherStructure.graphAt_quiescent
#print axioms HigherStructure.path_connectivity_residue
#print axioms HigherStructure.ladder_dim2
#print axioms HigherStructure.ladder_dim3
#print axioms HigherStructure.shell_guard_load_bearing
#print axioms HigherStructure.k4_skeleton_from_passage
#print axioms HigherStructure.k4_builds
#print axioms HigherStructure.k4_skeleton_agrees
#print axioms HigherStructure.filling_not_forced
#print axioms HigherStructure.altNum_stages
#print axioms HigherStructure.cut_census_growth
#print axioms HigherStructure.d2_zero_triangles
#print axioms HigherStructure.d2_zero_tet
#print axioms HigherStructure.boundary_not_forced
"""

EXPECTED = {
    "Textbook.U55.blocks": NONE,
    "Textbook.U55.stage_three": BOTH,
    "Textbook.U55.stage_three_is_path": BOTH,
    "Textbook.U55.round_three_obstructed": BOTH,
    "Textbook.U55.round_three_proposal": BOTH,
    "Textbook.U55.round_three_lands": BOTH,
    "Textbook.U55.round_three_values": BOTH,
    "Textbook.U55.budget_gates_round": BOTH,
    "Textbook.U55.stage_three_quiet": BOTH,
    "Textbook.U55.stage_three_quiet_schema": BOTH,
    "Textbook.U55.residue_three": BOTH,
    "Textbook.U55.residue_blind": NONE,
    "Textbook.U55.edge_stage_value": BOTH,
    "Textbook.U55.ladder_two_here": BOTH,
    "Textbook.U55.ladder_three_here": BOTH,
    "Textbook.U55.last_step_is_solid": BOTH,
    "Textbook.U55.horn_two_refused": BOTH,
    "Textbook.U55.horn_three_refused": BOTH,
    "Textbook.U55.altNum_not_invariant": BOTH,
    "Textbook.U55.cut_census_five": BOTH,
    "Textbook.U55.push_triangle": NONE,
    "HigherStructure.graphAt_spec": BOTH,
    "HigherStructure.round_obstruction": BOTH,
    "HigherStructure.round_two_rule": BOTH,
    "HigherStructure.round_resolution": BOTH,
    "HigherStructure.round_creation_record": NONE,
    "HigherStructure.graph_growth": BOTH,
    "HigherStructure.graphAt_quiescent": BOTH,
    "HigherStructure.path_connectivity_residue": BOTH,
    "HigherStructure.ladder_dim2": BOTH,
    "HigherStructure.ladder_dim3": BOTH,
    "HigherStructure.shell_guard_load_bearing": BOTH,
    "HigherStructure.k4_skeleton_from_passage": BOTH,
    "HigherStructure.k4_builds": BOTH,
    "HigherStructure.k4_skeleton_agrees": BOTH,
    "HigherStructure.filling_not_forced": BOTH,
    "HigherStructure.altNum_stages": BOTH,
    "HigherStructure.cut_census_growth": BOTH,
    "HigherStructure.d2_zero_triangles": BOTH,
    "HigherStructure.d2_zero_tet": BOTH,
    "HigherStructure.boundary_not_forced": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U55"))
