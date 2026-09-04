import SecondNoFirst.Inert

/-!
# The temporal form: demands along a run

NOT PREDICTED.  This module was written after an adversarial reading of
the package, before it was committed, found that no statement in it
mentioned a run at all: every theorem of stages two and three is about a
single regime, so the word "first" in the headline conjunction was
discharged only by the stage-four rectangle, which reaches sequence length
four.  The reading is recorded in `STATUS.md`; this module is the repair,
and it is labelled unpredicted work throughout.

What it adds: the three demand-inert kinds compose along a HISTORY.  A run
of the sealed grammar reconstructed here whose events are all supplies,
impositions and form admissions reaches, from a well-formed base, only
regimes whose demands are the base's demands -- for every stake, at every
prefix.  So under such a run no demand is ever first, because none is ever
new.

What it does NOT add: a general first-demand index.  The other three
kinds -- the admission of a datum, of an instance, and of a uniform rule --
do change demand sets, and locating the first demand of a run containing
them is a leftover, named and priced in `STATUS.md` and executed nowhere.

AuthorityEffect: None.
-/

namespace SecondNoFirst
namespace Run

open SecondNoFirst.Sealed
open SecondNoFirst.Stake
open SecondNoFirst.NoFirst
open SecondNoFirst.Inert

/-! ## 1. Replay, one event at a time -/

/-- Replay peels one event from the front. -/
theorem replayE_cons (e : Event) (rest : List Event) (base : Regime) :
    replayE (e :: rest) base = (stepE base e).bind (fun b => replayE rest b) := by
  unfold replayE
  cases hse : stepE base e <;> simp [List.foldlM, hse]

theorem replayE_nil (base : Regime) : replayE [] base = some base := rfl

/-! ## 2. The inert kinds of the grammar -/

/-- The three event kinds this rung proves demand-inert: the supply, the
imposition, and the admission of a judgment form.  The other three kinds
of the sealed grammar are deliberately absent, and nothing here claims
anything about them. -/
inductive InertEvent : Event → Prop where
  | supply (t : Nat) : InertEvent (.supply t)
  | impose (i j : Nat) : InertEvent (.impose i j)
  | admitForm (a : Nat) : InertEvent (.admitForm a)

/-! ## 3. Well-formedness survives an inert step -/

/-- Admitting a form of arity at least one to a well-formed regime leaves
it well formed. -/
theorem wf_addForm (r : Regime) (hwf : r.wf) (a : Nat) (ha : 1 ≤ a) :
    (addForm r a).wf := by
  obtain ⟨hi, hr, hq, hf⟩ := hwf
  refine ⟨?_, ?_, hq, ?_⟩
  · intro p hp
    have hp' : p ∈ r.insts := hp
    obtain ⟨h1, h2, h3⟩ := hi p hp'
    refine ⟨?_, ?_, h3⟩
    · show p.1 < (r.forms ++ [a]).length
      rw [List.length_append]; omega
    · rw [show (addForm r a).forms = r.forms ++ [a] from rfl,
        getD_append_left r.forms a p.1 h1]
      exact h2
  · intro f hf'
    have := hr f hf'
    show f < (r.forms ++ [a]).length
    rw [List.length_append]; omega
  · intro b hb
    have hb' : b ∈ r.forms ++ [a] := hb
    rw [List.mem_append] at hb'
    rcases hb' with h | h
    · exact hf b h
    · rw [List.mem_singleton.mp h]; exact ha

/-- Imposing a requirement between admitted data leaves a well-formed
regime well formed. -/
theorem wf_addReq (r : Regime) (hwf : r.wf) (i j : Nat) (hij : i < j)
    (hj : j < r.data) : (addReq r i j).wf := by
  obtain ⟨hi, hr, hq, hf⟩ := hwf
  refine ⟨hi, hr, ?_, hf⟩
  intro q hq'
  have hq'' : q ∈ insertNew r.reqs (i, j) := hq'
  by_cases hmem : (i, j) ∈ r.reqs
  · rw [insertNew_of_mem hmem] at hq''
    exact hq q hq''
  · rw [insertNew_of_not_mem hmem, List.mem_append] at hq''
    rcases hq'' with h | h
    · exact hq q h
    · rw [List.mem_singleton.mp h]; exact ⟨hij, hj⟩

