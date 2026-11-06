import ResearchInstitutionForces.Joint

/-!
# L1: robustness of knowledge against replaced or deleted seats

AuthorityEffect: None.  Outside the seal.

* `Repl k Q Q'`: `Q'` is `Q` with at most `k` seats replaced.  Both lists
  have the same length; a replaced seat may receive any presentation,
  including the one it had.  The relation is defined by list recursion,
  one constructor per seat, so "at most `k`" is a count of constructors,
  not a quantifier over an infinite set of positions.
* `robust_iff` (L1): `Q'` knows `q` for every such `Q'` exactly when every
  pair of `D` that `q` separates has at least `k + 1` separating seats.
  The necessity direction builds the replacement: each separating seat of
  the weak pair gets the constant `0` (`blunt`).
* `Del k Q K`: `K` is `Q` with at most `k` seats deleted.
  `deletion_robust_iff` is the same count for deletion.  Deletion and
  replacement by a constant have the same effect on knowledge, so the two
  thresholds coincide.
* `robustB`: the condition as a Boolean computation over the carrier,
  `robustB_iff` its correctness, and `robust_parity_half` the four-point
  family with its exact robustness, before and after duplicating it.

The theorems speak of determination only.  A replaced seat can also add
separations that are false of a target; that never breaks knowledge
(knowledge is monotone in the family) and is the separate question of
`ResearchActorInstitution.Chain.determination_not_truth`.
-/

namespace ResearchInstitutionForces
namespace Robust

open Compression ResearchTwoTheorems.Institution Joint

/-- `Repl k Q Q'`: `Q'` is `Q` with at most `k` seats replaced. -/
inductive Repl : Nat → Institution → Institution → Prop
  | nil (k : Nat) : Repl k [] []
  | keep {k : Nat} {Q Q' : Institution} (m : Nat → Nat) :
      Repl k Q Q' → Repl k (m :: Q) (m :: Q')
  | swap {k : Nat} {Q Q' : Institution} (m m' : Nat → Nat) :
      Repl k Q Q' → Repl (k + 1) (m :: Q) (m' :: Q')

theorem repl_refl (k : Nat) : ∀ Q : Institution, Repl k Q Q := by
  intro Q
  induction Q with
  | nil => exact Repl.nil k
  | cons m Q ih => exact Repl.keep m ih

theorem repl_mono {k : Nat} {Q Q' : Institution} (h : Repl k Q Q') :
    ∀ k', k ≤ k' → Repl k' Q Q' := by
  induction h with
  | nil _ => intro k' _; exact Repl.nil k'
  | keep m _ ih => intro k' hk; exact Repl.keep m (ih k' hk)
  | swap m m' _ ih =>
    rename_i j _ _ _
    intro k' hk
    obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hk
    have e : j + 1 + d = (j + d) + 1 := by omega
    rw [e]
    exact Repl.swap m m' (ih (j + d) (Nat.le_add_right j d))

theorem repl_length {k : Nat} {Q Q' : Institution} (h : Repl k Q Q') :
    Q'.length = Q.length := by
  induction h with
  | nil _ => rfl
  | keep _ _ ih => rw [List.length_cons, List.length_cons, ih]
  | swap _ _ _ ih => rw [List.length_cons, List.length_cons, ih]

/-- Replacing at most `k` seats removes at most `k` separating seats. -/
theorem redundancy_le_repl {k : Nat} {Q Q' : Institution} (h : Repl k Q Q')
    (x y : Nat) : redundancy Q x y ≤ k + redundancy Q' x y := by
  induction h with
  | nil k => exact Nat.zero_le _
  | keep m _ ih =>
    rw [redundancy_cons, redundancy_cons]
    omega
  | swap m m' _ ih =>
    rw [redundancy_cons, redundancy_cons]
    have h1 := sepCount_le_one m x y
    omega

/-- Replace every seat that separates `x` from `y` by the constant `0`. -/
def blunt (x y : Nat) : Institution → Institution
  | [] => []
  | m :: Q => (if m x = m y then m else fun _ => 0) :: blunt x y Q

theorem repl_blunt (x y : Nat) :
    ∀ Q : Institution, Repl (redundancy Q x y) Q (blunt x y Q) := by
  intro Q
  induction Q with
  | nil => exact Repl.nil 0
  | cons m Q ih =>
    show Repl (sepCount m x y + redundancy Q x y) (m :: Q)
      ((if m x = m y then m else fun _ => 0) :: blunt x y Q)
    cases Nat.decEq (m x) (m y) with
    | isTrue e =>
      rw [if_pos e, sepCount_eq_zero e, Nat.zero_add]
      exact Repl.keep m ih
    | isFalse ne =>
      rw [if_neg ne, sepCount_eq_one ne, Nat.add_comm]
      exact Repl.swap m _ ih

