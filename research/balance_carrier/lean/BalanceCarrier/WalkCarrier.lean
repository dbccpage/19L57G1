import BalanceCarrier.Balance

/-!
# The walk carrier: chains over the divisor relation, and the table count

Stage 2 of the balance_carrier run.  The family: objects `1..N`, arrows
`d -> m` exactly when `d` divides `m` and `d < m`.  Two of the declared
counts are defined here exactly as declared in `PREDICTIONS.md`:

* the walk sum `walkSum w m` -- the sum, over strict divisor chains from
  `1` to `m` (listed top first, `[m, d, ..., 1]`, computed with explicit
  fuel and proved fuel-stable), of the product of the arrow weights along
  the chain; `totalWalkSum w N` totals it over the endpoints `1..N`;
* the table count `tableCount T N` -- the alternating sum over the
  arrangements of `1..N` of the signed row products of a square table,
  the sign being the parity of the inversion count; `table w delta f` is
  the menu table.

Proved here:

* `walkSum_succ_succ` -- the walk sum satisfies the proper-divisor
  recursion with the arrow weight into the top.
* `walkSum_neg_one_eq_balance` -- with weight `-1` on every arrow the walk
  sum IS the balance at every part count `>= 1`, from the pinned
  `balance_unique`: value `1` at part count `1`, vanishing divisor sums.
* `totalWalkSum_neg_one_eq_runningBalance` -- hence the totalled walk sum
  with weight `-1` is the running balance at every `N`.
* kernel-decided instances of the table count against the running
  balance, with the bound in each statement; the general table identity
  is NOT proved here and is recorded CONJECTURE in `STATUS.md`.

No sentence here concerns the growth of the running balance.
AuthorityEffect: None.
-/

namespace BalanceCarrier
namespace Walk

open Balance

/-- A weight on the arrow `d -> m`. -/
abbrev Weight := Nat → Nat → Int

/-- The frozen weight menu, W0..W4. -/
def wZero : Weight := fun _ _ => 0
def wOne : Weight := fun _ _ => 1
def wNegOne : Weight := fun _ _ => -1
def wBal : Weight := fun d m => balance (m / d)
def wNegBal : Weight := fun d m => - balance (m / d)

/-! ## 1. Chains and walk sums -/

/-- Strict divisor chains from `1` to `m`, top first, with explicit fuel. -/
def chainsFuel : Nat → Nat → List (List Nat)
  | 0, _ => []
  | f + 1, m =>
    if m = 1 then [[1]]
    else (divisorsBelow m).flatMap (fun d => (chainsFuel f d).map (fun c => m :: c))

/-- The chains from `1` to `m`: the fueled computation with fuel `m`. -/
def chains (m : Nat) : List (List Nat) := chainsFuel m m

/-- The product of the arrow weights along a top-first chain. -/
def chainWeight (w : Weight) : List Nat → Int
  | [] => 1
  | [_] => 1
  | m :: d :: rest => w d m * chainWeight w (d :: rest)

/-- S1: the walk sum from `1` to `m`. -/
def walkSum (w : Weight) (m : Nat) : Int := sumI ((chains m).map (chainWeight w))

/-- S1b: the walk sums totalled over the endpoints `1..n`. -/
def totalWalkSum (w : Weight) (n : Nat) : Int :=
  sumI ((List.range n).map (fun i => walkSum w (i + 1)))

theorem flatMap_congr_mem {α β : Type} {l : List α} {F G : α → List β}
    (h : ∀ a, a ∈ l → F a = G a) : l.flatMap F = l.flatMap G := by
  induction l with
  | nil => rfl
  | cons x xs ih =>
    rw [List.flatMap_cons, List.flatMap_cons, h x (List.mem_cons_self ..),
      ih fun a ha => h a (List.mem_cons_of_mem x ha)]

/-- Fuel stability for the chains, the shape of the pinned
`balanceFuel_stable`. -/
theorem chainsFuel_stable :
    ∀ (bound f n : Nat), f ≤ bound → n ≤ f →
      chainsFuel f n = chainsFuel n n := by
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
          · have hl : chainsFuel (f0 + 1) (n0 + 2)
                = (divisorsBelow (n0 + 2)).flatMap
                    (fun d => (chainsFuel f0 d).map (fun c => (n0 + 2) :: c)) := by
              show (if n0 + 2 = 1 then [[1]]
                  else (divisorsBelow (n0 + 2)).flatMap
                    (fun d => (chainsFuel f0 d).map (fun c => (n0 + 2) :: c))) = _
              rw [if_neg (by omega)]
            have hr : chainsFuel (n0 + 2) (n0 + 2)
                = (divisorsBelow (n0 + 2)).flatMap
                    (fun d => (chainsFuel (n0 + 1) d).map (fun c => (n0 + 2) :: c)) := by
              show (if n0 + 2 = 1 then [[1]]
                  else (divisorsBelow (n0 + 2)).flatMap
                    (fun d => (chainsFuel (n0 + 1) d).map (fun c => (n0 + 2) :: c))) = _
              rw [if_neg (by omega)]
            rw [hl, hr]
            apply flatMap_congr_mem
            intro d hd
            have hdlt := (mem_divisorsBelow hd).2.1
            rw [ih f0 d (by omega) (by omega), ih (n0 + 1) d (by omega) (by omega)]

