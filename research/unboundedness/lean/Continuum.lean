import Limits
import Metric

/-!
# Continuum: non-enumerability of the already-infinitary thread space

This module proves that for any branching factor `c ≥ 2`, no family
`T : Nat → Thread c` covers `Thread c`. That is non-enumerability of a
space whose infinitary index was supplied by its definition, not a
finite-to-continuum ladder.

**Scope, stated once and honoured throughout.** What is proved here is
non-enumerability: for every family `T : Nat → Thread c` there is a thread no
`T n` equals. No cardinal arithmetic is carried out, and **no claim that
`|Thread c| = 2^ℵ₀` is made or proved** — that would require exhibiting an
injection each way with `Nat → Bool`, which this module does not do.

**What this does NOT show.** `Thread c` is *defined* in `Limits.lean` as a
compatible family over every scale `n : Nat`, and `toSeq_ofSeq` / `ofSeq_toSeq`
prove it *is* the sequence space `Nat → Fin c` — "a bijection and nothing
more", in that module's own words. The diagonal below is therefore the
standard diagonal argument applied to an object whose infinitary index was
supplied by its definition. It does not exhibit a finite engine run reaching
an uncountable boundary, and it does not treat an uncountable path space as a
consequence of the finite system.

## 1. Diagonal argument on sequences
No sequence of binary sequences can cover `Nat → Bool` (`diagonal_bool`).
For any alphabet `c ≥ 2`, no sequence of sequences can cover `Nat → Fin c` (`seq_uncountable`).

## 2. Uncountability of the Thread Space
Because `Limits.toSeq` and `Limits.ofSeq` form a constructive bijection between
`Thread c` and `Nat → Fin c` (`toSeq_ofSeq`, `ofSeq_toSeq`), no enumeration
`T : Nat → Thread c` can cover `Thread c` (`thread_uncountable`).

## 3. Explicit Metric Separation
For any enumeration `T : Nat → Thread c`, the diagonal thread `diagThread c hc T`
is separated from the `n`-th thread `T n` at scale `n + 1`:
`¬ Agrees c (T n) (diagThread c hc T) (n + 1)` (`thread_not_agrees_diagonal`).

`Metric.limit_converges` is convergence of `IsCoherent` families under
`DistLe := Agrees`, not an arbitrary distance-valued Cauchy sequence.
`Limits.twins_are_two_threads` refuses one identification of two sequences.
Neither is total disconnectedness of a metric completion, and neither
computes a cardinality.

AuthorityEffect: None.
-/

namespace Continuum

open Limits Metric

/-! ## 1. Diagonalization on Boolean sequences -/

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

/-! ## 2. Diagonalization on sequences over `Fin c` for `c ≥ 2` -/

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

/-! ## 3. Uncountability of the thread space -/

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
It does **not** say `|Thread c| = 2^ℵ₀`; no cardinality is established here.
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

/-! ## 4. Metric separation of the diagonal thread -/

/-- At scale `n + 1`, the `n`-th thread `T n` disagrees with the diagonal thread.
AuthorityEffect: None. -/
theorem thread_not_agrees_diagonal (c : Nat) (hc : 2 ≤ c) (T : Nat → Thread c) (n : Nat) :
    ¬ Agrees c (T n) (diagThread c hc T) (n + 1) := by
  intro hagrees
  have hseq : toSeq c (T n) n = toSeq c (diagThread c hc T) n := by
    rw [agrees_iff_toSeq] at hagrees
    exact hagrees n (Nat.lt_succ_self n)
  exact diagThread_diff_seq c hc T n hseq.symm

/-- Any candidate countable coverage fails at every point: the diagonal thread is
separated from each `T n` at scale `n + 1`.
AuthorityEffect: None. -/
theorem thread_diag_dist_pos (c : Nat) (hc : 2 ≤ c) (T : Nat → Thread c) (n : Nat) :
    (T n).val (n + 1) ≠ (diagThread c hc T).val (n + 1) := by
  intro heq
  exact thread_not_agrees_diagonal c hc T n heq

end Continuum

#print axioms Continuum.diagonal_bool
#print axioms Continuum.flipFin_ne
#print axioms Continuum.diagSeq_diff_at
#print axioms Continuum.seq_uncountable
#print axioms Continuum.diagThread_diff_seq
#print axioms Continuum.thread_uncountable
#print axioms Continuum.not_surjective_nat_to_thread
#print axioms Continuum.thread_not_agrees_diagonal
#print axioms Continuum.thread_diag_dist_pos
