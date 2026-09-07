import Derivation.Erasure
import Derivation.Inertia
import Derivation.Progress
import Derivation.Rounds
import Derivation.TraceAlgebra

/-!
Finite reuse over the existing admission and response definitions.
The response relation quantifies over all valid responses. Candidate
enumeration, minimisation, orbit selection and resource counters are not
formalized by this module. A Python engine refinement is not claimed.
AuthorityEffect: None.
-/

namespace LocalReuse

open Derivation

theorem replayE_suffix (pre suffix : List Event) (base : Regime) :
    replayE (pre ++ suffix) base =
      (replayE pre base).bind (fun cut => replayE suffix cut) := by
  induction pre generalizing base with
  | nil => rfl
  | cons event rest ih =>
      simp only [List.cons_append, replayE_cons]
      cases stepE base event <;> simp [ih]

theorem replayT_suffix (pre suffix : List TEvent) (base : TRegime) :
    replayT (pre ++ suffix) base =
      (replayT pre base).bind (fun cut => replayT suffix cut) := by
  induction pre generalizing base with
  | nil => rfl
  | cons event rest ih =>
      simp only [List.cons_append, replayT_cons]
      cases stepT base event <;> simp [ih]

theorem replayE_restart {pre suffix : List Event} {base cut : Regime}
    (hcut : replayE pre base = some cut) :
    replayE (pre ++ suffix) base = replayE suffix cut := by
  rw [replayE_suffix, hcut]
  rfl

theorem replayT_restart {pre suffix : List TEvent} {base cut : TRegime}
    (hcut : replayT pre base = some cut) :
    replayT (pre ++ suffix) base = replayT suffix cut := by
  rw [replayT_suffix, hcut]
  rfl

def itemEvent : Item → Event
  | .newDatum => .admitDatum
  | .newForm arity => .admitForm arity
  | .newInst form args => .admitInst form args
  | .newRuleAll form => .admitRuleAll form

theorem stepE_itemEvent (state : Regime) (item : Item) :
    stepE state (itemEvent item) = applyItem state item := by
  cases item <;> rfl

theorem delta_replays (state : Regime) (delta : List Item) :
    replayE (delta.map itemEvent) state = applyDelta state delta := by
  induction delta generalizing state with
  | nil => rfl
  | cons item rest ih =>
      rw [List.map_cons, replayE_cons, stepE_itemEvent, applyDelta_cons]
      cases applyItem state item <;> simp [ih]

def roundEvents (round : Round) : List Event :=
  .impose round.target.1 round.target.2 :: round.response.map itemEvent

theorem round_replays (state : Regime) (round : Round) :
    replayE (roundEvents round) state =
      respond state round.target.1 round.target.2 round.response := by
  unfold roundEvents
  rw [replayE_cons]
  unfold respond
  cases stepE state (.impose round.target.1 round.target.2) <;> simp [delta_replays]

inductive ResponsePath : Regime → List Round → Regime → Prop where
  | nil (state : Regime) : ResponsePath state [] state
  | cons {state next finish : Regime} {round : Round} {rest : List Round} :
      TransStep state round.target.1 round.target.2 round.response next →
      ResponsePath next rest finish → ResponsePath state (round :: rest) finish

theorem responsePath_append {start cut finish : Regime} {pre suffix : List Round}
    (hp : ResponsePath start pre cut) (hs : ResponsePath cut suffix finish) :
    ResponsePath start (pre ++ suffix) finish := by
  induction hp with
  | nil => exact hs
  | cons step path ih => exact ResponsePath.cons step (ih hs)

theorem responsePath_split {start finish : Regime} (pre suffix : List Round)
    (h : ResponsePath start (pre ++ suffix) finish) :
    ∃ cut, ResponsePath start pre cut ∧ ResponsePath cut suffix finish := by
  induction pre generalizing start with
  | nil => exact ⟨start, ResponsePath.nil start, h⟩
  | cons round rest ih =>
      cases h with
      | cons step path =>
          obtain ⟨cut, hp, hs⟩ := ih path
          exact ⟨cut, ResponsePath.cons step hp, hs⟩

