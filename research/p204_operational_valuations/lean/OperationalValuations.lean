/-!
# Operational Valuations & Convex State Spaces (Target P204)

Constructive formalization of:
1. Operational rational valuations: exact fractions and valuation pairing.
2. State normalization and unit effect evaluation invariance.
3. Convex mixtures of preparation states and operational effects.
4. Bilinearity of state-effect evaluation.
5. Classical simplex state space: uniqueness of convex decomposition into extreme states.
6. Discrete square state space: non-uniqueness of convex decomposition into extreme states.
7. Tensor composition and operational non-signaling across bipartite cuts.

AuthorityEffect: None.
Axiom Scope: Constructive core Lean 4; `#print axioms` strictly within `{propext, Quot.sound}`;
zero `Classical.choice`; zero `mathlib`.
-/

namespace P204OperationalValuations

-- =========================================================================
-- 1. Exact Rational Valuations
-- =========================================================================

/-- Exact positive-denominator rational fraction. -/
@[ext]
structure QVal where
  num : Nat
  den : Nat
  den_pos : den > 0
  deriving DecidableEq, Repr

def QVal.zero : QVal := ⟨0, 1, Nat.zero_lt_succ 0⟩
def QVal.one : QVal := ⟨1, 1, Nat.zero_lt_succ 0⟩
def QVal.half : QVal := ⟨1, 2, Nat.zero_lt_succ 1⟩
def QVal.quarter : QVal := ⟨1, 4, Nat.zero_lt_succ 3⟩

def QVal.add (a b : QVal) : QVal :=
  ⟨a.num * b.den + b.num * a.den, a.den * b.den, Nat.mul_pos a.den_pos b.den_pos⟩

def QVal.mul (a b : QVal) : QVal :=
  ⟨a.num * b.num, a.den * b.den, Nat.mul_pos a.den_pos b.den_pos⟩

instance : Add QVal := ⟨QVal.add⟩
instance : Mul QVal := ⟨QVal.mul⟩

def QVal.eqv (a b : QVal) : Prop :=
  a.num * b.den = b.num * a.den

theorem qval_eqv_refl (a : QVal) : QVal.eqv a a := rfl

theorem qval_eqv_symm {a b : QVal} (h : QVal.eqv a b) : QVal.eqv b a := Eq.symm h

theorem qval_mul_comm (a b : QVal) : QVal.eqv (a * b) (b * a) := by
  show (a.num * b.num) * (b.den * a.den) = (b.num * a.num) * (a.den * b.den)
  ac_rfl

theorem qval_add_comm (a b : QVal) : QVal.eqv (a + b) (b + a) := by
  show (a.num * b.den + b.num * a.den) * (b.den * a.den) =
       (b.num * a.den + a.num * b.den) * (a.den * b.den)
  rw [Nat.add_comm (b.num * a.den) (a.num * b.den), Nat.mul_comm b.den a.den]

theorem half_plus_half_eqv_one : QVal.eqv (QVal.half + QVal.half) QVal.one := rfl

theorem quarter_plus_quarter_eqv_half : QVal.eqv (QVal.quarter + QVal.quarter) QVal.half := rfl

-- =========================================================================
-- 2. Operational States and Effects on Binary Outcome Spaces
-- =========================================================================

@[ext]
structure State2 where
  p0 : Nat
  p1 : Nat
  deriving DecidableEq, Repr

@[ext]
structure Effect2 where
  w0 : Nat
  w1 : Nat
  deriving DecidableEq, Repr

def unitEffect2 : Effect2 := ⟨1, 1⟩
def zeroEffect2 : Effect2 := ⟨0, 0⟩

/-- Operational valuation pairing <e, s> = w0 * p0 + w1 * p1. -/
def eval2 (e : Effect2) (s : State2) : Nat :=
  e.w0 * s.p0 + e.w1 * s.p1

/-- Theorem 1: Unit effect evaluation equals the state normalization sum. -/
theorem eval2_unit_effect (s : State2) : eval2 unitEffect2 s = s.p0 + s.p1 := by
  dsimp [eval2, unitEffect2]
  rw [Nat.one_mul, Nat.one_mul]

