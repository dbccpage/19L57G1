import NaturalSections

/-!
# Budget closure: the operations are forced, the generators are declared

A budget maps a size to a step allowance.  The tower forces two
operations on budgets: COMPOSITION (chaining: costs substitute) and
POINTWISE PRODUCT (nesting: costs multiply).  `Gen B` is the closure of
a declared generator set `B` under exactly those two operations.

Results: the closure of the linear budgets is polynomially bounded
(`gen_linear_polyBounded`) and reaches every polynomial bound
(`pow_in_gen_linear`); adjoining one budget outside -- the doubling
budget -- makes the closure escape every polynomial bound
(`two_pow_not_polyBounded`, `generators_decide_the_class`).  So the
class of polynomial budgets is exactly what the two forced operations
make of LINEAR generators; the operations are forced, the choice of
generators is a declaration, and changing it changes the class.
AuthorityEffect: None.
-/

namespace NaturalSections.Budgets

abbrev Budget := Nat → Nat

/-- Bounded by `c * (n + 1) ^ k` for some `k`, `c`. -/
def PolyBounded (f : Budget) : Prop := ∃ k c, ∀ n, f n ≤ c * (n + 1) ^ k

/-- The closure of a declared generator set under the two forced
operations: composition and pointwise product. -/
inductive Gen (B : Budget → Prop) : Budget → Prop where
  | base {f} : B f → Gen B f
  | comp {f g} : Gen B f → Gen B g → Gen B (fun n => f (g n))
  | mul {f g} : Gen B f → Gen B g → Gen B (fun n => f n * g n)

/-- Linear budgets: `a * n + b`. -/
def Linear (f : Budget) : Prop := ∃ a b, ∀ n, f n = a * n + b

/-- The doubling budget: outside every polynomial bound. -/
def TwoPow : Budget := fun n => 2 ^ n

theorem linear_polyBounded {f : Budget} (h : Linear f) : PolyBounded f := by
  obtain ⟨a, b, hf⟩ := h
  refine ⟨1, a + b, fun n => ?_⟩
  rw [hf n, Nat.pow_one]
  have e : (a + b) * (n + 1) = a * n + a + (b * n + b) := by
    rw [Nat.add_mul, Nat.mul_add, Nat.mul_add, Nat.mul_one, Nat.mul_one]
  omega

theorem polyBounded_mul {f g : Budget} (hf : PolyBounded f) (hg : PolyBounded g) :
    PolyBounded (fun n => f n * g n) := by
  obtain ⟨k1, c1, h1⟩ := hf
  obtain ⟨k2, c2, h2⟩ := hg
  refine ⟨k1 + k2, c1 * c2, fun n => ?_⟩
  calc f n * g n ≤ c1 * (n + 1) ^ k1 * (c2 * (n + 1) ^ k2) :=
        Nat.mul_le_mul (h1 n) (h2 n)
    _ = c1 * c2 * (n + 1) ^ (k1 + k2) := by
        rw [Nat.mul_mul_mul_comm, ← Nat.pow_add]

theorem polyBounded_comp {f g : Budget} (hf : PolyBounded f) (hg : PolyBounded g) :
    PolyBounded (fun n => f (g n)) := by
  obtain ⟨k1, c1, h1⟩ := hf
  obtain ⟨k2, c2, h2⟩ := hg
  refine ⟨k2 * k1, c1 * (c2 + 1) ^ k1, fun n => ?_⟩
  have hpos : 0 < (n + 1) ^ k2 := Nat.pow_pos (by omega)
  have hg1 : g n + 1 ≤ (c2 + 1) * (n + 1) ^ k2 := by
    have hb := h2 n
    have e : (c2 + 1) * (n + 1) ^ k2 = c2 * (n + 1) ^ k2 + (n + 1) ^ k2 :=
      Nat.succ_mul c2 ((n + 1) ^ k2)
    omega
  calc f (g n) ≤ c1 * (g n + 1) ^ k1 := h1 (g n)
    _ ≤ c1 * ((c2 + 1) * (n + 1) ^ k2) ^ k1 :=
        Nat.mul_le_mul_left c1 (Nat.pow_le_pow_left hg1 k1)
    _ = c1 * (c2 + 1) ^ k1 * (n + 1) ^ (k2 * k1) := by
        rw [Nat.mul_pow, Nat.pow_mul, Nat.mul_assoc]

/-- **BC1, soundness half**: the forced closure of the linear budgets is
polynomially bounded. -/
theorem gen_linear_polyBounded {f : Budget} (h : Gen Linear f) : PolyBounded f := by
  induction h with
  | base hb => exact linear_polyBounded hb
  | comp _ _ ihf ihg => exact polyBounded_comp ihf ihg
  | mul _ _ ihf ihg => exact polyBounded_mul ihf ihg

/-- Transport `Gen` along pointwise equality (function extensionality is
within the allowed axioms). -/
theorem gen_congr {B : Budget → Prop} {f g : Budget} (h : ∀ n, f n = g n)
    (hf : Gen B f) : Gen B g :=
  (funext h : f = g) ▸ hf

/-- **BC1, reach half**: every polynomial bound is in the closure. -/
theorem pow_in_gen_linear (k : Nat) : Gen Linear (fun n => (n + 1) ^ k) := by
  induction k with
  | zero =>
    refine gen_congr (fun n => ?_) (Gen.base (f := fun _ => 1) ⟨0, 1, fun n => by simp⟩)
    simp
  | succ k ih =>
    have hlin : Gen Linear (fun n => n + 1) :=
      Gen.base ⟨1, 1, fun n => by simp⟩
    exact gen_congr (fun n => (Nat.pow_succ (n + 1) k).symm) (Gen.mul ih hlin)

