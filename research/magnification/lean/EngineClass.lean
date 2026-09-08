import Derivation.Basic
import Derivation.Inertia
import Derivation.Mention
import Derivation.Progress
import Derivation.Minimality
import Derivation.RuleBridge
import Derivation.Rounds
import Derivation.TransitionTransport
import Derivation.Ext
import LocalReuse
import Ignition

/-!
# The engine's class, as a relation over the sealed definitions

The sealed engine (`code/derivation/engine.py::build_tree`) answers, at every
node, one demand per automorphism orbit of the collapsed pairs, with every
minimum-cost valid response inside the declared candidate space, quotiented
by the implemented isomorphism; when no pair is collapsed it supplies one
fresh datum if supply is enabled.  This module states that process as a
relation over the sealed `Regime`, `collapsed`, `validResponse` and
`respond`, without selecting any representative:

* `InBounds`, `cost`, `IsMin` — the declared candidate space and the two
  declared measures as one lexicographic cost; a minimum never carries a
  rule item (`isMin_no_rule`, from the sealed `rule_item_never_minimal`).
* `Fire` — a collapsed pair answered by a minimum response (the sealed
  `TransStep` plus minimality); `OrbitRep` — a collapsed pair least in its
  orbit under the automorphisms of the regime, the engine's demand;
  `EngineFire`, `EngineStep`, `Path`, `Rooted` — the engine's history class
  with the seed round answering the declared target.
* `Good` — well-formed, rule-free, every standing requirement separated —
  preserved by every step and every path (`good_path`, `good_rooted`).
* Every step decodes to a sealed event block replaying to its successor
  (`fire_replays`, `path_replays`).

The well-formedness lemmas of section 1 are the merged ignition family's,
consumed through `import Ignition` (they were local copies until
2026-09-08).

AuthorityEffect: None.
-/

namespace EngineClass

open Derivation Ignition

/-! ## 1. Well-formedness and rule-freeness along responses

`applyItem_wf`, `applyDelta_wf`, `applyItem_rules`, `applyDelta_rules`,
`applyItem_reqs_free` and `applyDelta_reqs_free` are the merged ignition
family's theorems (`research/ignition/lean/Ignition.lean`), consumed through
`import Ignition`; until 2026-09-08 this section carried local copies. -/

/-! ## 2. The declared candidate space and the two measures -/

/-- The declared candidate space: at most two items, new forms of arity at
most two (`Bounds(max_items=2, max_arity=2)`). -/
def InBounds (δ : List Item) : Prop :=
  δ.length ≤ 2 ∧ ∀ a, Item.newForm a ∈ δ → a ≤ 2

inductive Measure where
  | mu1
  | mu2
deriving DecidableEq, Repr

/-- Both declared measures as one lexicographic cost: `mu1` is the item
count, `mu2` the item count then the new-form arity sum. -/
def cost : Measure → List Item → Nat × Nat
  | .mu1, δ => (δ.length, 0)
  | .mu2, δ => (δ.length, aritySum δ)

/-- Lexicographic order on pairs. -/
def lexLE (p q : Nat × Nat) : Prop := p.1 < q.1 ∨ (p.1 = q.1 ∧ p.2 ≤ q.2)

instance (p q : Nat × Nat) : Decidable (lexLE p q) := by
  unfold lexLE
  infer_instance

theorem lexLE_refl (p : Nat × Nat) : lexLE p p := Or.inr ⟨rfl, Nat.le_refl _⟩

/-- A minimum valid response inside the bounds under the measure. -/
def IsMin (m : Measure) (r : Regime) (i j : Nat) (δ : List Item) : Prop :=
  InBounds δ ∧ validResponse r i j δ ∧
    ∀ δ', InBounds δ' → validResponse r i j δ' → lexLE (cost m δ) (cost m δ')

theorem isMin_valid {m : Measure} {r : Regime} {i j : Nat} {δ : List Item}
    (h : IsMin m r i j δ) : validResponse r i j δ := h.2.1

