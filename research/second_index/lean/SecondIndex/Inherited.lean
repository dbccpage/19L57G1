import SecondIndex.Kernel

/-!
# The sibling rung's stake and inertia slice, reconstructed verbatim

PIN NOTE (whole file).  Every declaration below is reproduced VERBATIM
from the previous rung's committed package
`research/second_nofirst/lean/SecondNoFirst/`, at the blobs recorded in
`SOURCE_MANIFEST.json`, at the snapshot recorded there: the label, the
two-sided stake, honour and the demand predicate over the sealed regime
from `Stake.lean`; four demand lemmas from `NoFirst.lean`; the
transport result and the two inert-kind results from `Inert.lean`; and replay by
one event, well-formedness under an inert step, the inert event kinds and
the two inert-run theorems from `Run.lean`.

The only changes are the outer namespace, which flattens that package's
four namespaces into one so that this package stays self-contained and
imports nothing of the sibling, and the file-level doc comment, which is
this file's own.  Section headers, declaration doc comments and proofs
are the sibling's, unedited.

What is deliberately NOT reconstructed: that package's bridge to the
one-sided represented state (`dishonouredW`, `demandsW`, `ofCommitment`,
`reconstruction_matches`), its event code and its headline conjunctions
(`eventCode`, `grammar_carries_no_stake`, `no_first_demand`,
`three_kinds_are_demand_inert`, `demand_depends_only_on_the_label`,
`supplies_preserve_regime`, `supplies_preserve_demands`,
`no_demand_is_first_under_an_inert_run`,
`free_stake_no_demand_along_any_run`).  None of them is consumed by this
rung's arguments.  What IS reconstructed and not consumed either is
`allSame`, which sits inside the pinned span this file reproduces whole;
it is reproduced rather than excised, because a span reproduced with a
hole in it is no longer a verbatim span.  The omitted names are pinned in
`test_reconstruction.py`, which also checks that no declaration here
mentions one of them; that the omissions are SAFE is read by hand and is
recorded as such in `STATUS.md`.

What a pin proves: that the sibling source did not move.  A theorem
reconstructed here is the sibling's result, classed RECONSTRUCTION in the
census, and is never counted as this rung's content.

AuthorityEffect: None.
-/

namespace SecondIndex
namespace Inherited

open SecondIndex.Sealed

/-! ## 1. The label and the stake -/

/-- The three values a stake assigns to an ordered pair of datum indices. -/
inductive Label where
  | apart
  | same
  | free
deriving Repr, DecidableEq

/-- A label is LABELLED when it constrains: apart and same do, free does
not. -/
def Label.labelled : Label → Bool
  | .free => false
  | _ => true

/-- A two-sided STAKE: a label on every ordered pair of datum indices,
present or future, free on the diagonal by construction.  It is declared
once, reads no state, and emits nothing. -/
structure Stake where
  label : Nat → Nat → Label
  diag : ∀ i, label i i = Label.free

/-- The stake that constrains nothing. -/
def freeStake : Stake where
  label _ _ := Label.free
  diag _ := rfl

/-- The stake that keeps every distinct pair apart. -/
def allApart : Stake where
  label i j := if i = j then Label.free else Label.apart
  diag i := by simp

/-- The stake that requires every distinct pair collapsed. -/
def allSame : Stake where
  label i j := if i = j then Label.free else Label.same
  diag i := by simp

/-- **stake_irrefl.**  No pair of a datum with itself carries a label.
AT THE LEVEL OF A DEFINITION: one rewrite of the structure field, then
`rfl`. -/
theorem stake_irrefl (S : Stake) (i : Nat) :
    (S.label i i).labelled = false := by
  rw [S.diag i]; rfl

/-! ## 2. Honour and demands over the sealed regime -/

/-- HONOUR of a labelled pair by a regime: apart is honoured by
separability, same by collapse, free always. -/
def honour (r : Regime) (l : Label) (i j : Nat) : Prop :=
  match l with
  | .apart => separable r i j
  | .same => collapsed r i j
  | .free => True

/-- A DEMAND of the stake `S` at the regime `r`: an ordered pair of held
data that `S` labels and that `r` does not honour. -/
def Demand (S : Stake) (r : Regime) (i j : Nat) : Prop :=
  i < j ∧ j < r.data ∧ (S.label i j).labelled = true ∧
    ¬ honour r (S.label i j) i j

