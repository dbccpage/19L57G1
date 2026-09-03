/-!
# The represented state, reconstructed verbatim

PIN NOTE.  Every declaration in this file is reproduced VERBATIM from
`lean4/Derivation/Represented.lean` at blob
`4c395d6d4d6ceac5f5b75ecd79ec12bc936e87de` (snapshot
`f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be` of `main`, pinned in
`SOURCE_MANIFEST.json`).  The only change is the outer namespace, so this
package stays self-contained and imports nothing sealed.
`verify_pins.py` checks the projection against the pinned source and fails
on any drift.

Why only this slice: the standing-commitment rung needs the represented
state and its decidable observation semantics, and nothing else of the
sealed module.  The repair, augmentation, and gate machinery is NOT
reconstructed, because this rung asks where demands COME FROM, not how
they are discharged.  AuthorityEffect: None.
-/

namespace StandingCommitment

abbrev View := List Nat

abbrev Req := Nat × Nat

/-! ## Reconstructed: the represented state and its observation semantics -/

/-- The represented state.  Every load-bearing input lives here:
`budget` is the fuel, `augLicensed` the structure-creation
authorization, `refusals` the represented unresolved obstructions,
`notes` a represented but transition-inert commentary field (used by
the support theorem). -/
structure World where
  data : List Nat
  views : List View
  reqs : List Req
  refusals : List Req
  budget : Nat
  augLicensed : Bool
  notes : List Nat
deriving Repr, DecidableEq

def genesis : World := ⟨[], [], [], [], 0, true, []⟩

/-! ## Observation semantics (decidable throughout) -/

def sepB (c : View) (i j : Nat) : Bool :=
  (decide (i ∈ c)) != (decide (j ∈ c))

def satB (w : World) (r : Req) : Bool :=
  w.views.any (fun c => sepB c r.1 r.2)

def violB (w : World) (r : Req) : Bool :=
  (decide (r ∈ w.reqs)) && !satB w r

def quiescentB (w : World) : Bool :=
  w.reqs.all (fun r => satB w r)

end StandingCommitment
