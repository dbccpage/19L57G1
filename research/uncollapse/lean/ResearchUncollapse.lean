import Derivation.Basic
import Derivation.CountTransport
import Derivation.Mention
import Derivation.Inertia
import Derivation.Minimality
import Derivation.Apartness
import Derivation.TransitionTransport
import Ignition

/-!
# Can a new regime "uncollapse" `collapsed r a b`?

Outside the seal: a research tree that consumes the sealed `Derivation`
package read-only and changes nothing in it.  First built against
`23979a46308219b4cc9e7e172e4e32511f8efdb0`, core Lean 4.33.0.  AuthorityEffect: None.

`collapsed : Regime → Nat → Nat → Prop` takes ONE regime.  There is no
regime set in `Basic.lean`, so "adding a regime" has a referent only under
one of two readings:

* (E) extension: `r'` is `r` after admissions (`applyItem` / `applyDelta`);
* (F) family: collapse quantified over a set of regimes, and `r'` joins it.

Under (E) the answer is yes (witness: a two-item delta, `uncollapse_by_delta`).
On a well-formed regime, a delta keeps a collapsed pair collapsed unless one
of its items is an instance mentioning a target datum
(`uncollapse_only_by_mention_delta`); without well-formedness this fails.
Under (F) the answer is yes exactly when `r'` separates the pair
(`uncollapse_family_sep_iff`), provided the members share indices
(`family_index_dependence`); with correspondence maps the family is
presentation-relative and a renamed copy cannot uncollapse
(`collapsedInR_rename_cons`).
Section 3 ties both to `Apartness.lean`: `collapsed r` is `Indist` of the
regime's own apartness `separable r`.
-/

namespace ResearchUncollapse

open Derivation

/-! ## 1. Reading (E): extension by admission -/

/-- **Uncollapse happens.**  The Challenge 3 response: `R2L` collapses
`0, 1`; after `newForm 1, newInst 0 [0]` the pair is separated. -/
theorem uncollapse_by_delta :
    collapsed R2L 0 1 ∧ applyDelta R2L deltaU0 = some U0 ∧
      ¬ collapsed U0 0 1 :=
  ⟨R2L_collapsed, by decide, separable_not_collapsed U0_separable⟩

