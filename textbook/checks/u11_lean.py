"""Unit 11 check: kernel-check the book's Lean for Unit 11.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u11_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Bridge

namespace Textbook.U11
open Derivation Bridge

/-- The empty token-aware state. -/
def start : TRegime := ⟨[], [], [], [], []⟩

/-- Every event that is not a datum admission is single-token for any
token, because the hypothesis of `SingleTok` is never met. -/
theorem supply_singleTok (t0 tok : Nat) : SingleTok t0 (.supply tok) :=
  fun _ h => nomatch h

/-- Admitting the chosen token is single-token. -/
theorem admit_same_singleTok (t0 : Nat) : SingleTok t0 (.admitDatum t0) :=
  fun _ h => by cases h; rfl

/-- Admitting another token is not. -/
theorem admit_other_not_singleTok : ¬ SingleTok 0 (.admitDatum 1) :=
  fun h => Nat.one_ne_zero (h 1 rfl)

/-- The empty state satisfies the invariant: its store is empty. -/
theorem start_atMostTok (t0 : Nat) : AtMostTok t0 start := Or.inl rfl

/-- Re-admitting the same token three times leaves one entry. -/
theorem readmit_three : replayT [.admitDatum 0, .admitDatum 0, .admitDatum 0]
    start = some ⟨[0], [], [], [], []⟩ := by decide

/-- The seven-event history that re-supplies and re-admits ⟨⟩ and admits
a form and a self-instance: still one datum. -/
def busy : List TEvent :=
  [.supply 0, .admitDatum 0, .supply 0, .admitDatum 0, .admitForm 2,
   .admitInst 0 [0, 0], .admitDatum 0]

theorem busy_all_singleTok : ∀ e ∈ busy, SingleTok 0 e := by decide

theorem busy_replays :
    replayT busy start = some ⟨[0], [2], [(0, [0, 0])], [], []⟩ := by decide

/-- The Genesis theorem applied to `busy`: at most one token. -/
theorem busy_bound : (⟨[0], [2], [(0, [0, 0])], [], []⟩ : TRegime).tokens.length ≤ 1 :=
  single_token_carrier_bound 0 busy busy_all_singleTok (start_atMostTok 0)
    busy_replays

/-- The bound is reached: one admission gives exactly one. -/
theorem bound_is_sharp :
    ∃ res, replayT [.admitDatum 0] start = some res ∧ res.tokens.length = 1 :=
  ⟨⟨[0], [], [], [], []⟩, by decide, rfl⟩

/-- Without the hypothesis the conclusion fails: `hist01` admits two
tokens and reaches a store of length two. -/
theorem two_tokens_escape :
    ∃ res, replayT hist01 start = some res ∧ res.tokens.length = 2 :=
  ⟨⟨[0, 1], [], [], [], []⟩, by decide, rfl⟩

/-- And `hist01` is indeed not single-token for token 0. -/
theorem hist01_not_singleTok : ¬ ∀ e ∈ hist01, SingleTok 0 e := by decide

/-- The invariant step, re-proved for the one case that matters: admitting
the chosen token. The other five cases copy the token store unchanged. -/
theorem admit_keeps_atMostTok {t0 : Nat} {t t' : TRegime}
    (ht : AtMostTok t0 t) (hs : stepT t (.admitDatum t0) = some t') :
    AtMostTok t0 t' := by
  by_cases hmem : t0 ∈ t.tokens
  · simp only [stepT] at hs
    rw [if_pos hmem] at hs
    cases Option.some.inj hs
    exact ht
  · simp only [stepT] at hs
    rw [if_neg hmem] at hs
    cases Option.some.inj hs
    cases ht with
    | inl h0 =>
        right
        show t.tokens ++ [t0] = [t0]
        rw [h0]
        rfl
    | inr h1 =>
        exact absurd (by rw [h1]; simp) hmem

/-- The invariant gives the bound: a store that is `[]` or `[t0]` has at
most one entry. -/
theorem atMostTok_length {t0 : Nat} {t : TRegime} (ht : AtMostTok t0 t) :
    t.tokens.length ≤ 1 := by
  cases ht with
  | inl h0 => rw [h0]; exact Nat.zero_le 1
  | inr h1 => rw [h1]; exact Nat.le_refl 1

/-- A single-token history condition alone gives no bound on an arbitrary base. -/
def twoBase : TRegime := ⟨[5, 7], [], [], [], []⟩

theorem initial_guard_needed :
    replayT [] twoBase = some twoBase ∧ twoBase.tokens.length = 2 ∧
    (∀ e ∈ ([] : List TEvent), SingleTok 5 e) ∧ ¬ AtMostTok 5 twoBase := by
  refine ⟨rfl, rfl, ?_, ?_⟩
  · simp
  · simp [AtMostTok, twoBase]

end Textbook.U11

#print axioms Textbook.U11.supply_singleTok
#print axioms Textbook.U11.admit_same_singleTok
#print axioms Textbook.U11.admit_other_not_singleTok
#print axioms Textbook.U11.start_atMostTok
#print axioms Textbook.U11.readmit_three
#print axioms Textbook.U11.busy_all_singleTok
#print axioms Textbook.U11.busy_replays
#print axioms Textbook.U11.busy_bound
#print axioms Textbook.U11.bound_is_sharp
#print axioms Textbook.U11.two_tokens_escape
#print axioms Textbook.U11.hist01_not_singleTok
#print axioms Textbook.U11.admit_keeps_atMostTok
#print axioms Textbook.U11.atMostTok_length
#print axioms Textbook.U11.initial_guard_needed
#print axioms Bridge.stepT_preserves_atMostTok
#print axioms Bridge.single_token_carrier_bound
"""

EXPECTED = {
    "Textbook.U11.supply_singleTok": NONE,
    "Textbook.U11.admit_same_singleTok": NONE,
    "Textbook.U11.admit_other_not_singleTok": PROPEXT,
    "Textbook.U11.start_atMostTok": NONE,
    "Textbook.U11.readmit_three": BOTH,
    "Textbook.U11.busy_all_singleTok": NONE,
    "Textbook.U11.busy_replays": BOTH,
    "Textbook.U11.busy_bound": BOTH,
    "Textbook.U11.bound_is_sharp": BOTH,
    "Textbook.U11.two_tokens_escape": BOTH,
    "Textbook.U11.hist01_not_singleTok": NONE,
    "Textbook.U11.admit_keeps_atMostTok": BOTH,
    "Textbook.U11.atMostTok_length": NONE,
    "Textbook.U11.initial_guard_needed": BOTH,
    "Bridge.stepT_preserves_atMostTok": BOTH,
    "Bridge.single_token_carrier_bound": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U11"))
