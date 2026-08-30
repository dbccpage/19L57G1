import NaturalSections
import NaturalSections.HopFixture

/-!
# The weighted layer: amplitudes on arrows, sums over declared closed walks

Every theorem below this file is about group elements.  This file is
where sums enter, and it enters as a layer OVER `HFamily`: nothing in
`Step`, `Walk`, `Forest` or the iff theorems is touched; the layer uses
`Walk.transport_of_natural` and nothing else from them.

`Weighting D R` assigns each declared arrow an amplitude and a reverse
amplitude in `R`; `Walk.weight` multiplies them along a walk; `total`
sums the weights of a DECLARED finite list of closed walks at a base;
`twisted` sums the same list read in a local convention `p` -- a walk
contributes its weight when its holonomy fixes `p` and `0` otherwise.

What `R` must be: a type with `Mul` and `One` for products and `Add`
and `Zero` for sums.  No ring law is assumed anywhere in this file;
that is a finding, not an omission (see `STATUS.md`).

Results: a natural section collapses the convention (`twisted_of_natural`);
the converse fails over the integers with every amplitude nonzero
(`sum_blind_to_obstruction`); counting in the natural numbers detects
every moving walk (`count_eq_length_iff`, `count_lt_of_mover`); and a
ring-weighted sum can take every value on the obstructed square and the
unobstructed chain alike (`every_value_square`, `every_value_chain`).
AuthorityEffect: None.
-/

namespace NaturalSections

open DiffInterface ContactKernel PresentationNaturality

/-- Amplitudes on the declared arrows: forward and backward. -/
structure Weighting (D : HFamily) (R : Type) where
  amp : ∀ {a b : D.Obj}, D.Hom a b → R
  ramp : ∀ {a b : D.Obj}, D.Hom a b → R

variable {D : HFamily} {R : Type}

def Step.weight [Mul R] [One R] (W : Weighting D R) :
    {a b : D.Obj} → Step D a b → R
  | _, _, .fwd h => W.amp h
  | _, _, .bwd h => W.ramp h

/-- The product of the step amplitudes along a walk; `1` on the empty walk. -/
def Walk.weight [Mul R] [One R] (W : Weighting D R) :
    {a b : D.Obj} → Walk D a b → R
  | _, _, .nil => 1
  | _, _, .cons s w => s.weight W * w.weight W

def sumList [Add R] [Zero R] : List R → R
  | [] => 0
  | x :: xs => x + sumList xs

/-- The plain weighted sum over a declared list of closed walks. -/
def total [Mul R] [One R] [Add R] [Zero R] (W : Weighting D R) {r : D.Obj}
    (ws : List (Walk D r r)) : R :=
  sumList (ws.map fun w => w.weight W)

/-- The same sum read in the local convention `p`: a walk counts when its
holonomy fixes `p`.  Deciding that needs decidable equality on the fibre,
supplied explicitly. -/
def twisted [Mul R] [One R] [Add R] [Zero R] (W : Weighting D R) {r : D.Obj}
    (dec : DecidableEq (NonZeroPair (D.obs r)))
    (ws : List (Walk D r r)) (p : NonZeroPair (D.obs r)) : R :=
  sumList (ws.map fun w => @ite R (w.transport p = p) (dec _ _) (w.weight W) 0)

/-! ## A1. A natural section collapses the convention -/

theorem sumList_map_congr [Add R] [Zero R] {α : Type} (f g : α → R) :
    ∀ (xs : List α), (∀ x, x ∈ xs → f x = g x) →
      sumList (xs.map f) = sumList (xs.map g)
  | [], _ => rfl
  | x :: xs, h => by
    show f x + sumList (xs.map f) = g x + sumList (xs.map g)
    rw [h x (List.mem_cons_self), sumList_map_congr f g xs
      (fun y hy => h y (List.mem_cons_of_mem x hy))]

/-- **A1.**  If `s` is a natural section, the sum read in the convention
`s r` is the plain sum, for every weighting, every `R`, every list. -/
theorem twisted_of_natural [Mul R] [One R] [Add R] [Zero R] (W : Weighting D R)
    {r : D.Obj} (dec : DecidableEq (NonZeroPair (D.obs r)))
    (ws : List (Walk D r r)) {s : HSec D} (hs : HIsNatural D s) :
    twisted W dec ws (s r) = total W ws := by
  unfold twisted total
  apply sumList_map_congr
  intro w _
  exact if_pos (Walk.transport_of_natural hs w)

/-! ## B1. Counting in the natural numbers detects every moving walk -/

/-- Unit amplitudes. -/
def unit (D : HFamily) : Weighting D Nat := ⟨fun _ => 1, fun _ => 1⟩

