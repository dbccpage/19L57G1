/-!
# DepthLadder: General Multi-Depth Retained-Record Enablement Ladder

This module generalizes the depth-one (`Record.lean`) and depth-two (`Depth.lean`)
retained-record enablement machines to an arbitrary depth-$k$ ladder.

## Mathematical Content
1. `windowsOf (k : Nat) : List Nat → List (List Nat)` extracts all contiguous
   length-$k$ sublists of a tape.
2. `functional (k : Nat) (tape : List Nat) : Prop` asserts that any two windows
   of length $k + 1$ that agree on their first $k$ entries (the antecedent)
   must be identical (the successor is uniquely determined).
3. `ladder_monotonic` proves the general monotonicity theorem:
   `functional k tape → functional (k + 1) tape` for all `k` and `tape`.

Axioms audited: strictly contained in `{propext, Quot.sound}` (zero Classical.choice).
AuthorityEffect: None.
-/

namespace DepthLadder

/-- All contiguous sublists of length `k` in order. -/
def windowsOf (k : Nat) : List Nat → List (List Nat)
  | [] => []
  | x :: xs =>
    if (x :: xs).length < k then []
    else (x :: xs).take k :: windowsOf k xs

/-- A tape is functional in `k` entries when any two windows of length `k + 1`
that agree on their first `k` entries are identical. -/
def functional (k : Nat) (tape : List Nat) : Prop :=
  ∀ w1 w2, w1 ∈ windowsOf (k + 1) tape → w2 ∈ windowsOf (k + 1) tape →
    w1.take k = w2.take k → w1 = w2

theorem windowsOf_nil (k : Nat) : windowsOf k [] = [] := by
  rfl

theorem windowsOf_cons (k : Nat) (x : Nat) (xs : List Nat) :
    windowsOf k (x :: xs) =
      if (x :: xs).length < k then []
      else (x :: xs).take k :: windowsOf k xs := by
  rfl

theorem windowsOf_of_ge {k : Nat} {x : Nat} {xs : List Nat} (h : (x :: xs).length ≥ k) :
    windowsOf k (x :: xs) = (x :: xs).take k :: windowsOf k xs := by
  have hnot : ¬(x :: xs).length < k := by omega
  rw [windowsOf_cons, if_neg hnot]

/-- Every window of length `k` produced by `windowsOf k` has length `k`. -/
theorem length_of_mem_windowsOf {k : Nat} {tape : List Nat} {w : List Nat}
    (hw : w ∈ windowsOf k tape) : w.length = k := by
  induction tape with
  | nil =>
    rw [windowsOf_nil] at hw
    cases hw
  | cons x xs ih =>
    rw [windowsOf_cons] at hw
    split at hw
    · cases hw
    · cases hw with
      | head =>
        rw [List.length_take]
        omega
      | tail _ htail =>
        exact ih htail

/-- Taking the prefix of length `k + 1` of a window of length `k + 2`
yields a window of length `k + 1`. -/
theorem take_mem_windowsOf (k : Nat) {tape : List Nat} {w : List Nat}
    (hw : w ∈ windowsOf (k + 2) tape) : w.take (k + 1) ∈ windowsOf (k + 1) tape := by
  induction tape with
  | nil =>
    rw [windowsOf_nil] at hw
    cases hw
  | cons x xs ih =>
    rw [windowsOf_cons] at hw
    split at hw
    · cases hw
    · rename_i hlen
      have hlen1 : (x :: xs).length ≥ k + 1 := by omega
      rw [windowsOf_of_ge hlen1]
      cases hw with
      | head =>
        have htake_take : List.take (k + 1) (List.take (k + 2) (x :: xs)) = List.take (k + 1) (x :: xs) := by
          rw [List.take_take]
          have : min (k + 1) (k + 2) = k + 1 := by omega
          rw [this]
        rw [htake_take]
        apply List.Mem.head
      | tail _ htail =>
        apply List.Mem.tail
        exact ih htail

