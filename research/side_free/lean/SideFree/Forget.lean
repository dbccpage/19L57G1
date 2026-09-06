/-
The forgetting map and the forgetful lemma, over the two declared carriers.

The Python census checks the lemma at 1344 declared cells.  This file proves
it for ALL regimes, ALL renamings and both flag settings, with no finite
bound, so the census is the bounded cross-check and this is the proof.

What the lemma says: whatever a side-typed renaming does to a side-typed
regime, the same renaming does the corresponding thing to the forgotten one,
and a side-typed automorphism therefore has a side-free counterpart.  Its
corollary fixes the SIGN of the whole comparison: side-free separation
implies side-typed separation, so the pinned minimum is at most the side-free
minimum and a negative difference is unreachable.

The side-typed carrier here is this tree's own re-declaration: a
COUNTERMODEL-DOMAIN object, never claimed to be the pinned carrier.

A renaming is carried by an index list rather than by a permutation
structure, and ``reorder`` reads the marks at those indices in that order.
Nothing below needs the index list to be a permutation.  The lemma holds for
every index list, which is strictly stronger than needed and avoids importing
a permutation theory this package does not have.
-/

import SideFree.Basic

namespace SideFree

/-- A side-typed regime: a reading, and for each mark its label with the side
it lies on.  Carrying the pair guarantees the two lists have equal length,
which the pinned carrier enforces by a refusal instead. -/
structure SidedRegime where
  reading : Bool
  marks : List (String × Bool)
  deriving DecidableEq, Repr

/-- The side exchange.  It moves every mark to the other side and touches no
label. -/
def reflect (r : SidedRegime) : SidedRegime :=
  ⟨r.reading, r.marks.map (fun p => (p.1, !p.2))⟩

/-- Forget the reading and the placement; keep the labels in their order. -/
def forget (r : SidedRegime) : Regime := ⟨r.marks.map Prod.fst⟩

/-- A renaming, applied to a list: read the entries at the given indices, in
the given order. -/
def reorder (pi : List Nat) (xs : List α) : List α :=
  match pi with
  | [] => []
  | i :: rest =>
    match xs[i]? with
    | none => reorder rest xs
    | some x => x :: reorder rest xs

/-- Rename the marks of a side-typed regime. -/
def sidedRename (pi : List Nat) (r : SidedRegime) : SidedRegime :=
  ⟨r.reading, reorder pi r.marks⟩

/-- Rename the marks of a side-free regime. -/
def freeRename (pi : List Nat) (r : Regime) : Regime := ⟨reorder pi r.marks⟩

/-- Replace every entry by one placeholder: what a key that forgets the
labels leaves behind. -/
def blank (xs : List α) : List String := xs.map (fun _ => "")

/-- The side-typed key.  With the labels kept it is the reading and the whole
pair list; with them forgotten the labels are blanked, so what is left is the
reading and the placement. -/
def sidedKey (keepLabels : Bool) (r : SidedRegime) : Bool × List (String × Bool) :=
  if keepLabels then (r.reading, r.marks)
  else (r.reading, r.marks.map (fun p => ("", p.2)))

/-- The side-free key.  With the labels kept it is the label list; with them
forgotten the labels are blanked, so what is left is the arity. -/
def freeKey (keepLabels : Bool) (r : Regime) : List String :=
  if keepLabels then r.marks else blank r.marks

/-! ## Renaming commutes with forgetting -/

/-- Reading entries at indices commutes with mapping a function over them. -/
theorem reorder_map (f : α → β) (pi : List Nat) (xs : List α) :
    reorder pi (xs.map f) = (reorder pi xs).map f := by
  induction pi with
  | nil => rfl
  | cons i rest ih =>
    have hmap : (xs.map f)[i]? = (xs[i]?).map f := List.getElem?_map ..
    cases h : xs[i]? with
    | none => simp [reorder, hmap, h, ih]
    | some x => simp [reorder, hmap, h, ih]

/-- Blanking depends on nothing but the length. -/
theorem blank_congr (xs : List α) (ys : List β) (h : xs.length = ys.length) :
    blank xs = blank ys := by
  induction xs generalizing ys with
  | nil =>
    cases ys with
    | nil => rfl
    | cons b bs => exact Nat.noConfusion h
  | cons a as ih =>
    cases ys with
    | nil => exact Nat.noConfusion h
    | cons b bs =>
      have hrest : as.length = bs.length := Nat.succ.inj h
      show "" :: blank as = "" :: blank bs
      rw [ih bs hrest]

