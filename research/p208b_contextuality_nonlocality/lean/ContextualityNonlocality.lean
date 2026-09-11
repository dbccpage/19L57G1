import Lean

/-!
# Constructive Formalization of Contextuality and Nonlocality

AuthorityEffect: None.

Discrete formalization covering:
1. Bell-CHSH Local Hidden Variable (LHV) bound: |S| <= 2 for deterministic strategies.
2. Rational non-local correlator S = 14/5 > 2 over Pythagorean coordinates in Q^2.
3. Cabello 18-ray contextuality configuration in Q^4:
   9 orthogonal contexts of 4 mutually orthogonal rays each,
   exact 2-incidence regularity across the 18 rays,
   and non-existence of non-contextual binary valuations via parity obstruction in H^1(Z_2).
-/

namespace ContextualityNonlocality

-- ============================================================================
-- Part 1: Bipartite Bell-CHSH Scenario and LHV Bound
-- ============================================================================

/-- The CHSH correlator functional on deterministic response functions. -/
def S (A B : Fin 2 → Int) : Int :=
  A 0 * B 0 + A 0 * B 1 + A 1 * B 0 - A 1 * B 1

/-- For any deterministic local strategy taking values in {-1, 1},
    the CHSH correlator evaluates to either 2 or -2. -/
theorem bell_chsh_lhv_values (A B : Fin 2 → Int)
    (hA : ∀ x, A x = 1 ∨ A x = -1)
    (hB : ∀ y, B y = 1 ∨ B y = -1) :
    S A B = 2 ∨ S A B = -2 := by
  rcases hA 0 with hA0 | hA0 <;>
  rcases hA 1 with hA1 | hA1 <;>
  rcases hB 0 with hB0 | hB0 <;>
  rcases hB 1 with hB1 | hB1 <;>
  dsimp [S] <;>
  rw [hA0, hA1, hB0, hB1] <;>
  decide

/-- The CHSH correlator is bounded between -2 and 2 for all local deterministic strategies. -/
theorem bell_chsh_lhv_bound (A B : Fin 2 → Int)
    (hA : ∀ x, A x = 1 ∨ A x = -1)
    (hB : ∀ y, B y = 1 ∨ B y = -1) :
    S A B ≤ 2 ∧ -2 ≤ S A B := by
  rcases bell_chsh_lhv_values A B hA hB with h | h
  · rw [h]
    exact ⟨Int.le_refl 2, by decide⟩
  · rw [h]
    exact ⟨by decide, Int.le_refl (-2)⟩


-- ============================================================================
-- Part 2: Rational Realization of Correlator S = 14/5 > 2
-- ============================================================================

/-- Exact rational number representation for correlation bounds. -/
structure Q where
  num : Int
  den : Nat

/-- Addition of rational numbers. -/
def Q.add (x y : Q) : Q :=
  { num := x.num * (y.den : Int) + y.num * (x.den : Int), den := x.den * y.den }

/-- Subtraction of rational numbers. -/
def Q.sub (x y : Q) : Q :=
  { num := x.num * (y.den : Int) - y.num * (x.den : Int), den := x.den * y.den }

/-- Strict inequality between rational numbers with positive denominators. -/
def Q.lt (x y : Q) : Prop :=
  x.num * (y.den : Int) < y.num * (x.den : Int)

-- Inner products of Pythagorean unit vectors:
-- a_0 = (1, 0), a_1 = (0, 1)
-- b_0 = (4/5, 3/5), b_1 = (4/5, -3/5)
def e00 : Q := { num := 4, den := 5 }
def e01 : Q := { num := 4, den := 5 }
def e10 : Q := { num := 3, den := 5 }
def e11 : Q := { num := -3, den := 5 }

/-- The Pythagorean non-local correlator: (e00 + e01) + (e10 - e11). -/
def S_pyth : Q := (e00.add e01).add (e10.sub e11)

/-- Unreduced numerator of S_pyth evaluates to 1750. -/
theorem pythagorean_correlator_num : S_pyth.num = 1750 := by rfl

/-- Unreduced denominator of S_pyth evaluates to 625 (1750 / 625 = 14 / 5). -/
theorem pythagorean_correlator_den : S_pyth.den = 625 := by rfl

/-- The Pythagorean correlator strictly exceeds the local bound 2 (14/5 = 2.8 > 2). -/
theorem pythagorean_exceeds_lhv : Q.lt { num := 2, den := 1 } S_pyth := by
  change 2 * 625 < 1750 * 1
  omega