/-- Theorem 2: Zero effect evaluation yields zero. -/
theorem eval2_zero_effect (s : State2) : eval2 zeroEffect2 s = 0 := by
  dsimp [eval2, zeroEffect2]
  rw [Nat.zero_mul, Nat.zero_mul, Nat.add_zero]

/-- Theorem 3: Operational normalization is preserved under convex combinations. -/
theorem state2_normalization_preserved (p1 p2 : Nat) (s1 s2 : State2)
    (hs1 : s1.p0 + s1.p1 = 1) (hs2 : s2.p0 + s2.p1 = 1) (hp : p1 + p2 = 1) :
    (p1 * s1.p0 + p2 * s2.p0) + (p1 * s1.p1 + p2 * s2.p1) = 1 := by
  have h_reorder :
    (p1 * s1.p0 + p2 * s2.p0) + (p1 * s1.p1 + p2 * s2.p1) =
    (p1 * s1.p0 + p1 * s1.p1) + (p2 * s2.p0 + p2 * s2.p1) := by
    ac_rfl
  rw [h_reorder, ← Nat.mul_add, ← Nat.mul_add, hs1, hs2, Nat.mul_one, Nat.mul_one, hp]

-- =========================================================================
-- 3. Bilinearity of Operational Evaluation
-- =========================================================================

/-- Theorem 4: Evaluation is linear in preparation mixtures. -/
theorem eval2_linearity_state (e : Effect2) (p1 p2 : Nat) (s1 s2 : State2) :
    eval2 e ⟨p1 * s1.p0 + p2 * s2.p0, p1 * s1.p1 + p2 * s2.p1⟩ =
    p1 * eval2 e s1 + p2 * eval2 e s2 := by
  dsimp [eval2]
  rw [Nat.mul_add, Nat.mul_add, Nat.mul_add, Nat.mul_add]
  ac_rfl

/-- Theorem 5: Evaluation is linear in effect mixtures. -/
theorem eval2_linearity_effect (q1 q2 : Nat) (e1 e2 : Effect2) (s : State2) :
    eval2 ⟨q1 * e1.w0 + q2 * e2.w0, q1 * e1.w1 + q2 * e2.w1⟩ s =
    q1 * eval2 e1 s + q2 * eval2 e2 s := by
  dsimp [eval2]
  rw [Nat.add_mul, Nat.add_mul, Nat.mul_add, Nat.mul_add]
  ac_rfl

/-- Theorem 6: Evaluation is jointly bilinear across state and effect mixtures. -/
theorem eval2_joint_bilinearity (q1 q2 p1 p2 : Nat) (e1 e2 : Effect2) (s1 s2 : State2) :
    eval2 ⟨q1 * e1.w0 + q2 * e2.w0, q1 * e1.w1 + q2 * e2.w1⟩
          ⟨p1 * s1.p0 + p2 * s2.p0, p1 * s1.p1 + p2 * s2.p1⟩ =
    q1 * p1 * eval2 e1 s1 + q1 * p2 * eval2 e1 s2 +
    q2 * p1 * eval2 e2 s1 + q2 * p2 * eval2 e2 s2 := by
  rw [eval2_linearity_effect]
  rw [eval2_linearity_state e1 p1 p2 s1 s2]
  rw [eval2_linearity_state e2 p1 p2 s1 s2]
  rw [Nat.mul_add, Nat.mul_add]
  ac_rfl

-- =========================================================================
-- 4. Classical Simplex: Unique Extreme Decomposition
-- =========================================================================

def delta0 : State2 := ⟨1, 0⟩
def delta1 : State2 := ⟨0, 1⟩

/-- Theorem 7: In a classical binary simplex, convex decomposition into
    extreme states is unique: c0 * delta0 + c1 * delta1 = (p0, p1) implies c0 = p0 and c1 = p1. -/