/-- **demands_subset_labelled.**  Every demand is at a labelled pair.
AT THE LEVEL OF A DEFINITION: the labelling condition is a conjunct of
`Demand`, so this is a projection. -/
theorem demands_subset_labelled (S : Stake) (r : Regime) (i j : Nat)
    (h : Demand S r i j) : (S.label i j).labelled = true := h.2.2.1

/-- **free_stake_no_demand.**  Under the stake that labels every pair
free there is no demand at any regime, reachable or not.
AT THE LEVEL OF A DEFINITION: the label is `free` by unfolding, so the
labelling conjunct of `Demand` is `false = true`. -/
theorem free_stake_no_demand (r : Regime) (i j : Nat) :
    ¬ Demand freeStake r i j := by
  intro h
  exact absurd h.2.2.1 (by simp [freeStake, Label.labelled])

/-- A labelled pair is labelled apart or labelled same.  A three-way case
split with the free case discharged by the labelling condition. -/
theorem labelled_cases (l : Label) (h : l.labelled = true) :
    l = Label.apart ∨ l = Label.same := by
  cases l with
  | apart => exact Or.inl rfl
  | same => exact Or.inr rfl
  | free => exact absurd h (by simp [Label.labelled])

/-! ## Reconstructed from the sibling's `NoFirst` module -/

