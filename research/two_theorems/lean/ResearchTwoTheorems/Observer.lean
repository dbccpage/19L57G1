import Derivation.Represented
import Derivation.NoOutside
import Derivation.Compression
import Derivation.PresentationRelativity
import Derivation.CapacityBound

/-!
# Theorem I — sharp observability

AuthorityEffect: None.  Outside the seal; consumes the sealed `Derivation`
package read-only.

Vocabulary, each item tagged.

* DECLARED (supplied by the requester, not Genesis): an *actor* is a
  presentation `p : Nat → Nat` of the represented carrier; an *observer*
  is a Genesis evaluator `Represented.Evaluator`, a finite list of views;
  the observer *observes* `x` and `y` as one when no view separates them
  (`verdictB E x y = false`).
* DEFINITION: `Sharp D E p` — the observer's verdict kernel on `D` is
  exactly the actor's fiber partition.
* THEOREMS: `sharp_iff_presentationIdentity` (sharpness is Genesis
  presentation identity between the actor and the observer's signature
  quotient); `verdict_ceiling` (no verdict computed from the observer's own
  answers separates what the observer merges); `sharp_observable_iff`
  (an actor is sharply observable by some `m`-view observer exactly when it
  has at most `2 ^ m` fibers on `D` — both directions, hence sharp);
  `absolute_observer_iff` (an observer adequate for every question family
  separates every pair of `D`: absolute observation is no compression,
  Genesis `absolute_adequacy_iff_injective`).
* FACT, NOT LAW: `sep_irrefl`, `sep_witness_ne`, `separation_fact_not_law`.
  Observed separation never holds of a point and itself, because `sepB` is
  built from the metatheory's decidable inequality on `Bool` (the priced
  import A3 of `paper/primitive_difference.md`).  This is a property of the
  observer calculus, not an admitted law on the carrier, and a witnessed
  separation of one pair says nothing about any other pair.

Metatheory used: types, lists, propositional logic, structural recursion,
`Decidable`/`decide`, and the Genesis pigeonhole.  No choice principles.
-/

namespace ResearchTwoTheorems

open Represented Compression

/-- DECLARED: an actor is a presentation of the carrier. -/
abbrev Presentation := Nat → Nat

/-! ## Views as questions -/

/-- A view read as a question with answers in `{0, 1}`. -/
def viewQ (c : View) : Nat → Nat := fun x => if x ∈ c then 1 else 0

/-- The question family of an observer. -/
def questions (E : Evaluator) : List (Nat → Nat) := E.map viewQ

theorem viewQ_eq_iff (c : View) (x y : Nat) :
    viewQ c x = viewQ c y ↔ ((x ∈ c) ↔ (y ∈ c)) := by
  unfold viewQ
  by_cases hx : x ∈ c <;> by_cases hy : y ∈ c <;> simp [hx, hy]

theorem sepB_eq_false_iff (c : View) (x y : Nat) :
    sepB c x y = false ↔ ((x ∈ c) ↔ (y ∈ c)) := by
  unfold sepB
  by_cases hx : x ∈ c <;> by_cases hy : y ∈ c <;> simp [hx, hy]

theorem verdictB_eq_false_iff (E : Evaluator) (x y : Nat) :
    verdictB E x y = false ↔ ∀ c, c ∈ E → sepB c x y = false := by
  unfold verdictB
  rw [List.any_eq_false]
  constructor
  · intro h c hc
    have := h c hc
    cases hs : sepB c x y with
    | false => rfl
    | true => exact absurd hs this
  · intro h c hc
    rw [h c hc]
    exact Bool.false_ne_true

/-- The observer merges `x` and `y` exactly when they agree on every
question of the observer: the verdict kernel is Genesis signature
equality. -/
theorem verdictB_false_iff_sigEq (E : Evaluator) (x y : Nat) :
    verdictB E x y = false ↔ SigEq (questions E) x y := by
  rw [verdictB_eq_false_iff]
  constructor
  · intro h q hq
    obtain ⟨c, hc, rfl⟩ := List.mem_map.mp hq
    exact (viewQ_eq_iff c x y).mpr ((sepB_eq_false_iff c x y).mp (h c hc))
  · intro h c hc
    exact (sepB_eq_false_iff c x y).mpr
      ((viewQ_eq_iff c x y).mp (h (viewQ c) (List.mem_map.mpr ⟨c, hc, rfl⟩)))

