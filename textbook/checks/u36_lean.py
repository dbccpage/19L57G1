"""Unit 36 check: kernel-check the book's Lean for Unit 36.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u36_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Ext

namespace Textbook.U36
open Derivation

/-- The same two marks, admitted in the two orders. -/
def twoA : Regime := ⟨2, [1, 1], [(0, [0]), (1, [1])], [], [(0, 1)]⟩
def twoB : Regime := ⟨2, [1, 1], [(1, [1]), (0, [0])], [], [(0, 1)]⟩

/-- As Lean regimes they are different. -/
theorem twoA_ne_twoB : twoA ≠ twoB := by decide

/-- As sets of admissions they are the same. -/
theorem twoA_ext_twoB : RegimeExt twoA twoB := by
  refine ⟨rfl, rfl, ?_, SetEq.rfl' _, SetEq.rfl' _⟩
  intro x
  simp only [twoA, twoB, List.mem_cons, List.not_mem_nil, or_false]
  exact or_comm

/-- So every observable agrees: derivability of a given instance, ... -/
theorem derivable_agrees : derivable twoA (0, [0]) ↔ derivable twoB (0, [0]) :=
  derivable_ext twoA_ext_twoB _

/-- ... collapse and separability of the pair, ... -/
theorem separable_agrees : separable twoA 0 1 ↔ separable twoB 0 1 :=
  separable_ext twoA_ext_twoB 0 1

/-- ... and validity of every response. -/
theorem valid_agrees (δ : List Item) :
    validResponse twoA 0 1 δ ↔ validResponse twoB 0 1 δ :=
  validResponse_ext twoA_ext_twoB 0 1 δ

/-- Duplicate admission is a no-op on the list, as on the Python set. -/
theorem dup_inst_noop : insertNew [((0 : Nat), [(0 : Nat)])] (0, [0]) = [(0, [0])] :=
  insertNew_of_mem (by simp)

/-- What `RegimeExt` does not quotient: the form table is compared as a
list, because a form's index is its name. -/
theorem form_order_matters :
    ¬ RegimeExt ⟨2, [1, 2], [], [], []⟩ ⟨2, [2, 1], [], [], []⟩ := by
  intro h
  have h2 := h.2.1
  simp at h2

/-- Nor the datum count: two data and three are never `RegimeExt`. -/
theorem data_count_matters :
    ¬ RegimeExt ⟨2, [], [], [], []⟩ ⟨3, [], [], [], []⟩ := by
  intro h
  have h1 := h.1
  simp at h1

/-- `RegimeExt` is reflexive and symmetric (Genesis); the book adds that
it is transitive, so it is an equivalence. -/
theorem RegimeExt.trans' {r s t : Regime} (h1 : RegimeExt r s) (h2 : RegimeExt s t) :
    RegimeExt r t :=
  ⟨h1.1.trans h2.1, h1.2.1.trans h2.2.1,
   fun x => (h1.2.2.1 x).trans (h2.2.2.1 x),
   fun x => (h1.2.2.2.1 x).trans (h2.2.2.2.1 x),
   fun x => (h1.2.2.2.2 x).trans (h2.2.2.2.2 x)⟩

/-- A raw duplicate demand changes the list but not its membership. -/
def repeatedDemand : Regime := { twoA with reqs := [(0, 1), (0, 1)] }

theorem repeated_demand_ext : RegimeExt twoA repeatedDemand := by
  refine ⟨rfl, rfl, SetEq.rfl' _, SetEq.rfl' _, ?_⟩
  intro q
  simp [twoA, repeatedDemand]

theorem repeated_demand_counts :
    twoA.reqs.length = 1 ∧ repeatedDemand.reqs.length = 2 := by decide

/-- Token-erased datum items have no token to deduplicate. -/
theorem two_new_data :
    applyDelta ⟨0, [], [], [], []⟩ [.newDatum, .newDatum] =
      some ⟨2, [], [], [], []⟩ := by decide

end Textbook.U36

#print axioms Textbook.U36.twoA_ne_twoB
#print axioms Textbook.U36.twoA_ext_twoB
#print axioms Textbook.U36.derivable_agrees
#print axioms Textbook.U36.separable_agrees
#print axioms Textbook.U36.valid_agrees
#print axioms Textbook.U36.dup_inst_noop
#print axioms Textbook.U36.form_order_matters
#print axioms Textbook.U36.data_count_matters
#print axioms Textbook.U36.RegimeExt.trans'
#print axioms Textbook.U36.repeated_demand_ext
#print axioms Textbook.U36.repeated_demand_counts
#print axioms Textbook.U36.two_new_data
#print axioms Derivation.derivable_ext
#print axioms Derivation.collapsed_ext
#print axioms Derivation.separable_ext
#print axioms Derivation.applyDelta_ext
#print axioms Derivation.validResponse_ext
"""

EXPECTED = {
    "Textbook.U36.twoA_ne_twoB": NONE,
    "Textbook.U36.twoA_ext_twoB": PROPEXT,
    "Textbook.U36.derivable_agrees": PROPEXT,
    "Textbook.U36.separable_agrees": PROPEXT,
    "Textbook.U36.valid_agrees": PROPEXT,
    "Textbook.U36.dup_inst_noop": PROPEXT,
    "Textbook.U36.form_order_matters": PROPEXT,
    "Textbook.U36.data_count_matters": PROPEXT,
    "Textbook.U36.RegimeExt.trans'": NONE,
    "Textbook.U36.repeated_demand_ext": PROPEXT,
    "Textbook.U36.repeated_demand_counts": NONE,
    "Textbook.U36.two_new_data": PROPEXT,
    "Derivation.derivable_ext": NONE,
    "Derivation.collapsed_ext": PROPEXT,
    "Derivation.separable_ext": PROPEXT,
    "Derivation.applyDelta_ext": PROPEXT,
    "Derivation.validResponse_ext": PROPEXT,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U36"))
