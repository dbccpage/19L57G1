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
import Driver

namespace Unboundedness

open Derivation
open LocalReuse
open Ignition
open Ignition.Driver

/-!
# Unboundedness of the Extension and Analysis of the Minimum Driver

This module formalizes the growth of the data carrier and the depth of the
quotient structure under the extension relation `XStep` and the engine driver
relation `EngineDriver` under measure `mu2`.

AuthorityEffect: None.
-/

/-! ## 1. Refinement and Invariants -/

/-- AuthorityEffect: None.
Every driver transition refines the permissive extension step `XStep`. -/
theorem driver_step_refines_xstep {m : Ignition.Driver.Measure} {supply : Bool} {r t : Regime}
    (h : EngineDriver m supply r t) : XStep r t :=
  engineDriver_refines_xstep h

/-- AuthorityEffect: None.
Driver transitions preserve the `Good` state invariant. -/
theorem driver_step_good {m : Ignition.Driver.Measure} {supply : Bool} {r t : Regime}
    (hg : Ignition.Good r) (h : EngineDriver m supply r t) : Ignition.Good t :=
  good_driver hg h

/-! ## 2. Data Carrier Monotonicity -/

/-- AuthorityEffect: None.
Imposing a requirement preserves the data count. -/
theorem stepE_impose_data (r : Regime) (i j : Nat) (mid : Regime)
    (h : stepE r (.impose i j) = some mid) : mid.data = r.data := by
  dsimp [stepE] at h
  split at h
  · injection h with hmid
    subst hmid
    rfl
  · contradiction

/-- AuthorityEffect: None.
Applying a response delta never decreases the data count of a regime. -/
theorem respond_data_mono {r t : Regime} {i j : Nat} {δ : List Item}
    (h : respond r i j δ = some t) : r.data ≤ t.data := by
  unfold respond at h
  cases hmid : stepE r (.impose i j) with
  | none =>
      rw [hmid] at h
      contradiction
  | some mid =>
      rw [hmid] at h
      have hdata := stepE_impose_data r i j mid hmid
      have hmono := applyDelta_data_mono (s := t) h
      omega

/-- AuthorityEffect: None.
Firing on a demand never decreases the data count. -/
theorem fire_data_mono {m : Ignition.Driver.Measure} {r t : Regime} {i j : Nat} {δ : List Item}
    (h : Ignition.Driver.Fire m r i j δ t) : r.data ≤ t.data :=
  respond_data_mono h.2.2.2.2

/-- AuthorityEffect: None.
Every engine driver transition is monotonically non-decreasing in data count. -/
theorem driver_data_mono {m : Ignition.Driver.Measure} {supply : Bool} {r t : Regime}
    (h : EngineDriver m supply r t) : r.data ≤ t.data := by
  cases h with
  | fire hf =>
      obtain ⟨i, j, δ, _, hfire⟩ := hf
      exact fire_data_mono hfire
  | grow _ _ =>
      show r.data ≤ r.data + 1
      omega

/-- AuthorityEffect: None.
Driver paths preserve monotonicity of the data count. -/
theorem driver_path_data_mono {m : Ignition.Driver.Measure} {supply : Bool}
    {r t : Regime} {states : List Regime}
    (h : DriverPath m supply r states t) : r.data ≤ t.data := by
  induction h with
  | nil => exact Nat.le_refl _
  | cons hstep _ ih =>
      have h1 := driver_data_mono hstep
      exact Nat.le_trans h1 ih

/-- AuthorityEffect: None.
Growth strictly increases the data count by one. -/
theorem quiet_grow_data_succ (r : Regime) : (Ignition.grow r).data = r.data + 1 := rfl

/-! ## 3. Response Existence Under Bound Conditions -/

/-- AuthorityEffect: None.
For any pair of distinct admitted data in a good regime, the fresh-mark
construction yields a valid response within the declared bounds. -/
theorem good_has_inBounds_valid (r : Regime) (hg : Ignition.Good r)
    (i j : Nat) (hij : i < j) (hjd : j < r.data) :
    Ignition.Driver.InBounds [.newForm 1, .newInst r.forms.length [j]] ∧
      validResponse r i j [.newForm 1, .newInst r.forms.length [j]] :=
  mark_response_inBounds hg hij hjd