theorem unit_weight : ∀ {a b : D.Obj} (w : Walk D a b), w.weight (unit D) = 1
  | _, _, .nil => rfl
  | _, _, .cons s w => by
    show s.weight (unit D) * w.weight (unit D) = 1
    rw [unit_weight w]
    cases s <;> rfl

theorem total_unit {r : D.Obj} (ws : List (Walk D r r)) :
    total (unit D) ws = ws.length := by
  induction ws with
  | nil => rfl
  | cons w ws ih =>
    show w.weight (unit D) + total (unit D) ws = ws.length + 1
    rw [unit_weight, ih, Nat.add_comm]

/-- The count of walks in `ws` fixing `p` is at most the length, with
equality exactly when every walk fixes `p`. -/
theorem count_le_length {r : D.Obj} (dec : DecidableEq (NonZeroPair (D.obs r)))
    (ws : List (Walk D r r)) (p : NonZeroPair (D.obs r)) :
    twisted (unit D) dec ws p ≤ ws.length := by
  induction ws with
  | nil => exact Nat.le_refl 0
  | cons w ws ih =>
    show (@ite Nat (w.transport p = p) (dec _ _) (w.weight (unit D)) 0)
        + twisted (unit D) dec ws p ≤ ws.length + 1
    rw [unit_weight]
    split <;> omega

theorem count_eq_length_iff {r : D.Obj} (dec : DecidableEq (NonZeroPair (D.obs r)))
    (ws : List (Walk D r r)) (p : NonZeroPair (D.obs r)) :
    twisted (unit D) dec ws p = total (unit D) ws ↔ ∀ w, w ∈ ws → w.transport p = p := by
  rw [total_unit]
  induction ws with
  | nil => exact ⟨fun _ _ h => (nomatch h), fun _ => rfl⟩
  | cons w ws ih =>
    show (@ite Nat (w.transport p = p) (dec _ _) (w.weight (unit D)) 0)
        + twisted (unit D) dec ws p = ws.length + 1 ↔ _
    rw [unit_weight]
    have hle := count_le_length dec ws p
    constructor
    · intro h
      have hfix : w.transport p = p := by
        cases dec (w.transport p) p with
        | isTrue hf => exact hf
        | isFalse hne =>
          rw [if_neg hne] at h
          omega
      intro u hu
      rcases List.mem_cons.mp hu with rfl | hu'
      · exact hfix
      · rw [if_pos hfix] at h
        exact (ih.mp (by omega)) u hu'
    · intro h
      rw [if_pos (h w List.mem_cons_self), ih.mpr (fun u hu => h u (List.mem_cons_of_mem w hu))]
      omega

/-- **B1.**  A single moving walk in the list makes the count strictly
smaller than the length: in the natural numbers the obstruction is
visible in the value. -/
theorem count_lt_of_mover {r : D.Obj} (dec : DecidableEq (NonZeroPair (D.obs r)))
    (ws : List (Walk D r r)) (p : NonZeroPair (D.obs r))
    {w : Walk D r r} (hw : w ∈ ws) (hmove : w.transport p ≠ p) :
    twisted (unit D) dec ws p < total (unit D) ws := by
  have hne : twisted (unit D) dec ws p ≠ total (unit D) ws :=
    fun h => hmove ((count_eq_length_iff dec ws p).mp h w hw)
  have hle := count_le_length dec ws p
  rw [total_unit]
  rw [total_unit] at hne
  omega

/-! ## A3 and B2 on the two-label square (no natural section) -/

namespace Sq

open Hop

abbrev F := Hop.squareFamily

def dec : DecidableEq (NonZeroPair (F.obs .c01)) :=
  inferInstanceAs (DecidableEq (NonZeroPair boolEqObs))

/-- `{0,1} -> {1,2}`: the particle at `0` hops to `2`, above `1`: a flip. -/
def h0112 : F.Hom .c01 .c12 := ⟨by decide⟩
def h0103 : F.Hom .c01 .c03 := ⟨by decide⟩

/-- Backtrack across `{0,1} -> {1,2}` and straight back: holonomy the identity. -/
def backtrack : Walk F .c01 .c01 := .cons (.fwd h0112) (.cons (.bwd h0112) .nil)

theorem backtrack_fixes (p : NonZeroPair (F.obs .c01)) : backtrack.transport p = p :=
  Step.inv_transport (.fwd h0112) p

/-- Backtrack, then the exchange: holonomy the swap, like `sqWalk`. -/
def exchange2 : Walk F .c01 .c01 := backtrack.append sqWalk

