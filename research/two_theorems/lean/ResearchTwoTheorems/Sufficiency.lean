import ResearchTwoTheorems.Reading

/-!
# Sharp against sufficient, and representation against acquisition
(2026-10-28, after the second review)

AuthorityEffect: None.  Outside the seal.

Two readings of "the observer sees the actor" come apart.

* `Sufficient D E p`: the observer's questions know the actor
  (`Knows D (questions E) p`): whatever the observer merges, the actor
  merges.  An over-informative observer is sufficient.
* `Sharp D E p`: the verdict kernel is exactly the actor's partition.
* `sharp_iff_sufficient_and_consistent`: sharp is sufficient together with
  consistent (`Reading.Consistent`: whatever the observer separates, the
  actor separates).  `sufficient_not_sharp` and `consistent_not_sufficient`
  show the two conjuncts independent: on `[0, 1]` the one-view observer
  `[[0]]` is sufficient for the constant actor and not sharp, and the
  empty observer is consistent with the identity and not sufficient.

Representation against acquisition.  `sharp_observable_iff` (Observer)
says an actor with at most `2 ^ m` fibers on `D` is sharply observed by
some `m`-view observer.  Its witness `sharpObserver D p m` is built from
`fiberIdx D p`, the actor's own fiber index: `sharpObserver_views` shows
each view cut from `D` by one bit of that index, and
`sharpObserver_congr` shows the construction depends on `p` only through
its partition on `D`.  So the theorem is one of **representation
capacity**: `m` views can carry a partition with at most `2 ^ m` fibers.
It says nothing about **acquisition**: how an observer that does not
hold the partition could come to hold it by admitted operations, and at
what cost.  `sharp_fixes_partition` is the converse side: any sharp
observer carries exactly the actor's partition, so acquiring a sharp
observer is acquiring that partition.  Acquisition is OPEN (CLAIMS
TT-43o); a statement is drafted in the README and not proved.
-/

namespace ResearchTwoTheorems
namespace Sufficiency

open Represented Compression Institution Reading

/-- Sufficient observation: the observer's questions know the actor. -/
def Sufficient (D : List Nat) (E : Evaluator) (p : Presentation) : Prop :=
  Knows D (questions E) p

instance (D : List Nat) (E : Evaluator) (p : Presentation) :
    Decidable (Sufficient D E p) :=
  knowsDecidable D (questions E) p

/-- Sufficiency unfolded: whatever the observer merges, the actor merges. -/
theorem sufficient_iff (D : List Nat) (E : Evaluator) (p : Presentation) :
    Sufficient D E p ↔
      ∀ x, x ∈ D → ∀ y, y ∈ D → verdictB E x y = false → p x = p y := by
  unfold Sufficient
  rw [knows_iff_determined]
  constructor
  · intro h x hx y hy hv
    exact h x hx y hy ((verdictB_false_iff_sigEq E x y).mp hv)
  · intro h x hx y hy hs
    exact h x hx y hy ((verdictB_false_iff_sigEq E x y).mpr hs)

/-- **Sharp is sufficient and consistent.**  Exact observation is the
conjunction of the two one-directional readings. -/
theorem sharp_iff_sufficient_and_consistent (D : List Nat) (E : Evaluator)
    (p : Presentation) :
    Sharp D E p ↔ Sufficient D E p ∧ Consistent D E p := by
  rw [sufficient_iff]
  constructor
  · intro h
    exact ⟨fun x hx y hy hv => (h x hx y hy).mp hv, sharp_consistent h⟩
  · rintro ⟨hk, hc⟩ x hx y hy
    constructor
    · exact hk x hx y hy
    · intro hp
      cases hv : verdictB E x y with
      | false => rfl
      | true => exact absurd hp (hc x hx y hy hv)

/-- An over-informative observer: sufficient for the constant actor on
`[0, 1]`, not sharp (it separates what the actor merges). -/
theorem sufficient_not_sharp :
    Sufficient [0, 1] [[0]] (fun _ => 0) ∧ ¬ Sharp [0, 1] [[0]] (fun _ => 0) := by
  constructor
  · decide
  · unfold Sharp
    decide

/-- An under-informative observer: consistent with the identity on
`[0, 1]`, not sufficient (it merges what the actor separates). -/
theorem consistent_not_sufficient :
    Consistent [0, 1] [] (fun x => x) ∧ ¬ Sufficient [0, 1] [] (fun x => x) := by
  constructor
  · unfold Consistent
    decide
  · decide

/-- Neither conjunct implies the other. -/
theorem sufficient_consistent_independent :
    (∃ D E p, Sufficient D E p ∧ ¬ Consistent D E p) ∧
    (∃ D E p, Consistent D E p ∧ ¬ Sufficient D E p) := by
  refine ⟨⟨[0, 1], [[0]], fun _ => 0, sufficient_not_sharp.1, ?_⟩,
    ⟨[0, 1], [], fun x => x, consistent_not_sufficient.1,
      consistent_not_sufficient.2⟩⟩
  intro hc
  exact sufficient_not_sharp.2
    ((sharp_iff_sufficient_and_consistent _ _ _).mpr ⟨sufficient_not_sharp.1, hc⟩)

/-! ## Representation, not acquisition -/