theorem mem_dropRules {x : Item} : ∀ {δ : List Item}, x ∈ dropRules δ → x ∈ δ
  | [], h => absurd h List.not_mem_nil
  | .newRuleAll f :: rest, h =>
      List.mem_cons_of_mem _ (mem_dropRules (δ := rest) h)
  | .newDatum :: rest, h => by
      have h' : x ∈ Item.newDatum :: dropRules rest := h
      rcases List.mem_cons.mp h' with rfl | hm
      · exact List.mem_cons_self
      · exact List.mem_cons_of_mem _ (mem_dropRules hm)
  | .newForm a :: rest, h => by
      have h' : x ∈ Item.newForm a :: dropRules rest := h
      rcases List.mem_cons.mp h' with rfl | hm
      · exact List.mem_cons_self
      · exact List.mem_cons_of_mem _ (mem_dropRules hm)
  | .newInst f args :: rest, h => by
      have h' : x ∈ Item.newInst f args :: dropRules rest := h
      rcases List.mem_cons.mp h' with rfl | hm
      · exact List.mem_cons_self
      · exact List.mem_cons_of_mem _ (mem_dropRules hm)

theorem inBounds_dropRules {δ : List Item} (h : InBounds δ) : InBounds (dropRules δ) :=
  ⟨Nat.le_trans (dropRules_length_le δ) h.1, fun a ha => h.2 a (mem_dropRules ha)⟩

/-- **A minimum never carries a rule item**, under either measure: the
sealed `rule_item_never_minimal` gives a strictly shorter valid response
with the same arity sum. -/
theorem isMin_no_rule {m : Measure} {r : Regime} {i j : Nat} {δ : List Item}
    (h : IsMin m r i j δ) : ∀ f, Item.newRuleAll f ∉ δ := by
  intro f hf
  obtain ⟨hb, hv, hmin⟩ := h
  obtain ⟨hv', hlt, hsum⟩ := rule_item_never_minimal hf hv
  have hle := hmin (dropRules δ) (inBounds_dropRules hb) hv'
  cases m with
  | mu1 =>
      have hle' : δ.length < (dropRules δ).length ∨
          (δ.length = (dropRules δ).length ∧ 0 ≤ 0) := hle
      rcases hle' with h1 | ⟨h2, _⟩
      · exact absurd hlt (Nat.lt_asymm h1)
      · omega
  | mu2 =>
      have hle' : δ.length < (dropRules δ).length ∨
          (δ.length = (dropRules δ).length ∧ aritySum δ ≤ aritySum (dropRules δ)) := hle
      rcases hle' with h1 | ⟨h2, _⟩
      · exact absurd hlt (Nat.lt_asymm h1)
      · omega

/-! ## 3. Firing, orbits, and the engine step -/

/-- Firing on a collapsed pair with a minimum response.  No representative
is selected: every collapsed pair and every minimum is a firing. -/
def Fire (m : Measure) (r : Regime) (i j : Nat) (δ : List Item) (t : Regime) : Prop :=
  i < j ∧ j < r.data ∧ collapsed r i j ∧ IsMin m r i j δ ∧ respond r i j δ = some t

theorem fire_transStep {m : Measure} {r t : Regime} {i j : Nat} {δ : List Item}
    (h : Fire m r i j δ t) : TransStep r i j δ t :=
  ⟨h.1, h.2.1, h.2.2.1, isMin_valid h.2.2.2.1, h.2.2.2.2⟩

/-- The relabelling the sealed `iso.py::rename` performs: a datum bijection
on instance arguments and requirement pairs, a form bijection on the arity
table, the instances and the rules (`φinv` reads the arity table back). -/
def relab (r : Regime) (π φ φinv : Nat → Nat) : Regime :=
  ⟨r.data,
   (List.range r.forms.length).map (fun g => r.forms.getD (φinv g) 0),
   r.insts.map (fun p => (φ p.1, p.2.map π)),
   r.rules.map φ,
   r.reqs.map (mapReq π)⟩

/-- An automorphism: a datum bijection and a form bijection whose
relabelling is the regime up to list order — the sealed `RegimeExt`, which
is what `iso.py::automorphisms` decides through sorted serializations. -/
def IsAuto (r : Regime) (π : DRen r.data) (φ : DRen r.forms.length) : Prop :=
  RegimeExt (relab r π.f φ.f φ.g) r

