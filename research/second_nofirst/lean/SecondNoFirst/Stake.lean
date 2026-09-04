import SecondNoFirst.Kernel
import SecondNoFirst.Inherited

/-!
# Stage one: the two-sided stake, defined natively

This file is this rung's own object.  Nothing in it is reconstructed;
what it consumes is the reconstruction in `Kernel.lean` and
`Inherited.lean`, each carrying its own pin note.

A two-sided STAKE is a label on ordered index pairs, taking apart, same,
or free, and free on the diagonal by construction.  A regime HONOURS a
labelled pair when the label agrees with what the regime observes: apart
is honoured by separability, same by collapse, free always.  A DEMAND of a
stake at a regime is a labelled held pair the regime does not honour.

Three carriers appear in this rung and are kept apart, as FW-SCOPE
requires:

1. the sealed regime, this rung's primary carrier, on which `Demand` is a
   proposition because the sealed collapse and separability quantify over
   contexts;
2. the represented state of the pinned one-sided tree, on which a
   two-sided reading `demandsW` is a list, because that tree's separation
   test is a Boolean over a finite list of views;
3. the pinned one-sided `demands`, which is that tree's own definition.

`reconstruction_matches` below bridges carriers two and three.  It does
NOT bridge either to carrier one, and no theorem here claims that it
does; the missing bridge is named and priced as a leftover in
`STATUS.md`.

AuthorityEffect: None.
-/

namespace SecondNoFirst
namespace Stake

open SecondNoFirst.Sealed

/-! ## 1. The label and the stake -/

/-- The three values a stake assigns to an ordered pair of datum indices. -/
inductive Label where
  | apart
  | same
  | free
deriving Repr, DecidableEq

/-- A label is LABELLED when it constrains: apart and same do, free does
not. -/
def Label.labelled : Label → Bool
  | .free => false
  | _ => true

/-- A two-sided STAKE: a label on every ordered pair of datum indices,
present or future, free on the diagonal by construction.  It is declared
once, reads no state, and emits nothing. -/
structure Stake where
  label : Nat → Nat → Label
  diag : ∀ i, label i i = Label.free

/-- The stake that constrains nothing. -/
def freeStake : Stake where
  label _ _ := Label.free
  diag _ := rfl

/-- The stake that keeps every distinct pair apart. -/
def allApart : Stake where
  label i j := if i = j then Label.free else Label.apart
  diag i := by simp

/-- The stake that requires every distinct pair collapsed. -/
def allSame : Stake where
  label i j := if i = j then Label.free else Label.same
  diag i := by simp

/-- **stake_irrefl.**  No pair of a datum with itself carries a label.
AT THE LEVEL OF A DEFINITION: one rewrite of the structure field, then
`rfl`. -/
theorem stake_irrefl (S : Stake) (i : Nat) :
    (S.label i i).labelled = false := by
  rw [S.diag i]; rfl

/-! ## 2. Honour and demands over the sealed regime -/

/-- HONOUR of a labelled pair by a regime: apart is honoured by
separability, same by collapse, free always. -/
def honour (r : Regime) (l : Label) (i j : Nat) : Prop :=
  match l with
  | .apart => separable r i j
  | .same => collapsed r i j
  | .free => True

/-- A DEMAND of the stake `S` at the regime `r`: an ordered pair of held
data that `S` labels and that `r` does not honour. -/
def Demand (S : Stake) (r : Regime) (i j : Nat) : Prop :=
  i < j ∧ j < r.data ∧ (S.label i j).labelled = true ∧
    ¬ honour r (S.label i j) i j

/-- **demands_subset_labelled.**  Every demand is at a labelled pair.
AT THE LEVEL OF A DEFINITION: the labelling condition is a conjunct of
`Demand`, so this is a projection. -/
theorem demands_subset_labelled (S : Stake) (r : Regime) (i j : Nat)
    (h : Demand S r i j) : (S.label i j).labelled = true := h.2.2.1

/-- **free_stake_no_demand.**  Under the stake that labels every pair
free there is no demand at any regime, reachable or not.
AT THE LEVEL OF A DEFINITION: the label is `free` by unfolding, so the
labelling conjunct of `Demand` is `false = true`. -/
theorem free_stake_no_demand (r : Regime) (i j : Nat) :
    ¬ Demand freeStake r i j := by
  intro h
  exact absurd h.2.2.1 (by simp [freeStake, Label.labelled])

/-- A labelled pair is labelled apart or labelled same.  A three-way case
split with the free case discharged by the labelling condition. -/
theorem labelled_cases (l : Label) (h : l.labelled = true) :
    l = Label.apart ∨ l = Label.same := by
  cases l with
  | apart => exact Or.inl rfl
  | same => exact Or.inr rfl
  | free => exact absurd h (by simp [Label.labelled])

/-! ## 3. The bridge to the pinned one-sided stake

`demandsW` is the two-sided reading over the represented state: the same
three-valued label, with the pinned tree's Boolean separation test in
place of the sealed contexts.  It is a definition of this rung; the
carrier is the pinned tree's. -/

open SecondNoFirst.Inherited in
/-- Whether the represented state fails to honour the pair under `S`. -/
def dishonouredW (S : Stake) (w : World) (r : Req) : Bool :=
  match S.label r.1 r.2 with
  | .apart => !satB w r
  | .same => satB w r
  | .free => false

open SecondNoFirst.Inherited in
/-- The two-sided demands over the represented state. -/
def demandsW (S : Stake) (w : World) : List Req :=
  (pairsOf w.data).filter (dishonouredW S w)

open SecondNoFirst.Inherited in
/-- The stake a one-sided commitment induces: the pairs the commitment
holds are labelled apart, and every other pair is labelled free.  Nothing
is labelled same, because a one-sided commitment cannot ask for one. -/
def ofCommitment (C : Commitment) : Stake where
  label i j := if C.holds i j then Label.apart else Label.free
  diag i := by rw [C.irrefl i]; rfl

open SecondNoFirst.Inherited in
/-- **reconstruction_matches.**  Over the represented state, the two-sided
demands of the stake a one-sided commitment induces are, as a list and in
order, the pinned one-sided demands of that commitment -- at every
represented state, with no side hypothesis.  This bridges carriers two and
three of the three named at the head of this file, and bridges neither to
the sealed regime. -/
theorem reconstruction_matches (C : Commitment) (w : World) :
    demandsW (ofCommitment C) w = demands C w := by
  unfold demandsW demands
  refine List.filter_congr ?_
  intro r _
  show dishonouredW (ofCommitment C) w r = (C.holds r.1 r.2 && !satB w r)
  unfold dishonouredW ofCommitment
  cases hC : C.holds r.1 r.2 with
  | false => simp [hC]
  | true => simp [hC]

end Stake
end SecondNoFirst
