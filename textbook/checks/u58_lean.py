"""Unit 58 check: kernel-check the book's Lean for Unit 58.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u58_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.ControllerCategory

namespace Textbook.U58
open PrimitivePassage ControllerCategory

/-- A disabled kind is inert: the no-addCol controller leaves OBST5 alone. -/
theorem noAdd_inert : interpK noAddK OBST5 (.addCol [0]) = OBST5 := rfl

/-- The all-on controller runs the same event as the sealed step. -/
theorem full_runs_step : interpK fullK OBST5 (.addCol [0]) = step OBST5 (.addCol [0]) :=
  interpK_full _ _

/-- The two-rule block at OBST5 under the no-refuse controller (a live member). -/
theorem noRef_resolves :
    obstP (interpK noRefK (interpK noRefK OBST5 (.setBudget 1)) (.addCol [0])) 0 1 = false :=
  tworule_executable_of_live noRefK noRefK_live

/-- Live is not "resolves OBST5 by the block": the block needs only two
of the three live bits, so the no-refine controller resolves OBST5 too. -/
theorem noRefine_resolves_obst5 :
    obstP (replayK noRefineK [.setBudget 1, .addCol [0]] OBST5) 0 1 = false := by decide

theorem noRefine_not_live : ResponseLiveB noRefineK = false := by decide

/-- A constant simulation into a halted state, evaluated. -/
theorem const_value : (constSim noRefCtrl fullCtrl HALTED0 rfl).f OBST5 = HALTED0 := rfl

/-- Refusal erasure at a state carrying a refusal, and its square at a refuse event. -/
theorem erase_value : eraseSim.f { OBST5 with refusals := [(0, 1)] } = OBST5 := rfl

theorem erase_square_refuse :
    eraseRef (interpK fullK OBST5 (.refuse 0 1)) = interpK noRefK (eraseRef OBST5) (.refuse 0 1) :=
  eraseSim.comm OBST5 (.refuse 0 1)

theorem erase_square_values :
    eraseRef (interpK fullK OBST5 (.refuse 0 1)) = OBST5 ∧
    interpK noRefK (eraseRef OBST5) (.refuse 0 1) = OBST5 := by
  constructor <;> decide

/-- The twist and erasure, as simulations, are different. -/
theorem twist_ne_erase_sim : (twistSim : Sim fullCtrl noRefCtrl) ≠ eraseSim := by
  intro h
  exact twist_ne_erase_at_dup (congrArg (fun u : Sim fullCtrl noRefCtrl => u.f DUPSTATE) h)

theorem twist_values :
    twistF DUPSTATE = { DUPSTATE with refusals := [(0, 0)] } ∧
    eraseRef DUPSTATE = { DUPSTATE with refusals := [] } := by
  constructor <;> rfl

/-- Admission deduplicates, so a replayed store has no duplicate. -/
theorem dedup_example : (replayP [.admitOcc 5, .admitOcc 5] genesisP).occ = [5] := by decide

theorem dedup_general : hasDup (replayP [.admitOcc 5, .admitOcc 5] genesisP).occ = false :=
  reachable_no_dup _

/-- Agreement on the orbit, at one history, by the theorem and by evaluation. -/
def hist2 : List PEvent := [.admitOcc 7, .admitOcc 8, .assertWit 0 1]

theorem agree_hist2 :
    twistStrict.toSim.f (replayP hist2 genesisP) = eraseStrict.toSim.f (replayP hist2 genesisP) :=
  strict_agree_on_reachable _ _ hist2

theorem agree_hist2_value : twistF (replayP hist2 genesisP) = replayP hist2 genesisP := by decide

/-! The unqualified docstring reading ("any two genesis-preserving
simulations agree on every state replayed from genesis") names no pair.
For the pair the theorem fixes it is proved; for another pair, with
replay still meaning `replayP`, here is a counterexample. -/

/-- Tag any nonempty refusal store with one junk record. -/
def refTag : PState → PState :=
  fun s => if s.refusals = [] then s else setRef [(0, 0)] s

theorem refusals_step_nonrefuse (s : PState) (e : PEvent) (h : isRefuse e = false) :
    (step s e).refusals = s.refusals := by
  have h1 := setRef_step_comm s.refusals s e h
  have h2 : setRef s.refusals s = s := rfl
  rw [h2] at h1
  exact (congrArg PState.refusals h1).symm

theorem refTag_step_comm (s : PState) (e : PEvent) (h : isRefuse e = false) :
    refTag (step s e) = step (refTag s) e := by
  unfold refTag
  simp only [refusals_step_nonrefuse s e h]
  by_cases hr : s.refusals = []
  · rw [if_pos hr, if_pos hr]
  · rw [if_neg hr, if_neg hr]
    exact setRef_step_comm [(0, 0)] s e h

/-- `refTag` is a simulation from the refusal-free controller to itself:
on refuse events that controller is inert on both sides. -/
def refTagSim : Sim noRefCtrl noRefCtrl where
  f := refTag
  comm := by
    intro s e
    cases e with
    | admitOcc t => exact refTag_step_comm s (.admitOcc t) rfl
    | assertWit i j => exact refTag_step_comm s (.assertWit i j) rfl
    | admitWit i j => exact refTag_step_comm s (.admitWit i j) rfl
    | protect i j => exact refTag_step_comm s (.protect i j) rfl
    | declareObs => exact refTag_step_comm s .declareObs rfl
    | refineCol v p => exact refTag_step_comm s (.refineCol v p) rfl
    | addCol c => exact refTag_step_comm s (.addCol c) rfl
    | refuse i j => rfl
    | setBudget n => exact refTag_step_comm s (.setBudget n) rfl
    | setLicense b => exact refTag_step_comm s (.setLicense b) rfl
    | halt => exact refTag_step_comm s .halt rfl

theorem refTag_genesis : refTag genesisP = genesisP := rfl

/-- A history of the sealed step that records a refusal. -/
def refHist : List PEvent :=
  [.admitOcc 7, .admitOcc 8, .assertWit 0 1, .admitWit 0 1, .protect 0 1, .declareObs,
   .setBudget 1, .refuse 0 1]

theorem refHist_records : (replayP refHist genesisP).refusals = [(0, 1)] := by decide

/-- Two genesis-preserving simulations noRefCtrl → noRefCtrl that differ on
a state replayed (by `replayP`) from genesis. -/
theorem other_pair_counterexample :
    refTagSim.f genesisP = genesisP ∧ (idSim noRefCtrl).f genesisP = genesisP ∧
    refTagSim.f (replayP refHist genesisP) ≠ (idSim noRefCtrl).f (replayP refHist genesisP) := by
  refine ⟨rfl, rfl, ?_⟩
  show refTag (replayP refHist genesisP) ≠ replayP refHist genesisP
  decide

/-- Under replay by the refusal-free controller itself the store stays
empty, so there the two agree: the counterexample is specific to `replayP`. -/
theorem same_under_own_replay :
    refTag (replayK noRefK refHist genesisP) = replayK noRefK refHist genesisP := by decide

/-- Replay must use the simulation's own source and target controllers. -/
theorem simulation_replay (C1 C2 : Ctrl) (u : Sim C1 C2) (h : List PEvent)
    (s : PState) :
    u.f (replayK C1.d h s) = replayK C2.d h (u.f s) := by
  induction h generalizing s with
  | nil => rfl
  | cons e h ih =>
    change u.f (replayK C1.d h (interpK C1.d s e)) =
      replayK C2.d h (interpK C2.d (u.f s) e)
    rw [ih, u.comm]

theorem same_start_same_own_replay (C1 C2 : Ctrl) (u v : Sim C1 C2)
    (s : PState) (hs : u.f s = v.f s) (h : List PEvent) :
    u.f (replayK C1.d h s) = v.f (replayK C1.d h s) := by
  rw [simulation_replay, simulation_replay, hs]

end Textbook.U58

#print axioms Textbook.U58.noAdd_inert
#print axioms Textbook.U58.simulation_replay
#print axioms Textbook.U58.same_start_same_own_replay
#print axioms Textbook.U58.full_runs_step
#print axioms Textbook.U58.noRef_resolves
#print axioms Textbook.U58.noRefine_resolves_obst5
#print axioms Textbook.U58.noRefine_not_live
#print axioms Textbook.U58.const_value
#print axioms Textbook.U58.erase_value
#print axioms Textbook.U58.erase_square_refuse
#print axioms Textbook.U58.erase_square_values
#print axioms Textbook.U58.twist_ne_erase_sim
#print axioms Textbook.U58.twist_values
#print axioms Textbook.U58.dedup_example
#print axioms Textbook.U58.dedup_general
#print axioms Textbook.U58.agree_hist2
#print axioms Textbook.U58.agree_hist2_value
#print axioms Textbook.U58.refusals_step_nonrefuse
#print axioms Textbook.U58.refTag_step_comm
#print axioms Textbook.U58.refTag_genesis
#print axioms Textbook.U58.refHist_records
#print axioms Textbook.U58.other_pair_counterexample
#print axioms Textbook.U58.same_under_own_replay
#print axioms ControllerCategory.allKinds_complete
#print axioms ControllerCategory.interpK_full
#print axioms ControllerCategory.live_census
#print axioms ControllerCategory.tworule_executable_of_live
#print axioms ControllerCategory.dead_without_addcol
#print axioms ControllerCategory.dead_without_budget
#print axioms ControllerCategory.dead_without_refine
#print axioms ControllerCategory.nonrefuse_agree
#print axioms ControllerCategory.refuse_distinguishes
#print axioms ControllerCategory.comp_assoc
#print axioms ControllerCategory.erase_sim
#print axioms ControllerCategory.every_pair_connected
#print axioms ControllerCategory.sims_never_unique
#print axioms ControllerCategory.no_initial_ctrl
#print axioms ControllerCategory.no_initial_live_ctrl
#print axioms ControllerCategory.const_not_strict
#print axioms ControllerCategory.strict_not_unique
#print axioms ControllerCategory.reachable_no_dup
#print axioms ControllerCategory.sim_pinned
#print axioms ControllerCategory.strict_agree_on_reachable
"""

