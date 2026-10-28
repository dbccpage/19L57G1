import Derivation.CapacityBound

/-!
# Theorem I(d) — the local capacity threshold is exact

AuthorityEffect: None.  Outside the seal.

Genesis `CapacityBound.capacity_bound` proves: a `d`-local view of a
`k`-colouring collides on the interior of any carrier of size at least
`k ^ (2d+1) + 2d + 2`, and states "No threshold minimality or tightness is
claimed".  This module supplies the missing half at tested parameters: one
below the threshold, a *window-distinct colouring* — every window of
`2d+1` consecutive colours distinct — carries a `d`-local view with no
interior collision, so the Genesis threshold is the exact point at which a
collision becomes forced.

* DEFINITION: `TightAt k d`.
* THEOREMS (by `decide` over the finite interior): `tight_1_0`,
  `tight_2_0`, `tight_3_0`, `tight_2_1`, `tight_3_1`, `tight_2_2`.
* THEOREM: `exact_threshold` — for any `(k, d)` with `TightAt k d`, the
  collision is forced at `k ^ (2d+1) + 2d + 2` and not at one less.
* NOT CLAIMED IN LEAN: `TightAt k d` for every `k ≥ 1`, `d`.  The Python
  model constructs window-distinct colourings for every `(k, d)` it is
  asked for and checks them; that general statement is *computed* at the
  tested parameters and otherwise *open* here.

The lists below were produced by the model's construction (a closed walk
through every word of length `2d+1` once) and are checked here by `decide`,
independently of how they were found.
-/

namespace ResearchTwoTheorems
namespace Capacity

open CapacityBound

/-- A colouring read off a list; positions beyond the list are coloured 0. -/
def colourOf (l : List Nat) : Nat → Nat := fun i => l.getD i 0

theorem colourOf_lt {l : List Nat} {k : Nat} (hk : 0 < k)
    (hl : ∀ y ∈ l, y < k) (x : Nat) : colourOf l x < k := by
  unfold colourOf
  rw [List.getD_eq_getElem?_getD]
  cases h : l[x]? with
  | none => exact hk
  | some y => exact hl y (List.mem_of_getElem? h)

/-- The `d`-local view that reads its window as a `k`-ary numeral. -/
def codeView (k : Nat) (colour : Nat → Nat) (d : Nat) : Nat → Nat :=
  fun i => encode k (colourBall colour i d)

theorem codeView_local (k : Nat) (colour : Nat → Nat) (d : Nat) :
    ViewLocal (codeView k colour d) colour d :=
  ⟨encode k, fun _ => rfl⟩

