import DiagonalIdentity.Covering

/-!
# Square-then-flip combinator, internal to the covering theorems

`diagBool` and `diagSeq` are the same combinator at two alphabets.  That
is a packaging of the covering theorems already restated in `Covering`.
It does not instantiate at the binders of `PrimDiff.obstruction_under_irrefl`
(a relation, a witnessed pair, and an identifying map).  A share-bridge
that would do so is not constructed here.

AuthorityEffect: None.
-/

namespace DiagonalIdentity.Combinator

open DiagonalIdentity.Covering

/-- Square evaluation followed by a pointwise endomap.
AuthorityEffect: None. -/
def diagFlip {ι α : Type} (flip : α → α) (F : ι → ι → α) : ι → α :=
  fun x => flip (F x x)

/-- `diagBool` is `diagFlip` at boolean negation.
AuthorityEffect: None. -/
theorem diagBool_is_diagFlip (f : Nat → (Nat → Bool)) :
    diagBool f = diagFlip (fun b => !b) f :=
  rfl

/-- `diagSeq` is `diagFlip` at `flipFin`.
AuthorityEffect: None. -/
theorem diagSeq_is_diagFlip (c : Nat) (hc : 2 ≤ c) (S : Nat → (Nat → Fin c)) :
    diagSeq c hc S = diagFlip (flipFin c hc) S :=
  rfl

/-- If `flip` has no fixed point, the combinator differs from every row.
AuthorityEffect: None. -/
theorem diagFlip_ne_row {ι α : Type} (flip : α → α)
    (hflip : ∀ a, flip a ≠ a) (F : ι → ι → α) (i : ι) :
    F i ≠ diagFlip flip F := by
  intro h
  have hi := congrFun h i
  exact (hflip (F i i)) hi.symm

end DiagonalIdentity.Combinator
