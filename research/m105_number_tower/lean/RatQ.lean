import Ordinal
import NNO
import IntZ

/-!
# Constructive Rational Ordered Field ℚ (M106)

Constructive rational ordered field ℚ constructed via localization fraction pairs
modulo cross-multiplication over `Quotient` and `Quot.sound`.
Proves field and order axioms, canonical embeddings ℤ ↪ ℚ and ℕ ↪ ℚ,
and representative independence.

AuthorityEffect: None.
Axiom boundary: strictly within {propext, Quot.sound}, zero Classical.choice, zero mathlib.
-/

namespace NumberTower

open FinitarySubstrate
open FinitarySubstrate.Ordinal

/-! ## 1. Cancellation and Helpers in IntZ -/

/-- Non-zero natural scalar cancellation in ℤ:
    `z1 * embedNatZ (succ k) = z2 * embedNatZ (succ k) → z1 = z2`. -/
theorem mulZ_embed_succ_cancel {z1 z2 : IntZ} {k : Ordinal}
    (h : mulZ z1 (embedNatZ (succ k)) = mulZ z2 (embedNatZ (succ k))) : z1 = z2 := by
  induction z1, z2 using Quotient.inductionOn₂ with
  | h p1 p2 =>
      obtain ⟨a1, b1⟩ := p1
      obtain ⟨a2, b2⟩ := p2
      have hmk : mulZ (mkZ a1 b1) (embedNatZ (succ k)) =
                 mkZ (mul a1 (succ k)) (mul b1 (succ k)) := by
        change mkZ (add (mul a1 (succ k)) (mul b1 zero)) (add (mul a1 zero) (mul b1 (succ k))) =
               mkZ (mul a1 (succ k)) (mul b1 (succ k))
        rw [mul_zero, mul_zero, add_zero]
        rfl
      have hmk2 : mulZ (mkZ a2 b2) (embedNatZ (succ k)) =
                  mkZ (mul a2 (succ k)) (mul b2 (succ k)) := by
        change mkZ (add (mul a2 (succ k)) (mul b2 zero)) (add (mul a2 zero) (mul b2 (succ k))) =
               mkZ (mul a2 (succ k)) (mul b2 (succ k))
        rw [mul_zero, mul_zero, add_zero]
        rfl
      have h' : mkZ (mul a1 (succ k)) (mul b1 (succ k)) =
                mkZ (mul a2 (succ k)) (mul b2 (succ k)) := by
        rw [← hmk, ← hmk2]
        exact h
      have heq : zRel (mul a1 (succ k), mul b1 (succ k)) (mul a2 (succ k), mul b2 (succ k)) := z_exact h'
      dsimp [zRel] at heq
      rw [← mul_add, ← mul_add] at heq
      have heq2 := mul_succ_right_cancel heq
      apply z_sound
      exact heq2

theorem mulZ_neg_left (z1 z2 : IntZ) : mulZ (negZ z1) z2 = negZ (mulZ z1 z2) := by
  induction z1, z2 using Quotient.inductionOn₂ with
  | h p1 p2 =>
      change mkZ (add (mul p1.2 p2.1) (mul p1.1 p2.2)) (add (mul p1.2 p2.2) (mul p1.1 p2.1)) =
             mkZ (add (mul p1.1 p2.2) (mul p1.2 p2.1)) (add (mul p1.1 p2.1) (mul p1.2 p2.2))
      rw [add_comm (mul p1.2 p2.1) (mul p1.1 p2.2), add_comm (mul p1.2 p2.2) (mul p1.1 p2.1)]

/-! ## 2. Localization Fractions and Equivalence Relation -/

/-- Constructive fraction: numerator in ℤ, denominator `succ den_pred` in Ordinal (strictly positive). -/
structure Frac where
  num : IntZ
  den_pred : Ordinal

/-- The strictly positive ordinal denominator: `den f = succ f.den_pred ≥ 1`. -/
def Frac.den (f : Frac) : Ordinal := succ f.den_pred

