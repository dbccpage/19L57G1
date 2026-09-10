import Protocol
import Commutation

/-!
# Spacelike Non-Signaling & Marginal Invariance

Establishes:
1. `spacelike_non_signaling`:
   Local interventions at Locus 1 do not perturb the outcome of readouts
   at Locus 2 prior to relational step propagation.
2. `spacelike_marginal_invariance`:
   Observer 2's projected observation `proj2` is invariant under arbitrary
   interventions at Locus 1.
3. Arbitrary sequential interventions at Locus 1 leave distant readouts invariant.
4. Causal propagation contrast:
   Signaling is enabled strictly after relational step propagation through
   mediating channel M.

AuthorityEffect: None.
Axiom Scope: Strictly constructive; `#print axioms` in `{propext, Quot.sound}`.
-/

namespace P200OperationalProtocols

/-- **Spacelike Non-Signaling Theorem.**
    For any local intervention `f` at Locus 1 and any readout instrument `probe`
    at Locus 2, Observer 2's recorded mark is strictly invariant under `f`:
        (readout2 probe (interveneL1 f s)).r2 = (readout2 probe s).r2
-/
theorem spacelike_non_signaling (f : Nat → Nat) (probe : Nat → Nat) (s : CarrierState) :
    (readout2 probe (interveneL1 f s)).r2 = (readout2 probe s).r2 := rfl

/-- **Marginal Observation Invariance.**
    Observer 2's full projected observation (target coordinate, record mark)
    is invariant under arbitrary local interventions at Locus 1. -/
theorem spacelike_marginal_invariance (f : Nat → Nat) (s : CarrierState) :
    proj2 (interveneL1 f s) = proj2 s := rfl

/-- Marginal readout record at Observer 2 is invariant under Locus 1 intervention. -/
theorem spacelike_marginal2_invariance (f : Nat → Nat) (s : CarrierState) :
    marginal2 (interveneL1 f s) = marginal2 s := rfl

/-- Sequential interventions at Locus 1 cannot perturb distant Observer 2 readout. -/
theorem spacelike_sequence_non_signaling (f g : Nat → Nat) (probe : Nat → Nat) (s : CarrierState) :
    (readout2 probe (interveneL1 g (interveneL1 f s))).r2 = (readout2 probe s).r2 := rfl

/-- Relay step 1: Locus 1 transmits state to coupling channel M. -/
def relayTransmitL1 (s : CarrierState) : CarrierState :=
  { s with m := s.l1 }

/-- Relay step 2: Locus 2 receives state from coupling channel M. -/
def relayReceiveM (s : CarrierState) : CarrierState :=
  { s with l2 := s.m }

/-- Full relational step propagation across the carrier through channel M. -/
def causalRelay (s : CarrierState) : CarrierState :=
  relayReceiveM (relayTransmitL1 s)

/-- **Causal Propagation Contrast Theorem.**
    While spacelike separation demonstrates zero readout perturbation,
    relational propagation through mediating channel M allows causal signaling. -/
theorem causal_signaling_divergence :
    let s0 : CarrierState := { l1 := 0, l2 := 0, m := 0, r1 := 0, r2 := 0, dist := 0 }
    let s1 : CarrierState := { l1 := 1, l2 := 0, m := 0, r1 := 0, r2 := 0, dist := 0 }
    (readout2 (fun x => x) (causalRelay s0)).r2 ≠
    (readout2 (fun x => x) (causalRelay s1)).r2 := by
  decide

end P200OperationalProtocols
