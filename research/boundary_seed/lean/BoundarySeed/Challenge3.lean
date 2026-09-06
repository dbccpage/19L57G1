import BoundarySeed.Basic
import BoundarySeed.Challenge1
import BoundarySeed.Challenge2

/-!
# Challenge 3: the required separation of the two retained wholes

Core Lean only.  The caller requires the two retained wholes to be internally
separable in a declared sense: no permitted renaming that carries the regime
onto itself carries one of the two marks to the other.

This file closes two things the Python enumeration cannot close on its own.

The first is the whole family of candidates that only add judgment forms.
`no_invariant_mark_property_separates_retained` is stated for an ARBITRARY
property of a `(Regime, Nat)` pair, so it covers every form the closed grammar
might gain and not only the ones the Python space enumerates: while the
composite of the side exchange with the exchange of the two internal
identities leaves a property alone, that property takes the same value at both
retained marks.  Its hypothesis is not vacuous and it is not vacuously
satisfied either: `mark_form_is_not_invariant_under_the_composite` exhibits a
property outside it, which is exactly why the two mark forms separate the two
marks as raw data and neither does so internally.

The second is the further-mark candidate.  A renaming of the marks is a
permutation of the placement list, and a permutation preserves how many marks
lie on each side; the side exchange exchanges those two counts.  So at a
placement whose two sides carry different numbers of marks, no renaming
returns the reflected placement to the original — for EVERY permutation, not
for the ones a bounded search enumerates.  `retained_counts_equal` records the
converse at the retained regime itself, where the two counts are equal and the
argument therefore says nothing: that is why the requirement genuinely fails
there rather than failing for want of a proof.

Every theorem below is stated for both readings.  Which of them is meaningful
under which reading is prose: whether the side exchange is a permitted
renaming is a fact about the reading and not about the placement, so the
statements are about the functions and the reading-dependence is named here.
Under `O` the composite is not a permitted renaming, so the first theorem
constrains nothing there; under `U` it is, and it is the obstruction.
-/

namespace BoundarySeed

/-! ## The composite, and what it leaves alone -/

/-- The side exchange followed by the exchange of the two internal identities. -/
def composite (r : Regime) : Regime := exchangeMarks (reflect r)

theorem composite_retained (rd : Reading) : composite (retained rd) = retained rd :=
  exchangeMarks_reflect_retained rd

theorem exchangeFirstTwo_zero : exchangeFirstTwo 0 = 1 := rfl

theorem exchangeFirstTwo_one : exchangeFirstTwo 1 = 0 := rfl

/-- Under `U` the composite is a renaming the reading permits, it carries the
retained regime onto itself, and it carries the first retained mark to the
second.  That is the Challenge 3 requirement failing under `U`. -/
theorem retained_U_requirement_fails :
    reflectionPermitted .U ∧ composite (retained .U) = retained .U
      ∧ exchangeFirstTwo 0 = 1 :=
  ⟨reflection_permitted_U, composite_retained .U, exchangeFirstTwo_zero⟩

/-- **No property of a mark that the composite leaves alone separates the two
retained marks.**  `P` ranges over every property of a `(Regime, Nat)` pair,
so this covers every judgment form the closed grammar might gain: adding forms
cannot meet the requirement while the composite remains a permitted renaming,
which under `U` it does.  Under `O` the composite is not permitted and the
statement constrains nothing. -/
theorem no_invariant_mark_property_separates_retained
    (rd : Reading) (P : Regime → Nat → Bool)
    (hinv : ∀ (r : Regime) (i : Nat), P (composite r) (exchangeFirstTwo i) = P r i) :
    P (retained rd) 0 = P (retained rd) 1 := by
  have h := hinv (retained rd) 0
  rw [composite_retained] at h
  exact h.symm

/-- The hypothesis above is a real restriction: neither mark form satisfies it.
This is why both forms separate the two retained marks as raw data while
neither separates them internally under `U`. -/
theorem mark_form_is_not_invariant_under_the_composite (s : Bool) :
    ¬ (∀ (r : Regime) (i : Nat),
        holds (composite r) (.onSide (exchangeFirstTwo i) s)
          = holds r (.onSide i s)) := by
  intro h
  have h0 := h (retained .U) 0
  rw [composite_retained, exchangeFirstTwo_zero, retained_onSide_one,
    retained_onSide_zero] at h0
  cases s <;> simp at h0

/-! ## How many marks lie on a side -/

/-- The number of marks a placement puts on a side.  Metatheoretic: it is a
count of the placement list and not an object-language judgment, the closed
grammar having no counting form. -/
def countOn : List Bool → Bool → Nat
  | [], _ => 0
  | b :: t, s => (if b == s then 1 else 0) + countOn t s

theorem countOn_nil (s : Bool) : countOn [] s = 0 := rfl

