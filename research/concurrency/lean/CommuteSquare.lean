import Carrier
import Footprint

/-!
# Commuting Squares & Operational Interference

Proves:
1. Operational Independence Theorem: Two operations with disjoint access
   footprints commute on state outcomes (S1 ∘ S2 = S2 ∘ S1).
2. Non-Commuting Failing Squares: Operations with overlapping/conflicting
   access footprints fail to commute.

AuthorityEffect: None.
-/

namespace Concurrency

/-- Commutation of two state operations on state outcomes. -/
def Commutes (S1 S2 : State3 → State3) : Prop :=
  ∀ s, S1 (S2 s) = S2 (S1 s)

/-- An operation step preserves all coordinates read by another disjoint operation. -/
theorem agrees_on_reads_step (f1 f2 : Footprint) (hdisj : isDisjoint f1 f2 = true)
    (S2 : State3 → State3) (hS2 : Respects f2 S2) (s : State3) :
    AgreesOnReads f1 (S2 s) s := by
  refine ⟨?_, ?_, ?_⟩
  · intro hr1
    have hw1 : f2.w1 = false := not_w1_of_r1_disjoint hdisj hr1
    exact hS2.preserves.1 hw1 s
  · intro hr2
    have hw2 : f2.w2 = false := not_w2_of_r2_disjoint hdisj hr2
    exact hS2.preserves.2.1 hw2 s
  · intro hrm
    have hwm : f2.wm = false := not_wm_of_rm_disjoint hdisj hrm
    exact hS2.preserves.2.2 hwm s

/-- Disjoint operations commute on the L1 coordinate. -/
theorem disjoint_comm_l1 (f1 f2 : Footprint) (hdisj : isDisjoint f1 f2 = true)
    (S1 S2 : State3 → State3) (hS1 : Respects f1 S1) (hS2 : Respects f2 S2) (s : State3) :
    (S1 (S2 s)).l1 = (S2 (S1 s)).l1 := by
  have hdisj2 : isDisjoint f2 f1 = true := by rw [isDisjoint_symm]; exact hdisj
  have hAgr1 := agrees_on_reads_step f1 f2 hdisj S2 hS2 s
  have hAgr2 := agrees_on_reads_step f2 f1 hdisj2 S1 hS1 s
  cases hw1 : f1.w1 <;> cases hw2 : f2.w1
  · -- f1.w1 = false, f2.w1 = false
    have h1 : (S1 (S2 s)).l1 = (S2 s).l1 := hS1.preserves.1 hw1 (S2 s)
    have h2 : (S2 s).l1 = s.l1 := hS2.preserves.1 hw2 s
    have h3 : (S2 (S1 s)).l1 = (S1 s).l1 := hS2.preserves.1 hw2 (S1 s)
    have h4 : (S1 s).l1 = s.l1 := hS1.preserves.1 hw1 s
    rw [h1, h2, h3, h4]
  · -- f1.w1 = false, f2.w1 = true
    have h1 : (S1 (S2 s)).l1 = (S2 s).l1 := hS1.preserves.1 hw1 (S2 s)
    have h3 : (S2 (S1 s)).l1 = (S2 s).l1 := (hS2.readsOnly (S1 s) s hAgr2).1 hw2
    rw [h1, h3]
  · -- f1.w1 = true, f2.w1 = false
    have h1 : (S1 (S2 s)).l1 = (S1 s).l1 := (hS1.readsOnly (S2 s) s hAgr1).1 hw1
    have h3 : (S2 (S1 s)).l1 = (S1 s).l1 := hS2.preserves.1 hw2 (S1 s)
    rw [h1, h3]
  · -- f1.w1 = true, f2.w1 = true (impossible under disjointness)
    exact False.elim (not_both_w1_disjoint hdisj hw1 hw2)

/-- Disjoint operations commute on the L2 coordinate. -/
theorem disjoint_comm_l2 (f1 f2 : Footprint) (hdisj : isDisjoint f1 f2 = true)
    (S1 S2 : State3 → State3) (hS1 : Respects f1 S1) (hS2 : Respects f2 S2) (s : State3) :
    (S1 (S2 s)).l2 = (S2 (S1 s)).l2 := by
  have hdisj2 : isDisjoint f2 f1 = true := by rw [isDisjoint_symm]; exact hdisj
  have hAgr1 := agrees_on_reads_step f1 f2 hdisj S2 hS2 s
  have hAgr2 := agrees_on_reads_step f2 f1 hdisj2 S1 hS1 s
  cases hw1 : f1.w2 <;> cases hw2 : f2.w2
  · have h1 : (S1 (S2 s)).l2 = (S2 s).l2 := hS1.preserves.2.1 hw1 (S2 s)
    have h2 : (S2 s).l2 = s.l2 := hS2.preserves.2.1 hw2 s
    have h3 : (S2 (S1 s)).l2 = (S1 s).l2 := hS2.preserves.2.1 hw2 (S1 s)
    have h4 : (S1 s).l2 = s.l2 := hS1.preserves.2.1 hw1 s
    rw [h1, h2, h3, h4]
  · have h1 : (S1 (S2 s)).l2 = (S2 s).l2 := hS1.preserves.2.1 hw1 (S2 s)
    have h3 : (S2 (S1 s)).l2 = (S2 s).l2 := (hS2.readsOnly (S1 s) s hAgr2).2.1 hw2
    rw [h1, h3]
  · have h1 : (S1 (S2 s)).l2 = (S1 s).l2 := (hS1.readsOnly (S2 s) s hAgr1).2.1 hw1
    have h3 : (S2 (S1 s)).l2 = (S1 s).l2 := hS2.preserves.2.1 hw2 (S1 s)
    rw [h1, h3]
  · exact False.elim (not_both_w2_disjoint hdisj hw1 hw2)