/-- AuthorityEffect: None.
When external supply is enabled, a quiet regime admits extension by growth. -/
theorem quiet_state_extends_with_supply {m : Ignition.Driver.Measure}
    {r : Regime} (hq : Ignition.Driver.Quiet r) :
    EngineDriver m true r (Ignition.grow r) :=
  quiet_driver_grow hq

/-! ## 4. Permissive Unboundedness of the Quotient Tree -/

/-- AuthorityEffect: None.
The data count along the permissive runState iteration increases by two
at each horizon step. -/
theorem xstep_runState_data (r : Regime) (k : Nat) :
    (runState r k).data = r.data + 2 * k :=
  runState_data r k

/-- AuthorityEffect: None.
Each state in the runState sequence is good. -/
theorem xstep_runState_good {r : Regime} (hg : Ignition.Good r) (k : Nat) :
    Ignition.Good (runState r k) :=
  runState_good hg k

/-- AuthorityEffect: None.
The runHist sequence replays through the sealed step at each horizon. -/
theorem xstep_runHist_replays {r : Regime} (hg : Ignition.Good r) (k : Nat) :
    replayE (runHist r k) r = some (runState r k) :=
  runHist_replays hg k

/-- AuthorityEffect: None.
For each natural number n, there exists a regime reachable by replay
from any good root whose data count exceeds r.data + n. -/
theorem xstep_unbounded_exists (r : Regime) (hg : Ignition.Good r) (n : Nat) :
    ∃ (s : Regime) (hist : List Event),
      replayE hist r = some s ∧ Ignition.Good s ∧ s.data ≥ r.data + n := by
  refine ⟨runState r n, runHist r n, xstep_runHist_replays hg n, xstep_runState_good hg n, ?_⟩
  rw [xstep_runState_data]
  omega

/-! ## 5. Carrier Distinction -/

/-- AuthorityEffect: None.
Regimes with different data counts have distinct data carrier sizes. -/
theorem data_count_injective {r s : Regime} (h : r.data ≠ s.data) :
    r ≠ s := by
  intro heq
  subst heq
  exact h rfl

/-! ## 6. The Minimum Driver Gap -/

/-- AuthorityEffect: None.
A single instance on an existing form has lexicographic cost (1, 0)
under measure mu2. -/
theorem cost_single_inst_mu2 (f : Nat) (args : List Nat) :
    Ignition.Driver.cost .mu2 [.newInst f args] = (1, 0) := rfl

/-- AuthorityEffect: None.
A fresh form of arity 1 with an instance has lexicographic cost (2, 1)
under measure mu2. -/
theorem cost_mark_delta_mu2 (f : Nat) (args : List Nat) :
    Ignition.Driver.cost .mu2 [.newForm 1, .newInst f args] = (2, 1) := rfl

/-- AuthorityEffect: None.
A single instance on an existing form has strictly lower cost than
the fresh mark delta under measure mu2. -/
theorem single_inst_beats_fresh_mark (f1 f2 : Nat) (args1 args2 : List Nat) :
    Ignition.Driver.lexLE (Ignition.Driver.cost .mu2 [.newInst f1 args1])
      (Ignition.Driver.cost .mu2 [.newForm 1, .newInst f2 args2]) := by
  rw [cost_single_inst_mu2, cost_mark_delta_mu2]
  exact Or.inl (by decide)

end Unboundedness

#print axioms Unboundedness.driver_step_refines_xstep
#print axioms Unboundedness.driver_step_good
#print axioms Unboundedness.stepE_impose_data
#print axioms Unboundedness.respond_data_mono
#print axioms Unboundedness.fire_data_mono
#print axioms Unboundedness.driver_data_mono
#print axioms Unboundedness.driver_path_data_mono
#print axioms Unboundedness.quiet_grow_data_succ
#print axioms Unboundedness.good_has_inBounds_valid
#print axioms Unboundedness.quiet_state_extends_with_supply
#print axioms Unboundedness.xstep_runState_data
#print axioms Unboundedness.xstep_runState_good
#print axioms Unboundedness.xstep_runHist_replays
#print axioms Unboundedness.xstep_unbounded_exists
#print axioms Unboundedness.data_count_injective
#print axioms Unboundedness.cost_single_inst_mu2
#print axioms Unboundedness.cost_mark_delta_mu2
#print axioms Unboundedness.single_inst_beats_fresh_mark