/-- The Pythagorean correlator respects the algebraic no-signaling bound 4. -/
theorem pythagorean_respects_algebraic_bound : Q.lt S_pyth { num := 4, den := 1 } := by
  change 1750 * 1 < 4 * 625
  omega


-- ============================================================================
-- Part 3: Cabello 18-Ray Contextuality Configuration
-- ============================================================================

/-- 4-dimensional discrete vector with integer coordinates in {-1, 0, 1}. -/
structure Vec4 where
  x : Int
  y : Int
  z : Int
  w : Int
deriving DecidableEq

/-- Euclidean dot product on Vec4. -/
def dot (u v : Vec4) : Int :=
  u.x * v.x + u.y * v.y + u.z * v.z + u.w * v.w

-- The 18 discrete rays of the Cabello configuration
def r0 : Vec4 := { x := 1, y := 1, z := 1, w := 1 }
def r1 : Vec4 := { x := 1, y := 1, z := 1, w := -1 }
def r2 : Vec4 := { x := 1, y := 1, z := -1, w := 1 }
def r3 : Vec4 := { x := 1, y := 1, z := -1, w := -1 }
def r4 : Vec4 := { x := 1, y := 0, z := 1, w := 0 }
def r5 : Vec4 := { x := 1, y := 0, z := 0, w := 1 }
def r6 : Vec4 := { x := 1, y := 0, z := 0, w := 0 }
def r7 : Vec4 := { x := 1, y := 0, z := 0, w := -1 }
def r8 : Vec4 := { x := 1, y := -1, z := 0, w := 0 }
def r9 : Vec4 := { x := 1, y := -1, z := -1, w := 1 }
def r10 : Vec4 := { x := 1, y := -1, z := -1, w := -1 }
def r11 : Vec4 := { x := 0, y := 1, z := 0, w := 1 }
def r12 : Vec4 := { x := 0, y := 1, z := 0, w := 0 }
def r13 : Vec4 := { x := 0, y := 1, z := 0, w := -1 }
def r14 : Vec4 := { x := 0, y := 1, z := -1, w := 0 }
def r15 : Vec4 := { x := 0, y := 0, z := 1, w := 1 }
def r16 : Vec4 := { x := 0, y := 0, z := 1, w := 0 }
def r17 : Vec4 := { x := 0, y := 0, z := 1, w := -1 }

/-- Ordered list of the 18 Cabello rays. -/
def rays : List Vec4 := [
  r0, r1, r2, r3, r4, r5, r6, r7, r8,
  r9, r10, r11, r12, r13, r14, r15, r16, r17
]

/-- The 9 orthogonal contexts, each consisting of 4 ray indices. -/
def contexts : List (List Nat) := [
  [0, 3, 8, 17],
  [0, 7, 9, 14],
  [1, 2, 8, 15],
  [1, 5, 10, 14],
  [2, 4, 10, 13],
  [3, 4, 9, 11],
  [5, 7, 12, 16],
  [6, 11, 13, 16],
  [6, 12, 15, 17]
]

/-- Lookup ray by index with zero-vector fallback. -/
def rayAt (i : Nat) : Vec4 :=
  rays.getD i { x := 0, y := 0, z := 0, w := 0 }

/-- Predicate verifying pairwise orthogonality within a context. -/
def is_ortho_context (c : List Nat) : Bool :=
  match c with
  | [] => true
  | x :: xs => xs.all (fun y => dot (rayAt x) (rayAt y) == 0) && is_ortho_context xs

/-- Every context consists of mutually orthogonal rays. -/
theorem all_contexts_orthogonal : contexts.all is_ortho_context = true := by
  decide

/-- Incidence count of ray i across all 9 contexts. -/
def ray_incidence_count (i : Nat) : Nat :=
  contexts.foldl (fun acc ctx => acc + if ctx.contains i then 1 else 0) 0

/-- Each of the 18 rays appears in exactly 2 contexts. -/
theorem all_rays_degree_two : (List.range 18).all (fun i => ray_incidence_count i == 2) = true := by
  decide

/-- Type of valuations on the 18 rays taking non-negative integer values. -/
def V := Fin 18 → Nat

/-- Sum of valuation over a list of ray indices. -/
def context_sum (v : V) (c : List (Fin 18)) : Nat :=
  match c with
  | [] => 0
  | x :: xs => v x + context_sum v xs