theorem sq_le_two_pow : ∀ s, 4 ≤ s → s * s ≤ 2 ^ s := by
  intro s
  induction s with
  | zero => omega
  | succ s ih =>
    intro hs
    rcases Nat.lt_or_ge s 4 with h4 | h4
    · have h3 : s = 3 := by omega
      subst h3
      decide
    · have h1 := ih h4
      have e : (s + 1) * (s + 1) = s * s + s + (s + 1) := by
        rw [Nat.mul_add, Nat.add_mul, Nat.mul_one, Nat.one_mul]
      have h4s : 4 * s ≤ s * s := Nat.mul_le_mul_right s h4
      have hstep : (s + 1) * (s + 1) ≤ 2 * (s * s) := by omega
      calc (s + 1) * (s + 1) ≤ 2 * (s * s) := hstep
        _ ≤ 2 * 2 ^ s := Nat.mul_le_mul_left 2 h1
        _ = 2 ^ (s + 1) := by rw [Nat.pow_succ, Nat.mul_comm]

/-- Proved locally rather than by name: `n < 2 ^ n`. -/
theorem self_lt_two_pow : ∀ n : Nat, n < 2 ^ n := by
  intro n
  induction n with
  | zero => decide
  | succ n ih =>
    have hpos : 0 < 2 ^ n := Nat.pow_pos (by omega)
    have e : (2 : Nat) ^ (n + 1) = 2 ^ n + 2 ^ n := by
      rw [Nat.pow_succ]
      omega
    omega

/-- The doubling budget beats every polynomial bound somewhere. -/
theorem two_pow_escapes (k c : Nat) : ∃ n, c * (n + 1) ^ k < 2 ^ n := by
  refine ⟨k * (k + c + 4) + c + 1, ?_⟩
  have hs4 : 4 ≤ k + c + 4 := by omega
  have hsq := sq_le_two_pow (k + c + 4) hs4
  have hB : (k + c + 4) * (k + c + 4) = k * (k + c + 4) + c * (k + c + 4) + 4 * (k + c + 4) := by
    rw [Nat.add_mul, Nat.add_mul]
  have hc : c ≤ c * (k + c + 4) := by
    have := Nat.mul_le_mul_left c (show 1 ≤ k + c + 4 by omega)
    simpa using this
  have hn1 : k * (k + c + 4) + c + 1 + 1 ≤ 2 ^ (k + c + 4) := by omega
  have hpk : (k * (k + c + 4) + c + 1 + 1) ^ k ≤ 2 ^ ((k + c + 4) * k) := by
    calc (k * (k + c + 4) + c + 1 + 1) ^ k ≤ (2 ^ (k + c + 4)) ^ k :=
          Nat.pow_le_pow_left hn1 k
      _ = 2 ^ ((k + c + 4) * k) := (Nat.pow_mul 2 (k + c + 4) k).symm
  have hlt : c < 2 ^ (c + 1) := by
    have h1 := self_lt_two_pow c
    have h2 : (2 : Nat) ^ c ≤ 2 ^ (c + 1) := Nat.pow_le_pow_right (by omega) (by omega)
    omega
  have hXpos : 0 < 2 ^ ((k + c + 4) * k) := Nat.pow_pos (by omega)
  have hmul1 : c * ((k * (k + c + 4) + c + 1 + 1) ^ k) ≤ c * 2 ^ ((k + c + 4) * k) :=
    Nat.mul_le_mul_left c hpk
  have hsucc : (c + 1) * 2 ^ ((k + c + 4) * k) =
      c * 2 ^ ((k + c + 4) * k) + 2 ^ ((k + c + 4) * k) :=
    Nat.succ_mul c (2 ^ ((k + c + 4) * k))
  have hmul2 : (c + 1) * 2 ^ ((k + c + 4) * k) ≤ 2 ^ (c + 1) * 2 ^ ((k + c + 4) * k) :=
    Nat.mul_le_mul_right (2 ^ ((k + c + 4) * k)) (by omega)
  have hpowadd : (2 : Nat) ^ (c + 1) * 2 ^ ((k + c + 4) * k) =
      2 ^ (c + 1 + (k + c + 4) * k) := (Nat.pow_add 2 (c + 1) ((k + c + 4) * k)).symm
  have hexp : c + 1 + (k + c + 4) * k = k * (k + c + 4) + c + 1 := by
    rw [Nat.mul_comm]
    omega
  rw [hexp] at hpowadd
  omega

/-- **BC2, escape half**: the doubling budget is not polynomially bounded. -/
theorem two_pow_not_polyBounded : ¬ PolyBounded TwoPow := by
  intro h
  obtain ⟨k, c, hb⟩ := h
  obtain ⟨n, hn⟩ := two_pow_escapes k c
  have hbn : (2 : Nat) ^ n ≤ c * (n + 1) ^ k := hb n
  omega

/-- **BC2.**  The closure operations do not determine the class; the
declared generators do: the closure of linear generators is polynomially
bounded, while adjoining the doubling budget as one more generator
escapes every polynomial bound. -/
theorem generators_decide_the_class :
    (∀ f, Gen Linear f → PolyBounded f) ∧
      Gen (fun f => Linear f ∨ f = TwoPow) TwoPow ∧
      ¬ PolyBounded TwoPow :=
  ⟨fun _ h => gen_linear_polyBounded h, Gen.base (Or.inr rfl), two_pow_not_polyBounded⟩

end NaturalSections.Budgets
