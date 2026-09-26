import SecondEngine.Kernel
import SecondEngine.Stake

/-!
# What an engine is, as a definition

Native to continuation one.

The seed's challenge three asks for a precise declaration of an engine:
a generator that reads demands off the state, a responder that answers a
demand, a continuation rule, and a replay rule, such that after genesis
no external act occurs except those the declaration names.  Here that is
a structure over a state type `S`, a demand type `D` and an event type
`E`:

* `Demand s d`: the generator's reading -- `d` is a demand of `s`;
* `Resp s d h`: the responder's -- the history `h` is a minimum response
  to `d` at `s` (which minimum, under which measure, is the responder's
  business and is not mirrored here: the sealed candidate space is not
  reconstructed in Lean);
* `Cont s h`: the continuation's -- `h` is a continuation history
  enabled at `s`;
* `apply s h`: the replay rule, applying a history to a state.

A history is NAMED at a state when it is a response to one of the
state's demands, or the state has no demand and the history is an
enabled continuation.  A STEP applies a named history; a RUN is a chain
of steps.  So, by definition, every history of every run is named by the
declaration at the state it is taken from -- `run_named` says so -- and
nothing else can happen after genesis.  That is a statement at the level
of a definition, and the ledger records it so.

* `fixpoint_of_halt`: with no enabled continuation, a demand-free state
  has no step.
* `step_at_demand_is_response`: a step from a state with a demand is a
  response to one of its demands; the continuation is never taken there.
* `e1_engine_quiet`, `e1_halt_no_step`: an engine whose generator reads
  E-one, in plain mode, has no demand at any regime, and with no
  continuation has no step.

AuthorityEffect: None.
-/

namespace SecondEngine
namespace EngineDef

open Sealed Stake

/-- An engine: a generator, a responder, a continuation and a replay
rule. -/
structure Engine (S D E : Type) where
  Demand : S → D → Prop
  Resp : S → D → List E → Prop
  Cont : S → List E → Prop
  apply : S → List E → Option S

variable {S D E : Type}

/-- A state with no demand. -/
def Quiet (e : Engine S D E) (s : S) : Prop := ∀ d, ¬ e.Demand s d

/-- The histories the declaration names at a state. -/
def Named (e : Engine S D E) (s : S) (h : List E) : Prop :=
  (∃ d, e.Demand s d ∧ e.Resp s d h) ∨ (Quiet e s ∧ e.Cont s h)

/-- One step: a named history, applied. -/
def Step (e : Engine S D E) (s s' : S) : Prop :=
  ∃ h, Named e s h ∧ e.apply s h = some s'

/-- A run: a chain of steps, with the history of each. -/
inductive Run (e : Engine S D E) : S → S → List (List E) → Prop
  | refl (s : S) : Run e s s []
  | step {s s' s'' : S} {h : List E} {hs : List (List E)} :
      Named e s h → e.apply s h = some s' → Run e s' s'' hs → Run e s s'' (h :: hs)

/-- With no enabled continuation, a demand-free state has no step. -/
theorem fixpoint_of_halt (e : Engine S D E) (hc : ∀ s h, ¬ e.Cont s h) {s s' : S}
    (hq : Quiet e s) : ¬ Step e s s' := by
  rintro ⟨h, (⟨d, hd, _⟩ | ⟨_, hh⟩), _⟩
  · exact hq d hd
  · exact hc s h hh

/-- A step from a state with a demand is a response to one of its
demands. -/
theorem step_at_demand_is_response (e : Engine S D E) {s s' : S} {d₀ : D}
    (hd₀ : e.Demand s d₀) (hst : Step e s s') :
    ∃ d h, e.Demand s d ∧ e.Resp s d h ∧ e.apply s h = some s' := by
  obtain ⟨h, hn, ha⟩ := hst
  cases hn with
  | inl hr =>
    obtain ⟨d, hd, hresp⟩ := hr
    exact ⟨d, h, hd, hresp, ha⟩
  | inr hq => exact absurd hd₀ (hq.1 d₀)

/-- Every history of every run is named by the declaration at some
state the run passes through. -/
theorem run_named (e : Engine S D E) {s s' : S} {hs : List (List E)}
    (hr : Run e s s' hs) : ∀ h ∈ hs, ∃ t, Named e t h := by
  induction hr with
  | refl _ => intro h hh; cases hh
  | step hn _ _ ih =>
    intro h hh
    cases hh with
    | head => exact ⟨_, hn⟩
    | tail _ hm => exact ih h hm

/-- The generator of a stake reading in a mode: a pair of admitted data,
the first below the second, whose label read in the mode is not
honoured.  A state is a regime and a mode, `false` plain and `true`
flipped. -/
def stakeDemand (ρ : Reading) (s : Regime × Bool) (p : Nat × Nat) : Prop :=
  p.1 < p.2 ∧ p.2 < s.1.data ∧ Demand (if s.2 then ρ.flip else ρ) s.1 p.1 p.2

/-- An engine whose generator reads E-one has no demand at any plain
state, whatever its responder, continuation and replay rule. -/
theorem e1_engine_quiet {E : Type} (e : Engine (Regime × Bool) (Nat × Nat) E)
    (hg : e.Demand = stakeDemand E1) (r : Regime) : Quiet e (r, false) := by
  intro p hp
  rw [hg] at hp
  exact e1_never_demands r p.1 p.2 hp.2.2

/-- An engine whose generator reads E-one and which has no enabled
continuation has no step from any plain state. -/
theorem e1_halt_no_step {E : Type} (e : Engine (Regime × Bool) (Nat × Nat) E)
    (hg : e.Demand = stakeDemand E1) (hc : ∀ s h, ¬ e.Cont s h) (r : Regime)
    (s' : Regime × Bool) : ¬ Step e (r, false) s' :=
  fixpoint_of_halt e hc (e1_engine_quiet e hg r)

end EngineDef
end SecondEngine