theorem classical_simplex_unique_decomposition (c0 c1 p0 p1 : Nat)
    (h0 : c0 * delta0.p0 + c1 * delta1.p0 = p0)
    (h1 : c0 * delta0.p1 + c1 * delta1.p1 = p1) :
    c0 = p0 ∧ c1 = p1 := by
  dsimp [delta0, delta1] at h0 h1
  rw [Nat.mul_one] at h0
  rw [Nat.zero_add, Nat.mul_one] at h1
  exact ⟨h0, h1⟩

-- =========================================================================
-- 5. Discrete Square State Space: Non-Unique Extreme Decompositions
-- =========================================================================

@[ext]
structure State4 where
  p0 : QVal
  p1 : QVal
  p2 : QVal
  p3 : QVal
  deriving DecidableEq, Repr

def sq_v1 : State4 := ⟨QVal.half, QVal.zero, QVal.half, QVal.zero⟩
def sq_v2 : State4 := ⟨QVal.zero, QVal.half, QVal.half, QVal.zero⟩
def sq_v3 : State4 := ⟨QVal.zero, QVal.half, QVal.zero, QVal.half⟩
def sq_v4 : State4 := ⟨QVal.half, QVal.zero, QVal.zero, QVal.half⟩

def sq_center : State4 := ⟨QVal.quarter, QVal.quarter, QVal.quarter, QVal.quarter⟩

def mixState4 (w1 w2 : QVal) (s1 s2 : State4) : State4 :=
  ⟨w1 * s1.p0 + w2 * s2.p0,
   w1 * s1.p1 + w2 * s2.p1,
   w1 * s1.p2 + w2 * s2.p2,
   w1 * s1.p3 + w2 * s2.p3⟩

def sq_decomp1 : State4 := mixState4 QVal.half QVal.half sq_v1 sq_v3
def sq_decomp2 : State4 := mixState4 QVal.half QVal.half sq_v2 sq_v4

/-- Theorem 8: First diagonal mixture matches center state on outcome 0. -/
theorem sq_decomp1_p0_eqv : QVal.eqv sq_decomp1.p0 sq_center.p0 := rfl

/-- Theorem 9: First diagonal mixture matches center state on outcome 1. -/
theorem sq_decomp1_p1_eqv : QVal.eqv sq_decomp1.p1 sq_center.p1 := rfl

/-- Theorem 10: First diagonal mixture matches center state on outcome 2. -/
theorem sq_decomp1_p2_eqv : QVal.eqv sq_decomp1.p2 sq_center.p2 := rfl

/-- Theorem 11: First diagonal mixture matches center state on outcome 3. -/
theorem sq_decomp1_p3_eqv : QVal.eqv sq_decomp1.p3 sq_center.p3 := rfl

/-- Theorem 12: Second diagonal mixture matches center state on outcome 0. -/
theorem sq_decomp2_p0_eqv : QVal.eqv sq_decomp2.p0 sq_center.p0 := rfl

/-- Theorem 13: Second diagonal mixture matches center state on outcome 1. -/
theorem sq_decomp2_p1_eqv : QVal.eqv sq_decomp2.p1 sq_center.p1 := rfl

/-- Theorem 14: Second diagonal mixture matches center state on outcome 2. -/
theorem sq_decomp2_p2_eqv : QVal.eqv sq_decomp2.p2 sq_center.p2 := rfl

/-- Theorem 15: Second diagonal mixture matches center state on outcome 3. -/
theorem sq_decomp2_p3_eqv : QVal.eqv sq_decomp2.p3 sq_center.p3 := rfl

@[ext]
structure Weight4 where
  w0 : QVal
  w1 : QVal
  w2 : QVal
  w3 : QVal
  deriving DecidableEq, Repr

def sq_weights1 : Weight4 := ⟨QVal.half, QVal.zero, QVal.half, QVal.zero⟩
def sq_weights2 : Weight4 := ⟨QVal.zero, QVal.half, QVal.zero, QVal.half⟩