/-! ## Fact, not law -/

/-- Observed separation never holds of a point and itself.  This comes
from `Bool`'s decidable inequality, not from any admitted law. -/
theorem sep_irrefl (c : View) (i : Nat) : sepB c i i = false := by
  unfold sepB
  cases decide (i ∈ c) <;> rfl

/-- A witnessed separation has distinct endpoints (the observer-calculus
analogue of `PrimDiff.irrefl_witness_ne`, needing no admitted law). -/
theorem sep_witness_ne {c : View} {i j : Nat} (h : sepB c i j = true) :
    i ≠ j := by
  intro hij
  subst hij
  rw [sep_irrefl] at h
  exact Bool.false_ne_true h

theorem verdict_irrefl (E : Evaluator) (i : Nat) : verdictB E i i = false :=
  (verdictB_eq_false_iff E i i).mpr (fun c _ => sep_irrefl c i)

theorem verdict_witness_ne {E : Evaluator} {i j : Nat}
    (h : verdictB E i j = true) : i ≠ j := by
  intro hij
  subst hij
  rw [verdict_irrefl] at h
  exact Bool.false_ne_true h

/-- A witnessed separation is a fact about one pair and licenses no law
about another: one view separates `0` from `1` and merges `0` with `2`. -/
theorem separation_fact_not_law :
    ∃ (c : View) (i j k : Nat),
      sepB c i j = true ∧ j ≠ k ∧ sepB c i k = false :=
  ⟨[0, 2], 0, 1, 2, by decide, by decide, by decide⟩

/-! ## Sharp observation -/

/-- Sharp observation of the actor `p` by the observer `E` on `D`: the
verdict kernel is exactly the fiber partition of `p`. -/
def Sharp (D : List Nat) (E : Evaluator) (p : Presentation) : Prop :=
  ∀ x, x ∈ D → ∀ y, y ∈ D → (verdictB E x y = false ↔ p x = p y)

/-- Sharpness is fiber identity between the actor and the observer's
signature quotient `pQ D (questions E)`. -/
theorem sharp_iff_fiberIdentity (D : List Nat) (E : Evaluator)
    (p : Presentation) :
    Sharp D E p ↔
      PresentationRelativity.FiberIdentityOn D (pQ D (questions E)) p := by
  unfold Sharp PresentationRelativity.FiberIdentityOn
  constructor
  · intro h x hx y hy
    rw [pQ_exact D _ x hx y hy, ← verdictB_false_iff_sigEq]
    exact h x hx y hy
  · intro h x hx y hy
    rw [verdictB_false_iff_sigEq, ← pQ_exact D _ x hx y hy]
    exact h x hx y hy

/-- **Theorem I(a).**  Sharpness is Genesis presentation identity (mutual
factorization) between the actor and the observer's signature quotient. -/
theorem sharp_iff_presentationIdentity (D : List Nat) (E : Evaluator)
    (p : Presentation) :
    Sharp D E p ↔
      PresentationRelativity.PresentationIdentityOn D (pQ D (questions E)) p := by
  rw [sharp_iff_fiberIdentity,
    PresentationRelativity.presentationIdentity_iff_fiberIdentity]

