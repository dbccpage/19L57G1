import Derivation

namespace G010

/-!
# G010 Computational Capabilities and Profiles

Formal constructive definitions of computational capabilities subject to genuine
semantic removal, and the shared PublicObservation interface invariant across systems.

AuthorityEffect: None.
-/

/-- Primitive computational capabilities subject to genuine semantic removal. -/
inductive Capability where
  | branching : Capability
  | memoryRetention : Capability
  | addressAllocation : Capability
  deriving DecidableEq, Repr

/-- Constructive capability membership in an active profile. -/
def CapProfile := Capability → Bool

def fullProfile : CapProfile := fun _ => true

def removeCap (c : Capability) (p : CapProfile) : CapProfile :=
  fun c' => if c' == c then false else p c'

def withoutBranch : CapProfile := removeCap Capability.branching fullProfile
def withoutMemory : CapProfile := removeCap Capability.memoryRetention fullProfile
def withoutAlloc : CapProfile := removeCap Capability.addressAllocation fullProfile

theorem removeCap_self (c : Capability) (p : CapProfile) :
    removeCap c p c = false := by
  dsimp [removeCap]
  simp

theorem removeCap_other (c c' : Capability) (p : CapProfile) (h : c' ≠ c) :
    removeCap c p c' = p c' := by
  dsimp [removeCap]
  have h_ne : (c' == c) = false := by
    cases c <;> cases c' <;> try rfl
    all_goals contradiction
  simp [h_ne]

/-- Public observation interface shared across all execution systems. -/
structure PublicObservation where
  outputTape : List Nat
  steps : Nat
  halted : Bool
  deriving DecidableEq, Repr

end G010