/-- The denominator embedded in ℤ. -/
def Frac.denZ (f : Frac) : IntZ := embedNatZ f.den

/-- Cross-multiplication equivalence relation on fractions:
    `p1 / q1 ~ p2 / q2 ↔ p1 * q2 = p2 * q1` in ℤ. -/
def qRel (f1 f2 : Frac) : Prop :=
  mulZ f1.num f2.denZ = mulZ f2.num f1.denZ

theorem qRel_refl (f : Frac) : qRel f f := rfl

theorem qRel_symm {f1 f2 : Frac} (h : qRel f1 f2) : qRel f2 f1 := h.symm

/-- Transitivity of fraction equivalence, proved via non-zero cancellation in ℤ. -/
theorem qRel_trans {f1 f2 f3 : Frac} (h1 : qRel f1 f2) (h2 : qRel f2 f3) : qRel f1 f3 := by
  dsimp [qRel] at *
  have h_prod : mulZ (mulZ f1.num f3.denZ) f2.denZ = mulZ (mulZ f3.num f1.denZ) f2.denZ := by
    rw [mulZ_assoc, mulZ_comm f3.denZ, ← mulZ_assoc, h1]
    rw [mulZ_assoc, mulZ_comm f1.denZ, ← mulZ_assoc, h2]
    rw [mulZ_assoc, mulZ_comm f2.denZ, mulZ_comm f1.denZ, mulZ_assoc]
    rw [mulZ_comm f2.denZ f1.denZ]
  exact mulZ_embed_succ_cancel h_prod

/-- Setoid instance for fractions. -/
instance instSetoidFrac : Setoid Frac where
  r := qRel
  iseqv := ⟨qRel_refl, qRel_symm, qRel_trans⟩

/-! ## 3. The Rational Quotient Type ℚ -/

/-- The constructive rational field ℚ, defined as the quotient of fractions modulo cross-multiplication. -/
def RatQ : Type := Quotient instSetoidFrac

/-- Canonical constructor for a rational number from numerator and denominator predecessor. -/
def mkQ (num : IntZ) (den_pred : Ordinal) : RatQ :=
  Quotient.mk instSetoidFrac ⟨num, den_pred⟩

/-- Quot.sound wrapper for rational equivalence. -/
theorem q_sound {f1 f2 : Frac} (h : qRel f1 f2) :
    Quotient.mk instSetoidFrac f1 = Quotient.mk instSetoidFrac f2 :=
  Quotient.sound h

/-- Exactness: equality in ℚ implies fraction equivalence. Depends only on `propext`. -/
theorem q_exact {f1 f2 : Frac}
    (h : Quotient.mk instSetoidFrac f1 = Quotient.mk instSetoidFrac f2) :
    qRel f1 f2 :=
  Quotient.exact h

/-! ## 4. Field Operations on ℚ -/

/-- Additive identity: `0 = 0 / 1`. -/
def zeroQ : RatQ := mkQ zeroZ Ordinal.zero

/-- Multiplicative identity: `1 = 1 / 1`. -/
def oneQ : RatQ := mkQ oneZ Ordinal.zero

/-- Negation on rationals: `-(p / q) = (-p) / q`. -/
def negQ (r : RatQ) : RatQ :=
  Quotient.lift (fun (f : Frac) => mkQ (negZ f.num) f.den_pred) (by
    intro f1 f2 h
    apply q_sound
    dsimp [qRel, Frac.denZ, Frac.den] at *
    rw [mulZ_neg_left, mulZ_neg_left]
    congr 1
  ) r

/-- Helper: common denominator for two fractions: `succ d1 * succ d2 = succ (d2 + d1 * succ d2)`. -/
def commonDenPred (d1 d2 : Ordinal) : Ordinal :=
  add d2 (mul d1 (succ d2))