/-- One inert step preserves well-formedness. -/
theorem wf_step_inert (r r' : Regime) (hwf : r.wf) (e : Event)
    (he : InertEvent e) (h : stepE r e = some r') : r'.wf := by
  cases he with
  | supply t =>
      rw [supply_no_op r t] at h
      rw [← Option.some.inj h]; exact hwf
  | impose i j =>
      by_cases hg : i < j ∧ j < r.data
      · rw [stepE_impose r i j hg.1 hg.2] at h
        rw [← Option.some.inj h]
        exact wf_addReq r hwf i j hg.1 hg.2
      · exfalso
        have : stepE r (.impose i j) = none := by
          show (if i < j ∧ j < r.data then _ else none) = none
          rw [if_neg hg]
        rw [this] at h
        exact absurd h (by simp)
  | admitForm a =>
      by_cases ha : 1 ≤ a
      · rw [stepE_admitForm r a ha] at h
        rw [← Option.some.inj h]
        exact wf_addForm r hwf a ha
      · exfalso
        have : stepE r (.admitForm a) = none := by
          show (if 1 ≤ a then _ else none) = none
          rw [if_neg ha]
        rw [this] at h
        exact absurd h (by simp)

/-! ## 4. One inert step changes no demand -/

/-- **demands_step_inert.**  In the sealed grammar reconstructed here,
extended by a declared two-sided stake: one event of an inert kind, from a
well-formed regime, leaves every demand of every stake exactly as it
was. -/
theorem demands_step_inert (S : Stake) (r r' : Regime) (hwf : r.wf) (e : Event)
    (he : InertEvent e) (h : stepE r e = some r') (i j : Nat) :
    Demand S r' i j ↔ Demand S r i j := by
  cases he with
  | supply t => exact supply_preserves_demands S r r' t h i j
  | impose a b =>
      by_cases hg : a < b ∧ b < r.data
      · rw [stepE_impose r a b hg.1 hg.2] at h
        rw [← Option.some.inj h]
        exact impose_preserves_demands S r a b i j
      · exfalso
        have hn : stepE r (.impose a b) = none := by
          show (if a < b ∧ b < r.data then _ else none) = none
          rw [if_neg hg]
        rw [hn] at h
        exact absurd h (by simp)
  | admitForm a =>
      by_cases ha : 1 ≤ a
      · rw [stepE_admitForm r a ha] at h
        rw [← Option.some.inj h]
        exact admitForm_preserves_demands S r hwf a i j
      · exfalso
        have hn : stepE r (.admitForm a) = none := by
          show (if 1 ≤ a then _ else none) = none
          rw [if_neg ha]
        rw [hn] at h
        exact absurd h (by simp)

/-! ## 5. A whole run of inert events -/

/-- **demands_replay_inert.**  In the sealed grammar reconstructed here,
extended by a declared two-sided stake, and in no other grammar: a RUN
whose every event is a supply, an imposition, or a form admission reaches,
from a well-formed base, only regimes carrying exactly the demands the base
carried -- for every stake, and at the end of every such history.

This is the statement in which a run appears rather than a single regime.
Under such a run no demand is ever first, because none is ever new. -/
theorem demands_replay_inert (S : Stake) :
    ∀ (h : List Event) (base r : Regime),
      (∀ e ∈ h, InertEvent e) → base.wf → replayE h base = some r →
      ∀ i j, (Demand S r i j ↔ Demand S base i j)
  | [], base, r, _, _, hr, i, j => by
      rw [replayE_nil base] at hr
      rw [← Option.some.inj hr]
  | e :: rest, base, r, hall, hwf, hr, i, j => by
      rw [replayE_cons e rest base] at hr
      cases hse : stepE base e with
      | none => rw [hse] at hr; exact absurd hr (by simp)
      | some mid =>
          rw [hse] at hr
          have hmid : InertEvent e := hall e List.mem_cons_self
          have hwf' : mid.wf := wf_step_inert base mid hwf e hmid hse
          have hrest : ∀ x ∈ rest, InertEvent x :=
            fun x hx => hall x (List.mem_cons_of_mem e hx)
          have ih := demands_replay_inert S rest mid r hrest hwf' (by simpa using hr) i j
          exact ih.trans (demands_step_inert S base mid hwf e hmid hse i j)

/-- **no_demand_is_first_under_an_inert_run.**  The same fact stated the
way the rung's question asks it: from a well-formed base carrying no
demand under a declared stake, no regime reached by a run of inert events
carries a demand.  In this grammar, and under such a run, there is no
first demand. -/
theorem no_demand_is_first_under_an_inert_run (S : Stake) (h : List Event)
    (base r : Regime) (hall : ∀ e ∈ h, InertEvent e) (hwf : base.wf)
    (hquiet : ∀ i j, ¬ Demand S base i j) (hr : replayE h base = some r)
    (i j : Nat) : ¬ Demand S r i j :=
  fun hd => hquiet i j ((demands_replay_inert S h base r hall hwf hr i j).mp hd)

/-- **free_stake_no_demand_along_any_run.**  Under the stake that labels
every pair free, no regime reached by ANY history of sealed events from ANY
base carries a demand -- inert or not, well formed or not.
AT THE LEVEL OF A DEFINITION: the free stake labels nothing, so the
labelling conjunct of `Demand` fails at every regime whatever, and the
history plays no part in the argument.  It is stated because the question
is asked about runs and an answer about regimes is not literally an answer
about runs; it is labelled because stating it costs nothing. -/
theorem free_stake_no_demand_along_any_run (h : List Event) (base r : Regime)
    (_hr : replayE h base = some r) (i j : Nat) : ¬ Demand freeStake r i j :=
  free_stake_no_demand r i j

end Run
end SecondNoFirst
