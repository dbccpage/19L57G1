import NaturalSections

/-!
# The phase receiver: one value group built from every rotation layer

The slot-exchange rung graded each oriented `k`-slot action by
`Fin (k+1)`.  This module constructs the single value group that
receives every layer compatibly, FROM the layers: `QOne` is the
quotient of indexed pairs `(n, k)` -- read as the `n`-th part of
`k + 1` -- under cross-multiplication equivalence, with addition by
cross-multiplication.  No completion, no order, and no ambient object
are declared anywhere; the receiver is the union of the insides.

Proved here, as pre-registered in `STATUS.md`:

* RC1 -- `QOne` is a commutative group (`add_comm`, `add_assoc`,
  `add_zero`, `add_neg`), with the group laws that are raw pair
  identities proved at the raw level and only the inverse law using
  the quotient relation.
* RC2 -- the layers embed additively (`layer_add`) and compatibly:
  each layer factors through every multiple (`layer_mul_compat`).
* RC3 -- every element of `QOne` is `layer k c` for some `k` and `c`
  (`receiver_is_union`): nothing lives in the receiver beyond the
  layers.
* RC4 -- the two-part layer recovers the sign story: `half + half = 0`
  and `half ≠ 0`, the latter through `Quot.exact` and the collapse of
  the generated equivalence onto the relation.

Deliberately NOT claimed: any universal property of the receiver
(OPEN), and any passage to a connected or complete carrier (a separate
rung with a priced declaration).  AuthorityEffect: None.
-/

namespace NaturalSections
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

/-- Raw addition by cross-multiplication; the returned index stores the
product of the part counts, minus one. -/
def rawAdd (a b : Raw) : Raw :=
  (a.1 * den b.2 + b.1 * den a.2, a.2 * b.2 + a.2 + b.2)

theorem den_rawAdd (a b : Raw) :
    den (rawAdd a b).2 = den a.2 * den b.2 := by
  simp [rawAdd, den, Nat.mul_add, Nat.add_mul] <;> omega

/-- The raw inverse: `n` parts of `k + 1` is undone by `n * k` more,
because `n + n * k = n * (k + 1)`, a whole number of turns.  No
remainder computation is needed. -/
def rawNeg (a : Raw) : Raw := (a.1 * a.2, a.2)

