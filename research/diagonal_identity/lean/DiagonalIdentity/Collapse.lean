import Derivation.PrimDiff

/-!
# Finite collapse obstruction under protected irreflexivity

Inhabitant already in the sealed module: identifying the witnessed pair of
`PrimDiff.D2` along the constant map `Bool → Unit` is
`PrimDiff.FidelityObstruction PrimDiff.Irrefl`.  Binders are a relation, a
witnessed pair, and an identifying map.  There is no family
`Nat → (Nat → Fin c)` and the conclusion is not a missed sequence.

AuthorityEffect: None.
-/

namespace DiagonalIdentity.Collapse

/-- The constant map on `Bool` identifies the witnessed pair of `D2`.
AuthorityEffect: None. -/
theorem d2_constant_obstructs :
    PrimDiff.FidelityObstruction PrimDiff.Irrefl PrimDiff.D2
      (fun _ : Bool => ()) :=
  PrimDiff.obstruction_under_irrefl PrimDiff.D2_witness rfl

/-- The second conjunct of `obstruction_under_irrefl`: the pushforward is
not irreflexive.
AuthorityEffect: None. -/
theorem identifying_push_not_irrefl {α β : Type} {r : α → α → Prop}
    {a b : α} (h : r a b) {k : α → β} (hk : k a = k b) :
    ¬ PrimDiff.Irrefl (PrimDiff.Push r k) :=
  (PrimDiff.obstruction_under_irrefl h hk).2

/-- Identifying a witnessed pair makes the pushforward hold of a self-pair.
AuthorityEffect: None. -/
theorem identifying_push_self_loop {α β : Type} {r : α → α → Prop}
    {a b : α} (h : r a b) {k : α → β} (hk : k a = k b) :
    PrimDiff.Push r k (k a) (k a) :=
  hk ▸ PrimDiff.push_witness h k

end DiagonalIdentity.Collapse
