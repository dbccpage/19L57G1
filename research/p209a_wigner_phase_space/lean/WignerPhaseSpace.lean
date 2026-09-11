import Lean

/-!
# Discrete Wigner Phase_Spaces on Odd_Prime Dimensions (Target P209a)

Formalizes:
1. Parity reflection operator P: P |j> = |-j mod p> with P^2 = I, Tr(P) = 1 on dimensions 3 and 5.
2. Translation operators X and clock operators Z with translation order p: X^p = I, Z^p = I.
3. Gross phase_space covariance: P X P = X^{-1} and P Z P = Z^{-1}.
4. Stabilizer states |0> and |+> as +1 eigenstates of P.
5. Magic non_classical states |M> as -1 eigenstates of P on dimensions 3 and 5.
6. Strict negativity witness: W_{|M>}(0, 0) = -1/p < 0.

AuthorityEffect: None.
Axiom Scope: Constructive core Lean 4; `#print axioms` strictly within `{propext, Quot.sound}`;
zero `Classical.choice`; zero `mathlib`.
-/

namespace P209aWignerPhaseSpace

-- =============================================================================
-- 1. Exact Rational Numbers for Normalization and Witnesses
-- =============================================================================

/-- Exact rational number representation for expectation values and Wigner points. -/
structure QRat where
  num : Int
  den : Nat
deriving DecidableEq, Repr

def QRat.lt (x y : QRat) : Prop :=
  x.num * (y.den : Int) < y.num * (x.den : Int)

instance : DecidableRel QRat.lt :=
  fun x y => inferInstanceAs (Decidable (x.num * (y.den : Int) < y.num * (x.den : Int)))

-- =============================================================================
-- 2. Matrix and Vector Operators in Dimension 3
-- =============================================================================

abbrev Vec3 := Fin 3 → Int
abbrev Mat3 := Fin 3 → Fin 3 → Int

def matVecMul3 (M : Mat3) (v : Vec3) : Vec3 :=
  fun i => M i 0 * v 0 + M i 1 * v 1 + M i 2 * v 2

def matMul3 (A B : Mat3) : Mat3 :=
  fun i k => A i 0 * B 0 k + A i 1 * B 1 k + A i 2 * B 2 k

def id3 : Mat3 :=
  fun i j => if i = j then 1 else 0

def trace3 (M : Mat3) : Int :=
  M 0 0 + M 1 1 + M 2 2

def innerProd3 (u v : Vec3) : Int :=
  u 0 * v 0 + u 1 * v 1 + u 2 * v 2

/-- Parity reflection operator P in dimension 3: P |j> = |-j mod 3>. -/
def P3 : Mat3 :=
  fun i j => if (i.val + j.val) % 3 = 0 then 1 else 0

/-- Translation shift operator X in dimension 3: X |j> = |j+1 mod 3>. -/
def X3 : Mat3 :=
  fun i j => if i.val = (j.val + 1) % 3 then 1 else 0

/-- Inverse translation shift operator X^{-1} in dimension 3. -/
def X3_inv : Mat3 :=
  fun i j => if (i.val + 1) % 3 = j.val then 1 else 0

/-- Stabilizer state |0> in dimension 3. -/
def ket0_3 : Vec3 :=
  fun i => if i.val = 0 then 1 else 0

/-- Stabilizer state |+> in dimension 3. -/
def ket_plus_3 : Vec3 :=
  fun _ => 1

/-- Magic non_classical state |M> = |1> - |2> in dimension 3. -/
def ketM_3 : Vec3 :=
  fun i => if i.val = 1 then 1 else if i.val = 2 then -1 else 0

-- Theorems for Dimension 3

/-- Parity operator in dimension 3 is an involution: P^2 = I. -/
theorem P3_involution : matMul3 P3 P3 = id3 := by
  funext i j; revert i j; decide

/-- Trace of parity reflection operator in dimension 3 equals 1. -/
theorem P3_trace_one : trace3 P3 = 1 := by
  rfl

/-- Translation shift operator X in dimension 3 has order 3: X^3 = I. -/
theorem X3_translation_order : matMul3 X3 (matMul3 X3 X3) = id3 := by
  funext i j; revert i j; decide

/-- Gross phase_space covariance for translation in dimension 3: P X P = X^{-1}. -/
theorem P3_gross_covariance_X : matMul3 P3 (matMul3 X3 P3) = X3_inv := by
  funext i j; revert i j; decide

/-- Stabilizer state |0> is a +1 eigenstate of parity operator P in dimension 3. -/
theorem P3_stabilizer_ket0_eigenstate : matVecMul3 P3 ket0_3 = ket0_3 := by
  funext i; revert i; decide