/-- Addition respects the relation on the left. -/
theorem rawAdd_left_congr {a a' : Raw} (b : Raw) (h : R a a') :
    R (rawAdd a b) (rawAdd a' b) := by
  obtain ⟨t, ht⟩ := h
  refine ⟨t, ?_⟩
  have key :
      ((rawAdd a b).1 : Int) * den (rawAdd a' b).2
          - ((rawAdd a' b).1 : Int) * den (rawAdd a b).2
        = ((a.1 : Int) * den a'.2 - (a'.1 : Int) * den a.2)
          * ((den b.2 : Int) * den b.2) := by
    simp [rawAdd, rawNeg, den_rawAdd, den, Int.natCast_add, Int.natCast_mul,
      Int.natCast_one, Int.mul_sub, Int.sub_mul, Int.mul_add, Int.add_mul,
      Int.mul_comm, Int.mul_left_comm, Int.mul_assoc] <;> omega
  rw [key, ht]
  simp [rawAdd, rawNeg, den_rawAdd, den, Int.natCast_add, Int.natCast_mul,
      Int.natCast_one, Int.mul_sub, Int.sub_mul, Int.mul_add, Int.add_mul,
      Int.mul_comm, Int.mul_left_comm, Int.mul_assoc] <;> omega

/-- Addition respects the relation on the right. -/
theorem rawAdd_right_congr (a : Raw) {b b' : Raw} (h : R b b') :
    R (rawAdd a b) (rawAdd a b') := by
  obtain ⟨t, ht⟩ := h
  refine ⟨t, ?_⟩
  have key :
      ((rawAdd a b).1 : Int) * den (rawAdd a b').2
          - ((rawAdd a b').1 : Int) * den (rawAdd a b).2
        = ((b.1 : Int) * den b'.2 - (b'.1 : Int) * den b.2)
          * ((den a.2 : Int) * den a.2) := by
    simp [rawAdd, rawNeg, den_rawAdd, den, Int.natCast_add, Int.natCast_mul,
      Int.natCast_one, Int.mul_sub, Int.sub_mul, Int.mul_add, Int.add_mul,
      Int.mul_comm, Int.mul_left_comm, Int.mul_assoc] <;> omega
  rw [key, ht]
  simp [rawAdd, rawNeg, den_rawAdd, den, Int.natCast_add, Int.natCast_mul,
      Int.natCast_one, Int.mul_sub, Int.sub_mul, Int.mul_add, Int.add_mul,
      Int.mul_comm, Int.mul_left_comm, Int.mul_assoc] <;> omega

/-- Receiver addition, lifted argument by argument. -/
def add (x y : QOne) : QOne :=
  Quotient.lift
    (fun a =>
      Quotient.lift (fun b => mk (rawAdd a b))
        (fun b b' h => Quotient.sound (rawAdd_right_congr a h)) y)
    (fun a a' h => by
      induction y using Quotient.ind with
      | _ b => exact Quotient.sound (rawAdd_left_congr b h))
    x

def zero : QOne := mk (0, 0)

/-- RC1, commutativity: a raw pair identity -- the two cross sums are
the same numbers. -/
theorem add_comm (x y : QOne) : add x y = add y x := by
  induction x using Quotient.ind with
  | _ a =>
    induction y using Quotient.ind with
    | _ b =>
      show mk (rawAdd a b) = mk (rawAdd b a)
      have h : rawAdd a b = rawAdd b a := by
        simp [rawAdd, den, Nat.mul_comm, Nat.mul_left_comm, Nat.add_comm,
          Nat.add_left_comm] <;> omega
      rw [h]

/-- RC1, associativity: a raw pair identity after distribution. -/
theorem add_assoc (x y z : QOne) :
    add (add x y) z = add x (add y z) := by
  induction x using Quotient.ind with
  | _ a =>
    induction y using Quotient.ind with
    | _ b =>
      induction z using Quotient.ind with
      | _ c =>
        show mk (rawAdd (rawAdd a b) c) = mk (rawAdd a (rawAdd b c))
        have h : rawAdd (rawAdd a b) c = rawAdd a (rawAdd b c) := by
          simp [rawAdd, den, Nat.mul_add, Nat.add_mul, Nat.mul_comm,
            Nat.mul_left_comm, Nat.mul_assoc]
          constructor
          · omega
          · omega
        rw [h]

/-- RC1, the zero law: a raw pair identity. -/
theorem add_zero (x : QOne) : add x zero = x := by
  induction x using Quotient.ind with
  | _ a =>
    show mk (rawAdd a (0, 0)) = mk a
    have h : rawAdd a (0, 0) = a := by
      simp [rawAdd, den]
    rw [h]

theorem rawNeg_congr {a a' : Raw} (h : R a a') : R (rawNeg a) (rawNeg a') := by
  obtain ⟨t, ht⟩ := h
  refine ⟨(a.1 : Int) - a'.1 - t, ?_⟩
  have key :
      ((rawNeg a).1 : Int) * den (rawNeg a').2
          - ((rawNeg a').1 : Int) * den (rawNeg a).2
        = ((a.1 : Int) - a'.1) * ((den a.2 : Int) * den a'.2)
          - ((a.1 : Int) * den a'.2 - (a'.1 : Int) * den a.2) := by
    simp [rawAdd, rawNeg, den_rawAdd, den, Int.natCast_add, Int.natCast_mul,
      Int.natCast_one, Int.mul_sub, Int.sub_mul, Int.mul_add, Int.add_mul,
      Int.mul_comm, Int.mul_left_comm, Int.mul_assoc] <;> omega
  rw [key, ht]
  simp [rawAdd, rawNeg, den_rawAdd, den, Int.natCast_add, Int.natCast_mul,
      Int.natCast_one, Int.mul_sub, Int.sub_mul, Int.mul_add, Int.add_mul,
      Int.mul_comm, Int.mul_left_comm, Int.mul_assoc] <;> omega

def neg (x : QOne) : QOne :=
  Quotient.lift (fun a => mk (rawNeg a))
    (fun _ _ h => Quotient.sound (rawNeg_congr h)) x

/-- RC1, the inverse law: adding the complement lands in the class of
zero, with the explicit witness `n`. -/
theorem add_neg (x : QOne) : add x (neg x) = zero := by
  induction x using Quotient.ind with
  | _ a =>
    show mk (rawAdd a (rawNeg a)) = mk (0, 0)
    apply Quotient.sound
    refine ⟨(a.1 : Int), ?_⟩
    simp [rawAdd, rawNeg, den_rawAdd, den, Int.natCast_add, Int.natCast_mul,
      Int.natCast_one, Int.mul_sub, Int.sub_mul, Int.mul_add, Int.add_mul,
      Int.mul_comm, Int.mul_left_comm, Int.mul_assoc] <;> omega

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

/-- RC2, additivity: the layer embedding turns `Fin` addition into
receiver addition.  The sum of two parts wraps at most once, so the
witness is `0` or `-1` by cases -- no division enters. -/
theorem layer_add (k : Nat) (c d : Fin (k + 1)) :
    layer k (c + d) = add (layer k c) (layer k d) := by
  have hc : c.val < k + 1 := c.isLt
  have hd : d.val < k + 1 := d.isLt
  rcases Nat.lt_or_ge (c.val + d.val) (k + 1) with hlt | hge
  · apply Quotient.sound
    refine ⟨0, ?_⟩
    have hval : (((c + d : Fin (k + 1)).val : Nat) : Int)
        = (c.val : Int) + d.val := by
      rw [Fin.val_add, Nat.mod_eq_of_lt hlt]
      omega
    rw [hval]
    simp [rawAdd, den, Int.natCast_add, Int.natCast_mul, Int.natCast_one,
      Int.mul_add, Int.add_mul, Int.mul_sub, Int.sub_mul, Int.mul_comm,
      Int.mul_left_comm, Int.mul_assoc] <;> omega
  · apply Quotient.sound
    refine ⟨-1, ?_⟩
    have hval : (((c + d : Fin (k + 1)).val : Nat) : Int)
        = (c.val : Int) + d.val - (k + 1) := by
      rw [Fin.val_add, Nat.mod_eq_sub_mod hge,
        Nat.mod_eq_of_lt (by omega)]
      omega
    rw [hval]
    simp [rawAdd, den, Int.natCast_add, Int.natCast_mul, Int.natCast_one,
      Int.mul_add, Int.add_mul, Int.mul_sub, Int.sub_mul, Int.mul_comm,
      Int.mul_left_comm, Int.mul_assoc] <;> omega

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

/-- RC4: the two-part layer -- one part of two. -/
def half : QOne := layer 1 ⟨1, by omega⟩

/-- RC4: the sign story's addition law sits inside the receiver --
half plus half is zero, because half is its own inverse at the raw
level (`rawNeg (1, 1) = (1, 1)`). -/
theorem half_add_half : add half half = zero := by
  have h : neg half = half := rfl
  rw [← h]
  exact add_neg half

/-- RC4: half is not zero -- through `Quotient.exact`, the relation
would force two to divide one. -/
theorem half_ne_zero : half ≠ zero := by
  intro h
  have hr : R (1, 1) (0, 0) := Quotient.exact h
  obtain ⟨t, ht⟩ := hr
  simp [den] at ht
  omega

end Receiver
end NaturalSections
