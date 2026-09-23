import ResearchConservationLadder.Dual

/-!
# A discrete action, its admissible variations, and a conserved charge

AuthorityEffect: None.  Every structure in this module is **supplied**, not
read off the sealed seed:

* configurations are integer pairs `P = Int × Int`;
* a history is a function `q : Nat → P`;
* a two-point weight `L` is a polynomial expression in the four variables
  `x₀ y₀ x₁ y₁` (slots 0 to 3);
* the action of a history up to `N` sums `L` over consecutive pairs;
* an admissible variation moves one interior point `k` by `ε v`, with `ε`
  the dual unit, and fixes every other point;
* a symmetry generator is a function `ξ : P → P`.

Proved here, with every hypothesis named in the statement:

* `action_variation`: the `ε` coefficient of the varied action is
  `D₂L(q_{k-1}, q_k)·v + D₁L(q_k, q_{k+1})·v` for an interior point.  So a
  history is stationary under every admissible variation at `k` exactly
  when the stationarity equation `Stationary L q k` holds.
* `invariant_iff_dual`: infinitesimal invariance of `L` under `ξ`
  (the `ε` coefficient of `L` along the generated flow vanishes) is the
  identity `D₁L·ξ(q₀) + D₂L·ξ(q₁) = 0`.
* `charge_step`, `charge_const`: if `L` is invariant under `ξ` and the
  history is stationary at `k`, the charge `J = D₂L·ξ` is equal on the two
  edges at `k`.  Along a history stationary at every interior point, the
  charge is constant.
-/

namespace ResearchConservationLadder

open Expr

abbrev P := Int × Int

/-- The assignment of the four slots for the pair `(a, b)`. -/
def slots (a b : P) : Nat → Int
  | 0 => a.1
  | 1 => a.2
  | 2 => b.1
  | 3 => b.2
  | _ => 0

/-- A direction in the first two slots only. -/
def first (v : P) : Nat → Int
  | 0 => v.1
  | 1 => v.2
  | _ => 0

/-- A direction in the last two slots only. -/
def second (v : P) : Nat → Int
  | 2 => v.1
  | 3 => v.2
  | _ => 0

/-- Derivative of `L` in its first point, in direction `v`. -/
def D₁ (L : Expr) (a b v : P) : Int := ddir (slots a b) (first v) L

/-- Derivative of `L` in its second point, in direction `v`. -/
def D₂ (L : Expr) (a b v : P) : Int := ddir (slots a b) (second v) L

/-- The stationarity equation at an interior point `k`. -/
def Stationary (L : Expr) (q : Nat → P) (k : Nat) : Prop :=
  ∀ v : P, D₂ L (q (k - 1)) (q k) v + D₁ L (q k) (q (k + 1)) v = 0

/-- A history varied at one point, as a dual-valued history. -/
def vary (q : Nat → P) (k : Nat) (v : P) (j : Nat) : Dual × Dual :=
  if j = k then (⟨(q j).1, v.1⟩, ⟨(q j).2, v.2⟩)
  else (⟨(q j).1, 0⟩, ⟨(q j).2, 0⟩)

/-- The dual assignment of a pair of dual points. -/
def dslots (a b : Dual × Dual) : Nat → Dual
  | 0 => a.1
  | 1 => a.2
  | 2 => b.1
  | 3 => b.2
  | _ => ⟨0, 0⟩

/-- The dual action of a dual history over its first `N` edges. -/
def actionD (L : Expr) (h : Nat → Dual × Dual) : Nat → Dual
  | 0 => ⟨0, 0⟩
  | n + 1 => Dual.add (actionD L h n) (evalD (dslots (h n) (h (n + 1))) L)

