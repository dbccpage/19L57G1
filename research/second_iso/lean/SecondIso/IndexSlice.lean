import SecondIso.Inherited

/-!
# Rung three's prefix reading and first count, reconstructed verbatim

PIN NOTE (whole file).  Every declaration below is reproduced VERBATIM
from rung three's committed package, `research/second_index/lean/`, file
`SecondIndex/Index.lean`, at the blob recorded in `SOURCE_MANIFEST.json`,
at the snapshot recorded there: lines forty-three through sixty-one --
the regime a prefix reaches, and its values at the count zero and at the
full length; and lines eighty-three through one hundred and twenty --
carrying a demand, being a first count, quiet before the index, and the
uniqueness of the first count.

The only changes are the outer namespace and the file-level doc comment,
which is this file's own.  Declaration doc comments and proofs are rung
three's, unedited.  `test_reconstruction.py` compares this file
declaration by declaration with the pinned blob AT THE SNAPSHOT.

What a pin proves: that rung three's source did not move.  A theorem
reconstructed here is rung three's result, classed RECONSTRUCTION in the
census, and is never counted as this rung's content.

AuthorityEffect: None.
-/

namespace SecondIso
namespace IndexSlice

open SecondIso.Sealed
open SecondIso.Inherited

/-- The regime the prefix of `h` of length `k` reaches from `base`.  For
`k` above the length of `h` this is the regime the whole history reaches;
the index statements below never need that case, and none of them assumes
it away. -/
def stateAt (h : List Event) (base : Regime) (k : Nat) : Option Regime :=
  replayE (h.take k) base

/-- **stateAt_zero.**  The count zero names the base itself.
AT THE LEVEL OF A DEFINITION: the prefix of length zero is the empty
list, which replays to the base by `rfl`. -/
theorem stateAt_zero (h : List Event) (base : Regime) :
    stateAt h base 0 = some base := rfl

/-- **stateAt_full.**  The count equal to the length of the history names
the regime the whole history reaches. -/
theorem stateAt_full (h : List Event) (base : Regime) :
    stateAt h base h.length = replayE h base := by
  unfold stateAt
  rw [List.take_length]

/-- A regime CARRIES A DEMAND under a stake when some ordered pair of its
held data is a demand.  Read off the stake and the regime's own
observables and off nothing else. -/
def HasDemand (S : Stake) (r : Regime) : Prop :=
  ∃ i j, Demand S r i j

/-- `k` is a FIRST COUNT for the base, the history and the stake when the
prefix of length `k` reaches a regime carrying a demand and no shorter
prefix reaches one.  A proposition, not a function: nothing here asserts
that such a `k` exists, and `first_demand_unique` is what makes the
phrase "the first count" legitimate when one does. -/
def IsFirstDemand (S : Stake) (base : Regime) (h : List Event) (k : Nat) : Prop :=
  (∃ r, stateAt h base k = some r ∧ HasDemand S r) ∧
    (∀ m, m < k → ∀ r, stateAt h base m = some r → ¬ HasDemand S r)

/-- **quiet_before_the_index.**  Every prefix shorter than a first count
reaches a regime carrying no demand.
AT THE LEVEL OF A DEFINITION: the second conjunct of `IsFirstDemand`,
projected. -/
theorem quiet_before_the_index (S : Stake) (base : Regime) (h : List Event)
    (k m : Nat) (hfirst : IsFirstDemand S base h k) (hm : m < k) (r : Regime)
    (hr : stateAt h base m = some r) : ¬ HasDemand S r :=
  hfirst.2 m hm r hr

/-- **first_demand_unique.**  For one base, one history and one stake, at
most one count is a first count.  No decidability hypothesis, no
hypothesis on the events, no hypothesis on the base.  This is what
licenses the phrase "the first-demand index". -/
theorem first_demand_unique (S : Stake) (base : Regime) (h : List Event)
    (k k' : Nat) (hk : IsFirstDemand S base h k)
    (hk' : IsFirstDemand S base h k') : k = k' := by
  by_cases hlt : k < k'
  · obtain ⟨r, hr, hd⟩ := hk.1
    exact absurd hd (hk'.2 k hlt r hr)
  · by_cases hgt : k' < k
    · obtain ⟨r, hr, hd⟩ := hk'.1
      exact absurd hd (hk.2 k' hgt r hr)
    · omega

end IndexSlice
end SecondIso