/-- Taking the tail of a window of length `k + 2`
yields a window of length `k + 1`. -/
theorem tail_mem_windowsOf (k : Nat) {tape : List Nat} {w : List Nat}
    (hw : w ∈ windowsOf (k + 2) tape) : w.tail ∈ windowsOf (k + 1) tape := by
  induction tape with
  | nil =>
    rw [windowsOf_nil] at hw
    cases hw
  | cons x xs ih =>
    rw [windowsOf_cons] at hw
    split at hw
    · cases hw
    · rename_i hlen
      have hlen1 : (x :: xs).length ≥ k + 1 := by omega
      rw [windowsOf_of_ge hlen1]
      cases hw with
      | head =>
        apply List.Mem.tail
        cases xs with
        | nil =>
          have hlen_nil : (x :: []).length = 1 := rfl
          rw [hlen_nil] at hlen
          have hcontra : k + 2 ≤ 1 := by omega
          cases hcontra with
          | step h1 => cases h1
        | cons y ys =>
          have hys_len : (y :: ys).length ≥ k + 1 := by
            have : (x :: y :: ys).length = (y :: ys).length + 1 := rfl
            omega
          rw [windowsOf_of_ge hys_len]
          have htake_tail : (List.take (k + 2) (x :: y :: ys)).tail = List.take (k + 1) (y :: ys) := by
            rfl
          rw [htake_tail]
          apply List.Mem.head
      | tail _ htail =>
        apply List.Mem.tail
        exact ih htail

/-- Suffix take identity: for any list, taking `k` elements of its tail
equals the tail of taking `k + 1` elements. -/
theorem take_tail_eq_tail_take (k : Nat) (w : List Nat) :
    (w.tail).take k = (w.take (k + 1)).tail := by
  cases w with
  | nil => simp
  | cons x xs => simp only [List.tail_cons, List.take_succ_cons]

/-- Head agreement from take agreement. -/
theorem head_eq_of_take_succ {k : Nat} {w1 w2 : List Nat}
    (heq : w1.take (k + 1) = w2.take (k + 1)) :
    w1.take 1 = w2.take 1 := by
  have h := congrArg (List.take 1) heq
  rw [List.take_take, List.take_take] at h
  exact h

/-- **The General Monotonicity Theorem**:
A tape functional in `k` entries is unconditionally functional in `k + 1` entries. -/
theorem ladder_monotonic (k : Nat) (tape : List Nat)
    (hfunc : functional k tape) : functional (k + 1) tape := by
  intro w1 w2 hw1 hw2 htake
  -- Tails are windows of length k + 1
  have htail1 : w1.tail ∈ windowsOf (k + 1) tape := tail_mem_windowsOf k hw1
  have htail2 : w2.tail ∈ windowsOf (k + 1) tape := tail_mem_windowsOf k hw2

  -- Tails agree on their first k elements
  have htail_take : (w1.tail).take k = (w2.tail).take k := by
    rw [take_tail_eq_tail_take, take_tail_eq_tail_take]
    rw [htake]

  -- By functionality at level k, the tails are equal
  have htail_eq : w1.tail = w2.tail := hfunc (w1.tail) (w2.tail) htail1 htail2 htail_take

  -- Heads are equal because w1.take (k + 1) = w2.take (k + 1)
  have htake1 : w1.take 1 = w2.take 1 := head_eq_of_take_succ htake

  -- Therefore w1 = w2
  cases w1 with
  | nil =>
    have hw1_len := length_of_mem_windowsOf hw1
    have hnil_len : ([] : List Nat).length = 0 := rfl
    rw [hnil_len] at hw1_len
    have hcontra : k + 2 ≤ 0 := by omega
    cases hcontra
  | cons x1 xs1 =>
    cases w2 with
    | nil =>
      have hw2_len := length_of_mem_windowsOf hw2
      have hnil_len : ([] : List Nat).length = 0 := rfl
      rw [hnil_len] at hw2_len
      have hcontra : k + 2 ≤ 0 := by omega
      cases hcontra
    | cons x2 xs2 =>
      have hx : x1 = x2 := by
        cases htake1
        rfl
      have hxs : xs1 = xs2 := htail_eq
      rw [hx, hxs]

#print axioms length_of_mem_windowsOf
#print axioms take_mem_windowsOf
#print axioms tail_mem_windowsOf
#print axioms take_tail_eq_tail_take
#print axioms head_eq_of_take_succ
#print axioms ladder_monotonic

end DepthLadder
