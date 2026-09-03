import FreshCharacters.Receiver

/-!
# Fresh representatives and the balance, reconstructed verbatim

PIN NOTE.  Every definition and theorem in this file is reproduced
verbatim from `research/natural_sections/lean/NaturalSections/LayerBalance.lean`
at blob `493bdc275a5d064e51a1bca336a5a1f70ad9adca` (snapshot
`f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be` of `main`, pinned in
`SOURCE_MANIFEST.json`), sections 1 to 3.  The one change is the outer
namespace, `FreshCharacters` in place of the sibling's.  Nothing here is
claimed as original: these are CONDITIONAL_THEOREM citations into the
pinned packet, compiled here so that this tree's theorems are stated
against the pinned definitions themselves.  The pinned statements this
tree relies on by name are `fresh_rep_unique` (the observer's
well-definedness), `balance_unique` (the walk-sum identity), and the
definitions `balance`, `divisors`, `divisorsBelow`, `sumI`, and
`runningBalance`.  AuthorityEffect: None.
-/

namespace FreshCharacters
namespace Balance

open Receiver

/-! ## 1. Fresh elements of a layer -/

/-- `c` is fresh at layer `k`: its part shares no common factor greater
than one with the part count `k + 1`. -/
def FreshAt (k : Nat) (c : Fin (k + 1)) : Prop := Nat.gcd c.val (k + 1) = 1

instance (k : Nat) (c : Fin (k + 1)) : Decidable (FreshAt k c) :=
  inferInstanceAs (Decidable (Nat.gcd c.val (k + 1) = 1))

/-- Casting divisibility down from the integers, constructively -- the
core cast lemma carries a choice principle this package refuses, so the
descent is done by hand on the two integer constructors. -/
theorem natCast_dvd_down {m n : Nat} (h : (m : Int) ∣ (n : Int)) : m ∣ n := by
  obtain ⟨t, ht⟩ := h
  match t with
  | Int.ofNat s =>
    refine ⟨s, ?_⟩
    have key : (n : Int) = ((m * s : Nat) : Int) := by
      rw [ht, Int.natCast_mul]
      rfl
    omega
  | Int.negSucc s =>
    refine ⟨0, ?_⟩
    have key : (n : Int) = - ((m * (s + 1) : Nat) : Int) := by
      rw [ht]
      simp [Int.natCast_mul, Int.natCast_add, Int.natCast_one,
        Int.negSucc_eq, Int.mul_neg]
    omega

/-- Cancelling a common left factor out of a strict product inequality,
constructively -- the core lemma of this shape also carries the choice
principle. -/
theorem lt_of_mul_left {a b c : Nat} (h : a * b < a * c) : b < c := by
  rcases Nat.lt_or_ge b c with h1 | h1
  · exact h1
  · have := Nat.mul_le_mul_left a h1
    omega