theorem sigEq_blunt (x y : Nat) : ∀ Q : Institution, SigEq (blunt x y Q) x y := by
  intro Q
  induction Q with
  | nil => intro p hp; cases hp
  | cons m Q ih =>
    intro p hp
    rcases List.mem_cons.mp hp with h | h
    · rw [h]
      cases Nat.decEq (m x) (m y) with
      | isTrue e => rw [if_pos e]; exact e
      | isFalse ne => rw [if_neg ne]
    · exact ih p h

/-- **L1, k-robustness.**  Every family obtained from `Q` by replacing at
most `k` seats knows `q` on `D` exactly when every pair of `D` that `q`
separates has at least `k + 1` separating seats in `Q`. -/
theorem robust_iff (D : List Nat) (Q : Institution) (q : Nat → Nat) (k : Nat) :
    (∀ Q', Repl k Q Q' → Knows D Q' q) ↔
      ∀ x, x ∈ D → ∀ y, y ∈ D → q x ≠ q y → k + 1 ≤ redundancy Q x y := by
  constructor
  · intro h x hx y hy hne
    cases Nat.decLe (k + 1) (redundancy Q x y) with
    | isTrue hle => exact hle
    | isFalse hlt =>
      exfalso
      have hle : redundancy Q x y ≤ k := by omega
      have hk := h (blunt x y Q) (repl_mono (repl_blunt x y Q) k hle)
      exact hne ((knows_iff_determined D _ q).mp hk x hx y hy (sigEq_blunt x y Q))
  · intro h Q' hr
    rw [knows_iff_determined]
    intro x hx y hy hs
    cases Nat.decEq (q x) (q y) with
    | isTrue e => exact e
    | isFalse ne =>
      exfalso
      have h1 := h x hx y hy ne
      have h2 := redundancy_le_repl hr x y
      have h3 : 0 < redundancy Q' x y := by omega
      exact (redundancy_pos_iff_not_sigEq Q' x y).mp h3 hs

theorem repl_zero_aux {k : Nat} {Q Q' : Institution} (h : Repl k Q Q') :
    k = 0 → Q' = Q := by
  induction h with
  | nil _ => intro _; rfl
  | keep m _ ih => intro e; rw [ih e]
  | swap _ _ _ _ => intro e; exact absurd e (Nat.succ_ne_zero _)

/-- At `k = 0` the only replacement is `Q` itself, and L1 is
`knows_iff_redundancy`. -/
theorem repl_zero {Q Q' : Institution} (h : Repl 0 Q Q') : Q' = Q :=
  repl_zero_aux h rfl

/-! ## Deletion -/

/-- `Del k Q K`: `K` is `Q` with at most `k` seats deleted. -/
inductive Del : Nat → Institution → Institution → Prop
  | nil (k : Nat) : Del k [] []
  | keep {k : Nat} {Q K : Institution} (m : Nat → Nat) :
      Del k Q K → Del k (m :: Q) (m :: K)
  | drop {k : Nat} {Q K : Institution} (m : Nat → Nat) :
      Del k Q K → Del (k + 1) (m :: Q) K

theorem del_mono {k : Nat} {Q K : Institution} (h : Del k Q K) :
    ∀ k', k ≤ k' → Del k' Q K := by
  induction h with
  | nil _ => intro k' _; exact Del.nil k'
  | keep m _ ih => intro k' hk; exact Del.keep m (ih k' hk)
  | drop m _ ih =>
    rename_i j _ _ _
    intro k' hk
    obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hk
    have e : j + 1 + d = (j + d) + 1 := by omega
    rw [e]
    exact Del.drop m (ih (j + d) (Nat.le_add_right j d))

theorem redundancy_le_del {k : Nat} {Q K : Institution} (h : Del k Q K)
    (x y : Nat) : redundancy Q x y ≤ k + redundancy K x y := by
  induction h with
  | nil k => exact Nat.zero_le _
  | keep m _ ih =>
    rw [redundancy_cons, redundancy_cons]
    omega
  | drop m _ ih =>
    rw [redundancy_cons]
    have h1 := sepCount_le_one m x y
    omega

/-- Keep the seats that do not separate `x` from `y`. -/
def agreeing (x y : Nat) : Institution → Institution
  | [] => []
  | m :: Q => if m x = m y then m :: agreeing x y Q else agreeing x y Q

theorem del_agreeing (x y : Nat) :
    ∀ Q : Institution, Del (redundancy Q x y) Q (agreeing x y Q) := by
  intro Q
  induction Q with
  | nil => exact Del.nil 0
  | cons m Q ih =>
    show Del (sepCount m x y + redundancy Q x y) (m :: Q)
      (if m x = m y then m :: agreeing x y Q else agreeing x y Q)
    cases Nat.decEq (m x) (m y) with
    | isTrue e =>
      rw [if_pos e, sepCount_eq_zero e, Nat.zero_add]
      exact Del.keep m ih
    | isFalse ne =>
      rw [if_neg ne, sepCount_eq_one ne, Nat.add_comm]
      exact Del.drop m ih

theorem sigEq_agreeing (x y : Nat) : ∀ Q : Institution, SigEq (agreeing x y Q) x y := by
  intro Q
  induction Q with
  | nil => intro p hp; cases hp
  | cons m Q ih =>
    intro p hp
    have hp' : p ∈ (if m x = m y then m :: agreeing x y Q else agreeing x y Q) := hp
    cases Nat.decEq (m x) (m y) with
    | isTrue e =>
      rw [if_pos e] at hp'
      rcases List.mem_cons.mp hp' with h | h
      · rw [h]; exact e
      · exact ih p h
    | isFalse ne =>
      rw [if_neg ne] at hp'
      exact ih p hp'

/-- **L1 for deletion.**  Every family obtained from `Q` by deleting at
most `k` seats knows `q` exactly when every `q`-separated pair has at least
`k + 1` separating seats: the same threshold as for replacement. -/
theorem deletion_robust_iff (D : List Nat) (Q : Institution) (q : Nat → Nat) (k : Nat) :
    (∀ K, Del k Q K → Knows D K q) ↔
      ∀ x, x ∈ D → ∀ y, y ∈ D → q x ≠ q y → k + 1 ≤ redundancy Q x y := by
  constructor
  · intro h x hx y hy hne
    cases Nat.decLe (k + 1) (redundancy Q x y) with
    | isTrue hle => exact hle
    | isFalse hlt =>
      exfalso
      have hle : redundancy Q x y ≤ k := by omega
      have hk := h (agreeing x y Q) (del_mono (del_agreeing x y Q) k hle)
      exact hne ((knows_iff_determined D _ q).mp hk x hx y hy (sigEq_agreeing x y Q))
  · intro h K hd
    rw [knows_iff_determined]
    intro x hx y hy hs
    cases Nat.decEq (q x) (q y) with
    | isTrue e => exact e
    | isFalse ne =>
      exfalso
      have h1 := h x hx y hy ne
      have h2 := redundancy_le_del hd x y
      have h3 : 0 < redundancy K x y := by omega
      exact (redundancy_pos_iff_not_sigEq K x y).mp h3 hs

/-! ## The count, computed -/

/-- The L1 condition as a Boolean computation over the carrier. -/
def robustB (D : List Nat) (Q : Institution) (q : Nat → Nat) (k : Nat) : Bool :=
  D.all (fun x => D.all (fun y =>
    decide (q x = q y) || decide (k + 1 ≤ redundancy Q x y)))

theorem robustB_iff (D : List Nat) (Q : Institution) (q : Nat → Nat) (k : Nat) :
    robustB D Q q k = true ↔
      ∀ x, x ∈ D → ∀ y, y ∈ D → q x ≠ q y → k + 1 ≤ redundancy Q x y := by
  unfold robustB
  rw [List.all_eq_true]
  constructor
  · intro h x hx y hy hne
    have h1 := h x hx
    rw [List.all_eq_true] at h1
    rcases Bool.or_eq_true_iff.mp (h1 y hy) with e | e
    · exact absurd (of_decide_eq_true e) hne
    · exact of_decide_eq_true e
  · intro h x hx
    rw [List.all_eq_true]
    intro y hy
    cases Nat.decEq (q x) (q y) with
    | isTrue e => rw [decide_eq_true e, Bool.true_or]
    | isFalse ne => rw [decide_eq_true (h x hx y hy ne), Bool.or_true]

/-- On four points `[parity, half]` knows the identity with no slack: one
replaced seat can break it.  Duplicating the family gives every
identity-separated pair at least two seats, so one replaced seat cannot
break it and two can.  The duplicate counts as an independent seat; one
source feeding both copies would make the count overstate robustness. -/
theorem robust_parity_half :
    robustB [0, 1, 2, 3] [parity, half] (fun x => x) 0 = true ∧
    robustB [0, 1, 2, 3] [parity, half] (fun x => x) 1 = false ∧
    robustB [0, 1, 2, 3] [parity, half, parity, half] (fun x => x) 1 = true ∧
    robustB [0, 1, 2, 3] [parity, half, parity, half] (fun x => x) 2 = false := by
  decide

end Robust
end ResearchInstitutionForces