/-- Disjoint operations commute on the Message Locus M. -/
theorem disjoint_comm_m (f1 f2 : Footprint) (hdisj : isDisjoint f1 f2 = true)
    (S1 S2 : State3 → State3) (hS1 : Respects f1 S1) (hS2 : Respects f2 S2) (s : State3) :
    (S1 (S2 s)).m = (S2 (S1 s)).m := by
  have hdisj2 : isDisjoint f2 f1 = true := by rw [isDisjoint_symm]; exact hdisj
  have hAgr1 := agrees_on_reads_step f1 f2 hdisj S2 hS2 s
  have hAgr2 := agrees_on_reads_step f2 f1 hdisj2 S1 hS1 s
  cases hw1 : f1.wm <;> cases hw2 : f2.wm
  · have h1 : (S1 (S2 s)).m = (S2 s).m := hS1.preserves.2.2 hw1 (S2 s)
    have h2 : (S2 s).m = s.m := hS2.preserves.2.2 hw2 s
    have h3 : (S2 (S1 s)).m = (S1 s).m := hS2.preserves.2.2 hw2 (S1 s)
    have h4 : (S1 s).m = s.m := hS1.preserves.2.2 hw1 s
    rw [h1, h2, h3, h4]
  · have h1 : (S1 (S2 s)).m = (S2 s).m := hS1.preserves.2.2 hw1 (S2 s)
    have h3 : (S2 (S1 s)).m = (S2 s).m := (hS2.readsOnly (S1 s) s hAgr2).2.2 hw2
    rw [h1, h3]
  · have h1 : (S1 (S2 s)).m = (S1 s).m := (hS1.readsOnly (S2 s) s hAgr1).2.2 hw1
    have h3 : (S2 (S1 s)).m = (S1 s).m := hS2.preserves.2.2 hw2 (S1 s)
    rw [h1, h3]
  · exact False.elim (not_both_wm_disjoint hdisj hw1 hw2)

/-- **The Operational Independence Theorem.**
    Two operations with disjoint footprints commute on all states. -/
theorem disjoint_commutes (f1 f2 : Footprint) (hdisj : isDisjoint f1 f2 = true)
    (S1 S2 : State3 → State3) (hS1 : Respects f1 S1) (hS2 : Respects f2 S2) :
    Commutes S1 S2 := by
  intro s
  apply State3.ext
  · exact disjoint_comm_l1 f1 f2 hdisj S1 S2 hS1 hS2 s
  · exact disjoint_comm_l2 f1 f2 hdisj S1 S2 hS1 hS2 s
  · exact disjoint_comm_m f1 f2 hdisj S1 S2 hS1 hS2 s

/-- Coordinate updates on L1 and L2 commute. -/
theorem updateL1_updateL2_commutes (f g : Nat → Nat) :
    Commutes (updateL1 f) (updateL2 g) :=
  disjoint_commutes (fpL1 true true) (fpL2 true true) (fpL1_fpL2_disjoint true true true true)
    (updateL1 f) (updateL2 g) (updateL1_respects f) (updateL2_respects g)

/-- Coordinate updates on L1 and M commute. -/
theorem updateL1_updateM_commutes (f h : Nat → Nat) :
    Commutes (updateL1 f) (updateM h) :=
  disjoint_commutes (fpL1 true true) (fpM true true) (fpL1_fpM_disjoint true true true true)
    (updateL1 f) (updateM h) (updateL1_respects f) (updateM_respects h)

/-- Coordinate updates on L2 and M commute. -/
theorem updateL2_updateM_commutes (g h : Nat → Nat) :
    Commutes (updateL2 g) (updateM h) :=
  disjoint_commutes (fpL2 true true) (fpM true true) (fpL2_fpM_disjoint true true true true)
    (updateL2 g) (updateM h) (updateL2_respects g) (updateM_respects h)

/-- Operation A: write 1 to L1. -/
def opWrite1 (s : State3) : State3 := { s with l1 := 1 }

/-- Operation B: write 2 to L1. -/
def opWrite2 (s : State3) : State3 := { s with l1 := 2 }

/-- **Write-Write Conflict Fails Commuting Square.** -/
theorem write_write_conflict_fails_commute :
    ¬ Commutes opWrite1 opWrite2 := by
  intro h
  have heq : opWrite1 (opWrite2 { l1 := 0, l2 := 0, m := 0 }) =
             opWrite2 (opWrite1 { l1 := 0, l2 := 0, m := 0 }) := h _
  have hcontra : (opWrite1 (opWrite2 { l1 := 0, l2 := 0, m := 0 })).l1 =
                 (opWrite2 (opWrite1 { l1 := 0, l2 := 0, m := 0 })).l1 := by rw [heq]
  revert hcontra
  decide

/-- Operation reading M to update L1. -/
def opReadMWriteL1 (s : State3) : State3 := { s with l1 := s.m }

/-- Operation modifying M. -/
def opIncM (s : State3) : State3 := { s with m := s.m + 1 }

/-- **Read-Write Conflict Fails Commuting Square.** -/
theorem read_write_conflict_fails_commute :
    ¬ Commutes opReadMWriteL1 opIncM := by
  intro h
  have heq : opReadMWriteL1 (opIncM { l1 := 0, l2 := 0, m := 0 }) =
             opIncM (opReadMWriteL1 { l1 := 0, l2 := 0, m := 0 }) := h _
  have hcontra : (opReadMWriteL1 (opIncM { l1 := 0, l2 := 0, m := 0 })).l1 =
                 (opIncM (opReadMWriteL1 { l1 := 0, l2 := 0, m := 0 })).l1 := by rw [heq]
  revert hcontra
  decide

end Concurrency
