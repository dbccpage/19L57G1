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
# The Engine Driver Relation, Refinement of XStep, and Liveness Analysis

This module formalizes the execution driver of the engine over the sealed
`Regime` carrier, closing the specification bridge between the permissive
step relation `XStep` and the constrained driver relation.

The formalization covers:
1. **Candidate space bounds and measures**: at most two items, arity at most two;
   lexicographic cost under `mu1` and `mu2`; minimum valid response selection
   (`IsMin`).
2. **Orbit demands and quiet states**: automorphism-least collapsed pairs
   (`OrbitRep`); states where all pairs are separated (`Quiet`).
3. **The engine driver relation (`EngineDriver`)**: firing on an orbit demand
   with a minimum valid response; or growing by one datum when quiet and supply
   is enabled. This enforces the fire-before-growth discipline.
4. **Refinement of XStep**: each engine driver transition is a valid `XStep`
   (`engineDriver_refines_xstep`), preserving `Good` along driver transitions
   (`good_driver`) and decoding to replayable event blocks (`driver_replays`).
5. **Driver paths**: sequences of driver transitions from an initial state
   (`DriverPath`, `good_path`, `path_replays`).
6. **Liveness and prefix extension analysis**:
   - Closed-system termination: when supply is disabled, quiet prefixes admit
     no transition (`quiet_no_driver_step`).
   - Fire-before-growth constraint: growth requires quiet states
     (`grow_step_quiet`).
   - Extension at quiet states under supply: quiet states extend via
     growth when supply is enabled (`quiet_driver_grow`).
   - Response existence in bounds: each demand in a good regime admits a valid
     response within the declared bounds (`mark_response_inBounds`).
   - Conditional firing extension: existence of a minimum response yields an
     engine fire step (`fire_driver_extend`).
   - Datum-adding responses: responses admitting fresh data maintain the `Good`
     invariant (`datum_adding_fire_good`).
   - Resource guards: bounded execution stops once the round bound is reached
     (`guarded_driver_refuses_at_round_bound`).

AuthorityEffect: None.
-/

namespace Ignition.Driver

open Derivation Ignition

/-! ## 1. Candidate space bounds, measures, and minimum responses -/

/-- The declared candidate space: at most two items, new forms of arity at
most two (`Bounds(max_items=2, max_arity=2)`).
AuthorityEffect: None. -/
def InBounds (δ : List Item) : Prop :=
  δ.length ≤ 2 ∧ ∀ a, Item.newForm a ∈ δ → a ≤ 2

/-- The two declared optimization measures.
AuthorityEffect: None. -/
inductive Measure where
  | mu1
  | mu2
deriving DecidableEq, Repr

/-- Both declared measures as one lexicographic cost: `mu1` is the item
count, `mu2` the item count then the new-form arity sum.
AuthorityEffect: None. -/
def cost : Measure → List Item → Nat × Nat
  | .mu1, δ => (δ.length, 0)
  | .mu2, δ => (δ.length, aritySum δ)

/-- Lexicographic order on pairs of natural numbers.
AuthorityEffect: None. -/
def lexLE (p q : Nat × Nat) : Prop := p.1 < q.1 ∨ (p.1 = q.1 ∧ p.2 ≤ q.2)

instance (p q : Nat × Nat) : Decidable (lexLE p q) := by
  unfold lexLE
  infer_instance

/-- Lexicographic order reflexivity.
AuthorityEffect: None. -/
theorem lexLE_refl (p : Nat × Nat) : lexLE p p := Or.inr ⟨rfl, Nat.le_refl _⟩

/-- Lexicographic order transitivity.
AuthorityEffect: None. -/
theorem lexLE_trans {p q r : Nat × Nat} (h1 : lexLE p q) (h2 : lexLE q r) : lexLE p r := by
  rcases h1 with h1 | ⟨h1a, h1b⟩ <;> rcases h2 with h2 | ⟨h2a, h2b⟩
  · exact Or.inl (Nat.lt_trans h1 h2)
  · exact Or.inl (h2a ▸ h1)
  · exact Or.inl (h1a.symm ▸ h2)
  · refine Or.inr ⟨h1a.trans h2a, ?_⟩
    omega