/-- Any two actors sharply observed by one observer have the same
partition on `D`: a sharp observer carries exactly its actor's
partition. -/
theorem sharp_fixes_partition {D : List Nat} {E : Evaluator} {p p' : Presentation}
    (h : Sharp D E p) (h' : Sharp D E p') :
    ∀ x, x ∈ D → ∀ y, y ∈ D → (p x = p y ↔ p' x = p' y) := by
  intro x hx y hy
  rw [← h x hx y hy, ← h' x hx y hy]

/-- The observer that `sharp_observable_of_fibers_le` exhibits. -/
def sharpObserver (D : List Nat) (p : Presentation) (m : Nat) : Evaluator :=
  bitObserver D (fiberIdx D p) m

theorem sharpObserver_sharp (D : List Nat) (p : Presentation) (m : Nat)
    (h : classCount D [p] ≤ 2 ^ m) : Sharp D (sharpObserver D p m) p :=
  bitObserver_sharp D _ m
    (fun _ hx => Nat.lt_of_lt_of_le (fiberIdx_lt D p hx) h) p
    (fun _ hx _ hy => fiberIdx_eq_iff D p hx hy)

/-- Each view of the exhibited observer is `D` cut by one bit of the
actor's own fiber index: the construction consumes `p`. -/
theorem sharpObserver_views (D : List Nat) (p : Presentation) (m : Nat) :
    sharpObserver D p m =
      (List.range m).map (fun b => D.filter (fun x => (fiberIdx D p x).testBit b)) :=
  rfl

/-- First-match positions in the deduplicated signature lists agree for two
signature maps with the same partition on `D`. -/
theorem posOf_dedupL_congr (D : List Nat) (f g : Nat → List Nat)
    (h : ∀ a, a ∈ D → ∀ b, b ∈ D → (f a = f b ↔ g a = g b)) :
    ∀ x, x ∈ D →
      posOf (f x) (dedupL (D.map f)) = posOf (g x) (dedupL (D.map g)) := by
  induction D with
  | nil => intro x hx; cases hx
  | cons a t ih =>
    have ih' := ih (fun b hb c hc =>
      h b (List.mem_cons_of_mem _ hb) c (List.mem_cons_of_mem _ hc))
    have hmem : memB (f a) (t.map f) = memB (g a) (t.map g) := by
      cases hf : memB (f a) (t.map f) with
      | true =>
        obtain ⟨b, hb, hfb⟩ := List.mem_map.mp ((memB_iff _ _).mp hf)
        have hgb : g b = g a :=
          (h b (List.mem_cons_of_mem _ hb) a List.mem_cons_self).mp hfb
        exact ((memB_iff _ _).mpr (List.mem_map.mpr ⟨b, hb, hgb⟩)).symm
      | false =>
        cases hg : memB (g a) (t.map g) with
        | false => rfl
        | true =>
          obtain ⟨b, hb, hgb⟩ := List.mem_map.mp ((memB_iff _ _).mp hg)
          have hfb : f b = f a :=
            (h b (List.mem_cons_of_mem _ hb) a List.mem_cons_self).mpr hgb
          have := (memB_iff _ _).mpr (List.mem_map.mpr ⟨b, hb, hfb⟩)
          rw [hf] at this
          exact Bool.noConfusion this
    intro x hx
    simp only [List.map_cons, dedupL_cons]
    cases hf : memB (f a) (t.map f) with
    | true =>
      rw [← hmem, hf]
      simp only [cond_true]
      obtain ⟨b, hb, hfb⟩ := List.mem_map.mp ((memB_iff _ _).mp hf)
      cases hx with
      | head =>
        have hgb : g b = g a :=
          (h b (List.mem_cons_of_mem _ hb) a List.mem_cons_self).mp hfb
        rw [← hfb, ← hgb]
        exact ih' b hb
      | tail _ hm => exact ih' x hm
    | false =>
      rw [← hmem, hf]
      simp only [cond_false, posOf_cons]
      cases hx with
      | head =>
        rw [if_pos rfl, if_pos rfl]
      | tail _ hm =>
        have hfx : f x ≠ f a := by
          intro he
          have := (memB_iff _ _).mpr (List.mem_map.mpr ⟨x, hm, he⟩)
          rw [hf] at this
          exact Bool.noConfusion this
        have hgx : g x ≠ g a := fun he => hfx
          ((h x (List.mem_cons_of_mem _ hm) a List.mem_cons_self).mpr he)
        rw [if_neg hfx, if_neg hgx, ih' x hm]

/-- The fiber index depends on the actor only through its partition on `D`. -/
theorem fiberIdx_congr (D : List Nat) (p p' : Presentation)
    (h : ∀ x, x ∈ D → ∀ y, y ∈ D → (p x = p y ↔ p' x = p' y)) :
    ∀ x, x ∈ D → fiberIdx D p x = fiberIdx D p' x := by
  intro x hx
  unfold fiberIdx classList
  apply posOf_dedupL_congr D (sigList [p]) (sigList [p'])
  · intro a _ b _
    rw [sigList_single, sigList_single, sigList_single, sigList_single]
    constructor
    · intro he; injection he with he; rw [(h a ‹_› b ‹_›).mp he]
    · intro he; injection he with he; rw [(h a ‹_› b ‹_›).mpr he]
  · exact hx

/-- **The exhibited observer is a function of the partition alone.**  Two
actors with the same partition on `D` yield the same observer: what the
construction consumes is exactly the partition it is then said to
observe. -/
theorem sharpObserver_congr (D : List Nat) (p p' : Presentation) (m : Nat)
    (h : ∀ x, x ∈ D → ∀ y, y ∈ D → (p x = p y ↔ p' x = p' y)) :
    sharpObserver D p m = sharpObserver D p' m := by
  unfold sharpObserver bitObserver bitView
  apply List.map_congr_left
  intro b _
  apply List.filter_congr
  intro x hx
  rw [fiberIdx_congr D p p' h x hx]

end Sufficiency
end ResearchTwoTheorems