/-- Blanking a list of the same length gives a list of the same length. -/
theorem blank_length (xs : List α) : (blank xs).length = xs.length := by
  simp [blank]

/-- Reading entries at indices gives a length that depends on nothing but the
length of the list read. -/
theorem reorder_length_congr (pi : List Nat) (xs : List α) (ys : List β)
    (h : xs.length = ys.length) :
    (reorder pi xs).length = (reorder pi ys).length := by
  induction pi with
  | nil => rfl
  | cons i rest ih =>
    by_cases hx : i < xs.length
    · have hy : i < ys.length := by omega
      have ex : xs[i]? = some xs[i] := List.getElem?_eq_getElem hx
      have ey : ys[i]? = some ys[i] := List.getElem?_eq_getElem hy
      simp only [reorder, ex, ey, List.length_cons]
      omega
    · have hxn : xs[i]? = none := List.getElem?_eq_none (by omega)
      have hyn : ys[i]? = none := List.getElem?_eq_none (by omega)
      simp only [reorder, hxn, hyn]
      exact ih

/-- Forgetting a renamed regime is renaming the forgotten one. -/
theorem forget_rename (pi : List Nat) (r : SidedRegime) :
    forget (sidedRename pi r) = freeRename pi (forget r) := by
  simp [forget, sidedRename, freeRename, reorder_map]

/-- The side exchange is invisible after forgetting. -/
theorem forget_reflect (r : SidedRegime) : forget (reflect r) = forget r := by
  simp [forget, reflect, List.map_map, Function.comp_def]

/-- The side exchange leaves the number of marks alone. -/
theorem reflect_length (r : SidedRegime) :
    (reflect r).marks.length = r.marks.length := by
  simp [reflect]

/-! ## The forgetful lemma -/

/-- **The forgetful lemma, with the labels kept.**  If a renaming carries a
side-typed regime -- or its exchange, since ``forget_reflect`` makes the two
indistinguishable after forgetting -- onto itself, then the same renaming
carries the forgotten regime onto itself. -/
theorem forgetful_lemma_keeping_labels (pi : List Nat) (r base : SidedRegime)
    (hbase : forget base = forget r)
    (haut : sidedKey true (sidedRename pi base) = sidedKey true r) :
    freeKey true (freeRename pi (forget r)) = freeKey true (forget r) := by
  have hmarks : reorder pi base.marks = r.marks := by
    have h := congrArg Prod.snd haut
    simpa [sidedKey, sidedRename] using h
  have hfst : reorder pi (base.marks.map Prod.fst) = r.marks.map Prod.fst := by
    rw [reorder_map, hmarks]
  have hb : base.marks.map Prod.fst = r.marks.map Prod.fst :=
    congrArg Regime.marks hbase
  rw [hb] at hfst
  simpa [freeKey, freeRename, forget] using hfst

/-- **The forgetful lemma, with the labels forgotten.**  The same statement
under the poorer key, where what survives is the arity. -/
theorem forgetful_lemma_forgetting_labels (pi : List Nat) (r base : SidedRegime)
    (hbase : base.marks.length = r.marks.length)
    (haut : sidedKey false (sidedRename pi base) = sidedKey false r) :
    freeKey false (freeRename pi (forget r)) = freeKey false (forget r) := by
  have hmarks :
      (reorder pi base.marks).map (fun p : String × Bool => ("", p.2))
        = r.marks.map (fun p : String × Bool => ("", p.2)) := by
    have h := congrArg Prod.snd haut
    simpa [sidedKey, sidedRename] using h
  have hlen : (reorder pi base.marks).length = r.marks.length := by
    have h := congrArg List.length hmarks
    simpa using h
  have hsame : (reorder pi r.marks).length = (reorder pi base.marks).length :=
    reorder_length_congr pi r.marks base.marks hbase.symm
  have hgoal : (reorder pi (r.marks.map Prod.fst)).length
      = (r.marks.map Prod.fst).length := by
    rw [reorder_map]
    simp only [List.length_map]
    omega
  have := blank_congr (reorder pi (r.marks.map Prod.fst)) (r.marks.map Prod.fst) hgoal
  simpa [freeKey, freeRename, forget] using this

