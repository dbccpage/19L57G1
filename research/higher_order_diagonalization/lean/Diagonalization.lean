import ObserverHierarchy
import SeparationCapacity

/-!
# Diagonalization: The Higher-Order Diagonalization Theorem and Diagonal Fibers

Formalization of Requirement R2 (Part 2):
- Choice-free finite counting and pigeonhole principle in pure Core Init.
- Proof of the Higher-Order Diagonalization Theorem:
  For every finite observer O ∈ O_k, there exists an indistinguishable pair (r1, r2)
  such that r1 ≇ r2 yet eval_k(O, r1) = eval_k(O, r2).
- Non-singleton diagonal evaluation fiber: no finite observer can separate its own evaluation fiber.
- Dual synthesis: simultaneous pair-identification collapse (injectivity failure) and
  family-covering miss (separation surjectivity failure) on higher-order observers.

Axioms: strictly within {propext, Quot.sound}, zero mathlib, zero custom axioms, zero unproven escapes.
AuthorityEffect: None.
-/

namespace HigherOrderDiagonalization

/-! ## 1. Choice-Free Finite Counting and Pigeonhole -/

theorem nodup_head {α : Type} {x : α} {t : List α}
    (h : List.Nodup (x :: t)) : ∀ a ∈ t, x ≠ a := by
  cases h with
  | cons h1 _ => exact h1

theorem nodup_tail {α : Type} {x : α} {t : List α}
    (h : List.Nodup (x :: t)) : List.Nodup t := by
  cases h with
  | cons _ h2 => exact h2

theorem length_filter_split {α : Type} (p : α → Bool) :
    ∀ l : List α,
      (l.filter p).length + (l.filter (fun x => !p x)).length = l.length
  | [] => rfl
  | x :: t => by
      have ih := length_filter_split p t
      rw [List.filter_cons, List.filter_cons]
      cases hp : p x with
      | true =>
          show (t.filter p).length + 1 + (t.filter (fun x => !p x)).length = t.length + 1
          omega
      | false =>
          show (t.filter p).length + ((t.filter (fun x => !p x)).length + 1) = t.length + 1
          omega

theorem filter_nodup {α : Type} (p : α → Bool) :
    ∀ l : List α, List.Nodup l → List.Nodup (l.filter p)
  | [], _ => List.Pairwise.nil
  | x :: t, hnd => by
      rw [List.filter_cons]
      have iht := filter_nodup p t (nodup_tail hnd)
      cases hp : p x with
      | true =>
          show List.Nodup (x :: t.filter p)
          refine List.Pairwise.cons ?_ iht
          intro a ha
          exact nodup_head hnd a (List.mem_filter.mp ha).1
      | false =>
          exact iht

theorem filter_eq_nil_of_none {α : Type} (p : α → Bool) :
    ∀ l : List α, (∀ y ∈ l, p y = false) → l.filter p = []
  | [], _ => rfl
  | x :: t, h => by
      have hx : p x = false := h x (List.mem_cons_self ..)
      rw [List.filter_cons, hx]
      show t.filter p = []
      exact filter_eq_nil_of_none p t
        (fun y hy => h y (List.mem_cons_of_mem x hy))

theorem nodup_filter_eq_le_one (B : Nat) :
    ∀ l : List Nat, List.Nodup l →
      (l.filter (fun x => decide (x = B))).length ≤ 1
  | [], _ => Nat.zero_le 1
  | x :: t, hnd => by
      rw [List.filter_cons]
      cases hp : (decide (x = B)) with
      | true =>
          show (x :: t.filter (fun y => decide (y = B))).length ≤ 1
          have hxB : x = B := of_decide_eq_true hp
          have hnone : ∀ y ∈ t, (decide (y = B)) = false := by
            intro y hy
            refine decide_eq_false ?_
            intro hyB
            exact nodup_head hnd y hy (hxB.trans hyB.symm)
          rw [filter_eq_nil_of_none _ t hnone]
          exact Nat.le_refl 1
      | false =>
          show (t.filter (fun y => decide (y = B))).length ≤ 1
          exact nodup_filter_eq_le_one B t (nodup_tail hnd)

theorem nodup_length_le :
    ∀ (B : Nat) (l : List Nat), List.Nodup l → (∀ x ∈ l, x < B) →
      l.length ≤ B
  | 0, l, _, hb => by
      cases l with
      | nil => exact Nat.le_refl 0
      | cons x t =>
          exact absurd (hb x (List.mem_cons_self ..)) (Nat.not_lt_zero x)
  | B + 1, l, hnd, hb => by
      have hsplit := length_filter_split (fun x => decide (x = B)) l
      have h1 : (l.filter (fun x => decide (x = B))).length ≤ 1 :=
        nodup_filter_eq_le_one B l hnd
      have h2 : (l.filter (fun x => !(decide (x = B)))).length ≤ B := by
        refine nodup_length_le B _ (filter_nodup _ l hnd) ?_
        intro x hx
        have hm := List.mem_filter.mp hx
        have hlt : x < B + 1 := hb x hm.1
        have hne : x ≠ B := by
          have hb2 : ((!(decide (x = B))) = true) := hm.2
          cases hd : (decide (x = B)) with
          | false => exact of_decide_eq_false hd
          | true =>
              rw [hd] at hb2
              exact Bool.noConfusion hb2
        omega
      omega

def upto : Nat → List Nat
  | 0 => []
  | n + 1 => n :: upto n

theorem upto_length : ∀ n, (upto n).length = n
  | 0 => rfl
  | n + 1 => by
      show (upto n).length + 1 = n + 1
      rw [upto_length n]

