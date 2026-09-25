import SecondIso.Kernel

/-!
# The track-one sibling's stake and demand slice, reconstructed verbatim

PIN NOTE (whole file).  Every declaration below is reproduced VERBATIM
from the committed package of the track-one sibling rung,
`research/second_nofirst/lean/SecondNoFirst/`, at the blobs recorded in
`SOURCE_MANIFEST.json`, at the snapshot recorded there: from `Stake.lean`,
lines forty-one through one hundred and twenty-three -- the label, the
two-sided stake, the three constant stakes, honour and the demand
predicate over the sealed regime; and from `NoFirst.lean`, lines one
hundred and ninety-one through two hundred and three -- the two
constructive readings of collapse against separability.

The only changes are the outer namespace, which flattens that package's
namespaces into one, and the file-level doc comment, which is this
file's own.  Declaration doc comments and proofs are the sibling's,
unedited.  `test_reconstruction.py` compares this file declaration by
declaration with the pinned blobs AT THE SNAPSHOT.

What a pin proves: that the sibling source did not move.  A theorem
reconstructed here is the sibling's result, classed RECONSTRUCTION in the
census, and is never counted as this rung's content.

AuthorityEffect: None.
-/

namespace SecondIso
namespace Inherited

open SecondIso.Sealed

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

/-- Collapse rules out separability, constructively. -/
theorem collapsed_not_separable {r : Regime} {d d' : Nat}
    (h : collapsed r d d') : ¬ separable r d d' :=
  fun ⟨c, hw, hne⟩ => hne (h c hw)

/-- Failing to separate is being collapsed: derivability is decidable, so
the double negation is eliminated without any choice. -/
theorem collapsed_of_not_separable {r : Regime} {d d' : Nat}
    (h : ¬ separable r d d') : collapsed r d d' := by
  intro c hw
  by_cases hd : (derivable r (plug c d) ↔ derivable r (plug c d'))
  · exact hd
  · exact absurd ⟨c, hw, hd⟩ h

end Inherited
end SecondIso
