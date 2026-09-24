import ResearchNativeStructure.Cells

/-!
# Proof-relevant cells

AuthorityEffect: None.  NS-5 asked for a cell calculus in which the order
of swaps is data, with composition, unit, associativity and interchange
laws that are not trivial.  `Cell` is a proposition, so those laws held
only in the degenerate sense.

Here a cell from `l` to `l'` at `s` (`CellD`) is a sequence of swap
positions, with the proof that each swap is verified (at the state its
prefix reaches, the two orders of the pair reach the same state) and that
the sequence ends at `l'`.  Two cells are equal exactly when their swap
sequences are equal.  Proved here:

* `CellD.id_vcomp`, `CellD.vcomp_id`, `CellD.vcomp_assoc`: vertical
  composition, which runs one sequence after the other, is strictly
  unital and associative.
* `CellD.whiskerR`, `CellD.whiskerL`, `CellD.hcomp`: whiskering keeps or
  shifts the positions; horizontal composition whiskers and composes.
* `CellD.interchange`: the interchange law holds up to `FarRel`, the
  declared relation that exchanges two adjacent swaps at least two
  positions apart, in any context.  It does not hold strictly.
* `cell_iff_nonempty`: the thin quotient is the existing `Cell`: a `Cell`
  exists exactly when a `CellD` does.
* `braid_cells_differ`: from genesis, three pairwise commuting events give
  two cells with the same endpoints, by positions `0, 1, 0` and
  `1, 0, 1`, that differ and are not related by `FarRel`.  So the calculus
  is not thin, even modulo distant exchanges.
* `vcomp_inv_ne_id`: a cell composed with its inverse is not the identity.
  This is a category of cells, not a groupoid; cancellation, and the
  three-swap relation above, would be further declared relations.
-/

namespace ResearchNativeStructure

open PrimitivePassage TraceAlgebra TransitionAlphabet

/-! ## Swaps at a position -/

/-- Exchange the entries at positions `i` and `i + 1`, when both exist. -/
def swapAt : Nat → List PEvent → List PEvent
  | 0, x :: y :: r => y :: x :: r
  | i + 1, x :: r => x :: swapAt i r
  | _, l => l

/-- Position `i` of `l` is a verified swap from `s`: at the state the
prefix reaches, the two orders of the pair reach the same state. -/
def okAt : PState → Nat → List PEvent → Prop
  | s, 0, x :: y :: _ => step (step s x) y = step (step s y) x
  | s, i + 1, x :: r => okAt (step s x) i r
  | _, _, _ => False

theorem swapAt_swapAt : ∀ (i : Nat) (l : List PEvent), swapAt i (swapAt i l) = l
  | 0, _ :: _ :: _ => rfl
  | 0, [] => rfl
  | 0, [_] => rfl
  | _ + 1, [] => rfl
  | i + 1, x :: r => by simp only [swapAt]; rw [swapAt_swapAt i r]

theorem okAt_swapAt : ∀ (s : PState) (i : Nat) (l : List PEvent), okAt s i l → okAt s i (swapAt i l)
  | _, 0, _ :: _ :: _, h => h.symm
  | s, i + 1, x :: r, h => okAt_swapAt (step s x) i r h

theorem length_swapAt : ∀ (i : Nat) (l : List PEvent), (swapAt i l).length = l.length
  | 0, _ :: _ :: _ => rfl
  | 0, [] => rfl
  | 0, [_] => rfl
  | _ + 1, [] => rfl
  | i + 1, x :: r => by simp only [swapAt, List.length_cons]; rw [length_swapAt i r]

theorem okAt_lt : ∀ (s : PState) (i : Nat) (l : List PEvent), okAt s i l → i + 1 < l.length
  | _, 0, _ :: _ :: _, _ => by simp
  | s, i + 1, _ :: r, h => by
      have := okAt_lt (step s _) i r h
      simp only [List.length_cons]; omega

/-! ## Swap sequences -/