/-- No collision among the interior positions of a carrier of size `n`
(the positions Genesis's bound speaks about). -/
def InjInterior (v : Nat → Nat) (d n : Nat) : Prop :=
  ∀ i j, d < i → i + d < n → d < j → j + d < n → v i = v j → i = j

/-- The same, with the quantifiers bounded so that `decide` can run. -/
abbrev InjInteriorB (v : Nat → Nat) (d n : Nat) : Prop :=
  ∀ i ∈ List.range n, ∀ j ∈ List.range n,
    d < i → i + d < n → d < j → j + d < n → v i = v j → i = j

theorem injInterior_of_bounded {v : Nat → Nat} {d n : Nat}
    (h : InjInteriorB v d n) : InjInterior v d n :=
  fun i j hi hin hj hjn he =>
    h i (List.mem_range.mpr (Nat.lt_of_le_of_lt (Nat.le_add_right i d) hin))
      j (List.mem_range.mpr (Nat.lt_of_le_of_lt (Nat.le_add_right j d) hjn))
      hi hin hj hjn he

/-- Tightness of the Genesis capacity bound at `(k, d)`: on a carrier of
size `k ^ (2d+1) + 2d + 1`, one below the threshold, some `k`-colouring
carries a `d`-local view with no interior collision. -/
def TightAt (k d : Nat) : Prop :=
  ∃ colour : Nat → Nat, (∀ x, colour x < k) ∧
    ∃ v : Nat → Nat, ViewLocal v colour d ∧
      InjInterior v d (k ^ (2 * d + 1) + 2 * d + 1)

theorem tightAt_of_list (k d : Nat) (l : List Nat) (hk : 0 < k)
    (hl : ∀ y ∈ l, y < k)
    (h : InjInteriorB (codeView k (colourOf l) d) d
      (k ^ (2 * d + 1) + 2 * d + 1)) : TightAt k d :=
  ⟨colourOf l, colourOf_lt hk hl, codeView k (colourOf l) d,
    codeView_local k (colourOf l) d, injInterior_of_bounded h⟩

/-! ## Window-distinct colourings at the exact threshold -/

def list_1_0 : List Nat := [0, 0]
def list_2_0 : List Nat := [0, 0, 1]
def list_3_0 : List Nat := [0, 0, 1, 2]
def list_2_1 : List Nat := [0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1]
def list_3_1 : List Nat :=
  [0, 0, 1, 0, 0, 2, 0, 1, 1, 0, 1, 2, 0, 2, 1, 0, 2, 2, 1, 1, 1, 2, 1, 2, 2,
   2, 0, 0, 0, 1]
def list_2_2 : List Nat :=
  [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1,
   1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0]

theorem tight_1_0 : TightAt 1 0 :=
  tightAt_of_list 1 0 list_1_0 (by decide) (by decide) (by decide)
theorem tight_2_0 : TightAt 2 0 :=
  tightAt_of_list 2 0 list_2_0 (by decide) (by decide) (by decide)
theorem tight_3_0 : TightAt 3 0 :=
  tightAt_of_list 3 0 list_3_0 (by decide) (by decide) (by decide)
theorem tight_2_1 : TightAt 2 1 :=
  tightAt_of_list 2 1 list_2_1 (by decide) (by decide) (by decide)
theorem tight_3_1 : TightAt 3 1 :=
  tightAt_of_list 3 1 list_3_1 (by decide) (by decide) (by decide)
theorem tight_2_2 : TightAt 2 2 :=
  tightAt_of_list 2 2 list_2_2 (by decide) (by decide) (by decide)

/-! ## The threshold is exact -/

/-- A collision on the interior of a carrier of size `n`, as Genesis
states it. -/
def Collides (v : Nat → Nat) (d n : Nat) : Prop :=
  ∃ i j, i ≠ j ∧ d < i ∧ i + d < n ∧ d < j ∧ j + d < n ∧ v i = v j

theorem not_collides_of_injInterior {v : Nat → Nat} {d n : Nat}
    (h : InjInterior v d n) : ¬ Collides v d n := by
  rintro ⟨i, j, hne, hi, hin, hj, hjn, he⟩
  exact hne (h i j hi hin hj hjn he)

/-- **Exact threshold.**  Wherever tightness holds, `k ^ (2d+1) + 2d + 2`
is the least carrier size forcing an interior collision of every
`d`-local view of every `k`-colouring: at that size every such view
collides (Genesis `capacity_bound`), at one less some does not. -/
theorem exact_threshold (k d : Nat) (ht : TightAt k d) :
    (∀ colour v : Nat → Nat, (∀ x, colour x < k) → ViewLocal v colour d →
      Collides v d (k ^ (2 * d + 1) + 2 * d + 2)) ∧
    (∃ colour v : Nat → Nat, (∀ x, colour x < k) ∧ ViewLocal v colour d ∧
      ¬ Collides v d (k ^ (2 * d + 1) + 2 * d + 1)) := by
  refine ⟨fun colour v hk hloc => ?_, ?_⟩
  · exact capacity_bound colour v k d _ hk hloc (Nat.le_refl _)
  · obtain ⟨colour, hk, v, hloc, hinj⟩ := ht
    exact ⟨colour, v, hk, hloc, not_collides_of_injInterior hinj⟩

end Capacity
end ResearchTwoTheorems