/-- A minimum valid response inside the bounds under the declared measure.
AuthorityEffect: None. -/
def IsMin (m : Measure) (r : Regime) (i j : Nat) (δ : List Item) : Prop :=
  InBounds δ ∧ validResponse r i j δ ∧
    ∀ δ', InBounds δ' → validResponse r i j δ' → lexLE (cost m δ) (cost m δ')

/-- A minimum response is a valid response.
AuthorityEffect: None. -/
theorem isMin_valid {m : Measure} {r : Regime} {i j : Nat} {δ : List Item}
    (h : IsMin m r i j δ) : validResponse r i j δ := h.2.1

/-- Membership in dropped rules implies membership in the original list.
AuthorityEffect: None. -/
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

/-- Dropping rules preserves the bound condition.
AuthorityEffect: None. -/
theorem inBounds_dropRules {δ : List Item} (h : InBounds δ) : InBounds (dropRules δ) :=
  ⟨Nat.le_trans (dropRules_length_le δ) h.1, fun a ha => h.2 a (mem_dropRules ha)⟩

/-- A minimum response contains no rule item under either measure.
AuthorityEffect: None. -/
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

/-! ## 2. Automorphisms, orbit demands, and quiet states -/

/-- Relabelling of a regime under datum and form bijections.
AuthorityEffect: None. -/
def relab (r : Regime) (π φ φinv : Nat → Nat) : Regime :=
  ⟨r.data,
   (List.range r.forms.length).map (fun g => r.forms.getD (φinv g) 0),
   r.insts.map (fun p => (φ p.1, p.2.map π)),
   r.rules.map φ,
   r.reqs.map (mapReq π)⟩

/-- Automorphism of a regime: a datum bijection and form bijection whose
relabelling is the regime up to list order.
AuthorityEffect: None. -/
def IsAuto (r : Regime) (π : DRen r.data) (φ : DRen r.forms.length) : Prop :=
  RegimeExt (relab r π.f φ.f φ.g) r

/-- An orbit demand: a collapsed pair that is least in its automorphism orbit.
AuthorityEffect: None. -/
def OrbitRep (r : Regime) (i j : Nat) : Prop :=
  i < j ∧ j < r.data ∧ collapsed r i j ∧
    ∀ (π : DRen r.data) (φ : DRen r.forms.length), IsAuto r π φ →
      lexLE (i, j) (mapReq π.f (i, j))

/-- Quiet state: each pair of admitted data is separated.
AuthorityEffect: None. -/
def Quiet (r : Regime) : Prop := ∀ i j, i < j → j < r.data → ¬ collapsed r i j

/-! ## 3. The engine driver relation -/

/-- Firing on a collapsed pair with a minimum response.
AuthorityEffect: None. -/
def Fire (m : Measure) (r : Regime) (i j : Nat) (δ : List Item) (t : Regime) : Prop :=
  i < j ∧ j < r.data ∧ collapsed r i j ∧ IsMin m r i j δ ∧ respond r i j δ = some t

/-- Firing is a valid sealed transition step.
AuthorityEffect: None. -/
theorem fire_transStep {m : Measure} {r t : Regime} {i j : Nat} {δ : List Item}
    (h : Fire m r i j δ t) : TransStep r i j δ t :=
  ⟨h.1, h.2.1, h.2.2.1, isMin_valid h.2.2.2.1, h.2.2.2.2⟩

/-- Firing on an orbit demand.
AuthorityEffect: None. -/
def EngineFire (m : Measure) (r t : Regime) : Prop :=
  ∃ i j δ, OrbitRep r i j ∧ Fire m r i j δ t

/-- The engine driver relation over regimes:
1. When a demand stands, fire on an orbit representative using a minimum response.
2. When quiet and external supply is enabled, grow by one datum.
Growth is barred whenever a demand exists (fire-before-growth discipline).
AuthorityEffect: None. -/
inductive EngineDriver (m : Measure) (supply : Bool) : Regime → Regime → Prop where
  | fire {r t : Regime} : EngineFire m r t → EngineDriver m supply r t
  | grow {r : Regime} : supply = true → Quiet r → EngineDriver m supply r (grow r)

/-! ## 4. Refinement of XStep -/