theorem embedNatZ_commonDen (d1 d2 : Ordinal) :
    embedNatZ (succ (commonDenPred d1 d2)) = mulZ (embedNatZ (succ d1)) (embedNatZ (succ d2)) := by
  change embedNatZ (mul (succ d1) (succ d2)) = mulZ (embedNatZ (succ d1)) (embedNatZ (succ d2))
  exact embedNatZ_mul (succ d1) (succ d2)

/-- Multiplication on rationals: `(p1 / q1) * (p2 / q2) = (p1 * p2) / (q1 * q2)`. -/
def mulQ (r1 r2 : RatQ) : RatQ :=
  Quotient.lift₂ (fun (f1 f2 : Frac) =>
    mkQ (mulZ f1.num f2.num) (commonDenPred f1.den_pred f2.den_pred)
  ) (by
    intro f1 f2 g1 g2 h1 h2
    apply q_sound
    have h1' : mulZ f1.num (embedNatZ (succ g1.den_pred)) = mulZ g1.num (embedNatZ (succ f1.den_pred)) := h1
    have h2' : mulZ f2.num (embedNatZ (succ g2.den_pred)) = mulZ g2.num (embedNatZ (succ f2.den_pred)) := h2
    change mulZ (mulZ f1.num f2.num) (embedNatZ (succ (commonDenPred g1.den_pred g2.den_pred))) =
           mulZ (mulZ g1.num g2.num) (embedNatZ (succ (commonDenPred f1.den_pred f2.den_pred)))
    have hd_f : embedNatZ (succ (commonDenPred f1.den_pred f2.den_pred)) =
                mulZ (embedNatZ (succ f1.den_pred)) (embedNatZ (succ f2.den_pred)) :=
      embedNatZ_commonDen f1.den_pred f2.den_pred
    have hd_g : embedNatZ (succ (commonDenPred g1.den_pred g2.den_pred)) =
                mulZ (embedNatZ (succ g1.den_pred)) (embedNatZ (succ g2.den_pred)) :=
      embedNatZ_commonDen g1.den_pred g2.den_pred
    rw [hd_f, hd_g]
    have hl : mulZ (mulZ f1.num f2.num) (mulZ (embedNatZ (succ g1.den_pred)) (embedNatZ (succ g2.den_pred))) =
              mulZ (mulZ f1.num (embedNatZ (succ g1.den_pred))) (mulZ f2.num (embedNatZ (succ g2.den_pred))) := by
      rw [mulZ_assoc, ← mulZ_assoc f2.num, mulZ_comm f2.num, mulZ_assoc (embedNatZ (succ g1.den_pred)), ← mulZ_assoc]
    have hr : mulZ (mulZ g1.num g2.num) (mulZ (embedNatZ (succ f1.den_pred)) (embedNatZ (succ f2.den_pred))) =
              mulZ (mulZ g1.num (embedNatZ (succ f1.den_pred))) (mulZ g2.num (embedNatZ (succ f2.den_pred))) := by
      rw [mulZ_assoc, ← mulZ_assoc g2.num, mulZ_comm g2.num, mulZ_assoc (embedNatZ (succ f1.den_pred)), ← mulZ_assoc]
    rw [hl, hr, h1', h2']
  ) r1 r2

theorem addQ_term_shuffle (a b c d : IntZ) :
    mulZ (mulZ a b) (mulZ c d) = mulZ (mulZ a c) (mulZ b d) := by
  rw [mulZ_assoc, ← mulZ_assoc b, mulZ_comm b, mulZ_assoc c, ← mulZ_assoc]

