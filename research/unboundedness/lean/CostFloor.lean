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

namespace CostFloor

open Derivation
open LocalReuse
open Ignition
open Ignition.Driver

/-!
# Stratified Separation Cost Floor Theorem

This module establishes the lower bound on the cost of separating an
observational collapse in a regime.

The cost floor is stratified:
1. Every valid response to a collapsed pair has length at least 1
   (`valid_response_len_pos_of_collapsed`).
2. At genesis, when no forms or instances exist, any valid response has length
   at least 2 (`valid_response_len_ge_two_at_genesis`).
3. Under both declared measures `mu1` and `mu2`, the primary cost component
   `(cost m δ).1` is bounded below by 2 at genesis and by 1 post-genesis
   (`separation_cost_floor`).
4. Both bounds are attained (`genesis_mark_cost`, `post_genesis_inst_cost`).

AuthorityEffect: None.
-/

/-! ## 1. Inhabitation of Contexts and Derivability -/

/-- AuthorityEffect: None.
When forms are empty, no well-formed context exists. -/
theorem not_wfCtx_of_forms_empty {s : Regime} (h : s.forms = []) (c : Ctx) :
    ¬ wfCtx s c := by
  intro hwf
  have hlt := hwf.1
  rw [h] at hlt
  exact Nat.not_lt_zero _ hlt

/-- AuthorityEffect: None.
A regime with no admitted forms separates no pair of data. -/
theorem not_separable_of_forms_empty {s : Regime} (h : s.forms = []) (i j : Nat) :
    ¬ separable s i j := by
  rintro ⟨c, hwf, _⟩
  exact not_wfCtx_of_forms_empty h c hwf

/-- AuthorityEffect: None.
A regime with no instances and no rules separates no pair of data, because
every plugged context evaluates to false under derivability. -/
theorem not_separable_of_insts_rules_empty {s : Regime}
    (hi : s.insts = []) (hr : s.rules = []) (i j : Nat) :
    ¬ separable s i j := by
  rintro ⟨c, _, hdiff⟩
  apply hdiff
  dsimp [derivable]
  rw [hi, hr]
  simp

/-! ## 2. Lower Bounds on Response Length -/

/-- AuthorityEffect: None.
Any valid response separating a collapsed pair has length at least 1. -/
theorem valid_response_len_pos_of_collapsed {r : Regime} {i j : Nat} {δ : List Item}
    (hcol : collapsed r i j) (hval : validResponse r i j δ) : 1 ≤ δ.length := by
  match δ with
  | [] =>
      obtain ⟨s, hs, hsep, _⟩ := hval
      dsimp [applyDelta] at hs
      injection hs with hsr
      subst hsr
      exact absurd hcol (separable_not_collapsed hsep)
  | _ :: _ =>
      simp only [List.length_cons]
      omega

/-- AuthorityEffect: None.
At genesis, when the form and instance sets are empty, applying a response of
length at most 1 cannot separate any pair of data. -/
theorem valid_response_len_ge_two_at_genesis {r : Regime} {i j : Nat} {δ : List Item}
    (hf : r.forms = []) (hi : r.insts = []) (hr : r.rules = [])
    (hval : validResponse r i j δ) : 2 ≤ δ.length := by
  match δ with
  | [] =>
      obtain ⟨s, hs, hsep, _⟩ := hval
      dsimp [applyDelta] at hs
      injection hs with hsr
      subst hsr
      have hnot := not_separable_of_forms_empty hf i j
      exact absurd hsep hnot
  | [x] =>
      obtain ⟨s, hs, hsep, _⟩ := hval
      have hs' : applyItem r x = some s := by
        simpa [applyDelta] using hs
      cases x with
      | newDatum =>
          dsimp [applyItem] at hs'
          injection hs' with hsr
          subst hsr
          have hforms : ({ r with data := r.data + 1 } : Regime).forms = [] := hf
          have hnot := not_separable_of_forms_empty hforms i j
          exact absurd hsep hnot
      | newForm a =>
          dsimp [applyItem] at hs'
          split at hs'
          · injection hs' with hsr
            subst hsr
            have hinsts : ({ r with forms := r.forms ++ [a] } : Regime).insts = [] := hi
            have hrules : ({ r with forms := r.forms ++ [a] } : Regime).rules = [] := hr
            have hnot := not_separable_of_insts_rules_empty hinsts hrules i j
            exact absurd hsep hnot
          · contradiction
      | newInst fm args =>
          dsimp [applyItem] at hs'
          split at hs'
          · rename_i hlt
            have hlt' := hlt.1
            rw [hf] at hlt'
            exact absurd hlt' (Nat.not_lt_zero fm)
          · contradiction
      | newRuleAll fm =>
          dsimp [applyItem] at hs'
          split at hs'
          · rename_i hlt
            rw [hf] at hlt
            exact absurd hlt (Nat.not_lt_zero fm)
          · contradiction
  | _ :: _ :: _ =>
      simp only [List.length_cons]
      omega