/-- **The engine's demand**: a collapsed pair of admitted data that is least
(lexicographically) in its orbit under the automorphisms of the regime —
the sealed `closure_challenge_orbits` representative. -/
def OrbitRep (r : Regime) (i j : Nat) : Prop :=
  i < j ∧ j < r.data ∧ collapsed r i j ∧
    ∀ (π : DRen r.data) (φ : DRen r.forms.length), IsAuto r π φ →
      lexLE (i, j) (mapReq π.f (i, j))

/-- A firing on an orbit demand. -/
def EngineFire (m : Measure) (r t : Regime) : Prop :=
  ∃ i j δ, OrbitRep r i j ∧ Fire m r i j δ t

/-- No demand stands: every pair of admitted data is separated. -/
def Quiet (r : Regime) : Prop := ∀ i j, i < j → j < r.data → ¬ collapsed r i j

/-- Growth: the sealed `admitDatum` step. -/
def grow (r : Regime) : Regime := { r with data := r.data + 1 }

/-- **One engine step**: fire on an orbit demand; or, when quiet and supply
is enabled, grow. -/
inductive EngineStep (m : Measure) (supply : Bool) : Regime → Regime → Prop where
  | fire {r t : Regime} : EngineFire m r t → EngineStep m supply r t
  | grow {r : Regime} : supply = true → Quiet r → EngineStep m supply r (grow r)

/-- A path of engine steps, listing the states visited. -/
inductive Path (m : Measure) (supply : Bool) : Regime → List Regime → Regime → Prop where
  | nil (r : Regime) : Path m supply r [] r
  | cons {r s t : Regime} {rest : List Regime} :
      EngineStep m supply r s → Path m supply s rest t → Path m supply r (s :: rest) t

/-- **The rooted class**: the seed round on the declared target
followed by engine steps.  The seed target is a parameter because the sealed
engine answers `reading.target` at the root rather than an orbit
representative (see `Restart.not_orbitRep_rootF_12`). -/
inductive Rooted (m : Measure) (supply : Bool) (root : Regime) (tgt : Nat × Nat) :
    Regime → Prop where
  | seed {s : Regime} {δ : List Item} :
      Fire m root tgt.1 tgt.2 δ s → Rooted m supply root tgt s
  | step {s t : Regime} :
      Rooted m supply root tgt s → EngineStep m supply s t → Rooted m supply root tgt t

/-! ## 4. The invariant -/

/-- Well-formed, rule-free, every standing requirement separated. -/
def Good (r : Regime) : Prop :=
  r.wf ∧ r.rules = [] ∧ ∀ q ∈ r.reqs, separable r q.1 q.2

theorem grow_wf {r : Regime} (hwf : r.wf) : (grow r).wf := by
  obtain ⟨hinst, hrule, hreq, hform⟩ := hwf
  refine ⟨?_, hrule, ?_, hform⟩
  · intro p hp
    obtain ⟨h1, h2, h3⟩ := hinst p hp
    exact ⟨h1, h2, fun a ha => Nat.lt_succ_of_lt (h3 a ha)⟩
  · intro q hq
    obtain ⟨h1, h2⟩ := hreq q hq
    exact ⟨h1, Nat.lt_succ_of_lt h2⟩

theorem separable_grow {r : Regime} {d d' : Nat} (h : separable r d d') :
    separable (grow r) d d' := by
  obtain ⟨c, hc, hne⟩ := h
  refine ⟨c, ⟨hc.1, hc.2.1, hc.2.2.1, ?_⟩, hne⟩
  intro s hs
  have := hc.2.2.2 s hs
  cases s with
  | none => trivial
  | some x => exact Nat.lt_succ_of_lt this

theorem good_grow {r : Regime} (hg : Good r) : Good (grow r) :=
  ⟨grow_wf hg.1, hg.2.1, fun q hq => separable_grow (hg.2.2 q hq)⟩