/-- **supply_preserves_demands.**  In the sealed grammar reconstructed
here, extended by a declared two-sided stake, the demands after a supply
are the demands before it, for every stake and every pair.  The content is
carried by the sealed `supply_no_op`; what this theorem adds is the
transport of that fact through the demand predicate, which is one
substitution. -/
theorem supply_preserves_demands (S : Stake) (r r' : Regime) (t : Nat)
    (h : stepE r (.supply t) = some r') (i j : Nat) :
    Demand S r' i j ↔ Demand S r i j := by
  rw [supply_no_op r t] at h
  rw [Option.some.inj h]

/-- **demand_needs_label.**  In the sealed grammar reconstructed here,
extended by a declared two-sided stake, a pair that is a demand at a
regime is a pair the stake labels apart or labels same.
AT THE LEVEL OF A DEFINITION: `Demand` carries the labelling condition as
a conjunct, and the three-way case split on the label is immediate. -/
theorem demand_needs_label (S : Stake) (r : Regime) (i j : Nat)
    (h : Demand S r i j) :
    S.label i j = Label.apart ∨ S.label i j = Label.same :=
  labelled_cases _ h.2.2.1

/-! ## 5. What the demand set is, where the grammar has not yet built one -/

/-- Collapse rules out separability, constructively. -/
theorem collapsed_not_separable {r : Regime} {d d' : Nat}
    (h : collapsed r d d') : ¬ separable r d d' :=
  fun ⟨c, hw, hne⟩ => hne (h c hw)

/-- Failing to separate is being collapsed: derivability is decidable, so
the double negation is eliminated without any choice. -/
theorem collapsed_of_not_separable {r : Regime} {d d' : Nat}
    (h : ¬ separable r d d') : collapsed r d d' := by
  intro c hw
  by_cases hd : (derivable r (plug c d) ↔ derivable r (plug c d'))
  · exact hd
  · exact absurd ⟨c, hw, hd⟩ h

/-- **apart_demand_of_no_forms.**  In the sealed grammar reconstructed
here, extended by a declared two-sided stake: at a regime with no admitted
form there is no well-formed context, so no pair is separable, and every
held pair the stake labels apart is a demand. -/
theorem apart_demand_of_no_forms (S : Stake) (r : Regime) (hf : r.forms = [])
    (i j : Nat) (hij : i < j) (hj : j < r.data)
    (hlab : S.label i j = Label.apart) : Demand S r i j := by
  refine ⟨hij, hj, by rw [hlab]; rfl, ?_⟩
  rw [hlab]
  intro ⟨c, hw, _⟩
  have := hw.1
  rw [hf] at this
  exact absurd this (by simp)

/-- **demand_iff_apart_of_no_insts.**  In the sealed grammar reconstructed
here, extended by a declared two-sided stake: at a regime with no admitted
instance, a held pair is a demand exactly when the stake labels it apart.
The forward direction rules out the same label, because with no instance
every pair is collapsed and a same label is therefore honoured; the
backward direction uses the same collapse to defeat separability. -/
theorem demand_iff_apart_of_no_insts (S : Stake) (r : Regime)
    (hi : r.insts = []) (i j : Nat) (hij : i < j) (hj : j < r.data) :
    Demand S r i j ↔ S.label i j = Label.apart := by
  constructor
  · intro h
    rcases demand_needs_label S r i j h with hap | hsm
    · exact hap
    · exfalso
      have hno := h.2.2.2
      rw [hsm] at hno
      exact hno (collapsed_of_no_insts r hi i j)
  · intro hlab
    refine ⟨hij, hj, by rw [hlab]; rfl, ?_⟩
    rw [hlab]
    exact collapsed_not_separable (collapsed_of_no_insts r hi i j)

/-! ## Reconstructed from the sibling's `Inert` module -/

/-! ## 0. Transporting a demand along an agreement of observation

Collapse and separability are transported SEPARATELY.  Deriving one from
the other would need, in the direction from "not collapsed" to
"separable", a choice of witness over the context type, which is
infinite; that direction is not available constructively and is not used.
Every transport below supplies both halves and its own witness. -/

/-- A demand transports along any pair of agreements -- of the data count,
of separability, and of collapse -- between two regimes.  This is the one
bridge the three inertia theorems share. -/
theorem demand_congr (S : Stake) (r r' : Regime)
    (hdata : r'.data = r.data)
    (hsep : ∀ i j, separable r' i j ↔ separable r i j)
    (hcol : ∀ i j, collapsed r' i j ↔ collapsed r i j) (i j : Nat) :
    Demand S r' i j ↔ Demand S r i j := by
  unfold Demand honour
  rw [hdata]
  refine and_congr_right (fun _ => and_congr_right (fun _ =>
    and_congr_right (fun _ => not_congr ?_)))
  cases S.label i j with
  | apart => exact hsep i j
  | same => exact hcol i j
  | free => exact Iff.rfl

/-! ## 1. An imposition is demand-inert -/

/-- The regime an imposition reaches. -/
def addReq (r : Regime) (i j : Nat) : Regime :=
  { r with reqs := insertNew r.reqs (i, j) }

theorem stepE_impose (r : Regime) (i j : Nat) (h : i < j) (hj : j < r.data) :
    stepE r (.impose i j) = some (addReq r i j) := by
  show (if i < j ∧ j < r.data then some (addReq r i j) else none) = some (addReq r i j)
  rw [if_pos ⟨h, hj⟩]

/-- **impose_preserves_demands.**  In the sealed grammar reconstructed
here, extended by a declared two-sided stake, an imposition changes no
demand of any stake.
AT THE LEVEL OF A DEFINITION: an imposition writes only the requirement
field, and that field enters neither derivability nor the well-formedness
of a context, so both sides unfold to the same proposition. -/
theorem impose_preserves_demands (S : Stake) (r : Regime) (i j : Nat)
    (a b : Nat) : Demand S (addReq r i j) a b ↔ Demand S r a b := Iff.rfl

/-! ## 2. Admitting a form is demand-inert -/

/-- The regime a form admission reaches. -/
def addForm (r : Regime) (a : Nat) : Regime :=
  { r with forms := r.forms ++ [a] }

theorem stepE_admitForm (r : Regime) (a : Nat) (h : 1 ≤ a) :
    stepE r (.admitForm a) = some (addForm r a) := by
  show (if 1 ≤ a then some (addForm r a) else none) = some (addForm r a)
  rw [if_pos h]

/-- Appending to the form list does not move the arity of a form already
admitted. -/
theorem getD_append_left (l : List Nat) (a i : Nat) (h : i < l.length) :
    (l ++ [a]).getD i 0 = l.getD i 0 := by
  simp [List.getD_eq_getElem?_getD, List.getElem?_append_left h]

/-- A context naming a form admitted before the new one is well formed
after the admission exactly when it was well formed before. -/
theorem wfCtx_addForm_left (r : Regime) (a : Nat) (c : Ctx)
    (hlt : c.form < r.forms.length) :
    wfCtx (addForm r a) c ↔ wfCtx r c := by
  have harity : (addForm r a).forms.getD c.form 0 = r.forms.getD c.form 0 :=
    getD_append_left r.forms a c.form hlt
  have hlen : c.form < (addForm r a).forms.length := by
    show c.form < (r.forms ++ [a]).length
    rw [List.length_append]
    omega
  constructor
  · intro h
    obtain ⟨_, h2, h3, h4⟩ := h
    rw [harity] at h2
    exact ⟨hlt, h2, h3, h4⟩
  · intro h
    obtain ⟨_, h2, h3, h4⟩ := h
    rw [← harity] at h2
    exact ⟨hlen, h2, h3, h4⟩

/-- A context of the newly admitted form derives nothing, whatever datum
is plugged into it: no admitted instance of a well-formed regime names a
form index that large, and the new form carries no uniform rule. -/
theorem new_form_derives_nothing (r : Regime) (hwf : r.wf) (a : Nat) (c : Ctx)
    (hnew : c.form = r.forms.length) (d : Nat) :
    ¬ derivable (addForm r a) (plug c d) := by
  intro h
  cases h with
  | inl hm =>
      have hb := (hwf.1 _ hm).1
      show False
      rw [show (plug c d).1 = c.form from rfl, hnew] at hb
      exact absurd hb (Nat.lt_irrefl _)
  | inr hr =>
      have hb := hwf.2.1 _ hr
      show False
      rw [show (plug c d).1 = c.form from rfl, hnew] at hb
      exact absurd hb (Nat.lt_irrefl _)

/-- **collapsed_addForm.**  Admitting a judgment form to a well-formed
regime changes no pair's collapse: the contexts of forms already admitted
answer exactly as before, and the contexts of the new form derive nothing
for any datum, so they separate nothing. -/
theorem collapsed_addForm (r : Regime) (hwf : r.wf) (a : Nat) (d d' : Nat) :
    collapsed (addForm r a) d d' ↔ collapsed r d d' := by
  constructor
  · intro h c hw
    exact h c ((wfCtx_addForm_left r a c hw.1).mpr hw)
  · intro h c hw
    by_cases hlt : c.form < r.forms.length
    · exact h c ((wfCtx_addForm_left r a c hlt).mp hw)
    · have hb : c.form < (r.forms ++ [a]).length := hw.1
      rw [List.length_append] at hb
      have hnew : c.form = r.forms.length := by simp at hb; omega
      constructor
      · intro hd
        exact absurd hd (new_form_derives_nothing r hwf a c hnew d)
      · intro hd
        exact absurd hd (new_form_derives_nothing r hwf a c hnew d')

/-- **separable_addForm.**  Admitting a judgment form to a well-formed
regime separates no pair it did not already separate, and unseparates
none: a witness of the new form derives nothing on either side, so it
cannot be a witness at all. -/
theorem separable_addForm (r : Regime) (hwf : r.wf) (a : Nat) (d d' : Nat) :
    separable (addForm r a) d d' ↔ separable r d d' := by
  constructor
  · intro ⟨c, hw, hne⟩
    by_cases hlt : c.form < r.forms.length
    · exact ⟨c, (wfCtx_addForm_left r a c hlt).mp hw, hne⟩
    · exfalso
      have hb : c.form < (r.forms ++ [a]).length := hw.1
      rw [List.length_append] at hb
      have hnew : c.form = r.forms.length := by simp at hb; omega
      exact hne ⟨fun hd => absurd hd (new_form_derives_nothing r hwf a c hnew d),
                 fun hd => absurd hd (new_form_derives_nothing r hwf a c hnew d')⟩
  · intro ⟨c, hw, hne⟩
    exact ⟨c, (wfCtx_addForm_left r a c hw.1).mpr hw, hne⟩

/-- **admitForm_preserves_demands.**  In the sealed grammar reconstructed
here, extended by a declared two-sided stake: admitting a judgment form to
a well-formed regime changes no demand of any stake.  A form is
demand-inert until an instance or a uniform rule reaches it.

This is the third of the three inert kinds, and the only one of the three
with content.  It was not predicted; it was proved after the stage-four
rectangle found the count to be three where the frozen prediction said
two. -/
theorem admitForm_preserves_demands (S : Stake) (r : Regime) (hwf : r.wf)
    (a : Nat) (i j : Nat) :
    Demand S (addForm r a) i j ↔ Demand S r i j :=
  demand_congr S r (addForm r a) rfl
    (fun x y => separable_addForm r hwf a x y)
    (fun x y => collapsed_addForm r hwf a x y) i j

/-! ## Reconstructed from the sibling's `Run` module -/

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

end Inherited
end SecondIndex