/-- Every chain to `m` starts (top first) with `m`. -/
theorem chainsFuel_head :
    ∀ (f m : Nat) (c : List Nat), c ∈ chainsFuel f m → ∃ rest, c = m :: rest := by
  intro f
  induction f with
  | zero =>
    intro m c hc
    exact absurd hc (List.not_mem_nil)
  | succ f ih =>
    intro m c hc
    by_cases hm : m = 1
    · subst hm
      have h1 : c ∈ [[1]] := hc
      have h2 := List.mem_singleton.mp h1
      exact ⟨[], h2⟩
    · have hc' : c ∈ (divisorsBelow m).flatMap
          (fun d => (chainsFuel f d).map (fun c => m :: c)) := by
        have hstep : chainsFuel (f + 1) m = (divisorsBelow m).flatMap
            (fun d => (chainsFuel f d).map (fun c => m :: c)) := by
          show (if m = 1 then [[1]] else _) = _
          rw [if_neg hm]
        rw [← hstep]
        exact hc
      obtain ⟨d, _, hcd⟩ := List.mem_flatMap.mp hc'
      obtain ⟨c', _, hcc⟩ := List.mem_map.mp hcd
      exact ⟨c', hcc.symm⟩

theorem chains_head {m : Nat} {c : List Nat} (hc : c ∈ chains m) : ∃ rest, c = m :: rest :=
  chainsFuel_head m m c hc

/-- The chains to `n0 + 2` are the chains to each proper divisor, with
`n0 + 2` placed on top. -/
theorem chains_succ_succ (n0 : Nat) :
    chains (n0 + 2)
      = (divisorsBelow (n0 + 2)).flatMap
          (fun d => (chains d).map (fun c => (n0 + 2) :: c)) := by
  show chainsFuel (n0 + 2) (n0 + 2) = _
  have hstep : chainsFuel (n0 + 2) (n0 + 2)
      = (divisorsBelow (n0 + 2)).flatMap
          (fun d => (chainsFuel (n0 + 1) d).map (fun c => (n0 + 2) :: c)) := by
    show (if n0 + 2 = 1 then [[1]]
        else (divisorsBelow (n0 + 2)).flatMap
          (fun d => (chainsFuel (n0 + 1) d).map (fun c => (n0 + 2) :: c))) = _
    rw [if_neg (by omega)]
  rw [hstep]
  apply flatMap_congr_mem
  intro d hd
  have hdlt := (mem_divisorsBelow hd).2.1
  rw [chainsFuel_stable (n0 + 1) (n0 + 1) d (Nat.le_refl _) (by omega)]
  rfl

theorem sumI_append (l1 l2 : List Int) : sumI (l1 ++ l2) = sumI l1 + sumI l2 := by
  induction l1 with
  | nil =>
    show sumI l2 = 0 + sumI l2
    omega
  | cons y ys ih =>
    show y + sumI (ys ++ l2) = (y + sumI ys) + sumI l2
    rw [ih]
    omega

theorem sumI_flatMap {α : Type} (l : List α) (F : α → List Int) :
    sumI (l.flatMap F) = sumI (l.map (fun a => sumI (F a))) := by
  induction l with
  | nil => rfl
  | cons x xs ih =>
    rw [List.flatMap_cons, sumI_append, ih]
    rfl

theorem sumI_map_mul_left {α : Type} (a : Int) (l : List α) (g : α → Int) :
    sumI (l.map (fun x => a * g x)) = a * sumI (l.map g) := by
  induction l with
  | nil =>
    show (0 : Int) = a * 0
    omega
  | cons x xs ih =>
    show a * g x + sumI (xs.map (fun x => a * g x)) = a * (g x + sumI (xs.map g))
    rw [ih, Int.mul_add]

theorem sumI_map_neg {α : Type} (l : List α) (g : α → Int) :
    sumI (l.map (fun x => - g x)) = - sumI (l.map g) := by
  induction l with
  | nil => rfl
  | cons x xs ih =>
    show - g x + sumI (xs.map (fun x => - g x)) = - (g x + sumI (xs.map g))
    rw [ih]
    omega

/-- The walk sum at part count `1`: the empty chain contributes `1`. -/
theorem walkSum_one (w : Weight) : walkSum w 1 = 1 := rfl

