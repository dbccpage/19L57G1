/-!
# The receiver, reconstructed verbatim from the pinned source

PIN NOTE.  Every definition and theorem in this file is reproduced
verbatim from `research/natural_sections/lean/NaturalSections/PhaseReceiver.lean`
at blob `ba88fa7cfba02a49d7d582f8a48aee56322e53c2` (snapshot
`f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be` of `main`, pinned in
`SOURCE_MANIFEST.json`).  The one change is the outer namespace:
`FreshCharacters` in place of the sibling's, so that this package stays
self-contained and imports nothing from a sibling or sealed package.  The
receiver's group laws (`add`, `neg`, `zero` and their theorems) are not
needed by the observer and are not reproduced.  Nothing here is claimed as
original: these are CONDITIONAL_THEOREM citations into the pinned packet,
compiled here so that the observer's theorems can be stated against the
pinned definitions themselves.  AuthorityEffect: None.
-/

namespace FreshCharacters
namespace Receiver

/-- Indexed pairs: `(n, k)` stands for the `n`-th part of `k + 1`. -/
abbrev Raw : Type := Nat × Nat

/-- The stored index plus one -- the part count of the layer. -/
def den (k : Nat) : Nat := k + 1

/-- Cross-multiplication equivalence: `(n₁, k₁)` and `(n₂, k₂)` name
the same receiver element when the cross difference is an integer
multiple of the product of the part counts. -/
def R (a b : Raw) : Prop :=
  ∃ t : Int,
    (a.1 : Int) * den b.2 - (b.1 : Int) * den a.2
      = t * ((den a.2 : Int) * den b.2)

theorem R_refl (a : Raw) : R a a := by
  refine ⟨0, ?_⟩
  simp [Int.sub_self]

theorem R_symm {a b : Raw} (h : R a b) : R b a := by
  obtain ⟨t, ht⟩ := h
  refine ⟨-t, ?_⟩
  have hswap : (b.1 : Int) * den a.2 - (a.1 : Int) * den b.2
      = -((a.1 : Int) * den b.2 - (b.1 : Int) * den a.2) := by
    omega
  rw [hswap, ht]
  rw [Int.mul_comm (den a.2 : Int) (den b.2 : Int)]
  rw [Int.neg_mul]

/-- Cancellation of a nonzero left factor over the integers,
self-contained on `Int.mul_eq_zero`. -/
theorem int_left_cancel {a b c : Int} (ha : a ≠ 0) (h : a * b = a * c) :
    b = c := by
  have hz : a * (b - c) = 0 := by
    rw [Int.mul_sub, h]
    omega
  rcases Int.mul_eq_zero.mp hz with h0 | h0
  · exact absurd h0 ha
  · omega

theorem den_int_ne_zero (k : Nat) : (den k : Int) ≠ 0 := by
  simp [den]
  omega

theorem R_trans {a b c : Raw} (hab : R a b) (hbc : R b c) : R a c := by
  obtain ⟨t, ht⟩ := hab
  obtain ⟨s, hs⟩ := hbc
  refine ⟨t + s, ?_⟩
  have h1 : ((a.1 : Int) * den b.2 - (b.1 : Int) * den a.2) * den c.2
      = t * ((den a.2 : Int) * den b.2) * den c.2 := by rw [ht]
  have h2 : ((b.1 : Int) * den c.2 - (c.1 : Int) * den b.2) * den a.2
      = s * ((den b.2 : Int) * den c.2) * den a.2 := by rw [hs]
  apply int_left_cancel (den_int_ne_zero b.2)
  have expand :
      (den b.2 : Int)
          * ((a.1 : Int) * den c.2 - (c.1 : Int) * den a.2)
        = ((a.1 : Int) * den b.2 - (b.1 : Int) * den a.2) * den c.2
          + ((b.1 : Int) * den c.2 - (c.1 : Int) * den b.2) * den a.2 := by
    simp [Int.mul_sub, Int.sub_mul, Int.mul_comm, Int.mul_left_comm,
      Int.mul_assoc] <;> omega
  rw [expand, h1, h2]
  simp [den, Int.natCast_add, Int.natCast_mul, Int.natCast_one,
    Int.mul_add, Int.add_mul, Int.mul_comm, Int.mul_left_comm,
    Int.mul_assoc] <;> omega

instance rSetoid : Setoid Raw :=
  ⟨R, ⟨R_refl, fun h => R_symm h, fun h1 h2 => R_trans h1 h2⟩⟩

/-- The receiver: raw pairs up to cross-multiplication equivalence. -/
def QOne : Type := Quotient rSetoid

def mk (a : Raw) : QOne := Quotient.mk rSetoid a

/-- RC2: the `k`-th layer's embedding -- `c` parts of `k + 1`. -/
def layer (k : Nat) (c : Fin (k + 1)) : QOne := mk (c.val, k)

/-- RC2, compatibility: each layer factors through every multiple --
`c` parts of `k + 1` is `c * (m + 1)` parts of `(k + 1) * (m + 1)`,
with cross difference literally zero. -/
theorem layer_mul_compat (k m : Nat) (c : Fin (k + 1)) :
    layer k c = mk (c.val * (m + 1), k * m + k + m) := by
  apply Quotient.sound
  refine ⟨0, ?_⟩
  simp [den, Int.natCast_add, Int.natCast_mul, Int.natCast_one,
    Int.mul_add, Int.add_mul, Int.mul_comm, Int.mul_left_comm,
    Int.mul_assoc] <;> omega

/-- RC3: the receiver is exactly the union of the layers -- every
element is `layer k c` for some `k` and some `c`. -/
theorem receiver_is_union (x : QOne) :
    ∃ (k : Nat) (c : Fin (k + 1)), layer k c = x := by
  induction x using Quotient.ind with
  | _ a =>
    obtain ⟨q, hq⟩ : ∃ q, a.1 / den a.2 = q := ⟨_, rfl⟩
    obtain ⟨r, hr⟩ : ∃ r, a.1 % den a.2 = r := ⟨_, rfl⟩
    refine ⟨a.2, ⟨a.1 % den a.2, Nat.mod_lt _ (by simp [den] <;> omega)⟩, ?_⟩
    apply Quotient.sound
    refine ⟨-(q : Int), ?_⟩
    have hdm := Nat.div_add_mod a.1 (den a.2)
    rw [hq, hr] at hdm
    have hNat : a.1 * den a.2 = r * den a.2 + q * (den a.2 * den a.2) := by
      have e := congrArg (fun n => n * den a.2) hdm
      simp [Nat.mul_add, Nat.add_mul, Nat.mul_comm, Nat.mul_left_comm,
        Nat.mul_assoc] at e ⊢ <;> omega
    have hInt : ((a.1 * den a.2 : Nat) : Int)
        = ((r * den a.2 + q * (den a.2 * den a.2) : Nat) : Int) := by
      rw [hNat]
    simp only [Int.natCast_add, Int.natCast_mul] at hInt
    show ((a.1 % den a.2 : Nat) : Int) * den a.2 - (a.1 : Int) * den a.2
        = -(q : Int) * ((den a.2 : Int) * den a.2)
    rw [hr]
    simp [Int.neg_mul, Int.mul_neg, Int.mul_comm, Int.mul_left_comm,
      Int.mul_assoc] at hInt ⊢ <;> omega

end Receiver
end FreshCharacters