theorem dslots_vary (q : Nat → P) (k : Nat) (v : P) (n : Nat) :
    dslots (vary q k v n) (vary q k v (n + 1)) =
      fun i => ⟨slots (q n) (q (n + 1)) i,
        (if n = k then first v i else 0) + (if n + 1 = k then second v i else 0)⟩ := by
  funext i
  by_cases h1 : n = k <;> by_cases h2 : n + 1 = k
  · exact absurd h2 (by omega)
  all_goals
    match i with
    | 0 => simp only [dslots, vary, slots, first, second, h1, h2, Nat.succ_ne_self,
        ↓reduceIte, Int.add_zero, Int.zero_add]
    | 1 => simp only [dslots, vary, slots, first, second, h1, h2, Nat.succ_ne_self,
        ↓reduceIte, Int.add_zero, Int.zero_add]
    | 2 => simp only [dslots, vary, slots, first, second, h1, h2, Nat.succ_ne_self,
        ↓reduceIte, Int.add_zero, Int.zero_add]
    | 3 => simp only [dslots, vary, slots, first, second, h1, h2, Nat.succ_ne_self,
        ↓reduceIte, Int.add_zero, Int.zero_add]
    | _ + 4 => simp only [dslots, slots, first, second, ite_self, Int.add_zero]

theorem edge_du (L : Expr) (q : Nat → P) (k : Nat) (v : P) (n : Nat) :
    (evalD (dslots (vary q k v n) (vary q k v (n + 1))) L).du =
      (if n = k then D₁ L (q n) (q (n + 1)) v else 0) +
        (if n + 1 = k then D₂ L (q n) (q (n + 1)) v else 0) := by
  rw [dslots_vary, evalD_eq, ddir_add]
  by_cases h1 : n = k
  · subst h1
    have h2 : ¬ n + 1 = n := by omega
    simp only [eq_self_iff_true, h2, ↓reduceIte, D₁, D₂, ddir_zero, Int.add_zero]
  · by_cases h2 : n + 1 = k
    · subst h2
      simp only [eq_self_iff_true, h1, ↓reduceIte, D₁, D₂, ddir_zero, Int.zero_add]
    · simp only [h1, h2, ↓reduceIte, ddir_zero, Int.add_zero]

/-- **The first variation of the action.**  For an interior point `k`
(`1 ≤ k` and `k < N`), the `ε` coefficient of the action varied at `k` in
direction `v` is the left side of the stationarity equation at `v`. -/
theorem action_variation (L : Expr) (q : Nat → P) (k N : Nat) (v : P)
    (hk : 1 ≤ k) (hN : k < N) :
    (actionD L (vary q k v) N).du =
      D₂ L (q (k - 1)) (q k) v + D₁ L (q k) (q (k + 1)) v := by
  have key : ∀ n, (actionD L (vary q k v) n).du =
      (if k ≤ n then D₂ L (q (k - 1)) (q k) v else 0) +
        (if k + 1 ≤ n then D₁ L (q k) (q (k + 1)) v else 0) := by
    intro n
    induction n with
    | zero =>
        have c1 : ¬ k ≤ 0 := by omega
        have c2 : ¬ k + 1 ≤ 0 := by omega
        simp only [c1, c2, ↓reduceIte]
        rfl
    | succ n ih =>
        show (actionD L (vary q k v) n).du +
          (evalD (dslots (vary q k v n) (vary q k v (n + 1))) L).du = _
        rw [ih, edge_du]
        rcases Nat.lt_or_ge (n + 1) k with hlt | hge
        · have c1 : ¬ k ≤ n := by omega
          have c2 : ¬ k + 1 ≤ n := by omega
          have c3 : ¬ n = k := by omega
          have c4 : ¬ n + 1 = k := by omega
          have c5 : ¬ k ≤ n + 1 := by omega
          have c6 : ¬ k + 1 ≤ n + 1 := by omega
          simp only [c1, c2, c3, c4, c5, c6, ↓reduceIte]
          rfl
        · rcases Nat.lt_or_ge (n + 1) (k + 1) with hlt2 | hge2
          · have hk' : k = n + 1 := by omega
            subst hk'
            have c1 : ¬ n + 1 ≤ n := by omega
            have c2 : ¬ n + 1 + 1 ≤ n := by omega
            have c3 : ¬ n = n + 1 := by omega
            have c5 : n + 1 ≤ n + 1 := Nat.le_refl _
            have c6 : ¬ n + 1 + 1 ≤ n + 1 := by omega
            simp only [c1, c2, c3, c5, c6, ↓reduceIte, Nat.add_sub_cancel]
            omega
          · rcases Nat.lt_or_ge k n with hlt3 | hge3
            · have c1 : k ≤ n := by omega
              have c2 : k + 1 ≤ n := hlt3
              have c3 : ¬ n = k := by omega
              have c4 : ¬ n + 1 = k := by omega
              have c5 : k ≤ n + 1 := by omega
              have c6 : k + 1 ≤ n + 1 := by omega
              simp only [c1, c2, c3, c4, c5, c6, ↓reduceIte]
              omega
            · have hk' : k = n := by omega
              subst hk'
              have c2 : ¬ k + 1 ≤ k := by omega
              have c4 : ¬ k + 1 = k := by omega
              have c5 : k ≤ k + 1 := Nat.le_succ k
              simp only [Nat.le_refl, c2, c4, c5, ↓reduceIte]
              omega
  rw [key N]
  have h1 : k ≤ N := Nat.le_of_lt hN
  have h2 : k + 1 ≤ N := hN
  simp only [h1, h2, ↓reduceIte]

