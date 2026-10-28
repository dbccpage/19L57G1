"""Unit 05 check: kernel-check the book's Lean for Unit 05.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u05_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Inertia
import Derivation.Erasure

namespace Textbook.U05
open Derivation

/-- The two readings end in two different regimes. -/
theorem R2L_ne_R2F : R2L ≠ R2F := by decide

/-- They differ by exactly one admitted datum: the initial inscription. -/
theorem readings_differ_by_one : R2F.data = R2L.data + 1 := rfl

/-- Reading F's history with its genesis admission removed does not replay:
the demand `impose 1 2` names a third datum that is then never admitted.
The indices in a demand are relative to the reading. -/
theorem F_without_genesis_admission :
    replayE [.supply 0, .supply 1, .supply 1, .supply 2,
             .admitDatum, .admitDatum, .impose 1 2] genesis = none := by
  decide

/-- Reading L's history with the demand renumbered as in F also fails. -/
theorem L_with_F_demand :
    replayE [.supply 0, .supply 1, .supply 1, .supply 2,
             .admitDatum, .admitDatum, .impose 1 2] genesis = none :=
  F_without_genesis_admission

/-- Token-aware genesis: no tokens. -/
def tgenesis : TRegime := ⟨[], [], [], [], []⟩

/-- Challenge 1's two sub-readings (admit `<a>` on supply, or not) reach
the same token-aware regime once Challenge 2 retains `<a>` and `<ab>`.
Tokens: 0 is ⟨⟩, 1 is ⟨A⟩, 2 is ⟨AB⟩. -/
theorem subreadings_converge :
    replayT [.supply 0, .supply 1, .admitDatum 1, .supply 1, .supply 2,
             .admitDatum 1, .admitDatum 2] tgenesis
      = replayT [.supply 0, .supply 1, .supply 1, .supply 2,
                 .admitDatum 1, .admitDatum 2] tgenesis := by
  decide

/-- What they converge to: the two tokens, in order, nothing else. -/
theorem subreadings_regime :
    replayT [.supply 0, .supply 1, .supply 1, .supply 2,
             .admitDatum 1, .admitDatum 2] tgenesis
      = some ⟨[1, 2], [], [], [], []⟩ := by
  decide

/-- Whether ⟨⟩ is admitted is not settled by convergence: the two readings
remain two token-aware regimes. -/
theorem readings_do_not_converge :
    replayT [.supply 0, .admitDatum 0, .supply 1, .supply 1, .supply 2,
             .admitDatum 1, .admitDatum 2] tgenesis
      ≠ replayT [.supply 0, .supply 1, .supply 1, .supply 2,
                 .admitDatum 1, .admitDatum 2] tgenesis := by
  decide

end Textbook.U05

#print axioms Textbook.U05.R2L_ne_R2F
#print axioms Textbook.U05.readings_differ_by_one
#print axioms Textbook.U05.F_without_genesis_admission
#print axioms Textbook.U05.L_with_F_demand
#print axioms Textbook.U05.subreadings_converge
#print axioms Textbook.U05.subreadings_regime
#print axioms Textbook.U05.readings_do_not_converge
#print axioms Derivation.historyL_replays
#print axioms Derivation.historyF_replays
"""

EXPECTED = {
    "Textbook.U05.R2L_ne_R2F": NONE,
    "Textbook.U05.readings_differ_by_one": NONE,
    "Textbook.U05.F_without_genesis_admission": PROPEXT,
    "Textbook.U05.L_with_F_demand": PROPEXT,
    "Textbook.U05.subreadings_converge": BOTH,
    "Textbook.U05.subreadings_regime": BOTH,
    "Textbook.U05.readings_do_not_converge": BOTH,
    "Derivation.historyL_replays": PROPEXT,
    "Derivation.historyF_replays": PROPEXT,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U05"))