/-! ## The corollary that fixes the sign -/

/-- A renaming moves one index to another. -/
def moves (pi : List Nat) (i j : Nat) : Bool := (pi[i]?.getD i) == j

/-- **The corollary, with the labels kept.**  If no renaming that is a
side-free automorphism carries mark ``i`` to mark ``j``, then no renaming
that is a side-typed automorphism does either.  Side-free separation implies
side-typed separation, and never the other way about. -/
theorem free_separation_implies_sided_separation
    (r base : SidedRegime) (i j : Nat) (pis : List (List Nat))
    (hbase : forget base = forget r)
    (hfree : ∀ pi ∈ pis,
      freeKey true (freeRename pi (forget r)) = freeKey true (forget r) →
        moves pi i j = false) :
    ∀ pi ∈ pis,
      sidedKey true (sidedRename pi base) = sidedKey true r → moves pi i j = false := by
  intro pi hpi haut
  exact hfree pi hpi (forgetful_lemma_keeping_labels pi r base hbase haut)

/-- **The corollary, with the labels forgotten.** -/
theorem free_separation_implies_sided_separation_forgetting_labels
    (r base : SidedRegime) (i j : Nat) (pis : List (List Nat))
    (hbase : base.marks.length = r.marks.length)
    (hfree : ∀ pi ∈ pis,
      freeKey false (freeRename pi (forget r)) = freeKey false (forget r) →
        moves pi i j = false) :
    ∀ pi ∈ pis,
      sidedKey false (sidedRename pi base) = sidedKey false r → moves pi i j = false := by
  intro pi hpi haut
  exact hfree pi hpi (forgetful_lemma_forgetting_labels pi r base hbase haut)

/-! ## The four rows of the side-free enumeration, at the retained regime -/

/-- The exchange of the two retained marks. -/
def exchange : List Nat := [1, 0]

/-- The identity renaming of two marks: the only one the withdrawal permits. -/
def identity2 : List Nat := [0, 1]

/-- The retained regime with the further mark the process admits. -/
def retainedPlus : Regime := ⟨["a", "a", "a"]⟩

/-- The exchange of the first two of three marks. -/
def exchange3 : List Nat := [1, 0, 2]

/-- **base fails.**  With the labels forgotten and the permutations kept, the
exchange is an automorphism of the retained regime. -/
theorem base_exchange_is_an_automorphism :
    freeKey false (freeRename exchange retained) = freeKey false retained := rfl

/-- The exchange carries the first retained mark to the second, so the
requirement fails at base. -/
theorem exchange_moves_zero_to_one : moves exchange 0 1 = true := rfl

/-- **keep_labels fails.**  Both retained marks carry the same label, so
keeping the labels distinguishes nothing and the exchange survives. -/
theorem keep_labels_exchange_is_an_automorphism :
    freeKey true (freeRename exchange retained) = freeKey true retained := rfl

/-- **extra_mark fails.**  With a third mark admitted and the labels
forgotten, what survives the key is the arity, which the exchange preserves. -/
theorem extra_mark_exchange_is_an_automorphism :
    freeKey false (freeRename exchange3 retainedPlus) = freeKey false retainedPlus := rfl

/-- The three-mark regime is the replay of the caller's history extended by
the process's own admission. -/
theorem retainedPlus_replays_from_genesis :
    replay genesis (callerHistory ++ [.admitOccurrence "a"]) = retainedPlus := rfl

/-- **withdraw_mark_permutations satisfies, BY UNFOLDING.**  With the
permutations withdrawn the identity is the only permitted renaming, and it
moves no index; the requirement then holds by unfolding the declaration and
not by any fact about the regime.  This is DEFINITION-level and is never
counted as content. -/
theorem withdrawal_moves_no_index :
    moves identity2 0 0 = true ∧ moves identity2 1 1 = true := ⟨rfl, rfl⟩

/-- Under the withdrawal the only permitted renaming does not carry the first
retained mark to the second. -/
theorem withdrawal_does_not_move_zero_to_one :
    ∀ pi ∈ [identity2], moves pi 0 1 = false := by
  intro pi hpi
  simp only [List.mem_singleton] at hpi
  subst hpi
  rfl

/-- The exchange is not the identity, so the withdrawal is a real restriction
and not a vacuous one. -/
theorem exchange_is_not_the_identity : exchange ≠ identity2 := by decide

end SideFree
