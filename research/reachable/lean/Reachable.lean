import Derivation.Basic
import Derivation.Inertia
import Derivation.Minimality
import Derivation.Rounds
import Derivation.RuleBridge
import Derivation.TransitionTransport

/-!
Reachability under demand and minimum response, over the sealed definitions.

A state is reachable when it is a tower root or follows a reachable state by
one supply (a fresh datum) or one round: a collapsed target, a valid response
that is shortest inside the declared candidate space, and the recorded
successor.  Four invariants hold of every reachable state: no rule is ever
admitted, well-formedness is kept, every standing requirement is answered,
and every admitted form carries an instance.  Two well-formed
states inside the bounds are then shown unreachable.

The round relation quantifies over every shortest valid response.  Orbit
selection, the isomorphism quotient and the resource guards are not
formalized here, and no Python engine refinement is claimed: that the
engine's accepted responses are shortest valid responses is checked
computationally, edge by edge, by the census.  AuthorityEffect: None.
-/

namespace Reachable

open Derivation

/-! ## 1. The candidate space, minimum responses, and reachability -/

/-- The declared candidate space: at most two items, every new form of arity
at most two. -/
def InBounds (δ : List Item) : Prop :=
  δ.length ≤ 2 ∧ ∀ a, Item.newForm a ∈ δ → a ≤ 2

/-- A shortest valid response inside the candidate space.  Both declared
measures order first by item count, so every response the engine accepts
is one of these. -/
def MinResponse (r : Regime) (i j : Nat) (δ : List Item) : Prop :=
  InBounds δ ∧ validResponse r i j δ ∧
    ∀ δ', InBounds δ' → validResponse r i j δ' → δ.length ≤ δ'.length

/-- One accepted round with a shortest response: the sealed transition
relation restricted to minimum responses. -/
def MinStep (r : Regime) (i j : Nat) (δ : List Item) (s : Regime) : Prop :=
  TransStep r i j δ s ∧ MinResponse r i j δ

/-- Reachability from a root by supplies and minimum rounds. -/
inductive Reach (root : Regime) : Regime → Prop where
  | refl : Reach root root
  | supply {s t : Regime} :
      Reach root s → stepE s .admitDatum = some t → Reach root t
  | round {s t : Regime} {i j : Nat} {δ : List Item} :
      Reach root s → MinStep s i j δ t → Reach root t

/-- The two tower roots: the Challenge 2 close of each reading, before the
first demand is imposed. -/
def rootL : Regime := ⟨2, [], [], [], []⟩
def rootF : Regime := ⟨3, [], [], [], []⟩

theorem rootL_wf : rootL.wf := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [rootL]

theorem rootF_wf : rootF.wf := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [rootF]

/-! ## 2. Item-level bookkeeping -/

theorem getD_append_lt : ∀ (l : List Nat) (a i : Nat), i < l.length →
    (l ++ [a]).getD i 0 = l.getD i 0
  | [], _, _, h => absurd h (Nat.not_lt_zero _)
  | _ :: _, _, 0, _ => rfl
  | _ :: t, a, i + 1, h => getD_append_lt t a i (Nat.lt_of_succ_lt_succ h)

theorem applyItem_newDatum {r s : Regime}
    (h : applyItem r Item.newDatum = some s) :
    s = { r with data := r.data + 1 } :=
  (Option.some.inj h).symm

theorem applyItem_newForm {r s : Regime} {a : Nat}
    (h : applyItem r (Item.newForm a) = some s) :
    1 ≤ a ∧ s = { r with forms := r.forms ++ [a] } := by
  simp only [applyItem] at h
  split at h
  next ha => exact ⟨ha, (Option.some.inj h).symm⟩
  next => exact nomatch h

theorem applyItem_newInst {r s : Regime} {f : Nat} {args : List Nat}
    (h : applyItem r (Item.newInst f args) = some s) :
    (f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
        ∀ x ∈ args, x < r.data) ∧
      s = { r with insts := insertNew r.insts (f, args) } := by
  simp only [applyItem] at h
  split at h
  next hg => exact ⟨hg, (Option.some.inj h).symm⟩
  next => exact nomatch h

theorem applyItem_no_rule_rules {r s : Regime} {it : Item}
    (hne : ∀ f, it ≠ Item.newRuleAll f) (h : applyItem r it = some s) :
    s.rules = r.rules := by
  cases it with
  | newDatum =>
    injection h with h
    subst h
    rfl
  | newForm a =>
    simp only [applyItem] at h
    split at h
    · injection h with h
      subst h
      rfl
    · exact nomatch h
  | newInst f args =>
    simp only [applyItem] at h
    split at h
    · injection h with h
      subst h
      rfl
    · exact nomatch h
  | newRuleAll f => exact absurd rfl (hne f)