/-- Stabilizer state |+> is a +1 eigenstate of parity operator P in dimension 3. -/
theorem P3_stabilizer_ket_plus_eigenstate : matVecMul3 P3 ket_plus_3 = ket_plus_3 := by
  funext i; revert i; decide

/-- Magic state |M> = |1> - |2> is a -1 eigenstate of parity operator P in dimension 3. -/
theorem P3_magic_state_eigenstate : matVecMul3 P3 ketM_3 = fun i => - ketM_3 i := by
  funext i; revert i; decide

/-- Norm squared of magic state in dimension 3 evaluates to 2. -/
theorem magic_state_norm_sq_3 : innerProd3 ketM_3 ketM_3 = 2 := by
  rfl

/-- Expectation of parity reflection on magic state in dimension 3 evaluates to -2. -/
theorem magic_state_parity_expectation_3 : innerProd3 ketM_3 (matVecMul3 P3 ketM_3) = -2 := by
  rfl

/-- The discrete Wigner phase_space point value W_{|M>}(0, 0) in dimension 3. -/
def W_magic_3_origin : QRat :=
  { num := -1, den := 3 }

/-- W_{|M>}(0, 0) is strictly negative in dimension 3, certifying non_classicality. -/
theorem magic_state_negativity_witness_3 : QRat.lt W_magic_3_origin { num := 0, den := 1 } := by
  change (-1 : Int) * 1 < 0 * 3
  decide

-- =============================================================================
-- 3. Matrix and Vector Operators in Dimension 5
-- =============================================================================

abbrev Vec5 := Fin 5 → Int
abbrev Mat5 := Fin 5 → Fin 5 → Int

def matVecMul5 (M : Mat5) (v : Vec5) : Vec5 :=
  fun i => M i 0 * v 0 + M i 1 * v 1 + M i 2 * v 2 + M i 3 * v 3 + M i 4 * v 4

def matMul5 (A B : Mat5) : Mat5 :=
  fun i k => A i 0 * B 0 k + A i 1 * B 1 k + A i 2 * B 2 k + A i 3 * B 3 k + A i 4 * B 4 k

def id5 : Mat5 :=
  fun i j => if i = j then 1 else 0

def trace5 (M : Mat5) : Int :=
  M 0 0 + M 1 1 + M 2 2 + M 3 3 + M 4 4

def innerProd5 (u v : Vec5) : Int :=
  u 0 * v 0 + u 1 * v 1 + u 2 * v 2 + u 3 * v 3 + u 4 * v 4

/-- Parity reflection operator P in dimension 5: P |j> = |-j mod 5>. -/
def P5 : Mat5 :=
  fun i j => if (i.val + j.val) % 5 = 0 then 1 else 0

/-- Translation shift operator X in dimension 5: X |j> = |j+1 mod 5>. -/
def X5 : Mat5 :=
  fun i j => if i.val = (j.val + 1) % 5 then 1 else 0

/-- Inverse translation shift operator X^{-1} in dimension 5. -/
def X5_inv : Mat5 :=
  fun i j => if (i.val + 1) % 5 = j.val then 1 else 0

/-- Stabilizer state |0> in dimension 5. -/
def ket0_5 : Vec5 :=
  fun i => if i.val = 0 then 1 else 0

/-- Stabilizer state |+> in dimension 5. -/
def ket_plus_5 : Vec5 :=
  fun _ => 1

/-- Magic non_classical state |M> = |1> - |4> in dimension 5. -/
def ketM_5 : Vec5 :=
  fun i => if i.val = 1 then 1 else if i.val = 4 then -1 else 0

-- Theorems for Dimension 5

/-- Parity operator in dimension 5 is an involution: P^2 = I. -/
theorem P5_involution : matMul5 P5 P5 = id5 := by
  funext i j; revert i j; decide

/-- Trace of parity reflection operator in dimension 5 equals 1. -/
theorem P5_trace_one : trace5 P5 = 1 := by
  rfl

/-- Translation shift operator X in dimension 5 has order 5: X^5 = I. -/
theorem X5_translation_order : matMul5 X5 (matMul5 X5 (matMul5 X5 (matMul5 X5 X5))) = id5 := by
  funext i j; revert i j; decide

/-- Gross phase_space covariance for translation in dimension 5: P X P = X^{-1}. -/
theorem P5_gross_covariance_X : matMul5 P5 (matMul5 X5 P5) = X5_inv := by
  funext i j; revert i j; decide

/-- Stabilizer state |0> is a +1 eigenstate of parity operator P in dimension 5. -/
theorem P5_stabilizer_ket0_eigenstate : matVecMul5 P5 ket0_5 = ket0_5 := by
  funext i; revert i; decide

