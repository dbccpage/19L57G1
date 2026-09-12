import Limits
import Periodic

/-!
# Limits.Metric: ultrametric structure and completeness of the thread space

This module establishes the metric and topological structure of `Thread c`
under constructive principles.

Observations at scale `n` are words of length `n` (`Stage c n`).
Two threads agree up to scale `n` when their scale-`n` observations coincide
(`Agrees`).  Because bonding forgets the final entry, agreement at scale `n + 1`
implies agreement at scale `n`.

Three properties characterize this structure:
1. **Ultrametric prefix structure.**  Agreement at scale `n` satisfies reflexivity,
   symmetry, transitivity, identity of indiscernibles across all scales, and the
   strong triangle inequality (`agrees_min`): agreement between `s` and `u` extends
   to at least `min j k` when `s, t` agree to `j` and `t, u` agree to `k`.
2. **Completeness.**  Every coherent sequence of threads (a Cauchy sequence
   represented constructively by compatible prefixes) converges to a unique thread
   in `Thread c` (`limit`, `limit_converges`, `limit_unique`).
3. **The process image as a closed proper subset.**  A sequence produced by deterministic
   execution is functional: identical entries produce identical successors.
   Functional threads form a proper closed subset of `Thread c`.  On a finite carrier,
   every functional thread is eventually periodic (`functional_thread_is_eventually_periodic`).
   In contrast, the set of arbitrary eventually periodic threads is dense in `Thread c`
   (`eventually_periodic_dense`).

AuthorityEffect: None.
-/

namespace Limits

/-!
## 1. Prefix agreement and ultrametric structure
AuthorityEffect: None.
-/

/-- Two threads agree up to scale `n` if their observations at scale `n` coincide.
AuthorityEffect: None. -/
def Agrees (c : Nat) (s t : Thread c) (n : Nat) : Prop :=
  s.val n = t.val n

/-- Agreement is reflexive.
AuthorityEffect: None. -/
theorem agrees_refl (c : Nat) (s : Thread c) (n : Nat) : Agrees c s s n := rfl

/-- Agreement is symmetric.
AuthorityEffect: None. -/
theorem agrees_symm (c : Nat) {s t : Thread c} {n : Nat} (h : Agrees c s t n) : Agrees c t s n :=
  h.symm

/-- Agreement is transitive.
AuthorityEffect: None. -/
theorem agrees_trans (c : Nat) {s t u : Thread c} {n : Nat}
    (h1 : Agrees c s t n) (h2 : Agrees c t u n) : Agrees c s u n :=
  h1.trans h2

/-- At scale 0, all observations are on `Fin 0` and therefore all threads agree.
AuthorityEffect: None. -/
theorem agrees_zero (c : Nat) (s t : Thread c) : Agrees c s t 0 := by
  show s.val 0 = t.val 0
  funext i
  exact absurd i.isLt (Nat.not_lt_zero i.val)

/-- Agreement at scale `n` implies agreement at any smaller scale `m ≤ n`.
AuthorityEffect: None. -/
theorem agrees_le (c : Nat) {s t : Thread c} {m n : Nat} (hmn : m ≤ n)
    (h : Agrees c s t n) : Agrees c s t m := by
  show s.val m = t.val m
  funext i
  have hsi := stable c s n m hmn i.val i.isLt (Nat.lt_of_lt_of_le i.isLt hmn)
  have hti := stable c t n m hmn i.val i.isLt (Nat.lt_of_lt_of_le i.isLt hmn)
  have heq : s.val n ⟨i.val, Nat.lt_of_lt_of_le i.isLt hmn⟩ =
             t.val n ⟨i.val, Nat.lt_of_lt_of_le i.isLt hmn⟩ := by
    rw [h]
  rw [← hsi, heq, hti]

/-- The strong ultrametric triangle inequality: agreement depth satisfies
`depth(s, u) ≥ min(depth(s, t), depth(t, u))`.
AuthorityEffect: None. -/
theorem agrees_min (c : Nat) {s t u : Thread c} {j k : Nat}
    (h1 : Agrees c s t j) (h2 : Agrees c t u k) : Agrees c s u (min j k) := by
  have hj : min j k ≤ j := Nat.min_le_left j k
  have hk : min j k ≤ k := Nat.min_le_right j k
  have h1' := agrees_le c hj h1
  have h2' := agrees_le c hk h2
  exact agrees_trans c h1' h2'

