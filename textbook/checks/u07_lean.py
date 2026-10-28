"""Unit 07 check: kernel-check the book's Lean for Unit 07.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u07_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, PROPEXT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Inertia
import Derivation.Erasure

namespace Textbook.U07
open Derivation

def tgenesis : TRegime := ⟨[], [], [], [], []⟩

/-- Reading L's history with its tokens kept (Unit 05's numbering). -/
def tL : List TEvent :=
  [.supply 0, .supply 1, .supply 1, .supply 2, .admitDatum 1, .admitDatum 2, .impose 0 1]

/-- Erasing it gives exactly the history `historyL_replays` is stated for. -/
theorem tL_erases :
    eraseHistory tgenesis tL =
      [.supply 0, .supply 1, .supply 1, .supply 2, .admitDatum, .admitDatum, .impose 0 1] := by
  decide

/-- The token-aware replay, erased, is R2L. -/
theorem tL_replays_erased : (replayT tL tgenesis).map TRegime.erase = some R2L := by
  decide

/-- The simulation theorem, instantiated: the erased replay of the token
history equals the erased-model replay of the erased history. -/
theorem simulation_on_L :
    (replayT tL tgenesis).map TRegime.erase = replayE (eraseHistory tgenesis tL) genesis :=
  erase_replay tL tgenesis

/-- `historyL_replays` recovered from the token side, through the simulation. -/
theorem historyL_via_erasure :
    replayE [.supply 0, .supply 1, .supply 1, .supply 2,
             .admitDatum, .admitDatum, .impose 0 1] genesis = some R2L := by
  rw [← tL_erases, ← simulation_on_L]
  exact tL_replays_erased

/-- A history with a duplicate: the duplicate erases to a supply. -/
theorem dup_history_erases :
    eraseHistory tgenesis [.admitDatum 1, .admitDatum 1, .admitDatum 2]
      = [.admitDatum, .supply 1, .admitDatum] := by
  decide

theorem simulation_on_dup :
    (replayT [.admitDatum 1, .admitDatum 1, .admitDatum 2] tgenesis).map TRegime.erase
      = replayE [.admitDatum, .supply 1, .admitDatum] genesis := by
  rw [erase_replay]
  decide

/-- An ill-formed step poisons both replays; the erased history is cut there. -/
theorem poison_both :
    (replayT [.admitDatum 1, .impose 0 1, .admitDatum 2] tgenesis) = none := by
  decide

theorem poison_cut :
    eraseHistory tgenesis [.admitDatum 1, .impose 0 1, .admitDatum 2] = [.admitDatum, .impose 0 1] := by
  decide

end Textbook.U07

#print axioms Textbook.U07.tL_erases
#print axioms Textbook.U07.tL_replays_erased
#print axioms Textbook.U07.simulation_on_L
#print axioms Textbook.U07.historyL_via_erasure
#print axioms Textbook.U07.dup_history_erases
#print axioms Textbook.U07.simulation_on_dup
#print axioms Textbook.U07.poison_both
#print axioms Textbook.U07.poison_cut
#print axioms Derivation.erase_step
#print axioms Derivation.erase_replay
"""

EXPECTED = {
    "Textbook.U07.tL_erases": BOTH,
    "Textbook.U07.tL_replays_erased": BOTH,
    "Textbook.U07.simulation_on_L": BOTH,
    "Textbook.U07.historyL_via_erasure": BOTH,
    "Textbook.U07.dup_history_erases": BOTH,
    "Textbook.U07.simulation_on_dup": BOTH,
    "Textbook.U07.poison_both": BOTH,
    "Textbook.U07.poison_cut": BOTH,
    "Derivation.erase_step": BOTH,
    "Derivation.erase_replay": BOTH,
}
_ = PROPEXT

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U07"))
