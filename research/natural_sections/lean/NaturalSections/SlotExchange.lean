import NaturalSections
import NaturalSections.WeightedLayer

/-!
# Slot exchange: characters of the two slot actions, and odd-pairing cancellation

The sealed `Derivation.PrimDiff` (inside this package's pinned closure)
carries the oriented two-slot primitive `D2`, its transpose `D2rev`,
the symmetrisation `S2 = Sym D2`, and irreflexivity for both.  This
module proves the rung pre-registered in `STATUS.md`:

1. Value assignments to the CYCLIC slot action's generator, taken in
   `Fin (k+1)` under addition, are all admissible: `k+1` iterated
   additions of any element return to zero (`repAdd_rot_zero`).  The
   SWAP generator of the full slot-permutation action instead
   constrains `c + c = 0`, and the count of admissible values depends
   on the value group: over `Fin k` it is `2` for even `k` and `1` for
   odd `k` (`swap_count_one` .. `swap_count_eight`, by `decide`).  The
   familiar "exactly two" is a fact about two-torsion in the chosen
   value group, not about the slot count.

2. An ODD integer weight family (`W b a = - W a b`, the weight-level
   mirror of `Transpose`) vanishes on the diagonal, has total zero on
   the two-point carrier, and is identically zero if it is also
   symmetric.  A family supported on an irreflexive relation vanishes
   on the diagonal for the support reason.  The canonical odd family
   built on the sealed `D2`/`D2rev` support is odd, so it cancels.

3. A declared pairing-plus-residual list sums to its residual, so a
   non-negative residual gives a non-negative total: cancellation
   carried out in algebra, before any summation policy is chosen
   (`sum_pairs_residual`, `sum_pairs_residual_nonneg`).  The refusal:
   DISCARDING partners is not cancelling them (`discard_is_not_cancel`).

AuthorityEffect: None.
-/

namespace NaturalSections
namespace SlotEx

/-- `m` iterated additions of `c` in `Fin (k+1)`. -/
def repAdd {k : Nat} : Nat → Fin (k + 1) → Fin (k + 1)
  | 0, _ => 0
  | m + 1, c => c + repAdd m c

/-- Reduction of a double remainder, self-contained on positivity. -/
theorem mod_idem (a n : Nat) (hn : 0 < n) : a % n % n = a % n :=
  Nat.mod_eq_of_lt (Nat.mod_lt a hn)

theorem repAdd_val {k : Nat} (m : Nat) (c : Fin (k + 1)) :
    (repAdd m c).val = m * c.val % (k + 1) := by
  induction m with
  | zero => simp [repAdd]
  | succ n ih =>
    show ((c + repAdd n c) : Fin (k + 1)).val = (n + 1) * c.val % (k + 1)
    rw [Fin.val_add, ih, Nat.succ_mul]
    rw [Nat.add_mod, mod_idem (n * c.val) (k + 1) (Nat.succ_pos k)]
    rw [← Nat.add_mod, Nat.add_comm (n * c.val) c.val]

/-- SX1: every value is admissible for the rotation generator -- the
`k+1`-fold iterate of any `c : Fin (k+1)` is zero. -/
theorem repAdd_rot_zero {k : Nat} (c : Fin (k + 1)) :
    repAdd (k + 1) c = 0 := by
  apply Fin.ext
  rw [repAdd_val, Fin.val_zero, Nat.mul_comm, Nat.mul_mod_left]

/-- SX2, `k = 1`: swap-admissible values in `Fin 1`. -/
theorem swap_count_one :
    (([0] : List (Fin 1)).filter fun c => c + c == 0).length = 1 := by
  decide

theorem swap_count_two :
    (([0, 1] : List (Fin 2)).filter fun c => c + c == 0).length = 2 := by
  decide

theorem swap_count_three :
    (([0, 1, 2] : List (Fin 3)).filter fun c => c + c == 0).length = 1 := by
  decide

theorem swap_count_four :
    (([0, 1, 2, 3] : List (Fin 4)).filter fun c => c + c == 0).length = 2 := by
  decide

theorem swap_count_five :
    (([0, 1, 2, 3, 4] : List (Fin 5)).filter fun c => c + c == 0).length = 1 := by
  decide

theorem swap_count_six :
    (([0, 1, 2, 3, 4, 5] : List (Fin 6)).filter fun c => c + c == 0).length = 2 := by
  decide

theorem swap_count_seven :
    (([0, 1, 2, 3, 4, 5, 6] : List (Fin 7)).filter fun c => c + c == 0).length = 1 := by
  decide

theorem swap_count_eight :
    (([0, 1, 2, 3, 4, 5, 6, 7] : List (Fin 8)).filter fun c => c + c == 0).length = 2 := by
  decide

/-- The weight-level mirror of the sealed `Transpose`. -/
def transposeW {α : Type} (W : α → α → Int) : α → α → Int :=
  fun a b => W b a

/-- The mirror of transpose involutivity, definitional. -/
theorem transposeW_transposeW {α : Type} (W : α → α → Int) :
    transposeW (transposeW W) = W := rfl

/-- Odd families: the weight-level mirror of orientation. -/
def OddW {α : Type} (W : α → α → Int) : Prop :=
  ∀ a b, W b a = - W a b

/-- Symmetric families: the weight-level mirror of `Sym`. -/
def SymW {α : Type} (W : α → α → Int) : Prop :=
  ∀ a b, W b a = W a b

/-- SX3: an odd family vanishes on the diagonal. -/
theorem oddW_diag_zero {α : Type} (W : α → α → Int) (h : OddW W) (a : α) :
    W a a = 0 := by
  have hh := h a a
  omega

/-- SX3: on the two-point carrier an odd family has total zero -- the
diagonal is forced to zero and the two off-diagonal entries cancel. -/
theorem odd_total_zero (W : Bool → Bool → Int) (h : OddW W) :
    W false false + W false true + W true false + W true true = 0 := by
  have h1 := h false true
  have h2 := oddW_diag_zero W h false
  have h3 := oddW_diag_zero W h true
  omega

/-- SX3: a family both symmetric and odd is identically zero -- the two
characters meet only in the trivial family. -/
theorem sym_odd_zero {α : Type} (W : α → α → Int)
    (hsym : SymW W) (hodd : OddW W) (a b : α) : W a b = 0 := by
  have h1 := hsym a b
  have h2 := hodd a b
  omega

/-- Support of a weight family on a declared relation. -/
def SupportedOn {α : Type} (W : α → α → Int) (r : α → α → Prop) : Prop :=
  ∀ a b, ¬ r a b → W a b = 0

/-- SX3: support on an irreflexive relation forces diagonal zero -- the
support form of the same refusal. -/
theorem irrefl_support_diag_zero {α : Type} (W : α → α → Int)
    (r : α → α → Prop) (hs : SupportedOn W r) (hi : PrimDiff.Irrefl r)
    (a : α) : W a a = 0 :=
  hs a a (hi a)

/-- The canonical family on the sealed oriented support: weight `x` on
the `D2` witness, `-x` on its transpose, zero elsewhere. -/
def d2Fam (x : Int) : Bool → Bool → Int := fun a b =>
  if a = false ∧ b = true then x
  else if a = true ∧ b = false then - x
  else 0

/-- SX4: the canonical family is odd. -/
theorem d2Fam_odd (x : Int) : OddW (d2Fam x) := by
  intro a b
  cases a <;> cases b <;> simp [d2Fam]

/-- SX4: the canonical family is supported on the sealed oriented
witness and its transpose. -/
theorem d2Fam_supported (x : Int) :
    SupportedOn (d2Fam x) fun a b => PrimDiff.D2 a b ∨ PrimDiff.D2rev a b := by
  intro a b hn
  cases a <;> cases b
  · simp [d2Fam]
  · exact absurd (Or.inl ⟨rfl, rfl⟩) hn
  · exact absurd (Or.inr ⟨rfl, rfl⟩) hn
  · simp [d2Fam]

/-- SX4: the canonical family's total is zero, by oddness. -/
theorem d2Fam_total_zero (x : Int) :
    d2Fam x false false + d2Fam x false true
      + d2Fam x true false + d2Fam x true true = 0 :=
  odd_total_zero (d2Fam x) (d2Fam_odd x)

/-- One cancelling pair at the head of a sum. -/
theorem sumList_pair_cancel (x : Int) (rest : List Int) :
    sumList (x :: - x :: rest) = sumList rest := by
  show x + (- x + sumList rest) = sumList rest
  omega

/-- A sum of non-negative entries is non-negative. -/
theorem sumList_nonneg (l : List Int) (h : ∀ x, x ∈ l → 0 ≤ x) :
    0 ≤ sumList l := by
  induction l with
  | nil => exact Int.le_refl 0
  | cons y ys ih =>
    have hy := h y List.mem_cons_self
    have hys := ih fun x hx => h x (List.mem_cons_of_mem y hx)
    show 0 ≤ y + sumList ys
    omega

/-- SX5: a declared pairing-plus-residual list sums to its residual --
every pair cancels in algebra, before any summation policy. -/
theorem sum_pairs_residual (pairs res : List Int) :
    sumList ((pairs.flatMap fun x => [x, - x]) ++ res) = sumList res := by
  induction pairs with
  | nil => rfl
  | cons p ps ih =>
    show sumList (([p, - p] ++ ps.flatMap fun x => [x, - x]) ++ res)
      = sumList res
    rw [List.append_assoc]
    show sumList (p :: - p :: ((ps.flatMap fun x => [x, - x]) ++ res))
      = sumList res
    rw [sumList_pair_cancel]
    exact ih

/-- SX5: with a non-negative residual, the paired total is
non-negative. -/
theorem sum_pairs_residual_nonneg (pairs res : List Int)
    (h : ∀ x, x ∈ res → 0 ≤ x) :
    0 ≤ sumList ((pairs.flatMap fun x => [x, - x]) ++ res) := by
  rw [sum_pairs_residual]
  exact sumList_nonneg res h

/-- SX6: discarding partners is not cancelling them -- the full list
totals zero, the discarded-partner list totals four, and conflating the
two is the refused move. -/
theorem discard_is_not_cancel :
    sumList ([3, -3, 1, -1] : List Int) = 0
      ∧ sumList ([3, 1] : List Int) = 4 := by
  exact ⟨rfl, rfl⟩

/-- SX7: a weight-reversing involution fixes only zero-weight points --
the no-fixed-points hypothesis is free, not expensive.  Adopted from an
independent review of this rung; the price sits in SX8 instead. -/
theorem flip_fixed_zero {γ : Type} (σ : γ → γ) (W : γ → Int)
    (hodd : ∀ c, W (σ c) = - W c) (c : γ) (h : σ c = c) : W c = 0 := by
  have hc := hodd c
  rw [h] at hc
  omega

/-- SX8: the residual hypothesis of SX5 is necessary -- a mixed-sign
complement makes the total negative, so single-signedness of the
leftover is the load-bearing premise of the whole route. -/
theorem mixed_residual_negative :
    sumList ([1, -2] : List Int) = -1 := rfl

end SlotEx
end NaturalSections