/-- Every position of the sequence is a verified swap, each read on the
list the earlier swaps produced. -/
def Valid (s : PState) : List PEvent → List Nat → Prop
  | _, [] => True
  | l, i :: ws => okAt s i l ∧ Valid s (swapAt i l) ws

/-- The list a sequence of swaps produces. -/
def applyAll : List PEvent → List Nat → List PEvent
  | l, [] => l
  | l, i :: ws => applyAll (swapAt i l) ws

theorem applyAll_append (l : List PEvent) (ws₁ ws₂ : List Nat) :
    applyAll l (ws₁ ++ ws₂) = applyAll (applyAll l ws₁) ws₂ := by
  induction ws₁ generalizing l with
  | nil => rfl
  | cons i rest ih => exact ih (swapAt i l)

theorem valid_append (s : PState) (l : List PEvent) (ws₁ ws₂ : List Nat) :
    Valid s l (ws₁ ++ ws₂) ↔ Valid s l ws₁ ∧ Valid s (applyAll l ws₁) ws₂ := by
  induction ws₁ generalizing l with
  | nil => simp [Valid, applyAll]
  | cons i rest ih =>
      show (okAt s i l ∧ Valid s (swapAt i l) (rest ++ ws₂)) ↔
        (okAt s i l ∧ Valid s (swapAt i l) rest) ∧ Valid s (applyAll (swapAt i l) rest) ws₂
      rw [ih]; exact and_assoc.symm

theorem length_applyAll (l : List PEvent) (ws : List Nat) :
    (applyAll l ws).length = l.length := by
  induction ws generalizing l with
  | nil => rfl
  | cons i rest ih => show (applyAll (swapAt i l) rest).length = _; rw [ih, length_swapAt]

/-- Every position in a valid sequence is below the list's last index. -/
theorem valid_bound (s : PState) (l : List PEvent) (ws : List Nat) (h : Valid s l ws) :
    ∀ i ∈ ws, i + 1 < l.length := by
  induction ws generalizing l with
  | nil => intro i hi; cases hi
  | cons j rest ih =>
      intro i hi
      obtain ⟨hj, hr⟩ := h
      cases hi with
      | head => exact okAt_lt s j l hj
      | tail _ hi' => have := ih (swapAt j l) hr i hi'; rwa [length_swapAt] at this

/-! ## Proof-relevant cells -/