/-- Identity of indiscernibles: agreement at all scales determines thread identity.
AuthorityEffect: None. -/
theorem threads_eq_of_agrees_all (c : Nat) (s t : Thread c) (h : ∀ n, Agrees c s t n) : s = t := by
  apply Subtype.ext
  funext n
  exact h n

/-- Agreement at scale `n` coincides with agreement of sequences on the initial segment `0 ≤ i < n`.
AuthorityEffect: None. -/
theorem agrees_iff_toSeq (c : Nat) (s t : Thread c) (n : Nat) :
    Agrees c s t n ↔ ∀ (i : Nat), i < n → toSeq c s i = toSeq c t i := by
  constructor
  · intro h i hi
    show s.val (i + 1) ⟨i, Nat.lt_succ_self i⟩ = t.val (i + 1) ⟨i, Nat.lt_succ_self i⟩
    have hsi := stable c s n (i + 1) (Nat.succ_le_of_lt hi) i (Nat.lt_succ_self i) hi
    have hti := stable c t n (i + 1) (Nat.succ_le_of_lt hi) i (Nat.lt_succ_self i) hi
    have hsn : s.val n ⟨i, hi⟩ = t.val n ⟨i, hi⟩ := by rw [h]
    rw [← hsi, hsn, hti]
  · intro h
    show s.val n = t.val n
    funext i
    have hs := stable c s n (i.val + 1) (Nat.succ_le_of_lt i.isLt) i.val (Nat.lt_succ_self i.val) i.isLt
    have ht := stable c t n (i.val + 1) (Nat.succ_le_of_lt i.isLt) i.val (Nat.lt_succ_self i.val) i.isLt
    have hi : toSeq c s i.val = toSeq c t i.val := h i.val i.isLt
    have h1 : s.val n i = s.val (i.val + 1) ⟨i.val, Nat.lt_succ_self i.val⟩ := hs
    have h2 : t.val n i = t.val (i.val + 1) ⟨i.val, Nat.lt_succ_self i.val⟩ := ht
    rw [h1, h2]
    exact hi

/-!
## 2. Computable agreement and difference detection
AuthorityEffect: None.
-/

/-- Computable decision for agreement of sequence prefixes.
AuthorityEffect: None. -/
def seqAgrees (s t : Nat → Nat) : Nat → Bool
  | 0 => true
  | n + 1 => seqAgrees s t n && (s n == t n)

/-- `seqAgrees` reflects equality on all indices `i < n`.
AuthorityEffect: None. -/
theorem seqAgrees_iff (s t : Nat → Nat) :
    ∀ (n : Nat), seqAgrees s t n = true ↔ ∀ (i : Nat), i < n → s i = t i
  | 0 => by
      simp [seqAgrees]
  | n + 1 => by
      simp only [seqAgrees, Bool.and_eq_true, beq_iff_eq]
      rw [seqAgrees_iff s t n]
      constructor
      · rintro ⟨hrec, hlast⟩ i hi
        rcases Nat.lt_or_eq_of_le (Nat.le_of_lt_succ hi) with hlt | heq
        · exact hrec i hlt
        · rw [heq, hlast]
      · intro h
        refine ⟨fun i hi => h i (Nat.lt_trans hi (Nat.lt_succ_self n)), ?_⟩
        exact h n (Nat.lt_succ_self n)

/-- Computable decision of whether two threads agree up to scale `n`.
AuthorityEffect: None. -/
def threadAgrees (c : Nat) (s t : Thread c) (n : Nat) : Bool :=
  seqAgrees (fun i => (toSeq c s i).val) (fun i => (toSeq c t i).val) n

/-- The computable check coincides with the prefix agreement property.
AuthorityEffect: None. -/
theorem threadAgrees_iff (c : Nat) (s t : Thread c) (n : Nat) :
    threadAgrees c s t n = true ↔ Agrees c s t n := by
  rw [threadAgrees, seqAgrees_iff, agrees_iff_toSeq]
  constructor
  · intro h i hi
    have heq := h i hi
    exact Fin.ext heq
  · intro h i hi
    have heq := h i hi
    exact congrArg Fin.val heq

instance (c : Nat) (s t : Thread c) (n : Nat) : Decidable (Agrees c s t n) :=
  decidable_of_iff (threadAgrees c s t n = true) (threadAgrees_iff c s t n)

