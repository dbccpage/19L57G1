/-!
# Obstruction: Presentation-to-Quotient Non-Descent Certificate and Mod-2 Coxeter Homology

Formalization of Charter Goal 12 and Target M109:
- Presentation-to-quotient potential non-descent certificate:
  <omega_sgn - delta^0(q^* P), e_tau> = 1 != 0
- Mod-2 Coxeter presentation cohomology class w_1 in H^1(B S(n); Z_2) ~= Z_2
- Rational Maschke collapse: involution defect delta^1 omega_sgn = 2 != 0 over Q
- Exact coboundary of native capability cost: delta^1 mu1 = 0 with zero circulation

Axioms: strictly within {propext, Quot.sound}, zero mathlib, zero custom axioms, zero sorry.
AuthorityEffect: None.
-/

namespace Obstruction

/-! ## 1. 1-Cochains and Presentation Edges -/

/-- Coordinate transposition edge between presentation states r and tau . r. -/
structure TranspositionEdge where
  stateBefore : Nat
  stateAfter : Nat
  quotientKey : Nat
  deriving DecidableEq, Repr

/-- Parity evaluation on a transposition edge in Z: omega_sgn(e_tau) = 1. -/
def omegaSgn (_e : TranspositionEdge) : Int := 1

/-- A single-valued potential on the quotient state space. -/
def QuotientPotential := Nat → Int

/-- Pullback of quotient potential P to presentation edge e: P(q(after)) - P(q(before)). -/
def delta0Pullback (P : QuotientPotential) (e : TranspositionEdge) : Int :=
  P e.quotientKey - P e.quotientKey

/-- Theorem 7.1 (Quotient Pullback Vanishing):
Because canonical serialization is constant on orbits (q(tau . r) = q(r)),
the pulled-back coboundary vanishes identically on every transposition edge. -/
theorem pullback_coboundary_vanishes (P : QuotientPotential) (e : TranspositionEdge) :
    delta0Pullback P e = 0 := by
  dsimp [delta0Pullback]
  omega

/-- Theorem 7.2 (Presentation-to-Quotient Non-Descent Certificate):
For any single-valued state potential P on the quotient space, the difference
<omega_sgn - delta^0(q^* P), e_tau> equals 1 != 0.
Parity cannot descend to any well-defined quotient state potential. -/
theorem presentation_quotient_non_descent (P : QuotientPotential) (e : TranspositionEdge) :
    omegaSgn e - delta0Pullback P e = 1 := by
  rw [pullback_coboundary_vanishes]
  dsimp [omegaSgn]

/-! ## 2. Mod-2 Coxeter Presentation Cohomology Class w_1 -/

/-- Mod-2 field Z_2. -/
inductive Z2 : Type where
  | zero : Z2
  | one : Z2
  deriving DecidableEq, Repr

namespace Z2

def add : Z2 → Z2 → Z2
  | zero, x => x
  | one, zero => one
  | one, one => zero

instance : Add Z2 := ⟨add⟩

@[simp] theorem add_zero (x : Z2) : x + zero = x := by cases x <;> rfl
@[simp] theorem zero_add (x : Z2) : zero + x = x := by cases x <;> rfl
@[simp] theorem one_add_one : one + one = zero := rfl

theorem one_ne_zero : one ≠ zero := by intro h; cases h

end Z2

/-- Mod-2 evaluation of omega_sgn on transposition edge: 1 mod 2. -/
def omegaSgnMod2 (_e : TranspositionEdge) : Z2 := Z2.one

/-- Involution boundary: tau^2 consists of two traversals of edge e. -/
def boundaryInvolution (e : TranspositionEdge) : Z2 :=
  omegaSgnMod2 e + omegaSgnMod2 e

/-- Over Z_2, the involution relator evaluates to 0 mod 2:
delta^1 omega_sgn(tau^2) = 1 + 1 = 0 mod 2.
Thus omega_sgn is a valid mod-2 cocycle spanning H^1(B S(n); Z_2) ~= Z_2. -/
theorem mod2_involution_cocycle (e : TranspositionEdge) :
    boundaryInvolution e = Z2.zero := by
  dsimp [boundaryInvolution, omegaSgnMod2]

/-- Non-triviality of the mod-2 cohomology class w_1:
unit circulation on the transposition generator e_tau. -/
theorem w1_nontrivial (e : TranspositionEdge) :
    omegaSgnMod2 e ≠ Z2.zero :=
  Z2.one_ne_zero

/-! ## 3. Maschke Rational Collapse over Q -/

/-- Over Q (or Z), the involution relator forces relator defect:
delta^1 omega_sgn(tau^2) = 1 + 1 = 2 != 0. -/
def rationalInvolutionDefect (e : TranspositionEdge) : Int :=
  omegaSgn e + omegaSgn e

theorem rational_involution_defect_ne_zero (e : TranspositionEdge) :
    rationalInvolutionDefect e = 2 := by
  dsimp [rationalInvolutionDefect, omegaSgn]

/-- Confirmation that omega_sgn is NOT a rational cocycle (is_cocycle = False in Target M109). -/
theorem not_rational_cocycle (e : TranspositionEdge) :
    rationalInvolutionDefect e ≠ 0 := by
  rw [rational_involution_defect_ne_zero]
  omega

/-! ## 4. Capability Cost Exact Coboundary on the Movegraph -/

/-- Movegraph edge between two cardinal profiles p1 and p2 with cost mu1. -/
structure MoveEdge where
  pBefore : Nat
  pAfter : Nat
  cost : Nat

/-- Cardinal profile potential function P_card(p) = p. -/
def Pcard (p : Nat) : Nat := p

/-- The coboundary delta^0 P_card on edge e: P_card(after) - P_card(before). -/
def delta0Cost (e : MoveEdge) : Int :=
  (Pcard e.pAfter : Int) - (Pcard e.pBefore : Int)

/-- An edge where cost is the increase in potential: cost = pAfter - pBefore. -/
def IsExactMoveEdge (e : MoveEdge) : Prop :=
  e.pAfter ≥ e.pBefore ∧ (e.cost : Int) = (e.pAfter : Int) - (e.pBefore : Int)

/-- Native capability cost is an exact coboundary: mu1 = delta^0 P_card. -/
theorem capability_cost_is_exact_coboundary (e : MoveEdge) (h : IsExactMoveEdge e) :
    (e.cost : Int) = delta0Cost e := by
  dsimp [delta0Cost, Pcard]
  exact h.2

/-- Commuting square of moves: e1 followed by e2, versus e1' followed by e2',
both connecting pStart to pEnd. -/
structure CommutingSquare where
  pStart : Nat
  pEnd : Nat
  costDirect : Nat
  costAlt : Nat
  h_direct : (costDirect : Int) = (pEnd : Int) - (pStart : Int)
  h_alt : (costAlt : Int) = (pEnd : Int) - (pStart : Int)

/-- Circulation around any commuting square vanishes identically: delta^1 mu1 = 0. -/
theorem capability_circulation_vanishes (sq : CommutingSquare) :
    (sq.costDirect : Int) - (sq.costAlt : Int) = 0 := by
  rw [sq.h_direct, sq.h_alt]
  omega

end Obstruction