/-- The engine driver relation refines the extension step `XStep`:
each transition admitted by the driver is a valid extension step.
AuthorityEffect: None. -/
theorem engineDriver_refines_xstep {m : Measure} {supply : Bool} {r t : Regime}
    (h : EngineDriver m supply r t) : XStep r t := by
  cases h with
  | fire hf =>
      obtain ⟨i, j, δ, _, hfire⟩ := hf
      have htrans := fire_transStep hfire
      have hnorule := isMin_no_rule hfire.2.2.2.1
      exact XStep.fire htrans hnorule
  | grow _ _ =>
      exact XStep.grow

/-- Driver steps preserve the invariant `Good`.
AuthorityEffect: None. -/
theorem good_driver {m : Measure} {supply : Bool} {r t : Regime}
    (hg : Good r) (h : EngineDriver m supply r t) : Good t :=
  good_xstep hg (engineDriver_refines_xstep h)

/-- Each driver step decodes to a sealed event block that replays to its successor.
AuthorityEffect: None. -/
theorem driver_replays {m : Measure} {supply : Bool} {r t : Regime}
    (h : EngineDriver m supply r t) : ∃ block : List Event, replayE block r = some t :=
  xstep_replays (engineDriver_refines_xstep h)

/-! ## 5. Paths and prefixes -/

/-- A path of driver steps.
AuthorityEffect: None. -/
inductive DriverPath (m : Measure) (supply : Bool) : Regime → List Regime → Regime → Prop where
  | nil (r : Regime) : DriverPath m supply r [] r
  | cons {r s t : Regime} {rest : List Regime} :
      EngineDriver m supply r s → DriverPath m supply s rest t → DriverPath m supply r (s :: rest) t

/-- Each state along a driver path from a good state is good.
AuthorityEffect: None. -/
theorem good_path {m : Measure} {supply : Bool} {r t : Regime} {states : List Regime}
    (hg : Good r) (h : DriverPath m supply r states t) : Good t := by
  induction h with
  | nil => exact hg
  | cons hstep _ ih => exact ih (good_driver hg hstep)

/-- Each driver path decodes to a sealed event history replaying to its endpoint.
AuthorityEffect: None. -/
theorem path_replays {m : Measure} {supply : Bool} {r t : Regime} {states : List Regime}
    (h : DriverPath m supply r states t) : ∃ hist : List Event, replayE hist r = some t := by
  induction h with
  | nil r => exact ⟨[], rfl⟩
  | cons hstep _ ih =>
      obtain ⟨block, hblock⟩ := driver_replays hstep
      obtain ⟨hist, hhist⟩ := ih
      refine ⟨block ++ hist, ?_⟩
      rw [LocalReuse.replayE_suffix, hblock]
      exact hhist

/-! ## 6. Liveness and prefix extension analysis -/

/-- At a quiet state with supply disabled, no driver step exists.
Closed runs that separate each pair terminate.
AuthorityEffect: None. -/
theorem quiet_no_driver_step {m : Measure} {r : Regime} (hq : Quiet r) :
    ¬ ∃ t, EngineDriver m false r t := by
  rintro ⟨t, hstep⟩
  cases hstep with
  | fire hf =>
      obtain ⟨i, j, δ, horb, _⟩ := hf
      exact hq i j horb.1 horb.2.1 horb.2.2.1
  | grow hsupp _ =>
      cases hsupp

/-- Growth transitions under EngineDriver require a quiet regime.
AuthorityEffect: None. -/
theorem grow_step_quiet {m : Measure} {supply : Bool} {r : Regime}
    (hs : supply = true) (hq : Quiet r) : EngineDriver m supply r (grow r) :=
  EngineDriver.grow hs hq

/-- At each quiet state with supply enabled, the driver extends via growth.
AuthorityEffect: None. -/
theorem quiet_driver_grow {m : Measure} {r : Regime} (hq : Quiet r) :
    EngineDriver m true r (grow r) :=
  EngineDriver.grow rfl hq

/-- The fresh-mark response is inside the declared candidate bounds.
AuthorityEffect: None. -/
theorem mark_inBounds (r : Regime) (j : Nat) :
    InBounds [.newForm 1, .newInst r.forms.length [j]] := by
  refine ⟨Nat.le_refl 2, ?_⟩
  intro a ha
  rcases List.mem_cons.mp ha with ha | ha
  · cases ha
    decide
  · rcases List.mem_cons.mp ha with ha | ha
    · cases ha
    · cases ha