theorem applyDelta_no_rule_rules {δ : List Item} :
    ∀ {r s : Regime}, (∀ f, Item.newRuleAll f ∉ δ) →
      applyDelta r δ = some s → s.rules = r.rules := by
  induction δ with
  | nil =>
    intro r s _ h
    injection h with h
    subst h
    rfl
  | cons it rest ih =>
    intro r s hno h
    rw [applyDelta_cons] at h
    cases happ : applyItem r it with
    | none =>
      rw [happ] at h
      exact nomatch h
    | some r1 =>
      rw [happ] at h
      have hne : ∀ f, it ≠ Item.newRuleAll f :=
        fun f he => hno f (he ▸ List.mem_cons_self)
      have hrest : ∀ f, Item.newRuleAll f ∉ rest :=
        fun f hm => hno f (List.mem_cons_of_mem _ hm)
      exact (ih hrest h).trans (applyItem_no_rule_rules hne happ)

theorem applyItem_not_form {r s : Regime} {it : Item}
    (hne : ∀ a, it ≠ Item.newForm a) (h : applyItem r it = some s) :
    s.forms = r.forms ∧ ∀ p ∈ r.insts, p ∈ s.insts := by
  cases it with
  | newDatum =>
    injection h with h
    subst h
    exact ⟨rfl, fun p hp => hp⟩
  | newForm a => exact absurd rfl (hne a)
  | newInst f args =>
    simp only [applyItem] at h
    split at h
    · injection h with h
      subst h
      exact ⟨rfl, fun p hp => mem_insertNew.mpr (Or.inl hp)⟩
    · exact nomatch h
  | newRuleAll f =>
    simp only [applyItem] at h
    split at h
    · injection h with h
      subst h
      exact ⟨rfl, fun p hp => hp⟩
    · exact nomatch h

theorem mem_dropRules {x : Item} : ∀ {δ : List Item}, x ∈ dropRules δ → x ∈ δ := by
  intro δ
  induction δ with
  | nil =>
    intro h
    exact nomatch h
  | cons it rest ih =>
    intro h
    cases it with
    | newRuleAll f => exact List.mem_cons_of_mem _ (ih h)
    | newDatum =>
      rcases List.mem_cons.mp h with he | hm
      · exact he ▸ List.mem_cons_self
      · exact List.mem_cons_of_mem _ (ih hm)
    | newForm a =>
      rcases List.mem_cons.mp h with he | hm
      · exact he ▸ List.mem_cons_self
      · exact List.mem_cons_of_mem _ (ih hm)
    | newInst f args =>
      rcases List.mem_cons.mp h with he | hm
      · exact he ▸ List.mem_cons_self
      · exact List.mem_cons_of_mem _ (ih hm)

theorem inBounds_dropRules {δ : List Item} (h : InBounds δ) :
    InBounds (dropRules δ) :=
  ⟨Nat.le_trans (dropRules_length_le δ) h.1,
    fun a ha => h.2 a (mem_dropRules ha)⟩

theorem inBounds_nil : InBounds [] :=
  ⟨Nat.zero_le _, fun _ h => nomatch h⟩

theorem inBounds_single {it : Item} (hne : ∀ a, it ≠ Item.newForm a) :
    InBounds [it] := by
  refine ⟨by show 1 ≤ 2; decide, fun a h => ?_⟩
  have he := List.mem_singleton.mp h
  exact absurd he.symm (hne a)

/-- A shortest response carries no uniform-rule item: dropping the rule
items leaves a valid response that is strictly shorter and still inside the
bounds. -/
theorem minResponse_no_rule {r : Regime} {i j : Nat} {δ : List Item}
    (h : MinResponse r i j δ) : ∀ f, Item.newRuleAll f ∉ δ := by
  intro f hf
  obtain ⟨hb, hv, hmin⟩ := h
  obtain ⟨hv', hlt, _⟩ := rule_item_never_minimal hf hv
  have hle := hmin (dropRules δ) (inBounds_dropRules hb) hv'
  omega

/-! ## 3. Invariant (a): no reachable state carries a rule -/

theorem transStep_applyDelta {r s : Regime} {i j : Nat} {δ : List Item}
    (h : respond r i j δ = some s) :
    applyDelta { r with reqs := insertNew r.reqs (i, j) } δ = some s :=
  (respond_anatomy h).2.2.2