/-- Computable agreement depth up to a given bound `B`: returns the largest `k ≤ B`
such that `s` and `t` agree up to scale `k`.
AuthorityEffect: None. -/
def agreeDepthBounded (c : Nat) (s t : Thread c) : Nat → Nat
  | 0 => 0
  | n + 1 => if threadAgrees c s t (n + 1) then n + 1 else agreeDepthBounded c s t n

/-- First difference index up to bound `B`, if one exists.
AuthorityEffect: None. -/
def firstDiffBounded (c : Nat) (s t : Thread c) : Nat → Option Nat
  | 0 => none
  | n + 1 =>
      match firstDiffBounded c s t n with
      | some i => some i
      | none =>
          if (toSeq c s n).val = (toSeq c t n).val then none
          else some n

/-- If no difference is found up to scale `n`, the threads agree up to scale `n`.
AuthorityEffect: None. -/
theorem firstDiffBounded_none (c : Nat) (s t : Thread c) :
    ∀ (n : Nat), firstDiffBounded c s t n = none → Agrees c s t n
  | 0, _ => agrees_zero c s t
  | n + 1, h => by
      dsimp [firstDiffBounded] at h
      cases hprev : firstDiffBounded c s t n with
      | some i =>
          rw [hprev] at h
          contradiction
      | none =>
          rw [hprev] at h
          have hrec := firstDiffBounded_none c s t n hprev
          dsimp at h
          split at h
          · rename_i heq_val
            have heq_n : toSeq c s n = toSeq c t n := Fin.ext heq_val
            rw [agrees_iff_toSeq] at hrec ⊢
            intro i hi
            rcases Nat.lt_or_eq_of_le (Nat.le_of_lt_succ hi) with hlt | heq
            · exact hrec i hlt
            · rw [heq, heq_n]
          · contradiction

/-- If a difference is found at index `i`, then `s` and `t` differ at `i` and agree on all `j < i`.
AuthorityEffect: None. -/
theorem firstDiffBounded_some (c : Nat) (s t : Thread c) :
    ∀ (n : Nat) (i : Nat), firstDiffBounded c s t n = some i →
      i < n ∧ toSeq c s i ≠ toSeq c t i ∧ Agrees c s t i
  | 0, i, h => by
      dsimp [firstDiffBounded] at h
      contradiction
  | n + 1, i, h => by
      dsimp [firstDiffBounded] at h
      cases hprev : firstDiffBounded c s t n with
      | some j =>
          rw [hprev] at h
          injection h with hij
          subst hij
          have ⟨hj_lt, hj_ne, hj_agr⟩ := firstDiffBounded_some c s t n j hprev
          exact ⟨Nat.lt_trans hj_lt (Nat.lt_succ_self n), hj_ne, hj_agr⟩
      | none =>
          rw [hprev] at h
          have hrec := firstDiffBounded_none c s t n hprev
          dsimp at h
          split at h
          · contradiction
          · rename_i hne_val
            injection h with hin
            subst hin
            have hne : toSeq c s n ≠ toSeq c t n := by
              intro heq
              exact hne_val (congrArg Fin.val heq)
            exact ⟨Nat.lt_succ_self n, hne, hrec⟩

/-!
## 3. Prefix distance bounds and strong triangle inequality
AuthorityEffect: None.
-/

/-- Relational distance bound: `DistLe c s t k` expresses that the distance between
threads `s` and `t` is bounded by `2^{-k}` (they agree up to scale `k`).
AuthorityEffect: None. -/
def DistLe (c : Nat) (s t : Thread c) (k : Nat) : Prop :=
  Agrees c s t k

/-- Bound at scale 0: all threads have distance bounded by `2^0 = 1`.
AuthorityEffect: None. -/
theorem distLe_zero (c : Nat) (s t : Thread c) : DistLe c s t 0 :=
  agrees_zero c s t

/-- Symmetry of distance bound.
AuthorityEffect: None. -/
theorem distLe_symm (c : Nat) {s t : Thread c} {k : Nat} (h : DistLe c s t k) : DistLe c t s k :=
  agrees_symm c h

