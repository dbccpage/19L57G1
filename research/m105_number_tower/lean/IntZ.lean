import Ordinal
import NNO

/-!
# Constructive Integer Ring ℤ (M106)

Constructive integer ring ℤ constructed via formal difference pairs (Grothendieck completion)
over `FinitarySubstrate.Ordinal` modulo cancellation equivalence using Lean's `Quotient` and `Quot.sound`.
Proves all ring axioms, canonical embedding ℕ ↪ ℤ, and representative independence.

AuthorityEffect: None.
Axiom boundary: strictly within {propext, Quot.sound}, zero Classical.choice, zero mathlib.
-/

namespace NumberTower

open FinitarySubstrate
open FinitarySubstrate.Ordinal

/-! ## 1. Cancellation and Algebraic Lemmas for Ordinal -/

/-- Right cancellation for ordinal addition: `a + c = b + c → a = b`. -/
theorem add_right_cancel {a b c : Ordinal} (h : add a c = add b c) : a = b := by
  have h2 := congrArg (fun x => sub x c) h
  rw [sub_add_cancel a c, sub_add_cancel b c] at h2
  exact h2

/-- Left cancellation for ordinal addition: `c + a = c + b → a = b`. -/
theorem add_left_cancel {a b c : Ordinal} (h : add c a = add c b) : a = b := by
  rw [add_comm c a, add_comm c b] at h
  exact add_right_cancel h

/-- Left distributivity of multiplication over addition: `a * (b + c) = a * b + a * c`. -/
theorem add_mul (a b c : Ordinal) : mul a (add b c) = add (mul a b) (mul a c) := by
  rw [mul_comm a (add b c), mul_add, mul_comm b a, mul_comm c a]

/-- Shuffle lemma: `(x + y) + (z + w) = (x + w) + (z + y)`. -/
theorem add_shuffle (x y z w : Ordinal) :
    add (add x y) (add z w) = add (add x w) (add z y) := by
  rw [add_assoc x y (add z w)]
  rw [← add_assoc y z w]
  rw [add_comm y z]
  rw [add_comm (add z y) w]
  rw [← add_assoc x w (add z y)]

/-- Shuffle lemma 2: `(x + y) + (z + w) = (x + z) + (y + w)`. -/
theorem add_shuffle2 (x y z w : Ordinal) :
    add (add x y) (add z w) = add (add x z) (add y w) := by
  rw [add_assoc x y (add z w)]
  rw [← add_assoc y z w]
  rw [add_comm y z]
  rw [add_assoc z y w]
  rw [← add_assoc x z (add y w)]

/-- Right cancellation for ordinal multiplication by a non-zero successor:
    `a * (succ k) = b * (succ k) → a = b`. -/
