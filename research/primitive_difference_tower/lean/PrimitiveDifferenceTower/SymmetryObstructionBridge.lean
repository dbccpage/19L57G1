import PrimitiveDifferenceTower

namespace SymmetryObstructionBridge

/-
This is a two-coordinate finite fixture for the bridge program.  The pair,
its swap, and the diagonal repair map are definitions local to this file.
They do not identify the fixture with a source-interface predicate or provide
an unbounded selection result.
-/

abbrev Cochain : Type := Bool × Bool

def swap : Cochain → Cochain
  | (left, right) => (right, left)

def boundary (potential : Bool) : Cochain := (potential, potential)

def residual : Cochain := (true, false)

def InResidualOrbit (cochain : Cochain) : Prop :=
  cochain = residual ∨ cochain = swap residual

theorem swap_involutive (cochain : Cochain) : swap (swap cochain) = cochain := by
  cases cochain
  rfl

theorem residual_orbit_has_no_fixed_singleton (cochain : Cochain)
    (member : InResidualOrbit cochain) : swap cochain ≠ cochain := by
  rcases member with rfl | rfl <;> decide

theorem residual_not_in_declared_boundary_image :
    ¬ ∃ potential : Bool, boundary potential = residual := by
  rintro ⟨potential, equality⟩
  cases potential <;> cases equality

/- An anchor is an additional datum.  The definition below exposes it rather
than deriving a singleton from the swap action. -/
structure AnchorImport where
  selected : Cochain
  member : InResidualOrbit selected

def anchoredChoice (anchor : AnchorImport) : Cochain := anchor.selected

theorem anchoredChoice_retains_import (anchor : AnchorImport) :
    anchoredChoice anchor = anchor.selected := rfl

/- This is the complete continuation grammar for this finite fixture only. -/
inductive Continuation where
  | anchored (anchor : AnchorImport)
  | retainOrbit
  | refuse

def singletonChoice? : Continuation → Option Cochain
  | .anchored anchor => some anchor.selected
  | .retainOrbit => none
  | .refuse => none

theorem continuation_cases (continuation : Continuation) :
    (∃ anchor, continuation = .anchored anchor) ∨
      continuation = .retainOrbit ∨ continuation = .refuse := by
  cases continuation with
  | anchored anchor => exact Or.inl ⟨anchor, rfl⟩
  | retainOrbit => exact Or.inr (Or.inl rfl)
  | refuse => exact Or.inr (Or.inr rfl)

theorem nonanchored_continuations_have_no_singleton (continuation : Continuation)
    (notAnchored : continuation = .retainOrbit ∨ continuation = .refuse) :
    singletonChoice? continuation = none := by
  rcases notAnchored with rfl | rfl <;> rfl

end SymmetryObstructionBridge