/-- Identity of indiscernibles: distance is zero (distance bounded by `2^{-k}` for all `k`)
if and only if the threads are identical.
AuthorityEffect: None. -/
theorem distLe_indiscernibles (c : Nat) (s t : Thread c) : (∀ k, DistLe c s t k) ↔ s = t := by
  constructor
  · exact threads_eq_of_agrees_all c s t
  · rintro rfl k
    exact agrees_refl c s k

/-- Strong ultrametric triangle inequality: `d(s, u) ≤ max(d(s, t), d(t, u))`.
In scale indexing, agreement depth satisfies `depth(s, u) ≥ min(depth(s, t), depth(t, u))`.
AuthorityEffect: None. -/
theorem distLe_ultrametric (c : Nat) {s t u : Thread c} {j k : Nat}
    (h1 : DistLe c s t j) (h2 : DistLe c t u k) : DistLe c s u (min j k) :=
  agrees_min c h1 h2

/-- Specialization of the strong triangle inequality at matching scales:
if `d(s, t) ≤ 2^{-k}` and `d(t, u) ≤ 2^{-k}`, then `d(s, u) ≤ 2^{-k}`.
AuthorityEffect: None. -/
theorem distLe_trans (c : Nat) {s t u : Thread c} {k : Nat}
    (h1 : DistLe c s t k) (h2 : DistLe c t u k) : DistLe c s u k := by
  have hmin := distLe_ultrametric c h1 h2
  rw [Nat.min_self] at hmin
  exact hmin

/-- Open/closed ball of radius `2^{-k}` centered at `s`: the set of threads agreeing with `s`
up to scale `k`.
AuthorityEffect: None. -/
def Ball (c : Nat) (s : Thread c) (k : Nat) (t : Thread c) : Prop :=
  Agrees c s t k

/-- The center of a ball belongs to the ball.
AuthorityEffect: None. -/
theorem ball_self (c : Nat) (s : Thread c) (k : Nat) : Ball c s k s :=
  agrees_refl c s k

/-- In an ultrametric space, every point of a ball is a center of the ball.
AuthorityEffect: None. -/
theorem ball_point_is_center (c : Nat) {s t : Thread c} {k : Nat} (h : Ball c s k t) :
    ∀ (u : Thread c), Ball c s k u ↔ Ball c t k u := by
  intro u
  show Agrees c s u k ↔ Agrees c t u k
  constructor
  · intro hsu
    exact agrees_trans c (agrees_symm c h) hsu
  · intro htu
    exact agrees_trans c h htu

/-- Two balls at matching radius are either disjoint or coincide.
AuthorityEffect: None. -/
theorem balls_disjoint_or_coincide (c : Nat) (s t : Thread c) (k : Nat) :
    (∃ (u : Thread c), Ball c s k u ∧ Ball c t k u) → (∀ (v : Thread c), Ball c s k v ↔ Ball c t k v) := by
  rintro ⟨u, hsu, htu⟩ v
  have hst : Agrees c s t k := agrees_trans c hsu (agrees_symm c htu)
  exact ball_point_is_center c hst v

/-!
## 4. Completeness of the thread space
AuthorityEffect: None.
-/

/-- A coherent sequence of threads: for each scale `n`, all subsequent terms `m ≥ n`
agree with term `n` at scale `n`.  This is the constructive representation of a Cauchy
sequence with standard modulus.
AuthorityEffect: None. -/
def IsCoherent (c : Nat) (T : Nat → Thread c) : Prop :=
  ∀ (n m : Nat), n ≤ m → Agrees c (T m) (T n) n

/-- The limit family of a coherent sequence of threads: take scale `n` from thread `T n`.
AuthorityEffect: None. -/
def limitFamily (c : Nat) (T : Nat → Thread c) : (n : Nat) → Stage c n :=
  fun n => (T n).val n

/-- The limit family satisfies the bonding condition at every scale, verified by
coherence between `T (n + 1)` and `T n` at scale `n`.
AuthorityEffect: None. -/
theorem limit_compatible (c : Nat) (T : Nat → Thread c) (hT : IsCoherent c T) :
    Compatible c (limitFamily c T) := by
  intro n
  show bond c n ((T (n + 1)).val (n + 1)) = (T n).val n
  have hcomp := (T (n + 1)).property n
  have hcoh := hT n (n + 1) (Nat.le_succ n)
  rw [hcomp]
  exact hcoh

/-- The limit thread of a coherent sequence.
AuthorityEffect: None. -/
def limit (c : Nat) (T : Nat → Thread c) (hT : IsCoherent c T) : Thread c :=
  ⟨limitFamily c T, limit_compatible c T hT⟩