theorem responsePath_append_iff {start finish : Regime} (pre suffix : List Round) :
    ResponsePath start (pre ++ suffix) finish ↔
      ∃ cut, ResponsePath start pre cut ∧ ResponsePath cut suffix finish := by
  constructor
  · exact responsePath_split pre suffix
  · rintro ⟨cut, hp, hs⟩
    exact responsePath_append hp hs

def pathEvents (rounds : List Round) : List Event := rounds.flatMap roundEvents

theorem responsePath_replays {start finish : Regime} {rounds : List Round}
    (h : ResponsePath start rounds finish) :
    replayE (pathEvents rounds) start = some finish := by
  induction h with
  | nil => rfl
  | @cons state next finish round rest hstep hpath ih =>
      change replayE (roundEvents round ++ pathEvents rest) state = some finish
      rw [replayE_suffix, round_replays, hstep.2.2.2.2]
      exact ih

theorem responsePath_cut_unique {start cut first : Regime} {pre : List Round}
    (hcut : ResponsePath start pre cut) (hfirst : ResponsePath start pre first) :
    cut = first := by
  have h := (responsePath_replays hcut).symm.trans (responsePath_replays hfirst)
  exact Option.some.inj h

/-- Each branch retains the same entire cut regime, including its requirements. -/
theorem finite_response_fan {start cut : Regime} {pre : List Round}
    (hp : ResponsePath start pre cut)
    (branches : List (List Round × Regime))
    (hs : ∀ branch ∈ branches, ResponsePath cut branch.1 branch.2) :
    ∀ branch ∈ branches,
      ResponsePath start (pre ++ branch.1) branch.2 ∧
      replayE (pathEvents (pre ++ branch.1)) start = some branch.2 := by
  intro branch hb
  have hpath := responsePath_append hp (hs branch hb)
  exact ⟨hpath, responsePath_replays hpath⟩

theorem supplied_target_has_response (state : Regime) (hwf : state.wf)
    (i j : Nat) (hi : i < state.data) (hj : j < state.data) (hne : i ≠ j)
    (hold : ∀ requirement ∈ state.reqs,
      separable state requirement.1 requirement.2) :
    validResponse state i j [.newForm 1, .newInst state.forms.length [j]] :=
  mark_progress state hwf i j hi hj hne hold

theorem stepE_retains_instance {state next : Regime} {event : Event} {inst : Inst}
    (hstep : stepE state event = some next) (hinst : inst ∈ state.insts) :
    inst ∈ next.insts := by
  cases event with
  | supply token => simp [stepE] at hstep; cases hstep; exact hinst
  | admitDatum => simp [stepE] at hstep; cases hstep; exact hinst
  | admitForm arity =>
      simp only [stepE] at hstep
      split at hstep
      · cases Option.some.inj hstep; exact hinst
      · cases hstep
  | admitInst form args =>
      simp only [stepE] at hstep
      split at hstep
      · cases Option.some.inj hstep
        exact mem_insertNew.mpr (Or.inl hinst)
      · cases hstep
  | admitRuleAll form =>
      simp only [stepE] at hstep
      split at hstep
      · cases Option.some.inj hstep; exact hinst
      · cases hstep
  | impose i j =>
      simp only [stepE] at hstep
      split at hstep
      · cases Option.some.inj hstep; exact hinst
      · cases hstep

theorem replayE_retains_instance {history : List Event} {state finish : Regime}
    {inst : Inst} (hreplay : replayE history state = some finish)
    (hinst : inst ∈ state.insts) : inst ∈ finish.insts := by
  induction history generalizing state with
  | nil => cases Option.some.inj hreplay; exact hinst
  | cons event rest ih =>
      rw [replayE_cons] at hreplay
      cases hstep : stepE state event with
      | none => simp [hstep] at hreplay
      | some next =>
          simp only [hstep, Option.bind_some] at hreplay
          exact ih hreplay (stepE_retains_instance hstep hinst)

def markedLeft : Regime := ⟨2, [1], [(0, [0])], [], []⟩
def markedRight : Regime := ⟨2, [1], [(0, [1])], [], []⟩

theorem markedLeft_wf : markedLeft.wf := by simp [Regime.wf, markedLeft]

theorem markedRight_wf : markedRight.wf := by simp [Regime.wf, markedRight]