/-- Theorem 16: The extreme state decomposition weight vectors are distinct. -/
theorem sq_weights_distinct : sq_weights1 ≠ sq_weights2 := by
  intro h
  have h0 : sq_weights1.w0 = sq_weights2.w0 := by rw [h]
  dsimp [sq_weights1, sq_weights2, QVal.half, QVal.zero] at h0
  injection h0 with hnum
  contradiction

-- =========================================================================
-- 6. Tensor Composition & Operational Non-Signaling Across Cuts
-- =========================================================================

@[ext]
structure CompositeState where
  p00 : Nat
  p01 : Nat
  p10 : Nat
  p11 : Nat
  deriving DecidableEq, Repr

/-- Marginal reduction to Subsystem B. -/
def marginalB (s : CompositeState) : State2 :=
  ⟨s.p00 + s.p10, s.p01 + s.p11⟩

/-- Marginal reduction to Subsystem A. -/
def marginalA (s : CompositeState) : State2 :=
  ⟨s.p00 + s.p01, s.p10 + s.p11⟩

/-- Helper identity for non-signaling term evaluation. -/
theorem non_signaling_term (a b w s : Nat) (h : a + b = 1) :
    a * w * s + b * w * s = w * s := by
  have h1 : a * w * s = a * (w * s) := by ac_rfl
  have h2 : b * w * s = b * (w * s) := by ac_rfl
  rw [h1, h2, ← Nat.add_mul, h, Nat.one_mul]

/-- Theorem 17: Operational non-signaling across bipartite cut A | B:
    Evaluating any operational partition of unity e_{A, 1} + e_{A, 2} = u_A on Subsystem A
    combined with effect e_B on Subsystem B yields identical statistics to the marginal
    evaluation <e_B, s_B>, independent of the choice of measurement partition on A. -/
theorem operational_non_signaling_bipartite (s : CompositeState) (eB : Effect2)
    (a0 a1 b0 b1 : Nat) (ha : a0 + b0 = 1) (hb : a1 + b1 = 1) :
    ((a0 * eB.w0 * s.p00 + a0 * eB.w1 * s.p01) + (a1 * eB.w0 * s.p10 + a1 * eB.w1 * s.p11)) +
    ((b0 * eB.w0 * s.p00 + b0 * eB.w1 * s.p01) + (b1 * eB.w0 * s.p10 + b1 * eB.w1 * s.p11)) =
    eval2 eB (marginalB s) := by
  have h_reorder :
    ((a0 * eB.w0 * s.p00 + a0 * eB.w1 * s.p01) + (a1 * eB.w0 * s.p10 + a1 * eB.w1 * s.p11)) +
    ((b0 * eB.w0 * s.p00 + b0 * eB.w1 * s.p01) + (b1 * eB.w0 * s.p10 + b1 * eB.w1 * s.p11)) =
    (a0 * eB.w0 * s.p00 + b0 * eB.w0 * s.p00) +
    (a0 * eB.w1 * s.p01 + b0 * eB.w1 * s.p01) +
    (a1 * eB.w0 * s.p10 + b1 * eB.w0 * s.p10) +
    (a1 * eB.w1 * s.p11 + b1 * eB.w1 * s.p11) := by
    ac_rfl
  rw [h_reorder]
  rw [non_signaling_term a0 b0 eB.w0 s.p00 ha]
  rw [non_signaling_term a0 b0 eB.w1 s.p01 ha]
  rw [non_signaling_term a1 b1 eB.w0 s.p10 hb]
  rw [non_signaling_term a1 b1 eB.w1 s.p11 hb]
  have h_group :
    eB.w0 * s.p00 + eB.w1 * s.p01 + eB.w0 * s.p10 + eB.w1 * s.p11 =
    (eB.w0 * s.p00 + eB.w0 * s.p10) + (eB.w1 * s.p01 + eB.w1 * s.p11) := by
    ac_rfl
  rw [h_group, ← Nat.mul_add, ← Nat.mul_add]
  rfl

