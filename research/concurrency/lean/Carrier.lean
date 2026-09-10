/-!
# Multi-Locus Product Carrier: L1 x L2 x M

Constructive three-locus product carrier for concurrent operational semantics.
- Locus 1: Observer 1's local coordinate (capacity n1)
- Locus 2: Observer 2's local coordinate (capacity n2)
- Locus M: Shared message/coupling cell (capacity nm)

AuthorityEffect: None.
-/

namespace Concurrency

/-- Three-locus product state. -/
@[ext]
structure State3 where
  l1 : Nat
  l2 : Nat
  m  : Nat
  deriving DecidableEq, Repr

/-- Validity predicate: coordinates remain strictly bounded by locus capacities. -/
def State3.valid (n1 n2 nm : Nat) (s : State3) : Prop :=
  s.l1 < n1 ∧ s.l2 < n2 ∧ s.m < nm

/-- Bijective canonical packing of 3-locus state into a single natural number. -/
def pack3 (n2 nm : Nat) (s : State3) : Nat :=
  nm * (n2 * s.l1 + s.l2) + s.m

/-- Unpacking a natural number back into a 3-locus state. -/
def unpack3 (n2 nm : Nat) (x : Nat) : State3 :=
  { l1 := (x / nm) / n2
    l2 := (x / nm) % n2
    m  := x % nm }

/-- Projected observation for Observer 1: (local state L1, message buffer M). -/
def proj1 (s : State3) : Nat × Nat := (s.l1, s.m)

/-- Projected observation for Observer 2: (local state L2, message buffer M). -/
def proj2 (s : State3) : Nat × Nat := (s.l2, s.m)

/-- Projected observation of the shared message cell. -/
def projM (s : State3) : Nat := s.m

/-- Local update at Locus 1. -/
def updateL1 (f : Nat → Nat) (s : State3) : State3 := { s with l1 := f s.l1 }

/-- Local update at Locus 2. -/
def updateL2 (g : Nat → Nat) (s : State3) : State3 := { s with l2 := g s.l2 }

/-- Local update at the shared Message Locus M. -/
def updateM (h : Nat → Nat) (s : State3) : State3 := { s with m := h s.m }

/-- An update at Locus 1 leaves Locus 2 unchanged. -/
theorem updateL1_preserves_l2 (f : Nat → Nat) (s : State3) : (updateL1 f s).l2 = s.l2 := rfl

/-- An update at Locus 1 leaves Message Locus M unchanged. -/
theorem updateL1_preserves_m (f : Nat → Nat) (s : State3) : (updateL1 f s).m = s.m := rfl

/-- An update at Locus 2 leaves Locus 1 unchanged. -/
theorem updateL2_preserves_l1 (g : Nat → Nat) (s : State3) : (updateL2 g s).l1 = s.l1 := rfl

/-- An update at Locus 2 leaves Message Locus M unchanged. -/
theorem updateL2_preserves_m (g : Nat → Nat) (s : State3) : (updateL2 g s).m = s.m := rfl

/-- An update at Message Locus M leaves Locus 1 unchanged. -/
theorem updateM_preserves_l1 (h : Nat → Nat) (s : State3) : (updateM h s).l1 = s.l1 := rfl

/-- An update at Message Locus M leaves Locus 2 unchanged. -/
theorem updateM_preserves_l2 (h : Nat → Nat) (s : State3) : (updateM h s).l2 = s.l2 := rfl

/-- Disjoint updates on L1 and L2 commute. -/
theorem updateL1_updateL2_comm (f g : Nat → Nat) (s : State3) :
    updateL1 f (updateL2 g s) = updateL2 g (updateL1 f s) := rfl

/-- Disjoint updates on L1 and M commute. -/
theorem updateL1_updateM_comm (f h : Nat → Nat) (s : State3) :
    updateL1 f (updateM h s) = updateM h (updateL1 f s) := rfl

/-- Disjoint updates on L2 and M commute. -/
theorem updateL2_updateM_comm (g h : Nat → Nat) (s : State3) :
    updateL2 g (updateM h s) = updateM h (updateL2 g s) := rfl

/-- Symmetry swap involution exchanging observers L1 and L2 while preserving M. -/
def swap (s : State3) : State3 := { l1 := s.l2, l2 := s.l1, m := s.m }

/-- Swap is an involution: applying it twice returns the original state. -/
theorem swap_involutive (s : State3) : swap (swap s) = s := rfl

/-- Swap preserves the shared message buffer M. -/
theorem swap_preserves_m (s : State3) : (swap s).m = s.m := rfl

/-- Observer 1's view of the swapped state equals Observer 2's view of the original state. -/
theorem proj1_swap_eq_proj2 (s : State3) : proj1 (swap s) = proj2 s := rfl

/-- Observer 2's view of the swapped state equals Observer 1's view of the original state. -/
theorem proj2_swap_eq_proj1 (s : State3) : proj2 (swap s) = proj1 s := rfl

/-- Round-trip: unpacking a packed valid state recovers the original state. -/
theorem unpack3_pack3 {n2 nm : Nat} (hn2 : 0 < n2) (hnm : 0 < nm) (s : State3)
    (h2 : s.l2 < n2) (hm : s.m < nm) : unpack3 n2 nm (pack3 n2 nm s) = s := by
  dsimp [unpack3, pack3]
  have hmod_m : (nm * (n2 * s.l1 + s.l2) + s.m) % nm = s.m := by
    rw [Nat.mul_add_mod, Nat.mod_eq_of_lt hm]
  have hdiv_m : (nm * (n2 * s.l1 + s.l2) + s.m) / nm = n2 * s.l1 + s.l2 := by
    rw [Nat.mul_add_div hnm, Nat.div_eq_of_lt hm, Nat.add_zero]
  rw [hmod_m, hdiv_m]
  have hmod_2 : (n2 * s.l1 + s.l2) % n2 = s.l2 := by
    rw [Nat.mul_add_mod, Nat.mod_eq_of_lt h2]
  have hdiv_2 : (n2 * s.l1 + s.l2) / n2 = s.l1 := by
    rw [Nat.mul_add_div hn2, Nat.div_eq_of_lt h2, Nat.add_zero]
  rw [hmod_2, hdiv_2]

/-- Packed state is bounded by the product of capacities. -/
theorem pack3_lt {n1 n2 nm : Nat} (s : State3)
    (h1 : s.l1 < n1) (h2 : s.l2 < n2) (hm : s.m < nm) :
    pack3 n2 nm s < n1 * n2 * nm := by
  dsimp [pack3]
  have h1_le : n2 * (s.l1 + 1) ≤ n2 * n1 := Nat.mul_le_mul_left n2 h1
  have h1_exp : n2 * (s.l1 + 1) = n2 * s.l1 + n2 := Nat.mul_succ n2 s.l1
  have h_inner : n2 * s.l1 + s.l2 < n2 * n1 := by omega
  have h2_le : nm * (n2 * s.l1 + s.l2 + 1) ≤ nm * (n2 * n1) := Nat.mul_le_mul_left nm h_inner
  have h2_exp : nm * (n2 * s.l1 + s.l2 + 1) = nm * (n2 * s.l1 + s.l2) + nm := Nat.mul_succ nm (n2 * s.l1 + s.l2)
  have h_outer : nm * (n2 * s.l1 + s.l2) + s.m < nm * (n2 * n1) := by omega
  have h_eq : nm * (n2 * n1) = n1 * n2 * nm := by
    rw [Nat.mul_comm n2 n1, Nat.mul_comm nm (n1 * n2)]
  exact h_eq ▸ h_outer

end Concurrency
