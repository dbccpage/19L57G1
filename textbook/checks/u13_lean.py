"""Unit 13 check: kernel-check the book's Lean for Unit 13.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u13_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Bridge

namespace Textbook.U13
open Derivation Bridge

def start : TRegime := ⟨[], [], [], [], []⟩

/-- `hist01` reaches two tokens. -/
theorem hist01_two : replayT hist01 start = some ⟨[0, 1], [], [], [], []⟩ := by
  decide

/-- The Genesis theorem applied to `hist01` with `t0 = 0`: some event of
`hist01` admits a token other than 0. -/
theorem hist01_needs_other :
    ∃ e ∈ hist01, ∃ tok, e = TEvent.admitDatum tok ∧ tok ≠ 0 :=
  second_token_required 0 hist01 hist01_two (Nat.le_refl 2)

/-- The witness, named: the fourth event, `admitDatum 1`. -/
theorem hist01_witness :
    (TEvent.admitDatum 1) ∈ hist01 ∧ (1 : Nat) ≠ 0 :=
  ⟨by decide, Nat.one_ne_zero⟩

/-- The theorem holds for every choice of `t0`, so with `t0 = 1` the witness
is the other admission. -/
theorem hist01_needs_other_1 :
    ∃ e ∈ hist01, ∃ tok, e = TEvent.admitDatum tok ∧ tok ≠ 1 :=
  second_token_required 1 hist01 hist01_two (Nat.le_refl 2)

/-- Unit 11's `busy` history reaches one token, so the theorem's second
hypothesis fails and it says nothing; the bound says the store has at most
one entry. -/
def busy : List TEvent :=
  [.supply 0, .admitDatum 0, .supply 0, .admitDatum 0, .admitForm 2,
   .admitInst 0 [0, 0], .admitDatum 0]

theorem busy_not_two :
    ∀ res, replayT busy start = some res → ¬ 2 ≤ res.tokens.length := by
  intro res hr
  have hle := single_token_carrier_bound 0 busy (by decide) (Or.inl rfl) hr
  exact fun h2 => absurd (Nat.le_trans h2 hle) (by decide)

/-- The helper: a refuted bounded universal over a list has a named
counterexample in the list. Instance on a concrete list. -/
theorem helper_example :
    ∃ x ∈ [2, 4, 5, 6], ¬ (x % 2 = 0) :=
  exists_not_of_not_ball [2, 4, 5, 6] (fun x => x % 2 = 0) (by decide)

/-- The theorem re-proved with every step named. -/
theorem second_token_required' (t0 : Nat) (h : List TEvent)
    {res : TRegime}
    (hr : replayT h start = some res)
    (htwo : 2 ≤ res.tokens.length) :
    ∃ e ∈ h, ∃ tok, e = TEvent.admitDatum tok ∧ tok ≠ t0 := by
  cases hd : decide (∀ e ∈ h, SingleTok t0 e) with
  | true =>
      have hall : ∀ e ∈ h, SingleTok t0 e := of_decide_eq_true hd
      have hle : res.tokens.length ≤ 1 :=
        single_token_carrier_bound t0 h hall (Or.inl rfl) hr
      exact absurd (Nat.le_trans htwo hle) (by decide)
  | false =>
      have hall : ¬ ∀ e ∈ h, SingleTok t0 e := of_decide_eq_false hd
      have ⟨e, he, hnot⟩ := exists_not_of_not_ball h (SingleTok t0) hall
      refine ⟨e, he, ?_⟩
      cases e with
      | admitDatum tok =>
          refine ⟨tok, rfl, fun htok => ?_⟩
          exact hnot (fun tok' hh => by cases hh; exact htok)
      | supply tok => exact absurd (fun _ hh => nomatch hh) hnot
      | admitForm a => exact absurd (fun _ hh => nomatch hh) hnot
      | admitInst f args => exact absurd (fun _ hh => nomatch hh) hnot
      | admitRuleAll f => exact absurd (fun _ hh => nomatch hh) hnot
      | impose i j => exact absurd (fun _ hh => nomatch hh) hnot

end Textbook.U13

#print axioms Textbook.U13.hist01_two
#print axioms Textbook.U13.hist01_needs_other
#print axioms Textbook.U13.hist01_witness
#print axioms Textbook.U13.hist01_needs_other_1
#print axioms Textbook.U13.busy_not_two
#print axioms Textbook.U13.helper_example
#print axioms Textbook.U13.second_token_required'
#print axioms Bridge.second_token_required
#print axioms Bridge.exists_not_of_not_ball
"""

EXPECTED = {
    "Textbook.U13.hist01_two": BOTH,
    "Textbook.U13.hist01_needs_other": BOTH,
    "Textbook.U13.hist01_witness": PROPEXT,
    "Textbook.U13.hist01_needs_other_1": BOTH,
    "Textbook.U13.busy_not_two": BOTH,
    "Textbook.U13.helper_example": NONE,
    "Textbook.U13.second_token_required'": BOTH,
    "Bridge.second_token_required": BOTH,
    "Bridge.exists_not_of_not_ball": NONE,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U13"))