/-- Convergence: for every scale `n` and every `m ≥ n`, thread `T m` agrees with the limit
up to scale `n`.
AuthorityEffect: None. -/
theorem limit_converges (c : Nat) (T : Nat → Thread c) (hT : IsCoherent c T)
    (n m : Nat) (hnm : n ≤ m) : Agrees c (T m) (limit c T hT) n := by
  show (T m).val n = (limit c T hT).val n
  show (T m).val n = (T n).val n
  exact hT n m hnm

/-- Uniqueness: any thread that is an accumulation point of the coherent sequence
coincides with the constructed limit thread.
AuthorityEffect: None. -/
theorem limit_unique (c : Nat) (T : Nat → Thread c) (hT : IsCoherent c T)
    (L : Thread c) (hL : ∀ (n : Nat), ∃ m, n ≤ m ∧ Agrees c (T m) L n) :
    L = limit c T hT := by
  apply threads_eq_of_agrees_all
  intro n
  obtain ⟨m, hnm, hmL⟩ := hL n
  have hmL' := agrees_symm c hmL
  have hmlim := limit_converges c T hT n m hnm
  exact agrees_trans c hmL' hmlim

/-!
## 5. The process image: functionality and eventual periodicity
AuthorityEffect: None.
-/

/-- A sequence of naturals is functional when equal entries have equal successors.
This characterizes deterministic tapes produced by step execution.
AuthorityEffect: None. -/
def IsFunctionalSeq (s : Nat → Nat) : Prop :=
  ∀ (i j : Nat), s i = s j → s (i + 1) = s (j + 1)

/-- A thread is functional when its read sequence is functional.
AuthorityEffect: None. -/
def IsFunctionalThread (c : Nat) (t : Thread c) : Prop :=
  IsFunctionalSeq (fun i => (toSeq c t i).val)

/-- Any non-functional thread has an open ball around it containing no functional threads.
AuthorityEffect: None. -/
theorem nonfunctional_open_ball (c : Nat) (t : Thread c) (i j : Nat)
    (heq : (toSeq c t i).val = (toSeq c t j).val)
    (hne : (toSeq c t (i + 1)).val ≠ (toSeq c t (j + 1)).val) :
    ∀ (u : Thread c), Agrees c t u (max i j + 2) → ¬ IsFunctionalThread c u := by
  intro u hag hfunc
  have hbound_i : i + 1 < max i j + 2 := by
    have : i ≤ max i j := Nat.le_max_left i j
    omega
  have hbound_j : j + 1 < max i j + 2 := by
    have : j ≤ max i j := Nat.le_max_right i j
    omega
  have h_seq := (agrees_iff_toSeq c t u (max i j + 2)).mp hag
  have hui : (toSeq c u i).val = (toSeq c t i).val := by
    congr 1
    exact (h_seq i (by omega)).symm
  have huj : (toSeq c u j).val = (toSeq c t j).val := by
    congr 1
    exact (h_seq j (by omega)).symm
  have hui1 : (toSeq c u (i + 1)).val = (toSeq c t (i + 1)).val := by
    congr 1
    exact (h_seq (i + 1) hbound_i).symm
  have huj1 : (toSeq c u (j + 1)).val = (toSeq c t (j + 1)).val := by
    congr 1
    exact (h_seq (j + 1) hbound_j).symm
  have heq_u : (toSeq c u i).val = (toSeq c u j).val := by
    rw [hui, huj, heq]
  have hsucc_u := hfunc i j heq_u
  change (toSeq c u (i + 1)).val = (toSeq c u (j + 1)).val at hsucc_u
  rw [hui1, huj1] at hsucc_u
  exact hne hsucc_u