/-- **Theorem I(b), the ceiling.**  Any verdict computed from the
observer's own answers is constant on the observer's kernel: whatever
`f` does with two signatures, it cannot tell a pair from a pair the
observer merges pointwise. -/
theorem verdict_ceiling (E : Evaluator) (f : List Nat → List Nat → Bool)
    {x x' y y' : Nat}
    (hx : verdictB E x x' = false) (hy : verdictB E y y' = false) :
    f (sigList (questions E) x) (sigList (questions E) y) =
      f (sigList (questions E) x') (sigList (questions E) y') := by
  have h1 := (sigEq_iff_sigList _ x x').mp
    ((verdictB_false_iff_sigEq E x x').mp hx)
  have h2 := (sigEq_iff_sigList _ y y').mp
    ((verdictB_false_iff_sigEq E y y').mp hy)
  rw [h1, h2]

/-! ## Resolution: `m` views resolve exactly `2 ^ m` fibers -/

theorem sigList_questions_length (E : Evaluator) (x : Nat) :
    (sigList (questions E) x).length = E.length := by
  unfold sigList questions
  rw [List.length_map, List.length_map]

theorem sigList_questions_bounded (E : Evaluator) (x : Nat) :
    ∀ z ∈ sigList (questions E) x, z < 2 := by
  intro z hz
  unfold sigList questions at hz
  rw [List.map_map] at hz
  obtain ⟨c, _, hc⟩ := List.mem_map.mp hz
  rw [← hc]
  show (if x ∈ c then (1 : Nat) else 0) < 2
  split <;> decide

/-- The code of `x`'s signature: a number below `2 ^ E.length`. -/
def sigCode (E : Evaluator) (x : Nat) : Nat :=
  CapacityBound.encode 2 (sigList (questions E) x)

theorem sigCode_lt (E : Evaluator) (x : Nat) : sigCode E x < 2 ^ E.length := by
  have h := CapacityBound.encode_lt 2 _ (sigList_questions_bounded E x)
  rw [sigList_questions_length] at h
  exact h

theorem verdict_false_of_sigCode_eq (E : Evaluator) {x y : Nat}
    (h : sigCode E x = sigCode E y) : verdictB E x y = false := by
  apply (verdictB_false_iff_sigEq E x y).mpr
  apply (sigEq_iff_sigList _ x y).mpr
  exact CapacityBound.encode_inj 2 _ _
    (by rw [sigList_questions_length, sigList_questions_length])
    (sigList_questions_bounded E x) (sigList_questions_bounded E y) h

/-- **Resolution ceiling.**  Among any `2 ^ m + 1` points (enumerated by
`f`), an `m`-view observer merges two distinct indices. -/
theorem resolution_ceiling (E : Evaluator) (f : Nat → Nat) :
    ∃ s t, s < 2 ^ E.length + 1 ∧ t < 2 ^ E.length + 1 ∧ s ≠ t ∧
      verdictB E (f s) (f t) = false := by
  obtain ⟨s, hs, t, ht, hst, heq⟩ :=
    Pigeonhole.pigeonhole (2 ^ E.length) (fun t => sigCode E (f t))
      (fun p _ => sigCode_lt E (f p))
  exact ⟨s, t, hs, ht, hst, verdict_false_of_sigCode_eq E heq⟩

/-- No `m`-view observer is sharp for an actor with `2 ^ m + 1` pairwise
separated points of `D`. -/
theorem not_sharp_of_many_fibers (D : List Nat) (E : Evaluator)
    (p : Presentation) (f : Nat → Nat)
    (hf : ∀ t, t < 2 ^ E.length + 1 → f t ∈ D)
    (hsep : ∀ s t, s < 2 ^ E.length + 1 → t < 2 ^ E.length + 1 → s ≠ t →
      p (f s) ≠ p (f t)) :
    ¬ Sharp D E p := by
  intro hS
  obtain ⟨s, t, hs, ht, hst, hv⟩ := resolution_ceiling E f
  exact hsep s t hs ht hst ((hS (f s) (hf s hs) (f t) (hf t ht)).mp hv)

/-! ### Attainment: bit views -/

/-- The `b`-th bit view of an index function on `D`. -/
def bitView (D : List Nat) (idx : Nat → Nat) (b : Nat) : View :=
  D.filter (fun x => (idx x).testBit b)

/-- The `m`-view observer reading the `m` low bits of an index. -/
def bitObserver (D : List Nat) (idx : Nat → Nat) (m : Nat) : Evaluator :=
  (List.range m).map (bitView D idx)

theorem bitObserver_length (D : List Nat) (idx : Nat → Nat) (m : Nat) :
    (bitObserver D idx m).length = m := by
  unfold bitObserver
  rw [List.length_map, List.length_range]

theorem mem_bitView {D : List Nat} {idx : Nat → Nat} {b x : Nat}
    (hx : x ∈ D) : x ∈ bitView D idx b ↔ (idx x).testBit b = true := by
  unfold bitView
  rw [List.mem_filter]
  exact ⟨fun h => h.2, fun h => ⟨hx, h⟩⟩

theorem bool_eq_of_iff {a b : Bool} (h : a = true ↔ b = true) : a = b := by
  cases a <;> cases b <;> simp_all

/-- The bit observer of an index below `2 ^ m` has exactly the index's
kernel on `D`. -/
theorem bitObserver_kernel (D : List Nat) (idx : Nat → Nat) (m : Nat)
    (hidx : ∀ x, x ∈ D → idx x < 2 ^ m) {x y : Nat} (hx : x ∈ D) (hy : y ∈ D) :
    verdictB (bitObserver D idx m) x y = false ↔ idx x = idx y := by
  rw [verdictB_eq_false_iff]
  constructor
  · intro h
    apply Nat.eq_of_testBit_eq
    intro b
    by_cases hb : b < m
    · have hmem : bitView D idx b ∈ bitObserver D idx m :=
        List.mem_map.mpr ⟨b, List.mem_range.mpr hb, rfl⟩
      have := (sepB_eq_false_iff _ x y).mp (h _ hmem)
      rw [mem_bitView hx, mem_bitView hy] at this
      exact bool_eq_of_iff this
    · have hb' : m ≤ b := Nat.le_of_not_lt hb
      have hpow : 2 ^ m ≤ 2 ^ b := Nat.pow_le_pow_right (by decide) hb'
      rw [Nat.testBit_lt_two_pow (Nat.lt_of_lt_of_le (hidx x hx) hpow),
        Nat.testBit_lt_two_pow (Nat.lt_of_lt_of_le (hidx y hy) hpow)]
  · intro h c hc
    obtain ⟨b, _, rfl⟩ := List.mem_map.mp hc
    apply (sepB_eq_false_iff _ x y).mpr
    rw [mem_bitView hx, mem_bitView hy, h]

/-- An actor indexed below `2 ^ m` on `D` is sharply observed by its bit
observer. -/
theorem bitObserver_sharp (D : List Nat) (idx : Nat → Nat) (m : Nat)
    (hidx : ∀ x, x ∈ D → idx x < 2 ^ m) (p : Presentation)
    (hp : ∀ x, x ∈ D → ∀ y, y ∈ D → (idx x = idx y ↔ p x = p y)) :
    Sharp D (bitObserver D idx m) p := by
  intro x hx y hy
  rw [bitObserver_kernel D idx m hidx hx hy]
  exact hp x hx y hy

/-! ### Fiber indices from the Genesis class list -/

/-- Position of a signature in a list of signatures (first match). -/
def posOf (s : List Nat) : List (List Nat) → Nat
  | [] => 0
  | a :: t => if s = a then 0 else posOf s t + 1

theorem posOf_cons (s a : List Nat) (t : List (List Nat)) :
    posOf s (a :: t) = if s = a then 0 else posOf s t + 1 := rfl

theorem posOf_lt {s : List Nat} :
    ∀ {l : List (List Nat)}, s ∈ l → posOf s l < l.length := by
  intro l
  induction l with
  | nil => intro h; cases h
  | cons a t ih =>
    intro h
    rw [posOf_cons]
    split
    · exact Nat.succ_pos _
    · rename_i hne
      have hs : s ∈ t := by
        cases h with
        | head => exact absurd rfl hne
        | tail _ hm => exact hm
      exact Nat.succ_lt_succ (ih hs)

theorem posOf_inj {s s' : List Nat} :
    ∀ {l : List (List Nat)}, s ∈ l → s' ∈ l → posOf s l = posOf s' l → s = s' := by
  intro l
  induction l with
  | nil => intro h; cases h
  | cons a t ih =>
    intro hs hs' heq
    rw [posOf_cons, posOf_cons] at heq
    by_cases h1 : s = a
    · by_cases h2 : s' = a
      · exact h1.trans h2.symm
      · rw [if_pos h1, if_neg h2] at heq
        exact absurd heq (Nat.noConfusion)
    · by_cases h2 : s' = a
      · rw [if_neg h1, if_pos h2] at heq
        exact absurd heq.symm (Nat.noConfusion)
      · rw [if_neg h1, if_neg h2] at heq
        have hst : s ∈ t := by
          cases hs with
          | head => exact absurd rfl h1
          | tail _ hm => exact hm
        have hst' : s' ∈ t := by
          cases hs' with
          | head => exact absurd rfl h2
          | tail _ hm => exact hm
        exact ih hst hst' (Nat.succ.inj heq)

theorem mem_dedupL (s : List Nat) :
    ∀ l : List (List Nat), s ∈ dedupL l ↔ s ∈ l := by
  intro l
  induction l with
  | nil => exact Iff.rfl
  | cons a t ih =>
    rw [dedupL_cons]
    cases hm : memB a t with
    | true =>
      have ha : a ∈ t := (memB_iff a t).mp hm
      show s ∈ dedupL t ↔ s ∈ a :: t
      rw [ih]
      constructor
      · exact fun h => List.mem_cons_of_mem a h
      · intro h
        cases h with
        | head => exact ha
        | tail _ hm' => exact hm'
    | false =>
      show s ∈ a :: dedupL t ↔ s ∈ a :: t
      rw [List.mem_cons, List.mem_cons, ih]

theorem dedupL_nodup : ∀ l : List (List Nat), (dedupL l).Nodup := by
  intro l
  induction l with
  | nil => exact List.Pairwise.nil
  | cons a t ih =>
    rw [dedupL_cons]
    cases hm : memB a t with
    | true => exact ih
    | false =>
      show (a :: dedupL t).Nodup
      rw [List.nodup_cons]
      refine ⟨?_, ih⟩
      intro hmem
      have : memB a t = true := (memB_iff a t).mpr ((mem_dedupL a t).mp hmem)
      rw [this] at hm
      exact Bool.noConfusion hm

/-- Distinct positions of a duplicate-free list hold distinct entries. -/
theorem nodup_getD_inj {α : Type} [DecidableEq α] (d : α) :
    ∀ (l : List α), l.Nodup → ∀ s t, s < l.length → t < l.length →
      l.getD s d = l.getD t d → s = t := by
  intro l
  induction l with
  | nil => intro _ s t hs; cases hs
  | cons a u ih =>
    intro hnd s t hs ht heq
    rw [List.nodup_cons] at hnd
    obtain ⟨ha, hu⟩ := hnd
    cases s with
    | zero =>
      cases t with
      | zero => rfl
      | succ t' =>
        rw [List.getD_cons_zero, List.getD_cons_succ] at heq
        exfalso
        apply ha
        rw [heq]
        have ht' : t' < u.length := Nat.lt_of_succ_lt_succ ht
        rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem ht']
        exact List.getElem_mem ht'
    | succ s' =>
      cases t with
      | zero =>
        rw [List.getD_cons_succ, List.getD_cons_zero] at heq
        exfalso
        apply ha
        rw [← heq]
        have hs' : s' < u.length := Nat.lt_of_succ_lt_succ hs
        rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hs']
        exact List.getElem_mem hs'
      | succ t' =>
        rw [List.getD_cons_succ, List.getD_cons_succ] at heq
        have := ih hu s' t' (Nat.lt_of_succ_lt_succ hs)
          (Nat.lt_of_succ_lt_succ ht) heq
        rw [this]

theorem getD_mem {α : Type} (d : α) (l : List α) (i : Nat) (hi : i < l.length) :
    l.getD i d ∈ l := by
  rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi]
  exact List.getElem_mem hi

/-- The class list of an actor on `D` (Genesis `dedupL` of signatures). -/
def classList (D : List Nat) (p : Presentation) : List (List Nat) :=
  dedupL (D.map (sigList [p]))

theorem classList_length (D : List Nat) (p : Presentation) :
    (classList D p).length = classCount D [p] := rfl

theorem sigList_single (p : Presentation) (x : Nat) :
    sigList [p] x = [p x] := rfl

/-- The fiber index of `x`: the position of its class in the class list. -/
def fiberIdx (D : List Nat) (p : Presentation) (x : Nat) : Nat :=
  posOf (sigList [p] x) (classList D p)

theorem mem_classList_of_mem (D : List Nat) (p : Presentation) {x : Nat}
    (hx : x ∈ D) : sigList [p] x ∈ classList D p :=
  (mem_dedupL _ _).mpr (List.mem_map.mpr ⟨x, hx, rfl⟩)

theorem fiberIdx_lt (D : List Nat) (p : Presentation) {x : Nat} (hx : x ∈ D) :
    fiberIdx D p x < classCount D [p] :=
  posOf_lt (mem_classList_of_mem D p hx)

theorem fiberIdx_eq_iff (D : List Nat) (p : Presentation) {x y : Nat}
    (hx : x ∈ D) (hy : y ∈ D) :
    fiberIdx D p x = fiberIdx D p y ↔ p x = p y := by
  constructor
  · intro h
    have h' : sigList [p] x = sigList [p] y :=
      posOf_inj (mem_classList_of_mem D p hx) (mem_classList_of_mem D p hy) h
    rw [sigList_single, sigList_single] at h'
    injection h'
  · intro h
    unfold fiberIdx
    rw [sigList_single, sigList_single, h]

/-- **Attainment.**  An actor with at most `2 ^ m` fibers on `D` is
sharply observed by some `m`-view observer. -/
theorem sharp_observable_of_fibers_le (D : List Nat) (p : Presentation)
    (m : Nat) (h : classCount D [p] ≤ 2 ^ m) :
    ∃ E : Evaluator, E.length = m ∧ Sharp D E p :=
  ⟨bitObserver D (fiberIdx D p) m, bitObserver_length D _ m,
    bitObserver_sharp D _ m
      (fun _ hx => Nat.lt_of_lt_of_le (fiberIdx_lt D p hx) h) p
      (fun _ hx _ hy => fiberIdx_eq_iff D p hx hy)⟩

/-- A representative of the `t`-th class: first-match selection over the
represented `D` (Genesis `pick`), total and choice-free. -/
def classRep (D : List Nat) (p : Presentation) (t : Nat) : Nat :=
  (pick D (fun x => decide (sigList [p] x = (classList D p).getD t []))).getD 0

theorem classRep_spec (D : List Nat) (p : Presentation) {t : Nat}
    (ht : t < classCount D [p]) :
    classRep D p t ∈ D ∧ sigList [p] (classRep D p t) = (classList D p).getD t [] := by
  have hmem : (classList D p).getD t [] ∈ classList D p :=
    getD_mem [] _ t ht
  have hmap : (classList D p).getD t [] ∈ D.map (sigList [p]) :=
    (mem_dedupL _ _).mp hmem
  obtain ⟨x, hx, hxs⟩ := List.mem_map.mp hmap
  obtain ⟨r, hr⟩ := pick_some_of_mem D
    (fun z => decide (sigList [p] z = (classList D p).getD t [])) x hx
    (decide_eq_true hxs)
  have hval : classRep D p t = r := by
    unfold classRep
    rw [hr]
    rfl
  rw [hval]
  exact ⟨pick_mem D _ r hr, of_decide_eq_true (pick_holds D _ r hr)⟩

/-- **Non-attainment.**  An actor with more than `2 ^ m` fibers on `D` is
sharply observed by no `m`-view observer. -/
theorem not_sharp_observable_of_fibers_gt (D : List Nat) (p : Presentation)
    (m : Nat) (h : 2 ^ m < classCount D [p]) :
    ¬ ∃ E : Evaluator, E.length = m ∧ Sharp D E p := by
  rintro ⟨E, hE, hS⟩
  have hbound : 2 ^ E.length + 1 ≤ classCount D [p] := by
    rw [hE]
    exact h
  refine not_sharp_of_many_fibers D E p (classRep D p) ?_ ?_ hS
  · intro t ht
    exact (classRep_spec D p (Nat.lt_of_lt_of_le ht hbound)).1
  · intro s t hs ht hst hps
    have hs' := (classRep_spec D p (Nat.lt_of_lt_of_le hs hbound)).2
    have ht' := (classRep_spec D p (Nat.lt_of_lt_of_le ht hbound)).2
    apply hst
    apply nodup_getD_inj [] (classList D p) (dedupL_nodup _) s t
      (Nat.lt_of_lt_of_le hs hbound) (Nat.lt_of_lt_of_le ht hbound)
    rw [← hs', ← ht', sigList_single, sigList_single, hps]

/-- **Theorem I(c), sharp both ways.**  An actor is sharply observable by
some `m`-view observer on `D` exactly when it has at most `2 ^ m` fibers
on `D`.  The resolution of `m` views is exactly `2 ^ m`. -/
theorem sharp_observable_iff (D : List Nat) (p : Presentation) (m : Nat) :
    (∃ E : Evaluator, E.length = m ∧ Sharp D E p) ↔
      classCount D [p] ≤ 2 ^ m := by
  constructor
  · intro hE
    apply Nat.le_of_not_lt
    intro hlt
    exact not_sharp_observable_of_fibers_gt D p m hlt hE
  · exact sharp_observable_of_fibers_le D p m

/-! ## Absolute observation is carrier-relative -/

/-- An observer adequate for every declared question family separates
every pair of `D` it is asked about — absolute observation is exactly
no-compression (Genesis `absolute_adequacy_iff_injective`, read on the
observer's signature quotient). -/
theorem absolute_observer_iff (D : List Nat) (E : Evaluator) :
    (∀ Q : List (Nat → Nat), Adequate D Q (pQ D (questions E))) ↔
      (∀ x, x ∈ D → ∀ y, y ∈ D → verdictB E x y = false → x = y) := by
  rw [absolute_adequacy_iff_injective]
  constructor
  · intro h x hx y hy hv
    exact h x hx y hy ((pQ_exact D _ x hx y hy).mpr
      ((verdictB_false_iff_sigEq E x y).mp hv))
  · intro h x hx y hy hp
    exact h x hx y hy ((verdictB_false_iff_sigEq E x y).mpr
      ((pQ_exact D _ x hx y hy).mp hp))

/-- On a carrier with more than `2 ^ m` distinct points no `m`-view
observer is absolute. -/
theorem no_absolute_observer_of_large_carrier (D : List Nat) (E : Evaluator)
    (h : 2 ^ E.length < classCount D [fun x => x]) :
    ¬ (∀ Q : List (Nat → Nat), Adequate D Q (pQ D (questions E))) := by
  intro habs
  have hsep := (absolute_observer_iff D E).mp habs
  have hsharp : Sharp D E (fun x => x) := by
    intro x hx y hy
    constructor
    · exact hsep x hx y hy
    · intro hxy
      have hxy' : x = y := hxy
      rw [hxy']
      exact verdict_irrefl E y
  exact not_sharp_observable_of_fibers_gt D (fun x => x) E.length h ⟨E, rfl, hsharp⟩

/-- Absoluteness is carrier-relative.  On two points one view is adequate
for every question, so "no absolute observer" is false without a carrier;
what holds is `no_absolute_observer_of_large_carrier`: every `m`-view
observer fails on a carrier of more than `2 ^ m` points.  (Added
2026-10-28 after review.) -/
theorem absolute_observer_two_points :
    ∀ Q : List (Nat → Nat), Adequate [0, 1] Q (pQ [0, 1] (questions [[0]])) :=
  (absolute_observer_iff [0, 1] [[0]]).mpr (by decide)

end ResearchTwoTheorems
