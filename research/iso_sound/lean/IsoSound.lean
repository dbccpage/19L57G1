import Derivation.Basic
import Derivation.Inertia

/-!
# Kernel facts for the CL-ISO-SOUND hunt

The hunt itself is a finite computation over a declared Python space
(`research/iso_sound`).  The general converse — isomorphic regimes have
equal refined canonical keys, and equal refined keys imply isomorphism —
is **OPEN**, matching the sealed ledger field `CL-ISO-SOUND` Lean:
unresolved.

This module records only what the sealed identity presentation already
gives: the empty regime is unique among 0-data, 0-form, empty-store
regimes, and two regimes with equal fields are equal.  That is the
identity serialization, not the refined key.

AuthorityEffect: None.
-/

namespace IsoSound

open Derivation

theorem genesis_data : genesis.data = 0 := rfl

theorem genesis_forms : genesis.forms = [] := rfl

theorem genesis_insts : genesis.insts = [] := rfl

theorem genesis_rules : genesis.rules = [] := rfl

theorem genesis_reqs : genesis.reqs = [] := rfl

theorem genesis_wf : genesis.wf := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro p hp; cases hp
  · intro f hf; cases hf
  · intro q hq; cases hq
  · intro a ha; cases ha

theorem genesis_unique (r : Regime)
    (hd : r.data = 0) (hf : r.forms = [])
    (hi : r.insts = []) (hr : r.rules = []) (hq : r.reqs = []) :
    r = genesis := by
  cases r
  cases hd
  cases hf
  cases hi
  cases hr
  cases hq
  rfl

theorem equal_of_fields {r s : Regime}
    (hd : r.data = s.data) (hf : r.forms = s.forms)
    (hi : r.insts = s.insts) (hr : r.rules = s.rules)
    (hq : r.reqs = s.reqs) : r = s := by
  cases r
  cases s
  cases hd
  cases hf
  cases hi
  cases hr
  cases hq
  rfl

/-- The general refined-key / isomorphism bridge is not proved here. -/
def GeneralBridgeOpen : Prop := True

theorem general_bridge_recorded_open : GeneralBridgeOpen := trivial

end IsoSound

#print axioms IsoSound.genesis_data
#print axioms IsoSound.genesis_forms
#print axioms IsoSound.genesis_insts
#print axioms IsoSound.genesis_rules
#print axioms IsoSound.genesis_reqs
#print axioms IsoSound.genesis_wf
#print axioms IsoSound.genesis_unique
#print axioms IsoSound.equal_of_fields
#print axioms IsoSound.general_bridge_recorded_open