theorem no_admission_reversal :
    ¬ ∃ history : List Event, replayE history markedLeft = some markedRight := by
  rintro ⟨history, hreplay⟩
  have h := replayE_retains_instance (inst := (0, [0])) hreplay (by decide)
  have hn : (0, [0]) ∉ markedRight.insts := by decide
  exact hn h

theorem markedRight_separates : separable markedRight 0 1 := by
  refine ⟨⟨0, [none]⟩, ?_, ?_⟩ <;> decide

theorem difference_can_have_no_response_step :
    (0 ≠ 1 ∧ 1 < markedRight.data ∧ separable markedRight 0 1) ∧
      ∀ i j delta next, ¬ TransStep markedRight i j delta next := by
  refine ⟨⟨by decide, by decide, markedRight_separates⟩, ?_⟩
  intro i j delta next h
  have hi := h.1
  have hj := h.2.1
  change j < 2 at hj
  have heqi : i = 0 := by omega
  have heqj : j = 1 := by omega
  subst i; subst j
  exact separable_not_collapsed markedRight_separates h.2.2.1

theorem no_positive_path_from_markedRight (round : Round) (rest : List Round)
    (finish : Regime) : ¬ ResponsePath markedRight (round :: rest) finish := by
  intro h
  cases h with
  | cons step path => exact difference_can_have_no_response_step.2 _ _ _ _ step

theorem fixed_carrier_round_bound {start finish : Regime} {rounds : List Round}
    (h : ClosedRun start rounds finish) (hn : start.reqs.Nodup)
    (hwf : ∀ requirement ∈ start.reqs,
      requirement.1 < requirement.2 ∧ requirement.2 < start.data) :
    2 * (start.reqs.length + rounds.length) ≤ start.data * (start.data - 1) :=
  closedRun_round_bound h hn hwf

theorem no_seven_closed_rounds_on_two_data {start finish : Regime}
    {rounds : List Round} (hdata : start.data = 2) (hreqs : start.reqs = [])
    (hrounds : rounds.length = 7) : ¬ ClosedRun start rounds finish := by
  intro h
  have hb := closedRun_round_bound_from_empty h hreqs
  rw [hdata, hrounds] at hb
  omega

/-- The same response paths, with the well-formed source context recorded
at each round. This annotation supplies transport hypotheses explicitly. -/
inductive ContextPath : Regime → List Round → Regime → Prop where
  | nil (state : Regime) : ContextPath state [] state
  | cons {state next finish : Regime} {round : Round} {rest : List Round} :
      state.wf →
      TransStep state round.target.1 round.target.2 round.response next →
      ContextPath next rest finish → ContextPath state (round :: rest) finish

theorem contextPath_is_responsePath {start finish : Regime} {rounds : List Round}
    (h : ContextPath start rounds finish) : ResponsePath start rounds finish := by
  induction h with
  | nil => exact ResponsePath.nil _
  | cons hwf hstep hpath ih => exact ResponsePath.cons hstep ih

def mapRound (rename : Nat → Nat) (round : Round) : Round :=
  ⟨mapReq rename round.target, round.response.map (mapItem rename)⟩

theorem padF_absorb (rename : Nat → Nat) {n m : Nat} (hnm : n ≤ m) :
    padF m (padF n rename) = padF n rename := by
  funext x
  by_cases hxm : x < m
  · rw [padF_lt _ hxm]
  · have hxn : ¬ x < n := by omega
    rw [padF_ge _ hxm, padF_ge _ hxn]

/-- The initial renaming fixes every later fresh datum index. All instance
arguments and the entire requirement store are transported at every cut. -/
theorem contextPath_transport {n : Nat} (rename : DRen n)
    {start finish : Regime} {rounds : List Round}
    (h : ContextPath start rounds finish) (hn : n ≤ start.data) :
    ResponsePath (renameRegimeR (padF n rename.f) start)
      (rounds.map (mapRound (padF n rename.f)))
      (renameRegimeR (padF n rename.f) finish) := by
  induction h with
  | nil => exact ResponsePath.nil _
  | @cons state next finish round rest hwf hstep hpath ih =>
      have hdata : state.data ≤ next.data := by
        have ha := (respond_anatomy hstep.2.2.2.2).2.2.2
        have hm := applyDelta_data_mono ha
        exact hm
      have hnext := ih (Nat.le_trans hn hdata)
      have mapped := transStep_rename_fwd (rename.pad state.data hn) state rfl
        (fun inst hi => (hwf.1 inst hi).2.2) hwf.2.2.1 hstep
      have heq := padF_absorb rename.f hn
      change TransStep (renameRegimeR (padF n rename.f) state)
        (mapReq (padF n rename.f) round.target).1
        (mapReq (padF n rename.f) round.target).2
        (round.response.map (mapItem (padF state.data (padF n rename.f))))
        (renameRegimeR (padF state.data (padF n rename.f)) next) at mapped
      rw [heq] at mapped
      exact ResponsePath.cons mapped hnext

