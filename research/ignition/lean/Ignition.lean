import Derivation.Basic
import Derivation.Inertia
import Derivation.Mention
import Derivation.Progress
import Derivation.Minimality
import Derivation.Rounds
import Derivation.Compression
import Derivation.PresentationRelativity
import LocalReuse

/-!
# Endogenous activity on the sealed carrier: the boundary, exactly

Everything here is over the sealed `Derivation.Regime`, its sealed event
grammar `Event`, the sealed step `stepE`, the sealed observation
(`collapsed` / `separable`) and the sealed response relation `TransStep`.
Nothing in `lean4/` is changed; the replay-cut theorems of the merged
`local_reuse` family are imported, not re-proved.

The file answers one question in seven parts.

1. **The sealed signature has no autonomous transition.**  Every state
   change is indexed by an event, and a bare-supply history of any length
   is lawful and changes nothing (`inert_history`, `idle_lawful`).  So the
   idle interpretation satisfies every sealed premise: "what happens next"
   is not a property the sealed signature can state.
2. **Demand from state, characterized.**  A fresh datum collapses with an
   admitted datum exactly when that datum is mentioned by no instance
   (`grow_demand_iff`).  Two fresh data always collapse
   (`two_grows_collapsed`).  At a state where every pair is separated, one
   growth step creates at most one demand (`grow_at_most_one_demand`).
   Growth changes no verdict on the old data (`grow_keeps_verdicts`).
3. **The declared extension.**  `XStep` adds exactly two laws to the
   sealed step: growth (one fresh datum) and firing (a collapsed pair
   becomes the demand and a valid rule-free response answers it — the
   sealed `TransStep`).  Every `XStep` decodes to a sealed event block that
   replays to the same successor (`grow_replays`, `fire_replays`), and the
   invariant `Good` (well-formed, rule-free, every standing requirement
   separated) is preserved (`good_grow`, `good_fire`).
4. **The productive run.**  From any `Good` state, the block "grow, grow,
   demand the fresh pair, mark" replays to a `Good` state with two more
   data, one more form and one more requirement (`block_replays`,
   `blockState_good`), and iterates without bound (`runHist_replays`,
   `runState_data`, `runState_reqs`).  The response changes a verdict
   (`block_is_activity`); the growth steps alone do not.
5. **The residual bridge on the actual carrier.**  The sealed closure
   demand — a collapsed pair of distinct data — is exactly the residual
   of the profile presentation relative to the identity comparison
   (`demand_iff_residual`), and that comparison is not a digest of the
   profile signature (`identity_not_signature_determined`).  The joint
   presentation of the sealed `Compression` module has the promised
   fibers and is idempotent (`joint_eq_iff`, `joint_idempotent`); its
   partition is order-free and its representative is not
   (`partition_order_free`, `representative_order_dependent`).
6. **The future factors through the endpoint.**  Two histories reaching
   one regime have identical continuations (`future_factors_through_endpoint`);
   a route-dependent total is therefore invisible to every continuation
   (`routes_agree`, `routes_cost_differ`).
7. **What the boundary does not say.**  No statement here excludes the
   idle history; the extension's activity law is where that exclusion
   lives, and the fixed-carrier bound applies only to datum-fixed rounds.

AuthorityEffect: None.
-/

namespace Ignition

open Derivation

/-! ## 1. The sealed signature: every transition is indexed by an event -/

/-- Every event of the history is a bare supply. -/
def AllSupply (h : List Event) : Prop := ∀ e ∈ h, ∃ t, e = Event.supply t

/-- A history of bare supplies is lawful from every state and changes
nothing: the idle interpretation satisfies the sealed step. -/
theorem inert_history : ∀ (h : List Event), AllSupply h → ∀ r : Regime,
    replayE h r = some r
  | [], _, _ => rfl
  | e :: rest, hall, r => by
      obtain ⟨t, ht⟩ := hall e List.mem_cons_self
      subst ht
      rw [replayE_cons, supply_no_op]
      exact inert_history rest (fun e' he' => hall e' (List.mem_cons_of_mem _ he')) r

/-- Idle histories of every length exist from every state. -/
theorem idle_lawful (n : Nat) (r : Regime) :
    replayE (List.replicate n (Event.supply 0)) r = some r :=
  inert_history _ (fun _ he => ⟨0, List.eq_of_mem_replicate he⟩) r

/-! ## 2. Mention, growth and demand -/

/-- A datum is mentioned when some admitted instance names it. -/
def Mentioned (r : Regime) (d : Nat) : Prop := ∃ p ∈ r.insts, d ∈ p.2

/-- No plug of an unmentioned datum is an admitted instance: every
well-formed context has a hole, and the hole receives the datum. -/
theorem plug_not_mem_of_unmentioned {r : Regime} {d : Nat}
    (h : ¬ Mentioned r d) {c : Ctx} (hhole : none ∈ c.slots) :
    plug c d ∉ r.insts :=
  fun hm => h ⟨plug c d, hm, mem_plug_of_hole hhole d⟩

/-- For an unmentioned datum, derivability of a plug is exactly rule
coverage of the context's form. -/
theorem derivable_unmentioned_iff {r : Regime} {d : Nat}
    (h : ¬ Mentioned r d) {c : Ctx} (hhole : none ∈ c.slots) :
    derivable r (plug c d) ↔ c.form ∈ r.rules := by
  unfold derivable
  constructor
  · rintro (hm | hr)
    · exact absurd hm (plug_not_mem_of_unmentioned h hhole)
    · exact hr
  · intro hr
    exact Or.inr hr