-- Concrete Fin 18 contexts for formal summation
def C0 : List (Fin 18) := [0, 3, 8, 17]
def C1 : List (Fin 18) := [0, 7, 9, 14]
def C2 : List (Fin 18) := [1, 2, 8, 15]
def C3 : List (Fin 18) := [1, 5, 10, 14]
def C4 : List (Fin 18) := [2, 4, 10, 13]
def C5 : List (Fin 18) := [3, 4, 9, 11]
def C6 : List (Fin 18) := [5, 7, 12, 16]
def C7 : List (Fin 18) := [6, 11, 13, 16]
def C8 : List (Fin 18) := [6, 12, 15, 17]

/-- Total sum of valuation across all 9 contexts. -/
def total_context_sum (v : V) : Nat :=
  context_sum v C0 + context_sum v C1 + context_sum v C2 +
  context_sum v C3 + context_sum v C4 + context_sum v C5 +
  context_sum v C6 + context_sum v C7 + context_sum v C8

/-- Sum of valuation over all 18 individual rays. -/
def ray_sum (v : V) : Nat :=
  v 0 + v 1 + v 2 + v 3 + v 4 + v 5 + v 6 + v 7 + v 8 +
  v 9 + v 10 + v 11 + v 12 + v 13 + v 14 + v 15 + v 16 + v 17

/-- Incidence theorem: summing over all contexts equals twice the sum over all rays. -/
theorem total_eq_twice_ray_sum (v : V) : total_context_sum v = 2 * ray_sum v := by
  dsimp [total_context_sum, context_sum, C0, C1, C2, C3, C4, C5, C6, C7, C8, ray_sum]
  omega

/-- Parity lemma: no natural number M satisfies 2 * M = 9. -/
theorem no_even_equals_nine (M : Nat) : 2 * M = 9 → False := by
  intro h
  omega

/-- Non-contextual valuation obstruction on the 18-ray Cabello configuration. -/
theorem cabello_valuation_obstruction (v : V)
    (h0 : context_sum v C0 = 1) (h1 : context_sum v C1 = 1)
    (h2 : context_sum v C2 = 1) (h3 : context_sum v C3 = 1)
    (h4 : context_sum v C4 = 1) (h5 : context_sum v C5 = 1)
    (h6 : context_sum v C6 = 1) (h7 : context_sum v C7 = 1)
    (h8 : context_sum v C8 = 1) : False := by
  have h_tot : total_context_sum v = 9 := by
    dsimp [total_context_sum]
    rw [h0, h1, h2, h3, h4, h5, h6, h7, h8]
  have h_even : total_context_sum v = 2 * ray_sum v := total_eq_twice_ray_sum v
  omega

/-- Context sum parity mod 2: 9 mod 2 = 1. -/
theorem mod2_context_parity : 9 % 2 = 1 := by rfl

/-- Incidence sum parity mod 2: (2 * M) mod 2 = 0 for any natural M. -/
theorem mod2_incidence_parity (M : Nat) : (2 * M) % 2 = 0 := by
  omega

/-- Čech 1-cochain obstruction: the context cycle parity 1 does not equal coboundary parity 0. -/
theorem cech_cochain_obstruction_nonzero (M : Nat) : (9 % 2) ≠ ((2 * M) % 2) := by
  rw [mod2_context_parity, mod2_incidence_parity M]
  decide

end ContextualityNonlocality

#print axioms ContextualityNonlocality.bell_chsh_lhv_values
#print axioms ContextualityNonlocality.bell_chsh_lhv_bound
#print axioms ContextualityNonlocality.pythagorean_correlator_num
#print axioms ContextualityNonlocality.pythagorean_correlator_den
#print axioms ContextualityNonlocality.pythagorean_exceeds_lhv
#print axioms ContextualityNonlocality.pythagorean_respects_algebraic_bound
#print axioms ContextualityNonlocality.all_contexts_orthogonal
#print axioms ContextualityNonlocality.all_rays_degree_two
#print axioms ContextualityNonlocality.total_eq_twice_ray_sum
#print axioms ContextualityNonlocality.no_even_equals_nine
#print axioms ContextualityNonlocality.cabello_valuation_obstruction
#print axioms ContextualityNonlocality.mod2_context_parity
#print axioms ContextualityNonlocality.mod2_incidence_parity
#print axioms ContextualityNonlocality.cech_cochain_obstruction_nonzero