/-- The limit of a coherent sequence of functional threads is functional.
AuthorityEffect: None. -/
theorem functional_closed_limit (c : Nat) (T : Nat → Thread c) (hT : IsCoherent c T)
    (hfunc : ∀ m, IsFunctionalThread c (T m)) :
    IsFunctionalThread c (limit c T hT) := by
  intro i j heq
  change (toSeq c (limit c T hT) i).val = (toSeq c (limit c T hT) j).val at heq
  let N := max i j + 2
  have hN_i : i < N := by
    have : i ≤ max i j := Nat.le_max_left i j
    omega
  have hN_j : j < N := by
    have : j ≤ max i j := Nat.le_max_right i j
    omega
  have hN_i1 : i + 1 < N := by
    have : i ≤ max i j := Nat.le_max_left i j
    omega
  have hN_j1 : j + 1 < N := by
    have : j ≤ max i j := Nat.le_max_right i j
    omega
  have hconv := limit_converges c T hT N N (Nat.le_refl N)
  have hseq := (agrees_iff_toSeq c (T N) (limit c T hT) N).mp hconv
  have hTi : (toSeq c (T N) i).val = (toSeq c (limit c T hT) i).val := by
    congr 1
    exact hseq i hN_i
  have hTj : (toSeq c (T N) j).val = (toSeq c (limit c T hT) j).val := by
    congr 1
    exact hseq j hN_j
  have hTi1 : (toSeq c (T N) (i + 1)).val = (toSeq c (limit c T hT) (i + 1)).val := by
    congr 1
    exact hseq (i + 1) hN_i1
  have hTj1 : (toSeq c (T N) (j + 1)).val = (toSeq c (limit c T hT) (j + 1)).val := by
    congr 1
    exact hseq (j + 1) hN_j1
  have heq_T : (toSeq c (T N) i).val = (toSeq c (T N) j).val := by
    rw [hTi, hTj, heq]
  have hsucc_T := hfunc N i j heq_T
  change (toSeq c (T N) (i + 1)).val = (toSeq c (T N) (j + 1)).val at hsucc_T
  change (toSeq c (limit c T hT) (i + 1)).val = (toSeq c (limit c T hT) (j + 1)).val
  rw [← hTi1, ← hTj1]
  exact hsucc_T

/-- A non-functional sequence over carrier `Fin 2`: prefix `[0, 1, 0, 0]` repeats 0
with different successors (1 then 0).
AuthorityEffect: None. -/
def nonfuncSeq2 : Nat → Fin 2
  | 0 => ⟨0, by decide⟩
  | 1 => ⟨1, by decide⟩
  | 2 => ⟨0, by decide⟩
  | _ => ⟨0, by decide⟩

/-- `nonfuncSeq2` is not functional.
AuthorityEffect: None. -/
theorem nonfuncSeq2_not_functional :
    ¬ IsFunctionalSeq (fun i => (nonfuncSeq2 i).val) := by
  intro h
  have heq : (nonfuncSeq2 0).val = (nonfuncSeq2 2).val := rfl
  have hsucc := h 0 2 heq
  revert hsucc
  decide

/-- The thread space over 2 symbols contains a non-functional thread.
AuthorityEffect: None. -/
theorem proper_subset_two :
    ∃ (t : Thread 2), ¬ IsFunctionalThread 2 t := by
  refine ⟨ofSeq 2 nonfuncSeq2, ?_⟩
  intro hf
  have heq : (toSeq 2 (ofSeq 2 nonfuncSeq2) 0).val = (toSeq 2 (ofSeq 2 nonfuncSeq2) 2).val := rfl
  have hsucc := hf 0 2 heq
  revert hsucc
  decide

/-- A non-functional sequence over carrier `Fin 3` realizing the prefix `[0, 1, 0, 2]`
documented in `research/coherent_process_limits/README.md`.
AuthorityEffect: None. -/
def nonfuncSeq3 : Nat → Fin 3
  | 0 => ⟨0, by decide⟩
  | 1 => ⟨1, by decide⟩
  | 2 => ⟨0, by decide⟩
  | 3 => ⟨2, by decide⟩
  | _ => ⟨0, by decide⟩

/-- The thread space over 3 symbols contains a non-functional thread.
AuthorityEffect: None. -/
theorem proper_subset_three :
    ∃ (t : Thread 3), ¬ IsFunctionalThread 3 t := by
  refine ⟨ofSeq 3 nonfuncSeq3, ?_⟩
  intro hf
  have heq : (toSeq 3 (ofSeq 3 nonfuncSeq3) 0).val = (toSeq 3 (ofSeq 3 nonfuncSeq3) 2).val := rfl
  have hsucc := hf 0 2 heq
  revert hsucc
  decide