theorem reach_rules {root t : Regime} (h : Reach root t) :
    t.rules = root.rules := by
  induction h with
  | refl => rfl
  | supply _ hstep ih =>
    have ht := Option.some.inj hstep
    rw [← ht]
    exact ih
  | round _ hmin ih =>
    obtain ⟨hts, hmr⟩ := hmin
    have happ := transStep_applyDelta hts.2.2.2.2
    have hrules := applyDelta_no_rule_rules (minResponse_no_rule hmr) happ
    exact hrules.trans ih

/-! ## 4. Invariant (b): well-formedness is kept -/

theorem wf_admitDatum {r : Regime} (h : r.wf) :
    ({ r with data := r.data + 1 } : Regime).wf := by
  obtain ⟨hi, hr, hq, hf⟩ := h
  refine ⟨?_, hr, ?_, hf⟩
  · intro p hp
    obtain ⟨h1, h2, h3⟩ := hi p hp
    exact ⟨h1, h2, fun a ha => Nat.lt_succ_of_lt (h3 a ha)⟩
  · intro q hq'
    obtain ⟨h1, h2⟩ := hq q hq'
    exact ⟨h1, Nat.lt_succ_of_lt h2⟩

theorem wf_applyItem {r s : Regime} {it : Item} (h : r.wf)
    (happ : applyItem r it = some s) : s.wf := by
  obtain ⟨hi, hr, hq, hf⟩ := h
  cases it with
  | newDatum =>
    injection happ with happ
    subst happ
    exact wf_admitDatum ⟨hi, hr, hq, hf⟩
  | newForm a =>
    simp only [applyItem] at happ
    split at happ
    next ha =>
      injection happ with happ
      subst happ
      refine ⟨?_, ?_, hq, ?_⟩
      · intro p hp
        obtain ⟨h1, h2, h3⟩ := hi p hp
        refine ⟨?_, ?_, h3⟩
        · show p.1 < (r.forms ++ [a]).length
          rw [List.length_append]
          omega
        · show p.2.length = (r.forms ++ [a]).getD p.1 0
          rw [getD_append_lt r.forms a p.1 h1]
          exact h2
      · intro f hf'
        show f < (r.forms ++ [a]).length
        rw [List.length_append]
        have := hr f hf'
        omega
      · intro b hb
        rcases List.mem_append.mp hb with hb | hb
        · exact hf b hb
        · rw [List.mem_singleton.mp hb]
          exact ha
    next => exact nomatch happ
  | newInst f args =>
    simp only [applyItem] at happ
    split at happ
    next hg =>
      injection happ with happ
      subst happ
      refine ⟨?_, hr, hq, hf⟩
      intro p hp
      rcases mem_insertNew.mp hp with hp | hp
      · exact hi p hp
      · subst hp
        exact hg
    next => exact nomatch happ
  | newRuleAll f =>
    simp only [applyItem] at happ
    split at happ
    next hg =>
      injection happ with happ
      subst happ
      refine ⟨hi, ?_, hq, hf⟩
      intro g hg'
      rcases mem_insertNew.mp hg' with hg' | hg'
      · exact hr g hg'
      · subst hg'
        exact hg
    next => exact nomatch happ

theorem wf_applyDelta {δ : List Item} :
    ∀ {r s : Regime}, r.wf → applyDelta r δ = some s → s.wf := by
  induction δ with
  | nil =>
    intro r s h happ
    injection happ with happ
    subst happ
    exact h
  | cons it rest ih =>
    intro r s h happ
    rw [applyDelta_cons] at happ
    cases hit : applyItem r it with
    | none =>
      rw [hit] at happ
      exact nomatch happ
    | some r1 =>
      rw [hit] at happ
      exact ih (wf_applyItem h hit) happ

theorem wf_impose {r : Regime} (h : r.wf) {i j : Nat} (hij : i < j)
    (hj : j < r.data) :
    ({ r with reqs := insertNew r.reqs (i, j) } : Regime).wf := by
  obtain ⟨hi, hr, hq, hf⟩ := h
  refine ⟨hi, hr, ?_, hf⟩
  intro q hq'
  rcases mem_insertNew.mp hq' with hq' | hq'
  · exact hq q hq'
  · subst hq'
    exact ⟨hij, hj⟩

theorem wf_respond {r s : Regime} {i j : Nat} {δ : List Item} (h : r.wf)
    (hresp : respond r i j δ = some s) : s.wf := by
  obtain ⟨hij, hj, _, happ⟩ := respond_anatomy hresp
  exact wf_applyDelta (wf_impose h hij hj) happ

