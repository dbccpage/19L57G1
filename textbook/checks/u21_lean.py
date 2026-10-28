"""Unit 21 check: kernel-check the book's Lean for Unit 21.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u21_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Minimality

namespace Textbook.U21
open Derivation

/-- Arity is carried along the form bijection: the field, stated with a
plain `<` instead of list-range membership. -/
theorem arity_invariant {r s : Regime} (iso : Iso r s) (f : Nat)
    (hf : f < r.forms.length) :
    s.forms.getD (iso.fmap f) 0 = r.forms.getD f 0 :=
  iso.arity f (List.mem_range.mpr hf)

/-- The theorem, re-proved with every step named. -/
theorem U0_not_iso_BL' (iso : Iso U0 BL) : False := by
  -- U0 has one form (arity 1); BL has one form (arity 2).
  have hlt : iso.fmap 0 < BL.forms.length := iso.fmap_lt 0 (by decide)
  have h1 : iso.fmap 0 < 1 := by simpa [BL] using hlt
  have h0 : iso.fmap 0 = 0 := by omega
  have ha : BL.forms.getD (iso.fmap 0) 0 = U0.forms.getD 0 0 :=
    iso.arity 0 (by decide)
  rw [h0] at ha
  -- ha : 2 = 1
  simp [U0, BL] at ha

/-- An isomorphism runs backwards: swap the maps and the forward/backward
fields. -/
def isoSymm {r s : Regime} (iso : Iso r s) : Iso s r where
  dmap := iso.dinv
  dinv := iso.dmap
  fmap := iso.finv
  finv := iso.fmap
  dmap_lt := iso.dinv_lt
  dinv_lt := iso.dmap_lt
  dinv_dmap := iso.dmap_dinv
  dmap_dinv := iso.dinv_dmap
  fmap_lt := iso.finv_lt
  finv_lt := iso.fmap_lt
  finv_fmap := iso.fmap_finv
  fmap_finv := iso.finv_fmap
  arity := fun f hf => by
    have h := iso.arity (iso.finv f) (List.mem_range.mpr (iso.finv_lt f hf))
    rw [iso.fmap_finv f hf] at h
    exact h.symm
  insts_fwd := iso.insts_bwd
  insts_bwd := iso.insts_fwd
  rules_fwd := iso.rules_bwd
  rules_bwd := iso.rules_fwd
  reqs_fwd := iso.reqs_bwd
  reqs_bwd := iso.reqs_fwd

/-- The direction Genesis does not state, by symmetry. -/
theorem BL_not_iso_U0 (iso : Iso BL U0) : False := U0_not_iso_BL (isoSymm iso)

/-- And Unit 20's missing direction. -/
theorem BD_not_iso_BL (iso : Iso BD BL) : False := BL_not_iso_BD (isoSymm iso)

/-- The two unary marks, both ways. -/
def isoU0U1 : Iso U0 U1 := isoSymm isoU1U0

/-- `U0` is isomorphic to itself (its one demand is sorted). -/
def U0_self : Iso U0 U0 := isoRefl U0 (by decide)

/-- The eight conjuncts of the Genesis theorem, named. -/
theorem minimum_not_unique_core : (Iso U0 BL → False) :=
  mu1_minimum_not_unique.2.2.2.2.2.2.2

theorem both_land :
    applyDelta R2L deltaU0 = some U0 ∧ applyDelta R2L deltaBL = some BL :=
  ⟨mu1_minimum_not_unique.2.2.2.2.2.1, mu1_minimum_not_unique.2.2.2.2.2.2.1⟩

theorem both_cost_two : deltaU0.length = 2 ∧ deltaBL.length = 2 := ⟨rfl, rfl⟩

/-- The mu2 components of the two minima, for Unit 22. -/
theorem aritySum_deltaU0 : aritySum deltaU0 = 1 := rfl
theorem aritySum_deltaBL : aritySum deltaBL = 2 := rfl

/-- The infinite family: the 1-ary mark is `U1`, and marks of distinct
arity are non-isomorphic (Genesis), instantiated at 1 and 2. -/
theorem markK_one : markK 1 = U1 := rfl
theorem mark1_not_iso_mark2 (iso : Iso (markK 1) (markK 2)) : False :=
  markK_pairwise_noniso 1 2 (by decide) iso

end Textbook.U21

#print axioms Textbook.U21.arity_invariant
#print axioms Textbook.U21.U0_not_iso_BL'
#print axioms Textbook.U21.isoSymm
#print axioms Textbook.U21.BL_not_iso_U0
#print axioms Textbook.U21.BD_not_iso_BL
#print axioms Textbook.U21.isoU0U1
#print axioms Textbook.U21.U0_self
#print axioms Textbook.U21.minimum_not_unique_core
#print axioms Textbook.U21.both_land
#print axioms Textbook.U21.both_cost_two
#print axioms Textbook.U21.aritySum_deltaU0
#print axioms Textbook.U21.aritySum_deltaBL
#print axioms Textbook.U21.markK_one
#print axioms Textbook.U21.mark1_not_iso_mark2
#print axioms Derivation.U0_not_iso_BL
#print axioms Derivation.mu1_minimum_not_unique
#print axioms Derivation.isoU1U0
#print axioms Derivation.markK_pairwise_noniso
"""

EXPECTED = {
    "Textbook.U21.arity_invariant": BOTH,
    "Textbook.U21.U0_not_iso_BL'": BOTH,
    "Textbook.U21.isoSymm": BOTH,
    "Textbook.U21.BL_not_iso_U0": BOTH,
    "Textbook.U21.BD_not_iso_BL": BOTH,
    "Textbook.U21.isoU0U1": BOTH,
    "Textbook.U21.U0_self": BOTH,
    "Textbook.U21.minimum_not_unique_core": BOTH,
    "Textbook.U21.both_land": BOTH,
    "Textbook.U21.both_cost_two": NONE,
    "Textbook.U21.aritySum_deltaU0": PROPEXT,
    "Textbook.U21.aritySum_deltaBL": PROPEXT,
    "Textbook.U21.markK_one": NONE,
    "Textbook.U21.mark1_not_iso_mark2": PROPEXT,
    "Derivation.U0_not_iso_BL": BOTH,
    "Derivation.mu1_minimum_not_unique": BOTH,
    "Derivation.isoU1U0": BOTH,
    "Derivation.markK_pairwise_noniso": PROPEXT,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U21"))
