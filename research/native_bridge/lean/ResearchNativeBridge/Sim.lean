import ResearchNativeBridge.Passage

/-!
# Commuting translations into a step function

AuthorityEffect: None.  A translation of a deterministic system `g` into a
deterministic system `f` is a state encoding and, for each state and
event, a list of target events whose replay from the encoded state reaches
the encoding of the post-state.  That is one commuting square per step.

Proved here:

* `run_trHist`, `trHist_append`: the squares compose over histories.
* `lift`, `events_lift`, `lift_nil`, `lift_append`: every path of `g`
  maps to a path of `f` between the encoded endpoints, preserving
  identities and composition.
* `lift_cycle_core`, `acyclic_of_core_injective`: under the measure and
  core premises of `Path.cycle_core`, the encodings of all states on a
  cycle share a core; if the core of the encoding separates states, `g`
  has no cycle through two distinct states.
* `budgetSim`, `budgetSim_enc_injective`: for the sealed passage, every
  system with an injective numbering has a commuting translation with an
  injective encoding, through the budget field alone.  So a commuting
  square with an injective encoding does not by itself show that the
  target reproduces the source's structure.
* `passage_sim_cycle`: for the sealed passage, the encodings of states on
  a cycle differ at most in budget and license.
-/

namespace ResearchNativeBridge

open PrimitivePassage

/-- A commuting translation of `g` into `f`. -/
structure Sim {S E σ ε : Type} (g : S → E → S) (f : σ → ε → σ) where
  enc : S → σ
  tr : S → E → List ε
  comm : ∀ s e, run f (tr s e) (enc s) = enc (g s e)

namespace Sim

variable {S E σ ε : Type} {g : S → E → S} {f : σ → ε → σ}

/-- Translate a history, threading the source state. -/
def trHist (m : Sim g f) : S → List E → List ε
  | _, [] => []
  | s, e :: l => m.tr s e ++ trHist m (g s e) l

theorem run_trHist (m : Sim g f) (s : S) (l : List E) :
    run f (m.trHist s l) (m.enc s) = m.enc (run g l s) := by
  induction l generalizing s with
  | nil => rfl
  | cons e rest ih =>
      show run f (m.tr s e ++ m.trHist (g s e) rest) (m.enc s) = _
      rw [run_append, m.comm s e]
      exact ih (g s e)

theorem trHist_append (m : Sim g f) (s : S) (l₁ l₂ : List E) :
    m.trHist s (l₁ ++ l₂) = m.trHist s l₁ ++ m.trHist (run g l₁ s) l₂ := by
  induction l₁ generalizing s with
  | nil => rfl
  | cons e rest ih =>
      show m.tr s e ++ m.trHist (g s e) (rest ++ l₂) =
        (m.tr s e ++ m.trHist (g s e) rest) ++ m.trHist (run g rest (g s e)) l₂
      rw [ih (g s e), List.append_assoc]

/-- The image of a source path. -/
def lift (m : Sim g f) {s t : S} (τ : Path g s t) : Path f (m.enc s) (m.enc t) :=
  Path.ofSub ⟨m.trHist s (Path.events τ), by
    rw [run_trHist, Path.run_events]⟩

theorem events_lift (m : Sim g f) {s t : S} (τ : Path g s t) :
    Path.events (m.lift τ) = m.trHist s (Path.events τ) := by
  unfold lift
  exact congrArg Subtype.val (Path.toSub_ofSub _)

theorem lift_nil (m : Sim g f) (s : S) : m.lift (Path.nil s) = Path.nil (m.enc s) :=
  Path.events_injective _ _ (by rw [events_lift]; rfl)

theorem lift_append (m : Sim g f) {s t w : S} (p : Path g s t) (q : Path g t w) :
    m.lift (Path.append p q) = Path.append (m.lift p) (m.lift q) := by
  apply Path.events_injective
  rw [events_lift, Path.events_append, Path.events_append, events_lift,
    events_lift, trHist_append, Path.run_events]

/-- The encodings of states on a cycle share a core. -/
theorem lift_cycle_core {κ : Type} (m : Sim g f) (μ : σ → Nat) (core : σ → κ)
    (hmono : ∀ s e, μ s ≤ μ (f s e))
    (hkeep : ∀ s e, μ (f s e) = μ s → core (f s e) = core s)
    {s t : S} (p : Path g s t) (q : Path g t s) :
    core (m.enc t) = core (m.enc s) :=
  Path.cycle_core μ core hmono hkeep (m.lift p) (m.lift q)

/-- If the core of the encoding separates states, no cycle passes through
two distinct states. -/
theorem acyclic_of_core_injective {κ : Type} (m : Sim g f) (μ : σ → Nat)
    (core : σ → κ) (hmono : ∀ s e, μ s ≤ μ (f s e))
    (hkeep : ∀ s e, μ (f s e) = μ s → core (f s e) = core s)
    (hinj : ∀ a b, core (m.enc a) = core (m.enc b) → a = b)
    {s t : S} (p : Path g s t) (q : Path g t s) : t = s :=
  hinj t s (m.lift_cycle_core μ core hmono hkeep p q)

end Sim

/-- Any system with a numbering commutes with the sealed passage through
the budget field. -/
def budgetSim {S E : Type} (g : S → E → S) (code : S → Nat) : Sim g step where
  enc := fun s => { genesisP with budget := code s }
  tr := fun s e => [.setBudget (code (g s e))]
  comm := fun _ _ => rfl

theorem budgetSim_enc_injective {S E : Type} (g : S → E → S) (code : S → Nat)
    (hcode : ∀ a b, code a = code b → a = b) (a b : S)
    (h : (budgetSim g code).enc a = (budgetSim g code).enc b) : a = b :=
  hcode a b (congrArg PState.budget h)

/-- Encodings of states on a source cycle differ at most in budget and
license. -/
theorem passage_sim_cycle {S E : Type} {g : S → E → S} (m : Sim g step)
    {s t : S} (p : Path g s t) (q : Path g t s) :
    core (m.enc t) = core (m.enc s) :=
  m.lift_cycle_core size core size_step_mono core_step_of_size_eq p q

/-- A two-state toggle: a source system with a cycle through two distinct
states. -/
def toggle (b : Bool) (_ : Unit) : Bool := !b

def toggleSim : Sim toggle step := budgetSim toggle (fun b => bit b)

/-- The toggle's two states have distinct encodings with a common core:
the budget field is where the cycle lives. -/
theorem toggle_encoding :
    toggleSim.enc true ≠ toggleSim.enc false ∧
      core (toggleSim.enc true) = core (toggleSim.enc false) :=
  ⟨fun h => Nat.one_ne_zero (congrArg PState.budget h), rfl⟩

end ResearchNativeBridge
