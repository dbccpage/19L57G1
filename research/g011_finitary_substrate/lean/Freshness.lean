import Ordinal
import Address

/-!
# Endogenous Deterministic Freshness Allocator

Deterministic generation of fresh disjoint tree addresses from an admitted registry
without reliance on host memory addresses, object ids, or randomness oracles.

AuthorityEffect: None.
Axiom boundary: strictly within {propext, Quot.sound}, zero Classical.choice, zero mathlib.
-/

namespace FinitarySubstrate

namespace Freshness

open Address

/-! ## 1. Branch Extraction and Metrics -/

/-- Extracts the top-level branch ordinal under root, if any. -/
def rootBranchIndex : Address → Option Ordinal
  | .root => none
  | .child .root o => some o
  | .child p _ => rootBranchIndex p

theorem rootBranchIndex_root : rootBranchIndex Address.root = none := rfl

theorem rootBranchIndex_child_root (o : Ordinal) :
    rootBranchIndex (Address.child Address.root o) = some o := rfl

/-- Compute the maximum branch ordinal occurring among allocated addresses. -/
def maxBranchIndex : List Address → Ordinal
  | [] => .zero
  | a :: rest =>
      match rootBranchIndex a with
      | none => maxBranchIndex rest
      | some o => Ordinal.max o (maxBranchIndex rest)

/-- Whether the list contains any address branching from root. -/
def hasBranch : List Address → Bool
  | [] => false
  | a :: rest =>
      match rootBranchIndex a with
      | some _ => true
      | none => hasBranch rest

/-- The deterministic fresh ordinal index strictly exceeding all allocated branch indices. -/
def freshIndex (L : List Address) : Ordinal :=
  bif hasBranch L then Ordinal.succ (maxBranchIndex L) else .zero

/-- The deterministic fresh address under root. -/
def freshAddress (L : List Address) : Address :=
  Address.child Address.root (freshIndex L)

/-! ## 2. Address Registry -/

structure AddressRegistry where
  allocated : List Address
  count : Ordinal
  deriving DecidableEq, Repr

def emptyRegistry : AddressRegistry :=
  ⟨[], .zero⟩

/-- Deterministic stateful allocator: appends fresh address and updates registry. -/
def allocate (reg : AddressRegistry) : AddressRegistry × Address :=
  let fresh := freshAddress reg.allocated
  (⟨fresh :: reg.allocated, Ordinal.succ reg.count⟩, fresh)

/-! ## 3. Soundness and Freshness Theorems -/

theorem maxBranchIndex_ge : ∀ {a : Address} {L : List Address} {o : Ordinal},
    a ∈ L → rootBranchIndex a = some o → Ordinal.le o (maxBranchIndex L) = true
  | _, [], _, hmem, _ => by cases hmem
  | a, head :: rest, o, hmem, hbr => by
      cases List.mem_cons.mp hmem with
      | inl heq =>
          rw [heq] at hbr
          dsimp [maxBranchIndex]
          rw [hbr]
          exact Ordinal.le_max_left o (maxBranchIndex rest)
      | inr hrest =>
          have ih := maxBranchIndex_ge hrest hbr
          dsimp [maxBranchIndex]
          cases rootBranchIndex head with
          | none =>
              exact ih
          | some o' =>
              exact Ordinal.le_trans ih (Ordinal.le_max_right o' (maxBranchIndex rest))

theorem hasBranch_of_mem : ∀ {a : Address} {L : List Address} {o : Ordinal},
    a ∈ L → rootBranchIndex a = some o → hasBranch L = true
  | _, [], _, hmem, _ => by cases hmem
  | a, head :: rest, o, hmem, hbr => by
      cases List.mem_cons.mp hmem with
      | inl heq =>
          rw [heq] at hbr
          dsimp [hasBranch]
          rw [hbr]
      | inr hrest =>
          have ih := hasBranch_of_mem hrest hbr
          dsimp [hasBranch]
          cases rootBranchIndex head with
          | some _ => rfl
          | none => exact ih

theorem freshIndex_gt : ∀ {a : Address} {L : List Address} {o : Ordinal},
    a ∈ L → rootBranchIndex a = some o → Ordinal.lt o (freshIndex L) = true := by
  intro a L o hmem hbr
  have h_has : hasBranch L = true := hasBranch_of_mem hmem hbr
  have h_le : Ordinal.le o (maxBranchIndex L) = true := maxBranchIndex_ge hmem hbr
  dsimp [freshIndex]
  rw [h_has]
  exact h_le

theorem freshAddress_ne : ∀ {L : List Address} {a : Address},
    a ∈ L → freshAddress L ≠ a := by
  intro L a hmem heq
  have h_addr_eq : a = Address.child Address.root (freshIndex L) := heq.symm
  have hbr : rootBranchIndex a = some (freshIndex L) := by
    rw [h_addr_eq]
    rfl
  have hgt := freshIndex_gt hmem hbr
  have hir := Ordinal.lt_irrefl (freshIndex L)
  rw [hir] at hgt
  contradiction

theorem freshAddress_not_mem (L : List Address) : freshAddress L ∉ L := by
  intro hmem
  exact freshAddress_ne hmem rfl

theorem allocate_fresh (reg : AddressRegistry) :
    (allocate reg).2 ∉ reg.allocated :=
  freshAddress_not_mem reg.allocated

theorem allocate_allocated (reg : AddressRegistry) :
    (allocate reg).1.allocated = (allocate reg).2 :: reg.allocated := rfl

theorem allocate_count (reg : AddressRegistry) :
    (allocate reg).1.count = Ordinal.succ reg.count := rfl

end Freshness

end FinitarySubstrate
