import BoundarySeed.Basic

/-!
# Continuation stage 1: the challenge generator, and the resource bounds

Core Lean only.  The Python side declares the branch set, the generator space
and its prices, and computes the minima; none of that is closed here, and the
paper says so.  What this file closes is the two things the enumeration cannot
close on its own, and each is about a FUNCTION rather than about a state.

The first is the weakest emitting generator itself, modelled at the level the
claim is made: a record of the indices already presented, a bound, and the
least index below the bound the record does not carry.
`firstMissing_not_present` says the challenge it names has not been presented;
`firstMissing_never_repeats` says that once the record carries it the same
challenge is never named again, so no branch can be fed one inscription for
ever; and `firstMissingFrom_none_means_every_index_present` says it falls
silent only when the record already carries every index below the bound — a
branch that stops for want of a next challenge stops because the declared
domain is exhausted and not because the procedure gave up.

The second is the resource bound.  `nodes` is the largest number of nodes a
tree of a declared branching can hold after a declared number of rounds; it
does not decrease as the rounds grow (`nodes_mono`), and at the declared
ceiling of one thousand the largest round count that fits is four under each
reading's branch count (`roundBound_U`, `roundBound_O`, with the two fitting
values beside them).  So the seed's fifteen does not fit, which is why an exact
frontier under a smaller declared bound is owed.

Nothing here is an object-language statement: a generator is metatheory, and a
bound is metatheory about the run's own enumeration.
-/

namespace BoundarySeed

/-! ## The enumeration generator -/

/-- The least index at or above `i`, within the given allowance, that the
record does not carry. -/
def firstMissingFrom (presented : List Nat) : Nat → Nat → Option Nat
  | _, 0 => none
  | i, f + 1 =>
      match presented.contains i with
      | true => firstMissingFrom presented (i + 1) f
      | false => some i

/-- The generator's own form: search from the first index, to the bound. -/
def firstMissing (presented : List Nat) (bound : Nat) : Option Nat :=
  firstMissingFrom presented 0 bound

/-- The three defining equations, named so that a proof can rewrite with them
and be left with constructors rather than with an unreduced match. -/
theorem firstMissingFrom_zero (p : List Nat) (i : Nat) :
    firstMissingFrom p i 0 = none := rfl

theorem firstMissingFrom_succ_present (p : List Nat) (i f : Nat)
    (hc : p.contains i = true) :
    firstMissingFrom p i (f + 1) = firstMissingFrom p (i + 1) f := by
  rw [firstMissingFrom, hc]

theorem firstMissingFrom_succ_missing (p : List Nat) (i f : Nat)
    (hc : p.contains i = false) : firstMissingFrom p i (f + 1) = some i := by
  rw [firstMissingFrom, hc]

/-- **What it names has not been presented.** -/
theorem firstMissingFrom_not_present (p : List Nat) :
    ∀ (f i j : Nat), firstMissingFrom p i f = some j → p.contains j = false := by
  intro f
  induction f with
  | zero => intro i j h; rw [firstMissingFrom_zero] at h; simp at h
  | succ k ih =>
    intro i j h
    cases hc : p.contains i with
    | true =>
        rw [firstMissingFrom_succ_present p i k hc] at h
        exact ih (i + 1) j h
    | false =>
        rw [firstMissingFrom_succ_missing p i k hc] at h
        have hij : i = j := Option.some.inj h
        exact hij ▸ hc

/-- It never names an index below where the search began. -/
theorem firstMissingFrom_ge (p : List Nat) :
    ∀ (f i j : Nat), firstMissingFrom p i f = some j → i ≤ j := by
  intro f
  induction f with
  | zero => intro i j h; rw [firstMissingFrom_zero] at h; simp at h
  | succ k ih =>
    intro i j h
    cases hc : p.contains i with
    | true =>
        rw [firstMissingFrom_succ_present p i k hc] at h
        exact Nat.le_trans (Nat.le_succ i) (ih (i + 1) j h)
    | false =>
        rw [firstMissingFrom_succ_missing p i k hc] at h
        exact Nat.le_of_eq (Option.some.inj h)

/-- **It stays inside the bound**: what it names lies below the allowance. -/
theorem firstMissingFrom_lt (p : List Nat) :
    ∀ (f i j : Nat), firstMissingFrom p i f = some j → j < i + f := by
  intro f
  induction f with
  | zero => intro i j h; rw [firstMissingFrom_zero] at h; simp at h
  | succ k ih =>
    intro i j h
    cases hc : p.contains i with
    | true =>
        rw [firstMissingFrom_succ_present p i k hc] at h
        have hj := ih (i + 1) j h
        omega
    | false =>
        rw [firstMissingFrom_succ_missing p i k hc] at h
        have hij : i = j := Option.some.inj h
        omega

/-- **It falls silent only when there is nothing left to name.**  If the search
returns nothing then every index it could have named is already in the record,
so a branch that stops for want of a next challenge stops because the declared
domain is exhausted. -/
theorem firstMissingFrom_none_means_every_index_present (p : List Nat) :
    ∀ (f i j : Nat), firstMissingFrom p i f = none → i ≤ j → j < i + f →
      p.contains j = true := by
  intro f
  induction f with
  | zero => intro i j _ hij hjf; omega
  | succ k ih =>
    intro i j h hij hjf
    cases hc : p.contains i with
    | true =>
        rw [firstMissingFrom_succ_present p i k hc] at h
        cases Nat.lt_or_ge i j with
        | inl hlt => exact ih (i + 1) j h hlt (by omega)
        | inr hge =>
            have hij' : i = j := Nat.le_antisymm hij hge
            exact hij' ▸ hc
    | false =>
        rw [firstMissingFrom_succ_missing p i k hc] at h
        simp at h