/-- Every functional sequence on a carrier of size `c` is eventually periodic,
with preperiod and period together bounded by `c`.  This leverages the constructive
pigeonhole theorem in `Observe.pigeon`.
AuthorityEffect: None. -/
theorem functional_thread_is_eventually_periodic (c : Nat) (_hc : 0 < c)
    (t : Thread c) (hf : IsFunctionalThread c t) :
    ∃ (i k : Nat), 0 < k ∧ i + k ≤ c ∧
      ∀ (n : Nat), (toSeq c t (i + k + n)).val = (toSeq c t (i + n)).val := by
  let f := fun n => (toSeq c t n).val
  have hbound : ∀ i, i ≤ c → f i < c := fun i _ => (toSeq c t i).isLt
  obtain ⟨i, j, hij, hjc, heq⟩ := Observe.pigeon c f hbound
  refine ⟨i, j - i, by omega, by omega, ?_⟩
  intro n
  have hij_eq : i + (j - i) = j := by omega
  show f (i + (j - i) + n) = f (i + n)
  rw [hij_eq]
  induction n with
  | zero =>
      show f j = f i
      exact heq.symm
  | succ m ih =>
      show f (j + m + 1) = f (i + m + 1)
      have h1 : j + m + 1 = (j + m) + 1 := by omega
      have h2 : i + m + 1 = (i + m) + 1 := by omega
      rw [h1, h2]
      exact hf (j + m) (i + m) ih

/-- Sequence extension padding with a constant value beyond index `n`.
AuthorityEffect: None. -/
def padSeq (c : Nat) (s : Nat → Fin c) (n : Nat) (k : Nat) : Fin c :=
  if k < n then s k else s 0

/-- Arbitrary eventually periodic threads are dense in `Thread c`: any thread
can be approximated to arbitrary scale `n` by an eventually constant thread.
AuthorityEffect: None. -/
theorem eventually_periodic_dense (c : Nat) (t : Thread c) (n : Nat) :
    ∃ (u : Thread c), Agrees c t u n ∧
      ∃ (i k : Nat), 0 < k ∧ ∀ (m : Nat), (toSeq c u (i + k + m)).val = (toSeq c u (i + m)).val := by
  let seq := padSeq c (toSeq c t) n
  let u := ofSeq c seq
  refine ⟨u, ?_, n, 1, Nat.zero_lt_one, ?_⟩
  · rw [agrees_iff_toSeq]
    intro i hi
    show toSeq c t i = toSeq c u i
    have hu := toSeq_ofSeq c seq
    rw [hu]
    dsimp [seq, padSeq]
    rw [if_pos hi]
  · intro m
    have hu := toSeq_ofSeq c seq
    have hu1 := congrFun hu (n + 1 + m)
    have hu2 := congrFun hu (n + m)
    show (toSeq c u (n + 1 + m)).val = (toSeq c u (n + m)).val
    rw [hu1, hu2]
    dsimp [seq, padSeq]
    have h1 : ¬ (n + 1 + m < n) := by omega
    have h2 : ¬ (n + m < n) := by omega
    rw [if_neg h1, if_neg h2]

end Limits

#print axioms Limits.agrees_refl
#print axioms Limits.agrees_symm
#print axioms Limits.agrees_trans
#print axioms Limits.agrees_zero
#print axioms Limits.agrees_le
#print axioms Limits.agrees_min
#print axioms Limits.threads_eq_of_agrees_all
#print axioms Limits.agrees_iff_toSeq
#print axioms Limits.seqAgrees_iff
#print axioms Limits.threadAgrees_iff
#print axioms Limits.firstDiffBounded_none
#print axioms Limits.firstDiffBounded_some
#print axioms Limits.distLe_zero
#print axioms Limits.distLe_symm
#print axioms Limits.distLe_indiscernibles
#print axioms Limits.distLe_ultrametric
#print axioms Limits.distLe_trans
#print axioms Limits.ball_self
#print axioms Limits.ball_point_is_center
#print axioms Limits.balls_disjoint_or_coincide
#print axioms Limits.limit_compatible
#print axioms Limits.limit_converges
#print axioms Limits.limit_unique
#print axioms Limits.nonfunctional_open_ball
#print axioms Limits.functional_closed_limit
#print axioms Limits.nonfuncSeq2_not_functional
#print axioms Limits.proper_subset_two
#print axioms Limits.proper_subset_three
#print axioms Limits.functional_thread_is_eventually_periodic
#print axioms Limits.eventually_periodic_dense

