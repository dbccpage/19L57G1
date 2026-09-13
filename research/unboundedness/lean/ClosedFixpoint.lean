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
import Unboundedness

namespace ClosedFixpoint

open Derivation
open LocalReuse
open Ignition
open Ignition.Driver

/-!
# Closed-System Finite Quiet Fixpoint Theorem

This module formalizes the closed-system dynamics under the engine driver
relation `EngineDriver m false`.

We prove:
1. **Grow refusal**: Under `supply = false`, the growth transition is refused;
   every closed driver transition is an engine fire step (`closed_driver_is_fire`).
2. **Demand not in requirement store**: In any good regime, an orbit demand
   is not already present in the requirement store (`fire_demand_not_in_reqs`).
3. **Strict requirement accumulation**: Each fire step strictly increases the
   requirement count by exactly one (`fire_reqs_length_succ`).
4. **Carrier invariance**: Firing a response without a fresh datum preserves
   the carrier size (`fire_data_eq`).
5. **Fixed-carrier round bound**: A `ClosedRun` (not an `EngineDriver`
   path) without external data growth satisfies
   `2 * (r.reqs.length + rds.length) ≤ r.data * (r.data - 1)` under the
   side conditions `r.reqs.Nodup` and `∀ q ∈ r.reqs, q.1 < q.2 ∧ q.2 < r.data`
   (`closed_round_bound`). Those hypotheses are not discharged for an
   engine-reachable regime in this package.
6. **From empty requirements**: When the initial requirement store is empty,
   `2 * rds.length ≤ r.data * (r.data - 1)` (`closed_round_bound_from_empty`).
7. **Finite fixpoint depths under stated start hypotheses** (mnemonic names
   only; cite by hypotheses, not by reading L/F):
   - any `ClosedRun` with `data = 2` and `reqs = []` has length at most 1
     (`reading_L_max_rounds`);
   - any `ClosedRun` with `data = 3` and `reqs = []` has length at most 3
     (`reading_F_max_rounds`).
8. **Quiet fixpoint**: At a quiet state with supply disabled, no driver
   step exists (`closed_quiet_terminates`).

AuthorityEffect: None.
-/

/-! ## 1. Closed Driver Refusal and Firing Characterization -/

/-- AuthorityEffect: None.
Under supply = false, every engine driver transition is a fire step. -/
theorem closed_driver_is_fire {m : Measure} {r t : Regime}
    (h : EngineDriver m false r t) : EngineFire m r t := by
  cases h with
  | fire hf => exact hf
  | grow hsupp _ => contradiction

/-- AuthorityEffect: None.
In a good regime, the demand pair answered by a fire step was not already in
the requirement store. -/
theorem fire_demand_not_in_reqs {m : Measure} {r t : Regime} {i j : Nat} {δ : List Item}
    (hg : Good r) (hf : Fire m r i j δ t) : (i, j) ∉ r.reqs := by
  intro hmem
  have hsep := hg.2.2 (i, j) hmem
  have hnot := separable_not_collapsed hsep
  exact hnot hf.2.2.1

/-- AuthorityEffect: None.
Each fire step increments the requirement store length by exactly one. -/
theorem fire_reqs_length_succ {m : Measure} {r t : Regime} {i j : Nat} {δ : List Item}
    (hg : Good r) (hf : Fire m r i j δ t) : t.reqs.length = r.reqs.length + 1 := by
  have hnot := fire_demand_not_in_reqs hg hf
  exact round_reqs_succ hnot hf.2.2.2.2

/-- AuthorityEffect: None.
Firing a response delta with no fresh datum preserves the carrier size. -/
theorem fire_data_eq {m : Measure} {r t : Regime} {i j : Nat} {δ : List Item}
    (hnd : Item.newDatum ∉ δ) (hf : Fire m r i j δ t) : t.data = r.data :=
  round_data_eq hnd hf.2.2.2.2

/-! ## 2. Round Bounds on Closed Runs -/

