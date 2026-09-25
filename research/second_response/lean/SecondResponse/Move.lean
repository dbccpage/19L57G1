import SecondResponse.Kernel
import SecondResponse.ExhaustStep

/-!
# Which events move a pair, and which pairs one history can move

Native to rung ten, apart from the restatement named below.

A pair of data is MOVED by an event, or by a history, when it is
separable on one side and collapsed on the other.  Nothing here is about
a minimum, a cost or a tie: the sealed augmentation and response
machinery is not reconstructed, and every statement is about events and
histories of events, whatever responder chose them.

* `mem_plug_of_hole`: the datum plugged into a context with a hole is an
  argument of the plugging.
* `derivable_inst_unmentioned`, `separable_inst_unmentioned`,
  `collapsed_inst_unmentioned`: an accepted instance admission whose
  arguments mention neither datum of a pair leaves the pair's
  separability and collapse as they were, with no hypothesis.
* `slots_ok_of_plug_mem`, `collapsed_step_keep`: on a well-formed regime,
  every accepted event other than an instance admission keeps every
  collapsed pair collapsed.  Well-formedness is used for the datum and
  form admissions: a context reading the new datum or the new form holds
  no admitted instance.
* `step_wf`: every accepted event keeps a regime well formed (rung
  three's `wf_step_any`, restated and proved again here).
* `separation_needs_mention`: for a well-formed base and every history
  the sealed replay accepts from it, a pair collapsed before and
  separable after is mentioned by the arguments of some instance
  admission of the history.
* `collapse_needs_mention_or_rule`: a pair separable before and collapsed
  after is so mentioned, or the history holds a rule admission; with no
  hypothesis on the base.
* `moved_pairs_meet_mentions`, `separation_needs_inst`: the two
  corollaries for a history holding no rule admission, and for a
  separation.
* `one_inst_moves_two_pairs`, `response_collapses_a_pair`: one instance
  admission, on an exhibited well-formed regime, moves two pairs apart;
  and on another, moves one pair apart and a separable pair together.

AuthorityEffect: None.
-/

namespace SecondResponse
namespace Move

open Sealed
open ExhaustStep (getD_append_lt ctx_step_keep separable_step_keep)

/-- The datum plugged into a context with a hole is an argument of the
plugging. -/
theorem mem_plug_of_hole {c : Ctx} (h : none ∈ c.slots) (d : Nat) :
    d ∈ (plug c d).2 :=
  List.mem_map.mpr ⟨none, h, rfl⟩

/-- Adding an instance that does not mention the plugged datum leaves
derivability of the plugging as it was. -/
theorem derivable_inst_unmentioned {r : Regime} {c : Ctx} {f : Nat}
    {args : List Nat} {d : Nat} (hh : none ∈ c.slots) (hd : d ∉ args) :
    derivable { r with insts := insertNew r.insts (f, args) } (plug c d) ↔
      derivable r (plug c d) := by
  show (plug c d ∈ insertNew r.insts (f, args) ∨ (plug c d).1 ∈ r.rules) ↔
    (plug c d ∈ r.insts ∨ (plug c d).1 ∈ r.rules)
  rw [mem_insertNew]
  constructor
  · intro hx
    rcases hx with (hx | hx) | hx
    · exact Or.inl hx
    · have hm := mem_plug_of_hole hh d
      rw [hx] at hm
      exact absurd hm hd
    · exact Or.inr hx
  · intro hx
    rcases hx with hx | hx
    · exact Or.inl (Or.inl hx)
    · exact Or.inr hx

/-- An accepted instance admission mentioning neither datum of a pair
leaves the pair's separability as it was. -/
theorem separable_inst_unmentioned {r r' : Regime} {f : Nat} {args : List Nat}
    {d d' : Nat} (h : stepE r (.admitInst f args) = some r') (hd : d ∉ args)
    (hd' : d' ∉ args) : separable r' d d' ↔ separable r d d' := by
  simp only [stepE] at h
  split at h
  · cases Option.some.inj h
    constructor
    · intro ⟨c, hc, hne⟩
      refine ⟨c, hc, ?_⟩
      rw [← derivable_inst_unmentioned hc.2.2.1 hd,
        ← derivable_inst_unmentioned hc.2.2.1 hd']
      exact hne
    · intro ⟨c, hc, hne⟩
      refine ⟨c, hc, ?_⟩
      rw [derivable_inst_unmentioned hc.2.2.1 hd,
        derivable_inst_unmentioned hc.2.2.1 hd']
      exact hne
  · cases h

/-- An accepted instance admission mentioning neither datum of a pair
leaves the pair's collapse as it was. -/
theorem collapsed_inst_unmentioned {r r' : Regime} {f : Nat} {args : List Nat}
    {d d' : Nat} (h : stepE r (.admitInst f args) = some r') (hd : d ∉ args)
    (hd' : d' ∉ args) : collapsed r' d d' ↔ collapsed r d d' := by
  simp only [stepE] at h
  split at h
  · cases Option.some.inj h
    constructor
    · intro hc c hwc
      have e := hc c hwc
      rw [derivable_inst_unmentioned hwc.2.2.1 hd,
        derivable_inst_unmentioned hwc.2.2.1 hd'] at e
      exact e
    · intro hc c hwc
      rw [derivable_inst_unmentioned hwc.2.2.1 hd,
        derivable_inst_unmentioned hwc.2.2.1 hd']
      exact hc c hwc
  · cases h

/-- On a well-formed regime, a context whose plugging is a held instance
names only admitted data in its filled slots. -/
theorem slots_ok_of_plug_mem {r : Regime} (hwf : r.wf) {c : Ctx} {d : Nat}
    (h : plug c d ∈ r.insts) : ∀ s ∈ c.slots, slotOk r.data s := by
  intro s hs
  cases s with
  | none => trivial
  | some x =>
    have hx : x ∈ (plug c d).2 := List.mem_map.mpr ⟨some x, hs, rfl⟩
    exact (hwf.1 _ h).2.2 x hx

/-- On a well-formed regime, every accepted event other than an instance
admission keeps every collapsed pair collapsed. -/
theorem collapsed_step_keep {r r' : Regime} {e : Event} {d d' : Nat}
    (hwf : r.wf) (hi : ∀ f args, e ≠ .admitInst f args)
    (h : stepE r e = some r') (hc : collapsed r d d') : collapsed r' d d' := by
  cases e with
  | supply t =>
    cases Option.some.inj h
    exact hc
  | admitDatum =>
    cases Option.some.inj h
    intro c hwc
    obtain ⟨hf, hlen, hhole, _⟩ := hwc
    show (plug c d ∈ r.insts ∨ (plug c d).1 ∈ r.rules) ↔
      (plug c d' ∈ r.insts ∨ (plug c d').1 ∈ r.rules)
    by_cases h1 : plug c d ∈ r.insts
    · exact hc c ⟨hf, hlen, hhole, slots_ok_of_plug_mem hwf h1⟩
    · by_cases h2 : plug c d' ∈ r.insts
      · exact hc c ⟨hf, hlen, hhole, slots_ok_of_plug_mem hwf h2⟩
      · constructor
        · intro hx
          rcases hx with hx | hx
          · exact absurd hx h1
          · exact Or.inr hx
        · intro hx
          rcases hx with hx | hx
          · exact absurd hx h2
          · exact Or.inr hx
  | admitForm a =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      intro c hwc
      obtain ⟨hf, hlen, hhole, hslots⟩ := hwc
      by_cases hcl : c.form < r.forms.length
      · have hlen' : c.slots.length = r.forms.getD c.form 0 :=
          hlen.trans (getD_append_lt r.forms a hcl)
        exact hc c ⟨hcl, hlen', hhole, hslots⟩
      · have hnot : ∀ x, ¬ derivable r (plug c x) := by
          intro x hx
          cases hx with
          | inl hx => exact hcl (hwf.1 _ hx).1
          | inr hx => exact hcl (hwf.2.1 _ hx)
        exact iff_of_false (hnot d) (hnot d')
    · cases h
  | admitInst f args => exact absurd rfl (hi f args)
  | admitRuleAll g =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      intro c hwc
      by_cases hg : c.form = g
      · have hm : c.form ∈ insertNew r.rules g := mem_insertNew.mpr (Or.inr hg)
        exact iff_of_true (Or.inr hm) (Or.inr hm)
      · have key : ∀ y, derivable { r with rules := insertNew r.rules g } (plug c y) ↔
            derivable r (plug c y) := by
          intro y
          show (plug c y ∈ r.insts ∨ c.form ∈ insertNew r.rules g) ↔
            (plug c y ∈ r.insts ∨ c.form ∈ r.rules)
          rw [mem_insertNew]
          constructor
          · intro hy
            rcases hy with hy | hy | hy
            · exact Or.inl hy
            · exact Or.inr hy
            · exact absurd hy hg
          · intro hy
            rcases hy with hy | hy
            · exact Or.inl hy
            · exact Or.inr (Or.inl hy)
        rw [key, key]
        exact hc c hwc
    · cases h
  | impose i j =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      exact hc
    · cases h

/-- Every accepted event keeps a regime well formed (rung three's
`wf_step_any`, restated). -/
theorem step_wf {r r' : Regime} {e : Event} (hwf : r.wf)
    (h : stepE r e = some r') : r'.wf := by
  obtain ⟨hi, hr, hq, hf⟩ := hwf
  cases e with
  | supply t =>
    cases Option.some.inj h
    exact ⟨hi, hr, hq, hf⟩
  | admitDatum =>
    cases Option.some.inj h
    refine ⟨?_, hr, ?_, hf⟩
    · intro p hp
      obtain ⟨h1, h2, h3⟩ := hi p hp
      exact ⟨h1, h2, fun a ha => Nat.lt_succ_of_lt (h3 a ha)⟩
    · intro q hq'
      exact ⟨(hq q hq').1, Nat.lt_succ_of_lt (hq q hq').2⟩
  | admitForm a =>
    simp only [stepE] at h
    split at h
    · rename_i ha
      cases Option.some.inj h
      refine ⟨?_, ?_, hq, ?_⟩
      · intro p hp
        obtain ⟨h1, h2, h3⟩ := hi p hp
        refine ⟨?_, ?_, h3⟩
        · show p.1 < (r.forms ++ [a]).length
          rw [List.length_append]
          exact Nat.lt_succ_of_lt h1
        · show p.2.length = (r.forms ++ [a]).getD p.1 0
          rw [getD_append_lt r.forms a h1]
          exact h2
      · intro g hg
        show g < (r.forms ++ [a]).length
        rw [List.length_append]
        exact Nat.lt_succ_of_lt (hr g hg)
      · intro b hb
        rcases List.mem_append.mp hb with hb | hb
        · exact hf b hb
        · rw [List.mem_singleton.mp hb]
          exact ha
    · cases h
  | admitInst g args =>
    simp only [stepE] at h
    split at h
    · rename_i hg
      cases Option.some.inj h
      refine ⟨?_, hr, hq, hf⟩
      intro p hp
      rcases mem_insertNew.mp hp with hp | hp
      · exact hi p hp
      · rw [hp]
        exact hg
    · cases h
  | admitRuleAll g =>
    simp only [stepE] at h
    split at h
    · rename_i hg
      cases Option.some.inj h
      refine ⟨hi, ?_, hq, hf⟩
      intro x hx
      rcases mem_insertNew.mp hx with hx | hx
      · exact hr x hx
      · rw [hx]
        exact hg
    · cases h
  | impose i j =>
    simp only [stepE] at h
    split at h
    · rename_i hij
      cases Option.some.inj h
      refine ⟨hi, hr, ?_, hf⟩
      intro q hq'
      rcases mem_insertNew.mp hq' with hq' | hq'
      · exact hq q hq'
      · rw [hq']
        exact hij
    · cases h

/-- For a well-formed base and every history the sealed replay accepts
from it, a pair collapsed before and separable after is mentioned by the
arguments of some instance admission of the history. -/
theorem separation_needs_mention :
    ∀ (h : List Event) {r r' : Regime} {d d' : Nat}, r.wf →
      replayE h r = some r' → collapsed r d d' → separable r' d d' →
      ∃ f args, Event.admitInst f args ∈ h ∧ (d ∈ args ∨ d' ∈ args)
  | [], r, r', d, d', _, hrep, hc, hs => by
    cases Option.some.inj hrep
    exact absurd hc (separable_not_collapsed hs)
  | e :: t, r, r', d, d', hwf, hrep, hc, hs => by
    obtain ⟨r1, h1, ht⟩ : ∃ r1, stepE r e = some r1 ∧ replayE t r1 = some r' := by
      unfold replayE at hrep
      simp only [List.foldlM] at hrep
      cases hs1 : stepE r e with
      | none => rw [hs1] at hrep; cases hrep
      | some r1 =>
        rw [hs1] at hrep
        exact ⟨r1, rfl, hrep⟩
    have hwf1 := step_wf hwf h1
    have lift : (∃ f args, Event.admitInst f args ∈ t ∧ (d ∈ args ∨ d' ∈ args)) →
        ∃ f args, Event.admitInst f args ∈ e :: t ∧ (d ∈ args ∨ d' ∈ args) := by
      intro ⟨f, args, hm, hd⟩
      exact ⟨f, args, List.mem_cons_of_mem _ hm, hd⟩
    cases e with
    | admitInst f args =>
      by_cases hm : d ∈ args ∨ d' ∈ args
      · exact ⟨f, args, List.mem_cons_self, hm⟩
      · have hd : d ∉ args := fun x => hm (Or.inl x)
        have hd' : d' ∉ args := fun x => hm (Or.inr x)
        have hc1 := (collapsed_inst_unmentioned h1 hd hd').mpr hc
        exact lift (separation_needs_mention t hwf1 ht hc1 hs)
    | supply x =>
      exact lift (separation_needs_mention t hwf1 ht
        (collapsed_step_keep hwf (fun _ _ h => by cases h) h1 hc) hs)
    | admitDatum =>
      exact lift (separation_needs_mention t hwf1 ht
        (collapsed_step_keep hwf (fun _ _ h => by cases h) h1 hc) hs)
    | admitForm a =>
      exact lift (separation_needs_mention t hwf1 ht
        (collapsed_step_keep hwf (fun _ _ h => by cases h) h1 hc) hs)
    | admitRuleAll g =>
      exact lift (separation_needs_mention t hwf1 ht
        (collapsed_step_keep hwf (fun _ _ h => by cases h) h1 hc) hs)
    | impose i j =>
      exact lift (separation_needs_mention t hwf1 ht
        (collapsed_step_keep hwf (fun _ _ h => by cases h) h1 hc) hs)

/-- For every base and every history the sealed replay accepts from it, a
pair separable before and collapsed after is mentioned by the arguments
of some instance admission of the history, or the history holds a rule
admission. -/
theorem collapse_needs_mention_or_rule :
    ∀ (h : List Event) {r r' : Regime} {d d' : Nat},
      replayE h r = some r' → separable r d d' → collapsed r' d d' →
      (∃ f args, Event.admitInst f args ∈ h ∧ (d ∈ args ∨ d' ∈ args)) ∨
        ∃ g, Event.admitRuleAll g ∈ h
  | [], r, r', d, d', hrep, hs, hc => by
    cases Option.some.inj hrep
    exact absurd hc (separable_not_collapsed hs)
  | e :: t, r, r', d, d', hrep, hs, hc => by
    obtain ⟨r1, h1, ht⟩ : ∃ r1, stepE r e = some r1 ∧ replayE t r1 = some r' := by
      unfold replayE at hrep
      simp only [List.foldlM] at hrep
      cases hs1 : stepE r e with
      | none => rw [hs1] at hrep; cases hrep
      | some r1 =>
        rw [hs1] at hrep
        exact ⟨r1, rfl, hrep⟩
    have lift : ((∃ f args, Event.admitInst f args ∈ t ∧ (d ∈ args ∨ d' ∈ args)) ∨
          ∃ g, Event.admitRuleAll g ∈ t) →
        (∃ f args, Event.admitInst f args ∈ e :: t ∧ (d ∈ args ∨ d' ∈ args)) ∨
          ∃ g, Event.admitRuleAll g ∈ e :: t := by
      intro hx
      rcases hx with ⟨f, args, hm, hd⟩ | ⟨g, hg⟩
      · exact Or.inl ⟨f, args, List.mem_cons_of_mem _ hm, hd⟩
      · exact Or.inr ⟨g, List.mem_cons_of_mem _ hg⟩
    have keep : (∀ f args, e ≠ .admitInst f args) → (∀ g, e ≠ .admitRuleAll g) →
        separable r1 d d' := fun hi hr => separable_step_keep hi hr h1 hs
    cases e with
    | admitInst f args =>
      by_cases hm : d ∈ args ∨ d' ∈ args
      · exact Or.inl ⟨f, args, List.mem_cons_self, hm⟩
      · have hd : d ∉ args := fun x => hm (Or.inl x)
        have hd' : d' ∉ args := fun x => hm (Or.inr x)
        have hs1 := (separable_inst_unmentioned h1 hd hd').mpr hs
        exact lift (collapse_needs_mention_or_rule t ht hs1 hc)
    | admitRuleAll g => exact Or.inr ⟨g, List.mem_cons_self⟩
    | supply x =>
      exact lift (collapse_needs_mention_or_rule t ht
        (keep (fun _ _ h => by cases h) (fun _ h => by cases h)) hc)
    | admitDatum =>
      exact lift (collapse_needs_mention_or_rule t ht
        (keep (fun _ _ h => by cases h) (fun _ h => by cases h)) hc)
    | admitForm a =>
      exact lift (collapse_needs_mention_or_rule t ht
        (keep (fun _ _ h => by cases h) (fun _ h => by cases h)) hc)
    | impose i j =>
      exact lift (collapse_needs_mention_or_rule t ht
        (keep (fun _ _ h => by cases h) (fun _ h => by cases h)) hc)

/-- For a well-formed base and a history holding no rule admission, every
pair the history moves is mentioned by some instance admission of it. -/
theorem moved_pairs_meet_mentions {h : List Event} {r r' : Regime} {d d' : Nat}
    (hwf : r.wf) (hrep : replayE h r = some r') (hr : ∀ g, Event.admitRuleAll g ∉ h)
    (hmove : (collapsed r d d' ∧ separable r' d d') ∨
      (separable r d d' ∧ collapsed r' d d')) :
    ∃ f args, Event.admitInst f args ∈ h ∧ (d ∈ args ∨ d' ∈ args) := by
  rcases hmove with ⟨hc, hs⟩ | ⟨hs, hc⟩
  · exact separation_needs_mention h hwf hrep hc hs
  · rcases collapse_needs_mention_or_rule h hrep hs hc with hx | ⟨g, hg⟩
    · exact hx
    · exact absurd hg (hr g)

/-- For a well-formed base, every history that separates a collapsed
pair holds an instance admission. -/
theorem separation_needs_inst {h : List Event} {r r' : Regime} {d d' : Nat}
    (hwf : r.wf) (hrep : replayE h r = some r') (hc : collapsed r d d')
    (hs : separable r' d d') : ∃ f args, Event.admitInst f args ∈ h := by
  obtain ⟨f, args, hm, _⟩ := separation_needs_mention h hwf hrep hc hs
  exact ⟨f, args, hm⟩

/-- One instance admission, on an exhibited well-formed regime, moves two
collapsed pairs apart at once. -/
theorem one_inst_moves_two_pairs :
    ∃ r r', r.wf ∧ collapsed r 0 1 ∧ collapsed r 0 2 ∧
      stepE r (.admitInst 0 [0]) = some r' ∧ separable r' 0 1 ∧ separable r' 0 2 :=
  ⟨⟨3, [1], [], [], []⟩, ⟨3, [1], [(0, [0])], [], []⟩,
    by unfold Regime.wf; decide,
    collapsed_of_no_insts _ rfl 0 1, collapsed_of_no_insts _ rfl 0 2, by decide,
    ⟨⟨0, [none]⟩, by decide, by decide⟩, ⟨⟨0, [none]⟩, by decide, by decide⟩⟩

/-- One instance admission, on an exhibited well-formed regime, moves a
collapsed pair apart and a separable pair together. -/
theorem response_collapses_a_pair :
    ∃ r r', r.wf ∧ collapsed r 0 1 ∧ separable r 0 2 ∧
      stepE r (.admitInst 0 [0]) = some r' ∧ separable r' 0 1 ∧ collapsed r' 0 2 := by
  -- Every well-formed context of a regime whose only form has arity one
  -- is the one-hole context of that form.
  have only : ∀ (s : Regime), s.forms = [1] → ∀ c, wfCtx s c → c = ⟨0, [none]⟩ := by
    intro s hs c hc
    obtain ⟨form, slots⟩ := c
    obtain ⟨hf, hlen, hhole, _⟩ := hc
    have hf' : form < 1 := by rw [hs] at hf; exact hf
    have hf0 : form = 0 := Nat.eq_zero_of_le_zero (Nat.le_of_lt_succ hf')
    subst hf0
    have hl : slots.length = 1 := by rw [hs] at hlen; exact hlen
    match slots, hl, hhole with
    | [none], _, _ => rfl
    | [some y], _, hhole => simp at hhole
  refine ⟨⟨3, [1], [(0, [2])], [], []⟩, ⟨3, [1], [(0, [2]), (0, [0])], [], []⟩,
    by unfold Regime.wf; decide, ?_, ⟨⟨0, [none]⟩, by decide, by decide⟩, by decide,
    ⟨⟨0, [none]⟩, by decide, by decide⟩, ?_⟩
  · intro c hc
    rw [only _ rfl c hc]
    exact iff_of_false (by decide) (by decide)
  · intro c hc
    rw [only _ rfl c hc]
    exact iff_of_true (by decide) (by decide)

end Move
end SecondResponse