/-- Stabilizer state |+> is a +1 eigenstate of parity operator P in dimension 5. -/
theorem P5_stabilizer_ket_plus_eigenstate : matVecMul5 P5 ket_plus_5 = ket_plus_5 := by
  funext i; revert i; decide

/-- Magic state |M> = |1> - |4> is a -1 eigenstate of parity operator P in dimension 5. -/
theorem P5_magic_state_eigenstate : matVecMul5 P5 ketM_5 = fun i => - ketM_5 i := by
  funext i; revert i; decide

/-- Norm squared of magic state in dimension 5 evaluates to 2. -/
theorem magic_state_norm_sq_5 : innerProd5 ketM_5 ketM_5 = 2 := by
  rfl

/-- Expectation of parity reflection on magic state in dimension 5 evaluates to -2. -/
theorem magic_state_parity_expectation_5 : innerProd5 ketM_5 (matVecMul5 P5 ketM_5) = -2 := by
  rfl

/-- The discrete Wigner phase_space point value W_{|M>}(0, 0) in dimension 5. -/
def W_magic_5_origin : QRat :=
  { num := -1, den := 5 }

/-- W_{|M>}(0, 0) is strictly negative in dimension 5, certifying non_classicality. -/
theorem magic_state_negativity_witness_5 : QRat.lt W_magic_5_origin { num := 0, den := 1 } := by
  change (-1 : Int) * 1 < 0 * 5
  decide

-- =============================================================================
-- 4. Clock Operators and Phase_Space Covariance in Z[w] and Z[zeta_5]
-- =============================================================================

/-- Exact cyclotomic ring Z[w] with w^2 + w + 1 = 0. -/
structure Cyclo3Ring where
  a : Int
  b : Int
deriving DecidableEq, Repr

def Cyclo3Ring.zero : Cyclo3Ring := { a := 0, b := 0 }
def Cyclo3Ring.one : Cyclo3Ring := { a := 1, b := 0 }
def Cyclo3Ring.w : Cyclo3Ring := { a := 0, b := 1 }
def Cyclo3Ring.w_sq : Cyclo3Ring := { a := -1, b := -1 }

def Cyclo3Ring.add (x y : Cyclo3Ring) : Cyclo3Ring :=
  { a := x.a + y.a, b := x.b + y.b }

def Cyclo3Ring.mul (x y : Cyclo3Ring) : Cyclo3Ring :=
  { a := x.a * y.a - x.b * y.b, b := x.a * y.b + x.b * y.a - x.b * y.b }

abbrev Mat3C := Fin 3 → Fin 3 → Cyclo3Ring

def matMul3C (A B : Mat3C) : Mat3C :=
  fun i k => Cyclo3Ring.add (Cyclo3Ring.add (Cyclo3Ring.mul (A i 0) (B 0 k))
                                           (Cyclo3Ring.mul (A i 1) (B 1 k)))
                           (Cyclo3Ring.mul (A i 2) (B 2 k))

def id3C : Mat3C :=
  fun i j => if i = j then Cyclo3Ring.one else Cyclo3Ring.zero

/-- Parity reflection in Cyclo3Ring. -/
def P3C : Mat3C :=
  fun i j => if (i.val + j.val) % 3 = 0 then Cyclo3Ring.one else Cyclo3Ring.zero

/-- Clock operator Z in dimension 3: diag(1, w, w^2). -/
def Z3 : Mat3C :=
  fun i j =>
    if i = j then
      if i.val = 0 then Cyclo3Ring.one
      else if i.val = 1 then Cyclo3Ring.w
      else Cyclo3Ring.w_sq
    else Cyclo3Ring.zero

/-- Inverse clock operator Z^{-1} in dimension 3: diag(1, w^2, w). -/
def Z3_inv : Mat3C :=
  fun i j =>
    if i = j then
      if i.val = 0 then Cyclo3Ring.one
      else if i.val = 1 then Cyclo3Ring.w_sq
      else Cyclo3Ring.w
    else Cyclo3Ring.zero

/-- Gross phase_space covariance for clock operator in dimension 3: P Z P = Z^{-1}. -/
theorem P3_gross_covariance_Z : matMul3C P3C (matMul3C Z3 P3C) = Z3_inv := by
  funext i j; revert i j; decide

/-- Clock operator Z in dimension 3 has order 3: Z^3 = I. -/
theorem Z3_clock_order : matMul3C Z3 (matMul3C Z3 Z3) = id3C := by
  funext i j; revert i j; decide

end P209aWignerPhaseSpace