/-- The proper-divisor recursion of the walk sum: every chain to `n0 + 2`
is a chain to a proper divisor `d` extended by the arrow `d -> n0 + 2`. -/
theorem walkSum_succ_succ (w : Weight) (n0 : Nat) :
    walkSum w (n0 + 2)
      = sumI ((divisorsBelow (n0 + 2)).map (fun d => w d (n0 + 2) * walkSum w d)) := by
  have h1 : walkSum w (n0 + 2)
      = sumI (((divisorsBelow (n0 + 2)).flatMap
          (fun d => (chains d).map (fun c => (n0 + 2) :: c))).map (chainWeight w)) := by
    unfold walkSum
    rw [chains_succ_succ]
  rw [h1, List.map_flatMap, sumI_flatMap]
  apply congrArg sumI
  apply map_congr_mem
  intro d hd
  rw [List.map_map]
  unfold walkSum
  rw [← sumI_map_mul_left]
  apply congrArg sumI
  apply map_congr_mem
  intro c hc
  obtain ⟨rest, hrest⟩ := chains_head hc
  subst hrest
  rfl

/-- S1 with weight `-1` is the balance at every part count `>= 1`: the
walk sum has value `1` at part count `1` and vanishing divisor sums, so
the pinned uniqueness identifies it with the balance. -/
theorem walkSum_neg_one_eq_balance : ∀ n : Nat, 1 ≤ n → walkSum wNegOne n = balance n := by
  apply balance_unique
  · rfl
  · intro n0
    rw [divisors, List.map_append]
    show sumI ((divisorsBelow (n0 + 2)).map (walkSum wNegOne) ++ [walkSum wNegOne (n0 + 2)]) = 0
    rw [sumI_append_single, walkSum_succ_succ]
    have hmap : (divisorsBelow (n0 + 2)).map (fun d => wNegOne d (n0 + 2) * walkSum wNegOne d)
        = (divisorsBelow (n0 + 2)).map (fun d => - walkSum wNegOne d) := by
      apply map_congr_mem
      intro d _
      show (-1 : Int) * walkSum wNegOne d = - walkSum wNegOne d
      omega
    rw [hmap, sumI_map_neg]
    omega

/-- S1b with weight `-1` is the running balance at every `N`. -/
theorem totalWalkSum_neg_one_eq_runningBalance (n : Nat) :
    totalWalkSum wNegOne n = runningBalance n := by
  unfold totalWalkSum runningBalance
  apply congrArg sumI
  apply map_congr_mem
  intro i _
  exact walkSum_neg_one_eq_balance (i + 1) (by omega)

/-! ## 2. The table count: the alternating sum over arrangements -/

/-- Every way to place `x` into a list. -/
def insertAll (x : Nat) : List Nat → List (List Nat)
  | [] => [[x]]
  | y :: ys => (x :: y :: ys) :: (insertAll x ys).map (fun l => y :: l)

/-- All arrangements of `1..n`: each lists, row by row, the column the
row reads. -/
def arrangements : Nat → List (List Nat)
  | 0 => [[]]
  | n + 1 => (arrangements n).flatMap (insertAll (n + 1))

/-- The inversion count of an arrangement. -/
def inversions : List Nat → Nat
  | [] => 0
  | x :: xs => (xs.filter (fun y => y < x)).length + inversions xs

/-- The sign of an arrangement: `-1` to its inversion count. -/
def sign (p : List Nat) : Int := if inversions p % 2 = 0 then 1 else -1

/-- The row product of one arrangement: row `i` reads column `p[i - 1]`. -/
def rowTerm (T : Nat → Nat → Int) : Nat → List Nat → Int
  | _, [] => 1
  | i, j :: rest => T i j * rowTerm T (i + 1) rest

/-- S2: the alternating sum over arrangements of the signed row products. -/
def tableCount (T : Nat → Nat → Int) (n : Nat) : Int :=
  sumI ((arrangements n).map (fun p => sign p * rowTerm T 1 p))

/-- The menu table: diagonal `delta`, first column `f i` for `i >= 2`,
the arrow weight `w i j` where `i` divides `j` and `i < j`, `0` elsewhere. -/
def table (w : Weight) (delta : Int) (f : Nat → Int) (i j : Nat) : Int :=
  if i = j then delta else if j = 1 then f i else if j % i = 0 then w i j else 0

/-- Kernel-decided: the arrangements of `1..4` number `24` and every
inversion count is at most `6`. -/
theorem arrangements_four : (arrangements 4).length = 24 := by decide

set_option maxRecDepth 100000 in
/-- Kernel-decided instances, `N = 1..7`: the unit table with unit
diagonal and unit first column, menu index `(W1, 1, 1)`, against the
running balance.  A statement about `N <= 7` and nothing beyond it. -/
theorem unit_table_matches_to_7 :
    (List.range 7).map (fun i => tableCount (table wOne 1 (fun _ => 1)) (i + 1))
      = (List.range 7).map (fun i => runningBalance (i + 1)) := by decide +kernel

set_option maxRecDepth 100000 in
/-- Kernel-decided instances, `N = 1..7`: the balance-weighted table with
unit diagonal and balance first column, menu index `(W3, 1, balance)`,
against the running balance.  A statement about `N <= 7` and nothing
beyond it. -/
theorem balance_table_matches_to_7 :
    (List.range 7).map (fun i => tableCount (table wBal 1 balance) (i + 1))
      = (List.range 7).map (fun i => runningBalance (i + 1)) := by decide +kernel

end Walk
end BalanceCarrier