theorem upto_mem : ∀ (n x : Nat), x ∈ upto n → x < n
  | 0, x, hx => absurd hx List.not_mem_nil
  | n + 1, x, hx => by
      rcases List.mem_cons.mp hx with h | h
      · omega
      · have := upto_mem n x h
        omega

theorem map_nodup_of_inj (f : Nat → Nat) :
    ∀ n : Nat, (∀ p, p < n → ∀ q, q < n → p ≠ q → f p ≠ f q) →
      List.Nodup ((upto n).map f)
  | 0, _ => List.Pairwise.nil
  | n + 1, hinj => by
      show List.Nodup (f n :: (upto n).map f)
      refine List.Pairwise.cons ?_ ?_
      · intro a ha
        obtain ⟨x, hx, rfl⟩ := List.mem_map.mp ha
        have hxn : x < n := upto_mem n x hx
        exact hinj n (by omega) x (by omega) (by omega)
      · exact map_nodup_of_inj f n
          (fun p hp q hq hpq => hinj p (by omega) q (by omega) hpq)

/-- The Choice-Free Pigeonhole Principle.
A map sending B + 1 indices into B values necessarily produces a collision. -/
theorem pigeonhole (B : Nat) (f : Nat → Nat)
    (hf : ∀ p, p < B + 1 → f p < B) :
    ∃ p, p < B + 1 ∧ ∃ q, q < B + 1 ∧ p ≠ q ∧ f p = f q := by
  refine Decidable.byContradiction ?_
  intro hcon
  have hinj : ∀ p, p < B + 1 → ∀ q, q < B + 1 → p ≠ q → f p ≠ f q :=
    fun p hp q hq hpq hfe => hcon ⟨p, hp, q, hq, hpq, hfe⟩
  have hnd : List.Nodup ((upto (B + 1)).map f) :=
    map_nodup_of_inj f (B + 1) hinj
  have hall : ∀ y ∈ (upto (B + 1)).map f, y < B := by
    intro y hy
    obtain ⟨x, hx, rfl⟩ := List.mem_map.mp hy
    exact hf x (upto_mem (B + 1) x hx)
  have hle := nodup_length_le B ((upto (B + 1)).map f) hnd hall
  rw [List.length_map, upto_length] at hle
  omega

/-! ## 2. The Higher-Order Diagonalization Theorem -/

/-- Theorem 3.1: The Higher-Order Diagonalization Theorem.
For every finite observer O in O_k, there exists a pair of regimes (r1, r2)
at scale depth k+2 such that r1 and r2 are strictly non-isomorphic, yet O
evaluates them to identical signatures (r1 and r2 are indistinguishable to O). -/
theorem higher_order_diagonalization {k : Nat} (O : Observer k) :
    ∃ (r1 r2 : ScaleRegime), ¬ Iso r1 r2 ∧ eval O r1 = eval O r2 := by
  let B := capacity k
  let f : Nat → Nat := fun i => eval O (testRegime k i)
  have hf : ∀ p, p < B + 1 → f p < B := by
    intro p _
    exact eval_lt_capacity O (testRegime k p)
  obtain ⟨p, hp, q, hq, hne, heq⟩ := pigeonhole B f hf
  have hp_bound : p < 2 ^ (k + 1) := by
    dsimp [B, capacity] at hp
    rw [Nat.pow_succ]
    have hpos : 2 ^ k > 0 := Nat.two_pow_pos k
    omega
  have hq_bound : q < 2 ^ (k + 1) := by
    dsimp [B, capacity] at hq
    rw [Nat.pow_succ]
    have hpos : 2 ^ k > 0 := Nat.two_pow_pos k
    omega
  have h_not_iso := testRegime_pairwise_non_isomorphic k p q hp_bound hq_bound hne
  exact ⟨testRegime k p, testRegime k q, h_not_iso, heq⟩

/-! ## 3. Diagonal Evaluation Fibers -/

/-- The evaluation fiber of an observer O at signature sig. -/
def EvaluationFiber {k : Nat} (O : Observer k) (sig : Nat) (r : ScaleRegime) : Prop :=
  eval O r = sig

/-- Theorem 3.2: Diagonal Evaluation Fiber Non-Singleton.
No finite observer O in O_k can separate its own diagonal evaluation fiber:
there exists an evaluation signature whose fiber contains at least two
mutually non-isomorphic regimes. -/
theorem diagonal_fiber_non_singleton {k : Nat} (O : Observer k) :
    ∃ (sig : Nat) (r1 r2 : ScaleRegime),
      EvaluationFiber O sig r1 ∧
      EvaluationFiber O sig r2 ∧
      ¬ Iso r1 r2 := by
  obtain ⟨r1, r2, h_ne, h_eq⟩ := higher_order_diagonalization O
  exact ⟨eval O r1, r1, r2, rfl, h_eq.symm, h_ne⟩

/-! ## 4. Duality Synthesis: Pair-ID Collapse and Family Miss -/

/-- Theorem 3.3: Higher-Order Diagonal Duality.
On every finite observer O in O_k, the evaluation map simultaneously exhibits:
1. Pair-identification collapse: non-injective identification of non-isomorphic regimes.
2. Family-covering miss: strictly positive separation gap between scale-depth regimes
   and observer capacity. -/
theorem higher_order_diagonal_duality {k : Nat} (O : Observer k) :
    (∃ (r1 r2 : ScaleRegime), ¬ Iso r1 r2 ∧ eval O r1 = eval O r2) ∧
    (capacityGap k (k + 2) > 0) :=
  ⟨higher_order_diagonalization O, capacity_gap_strictly_positive k⟩

end HigherOrderDiagonalization