/-- Two unmentioned data are collapsed, rules or no rules. -/
theorem collapsed_of_unmentioned_pair {r : Regime} {d d' : Nat}
    (hd : ¬ Mentioned r d) (hd' : ¬ Mentioned r d') : collapsed r d d' := by
  intro c hc
  have hhole : none ∈ c.slots := hc.2.2.1
  rw [derivable_unmentioned_iff hd hhole, derivable_unmentioned_iff hd' hhole]

/-- Hole every occurrence of `d` in an argument list. -/
def holeAt (d : Nat) (args : List Nat) : List (Option Nat) :=
  args.map (fun a => if a = d then none else some a)

theorem holeAt_length (d : Nat) (args : List Nat) :
    (holeAt d args).length = args.length :=
  List.length_map _

theorem holeAt_getD (d a : Nat) :
    (if a = d then (none : Option Nat) else some a).getD d = a := by
  by_cases h : a = d
  · rw [if_pos h]
    exact h.symm
  · rw [if_neg h]
    rfl

theorem holeAt_map_getD (d : Nat) :
    ∀ args : List Nat, (holeAt d args).map (fun s => s.getD d) = args
  | [] => rfl
  | a :: t => by
      show ((if a = d then (none : Option Nat) else some a).getD d)
          :: (holeAt d t).map (fun s => s.getD d) = a :: t
      rw [holeAt_getD, holeAt_map_getD d t]

/-- Plugging the holed context with its own datum returns the instance. -/
theorem plug_holeAt (f d : Nat) (args : List Nat) :
    plug ⟨f, holeAt d args⟩ d = (f, args) := by
  show (f, (holeAt d args).map (fun s => s.getD d)) = (f, args)
  rw [holeAt_map_getD]

/-- The holed context of an admitted instance is well-formed. -/
theorem wfCtx_holeAt {r : Regime} (hwf : r.wf) {f : Nat} {args : List Nat}
    (hmem : (f, args) ∈ r.insts) {d : Nat} (hd : d ∈ args) :
    wfCtx r ⟨f, holeAt d args⟩ := by
  have hp := hwf.1 (f, args) hmem
  refine ⟨hp.1, ?_, ?_, ?_⟩
  · show (holeAt d args).length = r.forms.getD f 0
    rw [holeAt_length]
    exact hp.2.1
  · exact List.mem_map.mpr ⟨d, hd, by simp⟩
  · intro s hs
    obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hs
    by_cases h : a = d
    · rw [if_pos h]
      trivial
    · rw [if_neg h]
      exact hp.2.2 a ha

/-- A datum collapses with an unmentioned datum exactly when it is itself
unmentioned (rule-free, well-formed regimes). -/
theorem collapsed_with_unmentioned_iff {r : Regime} (hwf : r.wf)
    (hrules : r.rules = []) {a n : Nat} (hn : ¬ Mentioned r n) :
    collapsed r a n ↔ ¬ Mentioned r a := by
  constructor
  · intro hcol hma
    obtain ⟨⟨f, args⟩, hp, hd⟩ := hma
    have hwfc : wfCtx r ⟨f, holeAt a args⟩ := wfCtx_holeAt hwf hp hd
    have hder : derivable r (plug ⟨f, holeAt a args⟩ a) := by
      rw [plug_holeAt]
      exact Or.inl hp
    have hn' := (hcol _ hwfc).mp hder
    rw [derivable_unmentioned_iff hn hwfc.2.2.1, hrules] at hn'
    cases hn'
  · intro ha
    exact collapsed_of_unmentioned_pair ha hn

/-- Growth: one fresh datum, and nothing else.  This is the sealed
`admitDatum` step, named. -/
def grow (r : Regime) : Regime := { r with data := r.data + 1 }

theorem stepE_grow (r : Regime) : stepE r .admitDatum = some (grow r) := rfl

theorem grow_replays (r : Regime) : replayE [.admitDatum] r = some (grow r) := rfl

/-- A datum at or beyond the carrier is mentioned by no instance of a
well-formed regime. -/
theorem unmentioned_of_ge {r : Regime} (hwf : r.wf) {d : Nat}
    (hd : r.data ≤ d) : ¬ Mentioned r d := by
  rintro ⟨p, hp, hd'⟩
  have := (hwf.1 p hp).2.2 d hd'
  omega

theorem grow_wf {r : Regime} (hwf : r.wf) : (grow r).wf := by
  obtain ⟨hinst, hrule, hreq, hform⟩ := hwf
  refine ⟨?_, hrule, ?_, hform⟩
  · intro p hp
    obtain ⟨h1, h2, h3⟩ := hinst p hp
    exact ⟨h1, h2, fun a ha => Nat.lt_succ_of_lt (h3 a ha)⟩
  · intro q hq
    obtain ⟨h1, h2⟩ := hreq q hq
    exact ⟨h1, Nat.lt_succ_of_lt h2⟩

/-- Growth keeps every separation witness. -/
theorem separable_grow {r : Regime} {d d' : Nat} (h : separable r d d') :
    separable (grow r) d d' := by
  obtain ⟨c, hc, hne⟩ := h
  refine ⟨c, ⟨hc.1, hc.2.1, hc.2.2.1, ?_⟩, hne⟩
  intro s hs
  have := hc.2.2.2 s hs
  cases s with
  | none => trivial
  | some x => exact Nat.lt_succ_of_lt this

/-- Growth changes no verdict on the admitted data: the sealed R1 lemma,
instantiated at the growth step. -/
theorem grow_keeps_verdicts {r : Regime} (hwf : r.wf) (d d' : Nat) :
    collapsed (grow r) d d' ↔ collapsed r d d' :=
  collapsed_fresh_datum r d d' (fun p hp => (hwf.1 p hp).2.2)

/-- **The demand characterization.**  After one growth step the fresh
datum collapses with an admitted datum exactly when that datum is
mentioned by no instance.  So growth creates a demand iff the state holds
an unmentioned datum; it never depends on the fresh datum's presentation. -/
theorem grow_demand_iff {r : Regime} (hwf : r.wf) (hrules : r.rules = [])
    (a : Nat) : collapsed (grow r) a r.data ↔ ¬ Mentioned r a := by
  have hn : ¬ Mentioned (grow r) r.data := unmentioned_of_ge hwf (Nat.le_refl _)
  exact collapsed_with_unmentioned_iff (grow_wf hwf) hrules hn

theorem collapsed_trans {r : Regime} {a b c : Nat}
    (h1 : collapsed r a b) (h2 : collapsed r b c) : collapsed r a c :=
  fun ctx hc => (h1 ctx hc).trans (h2 ctx hc)

/-- **At most one demand per growth step** at a state where every pair of
data is separated: two admitted data both collapsed with the fresh datum
would be collapsed with each other. -/
theorem grow_at_most_one_demand {r : Regime}
    (hall : ∀ a b, a < b → b < r.data → separable r a b)
    {a b : Nat} (hab : a < b) (hb : b < r.data) :
    ¬ (collapsed (grow r) a r.data ∧ collapsed (grow r) b r.data) := by
  rintro ⟨ha, hb'⟩
  have hab' : collapsed (grow r) a b :=
    collapsed_trans ha ((collapsed_symm _ _ _).mp hb')
  exact separable_not_collapsed (separable_grow (hall a b hab hb)) hab'

/-- **Two growth steps always create a demand**: the two fresh data are
both unmentioned, hence collapsed. -/
theorem two_grows_collapsed {r : Regime} (hwf : r.wf) :
    collapsed (grow (grow r)) r.data (r.data + 1) := by
  have h0 : ¬ Mentioned (grow (grow r)) r.data := unmentioned_of_ge hwf (Nat.le_refl _)
  have h1 : ¬ Mentioned (grow (grow r)) (r.data + 1) := unmentioned_of_ge hwf (Nat.le_succ _)
  exact collapsed_of_unmentioned_pair h0 h1

/-- The demand created by two growth steps has a valid response: the
sealed `mark_progress` at the grown state. -/
theorem two_grows_response {r : Regime} (hwf : r.wf)
    (hreqs : ∀ q ∈ r.reqs, separable r q.1 q.2) :
    validResponse (grow (grow r)) r.data (r.data + 1)
      [.newForm 1, .newInst r.forms.length [r.data + 1]] :=
  mark_progress (grow (grow r)) (grow_wf (grow_wf hwf)) r.data (r.data + 1)
    (by show r.data < r.data + 1 + 1; omega)
    (by show r.data + 1 < r.data + 1 + 1; omega)
    (Nat.ne_of_lt (Nat.lt_succ_self _))
    (fun q hq => separable_grow (separable_grow (hreqs q hq)))

/-! ## 3. Well-formedness and rule-freeness along responses -/

theorem applyItem_wf {r s : Regime} (hwf : r.wf) {it : Item}
    (h : applyItem r it = some s) : s.wf := by
  obtain ⟨hinst, hrule, hreq, hform⟩ := hwf
  cases it with
  | newDatum =>
      have hs : s = { r with data := r.data + 1 } := (Option.some.inj h).symm
      subst hs
      refine ⟨?_, hrule, ?_, hform⟩
      · intro p hp
        obtain ⟨h1, h2, h3⟩ := hinst p hp
        exact ⟨h1, h2, fun a ha => Nat.lt_succ_of_lt (h3 a ha)⟩
      · intro q hq
        obtain ⟨h1, h2⟩ := hreq q hq
        exact ⟨h1, Nat.lt_succ_of_lt h2⟩
  | newForm a =>
      simp only [applyItem] at h
      split at h
      · rename_i ha
        have hs : s = { r with forms := r.forms ++ [a] } := (Option.some.inj h).symm
        subst hs
        refine ⟨?_, ?_, hreq, ?_⟩
        · intro p hp
          obtain ⟨h1, h2, h3⟩ := hinst p hp
          refine ⟨?_, ?_, h3⟩
          · show p.1 < (r.forms ++ [a]).length
            simp only [List.length_append, List.length_cons, List.length_nil]
            omega
          · show p.2.length = (r.forms ++ [a]).getD p.1 0
            rw [getD_append_lt _ _ _ h1]
            exact h2
        · intro f hf
          show f < (r.forms ++ [a]).length
          have := hrule f hf
          simp only [List.length_append, List.length_cons, List.length_nil]
          omega
        · intro b hb
          rcases List.mem_append.mp hb with hb | hb
          · exact hform b hb
          · have : b = a := List.mem_singleton.mp hb
            subst this
            exact ha
      · cases h
  | newInst f args =>
      simp only [applyItem] at h
      split at h
      · rename_i hc
        have hs : s = { r with insts := insertNew r.insts (f, args) } :=
          (Option.some.inj h).symm
        subst hs
        refine ⟨?_, hrule, hreq, hform⟩
        intro p hp
        rcases mem_insertNew.mp hp with hp | hp
        · exact hinst p hp
        · subst hp
          exact ⟨hc.1, hc.2.1, hc.2.2⟩
      · cases h
  | newRuleAll f =>
      simp only [applyItem] at h
      split at h
      · rename_i hc
        have hs : s = { r with rules := insertNew r.rules f } := (Option.some.inj h).symm
        subst hs
        refine ⟨hinst, ?_, hreq, hform⟩
        intro g hg
        rcases mem_insertNew.mp hg with hg | hg
        · exact hrule g hg
        · subst hg
          exact hc
      · cases h

theorem applyDelta_wf : ∀ {δ : List Item} {r s : Regime}, r.wf →
    applyDelta r δ = some s → s.wf
  | [], r, s, hwf, h => by
      have hs : s = r := (Option.some.inj h).symm
      subst hs
      exact hwf
  | it :: rest, r, s, hwf, h => by
      rw [applyDelta_cons] at h
      cases happ : applyItem r it with
      | none => rw [happ] at h; cases h
      | some r1 =>
          rw [happ] at h
          exact applyDelta_wf (applyItem_wf hwf happ) h

/-- No item other than a rule item touches the rule store. -/
theorem applyItem_rules {r s : Regime} {it : Item}
    (hnr : ∀ f, it ≠ Item.newRuleAll f) (h : applyItem r it = some s) :
    s.rules = r.rules := by
  cases it with
  | newDatum =>
      have hs : s = { r with data := r.data + 1 } := (Option.some.inj h).symm
      subst hs
      rfl
  | newForm a =>
      simp only [applyItem] at h
      split at h
      · have hs : s = { r with forms := r.forms ++ [a] } := (Option.some.inj h).symm
        subst hs
        rfl
      · cases h
  | newInst f args =>
      simp only [applyItem] at h
      split at h
      · have hs : s = { r with insts := insertNew r.insts (f, args) } :=
          (Option.some.inj h).symm
        subst hs
        rfl
      · cases h
  | newRuleAll f => exact absurd rfl (hnr f)

theorem applyDelta_rules : ∀ {δ : List Item} {r s : Regime},
    (∀ f, Item.newRuleAll f ∉ δ) → applyDelta r δ = some s → s.rules = r.rules
  | [], r, s, _, h => by
      have hs : s = r := (Option.some.inj h).symm
      subst hs
      rfl
  | it :: rest, r, s, hnr, h => by
      rw [applyDelta_cons] at h
      cases happ : applyItem r it with
      | none => rw [happ] at h; cases h
      | some r1 =>
          rw [happ] at h
          have hit : ∀ f, it ≠ Item.newRuleAll f :=
            fun f he => hnr f (he ▸ List.mem_cons_self)
          have hrest : ∀ f, Item.newRuleAll f ∉ rest :=
            fun f hm => hnr f (List.mem_cons_of_mem _ hm)
          exact (applyDelta_rules hrest h).trans (applyItem_rules hit happ)

/-- No item reads the requirement store: a delta applied after an
imposition is the delta applied before it, with the requirements carried
along. -/
theorem applyItem_reqs_free (r : Regime) (Q : List (Nat × Nat)) (it : Item) :
    applyItem { r with reqs := Q } it
      = (applyItem r it).map (fun u => { u with reqs := Q }) := by
  cases it with
  | newDatum => rfl
  | newForm a =>
      show (if 1 ≤ a then some _ else none)
        = Option.map _ (if 1 ≤ a then some _ else none)
      by_cases h : 1 ≤ a
      · rw [if_pos h, if_pos h]
        rfl
      · rw [if_neg h, if_neg h]
        rfl
  | newInst f args =>
      show (if f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
              (∀ x ∈ args, x < r.data) then some _ else none)
        = Option.map _ (if f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
              (∀ x ∈ args, x < r.data) then some _ else none)
      by_cases h : f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
          (∀ x ∈ args, x < r.data)
      · rw [if_pos h, if_pos h]
        rfl
      · rw [if_neg h, if_neg h]
        rfl
  | newRuleAll f =>
      show (if f < r.forms.length then some _ else none)
        = Option.map _ (if f < r.forms.length then some _ else none)
      by_cases h : f < r.forms.length
      · rw [if_pos h, if_pos h]
        rfl
      · rw [if_neg h, if_neg h]
        rfl

theorem applyDelta_reqs_free (Q : List (Nat × Nat)) :
    ∀ (δ : List Item) (r : Regime),
      applyDelta { r with reqs := Q } δ
        = (applyDelta r δ).map (fun u => { u with reqs := Q })
  | [], r => rfl
  | it :: rest, r => by
      rw [applyDelta_cons, applyDelta_cons, applyItem_reqs_free]
      cases applyItem r it with
      | none => rfl
      | some u => exact applyDelta_reqs_free Q rest u

/-! ## 4. The declared extension: growth and firing -/

/-- The invariant of the extension: well-formed, rule-free, every
standing requirement separated. -/
def Good (r : Regime) : Prop :=
  r.wf ∧ r.rules = [] ∧ ∀ q ∈ r.reqs, separable r q.1 q.2

/-- **The extension**, exactly two laws over the sealed step.  `grow`
admits one fresh datum.  `fire` takes a collapsed pair of admitted data
as the demand and answers it with a valid rule-free response: the sealed
`TransStep`, which quantifies over every valid response and selects
none.  Rule-freeness of the response mirrors the sealed engine invariant
(`rule_item_never_minimal`).  Neither law is a consequence of the sealed
inscription: both are declared here. -/
inductive XStep : Regime → Regime → Prop where
  | grow {r : Regime} : XStep r (grow r)
  | fire {r t : Regime} {i j : Nat} {δ : List Item} :
      TransStep r i j δ t → (∀ f, Item.newRuleAll f ∉ δ) → XStep r t

/-- The decoding square, firing half: a fire step is exactly the sealed
event block "impose, then the response items", replayed by the sealed
step to the same successor.  The event block is `LocalReuse.roundEvents`. -/
theorem fire_replays {r t : Regime} {i j : Nat} {δ : List Item}
    (h : TransStep r i j δ t) :
    replayE (LocalReuse.roundEvents ⟨(i, j), δ⟩) r = some t := by
  rw [LocalReuse.round_replays]
  exact h.2.2.2.2

/-- Every extension step decodes to a sealed event block that replays to
its successor. -/
theorem xstep_replays {r t : Regime} (h : XStep r t) :
    ∃ block : List Event, replayE block r = some t := by
  cases h with
  | grow => exact ⟨[.admitDatum], grow_replays r⟩
  | fire hstep _ => exact ⟨_, fire_replays hstep⟩

theorem good_grow {r : Regime} (hg : Good r) : Good (grow r) :=
  ⟨grow_wf hg.1, hg.2.1, fun q hq => separable_grow (hg.2.2 q hq)⟩

/-- A fire step preserves the invariant: the successor is well-formed,
rule-free, and separates every standing requirement — the old ones by the
validity condition, the new one because the response answered it. -/
theorem good_fire {r t : Regime} {i j : Nat} {δ : List Item}
    (hg : Good r) (hstep : TransStep r i j δ t)
    (hnr : ∀ f, Item.newRuleAll f ∉ δ) : Good t := by
  obtain ⟨hij, hj, _, hvalid, hresp⟩ := hstep
  obtain ⟨_, _, _, happ⟩ := respond_anatomy hresp
  obtain ⟨s, hs, hsep, hall⟩ := hvalid
  have hts : t = { s with reqs := insertNew r.reqs (i, j) } := by
    rw [applyDelta_reqs_free, hs] at happ
    exact (Option.some.inj happ).symm
  have hwf' : ({ r with reqs := insertNew r.reqs (i, j) } : Regime).wf := by
    obtain ⟨hinst, hrule, hreq, hform⟩ := hg.1
    refine ⟨hinst, hrule, ?_, hform⟩
    intro q hq
    rcases mem_insertNew.mp hq with hq | hq
    · exact hreq q hq
    · subst hq
      exact ⟨hij, hj⟩
  refine ⟨applyDelta_wf hwf' happ, ?_, ?_⟩
  · rw [applyDelta_rules hnr happ]
    exact hg.2.1
  · intro q hq
    rw [hts] at hq ⊢
    rw [separable_reqs_irrel]
    rcases mem_insertNew.mp hq with hq | hq
    · exact hall q hq
    · subst hq
      exact hsep

theorem good_xstep {r t : Regime} (hg : Good r) (h : XStep r t) : Good t := by
  cases h with
  | grow => exact good_grow hg
  | fire hstep hnr => exact good_fire hg hstep hnr

/-! ## 5. The productive run -/

/-- The ignition block from `r`: two growth events, the closure demand on
the two fresh data, and the mark response (`mark_progress`). -/
def block (r : Regime) : List Event :=
  [.admitDatum, .admitDatum, .impose r.data (r.data + 1),
   .admitForm 1, .admitInst r.forms.length [r.data + 1]]

/-- The mark response to the fresh pair. -/
def markDelta (r : Regime) : List Item :=
  [.newForm 1, .newInst r.forms.length [r.data + 1]]

/-- The state the block reaches. -/
def blockState (r : Regime) : Regime :=
  ⟨r.data + 2, r.forms ++ [1], r.insts ++ [(r.forms.length, [r.data + 1])],
   r.rules, r.reqs ++ [(r.data, r.data + 1)]⟩

theorem block_eq (r : Regime) :
    block r = [Event.admitDatum, Event.admitDatum]
      ++ LocalReuse.roundEvents ⟨(r.data, r.data + 1), markDelta r⟩ := rfl

theorem two_grows_replays (r : Regime) :
    replayE [Event.admitDatum, Event.admitDatum] r = some (grow (grow r)) := rfl

/-- The fresh pair was never a requirement of a well-formed regime. -/
theorem fresh_pair_not_req {r : Regime} (hwf : r.wf) :
    (r.data, r.data + 1) ∉ r.reqs := by
  intro hmem
  have := (hwf.2.2.1 _ hmem).2
  simp only at this
  omega

/-- The fresh mark instance was never admitted in a well-formed regime. -/
theorem fresh_mark_not_inst {r : Regime} (hwf : r.wf) :
    ((r.forms.length, [r.data + 1]) : Inst) ∉ r.insts := by
  intro hmem
  exact Nat.lt_irrefl _ ((hwf.1 _ hmem).1)

/-- The mark response, applied at the grown state with the demand
recorded, computes to `blockState`. -/
theorem markDelta_applies {r : Regime} (hwf : r.wf) :
    applyDelta { grow (grow r) with reqs := insertNew r.reqs (r.data, r.data + 1) }
      (markDelta r) = some (blockState r) := by
  have hreq : insertNew r.reqs (r.data, r.data + 1) = r.reqs ++ [(r.data, r.data + 1)] :=
    insertNew_of_not_mem (fresh_pair_not_req hwf)
  have h1 : applyItem { grow (grow r) with reqs := insertNew r.reqs (r.data, r.data + 1) }
      (.newForm 1)
      = some ⟨r.data + 2, r.forms ++ [1], r.insts, r.rules,
              insertNew r.reqs (r.data, r.data + 1)⟩ := by
    simp only [applyItem]
    rw [if_pos (Nat.le_refl 1)]
    rfl
  have hcond : r.forms.length < (r.forms ++ [1]).length ∧
      ([r.data + 1] : List Nat).length = (r.forms ++ [1]).getD r.forms.length 0 ∧
      ∀ x ∈ ([r.data + 1] : List Nat), x < r.data + 2 := by
    refine ⟨by simp, ?_, ?_⟩
    · rw [getD_concat_self]
      rfl
    · intro x hx
      have : x = r.data + 1 := List.mem_singleton.mp hx
      subst this
      omega
  have h2 : applyItem (⟨r.data + 2, r.forms ++ [1], r.insts, r.rules,
              insertNew r.reqs (r.data, r.data + 1)⟩ : Regime)
      (.newInst r.forms.length [r.data + 1]) = some (blockState r) := by
    simp only [applyItem]
    rw [if_pos hcond]
    rw [insertNew_of_not_mem (fresh_mark_not_inst hwf)]
    unfold blockState
    rw [hreq]
  unfold markDelta
  rw [applyDelta_pair, h1]
  exact h2

/-- The block's round is a sealed transition: the fresh pair is collapsed,
the mark is a valid response, and the round lands on `blockState`. -/
theorem block_is_transStep {r : Regime} (hg : Good r) :
    TransStep (grow (grow r)) r.data (r.data + 1) (markDelta r) (blockState r) := by
  refine ⟨Nat.lt_succ_self _, by show r.data + 1 < r.data + 1 + 1; omega,
    two_grows_collapsed hg.1, two_grows_response hg.1 hg.2.2, ?_⟩
  unfold respond
  have hstep : stepE (grow (grow r)) (.impose r.data (r.data + 1))
      = some { grow (grow r) with reqs := insertNew r.reqs (r.data, r.data + 1) } := by
    show (if r.data < r.data + 1 ∧ r.data + 1 < r.data + 1 + 1 then _ else _) = _
    rw [if_pos ⟨Nat.lt_succ_self _, by omega⟩]
    rfl
  rw [hstep]
  exact markDelta_applies hg.1

theorem markDelta_rule_free (r : Regime) : ∀ f, Item.newRuleAll f ∉ markDelta r := by
  intro f hf
  rcases List.mem_cons.mp hf with h | h
  · cases h
  · rcases List.mem_cons.mp h with h | h
    · cases h
    · cases h

/-- **The block replays** to `blockState` through the sealed step. -/
theorem block_replays {r : Regime} (hg : Good r) :
    replayE (block r) r = some (blockState r) := by
  rw [block_eq, LocalReuse.replayE_suffix, two_grows_replays]
  exact fire_replays (block_is_transStep hg)

/-- The block is three extension steps: grow, grow, fire. -/
theorem block_is_xsteps {r : Regime} (hg : Good r) :
    XStep r (grow r) ∧ XStep (grow r) (grow (grow r)) ∧
      XStep (grow (grow r)) (blockState r) :=
  ⟨XStep.grow, XStep.grow, XStep.fire (block_is_transStep hg) (markDelta_rule_free r)⟩

theorem blockState_good {r : Regime} (hg : Good r) : Good (blockState r) :=
  good_fire (good_grow (good_grow hg)) (block_is_transStep hg) (markDelta_rule_free r)

/-- **Activity.**  The response changes a verdict: the fresh pair is
collapsed before the round and separated after it. -/
theorem block_is_activity {r : Regime} (hg : Good r) :
    collapsed (grow (grow r)) r.data (r.data + 1) ∧
      separable (blockState r) r.data (r.data + 1) := by
  refine ⟨two_grows_collapsed hg.1, ?_⟩
  obtain ⟨_, _, _, hvalid, _⟩ := block_is_transStep hg
  obtain ⟨s, hs, hsep, _⟩ := hvalid
  have hts : blockState r = { s with reqs := insertNew r.reqs (r.data, r.data + 1) } := by
    have h := markDelta_applies hg.1
    rw [applyDelta_reqs_free, hs] at h
    exact (Option.some.inj h).symm
  rw [hts, separable_reqs_irrel]
  exact hsep

/-- The block is not idle: its endpoint differs from its start. -/
theorem blockState_ne (r : Regime) : blockState r ≠ r := by
  intro h
  have := congrArg Regime.data h
  simp only [blockState] at this
  omega

/-- The iterated run: states and histories. -/
def runState (r : Regime) : Nat → Regime
  | 0 => r
  | k + 1 => blockState (runState r k)

def runHist (r : Regime) : Nat → List Event
  | 0 => []
  | k + 1 => runHist r k ++ block (runState r k)

theorem runState_good {r : Regime} (hg : Good r) : ∀ k, Good (runState r k)
  | 0 => hg
  | k + 1 => blockState_good (runState_good hg k)

/-- **The run replays from any `Good` state, at every horizon.** -/
theorem runHist_replays {r : Regime} (hg : Good r) :
    ∀ k, replayE (runHist r k) r = some (runState r k)
  | 0 => rfl
  | k + 1 => by
      show replayE (runHist r k ++ block (runState r k)) r = some (blockState (runState r k))
      rw [LocalReuse.replayE_suffix, runHist_replays hg k]
      exact block_replays (runState_good hg k)

theorem runHist_prefix (r : Regime) (k : Nat) : runHist r k <+: runHist r (k + 1) :=
  ⟨block (runState r k), rfl⟩

/-- **Productivity**: two data, one form and one requirement per block. -/
theorem runState_data (r : Regime) : ∀ k, (runState r k).data = r.data + 2 * k
  | 0 => rfl
  | k + 1 => by
      show (runState r k).data + 2 = r.data + 2 * (k + 1)
      rw [runState_data r k]
      omega

theorem runState_forms (r : Regime) : ∀ k, (runState r k).forms.length = r.forms.length + k
  | 0 => rfl
  | k + 1 => by
      show ((runState r k).forms ++ [1]).length = r.forms.length + (k + 1)
      simp only [List.length_append, List.length_cons, List.length_nil]
      rw [runState_forms r k]
      omega

theorem runState_reqs (r : Regime) : ∀ k, (runState r k).reqs.length = r.reqs.length + k
  | 0 => rfl
  | k + 1 => by
      show ((runState r k).reqs ++ [((runState r k).data, (runState r k).data + 1)]).length
        = r.reqs.length + (k + 1)
      simp only [List.length_append, List.length_cons, List.length_nil]
      rw [runState_reqs r k]
      omega

/-- The Challenge 2 close of each reading is `Good`, so the run starts
from the sealed towers' own roots. -/
theorem rootL_good : Good ⟨2, [], [], [], []⟩ := by
  refine ⟨?_, rfl, ?_⟩
  · refine ⟨?_, ?_, ?_, ?_⟩ <;> simp
  · intro q hq
    cases hq

theorem rootF_good : Good ⟨3, [], [], [], []⟩ := by
  refine ⟨?_, rfl, ?_⟩
  · refine ⟨?_, ?_, ?_, ?_⟩ <;> simp
  · intro q hq
    cases hq

/-- **Two interpretations of the same static facts.**  From any `Good`
state the idle history and the block are both lawful under the sealed
step; the sealed premises prefer neither.  Excluding the first is the
extension's activity law, and nothing else. -/
theorem idle_and_active_both_lawful {r : Regime} (hg : Good r) :
    replayE [Event.supply 0] r = some r ∧
      replayE (block r) r = some (blockState r) ∧ blockState r ≠ r :=
  ⟨rfl, block_replays hg, blockState_ne r⟩

/-! ## 6. The residual bridge on the actual carrier -/

/-- The admissible slots over `n` data: a hole, or an admitted datum. -/
def slotOptions (n : Nat) : List (Option Nat) := none :: (List.range n).map some

theorem mem_slotOptions {n : Nat} {s : Option Nat} :
    s ∈ slotOptions n ↔ slotOk n s := by
  cases s with
  | none => simp [slotOptions, slotOk]
  | some x => simp [slotOptions, slotOk]

/-- All lists of a given length over a list of options. -/
def tuples {α : Type} (opts : List α) : Nat → List (List α)
  | 0 => [[]]
  | n + 1 => opts.flatMap (fun o => (tuples opts n).map (fun l => o :: l))

theorem mem_tuples {α : Type} (opts : List α) :
    ∀ (n : Nat) (l : List α), l ∈ tuples opts n ↔ l.length = n ∧ ∀ x ∈ l, x ∈ opts
  | 0, l => by
      constructor
      · intro h
        have hl : l = [] := List.mem_singleton.mp h
        subst hl
        exact ⟨rfl, fun x hx => absurd hx List.not_mem_nil⟩
      · rintro ⟨hl, _⟩
        cases l with
        | nil => exact List.mem_singleton.mpr rfl
        | cons a t => exact absurd hl (Nat.succ_ne_zero _)
  | n + 1, l => by
      constructor
      · intro h
        have h' : l ∈ opts.flatMap (fun o => (tuples opts n).map (fun l => o :: l)) := h
        simp only [List.mem_flatMap, List.mem_map] at h'
        obtain ⟨o, ho, l', hl', rfl⟩ := h'
        obtain ⟨hlen, hall⟩ := (mem_tuples opts n l').mp hl'
        refine ⟨by show l'.length + 1 = n + 1; rw [hlen], ?_⟩
        intro x hx
        rcases List.mem_cons.mp hx with rfl | hx
        · exact ho
        · exact hall x hx
      · rintro ⟨hlen, hall⟩
        cases l with
        | nil => exact absurd hlen.symm (Nat.succ_ne_zero n)
        | cons o l' =>
            show o :: l' ∈ opts.flatMap (fun o => (tuples opts n).map (fun l => o :: l))
            simp only [List.mem_flatMap, List.mem_map]
            refine ⟨o, hall o List.mem_cons_self, l', ?_, rfl⟩
            exact (mem_tuples opts n l').mpr
              ⟨Nat.succ.inj hlen, fun x hx => hall x (List.mem_cons_of_mem _ hx)⟩

/-- The finite list of well-formed contexts of a regime. -/
def ctxList (r : Regime) : List Ctx :=
  (List.range r.forms.length).flatMap fun f =>
    ((tuples (slotOptions r.data) (r.forms.getD f 0)).filter
        (fun s => decide (none ∈ s))).map (fun s => ⟨f, s⟩)

theorem mem_ctxList {r : Regime} {c : Ctx} : c ∈ ctxList r ↔ wfCtx r c := by
  unfold ctxList wfCtx
  simp only [List.mem_flatMap, List.mem_range, List.mem_map, List.mem_filter,
    decide_eq_true_eq]
  constructor
  · rintro ⟨f, hf, s, ⟨hs, hhole⟩, rfl⟩
    obtain ⟨hlen, hall⟩ := (mem_tuples _ _ s).mp hs
    exact ⟨hf, hlen, hhole, fun x hx => mem_slotOptions.mp (hall x hx)⟩
  · rintro ⟨hf, hlen, hhole, hok⟩
    exact ⟨c.form, hf, c.slots,
      ⟨(mem_tuples _ _ _).mpr ⟨hlen, fun x hx => mem_slotOptions.mpr (hok x hx)⟩, hhole⟩, rfl⟩

/-- The question asked by one context: is the plug derivable? -/
def question (r : Regime) (c : Ctx) : Nat → Nat :=
  fun d => if derivable r (plug c d) then 1 else 0

/-- The declared question family of a regime: one question per well-formed
context.  This is the profile presentation, as represented data. -/
def questions (r : Regime) : List (Nat → Nat) := (ctxList r).map (question r)

theorem question_eq_iff (r : Regime) (c : Ctx) (d d' : Nat) :
    question r c d = question r c d' ↔
      (derivable r (plug c d) ↔ derivable r (plug c d')) := by
  unfold question
  by_cases h1 : derivable r (plug c d) <;> by_cases h2 : derivable r (plug c d') <;>
    simp [h1, h2]

/-- **Signature agreement is collapse**: the sealed `Compression`
signature equality over the context family is exactly the sealed
observational collapse. -/
theorem sigEq_iff_collapsed (r : Regime) (d d' : Nat) :
    Compression.SigEq (questions r) d d' ↔ collapsed r d d' := by
  constructor
  · intro h c hc
    have hq : question r c ∈ questions r :=
      List.mem_map.mpr ⟨c, mem_ctxList.mpr hc, rfl⟩
    exact (question_eq_iff r c d d').mp (h _ hq)
  · intro h q hq
    obtain ⟨c, hc, rfl⟩ := List.mem_map.mp hq
    exact (question_eq_iff r c d d').mpr (h c (mem_ctxList.mp hc))

/-- The represented carrier: the admitted data by index. -/
def carrier (r : Regime) : List Nat := List.range r.data

/-- **The closure demand is the residual of the profile relative to the
identity comparison**: a pair of admitted data is a demand (distinct and
collapsed) exactly when the signature quotient identifies it and the
identity separates it. -/
theorem demand_iff_residual (r : Regime) {i j : Nat} (hi : i < r.data) (hj : j < r.data) :
    (i ≠ j ∧ collapsed r i j) ↔
      (Compression.pQ (carrier r) (questions r) i = Compression.pQ (carrier r) (questions r) j
        ∧ id i ≠ id j) := by
  have hi' : i ∈ carrier r := List.mem_range.mpr hi
  have hj' : j ∈ carrier r := List.mem_range.mpr hj
  rw [Compression.pQ_exact (carrier r) (questions r) i hi' j hj', sigEq_iff_collapsed]
  exact ⟨fun h => ⟨h.2, h.1⟩, fun h => ⟨h.2, h.1⟩⟩

/-- The same fact as a typed directional residual of the sealed
`PresentationRelativity` module. -/
theorem demand_residual {r : Regime} {i j : Nat} (hi : i < r.data) (hj : j < r.data)
    (hij : i ≠ j) (hcol : collapsed r i j) :
    Nonempty (PresentationRelativity.DirectionalResidual (carrier r)
      (Compression.pQ (carrier r) (questions r)) id) :=
  ⟨⟨i, j, List.mem_range.mpr hi, List.mem_range.mpr hj,
    ((demand_iff_residual r hi hj).mp ⟨hij, hcol⟩).1, hij⟩⟩

/-- **The comparison that produces the demand is not a digest of the
profile**: whenever a collapsed distinct pair exists, no function of the
signature reproduces the identity comparison. -/
theorem identity_not_signature_determined (r : Regime) {i j : Nat}
    (hij : i ≠ j) (hcol : collapsed r i j) :
    ¬ ∃ f : List Nat → Nat, ∀ z, id z = f (Compression.sigList (questions r) z) := by
  rintro ⟨f, hf⟩
  have hs : Compression.sigList (questions r) i = Compression.sigList (questions r) j :=
    (Compression.sigEq_iff_sigList _ _ _).mp ((sigEq_iff_collapsed r i j).mpr hcol)
  apply hij
  show id i = id j
  rw [hf i, hf j, hs]

/-- A collapsed distinct pair means the identity comparison does not
factor through the profile presentation; the sealed
`forced_split_of_factorization_failure` then says every presentation
carrying both must split that pair. -/
theorem demand_refutes_factorization (r : Regime) {i j : Nat}
    (hi : i < r.data) (hj : j < r.data) (hij : i ≠ j) (hcol : collapsed r i j) :
    ¬ Compression.FactorsOn (carrier r) (Compression.pQ (carrier r) (questions r)) id := by
  intro hf
  have hfc := (Compression.factors_iff_fiberConstant _ _ _).mp hf
  exact hij (hfc i (List.mem_range.mpr hi) j (List.mem_range.mpr hj)
    ((demand_iff_residual r hi hj).mp ⟨hij, hcol⟩).1)

theorem sigEq_pair (p q : Nat → Nat) (x y : Nat) :
    Compression.SigEq [p, q] x y ↔ (p x = p y ∧ q x = q y) := by
  constructor
  · intro h
    exact ⟨h p (by simp), h q (by simp)⟩
  · rintro ⟨hp, hq⟩ q' hq'
    rcases List.mem_cons.mp hq' with rfl | hq'
    · exact hp
    · rcases List.mem_cons.mp hq' with rfl | hq'
      · exact hq
      · cases hq'

/-- **The joint presentation has the promised fibers**: on the carrier,
`j x = j y` iff `p x = p y` and `q x = q y`. -/
theorem joint_eq_iff (D : List Nat) (p q : Nat → Nat) {x y : Nat}
    (hx : x ∈ D) (hy : y ∈ D) :
    Compression.pQ D [p, q] x = Compression.pQ D [p, q] y ↔ (p x = p y ∧ q x = q y) := by
  rw [Compression.pQ_exact D [p, q] x hx y hy]
  exact sigEq_pair p q x y

/-- **Idempotence**: repeating the unchanged comparison after taking the
joint partition reproduces the same partition. -/
theorem joint_idempotent (D : List Nat) (p q : Nat → Nat) {x y : Nat}
    (hx : x ∈ D) (hy : y ∈ D) :
    Compression.SigEq [Compression.pQ D [p, q], q] x y ↔ Compression.SigEq [p, q] x y := by
  rw [sigEq_pair, sigEq_pair, joint_eq_iff D p q hx hy]
  constructor
  · rintro ⟨⟨hp, hq⟩, _⟩
    exact ⟨hp, hq⟩
  · rintro ⟨hp, hq⟩
    exact ⟨⟨hp, hq⟩, hq⟩

/-- The partition does not depend on the order of the carrier list. -/
theorem partition_order_free (D D' : List Nat) (Q : List (Nat → Nat))
    (hDD' : ∀ z, z ∈ D ↔ z ∈ D') {x y : Nat} (hx : x ∈ D) (hy : y ∈ D) :
    (Compression.pQ D Q x = Compression.pQ D Q y ↔
      Compression.pQ D' Q x = Compression.pQ D' Q y) := by
  rw [Compression.pQ_exact D Q x hx y hy,
    Compression.pQ_exact D' Q x ((hDD' x).mp hx) y ((hDD' y).mp hy)]

/-- The representative does depend on it: first match. -/
theorem representative_order_dependent :
    Compression.pQ [0, 1] [fun _ => 0] 1 = 0 ∧
      Compression.pQ [1, 0] [fun _ => 0] 1 = 1 := by decide

/-! ## 7. The future factors through the endpoint -/

/-- Two histories reaching one regime have identical continuations: no
continuation can distinguish them, so no route-dependent quantity is
observable from within the sealed carrier. -/
theorem future_factors_through_endpoint {h1 h2 : List Event} {b s : Regime}
    (e1 : replayE h1 b = some s) (e2 : replayE h2 b = some s) (k : List Event) :
    replayE (h1 ++ k) b = replayE (h2 ++ k) b := by
  rw [LocalReuse.replayE_suffix, LocalReuse.replayE_suffix, e1, e2]

/-- The route pair of the merged path-cost family, on the sealed carrier:
commit a rule before or after growing. -/
def routeBase : Regime := ⟨2, [1], [], [], []⟩
def commitEarly : List Event := [.admitRuleAll 0, .admitDatum]
def commitLate : List Event := [.admitDatum, .admitRuleAll 0]

theorem routes_agree : replayE commitEarly routeBase = replayE commitLate routeBase := by
  decide

/-- The span weighting: a rule costs the carrier it ranges over when made. -/
def spanCost (r : Regime) : Event → Nat
  | .admitRuleAll _ => r.data
  | _ => 0

def spanTotal : List Event → Regime → Nat
  | [], _ => 0
  | e :: rest, r =>
      spanCost r e + (match stepE r e with
        | some r' => spanTotal rest r'
        | none => 0)

theorem routes_cost_differ :
    spanTotal commitEarly routeBase = 2 ∧ spanTotal commitLate routeBase = 3 := by
  decide

/-- Every continuation of the two routes agrees: the differing total is
not in the state and cannot be read back by any later history. -/
theorem routes_indistinguishable (k : List Event) :
    replayE (commitEarly ++ k) routeBase = replayE (commitLate ++ k) routeBase :=
  future_factors_through_endpoint (b := routeBase) (s := ⟨3, [1], [], [0], []⟩)
    (by decide) (by decide) k

end Ignition

#print axioms Ignition.inert_history
#print axioms Ignition.idle_lawful
#print axioms Ignition.plug_not_mem_of_unmentioned
#print axioms Ignition.derivable_unmentioned_iff
#print axioms Ignition.collapsed_of_unmentioned_pair
#print axioms Ignition.holeAt_length
#print axioms Ignition.holeAt_getD
#print axioms Ignition.holeAt_map_getD
#print axioms Ignition.plug_holeAt
#print axioms Ignition.wfCtx_holeAt
#print axioms Ignition.collapsed_with_unmentioned_iff
#print axioms Ignition.stepE_grow
#print axioms Ignition.grow_replays
#print axioms Ignition.unmentioned_of_ge
#print axioms Ignition.grow_wf
#print axioms Ignition.separable_grow
#print axioms Ignition.grow_keeps_verdicts
#print axioms Ignition.grow_demand_iff
#print axioms Ignition.collapsed_trans
#print axioms Ignition.grow_at_most_one_demand
#print axioms Ignition.two_grows_collapsed
#print axioms Ignition.two_grows_response
#print axioms Ignition.applyItem_wf
#print axioms Ignition.applyDelta_wf
#print axioms Ignition.applyItem_rules
#print axioms Ignition.applyDelta_rules
#print axioms Ignition.applyItem_reqs_free
#print axioms Ignition.applyDelta_reqs_free
#print axioms Ignition.fire_replays
#print axioms Ignition.xstep_replays
#print axioms Ignition.good_grow
#print axioms Ignition.good_fire
#print axioms Ignition.good_xstep
#print axioms Ignition.block_eq
#print axioms Ignition.two_grows_replays
#print axioms Ignition.fresh_pair_not_req
#print axioms Ignition.fresh_mark_not_inst
#print axioms Ignition.markDelta_applies
#print axioms Ignition.block_is_transStep
#print axioms Ignition.markDelta_rule_free
#print axioms Ignition.block_replays
#print axioms Ignition.block_is_xsteps
#print axioms Ignition.blockState_good
#print axioms Ignition.block_is_activity
#print axioms Ignition.blockState_ne
#print axioms Ignition.runState_good
#print axioms Ignition.runHist_replays
#print axioms Ignition.runHist_prefix
#print axioms Ignition.runState_data
#print axioms Ignition.runState_forms
#print axioms Ignition.runState_reqs
#print axioms Ignition.rootL_good
#print axioms Ignition.rootF_good
#print axioms Ignition.idle_and_active_both_lawful
#print axioms Ignition.mem_slotOptions
#print axioms Ignition.mem_tuples
#print axioms Ignition.mem_ctxList
#print axioms Ignition.question_eq_iff
#print axioms Ignition.sigEq_iff_collapsed
#print axioms Ignition.demand_iff_residual
#print axioms Ignition.demand_residual
#print axioms Ignition.identity_not_signature_determined
#print axioms Ignition.demand_refutes_factorization
#print axioms Ignition.sigEq_pair
#print axioms Ignition.joint_eq_iff
#print axioms Ignition.joint_idempotent
#print axioms Ignition.partition_order_free
#print axioms Ignition.representative_order_dependent
#print axioms Ignition.future_factors_through_endpoint
#print axioms Ignition.routes_agree
#print axioms Ignition.routes_cost_differ
#print axioms Ignition.routes_indistinguishable