theorem firstMissing_not_present (p : List Nat) (bound j : Nat)
    (h : firstMissing p bound = some j) : p.contains j = false :=
  firstMissingFrom_not_present p bound 0 j h

theorem firstMissing_lt_bound (p : List Nat) (bound j : Nat)
    (h : firstMissing p bound = some j) : j < bound := by
  have hj := firstMissingFrom_lt p bound 0 j h
  omega

/-- A record with an index at its head carries that index. -/
theorem contains_cons_self (p : List Nat) (j : Nat) : (j :: p).contains j = true := by
  simp

/-- **A challenge once named is never named again.**  Record what the generator
named and it names something else, so no branch is fed one inscription for
ever. -/
theorem firstMissing_never_repeats (p : List Nat) (bound j : Nat) :
    firstMissing (j :: p) bound ≠ some j := by
  intro h
  have hno := firstMissing_not_present (j :: p) bound j h
  rw [contains_cons_self p j] at hno
  simp at hno

/-- Recording what was named lengthens the record by exactly one. -/
theorem record_lengthens (p : List Nat) (j : Nat) : (j :: p).length = p.length + 1 :=
  rfl

/-! ## The run's own record, and its first challenge -/

/-- Where the six presented texts lie in the declared domain's order. -/
def presentedIndices : List Nat := [0, 12, 1, 14, 25, 72]

/-- The declared domain's size. -/
def domainSize : Nat := 144

/-- The first challenge, at the index the Python enumeration reports. -/
theorem firstMissing_presentedIndices :
    firstMissing presentedIndices domainSize = some 2 := rfl

/-- And the next one, once that challenge is recorded: the generator moves on. -/
theorem firstMissing_presentedIndices_recorded :
    firstMissing (2 :: presentedIndices) domainSize = some 3 := rfl

/-! ## The resource bound -/

/-- The largest number of nodes a tree of this branching can hold after this
many rounds.  Nothing is pruned, so this is an upper bound and never a count. -/
def nodes (b k : Nat) : Nat → Nat
  | 0 => b
  | r + 1 => nodes b k r + b * k ^ (r + 1)

theorem nodes_le_succ (b k r : Nat) : nodes b k r ≤ nodes b k (r + 1) :=
  Nat.le_add_right _ _

theorem nodes_add_le (b k r d : Nat) : nodes b k r ≤ nodes b k (r + d) := by
  induction d with
  | zero => exact Nat.le_refl _
  | succ n ih => exact Nat.le_trans ih (nodes_le_succ b k (r + n))

/-- The node count does not decrease as the round count grows. -/
theorem nodes_mono (b k : Nat) {r s : Nat} (h : r ≤ s) : nodes b k r ≤ nodes b k s := by
  have hd : r + (s - r) = s := by omega
  have hle := nodes_add_le b k r (s - r)
  rw [hd] at hle
  exact hle

theorem nodes_U_four : nodes 6 3 4 = 726 := by decide

theorem nodes_U_five : nodes 6 3 5 = 2184 := by decide

theorem nodes_O_four : nodes 5 3 4 = 605 := by decide

theorem nodes_O_five : nodes 5 3 5 = 1820 := by decide

/-- Four rounds fit the declared ceiling under reading U's branch count. -/
theorem roundBound_U_fits : nodes 6 3 4 ≤ 1000 := by decide

/-- Four rounds fit it under reading O's branch count. -/
theorem roundBound_O_fits : nodes 5 3 4 ≤ 1000 := by decide

/-- **Four is the largest round count that fits under reading U.** -/
theorem roundBound_U (r : Nat) (h : nodes 6 3 r ≤ 1000) : r ≤ 4 := by
  cases Nat.lt_or_ge r 5 with
  | inl hlt => omega
  | inr hge =>
      have hle : nodes 6 3 5 ≤ nodes 6 3 r := nodes_mono 6 3 hge
      rw [nodes_U_five] at hle
      omega

/-- **And under reading O.** -/
theorem roundBound_O (r : Nat) (h : nodes 5 3 r ≤ 1000) : r ≤ 4 := by
  cases Nat.lt_or_ge r 5 with
  | inl hlt => omega
  | inr hge =>
      have hle : nodes 5 3 5 ≤ nodes 5 3 r := nodes_mono 5 3 hge
      rw [nodes_O_five] at hle
      omega

/-- **The seed's fifteen rounds do not fit the declared ceiling**, which is why
an exact frontier under a smaller declared bound is owed. -/
theorem the_seed_bound_does_not_fit_U : ¬ (nodes 6 3 15 ≤ 1000) := by
  intro h
  have hr := roundBound_U 15 h
  omega

theorem the_seed_bound_does_not_fit_O : ¬ (nodes 5 3 15 ≤ 1000) := by
  intro h
  have hr := roundBound_O 15 h
  omega

/-- The computed bound is short of the seed's. -/
theorem roundBound_is_short_of_the_seed_bound : 4 < 15 := by decide

end BoundarySeed