EXPECTED = {
    "Textbook.U58.noAdd_inert": BOTH,
    "Textbook.U58.simulation_replay": BOTH,
    "Textbook.U58.same_start_same_own_replay": BOTH,
    "Textbook.U58.full_runs_step": BOTH,
    "Textbook.U58.noRef_resolves": BOTH,
    "Textbook.U58.noRefine_resolves_obst5": BOTH,
    "Textbook.U58.noRefine_not_live": NONE,
    "Textbook.U58.const_value": BOTH,
    "Textbook.U58.erase_value": BOTH,
    "Textbook.U58.erase_square_refuse": BOTH,
    "Textbook.U58.erase_square_values": BOTH,
    "Textbook.U58.twist_ne_erase_sim": BOTH,
    "Textbook.U58.twist_values": BOTH,
    "Textbook.U58.dedup_example": BOTH,
    "Textbook.U58.dedup_general": BOTH,
    "Textbook.U58.agree_hist2": BOTH,
    "Textbook.U58.agree_hist2_value": BOTH,
    "Textbook.U58.refusals_step_nonrefuse": BOTH,
    "Textbook.U58.refTag_step_comm": BOTH,
    "Textbook.U58.refTag_genesis": NONE,
    "Textbook.U58.refHist_records": BOTH,
    "Textbook.U58.other_pair_counterexample": BOTH,
    "Textbook.U58.same_under_own_replay": BOTH,
    "ControllerCategory.allKinds_complete": BOTH,
    "ControllerCategory.interpK_full": BOTH,
    "ControllerCategory.live_census": NONE,
    "ControllerCategory.tworule_executable_of_live": BOTH,
    "ControllerCategory.dead_without_addcol": BOTH,
    "ControllerCategory.dead_without_budget": BOTH,
    "ControllerCategory.dead_without_refine": BOTH,
    "ControllerCategory.nonrefuse_agree": BOTH,
    "ControllerCategory.refuse_distinguishes": BOTH,
    "ControllerCategory.comp_assoc": BOTH,
    "ControllerCategory.erase_sim": BOTH,
    "ControllerCategory.every_pair_connected": BOTH,
    "ControllerCategory.sims_never_unique": BOTH,
    "ControllerCategory.no_initial_ctrl": BOTH,
    "ControllerCategory.no_initial_live_ctrl": BOTH,
    "ControllerCategory.const_not_strict": BOTH,
    "ControllerCategory.strict_not_unique": BOTH,
    "ControllerCategory.reachable_no_dup": BOTH,
    "ControllerCategory.sim_pinned": BOTH,
    "ControllerCategory.strict_agree_on_reachable": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U58"))