/-- Theorem 18: Symmetric operational non-signaling across bipartite cut B | A:
    Local measurement choice on Subsystem B leaves all marginal observables on Subsystem A invariant. -/
theorem operational_non_signaling_symmetric (s : CompositeState) (eA : Effect2)
    (a0 a1 b0 b1 : Nat) (ha : a0 + b0 = 1) (hb : a1 + b1 = 1) :
    ((eA.w0 * a0 * s.p00 + eA.w1 * a1 * s.p10) + (eA.w0 * b0 * s.p00 + eA.w1 * b1 * s.p10)) +
    ((eA.w0 * a0 * s.p01 + eA.w1 * a1 * s.p11) + (eA.w0 * b0 * s.p01 + eA.w1 * b1 * s.p11)) =
    eval2 eA (marginalA s) := by
  have h_t0 : eA.w0 * a0 * s.p00 + eA.w0 * b0 * s.p00 = eA.w0 * s.p00 := by
    have h1 : eA.w0 * a0 * s.p00 = a0 * eA.w0 * s.p00 := by ac_rfl
    have h2 : eA.w0 * b0 * s.p00 = b0 * eA.w0 * s.p00 := by ac_rfl
    rw [h1, h2, non_signaling_term a0 b0 eA.w0 s.p00 ha]
  have h_t1 : eA.w0 * a0 * s.p01 + eA.w0 * b0 * s.p01 = eA.w0 * s.p01 := by
    have h1 : eA.w0 * a0 * s.p01 = a0 * eA.w0 * s.p01 := by ac_rfl
    have h2 : eA.w0 * b0 * s.p01 = b0 * eA.w0 * s.p01 := by ac_rfl
    rw [h1, h2, non_signaling_term a0 b0 eA.w0 s.p01 ha]
  have h_t2 : eA.w1 * a1 * s.p10 + eA.w1 * b1 * s.p10 = eA.w1 * s.p10 := by
    have h1 : eA.w1 * a1 * s.p10 = a1 * eA.w1 * s.p10 := by ac_rfl
    have h2 : eA.w1 * b1 * s.p10 = b1 * eA.w1 * s.p10 := by ac_rfl
    rw [h1, h2, non_signaling_term a1 b1 eA.w1 s.p10 hb]
  have h_t3 : eA.w1 * a1 * s.p11 + eA.w1 * b1 * s.p11 = eA.w1 * s.p11 := by
    have h1 : eA.w1 * a1 * s.p11 = a1 * eA.w1 * s.p11 := by ac_rfl
    have h2 : eA.w1 * b1 * s.p11 = b1 * eA.w1 * s.p11 := by ac_rfl
    rw [h1, h2, non_signaling_term a1 b1 eA.w1 s.p11 hb]
  have h_reorder :
    ((eA.w0 * a0 * s.p00 + eA.w1 * a1 * s.p10) + (eA.w0 * b0 * s.p00 + eA.w1 * b1 * s.p10)) +
    ((eA.w0 * a0 * s.p01 + eA.w1 * a1 * s.p11) + (eA.w0 * b0 * s.p01 + eA.w1 * b1 * s.p11)) =
    (eA.w0 * a0 * s.p00 + eA.w0 * b0 * s.p00) +
    (eA.w0 * a0 * s.p01 + eA.w0 * b0 * s.p01) +
    (eA.w1 * a1 * s.p10 + eA.w1 * b1 * s.p10) +
    (eA.w1 * a1 * s.p11 + eA.w1 * b1 * s.p11) := by
    ac_rfl
  rw [h_reorder, h_t0, h_t1, h_t2, h_t3]
  have h_group :
    eA.w0 * s.p00 + eA.w0 * s.p01 + eA.w1 * s.p10 + eA.w1 * s.p11 =
    (eA.w0 * s.p00 + eA.w0 * s.p01) + (eA.w1 * s.p10 + eA.w1 * s.p11) := by
    ac_rfl
  rw [h_group, ← Nat.mul_add, ← Nat.mul_add]
  rfl

end P204OperationalValuations
