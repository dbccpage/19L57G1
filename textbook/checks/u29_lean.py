"""Unit 29 check: kernel-check the book's Lean for Unit 29.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u29_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.CountTransport

namespace Textbook.U29
open Derivation

/-- The swap of two data, as a renaming. -/
def swapFun : Nat → Nat
  | 0 => 1
  | 1 => 0
  | n + 2 => n + 2

theorem swapFun_invol : ∀ x, swapFun (swapFun x) = x := by
  intro x
  match x with
  | 0 => rfl
  | 1 => rfl
  | _ + 2 => rfl

theorem swapFun_bound : ∀ x, x < 2 → swapFun x < 2 := by
  intro x hx
  match x with
  | 0 => decide
  | 1 => decide
  | y + 2 => exact absurd hx (by omega)

def swap2 : DRen 2 :=
  ⟨swapFun, swapFun, swapFun_invol, swapFun_invol, swapFun_bound, swapFun_bound⟩

/-- Renaming the countermodel moves the mark from datum 0 to datum 1. -/
theorem renamed_cm : renameRegime swap2.f cmRegime = ⟨2, [1], [(0, [1])], [], []⟩ := by
  decide

/-- Genesis's transport, at this renaming and this pair. -/
theorem cm_transport :
    collapsed (renameRegime swap2.f cmRegime) 1 0 ↔ collapsed cmRegime 0 1 :=
  collapsed_rename swap2 cmRegime rfl 0 1

/-- So the renamed regime does not collapse its (now swapped) pair either. -/
theorem renamed_not_collapsed : ¬ collapsed (renameRegime swap2.f cmRegime) 1 0 :=
  fun h => separable_not_collapsed cm_separable (cm_transport.mp h)

/-- The action touches `insts` only. -/
theorem rename_data (f : Nat → Nat) (r : Regime) : (renameRegime f r).data = r.data := rfl
theorem rename_forms (f : Nat → Nat) (r : Regime) : (renameRegime f r).forms = r.forms := rfl
theorem rename_rules (f : Nat → Nat) (r : Regime) : (renameRegime f r).rules = r.rules := rfl
theorem rename_reqs (f : Nat → Nat) (r : Regime) : (renameRegime f r).reqs = r.reqs := rfl

/-- Holes stay holes under `mapCtx`. -/
theorem mapCtx_keeps_hole (f : Nat → Nat) (c : Ctx) (h : none ∈ c.slots) :
    none ∈ (mapCtx f c).slots :=
  List.mem_map.mpr ⟨none, h, rfl⟩

/-- The constant map has no two-sided inverse, so it is no `DRen`: an
inverse would have to send 0 back to both 0 and 1. -/
theorem const_has_no_inverse : ¬ ∃ g : Nat → Nat, ∀ x, g ((fun _ : Nat => 0) x) = x := by
  rintro ⟨g, hg⟩
  have h0 : g 0 = 0 := hg 0
  have h1 : g 0 = 1 := hg 1
  omega

end Textbook.U29

#print axioms Textbook.U29.renamed_cm
#print axioms Textbook.U29.cm_transport
#print axioms Textbook.U29.renamed_not_collapsed
#print axioms Textbook.U29.rename_reqs
#print axioms Textbook.U29.mapCtx_keeps_hole
#print axioms Textbook.U29.const_has_no_inverse
#print axioms Derivation.plug_mapCtx
#print axioms Derivation.collapsed_rename
#print axioms Derivation.collapsedCount_rename
#print axioms Derivation.non_injective_does_not_transport
"""

EXPECTED = {
    "Textbook.U29.renamed_cm": BOTH,
    "Textbook.U29.cm_transport": BOTH,
    "Textbook.U29.renamed_not_collapsed": BOTH,
    "Textbook.U29.rename_reqs": NONE,
    "Textbook.U29.mapCtx_keeps_hole": BOTH,
    "Textbook.U29.const_has_no_inverse": BOTH,
    "Derivation.plug_mapCtx": BOTH,
    "Derivation.collapsed_rename": BOTH,
    "Derivation.collapsedCount_rename": BOTH,
    "Derivation.non_injective_does_not_transport": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U29"))