/-- LB1: each layer embedding is injective. -/
theorem layer_inj {k : Nat} {c c' : Fin (k + 1)}
    (h : layer k c = layer k c') : c = c' := by
  have hr : R (c.val, k) (c'.val, k) := Quotient.exact h
  obtain ⟨t, ht⟩ := hr
  have hc : c.val < k + 1 := c.isLt
  have hc' : c'.val < k + 1 := c'.isLt
  have key : (den k : Int) * ((c.val : Int) - c'.val)
      = (den k : Int) * (t * den k) := by
    simp [den, Int.natCast_add, Int.natCast_mul, Int.natCast_one,
      Int.mul_sub, Int.sub_mul, Int.mul_add, Int.add_mul, Int.mul_comm,
      Int.mul_left_comm, Int.mul_assoc] at ht ⊢ <;> omega
  have hcc : (c.val : Int) - c'.val = t * den k :=
    int_left_cancel (den_int_ne_zero k) key
  have hdvd : (den k : Int) ∣ ((c.val : Int) - c'.val) :=
    ⟨t, by rw [hcc]; exact Int.mul_comm t (den k)⟩
  have habs : den k ∣ ((c.val : Int) - c'.val).natAbs :=
    natCast_dvd_down (Int.dvd_natAbs.mpr hdvd)
  have hlt : ((c.val : Int) - c'.val).natAbs < den k := by
    simp [den]
    omega
  have hzero : ((c.val : Int) - c'.val).natAbs = 0 :=
    Nat.eq_zero_of_dvd_of_lt habs hlt
  apply Fin.ext
  omega

/-- LB2: a fresh element of layer `k` equals no element of any layer
with a smaller part count. -/
theorem fresh_not_below {k : Nat} {c : Fin (k + 1)} (hf : FreshAt k c)
    (d : Nat) (hd : d < k) (c' : Fin (d + 1)) :
    layer k c ≠ layer d c' := by
  intro h
  have hr : R (c.val, k) (c'.val, d) := Quotient.exact h
  obtain ⟨t, ht⟩ := hr
  -- the part count of layer `k` divides `c * (d + 1)`
  have hdvdI : ((k + 1 : Nat) : Int) ∣ ((c.val * (d + 1) : Nat) : Int) := by
    refine ⟨(c'.val : Int) + t * ((d : Int) + 1), ?_⟩
    have hnat : ((c.val * (d + 1) : Nat) : Int)
        = (c.val : Int) * ((d : Int) + 1) := by
      simp [Int.natCast_mul, Int.natCast_add, Int.natCast_one]
    rw [hnat]
    simp [den, Int.natCast_add, Int.natCast_mul, Int.natCast_one,
      Int.mul_sub, Int.sub_mul, Int.mul_add, Int.add_mul, Int.mul_comm,
      Int.mul_left_comm, Int.mul_assoc] at ht ⊢ <;> omega
  have hdvdN : (k + 1) ∣ c.val * (d + 1) := natCast_dvd_down hdvdI
  have hmul : (k + 1) ∣ Nat.gcd (c.val * (d + 1)) ((k + 1) * (d + 1)) :=
    Nat.dvd_gcd hdvdN ⟨d + 1, rfl⟩
  have hgcd : Nat.gcd (c.val * (d + 1)) ((k + 1) * (d + 1))
      = Nat.gcd c.val (k + 1) * (d + 1) := Nat.gcd_mul_right ..
  rw [hgcd, hf, Nat.one_mul] at hmul
  have := Nat.eq_zero_of_dvd_of_lt hmul (by omega)
  omega

/-- LB3: a non-fresh element of layer `k` equals an element of a
properly smaller layer -- the common-factor quotient, with cross
difference literally zero. -/
theorem reduce_below {k : Nat} {c : Fin (k + 1)} (hnf : ¬ FreshAt k c) :
    ∃ (d : Nat) (c' : Fin (d + 1)), d < k ∧ layer k c = layer d c' := by
  have hne : Nat.gcd c.val (k + 1) ≠ 1 := hnf
  have hgz : Nat.gcd c.val (k + 1) ≠ 0 := by
    intro h0
    have := Nat.eq_zero_of_gcd_eq_zero_right h0
    omega
  obtain ⟨m, hm⟩ := (Nat.gcd_dvd_right c.val (k + 1) :
    Nat.gcd c.val (k + 1) ∣ (k + 1))
  obtain ⟨c1, hc1⟩ := (Nat.gcd_dvd_left c.val (k + 1) :
    Nat.gcd c.val (k + 1) ∣ c.val)
  have hg2 : 2 ≤ Nat.gcd c.val (k + 1) := by omega
  have hmpos : 0 < m := by
    rcases Nat.eq_zero_or_pos m with h0 | h0
    · rw [h0, Nat.mul_zero] at hm
      omega
    · exact h0
  have h2m : 2 * m ≤ Nat.gcd c.val (k + 1) * m := Nat.mul_le_mul_right m hg2
  have hmlt : m - 1 < k := by omega
  have hc1lt : c1 < m := by
    apply lt_of_mul_left (a := Nat.gcd c.val (k + 1))
    calc Nat.gcd c.val (k + 1) * c1 = c.val := hc1.symm
      _ < k + 1 := c.isLt
      _ = Nat.gcd c.val (k + 1) * m := hm
  refine ⟨m - 1, ⟨c1, by omega⟩, hmlt, ?_⟩
  apply Quotient.sound
  refine ⟨0, ?_⟩
  have hnat : c.val * m = c1 * (k + 1) := by
    calc c.val * m = (Nat.gcd c.val (k + 1) * c1) * m := by rw [← hc1]
      _ = c1 * (Nat.gcd c.val (k + 1) * m) := by
          simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]
      _ = c1 * (k + 1) := by rw [← hm]
  have hden : den (m - 1) = m := by
    simp [den]
    omega
  show (c.val : Int) * den (m - 1) - (c1 : Int) * den k
      = 0 * ((den k : Int) * den (m - 1))
  rw [hden]
  have hInt : ((c.val * m : Nat) : Int) = ((c1 * (k + 1) : Nat) : Int) := by
    rw [hnat]
  simp [den, Int.natCast_add, Int.natCast_mul, Int.natCast_one] at hInt ⊢
  omega

/-- LB4, existence with explicit fuel: descending on the part count
reaches a fresh representative. -/
theorem fresh_descend :
    ∀ (fuel k : Nat), k ≤ fuel → ∀ (c : Fin (k + 1)),
      ∃ (k' : Nat) (c' : Fin (k' + 1)), FreshAt k' c' ∧ layer k' c' = layer k c := by
  intro fuel
  induction fuel with
  | zero =>
    intro k hk c
    have hk0 : k = 0 := by omega
    subst hk0
    exact ⟨0, c, Nat.gcd_one_right c.val, rfl⟩
  | succ f ih =>
    intro k hk c
    by_cases hfr : FreshAt k c
    · exact ⟨k, c, hfr, rfl⟩
    · obtain ⟨d, c', hd, heq⟩ := reduce_below hfr
      obtain ⟨k', c'', hf', heq'⟩ := ih d (by omega) c'
      exact ⟨k', c'', hf', heq'.trans heq.symm⟩

/-- LB4, existence: every element of the receiver has a fresh
representation. -/
theorem fresh_rep_exists (x : QOne) :
    ∃ (k : Nat) (c : Fin (k + 1)), FreshAt k c ∧ layer k c = x := by
  obtain ⟨k, c, hx⟩ := receiver_is_union x
  obtain ⟨k', c', hf, heq⟩ := fresh_descend k k (Nat.le_refl k) c
  exact ⟨k', c', hf, heq.trans hx⟩

/-- LB4, uniqueness: two fresh representations of the same element have
the same part count and the same part. -/
theorem fresh_rep_unique {k k' : Nat} {c : Fin (k + 1)} {c' : Fin (k' + 1)}
    (hf : FreshAt k c) (hf' : FreshAt k' c')
    (h : layer k c = layer k' c') : k = k' ∧ c.val = c'.val := by
  rcases Nat.lt_trichotomy k k' with hlt | heq | hgt
  · exact absurd h.symm (fresh_not_below hf' k hlt c)
  · subst heq
    exact ⟨rfl, congrArg Fin.val (layer_inj h)⟩
  · exact absurd h (fresh_not_below hf k' hgt c')

/-! ## 2. The balance: the signed correction of the divisor recursion -/

/-- Integer sum of a list. -/
def sumI (l : List Int) : Int := l.foldr (· + ·) 0

/-- Nat sum of a list. -/
def sumN (l : List Nat) : Nat := l.foldr (· + ·) 0

/-- The proper divisors of `n`: positive, dividing, below. -/
def divisorsBelow (n : Nat) : List Nat :=
  (List.range n).filter (fun d => d != 0 && n % d == 0)

/-- All divisors of `n`, the number itself last. -/
def divisors (n : Nat) : List Nat := divisorsBelow n ++ [n]

theorem mem_divisorsBelow {n d : Nat} (h : d ∈ divisorsBelow n) :
    0 < d ∧ d < n ∧ n % d = 0 := by
  have h1 := List.mem_filter.mp h
  have h2 := List.mem_range.mp h1.1
  have h3 := h1.2
  simp at h3
  exact ⟨by omega, h2, h3.2⟩

/-- The balance, computed with explicit fuel so that every value is a
kernel computation: `1` at part count `1`, and minus the proper-divisor
sum otherwise. -/
def balanceFuel : Nat → Nat → Int
  | 0, _ => 0
  | f + 1, n =>
    if n = 1 then 1
    else - sumI ((divisorsBelow n).map (fun d => balanceFuel f d))

/-- The balance at `n`: the fueled computation with fuel `n`. -/
def balance (n : Nat) : Int := balanceFuel n n

theorem map_congr_mem {α β : Type} {l : List α} {f g : α → β}
    (h : ∀ a, a ∈ l → f a = g a) : l.map f = l.map g := by
  induction l with
  | nil => rfl
  | cons x xs ih =>
    show f x :: xs.map f = g x :: xs.map g
    rw [h x (List.mem_cons_self ..),
      ih fun a ha => h a (List.mem_cons_of_mem x ha)]

/-- LB5, stability: once the fuel reaches the argument, the fueled
computation no longer depends on it. -/
theorem balanceFuel_stable :
    ∀ (bound f n : Nat), f ≤ bound → n ≤ f →
      balanceFuel f n = balanceFuel n n := by
  intro bound
  induction bound with
  | zero =>
    intro f n hf hn
    have hf0 : f = 0 := by omega
    have hn0 : n = 0 := by omega
    subst hf0
    subst hn0
    rfl
  | succ b ih =>
    intro f n hf hn
    by_cases h0 : n = 0
    · subst h0
      cases f with
      | zero => rfl
      | succ f0 => rfl
    · by_cases h1 : n = 1
      · subst h1
        cases f with
        | zero => exact absurd hn (by omega)
        | succ f0 => rfl
      · cases f with
        | zero => exact absurd hn (by omega)
        | succ f0 =>
          obtain ⟨n0, rfl⟩ : ∃ n0, n = n0 + 2 := ⟨n - 2, by omega⟩
          · have hl : balanceFuel (f0 + 1) (n0 + 2)
                = - sumI ((divisorsBelow (n0 + 2)).map
                    (fun d => balanceFuel f0 d)) := by
              show (if n0 + 2 = 1 then (1 : Int)
                  else - sumI ((divisorsBelow (n0 + 2)).map
                    (fun d => balanceFuel f0 d))) = _
              rw [if_neg (by omega)]
            have hr : balanceFuel (n0 + 2) (n0 + 2)
                = - sumI ((divisorsBelow (n0 + 2)).map
                    (fun d => balanceFuel (n0 + 1) d)) := by
              show (if n0 + 2 = 1 then (1 : Int)
                  else - sumI ((divisorsBelow (n0 + 2)).map
                    (fun d => balanceFuel (n0 + 1) d))) = _
              rw [if_neg (by omega)]
            rw [hl, hr]
            have hmap : (divisorsBelow (n0 + 2)).map (fun d => balanceFuel f0 d)
                = (divisorsBelow (n0 + 2)).map (fun d => balanceFuel (n0 + 1) d) := by
              apply map_congr_mem
              intro d hd
              have hdlt := (mem_divisorsBelow hd).2.1
              have hone : balanceFuel f0 d = balanceFuel d d :=
                ih f0 d (by omega) (by omega)
              have htwo : balanceFuel (n0 + 1) d = balanceFuel d d :=
                ih (n0 + 1) d (by omega) (by omega)
              rw [hone, htwo]
            rw [hmap]

/-- Enough fuel computes the balance. -/
theorem balance_eq_fuel {f n : Nat} (h : n ≤ f) : balanceFuel f n = balance n :=
  balanceFuel_stable f f n (Nat.le_refl f) h

/-- LB5: the balance at part count `1` is `1`. -/
theorem balance_one : balance 1 = 1 := rfl

theorem sumI_append_single (l : List Int) (x : Int) :
    sumI (l ++ [x]) = sumI l + x := by
  induction l with
  | nil =>
    show x + 0 = 0 + x
    omega
  | cons y ys ih =>
    show y + sumI (ys ++ [x]) = (y + sumI ys) + x
    rw [ih]
    omega

/-- LB5: at every part count of the form `n + 2` the divisor sum of the
balance vanishes -- the recursion, replayed as a theorem covering all
part counts at least `2`. -/
theorem balance_divisor_sum (n0 : Nat) :
    sumI ((divisors (n0 + 2)).map balance) = 0 := by
  have hsplit : sumI ((divisors (n0 + 2)).map balance)
      = sumI ((divisorsBelow (n0 + 2)).map balance) + balance (n0 + 2) := by
    rw [divisors, List.map_append]
    exact sumI_append_single ..
  have hval : balance (n0 + 2)
      = - sumI ((divisorsBelow (n0 + 2)).map balance) := by
    show balanceFuel (n0 + 2) (n0 + 2) = _
    have hstep : balanceFuel (n0 + 2) (n0 + 2)
        = - sumI ((divisorsBelow (n0 + 2)).map
            (fun d => balanceFuel (n0 + 1) d)) := by
      show (if n0 + 2 = 1 then (1 : Int)
          else - sumI ((divisorsBelow (n0 + 2)).map
            (fun d => balanceFuel (n0 + 1) d))) = _
      rw [if_neg (by omega)]
    rw [hstep]
    have hmap : (divisorsBelow (n0 + 2)).map (fun d => balanceFuel (n0 + 1) d)
        = (divisorsBelow (n0 + 2)).map balance := by
      apply map_congr_mem
      intro d hd
      have hdlt := (mem_divisorsBelow hd).2.1
      exact balance_eq_fuel (by omega)
    rw [hmap]
  rw [hsplit, hval]
  omega

/-- LB5, uniqueness (added on review: "unique" had been asserted in
prose but proved nowhere): ANY function with value `1` at part count
`1` and vanishing divisor sums agrees with the balance at every
positive part count.  "The unique signed correction" is a theorem,
not a description. -/
theorem balance_unique (g : Nat → Int) (h1 : g 1 = 1)
    (hrec : ∀ n0 : Nat, sumI ((divisors (n0 + 2)).map g) = 0) :
    ∀ n : Nat, 1 ≤ n → g n = balance n := by
  have aux : ∀ (bound n : Nat), n ≤ bound → 1 ≤ n → g n = balance n := by
    intro bound
    induction bound with
    | zero =>
      intro n hn h1n
      exact absurd h1n (by omega)
    | succ b ih =>
      intro n hn h1n
      by_cases hone : n = 1
      · subst hone
        rw [h1, balance_one]
      · obtain ⟨n0, rfl⟩ : ∃ n0, n = n0 + 2 := ⟨n - 2, by omega⟩
        have hg : sumI ((divisorsBelow (n0 + 2)).map g) + g (n0 + 2) = 0 := by
          have h := hrec n0
          rw [divisors, List.map_append] at h
          rw [← sumI_append_single]
          exact h
        have hb : sumI ((divisorsBelow (n0 + 2)).map balance)
            + balance (n0 + 2) = 0 := by
          have h := balance_divisor_sum n0
          rw [divisors, List.map_append] at h
          rw [← sumI_append_single]
          exact h
        have hmap : (divisorsBelow (n0 + 2)).map g
            = (divisorsBelow (n0 + 2)).map balance := by
          apply map_congr_mem
          intro d hd
          have hmem := mem_divisorsBelow hd
          exact ih d (by omega) (by omega)
        rw [hmap] at hg
        omega
  intro n hn
  exact aux n n (Nat.le_refl n) hn

/-! ## 3. The fresh count, and the kernel-decided instances -/

/-- The number of fresh parts at part count `n`. -/
def freshCount (n : Nat) : Nat :=
  ((List.range n).filter (fun j => Nat.gcd j n == 1)).length

/-- The running balance: the balance summed over part counts `1..n`. -/
def runningBalance (n : Nat) : Int :=
  sumI ((List.range n).map (fun i => balance (i + 1)))

/-- LB6: the balance at part counts `1..12`, decided by the kernel. -/
theorem balance_values :
    (List.range 12).map (fun i => balance (i + 1))
      = [1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0] := by decide

/-- LB6: the fresh counts at part counts `1..12`, decided by the
kernel; `1..8` are the receiver rung's reduced counts. -/
theorem freshCount_values :
    (List.range 12).map (fun i => freshCount (i + 1))
      = [1, 1, 2, 2, 4, 2, 6, 4, 6, 4, 10, 4] := by decide

/-- LB6, partition instances: the divisor sum of fresh counts equals
the part count, for `n ≤ 24`. -/
theorem partition_instances :
    (List.range 24).map (fun i => sumN ((divisors (i + 1)).map freshCount))
      = (List.range 24).map (fun i => i + 1) := by decide

/-- LB6, inversion instances: the fresh count is the balance-weighted
divisor sum, for `n ≤ 24` -- the balance inverts cumulative layer
counting into fresh counting. -/
theorem inversion_instances :
    (List.range 24).map
        (fun i => sumI ((divisors (i + 1)).map
          (fun d => balance d * (((i + 1) / d : Nat) : Int))))
      = (List.range 24).map (fun i => (freshCount (i + 1) : Int)) := by decide

set_option maxRecDepth 8192 in
/-- LB6: the running balance at the registered checkpoints. -/
theorem runningBalance_checkpoints :
    (runningBalance 10, runningBalance 30, runningBalance 100)
      = (-1, -3, 1) := by decide

end Balance
end FreshCharacters
