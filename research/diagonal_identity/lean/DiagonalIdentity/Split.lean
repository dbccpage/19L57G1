import DiagonalIdentity.Covering
import DiagonalIdentity.Collapse

/-!
# Typed split: covering-miss and identifying-push, simultaneously true

The covering theorems quantify a family of sequences (or threads) and miss
one.  The collapse theorems quantify one relation and one identifying map
and conclude that `Push` violates `Irrefl`.  Both families of facts hold.
Their conjunction is inhabited because the types share no data: neither
recodes the other.

This module does **not** prove an identification of
`PrimDiff.obstruction_under_irrefl` with `Covering.seq_uncountable`.
A closed `Prop`-iff of "both hold" is true and is not a typed identity.
A looser common schema that specialises to both remains OPEN.

AuthorityEffect: None.
-/

namespace DiagonalIdentity.Split

open DiagonalIdentity.Covering
open DiagonalIdentity.Collapse

/-- Collapse-yes and covering-no, already inhabited in the two source
families: `D2` collapsed to `Unit`, and `diagSeq_diff_at`.
AuthorityEffect: None. -/
theorem collapse_yes_covering_no :
    PrimDiff.FidelityObstruction PrimDiff.Irrefl PrimDiff.D2
      (fun _ : Bool => ()) ∧
    (∀ (k : Nat) (hk : 2 ≤ k) (S : Nat → (Nat → Fin k)) (n : Nat),
      diagSeq k hk S n ≠ S n n) :=
  ⟨d2_constant_obstructs, fun k hk S n => diagSeq_diff_at k hk S n⟩

/-- Conjunction of the existing covering-miss facts with the existing
identifying-push facts.  Not an `Iff` of the two theorem types.
AuthorityEffect: None. -/
theorem family_miss_and_identifying_push :
    (∀ f : Nat → (Nat → Bool), ∃ d : Nat → Bool, ∀ n, f n ≠ d) ∧
    (∀ (c : Nat) (hc : 2 ≤ c) (S : Nat → (Nat → Fin c)),
      ∃ d : Nat → Fin c, ∀ n, S n ≠ d) ∧
    (∀ (c : Nat) (hc : 2 ≤ c) (T : Nat → Limits.Thread c),
      ∃ t : Limits.Thread c, ∀ n, T n ≠ t) ∧
    (∀ {α β : Type} {r : α → α → Prop} {a b : α} (h : r a b)
        {k : α → β} (hk : k a = k b),
      ¬ PrimDiff.Irrefl (PrimDiff.Push r k)) ∧
    (∀ {α β : Type} {r : α → α → Prop} {a b : α} (h : r a b)
        {k : α → β} (hk : k a = k b),
      PrimDiff.Push r k (k a) (k a)) ∧
    PrimDiff.FidelityObstruction PrimDiff.Irrefl PrimDiff.D2
      (fun _ : Bool => ()) :=
  ⟨diagonal_bool,
   seq_uncountable,
   thread_uncountable,
   identifying_push_not_irrefl,
   identifying_push_self_loop,
   d2_constant_obstructs⟩

end DiagonalIdentity.Split