/-- AuthorityEffect: None.
A `ClosedRun` on a fixed carrier satisfies the quadratic round bound under
`Nodup` and ordered in-range pairs. This is not a theorem about
`EngineDriver m false`. -/
theorem closed_round_bound {r t : Regime} {rds : List Round}
    (h : ClosedRun r rds t) (hn : r.reqs.Nodup)
    (hwf : ∀ q ∈ r.reqs, q.1 < q.2 ∧ q.2 < r.data) :
    2 * (r.reqs.length + rds.length) ≤ r.data * (r.data - 1) :=
  closedRun_round_bound h hn hwf

/-- AuthorityEffect: None.
From an empty requirement store, closed runs satisfy `2 * rds.length ≤ d * (d - 1)`. -/
theorem closed_round_bound_from_empty {r t : Regime} {rds : List Round}
    (h : ClosedRun r rds t) (he : r.reqs = []) :
    2 * rds.length ≤ r.data * (r.data - 1) :=
  closedRun_round_bound_from_empty h he

/-! ## 3. Finite Fixpoints for Challenge Regimes -/

/-! ### Naming scope

The `reading_L` / `reading_F` names below are **mnemonic only**. Each theorem
bounds *any* closed run whose start regime satisfies the stated hypotheses
(`data = 2` resp. `3`, and `reqs = []`). Nothing here proves that the
derivation's reading L or reading F actually starts from such a regime; that
binding is not established in this package. Cite these by their hypotheses,
not by their names. -/

/-- AuthorityEffect: None.
Any closed run with `data = 2` and `reqs = []` has length at most 1.
The name is mnemonic; nothing here binds the start to reading L. -/
theorem reading_L_max_rounds {start finish : Regime} {rds : List Round}
    (hdata : start.data = 2) (hreqs : start.reqs = [])
    (h : ClosedRun start rds finish) : rds.length ≤ 1 := by
  have hb := closedRun_round_bound_from_empty h hreqs
  rw [hdata] at hb
  omega

/-- AuthorityEffect: None.
Two closed rounds on two data from an empty requirement store are excluded. -/
theorem no_two_closed_rounds_on_two_data {start finish : Regime}
    {rds : List Round} (hdata : start.data = 2) (hreqs : start.reqs = [])
    (hrds : 2 ≤ rds.length) : ¬ ClosedRun start rds finish := by
  intro h
  have hle := reading_L_max_rounds hdata hreqs h
  omega

/-- AuthorityEffect: None.
Any closed run with `data = 3` and `reqs = []` has length at most 3.
The name is mnemonic; nothing here binds the start to reading F. -/
theorem reading_F_max_rounds {start finish : Regime} {rds : List Round}
    (hdata : start.data = 3) (hreqs : start.reqs = [])
    (h : ClosedRun start rds finish) : rds.length ≤ 3 := by
  have hb := closedRun_round_bound_from_empty h hreqs
  rw [hdata] at hb
  omega

/-- AuthorityEffect: None.
Four closed rounds on three data from an empty requirement store are excluded. -/
theorem no_four_closed_rounds_on_three_data {start finish : Regime}
    {rds : List Round} (hdata : start.data = 3) (hreqs : start.reqs = [])
    (hrds : 4 ≤ rds.length) : ¬ ClosedRun start rds finish := by
  intro h
  have hle := reading_F_max_rounds hdata hreqs h
  omega

/-! ## 4. Quiet Termination -/

/-- AuthorityEffect: None.
At a quiet state with supply disabled, no engine driver transition exists. -/
theorem closed_quiet_terminates {m : Measure} {r : Regime} (hq : Quiet r) :
    ¬ ∃ t, EngineDriver m false r t :=
  quiet_no_driver_step hq

end ClosedFixpoint

#print axioms ClosedFixpoint.closed_driver_is_fire
#print axioms ClosedFixpoint.fire_demand_not_in_reqs
#print axioms ClosedFixpoint.fire_reqs_length_succ
#print axioms ClosedFixpoint.fire_data_eq
#print axioms ClosedFixpoint.closed_round_bound
#print axioms ClosedFixpoint.closed_round_bound_from_empty
#print axioms ClosedFixpoint.reading_L_max_rounds
#print axioms ClosedFixpoint.no_two_closed_rounds_on_two_data
#print axioms ClosedFixpoint.reading_F_max_rounds
#print axioms ClosedFixpoint.no_four_closed_rounds_on_three_data
#print axioms ClosedFixpoint.closed_quiet_terminates