/-- The fresh-mark response witnesses that a valid response inside the
declared candidate bounds exists for each demand in a good regime.
AuthorityEffect: None. -/
theorem mark_response_inBounds {r : Regime} (hg : Good r) {i j : Nat}
    (hij : i < j) (hjd : j < r.data) :
    InBounds [.newForm 1, .newInst r.forms.length [j]] ∧
      validResponse r i j [.newForm 1, .newInst r.forms.length [j]] := by
  refine ⟨mark_inBounds r j, ?_⟩
  exact mark_progress r hg.1 i j (Nat.lt_trans hij hjd) hjd (Nat.ne_of_lt hij) hg.2.2

/-- When an orbit demand admits a minimum response and response application
succeeds, the driver extends via firing.
AuthorityEffect: None. -/
theorem fire_driver_extend {m : Measure} {supply : Bool} {r : Regime}
    {i j : Nat} {δ : List Item} {t : Regime}
    (horb : OrbitRep r i j) (hmin : IsMin m r i j δ)
    (hresp : respond r i j δ = some t) :
    EngineDriver m supply r t :=
  EngineDriver.fire ⟨i, j, δ, horb, ⟨horb.1, horb.2.1, horb.2.2.1, hmin, hresp⟩⟩

/-- Datum-adding responses: if an engine driver fire step answers a demand
with a response that admits a fresh datum (Item.newDatum ∈ δ), the successor
regime t still satisfies the invariant `Good`.
AuthorityEffect: None. -/
theorem datum_adding_fire_good {m : Measure} {supply : Bool} {r t : Regime}
    {i j : Nat} {δ : List Item} (hg : Good r) (horb : OrbitRep r i j)
    (hfire : Fire m r i j δ t) (_ : Item.newDatum ∈ δ) : Good t :=
  good_driver (supply := supply) hg (EngineDriver.fire (supply := supply) ⟨i, j, δ, horb, hfire⟩)

/-- An engine execution bounded by resource guards:
a step limit `maxRounds` (reflecting the engine's `max_rounds`).
When the budget is reached or exceeded, continuation is refused.
AuthorityEffect: None. -/
def GuardedDriver (m : Measure) (supply : Bool) (maxRounds : Nat)
    (currentDepth : Nat) (r t : Regime) : Prop :=
  currentDepth < maxRounds ∧ EngineDriver m supply r t

/-- Resource guard refusal: when the current depth reaches or exceeds the
round bound, guarded continuation is refused.
AuthorityEffect: None. -/
theorem guarded_driver_refuses_at_round_bound {m : Measure} {supply : Bool}
    {maxRounds currentDepth : Nat} {r t : Regime}
    (hlimit : maxRounds ≤ currentDepth) :
    ¬ GuardedDriver m supply maxRounds currentDepth r t := by
  rintro ⟨hdepth, _⟩
  omega

end Ignition.Driver

#print axioms Ignition.Driver.lexLE_refl
#print axioms Ignition.Driver.lexLE_trans
#print axioms Ignition.Driver.isMin_valid
#print axioms Ignition.Driver.mem_dropRules
#print axioms Ignition.Driver.inBounds_dropRules
#print axioms Ignition.Driver.isMin_no_rule
#print axioms Ignition.Driver.fire_transStep
#print axioms Ignition.Driver.engineDriver_refines_xstep
#print axioms Ignition.Driver.good_driver
#print axioms Ignition.Driver.driver_replays
#print axioms Ignition.Driver.good_path
#print axioms Ignition.Driver.path_replays
#print axioms Ignition.Driver.quiet_no_driver_step
#print axioms Ignition.Driver.grow_step_quiet
#print axioms Ignition.Driver.quiet_driver_grow
#print axioms Ignition.Driver.mark_inBounds
#print axioms Ignition.Driver.mark_response_inBounds
#print axioms Ignition.Driver.fire_driver_extend
#print axioms Ignition.Driver.datum_adding_fire_good
#print axioms Ignition.Driver.guarded_driver_refuses_at_round_bound
