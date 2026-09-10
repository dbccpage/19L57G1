import Carrier

/-!
# W06: Observer Record Exchange

Models two observers receiving projected observations of a shared multi-locus
carrier (L1 x L2 x M).
1. Projections: π1(s) = (s.l1, s.m), π2(s) = (s.l2, s.m).
2. Symmetry and Agreement: If the carrier state is symmetric under swap (s.l1 = s.l2),
   both observers receive identical observations and make identical decisions.
3. Represented Message Transmission: Observer 1 writes to the shared buffer M.
4. Decision Divergence: Observer 2 reads from M and branches, demonstrating causal
   information transfer without external host oracles.
5. Negative Control: When Observer 1 only modifies L1 without writing to M, Observer 2's
   state is strictly invariant across different Observer 1 states.

AuthorityEffect: None.
-/

namespace Concurrency

/-- A carrier state is symmetric if the two observers' local coordinates are identical. -/
def IsSymmetric (s : State3) : Prop := s.l1 = s.l2

/-- Swapping a symmetric state leaves the state unchanged. -/
theorem swap_symmetric_eq (s : State3) (hs : IsSymmetric s) : swap s = s := by
  dsimp [swap, IsSymmetric] at *
  cases s
  dsimp at *
  rw [hs]

/-- **Symmetry Agreement Theorem.**
    Under state symmetry, both observers obtain identical projected observations. -/
theorem symmetry_agreement (s : State3) (hs : IsSymmetric s) :
    proj1 s = proj2 s := by
  dsimp [proj1, proj2, IsSymmetric] at *
  rw [hs]

/-- Identical local decision policies yield matching choices under symmetry. -/
theorem decision_agreement {α : Type} (dec : Nat × Nat → α) (s : State3) (hs : IsSymmetric s) :
    dec (proj1 s) = dec (proj2 s) := by
  rw [symmetry_agreement s hs]

/-- Observer 1 transmits its local coordinate to the shared message cell M. -/
def transmitL1 (s : State3) : State3 :=
  { s with m := s.l1 }

/-- Observer 1 transmits an arbitrary represented value to M. -/
def transmitVal (v : Nat) (s : State3) : State3 :=
  { s with m := v }

/-- Observer 2 receives the message from M and updates its local coordinate L2. -/
def receiveM (s : State3) : State3 :=
  { s with l2 := s.m }

/-- A complete exchange round: Observer 1 transmits, then Observer 2 receives. -/
def exchangeRound (s : State3) : State3 :=
  receiveM (transmitL1 s)

/-- **Decision Divergence Theorem.**
    Two runs starting with identical Observer 2 coordinates and identical buffer M,
    but differing in Observer 1's coordinate, causally diverge in Observer 2's final
    decision solely through the represented message exchange. -/
theorem decision_divergence :
    let s0 : State3 := { l1 := 0, l2 := 0, m := 0 }
    let s1 : State3 := { l1 := 1, l2 := 0, m := 0 }
    s0.l2 = s1.l2 ∧
    s0.m = s1.m ∧
    (exchangeRound s0).l2 ≠ (exchangeRound s1).l2 := by
  dsimp [exchangeRound, receiveM, transmitL1]
  decide

/-- Local update at L1 with no transmission to M (Observer 1 uncoupled move). -/
def localStepL1 (f : Nat → Nat) (s : State3) : State3 :=
  { s with l1 := f s.l1 }

/-- **Negative Control Theorem: Information Isolation.**
    Without transmission through the shared cell M, variations in Observer 1's
    local coordinate cannot cause Observer 2's subsequent state to diverge. -/
theorem uncoupled_preserves_receiver (f : Nat → Nat) (s0 s1 : State3)
    (hm : s0.m = s1.m) :
    (receiveM (localStepL1 f s0)).l2 = (receiveM (localStepL1 f s1)).l2 := by
  dsimp [receiveM, localStepL1]
  rw [hm]

end Concurrency