/-! ## 3. Cost Floor Under Declared Measures -/

/-- AuthorityEffect: None.
Under both declared measures, the first component of cost is the item count. -/
theorem cost_fst (m : Measure) (δ : List Item) : (cost m δ).1 = δ.length := by
  cases m <;> rfl

/-- AuthorityEffect: None.
At genesis, any valid separation costs at least 2 in item count. -/
theorem separation_cost_floor_genesis {m : Measure} {r : Regime} {i j : Nat} {δ : List Item}
    (hf : r.forms = []) (hi : r.insts = []) (hr : r.rules = [])
    (hval : validResponse r i j δ) : 2 ≤ (cost m δ).1 := by
  rw [cost_fst]
  exact valid_response_len_ge_two_at_genesis hf hi hr hval

/-- AuthorityEffect: None.
Post-genesis, any valid response separating a collapsed pair costs at least 1. -/
theorem separation_cost_floor_post_genesis {m : Measure} {r : Regime} {i j : Nat} {δ : List Item}
    (hcol : collapsed r i j) (hval : validResponse r i j δ) : 1 ≤ (cost m δ).1 := by
  rw [cost_fst]
  exact valid_response_len_pos_of_collapsed hcol hval

/-- AuthorityEffect: None.
The stratified separation cost floor theorem:
separation costs at least 2 at genesis and at least 1 post-genesis. -/
theorem separation_cost_floor {m : Measure} {r : Regime} {i j : Nat} {δ : List Item}
    (hcol : collapsed r i j)
    (hi : r.forms = [] → r.insts = [])
    (hr : r.forms = [] → r.rules = [])
    (hval : validResponse r i j δ) :
    (if r.forms = [] then 2 else 1) ≤ (cost m δ).1 := by
  by_cases hf : r.forms = []
  · rw [if_pos hf]
    exact separation_cost_floor_genesis hf (hi hf) (hr hf) hval
  · rw [if_neg hf]
    exact separation_cost_floor_post_genesis hcol hval

/-! ## 4. Sharpness -/

/-- AuthorityEffect: None.
The fresh mark delta has cost 2 under both measures. -/
theorem genesis_mark_cost (m : Measure) : (cost m [.newForm 1, .newInst 0 [1]]).1 = 2 := by
  cases m <;> rfl

/-- AuthorityEffect: None.
A single instance has cost 1 under both measures. -/
theorem post_genesis_inst_cost (m : Measure) (f : Nat) (j : Nat) :
    (cost m [.newInst f [j]]).1 = 1 := by
  cases m <;> rfl

end CostFloor

#print axioms CostFloor.not_wfCtx_of_forms_empty
#print axioms CostFloor.not_separable_of_forms_empty
#print axioms CostFloor.not_separable_of_insts_rules_empty
#print axioms CostFloor.valid_response_len_pos_of_collapsed
#print axioms CostFloor.valid_response_len_ge_two_at_genesis
#print axioms CostFloor.cost_fst
#print axioms CostFloor.separation_cost_floor_genesis
#print axioms CostFloor.separation_cost_floor_post_genesis
#print axioms CostFloor.separation_cost_floor
#print axioms CostFloor.genesis_mark_cost
#print axioms CostFloor.post_genesis_inst_cost