theorem mul_succ_right_cancel {a b k : Ordinal} (h : mul a (succ k) = mul b (succ k)) : a = b := by
  induction a generalizing b with
  | zero =>
      cases b with
      | zero => rfl
      | succ b' =>
          change zero = add (succ k) (mul b' (succ k)) at h
          change zero = succ (add k (mul b' (succ k))) at h
          nomatch h
  | succ a' ih =>
      cases b with
      | zero =>
          change add (succ k) (mul a' (succ k)) = zero at h
          change succ (add k (mul a' (succ k))) = zero at h
          nomatch h
      | succ b' =>
          change add (succ k) (mul a' (succ k)) = add (succ k) (mul b' (succ k)) at h
          have h_sub := add_left_cancel h
          have hab := ih h_sub
          rw [hab]

/-- Left cancellation for ordinal multiplication by a non-zero successor:
    `(succ k) * a = (succ k) * b → a = b`. -/
theorem mul_succ_left_cancel {a b k : Ordinal} (h : mul (succ k) a = mul (succ k) b) : a = b := by
  rw [mul_comm (succ k) a, mul_comm (succ k) b] at h
  exact mul_succ_right_cancel h

/-! ## 2. Difference Pairs and Equivalence Relation -/

/-- Equivalence relation on difference pairs:
    `(a, b) ~ (c, d) ↔ a + d = c + b` in `Ordinal`. -/
def zRel (p1 p2 : Ordinal × Ordinal) : Prop :=
  add p1.1 p2.2 = add p2.1 p1.2

/-- Reflexivity of `zRel`. -/
theorem zRel_refl (p : Ordinal × Ordinal) : zRel p p := rfl

/-- Symmetry of `zRel`. -/
theorem zRel_symm {p1 p2 : Ordinal × Ordinal} (h : zRel p1 p2) : zRel p2 p1 := h.symm

/-- Transitivity of `zRel`, proved constructively via addition cancellation. -/
theorem zRel_trans {p1 p2 p3 : Ordinal × Ordinal} (h1 : zRel p1 p2) (h2 : zRel p2 p3) : zRel p1 p3 := by
  dsimp [zRel] at *
  have hsum : add (add p1.1 p2.2) (add p2.1 p3.2) = add (add p2.1 p1.2) (add p3.1 p2.2) := by
    rw [h1, h2]
  have hl : add (add p1.1 p2.2) (add p2.1 p3.2) = add (add p1.1 p3.2) (add p2.1 p2.2) :=
    add_shuffle p1.1 p2.2 p2.1 p3.2
  have hr : add (add p2.1 p1.2) (add p3.1 p2.2) = add (add p3.1 p1.2) (add p2.1 p2.2) := by
    rw [add_comm (add p2.1 p1.2) (add p3.1 p2.2)]
    exact add_shuffle p3.1 p2.2 p2.1 p1.2
  rw [hl, hr] at hsum
  exact add_right_cancel hsum

/-- Setoid instance for difference pairs. -/
instance instSetoidIntPair : Setoid (Ordinal × Ordinal) where
  r := zRel
  iseqv := ⟨zRel_refl, zRel_symm, zRel_trans⟩

/-! ## 3. The Integer Quotient Type ℤ -/

/-- The constructive integer ring ℤ, defined as the quotient of difference pairs modulo cancellation. -/
def IntZ : Type := Quotient instSetoidIntPair

/-- Canonical constructor from difference pair. -/
def mkZ (a b : Ordinal) : IntZ :=
  Quotient.mk instSetoidIntPair (a, b)

/-- Quot.sound wrapper for integer equivalence. -/
theorem z_sound {p1 p2 : Ordinal × Ordinal} (h : zRel p1 p2) :
    Quotient.mk instSetoidIntPair p1 = Quotient.mk instSetoidIntPair p2 :=
  Quotient.sound h

/-- Exactness: equality of quotient integers implies difference pair equivalence.
    Depends only on `propext`. -/
theorem z_exact {p1 p2 : Ordinal × Ordinal}
    (h : Quotient.mk instSetoidIntPair p1 = Quotient.mk instSetoidIntPair p2) :
    zRel p1 p2 :=
  Quotient.exact h

/-! ## 4. Ring Operations on ℤ -/

/-- Additive identity: `0 = [(0, 0)]`. -/
def zeroZ : IntZ := mkZ Ordinal.zero Ordinal.zero

/-- Multiplicative identity: `1 = [(1, 0)]`. -/
def oneZ : IntZ := mkZ (Ordinal.succ Ordinal.zero) Ordinal.zero

/-- Negation on difference pairs: `-[(a, b)] = [(b, a)]`. -/
def negZ (z : IntZ) : IntZ :=
  Quotient.lift (fun (p : Ordinal × Ordinal) => mkZ p.2 p.1) (by
    intro p1 p2 h
    apply z_sound
    dsimp [zRel] at *
    rw [add_comm p1.2 p2.1, add_comm p2.2 p1.1]
    exact h.symm
  ) z

/-- Addition on difference pairs: `[(a, b)] + [(c, d)] = [(a + c, b + d)]`. -/
def addZ (z1 z2 : IntZ) : IntZ :=
  Quotient.lift₂ (fun p1 p2 => mkZ (add p1.1 p2.1) (add p1.2 p2.2)) (by
    intro a1 a2 b1 b2 h1 h2
    apply Quotient.sound
    have h1' : add a1.1 b1.2 = add b1.1 a1.2 := h1
    have h2' : add a2.1 b2.2 = add b2.1 a2.2 := h2
    change add (add a1.1 a2.1) (add b1.2 b2.2) = add (add b1.1 b2.1) (add a1.2 a2.2)
    have hl : add (add a1.1 a2.1) (add b1.2 b2.2) = add (add a1.1 b1.2) (add a2.1 b2.2) :=
      add_shuffle2 a1.1 a2.1 b1.2 b2.2
    have hr : add (add b1.1 b2.1) (add a1.2 a2.2) = add (add b1.1 a1.2) (add b2.1 a2.2) :=
      add_shuffle2 b1.1 b2.1 a1.2 a2.2
    rw [hl, hr, h1', h2']
  ) z1 z2

/-- Subtraction on integers: `z1 - z2 = z1 + (-z2)`. -/
def subZ (z1 z2 : IntZ) : IntZ :=
  addZ z1 (negZ z2)

/-- Helper for multiplication well-definedness under first argument equivalence. -/
theorem mul_well_defined_helper (a1 b1 a2 b2 c d : Ordinal) (h : add a1 b2 = add a2 b1) :
    add (add (mul a1 c) (mul b1 d)) (add (mul a2 d) (mul b2 c)) =
    add (add (mul a2 c) (mul b2 d)) (add (mul a1 d) (mul b1 c)) := by
  have hl : add (add (mul a1 c) (mul b1 d)) (add (mul a2 d) (mul b2 c)) =
            add (mul (add a1 b2) c) (mul (add a2 b1) d) := by
    rw [add_shuffle (mul a1 c) (mul b1 d) (mul a2 d) (mul b2 c)]
    rw [← mul_add, ← mul_add]
  have hr : add (add (mul a2 c) (mul b2 d)) (add (mul a1 d) (mul b1 c)) =
            add (mul (add a2 b1) c) (mul (add a1 b2) d) := by
    rw [add_shuffle (mul a2 c) (mul b2 d) (mul a1 d) (mul b1 c)]
    rw [← mul_add, ← mul_add]
  rw [hl, hr, h]

/-- Helper for multiplication well-definedness under second argument equivalence. -/
theorem mul_well_defined_helper2 (a b c1 d1 c2 d2 : Ordinal) (h : add c1 d2 = add c2 d1) :
    add (add (mul a c1) (mul b d1)) (add (mul a d2) (mul b c2)) =
    add (add (mul a c2) (mul b d2)) (add (mul a d1) (mul b c1)) := by
  have h1 : add (mul a c1) (mul b d1) = add (mul c1 a) (mul d1 b) := by rw [mul_comm a c1, mul_comm b d1]
  have h2 : add (mul a d2) (mul b c2) = add (mul c2 b) (mul d2 a) := by rw [mul_comm a d2, mul_comm b c2, add_comm]
  have h3 : add (mul a c2) (mul b d2) = add (mul c2 a) (mul d2 b) := by rw [mul_comm a c2, mul_comm b d2]
  have h4 : add (mul a d1) (mul b c1) = add (mul c1 b) (mul d1 a) := by rw [mul_comm a d1, mul_comm b c1, add_comm]
  rw [h1, h2, h3, h4]
  exact mul_well_defined_helper c1 d1 c2 d2 a b h

/-- Multiplication on difference pairs:
    `[(a, b)] * [(c, d)] = [(ac + bd, ad + bc)]`. -/
def mulZ (z1 z2 : IntZ) : IntZ :=
  Quotient.lift₂ (fun p1 p2 =>
    mkZ (add (mul p1.1 p2.1) (mul p1.2 p2.2)) (add (mul p1.1 p2.2) (mul p1.2 p2.1))
  ) (by
    intro a1 a2 b1 b2 h1 h2
    have step1 : mkZ (add (mul a1.1 a2.1) (mul a1.2 a2.2)) (add (mul a1.1 a2.2) (mul a1.2 a2.1)) =
                 mkZ (add (mul b1.1 a2.1) (mul b1.2 a2.2)) (add (mul b1.1 a2.2) (mul b1.2 a2.1)) := by
      apply Quotient.sound
      have h1' : add a1.1 b1.2 = add b1.1 a1.2 := h1
      exact mul_well_defined_helper a1.1 a1.2 b1.1 b1.2 a2.1 a2.2 h1'
    have step2 : mkZ (add (mul b1.1 a2.1) (mul b1.2 a2.2)) (add (mul b1.1 a2.2) (mul b1.2 a2.1)) =
                 mkZ (add (mul b1.1 b2.1) (mul b1.2 b2.2)) (add (mul b1.1 b2.2) (mul b1.2 b2.1)) := by
      apply Quotient.sound
      have h2' : add a2.1 b2.2 = add b2.1 a2.2 := h2
      exact mul_well_defined_helper2 b1.1 b1.2 a2.1 a2.2 b2.1 b2.2 h2'
    rw [step1, step2]
  ) z1 z2

/-! ## 5. Representative Independence -/

@[simp]
theorem negZ_mk (a b : Ordinal) : negZ (mkZ a b) = mkZ b a := rfl

@[simp]
theorem addZ_mk (a1 b1 a2 b2 : Ordinal) :
    addZ (mkZ a1 b1) (mkZ a2 b2) = mkZ (add a1 a2) (add b1 b2) := rfl

@[simp]
theorem mulZ_mk (a1 b1 a2 b2 : Ordinal) :
    mulZ (mkZ a1 b1) (mkZ a2 b2) =
    mkZ (add (mul a1 a2) (mul b1 b2)) (add (mul a1 b2) (mul b1 a2)) := rfl

/-! ## 6. Additive Group Axioms -/

theorem addZ_comm (z1 z2 : IntZ) : addZ z1 z2 = addZ z2 z1 := by
  induction z1, z2 using Quotient.inductionOn₂ with
  | h p1 p2 =>
      change mkZ (add p1.1 p2.1) (add p1.2 p2.2) = mkZ (add p2.1 p1.1) (add p2.2 p1.2)
      rw [add_comm p1.1, add_comm p1.2]

theorem addZ_assoc (z1 z2 z3 : IntZ) : addZ (addZ z1 z2) z3 = addZ z1 (addZ z2 z3) := by
  induction z1, z2, z3 using Quotient.inductionOn₃ with
  | h p1 p2 p3 =>
      change mkZ (add (add p1.1 p2.1) p3.1) (add (add p1.2 p2.2) p3.2) =
             mkZ (add p1.1 (add p2.1 p3.1)) (add p1.2 (add p2.2 p3.2))
      rw [add_assoc p1.1, add_assoc p1.2]

theorem zero_addZ (z : IntZ) : addZ zeroZ z = z := by
  induction z using Quotient.inductionOn with
  | h p =>
      apply z_sound
      dsimp [zRel, zeroZ, mkZ]
      change add p.1 p.2 = add p.1 p.2
      rfl

theorem addZ_zero (z : IntZ) : addZ z zeroZ = z := by
  rw [addZ_comm, zero_addZ]

theorem addZ_neg (z : IntZ) : addZ z (negZ z) = zeroZ := by
  induction z using Quotient.inductionOn with
  | h p =>
      apply z_sound
      dsimp [zRel, zeroZ, mkZ]
      rw [add_zero, add_comm p.2 p.1]
      rfl

theorem subZ_self (z : IntZ) : subZ z z = zeroZ :=
  addZ_neg z

/-! ## 7. Multiplicative Monoid Axioms -/

theorem mulZ_comm (z1 z2 : IntZ) : mulZ z1 z2 = mulZ z2 z1 := by
  induction z1, z2 using Quotient.inductionOn₂ with
  | h p1 p2 =>
      change mkZ (add (mul p1.1 p2.1) (mul p1.2 p2.2)) (add (mul p1.1 p2.2) (mul p1.2 p2.1)) =
             mkZ (add (mul p2.1 p1.1) (mul p2.2 p1.2)) (add (mul p2.1 p1.2) (mul p2.2 p1.1))
      rw [mul_comm p1.1 p2.1, mul_comm p1.2 p2.2, mul_comm p1.1 p2.2, mul_comm p1.2 p2.1, add_comm (mul p2.2 p1.1)]

theorem one_mulZ (z : IntZ) : mulZ oneZ z = z := by
  induction z using Quotient.inductionOn with
  | h p =>
      apply z_sound
      dsimp [zRel, oneZ, mkZ]
      change add (add (add p.1 (mul zero p.1)) zero) p.2 = add p.1 (add (add p.2 (mul zero p.2)) zero)
      change add (add (add p.1 zero) zero) p.2 = add p.1 (add (add p.2 zero) zero)
      rw [add_zero, add_zero, add_zero, add_zero]

theorem mulZ_one (z : IntZ) : mulZ z oneZ = z := by
  rw [mulZ_comm, one_mulZ]

theorem zero_mulZ (z : IntZ) : mulZ zeroZ z = zeroZ := by
  induction z using Quotient.inductionOn with
  | h p =>
      apply z_sound
      dsimp [zRel, zeroZ, mkZ]
      change add (add zero zero) zero = add zero (add zero zero)
      rfl

theorem mulZ_zero (z : IntZ) : mulZ z zeroZ = zeroZ := by
  rw [mulZ_comm, zero_mulZ]

/-- Distributivity helper: `(a1*a2 + b1*b2) + (a1*a3 + b1*b3) = a1*(a2+a3) + b1*(b2+b3)`. -/
theorem mulZ_distrib_component (a1 b1 a2 b2 a3 b3 : Ordinal) :
    add (add (mul a1 a2) (mul b1 b2)) (add (mul a1 a3) (mul b1 b3)) =
    add (mul a1 (add a2 a3)) (mul b1 (add b2 b3)) := by
  rw [add_shuffle2 (mul a1 a2) (mul b1 b2) (mul a1 a3) (mul b1 b3)]
  rw [← add_mul, ← add_mul]

/-- Left distributivity of multiplication over addition in ℤ:
    `z1 * (z2 + z3) = z1 * z2 + z1 * z3`. -/
theorem mulZ_add_distrib (z1 z2 z3 : IntZ) :
    mulZ z1 (addZ z2 z3) = addZ (mulZ z1 z2) (mulZ z1 z3) := by
  induction z1, z2, z3 using Quotient.inductionOn₃ with
  | h p1 p2 p3 =>
      change mkZ (add (mul p1.1 (add p2.1 p3.1)) (mul p1.2 (add p2.2 p3.2)))
                 (add (mul p1.1 (add p2.2 p3.2)) (mul p1.2 (add p2.1 p3.1))) =
             mkZ (add (add (mul p1.1 p2.1) (mul p1.2 p2.2)) (add (mul p1.1 p3.1) (mul p1.2 p3.2)))
                 (add (add (mul p1.1 p2.2) (mul p1.2 p2.1)) (add (mul p1.1 p3.2) (mul p1.2 p3.1)))
      rw [mulZ_distrib_component p1.1 p1.2 p2.1 p2.2 p3.1 p3.2]
      rw [mulZ_distrib_component p1.1 p1.2 p2.2 p2.1 p3.2 p3.1]

/-- Right distributivity: `(z1 + z2) * z3 = z1 * z3 + z2 * z3`. -/
theorem addZ_mul_distrib (z1 z2 z3 : IntZ) :
    mulZ (addZ z1 z2) z3 = addZ (mulZ z1 z3) (mulZ z2 z3) := by
  rw [mulZ_comm (addZ z1 z2) z3]
  rw [mulZ_add_distrib z3 z1 z2]
  rw [mulZ_comm z3 z1, mulZ_comm z3 z2]

/-! ## 8. Associativity of Multiplication -/

theorem mulZ_assoc_component (a b c d e f : Ordinal) :
    add (mul (add (mul a c) (mul b d)) e) (mul (add (mul a d) (mul b c)) f) =
    add (mul a (add (mul c e) (mul d f))) (mul b (add (mul c f) (mul d e))) := by
  rw [mul_add, mul_add, add_mul, add_mul]
  rw [mul_assoc, mul_assoc, mul_assoc, mul_assoc]
  rw [add_shuffle2 (mul a (mul c e)) (mul b (mul d e)) (mul a (mul d f)) (mul b (mul c f))]
  rw [add_comm (mul b (mul d e)) (mul b (mul c f))]

theorem mulZ_assoc (z1 z2 z3 : IntZ) : mulZ (mulZ z1 z2) z3 = mulZ z1 (mulZ z2 z3) := by
  induction z1, z2, z3 using Quotient.inductionOn₃ with
  | h p1 p2 p3 =>
      change mkZ (add (mul (add (mul p1.1 p2.1) (mul p1.2 p2.2)) p3.1) (mul (add (mul p1.1 p2.2) (mul p1.2 p2.1)) p3.2))
                 (add (mul (add (mul p1.1 p2.1) (mul p1.2 p2.2)) p3.2) (mul (add (mul p1.1 p2.2) (mul p1.2 p2.1)) p3.1)) =
             mkZ (add (mul p1.1 (add (mul p2.1 p3.1) (mul p2.2 p3.2))) (mul p1.2 (add (mul p2.1 p3.2) (mul p2.2 p3.1))))
                 (add (mul p1.1 (add (mul p2.1 p3.2) (mul p2.2 p3.1))) (mul p1.2 (add (mul p2.1 p3.1) (mul p2.2 p3.2))))
      rw [mulZ_assoc_component p1.1 p1.2 p2.1 p2.2 p3.1 p3.2]
      rw [mulZ_assoc_component p1.1 p1.2 p2.1 p2.2 p3.2 p3.1]

/-! ## 9. Canonical Embedding ℕ ↪ ℤ -/

/-- Canonical embedding of ordinals into integers: `n ↦ [(n, 0)]`. -/
def embedNatZ (n : Ordinal) : IntZ :=
  mkZ n Ordinal.zero

theorem embedNatZ_zero : embedNatZ Ordinal.zero = zeroZ := rfl

theorem embedNatZ_one : embedNatZ (Ordinal.succ Ordinal.zero) = oneZ := rfl

theorem embedNatZ_add (m n : Ordinal) :
    embedNatZ (add m n) = addZ (embedNatZ m) (embedNatZ n) := rfl

theorem embedNatZ_mul (m n : Ordinal) :
    embedNatZ (mul m n) = mulZ (embedNatZ m) (embedNatZ n) := by
  apply Quotient.sound
  change add (mul m n) (add (mul m zero) (mul zero n)) = add (add (mul m n) (mul zero zero)) zero
  dsimp [add, mul]
  rw [mul_zero m]
  rw [add_zero, add_zero, add_zero]

/-- Injectivity of the canonical embedding: `embedNatZ m = embedNatZ n → m = n`,
    proved constructively via `z_exact` and addition cancellation. -/
theorem embedNatZ_inj (m n : Ordinal) (h : embedNatZ m = embedNatZ n) : m = n := by
  have heq : zRel (m, Ordinal.zero) (n, Ordinal.zero) := z_exact h
  dsimp [zRel] at heq
  rw [add_zero, add_zero] at heq
  exact heq

/-- Non-triviality: `zeroZ ≠ oneZ`. -/
theorem zeroZ_ne_oneZ : zeroZ ≠ oneZ := by
  intro h
  have h_inj := embedNatZ_inj Ordinal.zero (Ordinal.succ Ordinal.zero) h
  exact zero_ne_succ Ordinal.zero h_inj

end NumberTower