/-- A firing preserves the invariant: the successor is well-formed, rule-free
(a minimum has no rule item), and separates every standing requirement — the
old ones by validity, the new one because the response answered it. -/
theorem good_fire {m : Measure} {r t : Regime} {i j : Nat} {δ : List Item}
    (hg : Good r) (h : Fire m r i j δ t) : Good t := by
  have hnr := isMin_no_rule h.2.2.2.1
  obtain ⟨hij, hj, _, hmin, hresp⟩ := h
  obtain ⟨_, _, _, happ⟩ := respond_anatomy hresp
  obtain ⟨s, hs, hsep, hall⟩ := isMin_valid hmin
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

theorem good_step {m : Measure} {supply : Bool} {r t : Regime}
    (hg : Good r) (h : EngineStep m supply r t) : Good t := by
  cases h with
  | fire hf =>
      obtain ⟨i, j, δ, _, hfire⟩ := hf
      exact good_fire hg hfire
  | grow _ _ => exact good_grow hg

theorem good_path {m : Measure} {supply : Bool} {r t : Regime} {states : List Regime}
    (hg : Good r) (h : Path m supply r states t) : Good t := by
  induction h with
  | nil => exact hg
  | cons hstep _ ih => exact ih (good_step hg hstep)

theorem good_rooted {m : Measure} {supply : Bool} {root t : Regime} {tgt : Nat × Nat}
    (hg : Good root) (h : Rooted m supply root tgt t) : Good t := by
  induction h with
  | seed hfire => exact good_fire hg hfire
  | step _ hstep ih => exact good_step ih hstep

/-! ## 5. Decoding to the sealed events -/

theorem fire_replays {m : Measure} {r t : Regime} {i j : Nat} {δ : List Item}
    (h : Fire m r i j δ t) :
    replayE (LocalReuse.roundEvents ⟨(i, j), δ⟩) r = some t := by
  rw [LocalReuse.round_replays]
  exact h.2.2.2.2

theorem grow_replays (r : Regime) : replayE [.admitDatum] r = some (grow r) := rfl

theorem step_replays {m : Measure} {supply : Bool} {r t : Regime}
    (h : EngineStep m supply r t) : ∃ block : List Event, replayE block r = some t := by
  cases h with
  | fire hf =>
      obtain ⟨i, j, δ, _, hfire⟩ := hf
      exact ⟨_, fire_replays hfire⟩
  | grow _ _ => exact ⟨[.admitDatum], grow_replays _⟩

/-- Every path decodes to one sealed history replaying to its endpoint. -/
theorem path_replays {m : Measure} {supply : Bool} {r t : Regime} {states : List Regime}
    (h : Path m supply r states t) : ∃ hist : List Event, replayE hist r = some t := by
  induction h with
  | nil r => exact ⟨[], rfl⟩
  | cons hstep _ ih =>
      obtain ⟨block, hblock⟩ := step_replays hstep
      obtain ⟨hist, hhist⟩ := ih
      refine ⟨block ++ hist, ?_⟩
      rw [LocalReuse.replayE_suffix, hblock]
      exact hhist

theorem rooted_replays {m : Measure} {supply : Bool} {root t : Regime} {tgt : Nat × Nat}
    (h : Rooted m supply root tgt t) : ∃ hist : List Event, replayE hist root = some t := by
  induction h with
  | seed hfire => exact ⟨_, fire_replays hfire⟩
  | step _ hstep ih =>
      obtain ⟨hist, hhist⟩ := ih
      obtain ⟨block, hblock⟩ := step_replays hstep
      refine ⟨hist ++ block, ?_⟩
      rw [LocalReuse.replayE_suffix, hhist]
      exact hblock

end EngineClass

#print axioms EngineClass.lexLE_refl
#print axioms EngineClass.isMin_valid
#print axioms EngineClass.mem_dropRules
#print axioms EngineClass.inBounds_dropRules
#print axioms EngineClass.isMin_no_rule
#print axioms EngineClass.fire_transStep
#print axioms EngineClass.grow_wf
#print axioms EngineClass.separable_grow
#print axioms EngineClass.good_grow
#print axioms EngineClass.good_fire
#print axioms EngineClass.good_step
#print axioms EngineClass.good_path
#print axioms EngineClass.good_rooted
#print axioms EngineClass.fire_replays
#print axioms EngineClass.grow_replays
#print axioms EngineClass.step_replays
#print axioms EngineClass.path_replays
#print axioms EngineClass.rooted_replays