/-- Amplitude `-1` on the two flipping arrows between `{0,1}` and `{1,2}`,
`1` elsewhere, reverse amplitudes `1`.  Every amplitude is nonzero.  A
first version put `-1` on `{0,1} -> {1,2}` only, which the exchange walk
does not traverse; `decide` refuted the claimed weight and the weighting
was corrected -- recorded in `STATUS.md`. -/
def signW : Weighting F Int where
  amp {a b} _ :=
    match (a : Hop.Pair4), (b : Hop.Pair4) with
    | .c01, .c12 => -1
    | .c12, .c01 => -1
    | _, _ => 1
  ramp _ := 1

def ws3 : List (Walk F .c01 .c01) := [.nil, sqWalk, exchange2]

theorem weights_ws3 :
    (Walk.nil : Walk F .c01 .c01).weight signW = 1 ∧
      sqWalk.weight signW = -1 ∧ exchange2.weight signW = 1 := by
  refine ⟨rfl, ?_, ?_⟩ <;> decide

/-- **A3.**  The square has no natural section, yet with these nonzero
integer amplitudes the twisted sum equals the plain sum at the pair
`(false, true)` and at `(true, false)`: the value does not see the
obstruction. -/
theorem sum_blind_to_obstruction :
    (¬ ∃ s : HSec F, HIsNatural F s) ∧
      twisted signW dec ws3 boolEqPair = total signW ws3 ∧
      twisted signW dec ws3 ⟨(true, false), boolEqObs_nonzero_tf⟩ = total signW ws3 := by
  refine ⟨square_no_natural_section, ?_, ?_⟩ <;> decide

/-- **B2 on the square.**  Every integer is the twisted sum of some
weighting, on this obstructed family: the class constrains nothing
about the value. -/
theorem every_value_square (v : Int) :
    ∃ W : Weighting F Int, twisted W dec [backtrack] boolEqPair = v ∧
      total W [backtrack] = v := by
  refine ⟨⟨fun _ => v, fun _ => 1⟩, ?_, ?_⟩
  · show @ite Int (backtrack.transport boolEqPair = boolEqPair) (dec _ _)
        (v * (1 * 1)) 0 + 0 = v
    rw [if_pos (backtrack_fixes boolEqPair), Int.mul_one, Int.mul_one, Int.add_zero]
  · show v * (1 * 1) + 0 = v
    rw [Int.mul_one, Int.mul_one, Int.add_zero]

end Sq

/-! ## B2 on the chain (a natural section exists): the same statement -/

namespace Ch

open Hop

abbrev F := Hop.chainFamily

def dec : DecidableEq (NonZeroPair (F.obs .c01)) :=
  inferInstanceAs (DecidableEq (NonZeroPair boolEqObs))

def h0102 : F.Hom .c01 .c02 := ⟨by decide⟩

def backtrack : Walk F .c01 .c01 := .cons (.fwd h0102) (.cons (.bwd h0102) .nil)

theorem backtrack_fixes (p : NonZeroPair (F.obs .c01)) : backtrack.transport p = p :=
  Step.inv_transport (.fwd h0102) p

/-- **B2 on the chain.**  Every integer is the twisted sum of some weighting
here too; the presence of a section (`chain_has_natural_section`) is
equally invisible in the value. -/
theorem every_value_chain (v : Int) :
    ∃ W : Weighting F Int, twisted W dec [backtrack] boolEqPair = v ∧
      total W [backtrack] = v := by
  refine ⟨⟨fun _ => v, fun _ => 1⟩, ?_, ?_⟩
  · show @ite Int (backtrack.transport boolEqPair = boolEqPair) (dec _ _)
        (v * (1 * 1)) 0 + 0 = v
    rw [if_pos (backtrack_fixes boolEqPair), Int.mul_one, Int.mul_one, Int.add_zero]
  · show v * (1 * 1) + 0 = v
    rw [Int.mul_one, Int.mul_one, Int.add_zero]

end Ch

/-- **The value is silent about the class.**  On the obstructed square and
the unobstructed chain, the twisted sum ranges over every integer. -/
theorem value_silent_about_class (v : Int) :
    (∃ W : Weighting Sq.F Int, twisted W Sq.dec [Sq.backtrack] boolEqPair = v) ∧
      ∃ W : Weighting Ch.F Int, twisted W Ch.dec [Ch.backtrack] boolEqPair = v :=
  -- `Exists.elim`, not `Exists.choose`: the goal is a `Prop`, and a first
  -- version that used `choose` was refused by the axiom audit for
  -- depending on choice.
  ⟨(Sq.every_value_square v).elim fun W h => ⟨W, h.1⟩,
   (Ch.every_value_chain v).elim fun W h => ⟨W, h.1⟩⟩

end NaturalSections