theorem countOn_cons (b : Bool) (t : List Bool) (s : Bool) :
    countOn (b :: t) s = (if b == s then 1 else 0) + countOn t s := rfl

/-- The side exchange exchanges the two counts. -/
theorem countOn_map_not (p : List Bool) (s : Bool) :
    countOn (p.map (fun b => !b)) s = countOn p (!s) := by
  induction p with
  | nil => rfl
  | cons b t ih =>
    show (if (!b) == s then 1 else 0) + countOn (t.map (fun b => !b)) s
      = (if b == (!s) then 1 else 0) + countOn t (!s)
    rw [ih]
    cases b <;> cases s <;> rfl

/-- A renaming of the marks preserves how many lie on each side. -/
theorem countOn_perm {p q : List Bool} (h : p.Perm q) (s : Bool) :
    countOn p s = countOn q s := by
  induction h with
  | nil => rfl
  | cons _ _ ih => rw [countOn_cons, countOn_cons, ih]
  | swap x y l =>
    rw [countOn_cons, countOn_cons, countOn_cons, countOn_cons]
    exact Nat.add_left_comm _ _ _
  | trans _ _ ih1 ih2 => exact ih1.trans ih2

/-- **At a placement whose two sides carry different numbers of marks, no
renaming undoes the side exchange.**  The renaming ranges over every
permutation of the placement, not over a bounded enumeration. -/
theorem reflect_not_undone_by_renaming (p q : List Bool)
    (hne : countOn p false ≠ countOn p true)
    (hq : q.Perm (p.map (fun b => !b))) : q ≠ p := by
  intro heq
  subst heq
  have h := countOn_perm hq false
  rw [countOn_map_not] at h
  exact hne h

/-! ## The further mark the process admits -/

/-- The regime reached by placing one further mark on a side of the retained
regime.  Which agent issues that event is a question about the Python
kernel's histories, decided there and priced there; the Lean model records
only what follows once the mark is placed. -/
def retainedPlus (rd : Reading) (s : Bool) : Regime := step (retained rd) (.place s)

theorem retainedPlus_eq (rd : Reading) (s : Bool) :
    retainedPlus rd s = ⟨rd, .initial, [false, true, s]⟩ := rfl

theorem retainedPlus_reading (rd : Reading) (s : Bool) : (retainedPlus rd s).reading = rd := rfl

theorem retainedPlus_initialDatum (rd : Reading) (s : Bool) :
    (retainedPlus rd s).initialDatum = .initial := rfl

/-- The placement alone, with the reading projected away, so that a decision
procedure is offered a goal with no free variable in it. -/
theorem retainedPlus_placement (rd : Reading) (s : Bool) :
    (retainedPlus rd s).placement = [false, true, s] := rfl

theorem retained_placement (rd : Reading) :
    (retained rd).placement = [false, true] := rfl

/-- After the further mark the two sides carry different numbers of marks. -/
theorem retainedPlus_counts_differ (rd : Reading) (s : Bool) :
    countOn (retainedPlus rd s).placement false
      ≠ countOn (retainedPlus rd s).placement true := by
  rw [retainedPlus_placement]
  cases s <;> decide

/-- So no renaming of the marks carries the reflected placement back: the side
exchange is part of no renaming that carries the regime onto itself, and the
obstruction of `no_invariant_mark_property_separates_retained` is gone. -/
theorem retainedPlus_reflection_is_not_an_automorphism (rd : Reading) (s : Bool)
    (q : List Bool)
    (hq : q.Perm ((retainedPlus rd s).placement.map (fun b => !b))) :
    q ≠ (retainedPlus rd s).placement :=
  reflect_not_undone_by_renaming _ q (retainedPlus_counts_differ rd s) hq

/-- The converse at the retained regime itself: its two sides carry equally
many marks, so the counting argument says nothing there.  The requirement
fails under `U` at that regime because the composite really does carry it onto
itself, not for want of an argument. -/
theorem retained_counts_equal (rd : Reading) :
    countOn (retained rd).placement false = countOn (retained rd).placement true := by
  rw [retained_placement]
  decide

/-- Both retained marks keep their judgments after the further mark is
placed. -/
theorem retainedPlus_judgments_survive (rd : Reading) (s : Bool) (i : Nat) (t : Bool)
    (hi : i < 2) :
    holds (retainedPlus rd s) (.onSide i t) = holds (retained rd) (.onSide i t) := by
  have hlen : i < (retained rd).placement.length := by
    rw [retained_placement_length]; exact hi
  exact step_preserves_onSide (retained rd) (.place s) i t hlen

/-- No event follows from the further-mark regime in the declared relation. -/
theorem no_event_follows_retainedPlus (rd : Reading) (s : Bool) (e : Event) :
    ¬ EventFollows (retainedPlus rd s) e :=
  no_event_follows _ _

end BoundarySeed