theorem reach_wf {root t : Regime} (h : Reach root t) (hw : root.wf) :
    t.wf := by
  induction h with
  | refl => exact hw
  | supply _ hstep ih =>
    have ht := Option.some.inj hstep
    rw [← ht]
    exact wf_admitDatum ih
  | round _ hmin ih => exact wf_respond ih hmin.1.2.2.2.2

/-! ## 5. Invariant (c): every standing requirement is answered -/

/-- Every imposed requirement is separated in the state itself. -/
def Answered (r : Regime) : Prop := ∀ q ∈ r.reqs, separable r q.1 q.2

/-- Separability never reads the requirement store. -/
theorem separable_reqs (r : Regime) (q : List (Nat × Nat)) (d d' : Nat) :
    separable { r with reqs := q } d d' ↔ separable r d d' :=
  Iff.rfl

theorem applyItem_reqs_free (r : Regime) (q : List (Nat × Nat)) (it : Item) :
    applyItem { r with reqs := q } it =
      (applyItem r it).map (fun u => { u with reqs := q }) := by
  cases it with
  | newDatum => rfl
  | newForm a =>
    by_cases h : 1 ≤ a
    · simp [applyItem, h]
    · simp [applyItem, h]
  | newInst f args =>
    by_cases h : f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
        ∀ x ∈ args, x < r.data
    · simp [applyItem, h]
    · simp [applyItem, h]
  | newRuleAll f =>
    by_cases h : f < r.forms.length
    · simp [applyItem, h]
    · simp [applyItem, h]

theorem applyDelta_reqs_free (q : List (Nat × Nat)) :
    ∀ (δ : List Item) (r : Regime),
      applyDelta { r with reqs := q } δ =
        (applyDelta r δ).map (fun u => { u with reqs := q })
  | [], _ => rfl
  | it :: rest, r => by
    rw [applyDelta_cons, applyDelta_cons, applyItem_reqs_free]
    cases applyItem r it with
    | none => rfl
    | some r1 => exact applyDelta_reqs_free q rest r1

theorem answered_of_transStep {r s : Regime} {i j : Nat} {δ : List Item}
    (h : TransStep r i j δ s) : Answered s := by
  obtain ⟨_, _, _, hv, hresp⟩ := h
  obtain ⟨s', happ', hsep, hall⟩ := hv
  obtain ⟨_, _, hreqs, happ⟩ := respond_anatomy hresp
  rw [applyDelta_reqs_free, happ'] at happ
  have hs : s = { s' with reqs := insertNew r.reqs (i, j) } :=
    (Option.some.inj happ).symm
  intro q hq
  rw [hreqs] at hq
  rcases mem_insertNew.mp hq with hq | hq
  · rw [hs]
    exact (separable_reqs _ _ _ _).mpr (hall q hq)
  · subst hq
    rw [hs]
    exact (separable_reqs _ _ _ _).mpr hsep

theorem separable_addDatum {r : Regime} {d d' : Nat} (h : separable r d d') :
    separable { r with data := r.data + 1 } d d' := by
  obtain ⟨c, ⟨h1, h2, h3, h4⟩, hne⟩ := h
  refine ⟨c, ⟨h1, h2, h3, ?_⟩, hne⟩
  intro s hs
  have hs' := h4 s hs
  cases s with
  | none => trivial
  | some x => exact Nat.lt_succ_of_lt hs'

theorem answered_supply {r s : Regime} (h : Answered r)
    (hstep : stepE r .admitDatum = some s) : Answered s := by
  have hs := Option.some.inj hstep
  rw [← hs]
  intro q hq
  exact separable_addDatum (h q hq)

theorem reach_answered {root t : Regime} (h : Reach root t)
    (ha : Answered root) : Answered t := by
  induction h with
  | refl => exact ha
  | supply _ hstep ih => exact answered_supply ih hstep
  | round _ hmin _ => exact answered_of_transStep hmin.1

/-- Every ordered pair of admitted data has been explicitly demanded.
This is stronger than reaching a closure fixpoint: one response can also
separate pairs that were never demanded. -/
def AllPairsDemanded (r : Regime) : Prop :=
  ∀ i j, i < j → j < r.data → (i, j) ∈ r.reqs

/-- The observational condition at a closure fixpoint: every admitted pair
has a separating witness. The Python census decides this with the sealed
collapsed-pair enumerator. -/
def Fixpoint (r : Regime) : Prop :=
  ∀ i j, i < j → j < r.data → separable r i j

theorem answered_allPairsDemanded_fixpoint {t : Regime} (ha : Answered t)
    (hf : AllPairsDemanded t) : Fixpoint t :=
  fun i j hij hj => ha (i, j) (hf i j hij hj)

/-- A witnessed fixpoint has no collapsed admitted pair. -/
theorem fixpoint_no_collapsed {t : Regime} (hf : Fixpoint t) :
    ∀ i j, i < j → j < t.data → ¬ collapsed t i j :=
  fun i j hij hj => separable_not_collapsed (hf i j hij hj)

theorem rootL_answered : Answered rootL := fun _ hq => nomatch hq
theorem rootF_answered : Answered rootF := fun _ hq => nomatch hq

/-- Reaching a state in which every pair has been demanded suffices for a
closure fixpoint. The converse is not claimed. -/
theorem reach_allPairsDemanded_fixpoint {root t : Regime} (h : Reach root t)
    (ha : Answered root) (hf : AllPairsDemanded t) : Fixpoint t :=
  answered_allPairsDemanded_fixpoint (reach_answered h ha) hf

/-! ## 6. Invariant (d): every admitted form carries an instance -/

/-- Every admitted form index occurs in some admitted instance. -/
def FormsUsed (r : Regime) : Prop :=
  ∀ f, f < r.forms.length → ∃ p ∈ r.insts, p.1 = f

/-- Appending a form that no instance and no rule names changes no
separability verdict: the contexts over the new form are underivable on
both sides, and every other context is unchanged. -/
theorem separable_appendForm {r : Regime} (hwf : r.wf) (a d d' : Nat) :
    separable { r with forms := r.forms ++ [a] } d d' ↔ separable r d d' := by
  constructor
  · rintro ⟨c, ⟨h1, h2, h3, h4⟩, hne⟩
    have hlen : c.form < r.forms.length + 1 := by
      have h1' : c.form < (r.forms ++ [a]).length := h1
      rw [List.length_append] at h1'
      simpa using h1'
    rcases Nat.lt_or_ge c.form r.forms.length with hlt | hge
    · refine ⟨c, ⟨hlt, ?_, h3, h4⟩, hne⟩
      have h2' : c.slots.length = (r.forms ++ [a]).getD c.form 0 := h2
      rw [getD_append_lt r.forms a c.form hlt] at h2'
      exact h2'
    · exfalso
      have heq : c.form = r.forms.length := by omega
      apply hne
      have hnot : ∀ x, ¬ derivable { r with forms := r.forms ++ [a] } (plug c x) := by
        intro x hx
        unfold derivable at hx
        rcases hx with hx | hx
        · have hlt := (hwf.1 _ hx).1
          change c.form < r.forms.length at hlt
          omega
        · have hlt := hwf.2.1 _ hx
          change c.form < r.forms.length at hlt
          omega
      exact ⟨fun h => absurd h (hnot d), fun h => absurd h (hnot d')⟩
  · rintro ⟨c, ⟨h1, h2, h3, h4⟩, hne⟩
    refine ⟨c, ⟨?_, ?_, h3, h4⟩, hne⟩
    · show c.form < (r.forms ++ [a]).length
      rw [List.length_append]
      omega
    · show c.slots.length = (r.forms ++ [a]).getD c.form 0
      rw [getD_append_lt r.forms a c.form h1]
      exact h2

theorem formsUsed_of_not_form {r s : Regime} {it : Item}
    (hne : ∀ a, it ≠ Item.newForm a) (h : applyItem r it = some s)
    (hfu : FormsUsed r) : FormsUsed s := by
  obtain ⟨hforms, hinsts⟩ := applyItem_not_form hne h
  intro f hf
  rw [hforms] at hf
  obtain ⟨p, hp, hpf⟩ := hfu f hf
  exact ⟨p, hinsts p hp, hpf⟩

/-- The two-item case whose first item is not a form: a form as the second
item is unused and the first item alone is a shorter valid response;
otherwise no form is added at all. -/
theorem formsUsed_pair_not_form {r r1 s : Regime} {i j : Nat} {it it2 : Item}
    (hwf1 : r1.wf) (hne1 : ∀ a, it ≠ Item.newForm a)
    (h1 : applyItem r it = some r1) (h2 : applyItem r1 it2 = some s)
    (hfu1 : FormsUsed r1) (hsep : separable s i j)
    (hall : ∀ q ∈ r.reqs, separable s q.1 q.2)
    (hmn : ∀ δ', InBounds δ' → validResponse r i j δ' → 2 ≤ δ'.length) :
    FormsUsed s := by
  cases it2 with
  | newForm a =>
    exfalso
    obtain ⟨_, hs2⟩ := applyItem_newForm h2
    subst hs2
    have hv' : validResponse r i j [it] :=
      ⟨r1, by rw [applyDelta_single]; exact h1,
        (separable_appendForm hwf1 a i j).mp hsep,
        fun q hq => (separable_appendForm hwf1 a q.1 q.2).mp (hall q hq)⟩
    have := hmn [it] (inBounds_single hne1) hv'
    simp at this
  | newDatum => exact formsUsed_of_not_form (fun _ h => by cases h) h2 hfu1
  | newInst f args => exact formsUsed_of_not_form (fun _ h => by cases h) h2 hfu1
  | newRuleAll g => exact formsUsed_of_not_form (fun _ h => by cases h) h2 hfu1

/-- A shortest response inside the bounds never leaves a form without an
instance.  The case analysis follows the item count: a lone new form
separates nothing, so the empty response is valid and shorter; a new form
followed by an item that does not use it can be dropped, again leaving a
shorter valid response; the only survivor is a new form followed by an
instance of that very form. -/
theorem minResponse_formsUsed {r s : Regime} {i j : Nat} {δ : List Item}
    (hwf : r.wf) (hfu : FormsUsed r) (hmin : MinResponse r i j δ)
    (happ : applyDelta r δ = some s) : FormsUsed s := by
  have hno := minResponse_no_rule hmin
  obtain ⟨⟨hlen, _⟩, hv, hmn⟩ := hmin
  rcases δ with _ | ⟨it, _ | ⟨it2, _ | ⟨it3, rest⟩⟩⟩
  · -- the empty response
    injection happ with happ
    subst happ
    exact hfu
  · -- one item
    rw [applyDelta_single] at happ
    cases it with
    | newForm a =>
      exfalso
      obtain ⟨s1, hs1, hsep, hall⟩ := hv
      rw [applyDelta_single] at hs1
      obtain ⟨_, rfl⟩ := applyItem_newForm hs1
      have hv' : validResponse r i j [] :=
        ⟨r, rfl, (separable_appendForm hwf a i j).mp hsep,
          fun q hq => (separable_appendForm hwf a q.1 q.2).mp (hall q hq)⟩
      have := hmn [] inBounds_nil hv'
      simp at this
    | newDatum => exact formsUsed_of_not_form (fun _ h => by cases h) happ hfu
    | newInst f args => exact formsUsed_of_not_form (fun _ h => by cases h) happ hfu
    | newRuleAll g => exact formsUsed_of_not_form (fun _ h => by cases h) happ hfu
  · -- two items
    rw [applyDelta_pair] at happ
    cases h1 : applyItem r it with
    | none =>
      rw [h1] at happ
      exact nomatch happ
    | some r1 =>
      rw [h1] at happ
      have h2 : applyItem r1 it2 = some s := happ
      have hwf1 : r1.wf := wf_applyItem hwf h1
      obtain ⟨s1, hs1, hsep, hall⟩ := hv
      rw [applyDelta_pair, h1] at hs1
      have hs1' : applyItem r1 it2 = some s1 := hs1
      have hss : s1 = s := Option.some.inj (hs1'.symm.trans h2)
      subst hss
      have hmn2 : ∀ δ', InBounds δ' → validResponse r i j δ' → 2 ≤ δ'.length :=
        fun δ' hb hv' => hmn δ' hb hv'
      cases it with
      | newForm a =>
        obtain ⟨_, hr1⟩ := applyItem_newForm h1
        subst hr1
        cases it2 with
        | newDatum =>
          exfalso
          have hs2 := applyItem_newDatum h2
          subst hs2
          have hsd : ({ r with data := r.data + 1 } : Regime).wf :=
            wf_admitDatum hwf
          have hkey : ∀ x y,
              separable ⟨r.data + 1, r.forms ++ [a], r.insts, r.rules, r.reqs⟩ x y →
                separable { r with data := r.data + 1 } x y :=
            fun x y hxy => (separable_appendForm hsd a x y).mp hxy
          have hv' : validResponse r i j [Item.newDatum] :=
            ⟨{ r with data := r.data + 1 }, rfl, hkey i j hsep,
              fun q hq => hkey q.1 q.2 (hall q hq)⟩
          have := hmn2 [Item.newDatum]
            (inBounds_single (fun _ h => by cases h)) hv'
          simp at this
        | newForm b =>
          exfalso
          obtain ⟨_, hs2⟩ := applyItem_newForm h2
          subst hs2
          have hwfa : ({ r with forms := r.forms ++ [a] } : Regime).wf :=
            wf_applyItem hwf h1
          have hkey : ∀ x y,
              separable { r with forms := (r.forms ++ [a]) ++ [b] } x y →
                separable r x y :=
            fun x y hxy => (separable_appendForm hwf a x y).mp
              ((separable_appendForm hwfa b x y).mp hxy)
          have hv' : validResponse r i j [] :=
            ⟨r, rfl, hkey i j hsep, fun q hq => hkey q.1 q.2 (hall q hq)⟩
          have := hmn2 [] inBounds_nil hv'
          simp at this
        | newInst f args =>
          obtain ⟨hg, hs2⟩ := applyItem_newInst h2
          subst hs2
          have hg1 : f < (r.forms ++ [a]).length := hg.1
          have hg2 : args.length = (r.forms ++ [a]).getD f 0 := hg.2.1
          have hg3 : ∀ x ∈ args, x < r.data := hg.2.2
          by_cases hfl : f < r.forms.length
          · exfalso
            have hg' : f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
                ∀ x ∈ args, x < r.data :=
              ⟨hfl, by rw [← getD_append_lt r.forms a f hfl]; exact hg2, hg3⟩
            have hap : applyItem r (Item.newInst f args) =
                some { r with insts := insertNew r.insts (f, args) } := by
              simp only [applyItem, if_pos hg']
            have hwf2 : ({ r with insts := insertNew r.insts (f, args) } : Regime).wf :=
              wf_applyItem hwf hap
            have hkey : ∀ x y,
                separable ⟨r.data, r.forms ++ [a], insertNew r.insts (f, args),
                  r.rules, r.reqs⟩ x y →
                  separable { r with insts := insertNew r.insts (f, args) } x y :=
              fun x y hxy => (separable_appendForm hwf2 a x y).mp hxy
            have hv' : validResponse r i j [Item.newInst f args] :=
              ⟨{ r with insts := insertNew r.insts (f, args) },
                by rw [applyDelta_single]; exact hap, hkey i j hsep,
                fun q hq => hkey q.1 q.2 (hall q hq)⟩
            have := hmn2 [Item.newInst f args]
              (inBounds_single (fun _ h => by cases h)) hv'
            simp at this
          · have hfeq : f = r.forms.length := by
              rw [List.length_append] at hg1
              simp at hg1
              omega
            intro g hgl
            have hgl' : g < (r.forms ++ [a]).length := hgl
            rw [List.length_append] at hgl'
            simp at hgl'
            rcases Nat.lt_or_ge g r.forms.length with hlt | hge
            · obtain ⟨p, hp, hpf⟩ := hfu g hlt
              exact ⟨p, mem_insertNew.mpr (Or.inl hp), hpf⟩
            · refine ⟨(f, args), mem_insertNew.mpr (Or.inr rfl), ?_⟩
              show f = g
              omega
        | newRuleAll g =>
          exact absurd (List.mem_cons_of_mem _ List.mem_cons_self) (hno g)
      | newDatum =>
        exact formsUsed_pair_not_form hwf1 (fun _ h => by cases h) h1 h2
          (formsUsed_of_not_form (fun _ h => by cases h) h1 hfu) hsep hall hmn2
      | newInst f args =>
        exact formsUsed_pair_not_form hwf1 (fun _ h => by cases h) h1 h2
          (formsUsed_of_not_form (fun _ h => by cases h) h1 hfu) hsep hall hmn2
      | newRuleAll g =>
        exact formsUsed_pair_not_form hwf1 (fun _ h => by cases h) h1 h2
          (formsUsed_of_not_form (fun _ h => by cases h) h1 hfu) hsep hall hmn2
  · -- three or more items: outside the bounds
    exfalso
    simp only [List.length_cons] at hlen
    omega

theorem reach_formsUsed {root t : Regime} (h : Reach root t) (hw : root.wf)
    (hfu : FormsUsed root) : FormsUsed t := by
  induction h with
  | refl => exact hfu
  | supply _ hstep ih =>
    have ht := Option.some.inj hstep
    rw [← ht]
    exact ih
  | @round s t i j δ hreach hmin ih =>
    have hwfs : s.wf := reach_wf hreach hw
    obtain ⟨hts, hmr⟩ := hmin
    obtain ⟨s', happ', _, _⟩ := hmr.2.1
    have hfs' : FormsUsed s' := minResponse_formsUsed hwfs ih hmr happ'
    have happ := transStep_applyDelta hts.2.2.2.2
    rw [applyDelta_reqs_free, happ'] at happ
    have ht : t = { s' with reqs := insertNew s.reqs (i, j) } :=
      (Option.some.inj happ).symm
    rw [ht]
    exact hfs'

theorem rootL_formsUsed : FormsUsed rootL :=
  fun f hf => absurd hf (Nat.not_lt_zero f)

theorem rootF_formsUsed : FormsUsed rootF :=
  fun f hf => absurd hf (Nat.not_lt_zero f)

/-! ## 7. Two unreachable states inside the bounds -/

/-- A form admitted without any instance.  Well-formed, rule-free, one form
of arity one, and the Challenge 3 demand standing. -/
def formNoInst : Regime := ⟨2, [1], [], [], [(0, 1)]⟩

theorem formNoInst_wf : formNoInst.wf := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [formNoInst]

theorem formNoInst_rule_free : formNoInst.rules = [] := rfl

theorem formNoInst_arities : ∀ a ∈ formNoInst.forms, a ≤ 2 := by decide

theorem formNoInst_not_formsUsed : ¬ FormsUsed formNoInst := by
  intro h
  obtain ⟨p, hp, _⟩ := h 0 (by decide)
  exact nomatch hp

/-- The form-without-instance state is reachable from neither root. -/
theorem formNoInst_unreachable :
    ¬ Reach rootL formNoInst ∧ ¬ Reach rootF formNoInst :=
  ⟨fun h => formNoInst_not_formsUsed (reach_formsUsed h rootL_wf rootL_formsUsed),
   fun h => formNoInst_not_formsUsed (reach_formsUsed h rootF_wf rootF_formsUsed)⟩

/-- The unary mark with its form promoted to a uniform rule.  Well-formed and
inside the bounds, but it carries a rule. -/
def ruledMark : Regime := ⟨2, [1], [(0, [0])], [0], [(0, 1)]⟩

theorem ruledMark_wf : ruledMark.wf := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [ruledMark]

theorem ruledMark_rules_ne : ruledMark.rules ≠ [] := by decide

/-- The ruled mark is reachable from neither root. -/
theorem ruledMark_unreachable :
    ¬ Reach rootL ruledMark ∧ ¬ Reach rootF ruledMark :=
  ⟨fun h => ruledMark_rules_ne (reach_rules h),
   fun h => ruledMark_rules_ne (reach_rules h)⟩

end Reachable

#print axioms Reachable.rootL_wf
#print axioms Reachable.rootF_wf
#print axioms Reachable.getD_append_lt
#print axioms Reachable.applyItem_newDatum
#print axioms Reachable.applyItem_newForm
#print axioms Reachable.applyItem_newInst
#print axioms Reachable.applyItem_no_rule_rules
#print axioms Reachable.applyDelta_no_rule_rules
#print axioms Reachable.applyItem_not_form
#print axioms Reachable.mem_dropRules
#print axioms Reachable.inBounds_dropRules
#print axioms Reachable.inBounds_nil
#print axioms Reachable.inBounds_single
#print axioms Reachable.minResponse_no_rule
#print axioms Reachable.transStep_applyDelta
#print axioms Reachable.reach_rules
#print axioms Reachable.wf_admitDatum
#print axioms Reachable.wf_applyItem
#print axioms Reachable.wf_applyDelta
#print axioms Reachable.wf_impose
#print axioms Reachable.wf_respond
#print axioms Reachable.reach_wf
#print axioms Reachable.separable_reqs
#print axioms Reachable.applyItem_reqs_free
#print axioms Reachable.applyDelta_reqs_free
#print axioms Reachable.answered_of_transStep
#print axioms Reachable.separable_addDatum
#print axioms Reachable.answered_supply
#print axioms Reachable.reach_answered
#print axioms Reachable.answered_allPairsDemanded_fixpoint
#print axioms Reachable.fixpoint_no_collapsed
#print axioms Reachable.rootL_answered
#print axioms Reachable.rootF_answered
#print axioms Reachable.reach_allPairsDemanded_fixpoint
#print axioms Reachable.separable_appendForm
#print axioms Reachable.formsUsed_of_not_form
#print axioms Reachable.formsUsed_pair_not_form
#print axioms Reachable.minResponse_formsUsed
#print axioms Reachable.reach_formsUsed
#print axioms Reachable.rootL_formsUsed
#print axioms Reachable.rootF_formsUsed
#print axioms Reachable.formNoInst_wf
#print axioms Reachable.formNoInst_rule_free
#print axioms Reachable.formNoInst_arities
#print axioms Reachable.formNoInst_not_formsUsed
#print axioms Reachable.formNoInst_unreachable
#print axioms Reachable.ruledMark_wf
#print axioms Reachable.ruledMark_rules_ne
#print axioms Reachable.ruledMark_unreachable