theorem contextPath_transport_length (rename : Nat → Nat) (rounds : List Round) :
    (rounds.map (mapRound rename)).length = rounds.length := by simp

/-- A finite family of passage traces shares its entire replayed context,
including the observation, licensing, budget, refusal and terminal fields. -/
theorem passage_finite_fan (start : PrimitivePassage.PState)
    (pre : List PrimitivePassage.PEvent)
    (branches : List (List PrimitivePassage.PEvent)) :
    branches.map (fun suffix => PrimitivePassage.replayP (pre ++ suffix) start) =
      branches.map (fun suffix =>
        PrimitivePassage.replayP suffix (PrimitivePassage.replayP pre start)) := by
  simp only [PrimitivePassage.replay_append]

/-- A certified rewrite of an interior trace preserves its endpoint after
every surrounding trace. The premise names the existing rewrite calculus. -/
theorem passage_rewrite_at_cut (start : PrimitivePassage.PState)
    (pre left right post : List PrimitivePassage.PEvent)
    (h : TraceAlgebra.RwStar left right) :
    PrimitivePassage.replayP (pre ++ left ++ post) start =
      PrimitivePassage.replayP (pre ++ right ++ post) start := by
  simp only [PrimitivePassage.replay_append]
  rw [TraceAlgebra.rwStar_sound left right h]

/-- Reusing the same passage context cannot clear its recorded terminal. -/
theorem passage_halted_cut (start : PrimitivePassage.PState)
    (pre suffix : List PrimitivePassage.PEvent)
    (h : (PrimitivePassage.replayP pre start).halted = true) :
    PrimitivePassage.replayP (pre ++ suffix) start =
      PrimitivePassage.replayP pre start := by
  rw [PrimitivePassage.replay_append]
  exact TraceAlgebra.replayP_halted suffix (PrimitivePassage.replayP pre start) h

end LocalReuse

#print axioms LocalReuse.replayE_suffix
#print axioms LocalReuse.replayT_suffix
#print axioms LocalReuse.replayE_restart
#print axioms LocalReuse.replayT_restart
#print axioms LocalReuse.stepE_itemEvent
#print axioms LocalReuse.delta_replays
#print axioms LocalReuse.round_replays
#print axioms LocalReuse.responsePath_append
#print axioms LocalReuse.responsePath_split
#print axioms LocalReuse.responsePath_append_iff
#print axioms LocalReuse.responsePath_replays
#print axioms LocalReuse.responsePath_cut_unique
#print axioms LocalReuse.finite_response_fan
#print axioms LocalReuse.supplied_target_has_response
#print axioms LocalReuse.stepE_retains_instance
#print axioms LocalReuse.replayE_retains_instance
#print axioms LocalReuse.markedLeft_wf
#print axioms LocalReuse.markedRight_wf
#print axioms LocalReuse.no_admission_reversal
#print axioms LocalReuse.markedRight_separates
#print axioms LocalReuse.difference_can_have_no_response_step
#print axioms LocalReuse.no_positive_path_from_markedRight
#print axioms LocalReuse.fixed_carrier_round_bound
#print axioms LocalReuse.no_seven_closed_rounds_on_two_data
#print axioms LocalReuse.contextPath_is_responsePath
#print axioms LocalReuse.padF_absorb
#print axioms LocalReuse.contextPath_transport
#print axioms LocalReuse.contextPath_transport_length
#print axioms LocalReuse.passage_finite_fan
#print axioms LocalReuse.passage_rewrite_at_cut
#print axioms LocalReuse.passage_halted_cut