/-- A history is stationary at `k` exactly when every admissible
variation at `k` leaves the action unchanged to first order. -/
theorem stationary_iff_variation (L : Expr) (q : Nat → P) (k N : Nat)
    (hk : 1 ≤ k) (hN : k < N) :
    Stationary L q k ↔ ∀ v : P, (actionD L (vary q k v) N).du = 0 := by
  constructor
  · intro h v; rw [action_variation L q k N v hk hN]; exact h v
  · intro h v; rw [← action_variation L q k N v hk hN]; exact h v

/-! ## Symmetry and charge -/

/-- Infinitesimal invariance of `L` under the generator `ξ`. -/
def Invariant (L : Expr) (ξ : P → P) : Prop :=
  ∀ a b : P, D₁ L a b (ξ a) + D₂ L a b (ξ b) = 0

/-- The flow generated by `ξ`, to first order, at the pair `(a, b)`. -/
def flow (ξ : P → P) (a b : P) : Nat → Dual :=
  fun i => ⟨slots a b i, first (ξ a) i + second (ξ b) i⟩

theorem invariant_iff_dual (L : Expr) (ξ : P → P) :
    Invariant L ξ ↔ ∀ a b : P, (evalD (flow ξ a b) L).du = 0 := by
  have h : ∀ a b, (evalD (flow ξ a b) L).du = D₁ L a b (ξ a) + D₂ L a b (ξ b) := by
    intro a b
    show (evalD (fun i => ⟨slots a b i, first (ξ a) i + second (ξ b) i⟩) L).du = _
    rw [evalD_eq, ddir_add]
    rfl
  constructor
  · intro hi a b; rw [h]; exact hi a b
  · intro hd a b; rw [← h]; exact hd a b

/-- The charge generated by `ξ` on the edge `(a, b)`. -/
def charge (L : Expr) (ξ : P → P) (a b : P) : Int := D₂ L a b (ξ b)

/-- **Conservation on one step.** -/
theorem charge_step (L : Expr) (ξ : P → P) (hinv : Invariant L ξ) (q : Nat → P)
    (k : Nat) (hs : Stationary L q k) :
    charge L ξ (q k) (q (k + 1)) = charge L ξ (q (k - 1)) (q k) := by
  have h1 := hinv (q k) (q (k + 1))
  have h2 := hs (ξ (q k))
  simp only [charge]
  omega

/-- **Conservation along a stationary history.** -/
theorem charge_const (L : Expr) (ξ : P → P) (hinv : Invariant L ξ) (q : Nat → P)
    (hs : ∀ k, 1 ≤ k → Stationary L q k) (k : Nat) :
    charge L ξ (q k) (q (k + 1)) = charge L ξ (q 0) (q 1) := by
  induction k with
  | zero => rfl
  | succ n ih =>
      have := charge_step L ξ hinv q (n + 1) (hs (n + 1) (by omega))
      simp only [Nat.add_sub_cancel] at this
      rw [this, ih]

end ResearchConservationLadder