/-- A rule never uncollapses (no well-formedness needed). -/
theorem collapsed_ruleAll (r : Regime) (f : Nat) {d d' : Nat}
    (h : collapsed r d d') :
    collapsed { r with rules := insertNew r.rules f } d d' := by
  intro c hc
  have hc' : wfCtx r c := hc
  have key : ∀ e, derivable { r with rules := insertNew r.rules f } (plug c e)
      ↔ derivable r (plug c e) ∨ c.form = f := by
    intro e
    show (_ ∨ _) ↔ _
    rw [mem_insertNew]
    exact ⟨fun h => h.elim (fun h => Or.inl (Or.inl h))
              (fun h => h.elim (fun h => Or.inl (Or.inr h)) Or.inr),
           fun h => h.elim (fun h => h.elim Or.inl (fun h => Or.inr (Or.inl h)))
              (fun h => Or.inr (Or.inr h))⟩
  rw [key d, key d']
  exact or_congr (h c hc') Iff.rfl

/-- **Only a mentioning instance can uncollapse.**  For a well-formed
regime, one admitted item preserves the collapse of `d, d'` unless it is
an instance whose arguments mention `d` or `d'`.  Assembled from the
existing R1 (`collapsed_fresh_datum`), R2 (`collapsed_fresh_form`), R3
(`collapsed_append_unmentioning`) and `collapsed_ruleAll`. -/
theorem uncollapse_only_by_mention (r : Regime) (hwf : r.wf) (it : Item)
    (s : Regime) (hs : applyItem r it = some s) {d d' : Nat}
    (h : collapsed r d d')
    (hno : ¬ ∃ f args, it = .newInst f args ∧ (d ∈ args ∨ d' ∈ args)) :
    collapsed s d d' := by
  cases it with
  | newDatum =>
    cases hs
    exact (collapsed_fresh_datum r d d' (fun p hp => (hwf.1 p hp).2.2)).mpr h
  | newForm a =>
    simp only [applyItem] at hs
    split at hs
    · cases hs
      exact (collapsed_fresh_form r d d' a (fun p hp => (hwf.1 p hp).1)
        hwf.2.1).mpr h
    · cases hs
  | newRuleAll f =>
    simp only [applyItem] at hs
    split at hs
    · cases hs; exact collapsed_ruleAll r f h
    · cases hs
  | newInst f args =>
    simp only [applyItem] at hs
    split at hs
    · cases hs
      have hd : d ∉ args := fun m => hno ⟨f, args, rfl, Or.inl m⟩
      have hd' : d' ∉ args := fun m => hno ⟨f, args, rfl, Or.inr m⟩
      by_cases hm : (f, args) ∈ r.insts
      · rw [insertNew_of_mem hm]; exact h
      · rw [insertNew_of_not_mem hm]
        refine (collapsed_append_unmentioning r [(f, args)] d d' ?_ ?_).mpr h
        · intro p hp; rw [List.mem_singleton.mp hp]; exact hd
        · intro p hp; rw [List.mem_singleton.mp hp]; exact hd'
    · cases hs

/-- **The delta-level form.**  On a well-formed regime, a delta none of whose
items is an instance mentioning `d` or `d'` keeps `collapsed r d d'`.  Each
step stays well-formed by `Ignition.applyItem_wf`. -/
theorem uncollapse_only_by_mention_delta {d d' : Nat} :
    ∀ (δ : List Item) (r s : Regime), r.wf → applyDelta r δ = some s →
      collapsed r d d' →
      (∀ it ∈ δ, ¬ ∃ f args, it = .newInst f args ∧ (d ∈ args ∨ d' ∈ args)) →
      collapsed s d d'
  | [], r, s, _, hs, h, _ => by
      have : s = r := (Option.some.inj hs).symm
      subst this; exact h
  | it :: rest, r, s, hwf, hs, h, hno => by
      rw [applyDelta_cons] at hs
      cases happ : applyItem r it with
      | none => rw [happ] at hs; cases hs
      | some t =>
          rw [happ] at hs
          exact uncollapse_only_by_mention_delta rest t s
            (Ignition.applyItem_wf hwf happ) hs
            (uncollapse_only_by_mention r hwf it t happ h (hno it List.mem_cons_self))
            (fun it' hm => hno it' (List.mem_cons_of_mem _ hm))

/-! Extension is not monotone in the other direction either: a pair that
is separated can be collapsed again by a later admission.  So neither
`collapsed` nor `separable` is preserved along extension in general. -/

/-- `U0` with the uniform rule on its unary form. -/
def U0rule : Regime := ⟨2, [1], [(0, [0])], [0], [(0, 1)]⟩
/-- `U0` with the second mark. -/
def U0both : Regime := ⟨2, [1], [(0, [0]), (0, [1])], [], [(0, 1)]⟩

/-- Every well-formed context of a one-unary-form regime is `⟨0, [none]⟩`. -/
theorem ctx_unary {r : Regime} (hf : r.forms = [1]) {c : Ctx}
    (hc : wfCtx r c) : c = ⟨0, [none]⟩ := by
  obtain ⟨h1, h2, h3, _⟩ := hc
  rw [hf] at h1 h2
  have h0 : c.form = 0 := by simp at h1; exact h1
  rw [h0] at h2
  cases c with
  | mk form slots =>
    simp only at h0 h2 h3
    subst h0
    match slots, h2, h3 with
    | [x], _, h3 =>
      have : x = none := by simp at h3; exact h3.symm
      subst this; rfl

/-- A regime whose one form carries the uniform rule. -/
def Rall : Regime := ⟨2, [1], [], [0], []⟩
/-- `Rall` with the instance `0 [0]`. -/
def Rall0 : Regime := ⟨2, [1], [(0, [0])], [0], []⟩

/-- **Mentioning is not sufficient.**  A collapsed pair, a newly admitted
instance that mentions datum 0, and the pair is still collapsed (the rule
already derives every plug). -/
theorem mention_not_sufficient :
    collapsed Rall 0 1 ∧ applyItem Rall (.newInst 0 [0]) = some Rall0 ∧
      (0, [0]) ∉ Rall.insts ∧ collapsed Rall0 0 1 := by
  refine ⟨?_, by decide, by decide, ?_⟩ <;>
  · intro c hc; rw [ctx_unary rfl hc]; decide

theorem recollapse_by_rule :
    separable U0 0 1 ∧ applyItem U0 (.newRuleAll 0) = some U0rule ∧
      collapsed U0rule 0 1 := by
  refine ⟨U0_separable, by decide, ?_⟩
  intro c hc
  rw [ctx_unary rfl hc]
  decide

theorem recollapse_by_instance :
    separable U0 0 1 ∧ applyItem U0 (.newInst 0 [1]) = some U0both ∧
      collapsed U0both 0 1 := by
  refine ⟨U0_separable, by decide, ?_⟩
  intro c hc
  rw [ctx_unary rfl hc]
  decide

/-- The rule re-collapse is not a valid response to the target `(0, 1)`:
the target clause of `validResponse` fails, because the rule collapses the
target itself.  The requirement clause plays no part here (this target is
the protected pair); `recollapse_breaks_requirement` is the case where it
does. -/
theorem recollapse_not_validResponse :
    applyDelta U0 [.newRuleAll 0] = some U0rule ∧
      ¬ validResponse U0 0 1 [.newRuleAll 0] := by
  have hd : applyDelta U0 [.newRuleAll 0] = some U0rule := by decide
  refine ⟨hd, ?_⟩
  intro ⟨s, hs, hsep, _⟩
  rw [hd] at hs
  cases hs
  exact separable_not_collapsed hsep recollapse_by_rule.2.2

/-- `U0` after a fresh datum and the mark on datum 1. -/
def U0new : Regime := ⟨3, [1], [(0, [0]), (0, [1])], [], [(0, 1)]⟩

/-- **The requirement clause bites.**  The delta `newDatum, newInst 0 [1]`
separates its target `(1, 2)` but collapses the imposed requirement
`(0, 1)`, so it is not a valid response: erasing a protected distinction is
not authorized by `validResponse`. -/
theorem recollapse_breaks_requirement :
    applyDelta U0 [.newDatum, .newInst 0 [1]] = some U0new ∧ (0, 1) ∈ U0.reqs ∧
      separable U0new 1 2 ∧ collapsed U0new 0 1 ∧
      ¬ validResponse U0 1 2 [.newDatum, .newInst 0 [1]] := by
  have hd : applyDelta U0 [.newDatum, .newInst 0 [1]] = some U0new := by decide
  have hc : collapsed U0new 0 1 := by
    intro c hc; rw [ctx_unary rfl hc]; decide
  refine ⟨hd, by decide, ⟨⟨0, [none]⟩, by decide, by decide⟩, hc, ?_⟩
  intro ⟨s, hs, _, hreq⟩
  rw [hd] at hs
  cases hs
  exact separable_not_collapsed (hreq (0, 1) (by decide)) hc

/-- **Scope of `separable`.**  Its indices are bare naturals, not admitted
data: `U0` admits data `0, 1` only, yet `separable U0 0 99` holds (the mark
on 0 is present, the plug at 99 is absent).  Every theorem in this file is
about the `Basic.lean` notion over all naturals; none restricts to
`d, d' < r.data`.  A claim about internally admitted distinctions must add
that hypothesis. -/
theorem separable_unadmitted : ¬ 99 < U0.data ∧ separable U0 0 99 :=
  ⟨by decide, ⟨⟨0, [none]⟩, by decide, by decide⟩⟩

/-! ## 2. Reading (F): a family of regimes -/

/-- Collapse relative to a family: collapsed in every member.

Scope: the family compares the SAME indices `d, d'` in every member, so it
presupposes that index `d` names one datum across all members.  Nothing in
`Regime` supplies that correspondence; indices are presentation.  Single-regime
collapse is rename-invariant (`Derivation.collapsed_rename`), but `collapsedIn`
is not: see `family_index_dependence`.  A family over regimes with distinct
presentations needs correspondence maps: `collapsedInR`. -/
def collapsedIn (S : List Regime) (d d' : Nat) : Prop :=
  ∀ r ∈ S, collapsed r d d'

/-- Collapse in the extended family is collapse in `r'` and in the old
family. -/
theorem collapsedIn_cons (r' : Regime) (S : List Regime) (d d' : Nat) :
    collapsedIn (r' :: S) d d' ↔ collapsed r' d d' ∧ collapsedIn S d d' :=
  List.forall_mem_cons

theorem uncollapse_family (r' : Regime) (S : List Regime) {d d' : Nat}
    (hs : separable r' d d') : ¬ collapsedIn (r' :: S) d d' :=
  fun h => separable_not_collapsed hs ((collapsedIn_cons r' S d d').mp h).1

/-- Given that the old family collapses the pair, the new family fails to
collapse it exactly when `r'` fails to collapse it. -/
theorem uncollapse_family_iff (r' : Regime) (S : List Regime) {d d' : Nat}
    (hS : collapsedIn S d d') :
    ¬ collapsedIn (r' :: S) d d' ↔ ¬ collapsed r' d d' :=
  ⟨fun h hc => h ((collapsedIn_cons r' S d d').mpr ⟨hc, hS⟩),
   fun h hc => h ((collapsedIn_cons r' S d d').mp hc).1⟩

/-- **A witness from non-collapse.**  The well-formed contexts are enumerated
by `Ignition.ctxList`, so a failure of collapse yields a separating context
by a finite decidable search. -/
theorem separable_of_not_collapsed (r : Regime) {d d' : Nat}
    (h : ¬ collapsed r d d') : separable r d d' := by
  by_cases hx : ∃ c ∈ Ignition.ctxList r,
      ¬ (derivable r (plug c d) ↔ derivable r (plug c d'))
  · obtain ⟨c, hc, hne⟩ := hx
    exact ⟨c, Ignition.mem_ctxList.mp hc, hne⟩
  · refine absurd (fun c hc => ?_) h
    by_cases hi : derivable r (plug c d) ↔ derivable r (plug c d')
    · exact hi
    · exact absurd ⟨c, Ignition.mem_ctxList.mpr hc, hi⟩ hx

/-- **U5 in full.**  Given that the old family collapses the pair, adding
`r'` uncollapses it exactly when `r'` separates it. -/
theorem uncollapse_family_sep_iff (r' : Regime) (S : List Regime) {d d' : Nat}
    (hS : collapsedIn S d d') :
    ¬ collapsedIn (r' :: S) d d' ↔ separable r' d d' :=
  ⟨fun h => separable_of_not_collapsed r' ((uncollapse_family_iff r' S hS).mp h),
   uncollapse_family r' S⟩

/-- Three data, one unary mark on datum 0. -/
def A3 : Regime := ⟨3, [1], [(0, [0])], [], []⟩
/-- The same regime with data 0 and 1 swapped: the mark is on datum 1. -/
def B3 : Regime := ⟨3, [1], [(0, [1])], [], []⟩
/-- The swap of data 0 and 1. -/
def swap01 (n : Nat) : Nat := if n = 0 then 1 else if n = 1 then 0 else n

/-- **Recurrence test for the shared-index presupposition.**  `B3` is `A3`
renamed by `swap01`.  The raw pair `(1, 2)` is collapsed in `A3` and separated
in `B3`, so `collapsedIn [A3, B3] 1 2` fails although the two members are one
regime up to renaming.  Transporting the pair along the renaming, `(0, 2)`,
restores agreement, as `collapsed_rename` requires. -/
theorem family_index_dependence :
    renameRegime swap01 A3 = B3 ∧ collapsed A3 1 2 ∧ separable B3 1 2 ∧
      collapsed B3 (swap01 1) (swap01 2) ∧ ¬ collapsedIn [A3, B3] 1 2 := by
  have hA : collapsed A3 1 2 := by
    intro c hc; rw [ctx_unary rfl hc]; decide
  have hB : separable B3 1 2 := ⟨⟨0, [none]⟩, by decide, by decide⟩
  refine ⟨by decide, hA, hB, ?_, ?_⟩
  · intro c hc; rw [ctx_unary rfl hc]; decide
  · intro h; exact separable_not_collapsed hB (h B3 (by simp))

/-- **Presentation-relative family.**  Each member carries the map that sends
the family's indices to its own presentation. -/
def collapsedInR (S : List (Regime × (Nat → Nat))) (d d' : Nat) : Prop :=
  ∀ p ∈ S, collapsed p.1 (p.2 d) (p.2 d')

theorem collapsedInR_cons (p : Regime × (Nat → Nat))
    (S : List (Regime × (Nat → Nat))) (d d' : Nat) :
    collapsedInR (p :: S) d d' ↔ collapsed p.1 (p.2 d) (p.2 d') ∧ collapsedInR S d d' :=
  List.forall_mem_cons

/-- With its map, the renamed copy no longer breaks the family:
`[(A3, id), (B3, swap01)]` collapses `1, 2`. -/
theorem family_index_repaired : collapsedInR [(A3, id), (B3, swap01)] 1 2 := by
  intro p hp
  simp only [List.mem_cons, List.mem_nil_iff, or_false] at hp
  rcases hp with rfl | rfl <;>
  · intro c hc; rw [ctx_unary rfl hc]; decide

/-- **A renamed copy cannot uncollapse.**  Adding a member's renaming by a
bijection, carried with the composed map, keeps the family's collapse
(`Derivation.collapsed_rename`). -/
theorem collapsedInR_rename_cons {S : List (Regime × (Nat → Nat))} {d d' : Nat}
    (hS : collapsedInR S d d') {r : Regime} {ρ : Nat → Nat} (hm : (r, ρ) ∈ S)
    {n : Nat} (σ : DRen n) (hn : r.data = n) :
    collapsedInR ((renameRegime σ.f r, σ.f ∘ ρ) :: S) d d' :=
  (collapsedInR_cons _ _ d d').mpr
    ⟨(collapsed_rename σ r hn (ρ d) (ρ d')).mpr (hS _ hm), hS⟩

/-! ## 3. The apartness reading (`Apartness.lean`)

`separable r` is a positive apartness in the sense of `Apartness.IsApart`,
and `collapsed r` is exactly its indistinguishability.  Constructive:
cotransitivity and the converse direction use only the decidability of
`derivable` and `wfCtx` already instantiated in `Basic.lean`. -/

theorem separable_isApart (r : Regime) : Apartness.IsApart (separable r) where
  irrefl := fun _ ⟨_, _, hne⟩ => hne Iff.rfl
  symm := fun _ _ ⟨c, hc, hne⟩ => ⟨c, hc, fun h => hne h.symm⟩
  cotrans := by
    intro x y ⟨c, hc, hne⟩ z
    by_cases hxz : derivable r (plug c x) ↔ derivable r (plug c z)
    · exact Or.inr ⟨c, hc, fun hzy => hne (hxz.trans hzy)⟩
    · exact Or.inl ⟨c, hc, hxz⟩

theorem collapsed_iff_indist (r : Regime) (d d' : Nat) :
    collapsed r d d' ↔ Apartness.Indist (separable r) d d' := by
  constructor
  · exact fun h hs => separable_not_collapsed hs h
  · intro h c hc
    by_cases hi : derivable r (plug c d) ↔ derivable r (plug c d')
    · exact hi
    · exact absurd ⟨c, hc, hi⟩ h

/-- `collapsed r` is an equivalence, obtained here by transport through
`collapsed_iff_indist` from `Apartness.indist_equivalence`.  This is a
consistency check between the two notions, not the cheapest proof: collapse
is an equivalence directly, context by context, by `Iff.refl`, `Iff.symm`
and `Iff.trans` (`Derivation.collapsed_symm`, `Ignition.collapsed_trans`),
without cotransitivity. -/
theorem collapsed_equivalence (r : Regime) : Equivalence (collapsed r) := by
  obtain ⟨hr, hs, ht⟩ := Apartness.indist_equivalence (separable_isApart r)
  have e := collapsed_iff_indist r
  exact ⟨fun x => (e x x).mpr (hr x),
    fun h => (e _ _).mpr (hs _ _ ((e _ _).mp h)),
    fun h1 h2 => (e _ _).mpr (ht _ _ _ ((e _ _).mp h1) ((e _ _).mp h2))⟩

/-- The family apartness: separated by some member.  A union of
apartnesses is an apartness, and its indistinguishability is `collapsedIn`. -/
def familyApart (S : List Regime) (d d' : Nat) : Prop :=
  ∃ r ∈ S, separable r d d'

theorem familyApart_isApart (S : List Regime) :
    Apartness.IsApart (familyApart S) where
  irrefl := fun x ⟨r, _, hs⟩ => (separable_isApart r).irrefl x hs
  symm := fun x y ⟨r, hr, hs⟩ => ⟨r, hr, (separable_isApart r).symm x y hs⟩
  cotrans := fun x y ⟨r, hr, hs⟩ z =>
    ((separable_isApart r).cotrans x y hs z).elim
      (fun h => Or.inl ⟨r, hr, h⟩) (fun h => Or.inr ⟨r, hr, h⟩)

theorem collapsedIn_iff_indist (S : List Regime) (d d' : Nat) :
    collapsedIn S d d' ↔ Apartness.Indist (familyApart S) d d' :=
  ⟨fun h ⟨r, hr, hs⟩ => separable_not_collapsed hs (h r hr),
   fun h r hr => (collapsed_iff_indist r d d').mpr fun hs => h ⟨r, hr, hs⟩⟩

end ResearchUncollapse
