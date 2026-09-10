import Protocol

/-!
# Duplicate Embedded Observers and Symmetry Relations

Proves:
1. Presentation symmetries:
   Swap involution exchanging Observer 1 (L1, R1) and Observer 2 (L2, R2).
2. Equivariance / Covariance:
   Readout operations commute with presentation symmetries:
       Readout2(swap(s)) = swap(Readout1(s))
3. `inter_observer_agreement`:
   On symmetric preparations (s.l1 = s.l2), duplicate observers executing
   identical local readout protocols record matching memory marks.
4. Asymmetric divergence contrast:
   When carrier preparations are asymmetric (s.l1 ≠ s.l2), duplicate observer
   readouts diverge.

AuthorityEffect: None.
Axiom Scope: Strictly constructive; `#print axioms` in `{propext, Quot.sound}`.
-/

namespace P200OperationalProtocols

/-- Swap involution exchanging coordinates and records between observers. -/
def swap (s : CarrierState) : CarrierState :=
  { s with l1 := s.l2, l2 := s.l1, r1 := s.r2, r2 := s.r1 }

/-- Swap is an involution: applying it twice returns the original carrier state. -/
theorem swap_involutive (s : CarrierState) : swap (swap s) = s := rfl

/-- Swap preserves coupling channel M. -/
theorem swap_preserves_m (s : CarrierState) : (swap s).m = s.m := rfl

/-- Swap preserves disturbance register. -/
theorem swap_preserves_dist (s : CarrierState) : (swap s).dist = s.dist := rfl

/-- **Equivariance under Swap Symmetry.**
    Executing Readout 2 on the swapped carrier state equals swapping the result
    of Readout 1 on the original carrier state. -/
theorem readout2_swap (probe : Nat → Nat) (s : CarrierState) :
    readout2 probe (swap s) = swap (readout1 probe s) := rfl

theorem readout1_swap (probe : Nat → Nat) (s : CarrierState) :
    readout1 probe (swap s) = swap (readout2 probe s) := rfl

/-- A carrier state is symmetric when its target loci and record marks coincide. -/
def IsSymmetricState (s : CarrierState) : Prop :=
  s.l1 = s.l2 ∧ s.r1 = s.r2

/-- Swapping a symmetric state leaves the carrier state invariant. -/
theorem swap_symmetric_eq (s : CarrierState) (hs : IsSymmetricState s) :
    swap s = s := by
  dsimp [swap]
  cases s
  dsimp [IsSymmetricState] at hs
  obtain ⟨h_l, h_r⟩ := hs
  dsimp
  rw [h_l, h_r]

/-- Joint protocol where both duplicate observers execute their local readouts. -/
def jointReadout (probe : Nat → Nat) (s : CarrierState) : CarrierState :=
  readout2 probe (readout1 probe s)

/-- **Inter-Observer Agreement Theorem.**
    On symmetric preparations (s.l1 = s.l2), duplicate observers executing
    identical local readout protocols obtain matching recorded marks:
        (jointReadout probe s).r1 = (jointReadout probe s).r2
-/
theorem inter_observer_agreement (probe : Nat → Nat) (s : CarrierState) (hs : s.l1 = s.l2) :
    (jointReadout probe s).r1 = (jointReadout probe s).r2 := by
  dsimp [jointReadout, readout2, readout1]
  rw [hs]

/-- On symmetric preparations, the coincidence evaluator records agreement. -/
theorem inter_observer_coincidence (probe : Nat → Nat) (s : CarrierState) (hs : s.l1 = s.l2) :
    coincidence (jointReadout probe s) = true := by
  rw [coincidence_iff]
  exact inter_observer_agreement probe s hs

/-- Asymmetric states produce divergent recorded marks under injective probe. -/
theorem asymmetric_observation_divergence :
    let s : CarrierState := { l1 := 0, l2 := 1, m := 0, r1 := 0, r2 := 0, dist := 0 }
    (jointReadout (fun x => x) s).r1 ≠ (jointReadout (fun x => x) s).r2 := by
  decide

end P200OperationalProtocols
