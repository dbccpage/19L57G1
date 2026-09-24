import ResearchNativeBridge.Sim

/-!
# Translations that preserve the passage's observation

AuthorityEffect: None.  NB-9 showed that a commuting replay square is
cheap: every system with an injective numbering commutes with the sealed
passage through budget writes alone.  NB-16 asked for a translation that
also preserves the passage's own observation, and whether that stronger
notion excludes the budget register.

The passage's native observation (`nobs`) is three readings of a state:
the zero relation of the declared observation (`none` before one is
declared), the active obstruction, and the refusal record.  Proved here:

* `nobs_of_core`: the native observation is a function of the core.  It
  reads no budget and no license.
* `ObsSim.obs_on_cycle`, `ObsSim.obs_const_on_cycle`: a translation that
  carries a source observation to the native one sees a single native
  observation on every source cycle; with a faithful observation map the
  source observation is constant on every cycle.  This is NB-8's core
  collapse read through the observation.
* `budgetSim_nobs`, `budget_obs_const`: every budget-register encoding has
  the native observation of genesis, so a budget register preserves an
  observation only when that observation is constant.
* `toggle_no_faithful_obs`: the two-state toggle, observed by its own
  state, has no faithful observation-preserving translation into the
  passage, though it has a commuting one with an injective encoding
  (`toggle_encoding`).
* `idObsSim`: the passage translated into itself by the identity, observed
  natively, is a faithful observation-preserving translation, so the
  notion is not empty.

So the stronger notion excludes the budget register for every source
whose observation is not constant, and it excludes every translation of a
source that has a cycle through two observationally distinct states.
-/

namespace ResearchNativeBridge

open PrimitivePassage

/-- The passage's native observation of a state. -/
structure NObs where
  zero : Option (Nat → Nat → Bool)
  obst : Nat → Nat → Bool
  refused : List (Nat × Nat)

/-- Read the zero relation, the active obstruction and the refusal record. -/
def nobs (s : PState) : NObs :=
  ⟨s.obs.map zeroP, obstP s, s.refusals⟩

/-- The native observation reads only core fields. -/
theorem nobs_of_core {s t : PState} (h : core s = core t) : nobs s = nobs t := by
  obtain ⟨occ, asserted, wit, prot, obs, budget, licensed, refusals, halted⟩ := s
  obtain ⟨occ', asserted', wit', prot', obs', budget', licensed', refusals', halted'⟩ := t
  simp only [core, Core.mk.injEq] at h
  obtain ⟨_, _, hw, hp, ho, hr, _⟩ := h
  subst hw hp ho hr
  rfl

/-- A commuting translation into the passage that also carries a source
observation `obsA` to the native one, through an observation map. -/
structure ObsSim {S E O : Type} (g : S → E → S) (obsA : S → O) extends Sim g step where
  obsMap : O → NObs
  obs_comm : ∀ s, nobs (enc s) = obsMap (obsA s)

namespace ObsSim

variable {S E O : Type} {g : S → E → S} {obsA : S → O}

/-- On a source cycle the native observation sees one value. -/
theorem obs_on_cycle (m : ObsSim g obsA) {s t : S} (p : Path g s t) (q : Path g t s) :
    m.obsMap (obsA t) = m.obsMap (obsA s) := by
  rw [← m.obs_comm, ← m.obs_comm]
  exact nobs_of_core (passage_sim_cycle m.toSim p q)

/-- With a faithful observation map, the source observation is constant on
every cycle. -/
theorem obs_const_on_cycle (m : ObsSim g obsA)
    (hinj : ∀ a b, m.obsMap a = m.obsMap b → a = b)
    {s t : S} (p : Path g s t) (q : Path g t s) : obsA t = obsA s :=
  hinj _ _ (m.obs_on_cycle p q)

end ObsSim

/-- Every budget-register encoding has the native observation of genesis. -/
theorem budgetSim_nobs {S E : Type} (g : S → E → S) (code : S → Nat) (s : S) :
    nobs ((budgetSim g code).enc s) = nobs genesisP := rfl

/-- A budget register preserves an observation only when the observation
the passage sees is constant. -/
theorem budget_obs_const {S E O : Type} {g : S → E → S} {obsA : S → O} (code : S → Nat)
    (m : ObsSim g obsA) (henc : ∀ s, m.enc s = (budgetSim g code).enc s) (a b : S) :
    m.obsMap (obsA a) = m.obsMap (obsA b) := by
  rw [← m.obs_comm, ← m.obs_comm, henc, henc, budgetSim_nobs, budgetSim_nobs]

/-- The toggle, observed by its own state, has no translation into the
passage that preserves the observation faithfully. -/
theorem toggle_no_faithful_obs (m : ObsSim toggle (fun b : Bool => b))
    (hinj : ∀ a b, m.obsMap a = m.obsMap b → a = b) : False := by
  have h := m.obs_const_on_cycle hinj (s := true) (t := false)
    (Path.cons () (Path.nil false)) (Path.cons () (Path.nil true))
  exact Bool.false_ne_true h

/-- The identity translation of the passage into itself, observed
natively. -/
def idObsSim : ObsSim step nobs where
  enc := id
  tr := fun _ e => [e]
  comm := fun _ _ => rfl
  obsMap := id
  obs_comm := fun _ => rfl

theorem idObsSim_faithful (a b : NObs) (h : idObsSim.obsMap a = idObsSim.obsMap b) : a = b := h

end ResearchNativeBridge