/-- A cell from `l` to `l'` at `s`: a sequence of swap positions, which is
data, with the proof that each swap is verified and that the sequence
ends at `l'`. -/
def CellD (s : PState) (l l' : List PEvent) : Type :=
  { ws : List Nat // Valid s l ws ∧ applyAll l ws = l' }

namespace CellD

variable {s : PState} {l l' l'' l''' : List PEvent}

/-- The identity cell: no swaps. -/
def id (s : PState) (l : List PEvent) : CellD s l l := ⟨[], trivial, rfl⟩

/-- Vertical composition: do the first cell's swaps, then the second's. -/
def vcomp (c : CellD s l l') (d : CellD s l' l'') : CellD s l l'' :=
  ⟨c.1 ++ d.1, (valid_append s l c.1 d.1).2 ⟨c.2.1, by rw [c.2.2]; exact d.2.1⟩,
    by rw [applyAll_append, c.2.2, d.2.2]⟩

theorem id_vcomp (c : CellD s l l') : (id s l).vcomp c = c := Subtype.ext rfl

theorem vcomp_id (c : CellD s l l') : c.vcomp (id s l') = c :=
  Subtype.ext (List.append_nil _)

theorem vcomp_assoc (c : CellD s l l') (d : CellD s l' l'') (e : CellD s l'' l''') :
    (c.vcomp d).vcomp e = c.vcomp (d.vcomp e) :=
  Subtype.ext (List.append_assoc _ _ _)

end CellD

/-! ## Inverse -/

theorem valid_reverse (s : PState) (l : List PEvent) (ws : List Nat) (h : Valid s l ws) :
    Valid s (applyAll l ws) ws.reverse ∧ applyAll (applyAll l ws) ws.reverse = l := by
  induction ws generalizing l with
  | nil => exact ⟨trivial, rfl⟩
  | cons i rest ih =>
      obtain ⟨hi, hr⟩ := h
      obtain ⟨hv, ha⟩ := ih (swapAt i l) hr
      have e1 : applyAll l (i :: rest) = applyAll (swapAt i l) rest := rfl
      rw [e1, List.reverse_cons, valid_append, applyAll_append, ha]
      refine ⟨⟨hv, okAt_swapAt s i l hi, trivial⟩, swapAt_swapAt i l⟩

namespace CellD

variable {s : PState} {l l' l'' : List PEvent}

/-- The inverse cell: the same swaps in reverse order. -/
def inv (c : CellD s l l') : CellD s l' l :=
  ⟨c.1.reverse, by
    have h := valid_reverse s l c.1 c.2.1
    rw [c.2.2] at h
    exact h⟩

end CellD

/-! ## Whiskering -/

theorem okAt_append_right : ∀ (s : PState) (i : Nat) (l m : List PEvent),
    okAt s i l → okAt s i (l ++ m)
  | _, 0, _ :: _ :: _, _, h => h
  | s, i + 1, x :: r, m, h => okAt_append_right (step s x) i r m h

theorem swapAt_append_right : ∀ (s : PState) (i : Nat) (l m : List PEvent),
    okAt s i l → swapAt i (l ++ m) = swapAt i l ++ m
  | _, 0, _ :: _ :: _, _, _ => rfl
  | s, i + 1, x :: r, m, h => by
      show x :: swapAt i (r ++ m) = x :: swapAt i r ++ m
      rw [swapAt_append_right (step s x) i r m h]; rfl

theorem valid_append_right (s : PState) (l m : List PEvent) (ws : List Nat) (h : Valid s l ws) :
    Valid s (l ++ m) ws ∧ applyAll (l ++ m) ws = applyAll l ws ++ m := by
  induction ws generalizing l with
  | nil => exact ⟨trivial, rfl⟩
  | cons i rest ih =>
      obtain ⟨hi, hr⟩ := h
      have hs := swapAt_append_right s i l m hi
      obtain ⟨hv, ha⟩ := ih (swapAt i l) hr
      refine ⟨⟨okAt_append_right s i l m hi, ?_⟩, ?_⟩
      · show Valid s (swapAt i (l ++ m)) rest; rw [hs]; exact hv
      · show applyAll (swapAt i (l ++ m)) rest = _; rw [hs]; exact ha

theorem okAt_append_left (s : PState) (k l : List PEvent) (i : Nat) :
    okAt s (k.length + i) (k ++ l) ↔ okAt (replayP k s) i l := by
  induction k generalizing s with
  | nil => simp [replayP]
  | cons x k ih =>
      have e : (x :: k).length + i = (k.length + i) + 1 := by simp only [List.length_cons]; omega
      rw [e]
      exact ih (step s x)

theorem swapAt_append_left (k l : List PEvent) (i : Nat) :
    swapAt (k.length + i) (k ++ l) = k ++ swapAt i l := by
  induction k with
  | nil => simp
  | cons x k ih =>
      have e : (x :: k).length + i = (k.length + i) + 1 := by simp only [List.length_cons]; omega
      rw [e]
      show x :: swapAt (k.length + i) (k ++ l) = x :: (k ++ swapAt i l)
      rw [ih]

theorem valid_append_left (s : PState) (k l : List PEvent) (ws : List Nat)
    (h : Valid (replayP k s) l ws) :
    Valid s (k ++ l) (ws.map (k.length + ·)) ∧
      applyAll (k ++ l) (ws.map (k.length + ·)) = k ++ applyAll l ws := by
  induction ws generalizing l with
  | nil => exact ⟨trivial, rfl⟩
  | cons i rest ih =>
      obtain ⟨hi, hr⟩ := h
      obtain ⟨hv, ha⟩ := ih (swapAt i l) hr
      have hs := swapAt_append_left k l i
      refine ⟨⟨(okAt_append_left s k l i).2 hi, ?_⟩, ?_⟩
      · show Valid s (swapAt (k.length + i) (k ++ l)) (rest.map (k.length + ·)); rw [hs]; exact hv
      · show applyAll (swapAt (k.length + i) (k ++ l)) (rest.map (k.length + ·)) = _
        rw [hs]; exact ha

/-! ## The thin quotient is `Cell` -/

theorem okAt_cell : ∀ (s : PState) (i : Nat) (l : List PEvent), okAt s i l → Cell s l (swapAt i l)
  | _, 0, x :: y :: r, h => Cell.swap (Swap.mk [] r x y h)
  | s, i + 1, x :: r, h => cell_append_left [x] (okAt_cell (step s x) i r h)

theorem valid_cell (s : PState) (l : List PEvent) (ws : List Nat) (h : Valid s l ws) :
    Cell s l (applyAll l ws) := by
  induction ws generalizing l with
  | nil => exact Cell.refl l
  | cons i rest ih => exact Cell.trans (okAt_cell s i l h.1) (ih (swapAt i l) h.2)

namespace CellD

variable {s : PState} {l l' : List PEvent}

theorem toCell (c : CellD s l l') : Cell s l l' := c.2.2 ▸ valid_cell s l c.1 c.2.1

theorem sound (c : CellD s l l') : replayP l s = replayP l' s := cell_sound c.toCell

end CellD

namespace CellD

variable {s s' : PState} {l l' l'' m m' m'' : List PEvent}

/-- Right whiskering: the same swaps, followed by an untouched suffix. -/
def whiskerR (m : List PEvent) (c : CellD s l l') : CellD s (l ++ m) (l' ++ m) :=
  ⟨c.1, by
    have h := valid_append_right s l m c.1 c.2.1
    rw [c.2.2] at h
    exact h⟩

/-- Left whiskering: the swaps shifted past an untouched prefix, read from
the state the prefix reaches. -/
def whiskerL (k : List PEvent) (c : CellD (replayP k s) l l') : CellD s (k ++ l) (k ++ l') :=
  ⟨c.1.map (k.length + ·), by
    have h := valid_append_left s k l c.1 c.2.1
    rw [c.2.2] at h
    exact h⟩

/-- Move a cell to an equal start state; the swaps are unchanged. -/
def castState (h : s = s') (c : CellD s l l') : CellD s' l l' := ⟨c.1, h ▸ c.2⟩

/-- **Horizontal composition.**  The first cell whiskered by the source
suffix, then the second cell, moved to the state the first cell's target
reaches, whiskered by that target. -/
def hcomp (c : CellD s l l') (d : CellD (replayP l s) m m') : CellD s (l ++ m) (l' ++ m') :=
  (c.whiskerR m).vcomp ((d.castState c.sound).whiskerL l')

theorem hcomp_val (c : CellD s l l') (d : CellD (replayP l s) m m') :
    (c.hcomp d).1 = c.1 ++ d.1.map (l'.length + ·) := rfl

end CellD

/-! ## Interchange, up to the exchange of distant swaps -/

/-- Exchanging two adjacent swaps whose positions are at least two apart,
in any context, closed under equivalence.  This is the declared relation
under which interchange holds. -/
inductive FarRel : List Nat → List Nat → Prop where
  | refl (ws : List Nat) : FarRel ws ws
  | exch (p q : List Nat) (i j : Nat) (h : i + 2 ≤ j ∨ j + 2 ≤ i) :
      FarRel (p ++ i :: j :: q) (p ++ j :: i :: q)
  | symm {a b : List Nat} : FarRel a b → FarRel b a
  | trans {a b c : List Nat} : FarRel a b → FarRel b c → FarRel a c

theorem FarRel.append_left (p : List Nat) {a b : List Nat} (h : FarRel a b) :
    FarRel (p ++ a) (p ++ b) := by
  induction h with
  | refl _ => exact FarRel.refl _
  | exch p' q i j hij =>
      have := FarRel.exch (p ++ p') q i j hij
      simpa [List.append_assoc] using this
  | symm _ ih => exact FarRel.symm ih
  | trans _ _ ih₁ ih₂ => exact FarRel.trans ih₁ ih₂

theorem FarRel.append_right (q : List Nat) {a b : List Nat} (h : FarRel a b) :
    FarRel (a ++ q) (b ++ q) := by
  induction h with
  | refl _ => exact FarRel.refl _
  | exch p q' i j hij =>
      have := FarRel.exch p (q' ++ q) i j hij
      simpa [List.append_assoc] using this
  | symm _ ih => exact FarRel.symm ih
  | trans _ _ ih₁ ih₂ => exact FarRel.trans ih₁ ih₂

/-- One swap moves past a block of swaps at least two positions above it. -/
theorem FarRel.move_one (i : Nat) (B q : List Nat) (hB : ∀ j ∈ B, i + 2 ≤ j) :
    FarRel (i :: (B ++ q)) (B ++ i :: q) := by
  induction B with
  | nil => exact FarRel.refl _
  | cons j B ih =>
      have h1 : FarRel (i :: j :: (B ++ q)) (j :: i :: (B ++ q)) :=
        FarRel.exch [] (B ++ q) i j (Or.inl (hB j (List.mem_cons_self ..)))
      have h2 : FarRel (j :: i :: (B ++ q)) (j :: (B ++ i :: q)) :=
        FarRel.append_left [j] (ih (fun k hk => hB k (List.mem_cons_of_mem j hk)))
      exact FarRel.trans h1 h2

/-- A block of swaps below position `n - 1` exchanges with a block at or
above `n`. -/
theorem FarRel.blocks (n : Nat) (A B : List Nat) (hA : ∀ i ∈ A, i + 1 < n)
    (hB : ∀ j ∈ B, n ≤ j) : FarRel (A ++ B) (B ++ A) := by
  induction A with
  | nil => simpa using FarRel.refl B
  | cons i A ih =>
      have h1 : FarRel (i :: (A ++ B)) (i :: (B ++ A)) :=
        FarRel.append_left [i] (ih (fun k hk => hA k (List.mem_cons_of_mem i hk)))
      have hi := hA i (List.mem_cons_self ..)
      have h2 : FarRel (i :: (B ++ A)) (B ++ i :: A) :=
        FarRel.move_one i B A (fun j hj => by have := hB j hj; omega)
      exact FarRel.trans h1 h2

namespace CellD

variable {s : PState} {l l' l'' m m' m'' : List PEvent}

theorem length_eq (c : CellD s l l') : l'.length = l.length := by
  rw [← c.2.2, length_applyAll]

/-- **Interchange**, up to `FarRel`: composing vertically then horizontally
and composing horizontally then vertically give swap sequences related by
exchanges of distant swaps. -/
theorem interchange (c₁ : CellD s l l') (c₂ : CellD s l' l'')
    (d₁ : CellD (replayP l s) m m') (d₂ : CellD (replayP l s) m' m'') :
    FarRel ((c₁.vcomp c₂).hcomp (d₁.vcomp d₂)).1
      ((c₁.hcomp d₁).vcomp (c₂.hcomp (d₂.castState c₁.sound))).1 := by
  have hl : l''.length = l'.length := c₂.length_eq
  have e1 : ((c₁.vcomp c₂).hcomp (d₁.vcomp d₂)).1 =
      (c₁.1 ++ c₂.1) ++ (d₁.1 ++ d₂.1).map (l''.length + ·) := rfl
  have e2 : ((c₁.hcomp d₁).vcomp (c₂.hcomp (d₂.castState c₁.sound))).1 =
      (c₁.1 ++ d₁.1.map (l'.length + ·)) ++ (c₂.1 ++ d₂.1.map (l''.length + ·)) := rfl
  rw [e1, e2, hl, List.map_append]
  have hA : ∀ i ∈ c₂.1, i + 1 < l'.length := valid_bound s l' c₂.1 c₂.2.1
  have hB : ∀ j ∈ d₁.1.map (l'.length + ·), l'.length ≤ j := by
    intro j hj
    obtain ⟨k, _, rfl⟩ := List.mem_map.1 hj
    omega
  have := FarRel.blocks l'.length c₂.1 (d₁.1.map (l'.length + ·)) hA hB
  have := FarRel.append_left c₁.1 (FarRel.append_right (d₂.1.map (l'.length + ·)) this)
  simpa [List.append_assoc] using this

end CellD

/-! ## The thin quotient, and cells that are not thin -/

/-- `Cell` is exactly the existence of a proof-relevant cell. -/
theorem cell_iff_nonempty {s : PState} {l l' : List PEvent} :
    Cell s l l' ↔ Nonempty (CellD s l l') := by
  constructor
  · intro h
    induction h with
    | refl l => exact ⟨CellD.id _ l⟩
    | swap h =>
        cases h with
        | mk a b e₁ e₂ hc =>
            refine ⟨⟨[a.length], ⟨?_, trivial⟩, ?_⟩⟩
            · simpa using (okAt_append_left _ a (e₁ :: e₂ :: b) 0).2 hc
            · exact swapAt_append_left a (e₁ :: e₂ :: b) 0
    | symm _ ih => exact ih.elim fun c => ⟨c.inv⟩
    | trans _ _ ih₁ ih₂ => exact ih₁.elim fun c => ih₂.elim fun d => ⟨c.vcomp d⟩
  · rintro ⟨c⟩
    exact c.toCell

/-- Distant exchanges only reorder a swap sequence. -/
theorem FarRel.perm {a b : List Nat} (h : FarRel a b) : a.Perm b := by
  induction h with
  | refl _ => exact List.Perm.refl _
  | exch p q i j _ => exact List.Perm.append_left p (List.Perm.swap j i q)
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂

/-- Three events that commute pairwise at genesis and after each other. -/
def braidList : List PEvent := [.setBudget 1, .setLicense false, .admitOcc 5]

/-- Exchange the outer two by swapping positions 0, 1, 0. -/
def braidLeft : CellD genesisP braidList (braidList.reverse) :=
  ⟨[0, 1, 0], ⟨by exact rfl, by exact rfl, by exact rfl, trivial⟩, rfl⟩

/-- The same exchange by swapping positions 1, 0, 1. -/
def braidRight : CellD genesisP braidList (braidList.reverse) :=
  ⟨[1, 0, 1], ⟨by exact rfl, by exact rfl, by exact rfl, trivial⟩, rfl⟩

/-- **Cells are not thin.**  The two cells differ, and no exchange of
distant swaps relates them. -/
theorem braid_cells_differ :
    braidLeft ≠ braidRight ∧ ¬ FarRel braidLeft.1 braidRight.1 := by
  refine ⟨fun h => ?_, fun h => ?_⟩
  · have := congrArg Subtype.val h
    simp [braidLeft, braidRight] at this
  · have := (FarRel.perm h).count_eq 0
    simp [braidLeft, braidRight] at this

/-- A composite with its inverse is a cell from a list to itself that is
not the identity: the calculus is a category, not yet a groupoid, and
cancellation holds only up to a further declared relation. -/
theorem vcomp_inv_ne_id : braidLeft.vcomp braidLeft.inv ≠ CellD.id genesisP braidList := by
  intro h
  have := congrArg Subtype.val h
  simp [CellD.vcomp, CellD.inv, CellD.id, braidLeft] at this

end ResearchNativeStructure
