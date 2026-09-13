import Limits

/-!
# Covering miss on an already-infinitary sequence space

Restatement of the covering definitions and theorems from
`research/unboundedness/lean/Continuum.lean` that do not mention `Metric`.
The formulas are the same; the module is this tree's, so a Lake path into
`research/unboundedness/lean` is not required.

What is proved: for `c ≥ 2`, no family `Nat → (Nat → Fin c)` covers
`Nat → Fin c`, and no family `Nat → Limits.Thread c` covers
`Limits.Thread c`.  The missed sequence is `diagSeq`; the missed thread
is `diagThread`.

What is not proved: cardinal arithmetic; any injection each way with
`Nat → Bool`; any finite-engine run reaching an uncountable boundary;
any identification with `PrimDiff.obstruction_under_irrefl`.

AuthorityEffect: None.
-/

namespace DiagonalIdentity.Covering

open Limits

/-- For any sequence of boolean sequences `f : Nat → (Nat → Bool)`,
the antidiagonal sequence `d n = ! (f n n)` differs from every `f n` at index `n`.
AuthorityEffect: None. -/
def diagBool (f : Nat → (Nat → Bool)) : Nat → Bool :=
  fun n => ! (f n n)

/-- No sequence of boolean sequences can cover `Nat → Bool`.
AuthorityEffect: None. -/
theorem diagonal_bool (f : Nat → (Nat → Bool)) :
    ∃ (d : Nat → Bool), ∀ n, f n ≠ d := by
  refine ⟨diagBool f, ?_⟩
  intro n h
  have hn := congrFun h n
  dsimp [diagBool] at hn
  cases hfn : f n n <;> rw [hfn] at hn <;> contradiction

/-- Given an element `x : Fin c` where `2 ≤ c`, choose a distinct element.
If `x.val = 0`, choose `1`; otherwise choose `0`.
AuthorityEffect: None. -/
def flipFin (c : Nat) (hc : 2 ≤ c) (x : Fin c) : Fin c :=
  if x.val = 0 then
    ⟨1, by omega⟩
  else
    ⟨0, by omega⟩

/-- The flipped element is always strictly distinct from the input.
AuthorityEffect: None. -/
theorem flipFin_ne (c : Nat) (hc : 2 ≤ c) (x : Fin c) : flipFin c hc x ≠ x := by
  intro h
  have hval := congrArg Fin.val h
  dsimp [flipFin] at hval
  by_cases h0 : x.val = 0
  · rw [if_pos h0] at hval
    rw [h0] at hval
    contradiction
  · rw [if_neg h0] at hval
    exact h0 hval.symm

/-- For any enumeration of sequences `S : Nat → (Nat → Fin c)` where `2 ≤ c`,
the diagonal sequence alters the `n`-th sequence at position `n`.
AuthorityEffect: None. -/
def diagSeq (c : Nat) (hc : 2 ≤ c) (S : Nat → (Nat → Fin c)) : Nat → Fin c :=
  fun n => flipFin c hc (S n n)

/-- The diagonal sequence differs from every sequence in the enumeration at its own index.
AuthorityEffect: None. -/
theorem diagSeq_diff_at (c : Nat) (hc : 2 ≤ c) (S : Nat → (Nat → Fin c)) (n : Nat) :
    diagSeq c hc S n ≠ S n n :=
  flipFin_ne c hc (S n n)

/-- No sequence can cover `Nat → Fin c` when `2 ≤ c`.
AuthorityEffect: None. -/
theorem seq_uncountable (c : Nat) (hc : 2 ≤ c) (S : Nat → (Nat → Fin c)) :
    ∃ (d : Nat → Fin c), ∀ n, S n ≠ d := by
  refine ⟨diagSeq c hc S, ?_⟩
  intro n hn
  have hn_at := congrFun hn n
  exact diagSeq_diff_at c hc S n hn_at.symm

/-- Given an enumeration of threads `T : Nat → Thread c` where `2 ≤ c`,
the diagonal thread is constructed by diagonalizing the corresponding sequence enumeration.
AuthorityEffect: None. -/
def diagThread (c : Nat) (hc : 2 ≤ c) (T : Nat → Thread c) : Thread c :=
  ofSeq c (diagSeq c hc (fun n => toSeq c (T n)))

/-- The diagonal thread disagrees with the `n`-th thread at position `n`.
AuthorityEffect: None. -/
theorem diagThread_diff_seq (c : Nat) (hc : 2 ≤ c) (T : Nat → Thread c) (n : Nat) :
    toSeq c (diagThread c hc T) n ≠ toSeq c (T n) n := by
  dsimp [diagThread]
  rw [toSeq_ofSeq]
  exact diagSeq_diff_at c hc (fun k => toSeq c (T k)) n

/-- **Non-enumerability of the thread space.**
No sequence of threads can cover `Thread c` when `2 ≤ c`.

Cite this by its type: it says every `T : Nat → Thread c` misses some thread.
It does **not** establish a cardinality; no injection with `Nat → Bool` is
constructed here.
AuthorityEffect: None. -/
theorem thread_uncountable (c : Nat) (hc : 2 ≤ c) (T : Nat → Thread c) :
    ∃ (t : Thread c), ∀ n, T n ≠ t := by
  refine ⟨diagThread c hc T, ?_⟩
  intro n hn
  have h_seq := congrArg (toSeq c) hn
  have h_val := congrFun h_seq n
  exact diagThread_diff_seq c hc T n h_val.symm

/-- No function from `Nat` to `Thread c` is surjective when `2 ≤ c`.
AuthorityEffect: None. -/
theorem not_surjective_nat_to_thread (c : Nat) (hc : 2 ≤ c) (T : Nat → Thread c) :
    ¬ (∀ (t : Thread c), ∃ n, T n = t) := by
  intro hsurj
  obtain ⟨t, hne⟩ := thread_uncountable c hc T
  obtain ⟨n, rfl⟩ := hsurj t
  exact hne n rfl

end DiagonalIdentity.Covering