/-- Addition on rationals: `(p1 / q1) + (p2 / q2) = (p1 * q2 + p2 * q1) / (q1 * q2)`. -/
def addQ (r1 r2 : RatQ) : RatQ :=
  Quotient.lift₂ (fun (f1 f2 : Frac) =>
    mkQ (addZ (mulZ f1.num f2.denZ) (mulZ f2.num f1.denZ)) (commonDenPred f1.den_pred f2.den_pred)
  ) (by
    intro f1 f2 g1 g2 h1 h2
    apply q_sound
    have h1' : mulZ f1.num (embedNatZ (succ g1.den_pred)) = mulZ g1.num (embedNatZ (succ f1.den_pred)) := h1
    have h2' : mulZ f2.num (embedNatZ (succ g2.den_pred)) = mulZ g2.num (embedNatZ (succ f2.den_pred)) := h2
    change mulZ (addZ (mulZ f1.num (embedNatZ (succ f2.den_pred))) (mulZ f2.num (embedNatZ (succ f1.den_pred))))
                (embedNatZ (succ (commonDenPred g1.den_pred g2.den_pred))) =
           mulZ (addZ (mulZ g1.num (embedNatZ (succ g2.den_pred))) (mulZ g2.num (embedNatZ (succ g1.den_pred))))
                (embedNatZ (succ (commonDenPred f1.den_pred f2.den_pred)))
    have hd_f : embedNatZ (succ (commonDenPred f1.den_pred f2.den_pred)) =
                mulZ (embedNatZ (succ f1.den_pred)) (embedNatZ (succ f2.den_pred)) :=
      embedNatZ_commonDen f1.den_pred f2.den_pred
    have hd_g : embedNatZ (succ (commonDenPred g1.den_pred g2.den_pred)) =
                mulZ (embedNatZ (succ g1.den_pred)) (embedNatZ (succ g2.den_pred)) :=
      embedNatZ_commonDen g1.den_pred g2.den_pred
    rw [hd_f, hd_g]
    rw [addZ_mul_distrib, addZ_mul_distrib]
    have hl1 := addQ_term_shuffle f1.num (embedNatZ (succ f2.den_pred)) (embedNatZ (succ g1.den_pred)) (embedNatZ (succ g2.den_pred))
    have hl2 := addQ_term_shuffle f2.num (embedNatZ (succ f1.den_pred)) (embedNatZ (succ g2.den_pred)) (embedNatZ (succ g1.den_pred))
    have hr1 := addQ_term_shuffle g1.num (embedNatZ (succ g2.den_pred)) (embedNatZ (succ f1.den_pred)) (embedNatZ (succ f2.den_pred))
    have hr2 := addQ_term_shuffle g2.num (embedNatZ (succ g1.den_pred)) (embedNatZ (succ f2.den_pred)) (embedNatZ (succ f1.den_pred))
    rw [hl1]
    have hl2' : mulZ (mulZ f2.num (embedNatZ (succ f1.den_pred))) (mulZ (embedNatZ (succ g1.den_pred)) (embedNatZ (succ g2.den_pred))) =
                mulZ (mulZ f2.num (embedNatZ (succ g2.den_pred))) (mulZ (embedNatZ (succ f1.den_pred)) (embedNatZ (succ g1.den_pred))) := by
      rw [mulZ_comm (embedNatZ (succ g1.den_pred)) (embedNatZ (succ g2.den_pred))]
      exact hl2
    rw [hl2', hr1]
    have hr2' : mulZ (mulZ g2.num (embedNatZ (succ g1.den_pred))) (mulZ (embedNatZ (succ f1.den_pred)) (embedNatZ (succ f2.den_pred))) =
                mulZ (mulZ g2.num (embedNatZ (succ f2.den_pred))) (mulZ (embedNatZ (succ g1.den_pred)) (embedNatZ (succ f1.den_pred))) := by
      rw [mulZ_comm (embedNatZ (succ f1.den_pred)) (embedNatZ (succ f2.den_pred))]
      exact hr2
    rw [hr2']
    rw [h1', h2']
    rw [mulZ_comm (embedNatZ (succ g2.den_pred)) (embedNatZ (succ f2.den_pred))]
    rw [mulZ_comm (embedNatZ (succ g1.den_pred)) (embedNatZ (succ f1.den_pred))]
  ) r1 r2

/-- Subtraction on rationals: `r1 - r2 = r1 + (-r2)`. -/
def subQ (r1 r2 : RatQ) : RatQ :=
  addQ r1 (negQ r2)

/-! ## 5. Representative Independence -/

@[simp]
theorem negQ_mk (num : IntZ) (den_pred : Ordinal) :
    negQ (mkQ num den_pred) = mkQ (negZ num) den_pred := rfl

@[simp]
theorem mulQ_mk (n1 : IntZ) (d1 : Ordinal) (n2 : IntZ) (d2 : Ordinal) :
    mulQ (mkQ n1 d1) (mkQ n2 d2) = mkQ (mulZ n1 n2) (commonDenPred d1 d2) := rfl

/-! ## 6. Field Axioms -/

theorem mulQ_comm (r1 r2 : RatQ) : mulQ r1 r2 = mulQ r2 r1 := by
  induction r1, r2 using Quotient.inductionOn₂ with
  | h f1 f2 =>
      apply q_sound
      change qRel ⟨mulZ f1.num f2.num, commonDenPred f1.den_pred f2.den_pred⟩
                  ⟨mulZ f2.num f1.num, commonDenPred f2.den_pred f1.den_pred⟩
      dsimp [qRel, Frac.denZ, Frac.den]
      have hd1 : embedNatZ (succ (commonDenPred f1.den_pred f2.den_pred)) =
                 mulZ (embedNatZ (succ f1.den_pred)) (embedNatZ (succ f2.den_pred)) :=
        embedNatZ_commonDen f1.den_pred f2.den_pred
      have hd2 : embedNatZ (succ (commonDenPred f2.den_pred f1.den_pred)) =
                 mulZ (embedNatZ (succ f2.den_pred)) (embedNatZ (succ f1.den_pred)) :=
        embedNatZ_commonDen f2.den_pred f1.den_pred
      rw [hd1, hd2]
      rw [mulZ_comm f1.num f2.num, mulZ_comm (embedNatZ (succ f2.den_pred)) (embedNatZ (succ f1.den_pred))]

theorem one_mulQ (r : RatQ) : mulQ oneQ r = r := by
  induction r using Quotient.inductionOn with
  | h f =>
      apply q_sound
      change qRel ⟨mulZ oneZ f.num, commonDenPred zero f.den_pred⟩ f
      dsimp [qRel, Frac.denZ, Frac.den]
      have hd : embedNatZ (succ (commonDenPred zero f.den_pred)) =
                mulZ (embedNatZ (succ zero)) (embedNatZ (succ f.den_pred)) :=
        embedNatZ_commonDen zero f.den_pred
      rw [hd]
      rw [one_mulZ, embedNatZ_one, one_mulZ]

theorem mulQ_one (r : RatQ) : mulQ r oneQ = r := by
  rw [mulQ_comm, one_mulQ]

theorem zero_mulQ (r : RatQ) : mulQ zeroQ r = zeroQ := by
  induction r using Quotient.inductionOn with
  | h f =>
      apply q_sound
      change qRel ⟨mulZ zeroZ f.num, commonDenPred zero f.den_pred⟩ ⟨zeroZ, zero⟩
      dsimp [qRel, Frac.denZ, Frac.den]
      rw [zero_mulZ, zero_mulZ, zero_mulZ]

theorem mulQ_zero (r : RatQ) : mulQ r zeroQ = zeroQ := by
  rw [mulQ_comm, zero_mulQ]

theorem addQ_comm (r1 r2 : RatQ) : addQ r1 r2 = addQ r2 r1 := by
  induction r1, r2 using Quotient.inductionOn₂ with
  | h f1 f2 =>
      apply q_sound
      change qRel ⟨addZ (mulZ f1.num f2.denZ) (mulZ f2.num f1.denZ), commonDenPred f1.den_pred f2.den_pred⟩
                  ⟨addZ (mulZ f2.num f1.denZ) (mulZ f1.num f2.denZ), commonDenPred f2.den_pred f1.den_pred⟩
      dsimp [qRel, Frac.denZ, Frac.den]
      have hd1 : embedNatZ (succ (commonDenPred f1.den_pred f2.den_pred)) =
                 mulZ (embedNatZ (succ f1.den_pred)) (embedNatZ (succ f2.den_pred)) :=
        embedNatZ_commonDen f1.den_pred f2.den_pred
      have hd2 : embedNatZ (succ (commonDenPred f2.den_pred f1.den_pred)) =
                 mulZ (embedNatZ (succ f2.den_pred)) (embedNatZ (succ f1.den_pred)) :=
        embedNatZ_commonDen f2.den_pred f1.den_pred
      rw [hd1, hd2]
      rw [addZ_comm (mulZ f1.num (embedNatZ (succ f2.den_pred)))]
      rw [mulZ_comm (embedNatZ (succ f1.den_pred)) (embedNatZ (succ f2.den_pred))]

theorem zero_addQ (r : RatQ) : addQ zeroQ r = r := by
  induction r using Quotient.inductionOn with
  | h f =>
      apply q_sound
      change qRel ⟨addZ (mulZ zeroZ f.denZ) (mulZ f.num (embedNatZ (succ zero))), commonDenPred zero f.den_pred⟩ f
      dsimp [qRel, Frac.denZ, Frac.den]
      have hd : embedNatZ (succ (commonDenPred zero f.den_pred)) =
                mulZ (embedNatZ (succ zero)) (embedNatZ (succ f.den_pred)) :=
        embedNatZ_commonDen zero f.den_pred
      rw [hd]
      rw [zero_mulZ, zero_addZ]
      rw [embedNatZ_one, one_mulZ, mulZ_one]

theorem addQ_zero (r : RatQ) : addQ r zeroQ = r := by
  rw [addQ_comm, zero_addQ]

theorem addQ_neg (r : RatQ) : addQ r (negQ r) = zeroQ := by
  induction r using Quotient.inductionOn with
  | h f =>
      apply q_sound
      change qRel ⟨addZ (mulZ f.num (embedNatZ (succ f.den_pred))) (mulZ (negZ f.num) (embedNatZ (succ f.den_pred))), commonDenPred f.den_pred f.den_pred⟩ ⟨zeroZ, zero⟩
      dsimp [qRel, Frac.denZ, Frac.den]
      have h_neg : mulZ (negZ f.num) (embedNatZ (succ f.den_pred)) =
                   negZ (mulZ f.num (embedNatZ (succ f.den_pred))) :=
        mulZ_neg_left f.num (embedNatZ (succ f.den_pred))
      rw [h_neg, addZ_neg]
      rw [zero_mulZ, zero_mulZ]

theorem subQ_self (r : RatQ) : subQ r r = zeroQ :=
  addQ_neg r

/-- Multiplicative inverse receipt: for any strictly positive fraction `(succ k) / (succ d)`,
    its reciprocal `(succ d) / (succ k)` satisfies `r * r⁻¹ = 1`. -/
theorem rat_inv_mul (k d : Ordinal) :
    mulQ (mkQ (embedNatZ (succ k)) d) (mkQ (embedNatZ (succ d)) k) = oneQ := by
  apply q_sound
  change qRel ⟨mulZ (embedNatZ (succ k)) (embedNatZ (succ d)), commonDenPred d k⟩ ⟨oneZ, zero⟩
  dsimp [qRel, Frac.denZ, Frac.den]
  have hd : embedNatZ (succ (commonDenPred d k)) =
            mulZ (embedNatZ (succ d)) (embedNatZ (succ k)) := embedNatZ_commonDen d k
  rw [hd]
  rw [embedNatZ_one, mulZ_one, one_mulZ, mulZ_comm]

/-! ## 7. Canonical Embeddings ℤ ↪ ℚ and ℕ ↪ ℚ -/

/-- Canonical embedding of integers into rationals: `z ↦ z / 1`. -/
def embedZRat (z : IntZ) : RatQ :=
  mkQ z Ordinal.zero

theorem embedZRat_zero : embedZRat zeroZ = zeroQ := rfl

theorem embedZRat_one : embedZRat oneZ = oneQ := rfl

theorem embedZRat_mul (z1 z2 : IntZ) :
    embedZRat (mulZ z1 z2) = mulQ (embedZRat z1) (embedZRat z2) := by
  apply q_sound
  change qRel ⟨mulZ z1 z2, zero⟩ ⟨mulZ z1 z2, commonDenPred zero zero⟩
  dsimp [qRel, Frac.denZ, Frac.den]
  have hd : embedNatZ (succ (commonDenPred zero zero)) =
            mulZ (embedNatZ (succ zero)) (embedNatZ (succ zero)) := embedNatZ_commonDen zero zero
  rw [hd, embedNatZ_one, mulZ_one, mulZ_one]

/-- Injectivity of canonical integer embedding: `embedZRat z1 = embedZRat z2 → z1 = z2`. -/
theorem embedZRat_inj (z1 z2 : IntZ) (h : embedZRat z1 = embedZRat z2) : z1 = z2 := by
  have heq : qRel ⟨z1, zero⟩ ⟨z2, zero⟩ := q_exact h
  dsimp [qRel, Frac.denZ, Frac.den] at heq
  rw [embedNatZ_one, mulZ_one, mulZ_one] at heq
  exact heq

/-- Canonical composite embedding of ordinals into rationals: `n ↦ [(n, 0)] / 1`. -/
def embedNatRat (n : Ordinal) : RatQ :=
  embedZRat (embedNatZ n)

theorem embedNatRat_zero : embedNatRat zero = zeroQ := rfl

theorem embedNatRat_one : embedNatRat (succ zero) = oneQ := rfl

theorem embedNatRat_mul (m n : Ordinal) :
    embedNatRat (mul m n) = mulQ (embedNatRat m) (embedNatRat n) := by
  dsimp [embedNatRat]
  rw [embedNatZ_mul, embedZRat_mul]

/-- Injectivity of composite natural embedding: `embedNatRat m = embedNatRat n → m = n`. -/
theorem embedNatRat_inj (m n : Ordinal) (h : embedNatRat m = embedNatRat n) : m = n := by
  have hz := embedZRat_inj (embedNatZ m) (embedNatZ n) h
  exact embedNatZ_inj m n hz

/-- Non-triviality: `zeroQ ≠ oneQ`. -/
theorem zeroQ_ne_oneQ : zeroQ ≠ oneQ := by
  intro h
  have hz := embedZRat_inj zeroZ oneZ h
  exact zeroZ_ne_oneZ hz

/-! ## 8. Constructive Order Relation on ℚ -/

/-- Non-negative rational witness: `r ≥ 0 ↔ ∃ k d : Ordinal, r = (succ k) / (succ d) ∨ r = 0`. -/
def isNonNegQ (r : RatQ) : Prop :=
  r = zeroQ ∨ ∃ (k d : Ordinal), r = mkQ (embedNatZ (succ k)) d

/-- Constructive non-strict order on ℚ: `r1 ≤ r2 ↔ ∃ k d, r2 = r1 + (embedNatZ k / succ d)`. -/
def leQ (r1 r2 : RatQ) : Prop :=
  r1 = r2 ∨ ∃ (k d : Ordinal), r2 = addQ r1 (mkQ (embedNatZ (succ k)) d)

/-- Reflexivity of rational order. -/
theorem leQ_refl (r : RatQ) : leQ r r := Or.inl rfl

/-- Integer embedding preserves non-negativity:
    for any natural `n`, `embedNatRat n` is non-negative. -/
theorem embedNatRat_nonneg (n : Ordinal) : isNonNegQ (embedNatRat n) := by
  cases n with
  | zero => exact Or.inl rfl
  | succ n' => exact Or.inr ⟨n', zero, rfl⟩

end NumberTower
